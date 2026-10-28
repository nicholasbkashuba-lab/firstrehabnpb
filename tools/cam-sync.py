#!/usr/bin/env python3
"""Sync a raw camera to the episode's RAW radio mp3 by audio cross correlation.

    python3 tools/cam-sync.py raw.mp3 camera.(mp4|mov|f32) [more cameras ...]

Prints, per camera, the line camera_time = rate * mp3_time + offset that
tools/reframe-clip.py and tools/recut-clip.py take as NAME=path:rate:offset. A .f32 file is
8 kHz mono float32 audio already pulled off the camera (for a 20 GB Dropbox file, extract it
once with: ffmpeg -i "<temporary link>" -map 0:a:0 -ac 1 -ar 8000 -f f32le cam.f32 — ffmpeg
range-reads only the audio, about 4 minutes for 12 GB).

Method: 20 s windows of camera audio every 45 s, each located in the mp3 by FFT cross
correlation; windows with a peak-to-sidelobe ratio under 12 are dropped (room noise, music
beds the camera never heard), then a line is fitted and refitted on the windows within
40 ms of it. Phones drift ~30 to 60 ppm against the board, so a single offset is off by
~0.1 s by the end of an episode; the rate term removes that.
"""
import subprocess
import sys

import numpy as np

SR = 8000


def load(path):
    if path.endswith(".f32"):
        return np.fromfile(path, np.float32)
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-map", "0:a:0", "-ac", "1", "-ar", str(SR),
                        "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32)


def sync(mp3, cam, win=20, hop=45):
    b = (mp3 - mp3.mean()) / (mp3.std() + 1e-9)
    n = 1 << int(np.ceil(np.log2(len(b) + win * SR)))
    B = np.fft.rfft(b, n)
    pts = []
    for c0 in range(0, len(cam) - win * SR, hop * SR):
        a = cam[c0:c0 + win * SR]
        if a.std() < 1e-4:
            continue
        a = (a - a.mean()) / a.std()
        r = np.fft.irfft(B * np.conj(np.fft.rfft(a, n)), n)[:len(b)]
        k = int(np.argmax(r))
        psr = (r[k] - r.mean()) / (r.std() + 1e-9)
        if psr >= 12:
            pts.append((k / SR, c0 / SR, psr))      # (mp3_t, cam_t, psr)
    if len(pts) < 3:
        return None
    m = np.array([p[0] for p in pts])
    c = np.array([p[1] for p in pts])
    keep = np.abs((c - m) - np.median(c - m)) < 1.0
    for _ in range(3):
        rate, off = np.polyfit(m[keep], c[keep], 1)
        res = c - (rate * m + off)
        keep = np.abs(res) < 0.04
        if keep.sum() < 3:
            return None
    return rate, off, int(keep.sum()), len(pts), float(np.abs(res[keep]).max())


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    mp3 = load(sys.argv[1])
    for cam in sys.argv[2:]:
        r = sync(mp3, load(cam))
        if r is None:
            print(f"{cam}: NO SYNC (camera audio does not match this mp3)")
        else:
            rate, off, k, n, res = r
            print(f"{cam}: rate {rate:.7f} offset {off:.4f}  ({k}/{n} windows, max resid {res * 1000:.0f} ms)")


if __name__ == "__main__":
    main()
