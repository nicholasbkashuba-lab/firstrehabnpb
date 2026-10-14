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
D9 = dict(src="ep9", fx=0.68, fy=0.45, z=1.3, **_V(fx=0.68, fy=0.45))
M9 = dict(src="ep9", fx=0.22, fy=0.45, z=1.3, **_V(fx=0.22, fy=0.45))
W9 = dict(src="ep9", fx=0.5, fy=0.45, z=1.0, **_V(fx=0.5, fy=0.45))

END = 2.6  # end card

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
    for seg in J["segs"]:
        a, b = seg[0], seg[1]
        tag = seg[2] if len(seg) > 2 else None
        cuts = [a] + [t for t, _ in J["cams"] if a < t < b] + [b]
        for x0, x1 in zip(cuts, cuts[1:]):
            shots.append(dict(cam_at(x0), t=x0, d=x1 - x0, push=0.05))
        dlg.append((a, b, T))
        for s, e, w in words:
            k1, k2 = round(s, 2), (round(s, 2), w)
            if a - 0.05 <= s < b and k1 not in drop and k2 not in drop:
                caps.append((s - a + T, min(e, b) - a + T, fix.get(k2, fix.get(k1, w))))
        T += b - a
        if tag == "punch":
            punches.append(T)
        elif tag == "sting":
            stings.append(T)
    shots.append(black(END))
    dur = T + END
    end_t = T

    def texts(fmt):
        g = fmt_geom(fmt)
        out = [kicker(fmt, 0.0, end_t, f"DAVE'S DAD JOKES  ·  {J['label']}")]
        out += captions(fmt, caps, max_words=3, max_chars=18)
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
