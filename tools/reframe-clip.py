#!/usr/bin/env python3
"""Re-centre the speaker in a finished vertical clip by re-cutting its shots from the raw cameras.

    python3 tools/reframe-clip.py old.mp4 new.mp4 --mp3 raw.mp3 \
        --cam D=dave.mp4:0.9999586:425.8706 --cam M=mike.mov:0.9999671:512.4313 \
        [--cam A=zoom.mp4:1:326.564] [--work DIR] [--caption-bottom 1590] [--keep-framing]

Each --cam is NAME=path:rate:offset, the episode's sync line: camera_time = rate * mp3_time
+ offset (the relay-work README for the episode has them). Run tools/clip-qa.py on the
result; it must PASS before the file goes anywhere.

Why: Episodes 19 and 20 cut their host shots from 720p phones with a FIXED crop window
(e.g. crop=405:720:440:0), so whenever Dave or Mike leaned, he drifted to the edge of the
frame. Nick's rule is that the subject is centred, every shot. This keeps everything else
about the clip exactly as shipped:

  1. finds where the clip sits in the raw mp3 by audio cross correlation;
  2. splits the clip into shots and matches each one to the camera it was cut from and the
     crop it used (template match against that camera's frame at the synced time);
  3. re-cuts each matched shot at the SAME crop size, so the same zoom and sharpness, with
     the window following the subject's face (YuNet, smoothed, 2 fps keyframes). A shot that
     matches no camera (a stacked two-shot, a title card) is copied over untouched;
  4. copies the burned-in caption box across pixel for pixel (it is opaque, so the box is
     the whole caption) and the clip's audio stream bit for bit. --caption-bottom moves the
     box so its bottom edge sits at that y (house style: 1590). --keep-framing re-cuts each
     shot at the crop it already had (no face following): a way to move captions on a clip
     whose framing already passes clip-qa but that has no clean render.

Needs opencv-python-headless and models/yunet.onnx (see tools/clip-qa.py).
"""
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
SR = 8000
SHARP = "unsharp=5:5:0.6:5:5:0"          # the Ep 19/20 renders sharpened every upscale


def sh(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def pcm(path, start=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", path]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(sh(cmd, capture_output=True).stdout, np.float32)


def locate(clip, mp3):
    """mp3 time at which the clip's first sample sits."""
    a = pcm(clip)[: SR * 12]
    b = pcm(mp3)
    a = (a - a.mean()) / (a.std() + 1e-9)
    b = (b - b.mean()) / (b.std() + 1e-9)
    n = 1 << int(np.ceil(np.log2(len(a) + len(b))))
    r = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(a, n)), n)[: len(b)]
    k = int(np.argmax(r))
    psr = (r[k] - r.mean()) / (r.std() + 1e-9)
    return k / SR, float(psr)


def clip_frames(path, w=W, h=H):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h}", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            return
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def cam_frame(path, t):
    p = sh(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", path, "-frames:v", "1", "-f", "image2pipe",
            "-vcodec", "png", "-"], capture_output=True)
    import cv2
    return cv2.imdecode(np.frombuffer(p.stdout, np.uint8), cv2.IMREAD_COLOR)


def shots_of(small):
    g = [s.astype(np.int16) for s in small]
    cuts = [0] + [i for i in range(1, len(g)) if np.abs(g[i] - g[i - 1]).mean() > 22] + [len(g)]
    out = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        if out and b - a <= 6:                # a flash of a few frames belongs to its neighbour
            out[-1][1] = b
        else:
            out.append([a, b])
    if len(out) > 1 and out[0][1] - out[0][0] <= 6:   # ...including one that opens the clip
        out[1][0] = out[0][0]
        out = out[1:]
    return out


def match(old, cams, t_mp3):
    """Which camera and crop an old frame came from. Returns (name, x, y, cw, ch, score)."""
    import cv2
    best = None
    tmpl_full = old[:1300]                     # above the caption band
    for name, (path, rate, off) in cams.items():
        fr = cam_frame(path, rate * t_mp3 + off)
        if fr is None:
            continue
        ch_, cw_ = fr.shape[:2]
        for crop_h in sorted({ch_, ch_ - 2}):
            sc = crop_h / H
            cw = int(round(W * sc))
            if cw > cw_:
                continue
            tm = cv2.resize(tmpl_full, (cw, int(round(1300 * sc))), interpolation=cv2.INTER_AREA)
            y_off = (ch_ - crop_h) // 2 if crop_h != ch_ else 0
            region = fr[y_off: y_off + tm.shape[0] + 2]
            if region.shape[0] < tm.shape[0]:
                continue
            res = cv2.matchTemplate(cv2.cvtColor(region, cv2.COLOR_BGR2GRAY), cv2.cvtColor(tm, cv2.COLOR_BGR2GRAY),
                                    cv2.TM_CCOEFF_NORMED)
            _, sc_, _, loc = cv2.minMaxLoc(res)
            if crop_h != ch_:
                sc_ -= 0.02                    # prefer the full height crop the renders used
            if best is None or sc_ > best[5]:
                best = (name, loc[0], y_off + loc[1], cw, crop_h, sc_)
    return best


