"""Reel 2 — THE DAD JOKE FILES (~54s). Dave promises a bad dad joke, then three
exhibits from three episodes (the grape / the lawsuit / the bossy lady), each landing
on Mike's reaction and a rimshot, closing on Mike: "one of my favorite parts of the week."
Captions are reviewed against a second, larger ASR pass (medium.en) and transcript-full.md."""
import synth as S
from lib import *
from lib import _M11, _M14
from engine import load_audio

_D11 = dict(src="ep11", fx=0.47, fy=0.62, z=2.0, **{"9x16": dict(fx=0.47, fy=0.6, z=1.6)})

A0 = 0.5 - 1459.25
A = 9.3 - 1483.9
B1 = 18.05 - 1479.9
B3 = 20.5 - 1491.1
B4 = 23.3 - 1496.6
B5 = 24.75 - 1498.05
B6 = 25.85 - 1505.75
C1 = 31.4 - 1594.4
C2 = 37.0 - 1600.95
C3 = 39.1 - 1604.85
C4 = 43.0 - 1611.55
VO = 45.3 - 1616.45

shots = [
    black(0.5),
    d16(1459.25, 4.75),
    d16(1464.0, 1.95) | dict(z=1.3, push=0.03),                  # jump-zoom: Mike "Every now and then."
    black(1.3),                                                   # THE DAD JOKE FILES
    black(0.8),                                                   # EXHIBIT A
    d16(1483.9, 4.05),
    m16(1488.9, 0.6),
    m16(1489.5, 3.3),
    black(0.8),                                                   # EXHIBIT B
    dict(SHOTS["d14_talk"], t=1479.9, d=2.45),
    dict(SHOTS["d14_talk"], t=1491.1, d=2.8, z=1.3),
    dict(SHOTS["d14_talk"], t=1496.6, d=1.45, z=1.12),
    dict(_M14, t=1498.05, d=1.1),
    dict(_M14, t=1505.75, d=4.75, push=0.08),
    black(0.8),                                                   # EXHIBIT C
    dict(_D11, t=1594.4, d=5.6, push=0.1),
    dict(_D11, t=1600.95, d=2.1, z=2.3),
    dict(_D11, t=1604.85, d=3.9, push=0.12),
    dict(_M11, t=1611.55, d=2.05),
    shot("d14_laugh", 0.9),
    shot("m9_laugh", 0.9),
    shot("d15_laugh", 0.9),
    shot("m15_laugh", 0.85),
    dict(_M11, t=1616.45 + (48.6 - 45.3), d=1.75),               # Mike on camera: "...as we wrap up the show."
    black(3.65),                                                  # end card
]
DUR = sum(s["d"] for s in shots)
hits = [7.2, 45.05]
flashes = [7.2, 8.5, 17.25, 30.6, 45.05, 50.35]

W_INTRO = [(1459.38, 1459.60, "Every"), (1459.60, 1459.76, "once"), (1459.76, 1459.98, "in"), (1459.98, 1460.0, "a"),
           (1460.0, 1460.5, "while,"), (1460.56, 1461.38, "I"), (1461.38, 1461.88, "try"), (1461.88, 1462.08, "to"),
           (1462.08, 1462.62, "throw"), (1462.62, 1462.78, "in"), (1462.78, 1462.94, "a"), (1462.94, 1463.2, "bad"),
           (1463.2, 1463.5, "dad"), (1463.5, 1463.95, "joke.")]
W_NOW = [(1464.2, 1464.6, "Every"), (1464.6, 1464.78, "now"), (1464.78, 1464.92, "and"), (1464.92, 1465.5, "then.")]
W_GRAPE = [(1484.1, 1484.42, "What"), (1484.42, 1484.52, "do"), (1484.52, 1484.62, "you"), (1484.62, 1484.76, "think"),
           (1484.76, 1485.04, "the"), (1485.04, 1486.16, "grape"), (1486.16, 1486.38, "did"), (1486.38, 1486.54, "when"),
           (1486.54, 1486.66, "he"), (1486.66, 1486.84, "saw"), (1486.84, 1486.98, "the"), (1486.98, 1487.22, "farmer"),
           (1487.22, 1487.4, "with"), (1487.4, 1487.56, "the"), (1487.56, 1487.9, "press?")]
W_WHINE = [(1489.64, 1490.08, "He"), (1490.08, 1490.8, "whined.")]
W_B1 = [(1479.98, 1480.52, "When"), (1480.52, 1480.74, "he"), (1480.74, 1480.92, "woke"), (1480.92, 1481.18, "up,"),
        (1481.18, 1481.48, "both"), (1481.48, 1481.8, "legs"), (1481.8, 1482.0, "were"), (1482.0, 1482.3, "gone.")]
W_B3 = [(1491.15, 1491.59, "He"), (1491.59, 1492.03, "sued"), (1492.03, 1492.25, "the"), (1492.25, 1492.61, "doctors,"),
        (1493.15, 1493.29, "but"), (1493.29, 1493.43, "he"), (1493.43, 1493.79, "lost.")]
