#!/usr/bin/env python3
"""Regenerate the front desk review QR card and the standalone QR code.

    pip install Pillow qrcode
    python3 tools/review-kit.py

Writes into assets/review/:
    review-qr.png        the bare QR on solid white, for reuse anywhere
    review-card-4x6.png  the front desk card, 4x6 inches at 300 DPI, print ready
    review-card-4x6.pdf  the same card as a PDF, which is what print shops want

Why this file exists
--------------------
CLAUDE.md has recorded since July that a review QR card "was generated (Pillow +
qrcode)" and should be regenerated "if the brand or link changes". The card was
never committed and neither was whatever produced it, so there was nothing to
regenerate from: a brand or link change meant redrawing it by hand. This is that
generator, committed.

The QR encodes https://www.firstrehabnpb.com/review, which vercel.json
302-redirects to the Google write-a-review dialog for place ID
ChIJ3fEUAhCmsYkREHNzv87U3TQ. Point the QR at our own domain rather than at the
Google URL directly: a printed card outlives any Google URL format, and the
redirect is one line to change while a printed stack of cards is not.

Design follows the site tokens in assets/css/styles.css: deep teal #0E3A47,
cream #F6F1E7, coral #F4A261. The card carries no clinical claim, no star
rating, and no wording that hints only happy patients should scan it. See
content/reviews/README.md for why that last one is not optional.
"""

import os
import sys

try:
    import qrcode
    from qrcode.image.pil import PilImage
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Needs Pillow and qrcode:  pip install Pillow qrcode")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "review")
LOGO = os.path.join(ROOT, "assets", "media", "logo.png")

REVIEW_URL = "https://www.firstrehabnpb.com/review"
PHONE = "561-624-4263"

INK = (14, 58, 71)        # --ink / deep teal
CREAM = (246, 241, 231)   # --cream
CORAL = (244, 162, 97)    # --coral
MUTED = (81, 100, 108)    # --muted

DPI = 300
CARD_W, CARD_H = 4 * DPI, 6 * DPI   # 1200 x 1800


def _font(size, bold=False):
    """Best available system font. Falls back to Pillow's bitmap default.

    The site ships Playfair Display and Inter as woff2, which Pillow cannot
    read, so the card uses whatever DejaVu the box has. The card is a print
    asset rather than a brand-locked one; if an exact match ever matters,
    drop the TTFs into assets/fonts/ and point this at them.
    """
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _centre(draw, y, text, font, fill, width=CARD_W):
    """Draw text horizontally centred, return the y below it."""
    box = draw.textbbox((0, 0), text, font=font)
    draw.text(((width - (box[2] - box[0])) / 2 - box[0], y), text, font=font, fill=fill)
    return y + (box[3] - box[1])


