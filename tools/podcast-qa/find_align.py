import subprocess, numpy as np, sys
FF="ffmpeg"; SR=16000
def grab(path,start,dur):
    raw=subprocess.run([FF,"-v","quiet","-ss",f"{start:.3f}","-t",f"{dur:.3f}","-i",path,
        "-vn","-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).astype(np.float64)
def locate(needle, hay, hay_start):
    n=1<<int(np.ceil(np.log2(len(hay)+len(needle))))
    a=hay-hay.mean(); b=needle-needle.mean()
    r=np.fft.irfft(np.fft.rfft(a,n)*np.conj(np.fft.rfft(b,n)),n)
    valid=r[:len(hay)-len(needle)+1]
    k=int(np.argmax(valid)); peak=valid[k]
    m=np.ones_like(valid,bool); m[max(0,k-400):k+400]=False
    psr=peak/(valid[m].std()+1e-12)
    return hay_start + k/SR, psr
RAW,ED=sys.argv[1],sys.argv[2]
HS,HD=1280.0,160.0
hay=grab(RAW,HS,HD)
print("Locating each 4s slice of the EDITED file inside RAW 1280-1440s")
print(f"{'pub_t':>9} {'-> raw_t':>10} {'PSR':>8}   implied cut offset")
print("-"*56)
for pub in [1295.0,1302.0,1306.0,1309.0,1311.0,1313.0,1315.0,1317.0,1319.0,1321.0,1325.0,1330.0]:
    nd=grab(ED,pub,4.0)
    if len(nd)<SR: print(f"{pub:9.2f}  short"); continue
    raw_t,psr=locate(nd,hay,HS)
    print(f"{pub:9.2f} {raw_t:10.2f} {psr:8.1f}   {raw_t-pub:+.2f}s")
