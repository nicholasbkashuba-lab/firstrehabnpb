"""python3 run.py <reel_module> <fmt> [<fmt> ...] [--draft]"""
import importlib
import os
import sys
import time

import engine as E

mod = importlib.import_module(sys.argv[1])
fmts = [a for a in sys.argv[2:] if not a.startswith("--")]
draft = "--draft" in sys.argv
out_dir = os.path.join(E.SCR, "out")
os.makedirs(out_dir, exist_ok=True)
name = sys.argv[1].replace("reel_", "")

wav = dry = None
if any(f != "hero" for f in fmts) and hasattr(mod, "score"):
    t = time.time()
    sc = mod.score()
    n = int(mod.DUR * 48000)
    wav = E.write_wav(os.path.join(out_dir, f"{name}.wav"), sc.mix()[:, :n])
    dry = E.write_wav(os.path.join(out_dir, f"{name}-nomusic.wav"), sc.mix(music=False)[:, :n])
    print(f"audio {time.time() - t:.1f}s", flush=True)
for f in fmts:
    t = time.time()
    p = os.path.join(out_dir, f"{name}-{f}{'-draft' if draft else ''}.mp4")
    E.render(mod.REEL, f, p, crf=26 if draft else 18, audio=wav, preset="ultrafast" if draft else "medium")
    if dry and f != "hero":
        # same picture, voice-only track
        import subprocess
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-i", dry, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", p.replace(".mp4", "-nomusic.mp4")],
                       check=True)
    print(f"{f} {time.time() - t:.1f}s -> {p}", flush=True)
