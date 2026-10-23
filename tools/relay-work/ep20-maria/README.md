# Episode 20 (Maria, Dave's cousin): the scripts that built it

Three voices: Dave and Mike in the studio, Maria remote on **Zoom** from Buffalo. Dropbox
`/Pain2Power/Cousin/`. Run in a folder whose sibling `../src/` holds `raw.mp3` (the RAW radio
mp3), `IMG_5519.MP4`, `IMG_2005.MP4` and `video1.mp4`.

## Sources

| file | who | format |
|---|---|---|
| P2P-Maria RAW.mp3 | board mix | 27:25.3, 320k, the reference clock |
| IMG_5519.MP4 | Dave | H.264 1280x720 30fps SDR |
| IMG_2005.MP4 (inside "Oct 15, 2026.zip") | Mike | H.264 1280x720 30fps SDR |
| video1897478150.mp4 | Zoom speaker view | H.264 640x360 25fps; Maria or Mike's name card |

All SDR, no tonemapping. Everything is upscaled with lanczos (Zoom shots add a light unsharp).
The Dropbox files came in through the `dropbox-relay` workflow (`tmp/ep20-*` branches);
`pull.sh` reassembles a relay branch and checks its sha256.

## What was different this time

- **Maria's Zoom feed is landscape and fills the frame** (Shannon's in Ep 19 was a phone tile).
  The master crops `604x340+18+0` off it, which also drops Zoom's name label in the corner.
  Vertical clips crop `202x360+219+0`, the same tile size Ep 19 shipped.
- **Zoom is either Maria or a black "Michael McGann" card.** Mean luma of a 32x18 thumbnail
  is bimodal (~30 card, ~130 Maria). `edl.py` dilates the card mask 0.4 s each side and only
  ever puts Maria on screen inside it; every card stretch during her talking becomes a studio
  listening cut. The finished master was then scanned at 2 fps: zero dark frames.
- **Attribution needed no embeddings.** Speaker turns came off the Descript transcript
  (`TURNS` in `edl.py`), which separated Dave, Mike and Maria cleanly at paragraph level.
  `feats.py` confirms Maria independently: both studio phones drop to ~0.02 to 0.05 of the
  board level when she talks, against ~0.4 for studio speech.
- **No outtakes.** No "edit that", no dropouts, no Whisper gaps over 4 s. The only cut is the
  22.2 s of Zoom setup and countdown at the top.
- **Zoom audio toggles 0.18 s** between 326.743 and 326.564 depending on which end is talking
  (network delay runs both ways). Maria's own speech sits at 326.564, so her picture uses that.

## Sync (dense.py, 4 s windows, line fit on PSR > 15)

- Dave cam: `cam_t = master_t + 425.8706 - 0.0000414 * master_t`, 193 windows, resid 0.9 ms
- Mike cam: `cam_t = master_t + 512.4313 - 0.0000329 * master_t`, 186 windows, resid 3.7 ms
- Zoom: `cam_t = master_t + 326.564` (PSR 100 to 270 through her monologues)

## Run order

1. `asr.py raw16k.pcm asr_medium.json medium.en` (decode the mp3 to s16le 16 kHz first: the
   installed PyAV rejects faster-whisper's `metadata_errors` argument)
2. `sync.py` for coarse offsets, `dense.py <cam>.8k.pcm <approx> <out>.json` per camera
3. `feats.py` (studio energy, f0, Zoom luma per 0.1 s), `edl.py` -> shots.json
4. `render.py` (3 parallel ffmpeg, ~45 min on 4 cores), then concat with an explicit
   `duration` per piece and mux the RAW mp3 from 22.2 s (0.4 s fade in, 1.5 s fade out)
5. `clips20.py` for the vertical clips; `clip_overrides.json` swaps clip 07's listening cut
   from Mike (looking at his phone) to Dave

## The master

`Pain to Power - Maria - multicam.mp4` in Dropbox `/Pain2Power/Cousin/Final/`, content_hash
verified. 27:02.4, 1920x1080 30fps (48,672 frames), H.264 crf 20, AAC 192k, 716,120,799 bytes,
sha256 `4c0f1cb88e4657d633b1af2d90a8501be55a22a52407d86594e43f9b59f6f607`.

138 shots, avg 11.8 s, longest 31.4 s. Maria 51.9% / Dave 27.4% / Mike 20.7%. Per five minutes:
`0-5 A4 D64 M32 | 5-10 A84 D6 M11 | 10-15 A63 D27 M10 | 15-20 A70 D6 M24 | 20-25 A58 D23 M19 | 25-27 A6 D54 M40`
(the first block is the hosts' intro before Maria speaks; the last is Dave's joke and Mike's
close, with Maria's three reactions where Zoom shows her).

Contact sheet, one frame a minute (27 frames): 24 show the person speaking. The other three
are listening cuts inside long stretches, all deliberate.

## Names

Maria Kendzierski (Nick confirmed the spelling 2026-10-23). On air she is only "Maria", and her
Zoom display name misspells it "Kendzierskki". Her mother was Phyllis, twin of
Dave's mother Dolly. Treatment centre: Roswell Park, Buffalo.
