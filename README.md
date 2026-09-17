# Pain 2 Power — Episode 15, Susan Mann — finished multicam video

`ep15-mann-FINAL.mp4`, split into 13 chunks because GitHub blocks blobs over 100 MB.

    cat ep15.chunk_* > ep15-mann-FINAL.mp4
    sha256sum -c ep15.sha256      # MUST pass before you use the file

- 1280x720, H.264, 30 fps, BT.709, AAC. **28:09.3**, 566,445,954 bytes
- sha256 `73f99185ed623c129a787f2fe52d0d085291a0ed4fdee23af690e892edf632e9`
- Audio bed is the radio board mix (`P2P-Susan mann 9-19 RAW.mp3`), untouched

## Sources

Three cameras from Dropbox `/Pain2Power/Susan Mann/`, all 1280x720 SDR BT.709,
so unlike earlier episodes there was no 4K downscale and no HDR tone mapping.

| file | who | role |
|---|---|---|
| IMG_0006.MP4 | Mike McGann | at the broadcast board |
| IMG_1852.MP4 | Dr. Dave Kashuba | guest-side desk, reference camera |
| IMG_5142.MP4 | Susan Mann | guest |

## Sync

The mp3 was NOT time-compressed this episode, which is unusual for a radio
master. `camera_t = master_t * 0.99998 + 7.30`, 36/36 inlier chunks, residual
std 0.01s, verify PSR 1181. The dense warp map confirmed it: 275 anchors, local
rate min 0.9996 / median 1.0000 / max 1.0003, no discontinuities.

`sync_preview.py` measured true offset at three points spanning the show:
errors -0.001s, +0.000s, -0.001s at PSR 137/118/117. No nudge applied.

Camera-to-camera: IMG_5142 -5.98s (PSR 733), IMG_0006 -0.38s (PSR 972).

## The cut

118 shots, avg 14.3s, longest 36s.

| | stock renderer | shipped |
|---|---|---|
| Susan (guest) | 17.2% | 44.1% |
| Dave | 44.9% | 28.1% |
| Mike | 37.9% | 27.8% |
| shots | 44 | 118 |
| longest shot | 176s | 36s |
| Susan, final 5 min | 0% | 14% |

**The stock mic-energy attribution was unusable.** It gave the guest 17% of her
own interview and dropped her entirely from the last five minutes, with one
176-second static shot. That is the same failure Episode 14 hit. Level alone
cannot separate Susan from Dave because they share a desk and his mic hears her
nearly as well as hers does.

`attrib.py` replaces it:
- pitch from the board mix separates Susan from the two men (f0 gate at 175 Hz,
  Schmitt trigger 0.62 enter / 0.40 exit, 0.3s sustain to enter)
- a calibrated bias (0.15) splits Dave from Mike on camera-mic energy, since
  Mike sits across the room and his mic is ~2.3x quieter
- reaction cuts break any shot over 34s at the quietest nearby point

The opening is corrected from the transcript, not tuned: the show starts under a
music bed whose stable pitch reads as a female voice and stole the first 16.5s.
Mike opens the show, so shot 1 is forced to him.

## Honest limits

Contact-sheet audit against `transcript-full.md`, one frame per minute: about 22
of 28 land on the right person, ~79% agreement. The podcast-multicam skill puts
the ceiling for mic-based attribution near 82%, so this is at spec, not perfect.
Misses cluster in fast three-way exchanges. The Dave/Mike bias is empirical.

Every participant appears in every five-minute block:
`0-5 D51/S43/M7 | 5-10 D7/S56/M37 | 10-15 D22/S45/M33 | 15-20 D29/S45/M26 | 20-25 D33/S51/M16 | 25-30 D26/S14/M61`

## Publishing

Upload by hand in YouTube Studio. Do not route it through Post Bridge: it times
out fetching files this size and rejects GitHub release assets.
