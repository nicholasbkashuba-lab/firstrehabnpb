#!/usr/bin/env python3
"""Run the clip QA gate on the files Post Bridge will actually publish.

    python3 tools/media-qa.py URL [URL ...] [--style box|pop]

Post Bridge stores an uploaded COPY, so the file a scheduled post will publish can differ from the one on
disk (CLAUDE.md, "Re-check the media on scheduled posts after ANY re-cut"). The daily routine passes the
signed URLs `list_media` returns for tomorrow's video posts; this downloads each to a temp dir and runs
tools/clip-qa.py on it, which now includes the ending check (tools/cut_check.py: no clip may end while
someone is still talking). Exit 1 if any file FAILs. Sizzle reels carry music and word-pop captions:
pass --style pop for those.
"""
import os
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    args = sys.argv[1:]
    style = "box"
    if "--style" in args:
        i = args.index("--style")
        style = args[i + 1]
        del args[i:i + 2]
    if not args:
        sys.exit(__doc__)
    tmp = tempfile.mkdtemp(prefix="media-qa-")
    files = []
    for n, url in enumerate(args):
        path = os.path.join(tmp, f"media{n:02d}.mp4")
        urllib.request.urlretrieve(url, path)
        files.append(path)
    r = subprocess.run([sys.executable, os.path.join(HERE, "clip-qa.py"), *files, "--style", style])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
