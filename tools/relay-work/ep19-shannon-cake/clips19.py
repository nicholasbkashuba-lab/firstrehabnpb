# Ep19 vertical clips, cut from the three source files, captioned in the 2026-10-09 house
# style: one line, max four words, MarginV=12, solid black box, each cue on its first word.
import json, os, re, subprocess, sys, numpy as np
from PIL import ImageFont
SPEC=[("01-23-emmys","if you take peter",237,"goosebumps too.",255),
 ("02-check-your-numbers","and so when you",869,"part of business.",892),
 ("03-centcom-at-first-rehab","but when you walk",1385,"walk into first rehab.",1424),
 ("04-workout-first-thing","if you're gonna get",1161,"gets least interrupted.",1175),
 ("05-antenna-joke","so a good friend",1582,"for that one.",1615),
 ("06-one-story","i feel like maybe",637,"many, many years.",661),
 ("07-not-time-priorities","it's not a matter",1305,"than unboxing videos.",1332),
 ("08-never-won-alone","i didn't win anything",309,"i am today.",343),
 ("09-daves-workout","but captain carey does",1500,"doing for him.",1548),
 ("10-go-vote","if you know that",1655,"look at that.",1683)]
if len(sys.argv)>1: SPEC=[s for s in SPEC if s[0] in sys.argv[1:]]
W=json.load(open("words.json"))
def norm(x): return x.strip().lower().strip(".,?!")
def find(phrase,near):
    toks=[norm(x) for x in phrase.split()]; best=None
    for i in range(len(W)-len(toks)):
        if [norm(W[i+k]["w"]) for k in range(len(toks))]==toks and (best is None or abs(W[i]["s"]-near)<abs(W[best]["s"]-near)): best=i
    if best is None: sys.exit(f"phrase not found: {phrase}")
    return best
SRC={"DAVE":("raw/IMG_1996.MP4",0.999967,-38.003),"MIKE":("raw/IMG_5504.MOV",0.999957,-35.282),
     "ZOOM":("raw/video1573954541.mp4",0.999974,237.084)}
SH="unsharp=5:5:0.6:5:5:0"
VF={"DAVE":(["DAVE"],f"[0:v]fps=30,crop=405:720:440:0,scale=1080:1920:flags=lanczos,{SH},setsar=1,format=yuv420p[v]"),
    "MIKE":(["MIKE"],f"[0:v]fps=30,crop=202:360:198:0,scale=1080:1920:flags=lanczos,{SH},setsar=1,format=yuv420p[v]"),
    "SHAN":(["ZOOM"],f"[0:v]fps=30,crop=202:358:219:1,scale=1080:1920:flags=lanczos,{SH},setsar=1,format=yuv420p[v]"),
    "HOSTV":(["DAVE","MIKE"],f"[0:v]fps=30,crop=720:640:290:40,scale=1080:960:flags=lanczos[t];[1:v]fps=30,crop=360:320:140:20,scale=1080:960:flags=lanczos[b];[t][b]vstack,{SH},setsar=1,format=yuv420p[v]")}
d=np.load("spk.npz"); t=d["t"]; names=list(d["names"]); tile=d["tile"]; lab=np.load("vit_lab.npy")
OVR=json.load(open("clip_overrides.json")) if os.path.exists("clip_overrides.json") else {}
def shots_in(name,s,e):
    if name in OVR: return [[s+a,min(s+b,e),n] for a,b,n in OVR[name]]
    m=(t>=s)&(t<=e); tt=t[m]; ll=[("SHAN" if tile[i] else "HOSTV") if names[lab[i]]=="SHANNON" else names[lab[i]] for i in np.where(m)[0]]
    out=[];st=s
    for i in range(1,len(tt)):
        if ll[i]!=ll[i-1]: b=(tt[i-1]+tt[i])/2; out.append([st,b,ll[i-1]]); st=b
    out.append([st,e,ll[-1]])
    res=[]
    for x in out:
        if x[1]-x[0]<1.5 and res: res[-1][1]=x[1]
        else: res.append(x)
    if len(res)>1 and res[0][1]-res[0][0]<1.5: res[1][0]=res[0][0]; res=res[1:]
    m2=[]
    for x in res:
        if m2 and m2[-1][2]==x[2]: m2[-1][1]=x[1]
        else: m2.append(x)
    return m2
# reviewed transcript corrections (also in tools/stage-episode.py NAME_FIXES)
FIX=[(r"\bKishuba\b","Kashuba"),(r"\bKashubon\b","Kashuba"),(r"\bCarey\b","Kerry"),(r"\bCarrie\b","Kerry"),
     (r"\benemies\b","Emmys"),(r"\bEhrenberg\b","Aronberg"),(r"\bWinter\b","Winner"),(r"\bShannon Kay\b","Shannon Cake"),
     (r"\bRhodes\b","roads"),(r"\bPain to Power\b","Pain 2 Power"),(r"(\d) \.(\d)",r"\1:\2"),
     (r"\bhydrox\b","Hydrox"),(r"^track$","tract"),]
