# Three voices: Dave + Mike in the studio, Shannon on Zoom. Fuse ECAPA embeddings
# (Dave vs Mike) with studio-phone energy (Shannon is only in the board mix, so both
# studio phones go quiet when she talks) and Zoom's own active-speaker tile.
import numpy as np, json
d=np.load("embeds.npz"); t=d["t"]; E=d["e"]; rms=d["rms"]
E=E/np.linalg.norm(E,axis=1,keepdims=True)
en=np.load("energy.npz"); z=np.load("zoomtile.npz")
ED=np.interp(t,en["t"],np.nan_to_num(en["DAVE"],nan=0)); EM=np.interp(t,en["t"],np.nan_to_num(en["MIKE"],nan=0))
tile=np.interp(t*0.999974+237.084,z["t"],z["m"])>80
studio=(ED+EM)/2
rng=lambda a,b:(t>=a)&(t<=b)
seeds={"MIKE":[(75,160),(1663,1720)],"DAVE":[(163,240),(726,790)],"SHANNON":[(282,305),(470,600),(1148,1250)]}
names=list(seeds); M=[]
loud=rms>np.percentile(rms,30)
for k in names:
    m=np.zeros(len(t),bool)
    for a,b in seeds[k]: m|=rng(a,b)
    c=E[m&loud].mean(0); M.append(c/np.linalg.norm(c))
M=np.stack(M); S=E@M.T
for _ in range(2):
    lab=S.argmax(1); srt=np.sort(S,1); marg=srt[:,-1]-srt[:,-2]
    for i in range(3):
        m=(lab==i)&(marg>0.12)&loud
        if m.sum()>20: c=E[m].mean(0); M[i]=c/np.linalg.norm(c)
    S=E@M.T
print("centroid sims\n",np.round(M@M.T,2))
z_=lambda a:(a-a.mean(0))/(a.std(0)+1e-9)
F=z_(S)
F[:,2]+= -1.2*np.clip(studio+0.8,-1.5,1.5) + 0.8*tile
F[:,0]+= 1.0*np.clip(EM-ED,-1,1); F[:,1]+= 1.0*np.clip(ED-EM,-1,1)
F[rms<np.percentile(rms,12)]=0
np.savez("spk.npz",t=t,F=F,names=np.array(names),rms=rms,tile=tile)
lab=F.argmax(1); sp=rms>np.percentile(rms,25)
for i,n in enumerate(names): print(n,f"{(lab[sp]==i).mean()*100:.1f}%")
emb=S.argmax(1); print("embedding vs fused agreement",f"{(emb[sp]==lab[sp]).mean()*100:.1f}%")
val=[("MIKE",92,150,"intro"),("DAVE",163,230,"Dave intro"),("SHANNON",310,370,"win alone"),("DAVE",380,460,"Dave Medicare"),
 ("SHANNON",480,600,"father/reporting"),("MIKE",668,705,"Mike broadcasting"),("DAVE",727,800,"China setup"),("SHANNON",805,828,"father"),
 ("SHANNON",1000,1090,"Winner"),("DAVE",1105,1140,"PT headaches"),("SHANNON",1150,1250,"workout"),("MIKE",1310,1340,"priorities"),
 ("SHANNON",1345,1480,"rotator"),("DAVE",1495,1545,"misrepresent"),("DAVE",1582,1610,"joke"),("DAVE",1648,1675,"vote"),("MIKE",1680,1725,"outro")]
tot=0;ok=0
for n,a,b,desc in val:
    m=rng(a,b)&sp; r={names[i]:(lab[m]==i).mean()*100 for i in range(3)}; tot+=m.sum(); ok+=(lab[m]==names.index(n)).sum()
    print(f"{desc:<18} expect {n:<8} "+" ".join(f"{k}={v:.0f}%" for k,v in r.items()))
print(f"validated windows correct: {ok/tot*100:.1f}%")
