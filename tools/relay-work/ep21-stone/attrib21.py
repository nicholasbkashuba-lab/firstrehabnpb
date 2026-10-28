import numpy as np
d=np.load("embeds.npz"); t=d["t"]; E=d["e"]; rms=d["rms"]
E=E/np.linalg.norm(E,axis=1,keepdims=True)
def rng(a,b): return (t>=a)&(t<=b)
seeds={"M":[(3,56),(541,577),(1553,1616)],
       "D":[(73,140),(905,1000),(1495,1532)],
       "G":[(280,357),(386,430),(455,538),(1036,1083)]}
names=list(seeds); C=[]
for k in names:
    m=np.zeros(len(t),bool)
    for a,b in seeds[k]: m|=rng(a,b)
    m&=rms>np.percentile(rms,30)
    c=E[m].mean(0); C.append(c/np.linalg.norm(c))
C=np.stack(C); S=E@C.T
for _ in range(2):
    lab=S.argmax(1); srt=np.sort(S,1); marg=srt[:,-1]-srt[:,-2]
    for i,n in enumerate(names):
        m=(lab==i)&(marg>0.12)&(rms>np.percentile(rms,30))
        if m.sum()>20: c=E[m].mean(0); C[i]=c/np.linalg.norm(c)
    S=E@C.T
lab=S.argmax(1)
np.savez("spk_emb.npz",t=t,S=S,names=np.array(names),rms=rms)
print("centroid sims\n",np.round(C@C.T,2))
sp=rms>np.percentile(rms,25)
for i,n in enumerate(names): print(n,f"{(lab[sp]==i).mean()*100:.1f}%")
# held-out checks (not seeds)
val=[("D",62,70,"1:02 Dave rock and roll"),("D",160,275,"2:40-4:35 Dave intro EMG"),("G",590,705,"9:43-11:45 Reed outcomes/H&P"),
     ("M",719,736,"11:59 Mike scientific"),("G",794,833,"13:14 Reed carpal/brachial"),("M",835,862,"13:55 Mike Dr House/Charcot"),
     ("G",863,890,"14:23 Reed stenosis"),("G",1009,1016,"16:49 phone"),("D",1087,1160,"18:07 Dave MRI/trust"),
     ("M",1199,1250,"19:59 Mike pain to power"),("D",1254,1338,"20:55 Dave vitamins/statin"),("M",1339,1360,"22:19 Mike Charcot"),
     ("G",1332,1343,"22:12? check"),("M",1460,1494,"24:20 Mike classics")]
for n,a,b,desc in val:
    m=rng(a,b)&(rms>np.percentile(rms,25))
    print(f"{desc:<30} expect {n} got "+" ".join(f"{names[i]}={((lab[m]==i).mean()*100):.0f}%" for i in range(3)))
