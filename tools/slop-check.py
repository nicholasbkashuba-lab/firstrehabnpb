#!/usr/bin/env python3
"""Check blog post bodies against the anti-AI-slop rules in BLOG-PLAYBOOK.md.

    python3 tools/slop-check.py                 # every post in BLOG_POSTS
    python3 tools/slop-check.py --slug my-post  # one post
    python3 tools/slop-check.py --file draft.html
    python3 tools/slop-check.py --new           # only posts not in the baseline

Exits 1 if any post has a violation, so the blog flow can gate on it. The seven posts
that predate the rules are listed in BASELINE and reported as warnings, not failures;
delete a slug from that list once its post has been rewritten.

Rules live in BLOG-PLAYBOOK.md under "No AI slop". Keep the two in sync.
"""
import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Posts written before the anti-slop rules existed. Warnings only.
BASELINE = {
    "reverse-shoulder-replacement-explained",
    "what-to-expect-first-pt-visit",
    "five-morning-habits-back-pain",
    "why-hand-therapy-is-different",
    "knee-arthritis-before-surgery",
    "headaches-that-start-in-the-neck",
    "cartilage-transplant-knee-explained",
}

# (label, compiled pattern). Matched against plain text, entities already decoded.
BANNED = [
    ("em/en dash in prose", re.compile(r"[–—]|(?<=\S) -- (?=\S)")),
    ("it's not X it's Y", re.compile(
        r"\b(?:it|this|that)'?s not (?:about )?[^.!?]{1,60}?,\s*(?:it|this|that)'?s\b", re.I)),
    ("isn't just / more than just", re.compile(
        r"\b(?:is|are|was|were|it'?s|that'?s)n'?t just\b|\bmore than just\b|\bnot just about\b", re.I)),
    ("not only ... but also", re.compile(r"\bnot only\b[^.!?]{1,80}\bbut also\b", re.I)),
    ("In today's world", re.compile(r"\bin (?:today'?s|the modern) (?:world|age|landscape)\b", re.I)),
    ("In the world of", re.compile(r"\bin the world of\b", re.I)),
    ("When it comes to", re.compile(r"\bwhen it comes to\b", re.I)),
    ("At the end of the day", re.compile(r"\bat the end of the day\b", re.I)),
    ("Here's the thing", re.compile(r"\bhere'?s the thing\b", re.I)),
    ("The truth is", re.compile(r"\bthe truth is\b", re.I)),
    ("It's worth noting", re.compile(r"\bit'?s worth noting\b|\bworth noting that\b", re.I)),
    ("That said", re.compile(r"(?:^|[.!?]\s+|>)that said\b", re.I)),
    ("Simply put", re.compile(r"\bsimply put\b", re.I)),
    ("Let's be clear", re.compile(r"\blet'?s be clear\b", re.I)),
    ("Whether you're X or Y", re.compile(r"\bwhether you'?re\b[^.!?]{1,60}\bor\b", re.I)),
    ("LLM vocabulary", re.compile(
        r"\b(?:delve|delves|delving|robust|leverage[sd]?|leveraging|seamless(?:ly)?|"
        r"crucial(?:ly)?|vital(?:ly)?|landscape|unlock(?:s|ing)?|empower(?:s|ing|ed)?|"
        r"game[- ]?changer|tailored|cutting[- ]edge|state[- ]of[- ]the[- ]art|"
        r"testament to|treasure trove|holistic approach)\b", re.I)),
    ("navigate/journey as metaphor", re.compile(
        r"\bnavigat(?:e|ing|es) (?:the|your|this)\b|\byour (?:healing|wellness|recovery) journey\b", re.I)),
    ("In conclusion", re.compile(r"\bin conclusion\b|\bto sum (?:up|it up)\b|\bin summary\b", re.I)),
    ("hedge stack", re.compile(
        r"\bmay (?:potentially|possibly)\b|\bcan potentially\b|\bmight possibly\b|"
        r"\bcould potentially\b", re.I)),
    ("exclamation mark", re.compile(r"!")),
    ("emoji", re.compile("[\U0001F300-\U0001FAFF☀-➿]")),
]

# Numbers that look like sourced statistics. The playbook bans invented ones outright,
# so any percentage in a post needs a human to confirm it came from the transcript.
STAT = re.compile(r"\b\d{1,3}(?:\.\d+)?\s?(?:%|percent)\b", re.I)

