#!/usr/bin/env python3
"""Spot a new Pain 2 Power episode the moment Nick drops it in Dropbox.

Nick records on a Tuesday or so, drops the radio mp3 and the camera files into
/Pain2Power/<Guest>/, and until now had to open a session and paste the folder
link to get anything started. This reads that folder tree and says which guest
folders are ready to be processed, so the episode watcher routine can start the
work on its own.

  python3 tools/episode-watch.py            # human-readable status of every folder
  python3 tools/episode-watch.py --json     # same, machine readable
  python3 tools/episode-watch.py --ready    # only folders ready to process; exit 1 if any

A folder's state, decided from what is in it:
  done        Final/ holds a finished .mp4 (the multicam master is delivered)
  claimed     Final/ exists but holds no .mp4 yet: a session is working on it.
              The first thing the episode runbook does is create Final/, so it
              doubles as a lock and two sessions never take the same episode.
  ready       no Final/, an audio master AND at least one camera file, and
              nothing in it has changed for STABLE_MINUTES (an upload in
              progress shows files whose modified time keeps moving)
  uploading   no Final/, but something changed in the last STABLE_MINUTES
  incomplete  no Final/, and either the audio or every camera file is missing
  legacy      listed in LEGACY: processed before the Final/ convention existed

Uses the Dropbox REST API through tools/dropbox-put.py, so the credential the
environment Setup script writes is all it needs. No connector required.
"""

import argparse
import importlib.util
import json
import os
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "/Pain2Power"

AUDIO = (".mp3", ".wav", ".m4a", ".aac", ".flac")
VIDEO = (".mp4", ".mov", ".m4v", ".mkv")

# A phone upload of a 6 GB camera file can stall for minutes between chunks.
# Forty-five quiet minutes is long enough that "nothing moved" means finished.
STABLE_MINUTES = 45

# Episodes 8 to 18 were processed before Final/ was used as the claim marker,
# so their folders cannot be judged by it. Never reprocess these.
LEGACY = {
    "Arlosoroff", "Butler", "Dr. Goodwin", "Kerry", "Leighton", "McVicker",
    "Paul Joyce", "Pilates", "Sabesan", "Simovitch", "Susan Mann",
}


def _dropbox():
    spec = importlib.util.spec_from_file_location(
        "dropbox_put", os.path.join(ROOT, "tools", "dropbox-put.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _when(entry):
    return datetime.fromisoformat(entry["server_modified"].replace("Z", "+00:00"))


def classify(dbx, token, name):
    path = f"{BASE}/{name}"
    entries = dbx.list_folder(token, path)
    files = [e for e in entries if e[".tag"] == "file"]
    folders = {e["name"].lower() for e in entries if e[".tag"] == "folder"}
    audio = [e for e in files if e["name"].lower().endswith(AUDIO)]
    video = [e for e in files if e["name"].lower().endswith(VIDEO)]
    info = {
        "folder": name,
        "path": path,
        "audio": [e["name"] for e in audio],
        "video": [e["name"] for e in video],
        "bytes": sum(e["size"] for e in files),
    }
    if files:
        info["last_change"] = max(_when(e) for e in files).strftime("%Y-%m-%dT%H:%M:%SZ")

    if name in LEGACY:
        info["state"] = "legacy"
    elif "final" in folders:
        final = dbx.list_folder(token, f"{path}/Final")
        done = any(e[".tag"] == "file" and e["name"].lower().endswith(VIDEO) for e in final)
        info["state"] = "done" if done else "claimed"
    elif not audio or not video:
        info["state"] = "incomplete"
    elif datetime.now(timezone.utc) - max(_when(e) for e in files) < timedelta(minutes=STABLE_MINUTES):
        info["state"] = "uploading"
    else:
        info["state"] = "ready"
    return info


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--ready", action="store_true",
                    help="list only folders ready to process; exit 1 when there are any")
    args = ap.parse_args()

    dbx = _dropbox()
    token = dbx.access_token(dbx.load_credentials(None))
    names = sorted(e["name"] for e in dbx.list_folder(token, BASE) if e[".tag"] == "folder")
    rows = [classify(dbx, token, n) for n in names]
    if args.ready:
        rows = [r for r in rows if r["state"] == "ready"]

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        for r in rows:
            gb = r["bytes"] / 1e9
            print(f"{r['state']:10}  {r['folder']:16}  {gb:6.1f} GB  "
                  f"audio {len(r['audio'])}  video {len(r['video'])}  "
                  f"last change {r.get('last_change', '-')}")
        if args.ready and not rows:
            print("nothing ready")
    if args.ready:
        sys.exit(1 if rows else 0)


if __name__ == "__main__":
    main()
