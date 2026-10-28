#!/usr/bin/env python3
"""Clip QA gate: every vertical clip gets this before it goes to Nick or Post Bridge.

    python3 tools/clip-qa.py clip.mp4 [more.mp4 ...] [--sheet DIR] [--json out.json]
                             [--style box|pop] [--model yunet.onnx]

Why it exists: the clip spec in CLAUDE.md was fixed one defect at a time by different
sessions, and each fix broke something the previous one had fixed. Captions sat at the
bottom edge (MarginV 12) and got cut off on Instagram; fit-captions.py then shrank the
picture over a blur; the refit that replaced it cropped and zoomed until heads were cut
off. Every one of those passed "it encoded" and failed Nick's eye. This script checks
the whole spec at once, on the actual file, so a fix for one rule cannot quietly break
another. Exit code 1 if any clip FAILs; WARNs are printed but do not block.

Checks, per clip:
  format    1080x1920, h264, yuv420p, 30 fps, AAC audio, moov atom before mdat (faststart),
            under 3 minutes (YouTube Shorts eligibility is decided by the file).
  loudness  integrated -14 LUFS for social (FAIL outside -20..-10, WARN outside -16..-12).
  fill      the picture fills the frame: no black bars, no inset picture over a blurred copy
            of itself (the retired fit-captions.py look).
  captions  --style box (default, the house style): a solid black box with white text,
            present through the clip, one line tall, entirely inside y 285..1610 (Instagram's
            4:5 feed crop keeps 285..1635; Reels/TikTok/Shorts cover the bottom ~420 px).
            --style pop: the tools/sizzle word-pop captions; only presence is not checked.
            --style none: no caption checks at all (a one-off post with no burned-in text).
  framing   YuNet face per frame at 2 fps: the subject (or a two-shot pair) within 10% of
            centre, the top of the head not cut off, no long stretch with no clear subject.

--sheet DIR writes <clip>.jpg: six frames with the 4:5 crop (yellow) and the Reels
overlay line (red) drawn on, plus the frames that failed framing. Look at it.
"""
import json
import os
import struct
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
SAFE_TOP, SAFE_BOTTOM = 285, 1610       # 4:5 feed crop keeps 285..1635; Nick set the box at ~1590 (2026-10-28)
FEED_BOTTOM = 1635                      # 4:5 feed crop bottom
MODEL_PATHS = [os.path.join(HERE, "..", "models", "yunet.onnx"),
               os.path.join(os.environ.get("SIZZLE_WORK", os.path.expanduser("~/sizzle-work")), "models", "yunet.onnx")]
YUNET_URL = ("https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/"
             "face_detection_yunet/face_detection_yunet_2023mar.onnx")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    p = run(["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_type,codec_name,width,height,pix_fmt,r_frame_rate,sample_rate:format=duration",
             "-of", "json", path])
    return json.loads(p.stdout)


def faststart(path):
    """True when the moov atom comes before mdat, so a phone can start playback while downloading."""
    with open(path, "rb") as f:
        while True:
            hdr = f.read(8)
            if len(hdr) < 8:
                return False
            size, kind = struct.unpack(">I4s", hdr)
            if kind == b"moov":
                return True
            if kind == b"mdat":
                return False
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0] - 8
            f.seek(size - 8, 1)


def loudness(path):
    p = run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"])
    I = tp = None
    for line in p.stderr.splitlines()[-20:]:
        line = line.strip()
        if line.startswith("I:"):
            I = float(line.split()[1])
        if line.startswith("Peak:"):
            tp = float(line.split()[1])
    return I, tp


def frames(path, fps):
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={W}:{H}",
                             "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    n = W * H * 3
    i = 0
    while True:
        buf = proc.stdout.read(n)
        if len(buf) < n:
            break
        yield i / fps, np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        i += 1


CAP_LO = 700                       # captions are looked for below this row
CAP_X0, CAP_X1 = 470, 610          # centre strip: even a one word caption covers it


