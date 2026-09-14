import subprocess, numpy as np, sys
FF="ffmpeg"; SR=16000
def grab(path,start,dur):
    raw=subprocess.run([FF,"-v","quiet","-ss",f"{start:.3f}","-t",f"{dur:.3f}","-i",path,
        "-vn","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).astype(np.float64)
def best(needle, hay, hay_start):
    if len(hay)<=len(needle): return None,0
    n=1<<int(np.ceil(np.log2(len(hay)+len(needle))))
    a=hay-hay.mean(); b=needle-needle.mean()
    b=b/ (np.linalg.norm(b)+1e-12)
    r=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(b,n)),n)
    valid=r[:len(hay)-len(needle)+1]
    k=int(np.argmax(valid)); peak=valid[k]
    m=np.ones_like(valid,bool); m[max(0,k-400):k+400]=False
    return hay_start+k/SR, peak/(valid[m].std()+1e-12)
RAW,ED=sys.argv[1],sys.argv[2]
ED_DUR=1658.96
NEEDLES=[
 ("PRIVATE LINE  '561-840-6551'", 1312.60, 4.60, "MUST BE ABSENT"),
 ("'that is a private line'",     1317.50, 4.00, "MUST BE ABSENT"),
 ("PERSONAL EMAIL 'carlosoroff57'",1352.90, 4.20, "MUST BE ABSENT"),
 ("'that is my personal one'",    1358.80, 3.20, "MUST BE ABSENT"),
 ("CONTROL office num 561-840-1090",1344.10,3.60, "must be PRESENT"),
 ("CONTROL intro",                  200.00,4.00, "must be PRESENT"),
]
print(f"{'needle':34} {'best PSR':>9} {'found at':>10}  {'expect':<15} result")
print("-"*88)
for label,st,dur,expect in NEEDLES:
    nd=grab(RAW,st,dur)
    bp=0; bt=None
    for cs in np.arange(0, ED_DUR, 100.0):
        hay=grab(ED,cs,min(110.0, ED_DUR-cs))
        if len(hay)<=len(nd): continue
        t,psr=best(nd,hay,cs)
        if psr>bp: bp,bt=psr,t
    present = bp>=20
    ok = (present and "PRESENT" in expect) or ((not present) and "ABSENT" in expect)
    loc = f"{bt:10.2f}" if (bt is not None and present) else "     n/a  "
    print(f"{label:34} {bp:9.1f} {loc}  {expect:<15} {'PASS' if ok else '*** FAIL ***'}")
print()
print("PSR >= 20 means the audio is present in the edited master. < 12 is noise.")
