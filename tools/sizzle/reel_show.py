"""Reel — THE SHOW TRAILER (~63s). Pain 2 Power as a show: Mike's voiceover is the spine
(his Ep 14 open and intro, his Ep 16 "great guests" line and sign-off), five guests with
name cards (drama + information), then Dave's dad joke and Mike's comeback (comedy), and
a title / tune-in finale. Owner notes 2026-10-14: Mike's VO louder (synth.Score mixes
voices up), fewer guests, more dramatic, comical and informational, keep the wording."""
import json
import os

import synth as S
import engine as E
from engine import load_audio, INSET16
from lib import *
from lib import _M14, _M16, _D14, _D16, _M11, _D15, _M15, _M9
from jokes import tighten

# guest clips (vertical, captions burned in below the regions given here)
E.SRC["c_leighton"] = f"{E.SCR}/src/clips/ep12_bestop.mp4"
E.SIZE["c_leighton"] = (1080, 1350)
E.REGION["c_leighton"] = (0, 0, 1080, 1000)
E.SRC["c_kerry"] = f"{E.SCR}/src/clips/ep13_searchlight.mp4"
E.SIZE["c_kerry"] = (1080, 1920)
E.REGION["c_kerry"] = (0, 0, 1080, 1450)
AUD = {"c_leighton": "ep12_bestop", "c_kerry": "ep13_searchlight"}

GW = json.load(open(os.path.join(E.SCR, "aud", "guest_words.json")))
JW = json.load(open(os.path.join(E.SCR, "aud", "joke_words.json")))
W16 = json.load(open(os.path.join(E.SCR, "aud", "words16.json")))

G_SABESAN = dict(src="ep9", fx=0.5, fy=0.4, z=1.15)
G_GOODWIN = dict(src="ep16", fx=0.62, fy=0.4, z=1.1)
G_JOYCE = dict(src="ep11", fx=0.5, fy=0.45, z=1.25)
G_LEIGHTON = dict(src="c_leighton", fx=0.6, fy=0.4, z=1.0)
G_KERRY = dict(src="c_kerry", fx=0.5, fy=0.4, z=1.0)

shots, dlg, caps, T_ = [], [], [], [0.0]
marks = {}


def now():
    return T_[0]


def black_(d):
    shots.append(black(d))
    T_[0] += d


def montage(names_durs):
    for n, d in names_durs:
        shots.append(shot(n, d))
        T_[0] += d


def _words_in(words, a, b, rename=None, skip=()):
    out = []
    for s, e, w in words:
        if a - 0.05 <= s < b and not any(x0 <= s < x1 for x0, x1 in skip):
            out.append((s, e, (rename or {}).get(round(s, 2), w)))
    return out


def sync(src, a, b, framing, words=(), tight=True, gain=1.0, rename=None, label=None):
    """Lip-synced piece: shots + audio + captions, long pauses cut like the dad jokes."""
    aud = AUD.get(src, src)
    pieces = tighten(aud, a, b) if tight else [(a, b)]
    t0 = now()
    starts = []
    for k, (p0, p1) in enumerate(pieces):
        shots.append(dict(framing, src=src, t=p0, d=p1 - p0, push=0.05, zmul=1.1 if k % 2 else 1.0))
        dlg.append((src, p0, p1, now(), gain))
        starts.append(now())
        T_[0] += p1 - p0
    # captions: a word whose ASR start lands in a trimmed pause snaps to the nearest piece
    for s, e, w in words:
        if not (a - 0.05 <= s < b):
            continue
        best = min(range(len(pieces)), key=lambda i: 0 if pieces[i][0] - 0.05 <= s < pieces[i][1]
                   else min(abs(s - pieces[i][0]), abs(s - pieces[i][1])))
        q0, q1 = pieces[best]
        st = min(max(s, q0), q1 - 0.15)
        caps.append((st - q0 + starts[best], min(max(e, st + 0.15), q1) - q0 + starts[best],
                     (rename or {}).get(round(s, 2), w)))
    if label:
        marks[label] = (t0, now())


def vo(src, a, b, visuals, words=(), label=None, gain=1.0):
    """Voiceover over a montage; visuals [(shot dict or name, dur)], last one stretched."""
    t0 = now()
    dlg.append((src, a, b, t0, gain))
    for s, e, w in words:
        caps.append((s - a + t0, e - a + t0, w))
    total = b - a
    used = 0.0
    for i, (v, d) in enumerate(visuals):
        d = total - used if i == len(visuals) - 1 else d
        sh = dict(SHOTS[v]) if isinstance(v, str) else dict(v)
        sh["d"] = d
        shots.append(sh)
        used += d
    T_[0] += total
    if label:
        marks[label] = (t0, now())


