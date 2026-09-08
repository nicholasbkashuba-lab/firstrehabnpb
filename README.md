# Pain 2 Power — Episode 14, Dr. Chaim Arlosoroff — finished multicam video

`ep14-arlosoroff-FINAL.mp4`, split into 25 chunks because GitHub blocks blobs over 100 MB.

    cat ep14.chunk_* > ep14-arlosoroff-FINAL.mp4
    sha256sum -c ep14.sha256      # MUST pass before you use the file

- 1920x1080, H.264 High, 30 fps, BT.709, AAC 192 kb/s stereo
- **27:38.96**, 1,176,641,117 bytes
- sha256 `26ffd2a3f981d564e4e0fcf0a24b194ba7d2fdc10e1e3ca5b9071041938c8d8b`

## What is in it

Three cameras cut to whoever is speaking, with the radio board mix as the audio bed.
Screen time: Arlosoroff 41.2%, Dave 30.3%, Mike 28.5%. 105 shots, average 16.5 s,
longest 43.5 s, and all three appear in every five minute block.

**Speaker attribution came from the transcript, not the camera mics.** The multicam
script picks the camera by microphone energy, which put the guest on screen for 12.5%
of his own interview and the co-host on 57.7%: all three cameras sit in one small studio
so every mic hears everyone, and the script z-scores each camera by its own standard
deviation, handing the argmax to whichever mic has the lowest noise floor. Speaker turns
from Descript's diarisation of the board mix replaced it (`--cuts`, added to the script;
the original mic-energy path is untouched). Reaction cuts were then inserted inside long
monologues: without them the guest's bio ran 4 min 53 s on one static shot.

## The two contact-info cuts

Removed at the hosts' own on-air request. Both contained the guest's private contact
details, read out by mistake.

| cut | raw-master time | removed |
|---|---|---|
| A | 1309.85 – 1340.70 s | wrong private line, plus the correction chatter |
| B | 1351.68 – 1393.00 s | personal email fumble |

The correct office number 561-840-1090 and main@orthocarefl.com are kept. Verified by
transcribing the joins in the finished file: neither the private line nor the personal
address survives, and the read is natural.

## Verified

- Duration 27:38.96 against an expected 27:38.90
- Audio matches the raw master at **0.0 ms** at 120 s, 600 s and 1100 s. The cut step
  first introduced a +23.2 ms audio delay (AAC priming, whose edit list the concat
  stream-copy dropped); corrected with `-itsoffset -0.0232` and re-measured at 0.0 ms.
- Contact sheet, one frame per minute: every frame upright (Mike and the guest camera
  carry a -180 display matrix), and the tone-mapped HDR camera colour-matches the two
  SDR ones at every cut.
