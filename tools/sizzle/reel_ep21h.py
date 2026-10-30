"""Episode 21, the Dave and Mike HALLOWEEN special: sizzle reel (~31 s, 9:16), Halloween themed
(Nick, 2026-10-30: "make the sizzle halloween themed"). Posted Sunday 10 AM ET after air day.

Dave, in Mike's red sequin jacket: "I'm dressed up as Mike, and Mike's dressed up as Dave." Mike, in
Dave's First Rehab shirt: "role reversal today." A HALLOWEEN SPECIAL card, Dave's pool table laps, Dave
raiding the kids' Snickers and Reese's, the skeleton punchline and Mike's laugh, then the Halloween
cartoon end card. Score: a minor key pad, a slow kick, a braam on the card and a wobbling theremin line.

Cut straight from the RAW cameras. Times are RAW mp3 seconds; each camera's time comes from its audio
sync line (tools/relay-work/ep21h-halloween/README.md). Put the files in $SIZZLE_WORK/src/ep21h/:
dave.mov (IMG_2045.MOV, 640x360), mike.mov (the 4K .mov), raw.mp3."""
import json
import numpy as np
import synth as S
import engine as E
from engine import load_audio
from lib import *

D21 = f"{E.SCR}/src/ep21h"
E.SRC.update({"h21d": f"{D21}/dave.mov", "h21m": f"{D21}/mike.mov", "h21a": f"{D21}/raw.mp3"})
E.SIZE.update({"h21d": (640, 360), "h21m": (3840, 2160)})
OFF = {"h21d": lambda t: 25.3415 - 0.0000332 * t,
       "h21m": lambda t: 18.5004 - 0.0000269 * t}
ORANGE = (255, 140, 26)
PURPLE = (178, 120, 255)


def cam(src, raw_t, d, **kw):
    """A lip-synced shot: raw mp3 time -> that camera's own time."""
    return dict(dict(src=src, t=raw_t + OFF[src](raw_t), d=d, fx=0.5, fy=0.3, z=1.0, push=0.0, hold=True,
                     _raw=raw_t), **kw)


_W = json.load(open(f"{D21}/words.json"))


def words(a, b):
    return [(w["s"], w["e"], w["w"].strip()) for w in _W if a <= w["s"] < b - 0.05]


# (key, camera, raw in, raw out) in reel order; the card sits after the second line
SEG = [("dave_as_mike", "h21d", 110.20, 112.95),
       ("mike_as_dave", "h21m", 112.95, 115.65),
       ("pool", "h21d", 319.35, 326.95),
       ("candy", "h21d", 1093.85, 1100.55),
       ("skin", "h21d", 1561.05, 1565.95),
       ("love", "h21m", 1567.75, 1570.35)]
CARD = 1.6
END = 4.4

shots, starts = [], {}
t = 0.0
for i, (k, src, a, b) in enumerate(SEG):
    starts[k] = t
    shots.append(cam(src, a, b - a))
    t += b - a
    if k == "mike_as_dave":
        shots.append(black(CARD))
        t += CARD
end_at = t
shots.append(black(END))
DUR = sum(s["d"] for s in shots)
card_at = starts["pool"] - CARD
hits = [card_at, starts["candy"], starts["skin"], end_at]
flashes = [card_at, end_at]


def card(fmt, t0, t1, name, sub, color=ORANGE):
    """Name card above the word pop captions (the stock name_card collides with captions at 1420 on 9:16)."""
    g = fmt_geom(fmt)
    img = E.text_img([(name, E.INTER_BLACK, g["name"], E.CREAM), (sub, E.INTER_XB, g["sub"], color)], g["W"],
                     track=0.015, stroke=max(3, int(g["name"]) // 20))
    return E.Txt(t0, t1, img, (g["cx"], 1150 if fmt == "9x16" else g["over"]), "rise")


def tl(k):
    a, b = next((x[2], x[3]) for x in SEG if x[0] == k)
    return [(x - a + starts[k], y - a + starts[k], w) for x, y, w in words(a, b)]


def texts(fmt):
    g = fmt_geom(fmt)
    T = [kicker(fmt, 0.1, end_at, "PAIN 2 POWER  ·  HALLOWEEN", color=ORANGE)]
    for k in starts:
        T += captions(fmt, tl(k))
    T.append(card(fmt, 0.4, starts["mike_as_dave"] - 0.1, "DR. DAVE KASHUBA", "DRESSED AS MIKE"))
    T.append(card(fmt, starts["mike_as_dave"] + 0.1, card_at - 0.1, "MIKE McGANN", "DRESSED AS DAVE", PURPLE))
    T.append(slam(fmt, card_at, card_at + CARD, "HALLOWEEN SPECIAL", where="card", size=g["slam"] * 0.78,
                  color=ORANGE))
    T.append(kicker(fmt, card_at + 0.15, card_at + CARD, "NO TRICKS, JUST GOOD INFORMATION", where=g["card"] + 110,
                    color=PURPLE))
    T.append(image_card(fmt, end_at, DUR, f"{REPO}/content/announcements/ep21-cover-halloween-1.jpg", 0.62, y=800,
                        on="glow"))
    T.append(slam(fmt, end_at + 0.2, DUR, "NEW EPISODE  ·  OUT NOW", where=1330, size=g["slam"] * 0.42,
                  color=ORANGE, anim="rise"))
    T.append(kicker(fmt, end_at + 0.4, DUR, "100.3 LEGENDS RADIO  ·  SPOTIFY  ·  YOUTUBE", where=1420, color=PURPLE))
    return T


def theremin(d, notes, g=1.0):
    """A wobbling sine with slow vibrato and glides between notes: the classic spooky movie line."""
    sr = 48000
    n = int(d * sr)
    tt = np.arange(n) / sr
    seg = d / len(notes)
    f = np.interp(tt, [i * seg for i in range(len(notes))] + [d], list(notes) + [notes[-1]])
    f = f * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * tt))
    x = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.minimum(1, tt / 0.4) * np.minimum(1, (d - tt) / 0.6)
    return S.verb(x * 0.35 * g, wet=0.45, seconds=3.0)


def score():
    sc = S.Score(DUR)
    sc.m(S.pad(card_at, [110, 130.81, 164.81], attack=1.0), 0.0, 0.45)
    sc.m(theremin(card_at, [440, 415.3, 392, 349.2, 329.6]), 0.0, 0.5)
    sc.m(S.riser(1.0), card_at - 1.0, 0.4)
    sc.s(S.boom(1.0), card_at, 0.9)
    sc.m(S.braam(1.6, 55.0), card_at, 0.6)
    sc.groove(card_at + CARD, end_at, 100, "four", 0.35, root=55.0)
    sc.m(S.pad(end_at - card_at - CARD, [110, 130.81, 164.81, 207.65]), card_at + CARD, 0.3)
    sc.m(theremin(end_at - card_at - CARD, [329.6, 349.2, 392, 349.2, 329.6, 311.1]), card_at + CARD, 0.28)
    sc.s(S.boom(0.7), starts["skin"], 0.5)
    sc.m(S.riser(1.2), end_at - 1.2, 0.5)
    sc.s(S.boom(1.1, tail=3.4), end_at, 1.0)
    sc.m(S.pad(END, [110, 130.81, 164.81, 220]), end_at, 0.8)
    sc.m(theremin(END, [440, 392, 349.2, 329.6]), end_at, 0.45)
    for k, src, a, b in SEG:
        sc.d(load_audio("h21a", a, b), starts[k])
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
