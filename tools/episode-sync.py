#!/usr/bin/env python3
"""Find the newest Pain 2 Power episode and tell the site about it.

Every Saturday the show airs at 8:30 AM ET and the episode appears on Spotify.
The full video goes to YouTube whenever Nick uploads it, which is NOT the same
moment: Episode 15 was on Spotify before 9 AM but the video did not land until
10:10 AM ET. So this never assumes the two arrive together, and the daily
routine can run `check` any day to backfill whichever half is still missing.

  python3 tools/episode-sync.py check              # read-only, says what is missing
  python3 tools/episode-sync.py add-video          # adds the VIDEOS entry, rebuilds
  python3 tools/episode-sync.py check --json       # same as check, machine readable
  python3 tools/episode-sync.py links              # every episode's Spotify + YouTube URL
  python3 tools/episode-sync.py links --episode 19 # one episode; exit 0 only if both exist
  python3 tools/episode-sync.py links --write      # also save content/episodes/links.json

`links` exists because Nick kept having to paste the Spotify and YouTube links
into chat by hand (Episode 18 on 2026-10-10 was the latest). Every session and
routine that writes a post should run it instead of asking him. It records what
it finds in content/episodes/links.json, so a link survives after it scrolls out
of the feeds: the YouTube channel feed holds only the newest 15 uploads, and the
daily Shorts push a full episode out of it within about two weeks.

WHAT THIS DELIBERATELY DOES NOT DO: write the EPISODES blurb. That is five
paragraphs of prose drawn from the episode transcript, and a generated one reads
like a generated one. `check` reports that EPISODES is missing the episode and
stops; a human or a session writes it from transcript-full.md on the
media/ep{NN}-clips branch. The VIDEOS entry IS fully mechanical -- id, upload
timestamp, title -- so this does that part itself.

Feeds (both public, both reachable from the sandbox):
  Spotify show embed -> the current episode id
  YouTube channel feed -> entries, where a long-form video's
    <link rel="alternate"> href contains /watch?v= and a Short's contains
    /shorts/. Filtering on that is the only reliable way to tell them apart.
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
import html as htmllib
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()

SHOW_ID = "033A1BQq9qqsygFFCq9SIu"
CHANNEL_ID = "UCFzCl3RvdVahfIjKZ1SfRvQ"
SPOTIFY_EMBED = f"https://open.spotify.com/embed/show/{SHOW_ID}"
# The public show page lists every recent episode as <a href="/episode/ID">
# with its title as the link text. The embed above carries only the newest.
SPOTIFY_SHOW = f"https://open.spotify.com/show/{SHOW_ID}"
SPOTIFY_OEMBED = ("https://open.spotify.com/oembed?url="
                  f"https%3A%2F%2Fopen.spotify.com%2Fshow%2F{SHOW_ID}")
YT_FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

NS = {"a": "http://www.w3.org/2005/Atom",
      "yt": "http://www.youtube.com/xml/schemas/2015"}

UA = {"User-Agent": "Mozilla/5.0 (compatible; firstrehabnpb-episode-sync)"}

LINKS_JSON = os.path.join(ROOT, "content", "episodes", "links.json")


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


# --------------------------------------------------------------------------
# feeds
# --------------------------------------------------------------------------

def newest_spotify():
    """Return (episode_id, title). The embed carries exactly one episode id:
    the current one. The oembed title is what names it, e.g.
    'Episode 15: Susan Mann'."""
    ids = re.findall(r"spotify:episode:([A-Za-z0-9]{22})", fetch(SPOTIFY_EMBED))
    if not ids:
        sys.exit("no episode id in the Spotify embed -- the page shape changed")
    title = ""
    try:
        title = json.loads(fetch(SPOTIFY_OEMBED)).get("title", "")
    except Exception as exc:                        # oembed is a nicety
        print(f"  (oembed title unavailable: {exc})", file=sys.stderr)
    return ids[0], title


def newest_youtube_longform():
    """Return (video_id, published, title) for the newest NON-Short video.

    A Short and a full episode both appear in this feed. They are told apart by
    the alternate link path, never by duration or title.
    """
    root = ET.fromstring(fetch(YT_FEED))
    for entry in root.findall("a:entry", NS):
        href = entry.find("a:link[@rel='alternate']", NS).get("href", "")
        if "/shorts/" in href:
            continue
        return (entry.find("yt:videoId", NS).text,
                entry.find("a:published", NS).text,
                entry.find("a:title", NS).text)
    return None, None, None


def all_spotify():
    """Every episode the public show page lists: {number: (id, title)}.
    The page carries roughly the last dozen episodes, newest first."""
    page = fetch(SPOTIFY_SHOW)
    out = {}
    for m in re.finditer(r'href="/episode/([A-Za-z0-9]{22})"[^>]*>(.{0,600}?)</a>',
                         page, re.S):
        text = htmllib.unescape(" ".join(re.sub(r"<[^>]+>", " ", m.group(2)).split()))
        num = re.search(r"Episode\s+(\d+)", text)
        if num and int(num.group(1)) not in out:
            out[int(num.group(1))] = (m.group(1), text)
    return out


def all_youtube_longform():
    """Long-form videos in the channel feed: {number: (id, published, title)}.
    The episode number is read from the title ("... | Pain 2 Power Ep 17: ...")."""
    root = ET.fromstring(fetch(YT_FEED))
    out = {}
    for entry in root.findall("a:entry", NS):
        href = entry.find("a:link[@rel='alternate']", NS).get("href", "")
        if "/shorts/" in href:
            continue
        title = entry.find("a:title", NS).text or ""
        num = re.search(r"Episode\s+(\d+)", title) or re.search(r"\bEp\.?\s*(\d+)", title)
        if num and int(num.group(1)) not in out:
            out[int(num.group(1))] = (entry.find("yt:videoId", NS).text,
                                      entry.find("a:published", NS).text, title)
    return out


def videos_in_build():
    """YouTube ids already recorded in build.py VIDEOS: {number: (id, uploaded)}.
    This is how links older than the feed's 15 newest uploads stay known."""
    src = build_py()
    start = src.find("VIDEOS = [")
    block = src[start:src.find("\n]\n", start)]
    out = {}
    # One dict per video; fields can be separated by comment lines, so read
    # each {...} on its own rather than assuming the keys sit side by side.
    for entry in re.findall(r"\{(.*?)\n    \}", block, re.S):
        vid = re.search(r'"id":\s*"([\w-]{11})"', entry)
        ep = re.search(r'"ep":\s*"Episode (\d+)"', entry)
        up = re.search(r'"uploaded":\s*"([^"]+)"', entry)
        if vid and ep:
            out.setdefault(int(ep.group(1)), (vid.group(1), up.group(1) if up else ""))
    return out


