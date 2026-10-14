"""Trailer sound design, synthesized from scratch (no licensed samples).

Everything returns float32 mono or stereo arrays at SR. A Score collects events
onto two buses: `music` (ducked under dialogue) and `sfx` (hits that punch through).
"""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
rng = np.random.default_rng(7)


def _t(d):
    return np.arange(int(d * SR)) / SR


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def noise(d):
    return rng.standard_normal(int(d * SR)).astype(np.float64)


def sine_sweep(d, f0, f1, tau):
    t = _t(d)
    f = f1 + (f0 - f1) * np.exp(-t / tau)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def saw(f, t, phase=0.0):
    x = (f * t + phase) % 1.0
    return 2 * x - 1


_IR = {}


def reverb_ir(seconds=2.6, bright=6000):
    key = (seconds, bright)
    if key not in _IR:
        t = _t(seconds)
        env = np.exp(-t / (seconds / 6.5))
        l = lp(noise(seconds), bright) * env
        r = lp(noise(seconds), bright) * env
        l[0] = r[0] = 0
        _IR[key] = np.stack([l, r]) / np.sqrt(np.sum(l ** 2))
    return _IR[key]


def verb(x, wet=0.35, seconds=2.6, bright=6000):
    ir = reverb_ir(seconds, bright)
    if x.ndim == 1:
        x = np.stack([x, x])
    out = np.zeros((2, x.shape[1] + ir.shape[1] - 1))
    out[:, : x.shape[1]] += x * (1 - wet)
    for c in range(2):
        out[c] += wet * fftconvolve(x[c], ir[c])
    return out


# ---------------------------------------------------------------- instruments
def kick(g=1.0):
    d = 0.5
    t = _t(d)
    body = sine_sweep(d, 160, 46, 0.035) * np.exp(-t / 0.22)
    click = hp(noise(d), 3000) * np.exp(-t / 0.004) * 0.35
    return np.tanh(2.2 * (body + click)) * 0.9 * g


def sub808(f=55.0, d=0.9, g=1.0):
    t = _t(d)
    x = sine_sweep(d, f * 1.6, f, 0.02) * np.exp(-t / (d * 0.55))
    x *= np.minimum(1, t / 0.004)
    return np.tanh(2.0 * x) / np.tanh(2.0) * 0.8 * g


def snare(g=1.0):
    d = 0.35
    t = _t(d)
    n = bp(noise(d), 1500, 9000) * np.exp(-t / 0.09)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.6
    return np.tanh(1.6 * (n * 0.8 + tone)) * 0.7 * g


def clap(g=1.0):
    d = 0.4
    t = _t(d)
    env = np.zeros_like(t)
    for k, off in enumerate((0, 0.011, 0.022)):
        m = t >= off
        env[m] += np.exp(-(t[m] - off) / (0.006 if k < 2 else 0.11))
    return bp(noise(d), 900, 4500) * env * 0.9 * g


def hat(open_=False, g=1.0):
    d = 0.3 if open_ else 0.08
    t = _t(d)
    return hp(noise(d), 7500, 4) * np.exp(-t / (0.09 if open_ else 0.018)) * 0.45 * g


def tom(f, g=1.0):
    d = 0.45
    t = _t(d)
    return np.tanh(1.5 * sine_sweep(d, f * 1.5, f, 0.03) * np.exp(-t / 0.16)) * 0.8 * g


def crash(d=2.2, g=1.0):
    t = _t(d)
    n = hp(noise(d), 2800, 2) * np.exp(-t / 0.55)
    ring = sum(np.sin(2 * np.pi * f * t + rng.random() * 6) for f in (3170, 4510, 5930, 7220)) * 0.05 * np.exp(-t / 0.8)
    return (n * 0.5 + ring) * g


def boom(g=1.0, tail=2.8):
    """The big trailer hit: sub drop + low thump + metallic body, in a hall."""
    d = tail
    t = _t(d)
    sub = sine_sweep(d, 75, 30, 0.45) * np.exp(-t / 1.1)
    thump = lp(noise(d), 220, 4) * np.exp(-t / 0.18) * 2.5
    metal = bp(noise(d), 180, 2600) * np.exp(-t / 0.35) * 0.6
    dry = np.tanh(1.8 * (sub * 1.1 + thump + metal))
    return verb(dry * g, wet=0.4, seconds=3.2, bright=3500)


