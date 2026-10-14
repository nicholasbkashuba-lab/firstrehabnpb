"""Dave's Dad Jokes: one vertical clip per joke (Reels, TikTok, Shorts).

Each joke is a list of source segments (dead air and side chatter cut out). Segments are
split at the master's real camera switches (found with ffmpeg scdet) so every sub-shot
gets the framing for whoever is actually on screen. Captions come from a medium.en
pass over each joke window (aud/joke_words.json in the work dir), with disfluencies
dropped by timestamp and a few words corrected. The punchline gets a flash, a punch-in
and a rimshot; the clip ends on a "new dad joke every Saturday" card.

    python3 run.py reel_joke_grape 9x16
"""
import json
import os

import synth as S
import engine as E
from engine import load_audio, INSET16
from lib import *
from lib import _M11, _M14, _M15, _D14, _D15, _D16, _M16

_V = lambda **k: {"9x16": dict(k, z=k.get("z", 1.0))}
D11 = dict(src="ep11", fx=0.53, fy=0.6, z=2.0, **_V(fx=0.57, fy=0.6, z=1.6))
G15 = dict(src="ep15", fx=0.4, fy=0.45, z=1.2, **_V(fx=0.4, fy=0.45))
D9 = dict(src="ep9", fx=0.68, fy=0.45, z=1.3, **_V(fx=0.68, fy=0.45, z=1.45))
M9 = dict(src="ep9", fx=0.22, fy=0.45, z=1.3, **_V(fx=0.22, fy=0.45))
W9 = dict(src="ep9", fx=0.5, fy=0.45, z=1.0, **_V(fx=0.5, fy=0.45))

END = 2.6  # end card
MAX_GAP = 0.3   # pauses longer than this inside a line are cut (owner: the grape clip dragged)
MIN_PIECE = 0.9  # never leave a jump-cut piece shorter than this; it reads as a glitch
PAD = 0.09      # breath kept either side of a cut


def tighten(ep, a, b, max_gap=MAX_GAP, lead=0.12, tail=0.15):
    """Split [a, b] into speech pieces, cutting pauses longer than max_gap.

    Pauses come from the audio, not the ASR: whisper stretches word end-times across
    silences. 20 ms RMS frames on the 16 kHz mono mix; silence is below 20% of the
    segment's 95th-percentile level after 60 ms smoothing; louder blips shorter than
    80 ms (breaths, a cough, a chair) still count as silence."""
    import numpy as np
    import soundfile as sf
    sr = 16000
    x, _ = sf.read(os.path.join(E.SCR, "aud", f"{ep}_16k.wav"), dtype="float32",
                   start=int(a * sr), stop=int(b * sr))
    hop = sr // 50
    n = len(x) // hop
    if n < 3:
        return [(a, b)]
    rms = np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1))
    rms = np.convolve(rms, np.ones(3) / 3, mode="same")
    loud = rms > 0.2 * np.percentile(rms, 95)
    i = 0
    while i < n:                      # drop speech runs shorter than 4 frames
        if loud[i]:
            j = i
            while j < n and loud[j]:
                j += 1
            if j - i < 4:
                loud[i:j] = False
            i = j
        else:
            i += 1
    idx = np.flatnonzero(loud)
    if not len(idx):
        return [(a, b)]
    t = lambda i: a + i * hop / sr
    start = max(a, t(idx[0]) - lead)
    end = min(b, t(idx[-1] + 1) + tail)
    pieces, p0 = [], start
    gap_min = int(max_gap * 50)
    run = 0
    for i in range(idx[0], idx[-1] + 1):
        if not loud[i]:
            run += 1
            continue
        if run > gap_min:
            g0, g1 = t(i - run), t(i)
            pieces.append((p0, g0 + PAD))
            p0 = g1 - PAD
        run = 0
    pieces.append((p0, end))
    # A piece shorter than MIN_PIECE merges into the neighbour across the SMALLER pause,
    # so the long pauses (the ones that drag) are still the ones that get cut.
    ps = [list(p) for p in pieces]
    while len(ps) > 1:
        lens = [p[1] - p[0] for p in ps]
        i = min(range(len(ps)), key=lambda k: lens[k])
        if lens[i] >= MIN_PIECE:
            break
        gl = ps[i][0] - ps[i - 1][1] if i > 0 else 1e9
        gr = ps[i + 1][0] - ps[i][1] if i + 1 < len(ps) else 1e9
        j = i - 1 if gl <= gr else i + 1
        lo, hi = min(i, j), max(i, j)
        ps[lo:hi + 1] = [[ps[lo][0], ps[hi][1]]]
    return [(float(x0), float(x1)) for x0, x1 in ps]

