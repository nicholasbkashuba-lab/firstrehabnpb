import json, os, re, subprocess, sys, numpy as np
from PIL import ImageFont
SPEC=[("01-eve-gentry","joe actually had",1110,"take you.",1173),
 ("02-healthy-healthy-dead","so i say i",304,"hydration and community.",326),
 ("03-thirty-percent","but 30",663,"gets damaged.",696),
 ("04-lolita-juno-beach","when i moved to",1077,"amazing lady.",1103),
 ("05-immune-system-gut","we all get cancer",789,"events to occur.",812),
 ("06-pilates-through-treatment","i found this year",527,"through their process.",554),
 ("07-joseph-pilates-was-real","so a lot of",991,"was not well.",1044),
 ("08-brussels-sprouts","the brussels sprouts are good",849,"pounds of brussels sprouts.",877),
 ("09-when-does-cancer-occur","well when does",1395,"put it for both of us.",1414),
 ("10-blue-light-glasses","one thing that's really",1512,"fall asleep deeper.",1526)]
if len(sys.argv)>1: SPEC=[s for s in SPEC if s[0] in sys.argv[1:]]
W=json.load(open('words.json'))
def find(phrase,near):
    toks=[x.strip('.,?!') for x in phrase.lower().replace(',','').split()]; best=None
    for i in range(len(W)-len(toks)):
        if [W[i+k]['w'].strip().lower().strip('.,?!') for k in range(len(toks))]==toks and (best is None or abs(W[i]['s']-near)<abs(W[best]['s']-near)): best=i
    return best
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
# vertical crops in 4K source pixels
ANG={"DAVE":("dave.mov",0.999971,195.143,False,f"crop=1215:2160:{1850-607}:0,scale=1080:1920:flags=lanczos,{TM}"),
     "MIKE":("Mike.mov",0.999973,212.981,True,f"crop=1215:2160:{1960-607}:0,scale=1080:1920:flags=lanczos,format=yuv420p"),
     "ELYSE":("IMG_5434.MOV",0.999960,186.044,True,f"crop=1215:2160:{1600-607}:0,scale=1080:1920:flags=lanczos,{TM}"),
     "DANI":("IMG_5434.MOV",0.999960,186.044,True,f"crop=810:1440:{2370-405}:383,scale=1080:1920:flags=lanczos,{TM}")}
d=np.load("spk_emb.npz"); t=d["t"]; names=list(d["names"]); lab=np.load("vit_lab.npy")
OVR=json.load(open("clip_overrides.json")) if os.path.exists("clip_overrides.json") else {}
def shots_in(name,s,e):
    if name in OVR: return [[s+a,min(s+b,e),n] for a,b,n in OVR[name]]
    m=(t>=s)&(t<=e); tt=t[m]; ll=lab[m]; out=[]; st=s
    for i in range(1,len(tt)):
        if ll[i]!=ll[i-1]: b=(tt[i-1]+tt[i])/2; out.append([st,b,names[ll[i-1]]]); st=b
    out.append([st,e,names[ll[-1]]])
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
FIX=[(r"\bPain to Power\b","Pain 2 Power"),(r"\bchoriferous\b","cruciferous"),(r"\bElise\b","Elyse"),
     (r"^Munch$","Munch"),(r"\bo 'clock\b","o'clock"),(r"(\d) %","\\1%"),(r"\bpost-menopausal\b","postmenopausal"),
     (r"\bOmega -3\b","Omega 3")]