# --------------------------------------------------------------------------
# build.py
# --------------------------------------------------------------------------

def build_py():
    with open(f"{ROOT}/build.py") as fh:
        return fh.read()


def episode_number(title):
    """Pull 'Episode 15' out of a feed title like 'Episode 15: Susan Mann' or
    '... | Pain 2 Power Ep 15'. Returns None rather than guessing."""
    m = re.search(r"Episode\s+(\d+)", title) or re.search(r"\bEp\.?\s*(\d+)", title)
    return f"Episode {m.group(1)}" if m else None


def cmd_check(args):
    src = build_py()
    sp_id, sp_title = newest_spotify()
    yt_id, yt_pub, yt_title = newest_youtube_longform()

    state = {
        "spotify": {"id": sp_id, "title": sp_title,
                    "in_build": sp_id in src,
                    "episode": episode_number(sp_title)},
        "youtube": {"id": yt_id, "published": yt_pub, "title": yt_title,
                    "in_build": bool(yt_id) and yt_id in src,
                    "episode": episode_number(yt_title or "")},
    }

    if args.json:
        print(json.dumps(state, indent=2))
    else:
        s, y = state["spotify"], state["youtube"]
        print(f"Spotify  {s['id']}  {s['title']}")
        print(f"         {'already in build.py' if s['in_build'] else 'MISSING from EPISODES'}")
        print(f"YouTube  {y['id']}  {y['published']}")
        print(f"         {y['title']}")
        print(f"         {'already in build.py' if y['in_build'] else 'MISSING from VIDEOS'}")
        if not s["in_build"]:
            ep = s["episode"] or "Episode ??"
            print(f"\nTODO: add EPISODES[0] for {ep}. This needs a written blurb from")
            print(f"  transcript-full.md on the media/ep{{NN}}-clips branch. Not mechanical,")
            print("  so this script will not fake one.")
        if y["id"] and not y["in_build"]:
            print("\nTODO: add the VIDEOS entry. Mechanical -- run:")
            print("  python3 tools/episode-sync.py add-video")

    # Exit 0 when everything is already on the site, 1 when work remains, so a
    # routine can branch on it without parsing text.
    missing = (not state["spotify"]["in_build"]) or (
        bool(yt_id) and not state["youtube"]["in_build"])
    return 1 if missing else 0