# cams: [(from_t, framing)] in source time; the last entry at or before t wins.
JOKES = {
    "grape": dict(
        ep="ep16", label="EP 16", cams=[(0, _D16), (1487.87, _M16)],
        segs=[(1459.1, 1464.0), (1474.45, 1481.95), (1483.55, 1487.95), (1489.6, 1490.85, "punch"),
              (1490.85, 1496.9)],
        drop=[1460.28, 1463.92, 1481.92, 1495.70, 1495.96, 1496.84],
        fix={1459.16: "Every", 1460.10: "while,", 1474.62: "There's", 1463.52: "joke.", 1477.06: "there,", 1481.62: "press.",
             1483.66: "What", 1487.64: "press?", 1489.76: "He", 1490.22: "whined.", 1493.18: "All",
             1493.68: "right.", 1495.48: "what,", 1496.66: "though."}),
    "lawsuit": dict(
        ep="ep14", label="EP 14", cams=[(0, _D14), (1468.33, _M14), (1471.83, _D14), (1497.83, _M14)],
        segs=[(1453.7, 1466.65), (1466.8, 1471.95), (1480.25, 1489.0), (1491.1, 1493.85),
              (1496.5, 1497.85, "punch"), (1497.85, 1499.2), (1505.7, 1510.6)],
        drop=[1453.78, 1486.20, 1496.24, 1496.34],
        fix={1453.96: "There", 1466.10: "amputated.", 1466.92: "Now", 1471.76: "fine.", 1480.36: "When",
             1488.86: "it.", 1491.22: "He", 1496.62: "He", 1498.68: "God."}),
    "bossy": dict(
        ep="ep11", label="EP 11", cams=[(0, D11), (1610.03, _M11)],
        segs=[(1594.6, 1599.95), (1600.85, 1603.1), (1604.7, 1608.85, "punch"), (1610.0, 1613.75, "sting")],
        drop=[], fix={1594.78: "The bartender"}),
    "breakthrough": dict(
        ep="ep15", label="EP 15", cams=[(0, _M15), (1555.90, _D15), (1575.07, G15), (1578.27, _D15)],
        segs=[(1551.2, 1559.6), (1559.95, 1570.3), (1570.4, 1586.3), (1586.9, 1595.25, "punch")],
        drop=[1559.68, 1567.50, 1571.44, 1571.64, 1571.90, 1572.60, 1572.76, 1587.68],
        fix={1567.48: "Which", 1588.04: "What"}),
    "kilometer": dict(
        ep="ep9", label="EP 9", cams=[(0, D9), (1573.93, W9), (1576.40, D9), (1586.4, M9), (1587.13, W9),
                                      (1589.57, M9)],
        segs=[(1558.5, 1570.65), (1575.95, 1579.35), (1580.6, 1586.4, "punch"), (1586.4, 1589.5)],
        drop=[(1558.58, "and"), 1562.12, 1567.22, 1579.22],
        fix={(1558.58, "I"): "I", 1578.86: "un-American.", 1581.08: "bartender's"}),
}


def _words(ep):
    path = os.path.join(E.SCR, "aud", "joke_words.json")
    return json.load(open(path))[ep]


