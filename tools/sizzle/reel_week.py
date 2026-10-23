"""This week's episode sizzle reel. One module serves every week; the episode comes from
the environment because run.py treats every other argument as an output format:

    SIZZLE_EP=ep18 python3 run.py reel_week 9x16 16x9
"""
import os

from weekly import build

_key = os.environ.get("SIZZLE_EP")
if not _key:
    raise SystemExit("set SIZZLE_EP=ep{NN} (the episodes/ep{NN}.json to build)")
REEL, DUR, score = build(_key)
