# Episode 10 — Dr. Zack McVicker

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

## Measured sync offsets

Against `rawaudio_synced`, measured by envelope cross-correlation over six probes spanning
the episode, discarding false peaks below SNR 15:

| Camera | Offset vs corrected board audio | Spread across probes |
|---|---|---|
| `mikecam` | **+78.12s** | 0.034s |
| `mckvickercam` | **+68.29s** | 0.056s |
| `davecam2` | **+269.99s** | 0.032s |

Independently cross-checked camera-to-camera: `mck − mike = −9.840s` and
`dave − mike = +191.88s`, both agreeing with the board-derived numbers to within 15ms.

As composition offsets from a common origin at davecam2 (which rolled earliest):

    davecam2         0
    mikecam          191.87
    mckvickercam     201.70
    rawaudio_synced  269.99

So the show itself starts at **269.99s** into that timeline — that is where Mike opens, and
where the FINAL cut begins.

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