def caption_rows(gray):
    """Per row from CAP_LO down: does the centre strip look like caption text on the house
    box (mostly solid black, some white glyph pixels, few mid greys)? Judged per row and
    then summed over the whole clip in caption_bands(), because any single frame is easy to
    fool (a black shirt, a white wall, a shirt logo beside the caption) but only a burned in
    caption puts text-on-black in the same rows frame after frame."""
    s = gray[CAP_LO:, CAP_X0:CAP_X1]
    white = (s > 200).mean(axis=1)
    black = (s < 25).mean(axis=1)
    midg = 1 - white - black
    return (white >= 0.04) & (black >= 0.45) & (midg <= 0.25)


def caption_bands(rows):
    """rows: frames x rows booleans. Returns [(top, bottom, share of frames)] for each band
    of rows that reads as caption text in at least 15% of frames, plus per-frame coverage."""
    prof = rows.mean(axis=0)
    hot = np.where(prof >= 0.15)[0]
    bands = []
    if len(hot):
        for g in np.split(hot, np.where(np.diff(hot) > 6)[0] + 1):
            if g[-1] - g[0] >= 15:
                bands.append((int(g[0] + CAP_LO), int(g[-1] + CAP_LO), float(prof[g].max())))
    cover = 0.0
    if bands:
        t, b, _ = max(bands, key=lambda x: x[2])
        r = rows[:, t - CAP_LO:b - CAP_LO + 1]
        cover = float((r.mean(axis=1) >= 0.3).mean())
    return bands, cover


def inset_score(acc_cols, acc_rows):
    """A picture shrunk over a blurred copy of itself leaves a hard vertical edge at the same
    x in every frame. Returns the strongest persistent column edge relative to the median."""
    c = acc_cols[20:-20]
    r = acc_rows[20:-20]
    return float(c.max() / (np.median(c) + 1e-6)), float(r.max() / (np.median(r) + 1e-6))


def load_detector(model):
    import cv2
    for p in ([model] if model else []) + MODEL_PATHS:
        if p and os.path.exists(p) and os.path.getsize(p) > 100000:
            return cv2.FaceDetectorYN.create(p, "", (270, 480), 0.7)
    sys.exit(f"YuNet model not found. Put it at models/yunet.onnx (gitignored):\n  curl -sSL -o models/yunet.onnx {YUNET_URL}")


