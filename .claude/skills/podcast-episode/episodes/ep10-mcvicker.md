# Episode 10 — Dr. Zach McVicker

**It is Zach, not Zack** — confirmed by Nick 2026-08-15. His own Dropbox filename says
"Zack" and is wrong; the published blog post already says Zach and is right. Do not add a
Zach→Zack rule to `name_fixes.py`; if anything the correction runs the other way.


Recorded Aug 13 2026. Target air date **Saturday Aug 22 2026, 9:00 AM ET**; clips Sun Aug 23
through Fri Aug 28.

First episode with a board audio feed, and the first cut hook-first. Also the episode that
found the 3% broadcast time-compression, which had been silently degrading nothing yet only
because no previous episode used the board feed.

## Source material

Dropbox `/Dr. Mckvicker/`, renamed by Nick on 2026-08-14 to say who is on camera:

| File | Size | Codec / colour | Role |
|---|---|---|---|
| `mikecam.mov` | 12,568,134,602 | HEVC 3840x2160, **HLG HDR** (`arib-std-b67`) | host — Mike |
| `mckvickercam.mov` | 7,574,178,561 | HEVC 3840x2160, bt709 | guest — Dr. Zack McVicker |
| `davecam.MOV` | 6,617,628,225 | H.264 3840x2160, bt709 | host — Dr. Dave Kashuba |
| `Pain to Power 10-Zack McVicker RAW (1).mp3` | 69,008,588 | 320kbps 44.1kHz stereo | board feed |

`/McVicker/IMG_1781.MOV` is byte-identical in size to `davecam.MOV` — the same upload
landing twice, not a fourth angle. Ignore it.

**mikecam is HDR and the other two are not.** Any clip cut from Mike's angle must be
tonemapped through linear light or it ships washed out with grey skin. See the iPhone HDR
section in CLAUDE.md for the filter. This is per-camera, not per-episode — check every time.

**All three cameras are landscape 4K.** Episode 9's guest camera was natively vertical
(`rotation=-90`) and could be used at zero crop. Not so here: every vertical clip needs a
9:16 crop window on the speaker.

## Descript project

`31ce4423-db4d-4841-9cf8-24d0009a2815` — https://web.descript.com/31ce4423-db4d-4841-9cf8-24d0009a2815

| Media | Duration | Note |
|---|---|---|
| `rawaudio` | 28:45 | **DO NOT USE** — the broadcast copy, 3% time-compressed |
| `rawaudio_synced` | 29:38 | the corrected bed, use this |
| `mikecam` | 31:11 | |
| `mckvickercam` | 30:51 | |
| `davecam2` | 34:30 | |
| `davecam` | — | dead placeholder from a failed upload, ignore |

## The 3% problem — read this before trusting any board feed

The delivered board audio does **not** match the video. It was time-compressed by exactly
3% (`rate = 1/0.97`) to fit its radio slot. Dropped straight onto the timeline it starts
roughly in sync and drifts nearly a full minute apart by the end — fine for the first
thirty seconds of a review, unusable by the middle.

How it showed up, because the symptom is misleading: the three cameras locked to each other
instantly (SNR 20-31, spread 5-15ms) while nothing locked to the board (SNR 5-6, random).
The tell was that offsets **grew steadily with probe position** instead of scattering. That
is a rate difference, not a timing one. Searching the rate directly, all three cameras
independently agreed on 1.0309 at SNR 107-143.

Fix: `ffmpeg -i in.mp3 -filter:a "atempo=0.97" out.wav`. Pitch-preserving. Verified by
raw-sample correlation improving and the offset going constant to within 6ms.

**Check this on every future episode.** It is a property of how the station delivers the
file, so it will almost certainly recur, and it is invisible unless you look for it.

## The SECOND problem — the board feed also has a hidden splice

The 3% stretch is not the whole story. There is also an **edit inside the board audio at
93.2s** where roughly 2.42 seconds were cut out. So a single offset cannot serve the whole
episode, and the first version shipped 2.43s out of sync for its opening 93 seconds. Nick
caught it immediately: "off from the very start, seconds or more."

**Why it was missed the first time:** every probe was at board time 120s or later, and past
the splice the offset is genuinely constant. The opening was never measured. **Always probe
the first 60 seconds**, and probe densely enough to see a step change rather than assuming
one number covers the show.

**The splice is in the BOARD FEED, not the cameras — verified two ways.** Nick pointed out
that the three cameras all start and stop at different moments but each contains the whole
podcast, which is true and worth checking against: (1) re-running the measurement with a
pure resample (`asetrate`) instead of `atempo` shows the identical 2.43s step, so WSOLA
time-stretching did not invent it; (2) all three cameras jump by the same ~2.42s at the
same instant AND stay locked to each other across it (`mck − mike` is −9.845s before and
−9.855s after). Cameras glitching individually would not stay in lockstep. The cameras are
continuous and complete; the board feed is the edited one.

Localising it was fiddly because that stretch is where the phone number gets repeated, and
repeated content produces strong false correlation peaks (a spurious lock at +121.6s scored
SNR 15-23). The technique that worked was abandoning argmax entirely: score the two KNOWN
candidate offsets directly and take whichever correlates better. Repeated content cannot
hijack a two-hypothesis test. All three cameras then agreed — strongly pre through 91s,
near-zero through the 92-94s pause, strongly post from 95s.

## Measured sync offsets

Two regimes, split at composition time **93.2s**. Camera source time at composition time t:

| Camera | Segment A (t < 93.2) | Segment B (t ≥ 93.2) | Shift |
|---|---|---|---|
| `mikecam` | t + **75.715** | t + **78.145** | +2.430 |
| `mckvickercam` | t + **65.870** | t + **68.290** | +2.420 |
| `davecam2` | t + **267.590** | t + **269.990** | +2.400 |

Segment A offsets locked with **zero spread** across four probes at SNR 16-20. Segment B
held to within 0.045s across the remaining 28 minutes. The three cameras cross-check
against each other independently: `mck − mike = −9.85s`, `dave − mike = +191.87s`, in both
regimes.

The residual 0.045s drift from board 80s to 1680s implies the true rate is a hair off
1/0.97 (about 2.8e-5). That is 45ms end to end, at the edge of perceptible, and was left
alone. If a future episode looks slightly soft at the very end, this is the knob.

## Standing decisions this episode set

- **Board audio is the audio bed for the whole video**, camera tracks muted throughout.
- **The cut starts where Mike starts the show**, i.e. the head of the corrected board feed.
- **Clips are hook-first, 15 to 25 seconds.** Settles the question CLAUDE.md carried open
  from 2026-08-03.

## Still to do

- FINAL 1080p composition, trimmed to the show start, filler removed, angles switched.
- Publish unlisted for Nick's review; full episode to YouTube by hand from Descript.
- Ten hook-first clips, ASR reviewed before captions burn, staged to `media/ep10-clips`.
- `EPISODES[0]` and `VIDEOS[0]` in `build.py` once the episode is live.
- Schedule the week in Post Bridge.
