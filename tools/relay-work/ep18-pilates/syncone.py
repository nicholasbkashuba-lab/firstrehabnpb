# usage: syncone.py cam_8k.wav  -> fits cam_t = rate*master_t + off, checks residuals
import sys,json,numpy as np
exec(open('lock_rate.py').read().split("files=os.listdir")[0])
M=decode('master.mp3'); C=decode(sys.argv[1]); mdur=len(M)/SR
CH=40; N=30; pts=[]
for s in np.linspace(5,mdur-CH-5,N).astype(int):
    o,p=align(M[s*SR:(s+CH)*SR],C); pts.append((float(s),float(-o),float(p))); print(f"m{s:5d} -> cam {-o:8.2f} (d {-o-s:+7.2f}) PSR {p:6.1f}",flush=True)
P=np.array(pts); g=P[:,2]>12
A=np.polyfit(P[g,0],P[g,1],1); r=P[g,1]-np.polyval(A,P[g,0])
print("FIT rate %.6f off %.3f  n=%d resid std %.3f max %.3f"%(A[0],A[1],g.sum(),r.std(),abs(r).max()))
json.dump({"rate":float(A[0]),"off":float(A[1]),"pts":pts},open(sys.argv[1]+".sync.json","w"))
