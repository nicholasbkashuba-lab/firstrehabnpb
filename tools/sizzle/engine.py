"""Sizzle-reel compositor.

A reel is a list of shots (each a slice of an episode master, with a focus point and a
push-in), plus timed text, captions and hit effects, plus a synthesized Score.
render(reel, fmt) streams source frames out of ffmpeg, composites them in numpy/PIL,
and pipes the result straight into an x264 encode muxed with the mixed audio.

Formats: '16x9' (1920x1080), '9x16' (1080x1920), both full bleed; 'hero' (1920x1080,
no type, no audio). Natural camera colour: no grade, no grain, no vignette, and type
is outlined rather than sitting on a dark glow (owner feedback 2026-10-14).
"""
import json
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

# ------------------------------------------------------------------ native vertical clips
# Owner, 2026-10-14: "use the clips with the best picture quality", "some of these were shot
# vertical so you don't need to crop those". Every episode's social clips (media/ep{NN}-clips
# branches, copied to $SIZZLE_WORK/src/v/<ep>/) are 1080x1920 cut from the raw cameras, so a
# 9:16 shot from them is near 1:1, where a 9:16 crop of a 16:9 master is 1.8x (2.7x for the
# 720p Ep 15 master). The only crop is above the clip's own burned-in captions (`cap`, found
# by vindex). aud/vindex.json: {"v/ep19/05-antenna-joke.mp4": {"cap": 1610, ...}}.
VCLIP_DIRS = {"ep9": ["v/ep9", "v/ep9b"], "ep11": ["v/ep11"], "ep14": ["v/ep14"], "ep15": ["v/ep15"],
              "ep16": ["v/ep16"]}
_VINDEX = None
_VMATCH = None


def vclip(rel):
    """Register a vertical clip (path relative to $SIZZLE_WORK/src) and return its key."""
    global _VINDEX
    key = "v:" + rel
    if key not in SRC:
        if _VINDEX is None:
            p = os.path.join(SCR, "aud", "vindex.json")
            _VINDEX = json.load(open(p)) if os.path.exists(p) else {}
        SRC[key] = f"{SCR}/src/{rel}"
        pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                             "-of", "csv=p=0", SRC[key]], capture_output=True, text=True)
        w, h = map(int, pr.stdout.strip().split(",")[:2])
        SIZE[key] = (w, h)
        cap = _VINDEX.get(rel, {}).get("cap", h)
        REGION[key] = (0, 0, w, min(h, cap - 24))
    return key


