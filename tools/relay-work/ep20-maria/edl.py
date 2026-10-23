"""Build the shot list for Episode 20 on the master (board mix) timeline."""
import numpy as np, json
f=np.load('feats.npz'); T,M,D,K,Z=[f[k] for k in 'T M D K Z'.split()]
# dilate the Zoom placeholder mask 0.4s each side: the Zoom track is sampled at 4fps
Z0=Z.copy(); Z=np.minimum.reduce([np.roll(Z,k) for k in range(-4,5)])
START, END = 22.2, 1644.6
FPS=30
def ts(s):
    m,x=s.split(':'); return int(m)*60+float(x)
# Speaker turns read off the Descript transcript (M=Mike, D=Dave, A=Maria).
TURNS=[("00:22.4","M"),("01:27.6","D"),("01:45.5","M"),("01:49.4","D"),("02:38.1","M"),("02:41.5","D"),
("03:57.8","M"),("04:02.7","D"),("04:58.7","A"),("05:54.1","M"),("05:56.0","A"),("10:19.1","D"),("10:28.5","A"),
("14:05.1","D"),("15:18.9","A"),("18:12.7","M"),("19:08.8","A"),("21:21.2","D"),("22:17.5","A"),("23:44.9","D"),
("23:48.4","A"),("24:47.4","M"),("25:21.7","D"),("26:32.9","M"),("27:22.5","D")]
turns=[(ts(a),s) for a,s in TURNS]
def turn_at(t):
    s=turns[0][1]
    for a,x in turns:
        if a<=t: s=x
    return s
H=0.1
idx=lambda t:int(round(t/H))
# per-frame desired camera
def listener(t0,t1):
    # whichever studio mic is louder relative to the other over the window
    ii=range(idx(t0),idx(t1)+1)
    return 'D' if np.median([np.log(D[i]/K[i]) for i in ii])>0.18 else 'M'
lab=[]
for t in np.arange(START,END,H):
    s=turn_at(t)
    if s=='A' and Z[idx(t)]<80: s='R'      # Zoom not showing Maria: studio reaction
    lab.append(s)
runs=[]
for i,s in enumerate(lab):
    t=START+i*H
    if runs and runs[-1][2]==s: runs[-1][1]=t+H
    else: runs.append([t,t+H,s])
# a Maria run under 2s is absorbed by neighbouring reaction (never show the placeholder card)
for r in runs:
    if r[2]=='A' and r[1]-r[0]<2.0: r[2]='R'
for r in runs:
    if r[2]=='R':
        a,b=r[0],r[1]
        if b-a<1.5: a,b=a-(1.5-(b-a))/2,b+(1.5-(b-a))/2
        r[0],r[1]=a,b; r[2]=listener(a,b)
# resolve overlaps created by widening: reactions win
for i in range(len(runs)-1):
    if runs[i][1]>runs[i+1][0]:
        if runs[i+1][2]!='A': runs[i][1]=runs[i+1][0]
        else: runs[i+1][0]=runs[i][1]
runs=[r for r in runs if r[1]-r[0]>0.05]
merged=[]
for r in runs:
    if merged and merged[-1][2]==r[2]: merged[-1][1]=r[1]; continue
    if merged and r[1]-r[0]<3.0 and r[2]!='A' and merged[-1][2]!='A': merged[-1][1]=r[1]; continue
    merged.append(r)
m2=[]
for r in merged:
    if m2 and m2[-1][2]==r[2]: m2[-1][1]=r[1]
    else: m2.append(list(r))
# reaction cuts: split any shot > 32s; insert 3.6s of the listener at the quietest master point near each 26s mark
shots=[]
react={'A':['D','M'],'D':['M'],'M':['D']}
for a,b,s in m2:
    if b-a<=32: shots.append([a,b,s]); continue
    cur=a; k=0
    while b-cur>32:
        tgt=cur+24
        win=np.arange(tgt-5,tgt+5,H)
        q=win[np.argmin([M[idx(x)] for x in win])]
        shots.append([cur,q,s]); who=react[s][k%len(react[s])]; k+=1
        shots.append([q,q+3.6,who]); cur=q+3.6
    shots.append([cur,b,s])
# Maria reactions during the closing joke and goodbyes, where Zoom does show her
for a,b in [(1539.4,1541.8),(1594.2,1596.5),(1609.4,1611.8)]:
    out=[]
    for x,y,s in shots:
        if y<=a or x>=b: out.append([x,y,s]); continue
        if x<a: out.append([x,a,s])
        if y>b: out.append([b,y,s])
    out.append([a,b,'A']); shots=sorted(out)
# absorb any slice under 1.8s into the shot before it
out=[]
for x,y,s in shots:
    if out and y-x<1.8: out[-1][1]=y
    else: out.append([x,y,s])
shots=out
# snap to frame grid
for sh in shots:
    sh[0]=round(sh[0]*FPS)/FPS; sh[1]=round(sh[1]*FPS)/FPS
for i in range(1,len(shots)): shots[i][0]=shots[i-1][1]
shots[0][0]=START; shots[-1][1]=round(END*FPS)/FPS
# Maria picture must exist for every A shot
bad=[(a,b) for a,b,s in shots if s=='A' and min(Z0[idx(t)] for t in np.arange(a+0.05,b-0.05,H))<80]
json.dump(shots,open('shots.json','w'))
L=np.array([b-a for a,b,s in shots])
tot={s:sum(b-a for a,b,x in shots if x==s) for s in 'ADM'}
print(len(shots),'shots, avg %.1f, max %.1f, min %.1f'%(L.mean(),L.max(),L.min()))
print({k:'%.1f%%'%(100*v/(END-START)) for k,v in tot.items()})
print('A shots with any non-Maria zoom frames:',len(bad),bad[:8])
blocks=[]
for b0 in range(int(START),int(END),300):
    seg={s:sum(max(0,min(b,b0+300)-max(a,b0)) for a,b,x in shots if x==s) for s in 'ADM'}
    blocks.append(f"{b0//60:02d}-{min(b0+300,END)//60:02.0f}: "+" ".join(f"{k}{100*v/sum(seg.values()):.0f}" for k,v in seg.items()))
print('\n'.join(blocks))
