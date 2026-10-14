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
DASHES = ("—", "–", "&mdash;", "&ndash;")
REQUIRED = ["slug", "name", "honorific", "credentials", "headline", "affiliation",
            "location", "episodes", "on_the_show", "on_the_show_quote", "background",
            "links", "instagram_handle", "phone_on_air", "research_notes", "researched"]


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="episodes whose guest has no file")
    c.add_argument("--json", action="store_true")
    v = sub.add_parser("validate", help="every guest file well formed and sourced")
    v.add_argument("paths", nargs="*")
    s = sub.add_parser("stale", help="guest files researched more than --days ago")
    s.add_argument("--days", type=int, default=180)
    args = ap.parse_args()
    return {"check": cmd_check, "validate": cmd_validate, "stale": cmd_stale}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
