# Episode 16 (Dr. Don Goodwin): the scripts that built it

Kept so the next all-male episode does not start from zero. Run order, in a folder holding
the three cameras and the radio mp3 (plus the podcast-multicam skill's lock_rate.py,
build_warp2.py, sync_preview.py):

1. `asr.py <mp3> medium.en asr_master.json` — faster-whisper, word timestamps (pip install faster-whisper)
2. lock_rate.py, build_warp2.py, sync_preview.py (skill) — sync checkpoint
3. `camalign.py` — camera to camera offsets plus closure check, writes camsig.npz
4. `embed.py` — ECAPA speaker embeddings on the board mix (pip install torch speechbrain, CPU wheels)
5. `attrib16.py` — seeds one centroid per voice from transcript-certain stretches, refines twice,
   prints validation against hand-labelled ranges. EDIT THE SEED RANGES per episode.
6. `energy16.py` — each camera's own mic energy, as an independent second opinion (89% agreement here)
7. `shots16.py` — fuse, Viterbi smooth, reaction cuts, coverage per 5 min block -> cuts16.json
8. `render16.py` — the render; skips a cut range in the master (the outtake) and pillarboxes a
   vertical camera on a blurred fill. Resumable: finished segments are reused.
9. `clips16.py` — vertical captioned clips; face-centred crops (pip install "opencv-python-headless<5";
   OpenCV 5 dropped the Haar CascadeClassifier)

Camera offsets, camera names and the outtake range are hard coded for this episode.