def w14(a, b):
    from json import load
    d = load(open(os.path.join(E.SCR, "aud", "ep14_tx.json")))
    return [(w[0], w[1], w[2].strip()) for s in d for w in s["w"] if a <= w[0] < b]


# ------------------------------------------------------------------ timeline
black_(0.7)                                                   # 100.3 LEGENDS RADIO PRESENTS
vo("ep14", 0.80, 8.95, [(dict(_M14, t=0.80), 1.7), ("d14_laugh", 1.2), ("m11_gest", 1.1), ("w9_duo", 1.4),
                        ("d16_onair", 1.0), ("m15_mic", 9)], label="open",
   words=[(s, e, {"Pain": "Pain", "to": "2"}.get(w, w) if 4.4 < s < 5.0 else w)
          for s, e, w in w14(0.8, 8.95)])
marks["hit1"] = now()
vo("ep14", 9.05, 15.45, [(dict(_M14, t=9.05), 1.3), ("m15_laugh", 1.4), ("w9_duo2", 1.6), ("d14_laugh2", 9)],
   label="intro")
vo("ep16", 10.35, 15.15, [("d15_point", 0.8), ("m9_point", 0.8), ("d14_wave", 0.8), ("m14_laugh", 0.8),
                          ("dk_smile", 0.8), ("m15_wave", 9)], label="great")
marks["surgeons"] = now()
black_(0.75)                                                  # THE SURGEONS.
sync("c_leighton", 0.95, 4.2, G_LEIGHTON, GW["ep12_bestop@0.0"], label="leighton")
sync("ep9", 794.95, 797.3, G_SABESAN, GW["ep9@793.0"], label="sabesan1")
sync("ep9", 800.05, 803.5, G_SABESAN, GW["ep9@793.0"], label="sabesan2")
marks["specialists"] = now()
black_(0.75)                                                  # THE SPECIALISTS.
sync("ep16", 349.25, 352.95, G_GOODWIN, GW["ep16@335.0"], rename={349.36: "Our"}, label="goodwin")
sync("ep11", 443.25, 445.95, G_JOYCE, GW["ep11@437.5"], label="joyce")
marks["captain"] = now()
black_(1.0)                                                   # ...AND A CAPTAIN FROM BELOW DECK.
sync("c_kerry", 3.2, 6.9, G_KERRY, GW["ep13_searchlight@0.0"], rename={3.24: "The"}, label="kerry")
sync("ep9", 803.95, 806.75, G_SABESAN, GW["ep9@793.0"], rename={804.02: "And"}, label="ninety")
marks["dave"] = now()
black_(1.1)                                                   # AND THEN THERE'S DAVE.
sync("ep16", 1483.6, 1487.95, _D16, JW["ep16"], label="grape",
     rename={1483.66: "What", 1487.64: "press?"})
sync("ep16", 1489.55, 1492.4, _M16, JW["ep16"], tight=False, rename={1489.76: "He", 1490.22: "whined."},
     label="whined")
marks["rim"] = marks["whined"][0] + (1490.75 - 1489.55)
# Mike's comeback
vo("ep16", 614.30, 616.55, [("m9_laugh2", 9)], words=[(s, e, w) for s, e, w in W16["610-630"] if 614.3 <= s < 616.5],
   label="never")
sync("ep16", 616.55, 618.65, _M16, [(616.58, 616.74, "Very"), (616.74, 617.36, "challenging"),
                                    (617.58, 617.7, "for"), (617.7, 617.8, "me"), (617.8, 617.88, "to"),
                                    (617.88, 618.04, "stay"), (618.04, 618.18, "still"), (618.18, 618.3, "that"),
                                    (618.3, 618.6, "long.")], tight=False, label="still")
marks["finale"] = now()
vo("ep16", 1606.75, 1609.75, [("d14_laugh2", 0.35), ("m9_laugh", 0.35), ("dk_laugh", 0.35), ("m11_gest3", 0.35),
                              ("d15_laugh", 0.35), ("m14_laugh", 0.35), ("w9_duo2", 9)], label="thishasbeen",
   words=[(s, e, {"to": "2"}.get(w, w)) for s, e, w in W16["1605-1630"] if 1606.7 <= s < 1609.7])
marks["title"] = now()
black_(2.6)
marks["end"] = now()
black_(3.2)
DUR = now()
OUT_AT = marks["title"][0] if isinstance(marks["title"], tuple) else marks["title"]
W_OUT = [(1622.46, 1622.62, "Pain"), (1622.62, 1622.8, "2"), (1622.8, 1623.08, "Power"), (1623.08, 1623.18, "on"),
         (1623.18, 1623.32, "a"), (1623.32, 1623.6, "South"), (1623.6, 1623.84, "Florida"), (1623.84, 1624.3, "Saturday.")]