W_B4 = [(1496.69, 1496.73, "He"), (1496.73, 1496.85, "didn't"), (1496.85, 1496.99, "have"), (1496.99, 1497.09, "a"),
        (1497.09, 1497.21, "leg"), (1497.21, 1497.41, "to"), (1497.41, 1497.63, "stand"), (1497.63, 1497.9, "on.")]
W_B5 = [(1498.0, 1498.39, "Oh"), (1498.39, 1498.67, "my"), (1498.67, 1499.1, "God.")]
W_B6 = [(1505.8, 1506.22, "That"), (1506.22, 1506.38, "may"), (1506.38, 1506.5, "be"), (1506.5, 1506.62, "the"),
        (1506.62, 1506.82, "best"), (1506.82, 1507.04, "you've"), (1507.04, 1507.18, "ever"), (1507.18, 1507.34, "done."),
        (1508.02, 1508.38, "I"), (1508.38, 1509.3, "honestly"), (1509.36, 1509.62, "thought"), (1509.62, 1509.7, "that"),
        (1509.7, 1509.96, "was"), (1509.96, 1510.08, "a"), (1510.08, 1510.16, "legit"), (1510.16, 1510.5, "story.")]
W_C1 = [(1594.48, 1594.88, "The"), (1594.88, 1595.28, "bartender's"), (1595.28, 1595.72, "all"),
        (1595.72, 1596.4, "excited."), (1596.58, 1596.76, "He's"), (1596.76, 1597.2, "like,"), (1597.28, 1597.6, "wow,"),
        (1597.68, 1597.78, "look"), (1597.78, 1598.0, "who's"), (1598.0, 1598.2, "coming"), (1598.2, 1598.6, "in."),
        (1598.72, 1598.92, "It's"), (1598.92, 1599.08, "that"), (1599.08, 1599.76, "bossy"), (1599.76, 1600.0, "lady.")]
W_C2 = [(1601.06, 1601.18, "And"), (1601.18, 1601.32, "they're"), (1601.32, 1601.6, "like,"), (1601.6, 1601.72, "why"),
        (1601.72, 1601.84, "do"), (1601.84, 1601.94, "you"), (1601.94, 1602.06, "want"), (1602.06, 1602.26, "a"),
        (1602.26, 1602.72, "bossy"), (1602.72, 1602.92, "lady"), (1602.92, 1603.0, "here?")]
W_C3 = [(1604.92, 1605.32, "What"), (1605.32, 1605.46, "do"), (1605.46, 1605.58, "you"), (1605.58, 1606.2, "think?"),
        (1606.8, 1607.02, "Right"), (1607.02, 1607.14, "when"), (1607.14, 1607.26, "she"), (1607.26, 1607.46, "gets"),
        (1607.46, 1607.72, "there,"), (1607.72, 1607.78, "she"), (1607.78, 1608.06, "orders"), (1608.06, 1608.42, "everyone"),
        (1608.42, 1608.75, "around.")]
W_C4 = [(1611.64, 1612.3, "Nice."), (1612.32, 1612.44, "I"), (1612.44, 1612.6, "think"), (1612.6, 1612.78, "I"),
        (1612.78, 1612.92, "might"), (1612.92, 1613.06, "have"), (1613.06, 1613.26, "dated"), (1613.26, 1613.55, "her.")]
W_VO = [(1616.54, 1616.98, "It's"), (1616.98, 1616.98, "one"), (1616.98, 1617.06, "of"), (1617.06, 1617.2, "my"),
        (1617.2, 1617.44, "favorite"), (1617.44, 1617.74, "parts"), (1617.74, 1617.86, "of"), (1617.86, 1617.98, "the"),
        (1617.98, 1618.4, "day,"), (1618.52, 1618.66, "the"), (1618.66, 1618.94, "week,"), (1618.94, 1619.52, "is"),
        (1619.52, 1619.82, "hearing"), (1619.82, 1620.24, "Dave"), (1620.24, 1620.44, "as"), (1620.44, 1620.6, "we"),
        (1620.6, 1620.76, "wrap"), (1620.76, 1620.98, "up"), (1620.98, 1621.16, "the"), (1621.16, 1621.4, "show.")]


def exhibit(fmt, t0, letter, title):
    g = fmt_geom(fmt)
    return [slam(fmt, t0, t0 + 0.8, f"EXHIBIT {letter}", where="mid", color=GOLD, size=g["slam"] * 0.8),
            kicker(fmt, t0 + 0.1, t0 + 0.8, title, where=g["mid"] + (110 if fmt == "9x16" else 120), color=CREAM)]


