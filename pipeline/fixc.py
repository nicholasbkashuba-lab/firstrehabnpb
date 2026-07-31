#!/usr/bin/env python3
"""Re-render ONLY the cam-c (guest) shots with a corrected crop and splice
them back against the existing master's other shots.

v1 placed the 16:9 window at y=103, from a reference still that caught
Dr. Sabesan mid-gesture; across the actual show her eyes sit ~80% down that
window with her mouth clipped. Corrected: eyes land at ~40% of frame height
(y=589). Audio, EDL, sync, and every host/wide shot are untouched — host/wide
segments are re-encoded once from the verified master (crf18, visually
transparent) instead of re-downloading 12 GB of source."""
import json, os, subprocess

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 1920, 1080
C_OFF = 83.874          # cam-c offset from sync.json (verified, conf 16.7)
CROP = "crop=2160:1215:0:589"


def sh(cmd):
    print("+", cmd[:160], flush=True)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:], flush=True)
        raise SystemExit(1)
    return r.stdout


def main():
    os.makedirs(OUT, exist_ok=True)
    os.chdir(WORK)
    edl = json.load(open("edl.json"))
    # master audio is final — reuse it byte-for-byte
    sh('ffmpeg -v error -y -i master.mp4 -map 0:a:0 -c copy audio.m4a')

    vlist = []
    for i, x in enumerate(edl):
        cam, s, e = x["cam"], x["s"], x["e"]
        d = e - s
        seg = f"v_{i:03d}.mp4"
        if cam == "C":
            local = s - C_OFF
            sh(f'ffmpeg -v error -y -ss {local:.3f} -t {d:.3f} -i cam-c.mov '
               f'-vf "{CROP},scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1" -an '
               f'-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {seg}')
        else:
            sh(f'ffmpeg -v error -y -ss {s:.3f} -t {d:.3f} -i master.mp4 '
               f'-vf "fps={FPS},setsar=1" -an '
               f'-c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p {seg}')
        dims = sh(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height '
                  f'-of csv=p=0 {seg}').strip()
        assert dims == f"{W},{H}", f"{seg}: {dims}"
        vlist.append(seg)
        if i % 10 == 0:
            print(f"shot {i}/{len(edl)}", flush=True)
    open("vlist.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vlist.txt -c copy video2.mp4')
    sh(f'ffmpeg -v error -y -i video2.mp4 -i audio.m4a -map 0:v:0 -map 1:a:0 '
       f'-c copy -movflags +faststart {OUT}/master.mp4')
    old = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4').strip())
    new = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master.mp4').strip())
    print(f"duration old {old:.2f} new {new:.2f}", flush=True)
    assert abs(new - old) < 1.5

    os.makedirs(f"{OUT}/cuts", exist_ok=True)
    for k, x in enumerate(c for c in edl if c["cam"] == "C"):
        if k % 4:
            continue
        t = x["s"] + 0.5
        sh(f'ffmpeg -v error -y -ss {t:.2f} -i {OUT}/master.mp4 -frames:v 1 '
           f'-vf scale=280:-2 -q:v 5 {OUT}/cuts/c{k:02d}_{t:.0f}.jpg')
    sh(f'ffmpeg -v error -y -ss 240 -t 180 -i {OUT}/master.mp4 -vf scale=854:480 '
       f'-c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 96k {OUT}/preview.mp4')
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
