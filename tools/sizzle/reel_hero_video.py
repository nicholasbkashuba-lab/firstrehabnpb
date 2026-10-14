"""Hero loop for /videos.html — silent, no type, no flashes. On-camera energy:
laughs, hands, the two-shot."""
from lib import *

shots = [
    shot("w9_duo2", 1.6, push=0.04),
    shot("d14_wave", 1.4, push=0.05),
    shot("m11_gest3", 1.4, push=0.05),
    shot("dk_laugh", 1.4, push=0.05),
    shot("m15_wave", 1.4, push=0.05),
    shot("d14_laugh2", 1.4, push=0.05),
    shot("m9_point", 1.4, push=0.05),
    shot("d15_grin", 1.4, push=0.05),
    shot("m14_laugh", 1.4, push=0.05, t=1378.0),
    shot("d15_point", 1.4, push=0.05),
]
DUR = sum(s["d"] for s in shots)
REEL = dict(shots=shots, texts=None, hits=[], flashes=[], blacks=[])
