#!/usr/bin/env python3
"""Move a clip's burned-in caption box up or down, using its clean (uncaptioned) render.

    python3 tools/move-captions.py captioned.mp4 clean.mp4 out.mp4 [--bottom 1590]

The house caption box is opaque, so each frame's box is lifted off the captioned clip pixel
for pixel and pasted onto the clean picture with its bottom edge at --bottom (default: the
house position in tools/reframe-clip.py, CAPTION_BOTTOM). Picture and audio are otherwise
the clean render's and the captioned clip's, untouched. This is why every clip keeps its
clean render: without one, moving captions means cropping the finished picture.

Nick asked for the captions lower on 2026-10-28 and picked a bottom edge of y 1590 (MarginV=49),
the lowest that the Instagram feed's 4:5 crop (y 285..1635) still shows in full.
Run tools/clip-qa.py on the result.
"""
import importlib.util
import os
import sys

_spec = importlib.util.spec_from_file_location("reframe", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                      "reframe-clip.py"))
rf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rf)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 3:
        sys.exit(__doc__)
    bottom = rf.CAPTION_BOTTOM
    if "--bottom" in args:
        bottom = int(args[args.index("--bottom") + 1])
    rf.transplant(args[0], args[1], args[2], bottom)
