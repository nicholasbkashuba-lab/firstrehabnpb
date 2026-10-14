"""Reel 1 — THE TRAILER (~35s). Movie-trailer cut: cold open on Mike's welcome,
character slams for Dave and Mike, a montage drop, a record-stop gag, the dad joke,
a finale burst and the title + tune-in card."""
import synth as S
from lib import *
from engine import load_audio

E16 = "ep16"
VO1 = 0.7      # ep16 audio t -> timeline t - VO1   ("Good morning and welcome...")
VO2 = 0.17     # ("Always so much great information...")

shots = [
    black(0.6),
    m16(0.6 + VO1, 1.3),                 # "Good morning and"
    shot("m15_mic", 0.7),
    shot("d14_talk", 0.65),
    m16(3.25 + VO1, 1.1),                # "to Pain 2 Power right"
    shot("m11_gest2", 0.85),
    shot("d16_onair", 0.7),
    m16(5.9 + VO1, 1.0),                 # "Legends 100.3"
    shot("d14_laugh", 1.6, push=0.1),    # THE DOCTOR
    shot("m11_gest", 1.6, push=0.1),     # THE VOICE
    shot("d15_point", 0.7),              # montage drop
    shot("m9_point", 0.7),
    shot("d14_wave", 0.7),
    shot("m14_laugh", 0.7),
    shot("dk_smile", 0.7),
    shot("m15_wave", 0.7),
    shot("d15_grin", 0.7),
    shot("m9_laugh2", 2.35, push=0.03),   # (Mike, listening) "That's something Mike can never do."
    m16(616.55, 1.75),                    # "Very challenging for me to stay still that long."
    black(1.3),                          # AND YES... / THE DAD JOKES.
    d16(1483.9, 4.0),                    # the grape setup, Dave on camera
    m16(1488.9, 0.6),                    # beat
    m16(1489.5, 2.9),                    # "He whined." + Mike cracking up
    shot("d14_laugh2", 0.35),            # finale burst
    shot("m9_laugh", 0.35),
    shot("dk_laugh", 0.35),
    shot("m11_gest3", 0.35),
    shot("d15_laugh", 0.35),
    shot("m14_laugh", 0.35, t=1378.2),
    black(5.0),                          # title + end card
]
DUR = sum(s["d"] for s in shots)

hits = [6.9, 8.5, 10.1, 27.9, 30.0]
flashes = [6.9, 8.5, 10.1, 19.8, 27.9, 30.0]

# reviewed against transcript-full.md (ASR heard "We used to stay still")
W_VO1 = [(1.38, 1.86, "Good"), (1.86, 2.28, "morning"), (2.28, 2.96, "and"), (2.96, 3.34, "welcome"),
         (3.34, 3.62, "once"), (3.62, 3.86, "again"), (3.86, 4.06, "to"), (4.06, 4.22, "Pain"),
         (4.22, 4.42, "2"), (4.42, 4.66, "Power"), (4.66, 5.14, "right"), (5.14, 5.48, "here"),
         (5.48, 6.08, "on"), (6.08, 6.38, "Legends"), (6.38, 7.5, "100.3")]
W_DAVE = [(614.42, 614.64, "That's"), (614.64, 614.88, "something"), (614.88, 615.14, "Mike"),
          (615.14, 615.32, "can"), (615.32, 615.56, "never"), (615.56, 616.2, "do.")]
W_MIKE = [(616.58, 616.74, "Very"), (616.74, 617.36, "challenging"), (617.58, 617.7, "for"),
          (617.7, 617.8, "me"), (617.8, 617.88, "to"), (617.88, 618.04, "stay"), (618.04, 618.18, "still"),
          (618.18, 618.3, "that"), (618.3, 618.6, "long.")]