def _aud4k(path, t0=None, d=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{t0:.3f}"] if t0 is not None else []) + ["-i", path]
    cmd += (["-t", f"{d:.3f}"] if d else []) + ["-ac", "1", "-ar", "4000", "-f", "f32le", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).astype(np.float64)
    return a - a.mean() if len(a) else a


_CLIPAUD = {}


def vertical_for(ep, t, d, min_r=0.9):
    """The vertical clip carrying master `ep` from t to t+d, as (key, clip_time), or None.
    Found by audio cross-correlation (the clips use the master's mixed track); a clip that
    cuts inside the span scores low and is rejected. Cached in aud/vmatch.json."""
    global _VMATCH
    import glob
    from scipy.signal import fftconvolve
    if _VMATCH is None:
        p = os.path.join(SCR, "aud", "vmatch_auto.json")
        _VMATCH = json.load(open(p)) if os.path.exists(p) else {}
    ck = f"{ep}@{t:.2f}+{d:.2f}"
    if ck not in _VMATCH:
        seg = _aud4k(SRC[ep], t, d)
        n, best = len(seg), None
        for dr in VCLIP_DIRS.get(ep, []):
            for f in sorted(glob.glob(f"{SCR}/src/{dr}/*.mp4")):
                if f not in _CLIPAUD:
                    _CLIPAUD[f] = _aud4k(f)
                c = _CLIPAUD[f]
                if n < 400 or len(c) < n:
                    continue
                num = fftconvolve(c, seg[::-1], "valid")
                en = np.sqrt(fftconvolve(c * c, np.ones(n), "valid").clip(1e-9) * (seg @ seg))
                r = num / en
                k = int(r.argmax())
                if best is None or r[k] > best[0]:
                    best = (float(r[k]), os.path.relpath(f, f"{SCR}/src"), k / 4000)
        _VMATCH[ck] = best
        json.dump(_VMATCH, open(os.path.join(SCR, "aud", "vmatch_auto.json"), "w"))
    m = _VMATCH[ck]
    return (vclip(m[1]), m[2]) if m and m[0] >= min_r else None


_REC = None


def _embed(key, t, region, hint=None):
    """SFace embedding of the face nearest `hint` (absolute x, y) in a frame, or the largest."""
    global _REC
    import cv2
    if _REC is None:
        _REC = cv2.FaceRecognizerSF.create(os.path.join(SCR, "models", "sface.onnx"), "")
    fr = _grab(key, t)
    if fr is None:
        return None
    rx0, ry0, rx1, ry1 = region
    crop = np.ascontiguousarray(fr[ry0:ry1, rx0:rx1])
    sc = 640 / max(crop.shape[:2])          # YuNet misses big faces at full resolution
    small = cv2.resize(crop, (int(crop.shape[1] * sc), int(crop.shape[0] * sc)))
    det = cv2.FaceDetectorYN.create(os.path.join(SCR, "models", "yunet.onnx"), "", (small.shape[1], small.shape[0]), 0.6)
    _, faces = det.detect(small)
    if faces is None:
        return None
    faces = faces.copy()
    faces[:, :14] /= sc
    if hint:
        hx, hy = hint[0] - rx0, hint[1] - ry0
        fc = min(faces, key=lambda f: abs(f[0] + f[2] / 2 - hx) + abs(f[1] + f[3] / 2 - hy))
    else:
        fc = max(faces, key=lambda f: f[2] * f[3])
    return _REC.feature(_REC.alignCrop(crop, fc))[0]


def same_person(shot, key, ct):
    """True when the vertical clip at `ct` shows the person the master shot is framed on.
    The social clips cut between cameras on their own, so the same moment can be on the
    guest in the clip and on Mike in the reel."""
    ck = f"same|{shot['src']}@{shot['t']:.2f}+{shot['d']:.2f}|{shot.get('fx', 0.5):.2f}|{key}"
    if ck not in _VMATCH:
        src = shot["src"]
        reg = shot.get("region") or REGION.get(src) or (0, 0, *SIZE[src])
        ok = True
        for f in (0.2, 0.8):
            fp = face_point(src, dict(shot), reg)
            a = _embed(src, shot["t"] + shot["d"] * f, reg, fp)
            b = _embed(key, ct + shot["d"] * f, REGION[key])
            if a is None or b is None or float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b))) < 0.42:
                ok = False
                break
        _VMATCH[ck] = ok
        json.dump(_VMATCH, open(os.path.join(SCR, "aud", "vmatch_auto.json"), "w"))
    return _VMATCH[ck]


def vertical_shot(shot):
    """9:16 only: swap a master shot for the same moment in its native vertical clip, framed
    full height with no extra zoom. Shots can opt out with vertical=False."""
    src = shot.get("src")
    if not src or src not in VCLIP_DIRS or shot.get("vertical") is False:
        return shot
    m = vertical_for(src, shot["t"], shot["d"])
    if not m or not same_person(shot, m[0], m[1]):
        return shot
    out = {k: v for k, v in shot.items() if k not in ("region", "pair", "fit", "z", "zmul", "fx", "fy", "dx")}
    out.update(src=m[0], t=m[1], fx=0.5, fy=0.42, z=1.0, push=min(shot.get("push", 0.05), 0.04), _from=src)
    return out

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
    "16x9": dict(W=1920, H=1080, band=(0, 0, 1920, 1080), text=True),
    "9x16": dict(W=1080, H=1920, band=(0, 0, 1080, 1920), text=True),
    "hero": dict(W=1920, H=1080, band=(0, 0, 1920, 1080), text=False),
}


# ------------------------------------------------------------------ helpers
def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def font(path, size):
    return ImageFont.truetype(path, int(size))


def text_img(lines, W, color=CREAM, stroke=0, stroke_color=(0, 0, 0), track=0.0, align="center", shadow=False):
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


# ------------------------------------------------------------------ picture
# Natural colour. The only processing is a light unsharp mask when a crop is being
# enlarged (720p Ep 15, vertical crops of 16:9 masters), which keeps faces crisp.
from PIL import ImageFilter
SHARPEN = ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=3)


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


# ------------------------------------------------------------------ face tracking
# Hand-set focus points drifted off Mike on the vertical crops, so every shot now finds
# the face nearest its intended subject (the shot's fx/fy is the hint) in three frames
# and centres on it, with the eyes about 40% down the crop. YuNet (OpenCV zoo, 230 KB)
# lives in $SIZZLE_WORK/models; results are cached in $SIZZLE_WORK/aud/faces.json.
_FACES = None
_DET = None