def build_qr(px=1000, bg=(255, 255, 255)):
    """The QR as dark teal modules on a SOLID light background.

    ERROR_CORRECT_H tolerates roughly 30% damage, which is what lets the logo
    sit in the middle without breaking the scan. Do not lower it while the
    logo overlay is in place.

    The background is solid on purpose. The first version of this script drew
    the QR on a transparent background; converting that to RGB for the card
    flattened the alpha to BLACK, leaving dark teal modules on near black and
    a code no phone could read. Both files were generated, looked plausible in
    a thumbnail, and failed to decode. A quiet zone only works if it is light,
    so pass a light colour here and never re-introduce back_color=None.

    `border=4` is the spec minimum quiet zone in modules. Going below it is the
    other classic way to produce a code that scans on a screen and fails on
    paper.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(REVIEW_URL)
    qr.make(fit=True)
    img = qr.make_image(image_factory=PilImage, fill_color=INK, back_color=bg)
    img = img.convert("RGB").resize((px, px), Image.NEAREST)

    # Logo knockout in the centre, on a matching pad so the mark stays legible.
    # 22% of the width is about 5% of the code area, well inside what level H
    # recovers. Raising it is how you silently break the scan.
    if os.path.exists(LOGO):
        pad = int(px * 0.22)
        plate = Image.new("RGB", (pad, pad), bg)
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((int(pad * 0.80), int(pad * 0.80)), Image.LANCZOS)
        plate.paste(logo, ((pad - logo.width) // 2, (pad - logo.height) // 2), logo)
        img.paste(plate, ((px - pad) // 2, (px - pad) // 2))
    return img


def build_card():
    card = Image.new("RGB", (CARD_W, CARD_H), CREAM)
    d = ImageDraw.Draw(card)

    # Teal header band
    band = int(CARD_H * 0.20)
    d.rectangle([0, 0, CARD_W, band], fill=INK)

    if os.path.exists(LOGO):
        logo = Image.open(LOGO).convert("RGBA")
        logo.thumbnail((int(CARD_W * 0.62), int(band * 0.52)), Image.LANCZOS)
        # logo.png is dark on transparent, so lighten it for the teal band
        light = Image.new("RGBA", logo.size, (246, 241, 231, 0))
        light.paste(CREAM + (255,), (0, 0), logo)
        card.paste(light, ((CARD_W - logo.width) // 2, (band - logo.height) // 2), light)
    else:
        _centre(d, int(band * 0.34), "First Rehabilitation", _font(64, True), CREAM)

    # Vertical budget is tight: 1800px total, 360 of it the header band. The
    # first draft used generous gaps and a 0.58 QR and pushed the URL and the
    # phone line clean off the bottom edge, which a thumbnail hides. If you
    # change any spacing here, re-run and LOOK at the PNG; main() also asserts
    # the last baseline lands inside the card.
    y = band + 80
    y = _centre(d, y, "How did we do?", _font(88, True), INK) + 52
    y = _centre(d, y, "Your review helps neighbours", _font(40), MUTED) + 40
    y = _centre(d, y, "find care they can trust.", _font(40), MUTED) + 74

    qr_px = int(CARD_W * 0.50)
    qr = build_qr(qr_px, bg=(255, 255, 255))
    frame = 22
    d.rectangle(
        [(CARD_W - qr_px) // 2 - frame, y - frame,
         (CARD_W + qr_px) // 2 + frame, y + qr_px + frame],
        fill=(255, 255, 255), outline=CORAL, width=8,
    )
    card.paste(qr, ((CARD_W - qr_px) // 2, y))
    y += qr_px + frame + 62

    y = _centre(d, y, "Point your camera here", _font(48, True), INK) + 46
    y = _centre(d, y, "firstrehabnpb.com/review", _font(38), MUTED) + 56

    d.line([(CARD_W * 0.20, y), (CARD_W * 0.80, y)], fill=CORAL, width=5)
    y += 46
    y = _centre(d, y, f"Questions? Call {PHONE}", _font(36), MUTED)
    return card, y


def main():
    os.makedirs(OUT, exist_ok=True)

    qr_path = os.path.join(OUT, "review-qr.png")
    build_qr(1000, bg=(255, 255, 255)).save(qr_path)

    card, last_y = build_card()
    if last_y > CARD_H - 40:
        sys.exit(f"Card overflows: last baseline at {last_y}px on a {CARD_H}px card. "
                 "Tighten the spacing in build_card().")
    png_path = os.path.join(OUT, "review-card-4x6.png")
    pdf_path = os.path.join(OUT, "review-card-4x6.pdf")
    card.save(png_path, dpi=(DPI, DPI))
    card.save(pdf_path, "PDF", resolution=DPI)

    for p in (qr_path, png_path, pdf_path):
        print(f"wrote {os.path.relpath(p, ROOT)}  ({os.path.getsize(p):,} bytes)")

    # Decode what we just drew. A QR that does not scan looks completely fine
    # in a thumbnail, which is how the first run of this script produced two
    # unscannable files. Never ship this to a printer on eyeballing alone.
    try:
        import cv2
        ok = True
        for p in (qr_path, png_path):
            data, _, _ = cv2.QRCodeDetector().detectAndDecode(cv2.imread(p))
            mark = "ok" if data == REVIEW_URL else "FAILED"
            if data != REVIEW_URL:
                ok = False
            print(f"  decode {os.path.basename(p)}: {mark}  {data or '(no data)'}")
        if not ok:
            sys.exit("\nQR did not decode back to the review URL. Do not print these.")
        print(f"\nQR encodes: {REVIEW_URL}")
    except ImportError:
        print(f"\nQR encodes: {REVIEW_URL}")
        print("opencv-python-headless not installed, so the decode check was SKIPPED.")
        print("Scan both files with a phone before sending anything to print.")


if __name__ == "__main__":
    main()
