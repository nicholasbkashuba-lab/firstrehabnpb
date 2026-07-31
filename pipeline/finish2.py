#!/usr/bin/env python3
"""v4 — the delivery cut of the Sabesan episode.

On top of v3 (tonemapped SDR, corrected guest crop) this:
  1. starts the show at Mike's "Good morning..." (t=89.77 in cam-a time) —
     everything before is pre-show chatter Nick asked to drop
  2. tightens dead air: inter-segment gaps > 1.0s are shortened to 0.45s
  3. re-identifies speakers with ECAPA voice embeddings + clustering.
     v1's pitch-only rule misread announcer-Mike as the guest (projected
     voice), so the intro cut to the wrong camera. Embeddings key on voice
     identity, not delivery. Pitch is only used afterwards to decide WHICH
     cluster is Dr. Sabesan (the one female voice).
  4. hides every tightening splice with a camera change — wide 3-shot where
     cam-b/fragments have coverage, otherwise a brief reaction shot
  5. forces exact per-shot frame counts (round(e*fps)-round(s*fps)) so
     rounding cannot accumulate into A/V drift across many splices — the
     failure mode that killed the fixc experiment.

Audio content comes from the v1/v3 master's continuous track (the verified
BT/fallback patchwork), re-cut to the kept spans with 15 ms edge fades.
"""
import json, os, subprocess

import numpy as np

WORK = os.environ.get("WORK", "/mnt/work")
OUT = os.path.join(WORK, "out")
FPS, W, H = 30, 1920, 1080
SHOW_START = 89.27            # 0.5s of air before "Good morning..."
GAP_TRIM, GAP_KEEP = 1.0, 0.45
MIN_SHOT = 2.4
COVER_LEN = 3.0               # cover-shot length at a tightening splice

OFFSETS = {"cam-a": 0.0, "cam-b": 80.674, "cam-c": 83.874,
           "f1087": 1086.516, "f1233": 1232.979, "f1527": 1526.617}
DUR = {"cam-b": 886.02, "f1087": 60.08, "f1233": 280.37, "f1527": 254.66}
WIDE = ["cam-b", "f1087", "f1233", "f1527"]

TONEMAP = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
           "tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
