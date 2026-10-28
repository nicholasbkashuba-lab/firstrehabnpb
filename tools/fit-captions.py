#!/usr/bin/env python3
"""RETIRED 2026-10-27. Do not use: Nick rejected the shrunk picture ("Looks horrible"). Every clip
fills the frame. Use tools/refit-clip/ instead. Kept only as a record of what not to ship.

Rescue an already rendered 9:16 clip whose burned-in captions sit too low.

Instagram's feed crops a Reel to 4:5 (keeps y 285..1635 of 1920) and Reels/TikTok/Shorts
lay their own text over the bottom ~420 px, so captions placed below ~y 1500 get cut off.
New clips fix this at render time (MarginV=49, see CLAUDE.md). This is for clips already
rendered: it shrinks the picture, top-anchored and horizontally centred, just enough that
the lowest caption row lands at --target, over a blurred copy of the same frame. Captions,
audio and framing are untouched; nothing is re-typed.

    python3 tools/fit-captions.py in.mp4 out.mp4 --caption-bottom 1838 [--target 1450]

--caption-bottom is the lowest pixel row any caption reaches (measure it on frames; the
2026-10-20 batch ranged 1590 to 1843). Used on 2026-10-20 for 24 queued clips.
"""
import argparse, subprocess, sys
sys.exit("fit-captions.py is retired: it shrinks the picture. Use tools/refit-clip/ (full frame).")
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dst")
ap.add_argument("--caption-bottom", type=int, required=True)
ap.add_argument("--target", type=int, default=1450)
a = ap.parse_args()
s = min(1.0, a.target / (a.caption_bottom + 4))
w = int(round(1080 * s / 2)) * 2; h = int(round(1920 * s / 2)) * 2
vf = (f"[0:v]split[a][b];[b]scale=1080:1920,boxblur=40:4,eq=brightness=-0.06[bg];"
      f"[a]scale={w}:{h}:flags=lanczos[fg];[bg][fg]overlay={(1080 - w) // 2}:0,format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-filter_complex", vf, "-map", "[v]", "-map", "0:a?",
                "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", "30", "-color_primaries", "bt709",
                "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+faststart", a.dst],
               check=True)
print(f"scale {s:.3f}; caption bottom now ~{int((a.caption_bottom + 4) * s)}")
