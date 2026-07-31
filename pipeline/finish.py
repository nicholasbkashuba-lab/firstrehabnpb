#!/usr/bin/env python3
"""Final assembly v3: re-render EVERY shot from the camera sources with
(a) proper HLG->SDR tone-mapping — all three iPhones shot HDR (arib-std-b67 /
bt2020) and v1 squeezed that into 8-bit without converting, which renders as a
washed-out tint on SDR displays — and (b) the corrected guest crop (eyes at
~40% of frame, window y=589 instead of 103).

Audio and EDL are reused from the verified v1 master: sync, speaker
classification and the cut list were all correct; only pixels change."""
import json, os, subprocess, time

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 1920, 1080
OFFSETS = {"A": 0.0, "B": 80.674, "C": 83.874}   # from verified sync.json
SRC = {"A": "cam-a.mov", "B": "cam-b.mov", "C": "cam-c.mov"}

# canonical ffmpeg HLG/PQ -> SDR chain, run at 1080p (downscale first) for speed
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
COLOR_TAGS = "-colorspace bt709 -color_primaries bt709 -color_trc bt709"

PRE = {
    "A": f"scale={W}:{H}:flags=lanczos",
    "B": f"scale={W}:{H}:flags=lanczos",
    "C": f"crop=2160:1215:0:589,scale={W}:{H}:flags=lanczos",
}


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL:", cmd[:160], flush=True)
        print(r.stderr[-1500:], flush=True)
        raise SystemExit(1)
    return r.stdout


def is_hdr(f):
    d = json.loads(sh(f'ffprobe -v error -show_streams -of json {f}'))
    v = next(s for s in d["streams"] if s.get("codec_type") == "video" and s.get("width"))
    trc = v.get("color_transfer", "")
    prim = v.get("color_primaries", "")
    print(f"{f}: transfer={trc} primaries={prim}", flush=True)
    return trc in ("arib-std-b67", "smpte2084") or prim == "bt2020"


def main():
    os.makedirs(OUT, exist_ok=True)
    os.chdir(WORK)
    edl = json.load(open("edl.json"))
    hdr = {c: is_hdr(SRC[c]) for c in SRC}

    # benchmark the tonemap chain before committing 30 minutes of footage to it
    t0 = time.time()
    sh(f'ffmpeg -v error -y -ss 300 -t 10 -i cam-a.mov '
       f'-vf "{PRE["A"]},{TONEMAP},fps={FPS}" -an -c:v libx264 -preset veryfast '
       f'-crf 20 {COLOR_TAGS} bench.mp4')
    rate = 10 / (time.time() - t0)
    print(f"tonemap speed: {rate:.2f}x realtime", flush=True)
    if rate < 0.2:
        raise SystemExit("tonemap too slow on this runner — refusing a 3h render")

    sh('ffmpeg -v error -y -i master.mp4 -map 0:a:0 -c copy audio.m4a')

    vlist = []
    for i, x in enumerate(edl):
        cam, s, e = x["cam"], x["s"], x["e"]
        d = e - s
        local = s - OFFSETS[cam]
        if local < 0:
            local, d = 0.0, d + local
        chain = PRE[cam] + ("," + TONEMAP if hdr[cam] else ",format=yuv420p")
        seg = f"v_{i:03d}.mp4"
        sh(f'ffmpeg -v error -y -ss {local:.3f} -t {d:.3f} -i {SRC[cam]} '
           f'-vf "{chain},fps={FPS},setsar=1" -an '
           f'-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {COLOR_TAGS} {seg}')
        dims = sh(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height '
                  f'-of csv=p=0 {seg}').strip()
        assert dims == f"{W},{H}", f"{seg}: {dims}"
        vlist.append(seg)
        if i % 10 == 0:
            print(f"shot {i}/{len(edl)}", flush=True)
    open("vlist.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vlist.txt -c copy video3.mp4')
    sh(f'ffmpeg -v error -y -i video3.mp4 -i audio.m4a -map 0:v:0 -map 1:a:0 '
       f'-c copy -movflags +faststart {OUT}/master.mp4')
    old = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4').strip())
    new = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master.mp4').strip())
    print(f"duration old {old:.2f} new {new:.2f}", flush=True)
    assert abs(new - old) < 1.5
    tags = sh(f'ffprobe -v error -select_streams v:0 -show_entries '
              f'stream=color_transfer,color_primaries -of csv=p=0 {OUT}/master.mp4').strip()
    print("output color:", tags, flush=True)
    assert "bt2020" not in tags and "arib" not in tags, "HDR tags leaked into output"

    # verification pack: A/C/B frames + preview
    os.makedirs(f"{OUT}/cuts", exist_ok=True)
    for i, x in enumerate(edl):
        if i % 4:
            continue
        t = x["s"] + min(0.5, (x["e"] - x["s"]) / 2)
        sh(f'ffmpeg -v error -y -ss {t:.2f} -i {OUT}/master.mp4 -frames:v 1 '
           f'-vf scale=280:-2 -q:v 5 {OUT}/cuts/s{i:03d}_{x["cam"]}_{int(t)}.jpg')
    sh(f'ffmpeg -v error -y -ss 240 -t 180 -i {OUT}/master.mp4 -vf scale=854:480 '
       f'-c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 96k {OUT}/preview.mp4')
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
