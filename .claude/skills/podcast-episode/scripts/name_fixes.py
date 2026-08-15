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

    # Episode 6.
    (r"\bpoaching my son's baseball\b", "coaching my son's baseball"),
    (r"\bdrive Weiner\b", "Dr. Weiner"),
    (r"\bAdls\b", "ADLs"),

    # Episode 7. ASR heard "Elkhechen" four ways and "Rami" as "Romney".
    (r"\b(?:El|Al)\s?Catch(?:ens|ins|in|en|es)?\b", "Elkhechen"),
    (r"\bRomney\b", "Rami"),
    (r"\bNYU Lingo\b", "NYU Langone"),
    (r"\bcounter ?sites\b", "chondrocytes"),

    # Episode 10 — Dr. McVicker. ASR gave four spellings of one surgeon and
    # four of his practice. All observed in the real transcript, not guessed.
    (r"\bMck?[vf]i(?:ck|g|k)er\b", "McVicker"),
    (r"\bMc ?Vicar\b", "McVicker"),
    (r"\bMc ?Vickar\b", "McVicker"),
    (r"\bMick ?Vicker\b", "McVicker"),
    # ASR invented a surname AND a practice out of "McVicker at Paley".
    (r"\bMcPherter\b", "McVicker"),
    (r"\bFamily Orthopedic\b", "Paley Orthopedic"),
    (r"\bPaleorthopedic\b", "Paley Orthopedic"),
    (r"\b(?:Pelley|Haley|Paleo|Pale)\b(?=\s*(?:Institute|Orthop))", "Paley"),
    # Clinical terms. A mangled diagnosis in a burned-in caption is worse than
    # no caption, and these are the episode's subject matter.
    (r"\bfemoral acetabular\b", "femoroacetabular"),
    (r"\bastabulum\b", "acetabulum"),
    (r"\bpincer legion\b", "pincer lesion"),
    (r"\bcaught on Aquina\b", "cauda equina"),
    (r"\bcue angle\b", "Q angle"),
    # "groin pain" is the episode's single most important phrase and ASR heard
    # "growing pain" throughout.
    (r"\bgrowing pain\b", "groin pain"),
    (r"\bthe camp side\b", "the cam side"),
    # The clinic's own name and domain. A wrong domain in a caption sends
    # viewers to a dead address, so this one really matters.
    (r"firstrehabnpv\.com", "firstrehabnpb.com"),
    (r"\bFirst Real Rehabilitation of Palm Beach\b",
     "First Rehabilitation of North Palm Beach"),
    (r"\bpublic's line\b", "Publix line"),

    # Hosts and the show itself.
    (r"\bPain[s]? (?:to|of) Power\b", "Pain 2 Power"),
    (r"\bFame to Power\b", "Pain 2 Power"),
    (r"\bCashuba\b", "Kashuba"),
    (r"\bKachuba\b", "Kashuba"),
    (r"\bMike McGahn\b", "Mike McGann"),
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