W_JOKE = [(1484.1, 1484.42, "What"), (1484.42, 1484.52, "do"), (1484.52, 1484.62, "you"),
          (1484.62, 1484.76, "think"), (1484.76, 1485.04, "the"), (1485.04, 1486.16, "grape"),
          (1486.16, 1486.38, "did"), (1486.38, 1486.54, "when"), (1486.54, 1486.66, "he"),
          (1486.66, 1486.84, "saw"), (1486.84, 1486.98, "the"), (1486.98, 1487.22, "farmer"),
          (1487.22, 1487.4, "with"), (1487.4, 1487.56, "the"), (1487.56, 1487.9, "press?")]
W_WHINE = [(1489.64, 1490.08, "He"), (1490.08, 1490.8, "whined.")]
W_OUT = [(1622.46, 1622.62, "Pain"), (1622.62, 1622.8, "2"), (1622.8, 1623.08, "Power"),
         (1623.08, 1623.18, "on"), (1623.18, 1623.32, "a"), (1623.32, 1623.6, "South"),
         (1623.6, 1623.84, "Florida"), (1623.84, 1624.3, "Saturday.")]
OUT_AT = 30.25 - 1622.40

# timeline offsets of the synced dialogue pieces
DAVE_AT = 15.10 - 614.30       # VO over Mike listening
JOKE_AT = 20.4 - 1483.9
WHINE_AT = 24.4 - 1488.9


def texts(fmt):
    g = fmt_geom(fmt)
    T = []
    T.append(kicker(fmt, 0.05, 0.6, "LEGENDS 100.3 FM", where="mid" if fmt != "9x16" else "top"))
    T += captions(fmt, words_from(W_VO1, -VO1))
    if fmt == "9x16":
        T.append(kicker(fmt, 0.7, 6.85, "SATURDAYS 8:30 AM"))
    T.append(slam(fmt, 6.9, 7.65, "THE DOCTOR.", where="mid" if fmt != "9x16" else "top"))
    T.append(name_card(fmt, 7.55, 8.5, "DR. DAVE KASHUBA", "Founder, First Rehabilitation · since 1991"))
    T.append(slam(fmt, 8.5, 9.25, "THE VOICE.", where="mid" if fmt != "9x16" else "top"))
    T.append(name_card(fmt, 9.15, 10.1, "MIKE McGANN", "17 years on Palm Beach County radio"))
    # VO2 words land as kinetic slams
    for t0, t1, w in [(10.73, 11.42, "GREAT INFORMATION."), (11.42, 12.2, "GREAT GUESTS."),
                      (12.27, 13.0, "TREMENDOUS"), (13.03, 14.95, "STUFF TO LEARN.")]:
        T.append(slam(fmt, t0 - VO2, t1 - VO2, w, where="mid" if fmt != "9x16" else "top",
                      size=g["slam"] * (0.82 if len(w) > 14 else 1.0), darken=0.25))
    T += captions(fmt, words_from(W_DAVE, DAVE_AT))
    T += captions(fmt, words_from(W_MIKE, DAVE_AT))
    T.append(slam(fmt, 19.1, 19.8, "AND YES…", where="mid", color=CREAM))
    T.append(slam(fmt, 19.8, 20.4, "THE DAD JOKES.", where="mid", color=GOLD))
    T += captions(fmt, words_from(W_JOKE, JOKE_AT), max_words=4, max_chars=22)
    T += captions(fmt, words_from(W_WHINE, WHINE_AT), end_pad=0.6)
    # title
    T.append(image_card(fmt, 30.0, 32.3, f"{REPO}/assets/media/podcast-cover.jpg", 0.36,
                        y=g["mid"] - (40 if fmt != "9x16" else 0), on="glow"))
    T += captions(fmt, words_from(W_OUT, OUT_AT), y=(g["cap"] if fmt == "9x16" else 960), max_words=4)
    # end card
    T.append(image_card(fmt, 32.3, DUR, f"{REPO}/assets/media/logo-dark.png", 0.2,
                        y=(g["mid"] - 210) if fmt != "9x16" else 640, anim="fade"))
    T.append(slam(fmt, 32.35, DUR, "SATURDAYS 8:30 AM", where=(g["mid"] + 40) if fmt != "9x16" else 960,
                  size=g["slam"] * 0.62, anim="rise", darken=0))
    T.append(slam(fmt, 32.5, DUR, "100.3 LEGENDS RADIO", where=(g["mid"] + 140) if fmt != "9x16" else 1065,
                  size=g["slam"] * 0.5, color=GOLD, anim="rise", darken=0))
    T.append(kicker(fmt, 32.7, DUR, "SPOTIFY · YOUTUBE · FIRSTREHABNPB.COM",
                    where=(g["mid"] + 250) if fmt != "9x16" else 1180, color=CREAM))
    return T


