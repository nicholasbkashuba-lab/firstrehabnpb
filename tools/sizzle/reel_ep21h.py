"""Episode 21, the Dave and Mike HALLOWEEN special: sizzle reel (~62 s, 9:16). Posted Sunday 10 AM ET.

Third cut (Nick, 2026-10-30: "the sizzle reel cuts off sentences too quickly" and "make sure the captions are
perfect too with the speed"): every line is a whole sentence with its in/out set from force-aligned word times,
the skeleton joke keeps its setup, Mike's lines run on into his reply, and the captions are force-aligned too.

Second cut (Nick, 2026-10-30, on the first: "not halloween enough and not enough mike its too much dave").
The first cut gave Mike 5 s of 27. This one is built on the in-character open, where the two of them
play each other, so Mike carries about half the reel:

  Dave (as Mike) opens the show: "Good morning, this is Mike McGann at Legends Radio, 100.3."
  Mike (as Dave): "As Dave, I help people deal with their pain, get them back in the game..."
  Dave: "How did you get that?"  Mike: "Some cash had to change hands, but all of it was legal..."
  Dave: "I'm dressed up as Mike, and Mike's dressed up as Dave."  Mike: "role reversal today."
  Dave: "Is it Mike or Dave? Now I'm confused."  Mike: "I never know who I am anyway."
  HALLOWEEN SPECIAL card: double lightning flash, thunder, an organ "dun dun DUN", bats.
  Dave on where costumes came from: "...dress up like them, it's the way they can't recognize us."
  The skeleton punchline, Mike: "Oh, wow. I love that."  Halloween cartoon end card, bats, a howl.

Speakers are confirmed by voice ID (ECAPA, spk_emb.npz), not by the camera. Halloween comes from the
type and the cards, never a colour grade (engine owner rule, 2026-10-14): orange caption highlight,
the thin PAIN 2 POWER · HALLOWEEN EDITION banner across the top (Dave), bats and ghosts drawn from Noto Color Emoji, lightning flashes.

Cut straight from the RAW cameras. Times are RAW mp3 seconds; each camera's time comes from its audio
sync line (tools/relay-work/ep21h-halloween/README.md). Put the files in $SIZZLE_WORK/src/ep21h/:
dave.mov (IMG_2045.MOV, 640x360), mike.mov (the 4K .mov), raw.mp3, words.json."""
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import synth as S
import engine as E
import lib
from engine import load_audio
from lib import *

D21 = f"{E.SCR}/src/ep21h"
E.SRC.update({"h21d": f"{D21}/dave.mov", "h21m": f"{D21}/mike.mov", "h21a": f"{D21}/raw.mp3"})
E.SIZE.update({"h21d": (640, 360), "h21m": (3840, 2160)})
OFF = {"h21d": lambda t: 25.3415 - 0.0000332 * t,
       "h21m": lambda t: 18.5004 - 0.0000269 * t}
ORANGE = (255, 140, 26)
PURPLE = (178, 120, 255)
lib.GOLD = ORANGE            # the active caption word lights up pumpkin orange, not gold
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


def cam(src, raw_t, d, **kw):
    """A lip-synced shot: raw mp3 time -> that camera's own time."""
    return dict(dict(src=src, t=raw_t + OFF[src](raw_t), d=d, fx=0.5, fy=0.3, z=1.0, push=0.0, hold=True,
                     _raw=raw_t), **kw)


_W = json.load(open(f"{D21}/words.json"))
E.WORDS["h21a"] = _W            # run.py's cut check reads these


def _merged(ws):
    """Whisper splits "100.3" into "100" + ".3." and "10,000" into "10" + ",000": glue them for the captions."""
    out = []
    for w in ws:
        tok = w["w"].strip()
        if out and tok[:1] in ",." and tok[1:2].isdigit():
            out[-1] = dict(out[-1], w=out[-1]["w"] + tok, e=w["e"])
        else:
            out.append(dict(w, w=tok))
    return out


_WM = _merged(_W)


def words(a, b):
    """Caption words for RAW [a, b], force-aligned to the audio (engine.aligned): on time to ~20 ms."""
    return E.aligned("h21a", a, b, _WM)