def _face_cache():
    global _FACES
    if _FACES is None:
        p = os.path.join(SCR, "aud", "faces.json")
        _FACES = json.load(open(p)) if os.path.exists(p) else {}
    return _FACES


def _grab(key, t):
    w, h = SIZE[key]
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", SRC[key], "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True)
    if len(p.stdout) != w * h * 3:
        return None
    return np.frombuffer(p.stdout, np.uint8).reshape(h, w, 3)


def face_point(key, shot, region, fracs=(0.15, 0.5, 0.85), track=False):
    """Absolute (x, y) of the face nearest the shot's hint, or None. With shot["pair"],
    the midpoint of the two largest faces (a two-shot is centred on the pair).
    track=True returns [(frac, x, y), ...] for every sampled frame with a face instead."""
    global _DET
    rx0, ry0, rx1, ry1 = region
    hx = rx0 + shot.get("fx", 0.5) * (rx1 - rx0)
    hy = ry0 + shot.get("fy", 0.45) * (ry1 - ry0)
    pair = bool(shot.get("pair"))
    ck = f"{key}@{shot['t']:.2f}+{shot['d']:.2f}|{hx:.0f},{hy:.0f}|{region}" + ("|pair" if pair else "")
    if track:
        ck += f"|track{len(fracs)}"
    cache = _face_cache()
    if ck in cache:
        return cache[ck]
    import cv2
    if _DET is None:
        _DET = cv2.FaceDetectorYN.create(os.path.join(SCR, "models", "yunet.onnx"), "", (320, 320), 0.6)
    pts = []
    for f in fracs:
        fr = _grab(key, shot["t"] + shot["d"] * f)
        if fr is None:
            continue
        crop = fr[ry0:ry1, rx0:rx1]
        sc = 640 / crop.shape[1]
        small = cv2.resize(crop, (640, int(crop.shape[0] * sc)))
        _DET.setInputSize((small.shape[1], small.shape[0]))
        _, faces = _DET.detect(small)
        if faces is None:
            continue
        if pair and len(faces) >= 2:
            fs = sorted(faces, key=lambda f: -f[2] * f[3])[:2]
            xs = [rx0 + (f[0] + f[2] / 2) / sc for f in fs]
            ys = [ry0 + (f[1] + f[3] * 0.42) / sc for f in fs]
            pts.append((f, sum(xs) / 2, sum(ys) / 2))
            continue
        best = None
        for fc in faces:
            x, y, w, h = (fc[:4] / sc)
            cx, cy = rx0 + x + w / 2, ry0 + y + h * 0.42
            # nearest to the hint (or to the last tracked point), larger faces preferred
            # (the background has posters)
            ax, ay = (pts[-1][1], pts[-1][2]) if (track and pts) else (hx, hy)
            cost = abs(cx - ax) + 0.3 * abs(cy - ay) - 0.8 * w
            if best is None or cost < best[0]:
                best = (cost, cx, cy, w)
        if best and best[3] > 0.04 * (rx1 - rx0):
            pts.append((f, best[1], best[2]))
    if track:
        res = [[float(a), float(b), float(c)] for a, b, c in pts]
    else:
        res = [float(np.median([p[1] for p in pts])), float(np.median([p[2] for p in pts]))] if pts else None
    cache[ck] = res
    os.makedirs(os.path.join(SCR, "aud"), exist_ok=True)
    json.dump(cache, open(os.path.join(SCR, "aud", "faces.json"), "w"))
    return res


MAX_UPSCALE = 2.6   # past this a punch-in looks soft; fall back to fit-with-fill instead


def ensure_centred(shot, region, aspect, out_w):
    """Owner rule (2026-10-14): the subject is centred in every shot, every time.
    A crop can only centre a face that is at least half a crop-width from the region
    edge. If it is closer, zoom in just enough to centre it; if that would enlarge the
    source more than MAX_UPSCALE, show the whole frame face-centred over a colour wash."""
    rx0, ry0, rx1, ry1 = region
    rw, rh = rx1 - rx0, ry1 - ry0
    cw0 = rh * aspect if rw / rh > aspect else rw
    xs = [p[1] for p in shot.get("_track") or []] or [shot["_face"][0]]
    room = min(min(x - rx0, rx1 - x) for x in xs)
    z = shot.get("z", 1.0) * shot.get("zmul", 1.0)
    if room <= 0:
        shot["fit"] = 1.0
        return
    z_need = cw0 / (2 * room) * 1.02
    if z_need <= z:
        return
    if out_w / (cw0 / z_need) <= MAX_UPSCALE:
        shot["z"] = z_need / shot.get("zmul", 1.0)
    else:
        shot["fit"] = 1.12


