import wave
import numpy as np
import sys

def load(path):
    with wave.open(path, 'rb') as w:
        sr = w.getframerate()
        n = w.getnframes()
        data = w.readframes(n)
        arr = np.frombuffer(data, dtype=np.int16).astype(np.float64)
        return arr, sr

a, sr_a = load('master.wav')
b, sr_b = load('dave.wav')
if sr_a != sr_b:
    print(f"SAMPLE_RATE_MISMATCH master={sr_a} dave={sr_b}", file=sys.stderr)
    sys.exit(1)
sr = sr_a

print(f"master_len_sec={len(a)/sr:.2f} dave_len_sec={len(b)/sr:.2f} sr={sr}")

a = a - a.mean()
b = b - b.mean()

n = 1
target = len(a) + len(b)
while n < target:
    n *= 2

A = np.fft.rfft(a, n)
B = np.fft.rfft(b, n)
corr = np.fft.irfft(A * np.conj(B), n)
corr_full = np.concatenate((corr[-(len(b)-1):], corr[:len(a)]))
lag = int(np.argmax(np.abs(corr_full))) - (len(b) - 1)
offset_sec = lag / sr
peak = float(np.max(np.abs(corr_full)))
noise = float(np.std(corr_full))
snr = peak / noise if noise > 0 else float('inf')

print(f"LAG_SAMPLES={lag}")
print(f"OFFSET_SECONDS={offset_sec:.4f}")
print(f"SNR={snr:.2f}")
print("Interpretation: positive OFFSET_SECONDS means dave audio lags behind master (dave clip should be shifted EARLIER by this many seconds to align). Negative means dave leads master (shift dave LATER).")
