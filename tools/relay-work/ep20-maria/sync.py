import numpy as np, sys
SR=8000
def load(p):
    x=np.fromfile(p,dtype=np.int16).astype(np.float32); return x/ (np.abs(x).max()+1)
m=load('master.8k.pcm')
def corr(a,b):
    n=1<<int(np.ceil(np.log2(len(a)+len(b))))
    A=np.fft.rfft(a-a.mean(),n); B=np.fft.rfft(b-b.mean(),n)
    c=np.fft.irfft(A*np.conj(B)*1/ (np.abs(A*np.conj(B))+1e-9),n)  # PHAT
    return c
for cam in sys.argv[1:]:
    c=load(cam)
    print('==',cam, len(c)/SR)
    for t in range(60, int(len(m)/SR)-60, 150):
        seg=m[t*SR:(t+20)*SR]
        cc=corr(c,seg)  # find seg inside c
        k=int(np.argmax(cc)); v=cc[k]
        side=np.sort(np.abs(cc))[-50]
        lag=k if k<len(cc)//2 else k-len(cc)
        print(f"master {t:5d}s -> cam {lag/SR:9.3f}s  offset {lag/SR-t:8.3f}  psr {v/ (np.std(cc)+1e-12):6.1f}")