def braam(d=2.6, root=55.0, g=1.0):
    t = _t(d)
    x = np.zeros_like(t)
    for f in (root, root * 1.5, root * 2, root * 0.5):
        for det in (-0.006, 0.0, 0.0065):
            x += saw(f * (1 + det), t, rng.random())
    # filter opens then closes: chunked time-varying lowpass
    out = np.zeros_like(x)
    cut = 180 + 2200 * np.minimum(1, t / 0.25) * np.exp(-np.maximum(0, t - 0.25) / 0.9)
    blk = 1024
    for i in range(0, len(x), blk):
        c = float(cut[i])
        out[i:i + blk] = lp(x[i:i + blk + 2048], max(60, c), 2)[: len(x[i:i + blk])]
    amp = np.minimum(1, t / 0.04) * np.exp(-t / (d * 0.45))
    dry = np.tanh(0.5 * out * amp) * 0.9
    return verb(dry * g, wet=0.45, seconds=3.0, bright=4000)


def riser(d=2.0, g=1.0):
    t = _t(d)
    n = noise(d)
    out = np.zeros_like(n)
    blk = 2048
    for i in range(0, len(n), blk):
        p = i / len(n)
        c = 300 * (8000 / 300) ** p
        out[i:i + blk] = bp(n[i:i + blk], c * 0.7, min(c * 1.4, 20000), 2)
    f = 180 * (6.5) ** (t / d)
    tone = sum(np.sin(2 * np.pi * np.cumsum(f * m) / SR) for m in (1, 1.5, 2.01)) * 0.25
    env = (t / d) ** 2.2
    return verb((out * 1.2 + tone) * env * g, wet=0.3, seconds=1.5)


def whoosh(d=0.55, g=1.0, up=False):
    t = _t(d)
    n = noise(d)
    out = np.zeros_like(n)
    blk = 1024
    for i in range(0, len(n), blk):
        p = i / len(n)
        p = p if up else 1 - p
        c = 350 * (6000 / 350) ** p
        out[i:i + blk] = bp(n[i:i + blk], c * 0.6, min(c * 1.6, 20000), 2)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    return out * env * 0.8 * g


def tick(g=1.0):
    d = 0.05
    t = _t(d)
    return (np.sin(2 * np.pi * 2300 * t) * np.exp(-t / 0.006) + hp(noise(d), 4000) * np.exp(-t / 0.003) * 0.4) * 0.5 * g


def reverse_swell(d=1.2, g=1.0):
    c = crash(d, 1.0)
    return verb(c[::-1].copy() * g, wet=0.3, seconds=1.2)


def pad(d, notes, g=1.0, attack=1.2):
    t = _t(d)
    x = np.zeros_like(t)
    for f in notes:
        for det in (-0.004, 0.004):
            x += saw(f * (1 + det), t, rng.random())
    x = lp(x, 900, 2)
    env = np.minimum(1, t / attack) * np.minimum(1, (d - t) / 0.6).clip(0)
    return verb(x * env * 0.08 * g, wet=0.5, seconds=3.0, bright=3000)


def stab(notes, d=0.5, g=1.0):
    t = _t(d)
    x = sum(saw(f, t, rng.random()) for f in notes)
    x = lp(x, 2500, 2) * np.exp(-t / 0.12)
    return verb(x * 0.18 * g, wet=0.35, seconds=1.8)


