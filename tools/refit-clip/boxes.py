# Find the burned-in caption box per sampled frame: solid black rows (value < 10) wide enough,
# with white text inside. Prints per-frame (t, top, bottom, left, right) and the overall min top.
import subprocess, sys, json, numpy as np
src, fps = sys.argv[1], 10
W, H = 1080, 1920
p = subprocess.run(["ffmpeg","-v","error","-i",src,"-vf",f"fps={fps},format=gray","-f","rawvideo","-"],capture_output=True,check=True)
frames = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W)
out = []
for i, f in enumerate(frames):
    band = f[1100:1920]
    black = (band < 10)
    rowfrac = black.mean(axis=1)
    white = (band > 225).sum(axis=1)
    rows = np.where((rowfrac > 0.12) )[0]
    # keep rows that belong to a block that contains white text rows
    box = None
    if len(rows):
        # group contiguous rows
        groups = np.split(rows, np.where(np.diff(rows) > 3)[0] + 1)
        for g in groups:
            if len(g) >= 25 and white[g[0]:g[-1]+1].sum() > 400:
                cols = np.where(black[g[0]:g[-1]+1].mean(axis=0) > 0.6)[0]
                box = (int(g[0]+1100), int(g[-1]+1100), int(cols.min()) if len(cols) else 0, int(cols.max()) if len(cols) else W)
    out.append((round(i/fps,2), box))
tops = [b[0] for _, b in out if b]
json.dump({"frames": out, "min_top": min(tops) if tops else None, "max_bottom": max(b[1] for _, b in out if b) if tops else None,
           "found": len(tops), "n": len(out)}, open(sys.argv[2], "w"))
print(sys.argv[1].split('/')[-1], "found", len(tops), "/", len(out), "top", min(tops) if tops else None, "bottom", max(b[1] for _, b in out if b) if tops else None)
