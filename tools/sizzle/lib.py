"""Shot library, type styles and caption builder shared by every reel."""
import os
from PIL import Image
import engine as E
from engine import Txt, text_img, INTER_BLACK, INTER_XB, INTER_SB, PLAYFAIR_I, CREAM, GOLD, CORAL, INSET16

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------- shots
# Each entry: source, focus (fx, fy as fraction of the usable region), zoom.
# Ep15 Dave camera has a privacy blur box top-left of frame; its framings keep clear of it.
_D15 = dict(src="ep15", fx=0.66, fy=0.42, z=1.5, **{"9x16": dict(fx=0.62, fy=0.45, z=1.0)})
_M15 = dict(src="ep15", fx=0.64, fy=0.42, z=1.25, **{"9x16": dict(fx=0.55, fy=0.45, z=1.0)})
_D14 = dict(src="ep14", fx=0.55, fy=0.38, z=1.12, **{"9x16": dict(fx=0.56, fy=0.42, z=1.0)})
_M14 = dict(src="ep14", fx=0.6, fy=0.42, z=1.25, **{"9x16": dict(fx=0.54, fy=0.45, z=1.0)})
_M11 = dict(src="ep11", fx=0.55, fy=0.42, z=1.3, **{"9x16": dict(fx=0.55, fy=0.45, z=1.0)})
_M9 = dict(src="ep9", fx=0.32, fy=0.45, z=1.25, **{"9x16": dict(fx=0.2, fy=0.45, z=1.0)})
_W9 = dict(src="ep9", fx=0.45, fy=0.45, z=1.0, **{"9x16": dict(fx=0.3, fy=0.45, z=1.0)})
_D16 = dict(src="ep16", fx=0.45, fy=0.55, z=1.0, **{"9x16": dict(fx=0.47, fy=0.5, z=1.0)})
# Ep16 Mike: vertical inset on a blurred fill. Wide formats keep the fill, vertical uses the inset.
_M16 = dict(src="ep16", fx=0.5, fy=0.48, z=1.5, **{"9x16": dict(region=INSET16, fx=0.5, fy=0.42, z=1.0)})
_DK = dict(fx=0.5, fy=0.42, z=1.0, **{"16x9": dict(fy=0.52), "hero": dict(fy=0.52)})

SHOTS = {
    # Dave
    "d14_laugh": dict(_D14, t=900.0),
    "d14_laugh2": dict(_D14, t=901.4),
    "d14_wave": dict(_D14, t=1228.4),
    "d14_talk": dict(_D14, t=66.0),
    "d14_talk2": dict(_D14, t=1440.0),
    "d15_laugh": dict(_D15, t=838.4),
    "d15_point": dict(_D15, t=1567.4),
    "d15_grin": dict(_D15, t=1572.0),
    "d15_gest": dict(_D15, t=1386.0),
    "d16_onair": dict(_D14, t=1440.0),  # Ep 14 ON AIR: the Ep 16 camera crops Dave's head
    "dk_smile": dict(_DK, src="k_captain_kerry_workout_branding", t=10.5),
    "dk_laugh": dict(_DK, src="k_depression_stats_why_kerry_matters", t=15.0),
    "dk_talk": dict(_DK, src="k_dogs_and_vets_charity", t=4.5),
    # Mike
    "m15_mic": dict(_M15, t=1076.4),
    "m15_wave": dict(_M15, t=535.8),
    "m15_laugh": dict(_M15, t=841.0),
    "m15_hand": dict(_M15, t=851.6),
    "m15_gest": dict(_M15, t=1393.4),
    "m15_gest2": dict(_M15, t=1546.8),
    "m14_laugh": dict(_M14, t=1376.8),
    "m11_gest": dict(_M11, t=209.8),
    "m11_gest2": dict(_M11, t=237.0),
    "m11_gest3": dict(_M11, t=240.0),
    "m9_laugh": dict(_M9, t=839.2),
    "m9_point": dict(_M9, t=597.6),
    "m9_laugh2": dict(_M9, t=56.6),
    "mk_four": dict(_DK, src="k_captain_kerry_workout_branding", t=34.0),
    # both
    "w9_duo": dict(_W9, t=56.4),
    "w9_duo2": dict(_W9, t=838.6),
}


def shot(name, d, **kw):
    s = dict(SHOTS[name])
    s.update(kw)
    s["d"] = d
    return s


def sync(src_key, t, d, base=None, **kw):
    """A shot whose audio is placed at the same source time (lip sync)."""
    s = dict(base or {}, src=src_key, t=t, d=d)
    s.update(kw)
    return s


def m16(t, d):
    return dict(_M16, t=t, d=d)


def d16(t, d):
    return dict(_D16, t=t, d=d)


def black(d):
    return dict(src=None, d=d)


