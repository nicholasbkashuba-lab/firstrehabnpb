#!/usr/bin/env python3
"""The one ASR corrections list for Pain 2 Power.

ASR mangles guest names badly and a burned-in caption cannot be fixed after the
fact, so corrections belong in one place that every episode inherits. This list
was previously duplicated across tools/stage-episode.py and
tools/ep9-bonus-spec.py, which meant a fix in one did not reach the other.

Add each new guest's mishearings here when their episode is cut. Order matters
only where one pattern would otherwise swallow another.

Usage:
    import sys; sys.path.insert(0, f"{SKILL_DIR}/scripts")
    from name_fixes import fix
    clean = fix(raw_asr_text)
"""
import re

# (pattern, replacement). Applied case-insensitively, in order.
NAME_FIXES = [
    # Episode 9 — Dr. Vani Sabesan
    (r"\bSebastian\b", "Sabesan"),
    (r"\bSabas(i|)an\b", "Sabesan"),
    (r"\bSebasan\b", "Sabesan"),
    (r"\bVanny\b", "Vani"),
    (r"\bVonnie\b", "Vani"),
    (r"\bBonnie\b", "Vani"),
    (r"\bVanni\b", "Vani"),
    (r"\bnot less sutures\b", "knotless sutures"),
    (r"\bsubscapularies\b", "subscapularis"),

    # Episode 10 — Dr. Zack McVicker.
    # Seeded from how ASR handles the name generally; confirm against the real
    # transcript when it lands and prune whatever never actually appears.
    (r"\bMc ?Vicar\b", "McVicker"),
    (r"\bMc ?Vickar\b", "McVicker"),
    (r"\bMc ?Vicker\b", "McVicker"),
    (r"\bMick ?Vicker\b", "McVicker"),
    (r"\bMcVikker\b", "McVicker"),
    (r"\bZach McVicker\b", "Zack McVicker"),

    # Hosts and the show itself, which ASR also gets wrong.
    (r"\bPain to Power\b", "Pain 2 Power"),
    (r"\bKashuba\b", "Kashuba"),
    (r"\bCashuba\b", "Kashuba"),
    (r"\bKachuba\b", "Kashuba"),
]

_COMPILED = [(re.compile(p, re.I), r) for p, r in NAME_FIXES]


def fix(text: str) -> str:
    """Apply every correction and collapse whitespace."""
    for pat, rep in _COMPILED:
        text = pat.sub(rep, text)
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    import sys
    sys.stdout.write(fix(sys.stdin.read()) + "\n")