COLOR_TAGS = "-colorspace bt709 -color_primaries bt709 -color_trc bt709"
PRE = {"A": f"scale={W}:{H}:flags=lanczos",
       "B": f"scale={W}:{H}:flags=lanczos",
       "C": f"crop=2160:1215:0:589,scale={W}:{H}:flags=lanczos"}


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
    segs = json.load(open("transcript.json"))

    # ---- speaker re-ID: ECAPA embeddings + clustering ---------------------
    print("=== speaker re-id ===", flush=True)
    sh('ffmpeg -v error -y -i master.mp4 -map 0:a:0 -ac 1 -ar 16000 show16k.wav')
    import torch
    from speechbrain.inference.speaker import EncoderClassifier
    enc = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb",
                                         savedir="/tmp/ecapa")
    # decode via ffmpeg — torchaudio.load now needs torchcodec, which we don't
    raw = subprocess.run('ffmpeg -v error -i show16k.wav -f f32le -',
                         shell=True, capture_output=True).stdout
    wav = torch.from_numpy(np.frombuffer(raw, dtype=np.float32).copy()).unsqueeze(0)
    embs, idxs = [], []
    for i, s in enumerate(segs):
        a, b = s["s"], s["e"]
        if b - a < 0.6:
            continue
        mid = (a + b) / 2
        a2, b2 = max(a, mid - 1.5), min(b, mid + 1.5)
        chunk = wav[:, int(a2 * 16000): int(b2 * 16000)]
        with torch.no_grad():
            e = enc.encode_batch(chunk).squeeze().numpy()
        embs.append(e / (np.linalg.norm(e) + 1e-9))
        idxs.append(i)
    X = np.stack(embs)
    from sklearn.cluster import KMeans
    km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
    lab = km.labels_
    # which cluster is Dr. Sabesan? the one with the highest median f0
    med = {}
    for c in range(3):
        f0s = [segs[idxs[j]]["f0"] for j in range(len(idxs))
               if lab[j] == c and segs[idxs[j]].get("f0")]
        med[c] = np.median(f0s) if f0s else 0
        print(f"cluster {c}: n={int((lab==c).sum())} f0med={med[c]:.0f}", flush=True)
    guest = max(med, key=med.get)
    assert med[guest] >= 150, f"no plausible female cluster ({med})"
    for j, i in enumerate(idxs):
        segs[i]["spk2"] = "G" if lab[j] == guest else "H"
    prev = "H"
    for s in segs:                       # short segments inherit their neighbour
        if "spk2" not in s:
            s["spk2"] = prev
        prev = s["spk2"]
    flips = sum(1 for s in segs if s["spk2"] != s["spk"])
    gshare = sum(1 for s in segs if s["spk2"] == "G") / len(segs)
    print(f"re-id changed {flips}/{len(segs)} labels; guest share {gshare:.2f}", flush=True)
    assert 0.15 < gshare < 0.85, "embedding split degenerate"
    json.dump(segs, open(f"{OUT}/transcript_v4.json", "w"), indent=1)

    # ---- kept spans (head trim + pause tightening) ------------------------
    live = [s for s in segs if s["e"] > SHOW_START]
    content_end = min(live[-1]["e"] + 2.0, 1807.4)
    spans, cur = [], SHOW_START
    removed = 0.0
    for a, b in zip(live, live[1:]):
        gap = b["s"] - a["e"]
        if gap > GAP_TRIM:
            spans.append((cur, a["e"] + GAP_KEEP / 2))
            cur = b["s"] - GAP_KEEP / 2
            removed += gap - GAP_KEEP
    spans.append((cur, content_end))
    total_out = sum(e - s for s, e in spans)
    print(f"{len(spans)} spans, tightened {removed:.1f}s, runtime {total_out/60:.1f} min",
          flush=True)

    # ---- shots ------------------------------------------------------------
    def cam_of(seg):
        if seg["spk2"] == "G" and 83.874 <= seg["s"] < 1813:
            return "C"
        return "A"

    shots = []          # (cam, show_s, show_e, span_idx)
    for si, (ss, se) in enumerate(spans):
        inside = [s for s in live if s["e"] > ss and s["s"] < se]
        cur_shots = []
        for seg in inside:
            cam = cam_of(seg)
            a, b = max(seg["s"], ss), min(seg["e"], se)
            if cur_shots and cur_shots[-1][0] == cam:
                cur_shots[-1][2] = b
            else:
                cur_shots.append([cam, a, b])
        if not cur_shots:
            cur_shots = [["A", ss, se]]
        cur_shots[0][1] = ss
        for k in range(len(cur_shots) - 1):
            cur_shots[k][2] = cur_shots[k + 1][1]
        cur_shots[-1][2] = se
        # absorb sub-minimum shots
        merged = []
        for c in cur_shots:
            if merged and (c[2] - c[1] < MIN_SHOT or merged[-1][0] == c[0]):
                merged[-1][2] = c[2]
            else:
                merged.append(c)
        # opening of the whole show: wide 3-shot for the greeting
        if si == 0 and wide_src(ss):
            head = min(8.0, merged[0][2] - ss)
            merged = [["B", ss, ss + head]] + \
                     [c for c in merged if c[2] > ss + head]
            if len(merged) > 1:
                merged[1][1] = ss + head
        # splice cover: if this span starts on the same cam the previous span
        # ended on, swap in a cover shot so the tightening cut reads as a
        # normal camera change
        if shots and merged[0][0] == shots[-1][0] and si > 0:
            cov = "B" if wide_src(ss) else ("C" if merged[0][0] == "A" else "A")
            cl = min(COVER_LEN, merged[0][2] - ss)
            merged = [[cov, ss, ss + cl]] + [c for c in merged if c[2] > ss + cl]
            if len(merged) > 1:
                merged[1][1] = ss + cl
        for c in merged:
            shots.append([c[0], c[1], c[2], si])
    from collections import Counter
    print("shots:", len(shots), Counter(s[0] for s in shots), flush=True)

    # ---- audio ------------------------------------------------------------
    print("=== audio ===", flush=True)
    sh('ffmpeg -v error -y -i master.mp4 -map 0:a:0 -c copy audio_full.m4a')
    alist = []
    for i, (ss, se) in enumerate(spans):
        d = se - ss
        w = f"a_{i:03d}.wav"
        sh(f'ffmpeg -v error -y -ss {ss:.3f} -t {d:.3f} -i audio_full.m4a '
           f'-af "afade=t=in:st=0:d=0.015,afade=t=out:st={d-0.015:.3f}:d=0.015" '
           f'-ar 48000 -ac 2 -c:a pcm_s16le {w}')
        alist.append(w)
    open("alist.txt", "w").write("".join(f"file '{a}'\n" for a in alist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i alist.txt -c copy audio_v4.wav')
    adur = float(sh('ffprobe -v error -show_entries format=duration -of csv=p=0 audio_v4.wav').strip())
    assert abs(adur - total_out) < 0.5, f"audio {adur} vs plan {total_out}"

    # ---- video ------------------------------------------------------------
    print("=== video ===", flush=True)
    hdrmap = {}
    vlist, out_t = [], 0.0
    for i, (cam, ss, se, si) in enumerate(shots):
        src = {"A": "cam-a", "C": "cam-c"}.get(cam) or wide_src(ss) or "cam-a"
        vcam = cam if cam != "B" or src != "cam-a" else "A"
        if src not in hdrmap:
            d = json.loads(sh(f'ffprobe -v error -show_streams -of json {src}.mov'))
            v = next(x for x in d["streams"] if x.get("codec_type") == "video" and x.get("width"))
            hdrmap[src] = v.get("color_transfer") in ("arib-std-b67", "smpte2084") \
                or v.get("color_primaries") == "bt2020"
        n = round((out_t + (se - ss)) * FPS) - round(out_t * FPS)
        out_t += se - ss
        if n <= 0:          # sub-frame sliver: contributes no frames by definition
            continue
        local = ss - OFFSETS[src]
        chain = PRE[vcam] + ("," + TONEMAP if hdrmap[src] else ",format=yuv420p")
        seg = f"v_{i:03d}.mp4"
        sh(f'ffmpeg -v error -y -ss {max(0,local):.3f} -i {src}.mov '
           f'-vf "{chain},fps={FPS},setsar=1" -frames:v {n} -an '
           f'-c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p {COLOR_TAGS} {seg}')
        got = int(sh(f'ffprobe -v error -select_streams v:0 -count_packets '
                     f'-show_entries stream=nb_read_packets -of csv=p=0 {seg}').strip())
        assert got == n, f"{seg}: {got} frames != {n}"
        vlist.append(seg)
        if i % 15 == 0:
            print(f"shot {i}/{len(shots)}", flush=True)
    open("vlist.txt", "w").write("".join(f"file '{v}'\n" for v in vlist))
    sh('ffmpeg -v error -y -f concat -safe 0 -i vlist.txt -c copy video_v4.mp4')
    sh(f'ffmpeg -v error -y -i video_v4.mp4 -i audio_v4.wav -map 0:v:0 -map 1:a:0 '
       f'-c:v copy -c:a aac -b:a 192k -movflags +faststart {OUT}/master.mp4')
    vdur = float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/master.mp4').strip())
    print(f"v4 master {vdur/60:.2f} min (plan {total_out/60:.2f})", flush=True)
    assert abs(vdur - total_out) < 0.5
    tags = sh(f'ffprobe -v error -select_streams v:0 -show_entries '
              f'stream=color_transfer,color_primaries -of csv=p=0 {OUT}/master.mp4').strip()
    assert "bt2020" not in tags and "arib" not in tags, "HDR tags leaked"

    # ---- verification pack ------------------------------------------------
    edl_out = []
    t = 0.0
    for cam, ss, se, si in shots:
        edl_out.append({"cam": cam, "out_s": round(t, 2), "show_s": round(ss, 2),
                        "d": round(se - ss, 2)})
        t += se - ss
    json.dump(edl_out, open(f"{OUT}/edl_v4.json", "w"), indent=1)
    json.dump([{"s": round(s, 2), "e": round(e, 2)} for s, e in spans],
              open(f"{OUT}/spans_v4.json", "w"), indent=1)
    os.makedirs(f"{OUT}/cuts", exist_ok=True)
    for i, x in enumerate(edl_out):
        if i % 3:
            continue
        tt = x["out_s"] + min(0.5, x["d"] / 2)
        sh(f'ffmpeg -v error -y -ss {tt:.2f} -i {OUT}/master.mp4 -frames:v 1 '
           f'-vf scale=280:-2 -q:v 5 {OUT}/cuts/s{i:03d}_{x["cam"]}.jpg')
    sh(f'ffmpeg -v error -y -t 120 -i {OUT}/master.mp4 -vf scale=854:480 '
       f'-c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 96k {OUT}/preview_open.mp4')
    sh(f'ffmpeg -v error -y -ss 600 -t 120 -i {OUT}/master.mp4 -vf scale=854:480 '
       f'-c:v libx264 -preset veryfast -crf 27 -c:a aac -b:a 96k {OUT}/preview_mid.mp4')
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
