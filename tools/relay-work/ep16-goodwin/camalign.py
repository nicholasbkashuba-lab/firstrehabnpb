import json,sys,numpy as np
sys.argv=['x']
exec(open('lock_rate.py').read().split("files=os.listdir")[0])
cams={"cam_main.mov":"GUEST","IMG_1918.MP4":"DAVE","IMG_4077.MP4":"MIKE"}
sig={c:decode(c) for c in cams}
np.savez("camsig.npz",**{k.replace('.','_'):v.astype(np.float32) for k,v in sig.items()})
res={}
names=list(cams)
for i in range(3):
    for j in range(i+1,3):
        o,p=align(sig[names[i]],sig[names[j]])
        res[f"{names[i]}->{names[j]}"]=(o,p); print(names[i],names[j],f"{o:+.3f}",f"PSR {p:.0f}")
a=res["cam_main.mov->IMG_1918.MP4"][0]; b=res["IMG_1918.MP4->IMG_4077.MP4"][0]; c=res["cam_main.mov->IMG_4077.MP4"][0]
print("consistency A->B + B->C - A->C =", a+b-c)
json.dump({"IMG_1918.MP4":a,"IMG_4077.MP4":c,"cam_main.mov":0.0},open("camoff.json","w"))
