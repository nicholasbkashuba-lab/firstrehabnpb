import numpy as np, subprocess, json
SR=8000
def rd(f): return np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-"],capture_output=True).stdout,np.float32)
CAMS={"DAVE":("IMG_1996_8k.wav",0.999967,-38.003),"MIKE":("IMG_5504_8k.wav",0.999957,-35.282),"ZOOM":("video1573954541_8k.wav",0.999974,237.084)}
t=np.arange(0.75,1770,0.5); out={}
M=rd("master.mp3") if False else None
for n,(f,r,o) in CAMS.items():
    x=rd(f); e=[]
    for tm in t:
        c=r*tm+o; a=int((c-0.75)*SR); b=int((c+0.75)*SR)
        seg=x[max(a,0):max(b,0)]
        e.append(np.sqrt((seg**2).mean()) if len(seg)>100 else np.nan)
    e=np.log(np.array(e)+1e-6); out[n]=e-np.nanmedian(e)
np.savez("energy.npz",t=t,**out)
print({k:np.isnan(v).sum() for k,v in out.items()})