PHONE = "561-624-4263"


def plain(body: str) -> str:
    """Strip tags and decode entities, leaving prose the rules can be matched against."""
    text = re.sub(r"<[^>]+>", " ", body)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def sentences(text: str):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def check(slug: str, post: dict):
    """Return (errors, warnings) for one post."""
    body = post.get("body", "")
    # The phone number's hyphens are legal; take them out before the dash rule runs.
    prose = plain(body).replace(PHONE, "PHONE").replace("561-624-GAME", "PHONE")
    errs, warns = [], []

    for label, pattern in BANNED:
        for m in pattern.finditer(prose):
            snippet = prose[max(0, m.start() - 40):m.end() + 40]
            errs.append(f"{label}: ...{snippet}...")

    # Structure and formatting, measured on the raw HTML.
    bold = len(re.findall(r"<strong[ >]", body))
    if bold > 1:
        errs.append(f"bold used {bold} times, limit is 1 per post")
    if re.search(r"<h1[ >]", body):
        errs.append("body contains an <h1>; the page hero renders the only h1")
    if re.search(r"<h[3-6][ >]", body):
        warns.append("body uses h3 or deeper; the house structure is h2 only")
    lists = len(re.findall(r"<ul[ >]|<ol[ >]", body))
    if lists > 1:
        errs.append(f"{lists} bulleted lists, limit is 1 per post")

    # Sourcing and voice.
    links = re.findall(r'href="(\.\./[^"]+)"', body)
    if len(links) < 2:
        errs.append(f"{len(links)} internal link(s), need at least 2")
    if not re.search(r"(?:said|says|puts it|told|explains|explained|according to)", prose, re.I):
        warns.append("no attributed speech found; podcast posts need at least two quotes")
    words = len(prose.split())
    short = [s for s in sentences(prose) if len(s.split()) < 8]
    if words >= 200 and len(short) < words // 200:
        warns.append(f"only {len(short)} short sentence(s) in {words} words; vary the rhythm")

    # Required furniture.
    if PHONE not in plain(body):
        errs.append(f"closing CTA is missing the phone number {PHONE}")
    if "not medical advice" not in prose.lower():
        errs.append("missing the medical-advice disclaimer paragraph")
    for m in STAT.finditer(prose):
        warns.append(f"statistic '{m.group(0)}' needs a transcript or site source on the flag list")

    if words < 400:
        warns.append(f"{words} words; posts run 600 to 1,200")

    return errs, warns


def load_posts():
    """Exec build.py's globals far enough to reach BLOG_POSTS without building the site."""
    src = (ROOT / "build.py").read_text()
    cut = src.index("OPEN_POSITIONS = [")
    ns = {"__file__": str(ROOT / "build.py"), "__name__": "build_slopcheck"}
    exec(compile(src[:cut], "build.py", "exec"), ns)
    return ns["BLOG_POSTS"]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", help="check one post")
    ap.add_argument("--file", help="check a standalone HTML fragment instead of build.py")
    ap.add_argument("--new", action="store_true", help="skip the pre-rules baseline posts")
    args = ap.parse_args()

    if args.file:
        targets = {Path(args.file).stem: {"body": Path(args.file).read_text()}}
    else:
        posts = load_posts()
        if args.slug:
            if args.slug not in posts:
                sys.exit(f"no such slug: {args.slug}")
            targets = {args.slug: posts[args.slug]}
        else:
            targets = posts

    failed = 0
    for slug, post in targets.items():
        baseline = slug in BASELINE and not args.file
        if args.new and baseline:
            continue
        errs, warns = check(slug, post)
        if not errs and not warns:
            print(f"OK    {slug}")
            continue
        tag = "BASE " if baseline else ("FAIL " if errs else "WARN ")
        print(f"{tag} {slug}")
        for e in errs:
            print(f"        {'warn' if baseline else 'FAIL'}: {e}")
        for w in warns:
            print(f"        warn: {w}")
        if errs and not baseline:
            failed += 1

    if failed:
        print(f"\n{failed} post(s) violate BLOG-PLAYBOOK.md. Fix them or justify each on the flag list.")
        return 1
    print("\nNo blocking violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
