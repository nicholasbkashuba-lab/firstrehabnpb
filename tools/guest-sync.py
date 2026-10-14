#!/usr/bin/env python3
"""Keep /guests.html in step with the episodes.

Every Pain 2 Power guest has one JSON file in content/guests/<slug>.json,
researched from what they said on the show plus their own public pages, with
the URL each background fact came from. build.py renders those files into
/guests.html, the "Meet the guest" links on /podcast.html, and the
PodcastEpisode contributor schema. This script is how a routine knows when a
guest is missing and whether a file is fit to publish.

  python3 tools/guest-sync.py check       # episodes with no guest file; exit 1 if any
  python3 tools/guest-sync.py check --json
  python3 tools/guest-sync.py validate    # every file well formed and sourced; exit 1 if not
  python3 tools/guest-sync.py validate content/guests/butler.json
  python3 tools/guest-sync.py stale --days 180   # files whose research is older than that
  python3 tools/guest-sync.py clips           # new Shorts on the channel, matched to guests
  python3 tools/guest-sync.py clips --write   # ...and add them to each guest's "clips"

WHAT THIS DELIBERATELY DOES NOT DO: research a guest. That is web work and
judgment (is this Instagram account really theirs?), done by a session
following .claude/skills/podcast-guest/SKILL.md. This only says what is
missing and refuses what is not fit to ship.
"""

import argparse
import datetime as dt
import glob
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip() or os.getcwd()
GUEST_DIR = os.path.join(ROOT, "content", "guests")

# Episodes with no outside guest. Episode 1 is Dave telling his own story.
NO_GUEST = {"Episode 1"}

LINK_TYPES = {"website", "profile", "instagram", "facebook", "linkedin", "x",
              "youtube", "tiktok", "podcast", "book", "other"}
# Directories and aggregators are never a fact's only source (skill, "Sources").
WEAK_SOURCES = ("healthgrades.", "vitals.com", "webmd.", "zoominfo.", "doximity.",
                "sharecare.", "npiprofile.", "npino.", "spokeo.", "whitepages.")
CATEGORIES = {"orthopedic-surgery", "shoulder-elbow-hand", "other-specialists",
              "nutrition-wellness", "community", "our-team"}   # GUEST_CATEGORIES in build.py
DASHES = ("—", "–", "&mdash;", "&ndash;")
REQUIRED = ["slug", "name", "honorific", "credentials", "headline", "affiliation",
            "location", "episodes", "on_the_show", "on_the_show_quote", "background",
            "links", "instagram_handle", "phone_on_air", "research_notes", "researched",
            "category"]


