# refit-clip: rebuild a 9:16 clip full frame with its captions in the safe zone

For clips already rendered with captions too low (Instagram's 4:5 feed crop keeps y 285..1635;
Reels/TikTok/Shorts cover the bottom ~420 px). Replaces the retired `tools/fit-captions.py`, which
shrank the picture over a blur and was rejected by Nick (2026-10-27). Every clip fills the frame.

Per clip, in a work folder holding `orig/<id>.mp4` (the full-frame original, e.g. from Post Bridge
`list_media`), with `models/yunet.onnx` (OpenCV zoo, media.githubusercontent.com) two levels above the scripts:

1. `boxes.py orig/<id>.mp4 boxes-<id>.json`: where the old solid black caption box sits (keep boxes
   40..200 px tall and centred; take the 2nd percentile top). Outline-only captions (Ep 11 Joyce) are
   not boxed: measure them on a frame.
2. `cues.py orig/<id>.mp4 <band_top> <band_bottom> cues-<id>.json [nobox]`: OCR of the old reviewed
   captions (tesseract). Used only to correct ASR spellings when no reviewed transcript exists.
3. `asr.py orig/<id>.mp4 asr-<id>.json`: word timestamps (faster-whisper medium.en).
4. `track.py orig/<id>.mp4 <y0> <y1> track-<id>.json`: largest face per shot (YuNet), so the narrower
   9:16 crop stays on the speaker.
5. `refit.py orig/<id>.mp4 out/<id>.mp4 <y0> <y1> asr-<id>.json cues-<id>.json --track=track-<id>.json
   --ref=ref-<id>.txt`: crops y0..y1 (y1 = old caption top minus ~12 px) at 9:16 around the tracked
   face, scales to 1080x1920, burns captions in the house style (Arial 10, white on a solid black box,
   MarginV=49, one line, <= 4 words, balanced within each sentence, each cue starting on its first
   word). `--ref` is the clip's section of the reviewed `transcripts.md` on `media/ep{NN}-clips`; its
   words win, timed by the ASR words they align to. NAME_FIXES from stage-episode.py apply.

Check every output on a contact sheet with both safe zones drawn, look for leftover old caption
pixels at the bottom edge, and run `tools/sizzle/qa_center.py` before it goes near a post.
Then `upload_media` (size_bytes + PUT) and `update_post` with platform_configurations passed back in full.
