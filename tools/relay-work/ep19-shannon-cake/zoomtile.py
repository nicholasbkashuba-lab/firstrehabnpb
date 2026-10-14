import numpy as np, subprocess
W,H=160,90
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","raw/video1573954541.mp4","-vf",f"fps=2,scale={W}:{H},format=gray","-f","rawvideo","-"],capture_output=True).stdout,np.uint8).reshape(-1,H,W).astype(float)
tile=x[:, :, 56:104]   # x 224..416 of 640
side=np.concatenate([x[:,:,:50],x[:,:,110:]],2)
m=tile.mean((1,2)); s=side.mean((1,2))
np.savez("zoomtile.npz",t=np.arange(len(m))/2.0,m=m,s=s)
h=np.histogram(m,bins=20)
for c,e in zip(*h): print(f"{e:6.1f} {c}")
