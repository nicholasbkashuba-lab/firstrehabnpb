# Episode 14 — multicam render handoff

Everything in this folder was measured in the sandbox from the real media. The
sync is solved and verified; what remains is the render, which belongs on a
machine with the 4K files local (see **Where to render**).

## Sources

Dropbox `/Arlosoroff/`:

| file | duration | format |
|---|---|---|
| `Mike.mov` | 33:12.28 | 3840x2160 HEVC Main 8-bit, **bt709 SDR**, 59.94 fps, rotation -180, 21.86 GB |
| `Dave.mov` | 30:30.81 | 3840x2160 HEVC **Main 10**, **bt2020/HLG HDR**, 59.94 fps, 13.55 GB |
| `Arlosoroff.MP4` | 29:06.14 | 1280x720 H.264, bt709 SDR, 30 fps, rotation -180, 0.78 GB |
| `P2P-Dr Arlosoroff 9-12 RAW.mp3` | 28:51.09 | 320 kb/s stereo — the audio master |

Mike is the co-host camera, Dave the host, Arlosoroff the guest.

## The sync, solved

**This master is not time-compressed.** Unlike the reference episode, the mp3 is a
raw board feed running at true rate, so one offset covers the whole show and the
usual warp-map problem does not arise here.

```
rate   = 0.99998   (-0.002%, i.e. none)
fit    = camera_t = master_t * 0.99998 + 257.77   (ref = Mike.mov)
inliers 36/36, residual std 0.01s, max 0.01s
whole-file re-correlation after rate correction: PSR 649.2
dense pass: 283 anchors, 142/142 chunks above PSR 12, every one within
0.01s of the single-rate prediction
```

Master time T lands on each camera at:

| camera | camera_t | PSR |
|---|---|---|
| Mike | `T + 257.7503` | 458.7 |
| Dave | `T + 91.0766` | 723.1 |
| Arlosoroff | `T + 3.4043` | 555.9 |

Camera-to-camera closure, the test that proves the cameras themselves are
trustworthy:

```
MIKE->DAVE (-166.6759) + DAVE->ARLO (-87.6723) = -254.3482
MIKE->ARLO direct                              = -254.3435
closure error 4.7 ms   (one frame @59.94 = 16.7 ms)   PASS
```

Note the raw correlation grid is `HOP/SR` = 20 ms, so the offsets above carry
parabolic sub-sample refinement; a raw argmax can only ever land on a 20 ms
multiple and would report a spurious 20 ms closure error.

`sync_lock.json` and `warp.json` here are the real artifacts — drop them in the
episode folder beside the cameras and `render_final_v3.py` will pick them up.
`warp.json` names `Mike.mov` as ref, which is also the largest video file, so the
script's own `vids[0]` choice agrees.

## Colour: the one thing that will look wrong if ignored

**Dave is HDR and the other two are not.** `yuv420p10le`, bt2020nc/bt2020/
arib-std-b67 (HLG). Squashed to BT.709 without tone mapping he gets lifted blacks
and grey skin, and the look changes at every cut to him. Confirm the renderer
tags him `HDR -> will tone-map` and leaves Mike and Arlosoroff alone.

Mike and Arlosoroff also carry `rotation: -180` — both cameras were mounted upside
down. ffmpeg applies the display matrix automatically; a pipeline that reads raw
frames will not.

## Where to render, and why not here

Measured on the sandbox (4 vCPU, software decode, no GPU):

| pass | fps | speed | full episode |
|---|---:|---:|---:|
| Mike plain decode | 36 | 0.606x | — |
| Mike -> 1080p x264 veryfast crf20 | 26 | 0.437x | ~76 min |
| Dave plain decode | 35 | 0.588x | ~52 min |
| **Dave tonemapped -> 1080p** | **8.7** | **0.145x** | **~210 min** |

The tone map is the entire cost: Dave decodes at 0.588x and collapses to 0.145x
once the HLG chain is attached, a 4.05x penalty from the zscale linear-light float
conversion rather than the HEVC decode. One full pass over both 4K cameras is
about 5 hours here, before the render itself, and a finished master cannot leave
this sandbox anyway (30 MiB chat cap, 100 MB GitHub blob cap, and the Dropbox
connector cannot upload binaries).

**So: tone-map Dave exactly once** into a 1080p SDR proxy, pay the cost a single
time, and drive every later pass off the proxy. Re-tone-mapping per pass costs
3.5 hours each time.

```bash
ffmpeg -i Dave.mov -an \
  -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,\
tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1920:1080" \
  -c:v libx264 -preset veryfast -crf 18 -color_primaries bt709 -color_trc bt709 \
  -colorspace bt709 Dave-proxy1080.mp4
```

## Render

With the four sources and `sync_lock.json` + `warp.json` in one folder:

```bash
python render_final_v3.py --width 1920 --height 1080 --fps 30 \
  --crf 20 --preset medium --min-shot 3
```

Leave `--min-shot` at 3. Raising it makes whoever has the longest shots swallow
the others; at 6 on the reference episode transcript agreement fell from 82% to
64% and dropped a participant from the final eight minutes.

Read the `source formats:` block before letting it run and confirm it found
exactly three cameras. Any stray render or export in the folder gets adopted as a
fourth angle and silently displaces a real one.

## After the render: apply the two cuts

The audio master shipped to air has two sections removed, both containing the
guest's private contact details read out by mistake and both edited at the hosts'
own on-air request. **Render against the RAW master, then cut the finished video**
— cutting first would invalidate every offset above.

| cut | raw-master time | removes |
|---|---|---|
| A | 1309.85 – 1340.70 s | wrong private line + correction chatter |
| B | 1351.68 – 1393.00 s | personal email fumble |

Keep the correct office number 561-840-1090 and main@orthocarefl.com, which sit
outside both cuts. Finished runtime 27:38.96 against the raw 28:51.09. The already
edited audio master is on branch `media/ep14-audio` if you want to conform to it
rather than re-cut.

## Verifying without watching it

Contact sheet, one frame per minute, tiled — cheap and attachable:

```bash
for i in $(seq 0 27); do ffmpeg -v error -ss $((i*60)) -i out.mp4 -frames:v 1 \
  -vf scale=240:-1 -y $(printf f%02d.jpg $i); done
ffmpeg -v error -y -i f%02d.jpg -vf tile=6x5 -frames:v 1 contact.jpg
```

Then check coverage in five-minute blocks rather than overall share: a healthy
total can still hide someone missing for seventeen straight minutes, which was the
original complaint on the reference episode. Expect roughly 82% agreement with the
transcript on speaker attribution; a participant whose mic catches more of the room
sits lower, and that is a microphone limit rather than a tuning problem.