FONT=ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",67)
MAXW1=900; MAXWORDS=4
HEAD="""[Script Info]
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,10,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,4,0,0,2,10,10,12,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:d}:{m:02d}:{s:05.2f}"
def words_for(i,j):
    ws=[]
    for w in W[i:j+1]:
        tok=w["w"].strip()
        if ws and re.match(r"^[.%'-]",tok): ws[-1]["w"]+=tok; ws[-1]["e"]=w["e"]; continue
        ws.append({"w":tok,"s":w["s"],"e":w["e"]})
    # two-word mishearings become one word spanning both timings
    MERGE={("spinal","thalamic"):"spinothalamic",("Shannon","Kay"):"Shannon Cake",("Tick","tock."):"TikTok."}
    k=0
    while k<len(ws)-1:
        key=(ws[k]["w"],ws[k+1]["w"])
        if key in MERGE: ws[k]["w"]=MERGE[key]; ws[k]["e"]=ws[k+1]["e"]; del ws[k+1]
        k+=1
    for w in ws:
        for p,r in FIX: w["w"]=re.sub(p,r,w["w"])
    for w in ws: w["w"]=re.sub(r'(?<=\w)-(?=\w)',' ',w["w"])
    return ws
def chunks(ws):
    out=[];cur=[]
    for w in ws:
        trial=" ".join(x["w"] for x in cur+[w])
        if cur and (len(cur)>=MAXWORDS or FONT.getlength(trial)>MAXW1): out.append(cur); cur=[]
        cur.append(w)
        if re.search(r"[.?!]$",w["w"]) or (re.search(r"[,;:]$",w["w"]) and len(cur)>=2): out.append(cur); cur=[]
    if cur: out.append(cur)
    m=[]
    for c in out:
        if m and len(c)==1 and len(m[-1])<MAXWORDS and FONT.getlength(" ".join(x["w"] for x in m[-1]+c))<=MAXW1 and not re.search(r"[.?!]$",m[-1][-1]["w"]): m[-1]=m[-1]+c
        else: m.append(c)
    return m
os.makedirs("clips",exist_ok=True); report={}
for name,pa,na,pb,nb in SPEC:
    i=find(pa,na); j=find(pb,nb)+len(pb.split())-1
    s=round(W[i]["s"]-0.12,2); e=round(W[j]["e"]+0.45,2); dur=e-s
    wd=f"tmp_{name}"; os.makedirs(wd,exist_ok=True)
    sh=shots_in(name,s,e); FPS=30
    edges=[int(round((a-s)*FPS)) for a,_,_ in sh]+[int(round(dur*FPS))]
    lst=[]
    for k,(a,b,nm) in enumerate(sh):
        nf=edges[k+1]-edges[k]
        if nf<=0: continue
        ms=s+edges[k]/FPS; srcs,vf=VF[nm]; out=f"{wd}/p{k:02d}.mp4"
        c=["ffmpeg","-v","error","-y"]
        for sname in srcs:
            f,r,o=SRC[sname]; c+=["-ss",f"{r*ms+o:.3f}","-i",f]
        c+=["-filter_complex",vf,"-map","[v]","-an","-frames:v",str(nf),"-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out]
        subprocess.run(c,check=True); lst.append(out)
    open(f"{wd}/l.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
    C=chunks(words_for(i,j)); cues=[]
    for k,c in enumerate(C):
        a=c[0]["s"]-s; nxt=C[k+1][0]["s"]-s if k+1<len(C) else dur
        b=min(nxt,c[-1]["e"]-s+0.5,dur); txt=" ".join(x["w"] for x in c)
        if k==0: txt=txt[:1].upper()+txt[1:]
        cues.append((max(a,0),max(b,a+0.25),txt))
    for k in range(len(cues)-1):
        if cues[k][1]>cues[k+1][0]: cues[k]=(cues[k][0],cues[k+1][0],cues[k][2])
    open(f"{wd}/cap.ass","w").write(HEAD+"".join(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{x}\n" for a,b,x in cues))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt","-ss",f"{s:.3f}","-t",f"{dur:.3f}","-i","master.mp3",
        "-filter_complex",f"[0:v]subtitles={wd}/cap.ass,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","192k","-movflags","+faststart",
        "-t",f"{dur:.3f}",f"clips/{name}.mp4"],check=True)
    report[name]={"raw":[s,e],"dur":round(dur,1),"shots":[[round(a-s,2),round(b-s,2),n] for a,b,n in sh],"text":" ".join(x for _,_,x in cues)}
    print(name,round(dur,1),"s",report[name]["shots"],flush=True)
    json.dump(report,open(f"clips_report_{'_'.join(sys.argv[1:]) or 'all'}.json","w"),indent=1)
