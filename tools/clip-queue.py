#!/usr/bin/env python3
"""One mixed clip queue across every Pain 2 Power episode.

Replaces "one episode owns one week" (Nick, 2026-09-18). That rule produced a
solid block of one guest: six consecutive days of Susan Mann in a 5 PM lane while
a separate 9 AM lane ran Captain Kerry four times in eight days. Same guest back
to back reads as a broadcast, not a feed.

This schedules ONE clip a day from a single pool of every unposted clip, with one
hard rule: never two clips from the same guest on consecutive days.

WHY THIS IS NOT A POST BRIDGE CLIENT: Post Bridge is only reachable through MCP
tools inside a Claude session, not over a plain HTTP key a script could hold. So
this file owns the scheduling MATHS and the queue STATE; the session (or the
daily routine) reads the plan and applies it with create_post/update_post, then
calls `mark` to record what landed. Keeping the arithmetic here means the order
is reviewable and reproducible instead of re-improvised every week.

Usage:
  python3 tools/clip-queue.py import   --posts <list_posts.json> [--write]
  python3 tools/clip-queue.py plan     --days 30 [--start 2026-09-20] [--json]
  python3 tools/clip-queue.py mark     --clip <post_id> --state posted
  python3 tools/clip-queue.py audit    --posts <list_posts.json>
"""

import argparse
import datetime as dt
import json
import os
import random
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "content", "clip-queue.json")

# The one daily slot, in UTC. 13:00 UTC is 9:00 AM ET during daylight time.
# NOTE: this is a fixed UTC hour, so it drifts to 8:00 AM ET when the US leaves
# DST in November. Re-check it then rather than assuming it tracks ET.
SLOT_HOUR_UTC = 13
SLOT_MINUTE = 0

# First Rehabilitation's accounts. Everything else in a Post Bridge dump belongs
# to another client and must never be pulled into this queue.
FIRST_REHAB_ACCOUNTS = {81353, 81324, 81358, 81356, 81378, 81322, 81642}

# A clip is a vertical video, so it always targets TikTok and/or YouTube. The
# announcement photo and the Saturday link post never do -- they go to the feed
# and Google Business accounts instead. That is what separates a clip from the
# rest of the week without needing the media's MIME type, which the Post Bridge
# listing does not carry.
VIDEO_ACCOUNTS = {81358, 81356}

# Guest attribution, by what the caption actually says. Order matters: the first
# pattern that hits wins, so the named guest beats the generic host patterns.
# A clip nobody matches is reported, not silently filed under a host.
GUEST_PATTERNS = [
    ("Susan Mann", r"Susan Mann|Bright Minds|processing disorder|Coach Carter"),
    ("Captain Kerry", r"Captain Kerry|Below Deck"),
    ("Dr. Chaim Arlosoroff", r"Arlosoroff|e bike|e-bike|electric bike"),
    ("Paul Joyce", r"Paul Joyce|New Life HRT|peptide|Wolverine stack|BPC-157"),
    ("Dave and Mike", r"Dave Kashuba|Mike McGann|Pain 2 Power"),
]

# A fresh episode should still get a push rather than queueing behind a guest who
# simply has more clips banked. This multiplies the newest guest's priority when
# picking who goes next; it never overrides the no-back-to-back rule.
NEW_GUEST_BOOST = 1.6

# Seeded so the same inputs always produce the same calendar. A schedule you
# cannot reproduce is a schedule you cannot review.
SEED = 20260918


# --------------------------------------------------------------------------
# state
# --------------------------------------------------------------------------

def load_queue():
    if not os.path.exists(QUEUE):
        return {"clips": []}
    with open(QUEUE) as fh:
        return json.load(fh)


def save_queue(q):
    os.makedirs(os.path.dirname(QUEUE), exist_ok=True)
    with open(QUEUE, "w") as fh:
        json.dump(q, fh, indent=2)
        fh.write("\n")
    print(f"wrote {os.path.relpath(QUEUE, ROOT)}  ({len(q['clips'])} clips)")


def classify(caption):
    for guest, pattern in GUEST_PATTERNS:
        if re.search(pattern, caption, re.I):
            return guest
    return None


def hook_of(caption):
    """The first line, which is the clip's hook and how a human recognises it."""
    return caption.strip().split("\n")[0][:90]


# --------------------------------------------------------------------------
# import
# --------------------------------------------------------------------------

