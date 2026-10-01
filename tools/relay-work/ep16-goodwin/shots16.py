import numpy as np, json
d=np.load("spk_emb.npz"); t=d["t"]; S=d["S"]; names=list(d["names"]); rms=d["rms"]
EL=np.load("energy_lab.npy")
z=lambda a:(a-a.mean(0))/(a.std(0)+1e-9)
F=z(S)+0.6*z(EL)
quiet=rms<np.percentile(rms,15)
F[quiet]=0  # no evidence in silence
# Viterbi with switch penalty
P=2.5; n=len(t); K=3
dp=np.zeros((n,K)); bp=np.zeros((n,K),int); dp[0]=F[0]
for i in range(1,n):
    for k in range(K):
        c=dp[i-1]-P*(np.arange(K)!=k); bp[i,k]=c.argmax(); dp[i,k]=c.max()+F[i,k]
lab=np.zeros(n,int); lab[-1]=dp[-1].argmax()
for i in range(n-1,0,-1): lab[i-1]=bp[i,lab[i]]
# Mike opens the show; force first 58s
lab[t<58]=names.index("MIKE")
step=t[1]-t[0]
CUT=(1351.80,1371.45); MDUR=1646.109
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
# reaction cuts: break shots > 34s at quietest point, cutting to the most recent other speaker
final=[]; RX=[0]
for s,e,nm in segs:
    while e-s>34:
        a,b=s+14,min(s+30,e-8)
        m=(t>=a)&(t<=b)
        q=t[m][np.argmin(rms[m])]
        others=[x for x in names if x!=nm]
        prev=[f[2] for f in final if f[2]!=nm]
        rx=prev[-1] if prev else others[0]
        if nm=="GUEST":  # alternate hosts' reactions during long guest answers
            rx=["MIKE","DAVE"][RX[0]%2]; RX[0]+=1
        final.append([s,q,nm]); final.append([q,q+3.0,rx]); s=q+3.0
    final.append([s,e,nm])
final=merge(final)
# remove the outtake from the timeline (master time kept; renderer skips CUT)
share={}
for s,e,nm in final:
    ov=max(0,min(e,CUT[1])-max(s,CUT[0])); share[nm]=share.get(nm,0)+(e-s-ov)
tot=sum(share.values())
print(len(final),"shots, avg",round(tot/len(final),1),"s, longest",round(max(e-s for s,e,_ in final),1))
for k,v in share.items(): print(k,f"{v/tot*100:.1f}%")
blocks=[]
for b0 in range(0,int(MDUR),300):
    c={}
    for s,e,nm in final:
        ov=max(0,min(e,b0+300)-max(s,b0)); c[nm]=c.get(nm,0)+ov
    tt=sum(c.values()); blocks.append(f"{b0//60}-{b0//60+5} "+" ".join(f"{k[0]}{v/tt*100:.0f}" for k,v in sorted(c.items())))
print(" | ".join(blocks))
# frame agreement with raw (pre-viterbi) embedding argmax on speech
raw=S.argmax(1); sp=rms>np.percentile(rms,30)
shot_at=np.array([names.index(next(nm for s,e,nm in final if s<=tt_<e or tt_>=final[-1][0])) for tt_ in t])
print("on-screen == embedding speaker on speech frames:", f"{(shot_at[sp]==raw[sp]).mean()*100:.1f}%")
json.dump({"shots":final,"cut":CUT,"names":names},open("cuts16.json","w"),indent=0)
