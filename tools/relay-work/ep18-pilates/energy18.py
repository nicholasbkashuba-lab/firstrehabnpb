import numpy as np, subprocess
SR=8000
def rd(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-"],capture_output=True).stdout,np.float32)
CAMS={"DAVE":("dave_8k.wav",0.999971,195.143),"MIKE":("mike_8k.wav",0.999973,212.981),"GUEST":("img_8k.wav",0.999960,186.044)}
d=np.load("spk_emb.npz"); t=d["t"]; rms=d["rms"]; S=d["S"]; names=list(d["names"])
En={}
for n,(f,r,o) in CAMS.items():
    x=rd(f); out=[]
    for tm in t:
        c=r*tm+o; a=int((c-0.75)*SR); b=int((c+0.75)*SR); seg=x[max(a,0):max(b,0)]
        out.append(np.sqrt((seg**2).mean()) if len(seg) else 1e-6)
    e=np.log(np.array(out)+1e-6); En[n]=e-np.median(e)
EL=np.stack([En["MIKE"] if n=="MIKE" else En["DAVE"] if n=="DAVE" else En["GUEST"] for n in names],1)
np.save("energy_lab.npy",EL)
lab=S.argmax(1); sp=rms>np.percentile(rms,30)
grp=lambda a: np.where(np.isin(a,[names.index("ELYSE"),names.index("DANI")]),9,a)
el=EL.argmax(1)
print("energy vs embedding (guests pooled) agreement:", f"{(grp(el[sp])==grp(lab[sp])).mean()*100:.1f}%")
for i,n in enumerate(names):
    m=sp&(lab==i); print(n,"-> energy says", {k:f"{(el[m]==j).mean()*100:.0f}%" for j,k in enumerate(names)})
