#!/usr/bin/env python3
"""Put a local image or video somewhere Post Bridge can fetch it, and print the URL.

    python3 tools/stage-media.py video.mov
    python3 tools/stage-media.py photo.jpg --slug magazine-2026

Post Bridge cannot be handed a local file: it fetches media over HTTP. Everything it
CAN reach has a catch, and this script encodes the ones already learned the hard way:

  raw.githubusercontent.com   serves application/octet-stream -> REJECTED
  GitHub release assets       same, octet-stream              -> REJECTED
  Dropbox links               this sandbox is proxy blocked, cannot even upload them
  jsDelivr                    works, but only up to about 20MB
  Vercel branch host          works at any size, but the hostname embeds the TEAM SLUG

So: commit the file to a media/ branch, then use the Vercel branch host, falling back
to jsDelivr for small files. Both URLs are printed; verify before posting.

.mov is converted to .mp4 (h264/aac, faststart). Platforms prefer mp4, and it is the
format the clip pipeline already produces.
"""
import argparse, os, re, subprocess, sys, shutil

REPO = "https://github.com/nicholasbkashuba-lab/firstrehabnpb"
PROJECT = "firstrehabnpb-zywd"
# Vercel team slug. Renamed from "first-rehabilitation" on 2026-08-03; the old host 404s.
# If the team is renamed again this MUST be updated or large uploads silently break.
TEAM = "thedesignofman"
JSDELIVR_LIMIT = 20 * 1024 * 1024


def sh(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str),
                          check=check, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="local image or video files")
    ap.add_argument("--slug", help="branch suffix, default derived from the first filename")
    ap.add_argument("--keep-mov", action="store_true", help="do not convert .mov to .mp4")
    a = ap.parse_args()

    for f in a.files:
        if not os.path.exists(f):
            sys.exit(f"no such file: {f}")

    slug = a.slug or re.sub(r"[^a-z0-9]+", "-", os.path.splitext(
        os.path.basename(a.files[0]))[0].lower()).strip("-")[:40]
    branch = f"media/{slug}"
    work = f"/tmp/stage-media-{slug}"
    sh(f"rm -rf {work} && mkdir -p {work}")

    staged = []
    for f in a.files:
        name = re.sub(r"[^A-Za-z0-9._-]+", "-", os.path.basename(f))
        dest = os.path.join(work, name)
        if name.lower().endswith(".mov") and not a.keep_mov:
            dest = os.path.splitext(dest)[0] + ".mp4"
            print(f"converting {name} -> {os.path.basename(dest)}")
            r = sh(["ffmpeg", "-v", "error", "-i", f, "-c:v", "libx264", "-preset",
                    "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    "-b:a", "128k", "-movflags", "+faststart", dest, "-y"], check=False)
            if r.returncode != 0:
                sys.exit(f"ffmpeg failed:\n{r.stderr[:800]}")
        else:
            shutil.copy(f, dest)
        staged.append(os.path.basename(dest))

    # report what actually got staged, so a wrong orientation is caught before posting
    for n in staged:
        p = os.path.join(work, n)
        size = os.path.getsize(p)
        dims = sh(["ffprobe", "-v", "error", "-select_streams", "v:0",
                   "-show_entries", "stream=width,height", "-of", "csv=p=0", p],
                  check=False).stdout.strip()
        print(f"  {n}  {size/1048576:.1f} MB  {dims or 'no video stream'}")
        if dims and "," in dims:
            w, h = (int(x) for x in dims.split(",")[:2])
            if w > h:
                print("    NOTE: landscape. Reels, TikTok and Shorts will letterbox this.")

    sh("git init -q . && git config http.postBuffer 524288000", cwd=work)
    sh(f"git remote add origin {REPO}", cwd=work)
    sh("git add -A", cwd=work)
    sh(['git', '-c', 'user.email=noreply@anthropic.com', '-c', 'user.name=Claude',
        'commit', '-q', '-m', f'media: {slug}'], cwd=work)
    for attempt in range(4):
        r = sh(f"git push -q -f origin HEAD:refs/heads/{branch}", cwd=work, check=False)
        if r.returncode == 0:
            break
        print(f"  push retry {attempt+1}")
        subprocess.run(["sleep", str(2 ** (attempt + 1))])
    else:
        sys.exit("push failed")

    print(f"\npushed to {branch}. URLs for Post Bridge upload_media:\n")
    for n in staged:
        size = os.path.getsize(os.path.join(work, n))
        vercel = f"https://{PROJECT}-git-{branch.replace('/', '-')}-{TEAM}.vercel.app/{n}"
        print(f"{n}")
        print(f"  {vercel}   <- use this one")
        if size <= JSDELIVR_LIMIT:
            print(f"  https://cdn.jsdelivr.net/gh/nicholasbkashuba-lab/firstrehabnpb@{branch}/{n}")
        else:
            print(f"  (too big for jsDelivr at {size/1048576:.0f} MB)")
    print("\nVercel needs a moment to build the branch. Range request one URL and expect")
    print("206 with the right content-type before calling upload_media.")


if __name__ == "__main__":
    main()
