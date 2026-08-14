# Episode 10 — Dr. Zack McVicker

Recorded Aug 13 2026. Target air date **Saturday Aug 22 2026, 9:00 AM ET**; clips Sun Aug 23
through Fri Aug 28.

First episode with a board audio feed, and the first cut hook-first.

## Source material

Dropbox `/Dr. Mckvicker/`, renamed by Nick on 2026-08-14 to say who is on camera:

| File | Size | Role |
|---|---|---|
| `mikecam.mov` | 12,568,134,602 | host — Mike |
| `mckvickercam.mov` | 7,574,178,561 | guest — Dr. Zack McVicker |
| `davecam.MOV` | 6,617,628,225 | host — Dr. Dave Kashuba |
| `Pain to Power 10-Zack McVicker RAW (1).mp3` | 69,008,588 | board feed — audio bed and show clock |

`/McVicker/IMG_1781.MOV` is byte-identical in size to `davecam.MOV` (6,617,628,225) — the
same upload landing twice, not a fourth angle. Ignore it.

## Standing decisions this episode set

- **Board audio is the audio bed for the whole video.** Episode 9 used camera audio and Nick
  judged it bad. Every camera track gets muted.
- **The cut starts where Mike starts the show.** The board feed begins with the radio show,
  so its own head is the true start; everything before it is setup.
- **Clips are hook-first, 15 to 25 seconds.** Settles the question CLAUDE.md carried open
  from 2026-08-03.

## Blocked: Descript cannot fetch the Dropbox files

Descript imports media from a URL and validates it with its own HTTP request first. Every
route tried on 2026-08-14 failed:

| Attempt | Result |
|---|---|
| `create_shared_link` file URL, `dl=0` | HTML preview page |
| same, `dl=1` | HTML preview page |
| same on `dl.dropboxusercontent.com` | HTTP 403 |
| public folder link + filename subpath, `dl=1` | HTML preview page |
| same on `dl.dropboxusercontent.com` | HTTP 403 |
| folder link + subpath + `st=` token, both hosts | HTML / HTTP 403 |
| `download_link` single-use temp URL | HTTP 403 — the validation probe consumes the single use before the download starts |

The sandbox cannot check any of this locally: every Dropbox host returns `CONNECT tunnel
failed, response 403` through the proxy, so each attempt costs a Descript round trip.

**Cause.** `create_shared_link` is hard-locked to `audience: no_one` and its links carry no
`st=` token. Dropbox now requires that signed token on public link fetches. Making the
parent folder public does not retroactively upgrade file links that were minted private.

**Fix.** Per-file links copied from the Dropbox web UI ("Copy link" on each file) carry an
`st=` token and resolve publicly. Four links needed: the three cameras and the mp3. Once
they exist the import is one call and the rest of the pipeline runs.

For future episodes the standing arrangement is a Dropbox folder already set to *Anyone
with the link · Can view* before footage is dropped in, so per-file links inherit public
access and no manual step is needed each week.

## Measured sync offsets

Not yet measured — blocked on the import above.

Try Descript's waveform alignment first. If it will not, use
`scripts/sync_offsets.py measure`, whose correlation math was verified 2026-08-14 against a
synthetic 83.15s offset: recovered `+83.150s` at two probes 300s apart, SNR 916, spread
0.000s.

| Camera | Offset vs board audio | SNR | Probes |
|---|---|---|---|
| mikecam | — | — | — |
| mckvickercam | — | — | — |
| davecam | — | — | — |

## Descript project

Not yet created. Model it on Episode 9, `6918397b-9b32-47f6-95dd-310aa655b867`, which
published its FINAL 1080p to `https://share.descript.com/view/S3jYorNVwUZ`.

## Clips

Not yet cut. Target ten, six air. Branch must be `media/ep10-clips`.

## Site

`EPISODES[0]` and `VIDEOS[0]` in `build.py` still to add once the episode is live on Spotify
and YouTube.
