import json, numpy as np
SR=8000; HOP=160
lock=json.load(open("sync_lock.json")); rate=lock["rate"]; off=lock["offset"]
camoff={"IMG_1852.MP4":0.0,"IMG_5142.MP4":-5.98,"IMG_0006.MP4":-0.38}
SUSAN="IMG_5142.MP4"; DAVE="IMG_1852.MP4"; MIKE="IMG_0006.MP4"
names=[DAVE,SUSAN,MIKE]
raw=np.load("rawe.npz")
f0=np.load("f0.npy"); voiced=np.load("voiced.npy")
mdur=1689.2636; refdur=1704.773333
nfr=int(refdur*SR/HOP)

# --- per-camera energy in REFERENCE time, mirroring render_final_v3 exactly
E=np.full((len(names),nfr),-1e9)
for i,v in enumerate(names):
    e=raw[v].copy(); e=np.log(e+1e-6); e=(e-np.median(e))/(e.std()+1e-9)
    w=max(1,int(0.6*SR/HOP)); e=np.convolve(e,np.ones(w)/w,mode='same')
    sh=int(round(camoff[v]*SR/HOP))
    s0=max(0,-sh); d0=max(0,sh); n2=min(len(e)-s0, nfr-d0)
    if n2>0: E[i,d0:d0+n2]=e[s0:s0+n2]

# --- f0 / voicing (master time) lifted into reference time
nm=len(f0)
ref_idx=np.clip(((np.arange(nm)*HOP/SR*rate+off)*SR/HOP).astype(int),0,nfr-1)
F=np.zeros(nfr); V=np.zeros(nfr,bool)
F[ref_idx]=f0; V[ref_idx]=voiced
# fill gaps
for arr in (F,):
    idx=np.where(arr>0)[0]
    if len(idx): arr[:]=np.interp(np.arange(nfr), idx, arr[idx])

THR=float(__import__('os').environ.get('THR','165'))
w=max(1,int(0.6*SR/HOP))
hi=np.convolve((F>THR).astype(float),np.ones(w)/w,mode='same')   # fraction of window that is high-pitch

win=np.empty(nfr,dtype=int)
BIAS=float(__import__("os").environ.get("BIAS","0"));male=np.where(E[0]>=E[2]+BIAS,0,2)      # Dave vs Mike on energy
# Schmitt trigger on the pitch gate: enter Susan high, leave low, so a value
# hovering near the threshold cannot flap and hand the shot to the wrong person.
ENT=float(__import__('os').environ.get('ENT','0.62')); EXT=float(__import__('os').environ.get('EXT','0.40'))
# entering Susan also needs the gate held for SUSTAIN seconds, so a music bed
# or a transient cannot latch her on (the show opens under music, which reads
# as stable high pitch and stole the first 16s before this was added).
SUSTAIN=float(__import__('os').environ.get('SUSTAIN','1.5'))
need=int(SUSTAIN*SR/HOP)
susan=np.zeros(nfr,dtype=bool); st_=False; run=0
for k in range(nfr):
    if st_:
        if hi[k]<EXT: st_=False; run=0
    else:
        run = run+1 if hi[k]>ENT else 0
        if run>=need: st_=True
    susan[k]=st_
win=np.where(susan, 1, male)        # 1 == SUSAN index in names

# --- shots in master time
fps_a=SR/HOP
shots=[];cur=None;st=0.0
for k in range(nfr):
    m_t=(k/fps_a-off)/rate
    if m_t<0 or m_t>mdur: continue
    if cur is None: cur=win[k]; st=m_t; continue
    if win[k]!=cur: shots.append([st,m_t,names[cur]]); cur=win[k]; st=m_t
if cur is not None: shots.append([st,mdur,names[cur]])
def merge(sq):
    out=[]
    for s,e,n in sq:
        if out and out[-1][2]==n: out[-1][1]=e
        else: out.append([s,e,n])
    return out
MINB=float(__import__('os').environ.get('MINB','2.0')); MINS=float(__import__('os').environ.get('MINS','3.0'))
shots=merge(shots); kept=[]
for s,e,n in shots:
    if e-s<MINB and kept: kept[-1][1]=e
    else: kept.append([s,e,n])
kept=merge(kept); final=[]
for s,e,n in kept:
    if e-s<MINS and final: final[-1][1]=e
    else: final.append([s,e,n])
