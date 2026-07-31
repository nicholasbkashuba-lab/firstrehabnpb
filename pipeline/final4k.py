#!/usr/bin/env python3
"""4K master: re-render every shot of the locked v4 cut at 3840x2160.

cam-a and the wides are native 4K sources (true detail). cam-c's approved
window (2160x1215 @ y=850) is lanczos-upscaled 1.78x — it cannot gain real
sensor detail, but the 4K container buys YouTube's premium codec treatment
for the whole episode. Cut list and audio are reused verbatim from v4;
exact per-shot frame counts keep A/V pinned."""
import json, os, subprocess

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 3840, 2160
OFFSETS = {"cam-a": 0.0, "cam-b": 80.674, "cam-c": 83.874,
           "f1087": 1086.516, "f1233": 1232.979, "f1527": 1526.617}
DUR = {"cam-b": 886.02, "f1087": 60.08, "f1233": 280.37, "f1527": 254.66}
WIDE = ["cam-b", "f1087", "f1233", "f1527"]
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
COLOR_TAGS = "-colorspace bt709 -color_primaries bt709 -color_trc bt709"
PRE = {"A": None, "B": None,          # native 4K — no geometry change
       "C": f"crop=2160:1215:0:850,scale={W}:{H}:flags=lanczos"}


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL:", cmd[:160], flush=True)
        print(r.stderr[-1500:], flush=True)
        raise SystemExit(1)
    return r.stdout


def wide_src(t):
    for w in WIDE:
        if OFFSETS[w] <= t < OFFSETS[w] + DUR[w] - 0.2:
            return w
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    os.chdir(WORK)
    edl = json.load(open("edl_v4.json"))
    sh('ffmpeg -v error -y -i master.mp4 -map 0:a:0 -c copy audio.m4a')

    vlist = []
    for i, x in enumerate(edl):
        cam, out_s, show_s, d = x["cam"], x["out_s"], x["show_s"], x["d"]
        n = round((out_s + d) * FPS) - round(out_s * FPS)
        if n <= 0:
            continue
        src = {"A": "cam-a", "C": "cam-c"}.get(cam) or wide_src(show_s) or "cam-a"
        local = show_s - OFFSETS[src]
        geo = PRE[cam]
        chain = (geo + "," if geo else "") + TONEMAP
        seg = f"k_{i:03d}.mp4"
        sh(f'ffmpeg -v error -y -ss {max(0,local):.3f} -i {src}.mov '
           f'-vf "{chain},fps={FPS},setsar=1" -frames:v {n} -an '
           f'-c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p {COLOR_TAGS} {seg}')
        dims = sh(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height '
                  f'-of csv=p=0 {seg}').strip()
        assert dims == f"{W},{H}", f"{seg}: {dims}"
        got = int(sh(f'ffprobe -v error -select_streams v:0 -count_packets '
                     f'-show_entries stream=nb_read_packets -of csv=p=0 {seg}').strip())
        assert got == n, f"{seg}: {got} != {n}"
        vlist.append(seg)
        print(f"shot {i}/{len(edl)} ok", flush=True)
    open("vlist.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vlist.txt -c copy video4k.mp4')
    sh(f'ffmpeg -v error -y -i video4k.mp4 -i audio.m4a -map 0:v:0 -map 1:a:0 '
       f'-c copy -movflags +faststart {OUT}/master4k.mp4')
    old = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4').strip())
    new = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master4k.mp4').strip())
    print(f"duration 1080p {old:.2f} vs 4k {new:.2f}", flush=True)
    assert abs(new - old) < 0.2
    tags = sh(f'ffprobe -v error -select_streams v:0 -show_entries '
              f'stream=color_transfer,color_primaries -of csv=p=0 {OUT}/master4k.mp4').strip()
    assert "bt2020" not in tags and "arib" not in tags
    print(f"size {os.path.getsize(OUT+'/master4k.mp4')/1e9:.2f} GB", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
