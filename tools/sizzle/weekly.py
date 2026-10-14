"""This week's episode as one sizzle reel (Nick, 2026-10-14: "I'd love to post a sizzle reel
of the current week's episode each time").

The October reels were hand-built shot lists over a fixed set of masters. This turns the
same engine into a weekly template: an episode is a short JSON file naming its master and
four to six of its best lines, and the builder does the rest.

    episodes/ep18.json   ->   SIZZLE_EP=ep18 python3 run.py reel_week 9x16 16x9

Shape, about 20 to 30 s:
  1. Cold open on the strongest line, lip synced, word-pop captions.
  2. Three to five more lines, hard cuts on a beat, the guest's name over their first line.
  3. End card: show artwork, a headline (default "NEW EPISODE · SATURDAY 8:30 AM") and the
     100.3 Legends / Spotify / YouTube line.
The score is synthesized (synth.py), so nothing is licensed and nothing is muted on upload.
Music ducks under the dialogue automatically.

The episode JSON (times are MASTER times, i.e. the edited multicam, not the RAW mp3):
{
  "episode": 18,
  "src": "ep18",                       # work dir key: $SIZZLE_WORK/src/ep18/master.mp4
  "size": [1920, 1080],
  "end_title": "NEW EPISODE  ·  SATURDAY 8:30 AM",     # optional
  "moments": [
    {"a": 304.20, "b": 306.70,         # in and out
     "fx": 0.46, "fy": 0.42, "z": 1.1, # 16:9 framing (focus as a fraction of the frame)
     "v": {"fx": 0.46, "fy": 0.42},    # 9:16 framing; set fx on the speaker's face
     "name": "ELYSE MARRONE", "sub": "REGISTERED DIETITIAN",   # optional, first line only
     "cams": [[305.9, {"fx": 0.3, "v": {"fx": 0.3}}]],          # optional camera switches
     "words": [[304.54, 304.64, "I"], ...]}                      # reviewed caption words
  ]
}

Choosing the lines is the judgment call, and it belongs to the episode session (see the
pain2power-episode skill): hook first, each line complete on its own, no line that needs
the setup it was cut from, nothing clinical stated as advice. Check every in-point on a
frame: the multicam master switches camera a few frames off the transcript (README).
"""
import json
import os

import synth as S
import engine as E
from engine import load_audio, Txt, text_img, INTER_BLACK, INTER_XB, CREAM, GOLD
from lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
END = 3.4  # end card


def load(key):
    with open(os.path.join(HERE, "episodes", f"{key}.json")) as fh:
        return json.load(fh)


def _register(cfg):
    """Teach the engine about this week's master without editing engine.py."""
    src = cfg["src"]
    E.SRC.setdefault(src, os.path.join(E.SCR, "src", src, "master.mp4"))
    E.SIZE.setdefault(src, tuple(cfg.get("size", (1920, 1080))))
    if not os.path.exists(E.SRC[src]):
        raise SystemExit(f"master not found: {E.SRC[src]} (copy or link the episode's multicam there)")


def _framing(src, m):
    f = dict(src=src, fx=m.get("fx", 0.5), fy=m.get("fy", 0.45), z=m.get("z", 1.0))
    v = m.get("v") or {}
    f["9x16"] = dict(fx=v.get("fx", f["fx"]), fy=v.get("fy", f["fy"]), z=v.get("z", 1.0))
    return f


def _name_card(fmt, t0, t1, name, sub):
    """Guest name high in the frame, clear of faces and of the captions at the bottom."""
    g = fmt_geom(fmt)
    img = text_img([(name, INTER_BLACK, g["name"] * 0.8, CREAM), (sub, INTER_XB, g["sub"], GOLD)], g["W"],
                   track=0.015, stroke=max(3, int(g["name"] * 0.8) // 20))
    if img.width > g["W"] * 0.92:
        from PIL import Image
        img = img.resize((int(g["W"] * 0.92), int(img.height * g["W"] * 0.92 / img.width)), Image.LANCZOS)
    y = 420 if fmt == "9x16" else 230
    return Txt(t0, t1, img, (g["cx"], y), "rise")


def build(key):
    cfg = load(key)
    _register(cfg)
    src = cfg["src"]
    ep_no = cfg["episode"]

    shots, dlg, caps, cuts, names = [], [], [], [], []
    T = 0.0
    for m in cfg["moments"]:
        a, b = m["a"], m["b"]
        base = _framing(src, m)
        switches = [(t, _framing(src, dict(m, **c))) for t, c in m.get("cams", []) if a < t < b]
        edges = [a] + [t for t, _ in switches] + [b]
        frames = [base] + [f for _, f in switches]
        for (x0, x1), fr in zip(zip(edges, edges[1:]), frames):
            shots.append(dict(fr, t=x0, d=x1 - x0, push=0.06))
        dlg.append((a, b, T))
        for s, e, w in m.get("words", []):
            if a - 0.05 <= s < b:
                caps.append((s - a + T, min(e, b) - a + T, w))
        if m.get("name"):
            names.append((T + 0.25, T + min(2.6, b - a - 0.1), m["name"], m.get("sub", "")))
        T += b - a
        cuts.append(T)
    cuts = cuts[:-1]
    end_t = T
    shots.append(black(END))
    dur = T + END
    end_title = cfg.get("end_title", "NEW EPISODE  ·  SATURDAY 8:30 AM")

    def texts(fmt):
        g = fmt_geom(fmt)
        out = [kicker(fmt, 0.0, end_t, f"PAIN 2 POWER  ·  EPISODE {ep_no}")]
        # Captions at the very bottom, Nick's standard for every clip (2026-10-09); the
        # October reels place them higher, so this overrides lib's default y.
        out += captions(fmt, caps, max_words=3, max_chars=18, y=1745 if fmt == "9x16" else 985)
        for t0, t1, n, s in names:
            out.append(_name_card(fmt, t0, t1, n, s))
        out.append(image_card(fmt, end_t, dur, f"{REPO}/assets/media/podcast-cover.jpg", 0.3,
                              y=(g["card"] - 120) if fmt != "9x16" else 820, on="glow"))
        out.append(slam(fmt, end_t + 0.15, dur, end_title,
                        where=(g["card"] + 250) if fmt != "9x16" else 1290, size=g["slam"] * 0.42, anim="rise"))
        out.append(kicker(fmt, end_t + 0.3, dur, "100.3 LEGENDS RADIO  ·  SPOTIFY  ·  YOUTUBE",
                          where=(g["card"] + 340) if fmt != "9x16" else 1380, color=GOLD))
        return out

    def score():
        sc = S.Score(dur)
        sc.m(S.pad(end_t + 0.2, [110, 130.81, 164.81], g=0.8), 0.0, 0.5)
        sc.groove(0.0, end_t, 120, "trap", 0.45)
        for c in cuts:
            sc.s(S.whoosh(0.45), c - 0.3, 0.35)
            sc.s(S.kick(), c, 0.5)
        sc.m(S.riser(1.4), end_t - 1.4, 0.45)
        sc.s(S.boom(1.0, tail=3.0), end_t, 0.9)
        sc.m(S.braam(END, 55.0), end_t, 0.55)
        sc.s(S.stab([220, 261.6, 329.6]), end_t, 0.5)
        for a, b, t in dlg:
            sc.d(load_audio(src, a, b), t)
        return sc

    reel = dict(shots=shots, texts=texts, hits=[end_t], flashes=[end_t], blacks=[])
    return reel, dur, score
