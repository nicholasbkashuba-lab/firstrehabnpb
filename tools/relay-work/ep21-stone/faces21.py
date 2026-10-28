# Face position per camera, sampled every 5 s of master time, in the camera's display coords.
import cv2, numpy as np, subprocess, json, sys
DET=cv2.FaceDetectorYN.create("/root/sizzle-work/models/yunet.onnx","",(640,360),0.6)
CAMS={'D':('src/IMG_2010.MP4',lambda t:107.8726-0.0000318*t,1280,720),
      'G':('src/IMG_5523.MP4',lambda t:94.5896-0.0000410*t,1280,720),
      'M':('main.mov',lambda t:90.2318-0.0000275*t,3840,2160)}
out={}
for k,(p,off,W,H) in CAMS.items():
    res=[]
    for t in np.arange(5,1620,5.0):
        r=subprocess.run(['ffmpeg','-v','error','-ss',f'{t+off(t):.2f}','-i',p,'-frames:v','1','-vf','scale=640:360','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True)
        if len(r.stdout)<640*360*3: continue
        fr=np.frombuffer(r.stdout,np.uint8).reshape(360,640,3)
        _,f=DET.detect(fr)
        if f is None: res.append([float(t),None,None,None]); continue
        b=max(f,key=lambda x:x[2]*x[3]); s=W/640
        res.append([float(t),float((b[0]+b[2]/2)*s),float((b[1]+b[3]/2)*s),float(b[2]*s)])
    out[k]=res
    v=np.array([r[1:] for r in res if r[1] is not None])
    print(k,len(res),'found',len(v),'cx p5/50/95',np.percentile(v[:,0],[5,50,95]).round(),'cy',np.percentile(v[:,1],[5,50,95]).round(),'fw',np.percentile(v[:,2],[5,50,95]).round(),flush=True)
json.dump(out,open('faces.json','w'))
