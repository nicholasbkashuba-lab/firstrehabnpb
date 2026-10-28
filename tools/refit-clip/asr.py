# Word timestamps for a clip's audio with faster-whisper (decode to PCM first: PyAV rejects metadata_errors).
import sys, json, subprocess, numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, word_timestamps=True, beam_size=5, vad_filter=False)
words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
json.dump(words, open(out, "w"))
print(" ".join(w["w"] for w in words))