def check(path, style="box", sheet=None, det=None):
    import cv2
    name = os.path.basename(path)
    fails, warns = [], []
    info = probe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    if not v:
        return {"clip": name, "fails": ["no video stream"], "warns": []}
    if (v["width"], v["height"]) != (W, H):
        fails.append(f"size {v['width']}x{v['height']}, want 1080x1920")
    if v["codec_name"] != "h264":
        fails.append(f"video codec {v['codec_name']}, want h264 (X rejects HEVC)")
    if v.get("pix_fmt") != "yuv420p":
        fails.append(f"pix_fmt {v.get('pix_fmt')}, want yuv420p")
    num, den = map(int, v["r_frame_rate"].split("/"))
    if abs(num / den - 30) > 0.05:
        fails.append(f"{num / den:.2f} fps, want 30")
    if not a:
        fails.append("no audio")
    else:
        if a["codec_name"] != "aac":
            fails.append(f"audio codec {a['codec_name']}, want aac")
        if a.get("sample_rate") != "48000":
            warns.append(f"audio {a.get('sample_rate')} Hz, want 48000")
    if not faststart(path):
        fails.append("moov atom after mdat (encode with -movflags +faststart)")
    if dur >= 180:
        fails.append(f"{dur:.0f}s long: 3 minutes or more is not a YouTube Short")
    elif dur > 75:
        warns.append(f"{dur:.0f}s long; clips have run 20 to 75 s, 15 to 25 s reaches furthest")
    if a:
        I, tp = loudness(path)
        if I is None:
            warns.append("could not measure loudness")
        elif not -20 <= I <= -10:
            fails.append(f"loudness {I:.1f} LUFS, want -14")
        elif not -16 <= I <= -12:
            warns.append(f"loudness {I:.1f} LUFS, want -14")
        if tp is not None and tp > -0.5:
            warns.append(f"true peak {tp:.1f} dBFS, clipping risk")

    fps = 2
    caps, faces, picks = [], [], []
    acc_cols = np.zeros(W)
    acc_rows = np.zeros(H)
    edges_n = 0
    dark_bars = 0
    nfr = 0
    want = {round(dur * (i + 0.5) / 6 * fps) / fps for i in range(6)}
    for t, fr in frames(path, fps):
        nfr += 1
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        caps.append(caption_rows(g))
        # persistent hard edges (inset picture), measured above the caption zone
        gf = g[:1250].astype(np.float32)
        acc_cols += np.abs(np.diff(gf, axis=1)).mean(axis=0).tolist() + [0]
        gr = g[:, 150:-150].astype(np.float32)
        acc_rows += np.abs(np.diff(gr, axis=0)).mean(axis=1).tolist() + [0]
        edges_n += 1
        if min(g[:, :24].mean(), g[:, -24:].mean()) < 6 or min(g[:24].mean(), g[-24:].mean()) < 6:
            dark_bars += 1
        small = cv2.resize(fr, (270, 480), interpolation=cv2.INTER_AREA)
        _, fs = det.detect(small)
        fs = sorted(fs, key=lambda f: -f[2] * f[3]) if fs is not None else []
        fs = [f for f in fs if f[2] >= 0.06 * 270]
        faces.append((t, fs))
        if t in want:
            picks.append((t, fr.copy()))

    # fill
    if dark_bars > 0.5 * nfr:
        fails.append(f"black bars at the frame edge in {dark_bars}/{nfr} frames: the picture must fill 9:16")
    cs, rs = inset_score(acc_cols / max(edges_n, 1), acc_rows / max(edges_n, 1))
    if cs > 6:
        fails.append(f"a hard vertical edge sits at the same x in every frame (score {cs:.1f}): "
                     "inset picture over a blur? Every clip fills the frame")

    # captions
    if style == "box":
        bands, cover = caption_bands(np.array(caps))
        if not bands or cover < 0.5:
            fails.append(f"house captions (white on a solid black box) on screen in only {cover:.0%} of frames: missing, or another style")
        for top, bot, share in bands:
            pad_bot = bot + 12                         # the box pads the text by ~12 px
            if pad_bot > SAFE_BOTTOM:
                where = "cut off by Instagram's 4:5 crop" if pad_bot > FEED_BOTTOM else "under the Reels/TikTok/Shorts buttons and caption"
                fails.append(f"caption text at y {top}..{bot} ({share:.0%} of frames) is {where}; keep the box above {SAFE_BOTTOM} (MarginV=49, tools/clip_captions.py)")
            if top - 12 < SAFE_TOP:
                fails.append(f"caption text at y {top}..{bot} is above Instagram's 4:5 crop line {SAFE_TOP}")
            if bot - top > 95:
                fails.append(f"caption text {bot - top} px tall at y {top}: two lines; the house style is ONE line, at most three words")
        if len(bands) > 1:
            fails.append("two caption layers burned in: " + ", ".join(f"y {t}..{b} ({s:.0%})" for t, b, s in bands))
        elif bands and bands[0][1] < 1250:
            warns.append(f"captions sit high (text bottom y {bands[0][1]}); house style puts it at ~1590 (MarginV=49)")

    # framing
    def off_of(fs):
        big = fs[0]
        cx = big[0] + big[2] / 2
        off = (cx - 135) / 270
        if len(fs) > 1 and fs[1][2] * fs[1][3] > 0.3 * big[2] * big[3]:
            po = ((cx + fs[1][0] + fs[1][2] / 2) / 2 - 135) / 270
            off = min(off, po, key=abs)
        return off

    seen = [(t, fs) for t, fs in faces if fs]
    offc = [(t, off_of(fs)) for t, fs in seen if abs(off_of(fs)) > 0.10]
    headcut = [t for t, fs in seen if fs[0][1] < 0.012 * 480]
    def runs(ts, gap=0.6):
        out = []
        for t in ts:
            if out and t - out[-1][1] <= gap:
                out[-1][1] = t
            else:
                out.append([t, t])
        return out
    bad_off = [r for r in runs([t for t, _ in offc]) if r[1] - r[0] >= 1.0]
    if bad_off:
        fails.append("subject off centre at " + ", ".join(f"{a:.1f}-{b:.1f}s" for a, b in bad_off))
    if seen and len(headcut) > 0.4 * len(seen):
        fails.append(f"top of the head cut off in {len(headcut)}/{len(seen)} face frames: over-zoomed or framed too high")
    elif headcut:
        warns.append(f"top of the head touches the frame edge in {len(headcut)}/{len(seen)} face frames")
    noface = [r for r in runs([t for t, fs in faces if not fs]) if r[1] - r[0] >= 3.0]
    if noface:
        warns.append("no clear subject (no face 6%+ of the width) at " + ", ".join(f"{a:.1f}-{b:.1f}s" for a, b in noface))

    if sheet:
        os.makedirs(sheet, exist_ok=True)
        flag_t = {round(t * fps) / fps for t, _ in offc} | {round(t * fps) / fps for t in headcut}
        tiles = []
        for t, fr in picks:
            tiles.append(_tile(fr, t, t in flag_t))
        img = np.hstack(tiles) if tiles else np.zeros((480, 270, 3), np.uint8)
        cv2.imwrite(os.path.join(sheet, os.path.splitext(name)[0] + ".jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 85])

    stats = {}
    if seen:
        stats = {"face_top": round(float(np.median([fs[0][1] / 480 for _, fs in seen])), 3),
                 "face_w": round(float(np.median([fs[0][2] / 270 for _, fs in seen])), 3),
                 "face_frames": f"{len(seen)}/{nfr}"}
    return {"clip": name, "duration": round(dur, 1), "fails": fails, "warns": warns, **stats}


def _tile(fr, t, flagged):
    import cv2
    tw, th = 270, 480
    s = cv2.resize(fr, (tw, th), interpolation=cv2.INTER_AREA)
    for y, c in ((SAFE_TOP, (0, 220, 255)), (FEED_BOTTOM, (0, 220, 255)), (SAFE_BOTTOM, (0, 0, 255))):
        yy = int(y * th / H)
        cv2.line(s, (0, yy), (tw, yy), c, 1)
    cv2.putText(s, f"{t:.1f}s", (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    if flagged:
        cv2.rectangle(s, (0, 0), (tw - 1, th - 1), (0, 0, 255), 4)
    return s


def main():
    args, files = sys.argv[1:], []
    opts = {"--sheet": None, "--json": None, "--style": "box", "--model": None}
    i = 0
    while i < len(args):
        if args[i] in opts:
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            files.append(args[i])
            i += 1
    if not files:
        sys.exit(__doc__)
    det = load_detector(opts["--model"])
    results, bad = [], 0
    for f in files:
        r = check(f, opts["--style"], opts["--sheet"], det)
        results.append(r)
        status = "FAIL" if r["fails"] else "PASS"
        bad += bool(r["fails"])
        print(f"{status}  {r['clip']}")
        for m in r["fails"]:
            print(f"      FAIL  {m}")
        for m in r["warns"]:
            print(f"      warn  {m}")
    if opts["--json"]:
        json.dump(results, open(opts["--json"], "w"), indent=1)
    print(f"\n{len(files) - bad}/{len(files)} pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
