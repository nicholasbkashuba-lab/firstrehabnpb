#!/usr/bin/env python3
"""Cut check: no clip or sizzle line may end while someone is still talking.

Nick, 2026-10-30, on the Halloween sizzle: "the sizzle reel cuts off sentences too quickly, how can we
... ensure this does not keep happening with every clip". Measured: 9 of its 11 dialogue cuts landed
0.03 to 0.45 s BEFORE the last word finished, and two lines started mid-sentence. Nothing checked it:
the reel cut on hand-typed RAW times and the word timings were never compared against them.

This is the check, used in two places so neither path can skip it:

  * tools/sizzle/run.py calls check_cuts() on every dialogue slice the reel pulls (engine.load_audio
    records each one) BEFORE rendering, and refuses to render on a FAIL.
  * tools/clip-qa.py calls tail_check() on the finished clip file: its audio has no music, so the last
    voiced frame must sit at least MIN_TAIL before the end.

Word times are re-aligned to the audio first (wav2vec2 forced aligner, the one the captions use, ~20 ms):
Whisper's own word ends run 0.2 to 0.7 s off. Energy alone cannot decide it either: the hosts laugh and
talk over each other, so a gap rarely falls below -15 dB, while a soft ending ("thera-py") can read -22 dB.

Rules for a slice [t0, t1] of a source:
  FAIL  the aligned last word ends after t1 - 0.06 (the cut clips it), unless another slice of the same
        source starts exactly at t1 (a camera change inside continuous audio).
  FAIL  the last 60 ms before t1 are within 6 dB of the slice's speech level (cut on a voiced peak).
  FAIL  t0 lands inside the first word (it started before t0 + 0.02).
  warn  the last word has no sentence end (. ? !): the line stops mid-thought.
  warn  the slice starts mid-sentence (the word before it has no . ? ! and the gap is under 0.35 s),
        or within 0.03 s of the first word's start (the attack is clipped).
suggest() returns the nearest in/out that passes: in 0.10 s before the first word, out at the quietest
20 ms between the last word's end + 0.08 s and the next word's start (at most + 0.40 s).

    python3 tools/cut_check.py AUDIO WORDS.json IN OUT [IN OUT ...]   # check RAW slices by hand
"""
import json
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))

SR = 16000
FRAME = 0.02            # 20 ms analysis frames
MIN_TAIL = 0.12         # clip-qa: room left after the last voiced frame before a clip file ends
VOICED = 0.18           # a frame is voiced above 18% (about -15 dB) of the slice's speech level
SENT_END = (".", "?", "!")


def load(path, t0=None, dur=None):
    cmd = ["ffmpeg", "-v", "error"]
    if t0 is not None:
        cmd += ["-ss", f"{max(0.0, t0):.3f}"]
    cmd += ["-i", path]
    if dur is not None:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).astype(np.float64)


def frames_rms(x):
    n = int(FRAME * SR)
    k = len(x) // n
    if k == 0:
        return np.zeros(0)
    return np.sqrt(np.mean(x[: k * n].reshape(k, n) ** 2, axis=1) + 1e-12)


def tail_check(x, end_trim=0.0):
    """(seconds of quiet before the end, speech level). x is the slice's mono audio."""
    if end_trim:
        x = x[: max(0, len(x) - int(end_trim * SR))]
    r = frames_rms(x)
    if len(r) < 5:
        return 0.0, 0.0
    level = float(np.percentile(r, 90))
    voiced = np.nonzero(r > VOICED * level)[0]
    if len(voiced) == 0:
        return len(r) * FRAME, level
    return (len(r) - 1 - voiced[-1]) * FRAME, level


def head_check(x):
    """Seconds of quiet at the start of the slice."""
    r = frames_rms(x)
    if len(r) < 5:
        return 0.0
    level = float(np.percentile(r, 90))
    voiced = np.nonzero(r > VOICED * level)[0]
    return (voiced[0] * FRAME) if len(voiced) else len(r) * FRAME


def _w(w):
    return w["w"].strip()


_CACHE = {}


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _int_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _int_words(n % 100))
    if n < 1000000:
        return _int_words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + _int_words(n % 1000))
    return " ".join(_ONES[int(c)] for c in str(n))


def spoken(tok):
    """A token as it is said, for the aligner only: '100.3' -> 'one hundred point three', '10,000' -> 'ten
    thousand', '50%' -> 'fifty percent'. Tokens with letters come back unchanged."""
    import re
    if re.search(r"[A-Za-z]", tok):
        return tok
    t = tok.replace(",", "").strip(".?!:;\"'")
    m = re.fullmatch(r"\$?(\d+)(?:\.(\d+))?(%?)", t)
    if not m:
        return tok
    out = _int_words(int(m.group(1)))
    if m.group(2):
        out += " point " + " ".join(_ONES[int(c)] for c in m.group(2))
    if m.group(3):
        out += " percent"
    return out


