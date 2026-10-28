# Rebuild a clip FULL FRAME: crop the picture above the old burned-in captions, scale it to fill
# 1080x1920, and burn fresh one-line captions (<= 4 words, house style, MarginV=49) timed from
# word-level ASR, with spellings taken from the old reviewed captions (OCR) where they match.
# usage: refit.py src.mp4 out.mp4 y0 y1 asr.json [cues.json] [--cx 540]
import sys, json, re, subprocess, difflib, os, importlib.util
from PIL import ImageFont
args = [a for a in sys.argv[1:] if not a.startswith("--")]
src, dst, y0, y1, asr = args[0], args[1], int(args[2]), int(args[3]), args[4]
cues = json.load(open(args[5])) if len(args) > 5 and os.path.exists(args[5]) else []
cx = 540; track = None
for a in sys.argv:
    if a.startswith("--cx="): cx = int(a[5:])
    if a.startswith("--track="): track = json.load(open(a[8:]))["shots"]
REPO = "/home/user/firstrehabnpb"
s = open(f"{REPO}/tools/stage-episode.py").read()
ns = {}; exec("import re\n" + s[s.index("NAME_FIXES = ["): s.index("]\n", s.index("NAME_FIXES = [")) + 2], ns)
FIX = ns["NAME_FIXES"]
W = json.load(open(asr))
# OCR tokens (reviewed caption text) to correct spellings
ocr = [t for c in cues for t in c["text"].split()]
norm = lambda t: re.sub(r"[^a-z0-9%$]", "", t.lower())
wn = [norm(w["w"]) for w in W]; on = [norm(t) for t in ocr]
OK = lambda t: re.fullmatch(r"[\"'A-Za-z0-9$][\w'’%$.,?!:;\"-]*", t) is not None
sm = difflib.SequenceMatcher(None, wn, on, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            if OK(ocr[j1 + k]): W[i1 + k]["w"] = ocr[j1 + k]
    elif tag == "replace" and i2 - i1 == j2 - j1:
        for k in range(i2 - i1):
            if difflib.SequenceMatcher(None, wn[i1 + k], on[j1 + k]).ratio() > 0.75 and OK(ocr[j1 + k]):
                W[i1 + k]["w"] = ocr[j1 + k]
REF = None
for a in sys.argv:
    if a.startswith("--ref="): REF = open(a[6:]).read().split()
if REF:
    # the reviewed transcript wins: keep its words, timed by the ASR words they align to
    rn = [norm(t) for t in REF]; wn2 = [norm(w["w"]) for w in W]
    sm2 = difflib.SequenceMatcher(None, rn, wn2, autojunk=False)
    times = [None] * len(REF)
    for tag, i1, i2, j1, j2 in sm2.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): times[i1 + k] = (W[j1 + k]["s"], W[j1 + k]["e"])
        elif tag == "replace":
            span = (W[j1]["s"], W[j2 - 1]["e"]); n = i2 - i1
            for k in range(n):
                a0 = span[0] + (span[1] - span[0]) * k / n; times[i1 + k] = (a0, a0 + (span[1] - span[0]) / n)
    idx = [i for i, t in enumerate(times) if t]
    lo, hi = idx[0], idx[-1]
    NW = []
    for i in range(lo, hi + 1):
        if times[i] is None:
            prev = NW[-1]["e"] if NW else times[lo][0]
            nxt = next(times[j][0] for j in range(i, hi + 1) if times[j])
            times[i] = (prev, max(prev, nxt))
        NW.append({"w": REF[i], "s": times[i][0], "e": times[i][1]})
    W = NW
text = " ".join(w["w"] for w in W)
for p, r in FIX: text = re.sub(p, r, text)
# re-split corrected text back onto timings (fixes may merge words; keep counts by greedy match)
toks = text.split()
if len(toks) != len(W):
    toks = [w["w"] for w in W]
for t, w in zip(toks, W): w["w"] = re.sub(r"(?<=\w)[–—-](?=\w)", " ", t)
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60) if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else None
MAXW = 900
def width(s): return FONT.getlength(s) if FONT else len(s) * 32
# sentences -> balanced chunks of at most 4 words (no orphan one-word cues where avoidable)
import math
sents = []; cur = []
for w in W:
    cur.append(w)
    if re.search(r"[.?!]$", w["w"]): sents.append(cur); cur = []
if cur: sents.append(cur)
merged = []
for snt in sents:
    n = len(snt); k = math.ceil(n / 4)
    while True:
        size = [n // k + (1 if i < n % k else 0) for i in range(k)]
        parts = []; i = 0
        for sz in size: parts.append(snt[i:i + sz]); i += sz
        if all(width(" ".join(x["w"] for x in p)) <= MAXW for p in parts) or k >= n: break
        k += 1
    merged.extend(parts)
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
lines = []
for i, c in enumerate(merged):
    st = c[0]["s"]; en = merged[i + 1][0]["s"] if i + 1 < len(merged) else min(dur, c[-1]["e"] + 0.6)
    en = min(en, c[-1]["e"] + 1.2); en = max(en, st + 0.3)
    txt = " ".join(x["w"] for x in c).replace("{", "(").replace("}", ")")
    lines.append(f"Dialogue: 0,{ts(st)},{ts(en)},Default,,0,0,0,,{txt}")
ASS = """[Script Info]
ScriptType: v4.00+
PlayResX: 384
PlayResY: 288
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,10,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,4,0,0,2,10,10,49,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(lines) + "\n"
assf = dst + ".ass"; open(assf, "w").write(ASS)
ch = y1 - y0; cw = int(round(ch * 9 / 16 / 2)) * 2
def clampx(c): return int(max(0, min(1080 - cw, round(c - cw / 2))))
if track:
    expr = str(clampx(track[-1][2]))
    for a, b, c in reversed(track[:-1]):
        expr = f"if(lt(t\\,{b:.3f})\\,{clampx(c)}\\,{expr})"
    x = expr
else:
    x = clampx(cx)
vf = f"crop={cw}:{ch}:{x}:{y0},scale=1080:1920:flags=lanczos,setsar=1,subtitles={assf},format=yuv420p"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                "-r", "30", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-c:a", "copy", "-movflags", "+faststart", dst], check=True)
print(f"{os.path.basename(dst)}: crop {cw}x{ch}+{'track' if track else x}+{y0} zoom {1920/ch:.2f}x, {len(merged)} cues")
for l in lines: print("  ", l.split(",", 9)[1][2:], l.split(",,", 2)[-1].split(",,")[-1])
