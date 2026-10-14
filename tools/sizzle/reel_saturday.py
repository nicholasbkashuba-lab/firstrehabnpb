"""Reel 3 — HAPPY SATURDAY (~21s). Short, upbeat, beat-cut promo for Stories/Shorts:
Mike's Ep 14 open runs as the voiceover over a montage from every episode, with name
slams when he introduces himself and Dave, a laugh burst and the tune-in card."""
import synth as S
from lib import *
from lib import _M14
from engine import load_audio

OFF = 0.5          # ep14 src t -> timeline t - OFF
B = 60 / 128 * 2   # two beats
HS = 18.4 - 1658.0

shots = [
    dict(_M14, t=0.5, d=1.6),
    shot("d14_laugh", B),
    shot("m11_gest", B),
    shot("d15_point", B),
    shot("m9_laugh2", B),
    shot("dk_smile", B),
    shot("m15_wave", B),
    shot("d16_onair", 7.9 - (1.6 + 6 * B)),
    dict(_M14, t=7.9 + OFF, d=1.6, push=0.1),      # "...100.3. I'm Mike McGann"
    shot("m15_laugh", 0.94),
    shot("w9_duo", 1.86, push=0.05),
    shot("d14_talk", 1.3, t=1440.0),
    shot("d14_laugh2", 1.4, push=0.1),             # "...my friend, Dave Kashuba."
    shot("m9_laugh", B / 2),
    shot("d15_laugh", B / 2),
    shot("m11_gest3", B / 2),
    shot("dk_laugh", B / 2),
    shot("m14_laugh", B / 2),
    shot("d14_wave", 17.82 - (15.0 + 5 * B / 2)),
    black(3.2),
]
DUR = sum(s["d"] for s in shots)
hits = [8.83, 13.67, 17.82]
flashes = hits

W = [(0.85, 1.41, "Good"), (1.41, 1.85, "morning,"), (2.05, 2.13, "happy"), (2.13, 2.59, "Saturday,"),
     (2.95, 3.19, "and"), (3.19, 3.41, "welcome"), (3.41, 3.65, "once"), (3.65, 4.01, "again"), (4.01, 4.47, "to"),
     (4.47, 4.83, "Pain"), (4.83, 5.23, "2"), (5.23, 5.65, "Power,"), (5.71, 6.09, "right"), (6.09, 6.37, "here"),
     (6.37, 7.11, "on"), (7.11, 7.45, "Legends"), (7.45, 8.93, "100.3."), (9.09, 9.33, "I'm"), (9.33, 9.49, "Mike"),
     (9.49, 9.83, "McGann,"), (10.05, 10.15, "and"), (10.15, 10.41, "with"), (10.41, 10.75, "me,"), (10.81, 10.93, "of"),
     (10.93, 11.3, "course,"), (11.39, 11.55, "as"), (11.55, 12.09, "always,"), (12.33, 12.99, "is"), (12.99, 13.25, "my"),
     (13.25, 13.75, "friend,"), (14.17, 14.73, "Dave"), (14.73, 15.41, "Kashuba.")]
W_HS = [(1658.07, 1658.17, "Happy"), (1658.17, 1658.6, "Saturday.")]


def texts(fmt):
    g = fmt_geom(fmt)
    T = []
    if fmt == "9x16":
        T.append(kicker(fmt, 0.1, 17.8, "PAIN 2 POWER  ·  100.3 LEGENDS RADIO"))
    T += captions(fmt, words_from(W, -OFF))
    T.append(slam(fmt, 8.83, 9.6, "MIKE McGANN", where="mid" if fmt != "9x16" else "top", darken=0.2))
    T.append(slam(fmt, 13.67, 15.0, "DR. DAVE KASHUBA", where="mid" if fmt != "9x16" else "top", darken=0.2,
                  size=g["slam"] * 0.85))
    T.append(image_card(fmt, 17.82, DUR, f"{REPO}/assets/media/podcast-cover.jpg", 0.3,
                        y=(g["mid"] - 120) if fmt != "9x16" else 820, on="glow"))
    T.append(slam(fmt, 18.0, DUR, "SATURDAYS 8:30 AM", where=(g["mid"] + 250) if fmt != "9x16" else 1290,
                  size=g["slam"] * 0.5, anim="rise", darken=0))
    T.append(kicker(fmt, 18.2, DUR, "100.3 LEGENDS RADIO  ·  SPOTIFY  ·  YOUTUBE",
                    where=(g["mid"] + 340) if fmt != "9x16" else 1380, color=GOLD))
    T += captions(fmt, words_from(W_HS, HS), y=(g["cap"] if fmt == "9x16" else 960), end_pad=1.5)
    return T


def score():
    sc = S.Score(DUR)
    sc.groove(0.0, 8.83, 128, "trap", 0.7)
    sc.m(S.pad(8.9, [110, 130.81, 164.81]), 0.0, 0.7)
    sc.m(S.riser(1.0), 7.83, 0.5)
    sc.s(S.boom(0.8), 8.83, 0.85)
    sc.groove(8.83, 13.67, 128, "four", 0.8)
    sc.m(S.pad(4.9, [98, 123.47, 146.83]), 8.83, 0.7)
    sc.m(S.riser(1.0), 12.67, 0.5)
    sc.s(S.boom(0.9), 13.67, 0.9)
    sc.m(S.braam(1.6, 55.0), 13.67, 0.6)
    sc.groove(15.0, 17.82, 128, "trap", 1.0)
    sc.m(S.riser(1.3), 16.5, 0.6)
    sc.s(S.boom(1.1, tail=3.4), 17.82, 1.0)
    sc.m(S.braam(3.2, 41.2), 17.82, 0.7)
    sc.m(S.pad(3.2, [110, 130.81, 164.81, 220]), 17.82, 0.9)
    sc.d(load_audio("ep14", 0.8, 15.5), 0.8 - OFF)
    sc.d(load_audio("ep14", 1658.0, 1658.75), 1658.0 + HS)
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