def build(key):
    J = JOKES[key]
    ep = J["ep"]
    words = _words(ep)
    def _key(k):
        return (round(k[0], 2), k[1]) if isinstance(k, tuple) else round(k, 2)
    drop = {_key(x) for x in J["drop"]}
    fix = {_key(k): v for k, v in J["fix"].items()}

    def cam_at(t):
        f = J["cams"][0][1]
        for t0, fr in J["cams"]:
            if t >= t0 - 1e-6:
                f = fr
        return f

    shots, dlg, caps, punches, stings = [], [], [], [], []
    T = 0.0
    after_punch = False
    for seg in J["segs"]:
        a, b = seg[0], seg[1]
        tag = seg[2] if len(seg) > 2 else None
        pieces = tighten(ep, a, b, max_gap=1.2 if after_punch else MAX_GAP,
                         lead=0.45 if tag == "punch" else 0.12)
        for k, (p0, p1) in enumerate(pieces):
            # a camera switch within 0.3 s of a piece edge would leave a sliver: skip it
            cuts = [p0] + [t for t, _ in J["cams"] if p0 + 0.3 < t < p1 - 0.3] + [p1]
            for x0, x1 in zip(cuts, cuts[1:]):
                # alternate a slight punch-in on each jump cut so it reads as intentional
                shots.append(dict(cam_at(x0), t=x0, d=x1 - x0, push=0.04, zmul=1.12 if k % 2 else 1.0))
            dlg.append((p0, p1, T))
            T += p1 - p0
        # Captions: a word whose ASR start lands inside a trimmed pause (whisper drifts on
        # slow speech) snaps to the nearest kept piece instead of vanishing.
        base = T - sum(q1 - q0 for q0, q1 in pieces)
        for s_, e_, w in words:
            k1, k2 = round(s_, 2), (round(s_, 2), w)
            if not (a - 0.05 <= s_ < b) or k1 in drop or k2 in drop:
                continue
            off = base
            best = None
            for q0, q1 in pieces:
                d = 0 if q0 - 0.05 <= s_ < q1 else min(abs(s_ - q0), abs(s_ - q1))
                if best is None or d < best[0]:
                    best = (d, q0, q1, off)
                off += q1 - q0
            d, q0, q1, off = best
            if d > 0.8:
                continue
            st = min(max(s_, q0), q1 - 0.15)
            caps.append((st - q0 + off, min(max(e_, st + 0.15), q1) - q0 + off, fix.get(k2, fix.get(k1, w))))
        if tag == "punch":
            punches.append(T)
            after_punch = True
        elif tag == "sting":
            stings.append(T)
    shots.append(black(END))
    dur = T + END
    end_t = T

    def texts(fmt):
        g = fmt_geom(fmt)
        out = [kicker(fmt, 0.0, end_t, f"DAVE'S DAD JOKES  ·  {J['label']}")]
        out += [c for c in captions(fmt, caps, max_words=3, max_chars=18) if c.t0 < end_t]
        for c in out:
            c.t1 = min(c.t1, end_t) if c.t0 < end_t else c.t1
        out.append(image_card(fmt, end_t, dur, f"{REPO}/assets/media/podcast-cover.jpg", 0.3,
                              y=(g["card"] - 120) if fmt != "9x16" else 820, on="glow"))
        out.append(slam(fmt, end_t + 0.15, dur, "NEW DAD JOKE EVERY SATURDAY",
                        where=(g["card"] + 250) if fmt != "9x16" else 1290, size=g["slam"] * 0.42, anim="rise"))
        out.append(kicker(fmt, end_t + 0.3, dur, "PAIN 2 POWER  ·  100.3 LEGENDS RADIO  ·  8:30 AM",
                          where=(g["card"] + 340) if fmt != "9x16" else 1380, color=GOLD))
        return out

    def score():
        sc = S.Score(dur)
        p0 = punches[0] if punches else end_t
        sc.m(S.pad(p0 + 0.2, [110, 130.81, 164.81], g=0.8), 0.0, 0.55)
        sc.ticks(0.0, p0, 100, 0.18)
        for p in punches:
            sc.s(S.tom(190), p, 0.8)
            sc.s(S.tom(140), p + 0.15, 0.8)
            sc.s(S.kick(), p + 0.32, 0.8)
            sc.s(S.crash(1.6), p + 0.32, 0.7)
        for p in stings:
            sc.s(S.kick(), p, 0.7)
            sc.s(S.crash(1.4), p, 0.55)
        if p0 < end_t - 0.5:
            sc.groove(p0 + 0.6, end_t, 120, "four", 0.45)
        sc.s(S.boom(0.7, tail=2.6), end_t, 0.8)
        sc.s(S.stab([220, 261.6, 329.6]), end_t, 0.6)
        for a, b, t in dlg:
            sc.d(load_audio(ep, a, b), t)
        return sc

    reel = dict(shots=shots, texts=texts, hits=punches, flashes=punches, blacks=[])
    return reel, dur, score
