import numpy as np, json
d=np.load("spk_emb.npz"); t=d["t"]; S=d["S"]; names=list(d["names"]); rms=d["rms"]
z=lambda a:(a-a.mean(0))/(a.std(0)+1e-9)
F=z(S); F[rms<np.percentile(rms,12)]=0
P=2.5; n=len(t); K=len(names)
dp=np.zeros((n,K)); bp=np.zeros((n,K),int); dp[0]=F[0]
for i in range(1,n):
    for k in range(K):
        c=dp[i-1]-P*(np.arange(K)!=k); bp[i,k]=c.argmax(); dp[i,k]=c.max()+F[i,k]
lab=np.zeros(n,int); lab[-1]=dp[-1].argmax()
for i in range(n-1,0,-1): lab[i-1]=bp[i,lab[i]]
np.save("vit_lab.npy",lab)
CUT=(1235.70,1247.40); MDUR=1637.20
ANG={"MIKE":"MIKE","DAVE":"DAVE","ELYSE":"G_ELYSE","DANI":"G_DANI"}
segs=[]; st=0.0
for i in range(1,n):
    if lab[i]!=lab[i-1]:
        b=(t[i-1]+t[i])/2; segs.append([st,b,names[lab[i-1]]]); st=b
segs.append([st,MDUR,names[lab[-1]]])
def merge(sq):
    o=[]
    for s in sq:
        if o and o[-1][2]==s[2]: o[-1][1]=s[1]
        else: o.append(list(s))
    return o
segs=merge(segs)
for minlen in (2.0,3.0):
    out=[]
    for s in segs:
        if s[1]-s[0]<minlen and out: out[-1][1]=s[1]
        else: out.append(s)
    segs=merge(out)
spk_segs=[list(s) for s in segs]
# angles + variety: guest monologues alternate single / wide; long host shots get a guest-wide reaction
final=[]; RX=[0]
for s,e,nm in segs:
    ang=ANG[nm]
    while e-s>26:
        a,b=s+12,min(s+22,e-8)
        m=(t>=a)&(t<=b); q=float(t[m][np.argmin(rms[m])])
        final.append([s,q,ang])
        if nm in("ELYSE","DANI"): rx=["G_WIDE",["DAVE","MIKE"][RX[0]%2]][0]; RX[0]+=1; rl=6.0
        else: rx="G_WIDE"; rl=3.5
        final.append([q,q+rl,rx]); s=q+rl
    final.append([s,e,ang])
final=merge(final)
share={}
for s,e,a in final:
    ov=max(0,min(e,CUT[1])-max(s,CUT[0])); share[a]=share.get(a,0)+(e-s-ov)
tot=sum(share.values())
L=[e-s for s,e,_ in final]
print(len(final),"shots, avg",round(tot/len(final),1),"s, longest",round(max(L),1))
for k,v in sorted(share.items()): print(f"  {k:<8}{v/tot*100:5.1f}%")
print("speaker time:",{k:round(sum(e-s for s,e,n in spk_segs if n==k)/MDUR*100,1) for k in names})
blocks=[]
for b0 in range(0,int(MDUR),300):
    c={}
    for s,e,nm in final:
        ov=max(0,min(e,b0+300)-max(s,b0)); c[nm]=c.get(nm,0)+ov
    tt=sum(c.values()); blocks.append(f"{b0//60:02d}-{b0//60+5:02d} "+" ".join(f"{k}:{v/tt*100:.0f}" for k,v in sorted(c.items()) if v>0))
print("\n".join(blocks))
sp=rms>np.percentile(rms,30); raw=S.argmax(1)
inv={v:k for k,v in ANG.items()}
def on(tt):
    for s,e,a in final:
        if s<=tt<e: return a
    return final[-1][2]
ons=np.array([on(x) for x in t]); spk=np.array([ANG[names[r]] for r in raw])
print("on-screen == embedding speaker (speech frames):",f"{(ons[sp]==spk[sp]).mean()*100:.1f}%")
json.dump({"shots":final,"cut":CUT,"mdur":MDUR,"speaker_segs":spk_segs},open("cuts18.json","w"),indent=0)
