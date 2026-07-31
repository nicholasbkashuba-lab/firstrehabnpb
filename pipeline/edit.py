#!/usr/bin/env python3
"""Multicam assembly for Pain 2 Power — Dr. Sabesan episode.

Three phones shot one 30-minute conversation:
  cam-a  horizontal two-shot of the hosts (Mike left, Dave right), full show
  cam-b  horizontal wide of the whole room; Bluetooth mics -> BEST AUDIO;
         died at 14:46 and restarted as the frag-* files
  cam-c  VERTICAL close-up of Dr. Sabesan, full show (cropped to 16:9 here)

Strategy: sync everything to cam-a's clock by audio cross-correlation, build
one continuous audio track (Bluetooth wherever it exists, cleaned cam-a audio
in the gaps), transcribe it, classify each utterance guest/host by pitch
(one female guest vs two male hosts separates reliably), then cut:
guest -> cam-c, hosts -> cam-a, wide -> crosstalk & long-shot relief.

Everything is deterministic and logged; verification frames are emitted at cut
boundaries so the speaker-matching can be EYEBALLED before delivery, because
"the tool said it worked" has burned us before.
"""
import json, math, os, subprocess, sys

import numpy as np

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
ENV_HZ = 100          # envelope rate for sync correlation
FPS = 30
W, H = 1920, 1080
AUDIO_I = -16         # LUFS target, podcast standard
MIN_SHOT = 2.4        # never cut faster than this
BT_MIN_ISLAND = 20.0  # BT scraps shorter than this aren't worth two timbre jumps
LONG_SHOT = 75.0      # split host shots longer than this with a wide insert
WIDE_INSERT = 5.0

# Bluetooth-quality chain: signal is already hot and close, keep it gentle.
AF_BT = f"highpass=f=60,afftdn=nr=6:nf=-30,loudnorm=I={AUDIO_I}:TP=-1.5:LRA=11"
# Camera-mic fallback chain (the Episode-8 chain): distant mic needs denoise,
# speech normalisation and compression before it can sit next to the BT track.
AF_CAM = (f"highpass=f=100,equalizer=f=2600:t=q:w=1.4:g=4,"
          f"speechnorm=e=25:r=0.0008:l=1,"
          f"acompressor=threshold=-24dB:ratio=6:attack=5:release=150,"
          f"loudnorm=I={AUDIO_I}:TP=-1.5,alimiter=limit=0.95")

SOURCES = {
    # name: (file, nominal start in cam-a time [s], role)
    "cam-a": ("cam-a.mov", 0.0,    "hosts"),
    "cam-b": ("cam-b.mov", 81.0,   "wide"),
    "cam-c": ("cam-c.mov", 84.0,   "guest"),
    "f1061": ("f1061.mov", 1061.0, "wide"),   # 5:03:42, 9.7s
    "f1087": ("f1087.mov", 1087.0, "wide"),   # 5:04:08, 60s
    "f1233": ("f1233.mov", 1233.0, "wide"),   # 5:06:34, 280s
    "f1527": ("f1527.mov", 1527.0, "wide"),   # 5:11:28, 255s
}


def sh(cmd, **kw):
    print("+", cmd[:180], flush=True)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stderr[-2000:], flush=True)
        raise SystemExit(f"command failed: {cmd[:120]}")
    return r.stdout


def probe(f):
    """iPhone .mov files carry extra data/metadata streams that can break naive
    v:0 queries — walk the full stream list instead."""
    d = json.loads(sh(f'ffprobe -v error -show_streams -show_format -of json {f}'))
    vs = [s for s in d["streams"]
          if s.get("codec_type") == "video" and s.get("width") and s.get("height")]
    assert vs, f"{f}: no sized video stream among {[s.get('codec_type') for s in d['streams']]}"
    dur = float(d["format"]["duration"])
    return int(vs[0]["width"]), int(vs[0]["height"]), dur