def read_dump(path):
    with open(path) as fh:
        data = json.load(fh)
    return data["data"] if isinstance(data, dict) and "data" in data else data


def cmd_import(args):
    posts = read_dump(args.posts)
    q = load_queue()
    known = {c["post_id"]: c for c in q["clips"]}

    added, skipped, unmatched = [], 0, []
    for p in posts:
        if not set(p.get("social_accounts") or []) & FIRST_REHAB_ACCOUNTS:
            continue
        media = p.get("media") or []
        if not media or not set(p["social_accounts"]) & VIDEO_ACCOUNTS:
            # Not a clip: no media at all, or a photo/link post aimed at the
            # feed and Google Business rather than TikTok and YouTube.
            continue
        cap = p.get("caption", "")
        guest = classify(cap)
        if guest is None:
            unmatched.append((p["id"][:8], hook_of(cap)))
            continue
        if p["id"] in known:
            skipped += 1
            continue
        added.append({
            "post_id": p["id"],
            "guest": guest,
            "media": media[0],
            "hook": hook_of(cap),
            "state": "posted" if p.get("status") == "posted" else "queued",
            "was_scheduled_at": p.get("scheduled_at"),
        })

    q["clips"].extend(added)
    print(f"{len(added)} new, {skipped} already known, {len(unmatched)} unclassified")
    for pid, hook in unmatched:
        print(f"  UNCLASSIFIED {pid}  {hook}")

    by_guest = defaultdict(int)
    for c in q["clips"]:
        if c["state"] not in ("posted", "killed"):
            by_guest[c["guest"]] += 1
    print("\nunposted clips by guest:")
    for guest, n in sorted(by_guest.items(), key=lambda kv: -kv[1]):
        print(f"  {n:3d}  {guest}")

    if args.write:
        save_queue(q)
    else:
        print("\n(dry run -- pass --write to save)")


# --------------------------------------------------------------------------
# plan
# --------------------------------------------------------------------------

def interleave(clips, newest_guest=None):
    """Order clips so no two from the same guest are adjacent.

    Greedy largest-remaining-first, excluding whoever went last. That is the
    standard rearrangement approach and it succeeds whenever a valid order
    exists at all -- which is exactly when no guest holds more than half the
    pool (rounded up).
    """
    rng = random.Random(SEED)
    pools = defaultdict(list)
    for c in clips:
        pools[c["guest"]].append(c)
    for guest in pools:
        rng.shuffle(pools[guest])

    total = len(clips)
    biggest = max((len(v) for v in pools.values()), default=0)
    feasible = biggest <= (total + 1) // 2

    order, last = [], None
    while any(pools.values()):
        options = [g for g, v in pools.items() if v and g != last]
        if not options:
            # Only the previous guest has clips left. Everything else is spent,
            # so the tail unavoidably repeats -- say so rather than hiding it.
            options = [g for g, v in pools.items() if v]
        def priority(g):
            boost = NEW_GUEST_BOOST if g == newest_guest else 1.0
            return (len(pools[g]) * boost, rng.random())
        pick = max(options, key=priority)
        order.append(pools[pick].pop())
        last = pick

    return order, feasible


def cmd_plan(args):
    q = load_queue()
    # "killed" is deliberate removal and "posted" is spent. Only these two are
    # excluded -- everything else is still owed a slot.
    pending = [c for c in q["clips"] if c["state"] not in ("posted", "killed")]
    if not pending:
        sys.exit("nothing queued")

    newest = args.boost
    order, feasible = interleave(pending, newest_guest=newest)

    if args.start:
        day = dt.date.fromisoformat(args.start)
    else:
        day = dt.datetime.now(dt.timezone.utc).date() + dt.timedelta(days=1)

    plan = []
    for clip in order[: args.days]:
        when = dt.datetime.combine(
            day, dt.time(SLOT_HOUR_UTC, SLOT_MINUTE), tzinfo=dt.timezone.utc
        )
        plan.append({**clip, "scheduled_at": when.strftime("%Y-%m-%dT%H:%M:%SZ")})
        day += dt.timedelta(days=1)

    if args.json:
        print(json.dumps(plan, indent=2))
        return

    print(f"{len(plan)} slots, one a day at {SLOT_HOUR_UTC:02d}:{SLOT_MINUTE:02d} UTC\n")
    prev = None
    for row in plan:
        clash = "  <-- SAME GUEST AS YESTERDAY" if row["guest"] == prev else ""
        date = row["scheduled_at"][:10]
        weekday = dt.date.fromisoformat(date).strftime("%a")
        print(f"  {date} {weekday}  {row['guest']:<22} {row['hook'][:58]}{clash}")
        prev = row["guest"]

    if not feasible:
        counts = defaultdict(int)
        for c in pending:
            counts[c["guest"]] += 1
        worst, n = max(counts.items(), key=lambda kv: kv[1])
        print(
            f"\nWARNING: {worst} holds {n} of {len(pending)} clips, more than half."
            "\n  A perfect alternation is impossible; the tail will repeat."
            "\n  Cut some of that guest's weaker clips, or bank them for later."
        )
    if len(plan) < args.days:
        print(f"\nOnly {len(plan)} clips available for {args.days} requested days.")


