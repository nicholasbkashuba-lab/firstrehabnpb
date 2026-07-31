#!/usr/bin/env python3
"""Final framing pass: re-render ONLY Dr. Sabesan's shots with the approved
window (y=850 — hair at the top edge, chest in frame, Nick's reference match)
and splice against the v4 master's other shots.

Safe now where the earlier splice attempt wasn't: every shot is cut to the
exact frame count implied by its out-timeline position, so video length is
arithmetically pinned to the audio. Host/wide segments are re-encoded once
from the v4 master (already tonemapped) at crf 18; guest shots come fresh
from cam-c with tonemap + the new crop."""
import json, os, subprocess

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 1920, 1080
C_OFF = 83.874
CROP = "crop=2160:1215:0:850"
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
COLOR_TAGS = "-colorspace bt709 -color_primaries bt709 -color_trc bt709"


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL:", cmd[:160], flush=True)
        print(r.stderr[-1500:], flush=True)
        raise SystemExit(1)
    return r.stdout


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
        seg = f"r_{i:03d}.mp4"
        if cam == "C":
            local = show_s - C_OFF
            sh(f'ffmpeg -v error -y -ss {local:.3f} -i cam-c.mov '
               f'-vf "{CROP},scale={W}:{H}:flags=lanczos,{TONEMAP},fps={FPS},setsar=1" '
               f'-frames:v {n} -an -c:v libx264 -preset veryfast -crf 20 '
               f'-pix_fmt yuv420p {COLOR_TAGS} {seg}')
        else:
            sh(f'ffmpeg -v error -y -ss {out_s:.3f} -i master.mp4 '
               f'-vf "fps={FPS},setsar=1" -frames:v {n} -an '
               f'-c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p {COLOR_TAGS} {seg}')
        got = int(sh(f'ffprobe -v error -select_streams v:0 -count_packets '
                     f'-show_entries stream=nb_read_packets -of csv=p=0 {seg}').strip())
        assert got == n, f"{seg}: {got} != {n}"
        vlist.append(seg)
        if i % 15 == 0:
            print(f"shot {i}/{len(edl)}", flush=True)
    open("vlist.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vlist.txt -c copy video_r.mp4')
    sh(f'ffmpeg -v error -y -i video_r.mp4 -i audio.m4a -map 0:v:0 -map 1:a:0 '
       f'-c copy -movflags +faststart {OUT}/master.mp4')
    old = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4').strip())
    new = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master.mp4').strip())
    print(f"duration old {old:.2f} new {new:.2f}", flush=True)
    assert abs(new - old) < 0.2, "A/V length mismatch"
    tags = sh(f'ffprobe -v error -select_streams v:0 -show_entries '
              f'stream=color_transfer,color_primaries -of csv=p=0 {OUT}/master.mp4').strip()
    assert "bt2020" not in tags and "arib" not in tags

    os.makedirs(f"{OUT}/cuts", exist_ok=True)
    cshots = [x for x in edl if x["cam"] == "C"]
    for k, x in enumerate(cshots):
        if k % 4:
            continue
        t = x["out_s"] + min(0.5, x["d"] / 2)
        sh(f'ffmpeg -v error -y -ss {t:.2f} -i {OUT}/master.mp4 -frames:v 1 '
           f'-vf scale=280:-2 -q:v 5 {OUT}/cuts/c{k:02d}.jpg')
    sh(f'ffmpeg -v error -y -t 120 -i {OUT}/master.mp4 -vf scale=854:480 '
       f'-c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 96k {OUT}/preview_open.mp4')
    sh(f'ffmpeg -v error -y -ss 600 -t 120 -i {OUT}/master.mp4 -vf scale=854:480 '
       f'-c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 96k {OUT}/preview_mid.mp4')
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
