#!/usr/bin/env python3
"""House captions for every Pain 2 Power clip: ONE implementation, used by every clip tool.

Nick, 2026-10-28: captions were "a little slow and late and they need to be a little lower ...
remember this ALWAYS for every clip from a podcast we do". The three rules:

  LATE   Whisper's word times are not where the words are: 0.2 to 0.7 s late on most clips, early
         on some. Every word of the reviewed transcript is FORCE-ALIGNED to the clip's own audio
         (wav2vec2, torchaudio MMS_FA, ~20 ms), and each cue shows LEAD s before its first syllable.
         Whisper is only used to find which stretch of the episode a clip covers.
  SLOW   At most 3 words per cue (4 felt slow), broken at clause punctuation AND at every pause
         over 0.35 s (otherwise "MRI so they" showed "so they" 2.3 s before she said it), balanced
         within each clause so there is no orphan one-word cue. Word ENDS are trimmed to the last
         voiced frame, so a cue never sits on screen through a silence.
  LOWER  MarginV 49 (PlayResY 288): box bottom at y ~1590 of 1920, the height Nick picked on a
         frame. Still above the 4:5 feed crop (y 1635), so Instagram's feed never cuts it.

Style is otherwise unchanged: Arial bold 10, white on an OPAQUE black box (BorderStyle 4,
BackColour &H00000000), one line, centred.

    from clip_captions import build_ass
    build_ass(words, audio_path_or_array, "cap.ass", dur)    # words: [{"w","s","e"}] in clip time

    python3 tools/clip_captions.py words.json clip_audio.(mp4|wav) out.ass
    python3 tools/clip_captions.py --check clean/*.ass        # house style? (stage-episode runs this)
"""
import json
import math
import re
import subprocess
import sys

import numpy as np

MAXWORDS = 3
LEAD = 0.08          # cue appears this far ahead of its first syllable, never more
MARGIN_V = 49        # box bottom ~y 1590 of 1920 (Nick, 2026-10-28)
MAX_LINE_PX = 900
PAUSE = 0.35         # a real pause always ends a cue: no word is ever shown before it is said    # at 1080 wide; a longer chunk is split further
SR = 16000

STAMP = "; built by tools/clip_captions.py v1 (aligned, <=3 words, MarginV 49)"

