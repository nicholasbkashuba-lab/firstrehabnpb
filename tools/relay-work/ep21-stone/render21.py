# Render every shot of shots.json from the RAW cameras, 1920x1080 30 fps, then join.
import json, subprocess, sys, os
import concurrent.futures as cf
FPS=30
SH="unsharp=5:5:0.5:5:5:0"
CAM={'D':('src/IMG_2010.MP4',lambda t:107.8726-0.0000318*t,f"scale=1920:1080:flags=lanczos,{SH}"),
     'G':('src/IMG_5523.MP4',lambda t:94.5896-0.0000410*t,f"crop=1152:648:0:0,scale=1920:1080:flags=lanczos,{SH}"),
     'M':('main.mov',        lambda t:90.2318-0.0000275*t,os.environ.get('MIKE_VF',"crop=2880:1620:640:0,scale=1920:1080:flags=lanczos"))}
J=json.load(open('shots.json')); shots=J['shots']
# per shot fixed re-centring crops (static within the shot, never a moving camera)
CROPS={int(k):v for k,v in json.load(open('crops.json')).items()} if os.path.exists('crops.json') else {}
only=set(int(x) for x in sys.argv[1:]) if len(sys.argv)>1 else None
os.makedirs('seg',exist_ok=True)
jobs=[]
with open('seg/list.txt','w') as lst:
    for i,(a,b,s) in enumerate(shots):
        n=round((b-a)*FPS); out=f'seg/{i:03d}.mp4'
        lst.write(f"file '{i:03d}.mp4'\nduration {n/FPS:.6f}\n")
        if only is not None and i not in only: continue
        if only is None and os.path.exists(out): continue
        path,off,vf=CAM[s]
        vf=CROPS.get(i,vf)
        cmd=['ffmpeg','-v','error','-y','-ss',f'{a+off(a):.4f}','-i',path,'-an','-vf',f"fps={FPS},{vf},setsar=1,format=yuv420p",
             '-frames:v',str(n),'-c:v','libx264','-preset','medium','-crf','19','-r',str(FPS),'-threads','2',
             '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out+'.tmp.mp4']
        jobs.append((i,s,a,n,cmd,out))
def run(j):
    i,s,a,n,cmd,out=j
    subprocess.run(cmd,check=True); os.replace(out+'.tmp.mp4',out)
    print(i,s,round(a,2),n,flush=True)
with cf.ThreadPoolExecutor(int(os.environ.get('PAR','3'))) as ex: list(ex.map(run,jobs))
print('ALL SHOTS DONE',flush=True)
