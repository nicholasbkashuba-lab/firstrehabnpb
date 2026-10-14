"""Centering QA: every video edited for Nick gets this before it ships (his rule, 2026-10-14).

    python3 qa_center.py out/show-9x16.mp4 [more.mp4 ...] [--tol 0.10] [--sheet]

Samples 2 frames a second, finds faces with YuNet, takes the largest face in each frame
and measures how far its centre sits from the frame's centre, as a fraction of the frame
width. Frames with no face (title cards, end cards) are skipped. Any run of flagged
frames is listed with its timestamp so the shot can be fixed; --sheet writes a contact
sheet of the flagged frames next to the video. Exit code 1 when anything is off.

Two-shots are measured on the pair: when the two largest faces are within 60% of each
other's size, the target is their midpoint, not either face.
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.environ.get("SIZZLE_WORK", os.path.expanduser("~/sizzle-work"))


def frames(path, fps=2, width=480):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    W, H = map(int, p.stdout.strip().split(",")[:2])
    h = int(H * width / W) // 2 * 2
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={fps},scale={width}:{h}",
                             "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    i = 0
    while True:
        buf = proc.stdout.read(width * h * 3)
        if len(buf) < width * h * 3:
            break
        yield i / fps, np.frombuffer(buf, np.uint8).reshape(h, width, 3)
        i += 1


def check(path, tol=0.10, sheet=False):
    import cv2
    det = None
    flagged, measured = [], 0
    for t, fr in frames(path):
        h, w = fr.shape[:2]
        if det is None:
            det = cv2.FaceDetectorYN.create(os.path.join(SCR, "models", "yunet.onnx"), "", (w, h), 0.7)
        _, faces = det.detect(fr)
        if faces is None:
            continue
        fs = sorted(faces, key=lambda f: -f[2] * f[3])
        big = fs[0]
        if big[2] < 0.06 * w:        # tiny faces (wide shots, posters) are not the subject
            continue
        measured += 1
        cx = big[0] + big[2] / 2
        if len(fs) > 1 and fs[1][2] * fs[1][3] > 0.6 * big[2] * big[3] and fs[1][2] > 0.06 * w:
            cx = (cx + fs[1][0] + fs[1][2] / 2) / 2      # two-shot: centre the pair
        off = (cx - w / 2) / w
        if abs(off) > tol:
            flagged.append((t, off, fr))
    runs = []
    for t, off, fr in flagged:
        if runs and t - runs[-1][1] <= 0.6:
            runs[-1][1] = t
            runs[-1][2].append(off)
            runs[-1][3].append(fr)
        else:
            runs.append([t, t, [off], [fr]])
    name = os.path.basename(path)
    if not runs:
        print(f"PASS  {name}: {measured} face frames, all within {tol:.0%} of centre")
        return True
    print(f"FAIL  {name}: {len(runs)} off-centre stretch(es) of {measured} face frames")
    for a, b, offs, _ in runs:
        m = float(np.mean(offs))
        print(f"      {a:5.1f}s-{b:5.1f}s  face {abs(m):.0%} {'right' if m > 0 else 'left'} of centre")
    if sheet:
        tiles = [r[3][len(r[3]) // 2] for r in runs][:24]
        import cv2
        th = tiles[0].shape[0]
        row = np.hstack([cv2.resize(t, (int(t.shape[1] * th / t.shape[0]), th)) for t in tiles])
        out = os.path.splitext(path)[0] + "-qa.jpg"
        cv2.imwrite(out, row)
        print(f"      sheet: {out}")
    return False


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tol = 0.10
    if "--tol" in sys.argv:
        tol = float(sys.argv[sys.argv.index("--tol") + 1])
        args = [a for a in args if a != str(tol) and a != sys.argv[sys.argv.index("--tol") + 1]]
    ok = all([check(p, tol, "--sheet" in sys.argv) for p in args])
    sys.exit(0 if ok else 1)