def texts(fmt):
    g = fmt_geom(fmt)
    T = [kicker(fmt, 0.03, 0.5, "PAIN 2 POWER PRESENTS", where="mid")]
    T += captions(fmt, words_from(W_INTRO, A0))
    T += captions(fmt, words_from(W_NOW, A0))
    T.append(slam(fmt, 7.2, 8.5, "THE DAD JOKE", where=g["mid"] - (70 if fmt == "9x16" else 80)))
    T.append(slam(fmt, 7.3, 8.5, "FILES.", where=g["mid"] + (70 if fmt == "9x16" else 80), color=CORAL))
    T += exhibit(fmt, 8.5, "A", "THE GRAPE  ·  EPISODE 16")
    T += captions(fmt, words_from(W_GRAPE, A), max_words=4, max_chars=22)
    T += captions(fmt, words_from(W_WHINE, A), end_pad=0.7)
    T += exhibit(fmt, 17.25, "B", "THE LAWSUIT  ·  EPISODE 14")
    T += captions(fmt, words_from(W_B1, B1))
    T += captions(fmt, words_from(W_B3, B3))
    T += captions(fmt, words_from(W_B4, B4), end_pad=0.05)
    T += captions(fmt, words_from(W_B5, B5), end_pad=0.4)
    T += captions(fmt, words_from(W_B6, B6), max_words=4, max_chars=22)
    T += exhibit(fmt, 30.6, "C", "THE BOSSY LADY  ·  EPISODE 11")
    T += captions(fmt, words_from(W_C1, C1))
    T += captions(fmt, words_from(W_C2, C2))
    T += captions(fmt, words_from(W_C3, C3), end_pad=0.1)
    T += captions(fmt, words_from(W_C4, C4), end_pad=0.5)
    T += captions(fmt, words_from(W_VO, VO), max_words=3)
    # end card
    T.append(image_card(fmt, 50.35, DUR, f"{REPO}/assets/media/podcast-cover.jpg", 0.3,
                        y=(g["mid"] - 120) if fmt != "9x16" else 820, on="glow"))
    T.append(slam(fmt, 50.6, DUR, "NEW JOKE EVERY SATURDAY", where=(g["mid"] + 250) if fmt != "9x16" else 1290,
                  size=g["slam"] * (0.5 if fmt != "9x16" else 0.46), anim="rise", darken=0))
    T.append(kicker(fmt, 50.8, DUR, "8:30 AM  ·  100.3 LEGENDS RADIO  ·  SPOTIFY  ·  YOUTUBE",
                    where=(g["mid"] + 340) if fmt != "9x16" else 1380, color=GOLD))
    return T


def rimshot(sc, t):
    sc.s(S.tom(190), t, 0.8)
    sc.s(S.tom(140), t + 0.15, 0.8)
    sc.s(S.kick(), t + 0.32, 0.8)
    sc.s(S.crash(1.6), t + 0.32, 0.7)


def score():
    sc = S.Score(DUR)
    sc.m(S.pad(7.2, [110, 130.81, 164.81]), 0.0, 0.8)
    sc.ticks(0.5, 7.2, 110, 0.3)
    sc.m(S.riser(1.6), 5.6, 0.6)
    sc.s(S.boom(), 7.2, 1.0)
    sc.m(S.braam(2.2, 55.0), 7.2, 0.8)
    for t in (8.5, 17.25, 30.6):
        sc.s(S.whoosh(0.5), t - 0.3, 0.7)
        sc.s(S.stab([110, 138.59, 164.81]), t, 0.8)
        sc.s(S.sub808(55, 0.8), t, 0.6)
    sc.m(S.pad(7.9, [55, 82.41]), 9.3, 0.8)
    sc.m(S.pad(12.5, [49, 73.4]), 18.05, 0.7)
    sc.m(S.pad(13.6, [55, 82.41]), 31.4, 0.7)
    rimshot(sc, 14.98)
    rimshot(sc, 24.7)
    rimshot(sc, 44.85)
    sc.s(S.boom(0.8), 45.05, 0.7)
    sc.groove(45.05, 50.35, 120, "four", 0.8)
    sc.m(S.pad(5.3, [110, 130.81, 164.81, 220]), 45.05, 0.9)
    sc.s(S.boom(1.1, tail=3.6), 50.35, 0.9)
    sc.m(S.braam(3.6, 41.2), 50.35, 0.7)
    # dialogue
    sc.d(load_audio("ep16", 1459.25, 1465.95), 1459.25 + A0)
    sc.d(load_audio("ep16", 1483.9, 1487.95), 1483.9 + A)
    sc.d(load_audio("ep16", 1488.9, 1492.75), 1488.9 + A)
    sc.d(load_audio("ep14", 1479.9, 1482.35), 1479.9 + B1)
    sc.d(load_audio("ep14", 1491.1, 1493.9), 1491.1 + B3)
    sc.d(load_audio("ep14", 1496.6, 1499.2), 1496.6 + B4)
    sc.d(load_audio("ep14", 1505.75, 1510.5), 1505.75 + B6)
    sc.d(load_audio("ep11", 1594.4, 1600.0), 1594.4 + C1)
    sc.d(load_audio("ep11", 1600.95, 1603.05), 1600.95 + C2)
    sc.d(load_audio("ep11", 1604.85, 1608.75), 1604.85 + C3)
    sc.d(load_audio("ep11", 1611.55, 1613.75), 1611.55 + C4)
    sc.d(load_audio("ep11", 1616.45, 1621.5), 1616.45 + VO)
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
