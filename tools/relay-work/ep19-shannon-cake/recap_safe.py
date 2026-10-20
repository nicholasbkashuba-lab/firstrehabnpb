# Re-mux Ep19 clips from cached pieces with captions moved into the platform safe zone.
# Usage (in the ep19 work folder): python3 recap_safe.py 75 <clip names...>  -> clips_safe/<name>.mp4
import json,re,subprocess,sys
MV=int(sys.argv[1]); names=sys.argv[2:]; out=sys.argv[0] and "clips_safe"
import os; os.makedirs("clips_safe",exist_ok=True)
rep=json.load(open("clips_report_all.json")); rep.update(json.load(open("clips_report_10-go-vote.json")))
for n in names:
    s,e=rep[n]["raw"]; dur=e-s; wd=f"tmp_{n}"
    a=open(f"{wd}/cap.ass").read()
    a=re.sub(r"(Style: Default,.*?,2,10,10,)\d+(,1)",rf"\g<1>{MV}\2",a); open(f"{wd}/cap_safe.ass","w").write(a)
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt","-ss",f"{s:.3f}","-t",f"{dur:.3f}","-i","master.mp3",
        "-filter_complex",f"[0:v]subtitles={wd}/cap_safe.ass,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","192k","-movflags","+faststart",
        "-t",f"{dur:.3f}",f"clips_safe/{n}.mp4"],check=True)
    print(n,"ok",flush=True)
