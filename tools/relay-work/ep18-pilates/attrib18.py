import numpy as np, json
d=np.load("embeds.npz"); t=d["t"]; E=d["e"]; rms=d["rms"]
E=E/np.linalg.norm(E,axis=1,keepdims=True)
def rng(a,b): return (t>=a)&(t<=b)
# seeds from transcript-certain stretches (master seconds)
seeds={"MIKE":[(3,56),(1230,1236),(1357,1395)],
       "DAVE":[(108,188),(1282,1340)],
       "ELYSE":[(259,296),(784,812)],
       "DANI":[(456,460),(527,553),(992,1040)]}
names=list(seeds); M=[]
for k in names:
    m=np.zeros(len(t),bool)
    for a,b in seeds[k]: m|=rng(a,b)
    m&=rms>np.percentile(rms,30)
    c=E[m].mean(0); M.append(c/np.linalg.norm(c))
M=np.stack(M); S=E@M.T
for _ in range(2):
    lab=S.argmax(1); srt=np.sort(S,1); marg=srt[:,-1]-srt[:,-2]
    for i,n in enumerate(names):
        m=(lab==i)&(marg>0.12)&(rms>np.percentile(rms,30))
        if m.sum()>20: c=E[m].mean(0); M[i]=c/np.linalg.norm(c)
    S=E@M.T
lab=S.argmax(1)
np.savez("spk_emb.npz",t=t,S=S,names=np.array(names),rms=rms)
print("centroid sims\n",np.round(M@M.T,2))
sp=rms>np.percentile(rms,25)
for i,n in enumerate(names): print(n,f"{(lab[sp]==i).mean()*100:.1f}%")
val=[("ELYSE",320,333,"5:13 seven pillars"),("DANI",435,446,"7:15? check"),("ELYSE",350,375,"5:52 office/number"),
     ("DANI",606,630,"10:12 studio Northlake"),("DAVE",664,700,"11:02 30% postmeno"),("ELYSE",783,830,"13:03 gut"),
     ("ELYSE",862,875,"14:22 brussels"),("DANI",1040,1110,"17:24 Pilates hist"),("DANI",1110,1177,"18:30 Eve Gentry"),
     ("MIKE",1188,1215,"19:51 Mike vital"),("ELYSE",1405,1415,"23:24 conditions"),("DAVE",1415,1446,"23:35 sleep Dave"),
     ("ELYSE",1513,1526,"25:13 blue light"),("MIKE",1573,1580,"26:13? "),("MIKE",1600,1634,"26:40 outro")]
for n,a,b,desc in val:
    m=rng(a,b)&(rms>np.percentile(rms,25))
    print(f"{desc:<22} expect {n:<5} got "+" ".join(f"{names[i]}={((lab[m]==i).mean()*100):.0f}%" for i in range(4)))
