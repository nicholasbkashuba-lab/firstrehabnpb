"""Sizzle-reel compositor.

A reel is a list of shots (each a slice of an episode master, with a focus point and a
push-in), plus timed text, captions and hit effects, plus a synthesized Score.
render(reel, fmt) streams source frames out of ffmpeg, composites them in numpy/PIL,
and pipes the result straight into an x264 encode muxed with the mixed audio.

Formats: '16x9' (1920x1080, thin cinematic bars), '9x16' (1080x1920, picture band with
type above/below), 'hero' (1920x1080 clean: no bars, no type, no audio).
"""
import math
import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from synth import SR

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
# Work dir holds src/<ep>/master.mp4, src/ep13/*.mp4 (Kerry clips), fonts/*.ttf and out/.
# None of it is committed (masters are GBs); see tools/sizzle/README.md to rebuild it.
SCR = os.environ.get("SIZZLE_WORK", os.path.expanduser("~/sizzle-work"))
SRC = {e: f"{SCR}/src/{e}/master.mp4" for e in ("ep9", "ep11", "ep14", "ep15", "ep16")}
SIZE = {"ep9": (1920, 1080), "ep11": (1920, 1080), "ep14": (1920, 1080), "ep15": (1280, 720), "ep16": (1920, 1080)}
for k in ("amazon_boxes_birthday", "captain_kerry_workout_branding", "depression_stats_why_kerry_matters",
          "dogs_and_vets_charity", "yacht_wakeup_moment"):
    SRC["k_" + k] = f"{SCR}/src/ep13/{k}.mp4"
    SIZE["k_" + k] = (1080, 1920)
# Kerry clips carry burned captions from y~1330 down; never crop below this.
REGION = {k: (0, 0, 1080, 1300) for k in SIZE if k.startswith("k_")}
# Ep16 Mike camera is a vertical inset on a blurred fill; this is the inset.
INSET16 = (656, 0, 1264, 1080)

INTER_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
INTER_XB = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
PLAYFAIR_I = f"{SCR}/fonts/playfair-display-latin-600-italic.ttf"
PLAYFAIR_B = f"{SCR}/fonts/playfair-display-latin-700-normal.ttf"

CREAM = (246, 241, 231)
GOLD = (233, 196, 106)
CORAL = (244, 162, 97)
TEAL = (14, 58, 71)
INK = (6, 22, 28)

FORMATS = {
    "16x9": dict(W=1920, H=1080, band=(0, 60, 1920, 1020), bars=True, text=True),
    "9x16": dict(W=1080, H=1920, band=(0, 300, 1080, 1650), bars=False, text=True),
    "hero": dict(W=1920, H=1080, band=(0, 0, 1920, 1080), bars=False, text=False),
}


# ------------------------------------------------------------------ helpers
def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def font(path, size):
    return ImageFont.truetype(path, int(size))


