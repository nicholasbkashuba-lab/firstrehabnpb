import json, os, subprocess, sys, numpy as np
from concurrent.futures import ThreadPoolExecutor
W,H,FPS=1920,1080,30
J=json.load(open("cuts16.json")); shots=J["shots"]; C0,C1=J["cut"]
WA=np.array(json.load(open("warp.json"))["anchors"])
def ref_time(m):
    if m<WA[0,0]: return WA[0,1]+(m-WA[0,0])
    if m>WA[-1,0]: return WA[-1,1]+(m-WA[-1,0])*0.99997
    return float(np.interp(m,WA[:,0],WA[:,1]))
CAM={"GUEST":("cam_main.mov",0.0),"DAVE":("IMG_1918.MP4",13.94),"MIKE":("IMG_4077.MP4",4.76)}
MDUR=1646.109; GAP=C1-C0
def m2o(m): return m if m<=C0 else m-GAP          # master -> output time
# pieces in master time, excluding the outtake
pieces=[]
for s,e,nm in shots:
    for a,b in ((s,min(e,C0)),(max(s,C1),e)):
        if b-a>0.01: pieces.append((a,b,nm))
odur=m2o(MDUR)
edges=[int(round(m2o(p[0])*FPS)) for p in pieces]+[int(round(odur*FPS))]
def vf(nm,lr):
    if nm=="MIKE":
        return (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:3,eq=brightness=-0.08[bg];"
                f"[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0,setsar=1,setpts=PTS/{lr:.6f},fps={FPS}")
    return f"scale={W}:{H}:flags=lanczos,setsar=1,setpts=PTS/{lr:.6f},fps={FPS}"
os.makedirs("seg",exist_ok=True)
def job(i):
    a,b,nm=pieces[i]; nf=edges[i+1]-edges[i]
    if nf<=0: return None
    out=f"seg/s{i:04d}.mp4"
    if os.path.exists(out) and os.path.getsize(out)>1000: return out
    # output frame grid -> master time (inside one piece output time is linear in master time)
    ms=a+(edges[i]/FPS-m2o(a)); me=ms+nf/FPS
    r0,r1=ref_time(ms),ref_time(me); lr=(r1-r0)/(me-ms)
    f,off=CAM[nm]; cs=r0+off; pre=max(cs-5,0)
    cmd=["ffmpeg","-v","error","-y","-ss",f"{pre:.3f}","-i",f,"-ss",f"{cs-pre:.3f}","-t",f"{(r1-r0)+0.5:.3f}",
         "-filter_complex" if nm=="MIKE" else "-vf",vf(nm,lr),"-an","-frames:v",str(nf),
         "-c:v","libx264","-preset","medium","-crf","20","-threads","2","-pix_fmt","yuv420p",
         "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",out]
    subprocess.run(cmd,check=True)
    return out
LIM=int(os.environ.get("LIM","0")) or len(pieces)
with ThreadPoolExecutor(3) as ex:
    outs=[]
    for k,o in enumerate(ex.map(job,range(LIM))):
        outs.append(o); print(f"{k+1}/{len(pieces)}",flush=True)
if LIM<len(pieces): sys.exit(0)
with open("seg/list.txt","w") as fh:
    for o in outs:
        if o: fh.write(f"file '{os.path.basename(o)}'\n")
# edited audio: cut the outtake with 30ms fades at the join
subprocess.run(["ffmpeg","-v","error","-y","-i","master.mp3","-filter_complex",
  f"[0:a]atrim=0:{C0},asetpts=PTS-STARTPTS,afade=t=out:st={C0-0.03}:d=0.03[a];"
  f"[0:a]atrim={C1},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03[b];[a][b]concat=n=2:v=0:a=1[o]",
  "-map","[o]","-c:a","pcm_s16le","audio_edit.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","seg/list.txt","-i","audio_edit.wav",
  "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",
  "../Pain to Power - Don Goodwin - multicam.mp4"],check=True)
print("done")
