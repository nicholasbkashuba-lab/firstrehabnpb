#!/usr/bin/env python3
"""Build the Episode 9 bonus-clip spec: cut ranges + burned-caption .ass files.

Times are SHOW time (transcript_v4.json). The render seeks the guest camera at
show_time + CAM_OFFSET, measured by cross correlating two known clips against
the camera audio (-83.20s and -83.10s, 22 minutes apart, so no drift).
"""
import json, os, re, textwrap

CAM_OFFSET = -83.15          # guest camera (rootA) time = show time + this
PRE, POST = 0.35, 0.45
# 56pt DejaVu Sans Bold in 1080 wide with 60px margins fits about 26 chars
WRAP = 26       # breathing room either side

# ASR corrections. NAME_FIXES from tools/stage-episode.py plus two this episode.
FIXES = [
    (r"\bSebastian\b", "Sabesan"), (r"\bSebasan\b", "Sabesan"),
    (r"\bBonnie\b", "Vani"), (r"\bVanny\b", "Vani"), (r"\bVanni\b", "Vani"),
    # context is Palm Beach, "people in my neighbourhood", an aging active
    # population and competitive play. Six is an ASR slip for sixty.
    (r"\ba six-year-old\b", "a sixty year old"),
    (r"\bsix-year-old\b", "sixty year old"),
    # she is describing her own practice, not a third party
    (r"\bThe guy started using knotless\b", "I started using knotless"),
]

# head_drop removes a trailing fragment of the previous thought from the FIRST
# caption when the cut starts mid segment. ASR segments do not break on
# sentences, so without this a clip opens on half a sentence, which CLAUDE.md
# already identifies as the main thing holding clip reach back.
CLIPS = [
    ("11-reps-in-the-or",     341.10, 360.00, r"^what you do, how you do it with that\.\s*"),
    ("12-we-listen-more",     320.00, 334.60, None),
    ("13-no-two-alike",       453.60, 472.10, None),
    ("14-self-healing",       922.80, 966.00, None),
    ("15-tech-for-techs-sake", 966.90, 983.70, None),
    ("16-good-as-the-user",  1035.60, 1048.30, None),
    ("17-knotless-heresy",   1061.50, 1074.60, None),
    # the run-up here is badly transcribed cross talk ("you ran 28 oh yeah
    # yeah I"). Start on the story itself instead.
    ("19-28-marathons",      1456.20, 1469.00, r"^won one and\s*"),
    ("18-six-days-a-week",   1234.40, 1246.20, None),
    ("20-ninety-year-old",   1484.00, 1517.30, None),
]

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,56,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,60,60,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def fix(t):
    for pat, rep in FIXES:
        t = re.sub(pat, rep, t)
    return re.sub(r"\s+", " ", t).strip()


def ass_time(t):
    if t < 0:
        t = 0.0
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def main():
    segs = json.load(open("transcript_v4.json"))
    os.makedirs("spec/ass", exist_ok=True)
    out = []

    for name, a, b, head_drop in CLIPS:
        s0, s1 = a - PRE, b + POST
        lines, texts = [], []
        first = True
        for sg in segs:
            if sg["e"] <= s0 or sg["s"] >= s1:
                continue
            t = fix(sg["t"])
            if first and head_drop:
                cut = re.sub(head_drop, "", t, flags=re.I)
                if cut != t:
                    t = cut[:1].upper() + cut[1:]   # it is a sentence start now
            if not t:
                continue
            st = max(sg["s"], s0) - s0
            en = min(sg["e"], s1) - s0
            # a sub-second sliver at either edge just flashes on screen, and at
            # the tail it is usually a half sentence bleeding in from the next
            # speaker. Drop it rather than burn it in.
            if en - st < 0.7:
                continue
            # Two lines max is the house style, but a long segment cannot be
            # squeezed into two lines without either overflowing (libass then
            # re-wraps it into three, which is what shipped the first time) or
            # truncating words. Split it into consecutive events instead and
            # divide the segment's time between them by character count.
            wrapped = textwrap.wrap(t, width=WRAP, break_long_words=False)
            chunks = [wrapped[i:i + 2] for i in range(0, len(wrapped), 2)] or [[t]]
            span = en - st
            total = sum(len(" ".join(c)) for c in chunks) or 1
            cur = st
            for ch in chunks:
                share = span * (len(" ".join(ch)) / total)
                body = r"\N".join(w.strip() for w in ch)
                lines.append(
                    f"Dialogue: 0,{ass_time(cur)},{ass_time(min(cur + share, en))},"
                    f"Cap,,0,0,0,,{body}")
                cur += share
            texts.append(t)
            first = False

        with open(f"spec/ass/{name}.ass", "w") as f:
            f.write(ASS_HEAD + "\n".join(lines) + "\n")

        out.append({
            "name": name,
            "show_start": round(s0, 2),
            "show_end": round(s1, 2),
            "cam_start": round(s0 + CAM_OFFSET, 3),
            "dur": round(s1 - s0, 2),
            "text": " ".join(texts),
        })
        print(f"{name:24s} show {s0:7.2f}-{s1:7.2f}  cam {s0+CAM_OFFSET:8.2f}  "
              f"{s1-s0:5.1f}s  {len(lines):2d} caption lines")

    json.dump(out, open("spec/clips.json", "w"), indent=1)
    print(f"\ntotal {sum(c['dur'] for c in out):.0f}s across {len(out)} clips")


if __name__ == "__main__":
    main()
