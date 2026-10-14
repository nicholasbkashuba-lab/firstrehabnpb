#!/usr/bin/env python3
"""
Derive responsive WebP + JPEG renditions for every real photograph on the site.

Source of truth for WHICH photos exist and where they focus is PHOTOS in build.py.
This script only does the pixel work: it reads that dict, and writes
assets/img/<name>-<width>.{webp,jpg} plus a manifest consumed by build.py.

Rules:
  - NEVER upscale. A 680px source produces a 680px largest rendition, not a 1440px
    blurry one. The manifest records the real cap so build.py can size accordingly.
  - WebP is the primary, JPEG the fallback. Both are emitted for every width.
  - Focal points live in build.py, not here, because they are a design decision.

Usage:  python3 tools/build-images.py [--force]
"""
import json
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "img")
MANIFEST = os.path.join(OUT_DIR, "manifest.json")

# Rendition ladder. Each photo gets every width that does not exceed its source.
WIDTHS = [480, 768, 1024, 1440, 1920]

WEBP_Q = 82
JPEG_Q = 84


def load_photos():
    """Import PHOTOS from build.py without executing the whole build."""
    sys.path.insert(0, ROOT)
    import importlib.util

    spec = importlib.util.spec_from_file_location("sitebuild", os.path.join(ROOT, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    # build.py runs its build at import only under __main__, so a plain import is safe.
    spec.loader.exec_module(mod)
    return mod.PHOTOS


def render(name, spec, force=False):
    src_path = os.path.join(ROOT, spec["src"])
    if not os.path.exists(src_path):
        return {"error": f"missing source {spec['src']}"}

    im = Image.open(src_path)
    im = im.convert("RGB")
    sw, sh = im.size

    widths = [w for w in WIDTHS if w <= sw]
    if not widths:
        widths = [sw]          # source smaller than the smallest rung: ship it as-is
    if sw not in widths and sw < max(WIDTHS):
        widths.append(sw)      # always include the native width as the top rung
    widths = sorted(set(widths))

    made = []
    for w in widths:
        h = round(sh * (w / sw))
        resized = im.resize((w, h), Image.LANCZOS) if w != sw else im

        for ext, kwargs in (
            ("webp", dict(format="WEBP", quality=WEBP_Q, method=6)),
            ("jpg", dict(format="JPEG", quality=JPEG_Q, progressive=True, optimize=True)),
        ):
            out = os.path.join(OUT_DIR, f"{name}-{w}.{ext}")
            if force or not os.path.exists(out):
                resized.save(out, **kwargs)
        made.append(w)

    return {
        "name": name,
        "source": spec["src"],
        "native": [sw, sh],
        "widths": made,
        "max_width": max(made),
        "aspect": round(sw / sh, 4),
        "focal": spec["focal"],
        "alt": spec["alt"],
    }


def main():
    force = "--force" in sys.argv
    os.makedirs(OUT_DIR, exist_ok=True)
    photos = load_photos()

    manifest, problems = {}, []
    for name, spec in photos.items():
        info = render(name, spec, force)
        if "error" in info:
            problems.append(f"{name}: {info['error']}")
            continue
        manifest[name] = info

    with open(MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    total = sum(len(v["widths"]) * 2 for v in manifest.values())
    print(f"images: {len(manifest)} photos -> {total} files in assets/img/")
    for name, v in sorted(manifest.items()):
        cap = "" if v["max_width"] >= 1440 else f"  (capped at {v['max_width']}px by source)"
        print(f"  {name:22s} {v['native'][0]}x{v['native'][1]}  widths={v['widths']}{cap}")
    for p in problems:
        print(f"  !! {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
