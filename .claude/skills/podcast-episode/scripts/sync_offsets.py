#!/usr/bin/env python3
"""Measure how far each camera is offset from the board audio.

Ask Descript to align by waveform first — when it works, none of this is needed.
This exists for when it does not, and for recovering sync months later when the
edit project is gone but the raw files remain.

The method:

  1. Reduce every track to mono 16 kHz WAV (`extract`).
  2. Take a probe window out of one track.
  3. FFT cross-correlate it against the reference.
  4. The peak's lag says where that probe sits on the reference clock, so
     offset = probe_time - lag.
  5. Repeat far apart. Offsets that disagree mean drift, and no single offset
     will hold.

**Correlate ENVELOPES, not raw samples.** Raw-sample correlation only works when
both recordings are essentially the same signal. Different microphones in the
same room are not: Episode 10 scored SNR 9-19 on raw samples with offsets
disagreeing by 790 seconds. The speech energy envelope survives different mics,
placement and AGC, because everyone gets loud and quiet at the same instants.
Camera-to-camera then scored SNR 20-31 with a 5 millisecond spread.

**A rate mismatch looks like a bad measurement, not like drift.** If offsets grow
steadily with probe position rather than scattering, the two recordings run at
different speeds and NO offset exists. Search the rate before concluding the
audio does not match:

    for rate in ...: stretch reference by rate, correlate, keep the sharpest peak

Episode 10's board feed was time-compressed exactly 3% for its radio slot
(rate 1/0.97). All three cameras independently agreed on 1.0309 at SNR 107-143.
Correct it with `atempo=0.97`, which preserves pitch, and the offset becomes
constant to within 6 milliseconds. `asetrate` also aligns but shifts pitch;
prefer atempo, and verify by checking that raw-sample correlation improves.

Beware false peaks: on raw samples anything under SNR ~15 is noise, even though
the envelope pass is trustworthy down to ~12. Take the MEDIAN of several probes
and look at the spread rather than trusting any single number.

Two subcommands:

  extract   ffmpeg a source file down to mono 16 kHz WAV
  measure   cross-correlate WAVs against a reference WAV

Needs numpy and ffmpeg, neither of which ships in this sandbox:
    pip3 install numpy && apt-get update && apt-get install -y ffmpeg
(the apt index is stale on a fresh box, so the update is not optional)

Dropbox is reachable as of 2026-08-15, so pull the cameras straight down with
tools/dropbox-grab.py, extract the audio, and delete the video — a 30 minute
mono 16 kHz WAV is about 57 MB, against 12 GB of 4K.
"""
import argparse
import subprocess
import sys
import wave

SR = 16000
# Envelope sample rate. 200 Hz gives 5ms resolution, well inside one video
# frame at 30fps, while making the correlation cheap enough to probe repeatedly.
ENV_RATE = 200


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


def envelope(sig, rate=ENV_RATE):
    """Speech energy envelope, downsampled to `rate` Hz.

    Correlating raw samples only works when both recordings are essentially the
    same signal. A board feed and a camera's on-board mic are NOT: different
    microphones, different placement in the room, different AGC. Episode 10
    scored SNR 9-19 on raw samples with offsets disagreeing by 790s — confidently
    useless.

    What survives all of that is the ENVELOPE: speech gets loud and quiet at the
    same instants on every microphone in the room. Rectify, smooth, downsample,
    and correlate that instead.
    """
    import numpy as np
    step = SR // rate
    n = (len(sig) // step) * step
    if n == 0:
        return np.zeros(0)
    # RMS per step is steadier than mean-abs when one mic is much hotter.
    blocks = sig[:n].reshape(-1, step)
    env = np.sqrt((blocks.astype(np.float64) ** 2).mean(axis=1))
    # Log compression stops one loud laugh from dominating the correlation.
    env = np.log1p(env)
    return env - env.mean()


def correlate(board, probe, rate=ENV_RATE):
    """Return (lag_seconds, snr) for probe's best position within board.

    Both inputs are envelopes at `rate` Hz, not raw samples.
    """
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
    # SNR against the rest of the surface. Exclude a second either side of the
    # peak so the peak's own shoulders do not inflate the noise floor.
    mask = np.ones(len(corr), dtype=bool)
    lo, hi = max(0, peak - rate), min(len(corr), peak + rate)
    mask[lo:hi] = False
    noise = corr[mask].std() or 1e-12
    return peak / rate, float(top / noise)


def measure(board_path, cams, probes, window=120.0):
    board_env = envelope(load(board_path))
    print(f"board {board_path}  {len(board_env)/ENV_RATE:.1f}s  "
          f"(envelope at {ENV_RATE} Hz, {window:.0f}s probes)\n")
    for cam in cams:
        cam_env = envelope(load(cam))
        results = []
        for at in probes:
            s = int(at * ENV_RATE)
            e = s + int(window * ENV_RATE)
            if e > len(cam_env):
                print(f"  {cam}: probe at {at}s is past the end, skipped")
                continue
            lag, snr = correlate(board_env, cam_env[s:e])
            offset = at - lag
            results.append((at, offset, snr))
            flag = "" if snr > 12 else "   <-- WEAK, do not trust"
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
    m.add_argument("--window", type=float, default=120.0,
                   help="probe length in seconds (default 120). Envelopes carry "
                        "less information per second than raw audio, so they need "
                        "a longer window than you would expect.")

    a = ap.parse_args()
    if a.cmd == "extract":
        extract(a.src, a.dest, a.start, a.dur)
    else:
        measure(a.board, a.cams, a.probes or [300.0, 1500.0], a.window)


if __name__ == "__main__":
    main()