# ---------------------------------------------------------------- score
class Score:
    def __init__(self, dur):
        self.n = int(dur * SR) + SR * 4
        self.music = np.zeros((2, self.n))
        self.sfx = np.zeros((2, self.n))
        self.dlg = np.zeros((2, self.n))
        self.stops = []
        self.mutes = []
        self.dlg_gain = 1.7

    def _add(self, bus, x, t, g=1.0, pan=0.0):
        if x.ndim == 1:
            l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan))
            x = np.stack([x * l * 1.414, x * r * 1.414])
        i = int(round(t * SR))
        if i < 0:
            x = x[:, -i:]
            i = 0
        j = min(self.n, i + x.shape[1])
        bus[:, i:j] += x[:, : j - i] * g

    def m(self, x, t, g=1.0, pan=0.0):
        self._add(self.music, x, t, g, pan)

    def s(self, x, t, g=1.0, pan=0.0):
        self._add(self.sfx, x, t, g, pan)

    def d(self, x, t, g=1.0):
        self._add(self.dlg, x, t, g)

    # beat helpers --------------------------------------------------------
    def groove(self, t0, t1, bpm=128, style="trap", g=1.0, root=55.0):
        b = 60 / bpm
        step = b / 4
        k = 0
        t = t0
        bass_notes = [root, root, root * 1.189, root * 0.891]  # i, i, iii-ish, vii
        while t < t1 - 1e-6:
            bar_pos = k % 16
            bar = k // 16
            if style == "trap":
                if bar_pos in (0, 7, 10):
                    self.m(kick(), t, 0.9 * g)
                    self.m(sub808(bass_notes[bar % 4], 0.6 if bar_pos else 0.9), t, 0.75 * g)
                if bar_pos in (4, 12):
                    self.m(clap(), t, 0.7 * g, pan=0.1)
                    self.m(snare(), t, 0.45 * g)
                hh = 0.33 * g * (1.0 if bar_pos % 2 == 0 else 0.6)
                self.m(hat(), t, hh, pan=0.3)
                if bar_pos in (13, 15) and bar % 2:
                    self.m(hat(), t + step / 2, 0.25 * g, pan=0.3)
            else:  # four on the floor drive
                if bar_pos % 4 == 0:
                    self.m(kick(), t, 0.95 * g)
                    self.m(sub808(bass_notes[bar % 4], 0.45), t, 0.55 * g)
                if bar_pos in (4, 12):
                    self.m(clap(), t, 0.65 * g)
                if bar_pos % 4 == 2:
                    self.m(hat(open_=True), t, 0.3 * g, pan=-0.2)
                self.m(hat(), t, 0.18 * g, pan=0.3)
            k += 1
            t = t0 + k * step

    def ticks(self, t0, t1, bpm=128, g=0.6):
        b = 60 / bpm / 2
        k = 0
        while t0 + k * b < t1:
            self.m(tick(), t0 + k * b, g * (1.0 if k % 2 == 0 else 0.6), pan=0.25 if k % 2 else -0.25)
            k += 1

    def tapestop(self, t, d=0.45, until=None):
        """Slow the music bus to a halt at t, silent until `until` (events after it play)."""
        self.stops.append((t, d, until if until is not None else self.n / SR))

    def mute(self, t0, t1):
        self.mutes.append((t0, t1))

    # mixdown -------------------------------------------------------------
    def mix(self, music=True):
        """music=False drops the music bed but keeps the sound effects (booms, whooshes,
        rimshots, stings) under the dialogue, for laying a licensed track under it in-app."""
        mus = self.music.copy() if music else np.zeros_like(self.music)
        for t, d, until in self.stops:
            i = int(t * SR)
            L = int(d * SR)
            rate = np.linspace(1, 0, L) ** 1.3
            pos = i + np.cumsum(rate)
            seg = np.stack([np.interp(pos, np.arange(self.n), mus[c]) for c in range(2)])
            seg *= np.linspace(1, 0, L) ** 0.5
            mus[:, i:i + L] = seg
            mus[:, i + L:int(until * SR)] = 0
        for t0, t1 in self.mutes:
            a, b = int(t0 * SR), int(t1 * SR)
            mus[:, a:b] = 0
            self.sfx[:, a:b] *= 0
        # sidechain duck music under dialogue
        env = np.abs(self.dlg).max(axis=0)
        win = int(0.05 * SR)
        env = np.convolve(env, np.ones(win) / win, mode="same")
        env = (env > 0.01).astype(float)
        sm = int(0.12 * SR)
        env = np.convolve(env, np.ones(sm) / sm, mode="same")
        # Owner (2026-10-14): Mike's voiceover was too quiet. Music now ducks to ~20% under
        # any voice and dialogue gets +4.5 dB before the -14 LUFS normalisation.
        duck = 1 - 0.8 * np.clip(env, 0, 1)
        sfx_duck = 1 - 0.45 * np.clip(env, 0, 1)
        out = mus * duck + self.sfx * sfx_duck + self.dlg * self.dlg_gain
        return out