def episodes():
    """EPISODES from build.py, as [(label, title), ...], without running the build."""
    spec = importlib.util.spec_from_file_location("site_build", os.path.join(ROOT, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [(e[0], e[1]) for e in mod.EPISODES]


def load():
    out = {}
    for path in sorted(glob.glob(os.path.join(GUEST_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            out[path] = json.load(f)
    return out


def _plain(s):
    return re.sub(r"&[a-z]+;", "", re.sub(r"<[^>]+>", "", s or "")).lower()


def cmd_check(args):
    guests = load().values()
    covered = {}
    for g in guests:
        for e in g.get("episodes", []):
            covered.setdefault(e, []).append(g)
    missing, partial = [], []
    for label, title in episodes():
        if label in NO_GUEST:
            continue
        have = covered.get(label, [])
        if not have:
            missing.append({"episode": label, "title": _plain(title)})
            continue
        # A two guest episode ("A and B") with only one file is half done.
        names = [n for n in re.split(r"\s+(?:and|&amp;|&)\s+", title) if n.strip()]
        if len(names) > len(have):
            partial.append({"episode": label, "title": _plain(title),
                            "have": [g["slug"] for g in have]})
    if args.json:
        print(json.dumps({"missing": missing, "partial": partial}, indent=2))
    else:
        for m in missing:
            print(f"MISSING  {m['episode']}: {m['title']}")
        for p in partial:
            print(f"PARTIAL  {p['episode']}: {p['title']} (have {', '.join(p['have'])})")
        if not missing and not partial:
            print("Every episode's guest has a file in content/guests/.")
    return 1 if (missing or partial) else 0


def validate_one(path, g, labels):
    errs = []
    slug = os.path.splitext(os.path.basename(path))[0]
    for k in REQUIRED:
        if k not in g:
            errs.append(f"missing key {k!r}")
    if errs:
        return errs
    if g["slug"] != slug:
        errs.append(f"slug {g['slug']!r} does not match file name {slug!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        errs.append("slug must be lowercase letters, digits and hyphens")
    if g["honorific"] not in ("", "Dr.", "Captain"):
        errs.append(f"honorific {g['honorific']!r} not one of '', 'Dr.', 'Captain'")
    if not g["episodes"]:
        errs.append("episodes is empty")
    for e in g["episodes"]:
        if e not in labels:
            errs.append(f"episode {e!r} is not in EPISODES")
    if len(g["headline"]) > 80:
        errs.append("headline over 80 characters")
    words = len(_plain(g["on_the_show"]).split())
    if not 30 <= words <= 140:
        errs.append(f"on_the_show is {words} words (want 30 to 140)")
    aff = g["affiliation"]
    if aff is not None and (not isinstance(aff, dict) or not aff.get("name")):
        errs.append("affiliation must be null or {name, url}")
    if aff and aff.get("url") and not aff["url"].startswith("https://"):
        errs.append("affiliation url must be https")
    for i, b in enumerate(g["background"]):
        src = b.get("source", "")
        if not b.get("text"):
            errs.append(f"background[{i}] has no text")
        if not src.startswith("https://"):
            errs.append(f"background[{i}] has no https source")
        elif any(w in src for w in WEAK_SOURCES):
            errs.append(f"background[{i}] sourced only to a directory ({src})")
    for i, l in enumerate(g["links"]):
        if l.get("type") not in LINK_TYPES:
            errs.append(f"links[{i}] type {l.get('type')!r} unknown")
        if not str(l.get("url", "")).startswith("https://"):
            errs.append(f"links[{i}] url must be https")
        if not l.get("verified_by"):
            errs.append(f"links[{i}] has no verified_by: say how you know it is theirs")
    h = g["instagram_handle"]
    if h and not re.fullmatch(r"[A-Za-z0-9._]{1,30}", h):
        errs.append(f"instagram_handle {h!r} is not a bare handle")
    if h and not any(l.get("type") == "instagram" for l in g["links"]):
        errs.append("instagram_handle set but no verified instagram link")
    prose = [g["headline"], g["on_the_show"], g["on_the_show_quote"]] + [b.get("text", "") for b in g["background"]]
    for t in prose:
        if any(d in t for d in DASHES):
            errs.append(f"dash in prose: {t[:60]!r}")
            break
    if g["category"] not in CATEGORIES:
        errs.append(f"category {g['category']!r} not one of {sorted(CATEGORIES)}")
    ph = g.get("photo")
    if ph:
        if ph.get("src"):
            for size in (160, 480):
                for ext in ("webp", "jpg"):
                    if not os.path.exists(os.path.join(ROOT, f"{ph['src']}-{size}.{ext}")):
                        errs.append(f"photo file {ph['src']}-{size}.{ext} missing (tools/guest-photo.py set)")
        elif not ph.get("registry"):
            errs.append("photo needs src (tools/guest-photo.py) or registry (a PHOTOS key)")
        if not ph.get("source"):
            errs.append("photo has no source: which of our videos is it from?")
    for i, c in enumerate(g.get("clips", [])):
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", c.get("youtube_id", "")):
            errs.append(f"clips[{i}] youtube_id is not an 11 character id")
        if not c.get("title"):
            errs.append(f"clips[{i}] has no title")
    try:
        dt.date.fromisoformat(g["researched"])
    except ValueError:
        errs.append("researched must be YYYY-MM-DD")
    return errs


def cmd_validate(args):
    labels = {e for e, _ in episodes()}
    files = load()
    if args.paths:
        files = {p: files.get(os.path.abspath(p)) or json.load(open(p, encoding="utf-8")) for p in args.paths}
    bad = 0
    for path, g in files.items():
        errs = validate_one(path, g, labels)
        name = os.path.relpath(path, ROOT)
        if errs:
            bad += 1
            print(f"FAIL {name}")
            for e in errs:
                print(f"     {e}")
        else:
            print(f"ok   {name}  ({len(g['background'])} facts, {len(g['links'])} links)")
    return 1 if bad else 0


def cmd_stale(args):
    cutoff = dt.date.today() - dt.timedelta(days=args.days)
    old = sorted((g["researched"], g["slug"]) for g in load().values()
                 if dt.date.fromisoformat(g["researched"]) < cutoff)
    for d, s in old:
        print(f"{s}  researched {d}")
    return 1 if old else 0


FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=UCFzCl3RvdVahfIjKZ1SfRvQ"


def _site_text(t):
    """Feed text -> the entity style the site uses; dashes become commas."""
    import html
    t = html.escape(t, quote=False)
    t = re.sub(r"\s*[\u2014\u2013]\s*|\s+-\s+", ", ", t)
    t = re.sub(r"(\w)'(\w)", "\\1&rsquo;\\2", t)
    t = re.sub(r'"([^"]*)"', "&ldquo;\\1&rdquo;", t)
    return t.replace("'", "&rsquo;")


def cmd_clips(args):
    """Shorts in the channel feed (newest 15 uploads) -> the guest each one names.

    Clip descriptions name the guest ("Dr. Don Goodwin on..."), so a Short is
    matched on the guest's full name, their surname, or an also_known_as entry
    ("Captain Kerry"). A Short naming no guest (Dave and Mike only) or more
    than one is left alone and listed, never guessed."""
    import urllib.request
    import xml.etree.ElementTree as ET
    ns = {"a": "http://www.w3.org/2005/Atom", "m": "http://search.yahoo.com/mrss/",
          "yt": "http://www.youtube.com/xml/schemas/2015"}
    with urllib.request.urlopen(FEED, timeout=30) as r:
        root = ET.fromstring(r.read())
    files = load()
    have = {c["youtube_id"] for g in files.values() for c in g.get("clips", [])}
    added, skipped = [], []
    for e in root.findall("a:entry", ns):
        if "/shorts/" not in e.find("a:link", ns).get("href", ""):
            continue
        vid = e.find("yt:videoId", ns).text
        if vid in have:
            continue
        title = e.find("a:title", ns).text or ""
        desc = e.find("m:group/m:description", ns).text or ""
        text = f"{title}\n{desc}"
        hits = []
        for path, g in files.items():
            names = [g["name"], g["name"].split()[-1]] + g.get("also_known_as", [])
            if any(re.search(rf"\b{re.escape(n)}\b", text) for n in names):
                hits.append(path)
        when = e.find("a:published", ns).text[:10]
        if len(hits) != 1:
            skipped.append((vid, title, len(hits)))
            continue
        g = files[hits[0]]
        g.setdefault("clips", []).append({"youtube_id": vid, "title": _site_text(title.strip()), "posted": when})
        g["clips"].sort(key=lambda c: c.get("posted", ""))
        added.append((g["slug"], vid, title))
        if args.write:
            with open(hits[0], "w", encoding="utf-8") as f:
                json.dump(g, f, indent=2, ensure_ascii=False)
                f.write("\n")
    for s, v, t in added:
        print(f"{'ADDED' if args.write else 'NEW'}  {s:12} {v}  {t}")
    for v, t, n in skipped:
        print(f"SKIP  {v}  ({'no guest named' if n == 0 else f'{n} guests named'})  {t}")
    if not added:
        print("No new guest clips in the feed.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="episodes whose guest has no file")
    c.add_argument("--json", action="store_true")
    v = sub.add_parser("validate", help="every guest file well formed and sourced")
    v.add_argument("paths", nargs="*")
    k = sub.add_parser("clips", help="new Shorts in the channel feed, matched to guests")
    k.add_argument("--write", action="store_true")
    s = sub.add_parser("stale", help="guest files researched more than --days ago")
    s.add_argument("--days", type=int, default=180)
    args = ap.parse_args()
    return {"check": cmd_check, "validate": cmd_validate, "stale": cmd_stale,
            "clips": cmd_clips}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
