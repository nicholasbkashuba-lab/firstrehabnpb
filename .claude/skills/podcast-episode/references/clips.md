# Clips — selection, captions, staging

## Selection

Cut about ten, knowing six air. The extra four are insurance against a clip that reads
worse on screen than it did in the transcript, and stock for a future gap week.

**Hook first.** Open on the most surprising sentence in the passage and cut the setup
entirely. 15 to 25 seconds. Nick settled this on 2026-08-14 after it sat open since
2026-08-03.

The failure it replaces is specific and worth being able to recognise: every Episode 8 and
9 clip opened either on an interviewer question or mid-sentence on the word "But". A viewer
scrolling past hears someone being asked something and keeps scrolling. Test each candidate
by reading its first six words aloud with no context — if they are a question, or a
conjunction, or a pronoun with no referent, move the in-point.

What makes a good hook here: a number that sounds wrong ("ninety is the new seventy"), a
practitioner contradicting their own field ("robots are great marketing, not better
outcomes"), an admission ("evidence forced me to change how I operate"), or a patient line
quoted back ("just shoot me up, Doc"). Episode 9's composition names are a good register to
match — they read as headlines, not descriptions.

Avoid: anything requiring a definition to land, anything where the punchline needs the
question, and anything making a clinical claim the guest did not clearly state. Never
invent credentials or sharpen a claim to make a better clip.

## Format

- 1080×1920 vertical, 30fps, H.264 crf 20, AAC.
- Captions burned in: white bold, dark outline, centred, **two lines maximum**, sitting
  around the lower third.
- **Source is the raw camera, not the finished master.** The guest camera shoots natively
  vertical and is used full frame at zero crop. Host moments crop the 4K two-shot to a 9:16
  window on whoever is speaking. Cropping the finished 16:9 master instead means upscaling
  a narrow slice of an already-cropped face — visibly worse.
- Audio from the board feed, normalised to -14 LUFS for social.

## Captions

**A human reads the ASR before anything is burned in.** A burned caption cannot be
corrected later, and ASR mangles guest names reliably — Episode 9 needed a whole
corrections table. Corrections live in `scripts/name_fixes.py`; add each new guest there
rather than fixing by hand, so the next episode inherits them.

The house `.ass` style line, 1080×1920 PlayRes:

```
Style: Cap,DejaVu Sans,56,&H00FFFFFF,&H00FFFFFF,&H00101010,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,60,60,430,1
```

56pt DejaVu Sans Bold at 1080 wide with 60px margins fits about 26 characters per line, so
wrap at 26. `WrapStyle: 0`, `ScaledBorderAndShadow: yes`, outline 5, shadow 2, alignment 2
(bottom-centre), MarginV 430.

Two lines is the house maximum, but a long segment cannot simply be squeezed into two —
libass silently re-wraps it to three, which shipped once. Split into consecutive events
instead and divide the segment's time between them by character count. Drop any event
shorter than 0.7s; at the head it flashes, at the tail it is usually half a sentence
bleeding in from the next speaker.

`tools/ep9-bonus-spec.py` is a working implementation of all of the above — it reads a
transcript of `{s, e, t}` segments and writes `spec/ass/{name}.ass` plus `spec/clips.json`.
It renders nothing itself; it only produces the spec.

## Staging

```
python3 tools/stage-episode.py {NN} <clips-dir> --transcripts <text-dir> \
  --guest "Dr. Zack McVicker" --credential "..."
```

Creates branch `media/ep{NN}-clips` with `clips/`, `playlist.txt`, `transcripts.md` and a
README, pushing in small batches because a single ~200 MB push gets reset by the git proxy.

**The branch name is load bearing.** The daily routine builds its fetch URLs from the
episode number, so anything else is invisible to it. Episode 9 first went to
`media/sabesan-clips` and would have posted nothing all week.

Three things it deliberately does not do: reorder `playlist.txt` (seeded numerically, a
human decides which six air), add the episode to `build.py`, or write captions.

## Verify before the week starts

Both must pass:

```
curl -sI https://raw.githubusercontent.com/nicholasbkashuba-lab/firstrehabnpb/media/ep{NN}-clips/playlist.txt
curl -sI -r 0-1000 https://firstrehabnpb-zywd-git-media-ep{NN}-clips-thedesignofman.vercel.app/clips/<first>.mp4
```

200 and 206 respectively. Vercel needs a moment to build the branch first.

**Clip hosting.** jsDelivr serves clips under ~20 MB; anything larger needs the Vercel
branch host. That hostname embeds the Vercel **team slug**, renamed to `thedesignofman` on
2026-08-03 — the old `-first-rehabilitation` host now 404s, so if the team is renamed again
every clip over 20 MB fails to upload. `raw.githubusercontent` and GitHub release assets
both serve `application/octet-stream` and are rejected by Post Bridge outright.

## YouTube Shorts

YouTube decides Shorts eligibility from the media itself — vertical and under 3 minutes is
enough. There is no API flag and Post Bridge exposes no toggle, so "make it a Short" is a
property of the file, not the request. Confirm after posting via the channel feed: the
video's `link rel=alternate` reads `/shorts/<id>` for a Short and `/watch?v=<id>` otherwise.

## iPhone HDR footage

Recent iPhone video is Dolby Vision: HEVC Main 10, `yuv420p10le`, BT.2020 primaries, HLG
transfer (`arib-std-b67`). Detect with
`ffprobe -show_entries stream=color_transfer,color_primaries,pix_fmt`.

Such a source must be tonemapped through linear light, not merely transcoded. A bare
`-pix_fmt yuv420p` keeps the HLG-encoded values while tagging them BT.709: lifted blacks,
milky whites, grey skin. It looks like a bad camera rather than a bad convert, so it ships
easily. `tools/stage-media.py` handles this correctly as of commit `d578b8f`.
