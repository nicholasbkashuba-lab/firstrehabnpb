#!/usr/bin/env python3
"""Make the /things-to-do.html photo renditions: assets/places/<key>-{800,1600}.{webp,jpg}.

    python3 tools/place-photo.py <key> <source.jpg> [<key> <source.jpg> ...]

Prints "<key> <width> <height>" for each, the numbers PLACE_PHOTOS in build.py records.
Never upscales: a source narrower than 1600 px caps the large rendition at its own width.
Where the photos come from, and the credit rules, are in the PLACE_PHOTOS comment.
"""
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "places")

def make(key, src):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    os.makedirs(OUT, exist_ok=True)
    for w in (800, 1600):
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(os.path.join(OUT, f"{key}-{w}.jpg"), quality=82, optimize=True, progressive=True)
        r.save(os.path.join(OUT, f"{key}-{w}.webp"), quality=78, method=6)
    big = Image.open(os.path.join(OUT, f"{key}-800.jpg"))
    print(key, big.width, big.height)

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or len(a) % 2:
        sys.exit(__doc__)
    for k, s in zip(a[::2], a[1::2]):
        make(k, s)
