import numpy as np, sys, json
SR=8000
def load(p):
    x=np.fromfile(p,dtype=np.int16).astype(np.float32); return x/(np.abs(x).max()+1)
m=load('master.8k.pcm')
cam=load(sys.argv[1]); approx=float(sys.argv[2]); out=sys.argv[3]
W=8; SEARCH=3
res=[]
for t in np.arange(2, len(m)/SR-W-1, 4.0):
    seg=m[int(t*SR):int((t+W)*SR)]
    if np.std(seg)<1e-3: continue
    c0=int((t+approx-SEARCH)*SR); c1=int((t+approx+W+SEARCH)*SR)
    if c0<0 or c1>len(cam): continue
    win=cam[c0:c1]
    n=1<<int(np.ceil(np.log2(len(win)+len(seg))))
    A=np.fft.rfft(win-win.mean(),n); B=np.fft.rfft(seg-seg.mean(),n)
    X=A*np.conj(B); cc=np.fft.irfft(X/(np.abs(X)+1e-9),n)
    valid=cc[:int(2*SEARCH*SR)+1]
    k=int(np.argmax(valid)); psr=(valid[k]-valid.mean())/(valid.std()+1e-12)
    res.append((float(t), (c0+k)/SR - t, float(psr)))
json.dump(res,open(out,'w'))
r=np.array(res); good=r[r[:,2]>12]
print(len(r),'windows',len(good),'good')
for t,o,p in good[::10]: print(f"{t:7.1f} {o:9.3f} {p:6.1f}")