def text_img(lines, W, color=CREAM, stroke=0, stroke_color=(0, 0, 0), track=0.0, align="center", shadow=True):
    """lines: list of (text, fontpath, size, color|None). Returns RGBA image sized to content."""
    rendered = []
    for txt, fp, sz, col in lines:
        f = font(fp, sz)
        tr = sz * track
        widths = [f.getlength(ch) for ch in txt]
        w = int(sum(widths) + tr * max(0, len(txt) - 1)) + stroke * 2 + 8
        asc, desc = f.getmetrics()
        h = asc + desc + stroke * 2
        im = Image.new("RGBA", (max(1, w), h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        x = stroke + 4
        for ch, cw in zip(txt, widths):
            d.text((x, stroke), ch, font=f, fill=(col or color) + (255,), stroke_width=stroke,
                   stroke_fill=stroke_color + (255,))
            x += cw + tr
        rendered.append(im)
    gap = 6
    tw = max(im.width for im in rendered)
    th = sum(im.height for im in rendered) + gap * (len(rendered) - 1)
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    y = 0
    for im in rendered:
        x = (tw - im.width) // 2 if align == "center" else 0
        out.alpha_composite(im, (x, y))
        y += im.height + gap
    if shadow:
        a = np.array(out.split()[-1]).astype(np.float32)
        from PIL import ImageFilter
        sh = Image.fromarray((a * 0.55).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))
        pad = Image.new("RGBA", out.size, (0, 0, 0, 0))
        pad.putalpha(sh)
        pad.alpha_composite(out)
        out = pad
    return out


# ------------------------------------------------------------------ grading
def build_lut():
    x = np.arange(256) / 255.0
    s = x * x * (3 - 2 * x)
    y = x + (s - x) * 0.45  # contrast
    r = y + 0.045 * y ** 2 - 0.03 * (1 - y) ** 3
    g = y + 0.008 * (1 - y) ** 3
    b = y - 0.04 * y ** 2 + 0.05 * (1 - y) ** 3
    lut = np.stack([r, g, b], -1)
    return (np.clip(lut, 0, 1) * 255).astype(np.uint8)


LUT = build_lut()


class Grader:
    def __init__(self, W, H):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        self.vig = (1 - 0.32 * np.clip(d - 0.35, 0, 1) ** 1.6)[..., None].astype(np.float32)
        r = np.random.default_rng(3)
        self.grain = [r.normal(0, 5.5, (H, W, 1)).astype(np.float32) for _ in range(6)]

    def __call__(self, img, i, sat=1.12):
        a = np.asarray(img)
        a = np.stack([LUT[a[..., 0], 0], LUT[a[..., 1], 1], LUT[a[..., 2], 2]], -1).astype(np.float32)
        l = a @ np.array([0.299, 0.587, 0.114], np.float32)
        a = l[..., None] + (a - l[..., None]) * sat
        a = a * self.vig + self.grain[i % 6]
        return np.clip(a, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ sources
class Reader:
    def __init__(self, key, t, nframes, speed=1.0):
        self.w, self.h = SIZE[key]
        vf = "fps=30" if speed == 1 else f"setpts=PTS/{speed},fps=30"
        self.p = subprocess.Popen(
            ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", SRC[key], "-frames:v", str(nframes + 2),
             "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.last = None

    def read(self):
        n = self.w * self.h * 3
        buf = self.p.stdout.read(n)
        if len(buf) == n:
            self.last = np.frombuffer(buf, np.uint8).reshape(self.h, self.w, 3)
        return self.last

    def close(self):
        self.p.stdout.close()
        self.p.kill()
        self.p.wait()


def crop_box(key, shot, aspect, prog, extra_zoom):
    rx0, ry0, rx1, ry1 = shot.get("region") or REGION.get(key) or (0, 0, *SIZE[key])
    rw, rh = rx1 - rx0, ry1 - ry0
    if rw / rh > aspect:
        ch, cw = rh, rh * aspect
    else:
        cw, ch = rw, rw / aspect
    z = shot.get("z", 1.0) * (1 + shot.get("push", 0.06) * prog) * extra_zoom
    cw, ch = cw / z, ch / z
    cx = rx0 + shot.get("fx", 0.5) * rw + shot.get("dx", 0) * prog * rw
    cy = ry0 + shot.get("fy", 0.5) * rh
    cx = min(max(cx, rx0 + cw / 2), rx1 - cw / 2)
    cy = min(max(cy, ry0 + ch / 2), ry1 - ch / 2)
    return (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)


# ------------------------------------------------------------------ text events
class Txt:
    """A timed text element. kind: slam | name | kicker | card | caption-chunk."""

    def __init__(self, t0, t1, img, pos, anim="slam", darken=0.0):
        self.t0, self.t1, self.img, self.pos, self.anim, self.darken = t0, t1, img, pos, anim, darken

    def draw(self, canvas, t):
        if not (self.t0 <= t < self.t1):
            return
        age, left = t - self.t0, self.t1 - t
        if self.anim == "slam":
            s = 1.22 - 0.22 * ease_out(age / 0.14) + 0.035 * (age / max(0.3, self.t1 - self.t0))
            a = min(1, age / 0.05) * min(1, left / 0.08)
        elif self.anim == "pop":
            s = 0.86 + 0.14 * ease_out(age / 0.1)
            a = min(1, age / 0.04) * min(1, left / 0.05)
        elif self.anim == "rise":
            s = 1.0
            a = ease_out(age / 0.3) * min(1, left / 0.25)
        else:
            s, a = 1.0, min(1, age / 0.25) * min(1, left / 0.25)
        img = self.img
        if abs(s - 1) > 0.003:
            img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BICUBIC)
        if a < 0.999:
            al = img.split()[-1].point(lambda v: int(v * a))
            img = img.copy()
            img.putalpha(al)
        cx, cy = self.pos
        dy = (1 - ease_out(age / 0.3)) * 30 if self.anim == "rise" else 0
        canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2 + dy)))


