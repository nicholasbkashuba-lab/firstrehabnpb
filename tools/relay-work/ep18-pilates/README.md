# Episode 18 (Elyse Marrone, Danielle Armstrong): the scripts that built it

Four voices (Dave, Mike, two women guests) on three cameras. Run in a folder holding the
cameras and the RAW radio mp3, plus lock_rate.py from the podcast-multicam skill.

1. `asr.py` (faster-whisper medium.en, fed decoded f32 audio because PyAV in this sandbox
   rejects `metadata_errors`). Whisper SKIPPED 43 s of real speech at 3:11; check the
   transcript for gaps against the audio level and re-run the gap window on its own.
2. `syncone.py cam_8k.wav` per camera: 30 chunk matches, line fit. All three locked to
   6 ms residual: Dave +195.143 (rate 0.999971), Mike +212.981, guests +186.044.
   `syncprobe18.py` is the checkpoint, through the render's own seek path.
3. `embed.py` + `attrib18.py`: ECAPA embeddings, four seeded centroids. 95 to 100% on the
   hand checked ranges. Camera mic energy was USELESS for the guests here (Mike's camera
   sat by Danielle's mic and heard her loudest 92% of the time), so shots use embeddings only.
4. `shots18.py` -> cuts18.json (145 shots, avg 11 s), `render18.py` renders straight from
   the raw 4K files, tone mapping the two HDR iPhones and skipping non-reference frames on
   the 60 fps ones.
5. `clips18.py`: vertical clips, sentence-aware captions wrapped by measured pixel width,
   per-clip speaker overrides (clip_overrides.json) and an EXCISE list for jump cuts.

Disk: three 4K cameras are 41 GB against ~27 GB usable. Mike.mov was never downloaded
whole: `mike_slice.py` range-fetches only the byte windows needed into a sparse file (moov
from the tail, head from offset 0), `mike_aud.sh` pulls audio slice by slice and punches
the bytes back out with `fallocate -p`. Each Dropbox temp link is single use, one range each.

Guest punch-ins: the first Elyse crop (1920x1080 native at 450,120) cut her chin off every
time she leaned in. Shipped crop is 2400x1350 at 300,220. Check a punch-in against a frame
from EVERY shot that uses it, not three samples.

Re-rendering only some shots: stream-copying the untouched shots out of the finished file
works (pixel identical), but each copied piece reports ~1/3 frame short, and the concat
demuxer stacks those into 1.2 s of drift over 110 shots. Join with a list that states every
file's exact `duration nf/30` (seg/list_exact.txt). Do not try a raw .h264 re-timestamp;
it breaks DTS at every join.
