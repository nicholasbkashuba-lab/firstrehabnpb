import sys, json
from faster_whisper import WhisperModel
src, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=4)
import numpy as np
audio = np.fromfile(src, dtype=np.int16).astype(np.float32)/32768
segs, info = m.transcribe(audio, language="en", word_timestamps=True, vad_filter=False, beam_size=5)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text,
                "words": [{"w": w.word, "s": w.start, "e": w.end} for w in s.words]})
    print(f"[{s.start:7.1f}] {s.text}", flush=True)
json.dump(res, open(out, "w"))
