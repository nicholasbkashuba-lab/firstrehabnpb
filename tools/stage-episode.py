#!/usr/bin/env python3
"""Stage one episode's clips so the daily posting routine can find them.

    python3 tools/stage-episode.py 9 /path/to/clips --transcripts /path/to/text

The routine builds its fetch URLs from the episode number, so the branch MUST be
named media/ep{NN}-clips. Episode 9's clips were originally pushed to
media/sabesan-clips and were therefore invisible to it — the routine would have
posted nothing all week. This script exists so that cannot happen again.

What it produces on the branch:
    clips/*.mp4      the vertical clips, unchanged
    playlist.txt     running order, strongest first, editable by hand
    transcripts.md   what each clip says, so captions are never invented
    README.md        a note for whoever opens the branch next

It pushes in batches. A single push of ~200MB gets reset by the git proxy.

It does NOT write captions, choose a running order intelligently, or touch
build.py. Order is seeded numerically and a human should reorder it; the
strongest clip is rarely the first one rendered.
"""
import argparse, json, os, re, subprocess, sys, textwrap

REPO = "https://github.com/nicholasbkashuba-lab/firstrehabnpb"

# Automatic transcription mangles guest names, and a wrong credential on a real
# physician is a genuine problem rather than a typo. The corrections live in one
# place so a fix made for one episode reaches every tool that touches a
# transcript; this list used to be duplicated here and in ep9-bonus-spec.py, and
# the two drifted. Add new guests to the skill's list, not here.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", ".claude", "skills", "podcast-episode",
                                "scripts"))
from name_fixes import NAME_FIXES  # noqa: E402


def sh(cmd, cwd=None, check=True):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str),
                          check=check, capture_output=True, text=True)


def clip_text(path):
    """Read a clip transcript. Accepts the [{s,e,t}] JSON the render pipeline
    emits, or a plain .txt file of the same name."""
    if path.endswith(".json"):
        segs = json.load(open(path))
        return " ".join(s.get("t", s.get("text", "")) for s in segs)
    return open(path, encoding="utf-8").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", type=int, help="episode number, e.g. 9")
    ap.add_argument("clips_dir", help="folder of NN-name.mp4 vertical clips")
    ap.add_argument("--transcripts", help="folder of matching .json or .txt files")
    ap.add_argument("--guest", default="", help='e.g. "Dr. Vani Sabesan, MD"')
    ap.add_argument("--credential", default="", help="credential exactly as stated on air")
    ap.add_argument("--batch", type=int, default=2, help="clips per push (default 2)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    nn = a.episode
    branch = f"media/ep{nn}-clips"
    clips = sorted(f for f in os.listdir(a.clips_dir) if f.endswith(".mp4"))
    if not clips:
        sys.exit(f"no .mp4 files in {a.clips_dir}")

    work = f"/tmp/stage-ep{nn}"
    sh(f"rm -rf {work} && mkdir -p {work}/clips")
    for c in clips:
        sh(["cp", os.path.join(a.clips_dir, c), f"{work}/clips/{c}"])

    # playlist, numeric order, for a human to reorder
    playlist = [
        f"# Posting order for Episode {nn} clips, strongest first.",
        "# The daily routine posts the first clip in this list that has not already",
        "# gone out. A clip absent from this file is never posted.",
        "# Edit freely: reorder lines to change priority, delete a line to pull a clip.",
        "#",
        "# SEEDED IN NUMERIC ORDER. Reorder before the week starts: six weekday slots",
        f"# and {len(clips)} clips means only the top six air, so order decides what runs.",
        "",
    ] + clips
    open(f"{work}/playlist.txt", "w").write("\n".join(playlist) + "\n")

    # transcripts
    head = [f"# Episode {nn} clip transcripts", ""]
    if a.guest:
        head += [f"Guest: **{a.guest}**" + (f" — {a.credential}" if a.credential else ""), ""]
        head += ["Use this spelling and this credential. Automatic transcription mangles",
                 "names, and never write a credential that does not appear here.", ""]
    body = []
    missing = []
    for c in clips:
        stem = c[:-4]
        body += [f"## {c}", ""]
        found = None
        if a.transcripts:
            for ext in (".json", ".txt"):
                p = os.path.join(a.transcripts, stem + ext)
                if os.path.exists(p):
                    found = p
                    break
        if found:
            txt = re.sub(r"\s+", " ", clip_text(found)).strip()
            for pat, rep in NAME_FIXES:
                txt = re.sub(pat, rep, txt, flags=re.I)
            body += [txt, ""]
        else:
            missing.append(c)
            body += ["_No transcript supplied. The routine will write a deliberately"
                     " generic caption for this clip rather than invent detail._", ""]
    open(f"{work}/transcripts.md", "w").write("\n".join(head + body))

    open(f"{work}/README.md", "w").write(textwrap.dedent(f"""\
        Episode {nn} social clips. Vertical 9:16, captioned.

        playlist.txt sets the posting order and is meant to be edited by hand.
        transcripts.md is what the routine reads before writing any caption.

        Branch name matters: the daily routine builds its URLs from the episode
        number, so it must be media/ep{nn}-clips and nothing else.
        """))

    print(f"episode {nn}: {len(clips)} clips -> {branch}")
    if missing:
        print(f"  WARNING: no transcript for {len(missing)}: {', '.join(missing)}")
    if a.dry_run:
        print(f"  dry run, staged at {work}")
        return

    sh("git init -q . && git config http.postBuffer 524288000", cwd=work)
    sh(f"git remote add origin {REPO}", cwd=work)
    sh("git add README.md playlist.txt transcripts.md", cwd=work)
    sh(['git', '-c', 'user.email=noreply@anthropic.com', '-c', 'user.name=Claude',
        'commit', '-q', '-m', f'Episode {nn} clips: playlist, transcripts, README'], cwd=work)
    sh(f"git push -q -f origin HEAD:refs/heads/{branch}", cwd=work)
    print("  text pushed")

    for i in range(0, len(clips), a.batch):
        batch = clips[i:i + a.batch]
        sh(["git", "add"] + [f"clips/{c}" for c in batch], cwd=work)
        sh(['git', '-c', 'user.email=noreply@anthropic.com', '-c', 'user.name=Claude',
            'commit', '-q', '-m', f'clips {i+1}-{i+len(batch)}'], cwd=work)
        for attempt in range(4):
            r = sh(f"git push -q origin HEAD:refs/heads/{branch}", cwd=work, check=False)
            if r.returncode == 0:
                break
            print(f"    retry {attempt+1}")
            subprocess.run(["sleep", str(2 ** (attempt + 1))])
        else:
            sys.exit(f"push failed for {batch}")
        print(f"  pushed {', '.join(batch)}")

    print(f"\ndone. verify these resolve before the week starts:")
    print(f"  https://raw.githubusercontent.com/nicholasbkashuba-lab/firstrehabnpb/{branch}/playlist.txt")
    print(f"  https://firstrehabnpb-zywd-git-media-ep{nn}-clips-thedesignofman.vercel.app/clips/{clips[0]}")
    print(f"\nstill to do by hand: add Episode {nn} to EPISODES[0] in build.py once it")
    print("is live on Spotify, and reorder playlist.txt so the strongest clip leads.")


if __name__ == "__main__":
    main()
