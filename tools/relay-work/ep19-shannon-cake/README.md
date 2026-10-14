# Episode 19 (Shannon Cake): the scripts that built it

Three voices: Dave and Mike in the studio, Shannon remote on **Zoom** from her car. Run in a
folder holding `raw/` (the three source files plus the mp3), `master.mp3` -> `raw/raw.mp3`, and
lock_rate.py from the podcast-multicam skill. `dbx.py` lists a Dropbox folder, makes a folder
and fetches a temp link through `tools/dropbox-put.py`'s credentials (that script has no `ls`).

## What was different this time

- **Small source files.** IMG_1996.MP4 (Dave) was 1280x720, IMG_5504.MOV (Mike) 640x360, and the
  Zoom recording video1573954541.mp4 640x360 at 25 fps. Earlier episodes had 4K phone originals.
  Nick said "go with what's there". Everything is upscaled with lanczos plus a light unsharp.
  None of it is HDR, so no tonemapping.
- **The guest only exists inside Zoom's speaker view.** Zoom shows either Shannon's 9:16 phone
  feed (a 202x358 tile at x=219, y=1 of the 640x360 frame) or Mike's name card. `zoomtile.py`
  classifies every half second by the tile's mean brightness (bimodal: ~30 card vs ~120 her
  picture), so a SHAN shot is only ever used while Zoom is actually showing her. When she is
  talking and Zoom has not switched yet, the cut goes to HOSTS (Dave and Mike side by side).
- **Attribution is easy for the guest, embeddings for the hosts.** Shannon is only in the board
  mix, so both studio phones drop ~2 log units when she talks. `attrib19.py` fuses ECAPA
  embeddings (`embed.py`, from ep18) with that studio energy, the Zoom tile, and the Dave minus
  Mike phone energy. 94.9% correct on hand checked transcript stretches; on screen matched the
  speaker 86.5% (Dave 88.4, Mike 88.1, Shannon 84.8, limited by Zoom's switch lag).
- **Outtakes were connection glitches, not "edit that".** `edit.json` keeps three ranges: drops
  the 1:12 pre-roll and countdown, the audio drop at RAW 13:47.95 to 14:01.22, and the camera
  drop at RAW 15:22.60 to 15:31.90. Each join was checked by re-transcribing the stitched audio.
- **Sync** (syncone.py from ep18, 30 chunks, line fit): Dave cam rate 0.999967 off -38.003
  (resid 8 ms), Mike cam 0.999957 / -35.282 (6 ms), Zoom 0.999974 / +237.084 (85 ms, Zoom
  jitter). The phones start ~36 s into the mp3, inside the pre-roll that gets cut anyway.

## Run order

1. `asr.py x medium.en asr_medium.json` (decoded f32 audio; no gaps over 4 s this time)
2. `syncone.py <cam>_8k.wav` per camera, `zoomtile.py`, `energy19.py`, `embed.py`
3. `attrib19.py` -> spk.npz, `shots19.py` -> cuts19.json (168 shots, avg 9.9 s, max 23.8 s)
4. `render19.py` (J=3, ~25 min). The concat list states each piece's exact duration as a decimal
   (`duration 9.500000`); the concat demuxer rejects a fraction like `285/30`.
5. `clips19.py` vertical clips in the 2026-10-09 caption standard (one line, max four words,
   MarginV=12, solid black box, each cue on its own first word). Vertical layouts: DAVE crop
   405x720 at x=440, MIKE 202x360 at x=198, SHAN the Zoom tile at zero crop, HOSTV Dave over Mike.

## Audit

Contact sheet, one frame a minute (28 frames): 22/28 show the person speaking (79%). Of the six
misses, four are deliberate reaction cuts inside long monologues, one is Shannon talking before
Zoom switched to her, and one is a genuine miss.

## Names (also in tools/stage-episode.py NAME_FIXES)

Shannon Cake (Zoom display name "Shannon Giaimo", ASR "Shannon Kay"); Dr. Paul Winner, DO,
Palm Beach Neurology (ASR "Winter"); Dave Aronberg (ASR "Ehrenberg"); Captain Kerry; Kashuba.
