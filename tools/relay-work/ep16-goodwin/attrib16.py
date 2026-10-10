import numpy as np, json
d=np.load("embeds.npz"); t=d["t"]; E=d["e"]; rms=d["rms"]
E=E/np.linalg.norm(E,axis=1,keepdims=True)
def rng(a,b): return (t>=a)&(t<=b)
seeds={"MIKE":[(3,56)],"DAVE":[(64,112),(140,200)],"GUEST":[(240,320),(400,440)]}
C={}
for k,rs in seeds.items():
    m=np.zeros(len(t),bool)
    for a,b in rs: m|=rng(a,b)
    c=E[m].mean(0); C[k]=c/np.linalg.norm(c)
names=list(C); M=np.stack([C[n] for n in names])
S=E@M.T
# refine: iterate centroids using confident frames (two rounds)
for _ in range(2):
    lab=S.argmax(1); marg=np.sort(S,1)[:,-1]-np.sort(S,1)[:,-2]
    for i,n in enumerate(names):
        m=(lab==i)&(marg>0.15)&(rms>np.percentile(rms,30))
        c=E[m].mean(0); M[i]=c/np.linalg.norm(c)
    S=E@M.T
lab=S.argmax(1); marg=np.sort(S,1)[:,-1]-np.sort(S,1)[:,-2]
np.savez("spk_emb.npz",t=t,S=S,names=np.array(names),rms=rms)
print("centroid sims\n",np.round(M@M.T,2))
for n,i in zip(names,range(3)): print(n, f"{(lab==i).mean()*100:.1f}%")
# validation ranges (from transcript reading)
val=[("MIKE",617,646,"10:17-10:46 Mike long comment"),("GUEST",637+1,0,""),
     ("DAVE",1037,1105,"17:37-18:25 Dave question (incl.)"),("GUEST",1110,1180,"18:30-19:40 Goodwin"),
     ("MIKE",1200,1260,"20:00-21:00 Mike men/celebs"),("GUEST",1263,1296,"21:03-21:36 Goodwin"),
     ("DAVE",1475,1505,"24:36-25:05 Dave joke"),("GUEST",1306,1335,"21:46-22:15 Goodwin gyneco"),("GUEST",400,470,"6:40-7:50")]
for n,a,b,desc in val:
    if b==0: continue
    m=rng(a,b)&(rms>np.percentile(rms,20))
    print(f"{desc:<34} expect {n:<5} got " + " ".join(f"{names[i]}={((lab[m]==i).mean()*100):.0f}%" for i in range(3)))