FONT=ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",67)  # FontSize 10 @ PlayResY 288 -> 1920px
MAXW=860
def cues(s,e,i0,i1,DROP=()):
    ws=[]
    for w in W[i0:i1+1]:
        tok=w["w"].strip()
        if ws and re.match(r"^[.%'-]",tok): ws[-1]["w"]+=tok; ws[-1]["e"]=w["e"]; continue
        ws.append({"w":tok,"s":max(w["s"],s),"e":min(w["e"],e)})
    def wrap(words):
        toks=" ".join(x["w"] for x in words).split()
        full=" ".join(toks)
        if FONT.getlength(full)<=MAXW: return [full]
        best=None
        for k in range(1,len(toks)):
            a=" ".join(toks[:k]); b=" ".join(toks[k:]); m=max(FONT.getlength(a),FONT.getlength(b))
            if best is None or m<best[0]: best=(m,[a,b])
        if best and best[0]<=MAXW: return best[1]
        return [full,"",""]  # does not fit in two lines
    k=0
    while k<len(ws)-2:
        if [x["w"] for x in ws[k:k+2]]==["Munch","and"] and ws[k+2]["w"].startswith("Gladbach"):
            ws[k]["w"]="Mönchengladbach"+ws[k+2]["w"][8:]; ws[k]["e"]=ws[k+2]["e"]; del ws[k+1:k+3]
        k+=1
    ws=[w for w in ws if not any(a<=w["s"]<b for a,b in DROP)]
    sents=[];cur=[]
    for w in ws:
        cur.append(w)
        if re.search(r"[.?!]$",w["w"]): sents.append(cur); cur=[]
    if cur: sents.append(cur)
    out=[]
    for sn in sents:
        n=1
        while True:
            k=len(sn); size=-(-k//n); parts=[sn[j:j+size] for j in range(0,k,size)]
            if all(len(wrap(p))<=2 for p in parts): break
            n+=1
        out+=parts
    # merge tiny sentences (<=3 words) into the next cue when it still fits
    m=[]
    for c in out:
        if m and len(m[-1])<=2 and len(wrap(m[-1]+c))<=2: m[-1]=m[-1]+c
        else: m.append(c)
    res=[]
    for i,c in enumerate(m):
        a=c[0]["s"]-s; b=(m[i+1][0]["s"]-s) if i+1<len(m) else (e-s)
        b=min(b,c[-1]["e"]-s+0.7)
        for w in c:
            for p_,r_ in FIX: w["w"]=re.sub(p_,r_,w["w"])
        txt="\\N".join(wrap(c))
        txt=re.sub(r'(?<=\w)-(?=\w)',' ',txt)
        res.append((max(a,0),max(b,a+0.3),txt))
    if res: res[0]=(res[0][0],res[0][1],res[0][2][:1].upper()+res[0][2][1:])
    for i in range(len(res)-1):
        if res[i][1]>res[i+1][0]: res[i]=(res[i][0],res[i+1][0],res[i][2])
    return res
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:d}:{m:02d}:{s:05.2f}"
ASS_HEAD="""[Script Info]
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,10,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,4,0,0,2,10,10,35,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
os.makedirs("clips",exist_ok=True); report={}
EXCISE={"07-joseph-pilates-was-real":[("he was a soldier",1003,"in the isle",1008)]}
for name,pa,na,pb,nb in SPEC:
    i=find(pa,na); j=find(pb,nb); j+=len(pb.split())-1
    s=round(W[i]["s"]-0.12,2); e=round(W[j]["e"]+0.45,2)
    DROP=[]
    for xa,xna,xb,xnb in EXCISE.get(name,[]):
        DROP.append((round(W[find(xa,xna)]["s"]-0.05,2), round(W[find(xb,xnb)]["s"]-0.08,2)))
    def o(m):  # master -> clip output time
        return m-s-sum(min(max(m-a,0),b-a) for a,b in DROP)
    keep=[];cur=s
    for a,b in DROP: keep.append((cur,a)); cur=b
    keep.append((cur,e)); dur=sum(b-a for a,b in keep)
    wd=f"tmp_{name}"; os.makedirs(wd,exist_ok=True)
    sh=shots_in(name,s,e)
    pieces=[]
    for a,b,nm in sh:
        for ka,kb in keep:
            x,y=max(a,ka),min(b,kb)
            if y-x>0.01: pieces.append((x,y,nm))
    report[name]={"master":[s,e],"drop":DROP,"shots":[[round(o(a),2),round(o(b),2),n] for a,b,n in pieces]}
    print(name, round(dur,1),"s", report[name]["shots"], DROP, flush=True)
    FPS=30; edges=[int(round(o(x[0])*FPS)) for x in pieces]+[int(round(dur*FPS))]
    lst=[]
    for k,(a,b,nm) in enumerate(pieces):
        nf=edges[k+1]-edges[k]
        if nf<=0: continue
        f,r,oo,skip,vf=ANG[nm]; ms=a+(edges[k]/FPS-o(a)); cs=r*ms+oo; pre=max(cs-4,0)
        out=f"{wd}/p{k:02d}.mp4"
        subprocess.run(["ffmpeg","-v","error","-y"]+(["-skip_frame","noref"] if skip else [])+["-ss",f"{pre:.3f}","-i",f,"-ss",f"{cs-pre:.3f}",
            "-vf",f"fps=30,{vf},setsar=1","-an","-frames:v",str(nf),"-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out],check=True)
        lst.append(out)
    open(f"{wd}/l.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
    C=[(o(s+a) if True else a, o(s+b), t_) for a,b,t_ in cues(s,e,i,j,DROP)]
    report[name]["captions"]=[c[2].replace("\\N"," ") for c in C]
    open(f"{wd}/cap.ass","w").write(ASS_HEAD+"".join(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{txt}\n" for a,b,txt in C))
    af="".join(f"[1:a]atrim={a-s:.3f}:{b-s:.3f},asetpts=PTS-STARTPTS[k{q}];" for q,(a,b) in enumerate(keep))
    af+="".join(f"[k{q}]" for q in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1[cat];"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt","-ss",f"{s:.3f}","-t",f"{e-s:.3f}","-i","master.mp3",
        "-filter_complex",f"[0:v]subtitles={wd}/cap.ass,format=yuv420p[v];{af}"
        f"[cat]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
        "-c:a","aac","-b:a","192k","-movflags","+faststart","-t",f"{dur:.3f}",f"clips/{name}.mp4"],check=True)
    print("  ->",name,os.path.getsize(f"clips/{name}.mp4")//1024,"KB",flush=True)
    json.dump(report,open(f"clips_report_{'_'.join(sys.argv[1:]) or 'all'}.json","w"),indent=1)
