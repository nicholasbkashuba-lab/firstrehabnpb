import json, sys
import numpy as np
from faster_whisper import WhisperModel
m=WhisperModel(sys.argv[2], device="cpu", compute_type="int8", cpu_threads=3)
segs,info=m.transcribe(np.fromfile("master16k.f32",dtype=np.float32), language="en", word_timestamps=True, vad_filter=False, beam_size=5,
    initial_prompt="Pain 2 Power on 100.3 Legends Radio. Dr. Dave Kashuba, Mike McGann, Elise, Danielle, Pilates. First Rehabilitation of North Palm Beach.")
out=[]
for s in segs:
    out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"s":w.start,"e":w.end,"w":w.word} for w in (s.words or [])]})
    print(f"[{int(s.start//60):02d}:{int(s.start%60):02d}] {s.text}", flush=True)
json.dump(out, open(sys.argv[3],"w"))
