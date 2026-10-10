import subprocess,numpy as np,sys
exec(open('lock_rate.py').read().split("files=os.listdir")[0])
CAM={"DAVE":("dave.mov",0.999971,195.143,False),"MIKE":("Mike.mov",0.999973,212.981,True),"GUEST":("IMG_5434.MOV",0.999960,186.044,True)}
M=decode('master.mp3')
for ang,ms in [("MIKE",30),("DAVE",130),("GUEST",500),("GUEST",1050),("MIKE",1420),("DAVE",1560)]:
    f,r,o,skip=CAM[ang]; cs=r*ms+o; pre=max(cs-4,0); D=12
    x=np.frombuffer(subprocess.run(["ffmpeg","-v","error"]+(["-skip_frame","noref"] if skip else [])+["-ss",f"{pre:.3f}","-i",f,"-ss",f"{cs-pre:.3f}","-t",str(D),"-map","0:a:0","-ac","1","-ar","8000","-f","f32le","-"],capture_output=True).stdout,np.float32).astype(float)
    seg=M[int((ms-3)*SR):int((ms+D+3)*SR)]
    off,p=align(seg,x)
    print(f"{ang:<6} master {ms:5d}s: camera audio lands at {off-3:+.3f}s (want 0.000)  PSR {p:.0f}")