def score():
    sc = S.Score(DUR)
    A = [110.0, 130.81, 164.81]
    sc.m(S.pad(10.2, A), 0.0, 1.0)
    sc.ticks(0.6, 6.9, 128, 0.5)
    sc.m(S.riser(2.0), 4.9, 0.8)
    sc.s(S.reverse_swell(1.0), 5.9, 0.5)
    sc.s(S.boom(), 6.9, 1.0)
    sc.m(S.braam(2.4, 55.0), 6.9, 0.9)
    sc.s(S.whoosh(0.5, up=True), 8.0, 0.6)
    sc.s(S.boom(), 8.5, 0.95)
    sc.m(S.braam(2.0, 49.0), 8.5, 0.85)
    sc.s(S.reverse_swell(0.9), 9.2, 0.5)
    sc.s(S.boom(), 10.1, 0.9)
    sc.s(S.crash(), 10.1, 0.5)
    sc.groove(10.1, 15.0, 128, "trap", 0.95)
    sc.m(S.pad(5.0, [110, 130.81, 164.81, 220]), 10.1, 0.8)
    sc.tapestop(15.0, 0.5, until=19.05)
    # dad joke section
    sc.s(S.whoosh(0.6, up=True), 18.6, 0.7)
    sc.s(S.stab([110, 138.59, 164.81]), 19.1, 0.9)
    sc.s(S.boom(0.7), 19.8, 0.8)
    sc.ticks(20.4, 24.4, 96, 0.28)
    sc.m(S.pad(4.6, [55, 82.41]), 20.4, 0.9)
    tr = 26.1
    sc.s(S.tom(190), tr, 0.8)
    sc.s(S.tom(140), tr + 0.15, 0.8)
    sc.s(S.kick(), tr + 0.32, 0.8)
    sc.s(S.crash(1.6), tr + 0.32, 0.7)
    # finale
    sc.s(S.reverse_swell(1.2), 26.8, 0.6)
    sc.s(S.boom(), 27.9, 1.0)
    sc.m(S.braam(2.2, 55.0), 27.9, 0.85)
    sc.groove(27.9, 30.0, 128, "four", 1.0)
    sc.m(S.riser(1.5), 28.5, 0.7)
    sc.s(S.boom(1.3, tail=4.0), 30.0, 1.0)
    sc.m(S.braam(4.0, 41.2), 30.0, 0.9)
    sc.m(S.pad(5.0, [110, 130.81, 164.81, 220]), 30.0, 1.0)
    sc.s(S.stab([220, 261.6, 329.6]), 32.3, 0.6)
    sc.s(S.sub808(41.2, 2.0), 32.3, 0.6)
    # dialogue
    sc.d(load_audio(E16, 1.30, 7.65), 1.30 - VO1)
    sc.d(load_audio(E16, 10.35, 15.15), 10.35 - VO2)
    sc.d(load_audio(E16, 614.30, 618.65), 614.30 + DAVE_AT)
    sc.d(load_audio(E16, 1483.9, 1487.95), 1483.9 + JOKE_AT)
    sc.d(load_audio(E16, 1488.9, 1492.35), 1488.9 + WHINE_AT, 0.95)
    sc.d(load_audio(E16, 1622.40, 1624.0), 1622.40 + OUT_AT)
    return sc


REEL = dict(shots=shots, texts=texts, hits=hits, flashes=flashes, blacks=[])
