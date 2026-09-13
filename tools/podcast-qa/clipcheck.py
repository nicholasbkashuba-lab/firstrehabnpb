import subprocess, numpy as np, os, json
FF="ffmpeg"; SR=16000
def grab(path,start=0,dur=None):
    cmd=[FF,"-v","quiet"]
    if start: cmd+=["-ss",f"{start:.3f}"]
    if dur: cmd+=["-t",f"{dur:.3f}"]
    cmd+=["-i",path,"-vn","-ac","1","-ar",str(SR),"-f","f32le","-"]
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,dtype=np.float32).astype(np.float64)
def locate(needle,hay,hay_start):
    n=1<<int(np.ceil(np.log2(len(hay)+len(needle))))
    a=hay-hay.mean(); b=needle-needle.mean(); b/= (np.linalg.norm(b)+1e-12)
    r=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(b,n)),n)
    v=r[:len(hay)-len(needle)+1]
    k=int(np.argmax(v)); m=np.ones_like(v,bool); m[max(0,k-400):k+400]=False
    return hay_start+k/SR, v[k]/(v[m].std()+1e-12)
def dur(p):
    o=subprocess.run([FF,"-hide_banner","-i",p],capture_output=True,text=True).stderr
    for ln in o.splitlines():
        if "Duration:" in ln:
            t=ln.split("Duration:")[1].split(",")[0].strip()
            h,m,s=t.split(":"); return int(h)*3600+int(m)*60+float(s)
    return None
MASTER="ep14/ep14-arlosoroff-FINAL.mp4"
# documented master in-points from clips.md "AS BUILT"
DOC={"01-15-versus-50.mp4":(753.90,767.10,"Mike"),
     "02-average-age-13.mp4":(648.40,673.80,"Arlosoroff"),
     "03-county-numbers.mp4":(600.20,619.15,"Arlosoroff"),
     "04-nobody-is-moving.mp4":(834.87,864.65,"Dave"),
     "05-sight-unseen.mp4":(448.59,470.70,"Arlosoroff"),
     "06-pedal-assist.mp4":(964.39,989.45,"Arlosoroff")}
print(f"{'clip':26} {'len':>6} {'doc_in':>8} {'found_in':>9} {'drift':>7} {'PSR':>7}  audio matches master?")
print("-"*92)
for name,(din,dout,who) in DOC.items():
    p=f"ep14clips/clips/{name}"
    d=dur(p)
    nd=grab(p)[:int(SR*min(6.0,d))]
    hay=grab(MASTER,max(0,din-45),110.0)
    t,psr=locate(nd,hay,max(0,din-45))
    ok = psr>=20
    print(f"{name:26} {d:6.2f} {din:8.2f} {t:9.2f} {t-din:+7.2f} {psr:7.1f}  {'YES' if ok else 'NO'}")
