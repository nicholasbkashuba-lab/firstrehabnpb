# Pain 2 Power — Episode 16, Dr. Don Goodwin — finished multicam video

`ep16-goodwin-FINAL.mp4` ("Pain to Power - Don Goodwin - multicam.mp4"), split into
18 chunks because GitHub blocks blobs over 100 MB. This branch is the BACKUP; the
delivery is Dropbox `/Pain2Power/Dr. Goodwin/Final/` once dropbox-put credentials exist.

    cat ep16.chunk_* > ep16-goodwin-FINAL.mp4
    sha256sum -c ep16.sha256      # MUST pass before you use the file

- 1920x1080, H.264 crf 20, 30 fps, BT.709, AAC 192k. **27:06.5**, 818,281,247 bytes
- Audio is the radio board mix `P2P-Don Goodwin 10-3 RAW.mp3`, untouched EXCEPT one cut:
  RAW 22:31.80 to 22:51.45 (19.65 s) is removed, the outtake where Mike says "don't
  worry, this is edited" and "I'm going to edit that too". 30 ms fades at the join.

## Sources (Dropbox `/Nicholas Kashuba/Pain2Power/Dr. Goodwin/`, content_hash verified)

| file | who | format |
|---|---|---|
| Video Sep 24 2026, 12 37 24 PM.mov | Dr. Goodwin (guest), reference | HEVC 1920x1080 SDR, rotated 180 |
| IMG_1918.MP4 (iCloud zip from David Kashuba) | Dave | H.264 1280x720 SDR, rotated 180 |
| IMG_4077.MP4 (iCloud zip from Cameron Dewar) | Mike | H.264 720x1280 vertical, pillarboxed on a blurred fill |

## Sync

The mp3 is NOT time compressed: `camera_t = master_t * 0.99997 + 26.80`, 36/36 inliers,
residual 0.01 s, verify PSR 1115. Warp map 266 anchors, local rate 0.9995 to 1.0004.
sync_preview at 30/400/800/1200/1550 s: errors +0.001/0.000/0.000/0.000/0.000 s, PSR 98 to 122.
Camera to camera: Dave +13.94 s (PSR 920), Mike +4.76 s (PSR 808), closure error 0.000 s.

## Speaker attribution — three men, so the pitch gate could not work

`tools/podcast-attrib.py` separates a female guest by pitch. Every voice here is male,
so this episode used ECAPA speaker embeddings (speechbrain, 1.5 s windows) on the board
mix, seeded from transcript-certain stretches and refined twice, fused with each
camera's own mic energy. The two signals are independent and agree on 89% of speech.
Viterbi smoothing, 3 s minimum shot, reaction cuts on any shot over 34 s.

116 shots, avg 14 s, longest 33 s. Guest 48.8% / Dave 29.1% / Mike 22.1%. On screen
matches the embedding speaker on 91% of speech frames. Everyone in every 5 min block:
`0-5 D54/G18/M28 | 5-10 D16/G81/M3 | 10-15 D18/G63/M19 | 15-20 D20/G60/M20 | 20-25 D39/G39/M22 | 25-30 D30/G6/M64`
Contact sheet, one frame a minute: 25 of 27 on the speaker, the other 2 are reaction cuts.

Honest limit: Dave's camera sits low and crops the top of his head for most of the show.
That is the source framing, not something the edit can fix.
