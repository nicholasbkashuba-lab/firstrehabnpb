# Renders the Ep19 multicam from the three small source files. Zoom guest: her
# 9:16 tile centred over a blurred fill of itself. HOSTS: Dave and Mike side by side.
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
W,H,FPS=1920,1080,30
J=json.load(open("cuts19.json")); shots=J["shots"]; K=J["keep"]
SRC={"DAVE":("raw/IMG_1996.MP4",0.999967,-38.003),"MIKE":("raw/IMG_5504.MOV",0.999957,-35.282),
     "ZOOM":("raw/video1573954541.mp4",0.999974,237.084)}
SH="unsharp=5:5:0.5:5:5:0"
VF={"DAVE":f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos,{SH},setsar=1,format=yuv420p[v]",
    "MIKE":f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos,{SH},setsar=1,format=yuv420p[v]",
    "SHAN":f"[0:v]fps={FPS},crop=202:358:219:1,split[a][b];[a]scale={W}:-2,crop={W}:{H},boxblur=40:4,eq=brightness=-0.12[bg];"
           f"[b]scale=608:{H}:flags=lanczos,{SH}[fg];[bg][fg]overlay=(W-w)/2:0,setsar=1,format=yuv420p[v]",
    "HOSTS":f"[0:v]fps={FPS},crop=640:720:330:0,scale=960:{H}:flags=lanczos[l];[1:v]fps={FPS},crop=320:360:140:0,scale=960:{H}:flags=lanczos[r];"
            f"[l][r]hstack,{SH},setsar=1,format=yuv420p[v]"}
INP={"DAVE":["DAVE"],"MIKE":["MIKE"],"SHAN":["ZOOM"],"HOSTS":["DAVE","MIKE"]}
def r2e(m):
    o=0
    for a,b in K:
        if m<=b: return o+max(m-a,0)
        o+=b-a
    return o
odur=sum(b-a for a,b in K)
edges=[int(round(r2e(s)*FPS)) for s,_,_ in shots]+[int(round(odur*FPS))]
def job(i):
    s,e,ang=shots[i]; nf=edges[i+1]-edges[i]
    if nf<=0: return None
    out=f"seg/s{i:04d}.mp4"
    if os.path.exists(out) and os.path.getsize(out)>1000: return out
    ms=s+(edges[i]/FPS-r2e(s))
    c=["ffmpeg","-v","error","-y","-threads","2"]
    for src in INP[ang]:
        f,r,o=SRC[src]; cs=r*ms+o
        c+=["-ss",f"{cs:.3f}","-i",f]   # accurate seek (ffmpeg decodes from the prior keyframe)
    c+=["-filter_complex",VF[ang],"-map","[v]","-an","-frames:v",str(nf),"-c:v","libx264","-preset","medium","-crf","19",
        "-pix_fmt","yuv420p","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",out+".tmp.mp4"]
    subprocess.run(c,check=True); os.rename(out+".tmp.mp4",out); return out
if __name__=="__main__":
    os.makedirs("seg",exist_ok=True)
    ids=list(range(len(shots)))
    if sys.argv[1:2]==["only"]: ids=[int(x) for x in sys.argv[2:]]
    with ThreadPoolExecutor(int(os.environ.get("J","3"))) as ex:
        for k,o in enumerate(ex.map(job,ids)): print(f"{k+1}/{len(ids)} {o}",flush=True)
    if len(ids)<len(shots): sys.exit(0)
    with open("seg/list.txt","w") as fh:
        for i in range(len(shots)):
            nf=edges[i+1]-edges[i]
            if nf>0: fh.write(f"file 's{i:04d}.mp4'\nduration {nf/FPS:.6f}\n")
    fc="".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={b-a-0.03:.3f}:d=0.03[k{q}];" for q,(a,b) in enumerate(K))
    fc+="".join(f"[k{q}]" for q in range(len(K)))+f"concat=n={len(K)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg","-v","error","-y","-i","master.mp3","-filter_complex",fc,"-map","[o]","-ar","48000","-c:a","pcm_s16le","audio_edit.wav"],check=True)
    os.makedirs("final",exist_ok=True)
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","seg/list.txt","-i","audio_edit.wav",
      "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",
      "final/Pain to Power - Shannon Cake - multicam.mp4"],check=True)
    print("done")
