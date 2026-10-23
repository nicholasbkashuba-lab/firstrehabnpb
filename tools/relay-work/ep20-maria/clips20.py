# Ep20 vertical clips, cut from the three source files, captioned in the house style:
# one line, max four words, MarginV=75, solid black box, each cue on its first word.
# Shots come from the master's shot list (shots.json), so a Maria shot is only ever used
# while Zoom is actually showing her.
import json, os, re, subprocess, sys
from PIL import ImageFont
SPEC=[("01-how-long-not-want-cancer","mris were not fun",445,"said fair enough",457),
 ("02-one-word","they found something suspicious",469,"anything else after that",492),
 ("03-under-40","i met",932,"always feel it",969),
 ("04-shooting-star","was walking my one dog",1026,"gonna be okay",1045),
 ("05-ringing-the-bell","how did it feel",1332,"believe it's me",1378),
 ("06-too-soon","so dave you'll appreciate",1405,"too soon yeah",1421),
 ("07-not-the-ritz","the chemotherapy though.",684,"wasn't the ritz",719),
 ("08-dr-google","people",1204,"away from dr. google",1231),
 ("09-secretary-and-treasurer","but i was ready sitting",519,"out of me",540),
 ("10-romantic-joke","i was in my",1540,"i love it",1594)]
if len(sys.argv)>1: SPEC=[s for s in SPEC if s[0] in sys.argv[1:]]
W=json.load(open("words.json"))
def norm(x): return x.strip().lower().strip(".,?!")
def find(phrase,near):
    toks=[norm(x) for x in phrase.split()]; best=None
    for i in range(len(W)-len(toks)):
        if [norm(W[i+k]["w"]) for k in range(len(toks))]==toks and (best is None or abs(W[i]["s"]-near)<abs(W[best]["s"]-near)): best=i
    if best is None or abs(W[best]["s"]-near)>15: sys.exit(f"phrase not found: {phrase}")
    return best
SH="unsharp=5:5:0.6:5:5:0"
CAM={"D":("../src/IMG_5519.MP4",lambda t:425.8706-0.0000414*t,f"crop=405:720:490:0,scale=1080:1920:flags=lanczos,{SH}"),
     "M":("../src/IMG_2005.MP4",lambda t:512.4313-0.0000329*t,f"crop=405:720:340:0,scale=1080:1920:flags=lanczos,{SH}"),
     "A":("../src/video1.mp4",lambda t:326.564,f"crop=202:360:219:0,scale=1080:1920:flags=lanczos,{SH}")}
SHOTS=json.load(open("shots.json"))
OVR=json.load(open("clip_overrides.json")) if os.path.exists("clip_overrides.json") else {}
def shots_in(name,s,e):
    if name in OVR: return [[s+a,min(s+b,e),n] for a,b,n in OVR[name]]
    out=[[max(a,s),min(b,e),n] for a,b,n in SHOTS if b>s and a<e]
    res=[]
    for x in out:
        if x[1]-x[0]<1.2 and res: res[-1][1]=x[1]
        else: res.append(x)
    if len(res)>1 and res[0][1]-res[0][0]<1.2: res[1][0]=res[0][0]; res=res[1:]
    return res
# reviewed transcript corrections: word sequences the ASR got wrong, checked against the
# Descript transcript and the audio. Timing is spread across the replacement words.
FIXSEQ=[("i'm gonna go to the bathroom","and won't go to the bathroom"),
        ("putting it up there","putting it out there"),
        ("i'm gonna hear that bell ring","when I hear that bell ring"),
        ("well your little glow","well, you're a little glow."),
        ("he's like too soon yeah","he's like, too soon? I'm like, yeah."),
        ("dr. google","Dr. Google"),
        ("you know me mama this is she she","you know me and my missus, she, she"),
        ("i said, oh, what's going on?","I said, Elmer, what's going on?"),
        ("i watched tv","I watch TV"),
        ("jb","Jabe,"),("attract her","attract her."),("no, i you know what","Oh. You know what?"),
        ("my first day he's like,","my first day. He's like,"),
        ("the in the doctor's office","the doctor's office")]
