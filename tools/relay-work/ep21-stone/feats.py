import numpy as np
SR=8000; H=0.1
def load(p): return np.fromfile(p,dtype=np.int16).astype(np.float32)/32768
m=load('master.8k.pcm')
cams={'D':(load('IMG_2010.8k.pcm'),lambda t:107.8726-0.0000318*t),
      'G':(load('IMG_5523.8k.pcm'),lambda t:94.5896-0.0000410*t),
      'M':(load('main.8k.pcm'),lambda t:90.2318-0.0000275*t)}
N=int(len(m)/SR/H); T=np.arange(N)*H
def rms(x,t0):
    a=int(t0*SR); b=a+int(H*SR)
    if a<0 or b>len(x): return 1e-6
    return float(np.sqrt(np.mean(x[a:b]**2))+1e-6)
out={'T':T,'M0':np.array([rms(m,t) for t in T])}
for k,(x,off) in cams.items(): out['E'+k]=np.array([rms(x,t+off(t)) for t in T])
np.savez('feats.npz',**out); print('done',N)
