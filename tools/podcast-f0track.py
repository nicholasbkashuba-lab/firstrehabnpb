#!/usr/bin/env python3
"""Speaker track from the MASTER board mix using pitch, plus camera mics to
split the two male voices. Writes speaker_track.json in master time."""
import json, subprocess, numpy as np

SR=8000; HOP=160                      # 20 ms frames, same grid as the renderer
def decode(p, sr=SR):
    c=["ffmpeg","-v","error","-i",p,"-vn","-ac","1","-ar",str(sr),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,dtype=np.float32).astype(np.float64)

m=decode("master.mp3")
n=(len(m)//HOP)*HOP; nfr=n//HOP
fr=m[:n].reshape(-1,HOP)

# --- frame energy / voicing on the master
rms=np.sqrt((fr**2).mean(axis=1))
lr=np.log(rms+1e-8)
voiced = lr > (np.percentile(lr,35))

# --- f0 by autocorrelation over a 40 ms window (two hops), 70-320 Hz
W=400
pad=np.concatenate([m[:n], np.zeros(W)])
f0=np.zeros(nfr)
lo,hi=int(SR/320), int(SR/70)         # lag bounds
for i in range(nfr):
    x=pad[i*HOP:i*HOP+W]
    if x.std()<1e-6: continue
    x=x-x.mean()
    a=np.correlate(x,x,mode='full')[W-1:]
    if a[0]<=0: continue
    a=a/a[0]
    seg=a[lo:hi]
    if len(seg)==0: continue
    k=int(np.argmax(seg))+lo
    if a[k]>0.30: f0[i]=SR/k

# smooth f0 over voiced frames only
f0s=f0.copy()
w=9
for i in range(nfr):
    lo_i,hi_i=max(0,i-w),min(nfr,i+w+1)
    vals=f0[lo_i:hi_i]; vals=vals[vals>0]
    if len(vals): f0s[i]=np.median(vals)

print(f"frames {nfr}  voiced {voiced.mean()*100:.0f}%")
vf=f0s[(f0s>0)&voiced]
print("f0 percentiles on voiced:", {p:round(float(np.percentile(vf,p)),1) for p in (10,25,50,75,90)})
np.save("f0.npy", f0s); np.save("voiced.npy", voiced); np.save("rms.npy", rms)
print("wrote f0.npy voiced.npy rms.npy")