# (key, camera, raw in, raw out) in reel order. Speaker by voice ID: D = Dave, M = Mike.
# Every in/out comes from the words force-aligned to the RAW audio (tools/cut_check.py), not from Whisper,
# whose word times ran 0.3 to 0.4 s early here and clipped the end of 9 of the first cut's 11 lines.
# Pairs that share a time (how/cash, reveal/reversal, confused/who) are one continuous stretch of audio
# with a camera change inside it, so nothing is cut at that point.
SEG = [("open", "h21d", 4.64, 9.40),          # D "Good morning, this is Mike McGann at Legends Radio, 100.3."
       ("as_dave", "h21m", 47.74, 57.24),     # M "Absolutely, as Dave, I help people ... through physical therapy."
       ("how", "h21d", 85.49, 86.40),         # D "How did you get that?"
       ("cash", "h21m", 86.40, 91.68),        # M "Well, some cash had to change hands, but ... legal and above board."
       ("reveal", "h21d", 110.26, 113.05),    # D "I'm dressed up as Mike, and Mike's dressed up as Dave."
       ("reversal", "h21m", 113.05, 116.21),  # M "That's it, we decided to do a little role reversal today."
       ("confused", "h21d", 133.40, 137.35),  # D "And the funny thing is, is Mike or Dave? Now I'm confused."
       ("who", "h21m", 137.35, 140.18),       # M "I'm confused as to who. I never know who I am anyway."
       ("survive", "h21d", 858.80, 873.21),   # D "They're all coming down. So all the spirits ... they can't recognize us." M "Gotcha."
       ("skin", "h21d", 1555.86, 1566.30),    # D "And what is a skeleton gonna do for you ... nothing gets under his skin."
       ("love", "h21m", 1567.40, 1570.72)]    # M "Oh, wow. I love that."
# Mike leans in toward the mic as his "I'm confused as to who" line starts: frame him 7% right so he stays within
# 10% of centre through the lean and after it (qa_center, 2026-10-30)
BIAS = {"who": {"hold_bias": 0.07}}
CARD = 2.3
END = 4.6

shots, starts = [], {}
t = 0.0
for k, src, a, b in SEG:
    starts[k] = t
    shots.append(cam(src, a, b - a, **BIAS.get(k, {})))
    t += b - a
    if k == "who":
        shots.append(black(CARD))
        t += CARD
end_at = t
shots.append(black(END))
DUR = sum(s["d"] for s in shots)
card_at = starts["survive"] - CARD
hits = [card_at, starts["survive"], starts["skin"], end_at]
flashes = [card_at, card_at + 0.16, starts["survive"], end_at]   # a double strike of lightning on the card


# ---------------------------------------------------------------- Halloween sprites
_EM = {}


def emoji(ch, px):
    """A Noto Color Emoji glyph as an RGBA image `px` wide."""
    if ch not in _EM:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        _EM[ch] = im.crop(im.getbbox())
    im = _EM[ch]
    return im.resize((px, int(im.height * px / im.width)), Image.LANCZOS)


class Sprite(E.Txt):
    """An image that travels along path(u) -> (x, y, scale) for u in 0..1; flap squashes it vertically
    at `flap` Hz (bat wings)."""

    def __init__(self, t0, t1, img, path, flap=0.0, alpha=1.0):
        super().__init__(t0, t1, img, (0, 0), "none")
        self.path, self.flap, self.alpha = path, flap, alpha

    def draw(self, canvas, t):
        if not (self.t0 <= t < self.t1):
            return
        u = (t - self.t0) / (self.t1 - self.t0)
        x, y, s = self.path(u)
        sy = s * (0.55 + 0.45 * abs(math.sin(2 * math.pi * self.flap * t))) if self.flap else s
        img = self.img.resize((max(1, int(self.img.width * s)), max(1, int(self.img.height * sy))), Image.BICUBIC)
        a = self.alpha * min(1, (t - self.t0) / 0.2) * min(1, (self.t1 - t) / 0.2)
        if a < 0.999:
            img.putalpha(img.split()[-1].point(lambda v: int(v * a)))
        canvas.alpha_composite(img, (int(x - img.width / 2), int(y - img.height / 2)))


def bats(t0, t1, n, y0, y1, seed, size=(70, 130), rtl=False):
    """A flock crossing the frame, each bat on its own wavy line and speed."""
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        px = int(rng.uniform(*size))
        ya, yb = rng.uniform(y0, y1), rng.uniform(y0, y1)
        amp, ph, lag = rng.uniform(20, 60), rng.uniform(0, 6.3), rng.uniform(0, 0.35) * (t1 - t0)
        xa, xb = (1200, -120) if rtl else (-120, 1200)

        def path(u, ya=ya, yb=yb, amp=amp, ph=ph, xa=xa, xb=xb):
            return xa + (xb - xa) * u, ya + (yb - ya) * u + amp * math.sin(6 * u + ph), 1.0
        out.append(Sprite(t0 + lag, t1, emoji("🦇", px), path, flap=rng.uniform(5, 8)))
    return out


