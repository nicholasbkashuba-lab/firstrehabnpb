#!/usr/bin/env python3
"""Surgical edit at Nick's flagged stretch (out 23:12-23:56 of the 1080p final):

  1. break the 34s guest hold (out 1390.3+34.3) with a 5s wide insert at
     out 1407.3 (show 1500.6 — f1233 covers it)
  2. remove the banter out [1424.7, 1448.7] (show 1517.3-1548.6): joins
     "...that's really a blessing for me" -> "But one last thing..."

Everything else is spliced from the existing master at shot boundaries
(which are keyframes) with exact frame counts; audio is the master track
minus the removed span, with 15ms fades at the joins."""
import json, os, subprocess

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 1920, 1080
F1233_OFF = 1232.979
WIDE_AT_OUT = 1407.3          # where the insert lands (old out-time)
WIDE_SHOW = 1500.6            # corresponding show time for f1233
WIDE_LEN = 5.0
CUT_A, CUT_B = 1424.7, 1448.7  # removed span (old out-time)
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
    mdur = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 master.mp4').strip())

    # new timeline pieces: (kind, src_t, dur) — src_t in old-master time,
    # except the wide insert which cuts from f1233
    pieces = [
        ("copy", 0.0, WIDE_AT_OUT),
        ("wide", WIDE_SHOW - F1233_OFF, WIDE_LEN),
        ("copy", WIDE_AT_OUT + WIDE_LEN, CUT_A - (WIDE_AT_OUT + WIDE_LEN)),
        ("copy", CUT_B, mdur - CUT_B),
    ]
    total = sum(p[2] for p in pieces)
    print(f"new runtime {total/60:.2f} min (was {mdur/60:.2f})", flush=True)

    vlist, out_t = [], 0.0
    for i, (kind, st, d) in enumerate(pieces):
        n = round((out_t + d) * FPS) - round(out_t * FPS)
        out_t += d
        seg = f"t_{i}.mp4"
        if kind == "wide":
            sh(f'ffmpeg -v error -y -ss {st:.3f} -i f1233.mov '
               f'-vf "scale={W}:{H}:flags=lanczos,{TONEMAP},fps={FPS},setsar=1" '
               f'-frames:v {n} -an -c:v libx264 -preset veryfast -crf 20 '
               f'-pix_fmt yuv420p {COLOR_TAGS} {seg}')
        else:
            sh(f'ffmpeg -v error -y -ss {st:.3f} -i master.mp4 '
               f'-vf "fps={FPS},setsar=1" -frames:v {n} -an '
               f'-c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p {COLOR_TAGS} {seg}')
        got = int(sh(f'ffprobe -v error -select_streams v:0 -count_packets '
                     f'-show_entries stream=nb_read_packets -of csv=p=0 {seg}').strip())
        assert got == n, f"{seg}: {got} != {n}"
        vlist.append(seg)
        print(f"piece {i} ({kind}) {d:.1f}s ok", flush=True)
    open("vl.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vl.txt -c copy video_t.mp4')

    # audio: continuous up to CUT_A, then resumes at CUT_B (the wide
    # insert keeps the master audio underneath — same conversation moment)
    alist = []
    for i, (st, d) in enumerate([(0.0, CUT_A), (CUT_B, mdur - CUT_B)]):
        w = f"at_{i}.wav"
        sh(f'ffmpeg -v error -y -ss {st:.3f} -t {d:.3f} -i master.mp4 -map 0:a:0 '
           f'-af "afade=t=in:st=0:d=0.015,afade=t=out:st={d-0.015:.3f}:d=0.015" '
           f'-ar 48000 -ac 2 -c:a pcm_s16le {w}')
        alist.append(w)
    open("al.txt", "w").write("".join(f"file '{a}'\n" for a in alist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i al.txt -c copy audio_t.wav')
    sh(f'ffmpeg -v error -y -i video_t.mp4 -i audio_t.wav -map 0:v:0 -map 1:a:0 '
       f'-c:v copy -c:a aac -b:a 192k -movflags +faststart {OUT}/master.mp4')
    vd = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master.mp4').strip())
    print(f"final {vd/60:.2f} min", flush=True)
    # lossless audio master so the EQ pick can be applied later without
    # decoding the delivered AAC a second time
    sh(f'ffmpeg -v error -y -i audio_t.wav -c:a flac {OUT}/audio_master.flac')
    assert abs(vd - total) < 0.3
    # verification: frames around both edit points
    os.makedirs(f"{OUT}/cuts", exist_ok=True)
    for t in (WIDE_AT_OUT - 1, WIDE_AT_OUT + 2, WIDE_AT_OUT + WIDE_LEN + 1,
              CUT_A - 2, CUT_A + 1, CUT_A + 6):
        sh(f'ffmpeg -v error -y -ss {t:.2f} -i {OUT}/master.mp4 -frames:v 1 '
           f'-vf scale=280:-2 -q:v 5 {OUT}/cuts/e_{t:.0f}.jpg')
    sh(f'ffmpeg -v error -y -ss {WIDE_AT_OUT-8:.2f} -t 40 -i {OUT}/master.mp4 '
       f'-vf scale=854:480 -c:v libx264 -preset veryfast -crf 27 '
       f'-c:a aac -b:a 96k {OUT}/preview_edit.mp4')
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