def cmd_add_video(args):
    src = build_py()
    yt_id, yt_pub, yt_title = newest_youtube_longform()
    if not yt_id:
        sys.exit("no long-form video in the channel feed")
    if yt_id in src:
        print(f"{yt_id} is already in build.py, nothing to do")
        return 0

    ep = episode_number(yt_title or "")
    if not ep:
        sys.exit(f"could not read an episode number out of the title: {yt_title!r}\n"
                 "  Add the VIDEOS entry by hand rather than guessing which episode.")

    # The feed title is "<hook>: <guest> | Pain 2 Power Ep NN". Keep the hook as
    # the card title; everything after the colon is the guest line.
    head = (yt_title or "").split("|")[0].strip()
    title, _, guest = head.partition(":")
    title, guest = title.strip(), guest.strip()

    entry = (
        "    {\n"
        f"        # Verified {yt_pub[:10]} against the channel feed: long-form entry\n"
        "        # (link rel=alternate is /watch?v=, not /shorts/).\n"
        f'        "id": "{yt_id}",\n'
        f'        "uploaded": "{yt_pub}",\n'
        f'        "ep": "{ep}",\n'
        f'        "title": "{title}",\n'
        f'        "guest": "{guest}",\n'
        f'        "teaser": "TEASER NEEDED -- one or two sentences from the episode.",\n'
        "    },\n"
    )
    anchor = "VIDEOS = [\n"
    if anchor not in src:
        sys.exit("could not find the VIDEOS list in build.py")
    with open(f"{ROOT}/build.py", "w") as fh:
        fh.write(src.replace(anchor, anchor + entry, 1))

    print(f"added {yt_id} as {ep}: {title}")
    print("TEASER IS A PLACEHOLDER. Replace it before this ships.")

    r = subprocess.run([sys.executable, "build.py"], cwd=ROOT,
                       capture_output=True, text=True)
    print(r.stdout[-800:] or r.stderr[-800:])
    if r.returncode != 0:
        sys.exit("build.py failed; do not commit this")
    if re.search(r"warn|error", r.stdout, re.I):
        sys.exit("build.py printed a warning; read it before committing")
    return 0


def load_links():
    try:
        with open(LINKS_JSON) as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def cmd_links(args):
    """Collect every episode's Spotify and YouTube link into one record."""
    reg = load_links()
    before = json.dumps(reg, sort_keys=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new = []

    def put(num, field, value, extra=None):
        rec = reg.setdefault(str(num), {})
        if not rec.get(field):
            rec[field] = value
            rec.setdefault("first_seen", {})[field] = now
            new.append((num, field, value))
        for k, v in (extra or {}).items():
            rec.setdefault(k, v)

    try:
        for num, (sid, title) in all_spotify().items():
            put(num, "spotify_url", f"https://open.spotify.com/episode/{sid}",
                {"spotify_title": title})
    except Exception as exc:
        print(f"  (Spotify show page unavailable: {exc})", file=sys.stderr)
    for num, (vid, uploaded) in videos_in_build().items():
        put(num, "youtube_url", f"https://www.youtube.com/watch?v={vid}",
            {"youtube_uploaded": uploaded})
    try:
        for num, (vid, pub, title) in all_youtube_longform().items():
            put(num, "youtube_url", f"https://www.youtube.com/watch?v={vid}",
                {"youtube_uploaded": pub, "youtube_title": title})
    except Exception as exc:
        print(f"  (YouTube feed unavailable: {exc})", file=sys.stderr)

    reg = dict(sorted(reg.items(), key=lambda kv: -int(kv[0])))
    if args.write and json.dumps(reg, sort_keys=True) != before:
        os.makedirs(os.path.dirname(LINKS_JSON), exist_ok=True)
        with open(LINKS_JSON, "w") as fh:
            json.dump(reg, fh, indent=2)
            fh.write("\n")

    rows = reg
    if args.episode:
        rows = {str(args.episode): reg.get(str(args.episode), {})}

    if args.json:
        print(json.dumps({"episodes": rows,
                          "new": [{"episode": n, "field": f, "value": v} for n, f, v in new]},
                         indent=2))
    else:
        for num, rec in rows.items():
            print(f"Episode {num}  {rec.get('spotify_title', '')}")
            print(f"   Spotify  {rec.get('spotify_url') or 'NOT FOUND YET'}")
            print(f"   YouTube  {rec.get('youtube_url') or 'NOT FOUND YET'}")
        for n, f, v in new:
            print(f"NEW  Episode {n}  {f}  {v}")

    if args.episode:
        rec = rows[str(args.episode)]
        return 0 if rec.get("spotify_url") and rec.get("youtube_url") else 2
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="report what the feeds have that the site lacks")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("add-video", help="add the newest long-form video to VIDEOS")
    p.set_defaults(func=cmd_add_video)

    p = sub.add_parser("links", help="every episode's Spotify and YouTube URL")
    p.add_argument("--episode", type=int, help="just this episode number")
    p.add_argument("--json", action="store_true")
    p.add_argument("--write", action="store_true",
                   help="save what was found to content/episodes/links.json")
    p.set_defaults(func=cmd_links)

    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