def aligned_window(path, words, t0, t1, before=1.0, after=1.5):
    """Transcript words around [t0, t1], re-timed by the wav2vec2 forced aligner (tools/clip_captions.align,
    ~20 ms). Whisper's own word ends are 0.2 to 0.7 s off, too loose to say whether a cut clips a word."""
    key = (path, round(t0, 2), round(t1, 2))
    if key in _CACHE:
        return _CACHE[key]
    import clip_captions as CC
    a0 = max(0.0, t0 - before)
    ws = [dict(w=w["w"].strip(), s=w["s"] - a0, e=w["e"] - a0) for w in words if a0 <= w["s"] < t1 + after]
    if not ws:
        return []
    x = load(path, a0, (t1 + after) - a0 + 1.2).astype(np.float32)   # room past the last word, or it is squeezed in
    said = [dict(w, w=spoken(w["w"])) for w in ws]          # "100.3" has no letters to align: say it
    out = [dict(w, w=o["w"], s=w["s"] + a0, e=w["e"] + a0) for w, o in zip(CC.align(said, x), ws)]
    _CACHE[key] = out
    return out


def word_problems(words, t0, t1, tail_continues=False, head_continues=False):
    """Words must already be aligned (aligned_window)."""
    fails, warns = [], []
    inside = [w for w in words if w["s"] < t1 - 0.02 and w["e"] > t0 + 0.02]
    if not inside:
        return fails, warns
    last, first = inside[-1], inside[0]
    if not tail_continues:
        if not re.search(r"[A-Za-z]", _w(last)):
            pass                    # numbers align badly ("100.3" lands on the next word): the energy test decides
        elif last["e"] > t1 - 0.06:
            fails.append(f"cut at {t1:.2f} while '{_w(last)}' is still being said (it ends {last['e']:.2f})")
        elif not _w(last).endswith(SENT_END):
            warns.append(f"ends mid-sentence on '{_w(last)}'")
    if not head_continues:
        if first["s"] < t0 + 0.02:
            fails.append(f"starts at {t0:.2f} inside '{_w(first)}' (it starts {first['s']:.2f})")
        prev = [w for w in words if w["e"] <= first["s"] + 0.01 and w["s"] < first["s"]]
        if prev and not _w(prev[-1]).endswith(SENT_END) and first["s"] - prev[-1]["e"] < 0.35:
            warns.append(f"starts mid-sentence at '{_w(first)}' (after '{_w(prev[-1])}')")
    return fails, warns


def suggest(words, t0, t1, audio_path=None):
    """Nearest passing (in, out): in 0.10 s before the first word, out in the quietest 20 ms between the last
    word's end + 0.08 s and the next word's start (at most + 0.40 s). Words are re-aligned when audio is given."""
    if audio_path:
        words = aligned_window(audio_path, words, t0, t1)
    inside = [w for w in words if w["s"] < t1 - 0.02 and w["e"] > t0 + 0.02]
    if not inside:
        return t0, t1
    first, last = inside[0], inside[-1]
    prev = [w for w in words if w["e"] <= first["s"] + 0.01 and w["s"] < first["s"]]
    nxt = [w for w in words if w["s"] >= last["e"] - 0.01 and w["s"] > last["s"]]
    a = first["s"] - 0.10
    if prev:
        a = max(a, prev[-1]["e"] + 0.02)
    lo = last["e"] + 0.08
    hi = min((nxt[0]["s"] - 0.04) if nxt else last["e"] + 0.40, last["e"] + 0.40)
    if hi <= lo:
        return round(a, 2), round(lo, 2)
    b = hi
    if audio_path:
        r = frames_rms(load(audio_path, lo, hi - lo))
        if len(r):
            b = lo + float(np.argmin(r)) * FRAME + FRAME / 2
    return round(a, 2), round(b, 2)


def check_cuts(cuts, src, words=None):
    """cuts: [(key, t0, t1)] in reel order; src: key -> audio path; words: key -> transcript word list.
    Returns [(cut, fails, warns, end_db)]. A slice another slice of the same source continues from (or into)
    is a camera change inside continuous audio, so that edge is not checked."""
    out = []
    for key, t0, t1 in cuts:
        tail_cont = any(k == key and abs(a - t1) < 0.02 for k, a, _ in cuts)
        head_cont = any(k == key and abs(b - t0) < 0.02 for k, _, b in cuts)
        fails, warns, end_db = [], [], None
        r = frames_rms(load(src[key], t0, t1 - t0))
        if len(r) > 5 and not tail_cont:
            end_db = float(20 * np.log10(np.mean(r[-3:]) / np.percentile(r, 90)))
            if end_db > -6:
                fails.append(f"the last 60 ms before {t1:.2f} are at full speech level ({end_db:.0f} dB): mid-word")
        ws = (words or {}).get(key)
        if ws:
            f2, w2 = word_problems(aligned_window(src[key], ws, t0, t1), t0, t1, tail_cont, head_cont)
            fails += f2
            warns += w2
        out.append(((key, t0, t1), fails, warns, end_db))
    return out


def main():
    a = sys.argv[1:]
    if len(a) < 4 or len(a) % 2:
        sys.exit(__doc__)
    audio, words = a[0], json.load(open(a[1]))
    pairs = [(float(a[i]), float(a[i + 1])) for i in range(2, len(a), 2)]
    res = check_cuts([("src", s, e) for s, e in pairs], {"src": audio}, {"src": words})
    bad = 0
    for (k, s, e), fails, warns, q in res:
        bad += bool(fails)
        print(f"{'FAIL' if fails else 'PASS'}  {s:.2f}-{e:.2f}")
        for m in fails:
            print(f"      FAIL  {m}")
        for m in warns:
            print(f"      warn  {m}")
        if fails or warns:
            print(f"      suggest {suggest(words, s, e, audio)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
