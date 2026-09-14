#!/usr/bin/env python3
"""Full QA on a finished episode render. Objective checks only, no eyes required.
usage: verify_episode.py RENDER MASTER_AUDIO RAW_AUDIO TURNS.txt"""
import subprocess, sys, json, numpy as np, collections, datetime
FF="ffmpeg"; FP="ffprobe"; SR=16000
R,MASTER,RAWA,TURNS = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
def sh(c): return subprocess.run(c,capture_output=True,text=True).stdout
def grab(p,st=None,du=None):
    c=[FF,"-v","quiet"]
    if st is not None: c+=["-ss",f"{st:.3f}"]
    if du is not None: c+=["-t",f"{du:.3f}"]
    c+=["-i",p,"-vn","-ac","1","-ar",str(SR),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(c,capture_output=True).stdout,dtype=np.float32).astype(np.float64)
def xc(a,b):
    n=1<<int(np.ceil(np.log2(len(a)+len(b))))
    a=a-a.mean(); b=b-b.mean()
    r=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(b,n)),n)
    r=np.concatenate((r[-(len(b)-1):],r[:len(a)]))
    lags=np.arange(-(len(b)-1),len(a)); k=int(np.argmax(np.abs(r)))
    m=np.ones_like(r,bool); m[max(0,k-400):k+400]=False
    return lags[k]/SR, abs(r[k])/(r[m].std()+1e-12)
def find(needle,hay,hs):
    if len(hay)<=len(needle): return None,0
    n=1<<int(np.ceil(np.log2(len(hay)+len(needle))))
    a=hay-hay.mean(); b=needle-needle.mean(); b/=(np.linalg.norm(b)+1e-12)
    r=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(b,n)),n)
    v=r[:len(hay)-len(needle)+1]; k=int(np.argmax(v))
    m=np.ones_like(v,bool); m[max(0,k-400):k+400]=False
    return hs+k/SR, v[k]/(v[m].std()+1e-12)
FAIL=[]; WARN=[]
print("="*74); print("EPISODE QA REPORT"); print("="*74)

# 1 FORMAT
info=sh([FP,"-v","error","-select_streams","v:0","-show_entries",
  "stream=width,height,r_frame_rate,pix_fmt,color_transfer,color_primaries",
  "-show_entries","format=duration","-of","default=nw=1",R])
print("\n[1] FORMAT"); print("  "+info.strip().replace("\n","\n  "))
dur=float([l for l in info.splitlines() if l.startswith("duration=")][0].split("=")[1])
mdur=float(sh([FP,"-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",MASTER]).strip())
print(f"  render {dur:.2f}s vs master {mdur:.2f}s  delta {dur-mdur:+.2f}s")
if abs(dur-mdur)>1.0: FAIL.append(f"duration off by {dur-mdur:+.2f}s")

# 2 LIP SYNC
print("\n[2] LIP SYNC  (render audio vs master, 0.0ms ideal, >50ms perceptible)")
pts=[t for t in np.linspace(60,dur-40,10)]
lags=[]
for t in pts:
    a=grab(R,t,20.0); b=grab(MASTER,t,20.0)
    if min(len(a),len(b))<SR: continue
    lag,psr=xc(a,b); lags.append(lag)
    flag="" if abs(lag)<=0.050 and psr>=12 else "  <-- CHECK"
    print(f"  {t:7.0f}s  {lag*1000:+8.1f} ms   PSR {psr:6.1f}{flag}")
if lags:
    mx=max(abs(np.array(lags)))*1000
    print(f"  worst |lag| {mx:.1f} ms   (one frame at 30fps = 33.3 ms)")
    if mx>50: FAIL.append(f"lip sync off by up to {mx:.0f}ms")
    elif mx>33.4: WARN.append(f"lip sync up to {mx:.0f}ms, over one frame")

