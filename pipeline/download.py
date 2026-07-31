#!/usr/bin/env python3
"""Parallel-download the sources listed in links.json (Dropbox temp links are
short-lived, so all first requests must fire immediately) and verify sizes."""
import json, os, subprocess, sys

links = json.load(open(os.path.join(os.path.dirname(__file__), "links.json")))
procs = {n: subprocess.Popen(["curl", "-sS", "--fail", "--retry", "2", "-L", "-o", n, v["url"]])
         for n, v in links.items()}
bad = [n for n, p in procs.items() if p.wait() != 0]
if bad:
    sys.exit(f"downloads failed: {bad}")
for n, v in links.items():
    got = os.path.getsize(n)
    assert got == v["size"], f"{n}: {got} != {v['size']}"
    print(n, "ok", got, flush=True)