OUT_SRC = 1622.40
hits = [marks["hit1"], marks["surgeons"], marks["specialists"], marks["captain"], marks["finale"], OUT_AT]
flashes = hits + [marks["rim"]]


def guest(fmt, label, name, cred):
    g = fmt_geom(fmt)
    t0, t1 = marks[label]
    sz = 58 if fmt == "9x16" else 54
    img = E.text_img([(name, E.INTER_BLACK, sz, CREAM), (cred, E.INTER_XB, sz * 0.58, GOLD)], g["W"], track=0.02,
                     stroke=4)
    y = g["top"] + (60 if fmt == "9x16" else 50)
    return Txt(t0 + 0.05, t1, img, (g["cx"], y), "rise")


def texts(fmt):
    g = fmt_geom(fmt)
    T = [kicker(fmt, 0.05, 0.7, "100.3 LEGENDS RADIO PRESENTS", where="card")]
    o0, o1 = marks["open"]
    T += captions(fmt, [(s - 0.80 + o0, e - 0.80 + o0, w) for s, e, w in
                        [(s, e, {"to": "2"}.get(w, w) if 4.8 < s < 5.3 else w) for s, e, w in w14(0.8, 8.95)]])
    T.append(kicker(fmt, 0.75, o1, "SATURDAYS  ·  8:30 AM"))
    i0, i1 = marks["intro"]
    off = i0 - 9.05
    T.append(slam(fmt, i0 + 0.05, i0 + 1.35, "THE VOICE."))
    T.append(name_card(fmt, i0 + 1.2, i0 + 2.6, "MIKE McGANN", "17 years on Palm Beach County radio"))
    T.append(slam(fmt, 14.17 + off, 14.17 + off + 0.9, "THE DOCTOR."))
    T.append(name_card(fmt, 14.17 + off + 0.8, i1, "DR. DAVE KASHUBA", "Founder, First Rehabilitation · since 1991"))
    g0, g1 = marks["great"]
    gof = g0 - 10.35
    for a, b, w in [(10.73, 11.42, "GREAT INFORMATION."), (11.42, 12.2, "GREAT GUESTS."), (12.27, 13.0, "TREMENDOUS"),
                    (13.03, 15.15, "STUFF TO LEARN.")]:
        T.append(slam(fmt, a + gof, min(b + gof, g1), w, size=g["slam"] * (0.82 if len(w) > 14 else 1.0)))
    T.append(slam(fmt, marks["surgeons"], marks["surgeons"] + 0.75, "THE SURGEONS.", where="card", color=GOLD))
    T.append(slam(fmt, marks["specialists"], marks["specialists"] + 0.75, "THE SPECIALISTS.", where="card", color=GOLD))
    c = marks["captain"]
    T.append(slam(fmt, c, c + 1.0, "AND A CAPTAIN", where=g["card"] - (60 if fmt == "9x16" else 70), color=CREAM))
    T.append(slam(fmt, c + 0.15, c + 1.0, "FROM BELOW DECK.", where=g["card"] + (60 if fmt == "9x16" else 70),
                  color=CORAL))
    d = marks["dave"]
    T.append(slam(fmt, d, d + 0.5, "AND THEN", where="card", color=CREAM))
    T.append(slam(fmt, d + 0.5, d + 1.1, "THERE'S DAVE.", where="card", color=GOLD))
    T.append(guest(fmt, "leighton", "DR. MICHAEL LEIGHTON, MD", "Orthopedic surgeon, Palm Beach Orthopedic Institute"))
    s1 = (marks["sabesan1"][0], marks["sabesan2"][1])
    marks["sabesan"] = s1
    T.append(guest(fmt, "sabesan", "DR. VANI SABESAN, MD", "Orthopaedic shoulder surgeon"))
    T.append(guest(fmt, "goodwin", "DR. DON GOODWIN", "Radiologist, TGH Imaging"))
    T.append(guest(fmt, "joyce", "PAUL JOYCE", "New Life HRT"))
    T.append(guest(fmt, "kerry", "CAPTAIN KERRY TITHERADGE", "Below Deck, Bravo"))
    T.append(guest(fmt, "ninety", "DR. VANI SABESAN, MD", "Orthopaedic shoulder surgeon"))
    T.append(kicker(fmt, marks["grape"][0], marks["whined"][1], "DAVE'S DAD JOKE"))
    cards = sorted([marks[k] for k in ("surgeons", "specialists", "captain", "dave", "title")])
    for c_ in captions(fmt, caps):
        if c_.t0 < marks["surgeons"]:
            continue
        nxt = next((x for x in cards if x > c_.t0 + 1e-3), DUR)
        c_.t1 = min(c_.t1, nxt)       # never let a caption bleed onto a black title card
        T.append(c_)
    # title + end
    t = OUT_AT
    T.append(image_card(fmt, t, marks["end"], f"{REPO}/assets/media/podcast-cover.jpg", 0.34,
                        y=g["card"] - (40 if fmt != "9x16" else 0), on="glow"))
    T += captions(fmt, [(s - OUT_SRC + t + 0.15, e - OUT_SRC + t + 0.15, w) for s, e, w in W_OUT],
                  y=(g["cap"] if fmt == "9x16" else 960), max_words=4)
    e = marks["end"]
    T.append(image_card(fmt, e, DUR, f"{REPO}/assets/media/logo-dark.png", 0.2,
                        y=(g["card"] - 210) if fmt != "9x16" else 640, anim="fade"))
    T.append(slam(fmt, e + 0.05, DUR, "SATURDAYS 8:30 AM", where=(g["card"] + 40) if fmt != "9x16" else 960,
                  size=g["slam"] * 0.62, anim="rise"))
    T.append(slam(fmt, e + 0.2, DUR, "100.3 LEGENDS RADIO", where=(g["card"] + 140) if fmt != "9x16" else 1065,
                  size=g["slam"] * 0.5, color=GOLD, anim="rise"))
    T.append(kicker(fmt, e + 0.4, DUR, "EVERY EPISODE ON SPOTIFY + YOUTUBE", where=(g["card"] + 250)
                    if fmt != "9x16" else 1180, color=CREAM))
    return T


