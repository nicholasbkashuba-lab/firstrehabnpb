import json, os, re, subprocess, sys, numpy as np, cv2
SPEC=[
 ("01-radiation-dose", 419.3, 449.8),
 ("02-dense-breasts", 512.9, 537.3),
 ("03-brca-mri", 553.0, 600.3),
 ("04-start-at-40", 334.9, 376.7),
 ("05-men-get-it-too", 1228.0, 1278.5),
 ("06-benign-surgeries", 849.6, 894.0),
 ("07-stage-one", 1145.2, 1179.3),
 ("08-dad-joke", 1492.6, 1527.6),
 ("09-callback-rates", 800.9, 833.4),
]
if len(sys.argv)>1: SPEC=[s for s in SPEC if s[0] in sys.argv[1:]]
WA=np.array(json.load(open("warp.json"))["anchors"])
ref=lambda m: float(np.interp(m,WA[:,0],WA[:,1]))
CAM={"GUEST":("cam_main.mov",0.0),"DAVE":("IMG_1918.MP4",13.94),"MIKE":("IMG_4077.MP4",4.76)}
# speaker labels (same fused evidence as the full episode, no reaction cuts)
d=np.load("spk_emb.npz"); t=d["t"]; S=d["S"]; names=list(d["names"]); rms=d["rms"]; EL=np.load("energy_lab.npy")
z=lambda a:(a-a.mean(0))/(a.std(0)+1e-9); F=z(S)+0.6*z(EL); F[rms<np.percentile(rms,15)]=0
n=len(t); dp=np.zeros((n,3)); bp=np.zeros((n,3),int); dp[0]=F[0]
for i in range(1,n):
    for k in range(3):
        c=dp[i-1]-2.0*(np.arange(3)!=k); bp[i,k]=c.argmax(); dp[i,k]=c.max()+F[i,k]