# 3 PII
print("\n[3] PRIVACY  (raw audio that must NOT survive the air cuts)")
NEED=[("private line 561-840-6551",1312.60,4.60,False),
      ("'that is a private line'",1317.50,4.00,False),
      ("personal email carlosoroff57",1352.90,4.20,False),
      ("'that is my personal one'",1358.80,3.20,False),
      ("CONTROL office 561-840-1090",1344.10,3.60,True),
      ("CONTROL intro",200.00,4.00,True)]
for lab,st,du,want in NEED:
    nd=grab(RAWA,st,du); best=0
    for cs in np.arange(0,dur,100.0):
        hay=grab(R,cs,min(110.0,dur-cs))
        if len(hay)<=len(nd): continue
        _,p=find(nd,hay,cs); best=max(best,p)
    present=best>=20; ok=(present==want)
    print(f"  {lab:32} PSR {best:6.1f}  {'present' if present else 'absent ':8} {'OK' if ok else '*** FAIL ***'}")
    if not ok: FAIL.append(f"PII check failed: {lab}")

# 4 CAMERA FOLLOWS SPEAKER
print("\n[4] CAMERA vs SPEAKER")
W,H=64,36
subprocess.run([FF,"-v","error","-y","-i",R,"-vf",f"fps=1/2,scale={W}:{H}","-pix_fmt","gray",
                "-f","rawvideo","/tmp/_qa.gray"],check=True)
X=np.fromfile("/tmp/_qa.gray",dtype=np.uint8).reshape(-1,W*H).astype(np.float64)
Z=X-X.mean(1,keepdims=True); Z/=(np.linalg.norm(Z,axis=1,keepdims=True)+1e-9)
def km(Z,k,it=80,seed=0):
    rng=np.random.default_rng(seed); C=Z[rng.choice(len(Z),k,replace=False)].copy()
    for _ in range(it):
        lab=np.argmax(Z@C.T,axis=1)
        for j in range(k):
            m=lab==j
            if m.sum(): C[j]=Z[m].mean(0)/(np.linalg.norm(Z[m].mean(0))+1e-9)
    return lab,C,(Z*C[lab]).sum(1).mean()
q={}
for k in (2,3,4): _,_,q[k]=km(Z,k)
print(f"  cluster quality k=2 {q[2]:.3f}  k=3 {q[3]:.3f}  k=4 {q[4]:.3f}  -> {'3 angles' if q[3]-q[2]>0.05 and q[4]-q[3]<0.03 else 'AMBIGUOUS'}")
lab,_,_=km(Z,3)
turns=[]
for ln in open(TURNS):
    t,s=ln.split(); h,m,sec=t.split(':')
    turns.append((int(h)*3600+int(m)*60+int(sec),int(s)))
turns.sort(key=lambda x: x[0])   # time only; stable, so ties keep transcript order
def spk(raw):
    cur=turns[0][1]
    for t,s in turns:
        if t<=raw: cur=s
        else: break
    return cur
CUT1,CUT2=1307.5,1318.0
def raw_of(p): return p if p<CUT1 else (p+30.85 if p<CUT2 else p+72.17)
IS_EDIT = abs(dur-mdur)<1.0 and mdur<1700
rows=[]
for i,c in enumerate(lab):
    pub=i*2.0
    raw = raw_of(pub) if IS_EDIT else pub
    rows.append((pub,spk(raw),int(c)))
NAME_={1:"Mike",2:"Dave",3:"Arlosoroff"}
best=None
import itertools
for perm in itertools.permutations([0,1,2]):
    mp={1:perm[0],2:perm[1],3:perm[2]}
    ag=sum(1 for _,s,c in rows if mp[s]==c)/len(rows)
    if best is None or ag>best[0]: best=(ag,mp)
