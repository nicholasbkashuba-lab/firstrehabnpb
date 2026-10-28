#!/usr/bin/env python3
"""Re-cut a finished vertical clip from the episode's RAW cameras, centred, at its original framing.

    python3 tools/recut-clip.py captioned.mp4 out.mp4 --mp3 raw.mp3 --orig-dir DIR \
        --cam NAME=src:rate:offset [--cam ...] [--work DIR]

  captioned.mp4  the clip as scheduled: its burned-in house caption box and its audio are
                 carried over untouched (the box is opaque, so its pixels ARE the caption)
  --orig-dir     the episode's first-generation clips (media/ep{NN}-clips/clips/*.mp4). The
                 one that covers this clip sets the framing Nick approved: same crop size
                 in the camera, so the same zoom, re-aimed on the face
  --cam          src is a local path or a URL (a Dropbox temporary link streams with range
                 reads; no 20 GB download). rate and offset come from tools/cam-sync.py

What it fixes (2026-10-28): 21 clips had been rebuilt by cropping the picture above old
burned-in captions and enlarging it 1.3x, because no clean render was kept. That cut heads
off at the top and softened the picture, and the narrower window could not reach a speaker
near the edge of the frame. Going back to the raw camera gives every shot the full original
picture again, from 4K where the camera shot 4K.

Per shot: find which camera and crop the first-generation clip used (multi-scale template
match, so a punch-in on a 4K two-shot is found as readily as a full-height crop of a 720p
phone), then re-cut that crop size with the window following the speaker's face (or the
pair, on a two-shot), with headroom kept above the head. iPhone HLG footage is tonemapped
through linear light (CLAUDE.md "iPhone HDR footage"). A shot that matches no camera is
copied from the captioned clip as is and reported. Run tools/clip-qa.py on the result.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("reframe", os.path.join(HERE, "reframe-clip.py"))
rf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rf)
W, H, FPS = rf.W, rf.H, rf.FPS
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
           "zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
TOP = 1250                                  # template rows: above any generation of burned-in captions


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def probe(src):
    p = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,color_transfer:stream_side_data=rotation", "-of", "json", src],
           capture_output=True, text=True)
    s = json.loads(p.stdout)["streams"][0]
    rot = 0
    for sd in s.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    w, h = s["width"], s["height"]
    if abs(rot) == 90:
        w, h = h, w
    return w, h, s.get("color_transfer") == "arib-std-b67"


class Cam:
    def __init__(self, name, src, rate, off):
        self.name, self.src, self.rate, self.off = name, src, rate, off
        self.w, self.h, self.hdr = probe(src)

    def t(self, mp3_t):
        return self.rate * mp3_t + self.off

    def frames(self, t0, n=1, fps=None, scale_h=None, crop=None):
        vf = []
        if fps:
            vf.append(f"fps={fps}")
        if crop:
            vf.append(crop)
        if self.hdr:
            vf.append(TONEMAP)
        if scale_h:
            vf.append(f"scale=-2:{scale_h}")
        vf.append("format=bgr24")
        p = sh(["ffmpeg", "-v", "error", "-ss", f"{max(t0, 0):.3f}", "-i", self.src, "-an", "-frames:v", str(n),
                "-vf", ",".join(vf), "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        import cv2
        out, b = [], p.stdout
        sig = b"\x89PNG\r\n\x1a\n"
        parts = [x for x in b.split(sig) if x]
        for x in parts:
            im = cv2.imdecode(np.frombuffer(sig + x, np.uint8), cv2.IMREAD_COLOR)
            if im is not None:
                out.append(im)
        return out


def match(orig_frame, cam, mp3_t):
    """Where the first-generation frame sits in this camera: (x, y, cw, ch, score) in camera px."""
    import cv2
    fr = cam.frames(cam.t(mp3_t))
    if not fr:
        return None
    full = cv2.cvtColor(fr[0], cv2.COLOR_BGR2GRAY)
    tm_full = cv2.cvtColor(orig_frame[:TOP], cv2.COLOR_BGR2GRAY)

    def score_at(ch, work_h):
        f = work_h / cam.h
        img = cv2.resize(full, (int(round(cam.w * f)), work_h), interpolation=cv2.INTER_AREA)
        sc = ch / H * f
        tw, th = int(round(W * sc)), int(round(TOP * sc))
        if tw < 12 or th < 12 or tw > img.shape[1] or th > img.shape[0]:
            return None
        tm = cv2.resize(tm_full, (tw, th), interpolation=cv2.INTER_AREA)
        res = cv2.matchTemplate(img, tm, cv2.TM_CCOEFF_NORMED)
        _, s, _, loc = cv2.minMaxLoc(res)
        return s, loc[0] / f, loc[1] / f

    best = None
    for ch in np.linspace(0.25 * cam.h, 1.0 * cam.h, 31):        # coarse, on a 360 px tall copy
        r = score_at(ch, 360)
        if r and (best is None or r[0] > best[0]):
            best = (r[0], ch)
    if best is None:
        return None
    lo, hi = best[1] * 0.95, min(best[1] * 1.05, cam.h)
    fine = None
    for ch in np.linspace(lo, hi, 15):                            # fine, on a 900 px tall copy
        r = score_at(ch, min(900, cam.h))
        if r and (fine is None or r[0] > fine[0]):
            fine = (r[0], ch, r[1], r[2])
    s, ch, x, y = fine
    ch = min(cam.h, int(round(ch / 2)) * 2)
    cw = int(round(ch * 9 / 16 / 2)) * 2
    return int(round(x)), int(round(y)), cw, ch, float(s)


def aim(cam, mp3_t0, nfr, x0, y0, cw, ch, det):
    """Per 0.5 s keyframe, the crop (x, y) that centres the subject: the face nearest the
    original crop's centre, or the midpoint of a two-shot pair when the original framed two
    people. Headroom: the top of the face box sits at least 12% of the crop height down."""
    import cv2
    t0 = cam.t(mp3_t0)
    band_y0 = max(0, y0 - ch // 4)
    band_h = min(cam.h - band_y0, ch + ch // 2)
    sc = 480 / band_h
    fr = cam.frames(t0, n=max(1, nfr // 15 + 1), fps=2, crop=f"crop={cam.w}:{band_h}:0:{band_y0}",
                    scale_h=480)
    keys = []
    tx, ty, pair = x0 + cw / 2, None, None
    for k, f in enumerate(fr):
        det.setInputSize((f.shape[1], f.shape[0]))
        _, faces = det.detect(f)
        faces = [] if faces is None else [
            ((x[0] + x[2] / 2) / sc, x[1] / sc + band_y0, x[2] / sc) for x in faces if x[2] / sc > 0.10 * cw]
        if k == 0:
            inside = [q for q in faces if x0 <= q[0] <= x0 + cw]
            big = [q for q in inside if q[2] > 0.6 * max((z[2] for z in inside), default=0)]
            pair = len(big) >= 2
        cx = None
        if faces:
            if pair:
                near = sorted(faces, key=lambda q: abs(q[0] - tx))[:2]
                if len(near) == 2 and abs(near[0][0] - near[1][0]) < 0.9 * cw:
                    cx = (near[0][0] + near[1][0]) / 2
                    top = min(near[0][1], near[1][1])
            if cx is None:
                q = min(faces, key=lambda q: abs(q[0] - tx))
                if abs(q[0] - tx) < 0.45 * cw or not keys:
                    cx, top = q[0], q[1]
        if cx is not None:
            tx = cx
            ty = top
        keys.append((k / 2, tx, ty))
    if not keys:
        keys = [(0, x0 + cw / 2, None)]
    ts = np.array([k[0] for k in keys])
    xs = np.array([k[1] for k in keys])
    sm = np.array([np.median(xs[max(0, j - 1):j + 2]) for j in range(len(xs))])
    out = [sm[0]]
    for v in sm[1:]:
        out.append(v if abs(v - out[-1]) > 0.06 * cw else out[-1])
    xs = np.clip(np.array(out) - cw / 2, 0, cam.w - cw)
    tops = [k[2] for k in keys if k[2] is not None]
    y = y0
    if tops:
        top = float(np.median(tops))
        want = top - 0.12 * ch                     # keep 12% of the frame above the head
        if want < y:
            y = want
        y = int(np.clip(y, 0, cam.h - ch))
    return ts, xs, y


def main():
    import cv2
    a = sys.argv[1:]
    src_clip, out = a[0], a[1]
    cams, mp3, orig_dir, work = [], None, None, None
    i = 2
    while i < len(a):
        if a[i] == "--cam":
            name, spec = a[i + 1].split("=", 1)
            path, rate, off = spec.rsplit(":", 2)
            cams.append(Cam(name, path, float(rate), float(off)))
        elif a[i] == "--mp3":
            mp3 = a[i + 1]
        elif a[i] == "--orig-dir":
            orig_dir = a[i + 1]
        elif a[i] == "--work":
            work = a[i + 1]
        i += 2
    work = work or tempfile.mkdtemp(prefix="recut-")
    os.makedirs(work, exist_ok=True)
    det = cv2.FaceDetectorYN.create(os.path.join(HERE, "..", "models", "yunet.onnx"), "", (270, 480), 0.6)
    name = os.path.basename(src_clip)

    ref = rf.pcm(mp3)
    ref = (ref - ref.mean()) / (ref.std() + 1e-9)
    nfft = 1 << int(np.ceil(np.log2(len(ref) + rf.SR * 12)))
    REF = np.fft.rfft(ref, nfft)

    def locate(path):
        x = rf.pcm(path)[: rf.SR * 12]
        x = (x - x.mean()) / (x.std() + 1e-9)
        r = np.fft.irfft(REF * np.conj(np.fft.rfft(x, nfft)), nfft)[: len(ref)]
        k = int(np.argmax(r))
        return k / rf.SR, float((r[k] - r.mean()) / (r.std() + 1e-9))

    s, psr = locate(src_clip)
    nfr = int(round(float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src_clip],
                             capture_output=True, text=True).stdout) * FPS))
    print(f"{name}: mp3 {s:.2f}s (psr {psr:.0f}), {nfr} frames")
    # the first-generation clip that covers it
    best = None
    for f in sorted(os.listdir(orig_dir)):
        if not f.endswith(".mp4"):
            continue
        so, po = locate(os.path.join(orig_dir, f))
        do = float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                       os.path.join(orig_dir, f)], capture_output=True, text=True).stdout)
        cover = min(so + do, s + nfr / FPS) - max(so, s)
        if po > 8 and (best is None or cover > best[0]):
            best = (cover, f, so)
    if not best or best[0] < 0.6 * nfr / FPS:
        sys.exit(f"{name}: no first-generation clip covers it in {orig_dir}")
    orig = os.path.join(orig_dir, best[1])
    so = best[2]
    print(f"  framing from {best[1]} (starts mp3 {so:.2f}s)")

    small = [cv2.cvtColor(cv2.resize(f, (64, 114)), cv2.COLOR_BGR2GRAY) for f in rf.clip_frames(src_clip, 270, 480)]
    shots = rf.shots_of(small)
    want = {}
    for a_, b_ in shots:
        k = int(round(((s + (a_ + b_) / 2 / FPS) - so) * FPS))
        want[k] = None
    for k, f in enumerate(rf.clip_frames(orig)):
        if k in want:
            want[k] = f.copy()
    pieces, report = [], []
    for j, (a_, b_) in enumerate(shots):
        n = b_ - a_
        t_mid = s + (a_ + b_) / 2 / FPS
        k = int(round((t_mid - so) * FPS))
        of = want.get(k)
        m = None
        if of is not None:
            cand = [(c, match(of, c, t_mid)) for c in cams]
            cand = [(c, r) for c, r in cand if r]
            if cand:
                m = max(cand, key=lambda z: z[1][4])
        piece = os.path.join(work, f"p{j:02d}.mp4")
        if m and m[1][3] < 480:
            # more than 4x enlargement: not how any first-generation clip was framed, so this is
            # a false match (Ep 11 Dave, whose camera file is damaged, matched a 7x crop of Paul)
            m = (m[0], m[1][:4] + (0.0,))
        if m and m[1][4] >= 0.55:
            cam, (x0, y0, cw, ch, sc) = m
            ts, xs, y = aim(cam, s + a_ / FPS, n, x0, y0, cw, ch, det)
            vf = [f"fps=30", f"crop={cw}:{ch}:'{rf.x_expr(ts, xs)}':{y}"]
            if cam.hdr:
                vf.append(TONEMAP)
            vf.append(f"scale={W}:{H}:flags=lanczos")
            if ch < 1100:
                vf.append(rf.SHARP)                 # the upscale from 720p phones
            vf += ["setsar=1", "format=yuv420p"]
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{cam.t(s + a_ / FPS):.3f}", "-i", cam.src, "-an",
                "-vf", ",".join(vf), "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "16", piece])
            line = (f"  shot {a_ / FPS:6.2f}-{b_ / FPS:6.2f}s  {cam.name} crop {cw}x{ch} "
                    f"x {x0}->{int(xs[0])}..{int(xs[-1])} y {y0}->{y} match {sc:.2f}{' HDR' if cam.hdr else ''}")
            report.append({"shot": [a_ / FPS, b_ / FPS], "cam": cam.name, "crop": [cw, ch], "x0": x0, "y0": y0,
                           "y": y, "match": round(sc, 3)})
        else:
            sh(["ffmpeg", "-v", "error", "-y", "-i", src_clip, "-an", "-vf",
                f"select='between(n\\,{a_}\\,{b_ - 1})',setpts=N/{FPS}/TB,format=yuv420p", "-frames:v", str(n),
                "-c:v", "libx264", "-preset", "medium", "-crf", "16", piece])
            line = f"  shot {a_ / FPS:6.2f}-{b_ / FPS:6.2f}s  NO CAMERA MATCH ({m[1][4]:.2f} best) - copied as is" if m \
                else f"  shot {a_ / FPS:6.2f}-{b_ / FPS:6.2f}s  NO CAMERA MATCH - copied as is"
            report.append({"shot": [a_ / FPS, b_ / FPS], "cam": None})
        print(line, flush=True)
        pieces.append((piece, n))
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\nduration {n / FPS:.6f}\n" for p, n in pieces))
    body = os.path.join(work, "body.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])

    band = rf.caption_band([f for k, f in enumerate(rf.clip_frames(src_clip)) if k % 15 == 0])
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", src_clip, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                            "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    copied = 0
    for fo, fn in zip(rf.clip_frames(src_clip), rf.clip_frames(body)):
        fn = fn.copy()
        r = rf.caption_rect(fo, band) if band else None
        if r:
            y0, y1, x0, x1 = r
            fn[y0:y1 + 1, x0:x1 + 1] = fo[y0:y1 + 1, x0:x1 + 1]
            copied += 1
        enc.stdin.write(fn.tobytes())
    enc.stdin.close()
    enc.wait()
    json.dump({"clip": name, "mp3_start": s, "orig": best[1], "shots": report},
              open(os.path.join(work, "report.json"), "w"), indent=1)
    print(f"  wrote {out}: captions carried on {copied}/{nfr} frames")


if __name__ == "__main__":
    main()