def score():
    sc = S.Score(DUR)
    A = [110.0, 130.81, 164.81]
    o0, o1 = marks["open"]
    sc.m(S.pad(o1 + 0.3, A), 0.0, 0.9)
    sc.ticks(0.7, o1, 128, 0.45)
    sc.m(S.riser(1.8), o1 - 1.8, 0.7)
    sc.s(S.boom(), marks["hit1"], 1.0)
    sc.m(S.braam(2.6, 55.0), marks["hit1"], 0.8)
    i0, i1 = marks["intro"]
    sc.s(S.boom(0.8), 14.17 + i0 - 9.05, 0.8)
    sc.m(S.pad(i1 - i0, [98, 123.47, 146.83]), i0 + 1.0, 0.6)
    g0, g1 = marks["great"]
    sc.s(S.crash(), g0, 0.45)
    sc.groove(g0, g1, 128, "trap", 0.9)
    # guests: documentary drive
    for k in ("surgeons", "specialists", "captain"):
        t = marks[k]
        sc.s(S.whoosh(0.5), t - 0.3, 0.7)
        sc.s(S.boom(0.75), t, 0.85)
        sc.s(S.stab([110, 138.59, 164.81]), t, 0.6)
    gs, ge = marks["surgeons"], marks["ninety"][1]
    sc.groove(gs + 0.75, ge, 120, "four", 0.6)
    sc.m(S.pad(ge - gs, [110, 130.81, 164.81, 220]), gs, 0.6)
    sc.tapestop(marks["dave"] - 0.05, 0.45, until=marks["finale"])
    d = marks["dave"]
    sc.s(S.tick(), d + 0.5, 0.8)
    sc.s(S.stab([220, 261.6, 329.6]), d + 0.5, 0.7)
    sc.ticks(marks["grape"][0], marks["grape"][1], 96, 0.25)
    r = marks["rim"]
    sc.s(S.tom(190), r, 0.8)
    sc.s(S.tom(140), r + 0.15, 0.8)
    sc.s(S.kick(), r + 0.32, 0.8)
    sc.s(S.crash(1.6), r + 0.32, 0.7)
    sc.s(S.kick(), marks["still"][1] - 0.1, 0.6)
    sc.s(S.crash(1.2), marks["still"][1] - 0.1, 0.4)
    f = marks["finale"]
    sc.s(S.reverse_swell(1.0), f - 1.0, 0.5)
    sc.s(S.boom(), f, 1.0)
    sc.m(S.braam(2.4, 55.0), f, 0.8)
    sc.groove(f, OUT_AT, 128, "four", 1.0)
    sc.s(S.boom(1.3, tail=4.0), OUT_AT, 1.0)
    sc.m(S.braam(4.0, 41.2), OUT_AT, 0.85)
    sc.m(S.pad(DUR - OUT_AT, A + [220]), OUT_AT, 0.9)
    sc.s(S.stab([220, 261.6, 329.6]), marks["end"], 0.6)
    for src, a, b, t, gain in dlg:
        sc.d(load_audio(src, a, b), t, gain)
    sc.d(load_audio("ep16", OUT_SRC, 1624.35), OUT_AT + 0.15)
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
