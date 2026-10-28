"""Episode 21 sizzle reel (~26s, 9:16) for the noon slot on air day. Dr. Reed Stone puts
the MRI down, a title card, his own comeback ("No pain, no surgery"), Mike's "who helps the
doctors out? Well, these guys", Dave's surgeon and God line, then the tune in card.

Cut straight from the RAW cameras (one resample, not a crop of the 720p-sourced master).
Times below are RAW mp3 seconds; each camera's time comes from its audio sync line
(tools/relay-work/ep21-stone/README.md). Put the files in $SIZZLE_WORK/src/ep21/:
dave.mp4 (IMG_2010.MP4), guest.mp4 (IMG_5523.MP4), mike.mov (the 4K .mov), raw.mp3."""
import synth as S
import engine as E
from engine import load_audio
from lib import *

D21 = f"{E.SCR}/src/ep21"
E.SRC.update({"s21d": f"{D21}/dave.mp4", "s21g": f"{D21}/guest.mp4", "s21m": f"{D21}/mike.mov",
              "s21a": f"{D21}/raw.mp3"})
E.SIZE.update({"s21d": (1280, 720), "s21g": (1280, 720), "s21m": (3840, 2160)})
OFF = {"s21d": lambda t: 107.8726 - 0.0000318 * t,
       "s21g": lambda t: 94.5896 - 0.0000410 * t,
       "s21m": lambda t: 90.2318 - 0.0000275 * t}


def cam(src, raw_t, d, **kw):
    """A lip-synced shot: raw mp3 time -> that camera's own time."""
    return dict(src=src, t=raw_t + OFF[src](raw_t), d=d, fx=0.5, fy=0.3, z=1.0, push=0.0, hold=True,
                _raw=raw_t, **kw)


WORDS = {
    "mri": [(1078.12, 1078.22, "When"), (1078.22, 1078.32, "a"), (1078.32, 1078.50, "patient"),
            (1078.50, 1078.76, "comes"), (1078.76, 1078.88, "in"), (1078.88, 1079.02, "with"),
            (1079.02, 1079.10, "an"), (1079.10, 1079.32, "MRI,"), (1079.46, 1079.56, "put"),
            (1079.56, 1079.70, "it"), (1079.70, 1080.02, "down."), (1080.84, 1080.94, "And"),
            (1080.94, 1081.04, "they"), (1081.04, 1081.16, "look"), (1081.16, 1081.28, "at"),
            (1081.28, 1081.44, "me,"), (1081.46, 1081.58, "aren't"), (1081.58, 1081.74, "you"),
            (1081.74, 1081.88, "going"), (1081.88, 1081.92, "to"), (1081.92, 1082.02, "look"),
            (1082.02, 1082.12, "at"), (1082.12, 1082.22, "the"), (1082.22, 1082.58, "MRI?"),
            (1083.00, 1083.24, "That's"), (1083.24, 1083.40, "the"), (1083.40, 1083.56, "last"),
            (1083.56, 1083.76, "thing.")],
    "gym": [(342.92, 343.20, "No"), (343.20, 343.50, "pain,"), (343.78, 343.94, "no"),
            (343.94, 344.44, "surgery,"), (344.96, 345.28, "nothing."), (345.70, 345.82, "I'm"),
            (345.82, 345.96, "back"), (345.96, 346.12, "in"), (346.12, 346.28, "the"), (346.28, 346.46, "gym.")],
    "doc": [(1221.70, 1221.76, "Who"), (1222.18, 1222.58, "helps"), (1222.58, 1222.76, "the"),
            (1222.76, 1223.00, "doctors"), (1223.00, 1223.26, "out?"), (1223.34, 1223.46, "Well,"),
            (1223.54, 1223.68, "these"), (1223.68, 1224.08, "guys.")],
    "god": [(771.12, 771.44, "I"), (771.44, 771.64, "always"), (771.64, 771.78, "say"),
            (771.78, 771.90, "the"), (771.90, 772.16, "difference"), (772.16, 772.52, "between"),
            (772.52, 772.76, "a"), (772.76, 773.06, "surgeon"), (773.06, 773.32, "and"),
            (773.32, 773.56, "God"), (773.56, 773.76, "is"), (773.76, 774.00, "God"),
            (774.00, 774.24, "knows"), (774.24, 774.50, "he's"), (774.50, 774.60, "not"),
            (774.60, 774.76, "a"), (774.76, 775.08, "surgeon."), (776.68, 776.84, "Oh,"),
            (777.24, 777.62, "that's"), (777.62, 777.86, "really"), (777.86, 778.22, "good.")],
}
# (key, camera, raw in, raw out) in reel order; the card and the end card sit between
SEG = [("mri", "s21g", 1078.00, 1084.15),
       ("gym", "s21g", 342.80, 346.85),
       ("doc", "s21m", 1221.55, 1224.40),
       ("god", "s21d", 771.00, 778.55)]
