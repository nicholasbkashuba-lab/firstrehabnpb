import json, subprocess, sys, os
FPS=30
SRC='../src/'
CAM={'D':(SRC+'IMG_5519.MP4', lambda t:425.8706-0.0000414*t, "scale=1920:1080:flags=lanczos"),
     'M':(SRC+'IMG_2005.MP4', lambda t:512.4313-0.0000329*t, "scale=1920:1080:flags=lanczos"),
     'A':(SRC+'video1.mp4',   lambda t:326.564,              "crop=604:340:18:0,scale=1920:1080:flags=lanczos,unsharp=5:5:0.6")}
shots=json.load(open('shots.json'))
import concurrent.futures as cf
only=set(int(x) for x in sys.argv[1:]) if len(sys.argv)>1 else None
jobs=[]
os.makedirs('seg',exist_ok=True)
lst=open('seg/list.txt','w')
for i,(a,b,s) in enumerate(shots):
    out=f'seg/{i:03d}.mp4'; lst.write(f"file '{i:03d}.mp4'\n")
    if only is not None and i not in only: continue
    if os.path.exists(out) and only is None: continue
    path,off,vf=CAM[s]; n=round((b-a)*FPS)
    cmd=['ffmpeg','-v','error','-y','-ss',f'{a+off(a):.4f}','-i',path,'-an','-vf',vf+f",fps={FPS},format=yuv420p,setsar=1",
         '-frames:v',str(n),'-c:v','libx264','-preset','medium','-crf','20','-r',str(FPS),
         '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out+'.tmp.mp4']
    jobs.append((i,s,a,b,cmd,out))
lst.close()
def run(j):
    i,s,a,b,cmd,out=j
    subprocess.run(cmd[:-1]+['-threads','2',cmd[-1]],check=True); os.replace(out+'.tmp.mp4',out)
    print(i,s,round(a,2),round(b-a,2),flush=True)
with cf.ThreadPoolExecutor(3) as ex: list(ex.map(run,jobs))
