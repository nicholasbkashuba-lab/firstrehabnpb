#!/usr/bin/env python3
"""Measure how far each camera is offset from the board audio.

Ask Descript to align by waveform first — when it works, none of this is needed.
This exists for when it does not, and for recovering sync months later when the
edit project is gone but the raw files remain.

The method (proven on Episode 9, which measured -83.20s and -83.10s for the same
camera 22 minutes apart, SNR 195 and 119):

  1. Reduce both the board audio and the camera audio to mono 16 kHz.
  2. Take a short probe window out of the camera track.
  3. FFT cross-correlate the probe against the board audio.
  4. The peak's lag is where that probe sits on the show clock, so
     offset = camera_probe_time - board_time.
  5. Repeat far away in the recording. If the two offsets disagree by more than
     ~0.2s the cameras are drifting and a single offset will not hold.

Correlating whole multi-hour tracks is both slower and worse than correlating a
30s probe: a long window averages over drift and blurs the peak.

Two subcommands:

  extract   ffmpeg a source file down to mono 16 kHz WAV
  measure   cross-correlate camera WAVs against the board WAV

Needs numpy and ffmpeg, neither of which ships in this sandbox:
    pip3 install numpy && apt-get install -y ffmpeg

The cameras cannot be downloaded into this sandbox (Dropbox is proxy-blocked and
the files are tens of GB regardless). Run `extract` wherever the bytes are — a
GitHub Actions runner has open egress and enough disk — and push just the WAVs
back. A 30 minute mono 16 kHz WAV is about 57 MB, comfortably under GitHub's
100 MB blob limit, and you only need the probe windows.
"""
import argparse
import subprocess
import sys
import wave

SR = 16000


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"failed: {cmd}\n{r.stderr.strip()}")
    return r.stdout


def extract(src, dest, start=None, dur=None):
    """Mono 16 kHz WAV, optionally just a window."""
    seek = f"-ss {start} " if start is not None else ""
    length = f"-t {dur} " if dur is not None else ""
    # -ss before -i seeks by keyframe and is fast; accurate enough at 16 kHz.
    sh(f'ffmpeg -v error -y {seek}-i "{src}" {length}-vn -ac 1 -ar {SR} '
       f'-c:a pcm_s16le "{dest}"')
    print(f"{dest}")


def load(path):
    import numpy as np
    with wave.open(path, "rb") as w:
        if w.getframerate() != SR:
            sys.exit(f"{path}: expected {SR} Hz, got {w.getframerate()}")
        if w.getnchannels() != 1:
            sys.exit(f"{path}: expected mono")
        raw = w.readframes(w.getnframes())
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
    a -= a.mean()
    return a


def correlate(board, probe):
    """Return (lag_seconds, snr) for probe's best position within board."""
    import numpy as np
    n = 1
    while n < len(board) + len(probe):
        n <<= 1
    # Normalise each side so the peak height reflects match quality, not volume.
    b = board / (np.linalg.norm(board) or 1.0)
    p = probe / (np.linalg.norm(probe) or 1.0)
    corr = np.fft.irfft(np.fft.rfft(b, n) * np.conj(np.fft.rfft(p, n)), n)
    peak = int(np.argmax(corr))
    top = corr[peak]
    # SNR against the rest of the surface. A real match scores in the hundreds;
    # single digits means these two recordings do not share audio.
    mask = np.ones(len(corr), dtype=bool)
    lo, hi = max(0, peak - SR), min(len(corr), peak + SR)
    mask[lo:hi] = False
    noise = corr[mask].std() or 1e-12
    return peak / SR, float(top / noise)


def measure(board_path, cams, probes):
    board = load(board_path)
    print(f"board {board_path}  {len(board)/SR:.1f}s\n")
    for cam in cams:
        audio = load(cam)
        results = []
        for at in probes:
            s = int(at * SR)
            e = s + 30 * SR
            if e > len(audio):
                print(f"  {cam}: probe at {at}s is past the end, skipped")
                continue
            lag, snr = correlate(board, audio[s:e])
            offset = at - lag
            results.append((at, offset, snr))
            flag = "" if snr > 50 else "   <-- WEAK, do not trust"
            print(f"  {cam}  probe {at:7.1f}s  ->  offset {offset:+8.3f}s  "
                  f"snr {snr:6.1f}{flag}")
        if len(results) > 1:
            spread = max(r[1] for r in results) - min(r[1] for r in results)
            verdict = "no drift" if spread < 0.2 else "DRIFTING — one offset will not hold"
            print(f"  {cam}  spread {spread:.3f}s  {verdict}\n")
        else:
            print()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract", help="source file -> mono 16 kHz WAV")
    e.add_argument("src")
    e.add_argument("dest")
    e.add_argument("--start", type=float, help="seconds into the source")
    e.add_argument("--dur", type=float, help="seconds to keep")

    m = sub.add_parser("measure", help="cross-correlate cameras against the board audio")
    m.add_argument("--board", required=True, help="board audio WAV (the show clock)")
    m.add_argument("--cam", action="append", required=True, dest="cams",
                   help="camera WAV; repeat per camera")
    m.add_argument("--probe", action="append", type=float, dest="probes",
                   help="seconds into the CAMERA to probe from; repeat, use two "
                        "far apart to prove there is no drift (default 300 and 1500)")

    a = ap.parse_args()
    if a.cmd == "extract":
        extract(a.src, a.dest, a.start, a.dur)
    else:
        measure(a.board, a.cams, a.probes or [300.0, 1500.0])


if __name__ == "__main__":
    main()
