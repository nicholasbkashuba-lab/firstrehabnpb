# Re-burn captions on the already-rendered clip pieces: short one-line cues, each shown
# when its first word is spoken, sitting at the very bottom of the frame.
import json, os, re, subprocess, sys
src=open('clips18.py').read().split('os.makedirs("clips"')[0]
exec(src)                                   # SPEC, W, find, FIX, FONT, ts, ASS_HEAD
MARGIN_V=int(os.environ.get("MV","12"))
HEAD=ASS_HEAD.replace(",2,10,10,35,1",f",2,10,10,{MARGIN_V},1")
assert HEAD!=ASS_HEAD
EXCISE={"07-joseph-pilates-was-real":[("he was a soldier",1003,"in the isle",1008)]}
MAXW1=900; MAXWORDS=4
def words_for(i,j,DROP):
    ws=[]
    for w in W[i:j+1]:
        tok=w["w"].strip()
        if ws and re.match(r"^[.%'-]",tok): ws[-1]["w"]+=tok; ws[-1]["e"]=w["e"]; continue
        ws.append({"w":tok,"s":w["s"],"e":w["e"]})
    k=0
    while k<len(ws)-2:
        if [x["w"] for x in ws[k:k+2]]==["Munch","and"] and ws[k+2]["w"].startswith("Gladbach"):
            ws[k]["w"]="Mönchengladbach"+ws[k+2]["w"][8:]; ws[k]["e"]=ws[k+2]["e"]; del ws[k+1:k+3]
        k+=1
    for w in ws:
        for p,r in FIX: w["w"]=re.sub(p,r,w["w"])
        w["w"]=re.sub(r'(?<=\w)-(?=\w)',' ',w["w"])
    return [w for w in ws if not any(a<=w["s"]<b for a,b in DROP)]
def chunks(ws):
    out=[];cur=[]
    for w in ws:
        trial=" ".join(x["w"] for x in cur+[w])
        if cur and (len(cur)>=MAXWORDS or FONT.getlength(trial)>MAXW1): out.append(cur); cur=[]
        cur.append(w)
        if re.search(r"[.?!]$",w["w"]) or (re.search(r"[,;:]$",w["w"]) and len(cur)>=2): out.append(cur); cur=[]
    if cur: out.append(cur)
    # fold a lone trailing word into the previous chunk when it still fits on one line
    m=[]
    for c in out:
        if m and len(c)==1 and FONT.getlength(" ".join(x["w"] for x in m[-1]+c))<=MAXW1 and not re.search(r"[.?!]$",m[-1][-1]["w"]): m[-1]=m[-1]+c
        else: m.append(c)
    return m
for name,pa,na,pb,nb in SPEC:
    if len(sys.argv)>1 and name not in sys.argv[1:]: continue
    i=find(pa,na); j=find(pb,nb); j+=len(pb.split())-1
    s=round(W[i]["s"]-0.12,2); e=round(W[j]["e"]+0.45,2)
    DROP=[(round(W[find(xa,xna)]["s"]-0.05,2), round(W[find(xb,xnb)]["s"]-0.08,2)) for xa,xna,xb,xnb in EXCISE.get(name,[])]
    o=lambda m: m-s-sum(min(max(m-a,0),b-a) for a,b in DROP)
    keep=[];cur=s
    for a,b in DROP: keep.append((cur,a)); cur=b
    keep.append((cur,e)); dur=sum(b-a for a,b in keep)
    C=chunks(words_for(i,j,DROP)); cues=[]
    for k,c in enumerate(C):
        a=o(c[0]["s"]); nxt=o(C[k+1][0]["s"]) if k+1<len(C) else dur
        b=min(nxt, o(c[-1]["e"])+0.5, dur)
        txt=" ".join(x["w"] for x in c)
        if k==0: txt=txt[:1].upper()+txt[1:]
        cues.append((max(a,0),max(b,a+0.25),txt))
    wd=f"tmp_{name}"
    open(f"{wd}/cap2.ass","w").write(HEAD+"".join(f"Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,{t}\n" for a,b,t in cues))
    af="".join(f"[1:a]atrim={a-s:.3f}:{b-s:.3f},asetpts=PTS-STARTPTS[k{q}];" for q,(a,b) in enumerate(keep))
    af+="".join(f"[k{q}]" for q in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1[cat];"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{wd}/l.txt","-ss",f"{s:.3f}","-t",f"{e-s:.3f}","-i","master.mp3",
        "-filter_complex",f"[0:v]subtitles={wd}/cap2.ass,format=yuv420p[v];{af}"
        f"[cat]loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:d=0.08,afade=t=out:st={dur-0.25:.2f}:d=0.25,aresample=48000[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","20","-r","30","-pix_fmt","yuv420p",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
        "-c:a","aac","-b:a","192k","-movflags","+faststart","-t",f"{dur:.3f}",f"clips/{name}.mp4"],check=True)
    print(name, len(cues),"cues", round(dur,1),"s", flush=True)