lab=np.zeros(n,int); lab[-1]=dp[-1].argmax()
for i in range(n-1,0,-1): lab[i-1]=bp[i,lab[i]]
A=json.load(open("../asr_master.json")); WORDS=[w for s in A for w in s["words"]]
FIX=[(r"\bPain to Power\b","Pain 2 Power"),(r"\bTyler Maine\b","Tyler Mane")]
casc=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
def frame(f,ts):
    p=subprocess.run(["ffmpeg","-v","error","-ss",f"{ts:.2f}","-i",f,"-frames:v","1","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(p,np.uint8),cv2.IMREAD_COLOR)
def face_cx(nm,ms,me):
    f,off=CAM[nm]; xs=[];wid=None
    for m in np.linspace(ms,me,6):
        im=frame(f,ref(m)+off); wid=im.shape[1]
        g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        fs=casc.detectMultiScale(g,1.1,5,minSize=(im.shape[0]//8,im.shape[0]//8))
        if len(fs): x,y,w,h=max(fs,key=lambda r:r[2]*r[3]); xs.append(x+w/2)
    return (float(np.median(xs)) if xs else wid/2), wid, len(xs)
OVR={1492.6:[[1492.6,1510.6,'DAVE'],[1510.6,1514.0,'GUEST'],[1514.0,1521.5,'MIKE'],[1521.5,1525.0,'DAVE'],[1525.0,1527.6,'MIKE']]}
def shots_in(s,e):
    if s in OVR: return OVR[s]
    m=(t>=s)&(t<=e); tt=t[m]; ll=lab[m]; out=[]; st=s
    for i in range(1,len(tt)):
        if ll[i]!=ll[i-1]: b=(tt[i-1]+tt[i])/2; out.append([st,b,names[ll[i-1]]]); st=b
    out.append([st,e,names[ll[-1]] if len(ll) else "GUEST"])
    # absorb shots under 1.5s
    res=[]
    for x in out:
        if x[1]-x[0]<1.5 and res: res[-1][1]=x[1]
        else: res.append(x)
    if len(res)>1 and res[0][1]-res[0][0]<1.5: res[1][0]=res[0][0]; res=res[1:]
    m2=[]
    for x in res:
        if m2 and m2[-1][2]==x[2]: m2[-1][1]=x[1]
        else: m2.append(x)
    if s==1145.2 and m2[-1][2]=='MIKE' and m2[-1][0]>=1176: m2[-2][1]=m2[-1][1]; m2=m2[:-1]
    return m2
def cues(s,e):
    ws=[]
    for w in WORDS:
        if w["s"]>=s-0.05 and w["s"]<e:
            tok=w["w"].strip()
            if ws and re.match(r"^[.%-]",tok): ws[-1]["w"]+=tok; ws[-1]["e"]=w["e"]; continue
            ws.append({"w":tok,"s":max(w["s"],s),"e":min(w["e"],e)})
    out=[];cur=[]
    for w in ws:
        cur.append(w); txt=" ".join(x["w"] for x in cur)
        if len(txt)>=26 or re.search(r"[.?!,]$",w["w"]) and len(txt)>12:
            out.append(cur); cur=[]
    if cur: out.append(cur)
    res=[]
    for i,c in enumerate(out):
        a=c[0]["s"]-s; b=(out[i+1][0]["s"]-s) if i+1<len(out) else (e-s)
        b=min(b,c[-1]["e"]-s+0.6); txt=" ".join(x["w"] for x in c)
        for p,r in FIX: txt=re.sub(p,r,txt)
        txt=re.sub(r'(?<=\w)-(?=\w)',' ',txt)
        res.append((max(a,0),max(b,a+0.3),txt))
    for i in range(len(res)-1):
        if res[i][1]>res[i+1][0]: res[i]=(res[i][0],res[i+1][0],res[i][2])
    return res
def ts(x): h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
STYLE="FontName=Arial,FontSize=10,PrimaryColour=&H00FFFFFF,BackColour=&H00000000,BorderStyle=4,Outline=0,Shadow=0,Bold=1,Alignment=2,MarginV=35"
for name,s,e in SPEC:
    wd=f"tmp_{name}"; os.makedirs(wd,exist_ok=True)
    sh=shots_in(s,e); cx={}
    for nm in set(x[2] for x in sh):
        rs=[x for x in sh if x[2]==nm]; cx[nm]=face_cx(nm,rs[0][0]+0.3,rs[-1][1]-0.3)
    print(name, [(round(a,1),round(b,1),c) for a,b,c in sh], {k:(round(v[0]),v[2]) for k,v in cx.items()})
    FPS=30; edges=[int(round((x[0]-s)*FPS)) for x in sh]+[int(round((e-s)*FPS))]
    lst=[]
    for i,(a,b,nm) in enumerate(sh):
        nf=edges[i+1]-edges[i]
        if nf<=0: continue
        f,off=CAM[nm]; ms=s+edges[i]/FPS; cs=ref(ms)+off
        if nm=="MIKE": vf="scale=1080:1920:flags=lanczos,setsar=1"
        else:
            c,wid,_=cx[nm]; H_=1080 if nm=="GUEST" else 720; cw=int(H_*9/16)//2*2
            x0=int(min(max(c-cw/2,0),wid-cw))
            vf=f"crop={cw}:{H_}:{x0}:0,scale=1080:1920:flags=lanczos,setsar=1"
        out=f"{wd}/p{i:02d}.mp4"; pre=max(cs-3,0)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{pre:.3f}","-i",f,"-ss",f"{cs-pre:.3f}","-vf",vf+",fps=30","-an",
            "-frames:v",str(nf),"-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",out],check=True)
        lst.append(out)
    open(f"{wd}/l.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in lst))
    srt="".join(f"{i+1}\n{ts(a)} --> {ts(b)}\n{txt}\n\n" for i,(a,b,txt) in enumerate(cues(s,e)))
    open(f"{wd}/cap.srt","w").write(srt)
    dur=e-s
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt",
        "-ss",f"{s:.3f}","-t",f"{dur:.3f}","-i","master.mp3",
        "-filter_complex",f"[0:v]subtitles={wd}/cap.srt:force_style='{STYLE}',format=yuv420p[v];"
        f"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
        "-c:a","aac","-b:a","192k","-movflags","+faststart","-t",f"{dur:.3f}",f"../clips/{name}.mp4"],check=True)
    print("  ->",name,os.path.getsize(f"../clips/{name}.mp4")//1024,"KB")
