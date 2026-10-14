"""Hero loop for /podcast.html — silent, no type, no flashes (it sits behind page text).
Mics, the board and the ON AIR sign; gentle push-ins, cut on a steady 1.4s pulse."""
from lib import *

shots = [
    shot("m15_mic", 1.4, push=0.05),
    shot("d14_talk", 1.4, push=0.05),
    shot("m11_gest", 1.4, push=0.05),
    shot("d14_laugh", 1.6, push=0.05),
    shot("w9_duo", 1.6, push=0.04),
    shot("m15_laugh", 1.4, push=0.05),
    shot("d16_onair", 1.4, push=0.04),
    shot("m14_laugh", 1.4, push=0.05),
    shot("d15_laugh", 1.4, push=0.05),
    shot("m11_gest2", 1.4, push=0.05),
]
DUR = sum(s["d"] for s in shots)
REEL = dict(shots=shots, texts=None, hits=[], flashes=[], blacks=[])