def envelope(f, dur=None):
    """Rectified, frame-averaged mono envelope at ENV_HZ for sync correlation."""
    lim = f"-t {dur}" if dur else ""
    raw = subprocess.run(
        f'ffmpeg -v error {lim} -i {f} -map 0:a:0 -ac 1 -ar 8000 -f f32le -',
        shell=True, capture_output=True).stdout
    y = np.abs(np.frombuffer(raw, dtype=np.float32))
    n = len(y) // (8000 // ENV_HZ)
    env = y[: n * (8000 // ENV_HZ)].reshape(n, -1).mean(axis=1)
    # log-compress so loud plosives don't dominate the correlation
    return np.log1p(env * 50)


def refine_offset(env_a, env_k, nominal, search=6.0):
    """Peak of FFT cross-correlation, restricted to nominal±search seconds."""
    n = len(env_a) + len(env_k) - 1
    nfft = 1 << (n - 1).bit_length()
    ca = np.fft.rfft(env_a - env_a.mean(), nfft)
    ck = np.fft.rfft(env_k - env_k.mean(), nfft)
    xc = np.fft.irfft(ca * np.conj(ck), nfft)[:n]
    lags = np.arange(n) - (len(env_k) - 1)
    lo, hi = int((nominal - search) * ENV_HZ), int((nominal + search) * ENV_HZ)
    win = (lags >= lo) & (lags <= hi)
    if not win.any():
        raise SystemExit(f"sync window empty for nominal {nominal}")
    i = np.argmax(xc[win])
    lag = lags[win][i]
    peak = xc[win][i]
    med = np.median(np.abs(xc[win]))
    conf = peak / (med + 1e-9)
    return lag / ENV_HZ, conf


def main():
    os.makedirs(OUT, exist_ok=True)
    os.chdir(WORK)

    # ---- probe everything -------------------------------------------------
    meta = {}
    for name, (f, nom, role) in SOURCES.items():
        w, h, dur = probe(f)
        meta[name] = {"w": w, "h": h, "dur": dur, "nominal": nom, "role": role}
        print(f"{name}: {w}x{h} {dur:.2f}s role={role}", flush=True)
    assert meta["cam-c"]["h"] > meta["cam-c"]["w"], "cam-c expected vertical"
    assert meta["cam-a"]["w"] > meta["cam-a"]["h"], "cam-a expected horizontal"

    # ---- sync -------------------------------------------------------------
    print("=== sync ===", flush=True)
    env_a = envelope("cam-a.mov")
    offsets = {"cam-a": 0.0}
    sync_report = {}
    for name in ("cam-b", "cam-c", "f1061", "f1087", "f1233", "f1527"):
        nom = meta[name]["nominal"]
        env_k = envelope(SOURCES[name][0])
        off, conf = refine_offset(env_a, env_k, nom, search=6.0 if name.startswith("cam") else 12.0)
        drift = off - nom
        print(f"{name}: nominal {nom:.1f} refined {off:.2f} (drift {drift:+.2f}s, conf {conf:.1f})",
              flush=True)
        if abs(drift) > 8.0:
            raise SystemExit(f"{name}: refined offset {off:.2f} too far from nominal {nom}")
        offsets[name] = off
        sync_report[name] = {"nominal": nom, "refined": round(off, 3), "conf": round(float(conf), 2)}
    json.dump(sync_report, open(f"{OUT}/sync.json", "w"), indent=1)

    a_dur = meta["cam-a"]["dur"]
    show_end = a_dur - 0.5

    # ---- coverage maps ----------------------------------------------------
    def cover(name):
        s = offsets[name]
        return (max(0.0, s), min(show_end, s + meta[name]["dur"]))

    bt_raw = [("cam-b", *cover("cam-b"))]
    for fr in ("f1061", "f1087", "f1233", "f1527"):
        c = cover(fr)
        if c[1] - c[0] >= BT_MIN_ISLAND:
            bt_raw.append((fr, *c))
        else:
            print(f"dropping BT island {fr} ({c[1]-c[0]:.1f}s < {BT_MIN_ISLAND}s)", flush=True)
    bt_raw.sort(key=lambda x: x[1])
    wide_cover = [(s, e) for _, s, e in bt_raw]        # wide video == BT sources
    c_cover = cover("cam-c")

    # ---- audio track ------------------------------------------------------
    print("=== audio ===", flush=True)
    pieces, t = [], 0.0
    for src, s, e in bt_raw:
        if s > t + 0.01:
            pieces.append(("cam-a", t, s, AF_CAM))
        pieces.append((src, max(t, s), e, AF_BT))
        t = e
    if t < show_end:
        pieces.append(("cam-a", t, show_end, AF_CAM))
    audio_list = []
    for i, (src, s, e, chain) in enumerate(pieces):
        local = s - offsets[src]
        d = e - s
        fades = f",afade=t=in:st=0:d=0.15,afade=t=out:st={d-0.15:.3f}:d=0.15"
        wav = f"ap_{i:02d}.wav"
        sh(f'ffmpeg -v error -y -ss {local:.3f} -t {d:.3f} -i {SOURCES[src][0]} '
           f'-map 0:a:0 -af "{chain}{fades}" -ar 48000 -ac 2 -c:a pcm_s16le {wav}')
        audio_list.append(wav)
        print(f"audio {i}: {src} show[{s:.1f}..{e:.1f}] ({'BT' if chain==AF_BT else 'CAM'})",
              flush=True)
    open("alist.txt", "w").write("".join(f"file '{w}'\n" for w in audio_list))
    sh('ffmpeg -v error -y -f concat -safe 0 -i alist.txt -c copy show_audio.wav')
    got = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 show_audio.wav').strip())
    assert abs(got - show_end) < 2.0, f"audio length {got} vs {show_end}"
    json.dump([{"src": p[0], "s": round(p[1], 2), "e": round(p[2], 2),
                "kind": "BT" if p[3] == AF_BT else "CAM"} for p in pieces],
              open(f"{OUT}/audio_map.json", "w"), indent=1)

    # ---- transcribe -------------------------------------------------------
    print("=== transcribe ===", flush=True)
    sh('ffmpeg -v error -y -i show_audio.wav -ac 1 -ar 16000 show16k.wav')
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe("show16k.wav", beam_size=5, vad_filter=True,
                               condition_on_previous_text=False)
    segments = [{"s": round(x.start, 2), "e": round(x.end, 2), "t": x.text.strip()}
                for x in segs]
    print(f"{len(segments)} segments", flush=True)

    # ---- speaker classification by pitch ----------------------------------
    print("=== pitch ===", flush=True)
    import librosa
    y16 = np.frombuffer(subprocess.run(
        'ffmpeg -v error -i show16k.wav -f f32le -', shell=True,
        capture_output=True).stdout, dtype=np.float32)
    prev = "H"
    for seg in segments:
        s, e = seg["s"], seg["e"]
        mid = (s + e) / 2
        s2, e2 = max(s, mid - 2.0), min(e, mid + 2.0)   # cap pyin cost per segment
        chunk = y16[int(s2 * 16000): int(e2 * 16000)]
        spk, f0med, voiced = prev, None, 0.0
        if len(chunk) > 1600:
            f0, vflag, _ = librosa.pyin(chunk, fmin=70, fmax=350, sr=16000,
                                        frame_length=1024)
            v = f0[vflag == True]  # noqa: E712
            voiced = float(len(v)) / max(1, len(f0))
            if len(v) >= 5 and voiced >= 0.15:
                f0med = float(np.median(v))
                if f0med >= 165:
                    spk = "G"
                elif f0med <= 150:
                    spk = "H"
                else:
                    spk = prev
        seg["spk"] = spk
        seg["f0"] = round(f0med, 1) if f0med else None
        seg["voiced"] = round(voiced, 2)
        prev = spk
    json.dump(segments, open(f"{OUT}/transcript.json", "w"), indent=1)
    ng = sum(1 for x in segments if x["spk"] == "G")
    print(f"guest segments: {ng}/{len(segments)}", flush=True)
    assert 0.05 < ng / len(segments) < 0.95, "pitch split looks degenerate — refusing to cut"

    # ---- EDL --------------------------------------------------------------
    print("=== edl ===", flush=True)

    def in_cover(t, cov):
        return any(s <= t < e for s, e in cov)

    def cam_for(seg):
        if seg["spk"] == "G" and c_cover[0] <= seg["s"] < c_cover[1]:
            return "C"
        return "A"

    content_end = min(show_end, segments[-1]["e"] + 2.5)
    shots = []
    for seg in segments:
        cam = cam_for(seg)
        if shots and shots[-1]["cam"] == cam:
            shots[-1]["e"] = seg["e"]
        else:
            shots.append({"cam": cam, "s": seg["s"], "e": seg["e"]})
    # stitch gaps: extend each shot to the start of the next
    for i in range(len(shots) - 1):
        shots[i]["e"] = shots[i + 1]["s"]
    shots[0]["s"] = 0.0
    shots[-1]["e"] = content_end

    # crosstalk: runs of >=3 consecutive short shots become one wide (if covered)
    merged, i = [], 0
    while i < len(shots):
        j = i
        while j < len(shots) and shots[j]["e"] - shots[j]["s"] < MIN_SHOT:
            j += 1
        if j - i >= 3:
            span_s, span_e = shots[i]["s"], shots[j - 1]["e"]
            mid = (span_s + span_e) / 2
            cam = "B" if in_cover(mid, wide_cover) else "A"
            merged.append({"cam": cam, "s": span_s, "e": span_e})
            i = j
        else:
            merged.append(shots[i])
            i += 1
    # absorb remaining too-short shots into their predecessor
    shots2 = []
    for sh_ in merged:
        if shots2 and sh_["e"] - sh_["s"] < MIN_SHOT:
            shots2[-1]["e"] = sh_["e"]
        elif shots2 and shots2[-1]["cam"] == sh_["cam"]:
            shots2[-1]["e"] = sh_["e"]
        else:
            shots2.append(sh_)
    # relief wides inside very long host shots
    final = []
    for sh_ in shots2:
        d = sh_["e"] - sh_["s"]
        if sh_["cam"] == "A" and d > LONG_SHOT:
            mid = (sh_["s"] + sh_["e"]) / 2
            if in_cover(mid, wide_cover) and in_cover(mid + WIDE_INSERT, wide_cover):
                final.append({"cam": "A", "s": sh_["s"], "e": mid})
                final.append({"cam": "B", "s": mid, "e": mid + WIDE_INSERT})
                final.append({"cam": "A", "s": mid + WIDE_INSERT, "e": sh_["e"]})
                continue
        final.append(sh_)
    json.dump(final, open(f"{OUT}/edl.json", "w"), indent=1)
    from collections import Counter
    print("shots:", len(final), Counter(x["cam"] for x in final), flush=True)
    for x in final[:12]:
        print(f'  {x["cam"]} {x["s"]:7.2f} -> {x["e"]:7.2f}', flush=True)

    # ---- render -----------------------------------------------------------
    print("=== render ===", flush=True)
    ch, cw = meta["cam-c"]["h"], meta["cam-c"]["w"]
    crop_h = int(cw * 9 / 16)
    # face sits in the upper part of the vertical frame (measured on stills)
    crop_y = max(0, int(0.185 * ch) - crop_h // 2)
    VF = {
        "A": f"scale={W}:{H}:flags=lanczos",
        "C": f"crop={cw}:{crop_h}:0:{crop_y},scale={W}:{H}:flags=lanczos",
        "B": f"scale={W}:{H}:flags=lanczos",
    }

    def src_for(cam, t):
        if cam == "A":
            return "cam-a"
        if cam == "C":
            return "cam-c"
        for name, s, e in bt_raw:
            if s <= t < e:
                return name
        return "cam-a"

    vlist = []
    for i, x in enumerate(final):
        cam, s, e = x["cam"], x["s"], x["e"]
        src = src_for(cam, s)
        if cam == "B" and src == "cam-a":
            cam = "A"
        local = s - offsets[src]
        d = e - s
        if local < 0:
            local, d = 0.0, d + local
        seg = f"v_{i:03d}.mp4"
        sh(f'ffmpeg -v error -y -ss {local:.3f} -t {d:.3f} -i {SOURCES[src][0]} '
           f'-vf "{VF[cam]},fps={FPS},setsar=1" -an '
           f'-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {seg}')
        dims = sh(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height '
                  f'-of csv=p=0 {seg}').strip()
        assert dims == f"{W},{H}", f"{seg}: {dims}"
        vlist.append(seg)
        if i % 25 == 0:
            print(f"shot {i}/{len(final)}", flush=True)
    open("vlist.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vlist.txt -c copy video_only.mp4')
    sh(f'ffmpeg -v error -y -i video_only.mp4 -i show_audio.wav '
       f'-map 0:v:0 -map 1:a:0 -t {content_end:.3f} '
       f'-c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart {OUT}/master.mp4')
    mdur = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master.mp4').strip())
    print(f"master: {mdur:.1f}s {os.path.getsize(OUT+'/master.mp4')/1e9:.2f} GB", flush=True)
    assert abs(mdur - content_end) < 2.0

    # ---- verification pack ------------------------------------------------
    print("=== verify ===", flush=True)
    os.makedirs(f"{OUT}/cuts", exist_ok=True)
    idxs = np.linspace(1, len(final) - 1, min(30, len(final) - 1)).astype(int)
    lines = []
    for k, i in enumerate(sorted(set(idxs))):
        t = final[i]["s"] + 0.4
        sh(f'ffmpeg -v error -y -ss {t:.2f} -i {OUT}/master.mp4 -frames:v 1 '
           f'-vf scale=320:-2 -q:v 5 {OUT}/cuts/cut{k:02d}_{final[i]["cam"]}_{t:.0f}.jpg')
        lines.append(f'cut{k:02d}: t={t:7.1f} cam={final[i]["cam"]}')
    open(f"{OUT}/cuts/index.txt", "w").write("\n".join(lines) + "\n")
    sh(f'ffmpeg -v error -y -ss 240 -t 180 -i {OUT}/master.mp4 '
       f'-vf scale=854:480 -c:v libx264 -preset veryfast -crf 27 '
       f'-c:a aac -b:a 96k {OUT}/preview.mp4')
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
