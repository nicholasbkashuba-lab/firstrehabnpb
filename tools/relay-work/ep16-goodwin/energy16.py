import numpy as np, json
SR=8000
z=np.load("camsig.npz")
cam={"GUEST":z["cam_main_mov"],"DAVE":z["IMG_1918_MP4"],"MIKE":z["IMG_4077_MP4"]}
camoff={"GUEST":0.0,"DAVE":13.94,"MIKE":4.76}   # cam_t = ref_t + camoff
d=np.load("spk_emb.npz"); t=d["t"]; S=d["S"]; names=list(d["names"]); rms=d["rms"]
lab=S.argmax(1)
En={}
for n,x in cam.items():
    out=[]
    for tm in t:
        c=tm+26.8+camoff[n]; a=int((c-0.75)*SR); b=int((c+0.75)*SR)
        seg=x[max(a,0):max(b,0)]
        out.append(np.sqrt((seg**2).mean()) if len(seg) else 1e-6)
    e=np.log(np.array(out)+1e-6); En[n]=e-np.median(e)
EL=np.stack([En[n] for n in names],1)
elab=EL.argmax(1)
loud=rms>np.percentile(rms,30)
print("energy-vs-embedding agreement on speech frames:", f"{(elab[loud]==lab[loud]).mean()*100:.1f}%")
for i,n in enumerate(names):
    m=loud&(lab==i); print(n,"embedding frames -> energy says", {names[j]:f"{(elab[m]==j).mean()*100:.0f}%" for j in range(3)})
np.save("energy_lab.npy",EL)
