# OCR the burned-in captions of a clip into timed cues: [{"s","e","text"}].
# usage: cues.py src.mp4 band_top band_bottom out.json
import subprocess, sys, json, numpy as np, re, os, tempfile
from PIL import Image
src, bt, bb, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
NOBOX = len(sys.argv) > 5 and sys.argv[5] == "nobox"
bt -= bt % 2; bb -= (bb - bt) % 2
bt -= bt % 2; bb -= (bb - bt) % 2
FPS = 10; W = 1080; H = bb - bt
p = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"fps={FPS},crop={W}:{H}:0:{bt},format=gray",
                    "-f", "rawvideo", "-"], capture_output=True, check=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W)
masks = fr > 200
if not NOBOX:
    masks = masks & (np.cumsum(fr < 12, axis=2) > 0) & (np.cumsum((fr < 12)[:, :, ::-1], axis=2)[:, :, ::-1] > 0)
segs = []; start = 0
def diff(a, b):
    u = (a | b).sum()
    return 0 if u == 0 else (a ^ b).sum() / u
for i in range(1, len(masks) + 1):
    if i == len(masks) or (diff(masks[i], masks[start]) > 0.35 and diff(masks[i], masks[i-1]) > 0.2):
        segs.append((start, i)); start = i
cues = []
tmp = tempfile.mkdtemp()
for a, b in segs:
    if masks[a:b].sum() / (b - a) < 300:
        continue  # no text on screen
    mid = fr[(a + b) // 2]
    dark = mid < 12
    rows = np.where(dark.mean(axis=1) > 0.15)[0]
    if len(rows) > 20 and not NOBOX:
        y0, y1 = rows.min(), rows.max()
        cols = np.where(dark[y0:y1 + 1].mean(axis=0) > 0.5)[0]
        x0, x1 = cols.min(), cols.max()
        mid = mid[y0 + 2:y1 - 1, x0 + 2:x1 - 1]
    hh, ww = mid.shape
    img = Image.fromarray(255 - np.where(mid > 170, 255, 0).astype(np.uint8)).resize((ww * 2, hh * 2))
    fn = os.path.join(tmp, "c.png"); img.save(fn)
    t = subprocess.run(["tesseract", fn, "-", "--psm", "6", "-l", "eng"], capture_output=True, text=True).stdout
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^[^A-Za-z0-9\"'$(]+", "", t)
    if not t: continue
    if cues and cues[-1]["text"] == t:
        cues[-1]["e"] = b / FPS; continue
    cues.append({"s": a / FPS, "e": b / FPS, "text": t})
json.dump(cues, open(out, "w"), indent=1)
for c in cues: print(f'{c["s"]:6.1f} {c["e"]:6.1f}  {c["text"]}')
