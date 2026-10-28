# Episode 21 vertical clips from the RAW cameras, house caption style: one line, at most four
# words, MarginV=75, solid black box, each cue on its first word's own time.
# SPEC: (name, start phrase, near, end phrase, near, [excise (from phrase, near, to phrase, near)])
# An excise removes from the first word of `from` up to (not including) the first word of `to`.
import json, os, re, subprocess, sys
from PIL import ImageFont
SPEC=[("01-put-the-mri-down","when a patient comes in with an mri",1077,"it's all rehabable",1110,[]),
 ("02-surgery-wont-fix-it","i'm seeing complicated patients who",865,"before they do the surgery",888,[]),
 ("03-autoclaved-needles","the original needles were autoclaved",477,"they're microphones essentially",503,[]),
 ("04-neurologist-turned-patient","but i had a lot of pain",323,"and now i'm asymptomatic",357,[]),
 ("05-god-is-not-a-surgeon","a good therapist knows what",759,"that's really good",777,[]),
 ("06-hand-in-water","and i started back in 87",188,"it wouldn't shrivel there",207,[]),
 ("07-not-als","we had somebody that we knew",643,"he was planning everything",680,
      [("and kennedy's disease is only in",658,"and because of his diagnosis",668)]),
 ("08-the-kneeler","and my mother's charcot",1322,"it was a starting point",1349,[]),
 ("09-put-the-prescription-down","so when i see a patient",595,"adequate history and physical",625,[]),
 ("10-i-was-the-mri","in 1987 there was no mris",916,"do i need to do surgery",950,[])]
if len(sys.argv)>1: SPEC=[s for s in SPEC if s[0] in sys.argv[1:]]
W=json.load(open("words.json"))
def norm(x): return x.strip().lower().strip(".,?!").replace(" ","")
def find(phrase,near):
    toks=[norm(x) for x in phrase.split()]; best=None
    for i in range(len(W)-len(toks)):
        if [norm(W[i+k]["w"]) for k in range(len(toks))]==toks and (best is None or abs(W[i]["s"]-near)<abs(W[best]["s"]-near)): best=i
    if best is None or abs(W[best]["s"]-near)>15: sys.exit(f"phrase not found: {phrase}")
    return best
SH="unsharp=5:5:0.6:5:5:0"
import cv2, numpy as np
_DET={}
def _det(w,h):
    if (w,h) not in _DET: _DET[(w,h)]=cv2.FaceDetectorYN.create("/root/sizzle-work/models/yunet.onnx","",(w,h),0.6)
    return _DET[(w,h)]