def face_track(key, shot, region):
    """The subject's position through the whole shot (owner rule: centred every frame, not
    just on average): sampled ~4x a second, smoothed, so the crop pans with a head turn."""
    n = max(3, int(shot["d"] * 4) + 1)
    fr = [round(0.02 + 0.96 * i / (n - 1), 3) for i in range(n)]
    pts = face_point(key, shot, region, fracs=tuple(fr), track=True)
    if not pts or len(pts) < 2:
        return None
    a = np.array(pts)
    if shot.get("hold"):
        return _hold_path(a, shot, region)
    k = 3 if len(a) >= 5 else 1                    # light smoothing: no jitter, no lag
    if k > 1:
        pad = np.pad(a[:, 1:], ((1, 1), (0, 0)), mode="edge")
        a[:, 1:] = (pad[:-2] + pad[1:-1] + pad[2:]) / 3
    return a.tolist()


def _hold_path(a, shot, region, dz=0.075, big=0.12):
    """shot["hold"]: a camera that HOLDS still instead of panning with every head turn (Nick,
    2026-10-28). The crop stays put; when the smoothed face drifts past dz of the crop width it
    glides over in 0.9 s, past big in 0.5 s. Height is held at the shot's median face.
    shot["hold_bias"] shifts the held framing by that fraction of the crop width (negative = left),
    for a subject who spends the shot turned one way (a profile toward a host)."""
    rx0, ry0, rx1, ry1 = region
    rw, rh = rx1 - rx0, ry1 - ry0
    cw = min(rw, rh * 9 / 16) / shot.get("z", 1.0)
    d = shot["d"]
    t = a[:, 0] * d
    k = min(len(a), 5)
    slow = np.convolve(np.pad(a[:, 1], (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")[:len(a)]
    pos, moves = float(np.median(a[:min(len(a), 4), 1])), []
    for ti, s_, f_ in zip(t, slow, a[:, 1]):
        if moves and ti < moves[-1][0] + moves[-1][3]:
            continue
        if abs(f_ - pos) > big * cw:
            moves.append((ti, pos, f_, 0.5)); pos = f_
        elif abs(s_ - pos) > dz * cw:
            moves.append((ti, pos, s_, 0.9)); pos = s_
    y = float(np.median(a[:, 2]))
    out = []
    for ti in np.linspace(0, d, max(3, int(d * 15) + 1)):
        x = moves[0][1] if moves else pos
        for t0, xa, xb, gl in moves:
            if ti < t0:
                break
            u = min(1.0, (ti - t0) / gl)
            x = xa + (xb - xa) * (u * u * (3 - 2 * u))
        out.append([ti / d, x + shot.get("hold_bias", 0.0) * cw, y])
    return out


def _track_at(shot, prog):
    tr = shot.get("_track")
    if not tr:
        return None
    f = [p[0] for p in tr]
    return (float(np.interp(prog, f, [p[1] for p in tr])), float(np.interp(prog, f, [p[2] for p in tr])))


def crop_box(key, shot, aspect, prog, extra_zoom):
    rx0, ry0, rx1, ry1 = shot.get("region") or REGION.get(key) or (0, 0, *SIZE[key])
    rw, rh = rx1 - rx0, ry1 - ry0
    if rw / rh > aspect:
        ch, cw = rh, rh * aspect
    else:
        cw, ch = rw, rw / aspect
    z = shot.get("z", 1.0) * shot.get("zmul", 1.0) * (1 + shot.get("push", 0.06) * prog) * extra_zoom
    cw, ch = cw / z, ch / z
    cx = rx0 + shot.get("fx", 0.5) * rw + shot.get("dx", 0) * prog * rw
    cy = ry0 + shot.get("fy", 0.5) * rh
    fp = _track_at(shot, prog) or shot.get("_face")
    if fp:
        cx = fp[0]
        cy = fp[1] + 0.1 * ch      # eyes ~40% down the frame
    cx = min(max(cx, rx0 + cw / 2), rx1 - cw / 2)
    cy = min(max(cy, ry0 + ch / 2), ry1 - ch / 2)
    return (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)


def fit_frame(fr, key, shot, bw, bh, prog, punch):
    """Show a source that is already a tight close-up WITHOUT cropping further: the whole
    usable region is scaled to fit, slid so the face sits at frame centre, and laid over a
    blurred, darkened copy of itself with feathered edges (no hard border line).
    Used for Dr. Leighton's clip, which was shot tight with his face at the right edge."""
    from PIL import ImageFilter
    rx0, ry0, rx1, ry1 = shot.get("region") or REGION.get(key) or (0, 0, *SIZE[key])
    rw, rh = rx1 - rx0, ry1 - ry0
    src = Image.fromarray(fr).crop((rx0, ry0, rx1, ry1))
    face = _track_at(shot, prog) or shot.get("_face")
    fx = ((face[0] - rx0) / rw) if face else shot.get("fx", 0.5)
    fy = ((face[1] - ry0) / rh) if face else shot.get("fy", 0.45)
    # background: a soft colour wash of the same picture (shrunk to a few pixels and
    # blown back up), darkened. It keeps the studio's colours with no recognisable
    # shapes, so the fill never shows a second, blurred face.
    if shot.get("blurfill"):
        # vertical source in a wide frame: the familiar treatment, a heavily blurred, dimmed
        # copy of the same picture scaled to cover (the 6x6 colour wash read as a dark box)
        cs = max(bw / rw, bh / rh)
        bg = src.resize((max(1, int(rw * cs / 8)), max(1, int(rh * cs / 8))), Image.BILINEAR)
        bg = bg.filter(ImageFilter.GaussianBlur(6)).resize((int(rw * cs), int(rh * cs)), Image.BICUBIC)
        bg = bg.crop(((bg.width - bw) // 2, (bg.height - bh) // 2, (bg.width - bw) // 2 + bw, (bg.height - bh) // 2 + bh))
        bg = Image.fromarray((np.asarray(bg).astype(np.float32) * 0.6).astype(np.uint8))
    else:
        bg = src.resize((6, 6), Image.BILINEAR).filter(ImageFilter.GaussianBlur(1)).resize((bw, bh), Image.BICUBIC)
        bg = Image.fromarray((np.asarray(bg).astype(np.float32) * 0.45).astype(np.uint8))
    # foreground: fit, times the shot's fit zoom, with the push-in and hit punch
    s = min(bw / rw, bh / rh) * shot["fit"] * (1 + shot.get("push", 0.05) * prog) * punch
    fw, fh = int(rw * s), int(rh * s)
    fg = src.resize((fw, fh), Image.BICUBIC)
    if s > 1.3:
        fg = fg.filter(SHARPEN)
    ox = int(bw / 2 - fx * fw)
    oy = int(bh * 0.42 - fy * fh)
    # Face dead centre, always (owner rule 2026-10-14); the blur fills whatever is left.
    oy = min(max(oy, bh - fh), 0) if fh >= bh else (bh - fh) // 2
    # feathered alpha so the edge melts into the blur
    feather = max(24, int(min(fw, fh) * 0.06))
    a = np.ones((fh, fw), np.float32)
    ramp = np.linspace(0, 1, feather, dtype=np.float32)
    a[:, :feather] *= ramp[None, :]
    a[:, -feather:] *= ramp[None, ::-1]
    a[:feather, :] *= ramp[:, None]
    a[-feather:, :] *= ramp[::-1, None]
    mask = Image.fromarray((a * 255).astype(np.uint8))
    bg.paste(fg, (ox, oy), mask)
    return bg


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
        if fmt == "9x16":
            shot = vertical_shot(shot)
        if shot.get("src") and shot.get("track", True):
            reg = shot.get("region") or REGION.get(shot["src"]) or (0, 0, *SIZE[shot["src"]])
            shot["_face"] = face_point(shot["src"], shot, reg)
            if shot["_face"]:
                shot["_track"] = face_track(shot["src"], shot, reg)
            if shot["_face"] and not shot.get("fit"):
                ensure_centred(shot, reg, aspect, bw)
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
                    if shot.get("fit"):
                        band = fit_frame(fr, key, shot, bw, bh, prog, punch)
                    else:
                        band = Image.fromarray(fr).resize((bw, bh), Image.BICUBIC, box=box)
                        if bw / (box[2] - box[0]) > 1.3:
                            band = band.filter(SHARPEN)
                    if rgb >= 1:
                        a = np.asarray(band).copy()
                        k2 = int(rgb)
                        a[:, k2:, 0] = a[:, :-k2, 0].copy()
                        a[:, :-k2, 2] = a[:, k2:, 2].copy()
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
