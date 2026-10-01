import numpy as np, subprocess, torch
from speechbrain.inference.speaker import EncoderClassifier
m=EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="/home/user/ep16/ecapa", run_opts={"device":"cpu"})
x=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i","master.mp3","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout,dtype=np.float32)
W=int(1.5*16000); H=int(0.5*16000)
starts=np.arange(0,len(x)-W,H)
embs=[];rms=[]
torch.set_num_threads(3)
B=64
for i in range(0,len(starts),B):
    batch=np.stack([x[s:s+W] for s in starts[i:i+B]])
    with torch.no_grad(): e=m.encode_batch(torch.from_numpy(batch)).squeeze(1).numpy()
    embs.append(e); rms+= [float(np.sqrt((b**2).mean())) for b in batch]
np.savez("embeds.npz",t=(starts+W/2)/16000,e=np.concatenate(embs),rms=np.array(rms))
print("done",len(starts))
