"""Episode 21 shot list on the master (RAW mp3) timeline. Speaker = ECAPA embedding label."""
import numpy as np, json
d=np.load('spk_emb.npz'); te=d['t']; S=d['S']; erms=d['rms']; names=list(d['names'])
lab_e=S.argmax(1)
f=np.load('feats.npz'); T=f['T']; M=f['M0']
H=0.1; FPS=30
START,END=0.0,1622.80
CUT=(359.2,381.3667)                      # Dave's retake of the Zander intro
idx=lambda t:int(round(t/H))
# per 0.1s speaker: nearest embedding window; silence keeps the previous speaker
lab=[]; prev='M'; thr=np.percentile(M,35)
for t in np.arange(START,END,H):
    i=int(np.argmin(np.abs(te-t)))
    s=names[lab_e[i]] if M[min(idx(t),len(M)-1)]>thr else prev
    lab.append(s); prev=s
runs=[]
for i,s in enumerate(lab):
    t=START+i*H
    if runs and runs[-1][2]==s: runs[-1][1]=t+H
    else: runs.append([t,t+H,s])
# absorb short interjections (<1.6s) into the surrounding shot, repeat until stable
for _ in range(4):
    out=[]
    for r in runs:
        if out and (r[1]-r[0]<1.6 or out[-1][2]==r[2]): out[-1][1]=r[1]
        else: out.append(list(r))
    runs=out
# shots over 30s get a reaction cut (3.5s of a listener) at the quietest point near each 22s mark
react={'G':['D','M'],'D':['G','M'],'M':['G','D']}
shots=[]; k=0
for a,b,s in runs:
    cur=a
    while b-cur>30:
        tgt=cur+22; win=np.arange(tgt-5,tgt+5,H)
        q=win[np.argmin([M[idx(x)] for x in win])]
        shots.append([cur,q,s]); who=react[s][k%2]; k+=1
        shots.append([q,q+3.5,who]); cur=q+3.5
    shots.append([cur,b,s])
# guest reaction on two known moments (laughs at Dave's lines)
# split at the edit, drop the cut range
out=[]
for a,b,s in shots:
    if b<=CUT[0] or a>=CUT[1]: out.append([a,b,s]); continue
    if a<CUT[0]: out.append([a,CUT[0],s])
    if b>CUT[1]: out.append([CUT[1],b,s])
shots=out
# absorb slivers under 1.5s into the previous shot (never across the edit)
out=[]
for a,b,s in shots:
    if out and b-a<1.5 and abs(out[-1][1]-a)<1e-6 and a!=CUT[1]: out[-1][1]=b
    else: out.append([a,b,s])
shots=out
for sh in shots: sh[0]=round(sh[0]*FPS)/FPS; sh[1]=round(sh[1]*FPS)/FPS
for i in range(1,len(shots)):
    if shots[i][0]!=round(CUT[1]*FPS)/FPS: shots[i][0]=shots[i-1][1]
shots[0][0]=START; shots[-1][1]=round(END*FPS)/FPS
json.dump({'cut':CUT,'shots':shots},open('shots.json','w'))
L=np.array([b-a for a,b,s in shots]); tot=sum(L)
print(len(shots),'shots, avg %.1f max %.1f min %.1f, total %.1f s'%(L.mean(),L.max(),L.min(),tot))
print({k:'%.1f%%'%(100*sum(b-a for a,b,x in shots if x==k)/tot) for k in 'GDM'})
for b0 in range(0,int(END),300):
    seg={k:sum(max(0,min(b,b0+300)-max(a,b0)) for a,b,x in shots if x==k) for k in 'GDM'}
    print(f"{b0//60:02d}-{min(b0+300,END)//60:02.0f}: "+" ".join(f"{k}{100*v/max(1,sum(seg.values())):.0f}" for k,v in seg.items()))
# agreement with frame speaker labels
agree=np.mean([next(s for a,b,s in shots if a<=t<b)==lab[i] for i,t in enumerate(np.arange(START,END-0.1,H)) if not CUT[0]<=t<CUT[1] and M[idx(t)]>thr])
print('shot == speaker on %.1f%% of speech'%(100*agree))
