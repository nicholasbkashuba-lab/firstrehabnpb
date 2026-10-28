# Per-shot face centre for a clip, so a 9:16 crop narrower than the frame stays on the subject.
# usage: track.py src.mp4 y0 y1 out.json   -> {"shots": [[t_start, t_end, cx], ...], "cw": crop width}
import subprocess, sys, json, numpy as np, cv2, os
src, y0, y1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "models", "yunet.onnx")
FPS = 5; SW, SH = 270, 480
p = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},scale={SW}:{SH}", "-pix_fmt", "bgr24",
                    "-f", "rawvideo", "-"], capture_output=True, check=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, SH, SW, 3)
det = cv2.FaceDetectorYN.create(MODEL, "", (SW, SH), 0.6)
g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.int16) for f in fr]
cuts = [0] + [i for i in range(1, len(g)) if np.abs(g[i] - g[i - 1]).mean() > 28] + [len(g)]
sy0, sy1 = y0 * SH / 1920, y1 * SH / 1920
shots = []
for a, b in zip(cuts[:-1], cuts[1:]):
    xs = []
    for f in fr[a:b]:
        _, faces = det.detect(f)
        if faces is None: continue
        faces = [x for x in faces if sy0 <= x[1] + x[3] / 2 <= sy1]
        if not faces: continue
        x = max(faces, key=lambda r: r[2] * r[3])
        xs.append((x[0] + x[2] / 2) * 1080 / SW)
    cx = float(np.median(xs)) if xs else None
    shots.append([a / FPS, b / FPS, cx])
# fill shots with no face from the neighbour, else centre
for i, s in enumerate(shots):
    if s[2] is None:
        nb = [t[2] for t in shots[max(0, i - 1):i + 2] if t[2] is not None]
        s[2] = nb[0] if nb else 540.0
json.dump({"shots": shots}, open(out, "w"))
print(os.path.basename(src), [(round(a, 1), round(c)) for a, b, c in shots])