final=merge(final)
share={}
for s,e,n in final: share[n]=share.get(n,0)+(e-s)
lab={DAVE:"Dave",SUSAN:"Susan",MIKE:"Mike"}
print(f"THR={THR}  shots {len(final)}  avg {mdur/len(final):.1f}s  max {max(e-s for s,e,n in final):.0f}s")
for n,v in sorted(share.items(),key=lambda x:-x[1]):
    print(f"  {lab[n]:6s} {v/60:5.1f} min {100*v/mdur:5.1f}%")
import collections
B=300; blocks=collections.defaultdict(lambda: collections.defaultdict(float))
for s,e,n in final:
    t=s
    while t<e:
        nb=(int(t//B)+1)*B; seg=min(e,nb)-t; blocks[int(t//B)][n]+=seg; t=min(e,nb)
print("  coverage per 5 min: " + " | ".join(
    f"{b*5}-{b*5+5}:" + ",".join(f"{lab[n][0]}{100*blocks[b].get(n,0)/max(sum(blocks[b].values()),1e-9):.0f}" for n in names)
    for b in sorted(blocks)))
json.dump([[s,e,n] for s,e,n in final], open("cuts_f0.json","w"))

# ---- reaction cuts inside long shots, at quiet points in the master
LONG=float(__import__('os').environ.get('LONG','34'))
RLEN=3.2
mr=np.load("rms.npy"); mfps=SR/HOP
out=[]
for s,e,n in final:
    d=e-s
    if d<=LONG: out.append([s,e,n]); continue
    others=[x for x in names if x!=n]
    k=int(d//LONG)                      # how many reaction beats to insert
    seg=d/(k+1)
    pos=[s+seg*(i+1) for i in range(k)]
    cur=s; oi=0
    for p in pos:
        lo=int(max(s,p-4.0)*mfps); hi=int(min(e,p+4.0)*mfps)
        if hi<=lo: continue
        q=lo+int(np.argmin(mr[lo:hi]))   # quietest frame nearby = natural pause
        qt=q/mfps
        if qt-cur<6 or e-(qt+RLEN)<6: continue
        out.append([cur,qt,n])
        out.append([qt,qt+RLEN,others[oi%len(others)]]); oi+=1
        cur=qt+RLEN
    out.append([cur,e,n])
final2=merge(out)
sh2={}
for s,e,n in final2: sh2[n]=sh2.get(n,0)+(e-s)
print(f"\nAFTER reaction cuts: {len(final2)} shots  avg {mdur/len(final2):.1f}s  max {max(e-s for s,e,n in final2):.0f}s")
for n,v in sorted(sh2.items(),key=lambda x:-x[1]):
    print(f"  {lab[n]:6s} {v/60:5.1f} min {100*v/mdur:5.1f}%")
blocks2=collections.defaultdict(lambda: collections.defaultdict(float))
for s,e,n in final2:
    t=s
    while t<e:
        nb=(int(t//B)+1)*B; sg=min(e,nb)-t; blocks2[int(t//B)][n]+=sg; t=min(e,nb)
print("  coverage: " + " | ".join(
    f"{b*5}-{b*5+5}:" + ",".join(f"{lab[n][0]}{100*blocks2[b].get(n,0)/max(sum(blocks2[b].values()),1e-9):.0f}" for n in names)
    for b in sorted(blocks2)))
json.dump([[s,e,n] for s,e,n in final2], open("cuts_final.json","w"))
print("wrote cuts_final.json")

# ---- opening correction (evidence-based, not tuning)
# transcript-full.md: [00:01] Mike opens "Good morning, and welcome once again
# to Pain 2 Power right here on Legends 100.3. Mike McGann with you". The show
# opens under a music bed whose stable pitch reads as Susan, so the gate hands
# her the first shot. Force the intro to Mike; Dave takes over at ~16.5s.
cuts=json.load(open("cuts_final.json"))
if cuts and cuts[0][2]!=MIKE and cuts[0][1]<=20:
    cuts[0][2]=MIKE
    cuts=[list(x) for x in merge([[c[0],c[1],c[2]] for c in cuts])]
    json.dump(cuts, open("cuts_final.json","w"))
    print(f"opening corrected to Mike; {len(cuts)} shots")