CARD = 1.5
END = 4.2

shots, starts = [], {}
t = 0.0
for i, (k, src, a, b) in enumerate(SEG):
    starts[k] = t
    shots.append(cam(src, a, b - a))
    t += b - a
    if i == 0:
        shots.append(black(CARD))
        t += CARD
end_at = t
shots.append(black(END))
DUR = sum(s["d"] for s in shots)
card_at = SEG[0][3] - SEG[0][2]
hits = [card_at, starts["doc"], end_at]
flashes = hits


def card(fmt, t0, t1, name, sub):
    """Name card above the word pop captions: the stock name_card sits at y 1290, which
    collides with captions at the 1420 safe height on 9:16."""
    g = fmt_geom(fmt)
    img = E.text_img([(name, E.INTER_BLACK, g["name"], E.CREAM), (sub, E.INTER_XB, g["sub"], E.GOLD)], g["W"],
                     track=0.015, stroke=max(3, int(g["name"]) // 20))
    return E.Txt(t0, t1, img, (g["cx"], 1150 if fmt == "9x16" else g["over"]), "rise")


def tl(k):
    a = SEG[[s[0] for s in SEG].index(k)][2]
    return [(x - a + starts[k], y - a + starts[k], w) for x, y, w in WORDS[k]]


def texts(fmt):
    g = fmt_geom(fmt)
    T = [kicker(fmt, 0.1, end_at, "PAIN 2 POWER  ·  EPISODE 21")]
    for k in starts:
        T += captions(fmt, tl(k))
    T.append(card(fmt, 0.6, card_at - 0.2, "DR. REED STONE", "NEUROLOGIST, PALM BEACH NEUROLOGY"))
    T.append(slam(fmt, card_at, card_at + CARD, "THE NERVE DOCTOR", where="card", size=g["slam"] * 0.8))
    T.append(kicker(fmt, card_at + 0.15, card_at + CARD, "40 YEARS OF NEUROLOGY", where=g["card"] + 110, color=GOLD))
    T.append(card(fmt, starts["doc"] + 0.2, starts["god"] - 0.1, "MIKE McGANN", "CO HOST, PAIN 2 POWER"))
    T.append(card(fmt, starts["god"] + 0.3, starts["god"] + 4.2, "DR. DAVE KASHUBA", "FIRST REHABILITATION"))
    T.append(image_card(fmt, end_at, DUR, f"{REPO}/assets/media/podcast-cover.jpg", 0.3, y=820, on="glow"))
    T.append(slam(fmt, end_at + 0.2, DUR, "NEW EPISODE  ·  SATURDAY 8:30 AM", where=1290, size=g["slam"] * 0.42,
                  anim="rise"))
    T.append(kicker(fmt, end_at + 0.4, DUR, "100.3 LEGENDS RADIO  ·  SPOTIFY  ·  YOUTUBE", where=1380, color=GOLD))
    return T


def score():
    sc = S.Score(DUR)
    sc.groove(0.0, card_at, 120, "trap", 0.45)
    sc.m(S.riser(1.0), card_at - 1.0, 0.4)
    sc.s(S.boom(0.9), card_at, 0.85)
    sc.m(S.braam(1.5, 55.0), card_at, 0.55)
    sc.groove(card_at + CARD, end_at, 120, "four", 0.4)
    sc.s(S.boom(0.7), starts["doc"], 0.6)
    sc.m(S.riser(1.2), end_at - 1.2, 0.5)
    sc.s(S.boom(1.1, tail=3.4), end_at, 1.0)
    sc.m(S.pad(END, [110, 130.81, 164.81, 220]), end_at, 0.8)
    for k, src, a, b in SEG:
        sc.d(load_audio("s21a", a, b), starts[k])
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