ag,mp=best
print("  cluster -> person mapping chosen: " + ", ".join(f"cluster{mp[k]}={NAME_[k]}" for k in (1,2,3)))
print(f"  agreement {ag*100:.1f}%   (~82% is the room-mic ceiling; below 70% means wrong camera)")
if ag<0.70: FAIL.append(f"camera follows speaker only {ag*100:.0f}%")
elif ag<0.78: WARN.append(f"camera agreement {ag*100:.0f}%, under the usual 82%")
inv={v:k for k,v in mp.items()}
NAME={1:"Mike",2:"Dave",3:"Arlosoroff"}
for cl in (0,1,2):
    on=(lab==cl).mean()*100
    sp=sum(1 for _,s,_ in rows if mp[s]==cl)/len(rows)*100
    print(f"    {NAME[inv[cl]]:11} on screen {on:5.1f}%  speaking {sp:5.1f}%  delta {on-sp:+5.1f}")
print("  five-minute blocks   (" + " ".join(NAME[inv[c]] for c in (0,1,2)) + "):")
for b0 in range(0,int(dur),300):
    seg=[(p,s,c) for p,s,c in rows if b0<=p<b0+300]
    if not seg: continue
    a=sum(1 for _,s,c in seg if mp[s]==c)/len(seg)*100
    sh_=[sum(1 for _,_,c in seg if c==cl)/len(seg)*100 for cl in (0,1,2)]
    miss="  <-- an angle is ABSENT" if min(sh_)==0 else ""
    print(f"    {b0//60:>3}-{min(b0+300,int(dur))//60:<3} min  {a:5.1f}%   {sh_[0]:5.1f} {sh_[1]:5.1f} {sh_[2]:5.1f}{miss}")
    if a<60: FAIL.append(f"block {b0//60}-{(b0+300)//60}min only {a:.0f}% agreement")

# 5 LOOK CONSISTENCY ACROSS ANGLES
print("\n[5] LOOK CONSISTENCY  (a mis-tone-mapped angle jumps at every cut to it)")
stats={}
for cl in (0,1,2):
    idx=np.where(lab==cl)[0][:40]
    vals=[]
    for i in idx[::max(1,len(idx)//12)]:
        raw=subprocess.run([FF,"-v","quiet","-ss",str(i*2),"-i",R,"-frames:v","1",
            "-vf","scale=64:36","-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True).stdout
        if len(raw)>=64*36*3:
            a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,3).astype(float); vals.append(a.mean(0))
    if vals:
        v=np.array(vals).mean(0); stats[cl]=v
        print(f"    {NAME[inv[cl]]:11} mean RGB {v[0]:5.1f} {v[1]:5.1f} {v[2]:5.1f}   luma {v.mean():5.1f}")
if len(stats)==3:
    lum=[stats[c].mean() for c in stats]
    spread=max(lum)-min(lum)
    print(f"    luma spread across angles {spread:.1f}  ({'OK' if spread<28 else 'WIDE - check tone mapping'})")
    if spread>=28: WARN.append(f"luma spread {spread:.0f} across angles")

# 6 BLACK / FROZEN
print("\n[6] BLACK OR FROZEN FRAMES")
blk=int((X.mean(1)<16).sum()); print(f"    near-black sampled frames: {blk}")
d=np.abs(np.diff(X,axis=0)).mean(1); frozen=int((d<0.35).sum())
print(f"    near-identical consecutive samples: {frozen} of {len(d)}")
if blk>2: FAIL.append(f"{blk} black frames")
if frozen>len(d)*0.06: WARN.append(f"{frozen} near-identical frame pairs, possible freeze")

# 7 LOUDNESS
print("\n[7] LOUDNESS")
e=subprocess.run([FF,"-hide_banner","-nostats","-i",R,"-af","ebur128=framelog=quiet","-f","null","-"],
                 capture_output=True,text=True).stderr
tail=[l.strip() for l in e.splitlines()[-14:] if any(x in l for x in ("I:","LRA:","Peak"))]
for l in tail: print("    "+l)

print("\n"+"="*74)
if FAIL: print("RESULT: FAIL"); [print("  FAIL: "+f) for f in FAIL]
elif WARN: print("RESULT: PASS WITH WARNINGS"); [print("  warn: "+w) for w in WARN]
else: print("RESULT: PASS - all checks clean")
print("="*74)