def face_path(path, t0, nfr, cw, ch, y0, x_old, det):
    """Crop x per 2 fps keyframe, following the face nearest the old crop's subject."""
    import cv2
    fr = cam_frame(path, t0)
    cam_w = fr.shape[1]
    step = FPS // 2
    keys = []
    target = x_old + cw / 2
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{max(t0, 0):.3f}", "-i", path, "-frames:v", str(nfr),
                             "-vf", "fps=30", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    fh = fr.shape[0]
    n = cam_w * fh * 3
    i = 0
    scale = 480 / fh
    sw = int(round(cam_w * scale))
    det.setInputSize((sw, 480))
    while True:
        b = proc.stdout.read(n)
        if len(b) < n:
            break
        if i % step == 0:
            f = np.frombuffer(b, np.uint8).reshape(fh, cam_w, 3)[y0:y0 + ch]
            small = cv2.resize(f, (sw, int(round(ch * scale))))
            det.setInputSize((small.shape[1], small.shape[0]))
            _, faces = det.detect(small)
            cx = None
            if faces is not None:
                cand = [(abs((x[0] + x[2] / 2) / scale - target), (x[0] + x[2] / 2) / scale, x[2] / scale) for x in faces
                        if x[2] / scale > 0.12 * cw]
                if cand:
                    d, cx, fw = min(cand)
                    if d > 0.45 * cw and keys:     # a different person entered: keep the subject
                        cx = None
            if cx is not None:
                target = cx
            keys.append((i / FPS, target))
        i += 1
    if not keys:
        keys = [(0, x_old + cw / 2)]
    ts = np.array([k[0] for k in keys])
    xs = np.array([k[1] for k in keys])
    # smooth: a 1.5 s median, then hold still unless the subject really moves (> 6% of the crop)
    sm = np.array([np.median(xs[max(0, j - 1):j + 2]) for j in range(len(xs))])
    out = [sm[0]]
    for v in sm[1:]:
        out.append(v if abs(v - out[-1]) > 0.06 * cw else out[-1])
    xs = np.clip(np.array(out) - cw / 2, 0, cam_w - cw)
    return ts, xs


def x_expr(ts, xs):
    """ffmpeg crop x as a piecewise linear function of t (eases between keyframes)."""
    if len(ts) == 1 or np.ptp(xs) < 1:
        return str(int(round(xs[0])))
    e = str(int(round(xs[-1])))
    for j in range(len(ts) - 2, -1, -1):
        a, b, xa, xb = ts[j], ts[j + 1], xs[j], xs[j + 1]
        seg = f"{xa:.1f}+({xb - xa:.1f})*(t-{a:.3f})/{b - a:.3f}" if abs(xb - xa) >= 1 else f"{xa:.1f}"
        e = f"if(lt(t\\,{b:.3f})\\,{seg}\\,{e})"
    return e


def caption_band(frames):
    """Rows of the house caption box, found once per clip: the rows whose centre strip reads
    as white text on black in many frames, plus the box's ~11 px of padding above."""
    prof = np.zeros(H)
    for f in frames:
        g = f[:, 470:610].mean(axis=2)
        prof += ((g < 25).mean(axis=1) > 0.45) & ((g > 200).mean(axis=1) >= 0.04)
    hot = np.where(prof >= 0.15 * len(frames))[0]
    hot = hot[hot > 700]
    if not len(hot):
        return None
    g = np.split(hot, np.where(np.diff(hot) > 6)[0] + 1)
    g = max(g, key=lambda x: prof[x].sum())
    return int(g[0]) - 11, int(g[-1])


def caption_rect(old, band):
    """The opaque caption box in one old frame: (y0, y1, x0, x1) or None. Columns come from
    the box's black padding row, narrowed to the text plus a margin, so a black shirt or a
    white wall touching the box is not copied with it."""
    y0, y1 = band
    pad = old[y0 + 3].mean(axis=1)
    if pad[540] >= 30:
        return None
    L = 540
    while L > 0 and pad[L - 1] < 30:
        L -= 1
    R = 540
    while R < W - 1 and pad[R + 1] < 30:
        R += 1
    wh = np.where(old[y0:y1 + 1, L:R + 1].mean(axis=2) > 200)[1]
    if not len(wh):
        return None
    return y0, y1, max(L, L + wh.min() - 10), min(R, L + wh.max() + 10)


CAPTION_BOTTOM = 1590    # house caption box bottom edge, y of 1920 (MarginV=49; Nick, 2026-10-28)