# --------------------------------------------------------------------------
# mark / audit
# --------------------------------------------------------------------------

def cmd_mark(args):
    q = load_queue()
    hits = [c for c in q["clips"] if c["post_id"].startswith(args.clip)]
    if not hits:
        sys.exit(f"no clip matching {args.clip}")
    if len(hits) > 1:
        sys.exit(f"{args.clip} is ambiguous ({len(hits)} matches)")
    hits[0]["state"] = args.state
    if args.scheduled_at:
        hits[0]["scheduled_at"] = args.scheduled_at
    print(f"{hits[0]['post_id'][:8]} -> {args.state}  {hits[0]['hook'][:50]}")
    save_queue(q)


def cmd_audit(args):
    """Check what Post Bridge actually holds against the no-repeat rule."""
    posts = read_dump(args.posts)
    rows = []
    for p in posts:
        if not set(p.get("social_accounts") or []) & FIRST_REHAB_ACCOUNTS:
            continue
        if not p.get("scheduled_at") or not p.get("media"):
            continue
        if not set(p["social_accounts"]) & VIDEO_ACCOUNTS:
            continue
        rows.append((p["scheduled_at"], p["id"][:8], p["media"][0],
                     classify(p.get("caption", "")) or "?",
                     hook_of(p.get("caption", ""))))
    rows.sort()

    problems = 0
    seen_media = {}
    by_day = defaultdict(list)
    for when, pid, media, guest, hook in rows:
        by_day[when[:10]].append((pid, guest, hook, when[11:16]))
        if media in seen_media:
            print(f"  DUPLICATE MEDIA {media[:8]}: {seen_media[media]} and {pid} "
                  f"are the same clip scheduled twice")
            problems += 1
        seen_media[media] = pid

    prev_guest, prev_day = None, None
    for day in sorted(by_day):
        entries = by_day[day]
        if len(entries) > 1:
            print(f"  {day}: {len(entries)} clips in one day "
                  f"({', '.join(e[3] for e in entries)})")
            problems += 1
        guest = entries[0][1]
        if prev_day and guest == prev_guest and \
                (dt.date.fromisoformat(day) - dt.date.fromisoformat(prev_day)).days == 1:
            print(f"  {day}: {guest} again, straight after {prev_day}")
            problems += 1
        prev_guest, prev_day = guest, day

    horizon = dt.date.today() + dt.timedelta(days=120)
    for when, pid, _m, guest, hook in rows:
        if dt.date.fromisoformat(when[:10]) > horizon:
            print(f"  {when[:10]}: {pid} is more than 120 days out -- "
                  f"almost certainly a typo. {hook[:50]}")
            problems += 1

    print(f"\n{len(rows)} scheduled clips, {problems} problems")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("import", help="build the queue from a Post Bridge dump")
    p.add_argument("--posts", required=True)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("plan", help="assign clips to daily slots")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--start", help="first slot date, YYYY-MM-DD (default tomorrow)")
    p.add_argument("--boost", help="guest to favour early, e.g. the newest episode")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("mark", help="record a clip's state")
    p.add_argument("--clip", required=True, help="post id or unique prefix")
    p.add_argument("--state", required=True,
                   choices=["queued", "scheduled", "posted", "killed"])
    p.add_argument("--scheduled-at")
    p.set_defaults(func=cmd_mark)

    p = sub.add_parser("audit", help="find problems in what is already scheduled")
    p.add_argument("--posts", required=True)
    p.set_defaults(func=cmd_audit)

    args = ap.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
