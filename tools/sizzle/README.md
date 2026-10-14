# Pain 2 Power sizzle reels

Code for the October 2026 sizzle reels of Dave and Mike and the two silent loops behind
the /podcast.html and /videos.html heroes. Every reel is a Python file: a shot list
(episode, in-point, focus, push-in), timed type and captions, and a synthesized score.
`run.py` renders it.

    export SIZZLE_WORK=~/sizzle-work          # masters, fonts and renders live here
    python3 run.py reel_trailer 9x16 16x9     # --draft for a fast low-quality pass
    python3 run.py reel_hero_audio hero       # silent, no type, no flashes
    ./webenc.sh $SIZZLE_WORK/out/hero_audio-hero.mp4 ../../assets/media/p2p-hero-audio

| reel | length | sources |
|---|---|---|
| `reel_trailer` | 0:35 | Ep 9, 11, 13, 14, 15, 16 |
| `reel_dadjokes` | 0:54 | Ep 16 grape, Ep 14 lawsuit, Ep 11 bossy lady |
| `reel_saturday` | 0:21 | Ep 14 open as voiceover, montage of all |
| `reel_hero_audio` / `reel_hero_video` | 0:14 / 0:14 | silent site loops |
| `reel_joke_{grape,bossy,kilometer,breakthrough,lawsuit}` | 0:18 to 0:46 | Dave's Dad Jokes, one per joke (`jokes.py`), 9:16 |

## Look

Natural camera colour, full bleed in every format, type outlined in black rather than
sitting on a dark glow or a dimmed picture. The owner tried a teal/orange grade with
grain, vignette and a bordered 9:16 band on 2026-10-14 and asked for all of it gone, so
don't bring it back. Type over footage lives in the lower third (`over` in `fmt_geom`),
clear of faces; title cards centre on black.

## Framing and audio versions

Every shot is face-tracked: `engine.face_point` runs YuNet (OpenCV zoo,
`face_detection_yunet_2023mar.onnx`, 230 KB, put it in `$SIZZLE_WORK/models/yunet.onnx`;
needs `opencv-python-headless`) on three frames, takes the face nearest the shot's fx/fy
hint and centres on it with the eyes ~40% down. Set `track=False` on a shot to use its
fx/fy as-is. The hint matters on two-shots (Ep 9) where both hosts are in frame.

**Centring is mandatory (owner rule).** After the crop is chosen, `ensure_centred()`
re-aims it so the face (or a two-shot's pair midpoint, `pair=True`) lands at frame
centre. When that needs more than `MAX_UPSCALE` (2.6x) of enlargement the shot is fitted
instead (`fit_frame`: whole picture scaled to fit, face centred, a soft colour wash of
the same shot filling the rest). `fit=` on a shot forces that look and sets its scale.
Then `qa_center.py` checks the rendered file at 2 fps and fails anything more than 10% of
the width off centre; `run.py` runs it after every render and `--sheet` writes a contact
sheet of the bad frames. Nothing ships without PASS.

    python3 qa_center.py $SIZZLE_WORK/out/show-9x16.mp4 --sheet

`run.py` writes every reel twice: `<name>-<fmt>.mp4` with the synthesized score and
`<name>-<fmt>-nomusic.mp4` with dialogue and sound effects only (no music bed), for
laying a track under it in-app.

## Adding a dad joke

Every episode ends on one. Add an entry to `JOKES` in `jokes.py`: the source segments
(cut dead air and side chatter), the camera switches (`ffmpeg ... -vf scdet=threshold=12`
over the window), which segment ends on the punchline, and caption drops/fixes. Run a
medium.en word pass over the window into `aud/joke_words.json` first; captions come from
it. Then `printf 'from jokes import build\nREEL, DUR, score = build("name")\n' > reel_joke_name.py`.

## Rebuilding the work dir

Nothing below is committed. The masters are GBs and live on `tmp/` branches as 45 MB
chunks; reassemble each and check its sha256 before use.

| work dir path | branch | note |
|---|---|---|
| `src/ep9/master.mp4` | `tmp/sabesan-out` | 1080p |
| `src/ep11/master.mp4` | `tmp/joyce-master-v2` | 1080p |
| `src/ep14/master.mp4` | `tmp/ep14-video-v2` | 1080p, air cuts applied |
| `src/ep15/master.mp4` | `tmp/ep15-video` | 720p |
| `src/ep16/master.mp4` | `tmp/ep16-video` | 1080p |
| `src/ep13/*.mp4` | `tmp/kerry-clips-v2-large` | vertical clips, captions burned in below y=1300 |

    git fetch origin tmp/ep16-video && mkdir -p $SIZZLE_WORK/src/ep16
    git archive origin/tmp/ep16-video | tar -x -C $SIZZLE_WORK/src/ep16
    cd $SIZZLE_WORK/src/ep16 && cat ep16.chunk_* > master.mp4 && sha256sum -c ...

Fonts: Inter Display comes from the system (`/usr/share/fonts/opentype/inter`).
Playfair Display is converted from the site's own woff2 into `$SIZZLE_WORK/fonts/`:

    python3 -c "from fontTools.ttLib import TTFont as T; f=T('assets/fonts/playfair-display-latin-600-italic.woff2'); f.flavor=None; f.save('$SIZZLE_WORK/fonts/playfair-display-latin-600-italic.ttf')"

Needs numpy, scipy, Pillow, soundfile, fonttools + brotli, and ffmpeg.

## Things that bit, so they don't again

- **Multicam masters cut a few frames off the transcript.** The Ep 16 master switches
  from the guest to Mike ~0.1 s after 616.40, so an in-point there flashed Dr. Goodwin
  for three frames. Check every sync in-point on a frame sheet, not the transcript.
- **Ep 16 Mike is a vertical inset on a blurred fill** (`INSET16`). 9:16 crops the inset;
  wide formats keep the fill and punch in.
- **Ep 15 Dave camera has a privacy blur box top-left.** Its framings in `lib.py` stay
  clear of it; don't widen them.
- **Kerry clips carry burned captions** from y~1330 down. `REGION` keeps every crop above.
- **The hero loops carry no flashes and no type**: they play behind the page h1, and
  flashing content behind text is both unreadable and a WCAG 2.3.1 risk.
- **Captions were checked against a second, larger ASR pass** (faster-whisper medium.en)
  where the small model disagreed with transcript-full.md. Never burn unreviewed ASR.
- **Vertical crops of 16:9 masters are enlarged** (1.8x for 1080p, 2.7x for Ep 15's 720p).
  The engine adds a light unsharp mask whenever a crop is upscaled more than 1.3x.
- **Upload limits.** Files sent through the chat cap at 30 MiB; `webenc.sh` makes the
  site renditions, and a two-pass x264 at a computed bitrate fits a reel under a cap.
- **The score is synthesized** (`synth.py`: booms, braams, risers, trap and four-on-floor
  drums, rimshots, tape stop). Nothing licensed, so nothing gets muted on upload.
