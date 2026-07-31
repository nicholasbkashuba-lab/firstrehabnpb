#!/usr/bin/env python3
"""Vertical 9:16 social clips from the Sabesan episode.

Dr. Sabesan's camera is NATIVE vertical — her segments use the full frame,
zero crop. Host moments crop the two-shot to a 9:16 window on whoever is
speaking (Mike x=46, Dave x=1900 — verified on stills). Audio comes from the
finished master's mixed track (BT mics + leveled fallback), bumped to
-14 LUFS for social. Every clip also gets a medium.en transcript committed
alongside for the caption pass (captions are burned locally after review —
never burn unreviewed ASR text into a deliverable)."""
import json, os, subprocess

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 1080, 1920
OFF = {"A": 0.0, "C": 83.874}
TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
COLOR_TAGS = "-colorspace bt709 -color_primaries bt709 -color_trc bt709"
VF = {
    "C":    f"scale={W}:{H}:flags=lanczos",
    "mike": f"crop=1215:2160:46:0,scale={W}:{H}:flags=lanczos",
    "dave": f"crop=1215:2160:1900:0,scale={W}:{H}:flags=lanczos",
}
SRC = {"C": "cam-c.mov", "mike": "cam-a.mov", "dave": "cam-a.mov"}

CLIPS = [
    ("01-move-tomorrow",    [("C", 237.7, 293.7)]),
    ("02-therapist-98",     [("C", 406.7, 451.2)]),
    ("03-3d-printed",       [("C", 472.2, 511.4)]),
    ("04-first-of-many",    [("mike", 527.9, 547.2), ("C", 547.2, 563.7)]),
    ("05-muscle-sparing",   [("C", 820.3, 863.0)]),
    ("06-90-is-new-70",     [("C", 873.5, 917.0)]),
    ("07-robots-marketing", [("C", 987.3, 1010.6), ("dave", 1010.6, 1036.6)]),
    ("08-tough-athletes",   [("C", 1152.5, 1214.9)]),
    ("09-end-of-the-line",  [("mike", 1401.8, 1403.6), ("C", 1403.6, 1434.6)]),
    ("10-crushed-elbow",    [("mike", 1548.8, 1557.8), ("C", 1557.8, 1646.3)]),
]


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
    spans = json.load(open("spans_v4.json"))
    outs = []
    t = 0.0
    for sp in spans:
        outs.append(t)
        t += sp["e"] - sp["s"]

    def to_out(show_t):
        for sp, o in zip(spans, outs):
            if sp["s"] - 0.01 <= show_t <= sp["e"] + 0.01:
                return o + (show_t - sp["s"])
        raise SystemExit(f"show time {show_t} not inside any kept span")

    for name, segs in CLIPS:
        parts, out_t = [], 0.0
        for i, (who, s, e) in enumerate(segs):
            d = e - s
            n = round((out_t + d) * FPS) - round(out_t * FPS)
            out_t += d
            local = s - OFF["C" if who == "C" else "A"]
            seg = f"{name}_{i}.mp4"
            sh(f'ffmpeg -v error -y -ss {local:.3f} -i {SRC[who]} '
               f'-vf "{VF[who]},{TONEMAP},fps={FPS},setsar=1" -frames:v {n} -an '
               f'-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {COLOR_TAGS} {seg}')
            dims = sh(f'ffprobe -v error -select_streams v:0 -show_entries '
                      f'stream=width,height -of csv=p=0 {seg}').strip()
            assert dims == f"{W},{H}", f"{seg}: {dims}"
            parts.append(seg)
        open(f"{name}.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
        sh(f'ffmpeg -v error -y -f concat -safe 0 -i {name}.txt -c copy {name}_v.mp4')
        a0 = to_out(segs[0][1])
        sh(f'ffmpeg -v error -y -ss {a0:.3f} -t {out_t:.3f} -i master.mp4 -map 0:a:0 '
           f'-af "loudnorm=I=-14:TP=-1.5" -ar 48000 -ac 2 -c:a aac -b:a 192k {name}_a.m4a')
        sh(f'ffmpeg -v error -y -i {name}_v.mp4 -i {name}_a.m4a -map 0:v:0 -map 1:a:0 '
           f'-c copy -movflags +faststart {OUT}/{name}.mp4')
        vd = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/{name}.mp4').strip())
        assert abs(vd - out_t) < 0.3, f"{name}: {vd} vs {out_t}"
        mv = sh(f'ffmpeg -hide_banner -nostats -i {OUT}/{name}.mp4 -af volumedetect -f null /dev/null 2>&1 '
                f'| grep mean_volume || true')
        print(f"{name}: {vd:.1f}s  {mv.strip().split(']')[-1].strip()}", flush=True)

    # medium.en transcripts for the caption pass
    print("=== transcribe ===", flush=True)
    from faster_whisper import WhisperModel
    m = WhisperModel("medium.en", device="cpu", compute_type="int8")
    os.makedirs(f"{OUT}/text", exist_ok=True)
    for name, _ in CLIPS:
        sh(f'ffmpeg -v error -y -i {OUT}/{name}.mp4 -ac 1 -ar 16000 {name}_16k.wav')
        segs, _i = m.transcribe(f"{name}_16k.wav", beam_size=5, vad_filter=True,
                                condition_on_previous_text=False)
        data = [{"s": round(x.start, 2), "e": round(x.end, 2), "t": x.text.strip()} for x in segs]
        json.dump(data, open(f"{OUT}/text/{name}.json", "w"), indent=1)
        print(name, len(data), "cues", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
