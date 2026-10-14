#!/usr/bin/env python3
"""Headshots for /guests.

Two sources, in this order (Nick, 2026-10-14: "use their site's photos"):
  1. The official headshot the guest's own practice or employer publishes on
     the profile page we already link. Credited on the profile ("Photo
     courtesy of HSS") and recorded with its URL. It is the guest's
     promotional photo, published so others show it next to their name.
  2. A still from OUR OWN Pain 2 Power footage, when no official headshot
     exists or the site will not serve one.
Never a generated image, and never a photo from a press agency or a TV network
(Bravo's cast shots belong to NBCUniversal; Captain Kerry uses a studio still).

  python3 tools/guest-photo.py site butler             # official headshot candidates
  python3 tools/guest-photo.py frames butler           # footage candidates + contact sheet
  python3 tools/guest-photo.py frames marrone --video clip.mp4   # add frames from a local clip
  python3 tools/guest-photo.py set butler 3            # use candidate 3
  python3 tools/guest-photo.py set butler --image f.jpg --box 520,140,180,180   # manual face box

`site` and `frames` both write /tmp/guest-photo/<slug>/sheet.jpg: every face found, numbered.
LOOK AT IT before choosing. A frame can hold a host (Dave, Mike) or the second
guest of a two guest episode; the number you pick must be the guest. When in
doubt, match the person speaking the guest's own captioned words in a clip.

`set` writes assets/guests/<slug>-{480,160}.{webp,jpg} (square, face centred
with headroom) and records "photo" in content/guests/<slug>.json. Then rebuild.
Needs Pillow and ffmpeg; face detection uses opencv-python-headless when it is
installed (pin <5: OpenCV 5 dropped CascadeClassifier) and otherwise falls back to a centred crop (pass --box instead).
"""

import argparse
import io
import json
import os
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip() or os.getcwd()
GUEST_DIR = os.path.join(ROOT, "content", "guests")
OUT_DIR = os.path.join(ROOT, "assets", "guests")
WORK = "/tmp/guest-photo"
SIZES = (480, 160)
# A bare "Mozilla/5.0" gets a 403 from some practice sites (orthocarefl.com); a full one does not.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def guest(slug):
    with open(os.path.join(GUEST_DIR, f"{slug}.json"), encoding="utf-8") as f:
        return json.load(f)


def save_guest(g):
    with open(os.path.join(GUEST_DIR, f"{g['slug']}.json"), "w", encoding="utf-8") as f:
        json.dump(g, f, indent=2, ensure_ascii=False)
        f.write("\n")