def ghost(t0, t1, x, y0, y1, px=150, phase=0.0):
    def path(u):
        return x + 30 * math.sin(4 * u + phase), y0 + (y1 - y0) * u, 1.0 + 0.06 * math.sin(7 * u + phase)
    return Sprite(t0, t1, emoji("👻", px), path, alpha=0.9)


def still(t0, t1, ch, x, y, px, bob=8.0, phase=0.0):
    def path(u):
        return x, y + bob * math.sin(2 * math.pi * u * (t1 - t0) * 0.8 + phase), 1.0
    return Sprite(t0, t1, emoji(ch, px), path)


# ---------------------------------------------------------------- type
def banner(W):
    """The thin top banner Dave asked for on every Halloween clip (2026-10-30), so the reel matches them:
    "PAIN 2 POWER · HALLOWEEN EDITION" in orange on ink, a pumpkin each side, an orange rule under it.
    It sits at the very top edge, above everyone's head; the same image is burned into the ten clips."""
    H, fs = 84, 36
    im = Image.new("RGBA", (W, H), (7, 30, 39, 225))
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 4, W, H], fill=ORANGE + (255,))
    f = ImageFont.truetype(E.INTER_BLACK, fs)
    txt, tr = "PAIN 2 POWER  ·  HALLOWEEN EDITION", fs * 0.1
    w = sum(f.getlength(c) for c in txt) + tr * (len(txt) - 1)
    x, y = (W - w) / 2, (H - 4 - fs) / 2 - fs * 0.14
    for c in txt:
        d.text((x, y), c, font=f, fill=ORANGE + (255,))
        x += f.getlength(c) + tr
    p = emoji("🎃", 44)
    im.alpha_composite(p, (int((W - w) / 2 - 20 - p.width), int((H - 4 - p.height) / 2)))
    im.alpha_composite(p, (int((W + w) / 2 + 20), int((H - 4 - p.height) / 2)))
    return im


def card(fmt, t0, t1, name, sub, color=ORANGE):
    """Name card above the word pop captions (the stock name_card collides with captions at 1420 on 9:16)."""
    g = fmt_geom(fmt)
    img = E.text_img([(name, E.INTER_BLACK, g["name"], E.CREAM), (sub, E.INTER_XB, g["sub"], color)], g["W"],
                     track=0.015, stroke=max(3, int(g["name"]) // 20))
    return E.Txt(t0, t1, img, (g["cx"], 1150 if fmt == "9x16" else g["over"]), "rise")


def tl(k):
    a, b = next((x[2], x[3]) for x in SEG if x[0] == k)
    return [(x - a + starts[k], min(y, b) - a + starts[k], w) for x, y, w in words(a, b) if x < b - 0.05]


def texts(fmt):
    g = fmt_geom(fmt)
    bn = banner(g["W"])
    T = [E.Txt(0.0, DUR, bn, (g["cx"], bn.height / 2), "none")]
    for k, src, a, b in SEG:
        caps = captions(fmt, tl(k))
        for tx in caps:                     # a line's last caption may not hang into the next line's shot
            tx.t1 = min(tx.t1, starts[k] + (b - a))
        T += [tx for tx in caps if tx.t1 > tx.t0 + 0.04]
    T.append(card(fmt, 0.3, starts["as_dave"] - 0.1, "DR. DAVE KASHUBA", "DRESSED AS MIKE"))
    T.append(card(fmt, starts["as_dave"] + 0.1, starts["how"] - 0.1, "MIKE McGANN", "DRESSED AS DAVE", PURPLE))
    T += bats(0.0, 2.4, 4, 380, 900, seed=3)                          # the open
    # the HALLOWEEN SPECIAL card
    T.append(E.Txt(card_at + 0.05, card_at + CARD, emoji("🎃", 300), (g["cx"], 700), "slam"))
    T.append(slam(fmt, card_at + 0.2, card_at + CARD, "HALLOWEEN SPECIAL", where="card", size=g["slam"] * 0.78,
                  color=ORANGE))
    T.append(kicker(fmt, card_at + 0.45, card_at + CARD, "WHO'S WHO?", where=g["card"] + 110, color=PURPLE))
    T += bats(card_at + 0.1, card_at + CARD, 7, 300, 1500, seed=8, size=(80, 160), rtl=True)
    # the costume origin story gets ghosts drifting up the edges
    s, e = starts["survive"], starts["survive"] + (SEG[8][3] - SEG[8][2])
    T += [ghost(s + 0.3, e, 130, 1300, 650), ghost(s + 1.4, e, 950, 1350, 760, px=120, phase=2.0)]
    # end card
    T.append(image_card(fmt, end_at, DUR, f"{REPO}/content/announcements/ep21-cover-halloween-1.jpg", 0.62, y=800,
                        on="glow"))
    T.append(slam(fmt, end_at + 0.2, DUR, "NEW EPISODE  ·  OUT NOW", where=1330, size=g["slam"] * 0.42,
                  color=ORANGE, anim="rise"))
    T.append(kicker(fmt, end_at + 0.4, DUR, "100.3 LEGENDS RADIO  ·  SPOTIFY  ·  YOUTUBE", where=1420, color=PURPLE))
    T += bats(end_at + 0.2, DUR, 5, 280, 420, seed=21, size=(60, 110))
    T += [still(end_at + 0.3, DUR, "🎃", 170, 1600, 120), still(end_at + 0.3, DUR, "🎃", 910, 1600, 120, phase=2.2),
          still(end_at + 0.5, DUR, "👻", 540, 1610, 110, bob=14)]
    return T


# ---------------------------------------------------------------- score
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


def organ(notes, d=0.9, g=1.0):
    """A pipe organ chord: drawbar harmonics, a slow tremolo, a long church reverb."""
    t = np.arange(int(d * S.SR)) / S.SR
    x = sum(np.sin(2 * np.pi * f * h * t) * w for f in notes for h, w in ((0.5, 0.6), (1, 1), (2, 0.6), (3, 0.3),
                                                                           (4, 0.25), (8, 0.12)))
    x *= (1 + 0.08 * np.sin(2 * np.pi * 6 * t)) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.25)
    return S.verb(x / len(notes) * 0.12 * g, wet=0.55, seconds=4.0, bright=3500)


def thunder(d=3.5, g=1.0):
    """A crack, then a long low rumble that rolls in waves."""
    t = np.arange(int(d * S.SR)) / S.SR
    crack = S.hp(S.noise(d), 1500) * np.exp(-t / 0.05) * 0.8
    roll = S.lp(S.noise(d), 160, 4) * np.exp(-t / 1.3) * (1 + 0.6 * np.sin(2 * np.pi * 1.7 * t) ** 2) * 3.0
    return S.verb(np.tanh(crack + roll) * g, wet=0.4, seconds=3.0, bright=2500)


def howl(d=2.4, g=1.0):
    """A wolf howl: a sine that swoops up, holds with a wobble, and falls away."""
    t = np.arange(int(d * S.SR)) / S.SR
    f = np.interp(t, [0, 0.5, 1.6, d], [330, 620, 600, 380]) * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / S.SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f) / S.SR)
    x *= np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.7)
    return S.verb(x * 0.25 * g, wet=0.6, seconds=3.5)