SRCW={"D":1280,"G":1280,"M":3840}
DEFX={"D":709,"G":543,"M":2126}
def face_track(cam,cam_t0,dur):
    """Face centre x (source px) every 0.125 s through the piece, decoded once at 640 wide,
    filled and smoothed over 1.25 s so the crop follows the person without jitter."""
    path=CAM[cam][0]; W=SRCW[cam]; h=360; fb=640*h*3
    p=subprocess.run(["ffmpeg","-v","error","-ss",f"{cam_t0:.3f}","-i",path,"-t",f"{dur+0.3:.3f}","-vf","fps=8,scale=640:360",
                      "-f","rawvideo","-pix_fmt","bgr24","-"],capture_output=True)
    xs=[]
    for i in range(len(p.stdout)//fb):
        fr=np.frombuffer(p.stdout[i*fb:(i+1)*fb],np.uint8).reshape(h,640,3)
        _,f=_det(640,h).detect(fr)
        if f is None: xs.append(None); continue
        bb=max(f,key=lambda x:x[2]*x[3]); xs.append(float((bb[0]+bb[2]/2)*W/640))
    good=[x for x in xs if x is not None]
    if not good: return [(0.0,float(DEFX[cam]))]
    last=good[0]; fill=[]
    for x in xs:
        last=x if x is not None else last; fill.append(last)
    a=np.array(fill); k=3
    sm=np.convolve(np.pad(a,(k//2,k//2),mode="edge"),np.ones(k)/k,mode="valid")
    return [(i/8,float(v)) for i,v in enumerate(sm)]
_NCMD=[0]
def x_cmds(track,cw,W,nf):
    """Per frame crop x, linearly interpolated from the face track and clamped to the frame,
    written as a sendcmd file (an inline expression this long overflows ffmpeg's parser)."""
    ts=np.array([t for t,_ in track]); xs=np.array([min(max(cx-cw/2,0),W-cw) for _,cx in track])
    _NCMD[0]+=1; path=f"/tmp/claude-0/cmd_{os.getpid()}_{_NCMD[0]}.txt"
    with open(path,"w") as f:
        for k in range(nf+2):
            f.write(f"{k/30:.4f} crop@c x {int(round(np.interp(k/30,ts,xs)))};\n")
    return path,int(round(xs[0]))
def vf_for(cam,cam_t0,dur):
    tr=face_track(cam,cam_t0,dur); nf=int(round(dur*30))
    cw,W,tail=(1215,3840,"scale=1080:1920:flags=lanczos") if cam=="M" else (405,1280,f"scale=1080:1920:flags=lanczos,{SH}")
    cf,x0=x_cmds(tr,cw,W,nf); ch=2160 if cam=="M" else 720
    return f"sendcmd=f={cf},crop@c={cw}:{ch}:{x0}:0,{tail}"
CAM={"D":("src/IMG_2010.MP4",lambda t:107.8726-0.0000318*t),
     "G":("src/IMG_5523.MP4",lambda t:94.5896-0.0000410*t),
     "M":("main.mov",lambda t:90.2318-0.0000275*t)}
SHOTS=json.load(open("shots.json"))["shots"]
OVR=json.load(open("clip_overrides.json")) if os.path.exists("clip_overrides.json") else {}
def shots_in(s,e):
    out=[[max(a,s),min(b,e),n] for a,b,n in SHOTS if b>s and a<e]
    res=[]
    for x in out:
        if x[1]-x[0]<1.2 and res: res[-1][1]=x[1]
        else: res.append(x)
    if len(res)>1 and res[0][1]-res[0][0]<1.2: res[1][0]=res[0][0]; res=res[1:]
    return res
FIXSEQ=[("dropped my wife nuts","drove my wife nuts"),("you work with me","your work with me"),
        ("pain to power","Pain 2 Power"),("charcot","Charcot"),("charcot,","Charcot,"),
        ("87.","'87."),("mris,","MRIs,"),("mri","MRI"),("mri,","MRI,"),("mri?","MRI?"),("mri.","MRI."),
        ("reed,","Reed,"),("dr.","Dr."),("i'm like, reed,","I'm like, Reed,")]
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
Style: Default,Arial,10,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,4,0,0,2,10,10,75,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
PROPER={"I","I'm","I've","I'll","Dave","Dave's","Mike","Reed","Reed,","Stone","Stone,","Dr.","MRI","MRI,","MRI?","MRI.","MRIs,","ALS.","ALS","ALS?","Kennedy's","Charcot","Charcot,","God","God,","Zander","Ireland,","Brooklyn","Palm","Beach"}
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:d}:{m:02d}:{s:05.2f}"
def words_for(idx):
    ws=[]
    for i in idx:
        w=W[i]; tok=w["w"].strip()
        if ws and re.match(r"^[.%'-]",tok): ws[-1]["w"]+=tok; ws[-1]["e"]=w["e"]; continue
        ws.append({"w":tok,"s":w["s"],"e":w["e"]})
    for pat,rep in FIXSEQ:
        p=pat.split(); r=rep.split(); k=0
        while k<=len(ws)-len(p):
            if [x["w"].lower() for x in ws[k:k+len(p)]]==p:
                s0,e0=ws[k]["s"],ws[k+len(p)-1]["e"]; st=(e0-s0)/len(r)
                ws[k:k+len(p)]=[{"w":r[q],"s":s0+q*st,"e":s0+(q+1)*st} for q in range(len(r))]; k+=len(r)
            else: k+=1
    for k,w in enumerate(ws):
        prev=ws[k-1]["w"] if k else "."
        if re.search(r"[.?!]$",prev): w["w"]=w["w"][:1].upper()+w["w"][1:]
        elif w["w"][:1].isupper() and w["w"] not in PROPER and not w["w"].startswith("I'"): w["w"]=w["w"][:1].lower()+w["w"][1:]
        w["w"]=re.sub(r'(?<=\w)-(?=\w)',' ',w["w"]).replace(" -"," ")
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
FPS=30
for name,pa,na,pb,nb,exc in SPEC:
    i=find(pa,na); j=find(pb,nb)+len(pb.split())-1
    s=round(W[i]["s"]-0.12,2); e=round(W[j]["e"]+0.45,2)
    # keep segments in master time
    keep=[[s,e]]; drop_idx=set()
    for fa,fna,ta,tna in exc:
        x=find(fa,fna); y=find(ta,tna)
        cs=round(W[x]["s"]-0.06,2); ce=round(W[y]["s"]-0.10,2)
        drop_idx.update(range(x,y))
        nk=[]
        for a,b in keep:
            if ce<=a or cs>=b: nk.append([a,b])
            else:
                if cs>a: nk.append([a,cs])
                if ce<b: nk.append([ce,b])
        keep=nk
    # snap keep boundaries to whole frames of output time
    seglen=[round((b-a)*FPS) for a,b in keep]; dur=sum(seglen)/FPS
    wd=f"tmp_{name}"; os.makedirs(wd,exist_ok=True)
    lst=[]; amaps=[]; tout=0.0; pk=0; shots_rep=[]
    for (a,b),nfs in zip(keep,seglen):
        b=a+nfs/FPS
        sh=OVR.get(name) and [[a+x,min(a+y,b),n] for x,y,n in OVR[name] if a+x<b] or shots_in(a,b)
        edges=[int(round((x-a)*FPS)) for x,_,_ in sh]+[nfs]
        for k,(x,y,nm) in enumerate(sh):
            nf=edges[k+1]-edges[k]
            if nf<=0: continue
            ms=a+edges[k]/FPS; path,off=CAM[nm]; out=f"{wd}/p{pk:02d}.mp4"; pk+=1
            c=["ffmpeg","-v","error","-y","-ss",f"{ms+off(ms):.3f}","-i",path,"-an","-vf",f"fps=30,{vf_for(nm,ms+off(ms),nf/FPS)},setsar=1,format=yuv420p",
               "-frames:v",str(nf),"-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out]
            subprocess.run(c,check=True); lst.append((out,nf)); shots_rep.append([round(tout+(ms-a),2),nm])
        amaps.append((a,b,tout)); tout+=nfs/FPS
    open(f"{wd}/l.txt","w").write("".join(f"file '{os.path.basename(p)}'\nduration {nf/FPS:.6f}\n" for p,nf in lst))
    def m2o(t):
        for a,b,o in amaps:
            if a-0.05<=t<=b+0.05: return o+(t-a)
        return None
    idx=[k for k in range(i,j+1) if k not in drop_idx]
    ws=[w for w in words_for(idx) if m2o(w["s"]) is not None]
    for w in ws:
        so=m2o(w["s"]); eo=m2o(w["e"]); w["s"]=so; w["e"]=eo if eo is not None else so+0.2
    C=chunks(ws); cues=[]
    for k,c in enumerate(C):
        a=c[0]["s"]; nxt=C[k+1][0]["s"] if k+1<len(C) else dur
        b=min(nxt,c[-1]["e"]+0.5,dur); txt=" ".join(x["w"] for x in c)
        if k==0: txt=txt[:1].upper()+txt[1:]
        cues.append((max(a,0),max(b,a+0.25),txt))
    for k in range(len(cues)-1):
        if cues[k][1]>cues[k+1][0]: cues[k]=(cues[k][0],cues[k+1][0],cues[k][2])
    open(f"{wd}/cap.ass","w").write(HEAD+"".join(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{x}\n" for a,b,x in cues))
    # audio: each keep segment from the RAW mp3, 15 ms fades at the joins, then loudness
    ain=[]; fl=[]
    for q,(a,b,o) in enumerate(amaps):
        ain+=["-ss",f"{a:.3f}","-t",f"{b-a:.3f}","-i","src/raw.mp3"]
        fl.append(f"[{q+1}:a]afade=t=in:d=0.015,afade=t=out:st={max(0,b-a-0.015):.3f}:d=0.015[a{q}]")
    fc=";".join(fl)+";"+"".join(f"[a{q}]" for q in range(len(amaps)))+f"concat=n={len(amaps)}:v=0:a=1[ac];[ac]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a];[0:v]subtitles={wd}/cap.ass,format=yuv420p[v]"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt",*ain,"-filter_complex",fc,
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","192k","-movflags","+faststart",
        "-t",f"{dur:.3f}",f"clips/{name}.mp4"],check=True)
    report[name]={"keep":keep,"dur":round(dur,1),"shots":shots_rep,"text":" ".join(x for _,_,x in cues)}
    print(name,round(dur,1),"s",shots_rep,flush=True)
    rp="clips_report.json"; R=json.load(open(rp)) if os.path.exists(rp) else {}; R.update({name:report[name]}); json.dump(R,open(rp,"w"),indent=1)