# ------------------------------------------------------------------ render
def render(reel, fmt, out_path, crf=18, audio=None, preset="medium"):
    F = FORMATS[fmt]
    W, H = F["W"], F["H"]
    bx0, by0, bx1, by1 = F["band"]
    bw, bh = bx1 - bx0, by1 - by0
    aspect = bw / bh
    grade = Grader(bw, bh)
    total = sum(s["d"] for s in reel["shots"])
    nfr = int(round(total * FPS))
    texts = reel["texts"](fmt) if (F["text"] and reel.get("texts")) else []
    hits = reel.get("hits", [])
    flashes = reel.get("flashes", hits)
    blacks = reel.get("blacks", []) if F["text"] else reel.get("hero_blacks", [])

    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-"]
    if audio and fmt != "hero":
        cmd += ["-i", audio, "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-movflags", "+faststart", "-t", f"{total:.3f}", out_path]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    rng = np.random.default_rng(11)
    t_shot = 0.0
    gi = 0
    for si, shot in enumerate(reel["shots"]):
        shot = {**shot, **shot.get(fmt, {})}
        n = int(round((t_shot + shot["d"]) * FPS)) - int(round(t_shot * FPS))
        key = shot.get("src")
        rd = Reader(key, shot["t"], n, shot.get("speed", 1.0)) if key else None
        for k in range(n):
            t = (int(round(t_shot * FPS)) + k) / FPS
            prog = k / max(1, n - 1)
            # hit punch zoom + shake
            punch, shake, rgb = 1.0, 0.0, 0.0
            for h in hits:
                dt = t - h
                if 0 <= dt < 0.4:
                    punch += 0.07 * math.exp(-dt / 0.09)
                    shake = max(shake, 22 * math.exp(-dt / 0.1))
                    rgb = max(rgb, 16 * math.exp(-dt / 0.1))
            band = Image.new("RGB", (bw, bh), INK if fmt == "9x16" else (0, 0, 0))
            if rd is not None and not any(a <= t < b for a, b in blacks):
                fr = rd.read()
                if fr is not None:
                    box = crop_box(key, shot, aspect, prog, punch)
                    if shake:
                        sx = rng.uniform(-1, 1) * shake * (box[2] - box[0]) / bw
                        sy = rng.uniform(-1, 1) * shake * (box[3] - box[1]) / bh
                        box = (box[0] + sx, box[1] + sy, box[2] + sx, box[3] + sy)
                    fh, fw = fr.shape[:2]
                    ox = min(0, fw - box[2]) - min(0, box[0])
                    oy = min(0, fh - box[3]) - min(0, box[1])
                    box = (box[0] + ox, box[1] + oy, box[2] + ox, box[3] + oy)
                    band = Image.fromarray(fr).resize((bw, bh), Image.BICUBIC, box=box)
                    a = grade(band, gi, sat=shot.get("sat", 1.12))
                    if rgb >= 1:
                        k2 = int(rgb)
                        a = a.copy()
                        a[:, k2:, 0] = a[:, :-k2, 0]
                        a[:, :-k2, 2] = a[:, k2:, 2]
                    dk = 0.0
                    for tx in texts:
                        if tx.t0 <= t < tx.t1 and tx.darken:
                            dk = max(dk, tx.darken)
                    if shot.get("darken"):
                        dk = max(dk, shot["darken"])
                    if dk:
                        a = (a.astype(np.float32) * (1 - dk)).astype(np.uint8)
                    band = Image.fromarray(a)
            canvas = Image.new("RGBA", (W, H), INK + (255,) if fmt == "9x16" else (0, 0, 0, 255))
            canvas.paste(band, (bx0, by0))
            for tx in texts:
                tx.draw(canvas, t)
            for h in flashes:
                dt = t - h
                if 0 <= dt < 0.25:
                    al = int(255 * 0.85 * math.exp(-dt / 0.045))
                    canvas.alpha_composite(Image.new("RGBA", (W, H), (255, 250, 240, al)))
            enc.stdin.write(canvas.convert("RGB").tobytes())
            gi += 1
        if rd:
            rd.close()
        t_shot += shot["d"]
    enc.stdin.close()
    enc.wait()
    return out_path


# ------------------------------------------------------------------ audio helpers
def load_audio(key, t0, t1, fade=0.012):
    """Stereo float32 slice of an episode's mixed audio."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", SRC[key], "-t", f"{t1 - t0:.3f}",
                        "-vn", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.float32).reshape(-1, 2).T.astype(np.float64)
    nf = int(fade * SR)
    if a.shape[1] > 2 * nf:
        ramp = np.linspace(0, 1, nf)
        a[:, :nf] *= ramp
        a[:, -nf:] *= ramp[::-1]
    return a


def write_wav(path, stereo, target_lufs=-14.0):
    raw = path + ".raw.wav"
    import soundfile as sf
    peak = np.abs(stereo).max() or 1
    sf.write(raw, (stereo / peak * 0.9).T.astype(np.float32), SR, subtype="FLOAT")
    # two-pass loudnorm to social loudness with a true-peak ceiling
    import json
    m = subprocess.run(["ffmpeg", "-hide_banner", "-i", raw, "-af",
                        f"loudnorm=I={target_lufs}:TP=-1.0:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    af = (f"loudnorm=I={target_lufs}:TP=-1.0:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}"
          f":measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}"
          f":linear=true,alimiter=limit=0.89:level=false")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", af, "-ar", str(SR), "-c:a", "pcm_s16le", path],
                   check=True)
    os.remove(raw)
    return path
