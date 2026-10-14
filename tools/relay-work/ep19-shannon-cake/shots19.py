import numpy as np, json
d=np.load("spk.npz"); t=d["t"]; F=d["F"]; names=list(d["names"]); rms=d["rms"]; tile=d["tile"]
K=json.load(open("edit.json"))["keep"]
P=2.5; n=len(t); k=len(names)
dp=np.zeros((n,k)); bp=np.zeros((n,k),int); dp[0]=F[0]
for i in range(1,n):
    for j in range(k):
        c=dp[i-1]-P*(np.arange(k)!=j); bp[i,j]=c.argmax(); dp[i,j]=c.max()+F[i,j]
lab=np.zeros(n,int); lab[-1]=dp[-1].argmax()
for i in range(n-1,0,-1): lab[i-1]=bp[i,lab[i]]
np.save("vit_lab.npy",lab)
# per-window angle: Shannon only when Zoom is actually showing her tile
ang=[]
for i in range(n):
    nm=names[lab[i]]
    ang.append("SHAN" if nm=="SHANNON" and tile[i] else "HOSTS" if nm=="SHANNON" else nm)
def runs(a):
    segs=[];st=t[0]-0.25
    for i in range(1,len(a)):
        if a[i]!=a[i-1]: b=(t[i-1]+t[i])/2; segs.append([st,b,a[i-1]]); st=b
    segs.append([st,t[-1]+0.25,a[-1]]); return segs
def merge(sq):
    o=[]
    for s in sq:
        if o and o[-1][2]==s[2]: o[-1][1]=s[1]
        else: o.append(list(s))
    return o
segs=merge(runs(ang))
for minlen in (1.5,2.5):
    out=[]
    for s in segs:
        if s[1]-s[0]<minlen and out: out[-1][1]=s[1]
        else: out.append(s)
    segs=merge(out)
spk=[list(s) for s in segs]
tileat=lambda x: tile[min(np.searchsorted(t,x),n-1)]
final=[];RX=[0]
for s,e,a in segs:
    while e-s>24:
        lo,hi=s+11,min(s+20,e-8)
        m=(t>=lo)&(t<=hi); q=float(t[m][np.argmin(rms[m])])
        final.append([s,q,a])
        if a=="SHAN": rx,rl="HOSTS",4.0
        elif a=="HOSTS": rx,rl=("DAVE","MIKE")[RX[0]%2],3.5; RX[0]+=1
        else:
            other="MIKE" if a=="DAVE" else "DAVE"
            rx,rl=("SHAN" if tileat(q+1) and tileat(q+3) else ["HOSTS",other][RX[0]%2]),3.5; RX[0]+=1
        final.append([q,q+rl,rx]); s=q+rl
    final.append([s,e,a])
final=merge(final)
# clip to the kept ranges
shots=[]
for s,e,a in final:
    for ka,kb in K:
        x,y=max(s,ka),min(e,kb)
        if y-x>0.02: shots.append([round(x,3),round(y,3),a])
shots[0][0]=K[0][0]; shots[-1][1]=K[-1][1]
tot=sum(e-s for s,e,_ in shots); share={}
for s,e,a in shots: share[a]=share.get(a,0)+e-s
print(len(shots),"shots avg",round(tot/len(shots),1),"longest",round(max(e-s for s,e,_ in shots),1))
for a,v in sorted(share.items()): print(f"  {a:<6}{v/tot*100:5.1f}%")
on=lambda x: next((a for s,e,a in shots if s<=x<e),None)
sp=rms>np.percentile(rms,30); kept=np.array([any(a<=x<b for a,b in K) for x in t])
want={"DAVE":"DAVE","MIKE":"MIKE","SHANNON":"SHAN"}
raw=F.argmax(1)
match=np.array([on(x)==want[names[r]] for x,r in zip(t,raw)])
m=sp&kept
print("on screen == fused speaker:",f"{match[m].mean()*100:.1f}%")
for i,nm in enumerate(names):
    mm=m&(raw==i); print(f"  {nm}: {match[mm].mean()*100:.1f}% of own speech on screen")
for b0 in range(0,1800,300):
    c={}
    for s,e,a in shots:
        ov=max(0,min(e,b0+300)-max(s,b0)); c[a]=c.get(a,0)+ov
    tt=sum(c.values())
    if tt: print(f"{b0//60:02d}-{b0//60+5:02d} "+" ".join(f"{k}:{v/tt*100:.0f}" for k,v in sorted(c.items()) if v>0))
json.dump({"shots":shots,"keep":K},open("cuts19.json","w"),indent=0)