# ---------------------------------------------------------------- type
def fmt_geom(fmt):
    # over = type laid over footage (lower third, clear of faces); card = centre of a
    # black title card; cap = word-pop captions; top = small kicker line.
    if fmt == "9x16":
        return dict(W=1080, cx=540, top=250, over=1290, card=960, cap=1420, slam=112, name=88, sub=44, cap_sz=82)
    return dict(W=1920, cx=960, top=120, over=850, card=540, cap=905, slam=140, name=100, sub=46, cap_sz=78)


def _y(g, where):
    if isinstance(where, (int, float)):
        return where
    return g["card"] if where == "card" else g["top"] if where == "kick" else g["over"]


def _stroke(sz):
    return max(3, int(sz) // 20)


def slam(fmt, t0, t1, text, where="over", size=None, color=CREAM, darken=0.0, anim="slam"):
    g = fmt_geom(fmt)
    sz = size or g["slam"]
    img = text_img([(text, INTER_BLACK, sz, color)], g["W"], track=0.02, stroke=_stroke(sz))
    if img.width > g["W"] * 0.92:
        img = img.resize((int(g["W"] * 0.92), int(img.height * g["W"] * 0.92 / img.width)), Image.LANCZOS)
    return Txt(t0, t1, img, (g["cx"], _y(g, where)), anim)


def name_card(fmt, t0, t1, name, sub):
    g = fmt_geom(fmt)
    img = text_img([(name, INTER_BLACK, g["name"], CREAM), (sub, INTER_XB, g["sub"], GOLD)], g["W"], track=0.015,
                   stroke=_stroke(g["name"]))
    return Txt(t0, t1, img, (g["cx"], g["over"]), "rise")


def kicker(fmt, t0, t1, text, where="kick", color=CORAL):
    g = fmt_geom(fmt)
    sz = 44 if fmt == "9x16" else 36
    img = text_img([(text, INTER_XB, sz, color)], g["W"], track=0.2, stroke=3)
    if img.width > g["W"] * 0.94:
        img = img.resize((int(g["W"] * 0.94), int(img.height * g["W"] * 0.94 / img.width)), Image.LANCZOS)
    return Txt(t0, t1, img, (g["cx"], _y(g, where)), "fade")


def captions(fmt, words, max_words=3, max_chars=18, y=None, end_pad=0.3):
    """words: [(t_start, t_end, text)] on the reel timeline. Word-pop captions, active word in gold."""
    g = fmt_geom(fmt)
    yy = y or g["cap"]
    chunks, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or len(" ".join(x[2] for x in cur + [w])) > max_chars
                    or w[0] - cur[-1][1] > 0.45 or cur[-1][2].endswith((".", "?", ","))):
            chunks.append(cur)
            cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    out = []
    for ci, ch in enumerate(chunks):
        nxt = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else ch[-1][1] + end_pad
        chunk_end = min(nxt, ch[-1][1] + end_pad)
        for wi, w in enumerate(ch):
            t1 = ch[wi + 1][0] if wi + 1 < len(ch) else chunk_end
            line = []
            img = _cap_img(fmt, [x[2] for x in ch], wi, g["cap_sz"])
            out.append(Txt(w[0], max(t1, w[0] + 0.05), img, (g["cx"], yy), "pop" if wi == 0 else "none"))
    return out


def _cap_img(fmt, words, active, sz):
    from PIL import ImageDraw
    f = E.font(INTER_BLACK, sz)
    stroke = max(4, sz // 12)
    space = f.getlength(" ")
    ws = [f.getlength(w.upper()) for w in words]
    W = int(sum(ws) + space * (len(words) - 1)) + stroke * 2 + 12
    asc, desc = f.getmetrics()
    H = asc + desc + stroke * 2 + 6
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x = stroke + 6
    for i, (w, wd) in enumerate(zip(words, ws)):
        col = GOLD if i == active else CREAM
        d.text((x, stroke), w.upper(), font=f, fill=col + (255,), stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        x += wd + space
    return im


def words_from(pairs, offset):
    """pairs: [(src_start, src_end, text)] -> timeline words."""
    return [(a + offset, b + offset, w) for a, b, w in pairs]


def image_card(fmt, t0, t1, path, width_frac=0.42, y=None, anim="slam", on=None):
    g = fmt_geom(fmt)
    im = Image.open(path).convert("RGBA")
    w = int(g["W"] * (width_frac if fmt != "9x16" else min(0.86, width_frac * 2.0)))
    im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    if on == "glow":
        from PIL import ImageFilter
        pad = 60
        glow = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
        sh = Image.new("RGBA", im.size, CORAL + (150,))
        glow.alpha_composite(sh, (pad, pad))
        glow = glow.filter(ImageFilter.GaussianBlur(28))
        glow.alpha_composite(im, (pad, pad))
        im = glow
    return Txt(t0, t1, im, (g["cx"], y if y is not None else g["card"]), anim)
