import numpy as np
SR=8000; H=0.1
def load(p): return np.fromfile(p,dtype=np.int16).astype(np.float32)/32768
m=load('master.8k.pcm'); d=load('IMG_5519.8k.pcm'); k=load('IMG_2005.8k.pcm')
N=int(len(m)/SR/H)
def off_d(t): return 425.8706-0.0000414*t
def off_k(t): return 512.4313-0.0000329*t
def rms(x,t0):
    a=int(t0*SR); b=a+int(H*SR)
    if a<0 or b>len(x): return 0.0
    return float(np.sqrt(np.mean(x[a:b]**2))+1e-6)
T=np.arange(N)*H
M=np.array([rms(m,t) for t in T]); D=np.array([rms(d,t+off_d(t)) for t in T]); K=np.array([rms(k,t+off_k(t)) for t in T])
# f0 on master (8k): normalized autocorrelation, 40ms window, 80-400Hz
F=np.zeros(N); C=np.zeros(N)
lo,hi=SR//400,SR//80
for i,t in enumerate(T):
    a=int(t*SR); x=m[a:a+int(0.04*SR)]
    if len(x)<320 or M[i]<0.01: continue
    x=x-x.mean(); e=np.dot(x,x)
    ac=np.array([np.dot(x[:-l],x[l:])/np.sqrt(np.dot(x[:-l],x[:-l])*np.dot(x[l:],x[l:])+1e-9) for l in range(lo,hi)])
    j=int(np.argmax(ac)); F[i]=SR/(lo+j); C[i]=ac[j]
z=np.load('zoom_mean.npy'); Z=np.array([z[min(len(z)-1,int((t+326.564)*4))] for t in T])
np.savez('feats.npz',T=T,M=M,D=D,K=K,F=F,C=C,Z=Z)
print('done',N)
