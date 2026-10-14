import json, os, subprocess, sys, numpy as np
from concurrent.futures import ThreadPoolExecutor
W,H,FPS=1920,1080,30
J=json.load(open("cuts18.json")); shots=J["shots"]; C0,C1=J["cut"]; MDUR=J["mdur"]
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
CAM={"DAVE":("dave.mov",0.999971,195.143,False,f"scale={W}:{H}:flags=bicubic,{TM}"),
     "MIKE":("Mike.mov",0.999973,212.981,True,f"scale={W}:{H}:flags=bicubic,format=yuv420p"),
     "G_WIDE":("IMG_5434.MOV",0.999960,186.044,True,f"scale={W}:{H}:flags=bicubic,{TM}"),
     "G_ELYSE":("IMG_5434.MOV",0.999960,186.044,True,f"crop=2400:1350:300:220,scale={W}:{H}:flags=bicubic,{TM}"),
     "G_DANI":("IMG_5434.MOV",0.999960,186.044,True,f"crop=1440:810:1800:540,scale={W}:{H}:flags=bicubic,{TM}")}
GAP=C1-C0
def m2o(m): return m if m<=C0 else m-GAP
pieces=[]
for s,e,a in shots:
    for x,y in ((s,min(e,C0)),(max(s,C1),e)):
        if y-x>0.01: pieces.append((x,y,a))
odur=m2o(MDUR)
edges=[int(round(m2o(p[0])*FPS)) for p in pieces]+[int(round(odur*FPS))]
def window(i):
    a,b,ang=pieces[i]; nf=edges[i+1]-edges[i]
    ms=a+(edges[i]/FPS-m2o(a)); f,r,o,skip,vf=CAM[ang]
    return ms, nf, f, r*ms+o, skip, vf
if __name__=="__main__" and sys.argv[1:2]==["mikewin"]:
    w=[(window(i)[3],window(i)[3]+window(i)[1]/FPS) for i in range(len(pieces)) if pieces[i][2]=="MIKE"]
    m=[]
    for a,b in sorted(w):
        if m and a-m[-1][1]<15: m[-1][1]=max(m[-1][1],b)
        else: m.append([a,b])
    print(json.dumps([[round(a-2,2),round(b+2,2)] for a,b in m])); sys.exit()
os.makedirs("seg",exist_ok=True)
def job(i):
    ms,nf,f,cs,skip,vf=window(i)
    if nf<=0: return None
    out=f"seg/s{i:04d}.mp4"
    if os.path.exists(out) and os.path.getsize(out)>1000: return out
    pre=max(cs-4,0)
    cmd=["ffmpeg","-v","error","-y"]+(["-skip_frame","noref"] if skip else [])+["-threads","2","-ss",f"{pre:.3f}","-i",f,
         "-ss",f"{cs-pre:.3f}","-vf",f"fps={FPS},{vf},setsar=1","-an","-frames:v",str(nf),
         "-c:v","libx264","-preset","medium","-crf","19","-threads","2","-pix_fmt","yuv420p",
         "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",out+".tmp.mp4"]
    subprocess.run(cmd,check=True); os.rename(out+".tmp.mp4",out)
    return out
if __name__=="__main__":
    ids=list(range(len(pieces)))
    if len(sys.argv)>1 and sys.argv[1]=="only": ids=[int(x) for x in sys.argv[2:]]
    with ThreadPoolExecutor(int(os.environ.get("J","3"))) as ex:
        for k,o in enumerate(ex.map(job,ids)): print(f"{k+1}/{len(ids)} {o}",flush=True)
    if len(ids)<len(pieces): sys.exit(0)
    with open("seg/list.txt","w") as fh:
        for i in range(len(pieces)):
            if edges[i+1]>edges[i]: fh.write(f"file 's{i:04d}.mp4'\n")
    subprocess.run(["ffmpeg","-v","error","-y","-i","master.mp3","-filter_complex",
      f"[0:a]atrim=0:{C0},asetpts=PTS-STARTPTS,afade=t=out:st={C0-0.03}:d=0.03[a];"
      f"[0:a]atrim={C1},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03[b];[a][b]concat=n=2:v=0:a=1[o]",
      "-map","[o]","-ar","48000","-c:a","pcm_s16le","audio_edit.wav"],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","seg/list.txt","-i","audio_edit.wav",
      "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",
      "final/Pain to Power - Elyse Marrone and Danielle Armstrong - multicam.mp4"],check=True)
    print("done")
