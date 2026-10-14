import cv2,numpy as np,subprocess,json,sys
casc=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
prof=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_profileface.xml")
CAM={"DAVE":("dave.mov",0.999971,195.143),"MIKE":("Mike.mov",0.999973,212.981),"IMG":("IMG_5434.MOV",0.999960,186.044)}
def frame(f,ts):
    p=subprocess.run(["ffmpeg","-v","error","-ss",f"{ts:.2f}","-i",f,"-frames:v","1","-vf","scale=1920:1080","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(p,np.uint8),cv2.IMREAD_COLOR)
for cam,times in json.loads(sys.argv[1]).items():
    f,r,o=CAM[cam]
    for m in times:
        im=frame(f,r*m+o); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        fs=list(casc.detectMultiScale(g,1.1,6,minSize=(80,80)))+list(prof.detectMultiScale(g,1.1,6,minSize=(80,80)))
        print(cam,m,[(int((x+w/2)*2),int((y+h/2)*2),int(w*2)) for x,y,w,h in fs])
