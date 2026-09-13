#!/usr/bin/env python3
"""Cut list from diarised transcript turns, with reaction cuts so long
monologues do not sit on one static shot. Turns are in RAW master time,
which is the master the renderer uses."""
import csv, sys
CAM={1:"Mike.mov", 2:"Dave.mov", 3:"Arlosoroff.MP4"}
MDUR=1731.09
MIN_SHOT=3.0; MIN_BACK=2.0
MAX_HOLD=32.0      # never sit on one angle longer than this
REACT=3.5          # length of a reaction cut
turns=[]
for ln in open(sys.argv[1]):
    t,s=ln.split(); h,m,sec=t.split(':')
    turns.append([int(h)*3600+int(m)*60+int(sec), int(s)])
turns.sort(key=lambda x:x[0])              # time only, stable
ded=[]
for t,s in turns:
    if ded and ded[-1][0]==t: ded[-1][1]=s
    else: ded.append([t,s])
segs=[]
for i,(t,s) in enumerate(ded):
    end = ded[i+1][0] if i+1<len(ded) else MDUR
    if end>t: segs.append([float(t),float(end),s])
def merge(sq):
    out=[]
    for s,e,n in sq:
        if out and out[-1][2]==n: out[-1][1]=e
        else: out.append([s,e,n])
    return out
segs=merge(segs)
kept=[]
for s,e,n in segs:
    if e-s<MIN_BACK and kept: kept[-1][1]=e
    else: kept.append([s,e,n])
kept=merge(kept)
base=[]
for s,e,n in kept:
    if e-s<MIN_SHOT and base: base[-1][1]=e
    else: base.append([s,e,n])
base=merge(base)
# reaction cuts: break any hold longer than MAX_HOLD with a look at a listener
out=[]; rot=0
for s,e,spk in base:
    others=[k for k in (1,2,3) if k!=spk]
    L=e-s
    if L<=MAX_HOLD:
        out.append([s,e,spk]); continue
    n=int(L//MAX_HOLD)
    step=L/(n+1)
    cur=s
    for i in range(n):
        seg_end=s+step*(i+1)
        out.append([cur, seg_end-REACT, spk])
        who=others[rot%2]; rot+=1
        out.append([seg_end-REACT, seg_end, who])
        cur=seg_end
    out.append([cur,e,spk])
out=[x for x in out if x[1]-x[0]>=1.0]
out=merge(out)
out[0][0]=0.0
for i in range(len(out)-1): out[i][1]=out[i+1][0]
out[-1][1]=MDUR
share={}
for s,e,n in out: share[n]=share.get(n,0)+(e-s)
print(f"{len(out)} shots over {MDUR/60:.1f} min, avg {MDUR/len(out):.1f}s, longest {max(e-s for s,e,_ in out):.1f}s")
NAME={1:"Mike",2:"Dave",3:"Arlosoroff"}
for n,v in sorted(share.items(),key=lambda x:-x[1]):
    print(f"  {NAME[n]:11} {v/60:5.1f} min  {v/MDUR*100:4.1f}%")
with open(sys.argv[2],'w',newline='') as f:
    w=csv.writer(f); w.writerow(["shot","master_start","master_end","duration","camera"])
    for i,(s,e,n) in enumerate(out,1): w.writerow([i,f"{s:.3f}",f"{e:.3f}",f"{e-s:.3f}",CAM[n]])
print("wrote",sys.argv[2])