HEAD = f"""[Script Info]
{STAMP}
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,10,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,4,0,0,2,10,10,{MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _font():
    try:
        from PIL import ImageFont
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except Exception:
        return None


FONT = _font()


def width(s):
    return FONT.getlength(s) if FONT else len(s) * 32


def load_audio(src):
    if isinstance(src, np.ndarray):
        return src
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).astype(np.float32) / 32768


_FA = None


def _norm(t):
    t = t.lower().replace("’", "'")
    return re.sub(r"[^a-z']", "", t)


def align(words, audio):
    """Pin every word to the audio with a wav2vec2 forced aligner (torchaudio MMS_FA, CPU).

    The text is the reviewed transcript, so the aligner only has to say WHERE each word is,
    which it does to ~20 ms. Whisper's own word times were measured 0.2 to 0.7 s off (late on
    some clips, early on others), which is what "slow and late" was. Tokens with no letters
    (501c3 -> "c", 2026 -> "") align by their letters or are interpolated between neighbours.
    """
    global _FA
    import torch
    import torchaudio
    b = torchaudio.pipelines.MMS_FA
    if _FA is None:
        _FA = (b.get_model(with_star=False).eval(), b.get_tokenizer(), b.get_aligner())
    model, tok, aligner = _FA
    a = load_audio(audio)
    wav = torch.from_numpy(a.copy()).unsqueeze(0)
    keep = [i for i, w in enumerate(words) if _norm(w["w"]).replace("'", "")]
    toks = [_norm(words[i]["w"]) for i in keep]
    with torch.inference_mode():
        em, _ = model(wav)
    spans = aligner(em[0], tok(toks))
    ratio = wav.shape[1] / em.shape[1] / SR
    out = [dict(w) for w in words]
    for i, sp in zip(keep, spans):
        out[i]["s"], out[i]["e"] = sp[0].start * ratio, sp[-1].end * ratio
    for i, w in enumerate(out):                     # letterless tokens sit between neighbours
        if i not in keep:
            pe = out[i - 1]["e"] if i else 0.0
            ns = next((out[j]["s"] for j in range(i + 1, len(out)) if j in keep), pe + 0.3)
            w["s"], w["e"] = pe, max(pe + 0.05, ns)
    return _trim_ends(out, a)


def _trim_ends(words, a):
    env = np.array([np.sqrt(np.mean(a[i:i + 320] ** 2)) for i in range(0, max(1, len(a) - 320), 160)])
    db = 20 * np.log10(env + 1e-6)
    hot = db > np.percentile(db, 10) + 12
    for w in words:
        lo, hi = int(w["s"] * 100), min(len(hot), int(w["e"] * 100) + 1)
        idx = np.where(hot[lo:hi])[0]
        if len(idx):
            w["e"] = max(w["s"] + 0.1, min(w["e"], (lo + idx[-1]) / 100 + 0.12))
    return words


snap_onsets = align


def chunk(words):
    """Clauses (split at , ; : . ? ! and at every pause over PAUSE s), then balanced chunks of <= MAXWORDS that fit one line.
    A one-word clause ("Well,") joins the next one when the pair still fits in a cue."""
    raw, cur = [], []
    for k, w in enumerate(words):
        cur.append(w)
        gap = words[k + 1]["s"] - w["e"] if k + 1 < len(words) else 0
        if re.search(r"[.?!,;:]$", w["w"]) or gap > PAUSE:
            raw.append(cur)
            cur = []
    if cur:
        raw.append(cur)
    sents = []
    for c in raw:
        if sents and len(sents[-1]) == 1 and len(sents[-1]) + len(c) <= MAXWORDS:
            sents[-1] = sents[-1] + c
        else:
            sents.append(c)
    out = []
    for snt in sents:
        n = len(snt)
        k = math.ceil(n / MAXWORDS)
        while True:
            size = [n // k + (1 if i < n % k else 0) for i in range(k)]
            parts, i = [], 0
            for sz in size:
                parts.append(snt[i:i + sz])
                i += sz
            if all(width(" ".join(x["w"] for x in p)) <= MAX_LINE_PX for p in parts) or k >= n:
                break
            k += 1
        out.extend(parts)
    return out


def ts(t):
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def cues(words, audio, dur):
    C = chunk(snap_onsets(words, audio))
    out = []
    for i, c in enumerate(C):
        st = max(0.0, c[0]["s"] - LEAD)
        nxt = max(0.0, C[i + 1][0]["s"] - LEAD) if i + 1 < len(C) else dur
        en = min(nxt, c[-1]["e"] + 0.4, dur)
        en = max(en, min(st + 0.3, nxt))
        txt = " ".join(x["w"] for x in c).replace("{", "(").replace("}", ")")
        out.append((st, en, txt))
    return out


def _tidy_asr(words):
    """Whisper splits '130%' into '130', '%' and 'one-fifth' into 'one', '-fifth'; glue them back."""
    out = []
    for w in words:
        t = w["w"].strip()
        if out and re.match(r"^[%'’.,?!]|^-", t):
            out[-1] = {**out[-1], "w": out[-1]["w"] + t, "e": w["e"]}
        elif t:
            out.append({**w, "w": t})
    return out


def merge_text(asr_words, reviewed):
    """Caption words = what is SAID (Whisper's word list, so no filler the speaker said is dropped
    and the aligner never has to stretch tidied text over extra speech), spelled the way the
    REVIEWED transcript spells it wherever the two agree or nearly agree (names, numbers, case,
    punctuation: "Miklas" -> "Nicklaus"). Hyphens become spaces (zero dashes in captions)."""
    import difflib
    W = _tidy_asr(asr_words)
    R = reviewed.split()
    n = lambda t: re.sub(r"[^a-z0-9%]", "", t.lower())
    wn, rn = [n(w["w"]) for w in W], [n(t) for t in R]
    RS = [j == 0 or bool(re.search(r"[.?!][\"”')]*$", R[j - 1])) for j in range(len(R))]   # sentence starts
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wn, rn, autojunk=False).get_opcodes():
        block = [dict(w, heard=w["w"]) for w in W[i1:i2]]
        if tag == "equal":
            for k, w in enumerate(block):
                w["w"] = R[j1 + k]
                w["refstart"] = RS[j1 + k]
        elif tag == "replace" and i2 - i1 == j2 - j1:
            for k, w in enumerate(block):
                r = R[j1 + k]
                if difflib.SequenceMatcher(None, wn[i1 + k], rn[j1 + k]).ratio() >= 0.5 or r[:1].isupper() or r[:1].isdigit():
                    w["w"] = r
                    w["refstart"] = RS[j1 + k]
        elif tag == "replace" and difflib.SequenceMatcher(None, "".join(wn[i1:i2]), "".join(rn[j1:j2])).ratio() >= 0.65:
            # same letters, split differently ("public who" / "publicly"): reviewed words, ASR span
            s0, e0, m = W[i1]["s"], W[i2 - 1]["e"], j2 - j1
            block = [{"w": R[j1 + k], "s": s0 + (e0 - s0) * k / m, "e": s0 + (e0 - s0) * (k + 1) / m} for k in range(m)]
        out.extend(block)
    for w in out:
        w["w"] = re.sub(r"(?<=\w)[-–—](?=\w)", " ", w["w"]).replace(" -", " ")
    # sentence case after spoken words were inserted: "sprouts. and No matter" -> "sprouts. And no matter"
    for k, w in enumerate(out):
        after_stop = k == 0 or re.search(r"[.?!][\"”')]*$", out[k - 1]["w"])
        if after_stop and w["w"][:1].islower():
            w["w"] = w["w"][:1].upper() + w["w"][1:]
        elif not after_stop and (w["w"] in STARTERS or (w.get("refstart") and w["w"][:1].isupper()
                                                         and w.get("heard", "")[:1].islower()
                                                         and not re.match(r"I\b|I'", w["w"]))):
            # a reviewed sentence start that now sits mid-sentence; Whisper's own casing says whether
            # it is really a name ("Kerry", "Park City" stay capitalised, "That's" does not)
            w["w"] = w["w"][:1].lower() + w["w"][1:]
    return out


STARTERS = {"No", "And", "So", "But", "The", "That", "This", "It", "Well", "Yeah", "Okay", "Right", "Oh",
            "You", "We", "They", "He", "She", "If", "What", "When", "How", "Then", "There", "Now", "Just",
            "Like", "A", "An", "Is", "Was", "Or", "Because", "Not", "Thus", "Everything", "Every"}


def build_ass(words, audio, path, dur):
    cs = cues(words, audio, dur)
    open(path, "w").write(HEAD + "".join(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{t}\n" for a, b, t in cs))
    return cs


def verify_ass(path):
    """Problems with a caption file, [] when it is house style. stage-episode.py refuses a clip
    whose .ass fails this, so a hand-rolled or old-style caption file can never be staged."""
    try:
        t = open(path).read()
    except OSError as e:
        return [f"cannot read {path}: {e}"]
    errs = []
    if STAMP.split(" v")[0] not in t:
        errs.append("not built by tools/clip_captions.py (no stamp): rebuild it with build_ass()")
    m = re.search(r"^Style: Default,.*,(\d+),\d+$", t, re.M)
    if not m or int(m.group(1)) != MARGIN_V:
        errs.append(f"MarginV is {m.group(1) if m else '?'}, house style is {MARGIN_V}")
    cues = re.findall(r"^Dialogue: [^,]*,([^,]*),([^,]*),(?:[^,]*,){6}(.*)$", t, re.M)
    if not cues:
        errs.append("no cues")
    long = [x for _, _, x in cues if len(x.split()) > MAXWORDS]
    if long:
        errs.append(f"{len(long)} cue(s) over {MAXWORDS} words, e.g. {long[0]!r}")
    return errs


if __name__ == "__main__" and sys.argv[1:2] == ["--check"]:
    bad = 0
    for f in sys.argv[2:]:
        e = verify_ass(f)
        print(("PASS  " if not e else "FAIL  ") + f + "".join("\n      " + x for x in e))
        bad += bool(e)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    words, audio, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio],
                               capture_output=True, text=True).stdout)
    for a, b, t in build_ass(words, audio, out, dur):
        print(f"{a:6.2f}-{b:6.2f}  {t}")