def videos_for(g):
    """YouTube ids of the guest's full episodes (from build.py VIDEOS) and clips."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("site_build", os.path.join(ROOT, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ids = [v["id"] for v in mod.VIDEOS if v["ep"] in g["episodes"]]
    ids += [c["youtube_id"] for c in g.get("clips", [])]
    return ids


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return Image.open(io.BytesIO(r.read())).convert("RGB")
    except Exception:
        return None


def faces(im):
    try:
        import cv2
        import numpy as np
    except ImportError:
        return []
    gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)
    casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    found = casc.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6,
                                  minSize=(max(60, im.width // 16),) * 2)
    return [tuple(int(v) for v in f) for f in found]


def square_crop(im, box):
    """Square around the face: face ~42% of the frame, eyes a little above centre."""
    x, y, w, h = box
    side = int(max(w, h) / 0.42)
    cx, cy = x + w / 2, y + h * 0.62
    left = int(min(max(cx - side / 2, 0), max(im.width - side, 0)))
    top = int(min(max(cy - side / 2, 0), max(im.height - side, 0)))
    side = min(side, im.width, im.height)
    return im.crop((left, top, left + side, top + side))


def cmd_frames(a):
    g = guest(a.slug)
    work = os.path.join(WORK, a.slug)
    os.makedirs(work, exist_ok=True)
    sources = []
    for vid in videos_for(g):
        for name in ("maxresdefault", "maxres2", "maxres3", "oardefault", "oar2", "oar3"):
            im = fetch(f"https://i.ytimg.com/vi/{vid}/{name}.jpg")
            if im is not None and im.width >= 400:
                sources.append((f"youtube:{vid}/{name}", im))
    for path in a.video or []:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "csv=p=0", path], capture_output=True, text=True).stdout or 0)
        for i in range(8):
            t = dur * (i + 0.5) / 8
            out = os.path.join(work, f"v{len(sources)}.jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", path,
                            "-frames:v", "1", out], check=False)
            if os.path.exists(out):
                sources.append((f"file:{os.path.basename(path)}@{t:.1f}s", Image.open(out).convert("RGB")))
    cands = []
    for src, im in sources:
        for box in faces(im):
            n = len(cands) + 1
            im.save(os.path.join(work, f"src{n}.jpg"), quality=95)
            cands.append({"n": n, "source": src, "box": box, "file": os.path.join(work, f"src{n}.jpg")})
    if not cands:
        print("No faces found. Pass --video with a clip, or use set --image --box.")
        return 1
    _sheet(work, cands)
    print(f"{len(cands)} faces from {len(sources)} frames -> {work}/sheet.jpg")
    return 0


def _abs(base, u):
    from urllib.parse import urljoin
    return urljoin(base, u.replace("&amp;", "&"))


def cmd_site(a):
    """og:image plus any <img> naming the guest, on each profile/website link."""
    import re
    from urllib.parse import urlparse
    g = guest(a.slug)
    work = os.path.join(WORK, a.slug)
    os.makedirs(work, exist_ok=True)
    names = {g["name"].split()[-1].lower(), g["name"].split()[0].lower()}
    pages = [l["url"] for l in g.get("links", []) if l["type"] in ("profile", "website")
             and "firstrehabnpb.com" not in l["url"]] + (a.page or [])
    urls = []
    for page in pages:
        try:
            req = urllib.request.Request(page, headers={"User-Agent": UA})
            html = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
        except Exception as e:
            print(f"  cannot read {page}: {e}")
            continue
        for m in re.finditer(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', html):
            urls.append((page, _abs(page, m.group(1))))
        for m in re.finditer(r"<img\b[^>]*>", html, re.I):
            tag = m.group(0)
            src = re.search(r'(?:data-src|src)="([^"]+)"', tag)
            if src and any(n in tag.lower() for n in names):
                urls.append((page, _abs(page, src.group(1))))
    cands, seen = [], set()
    for page, u in urls:
        if u in seen or u.lower().endswith(".svg"):
            continue
        seen.add(u)
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA, "Referer": page})
            im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=25).read())).convert("RGB")
        except Exception:
            continue
        if im.width < 150 or im.height < 150:
            continue   # icons, logos
        found = sorted(faces(im), key=lambda b: -b[2] * b[3])
        if len(found) > 1 and found[1][2] > found[0][2] * 0.6:
            continue   # two similar faces: a group shot, not a headshot
        # No face found (detector missed, or it is a logo): offer the whole
        # frame anyway, centred, and let the person choosing look at it.
        box = found[0] if found else (im.width // 4, im.height // 6, im.width // 2, im.width // 2)
        n = len(cands) + 1
        path = os.path.join(work, f"site{n}.jpg")
        im.save(path, quality=95)
        cands.append({"n": n, "source": u, "page": page, "box": list(box), "file": path,
                      "credit": (g.get("affiliation") or {}).get("name") or urlparse(page).netloc.replace("www.", "")})
    if not cands:
        print("No single-face headshot found on the guest's pages. Use frames instead.")
        return 1
    _sheet(work, cands)
    print(f"{len(cands)} headshot candidates -> {work}/sheet.jpg")
    return 0


def _sheet(work, cands):
    tiles = [square_crop(Image.open(c["file"]), c["box"]).resize((200, 200)) for c in cands]
    cols = 6
    sheet = Image.new("RGB", (200 * cols, 220 * ((len(tiles) + cols - 1) // cols)), "white")
    d = ImageDraw.Draw(sheet)
    for i, t in enumerate(tiles):
        x, y = (i % cols) * 200, (i // cols) * 220
        sheet.paste(t, (x, y))
        d.text((x + 6, y + 203), f"#{i + 1}", fill="black")
    sheet.save(os.path.join(work, "sheet.jpg"), quality=85)
    with open(os.path.join(work, "candidates.json"), "w") as f:
        json.dump(cands, f, indent=1)


def write_photo(g, im, source, credit=""):
    os.makedirs(OUT_DIR, exist_ok=True)
    for s in SIZES:
        out = im.resize((s, s), Image.LANCZOS)
        out.save(os.path.join(OUT_DIR, f"{g['slug']}-{s}.webp"), quality=82, method=6)
        out.save(os.path.join(OUT_DIR, f"{g['slug']}-{s}.jpg"), quality=84, optimize=True, progressive=True)
    g["photo"] = {"src": f"assets/guests/{g['slug']}", "source": source}
    if credit:
        g["photo"]["credit"] = credit
    save_guest(g)
    print(f"wrote assets/guests/{g['slug']}-{{480,160}}.{{webp,jpg}} from {source}")


def cmd_set(a):
    g = guest(a.slug)
    if a.image:
        im = Image.open(a.image).convert("RGB")
        box = tuple(int(v) for v in a.box.split(",")) if a.box else None
        if box is None:
            found = faces(im)
            if len(found) != 1:
                print(f"{len(found)} faces in that image; pass --box x,y,w,h")
                return 1
            box = found[0]
        write_photo(g, square_crop(im, box), a.source or f"file:{os.path.basename(a.image)}", a.credit or "")
        return 0
    cands = json.load(open(os.path.join(WORK, a.slug, "candidates.json")))
    c = next(c for c in cands if c["n"] == a.n)
    write_photo(g, square_crop(Image.open(c["file"]), c["box"]), c["source"], c.get("credit", ""))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    w = sub.add_parser("site")
    w.add_argument("slug")
    w.add_argument("--page", action="append", help="another page of theirs to look on")
    f = sub.add_parser("frames")
    f.add_argument("slug")
    f.add_argument("--video", action="append", help="local clip or episode file to sample")
    s = sub.add_parser("set")
    s.add_argument("slug")
    s.add_argument("n", nargs="?", type=int)
    s.add_argument("--image")
    s.add_argument("--box", help="face box x,y,w,h in the image's pixels")
    s.add_argument("--source", help="where the frame came from, recorded in the guest file")
    s.add_argument("--credit", help="who the photo belongs to, shown on the profile")
    a = ap.parse_args()
    return {"site": cmd_site, "frames": cmd_frames, "set": cmd_set}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