def transplant(old, body, new, bottom=None, audio="copy"):
    """Write `new`: the frames of `body` (the clean picture) with each frame's opaque caption box
    from `old` pasted on, moved so its bottom edge sits at `bottom` (None keeps it where it was),
    and the audio of `old`. The box is opaque, so its pixels are the whole caption."""
    band = caption_band([f for k, f in enumerate(clip_frames(old)) if k % 15 == 0])
    dy = (bottom - band[1]) if (band and bottom) else 0
    print(f"  caption box rows: {band}" + (f", moved {dy:+d} px to bottom y {bottom}" if dy else ""))
    a = ["-c:a", "copy"] if audio == "copy" else ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", old, "-map", "0:v", "-map", "1:a", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-colorspace", "bt709"] + a + ["-movflags", "+faststart",
                            "-shortest", new], stdin=subprocess.PIPE)
    copied = n = 0
    for fo, fn in zip(clip_frames(old), clip_frames(body)):
        fn = fn.copy()
        n += 1
        r = caption_rect(fo, band) if band else None
        if r:
            y0, y1, x0, x1 = r
            fn[y0 + dy:y1 + 1 + dy, x0:x1 + 1] = fo[y0:y1 + 1, x0:x1 + 1]
            copied += 1
        enc.stdin.write(fn.tobytes())
    enc.stdin.close()
    enc.wait()
    print(f"  wrote {new}: {n} frames, captions carried over on {copied}")


def main():
    import cv2
    args = sys.argv[1:]
    old, new = args[0], args[1]
    cams, mp3, work, bottom = {}, None, None, None
    keep = "--keep-framing" in args
    args = [x for x in args if x != "--keep-framing"]
    i = 2
    while i < len(args):
        if args[i] == "--cam":
            name, spec = args[i + 1].split("=", 1)
            path, rate, off = spec.rsplit(":", 2)
            cams[name] = (path, float(rate), float(off))
        elif args[i] == "--mp3":
            mp3 = args[i + 1]
        elif args[i] == "--work":
            work = args[i + 1]
        elif args[i] == "--caption-bottom":
            bottom = int(args[i + 1])
        i += 2
    work = work or tempfile.mkdtemp(prefix="reframe-")
    os.makedirs(work, exist_ok=True)
    model = os.path.join(HERE, "..", "models", "yunet.onnx")
    det = cv2.FaceDetectorYN.create(model, "", (270, 480), 0.6)

    s, psr = locate(old, mp3)
    print(f"{os.path.basename(old)}: starts at mp3 {s:.3f}s (psr {psr:.0f})")
    if psr < 8:
        sys.exit("audio does not line up with this mp3: wrong episode?")

    small = [cv2.cvtColor(cv2.resize(f, (64, 114)), cv2.COLOR_BGR2GRAY) for f in clip_frames(old, 270, 480)]
    nfr = len(small)
    shots = shots_of(small)
    mids = {(a + b) // 2: None for a, b in shots}
    for k, f in enumerate(clip_frames(old)):
        if k in mids:
            mids[k] = f.copy()
    plan = []
    for a, b in shots:
        mid = (a + b) // 2
        m = match(mids[mid], cams, s + mid / FPS)
        plan.append((a, b, m))
        print(f"  shot {a / FPS:6.2f}-{b / FPS:6.2f}s  " +
              (f"{m[0]} crop {m[3]}x{m[4]}+{m[1]}+{m[2]} match {m[5]:.2f}" if m else "no camera"))

    pieces = []
    for k, (a, b, m) in enumerate(plan):
        out = os.path.join(work, f"p{k:02d}.mp4")
        n = b - a
        if m and m[5] >= 0.6:
            name, x_old, y0, cw, ch, _ = m
            path, rate, off = cams[name]
            t0 = rate * (s + a / FPS) + off
            if keep:                                     # same framing, e.g. to move captions only
                ts, xs = np.array([0.0]), np.array([float(x_old)])
            else:
                ts, xs = face_path(path, t0, n, cw, ch, y0, x_old, det)
            print(f"  shot {k}: {name} x {x_old} -> {', '.join(str(int(v)) for v in xs[:: max(1, len(xs) // 6)])}")
            vf = f"fps=30,crop={cw}:{ch}:'{x_expr(ts, xs)}':{y0},scale={W}:{H}:flags=lanczos,{SHARP},setsar=1,format=yuv420p"
            sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-i", path, "-an", "-vf", vf, "-frames:v", str(n),
                "-c:v", "libx264", "-preset", "medium", "-crf", "16", out])
        else:
            sh(["ffmpeg", "-v", "error", "-y", "-i", old, "-an", "-vf",
                f"select='between(n\\,{a}\\,{b - 1})',setpts=N/{FPS}/TB,format=yuv420p", "-frames:v", str(n),
                "-c:v", "libx264", "-preset", "medium", "-crf", "16", out])
        pieces.append((out, n))
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\nduration {n / FPS:.6f}\n" for p, n in pieces))
    body = os.path.join(work, "body.mp4")
    sh(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", body])

    transplant(old, body, new, bottom)


if __name__ == "__main__":
    main()
