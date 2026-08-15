#!/usr/bin/env python3
"""Move big files: Dropbox -> this sandbox -> somewhere that needs the bytes.

Dropbox hosts were blocked by the egress policy until 2026-08-15. They are
allowlisted now (www.dropbox.com, *.dropboxusercontent.com, api.dropboxapi.com,
content.dropboxapi.com), so the old workarounds are dead: no public share links,
no `st=` tokens, no GitHub Actions relay. Get a link from the Dropbox MCP's
`download_link` and pull the bytes straight down at ~35 MB/s.

This script cannot mint the link itself — `download_link` is an MCP call, not an
HTTP one. The caller supplies the URL. That seam is deliberate and the reason
this is a script rather than a one-liner: everything AROUND the transfer is
where the failures live.

    # pull a file down
    python3 tools/dropbox-grab.py fetch --url "<download_url>" \
        --out /tmp/scratch/mikecam.mov --size 12568134602

    # hand it to a presigned PUT endpoint (Descript, S3, GCS...)
    python3 tools/dropbox-grab.py push --file /tmp/scratch/mikecam.mov \
        --url "<upload_url>"

    # both, deleting the local copy afterwards
    python3 tools/dropbox-grab.py relay --url "<download_url>" \
        --upload-url "<upload_url>" --size 12568134602 --work /tmp/scratch

Four things that each cost real time when learned the hard way:

1. **Never `curl --data-binary @file` for an upload.** It buffers the entire
   file in memory. It works on a 69 MB mp3 and dies on a 6.6 GB camera with
   "out of memory", after which the destination has a half-created record. Use
   `-T`, which streams. This script only ever uses `-T`.
2. **`download_link` URLs are single use**, consumed by the FIRST request of any
   method — a HEAD or a Range preflight burns them. Never probe one. If a
   transfer fails, mint a new link.
3. **Verify size, never sha256.** Dropbox's `content_hash` is its own
   block-based algorithm and will never equal a sha256 of the file. Byte count
   is exact and is the real check.
4. **Check free disk first.** The sandbox has ~30 GB writable. Three 4K cameras
   are 26.7 GB together, so they only fit one at a time.
"""
import argparse
import os
import shutil
import subprocess
import sys

# curl's own timeout, seconds. 12.6 GB at the ~17 MB/s upload rate is ~12
# minutes; this leaves generous headroom without hanging forever on a dead link.
TIMEOUT = 3000


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if abs(n) < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024


def free_bytes(path):
    return shutil.disk_usage(path).free


def fetch(url, out, expect_size=None):
    parent = os.path.dirname(os.path.abspath(out)) or "."
    os.makedirs(parent, exist_ok=True)

    if expect_size:
        avail = free_bytes(parent)
        if expect_size > avail:
            sys.exit(f"need {human(expect_size)} but only {human(avail)} free "
                     f"on {parent}. Delete something first — the sandbox holds "
                     f"about 30 GB and one 4K camera at a time.")

    r = subprocess.run(
        ["curl", "-sS", "-L", "--max-time", str(TIMEOUT), "-o", out,
         "-w", "%{http_code} %{size_download}", url],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"download failed ({r.returncode}): {r.stderr.strip()}\n"
                 f"download_link URLs are single use — mint a fresh one.")
    code, got = r.stdout.strip().split()[:2]
    got = int(got)

    if code != "200":
        sys.exit(f"download returned HTTP {code}. The link was probably already "
                 f"used or has expired; mint a fresh one.")

    actual = os.path.getsize(out)
    if expect_size and actual != expect_size:
        sys.exit(f"SIZE MISMATCH: got {actual} bytes, expected {expect_size}. "
                 f"Treat this as a failed transfer and retry.")

    print(f"fetched {out}  {actual} bytes ({human(actual)})"
          + ("  size verified" if expect_size else "  (no --size given, unverified)"))
    return actual


def push(path, url):
    if not os.path.isfile(path):
        sys.exit(f"no such file: {path}")
    size = os.path.getsize(path)

    # -T streams from disk. --data-binary would read the whole file into RAM
    # and OOM; see the module docstring.
    r = subprocess.run(
        ["curl", "-sS", "-X", "PUT", "-H", "Content-Type: application/octet-stream",
         "-T", path, "--max-time", str(TIMEOUT), "-o", "/dev/null",
         "-w", "%{http_code} %{size_upload}", url],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"upload failed ({r.returncode}): {r.stderr.strip()}")
    code, sent = r.stdout.strip().split()[:2]
    sent = int(sent)

    if code not in ("200", "201", "204"):
        sys.exit(f"upload returned HTTP {code} after {sent} bytes")
    if sent != size:
        sys.exit(f"SHORT UPLOAD: sent {sent} of {size} bytes. The destination "
                 f"may now hold a partial object — report the upload as failed "
                 f"before retrying.")

    print(f"uploaded {path}  {sent} bytes ({human(sent)})  HTTP {code}")
    return sent


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="Dropbox download_link URL -> local file")
    f.add_argument("--url", required=True, help="download_url from the Dropbox MCP")
    f.add_argument("--out", required=True)
    f.add_argument("--size", type=int, help="expected bytes; strongly recommended")

    p = sub.add_parser("push", help="local file -> presigned PUT URL")
    p.add_argument("--file", required=True)
    p.add_argument("--url", required=True)

    r = sub.add_parser("relay", help="fetch then push, then delete the local copy")
    r.add_argument("--url", required=True)
    r.add_argument("--upload-url", required=True)
    r.add_argument("--size", type=int)
    r.add_argument("--work", default="/tmp", help="scratch directory")
    r.add_argument("--keep", action="store_true", help="do not delete after upload")

    a = ap.parse_args()
    if a.cmd == "fetch":
        fetch(a.url, a.out, a.size)
    elif a.cmd == "push":
        push(a.file, a.url)
    else:
        tmp = os.path.join(a.work, "dropbox-relay.bin")
        fetch(a.url, tmp, a.size)
        try:
            push(tmp, a.upload_url)
        finally:
            if not a.keep and os.path.exists(tmp):
                os.remove(tmp)
                print(f"removed {tmp}  ({human(free_bytes(a.work))} free)")


if __name__ == "__main__":
    main()
