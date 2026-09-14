import subprocess, numpy as np, sys
FF="ffmpeg"; SR=16000
def grab(path,start,dur):
    raw=subprocess.run([FF,"-v","quiet","-ss",str(start),"-t",str(dur),"-i",path,
        "-vn","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).astype(np.float64)
def xc(a,b):
    n=1<<int(np.ceil(np.log2(len(a)+len(b))))
    a=a-a.mean(); b=b-b.mean()
    r=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(b,n)),n)
    r=np.concatenate((r[-(len(b)-1):],r[:len(a)]))
    lags=np.arange(-(len(b)-1),len(a))
    k=int(np.argmax(np.abs(r))); peak=abs(r[k])
    m=np.ones_like(r,bool); m[max(0,k-400):k+400]=False
    return lags[k]/SR, peak/(r[m].std()+1e-12)
V,A=sys.argv[1],sys.argv[2]
# splices on the PUBLISHED timeline are at 1309.85 and 1320.83
print("published-timeline splices at 1309.85s and 1320.83s")
print(f"{'at':>7} {'lag_ms':>9} {'PSR':>8}   region")
print("-"*46)
res=[]
for t in [60,200,400,600,800,1000,1200,1290,1340,1400,1450,1500,1550,1600,1640]:
    a=grab(V,t,25.0); b=grab(A,t,25.0)
    if min(len(a),len(b))<SR: print(f"{t:7d}  short"); continue
    lag,psr=xc(a,b)
    reg = "pre-cut" if t<1309 else ("straddles splice" if t<1321 else "post-cut")
    res.append((t,lag,reg))
    print(f"{t:7d} {lag*1000:+9.1f} {psr:8.1f}   {reg}")
pre=[l for t,l,r in res if r=="pre-cut"]; post=[l for t,l,r in res if r=="post-cut"]
print()
print(f"pre-cut  mean lag: {np.mean(pre)*1000:+.1f} ms  (n={len(pre)}, max |lag| {max(abs(np.array(pre)))*1000:.1f} ms)")
print(f"post-cut mean lag: {np.mean(post)*1000:+.1f} ms  (n={len(post)}, max |lag| {max(abs(np.array(post)))*1000:.1f} ms)")
print(f"one frame at 30fps = 33.3 ms")
