"""Hero loop for /videos.html — silent, no type, no flashes. On-camera energy:
laughs, hands, the two-shot. All 1080p masters (no 720p Ep 15)."""
from lib import *

shots = [
    shot("w9_duo2", 1.6, push=0.04),
    shot("d14_laugh2", 1.4, push=0.05),
    shot("m11_gest3", 1.4, push=0.05),
    shot("d14_talk2", 1.4, push=0.05),
    shot("m9_point", 1.4, push=0.05),
    shot("d14_wave", 1.4, push=0.05),
    shot("m14_laugh", 1.4, push=0.05, t=1378.0),
    shot("d14_laugh", 1.4, push=0.05, t=902.6),
    shot("m9_laugh2", 1.4, push=0.05),
    shot("d14_talk", 1.4, push=0.05, t=68.0),
]
DUR = sum(s["d"] for s in shots)
REEL = dict(shots=shots, texts=None, hits=[], flashes=[], blacks=[])
