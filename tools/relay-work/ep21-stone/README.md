# Episode 21 (Dr. Reed Stone, neurologist): the scripts that built it

Dropbox `/Pain2Power/Stone/`. Run in a folder holding `src/` (raw.mp3, IMG_2010.MP4,
IMG_5523.MP4) and `main.mov` (the 17.5 GB 4K camera). Work in progress; finished numbers
are added when the master ships.

## Sources

| file | who | format |
|---|---|---|
| P2P-Reed Stone RAW.mp3 | board mix | 27:02.9, the reference clock |
| IMG_2010.MP4 | Dave | H.264 1280x720 30 fps SDR |
| IMG_5523.MP4 | Dr. Stone | H.264 1280x720 30 fps SDR, rotation 180 |
| Video Oct 16 2026, 12 47 56 PM.mov | Mike | HEVC 3840x2160 59.94 fps SDR (bt709), rotation 180 |

No HDR, so no tonemapping. `dbx.py` range reads Dropbox through the REST API (reusable, unlike
single use temp links); the 17.5 GB camera came down in 8 parallel ranges, content_hash MATCH.

## Sync (dense.py, 8 s windows every 4 s, line fit on PSR > 15)

- Dave: `cam_t = t + 107.8726 - 0.0000318 t`, resid 2.6 ms
- Dr. Stone: `cam_t = t + 94.5896 - 0.0000410 t`, resid 2.5 ms
- Mike: `cam_t = t + 90.2318 - 0.0000275 t`, resid 4.2 ms

## Attribution

Three men, so ECAPA embeddings (embed.py from ep18, attrib21.py). Held out checks 95 to 100%.
edl21.py: 128 shots, avg 12.5 s, max 27.6 s, shot equals speaker on 89.7% of speech, everyone in
every five minute block. Shot 31 (a 1.4 s Mike sliver at the edit) relabelled to Dave by hand.

## The edit

One cut: RAW 359.2 to 381.367, Dave's retake of the question about Dr. Stone's son
("Xavier" then "Hold on one second... let's go back to the intro of Zander").

## Framing (faces21.py, YuNet every 5 s)

Dave cx 709/1280 (full frame), Dr. Stone cx 543/1280 (master crops 1152x648 at 0,0 so he sits
at 47%), Mike cx 2126/3840 (master crops 2880x1620 at 686,0). Vertical clips crop 405x720
(720p) or 1215x2160 (4K) and FOLLOW the face: YuNet at 8 fps through each piece, 0.375 s
smoothing, the crop x set every frame by a sendcmd file (an inline if() chain that long
overflows ffmpeg's expression parser). A fixed per shot crop failed qa_center at 23% when Dave
leaned; the tracked crop passes.

## Clips and reel

clips21.py: house caption style (one line, max four words, MarginV=75, solid black box, each
cue on its own first word). Clip 07 excises Dave's "not life threatening" aside.
Sizzle reel: tools/sizzle/reel_ep21.py, cut from the RAW cameras.