FIX=[(r"\bPain to Power\b","Pain 2 Power")]
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
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:d}:{m:02d}:{s:05.2f}"
def words_for(i,j):
    ws=[]
    for w in W[i:j+1]:
        tok=w["w"].strip()
        if ws and re.match(r"^[.%'-]",tok): ws[-1]["w"]+=tok; ws[-1]["e"]=w["e"]; continue
        ws.append({"w":tok,"s":w["s"],"e":w["e"]})
    for pat,rep in FIXSEQ:
        p=pat.split(); r=rep.split(); k=0
        while k<=len(ws)-len(p):
            if [x["w"].lower() for x in ws[k:k+len(p)]]==p or [norm(x["w"]) for x in ws[k:k+len(p)]]==[norm(y) for y in p]:
                s0,e0=ws[k]["s"],ws[k+len(p)-1]["e"]; st=(e0-s0)/len(r)
                ws[k:k+len(p)]=[{"w":r[q],"s":s0+q*st,"e":s0+(q+1)*st} for q in range(len(r))]
                k+=len(r)
            else: k+=1
    # ASR capitalises the first word of each of its segments; caption case follows the sentence
    PROPER={"I","Dave","Dave's","Mike","Maria","Roswell","Buffalo","Google","Google.","Dr.","Elmer","Elmer.","Alabama","John","Deere","TV","TV,","MRI","MRIs","Ritz","Ritz.","Facebook","Jay","Jay,","Bills","Sabres","Jabe,"}
    for k,w in enumerate(ws):
        prev=ws[k-1]["w"] if k else "."
        if re.search(r"[.?!]$",prev): w["w"]=w["w"][:1].upper()+w["w"][1:]
        elif w["w"][:1].isupper() and w["w"] not in PROPER and not w["w"].startswith("I'"): w["w"]=w["w"][:1].lower()+w["w"][1:]
    for w in ws:
        for p_,r_ in FIX: w["w"]=re.sub(p_,r_,w["w"])
        w["w"]=re.sub(r'(?<=\w)-(?=\w)',' ',w["w"])
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
        ms=s+edges[k]/FPS; path,off,vf=CAM[nm]; out=f"{wd}/p{k:02d}.mp4"
        c=["ffmpeg","-v","error","-y","-ss",f"{ms+off(ms):.3f}","-i",path,"-an","-vf",f"fps=30,{vf},setsar=1,format=yuv420p",
           "-frames:v",str(nf),"-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out]
        subprocess.run(c,check=True); lst.append((out,nf))
    open(f"{wd}/l.txt","w").write("".join(f"file '{os.path.basename(p)}'\nduration {nf/FPS:.6f}\n" for p,nf in lst))
    C=chunks(words_for(i,j)); cues=[]
    for k,c in enumerate(C):
        a=c[0]["s"]-s; nxt=C[k+1][0]["s"]-s if k+1<len(C) else dur
        b=min(nxt,c[-1]["e"]-s+0.5,dur); txt=" ".join(x["w"] for x in c)
        if k==0: txt=txt[:1].upper()+txt[1:]
        cues.append((max(a,0),max(b,a+0.25),txt))
    for k in range(len(cues)-1):
        if cues[k][1]>cues[k+1][0]: cues[k]=(cues[k][0],cues[k+1][0],cues[k][2])
    open(f"{wd}/cap.ass","w").write(HEAD+"".join(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{x}\n" for a,b,x in cues))
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt","-ss",f"{s:.3f}","-t",f"{dur:.3f}","-i","../src/raw.mp3",
        "-filter_complex",f"[0:v]subtitles={wd}/cap.ass,format=yuv420p[v];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-c:a","aac","-b:a","192k","-movflags","+faststart",
        "-t",f"{dur:.3f}",f"clips/{name}.mp4"],check=True)
    report[name]={"raw":[s,e],"dur":round(dur,1),"shots":[[round(a-s,2),round(b-s,2),n] for a,b,n in sh],"text":" ".join(x for _,_,x in cues)}
    print(name,round(dur,1),"s",report[name]["shots"],flush=True)
    json.dump(report,open(f"clips_report_{'_'.join(sys.argv[1:]) or 'all'}.json","w"),indent=1)