def score():
    sc = S.Score(DUR)
    # under the dialogue: a minor pad and the theremin, ducked by the mixer
    sc.m(S.pad(card_at, [110, 130.81, 164.81], attack=1.0), 0.0, 0.42)
    sc.m(theremin(card_at, [440, 415.3, 392, 349.2, 392, 349.2, 329.6, 311.1, 329.6]), 0.0, 0.42)
    # the card: riser, lightning, the organ "dun dun DUN", thunder underneath
    sc.m(S.riser(1.0), card_at - 1.0, 0.35)
    sc.s(thunder(), card_at, 0.75)
    sc.s(S.boom(1.0), card_at, 0.7)
    sc.m(organ([146.83, 174.61, 220.0], 0.32), card_at + 0.05, 0.9)          # D minor
    sc.m(organ([138.59, 164.81, 220.0], 0.32), card_at + 0.45, 0.9)          # A over C sharp
    sc.m(organ([73.42, 146.83, 174.61, 220.0], 1.6), card_at + 0.85, 1.0)    # D minor, held
    # second half: a slow spooky groove
    sc.groove(card_at + CARD, end_at, 96, "four", 0.3, root=55.0)
    sc.m(S.pad(end_at - card_at - CARD, [110, 130.81, 164.81, 207.65]), card_at + CARD, 0.3)
    sc.m(theremin(end_at - card_at - CARD, [329.6, 349.2, 392, 349.2, 329.6, 311.1]), card_at + CARD, 0.3)
    sc.s(S.boom(0.7), starts["skin"], 0.5)
    sc.m(S.riser(1.2), end_at - 1.2, 0.5)
    sc.s(thunder(3.0), end_at, 0.6)
    sc.s(S.boom(1.1, tail=3.4), end_at, 0.9)
    sc.m(S.pad(END, [110, 130.81, 164.81, 220]), end_at, 0.8)
    sc.s(howl(), end_at + 0.5, 0.55)
    for k, src, a, b in SEG:
        sc.d(load_audio("h21a", a, b), starts[k])
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
