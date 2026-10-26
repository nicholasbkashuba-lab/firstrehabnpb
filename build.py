#!/usr/bin/env python3
"""
First Rehabilitation of North Palm Beach — static site generator (v2).
Run `python3 build.py`; every page regenerates in place.
"""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))

PHONE = "561-624-4263"
FAX = "561-840-4234"
EMAIL = "firstrehabnpb@gmail.com"
PORTAL = "https://firstrehabilitationinc.patient.sprypt.com/clinics"
SPOTIFY = "https://open.spotify.com/show/033A1BQq9qqsygFFCq9SIu"
YOUTUBE = "https://www.youtube.com/channel/UCFzCl3RvdVahfIjKZ1SfRvQ"
INSTAGRAM = "https://www.instagram.com/firstrehabnpb"
FACEBOOK = "https://www.facebook.com/FirstRehabNPB/"
LINKEDIN = "https://www.linkedin.com/company/firstrehabnpb"
# Press coverage for the homepage "In the News" band. Newest first.
# Only add items that actually name this practice — this is a healthcare site and a
# link implying coverage that isn't ours is a factual claim, not decoration.
# The band renders only when this list has something in it, so an empty list
# removes the whole section from the homepage rather than leaving a bare heading.
NEWS = [
    # The Palm Beach Gardens Living "Profiles of Leadership" magazine feature was
    # here; Nick asked for it off the site on 2026-08-08.
    # Healthcare IT News ran a piece at
    # /news/first-rehabilitation-boosts-revenue-37-outpatient-platform.
    # Held back because the page sits behind Cloudflare and returns 403 to any
    # automated fetch, so the headline, date, and whether it names THIS practice
    # could not be confirmed. Add it once someone reads the live article and can
    # supply the exact headline and publication date.
    # Verified 2026-10-14 by reading the live article: byline Shannon Cake, posted
    # Apr 09, 2025, Dave named as owner, "39 years of experience" and "80,000
    # patients" in WPTV's own words, and a Google review cites it as how the
    # reviewer found us. Visible press is the single trust signal competitors
    # (HSS network badge at Synergy, ortho-group affiliation at PBOI) lean on most.
    {"outlet": "WPTV NewsChannel 5", "date": "April 2025",
     "url": "https://www.wptv.com/news/health/essential-wellness-tips-for-achieving-optimal-fitness-and-health",
     "title": "Essential wellness tips for achieving optimal fitness and health",
     "blurb": "Anchor Shannon Cake, rehabbing a rotator cuff injury of her own, visits First Rehabilitation for Dr. Dave Kashuba's tips on hydration, core strength, balance and staying injury free."},
]

# Accepted plans — owner-confirmed. Single source of truth: the homepage ticker,
# the insurance page, and the location pages all read this list, so it can never
# drift between pages. Adding or dropping a plan is a one-line edit here.
PLANS = ["Medicare", "Medicare Advantage", "Blue Cross Blue Shield", "Aetna",
         "Humana", "Tricare", "VA Community Care Network", "Workers' Comp", "Self Pay"]
TIKTOK = "https://www.tiktok.com/@firstrehabilitation"
TWITTER = "https://x.com/first_rehab_npb"
MAPS_EMBED = "https://www.google.com/maps?q=733+US+Highway+1+Suite+2A+North+Palm+Beach+FL+33408&output=embed"

# ---------------------------------------------------------------------------
# PHOTOS — the single registry of every real photograph on this site.
#
# One entry per photograph. Nothing else in this file may hardcode a photo path:
# templates call photo(name, ...) and get a <picture> with WebP + JPEG sources,
# a responsive srcset, and the focal point baked in.
#
# "focal" is an object-position value chosen by LOOKING at each frame, because a
# default centre crop decapitates people. It is the design decision; the pixel
# work (rendition ladder, WebP/JPEG encode) lives in tools/build-images.py, which
# reads this dict and writes assets/img/manifest.json.
#
# Every entry below is a genuine photograph of this clinic, its staff, or its
# building. There are 15 of them and they are the entire photographic library.
# No stock, no illustration, no AI imagery. If a layout needs a photo that is not
# in this dict, the layout is wrong — do not invent a slot and fill it with a
# gradient or an icon.
#
# NOTE ON SOURCE RESOLUTION: several of these are small (the exterior is 680px
# wide). build-images.py never upscales, so the manifest records a real cap and
# photo() emits a srcset that stops there. That is why some photos are used in
# constrained frames rather than full-bleed — it is a source limit, not a choice.
# ---------------------------------------------------------------------------
PHOTOS = {
    "treatment": {
        "src": "assets/media/clinic.jpg",
        # Dave's head and treating hands sit left of centre, upper third.
        "focal": "38% 30%",
        "alt": "Dr. Dave Kashuba, Occupational Therapist, stretching a patient's "
               "leg during a session at First Rehabilitation in North Palm Beach",
    },
    "gym": {
        "src": "assets/media/gym.jpg",
        # Wide interior. Ceiling eats the top third, so bias down to the floor.
        "focal": "center 62%",
        "alt": "The on-site rehabilitation gym at First Rehabilitation of "
               "North Palm Beach, with cardio and strength equipment",
    },
    # Previously named founder.jpg and captioned as a portrait of Dr. Kashuba.
    # It is not a portrait — it is the clinic building. The alt text was wrong
    # on every page that used it; corrected here (2026-09-15).
    "exterior": {
        "src": "assets/media/founder.jpg",
        "focal": "center 45%",
        "alt": "The First Rehabilitation of North Palm Beach clinic building "
               "at 733 US Highway 1, with covered entrance and palm trees",
    },
    "mike": {
        "src": "assets/media/mike.jpg",
        "focal": "center 18%",
        "alt": "Mike McGann, co-host of the Pain 2 Power podcast",
    },
}

# Team portraits join the same registry, so a headshot is fetched exactly the way
# any other photo is. Five of the six were shot in one session against the same
# hedge, so a shared 4:5 crop with per-face focal points reads as a real set.
_TEAM_FOCAL = {
    "david.jpg": ("45% 24%", "David Kashuba, Ph.D., OTR, founder and CEO of First Rehabilitation"),
    "nick.jpg": ("50% 26%", "Nick Kashuba, Chief Operating Officer of First Rehabilitation"),
    "logan.jpg": ("44% 26%", "Logan Van Sant, PT, DPT, Physical Therapist at First Rehabilitation"),
    "kayla.jpg": ("56% 20%", "Kayla Dorsey, PT, DPT, Physical Therapist at First Rehabilitation"),
    "joni.jpg": ("50% 27%", "Joan (Joni) Janik, OTD, Occupational Therapist at First Rehabilitation"),
    "laura.jpg": ("47% 25%", "Laura Drumm, MS, OTR/L, CHT, Certified Hand Therapist at First Rehabilitation"),
}
for _f, (_focal, _alt) in _TEAM_FOCAL.items():
    PHOTOS[f"team-{_f[:-4]}"] = {"src": f"assets/team/{_f}", "focal": _focal, "alt": _alt}

# The ten homepage gallery tiles are Instagram exports at ~520px. They are real
# photographs of this clinic, but they are small, so they are only ever used at
# gallery-tile size and never promoted into a hero.
for _i in range(1, 11):
    PHOTOS[f"social-{_i}"] = {
        "src": f"assets/social/post-{_i}.jpg",
        "focal": "center 45%",
        "alt": f"First Rehabilitation of North Palm Beach on social media, photo {_i}",
    }

# SERVICE_MEDIA — what photograph each service page leads with.
#
# Only two services have a genuine photograph OF THAT SERVICE: physical therapy
# (the treatment frame) and wellness (the gym). The other two previously shipped
# stand-ins — an Instagram tile stretched across the physical-therapy hero, and
# Laura's staff portrait cropped to look like a scene. Both were placeholders.
#
# Rather than fake a scene, a service without one leads with a CREDITED PORTRAIT
# of the clinician who actually runs it, framed and captioned as a portrait. That
# is an honest photograph doing honest work, and it is the reason a "portrait"
# kind exists alongside "scene" below.
SERVICE_MEDIA = {
    # The treatment frame is Dave — who is an Occupational Therapist — stretching
    # a patient, so it belongs to occupational therapy, not physical therapy.
    # It led the PT page briefly; that was wrong about who is in the photograph.
    "occupational-therapy": ("scene", "treatment", None, None),
    "wellness":             ("scene", "gym", None, None),
    # Logan rather than Kayla: the lead frame is landscape, and Kayla's source is
    # a portrait-orientation full-body shot that crops to a small face and dead
    # sky. Logan's is chest-up and landscape, matching Laura's on hand therapy.
    "physical-therapy":     ("portrait", "team-logan", "Logan Van Sant, PT, DPT", "Physical Therapist"),
    "hand-therapy":         ("portrait", "team-laura", "Laura Drumm, MS, OTR/L, CHT", "Certified Hand Therapist"),
}

# ----------------------------------------------------------------------------


import hashlib as _hashlib
def _v(path):
    """Short content hash for cache-busting static assets (?v=)."""
    with open(path, "rb") as f:
        return _hashlib.sha256(f.read()).hexdigest()[:8]
ASSET_V = {}
def asset_v(path):
    if path not in ASSET_V:
        ASSET_V[path] = _v(path)
    return ASSET_V[path]

# --- sitemap <lastmod> ------------------------------------------------------
# A page's lastmod must be the date that PAGE last changed, not the date of the
# build. Stamping today on all 50 URLs every build tells Google the whole site
# changed whenever anything did, which is how the signal gets ignored — and it
# is why sitemap.xml used to have to be kept out of commits by hand.
#
# So each generated page is hashed and the date its content last changed is
# remembered in SITEMAP_DATES, which is committed alongside the build. Delete
# that file and every page silently reverts to claiming it changed today.
#
# Asset cache-busters are stripped before hashing: bumping styles.css rewrites
# `?v=` on every page in the site, and that is not a content change to any of
# them.
import re as _re, subprocess as _sp
SITEMAP_DATES = "sitemap-dates.json"
_CACHE_BUSTER = _re.compile(r"\?v=[A-Za-z0-9]+")
_ISO_DATE = _re.compile(r"\d{4}-\d{2}-\d{2}")

def _page_file(page):
    """Filesystem path for a sitemap entry ("" is the home page)."""
    return page or "index.html"

def _page_fingerprint(page):
    f = _page_file(page)
    try:
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            html_src = fh.read()
    except FileNotFoundError:
        # Listed in build_meta()'s `pages` but never generated. This used to ship
        # a sitemap entry pointing at a 404; say so instead.
        raise SystemExit(
            f"sitemap: {f} is in the pages list but no such file was built. "
            f"Add the generator for it, or take it out of `pages` in build_meta().")
    return _hashlib.sha256(
        _CACHE_BUSTER.sub("", html_src).encode()).hexdigest()[:16]

_DIRTY = None
def _uncommitted():
    """Paths with uncommitted changes, so a seed date is never taken from git
    for a file whose working copy has already moved past that commit."""
    global _DIRTY
    if _DIRTY is None:
        try:
            r = _sp.run(["git", "status", "--porcelain", "--"], cwd=ROOT,
                        capture_output=True, text=True, timeout=30)
            _DIRTY = {line[3:].strip() for line in r.stdout.splitlines()} if r.returncode == 0 else set()
        except (OSError, _sp.SubprocessError):
            _DIRTY = set()
    return _DIRTY

def _git_last_changed(page):
    """Date of the last commit touching a page, for seeding a page we have no
    recorded hash for. None when git cannot answer."""
    f = _page_file(page)
    if f in _uncommitted():
        return None
    try:
        r = _sp.run(["git", "log", "-1", "--format=%cs", "--", f], cwd=ROOT,
                    capture_output=True, text=True, timeout=30)
    except (OSError, _sp.SubprocessError):
        return None
    d = r.stdout.strip()
    return d if r.returncode == 0 and _ISO_DATE.fullmatch(d) else None

def _lastmods(pages, today):
    """Per-page lastmod, carried forward for every page that did not change."""
    path = os.path.join(ROOT, SITEMAP_DATES)
    try:
        with open(path, encoding="utf-8") as f:
            seen = _json.load(f)
    except (OSError, ValueError):
        seen = {}
    out, store = {}, {}
    for p in pages:
        fp = _page_fingerprint(p)
        was = seen.get(p)
        if was and was.get("hash") == fp:
            out[p] = was["lastmod"]                      # unchanged
        elif was:
            out[p] = today                               # content really changed
        else:
            out[p] = _git_last_changed(p) or today       # first sighting
        store[p] = {"hash": fp, "lastmod": out[p]}       # drops retired pages
    with open(path, "w", encoding="utf-8") as f:
        _json.dump(store, f, indent=2, sort_keys=True)
        f.write("\n")
    return out

# --- Responsive imagery -----------------------------------------------------
# tools/build-images.py writes assets/img/manifest.json from PHOTOS. photo()
# turns a registry name into a <picture> with WebP + JPEG, a srcset capped at the
# source's real resolution, intrinsic width/height (so nothing shifts on load),
# and the focal point applied as object-position.
import json as _json

_MANIFEST = None
def _manifest():
    global _MANIFEST
    if _MANIFEST is None:
        p = os.path.join(ROOT, "assets", "img", "manifest.json")
        try:
            with open(p) as f:
                _MANIFEST = _json.load(f)
        except FileNotFoundError:
            _MANIFEST = {}
    return _MANIFEST


def service_media(slug):
    """Lead image for a service page: a real scene, or a credited clinician portrait."""
    kind, name, person, credential = SERVICE_MEDIA[slug]
    if kind == "scene":
        return ('<div class="split-media tilt2 reveal d2">'
                + photo(name, depth=1, sizes="(max-width:900px) 92vw, 560px")
                + "</div>")
    return (
        '<figure class="split-media split-portrait tilt2 reveal d2">'
        + photo(name, depth=1, sizes="(max-width:900px) 92vw, 560px", ratio="4/5")
        + f'<figcaption><strong>{person}</strong><span>{credential}</span></figcaption>'
        + "</figure>"
    )


def photo(name, depth=0, cls="", sizes="100vw", eager=False, ratio=None, alt=None):
    """Render a registry photograph as a responsive, art-directed <picture>.

    ratio: optional "W/H" forced aspect for the frame. The focal point keeps the
           subject in frame when the source is cropped to it.
    """
    m = _manifest().get(name)
    spec = PHOTOS.get(name)
    if spec is None:
        raise KeyError(f"photo('{name}') is not in PHOTOS — add it there, not inline")
    up = "../" * depth
    alt_text = html.escape(alt if alt is not None else spec["alt"], quote=True)
    focal = spec["focal"]

    if not m:
        # Manifest missing (build-images.py has not run). Fall back to the source
        # file so the page is still correct, just unoptimised.
        return (f'<img src="{up}{spec["src"]}" alt="{alt_text}" '
                f'style="object-position:{focal}" class="{cls}" '
                f'{"" if eager else "loading=lazy decoding=async"}>')

    widths = m["widths"]
    w, h = m["native"]
    webp = ", ".join(f"{up}assets/img/{name}-{x}.webp {x}w" for x in widths)
    jpg = ", ".join(f"{up}assets/img/{name}-{x}.jpg {x}w" for x in widths)
    biggest = m["max_width"]
    style = f"object-position:{focal}"
    if ratio:
        style += f";aspect-ratio:{ratio}"
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<picture class="{cls}">'
        f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
        f'<img src="{up}assets/img/{name}-{biggest}.jpg" srcset="{jpg}" sizes="{sizes}" '
        f'width="{w}" height="{h}" alt="{alt_text}" style="{style}" {load}>'
        f"</picture>"
    )

# Google tag (gtag.js) — GA4 property G-GZKFNKSP6D, First Rehabilitation of North
# Palm Beach ONLY. This measurement ID belongs to this clinic and must never be
# emitted on any other site. Kept as a plain (non f-string) constant so the
# snippet's own braces need no escaping, and injected by head() immediately
# after <head> on every generated page — exactly once, since head() is the only
# thing that writes that tag.
# Search Console HTML-tag ownership verification.
#
# The property lost verification some time before 2026-09-09 and every API route
# went 403 — no queries, no page data, no index coverage, no sitemap submission.
# It had never been carried by the site: verification lived in a DNS record or a
# leftover Wix token, so nothing in this repo kept it alive and nothing warned
# when it lapsed. Emitting the tag from head() puts it on all 48 pages, where a
# rebuild renews it and it cannot quietly expire again.
#
# PASTE THE TOKEN HERE: Search Console -> Settings -> Ownership verification ->
# HTML tag. Copy ONLY the content="..." value, not the whole <meta> element.
# Use the token from the OWNER's account (Nick's), not a service account's — the
# tag is what keeps his ownership permanent; the service account is a delegated
# user under Users and permissions and does not need to own the property.
# Empty string = no tag emitted, which is exactly today's behaviour, so the build
# stays green until the token is pasted.
GSC_VERIFICATION = "AIrqh67-C88X6VuoDTLQZdUvpFPQYpytxgqsf9ZHjAM"
GSC_VERIFY_TAG = (
    f'\n<meta name="google-site-verification" content="{html.escape(GSC_VERIFICATION)}">'
    if GSC_VERIFICATION else ""
)

GA_MEASUREMENT_ID = "G-GZKFNKSP6D"
GA_TAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '%s');
</script>""" % (GA_MEASUREMENT_ID, GA_MEASUREMENT_ID)

def head(title, desc, depth=0, canonical="", og_image="assets/media/hero-poster.jpg", page_type="website", extra_schema="", robots="index, follow, max-image-preview:large"):
    p = "../" * depth
    base = "https://www.firstrehabnpb.com"
    canon = f"{base}/{canonical}" if canonical else base + "/"
    # Absolute URL for the organization schema's image. Precomputed because the
    # template below is a triple-quoted f-string: the original wrote this as a
    # literal `"..." + PHOTOS["treatment"]["src"]` OUTSIDE any {} placeholder, so
    # Python emitted the Python expression verbatim into the JSON-LD. That made the
    # organization node unparseable on all 51 pages that carry it — every page on
    # the site — and an unparseable node is discarded wholesale by Google, taking
    # the @id, medicalSpecialty, availableService, geo, areaServed and sameAs with
    # it. Caught 2026-09-18. Keep this interpolated; do not inline the concatenation.
    org_image = f"{base}/{PHOTOS['treatment']['src']}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{GA_TAG}
<meta charset="UTF-8">{GSC_VERIFY_TAG}
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta name="author" content="First Rehabilitation of North Palm Beach">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="North Palm Beach">
<meta property="og:type" content="{page_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="First Rehabilitation of North Palm Beach">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{base}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{base}/{og_image}">
<meta name="theme-color" content="#0E3A47">
<link rel="icon" href="{p}assets/icons/favicon.ico?v=6" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/icons/icon-32.png?v=6">
<link rel="icon" type="image/png" sizes="16x16" href="{p}assets/icons/icon-16.png?v=6">
<link rel="apple-touch-icon" sizes="180x180" href="{p}assets/icons/apple-touch-icon.png?v=6">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/playfair-display-latin-700-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/inter-latin-400-normal.woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/styles.css?v={asset_v('assets/css/styles.css')}">
<link rel="stylesheet" href="{p}assets/css/intake.css?v={asset_v('assets/css/intake.css')}">
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": ["MedicalClinic", "MedicalBusiness"],
  "isAcceptingNewPatients": true,
  "@id": "https://www.firstrehabnpb.com/#organization",
  "name": "First Rehabilitation of North Palm Beach",
  "legalName": "First Rehabilitation of North Palm Beach",
  "alternateName": ["First Rehab NPB", "First Rehabilitation", "First Rehab of North Palm Beach"],
  "description": "Family-owned outpatient physical therapy, occupational therapy, certified hand therapy, and wellness clinic serving Palm Beach County since 1991.",
  "url": "https://www.firstrehabnpb.com",
  "logo": "https://www.firstrehabnpb.com/assets/media/logo.png",
  "image": "{org_image}",
  "telephone": "+1-561-624-4263",
  "faxNumber": "+1-561-840-4234",
  "email": "firstrehabnpb@gmail.com",
  "foundingDate": "1991",
  "founder": {{ "@type": "Person", "@id": "https://www.firstrehabnpb.com/about.html#david-kashuba", "name": "David Kashuba", "honorificSuffix": "Ph.D., OTR", "jobTitle": "CEO & Occupational Therapist" }},
  "priceRange": "$$",
  "slogan": "Our People Make the Difference",
  "medicalSpecialty": ["PhysicalTherapy", "OccupationalTherapy"],
  "availableService": [
    {{"@type": "MedicalTherapy", "@id": "https://www.firstrehabnpb.com/services/physical-therapy.html#therapy", "name": "Physical Therapy"}},
    {{"@type": "MedicalTherapy", "@id": "https://www.firstrehabnpb.com/services/occupational-therapy.html#therapy", "name": "Occupational Therapy"}},
    {{"@type": "MedicalTherapy", "@id": "https://www.firstrehabnpb.com/services/hand-therapy.html#therapy", "name": "Certified Hand Therapy"}},
    {{"@type": "MedicalTherapy", "@id": "https://www.firstrehabnpb.com/services/wellness.html#therapy", "name": "Wellness & Gym"}}
  ],
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "733 US Highway 1, Suite 2A",
    "addressLocality": "North Palm Beach",
    "addressRegion": "FL",
    "postalCode": "33408",
    "addressCountry": "US"
  }},
  "geo": {{ "@type": "GeoCoordinates", "latitude": 26.8234, "longitude": -80.0559 }},
  "hasMap": "https://www.google.com/maps/search/?api=1&query=733+US+Highway+1+Suite+2A+North+Palm+Beach+FL+33408",
  "areaServed": [{{"@type": "City", "name": "North Palm Beach"}}, {{"@type": "City", "name": "Palm Beach Gardens"}}, {{"@type": "City", "name": "Jupiter"}}, {{"@type": "City", "name": "Juno Beach"}}, {{"@type": "City", "name": "Tequesta"}}, {{"@type": "City", "name": "Lake Park"}}, {{"@type": "City", "name": "Palm Beach"}}, {{"@type": "City", "name": "Palm Beach Shores"}}, {{"@type": "City", "name": "Riviera Beach"}}, {{"@type": "City", "name": "West Palm Beach"}}],
  "openingHoursSpecification": [{{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00", "closes": "17:30"
  }}, {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Saturday"],
    "opens": "08:00", "closes": "12:30"
  }}],
  "sameAs": ["https://www.instagram.com/firstrehabnpb","https://www.facebook.com/FirstRehabNPB/","https://www.linkedin.com/company/firstrehabnpb","https://open.spotify.com/show/033A1BQq9qqsygFFCq9SIu","https://www.youtube.com/channel/UCFzCl3RvdVahfIjKZ1SfRvQ","https://www.tiktok.com/@firstrehabilitation","https://x.com/first_rehab_npb","https://maps.google.com/?cid=3809434844265673488"]
}}</script>
{extra_schema}</head>
<body>
"""

def nav(depth=0, solid=False):
    p = "../" * depth
    cls = "site-header solid" if solid else "site-header"
    conditions = [
        ("Overview of Treatments", "index.html"),
        ("Back Pain Relief", "back-pain.html"),
        ("Neck Pain", "neck-pain.html"),
        ("Shoulder Pain Relief", "shoulder-pain.html"),
        ("Knee Pain Relief", "knee-pain.html"),
        ("Hip Pain Relief", "hip-pain.html"),
        ("Foot Pain Relief", "foot-pain.html"),
        ("Ankle Pain Relief", "ankle-pain.html"),
        ("Hand &amp; Wrist", "hand-wrist.html"),
        ("Headache Relief", "headache-relief.html"),
        ("Post-Surgical Rehab", "post-surgical.html"),
        ("Workers' Comp", "workers-comp.html"),
        ("Auto Accident", "auto-accident.html"),
    ]
    cond_links = "".join(f'<a href="{p}treatments/{u}">{n}</a>' for n, u in conditions)
    return f"""
<header class="{cls}">
  <a class="skip-link" href="#main">Skip to main content</a>
  <div class="wrap nav-bar">
    <a class="brand" href="/" aria-label="First Rehabilitation home">
      <img class="logo-dark-v" src="{p}assets/media/logo-dark-nav.png" alt="First Rehabilitation of North Palm Beach" width="111" height="68">
      <img class="logo-light-v" src="{p}assets/media/logo-nav.png" alt="First Rehabilitation of North Palm Beach" width="111" height="68">
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav-el" aria-label="Main menu">
    <ul class="nav-links">
      <li><a class="nav-item" href="/">Home</a></li>
      <li>
        <a class="nav-item" href="{p}services/physical-therapy.html">Services</a>
        <div class="dropdown">
          <a href="{p}services/physical-therapy.html">Physical Therapy</a>
          <a href="{p}services/occupational-therapy.html">Occupational Therapy</a>
          <a href="{p}services/hand-therapy.html">Hand Therapy</a>
          <a href="{p}services/wellness.html">Wellness &amp; Gym</a>
        </div>
      </li>
      <li>
        <a class="nav-item" href="{p}treatments/index.html">Conditions</a>
        <div class="dropdown"><div class="dd-cols">{cond_links}</div></div>
      </li>
      <li><a class="nav-item" href="{p}about.html">About</a></li>
      <li><a class="nav-item" href="{p}blog/index.html">Blog</a></li>
      <li>
        <a class="nav-item" href="{p}podcast.html">Podcast</a>
        <div class="dropdown">
          <a href="{p}podcast.html">Audio Episodes</a>
          <a href="{p}videos.html">Video Episodes</a>
          <a href="{p}guests.html">Our Guests</a>
        </div>
      </li>
      <li><a class="nav-item" href="{p}faq.html">FAQ</a></li>
      <li><a class="nav-item" href="{p}contact.html">Contact</a></li>
      <li class="nav-portal"><a class="nav-item" href="{PORTAL}" target="_blank" rel="noopener">Portal</a></li>
    </ul>
    </nav>
    <a class="btn btn-coral nav-cta-btn" href="{p}contact.html">Book Appointment</a>
  </div>
</header>
"""

SOCIAL_ICONS = {
    "Instagram": (INSTAGRAM, '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>'),
    "Facebook": (FACEBOOK, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.7h2.6l.4-3h-3V8.4c0-.87.24-1.46 1.49-1.46h1.59V4.25c-.27-.04-1.22-.12-2.32-.12-2.3 0-3.86 1.4-3.86 3.98v2.22H7.8v3h2.6V21h3.1z"/></svg>'),
    "LinkedIn": (LINKEDIN, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 8.5H3.86V20h3.08V8.5zM5.4 3.5a1.78 1.78 0 1 0 0 3.56 1.78 1.78 0 0 0 0-3.56zM20.14 13.28c0-3.3-1.76-4.98-4.1-4.98-1.88 0-2.72 1.03-3.19 1.76V8.5H9.77V20h3.08v-6.07c0-1.6.72-2.55 2.06-2.55 1.29 0 2.15.86 2.15 2.55V20h3.08v-6.72z"/></svg>'),
    "Spotify": (SPOTIFY, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm4.44 14.5a.7.7 0 0 1-.96.24c-2.63-1.6-5.94-1.97-9.84-1.08a.7.7 0 1 1-.31-1.37c4.27-.97 7.94-.54 10.87 1.25.33.2.44.63.24.96zm1.3-2.96a.87.87 0 0 1-1.2.3c-3.01-1.85-7.6-2.38-11.16-1.3a.87.87 0 1 1-.5-1.67c4.07-1.23 9.12-.63 12.57 1.48.4.25.53.78.29 1.19zm.12-3.09C14.27 8.3 8.3 8.1 4.86 9.15a1.05 1.05 0 1 1-.6-2c3.94-1.2 10.5-.97 14.63 1.48a1.05 1.05 0 0 1-1.07 1.82z"/></svg>'),
    "YouTube": (YOUTUBE, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.58 7.19c-.23-.86-.9-1.54-1.76-1.77C18.25 5 12 5 12 5s-6.25 0-7.82.42c-.86.23-1.53.91-1.76 1.77C2 8.77 2 12 2 12s0 3.23.42 4.81c.23.86.9 1.54 1.76 1.77C5.75 19 12 19 12 19s6.25 0 7.82-.42c.86-.23 1.53-.91 1.76-1.77C22 15.23 22 12 22 12s0-3.23-.42-4.81zM10 15.02V8.98L15.2 12 10 15.02z"/></svg>'),
    "TikTok": (TIKTOK, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.82A4.28 4.28 0 0 1 15.54 3h-3.09v12.4a2.59 2.59 0 0 1-2.59 2.5 2.59 2.59 0 1 1 .76-5.07v-3.1a5.66 5.66 0 0 0-.76-.05A5.68 5.68 0 1 0 15.54 15.4V9.01a7.35 7.35 0 0 0 4.3 1.38V7.3a4.29 4.29 0 0 1-3.24-1.48z"/></svg>'),
    "X": (TWITTER, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.53 3h3.02l-6.6 7.54L21.7 21h-6.06l-4.75-6.2L5.46 21H2.44l7.05-8.06L2.3 3h6.21l4.29 5.67L17.53 3zm-1.06 16.18h1.67L7.6 4.73H5.81l10.66 14.45z"/></svg>'),
}

def social_row(cls=""):
    links = "".join(
        f'<a class="soc-btn" href="{url}" target="_blank" rel="noopener" aria-label="First Rehabilitation on {name}" title="{name}">{svg}</a>'
        for name, (url, svg) in SOCIAL_ICONS.items()
    )
    return f'<div class="soc-row {cls}">{links}</div>'

def p2p_mini(depth=0):
    """Floating mini-player: a small button beside the intake launcher that
    opens the latest Pain 2 Power episode. Collapsed on every page load — it
    only opens on click, never on hover or a timer. The Spotify iframe is
    injected on first open, so nothing third-party loads until asked."""
    import re as _re
    if not EPISODES:
        return ""
    num, title, _desc, url, _label = EPISODES[0]
    m = _re.search(r"open\.spotify\.com/episode/([A-Za-z0-9]+)", url)
    if not m:
        return ""
    p = "../" * depth
    embed = f"https://open.spotify.com/embed/episode/{m.group(1)}?utm_source=generator&amp;theme=0"
    return f'''<div class="p2p-mini" data-p2p>
  <div class="p2p-panel" id="p2p-panel" hidden>
    <div class="p2p-head">
      <span class="p2p-eyebrow">Latest Episode</span>
      <button class="p2p-x" type="button" aria-label="Close player">&#10005;</button>
    </div>
    <p class="p2p-title">{num} &middot; {title}</p>
    <div class="p2p-embed" data-embed="{embed}" data-embed-title="{title} — Pain 2 Power"></div>
    <a class="p2p-more" href="{p}podcast.html">All episodes <span class="arr">&rarr;</span></a>
  </div>
  <button class="p2p-btn" type="button" aria-expanded="false" aria-controls="p2p-panel"
          title="Play the latest Pain 2 Power episode">
    <img src="{p}assets/media/p2p-badge.jpg?v={asset_v('assets/media/p2p-badge.jpg')}" alt="" width="62" height="62" loading="lazy">
    <span class="p2p-play" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="15" height="15"><path fill="currentColor" d="M8 5v14l11-7z"/></svg>
    </span>
    <span class="sr-only">Play the latest Pain 2 Power episode</span>
  </button>
</div>'''

def footer(depth=0):
    p = "../" * depth
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="f-brand">
        <img src="{p}assets/media/logo-dark-nav.png" alt="First Rehabilitation logo" width="111" height="68" loading="lazy">
        <div class="brand-name">First Rehabilitation</div>
        <div class="brand-tag">Heal. Strengthen. Thrive.</div>
        <p>Family-owned outpatient rehabilitation serving the Palm Beaches since 1991. Physical therapy, occupational therapy, certified hand therapy, and wellness — all under one roof.</p>
        {social_row()}
      </div>
      <div>
        <h2 class="f-head">Services</h2>
        <ul>
          <li><a href="{p}services/physical-therapy.html">Physical Therapy</a></li>
          <li><a href="{p}services/occupational-therapy.html">Occupational Therapy</a></li>
          <li><a href="{p}services/hand-therapy.html">Hand Therapy</a></li>
          <li><a href="{p}services/wellness.html">Wellness &amp; Gym</a></li>
        </ul>
      </div>
      <div>
        <h2 class="f-head">Explore</h2>
        <ul>
          <li><a href="{p}treatments/index.html">What We Treat</a></li>
          <li><a href="{p}exercises.html">Home Exercise Library</a></li>
          <li><a href="{p}about.html">About Us</a></li>
          <li><a href="{p}first-visit.html">Your First Visit</a></li>
          <li><a href="{p}insurance.html">Insurance &amp; Medicare</a></li>
          <li><a href="{p}glossary.html">Patient Glossary</a></li>
          <li><a href="{p}things-to-do.html">Things to Do in North County</a></li>
          <li><a href="{p}blog/index.html">Blog</a></li>
          <li><a href="{p}podcast.html">Pain 2 Power Podcast</a></li>
          <li><a href="{p}videos.html">Video Episodes</a></li>
          <li><a href="{p}guests.html">Podcast Guests</a></li>
          <li><a href="{p}faq.html">FAQ</a></li>
          <li><a href="{p}careers.html">Careers</a></li>
          <li><a href="{PORTAL}" target="_blank" rel="noopener">Patient Portal</a></li>
        </ul>
      </div>
      <div>
        <h2 class="f-head">Areas We Serve</h2>
        <ul>
          <li><a href="{p}locations/palm-beach-gardens.html">Palm Beach Gardens</a></li>
          <li><a href="/">North Palm Beach</a></li>
          <li><a href="{p}locations/juno-beach.html">Juno Beach</a></li>
          <li><a href="{p}locations/jupiter.html">Jupiter</a></li>
          <li><a href="{p}locations/tequesta.html">Tequesta</a></li>
          <li><a href="{p}locations/lake-park.html">Lake Park</a></li>
          <li><a href="{p}locations/palm-beach.html">Palm Beach</a></li>
          <li><a href="{p}locations/west-palm-beach.html">West Palm Beach</a></li>
          <li><a href="{p}locations/riviera-beach.html">Riviera Beach</a></li>
        </ul>
      </div>
      <div>
        <h2 class="f-head">Visit Us</h2>
        <ul class="f-contact">
          <li>733 US Highway 1, Suite 2A<br>North Palm Beach, FL 33408</li>
          <li>Phone: <a href="tel:+15616244263">{PHONE}</a></li>
          <li>Fax: {FAX}</li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <span>&copy; 2026 First Rehabilitation of North Palm Beach. All rights reserved.</span>
      <span><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a> &nbsp;&middot;&nbsp; <a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a> &nbsp;&middot;&nbsp; <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> &nbsp;&middot;&nbsp; <a href="{SPOTIFY}" target="_blank" rel="noopener">Spotify</a> &nbsp;&middot;&nbsp; <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a> &nbsp;&middot;&nbsp; <a href="{TWITTER}" target="_blank" rel="noopener">X</a></span>
    </div>
  </div>
</footer>
<a class="mobile-call" href="tel:+15616244263" aria-label="Call First Rehabilitation now at 561-624-4263"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.4 21 3 13.6 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg><span>Call Now</span></a>
{p2p_mini(depth)}
<script src="{p}assets/js/main.js?v={asset_v('assets/js/main.js')}"></script>
<script src="{p}assets/js/intake.js?v={asset_v('assets/js/intake.js')}" defer></script>
<script src="{p}assets/js/p2p-mini.js?v={asset_v('assets/js/p2p-mini.js')}" defer></script>
<!-- Vercel Web Analytics (static-site tag; privacy-friendly, cookieless — no banner needed) -->
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

def appt_form(heading="Request an Appointment", sub=None, wrapped=True, depth=0):
    # The five-field contact form. Until 2026-09-09 this markup lived inline in
    # build_contact() and so existed on exactly one page — and that one page
    # produced 34 of the site's 41 lifetime leads, while every service,
    # condition, location and blog page produced zero between them. Those pages
    # were never short of calls to action; they carried three to five links each
    # to the phone number and to contact.html. They were short of somewhere to
    # convert: their only job was to send the reader one hop further, and 84% of
    # visitors never took it.
    #
    # So the form is a function now, and interior pages embed the real thing.
    # `wrapped=False` returns the bare card for the contact page, which places it
    # inside its own two-column grid.
    #
    # intake.js binds by getElementById('appt-form'), so exactly one of these may
    # appear per page — hence no id suffixing here. It records location.pathname
    # as the lead's `page`, so per-page attribution keeps working for free.
    # Insurance select added 2026-10-14: 74 of 79 real leads arrived with no insurance,
    # so every callback started with a question the front desk could have answered
    # before dialing (verify benefits first). Optional, so it costs no conversions;
    # options come from PLANS so the list can never drift from the insurance page.
    sub = sub or ("Tell us a little about what you need and our front desk will call "
                  "you back within one business day.")
    card = f"""<div class="appt-form-card reveal">
      <h2 class="h3-size">{heading}</h2>
      <p class="af-sub">{sub}</p>
      <form class="appt-form" id="appt-form" novalidate>
        <div class="af-field">
          <label for="af-name">Full name *</label>
          <input id="af-name" name="name" type="text" autocomplete="name" required maxlength="200">
        </div>
        <div class="af-two">
          <div class="af-field">
            <label for="af-phone">Phone *</label>
            <input id="af-phone" name="phone" type="tel" autocomplete="tel" required maxlength="40" placeholder="561-555-1234">
          </div>
          <div class="af-field">
            <label for="af-email">Email</label>
            <input id="af-email" name="email" type="email" autocomplete="email" maxlength="200">
          </div>
        </div>
        <div class="af-field">
          <label for="af-reason">Reason for visit *</label>
          <textarea id="af-reason" name="reason" required maxlength="2000" placeholder="e.g. knee pain after surgery, hand therapy follow-up&hellip;"></textarea>
        </div>
        <div class="af-two">
          <div class="af-field">
            <label for="af-ins">Insurance</label>
            <select id="af-ins" name="insurance">
              <option value="">Choose (optional)</option>
              {"".join(f'<option>{p}</option>' for p in PLANS)}
              <option>Other / not sure</option>
            </select>
          </div>
          <div class="af-field">
            <label for="af-time">Preferred call time</label>
            <select id="af-time" name="time">
              <option>Anytime</option>
              <option>Morning</option>
              <option>Afternoon</option>
            </select>
          </div>
        </div>
        <p class="af-note">This is a contact request, not a medical intake — please don't include detailed medical history or sensitive health information here. We only need the basics to call you back.</p>
        <p class="af-error" id="af-error" role="alert"></p>
        <button class="btn btn-coral" type="submit">Send Request <span class="arr">&rarr;</span></button>
      </form>
      <div class="af-done" id="af-done" hidden>
        <div class="af-check">&#10003;</div>
        <h3>Request received!</h3>
        <p id="af-done-msg">Thank you — our front desk will call you back within one business day. Need us sooner? Call <a href="tel:+15616244263">{PHONE}</a>.</p>
      </div>
    </div>"""
    if not wrapped:
        return card
    return f"""
<section class="section on-cream" id="request">
  <div class="wrap appt-form-solo">
    {card}
  </div>
</section>
"""


def cta_band(depth=0, heading='Life is too short to <em>live in pain.</em>', sub="Start your recovery today with a team dedicated to your long-term wellness and total healing."):
    p = "../" * depth
    return f"""
<section class="cta-band">
  <div class="hero-fallback"></div>
  <div class="beam-field" aria-hidden="true"><div class="beam"></div><div class="beam b2"></div></div>
  <div class="wrap cta-inner reveal">
    <h2>{heading}</h2>
    <p>{sub}</p>
    <a class="btn btn-coral" href="{p}contact.html">Start Your Recovery Today <span class="arr">&rarr;</span></a>
  </div>
</section>
"""

def page_hero(eyebrow, title, lede, crumbs_html="", cta_href=None, cta_label="Book Appointment", loop=None):
    # Condition, location and treatment-hub pages used to carry zero booking
    # CTA until a reader scrolled past the intro to a side-card or the very
    # bottom cta_band — the header link was doing nearly all the work despite
    # these pages earning real search traffic (see 2026-09 conversion-tracking
    # pull). An optional button here puts one where the reader already is.
    cta_html = (f'<div class="mt-2"><a class="btn btn-coral" href="{cta_href}">{cta_label} '
                f'<span class="arr">&rarr;</span></a></div>') if cta_href else ""
    if loop:
        return _video_page_hero(eyebrow, title, lede, crumbs_html, loop)
    return f"""
<section class="page-hero">
  <div class="hero-fallback"></div>
  <div class="beam-field" aria-hidden="true"><div class="beam" style="opacity:0.5;"></div></div>
  <div class="wrap">
    {crumbs_html}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {cta_html}
  </div>
</section>
"""

# Pain 2 Power sizzle reels, cut from the Episode 9-16 masters (Dave + Mike only).
# Each page hero plays a silent, text-free loop; the button opens the trailer with
# sound. Loops ship with NO <source> and preload="none" — main.js attaches ONE
# rendition (720p under 768px, 1080p above), same as the homepage lighthouse.
# Every file here is linked through asset_v(), so a re-encode busts its own cache.
P2P_LOOPS = {
    "audio": "p2p-hero-audio",
    "video": "p2p-hero-video",
    # Not Pain 2 Power: Nick's own drone pass over Juno Beach Pier (Dropbox
    # /Juno.MP4, 2688x1512), 0.8x slow with a 0.6s crossfade loop. Heads
    # /things-to-do.html. Same media contract; no trailer button.
    "juno": "ttd-hero-juno",
}
LOOP_LABELS = {
    "audio": "Dr. Dave Kashuba and Mike McGann on air in the Pain 2 Power studio at 100.3 Legends Radio",
    "video": "Dr. Dave Kashuba and Mike McGann on air in the Pain 2 Power studio at 100.3 Legends Radio",
    "juno": "Drone flight along Juno Beach Pier and the beach north of it, Juno Beach, Florida",
}
P2P_TRAILER = {
    "mp4": "assets/media/p2p-trailer.mp4",
    "poster": "assets/media/p2p-trailer-poster.jpg",
    "uploaded": "2026-10-14",
    "duration": "PT64S",
}

def _m(path):
    """Root-relative media URL with its content-hash cache-buster."""
    return f"{path}?v={asset_v(path)}"

def p2p_poster_preload(kind):
    return (f'<link rel="preload" as="image" href="{_m(f"assets/media/{P2P_LOOPS[kind]}-poster.jpg")}" '
            f'fetchpriority="high">\n')

def _video_page_hero(eyebrow, title, lede, crumbs_html, kind):
    base = f"assets/media/{P2P_LOOPS[kind]}"
    trailer_btn = trailer_dlg = ""
    if kind in ("audio", "video"):
        trailer_btn = ('<div class="mt-2"><button class="btn btn-coral trailer-open" type="button" aria-haspopup="dialog">\n'
                       '      <span aria-hidden="true">&#9654;</span> Watch the Trailer</button></div>')
        trailer_dlg = f"""<dialog class="trailer-modal" aria-label="Pain 2 Power trailer">
  <button class="trailer-close" type="button" aria-label="Close trailer">&times;</button>
  <video controls playsinline preload="none" poster="{_m(P2P_TRAILER['poster'])}"
    data-src="{_m(P2P_TRAILER['mp4'])}"></video>
</dialog>
"""
    return f"""
<section class="page-hero has-video hero-loop-{kind}">
  <div class="hero-media">
    <div class="hero-fallback"></div>
    <video autoplay muted loop playsinline preload="none" poster="{_m(base + '-poster.jpg')}"
      aria-label="{LOOP_LABELS[kind]}"
      data-mp4-full="{_m(base + '-hd.mp4')}"
      data-webm-full="{_m(base + '-hd.webm')}"
      data-mp4-mobile="{_m(base + '-mobile.mp4')}"
      data-webm-mobile="{_m(base + '-mobile.webm')}"></video>
    <button class="hero-pause" type="button" aria-label="Pause background video" aria-pressed="false">&#10073;&#10073;</button>
  </div>
  <div class="hero-scrim"></div>
  <div class="wrap">
    {crumbs_html}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {trailer_btn}
  </div>
</section>
{trailer_dlg}"""

def _trailer_schema():
    """VideoObject for the self-hosted Pain 2 Power trailer, tied to the org."""
    import json as _json
    base = "https://www.firstrehabnpb.com/"
    node = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "@id": base + "#p2p-trailer",
        "name": "Pain 2 Power Trailer: Dr. Dave Kashuba, Mike McGann and Guests",
        "description": "A one-minute trailer for Pain 2 Power, the physical rehab and wellness show hosted by "
                       "Dr. Dave Kashuba of First Rehabilitation of North Palm Beach with Mike McGann, with "
                       "guests including orthopaedic shoulder surgeon Dr. Vani Sabesan, radiologist Dr. Don "
                       "Goodwin, registered dietitian Elyse Marrone and Captain Kerry Titheradge. "
                       "Saturdays at 8:30 AM on 100.3 Legends Radio.",
        "thumbnailUrl": base + P2P_TRAILER["poster"],
        "contentUrl": base + P2P_TRAILER["mp4"],
        "uploadDate": P2P_TRAILER["uploaded"],
        "duration": P2P_TRAILER["duration"],
        "publisher": {"@id": base + "#organization"},
    }
    return '<script type="application/ld+json">' + _json.dumps(node, ensure_ascii=False) + '</script>\n'

def linkify_phone(html_out):
    """Every visible mention of the clinic phone number becomes a tap-to-call link.
    Existing anchors are protected so we never nest a link inside a link."""
    import re
    protected = []
    def _protect(m):
        protected.append(m.group(0))
        return f"\x00{len(protected) - 1}\x00"
    # <head> is protected wholesale: a tel: anchor is never wanted inside a
    # title, a meta description or a JSON-LD block, and injecting one there
    # silently truncates the snippet Google shows. (contact.html shipped that
    # way; putting the phone number in more descriptions exposed it.)
    s = re.sub(r"<(a|script|head)\b[^>]*>.*?</\1>", _protect, html_out, flags=re.S)
    s = s.replace(PHONE, f'<a href="tel:+15616244263">{PHONE}</a>')
    return re.sub(r"\x00(\d+)\x00", lambda m: protected[int(m.group(1))], s)

def write(path, content):
    if path.endswith(".html"):
        content = linkify_phone(content)
        content = content.replace("<main>", '<main id="main">', 1)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)

# ----------------------------------------------------------------------------
# BODY MAP SVG
# ----------------------------------------------------------------------------

def bodymap_svg():
    spots = [
        ("headache", 150, 45, "Headaches"),
        ("neck", 150, 96, "Neck"),
        ("shoulder", 95, 116, "Shoulder"),
        ("back", 150, 205, "Back &amp; Spine"),
        ("handwrist", 227, 328, "Hand &amp; Wrist"),
        ("hip", 110, 316, "Hip"),
        ("knee", 172, 442, "Knee"),
        ("ankle", 139, 570, "Ankle"),
        ("foot", 172, 598, "Foot"),
    ]
    spot_links = {
        "headache": "treatments/headache-relief.html", "neck": "treatments/neck-pain.html",
        "shoulder": "treatments/shoulder-pain.html", "back": "treatments/back-pain.html",
        "handwrist": "treatments/hand-wrist.html", "hip": "treatments/hip-pain.html",
        "knee": "treatments/knee-pain.html", "ankle": "treatments/ankle-pain.html",
        "foot": "treatments/foot-pain.html",
    }
    def _chip(x, y, lbl):
        """Hover/active label chip inside the SVG, flipped to whichever side fits."""
        plain = html.unescape(lbl)
        w = round(len(plain) * 6.6 + 18)
        rx = x + 15 if x < 150 else x - 15 - w
        rx = max(42, min(rx, 258 - w))
        ry = y - 10
        return (f'<g class="bm-chip"><rect x="{rx}" y="{ry}" width="{w}" height="20" rx="10"/>'
                f'<text x="{rx + w / 2}" y="{ry + 14}" text-anchor="middle">{lbl}</text></g>')

    spots_svg = "".join(
        f'''<a href="{spot_links[k]}" class="bm-spot" data-bm="{k}" aria-label="{lbl}">
        <circle class="hit" cx="{x}" cy="{y}" r="17" fill="#000" fill-opacity="0" pointer-events="all"/>
        <circle class="halo" cx="{x}" cy="{y}" r="10"/>
        <circle class="core" cx="{x}" cy="{y}" r="6"/>
        {_chip(x, y, lbl)}
        <title>{lbl}</title></a>''' for k, x, y, lbl in spots
    )
    silhouette = """
    <circle class="bm-silhouette" cx="150" cy="52" r="30"/>
    <path class="bm-silhouette" d="M150,92
      C156,92 162,94 168,98 C182,104 198,108 208,118 C214,124 218,140 221,160
      C223,190 225,225 224,225 C227,260 230,285 233,315 C235,330 233,340 227,341
      C221,342 217,333 215,320 C211,290 208,260 204,225 C202,205 200,185 197,168
      C196,162 193,158 190,158 C191,190 190,220 188,248 C189,275 194,295 197,315
      C197,350 193,395 188,440 C185,480 181,525 177,568 C176,580 178,592 186,596
      C188,602 180,606 172,604 C164,602 160,594 160,582 C160,540 158,480 157,430
      C156,400 153,370 150,352 C147,370 144,400 143,430 C142,480 140,540 140,582
      C140,594 136,602 128,604 C120,606 112,602 114,596 C122,592 124,580 123,568
      C119,525 115,480 112,440 C107,395 103,350 103,315 C106,295 111,275 112,248
      C110,220 109,190 110,158 C107,158 104,162 103,168 C100,185 98,205 96,225
      C92,260 89,290 85,320 C83,333 79,342 73,341 C67,340 65,330 67,315
      C70,285 73,260 76,225 C77,190 79,160 79,160 C82,140 86,124 92,118
      C102,108 118,104 132,98 C138,94 144,92 150,92 Z"/>
    """
    defs = ('<defs><linearGradient id="bmFig" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%" stop-color="rgba(246,241,231,0.17)"/>'
            '<stop offset="100%" stop-color="rgba(246,241,231,0.05)"/></linearGradient></defs>')
    platform = '<ellipse class="bm-platform" cx="150" cy="614" rx="92" ry="14"/>'
    return f'<svg viewBox="40 0 220 640" role="group" aria-label="Interactive body map — choose where it hurts">{defs}{platform}{silhouette}{spots_svg}</svg>'

# ----------------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------------

def build_home():
    phases = [
        ("Pain &amp; Injury", "Initial assessment and diagnosis of your condition."),
        ("Evaluation", "Comprehensive clinical evaluation to determine your specific needs."),
        ("Therapy", "Personalized treatment plans focusing on movement and function."),
        ("Graduation", "Progressive discharge planning to safely return to daily life."),
        ("Wellness", "On-site gym program to maintain strength and prevent future injury."),
        ("Thriving", "Long-term management and lifestyle optimization for lasting health."),
    ]
    roman = ["I", "II", "III", "IV", "V", "VI"]
    phases_html = "".join(
        f'<div class="phase reveal d{i%3+1}"><div class="ph-dot">{roman[i]}</div><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(phases)
    )

    pathways = [
        ("01", "Physical Therapy", "Restore movement. Eliminate pain.",
         "Expert, hands-on physical therapy for pain, injuries, and post-surgical recovery — personalized from day one.",
         ["Post-Surgical Rehab", "Sports Injuries", "Balance &amp; Neuro", "Back &amp; Neck"],
         "services/physical-therapy.html", ""),
        ("02", "Occupational Therapy", "Reclaim the activities that matter.",
         "From dressing and cooking to returning to work — OT restores your independence and quality of daily life.",
         ["Daily Life Skills", "Post-Stroke", "Ergonomics", "Cognitive Rehab"],
         "services/occupational-therapy.html", ""),
        ("03", "Hand Therapy", "Restore function to your hands.",
         "Certified hand therapy for the wrist, hand, and upper extremity — one of the most specialized areas of rehabilitation.",
         ["Carpal Tunnel", "Arthritis", "Tendon &amp; Fracture", "Custom Splinting"],
         "services/hand-therapy.html", ""),
        ("04", "Wellness &amp; Gym", "Recovery doesn't stop at discharge.",
         "The Palm Beaches' clinic where PT &amp; OT patients transition into an exclusive on-site wellness program.",
         ["Personal Training", "Group Classes", "Senior Fitness", "Sports Performance"],
         "services/wellness.html", '<span class="badge-inline">Exclusive</span>'),
    ]
    pathways_html = "".join(
        f'''<a class="pathway reveal" href="{url}">
          <span class="pw-num">{num}</span>
          <div><h3>{title}{badge}</h3><span class="pw-kicker">{kick}</span></div>
          <div class="pw-body"><p>{desc}</p>
            <div class="pw-tags">{"".join(f"<span>{t}</span>" for t in tags)}</div>
          </div>
          <span class="pw-go">&rarr;</span>
        </a>''' for num, title, kick, desc, tags, url, badge in pathways
    )

    # REAL patient quotes only — never publish fabricated testimonials. (The
    # original import shipped three invented placeholders; removed 2026-07-20.)
    # These are VERBATIM public reviews pulled from the clinic's Birdeye page
    # (reviews.birdeye.com/first-rehab-148204630280391), which republishes
    # Google + Facebook reviews. Reviewer names shown as first name + last
    # initial (owner's call); platform source labels intentionally omitted.
    quotes = [
        ("After I broke 5 vertebrae in my neck I thought I'd never get out of pain or build back neck strength. But the pros at FIRST Rehab did it right … my neck is out of pain and strong and healthy. They are personally responsible for getting me back to health!",
         "Brian L."),
        ("This is a 1st class rehab facility with very caring and talented therapists. I had a great experience rehabbing from double knee replacements. Great equipment and their team approach keeps you moving the whole session. I made great progress while there and really enjoyed it!",
         "Sandy S."),
        ("Personal and individual attention from the entire staff. Dave is the BEST and has the BEST staff to rehab even the most difficult problems. I wouldn't go anywhere else!",
         "Barb K."),
    ]
    quotes_html = "".join(
        f'''<figure class="quote-card reveal d{i+1}"><div class="stars">★★★★★</div><blockquote>{q}</blockquote><figcaption><strong>{n}</strong></figcaption></figure>'''
        for i, (q, n) in enumerate(quotes)
    ) or (
        '<figure class="quote-card reveal" style="text-align:center;">'
        '<div class="stars">★★★★★</div>'
        '<blockquote>Our patients say it better than we ever could. Read their words — '
        'unedited, straight from Google.</blockquote>'
        '<figcaption><a class="btn btn-ink" href="https://maps.google.com/?cid=3809434844265673488" '
        'target="_blank" rel="noopener">Read our Google reviews <span class="arr">&rarr;</span></a></figcaption>'
        '</figure>'
    )

    news_cards = "".join(
        f'''<a class="news-card reveal" href="{n["url"]}" target="_blank" rel="noopener">
          <span class="news-outlet">{n["outlet"]}<span class="news-date">{n["date"]}</span></span>
          <h3>{n["title"]}</h3>
          <p>{n["blurb"]}</p>
          <span class="news-go">Read it <span class="arr">&rarr;</span></span>
        </a>''' for n in NEWS
    )
    # No coverage listed = no band. A heading over an empty grid reads as broken.
    news_band = f'''
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">In the News</span>
      <h2>What They&rsquo;re <em class="accent">Saying About Us</em></h2>
    </div>
    <div class="news-grid">{news_cards}</div>
  </div>
</section>
''' if NEWS else ""

    social_cards = "".join(
        f'''<a class="sm-card" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="First Rehabilitation on Instagram — photo {i}">
          {photo(f"social-{i}", sizes="(max-width:768px) 45vw, 220px", alt="")}
        </a>''' for i in range(1, 11)
        if f"social-{i}" in PHOTOS and os.path.exists(os.path.join(ROOT, PHOTOS[f"social-{i}"]["src"]))
    )

    bm_list = [
        ("back", "Back &amp; Spine", "PT"), ("neck", "Neck", "PT"),
        ("shoulder", "Shoulder", "PT"), ("knee", "Knee", "PT"),
        ("hip", "Hip &amp; Pelvis", "PT"), ("handwrist", "Hand &amp; Wrist", "OT + CHT"),
        ("foot", "Foot", "PT"), ("ankle", "Ankle", "PT"),
        ("headache", "Headaches", "PT"), ("postsurg", "Post-Surgical", "PT + OT"),
        ("workers", "Workers' Comp", "PT + OT"), ("auto", "Auto Accident", "PT"),
    ]
    bm_urls = {
        "back": "back-pain", "neck": "neck-pain", "shoulder": "shoulder-pain", "knee": "knee-pain",
        "hip": "hip-pain", "handwrist": "hand-wrist", "foot": "foot-pain", "ankle": "ankle-pain",
        "headache": "headache-relief", "postsurg": "post-surgical", "workers": "workers-comp", "auto": "auto-accident",
    }
    bm_list_html = "".join(
        f'<a class="bm-item" data-bm="{k}" href="treatments/{bm_urls[k]}.html"><span>{n}</span><span class="bm-tag">{tag}</span></a>'
        for k, n, tag in bm_list
    )

    # Data for the tap-to-learn panel, sourced from the condition pages
    import json as _json
    def _plain(s):
        import re as _re
        return _re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")
    bm_data = {}
    for k, n, tag in bm_list:
        c = CONDITIONS[bm_urls[k]]
        bm_data[k] = {
            "name": _plain(c["name"]),
            "tag": _plain(tag),
            "lede": _plain(c["lede"]),
            "treats": [_plain(t) for t in c["treats"][:4]],
            "url": f"treatments/{bm_urls[k]}.html",
        }
    bm_json = _json.dumps(bm_data)

    ticker = "".join(f"<span>{s}</span>" for s in PLANS)

    journey_svg = '''<svg class="journey-path" viewBox="0 0 1200 260" preserveAspectRatio="none" aria-hidden="true">
      <path d="M40,80 C240,80 220,170 400,170 C580,170 560,80 740,80 C920,80 900,170 1160,170"/>
    </svg>'''

    body = f"""
<main>
<section class="hero">
  <div class="hero-media">
    <div class="hero-fallback"></div>
    <!-- Sources are attached by main.js via matchMedia so exactly ONE file
         downloads: the 720p mobile encode below 768px, the 1440p above.
         preload="none" keeps the (preloaded) poster painting instantly. -->
    <video autoplay muted loop playsinline preload="none" poster="assets/media/hero-poster.jpg?v=9"
      data-mp4-full="assets/media/lighthouse-hd.mp4?v=9"
      data-webm-full="assets/media/lighthouse-hd.webm?v=10"
      data-mp4-mobile="assets/media/lighthouse-mobile.mp4?v=10"
      data-webm-mobile="assets/media/lighthouse-mobile.webm?v=10"></video>
    <button class="hero-pause" type="button" aria-label="Pause background video" aria-pressed="false">&#10073;&#10073;</button>
    <a class="hero-credit" href="https://pelicanpix.com" target="_blank" rel="noopener"
       aria-label="Aerial video by Pelican Pix Real Estate Photography"
       title="Aerial video by Pelican Pix Real Estate Photography">Pelican&nbsp;Pix</a>
  </div>
  <div class="hero-scrim"></div>
  <div class="wrap hero-inner">
    <div class="hero-panel">
      <span class="eyebrow on-dark">Serving Palm Beach County Since 1991</span>
      <h1>
        <span class="line"><span>Heal.</span></span>
        <span class="line"><span>Strengthen.</span></span>
        <span class="line"><span><em class="accent">Thrive.</em><svg class="flourish" viewBox="0 0 220 22" aria-hidden="true"><path d="M4,16 C60,4 160,4 216,14" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></span></span>
      </h1>
      <p class="hero-tag">&ldquo;Our people make the difference.&rdquo;</p>
      <p class="hero-sub">Physical therapy, occupational therapy, certified hand therapy, and an exclusive on-site wellness program — a complete continuum of care under one roof in North Palm Beach.</p>
      <div class="hero-ctas">
        <a class="btn btn-coral" href="contact.html">Book Appointment <span class="arr">&rarr;</span></a>
        <a class="btn btn-ghost" href="#pathways">Explore Our Services</a>
      </div>
    </div>
    <div class="hero-meta">
      <div><strong data-count="39" data-suffix="+">39+</strong><span>Years of Expertise</span></div>
      <div><strong data-count="180000" data-suffix="+">180,000+</strong><span>Patients Treated</span></div>
      <div><strong>4-in-1</strong><span>Programs, One Roof</span></div>
      <div><strong>Est. 1991</strong><span>Family-Owned</span></div>
    </div>
  </div>
  <div class="scroll-hint"><span></span></div>
</section>

<div class="ins-strip"><div class="ticker">{ticker}</div></div>

<section class="section" id="pathways">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">What We Offer</span>
      <h2>Physical &amp; Occupational Therapy<br>in <em class="accent">North Palm Beach</em></h2>
      <p class="lede">From your first appointment to lifelong wellness — we're with you every step.</p>
    </div>
    <div class="pathways">{pathways_html}</div>
  </div>
</section>

<section class="section on-ink" id="bodymap">
  <div class="beam-field" aria-hidden="true"><div class="beam" style="opacity:0.55;"></div></div>
  <div class="wrap" style="position:relative;z-index:1;">
    <div class="section-head reveal">
      <span class="eyebrow">Where Does It Hurt?</span>
      <h2>Tap It. <em class="accent">We'll Take It From There.</em></h2>
      <p class="lede">Choose the area closest to your pain to see what we treat there and how — every pathway begins with a thorough evaluation.</p>
    </div>
    <div class="bodymap-grid three">
      <div class="bodymap-fig reveal">{bodymap_svg()}</div>
      <div class="bm-list reveal d2">{bm_list_html}</div>
      <aside class="bm-panel reveal d3" id="bm-panel" aria-live="polite">
        <div class="bm-panel-default">
          <span class="eyebrow on-dark">Your Guide</span>
          <h3>Select a glowing point</h3>
          <p>Tap any area on the figure — or any condition in the list — and we'll show you what we treat there and how we approach it.</p>
        </div>
      </aside>
    </div>
  </div>
  <script type="application/json" id="bm-data">{bm_json}</script>
</section>

<section class="section on-cream">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">The Continuum of Care</span>
      <h2>From First Visit to <em class="accent">Full Life</em></h2>
      <p class="lede">Six phases. One journey — from initial injury through complete recovery and long-term wellness.</p>
    </div>
    <div class="journey">{journey_svg}<div class="continuum-track">{phases_html}</div></div>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap split">
    <div class="split-media tilt reveal">
      {photo("treatment", sizes="(max-width:900px) 92vw, 560px")}
    </div>
    <div class="reveal d2">
      <span class="eyebrow">Our Story</span>
      <h2>Three Decades of Healing, <em class="accent">One Vision</em></h2>
      <p style="margin-top:1.2rem;">Since 1991, First Rehabilitation of North Palm Beach has been a cornerstone of recovery for the Palm Beaches. Founded by David Kashuba, Ph.D., our mission has always been to provide a comprehensive, high-end approach to rehabilitation — healing the body and restoring the spirit.</p>
      <div class="stat-row">
        <div><strong data-count="39" data-suffix="+">39+</strong><span>Years of Expertise</span></div>
        <div><strong data-count="180000" data-suffix="+">180,000+</strong><span>Patients Treated</span></div>
        <div><strong>4.9★</strong><span>Google Rating</span></div>
        <div><strong>Family</strong><span>Owned &amp; Operated</span></div>
      </div>
      <div class="mt-2"><a class="text-link" href="about.html">Meet our team &rarr;</a></div>
    </div>
  </div>
</section>

<section class="section on-cream">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Voices of Recovery</span>
      <h2><a href="https://maps.google.com/?cid=3809434844265673488" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;">4.9 <span style="color:var(--coral-text);">★</span> on Google</a></h2>
    </div>
    <div class="quote-grid"{'' if quotes else ' style="grid-template-columns:min(640px,100%);justify-content:center;"'}>{quotes_html}</div>
  </div>
</section>
{news_band}
<section class="social-band on-paper section" style="padding-bottom:0;">
  <div class="wrap">
    <div class="section-head center reveal" style="margin-bottom:2rem;">
      <span class="eyebrow">Follow Along</span>
      <h2>Life at <em class="accent">First Rehab</em></h2>
      <p class="lede">Moments from the clinic, the gym floor, and the <a class="text-link" href="podcast.html">Pain 2 Power</a> studio — <a class="text-link" href="{INSTAGRAM}" target="_blank" rel="noopener">@firstrehabnpb</a></p>
    </div>
  </div>
  <div class="marquee-mask"><div class="marquee">{social_cards}</div></div>
  <div style="height:clamp(4.5rem,9vw,8.5rem);"></div>
</section>

<section class="section on-paper" style="padding-top:0;">
  <div class="wrap">
    <p class="related-links reveal" style="text-align:center;"><strong>Also serving:</strong> <a href="locations/west-palm-beach.html">West Palm Beach</a> &middot; <a href="locations/palm-beach-gardens.html">Palm Beach Gardens</a> &middot; <a href="locations/palm-beach.html">Palm Beach</a> &middot; <a href="locations/juno-beach.html">Juno Beach</a> &middot; <a href="locations/jupiter.html">Jupiter</a> &middot; <a href="locations/tequesta.html">Tequesta</a> &middot; <a href="locations/lake-park.html">Lake Park</a> &middot; <a href="locations/riviera-beach.html">Riviera Beach</a></p>
  </div>
</section>

{cta_band(0)}
</main>
"""
    write("index.html",
          head("Physical Therapy North Palm Beach | First Rehab, Since 1991",
               "Family-owned physical, occupational and certified hand therapy in North Palm Beach since 1991. One-on-one care, 4.9★ on Google, Medicare accepted. Book today.",
               canonical="", og_image=PHOTOS["treatment"]["src"],
               extra_schema='<link rel="preload" as="image" href="assets/media/hero-poster.jpg?v=9" fetchpriority="high">\n')
          + nav(0) + body + footer(0))

# ----------------------------------------------------------------------------
# SERVICE PAGES
# ----------------------------------------------------------------------------

SERVICES = {
    "physical-therapy": {
        "seo_title": "Physical Therapy & Rehabilitation Services | North Palm Beach",
        "seo_desc": "One-on-one physical therapy and rehabilitation for pain, injury and post-surgical recovery, from a family-owned North Palm Beach clinic open since 1991.",
        "title": "Physical Therapy",
        "kicker": "Restore movement. Eliminate pain.",
        "lede": "Expert, hands-on physical therapy for pain, injuries, and post-surgical recovery — personalized from your very first visit.",
        "intro": "Physical therapy at First Rehabilitation begins with a comprehensive movement-based evaluation. Our therapists identify the patterns limiting you, then build a personalized plan combining skilled manual therapy, targeted exercise, and progressive functional training — so you don't just feel better, you move better for good.",
        "items": [
            ("Post-Surgical Rehabilitation", "Structured recovery protocols for joint replacements, spinal surgery, rotator cuff repair, and more — coordinated with your surgeon."),
            ("Sports Injury Recovery", "Return-to-play programs that rebuild strength, agility, and confidence after sprains, strains, and overuse injuries."),
            ("Balance &amp; Neurological Rehab", "Fall prevention, vestibular work, and neuro-focused therapy to restore stability and independence."),
            ("Back &amp; Neck Pain", "Manual therapy, posture correction, and core strengthening to resolve spinal pain at its source."),
            ("Auto &amp; Work Injuries", "Documentation-ready care for auto accident and workers' compensation cases, with clear communication to all parties."),
            ("Chronic Pain Management", "Graded, evidence-based programs that help you reclaim activity without fear of flare-ups."),
            # Added 2026-09-20. Both of these were advertised on the Google
            # Business Profile and appeared NOWHERE on this site or in SERVICES,
            # so anyone tapping the service on the listing landed on a site that
            # never mentioned it. Owner confirmed both are real.
            #
            # Wording is adapted from the clinic's own GBP service descriptions,
            # which are owner-authored, rather than invented here. Massage is
            # also corroborated repeatedly in the Google reviews, where patients
            # describe heat and massage as part of a session and contrast it
            # favourably with clinics that gave them neither.
            #
            # Deliberately items on this page rather than two new service pages:
            # CLAUDE.md's 2026-09-09 finding is that new pages land on page two
            # or three and add impressions nobody clicks, which drags site-wide
            # CTR. Depth on a page that already ranks beats breadth.
            ("Therapeutic Massage", "Soft-tissue work offered alongside your physical, occupational, or hand therapy program \u2014 part of a well-rounded approach to recovery, not an add-on you book separately."),
            ("Concierge Therapy", "The same therapist-led, hands-on care with added scheduling flexibility and availability, for patients who want more than a standard program allows. Call 561-624-4263 to ask what is open."),
        ],
    },
    "occupational-therapy": {
        "seo_title": "Occupational Therapy | North Palm Beach & West Palm Beach",
        "seo_desc": "Occupational therapy that restores daily independence after injury or surgery, from dressing and cooking to returning to work. Serving Palm Beach County.",
        "title": "Occupational Therapy",
        "kicker": "Reclaim the activities that matter.",
        "lede": "From dressing and cooking to returning to work — occupational therapy restores your independence and quality of daily life.",
        "intro": "Occupational therapy is about the life you want to live. Our OTs assess how your condition affects real daily activities — self-care, home management, work tasks — and rebuild the strength, coordination, and strategies you need to do them confidently again.",
        "items": [
            ("Activities of Daily Living", "Practical retraining for dressing, bathing, cooking, and the everyday skills independence depends on."),
            ("Post-Stroke Recovery", "Task-specific therapy to restore upper-extremity function, coordination, and daily routines after stroke."),
            ("Ergonomics &amp; Adaptive Equipment", "Workstation assessment and equipment recommendations that make daily tasks safer and easier."),
            ("Hand &amp; Upper Extremity Function", "Fine-motor and functional-use training in coordination with our certified hand therapy program."),
            ("Cognitive Rehabilitation", "Memory, attention, and problem-solving strategies for safe, confident daily living."),
            ("Return-to-Work Programs", "Graded conditioning and task simulation to get you safely back on the job."),
        ],
    },
    "hand-therapy": {
        "seo_title": "Certified Hand Therapist | North Palm Beach & Jupiter FL",
        "seo_desc": "Certified hand therapist in North Palm Beach treating carpal tunnel, trigger finger, thumb arthritis, tendon repairs and wrist fractures. Splints made on-site.",
        "title": "Hand Therapy",
        "kicker": "Restore function to your hands.",
        "lede": "Certified hand therapy for the wrist, hand, and upper extremity — one of the most precise and specialized areas of rehabilitation.",
        # Answer-first, 2026-10-14: "hand therapist" (263 impr, pos 30.8) and "hand
        # therapist near me" are practitioner searches, so the opener names the
        # practitioner and what she treats before anything else.
        "intro": "Our certified hand therapist, Laura Drumm, MS, OTR/L, CHT, CLT, treats the hand, wrist, elbow and forearm at our North Palm Beach clinic: carpal tunnel, arthritis, tendon repairs, fractures and the weeks after hand surgery, with custom splints made right here in the clinic. She is also a certified lymphedema therapist, and the program brings surgical-grade precision to every stage, from post-operative tendon protocols to the grip, pinch and dexterity you need back.",
        "items": [
            ("Carpal Tunnel &amp; Nerve Conditions", "Conservative and post-surgical care for nerve compression, with activity modification that lasts."),
            ("Arthritis Management", "Joint protection strategies, adaptive techniques, and pain-relieving modalities for arthritic hands."),
            ("Tendon &amp; Fracture Rehabilitation", "Careful, protocol-driven recovery after tendon repair, fracture, and complex hand surgery."),
            ("Custom Splinting &amp; Orthotics", "Precision-fabricated splints made in-clinic to protect healing structures and restore function."),
            ("Post-Surgical Hand Recovery", "Coordinated care with area hand surgeons for seamless recovery from surgery to full function."),
        ],
    },
    "wellness": {
        # seo_title / seo_desc added 2026-10-16: the only service page without
        # them (GSC 28d: ~59 impr at 8.2-8.5, 0 clicks). No prices, memberships,
        # insurance or non-patient access claimed (SEO-KEYWORDS do-not-claim).
        "seo_title": "Wellness Gym & Post-Rehab Training | North Palm Beach",
        "seo_desc": "An on-site wellness gym in our North Palm Beach clinic: personal training, post-rehab exercise and senior balance work with a team that knows your history.",
        "title": "Wellness &amp; Gym",
        "kicker": "Recovery doesn't stop at discharge.",
        "lede": "The Palm Beaches' clinic where PT &amp; OT patients can transition into an exclusive on-site wellness program.",
        "intro": "Most clinics say goodbye at discharge. We built a wellness program so we don't have to. Graduates of our therapy programs — and community members who simply want expert-guided fitness — train in the same facility, with a team that knows their history, at a pace built around long-term health.",
        "items": [
            ("Personal Training", "One-on-one sessions designed around your goals, history, and any conditions we've treated together."),
            ("Post-Rehab Exercise", "The bridge between therapy and independence — structured programs that protect your progress."),
            ("Sports Performance", "Strength, mobility, and conditioning work for active adults and athletes of every level."),
            ("Group Fitness Classes", "Small, supportive classes that make consistency enjoyable."),
            ("Senior Functional Fitness", "Balance, strength, and mobility training focused on independence and fall prevention."),
            ("Lifestyle &amp; Injury Prevention", "Long-term management and movement coaching for lasting health."),
        ],
    },
}


# VERBATIM public Google reviews, matched to the service they describe. Pulled
# 2026-10-14 from the clinic's own Google Business Profile (Windsor.ai,
# google_my_business reviews). Same rules as the homepage quotes: real words only,
# trimmed with an ellipsis where marked, reviewer shown as first name + last
# initial (owner's standing call). NO Review/AggregateRating markup: self-serving
# review schema breaks Google's guidelines; visible text is the whole point.
# Why it exists: every competitor that outranks us in the map pack shows its
# Google rating or review quotes ON the service page (Synergy "5.0 from 734",
# Gold Coast's quoted reviews, CORA's widget); our service pages showed none.
# Excluded on purpose: reviews that mention "Burns Rd", "Rob", "Lonn" or "any of
# their locations". Those were written for a DIFFERENT clinic with a similar name
# (thefirstrehab.com, 3375 Burns Rd) and landed on our listing by mistake.
SERVICE_REVIEWS = {
    "hand-therapy": [
        ("Great hand therapy from Laura. Recovering well from a wrist injury with her help. I'm well on my way back to kayaking, pickleball, golf and more!", "Thom F."),
        ("Laura did a lot of treatments to help with my tennis elbow and gave me at home exercise. I'm feeling great!", "Charlie C."),
        ("My hand therapist Laura is THE Best!!!! And all the staff at front desk have been so welcoming.", "Mary C."),
    ],
    "occupational-therapy": [
        ("I also want to highlight Joan Janik, who guided me through a series of exercises tailored to help my shoulder grow stronger. Her attention to detail and encouragement made a real difference in my rehab journey.", "Romina G."),
        ("Dave and his staff of PT’s OT’s and assistants are the BEST! They have helped me through shoulder and hand and wrist injuries as well as lumbar and SI joint problems.", "Danielle J."),
        ("I have OT with Laura and she has been great! Staff is friendly and professional.", "Renee W."),
    ],
    "physical-therapy": [
        ("Their physical therapists were exceptionally knowledgeable, kind, and caring with their assistance after my hip replacement, and built my strength, stamina, and walking confidence back quickly.", "Christine H."),
        ("It’s more one on one than other PT places I’ve been. I’m a name not a number very personable.", "Patricia T."),
        ("We were never rushed through the appointments, nor did we feel like we were there for an excessive amount of time. Scheduling was very accommodating.", "Georgia N."),
    ],
}
GOOGLE_RATING, GOOGLE_REVIEW_COUNT = "4.9", 110   # update when the listing moves


def service_reviews_html(slug):
    rv = SERVICE_REVIEWS.get(slug)
    if not rv:
        return ""
    cards = "".join(
        f'''<figure class="quote-card reveal d{i+1}"><div class="stars" aria-hidden="true">★★★★★</div><blockquote>{q}</blockquote><figcaption><strong>{n}</strong> &middot; Google review</figcaption></figure>'''
        for i, (q, n) in enumerate(rv))
    return f'''
<section class="section on-cream">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">From Our Patients</span>
      <h2><a href="https://maps.google.com/?cid=3809434844265673488" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;">{GOOGLE_RATING} <span style="color:var(--coral-text);">★</span> on Google</a></h2>
      <p class="lede">From {GOOGLE_REVIEW_COUNT} patient reviews of our North Palm Beach clinic.</p>
    </div>
    <div class="quote-grid">{cards}</div>
    <p class="related-links reveal" style="text-align:center;margin-top:1.4rem;">Verbatim excerpts, shared as posted. Every recovery is different. <a href="https://maps.google.com/?cid=3809434844265673488" target="_blank" rel="noopener">Read all our reviews on Google</a></p>
  </div>
</section>'''


# Supplemental visual data for service pages
SERVICE_EXTRAS = {
    "physical-therapy": {
        "tagline": "Movement is medicine — and we prescribe it precisely.",
        "stats": [("35+", "Years treating the Palm Beaches"), ("1-on-1", "Every session, hands-on"), ("Same-day", "Home program from visit one")],
        "process": [
            ("Evaluate", "A movement-based assessment pinpoints the patterns driving your pain."),
            ("Treat", "Skilled manual therapy plus targeted exercise, personalized from day one."),
            ("Progress", "We advance your plan as you improve — and prove it with measurable gains."),
            ("Thrive", "Graduate stronger, with the tools to stay pain-free for good."),
        ],
    },
    "occupational-therapy": {
        "tagline": "Getting you back to the life you actually live.",
        "stats": [("Daily-life", "Focused on real activities"), ("Whole-person", "Body, hands & mind"), ("Return-to-work", "Programs that get results")],
        "process": [
            ("Understand", "We learn how your condition affects your real daily activities and goals."),
            ("Rebuild", "Task-specific therapy restores strength, coordination, and confidence."),
            ("Adapt", "Smart strategies and equipment make daily tasks safer and easier."),
            ("Independence", "You return to the routines and roles that matter most to you."),
        ],
    },
    "hand-therapy": {
        "tagline": "Surgical-grade precision for the body's most intricate tool.",
        "stats": [("CHT", "Certified Hand Therapist on staff"), ("In-clinic", "Custom splints fabricated on-site"), ("Surgeon", "Coordinated post-op protocols")],
        "process": [
            ("Assess", "A detailed evaluation of motion, strength, and the fine mechanics of your hand."),
            ("Protect", "Custom orthoses, molded in-clinic, guard healing structures at exactly the right angle."),
            ("Restore", "Graded motion and strengthening, timed precisely to tissue healing."),
            ("Refine", "Functional retraining for grip, pinch, and the dexterity your life requires."),
        ],
    },
    "wellness": {
        "tagline": "Because recovery shouldn't end at discharge.",
        "stats": [("On-site", "Gym inside the clinic"), ("Guided", "By a team that knows your history"), ("Every age", "From athletes to seniors")],
        "process": [
            ("Graduate", "Finish therapy — then keep the momentum instead of losing it."),
            ("Transition", "Move into a structured program built on your rehab history."),
            ("Strengthen", "Personal training, classes, and conditioning at your pace."),
            ("Sustain", "Long-term movement coaching that protects your progress for life."),
        ],
    },
}

def build_services():
    for slug, s in SERVICES.items():
        x = SERVICE_EXTRAS[slug]
        # Numbered feature cards with alternating gold accent
        items = "".join(
            f'''<div class="svc-feature reveal">
              <span class="svc-feature-num">{i+1:02d}</span>
              <div><h3>{t}</h3><p>{d}</p></div>
            </div>''' for i, (t, d) in enumerate(s["items"])
        )
        stats = "".join(
            f'<div class="svc-stat"><strong>{v}</strong><span>{l}</span></div>' for v, l in x["stats"]
        )
        process = "".join(
            f'''<div class="svc-step reveal d{i%4+1}">
              <div class="svc-step-dot">{i+1}</div>
              <h3>{t}</h3><p>{d}</p>
            </div>''' for i, (t, d) in enumerate(x["process"])
        )
        crumbs = f'<div class="crumbs"><a href="/">Home</a> / <a href="physical-therapy.html">Services</a> / {s["title"]}</div>'
        cht_callout = ""
        if slug == "hand-therapy":
            cht_callout = '''
<section class="section on-cream" style="padding-top:0;">
  <div class="wrap">
    <div class="cht-callout reveal">
      <span class="eyebrow">Why It Matters</span>
      <h3>Why a Certified Hand Therapist matters</h3>
      <p>The CHT credential requires thousands of hours of specialized upper-extremity practice and a rigorous
      national examination — it's one of the most demanding certifications in rehabilitation. It's also why
      area hand surgeons refer their post-operative patients specifically to certified hand therapists:
      after tendon repair or fracture, moving too soon risks the repair, and too late costs motion.
      A CHT walks that line precisely, in coordination with your surgeon.</p>
    </div>
  </div>
</section>'''
        # Condition-level depth, currently hand therapy only.
        #
        # Why this exists: the 2026-09-09 Search Console pull put
        # /services/hand-therapy.html at position 25.3, with "hand therapist"
        # (95 impr) at 28.7 and "hand therapy" at 73.7 — real demand, ranking
        # nowhere. Unlike the city-qualified location-page terms, these carry no
        # map pack, and the clinic has a defensible claim in Laura Drumm, CHT and
        # on-site splint fabrication. The page was 702 words against hand centres
        # and hospital systems, so the gap was depth on the page that has to rank.
        #
        # Every sentence below restates something the site already asserts (the
        # hand-therapy FAQ category, SERVICES, CONDITIONS). It does NOT copy the
        # Q&As — those stay on /faq.html and are cross-linked, per CLAUDE.md — and
        # it adds no new clinical claim. Do not add mechanisms, statistics or
        # outcomes here without owner sign-off, and never claim hand surgery: we
        # rehabilitate, surgeons operate.
        SVC_DEEP = {
            "hand-therapy": {
                "h2": "What we treat, and how",
                "intro": "Hand therapy is not general rehabilitation applied to a smaller limb. Dozens of "
                         "tendons, joints and nerves work in tight quarters, each on its own healing "
                         "timeline, which is why hand surgeons refer post-operative patients to certified "
                         "hand therapists specifically. Here is what that looks like condition by condition.",
                "blocks": [
                ("Carpal tunnel syndrome",
                 "Conservative care helps many people, particularly when symptoms are caught early. "
                 "Treatment can include a custom night splint that holds the wrist in a neutral position "
                 "while you sleep, nerve and tendon gliding exercises, and practical changes to the "
                 "activities and workstation setup that keep provoking symptoms. If your case turns out "
                 "to warrant a surgical consult, we will say so plainly and coordinate with your physician."),
                ("Arthritis of the hand and thumb",
                 "Hand therapy is one of the most effective conservative options for arthritic hands and "
                 "thumbs. Joint-protection technique, targeted strengthening, a custom supportive splint "
                 "and smart activity modification work together to reduce pain and protect the things "
                 "arthritis threatens to take first, from opening jars to gardening and golf."),
                ("Tendon injuries and repairs",
                 "Repaired tendons heal on a strict timeline, and the margin for error is small: move too "
                 "soon and you risk the repair, too late and you lose motion. We work from your surgeon\u2019s "
                 "protocol, fabricate any splint to it, and stage motion and strengthening to the tissue "
                 "rather than the calendar."),
                ("Hand and wrist fractures",
                 "Recovery continues well after the cast comes off, when stiffness, swelling and lost grip "
                 "are usually the real obstacles. Care is staged: protect what is still healing, restore "
                 "motion in a graded way, then rebuild the strength and dexterity the hand needs to go "
                 "back to work and ordinary life."),
                ("Trigger finger and nerve conditions",
                 "Both are treated within the program, conservatively where that is appropriate and "
                 "post-operatively where surgery has already happened. Splinting, graded motion and "
                 "activity modification are the usual tools."),
                ("The elbow and forearm, not just the hand",
                 "The arm works as one connected chain, so the program covers the full upper extremity \u2014 "
                 "hand, wrist, forearm and elbow. Tennis elbow, wrist fractures and nerve entrapments all "
                 "fall inside a certified hand therapist\u2019s scope."),
                ("Splints and orthoses, made here",
                 "Custom splints and orthoses are fabricated in our clinic rather than ordered in. Each one "
                 "is molded to your hand for your specific condition, adjusted as healing progresses, and built "
                 "to your surgeon\u2019s protocol when you are recovering from surgery. Call 561-624-4263 if you "
                 "want to know whether your plan covers one \u2014 our front desk will check before you come in."),
                ("Working with your surgeon",
                 "Post-operative timelines are set by your surgeon, and they vary widely: some repairs begin "
                 "protected motion within days, others need a period of immobilization first. We work from that "
                 "protocol and coordinate with their office directly, so send us your surgery details before or "
                 "just after the procedure and your plan \u2014 and any splint you need \u2014 will be ready on schedule."),
                # Added 2026-10-14 (GSC deep dive, item 3): the practitioner searches
                # ("hand therapist", "certified hand therapist near me", "hand
                # therapists near me") were splitting between this page and the West
                # Palm Beach location page, which ranked 50 to 80 for the near-me
                # forms. These blocks make this page say plainly who the hand
                # therapist is, where, and how to start. Facts restate the
                # hand-therapy FAQ category and TEAM; nothing new is claimed.
                ("Who your hand therapist is",
                 "Laura Drumm, MS, OTR/L, CHT, CLT leads our hand therapy program. The OTR/L means she is a "
                 "licensed occupational therapist. The CHT is the Certified Hand Therapist credential, which takes "
                 "thousands of hours of specialized upper-extremity practice and a rigorous national exam, and it is "
                 "the credential area hand surgeons look for when they refer a patient after surgery. The CLT means "
                 "she is also a certified lymphedema therapist."),
                ("Finding a hand therapist near North Palm Beach",
                 "We have one location, at 733 US Highway 1, Suite 2A in North Palm Beach, and patients come to it "
                 "for hand therapy from across Palm Beach County, including "
                 "<a href=\"../locations/palm-beach-gardens.html\">Palm Beach Gardens</a>, "
                 "<a href=\"../locations/jupiter.html\">Jupiter</a> and "
                 "<a href=\"../locations/west-palm-beach.html\">West Palm Beach</a>. Ours is one of the area's "
                 "few certified hand therapy programs. Hours are Monday to Friday, 8:00 AM to 5:30 PM, and Saturday, 8:00 AM to 12:30 PM."),
                ("Do I need a referral to see a hand therapist?",
                 "It depends on your plan. After hand surgery you will usually arrive with a referral and a protocol "
                 "from your surgeon already. If you are coming on your own for something like carpal tunnel or thumb "
                 "arthritis, call 561-624-4263 and our front desk will check whether your plan needs a referral and "
                 "help arrange one. Before your first visit they verify your Medicare or commercial benefits, "
                 "including how your plan handles a custom splint."),
                ],
                "extra": '''
      <div class="data-table" tabindex="0" role="region" aria-label="Who does what in hand care">
        <table>
          <caption>How hand care splits between a surgeon and the therapists at our clinic, as described on our hand therapy and occupational therapy pages.</caption>
          <thead><tr><th scope="col">Who</th><th scope="col">What they do for your hand</th></tr></thead>
          <tbody>
            <tr><th scope="row">Hand surgeon</th><td>Operates when surgery is needed and sets the post-operative protocol</td></tr>
            <tr><th scope="row">Certified hand therapist</th><td>Rehabilitates the hand, wrist, forearm and elbow, makes custom splints in the clinic, and stages motion to the surgeon's protocol</td></tr>
            <tr><th scope="row">Occupational therapist</th><td>Turns restored motion into daily use: dressing, cooking, work tasks and the tools you use</td></tr>
            <tr><th scope="row">Physical therapist</th><td>Works on movement, strength and pain elsewhere in the body when the injury reaches past the arm</td></tr>
          </tbody>
        </table>
      </div>
      ''',
            },
            # Added 2026-09-18. The Search Console pull for the 90 days to
            # 2026-09-15 found 751 impressions and ZERO clicks across 35
            # occupational-therapy queries, nearly all of them West Palm Beach
            # ("physical and occupational therapy west palm beach" 150 impr at
            # pos 32.9, "occupational therapy treatment west palm beach" 108 at
            # 33.5, "occupational therapist 33401" 72 at 35.4). The page sat at
            # position 36.0 on 834 words. The nearest competitor by name,
            # thefirstrehab.com, runs three Palm Beach County clinics staffed by
            # PTs and PTAs and offers no occupational therapy at all, so this is
            # demand in their own city that they cannot answer. The gap was depth.
            #
            # Same rules as the hand-therapy block above: every sentence restates
            # something the site already asserts (SERVICES, TEAM, the FAQ). No new
            # clinical claim, no mechanisms, no statistics, no outcomes without
            # owner sign-off. OT evaluates and treats; we do not diagnose.
            "occupational-therapy": {
                "h2": "What occupational therapy actually does",
                "intro": "Physical therapy asks how well you move. Occupational therapy asks what you need "
                         "to get done, then works backward from there \u2014 the shirt buttoned, the meal cooked, "
                         "the job performed, the shower taken safely and alone. Our program is led by a "
                         "founder who is himself an occupational therapist and has been treating patients "
                         "since 1991. Here is what the work looks like in practice.",
                "blocks": [
                ("Activities of daily living",
                 "Dressing, bathing, grooming, cooking and home management are the tasks independence "
                 "actually rests on, and they are the first things an injury, a stroke or a joint "
                 "replacement takes away. Therapy here is practical and specific: we work on the real task "
                 "you are struggling with, in the sequence you actually perform it, and adapt the method "
                 "until you can do it without help."),
                ("Recovery after stroke",
                 "Stroke recovery is task-specific work. Rather than exercising an arm in the abstract, we "
                 "rebuild the routines that arm is needed for, restoring upper-extremity function, "
                 "coordination and the daily sequences that make a morning possible. Progress is measured "
                 "in tasks regained, not repetitions completed."),
                ("Returning to a specific job",
                 "Return-to-work programs are built around what your job actually demands rather than a "
                 "general strength target. We use graded conditioning and task simulation so the work you "
                 "rehearse in the clinic resembles the work waiting for you, which is also what an employer, "
                 "an adjuster or a case manager needs to see documented before a release."),
                # Added 2026-10-14 from docs/PATIENT-INSIGHTS-2026-10.md: OT patients
                # stay longest and many are working age, so return-to-work is the
                # commercial angle. Restates SERVICES, CONDITIONS["workers-comp"]
                # and the FAQ; the Florida claim rules live on the workers-comp page.
                ("Hurt at work, or worried you will be",
                 "Many of the people our occupational therapists treat are working age, and the goal is "
                 "usually specific: back to the job, safely, without the injury coming back. That means the "
                 "hands, wrists, elbows and shoulders, repetitive strain, and the individual tasks a job is "
                 "built from. Treatment rehearses those tasks at the weights, heights and pace the job "
                 "actually uses, and progress is reported in the same terms. If the injury is covered by "
                 "workers' comp, our <a href=\"../treatments/workers-comp.html\">work injury rehab</a> page "
                 "explains how authorization and reporting work in Florida."),
                ("Ergonomics and adaptive equipment",
                 "Sometimes the fastest route back to a task is changing the task. Workstation assessment, "
                 "tool and equipment recommendations, and technique changes can make daily activities safer "
                 "and less painful without waiting on strength to return. At a desk that can mean the height "
                 "of the screen and the position of the chair, keyboard and mouse. On a job site it can mean "
                 "tool grips, how a load is lifted and carried, and how the work is staged through the day. "
                 "The same thinking applies at home, from the kitchen to the garden. Call 561-624-4263 and "
                 "our front desk can tell you whether an assessment is covered under your plan."),
                ("Hand and upper-extremity function",
                 "Fine-motor and functional-use training runs alongside our certified hand therapy program, "
                 "so a patient whose hand is the limiting factor gets both: the protocol-driven hand work "
                 "from Laura Drumm, CHT, our <a href=\"hand-therapy.html\">certified hand therapist</a>, and the daily-function retraining that turns restored motion into "
                 "a usable hand. Few clinics in the county can put both in the same building."),
                ("Cognitive rehabilitation",
                 "Memory, attention, sequencing and problem-solving are as much a part of safe independent "
                 "living as strength is. Where they have been affected, therapy targets the strategies that "
                 "let someone manage medication, follow a recipe or handle a household routine again."),
                ("Occupational therapy or physical therapy?",
                 "They overlap and they are frequently prescribed together, which is why we run both under "
                 "one roof rather than referring out. The short version: physical therapy generally targets "
                 "movement, strength and pain, while occupational therapy targets the activities that "
                 "movement is for. If you are not sure which you need, our front desk can talk it through, "
                 "and your evaluation will settle it."),
                ],
            },
            # Wellness: balance and fall prevention. Added 2026-10-14 from
            # docs/PATIENT-INSIGHTS-2026-10.md (median patient age about 71, two
            # thirds 65+). Restates SERVICES["wellness"], the wellness FAQ, the
            # strength-after-60 post (Dave's quote is verbatim from it) and the
            # insurance page. Do NOT add prices, memberships, schedules or
            # non-patient access: all four are on the owner-confirmation list.
            "wellness": {
                "h2": "Balance and fall prevention, and where the gym fits",
                "intro": "Falls rarely start with a slip. They start months earlier, with weaker hips, a less "
                         "steady base and reaction time that has quietly slowed. Senior functional fitness in "
                         "our on-site gym works on both halves at once: the strength that holds you up and the "
                         "balance that catches you when something shifts. Here is how it fits with therapy.",
                "blocks": [
                ("Who is the balance work for?",
                 "Mostly people who have noticed the early signs: standing up from a chair more slowly, "
                 "holding the rail on the stairs, avoiding a walk they used to enjoy. Many have just finished "
                 "physical or occupational therapy with us and want to keep what they gained. The program "
                 "covers every age, from athletes to seniors, but balance and fall prevention are the heart "
                 "of senior functional fitness."),
                ("Therapy or the gym: which comes first?",
                 "If pain, a recent fall, dizziness or a new diagnosis is part of the picture, start with an "
                 "evaluation. Balance and fall prevention, vestibular work and neurological rehab are part of "
                 "our <a href=\"physical-therapy.html\">physical therapy</a> program, and medically necessary "
                 "therapy is covered by Medicare. When skilled therapy is no longer what you need, the gym is "
                 "how you keep the progress, with a team that already knows your chart."),
                ("What does a session look like?",
                 "Supervised strength and balance work, built around your history rather than a generic class "
                 "plan. Sit to stands are a good example: rising from a chair without using your hands is one "
                 "of the simplest tests of leg strength there is, and it is the same movement that keeps you "
                 "able to get off a low couch, a car seat or the toilet without help. You can train "
                 "one-on-one with a personal trainer or in a small group class, whichever keeps you coming back."),
                ("Can I keep doing it at home?",
                 "Yes, and you should. Dr. Dave Kashuba, Ph.D., OTR, asks patients for &ldquo;just a little bit "
                 "of exercises, ten, fifteen minutes a day, three minutes a day, and work your way up,&rdquo; "
                 "spread through the day rather than saved for one long session. Our "
                 "<a href=\"../exercises.html\">home exercises page</a> has his knee, hip and shoulder sets with "
                 "sets and reps, and <a href=\"../blog/strength-training-after-60-fall-prevention.html\">Strength "
                 "Training After 60</a> explains the thinking."),
                ("Does insurance cover the gym?",
                 "No. The wellness program does not take insurance, so the front desk explains how it works and "
                 "what it costs before you sign up. Therapy is different: it is covered by Medicare when it is "
                 "medically necessary, including skilled care that helps you maintain your function. Our "
                 "<a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> has the details."),
                ("Do I have to be a patient?",
                 "The program is designed first as a continuation for our therapy patients, so the person "
                 "guiding your training already knows your history. If you have not been a patient with us, "
                 "call 561-624-4263 and the front desk will walk you through the options."),
                ],
            },
        }
        svc_deep_html = ""
        if slug in SVC_DEEP:
            _d = SVC_DEEP[slug]
            _blocks = "".join(
                f"<h3>{t}</h3>\n      <p>{d}</p>\n      " for t, d in _d["blocks"]
            )
            svc_deep_html = f'''
<section class="section">
  <div class="wrap">
    <div class="prose reveal">
      <h2>{_d["h2"]}</h2>
      <p>{_d["intro"]}</p>
      {_blocks}{_d.get("extra", "")}</div>
  </div>
</section>'''

        # Conditions treated with this service — internal links for SEO + discovery
        svc_conds = {
            "physical-therapy": ["back-pain", "neck-pain", "shoulder-pain", "knee-pain", "hip-pain", "foot-pain", "ankle-pain", "headache-relief", "post-surgical", "auto-accident"],
            "occupational-therapy": ["hand-wrist", "post-surgical", "workers-comp"],
            "hand-therapy": ["hand-wrist", "post-surgical"],
        }
        # Descriptive anchors (2026-10-16): the brochure names ("Foot Pain Relief",
        # "Hand & Wrist Therapy") told search engines nothing about what each page
        # treats, and foot/ankle had no contextual inbound link at all. Anchors
        # match each page's title-tag keyword; names and H1s are unchanged.
        COND_ANCHOR = {
            "back-pain": "Low back pain and sciatica treatment",
            "neck-pain": "Neck pain treatment",
            "shoulder-pain": "Shoulder pain treatment",
            "knee-pain": "Knee pain treatment",
            "hip-pain": "Hip pain treatment",
            "foot-pain": "Foot pain and plantar fasciitis treatment",
            "ankle-pain": "Ankle sprain and ankle pain treatment",
            "headache-relief": "Chronic headache treatment",
            "post-surgical": "Post-surgical physical therapy",
            "auto-accident": "Car accident rehab",
            "workers-comp": "Work injury rehab",
            "hand-wrist": "Hand, wrist and carpal tunnel treatment",
        }
        svc_cond_links = ""
        if slug in svc_conds:
            links = " &middot; ".join(
                f'<a href="../treatments/{c}.html">{COND_ANCHOR.get(c, CONDITIONS[c]["name"])}</a>' for c in svc_conds[slug]
            )
            svc_cond_links = f'<p class="related-links reveal"><strong>Conditions we treat with {s["title"].lower()}:</strong> {links}</p>'

        # Service page -> the blog posts that explain it. Same reasoning as
        # COND_BLOG on the condition pages: without these, posts like the
        # PT-vs-OT explainer had one inbound link in the whole site.
        SVC_BLOG = {
            "physical-therapy": ["physical-therapy-vs-occupational-therapy", "what-to-expect-first-pt-visit"],
            "occupational-therapy": ["physical-therapy-vs-occupational-therapy", "why-hand-therapy-is-different"],
            "hand-therapy": ["why-hand-therapy-is-different"],
            "wellness": ["personal-training-with-a-therapist-who-knows-your-injury-history", "strength-training-after-60-fall-prevention", "gym-program-after-physical-therapy-north-palm-beach"],
        }
        _sposts = [b for b in SVC_BLOG.get(slug, []) if b in BLOG_POSTS]
        svc_blog_links = ""
        if _sposts:
            _slinks = " &middot; ".join(
                f'<a href="../blog/{b}.html">{BLOG_POSTS[b]["title"]}</a>' for b in _sposts)
            svc_blog_links = f'<p class="related-links reveal"><strong>From the blog:</strong> {_slinks}</p>'

        # Cross-link to this service's category on the filterable FAQ page
        faq_cat = {"physical-therapy": "physical-therapy", "occupational-therapy": "occupational-therapy",
                   "hand-therapy": "hand-therapy", "wellness": "wellness-gym"}[slug]
        cat_n = len(dict((c[0], c[2]) for c in FAQ_CATEGORIES)[faq_cat])
        svc_schema = ""
        svc_faq_html = f'''
<section class="section on-cream svc-faq">
  <div class="wrap center reveal" style="text-align:center;">
    <span class="eyebrow" style="justify-content:center;">Common Questions</span>
    <h2 style="margin-bottom:1rem;">Questions about {s["title"]}?</h2>
    <p class="lede" style="margin:0 auto 1.8rem;">We keep {cat_n} straight answers — referrals, insurance, what to expect, and more — on our FAQ page.</p>
    <a class="btn btn-ink" href="../faq.html#{faq_cat}">See all {s["title"]} FAQs <span class="arr">&rarr;</span></a>
  </div>
</section>'''
        # One visible line on each THERAPY service page (2026-10-14, from
        # docs/PATIENT-INSIGHTS-2026-10.md: two thirds of patients are 65+ and
        # about half are Medicare, so benefit clarity is the conversion lever).
        # Every claim in it is already made in the FAQ ("Will you verify my
        # insurance benefits before I start? Yes, always") and on /insurance.html.
        # Medigap is deliberately NOT named as verified before the visit: the
        # site only says "bring every card and we will sort out which pays
        # first"; Nick confirmed 2026-10-14 the front desk does not verify
        # Medigap, so it stays out. Wellness is excluded because it does not
        # take insurance (Nick, 2026-10-14).
        # The wellness program does NOT take insurance (Nick, 2026-10-14), so the
        # wellness page gets its own first-visit copy, side note and form line
        # instead of the shared "we accept most major insurance" wording.
        if slug == "wellness":
            first_visit_p = ('<p>Your first session starts with a conversation about your goals and, if you have '
                             'done therapy with us, a look at your rehab history so the program picks up where '
                             'treatment left off. The wellness program does not take insurance; the front desk '
                             'explains the options and pricing before you sign up.</p>')
            side_note = "The wellness program does not take insurance."
            form_sub = "Tell us what you are looking for and our front desk will call you back within one business day to walk you through the options."
        else:
            first_visit_p = ('<p>Your first appointment includes a comprehensive movement-based evaluation, an honest '
                             'conversation about your goals, and a proposed plan of care — with hands-on treatment '
                             'starting that very first day whenever appropriate. We accept most major insurance '
                             'plans, including Medicare, and our front desk will gladly verify your coverage before '
                             'you arrive.</p>')
            side_note = "Most major insurance accepted, including Medicare."
            form_sub = "Tell us what you need and our front desk will call you back within one business day. We will check your insurance before your first visit."
        verify_line = ""
        if slug != "wellness":
            verify_line = ('<p class="fv-highlight"><strong>Before your first visit, our front desk verifies your '
                           'Medicare or commercial insurance benefits</strong> and tells you what your plan covers, '
                           'any copay or deductible, and whether a referral is needed. On Medicare? Our '
                           '<a href="../insurance.html#medicare-guide">2026 Medicare guide</a> explains the '
                           'deductible, the 20% coinsurance and how a Medigap plan fits in.</p>')
        body = f"""
<main>
{page_hero("Our Services", f'{s["title"]} in <em class="accent">North Palm Beach</em>', s["lede"], crumbs)}

<div class="ins-strip"><div class="ticker">{"".join(f"<span>{v} &mdash; {l}</span>" for v, l in x["stats"])}</div></div>

<section class="section">
  <div class="wrap">
    <div class="split" style="margin-bottom:clamp(3rem,6vw,5rem);">
      <div class="reveal">
        <span class="eyebrow">{s["title"]}</span>
        <h2 style="margin-bottom:1rem;"><em class="accent">{x["tagline"]}</em></h2>
        <p style="font-size:1.08rem;">{s["intro"]}</p>
        <div class="svc-stats">{stats}</div>
        <div class="mt-2"><a class="btn btn-coral" href="../contact.html">Book an Evaluation <span class="arr">&rarr;</span></a></div>
      </div>
      {service_media(slug)}
    </div>
  </div>
</section>

<section class="section on-cream">
  <span class="sec-mark" aria-hidden="true" style="top:2rem;right:3vw;">{['I','II','III','IV'][list(SERVICES).index(slug)]}</span>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">What's Included</span>
      <h2>Every Angle of <em class="accent">{s["title"]}</em></h2>
    </div>
    <div class="svc-feature-grid">{items}</div>
    {svc_cond_links}
    {svc_blog_links}
  </div>
</section>
{cht_callout}{svc_deep_html}{service_reviews_html(slug)}
<section class="section on-ink">
  <div class="beam-field" aria-hidden="true"><div class="beam" style="opacity:0.5;"></div></div>
  <div class="wrap" style="position:relative;z-index:1;">
    <div class="section-head reveal">
      <span class="eyebrow">How It Works</span>
      <h2>Your Path Through <em class="accent">{s["title"]}</em></h2>
      <p class="lede">A clear, four-step journey — you'll always know what phase you're in and what comes next.</p>
    </div>
    <div class="svc-process">{process}</div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <h2>What to expect at your first visit</h2>
      {first_visit_p}
      {verify_line}
      <p>You're never a chart number here. Since 1991, our family-owned clinic has treated every patient with the individual attention that earns a 4.9&#9733; reputation across the Palm Beaches.</p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Begin with an evaluation</h3>
      <p>The first step is simple: a conversation and a movement assessment. We'll build the plan together.</p>
      <a class="btn btn-coral" href="../contact.html">Book Appointment</a>
      <div class="side-meta">
        <p>Prefer to call?<br><a href="tel:+15616244263">{PHONE}</a></p>
        <p style="margin-top:0.8rem;">{side_note}</p>
      </div>
    </aside>
  </div>
</section>
{svc_faq_html}
{appt_form(heading='Start ' + s['title'], sub=form_sub)}
{cta_band(1)}
</main>
"""
        svc_desc = s["lede"].replace("&amp;", "&")
        if len(svc_desc) <= 115:
            svc_desc += " Family-owned North Palm Beach clinic since 1991."
        svc_bc = breadcrumb_schema([("Home", ""), ("Services", "services/physical-therapy.html"),
                                    (s["title"], f"services/{slug}.html")]) + therapy_schema(slug, s["title"], s["lede"])
        write(f"services/{slug}.html",
              head(s.get("seo_title") or f'{s["title"].replace("&amp;","&")} | First Rehabilitation of North Palm Beach',
                   s.get("seo_desc") or svc_desc, depth=1, canonical=f"services/{slug}.html",
                   extra_schema=svc_schema + svc_bc)
              + nav(1) + body + footer(1))

# ----------------------------------------------------------------------------
# CONDITION PAGES
# ----------------------------------------------------------------------------

CONDITIONS = {
    "back-pain": {
        # Title/desc changed 2026-10-14 (GSC deep dive): six North Palm Beach back
        # pain queries, 191 impressions at average position 6.5, zero clicks in 90
        # days. Sciatica
        # and stenosis are named because people search them. Recorded in
        # SEO-KEYWORDS.md; judge on CTR at the same position.
        "seo_title": "Low Back Pain & Sciatica Treatment | North Palm Beach",
        "seo_desc": "One-on-one physical therapy for low back pain, sciatica, disc problems and spinal stenosis in North Palm Beach. Family-owned since 1991. Call 561-624-4263.",
        "name": "Back Pain Relief",
        "area": "Lower Back &amp; Spine",
        "lede": "Evidence-based physical therapy for low back pain, sciatica, and spinal conditions — treating the cause, not just the symptoms.",
        "answer": "Low back pain, sciatica and spinal stenosis are among the most treatable problems we see. One-on-one physical therapy at our North Palm Beach clinic combines hands-on work to restore mobility, core and hip strengthening to support the spine, and changes to the daily movements that keep provoking pain. In most cases Florida law lets you start with an evaluation, no referral needed.",
        "intro": "Back pain is the single most common reason people seek physical therapy, and one of the most treatable. Our approach starts with understanding <em>why</em> your back hurts — the movement patterns, postural habits, and strength deficits behind the pain — then resolving them with skilled manual therapy and progressive exercise.",
        "treats": ["Low back pain and stiffness", "Sciatica and radiating leg pain", "Herniated and bulging discs", "Degenerative disc disease", "Spinal stenosis", "Post-surgical spine recovery", "Muscle strains and spasms"],
        "approach": "Treatment typically blends hands-on manual therapy to restore mobility, targeted core and hip strengthening to support the spine, and movement retraining so daily activities stop provoking pain. You'll leave every visit with a clear home program and an honest picture of your progress.",
    },
    "neck-pain": {
        # Title/desc changed 2026-10-14 (GSC deep dive): 13 North Palm Beach neck
        # queries ("stiff neck", "pinched nerve in neck", "neck and shoulder pain")
        # drew 593 impressions across our pages at average position 8.2 (337 of
        # them on this page, at 10.1) and zero clicks in 90 days. The title now names the two symptoms people type. Recorded in
        # SEO-KEYWORDS.md; judge on CTR at the same position.
        "seo_title": "Neck Pain & Pinched Nerve Treatment in North Palm Beach",
        "seo_desc": "Physical therapy for a stiff neck, a pinched nerve, and neck and shoulder pain in North Palm Beach. One-on-one care, Medicare accepted. Call 561-624-4263.",
        "name": "Neck Pain Relief",
        "area": "Head &amp; Neck",
        "lede": "Manual therapy, posture correction, and strengthening for neck pain, stiffness, and whiplash.",
        "answer": "Most neck pain, including a stiff neck, a pinched nerve and pain that spreads into the shoulder, is treated well with one-on-one physical therapy: hands-on work to free the stiff joints, strengthening for the deep neck muscles, and changes to how you sit, sleep and work. At our North Palm Beach clinic that treatment usually starts at your first visit.",
        "intro": "Whether it crept in from years at a desk or arrived overnight after an accident, neck pain responds remarkably well to skilled physical therapy. We identify the joints, muscles, and postural patterns driving your symptoms and treat them directly.",
        "treats": ["Chronic neck pain and stiffness", "Whiplash-associated disorders", "Cervical radiculopathy (pinched nerve)", "Tension and postural neck pain", "Degenerative changes of the cervical spine", "Pain radiating to the shoulder or arm"],
        "approach": "Care usually combines gentle manual therapy and joint mobilization, deep neck flexor and postural strengthening, and workstation or sleep-position coaching. Most patients notice meaningful change within the first few weeks of consistent care.",
    },
    "shoulder-pain": {
        "seo_title": "Shoulder Pain Treatment North Palm Beach | First Rehab",
        "seo_desc": "Rotator cuff tears, frozen shoulder, impingement and post-surgical shoulder rehab, treated hands-on by a small family-owned team. Call 561-624-4263.",
        "name": "Shoulder Pain Relief",
        "area": "Shoulder",
        "lede": "Specialized rehabilitation for rotator cuff injuries, frozen shoulder, and everything in between.",
        "answer": "Most shoulder pain, from a rotator cuff strain to frozen shoulder or the weeks after surgery, is treated with one-on-one physical therapy: restore pain-free range first, rebuild rotator cuff and shoulder blade strength next, then get back to reaching, lifting, sport and sleep. At our North Palm Beach clinic that treatment usually starts at your first visit.",
        "intro": "The shoulder trades stability for mobility — which is why it's so useful and so vulnerable. Our therapists restore the balance of strength and motion your shoulder depends on, whether you're recovering from surgery or trying to avoid it.",
        "treats": ["Rotator cuff strains and repairs", "Frozen shoulder (adhesive capsulitis)", "Shoulder impingement", "Bursitis and tendinitis", "Labral injuries", "Post-surgical shoulder rehabilitation", "Shoulder instability"],
        "approach": "We progress you deliberately: restoring pain-free range first, then rebuilding rotator cuff and scapular strength, then returning you to overhead reaching, lifting, sport, and sleep without guarding. Post-surgical patients follow protocols coordinated with their surgeon.",
    },
    "knee-pain": {
        # seo_title / seo_desc / answer added 2026-10-14 (depth pass on striking-distance
        # condition pages; see docs/GSC-DEEP-DIVE-2026-10.md and SEO-KEYWORDS.md).
        "seo_title": "Knee Pain Treatment in North Palm Beach | First Rehab",
        "seo_desc": "Knee arthritis, meniscus and ACL injuries, runner's knee and knee replacement rehab. One-on-one assessment and therapy in North Palm Beach. Call 561-624-4263.",
        "answer": "Most knee pain, from arthritis, meniscus and ligament injuries and runner's knee to the months after a knee replacement, is treated with one-on-one physical therapy: hands-on work for a stiff joint, strength for the quadriceps, hips and glutes that carry the knee, and practice on stairs and walks. At our North Palm Beach clinic that treatment usually starts at your first visit.",
        "name": "Knee Pain Relief",
        "area": "Knee",
        "lede": "From arthritis to ACL recovery — rebuild strong, confident knees.",
        "intro": "Knees take the load of everything you do, and knee pain usually reflects how the whole leg is working — hips, ankles, and movement habits included. That's how we treat it: the joint, and the mechanics around it.",
        "treats": ["Knee osteoarthritis", "Total and partial knee replacement rehab", "ACL, MCL, and meniscus injuries", "Patellofemoral pain (runner's knee)", "Tendinitis and bursitis", "Post-surgical knee recovery"],
        "approach": "Expect progressive strengthening of the quadriceps, hips, and glutes, manual therapy for joint mobility, and functional retraining for stairs, walking distance, and return to activity. Joint replacement patients follow a structured pathway from first bend to full stride.",
    },
    "hip-pain": {
        # seo_title / seo_desc / answer added 2026-10-14 (depth pass on striking-distance
        # condition pages; see docs/GSC-DEEP-DIVE-2026-10.md and SEO-KEYWORDS.md).
        "seo_title": "Hip Pain & Labral Tear Treatment | North Palm Beach",
        "seo_desc": "Physical therapy for hip pain, bursitis, labral tears, arthritis and hip replacement rehab in North Palm Beach, near West Palm Beach. Call 561-624-4263.",
        "answer": "Most hip pain, from bursitis on the outside of the hip to a labral tear, arthritis or the weeks after a hip replacement, is treated with one-on-one physical therapy: restore hip motion, strengthen the glutes and deep stabilizers, and retrain the way you walk. Hip pain often passes for back pain, so the evaluation at our North Palm Beach clinic checks both.",
        "name": "Hip Pain Relief",
        "area": "Hip &amp; Pelvis",
        "lede": "Restore pain-free walking, standing, and living with targeted hip rehabilitation.",
        "intro": "Hip pain can masquerade as back pain, groin pain, or thigh pain — and vice versa. Our evaluation sorts out the true source, then treats it with the strength and mobility work the hip responds to best.",
        "treats": ["Hip osteoarthritis", "Total hip replacement rehabilitation", "Bursitis and tendinopathy", "Labral irritation and tears", "Groin and hip flexor strains", "Gait and balance dysfunction"],
        "approach": "Care centers on restoring hip mobility, strengthening the glutes and deep stabilizers, and retraining walking mechanics. For hip replacement patients, we manage precautions early and build steadily toward confident, unassisted movement.",
    },
    "foot-pain": {
        # seo_title / seo_desc added 2026-10-16: the generated title said "Relief"
        # (SEO-KEYWORDS rule 1) and the generated desc carried an em dash. Both
        # strings restate the "treats" list below; no new claim. Recorded in
        # SEO-KEYWORDS.md under "Title changes, 2026-10-16".
        "seo_title": "Foot Pain & Plantar Fasciitis Treatment | North Palm Beach",
        "seo_desc": "Physical therapy for plantar fasciitis, heel and arch pain, foot tendinitis and recovery after a fracture or foot surgery in North Palm Beach. 561-624-4263.",
        "name": "Foot Pain Relief",
        "area": "Foot",
        "lede": "Get back on your feet — literally — with expert care for plantar fasciitis and foot pain.",
        "intro": "Foot pain changes everything downstream: how you walk, stand, exercise, and sleep. Our therapists treat the foot directly while correcting the loading patterns that caused the problem in the first place.",
        "treats": ["Plantar fasciitis and heel pain", "Foot and arch pain", "Post-fracture rehabilitation", "Tendinitis of the foot", "Balance and gait dysfunction", "Post-surgical foot recovery"],
        "approach": "Treatment blends manual therapy and targeted stretching, intrinsic foot and calf strengthening, footwear guidance, and graded return to walking and activity — so relief holds up under real life, not just in the clinic.",
    },
    "ankle-pain": {
        # seo_title / seo_desc added 2026-10-16 (rule 1: "treatment", not "relief").
        # Restates the "treats" list below. See SEO-KEYWORDS.md.
        "seo_title": "Ankle Sprain & Ankle Pain Treatment | North Palm Beach",
        "seo_desc": "Rehab for ankle sprains, chronic instability, Achilles tendinitis and repairs, and stiffness after a fracture, one-on-one in North Palm Beach. 561-624-4263.",
        "name": "Ankle Pain Relief",
        "area": "Ankle",
        "lede": "Rebuild stability and strength after sprains, fractures, and chronic ankle problems.",
        "intro": "An undertreated ankle sprain is the most common reason ankles keep getting injured. We rehabilitate ankles completely — restoring not just motion and strength, but the balance and reaction time that prevent the next injury.",
        "treats": ["Acute and chronic ankle sprains", "Chronic ankle instability", "Achilles tendinitis and repair rehab", "Post-fracture rehabilitation", "Stiffness and loss of motion", "Balance deficits after injury"],
        "approach": "Expect early swelling and mobility management, progressive strengthening and balance training, and sport- or activity-specific work before you return to full speed. Our goal is an ankle you never have to think about.",
    },
    "hand-wrist": {
        # Retitled 2026-10-16 (GSC 28d: "wrist pain treatment west palm beach" 51
        # impr at 17.2, "hand pain treatment west palm beach" split three ways
        # across our pages, 0 clicks). This page owns SYMPTOM and condition
        # intent (hand/wrist pain, carpal tunnel, trigger finger); the service
        # page keeps practitioner intent ("certified hand therapist").
        "seo_title": "Hand, Wrist & Carpal Tunnel Treatment | North Palm Beach",
        "seo_desc": "Hand and wrist pain, numbness and lost grip treated by a certified hand therapist: carpal tunnel, trigger finger, thumb arthritis, fractures. Splints made here.",
        "name": "Hand &amp; Wrist Therapy",
        "area": "Wrist &amp; Hand",
        "lede": "Certified hand therapy for the intricate mechanics of your hands and wrists.",
        "intro": "Few areas of the body demand more specialized rehabilitation than the hand. Our certified hand therapy program — led by Laura Drumm, CHT — provides precise, protocol-driven care for conditions and surgeries of the hand, wrist, and forearm, including custom splinting fabricated in-clinic. Patients travel to us from across the county for this specialty, including <a href=\"../locations/west-palm-beach.html\">West Palm Beach</a> and <a href=\"../locations/palm-beach.html\">Palm Beach</a>.",
        "treats": ["Carpal tunnel syndrome", "Wrist fractures and sprains", "Tendon injuries and repairs", "Trigger finger", "Arthritis of the hand and thumb", "Post-surgical hand rehabilitation"],
        "approach": "Care is exacting by design: custom orthoses to protect healing structures, graded motion and strengthening timed to tissue healing, and functional retraining for grip, pinch, and dexterity. We coordinate closely with area hand surgeons throughout recovery. Splints are fabricated here in the clinic rather than ordered in, molded to your hand and adjusted as healing progresses \u2014 and built to your surgeon\u2019s protocol when you are recovering from an operation. For carpal tunnel and thumb arthritis caught early, conservative care is often enough: night splinting, nerve and tendon gliding, joint protection technique, and practical changes to the activities that keep provoking symptoms. After a repair or a fracture, the timeline belongs to the tissue rather than the calendar, so motion is staged deliberately \u2014 too soon risks the repair, too late costs motion. If a case warrants a surgical consult we say so plainly and coordinate with your physician. Our <a href=\"../services/hand-therapy.html\">certified hand therapist</a> page has the full condition-by-condition detail.",
    },
    "headache-relief": {
        # seo_title / seo_desc / answer added 2026-10-14 (depth pass on striking-distance
        # condition pages; see docs/GSC-DEEP-DIVE-2026-10.md and SEO-KEYWORDS.md).
        "seo_title": "Chronic Headache Treatment in North Palm Beach | First Rehab",
        "seo_desc": "Physical therapy for headaches that start in the neck: tension-type, cervicogenic and whiplash headaches, treated one-on-one in North Palm Beach. 561-624-4263.",
        "answer": "Headaches that start in the neck, including tension-type and cervicogenic headaches and headaches after whiplash or a concussion, are treated well with one-on-one physical therapy. Treatment frees the stiff joints and tight muscles at the top of the neck, then works on the posture and strength that let the tension rebuild. At our North Palm Beach clinic that care usually starts at your first visit.",
        "name": "Headache Relief",
        "area": "Head &amp; Neck",
        "lede": "Physical therapy for cervicogenic headaches and tension-type headaches that start in the neck.",
        "intro": "Many chronic headaches don't start in the head at all — they start in the neck. When joint stiffness, muscle tension, and posture are the drivers, physical therapy can reduce headache frequency and intensity dramatically.",
        "treats": ["Cervicogenic headaches", "Tension-type headaches", "Headaches after whiplash or concussion", "Neck-related migraine triggers", "Jaw and postural contributions to head pain"],
        "approach": "We treat the upper cervical joints and surrounding muscles with skilled manual therapy, then address the postural and strength deficits that let tension rebuild. Most patients also receive simple daily strategies that make a measurable difference between visits.",
    },
    "post-surgical": {
        # seo_title / seo_desc added 2026-10-16. Semrush top 10 for "post surgical
        # physical therapy" is PT-clinic condition pages titled that way; the
        # generated title said only "Post-Surgical Rehab". Desc restates "treats".
        "seo_title": "Post-Surgical Physical Therapy & Rehab | North Palm Beach",
        "seo_desc": "Physical therapy after knee or hip replacement, rotator cuff repair, or spine, hand and foot surgery, following your surgeon's protocol in North Palm Beach.",
        "name": "Post-Surgical Rehabilitation",
        "area": "Full Body",
        "lede": "Structured, surgeon-coordinated recovery from joint replacement, spine surgery, and beyond.",
        "intro": "Surgery is the beginning of recovery, not the end. Our post-surgical programs translate your surgeon's protocol into week-by-week progress — protecting what was repaired while steadily rebuilding the strength and confidence surgery was meant to restore.",
        "treats": ["Total knee and hip replacement", "Shoulder and rotator cuff repair", "Spinal surgery recovery", "Hand and wrist surgery", "Foot and ankle surgery", "Fracture fixation recovery"],
        "approach": "We follow your surgeon's protocol precisely, communicate progress clearly, and adjust based on how your tissue is actually healing. From first post-op visit through final clearance, you'll always know what phase you're in and what milestone comes next.",
    },
    "workers-comp": {
        # Title/desc added 2026-10-14 (GSC deep dive). The generated title ran to
        # 67 characters and the description carried an em dash. "work injury
        # rehab" (pos 15.2) and "work injury rehabilitation" (pos 30.4) are the
        # phrases people use, so they lead. Recorded in SEO-KEYWORDS.md.
        "seo_title": "Work Injury Rehab & Workers' Comp Therapy | North Palm Beach",
        "seo_desc": "Workers' comp physical and occupational therapy in North Palm Beach: return-to-work training, ergonomics and objective reports for your adjuster. 561-624-4263.",
        "name": "Workers' Compensation Rehab",
        "area": "Work Injury",
        "lede": "Get better and get back to work — with the documentation and communication your case requires.",
        "answer": "If you were hurt at work, therapy here is built around getting you back to your actual job. Physical and occupational therapy run under one roof, treatment rehearses the tasks your job demands, and your adjuster, case manager and physician get objective progress reports. Call 561-624-4263 with your claim number and our front desk will check the authorization before your first visit.",
        "intro": "A work injury involves more than healing: it involves adjusters, case managers, physicians, and return-to-work timelines. We've handled workers' compensation cases for decades, providing excellent clinical care alongside the clear, timely documentation every party needs.",
        "treats": ["Lifting and overexertion injuries", "Repetitive strain injuries", "Back and shoulder work injuries", "Hand and upper extremity injuries", "Slip, trip, and fall injuries", "Post-surgical work injury recovery"],
        "approach": "Treatment is functional from day one — built around the physical demands of your actual job. We provide objective progress reporting, coordinate with your physician and case manager, and prepare you for a safe, sustainable return to work.",
    },
    "auto-accident": {
        # Title/desc changed 2026-10-14 (GSC deep dive): "car accident rehab" sits
        # at 18.2 and "auto injury rehabilitation" at 24.7 on this page. "PIP" is
        # what Florida patients and adjusters call the coverage. Recorded in
        # SEO-KEYWORDS.md.
        "seo_title": "Car Accident Rehab & PIP Physical Therapy | North Palm Beach",
        "seo_desc": "Physical therapy after a car accident in North Palm Beach: Florida's 14-day PIP rule, whiplash and back care, and records for your adjuster. 561-624-4263.",
        "name": "Auto Accident Recovery",
        "area": "Full Body",
        "lede": "Comprehensive rehabilitation after a car accident — from whiplash to complex multi-area injuries.",
        "answer": "After a car accident in Florida, see a physician within 14 days: your personal injury protection (PIP) pays for medical care only if initial care starts within 14 days of the crash, and physical therapy is follow-up care your physician refers you to. Once you have that referral, we treat whiplash, back pain and the rest, and document your recovery for your adjuster.",
        "intro": "Even a minor collision can leave lasting pain, and symptoms often surface days after the accident. Early, skilled rehabilitation is the best predictor of full recovery — and we make the process straightforward, including the documentation your claim requires.",
        "treats": ["Whiplash and neck injuries", "Back and spine injuries", "Shoulder and knee trauma", "Headaches after collision", "Soft tissue strains and sprains", "Anxiety about returning to movement"],
        "approach": "Care begins gently — calming irritated tissue and restoring basic motion — then progresses to strengthening and full return to daily activity. We document objectively throughout, and communicate with your physician and representatives as needed.",
    },
}

def build_conditions():
    cards = "".join(
        f'<a class="cond-card reveal" href="/treatments/{slug}.html"><span class="cond-tag">{c["area"]}</span><h3>{c["name"]}</h3><p>{c["lede"]}</p></a>'
        for slug, c in CONDITIONS.items()
    )
    crumbs = '<div class="crumbs"><a href="/">Home</a> / What We Treat</div>'
    body = f"""
<main>
{page_hero("What We Treat", "Overview of Treatments",
  "Twelve specialized treatment pathways — every one beginning with a thorough evaluation and a plan built for you.", crumbs, cta_href="../contact.html")}
<section class="section">
  <div class="wrap">
    <h2 class="sr-only">All Conditions We Treat</h2>
    <div class="cond-grid" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr));">{cards}</div>
  </div>
</section>
{cta_band(1)}
</main>
"""
    write("treatments/index.html",
          head("Conditions We Treat | Physical Therapy North Palm Beach",
               "Back, neck, shoulder, knee, hip, foot and ankle pain, hand and wrist injuries, headaches, post-surgical rehab, workers' comp and auto accident recovery.", depth=1, canonical="treatments/index.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("What We Treat", "treatments/index.html")]))
          + nav(1) + body + footer(1))

    cond_slugs = list(CONDITIONS)
    svc_for = {"hand-wrist": ("hand-therapy", "Certified Hand Therapy"),
               "workers-comp": ("occupational-therapy", "Occupational Therapy"),
               "post-surgical": ("physical-therapy", "Physical Therapy")}
    for slug, c in CONDITIONS.items():
        # Condition page -> the blog posts that go deeper on it. Several posts had
        # exactly one inbound link (their card on blog/index.html) until these
        # were added; a condition page is the natural, topical place to link them.
        # Condition page -> the blog posts that go deeper on it. Several posts had
        # exactly one inbound link (their card on blog/index.html) until these
        # were added; a condition page is the natural, topical place to link them.
        # Slugs only — link text comes from BLOG_POSTS so titles never drift.
        COND_BLOG = {
            "knee-pain": ["knee-arthritis-before-surgery", "partial-vs-total-knee-replacement"],
            "back-pain": ["five-morning-habits-back-pain", "hip-impingement-back-pain-north-palm-beach"],
            "hand-wrist": ["why-hand-therapy-is-different"],
            "hip-pain": ["hip-impingement-back-pain-north-palm-beach", "pain-2-power-ep10-mcvicker"],
            "neck-pain": ["headaches-that-start-in-the-neck"],
            "shoulder-pain": ["reverse-shoulder-replacement-explained"],
            "headache-relief": ["headaches-that-start-in-the-neck"],
            "post-surgical": ["partial-vs-total-knee-replacement", "reverse-shoulder-replacement-explained"],
        }
        _posts = [b for b in COND_BLOG.get(slug, []) if b in BLOG_POSTS]
        if _posts:
            _links = " &middot; ".join(
                f'<a href="../blog/{b}.html">{BLOG_POSTS[b]["title"]}</a>' for b in _posts)
            blog_link = f'<section class="section" style="padding:1.6rem 0 0;"><div class="wrap"><p class="inline-refs">From the blog: {_links}</p></div></section>'
        else:
            blog_link = ""
        # Condition-level depth, currently hand and wrist only.
        #
        # Why this exists, and why it is NOT more words on a location page:
        # the 2026-09-21 Search Console pull showed Google finished collapsing
        # the old Wix URLs into their redirect targets partway through the
        # window (/hand-therapy went 655 impressions to 0 across two 45-day
        # halves while /services/hand-therapy.html went 172 to 865). Every
        # position averaged over 90 days was therefore a blend of two regimes
        # and could not be read. On the clean 45 days after consolidation, the
        # hand and wrist SYMPTOM queries are the live opportunity: "hand pain
        # treatment west palm beach" 129 impressions at position 14.4 and
        # "wrist pain treatment west palm beach" 98 at 23.0, 318 impressions a
        # month of symptom intent converting at zero.
        #
        # The problem those numbers describe is targeting, not thinness. The
        # SERVICE page was ranking for the symptom queries while this condition
        # page drew 111 impressions in 90 days, so our two pages split the
        # signal and neither won. The division of labour is now explicit:
        # /services/hand-therapy.html owns practitioner intent ("hand
        # therapist", "certified hand therapist"), and this page owns symptom
        # intent ("hand pain", "wrist pain", "carpal tunnel").
        #
        # So this block is written from the SYMPTOM inward, which is also how
        # people search it, and deliberately shares no sentence with the
        # diagnosis-first blocks in SVC_DEEP or the 12 hand Q&As on /faq.html.
        # Duplicating either would make three of our own pages compete.
        # Same content rules as SVC_DEEP: every statement restates something the
        # site already asserts, and there is no new clinical claim, no mechanism,
        # no statistic and no promised outcome. We evaluate and rehabilitate; we
        # do not diagnose here and we never claim surgery.
        COND_DEEP = {
            "hand-wrist": {
                "h2": "Hand and wrist pain, and what usually helps",
                "intro": "Most people do not arrive knowing what is wrong. They arrive because something "
                         "hurts, or has gone numb, or will not grip the way it used to. The evaluation is "
                         "what sorts that out. What follows is how the most common complaints tend to "
                         "present, so you have some idea what you are looking at before you call.",
                "blocks": [
                ("Numbness or tingling that wakes you up",
                 "Hand symptoms that are worse at night, or that show up while you are driving or holding "
                 "a phone, are a common reason people are referred to hand therapy. Caught early, these "
                 "cases often respond to conservative care, and a custom night splint is frequently part "
                 "of it. If your case turns out to warrant a surgical opinion we will tell you plainly "
                 "and coordinate with your physician rather than keep you in therapy."),
                # Carpal tunnel and trigger finger blocks added 2026-10-23 (Semrush
                # 10-23: "carpal tunnel treatment" and "trigger finger treatment"
                # outside the top 100; this page owns that condition intent since
                # 2026-10-16 but no heading named either condition). Every sentence
                # restates the site's own carpal tunnel / trigger finger copy (the
                # hand therapy service page and the /faq.html hand answers) in new
                # words: no mechanism, statistic, outcome or new technique.
                ("Carpal tunnel syndrome treatment",
                 "Carpal tunnel is treated here by our certified hand therapist, Laura Drumm, MS, OTR/L, "
                 "CHT, CLT, both for people trying to avoid surgery and for people recovering from it. "
                 "Without surgery, a plan can include a custom night splint, made in our clinic, that "
                 "keeps the wrist in a neutral position while you sleep, nerve and tendon gliding "
                 "exercises, and changes to the workstation setup and daily activities that keep setting "
                 "symptoms off. It tends to help most when symptoms are caught early. If your case needs "
                 "a surgical consult, you will hear that honestly and we will coordinate with your "
                 "physician. After surgery, care follows your surgeon’s protocol."),
                ("Wrist pain that has not settled",
                 "A wrist can stay painful and stiff long after the injury that caused it, and it is one "
                 "of the areas people most often assume they simply have to live with. Wrists fall "
                 "squarely inside a certified hand therapist\u2019s scope alongside the hand itself, and the "
                 "evaluation looks at motion, strength and how the whole forearm is loading before "
                 "anything is treated."),
                ("Grip and dexterity that have quietly gone",
                 "Jars, keys, buttons and steering wheels are usually where people first notice. Lost "
                 "grip and pinch are treated directly here rather than left to come back on their own, "
                 "and because our occupational therapy program runs in the same building, the daily tasks "
                 "you are actually struggling with can be worked on alongside the hand itself."),
                ("Pain at the base of the thumb",
                 "Thumb pain that flares with pinching, opening and twisting is common and it is one of "
                 "the conditions conservative hand therapy addresses most effectively. Treatment leans on "
                 "joint protection technique, targeted strengthening, a supportive splint made here, and "
                 "changing the specific movements that keep aggravating it."),
                ("Trigger finger treatment for a finger that catches",
                 "Trigger finger is treated in our hand therapy program both conservatively, where that "
                 "is appropriate, and after surgery, where it has already happened. The usual tools are a "
                 "splint fabricated here for your hand, graded motion, and changes to the grips and "
                 "activities that keep aggravating it. After an operation, the plan follows your "
                 "surgeon\u2019s protocol."),
                ("A hand that is still swollen after surgery",
                 "Post-operative hands are managed to the surgeon\u2019s protocol, and the swelling, "
                 "stiffness and scar that follow an operation are treated as part of the plan rather "
                 "than as something to wait out."),
                ("After a cast comes off",
                 "The fracture healing and the hand working again are two different problems, and the "
                 "second one is the reason people come here. Expect the early work to be about motion and "
                 "swelling before it is about strength, and expect the pace to be set by the tissue that "
                 "is healing rather than by a fixed number of weeks."),
                ("Do you need a referral, and will insurance cover it",
                 "It depends on your plan, and post-operative patients usually arrive with a referral and "
                 "protocol from their surgeon already. The quickest way to find out is to call the front "
                 "desk at 561-624-4263 \u2014 they will check what your plan requires, including how it "
                 "handles a custom splint, before you come in."),
                ],
            },
            # Shoulder pain. Added 2026-10-14 (Nick: "deepen the shoulder page
            # next"). The GSC deep dive found the homepage (pos 3.3) and the
            # treatments index (7.4) outranking this page (8.1) for "shoulder pain
            # treatment north palm beach", on a page of about 330 words. Quotes are
            # from Pain 2 Power: Episode 9 (Dr. Vani Sabesan, transcript_v4.json on
            # tmp/sabesan-out), Episode 8 (Dr. Ryan Simovitch, transcripts.md on
            # media/ep8-clips) and Episode 13 (Captain Kerry, transcript-full.md on
            # media/ep13-clips). Guest figures are attributed to the guest, never
            # stated as ours. The home exercise table restates EXERCISES.
            "shoulder-pain": {
                "h2": "Shoulder pain questions, answered",
                "intro": "We hear the same handful of shoulder questions every week at our North Palm Beach "
                         "clinic, and three of the shoulder specialists who have been on our Pain 2 Power show "
                         "have answered a few of them on air. Here they are in one place. Your own answers "
                         "still come from your evaluation.",
                "blocks": [
                ("Why does my shoulder ache at night?",
                 "Night pain is one of the most common things people mention, and it is worth mentioning. "
                 "Dr. Dave Kashuba, Ph.D., OTR, put it this way on Episode 9: patients start talking about "
                 "their shoulder &ldquo;and they&rsquo;re like, really aches at night. And so now you know, "
                 "you&rsquo;re looking more at a bursitis and a tendonitis.&rdquo; The details you give your "
                 "therapist steer the whole evaluation, so tell us when it hurts, what you were doing, and how "
                 "you sleep."),
                ("Is it my rotator cuff?",
                 "It might be, and you would have plenty of company. Orthopaedic shoulder surgeon Dr. Vani "
                 "Sabesan, MD, told our listeners that among people over 60, &ldquo;one out of three people are "
                 "going to have a rotator cuff pathology.&rdquo; Rotator cuff strains, tears and repairs are "
                 "among the conditions we treat most. The evaluation tests how the cuff and the shoulder blade "
                 "are working before anything gets a label."),
                ("Who wears out a shoulder fastest?",
                 "Not always the people you would guess. Orthopedic shoulder surgeon Dr. Ryan Simovitch "
                 "described the patient he sees most as the constant warrior: someone playing pickleball four "
                 "to six days a week with no moderation and no preparation, until something gives. Dr. Sabesan "
                 "made the same point about Florida, where the weather lets people play all year round. If that "
                 "sounds like your schedule, strength work for the cuff and shoulder blade is the cheapest "
                 "insurance you can buy."),
                ("Can therapy help me avoid surgery?",
                 "For a lot of shoulder problems, therapy is where care starts, and our approach is the same "
                 "whether you are trying to avoid surgery or recovering from it: restore pain-free range first, "
                 "then rebuild rotator cuff and shoulder blade strength, then get back to reaching overhead, "
                 "lifting, sport and sleep without guarding. If your evaluation points toward a surgical "
                 "opinion, we will tell you plainly and coordinate with your physician."),
                ("What about after rotator cuff repair or a shoulder replacement?",
                 "Your surgeon sets the protocol and we follow it exactly. Protocols are changing, too. Dr. "
                 "Sabesan described comparing six weeks in a sling with moving the shoulder within days after "
                 "surgery, and said of the result, &ldquo;we found that the outcomes were similar.&rdquo; She was "
                 "also candid about the hard part of cuff repairs: &ldquo;We&rsquo;re really good at fixing "
                 "them. We&rsquo;re not great at getting them to heal.&rdquo; That healing window is exactly "
                 "what post-operative therapy is paced around. If you are facing a reverse shoulder replacement, "
                 "read <a href=\"../blog/reverse-shoulder-replacement-explained.html\">Total vs. Reverse "
                 "Shoulder Replacement: How Surgeons Decide</a>."),
                ("Does the therapist really make a difference?",
                 "We are biased, so take it from a surgeon. Dr. Sabesan said her team surveyed their shoulder "
                 "replacement patients and &ldquo;98 percent of patients said the therapist was a huge impact on "
                 "their outcome.&rdquo; Her comparison was a good hairdresser: someone who talks to you, listens, "
                 "and adjusts. Every session here is one-on-one with a therapist, which is the whole point."),
                ("How often will I come in, and what do I do in between?",
                 "Usually a few visits a week, and the work between visits counts as much as the visits. "
                 "Captain Kerry, of Bravo&rsquo;s Below Deck, came to us about twenty years ago with a "
                 "rotator cuff injury and has had two surgeries on that shoulder since. On Episode 13 he said, "
                 "&ldquo;I&rsquo;ve got full motion. I&rsquo;ve had two surgeries in there now and both times "
                 "Dave and his team have got me back together.&rdquo; When he traveled, he took a band program "
                 "with him. Dave&rsquo;s rule on the same episode: he sees people two to three times a week, "
                 "&ldquo;and those other hours they&rsquo;ve got to be doing their exercises and they got to do "
                 "them correctly.&rdquo;"),
                ("Which exercises are safe to start at home?",
                 "The ones your therapist gives you after your evaluation. Most shoulder programs here borrow from "
                 "Dave&rsquo;s at-home set below, because almost everything we do all day pulls the shoulders "
                 "forward and inward and this set works the other way. Full instructions are on our "
                 "<a href=\"../exercises.html\">home exercises page</a>. If a movement causes sharp pain, stop "
                 "and ask us."),
                ("Do I need a referral, and will insurance cover it?",
                 "In most cases Florida's direct access law lets you begin a physical therapy evaluation "
                 "without a physician referral. Post-surgical patients usually arrive with a referral and "
                 "protocol from their surgeon already. Before your first visit our front desk verifies your "
                 "Medicare or commercial benefits and tells you what your plan needs. Our "
                 "<a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> explains deductibles "
                 "and coinsurance."),
                ],
                "extra": '''
      <div class="data-table" tabindex="0" role="region" aria-label="Dave's at-home shoulder set">
        <table>
          <caption>Dr. Dave Kashuba's at-home shoulder set, as he described it on Pain 2 Power Episode 8. Start it after your evaluation, not instead of one.</caption>
          <thead><tr><th scope="col">Exercise</th><th scope="col">How</th><th scope="col">Dose</th></tr></thead>
          <tbody>
            <tr><th scope="row">Wall slides</th><td>Face a wall with a towel under your forearms, arms bent at 90 degrees, and slide both arms up the wall and back down</td><td>3 sets of 10</td></tr>
            <tr><th scope="row">Cross-body stretch</th><td>Take one elbow in the other hand and draw that arm across your body, then switch</td><td>Hold, both sides</td></tr>
            <tr><th scope="row">Shoulder shrugs</th><td>Bring both shoulders straight up toward your ears, then let them down</td><td>3 sets of 10</td></tr>
            <tr><th scope="row">Scapular retractions</th><td>Draw both shoulders back as if to touch your shoulder blades together</td><td>3 sets of 10</td></tr>
            <tr><th scope="row">Band rows and extensions</th><td>Anchor a therapy band and pull back, elbows past your ribs, then draw the arm behind you</td><td>Build gradually</td></tr>
          </tbody>
        </table>
      </div>
      ''',
            },
            # headache-relief: deepened 2026-10-14 (GSC depth pass). Same content rules as
            # neck-pain: restates site facts and Pain 2 Power transcripts only.
            "headache-relief": {
                "h2": "Headache treatment questions, answered",
                "intro": "These are the practical questions people in North Palm Beach ask us about headaches, from what we treat to what helps between visits. For the longer explanation of how a stiff neck turns into head pain, read <a href=\"../blog/headaches-that-start-in-the-neck.html\">The Headache That Starts in Your Neck</a>.",
                "blocks": [
                ("Which headaches do you treat?",
                 "Headaches that come from the neck. That means cervicogenic headaches, which are driven by the joints and tissues at the top of the spine, and tension-type headaches, which tend to feel like a tight band around the head. It also means headaches after whiplash or a concussion, once a physician has seen you, and the jaw and posture habits that feed head pain. Plenty of people have a mix of these. The evaluation sorts out how much of yours is coming from the neck before anything is treated."),
                ("Do you treat migraines?",
                 "Migraine itself, along with its diagnosis and any medication for it, stays with your physician. Our part is the neck, when it is one of the things that sets a migraine off: stiff joints at the top of the spine, tight muscles running from the shoulders into the base of the skull, and long hours held in one position. Tell us what your doctor has diagnosed and what you take. We treat the part that belongs to us and leave your medication plan exactly as your physician set it."),
                ("How can I tell if my headache is coming from my neck?",
                 "On your own, you can only collect clues. A headache that starts at the base of the skull or on one side, builds through the afternoon, gets worse after a desk day or a long drive on I-95, and eases when you stand up and move makes the neck a suspect, especially with a stiff neck or sore shoulders alongside. <a href=\"../blog/headaches-that-start-in-the-neck.html\">Our headache article</a> sets those patterns out in a table. The evaluation is where we check them. If neck pain is the bigger complaint, start with our <a href=\"neck-pain.html\">neck pain treatment</a> page."),
                ("What happens at my first visit?",
                 "Plan on about an hour, one-on-one with your therapist. We start with your story: when the headaches come, which side, what you were doing beforehand and what helps. Then we watch how your neck moves and measure motion, strength and the positions that bring the pain on. Treatment usually begins the same day. On Episode 10 of Pain 2 Power, Dr. Dave Kashuba, Ph.D., OTR, described the clinic this way: &ldquo;we try to take each person individually and figure out a game plan for them.&rdquo; The <a href=\"../first-visit.html\">first visit page</a> covers what to bring."),
                ("What does treatment involve?",
                 "Usually two parts. First, skilled <a href=\"../glossary.html#manual-therapy\">manual therapy</a>: your therapist finds the stiff or irritable joints at the top of the neck and uses gentle techniques to restore how they move, while easing the muscles guarding around them. Second, the reasons the tension keeps rebuilding. That means strengthening for the deep neck flexors and upper back, plus coaching on your desk setup and the way you sleep. If your jaw is part of the picture, we look at that too. The plan changes as you respond."),
                ("What can I do between visits?",
                 "Your home program, done the way you were shown. Two staples of our neck programs are on the <a href=\"../exercises.html#shoulder\">home exercises page</a>: scapular retractions and shoulder shrugs, three sets of ten, because both work against the forward head posture that keeps the upper neck loaded. The <a href=\"../exercises.html#everyday\">everyday movement</a> list matters just as much. Put the phone down, get up and walk, and stretch before the day starts. Dave is plain about the goal. On Episode 8 he said, &ldquo;I do everything I can to let people not ever come to see me.&rdquo;"),
                ("How many visits will I need?",
                 "It depends on what is driving the headaches and how long you have had them. After your evaluation your therapist proposes a visit frequency and honest milestones, then reassesses as you go, so you are never attending sessions you don't need. When the neck is the driver, treating it can reduce how often the headaches come and how hard they hit. Jot down when each headache starts and what you were doing beforehand. A few weeks of those notes lets you and your therapist compare instead of guess."),
                ("When does a headache need a doctor first?",
                 "Some headaches are emergencies. A sudden, severe headache that feels like the worst of your life needs urgent medical care, and so does one with fever, confusion, vision loss, weakness, numbness or trouble speaking, or one that follows a significant blow to the head. A headache that is new, or different from your usual pattern, should be checked by a physician before therapy. The same goes after a car accident or a concussion: a physician first, and in Florida within 14 days of a crash if personal injury protection is going to pay. Our <a href=\"auto-accident.html\">car accident rehab</a> page explains that rule."),
                ("Do I need a referral, and will insurance cover it?",
                 "In most cases Florida's direct access law lets you begin a physical therapy evaluation without a physician referral. Some plans still require one for coverage, and Medicare requires a physician to certify your plan of care. Before your first visit our front desk verifies your Medicare or commercial benefits and tells you what your plan needs. After a car accident, physical therapy is follow-up care on your physician's referral. Our <a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> explains deductibles and coinsurance."),
                ],
                "extra": "\n      <div class=\"data-table\" tabindex=\"0\" role=\"region\" aria-label=\"Where to start with a headache\">\n        <table>\n          <caption>Where to start with a headache, and what therapy does about it. Drawn from the conditions we treat and the red flags in our headache article. Use it to decide who to call first; your physician or your evaluation decides the rest.</caption>\n          <thead><tr><th scope=\"col\">Your headache</th><th scope=\"col\">Where to start</th><th scope=\"col\">Our part</th></tr></thead>\n          <tbody>\n            <tr><th scope=\"row\">Cervicogenic: starts in the neck, often on one side</th><td>An evaluation with us</td><td>Manual therapy for the upper neck, then strength and posture work</td></tr>\n            <tr><th scope=\"row\">Tension-type: a tight band around the head</th><td>An evaluation with us</td><td>The same plan, plus coaching on your desk setup and sleep position</td></tr>\n            <tr><th scope=\"row\">Jaw or posture feeding the head pain</th><td>An evaluation with us</td><td>Part of the evaluation and the plan</td></tr>\n            <tr><th scope=\"row\">After whiplash or a concussion</th><td>A physician first; after a crash, within 14 days for PIP</td><td>Gentle care on referral, building as you recover</td></tr>\n            <tr><th scope=\"row\">Migraine</th><td>Your physician, who manages the diagnosis and medication</td><td>Neck-related triggers, alongside your physician's care</td></tr>\n            <tr><th scope=\"row\">New, or different from your usual pattern</th><td>Your physician first</td><td>Treatment once the serious causes are ruled out</td></tr>\n            <tr><th scope=\"row\">Sudden and severe, or with fever, confusion, vision loss, weakness, numbness or trouble speaking</th><td>Emergency care now</td><td>None until a physician has seen you</td></tr>\n          </tbody>\n        </table>\n      </div>\n      ",
            },
            # knee-pain: deepened 2026-10-14 (GSC depth pass). Same content rules as
            # neck-pain: restates site facts and Pain 2 Power transcripts only.
            "knee-pain": {
                "h2": "Knee pain questions, answered",
                "intro": "These are the knee questions we hear most at our North Palm Beach clinic, some of them answered on air by surgeons on our Pain 2 Power show. Your own answers come from your evaluation.",
                "blocks": [
                ("Can physical therapy help knee arthritis?",
                 "Usually, and it is where care starts. Osteoarthritis is the most common cause of the knee pain we see, and Dave has found it in patients as young as their mid-thirties. Orthopedic surgeon Dr. Richard Weiner, M.D., was plain about the order on Episode 6: &ldquo;Surgery is the last resort,&rdquo; he said. &ldquo;The first thing is conservative treatment.&rdquo; Therapy sits high on his list because &ldquo;you need to have strong muscles to stabilize the knee to have fewer symptoms.&rdquo; His whole ladder is in <a href=\"../blog/knee-arthritis-before-surgery.html\">Knee Pain: What to Try Before You Think About Surgery</a>."),
                ("What about a torn meniscus or a ligament injury?",
                 "ACL, MCL and meniscus injuries are among the knee problems we treat, before surgery and after it. For a fresh twist, sports medicine surgeon Dr. Rami Elkhechen, M.D., told listeners on Episode 7 to give it a few days of rest and ice. If the pain settles, you likely don't need an office visit. If it lingers, come in. Before an ACL operation he has patients strengthen the quadriceps and hip abductors. If imaging shows one small damaged patch of cartilage, read <a href=\"../blog/cartilage-transplant-knee-explained.html\">Cartilage Transplants: Rebuilding a Knee Instead of Replacing It</a>."),
                ("What is runner's knee?",
                 "It's the everyday name for patellofemoral pain, kneecap pain that is common in runners and non-runners alike. The vastus medialis, on the inside of the knee, helps track the kneecap, so Dave strengthens the whole quadriceps and works the muscles above and below the joint, glutes and calves included. Dave described many of his patients as &ldquo;building up their knee, building up their ankle to go back running, playing sports.&rdquo; If your mornings on A1A end with an aching knee, that is the goal we build toward."),
                ("What does a knee assessment look at?",
                 "Plan on about an hour, one-on-one. We start with your history: what hurts, when, and what it stops you doing. Then we watch you walk and climb a step, measure how far the knee bends and straightens and how strong the muscles around it are, and check the hips and ankles that share the load. Bring any imaging, though Dr. Weiner's rule applies: &ldquo;you don't treat an X-ray, you treat the patient.&rdquo; Treatment usually begins the same day. People come to our one clinic on US-1 from across the county, <a href=\"../locations/west-palm-beach.html\">West Palm Beach</a> included. See the <a href=\"../first-visit.html\">first visit page</a>."),
                ("What does knee pain treatment involve?",
                 "Every session is one-on-one. Expect hands-on <a href=\"../glossary.html#manual-therapy\">manual therapy</a> for joint mobility, progressive strengthening of the quadriceps, hips and glutes, and practice at what knees get asked to do: stairs, longer walks, getting out of a car. The goal comes from you. Some of Dave's patients are &ldquo;just wanting to get off the chair and be able to make themselves a pot of coffee,&rdquo; as he said on Episode 8. After your evaluation your therapist proposes a visit frequency and honest milestones, then adjusts to how you respond."),
                ("What does rehab look like after a knee replacement?",
                 "Your surgeon sets the protocol and we follow it exactly. Joint replacement patients here follow a structured pathway from first bend to full stride: range first, then quadriceps strength, then stairs and walking distance. One patient, Sandy S., wrote that they &ldquo;had a great experience rehabbing from double knee replacements.&rdquo; A partial usually needs less rehab than a total, which is one reason to read <a href=\"../blog/partial-vs-total-knee-replacement.html\">Partial vs Total Knee Replacement</a> before you book. On prehab, Dr. Michael Leighton, MD, said it is &ldquo;not a one-size-fits-all situation.&rdquo; More on our <a href=\"post-surgical.html\">post-surgical rehab</a> page."),
                ("Which knee exercises can I start at home?",
                 "Most knee programs here borrow from the set Dr. Dave Kashuba, Ph.D., OTR, walks through on Pain 2 Power, below. Do the heel to buttock one leg at a time; both at once, Dave warns, is how you end up on the floor. On the sit to stands, the pillow reaching forward makes your hips start the movement and take the load. Full instructions are on our <a href=\"../exercises.html#knee\">home exercises page</a>. If an exercise causes pain, swelling or warmth in the joint, stop and call us."),
                ("When should a doctor see my knee first?",
                 "A pop followed by sudden pain and a leg you can't stand on is a day for an orthopedic specialist or the hospital. So is a knee that turns hot, red and swollen with a fever, or knee pain after a significant fall. Get evaluated soon if the pain isn't settling, if swelling or warmth develops, or if the knee gives way or locks. Dr. Weiner's test has nothing to do with a pain score: get help &ldquo;when your symptoms interfere with ADLs, which means activities of daily living.&rdquo;"),
                ("Do I need a referral, and will insurance cover it?",
                 "In most cases Florida's direct access law lets you begin a physical therapy evaluation without a physician referral. Some plans still require one for coverage, and Medicare requires a physician to certify your plan of care. After a knee replacement or ligament repair you will usually arrive with a referral and protocol from your surgeon already. Before your first visit our front desk verifies your Medicare or commercial benefits and tells you what your plan needs. Our <a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> explains deductibles and coinsurance."),
                ],
                "extra": "\n      <div class=\"data-table\" tabindex=\"0\" role=\"region\" aria-label=\"Dave's at-home knee set\">\n        <table>\n          <caption>Dr. Dave Kashuba's at-home knee set, as he described it on Pain 2 Power Episodes 6 and 7. Start it after your evaluation, not instead of one.</caption>\n          <thead><tr><th scope=\"col\">Exercise</th><th scope=\"col\">How</th><th scope=\"col\">Dose</th></tr></thead>\n          <tbody>\n            <tr><th scope=\"row\">Seated leg extensions</th><td>Sit at the front edge of a chair, straighten one leg out in front of you, then lower it</td><td>3 sets of 10, building to 3 sets of 20</td></tr>\n            <tr><th scope=\"row\">Standing heel to buttock</th><td>Hold the back of a chair, stand tall and bring one heel toward your backside as far as is comfortable, one leg at a time</td><td>3 sets of 10, building to 3 sets of 20</td></tr>\n            <tr><th scope=\"row\">Pillow sit to stands</th><td>Hold a light pillow out in front of you, push it forward as you stand and keep it forward as you sit back down</td><td>3 sets of 10</td></tr>\n            <tr><th scope=\"row\">Step stool leans</th><td>One foot on a low step stool, a hand on something stable, lean your weight forward over the raised foot and back. No stepping up</td><td>Slow and controlled</td></tr>\n            <tr><th scope=\"row\">Glute bridge</th><td>Lie on your back, knees bent and feet flat, lift your hips, pause and squeeze at the top, then lower</td><td>3 sets of 10</td></tr>\n          </tbody>\n        </table>\n      </div>\n      ",
            },
            # hip-pain: deepened 2026-10-14 (GSC depth pass). Same content rules as
            # neck-pain: restates site facts and Pain 2 Power transcripts only.
            "hip-pain": {
                "h2": "Hip pain questions, answered",
                "intro": "These are the hip questions we hear most at our North Palm Beach clinic. Two orthopedic surgeons from our Pain 2 Power show answered several of them on air. Your own answers come from your evaluation.",
                "blocks": [
                ("Is it my hip or my back?",
                 "Dr. Dave Kashuba, Ph.D., OTR, listens for pain that travels toward the groin rather than down the leg. Orthopedic surgeon Dr. Zach McVicker, MD, said on Episode 10 that with hips, &ldquo;a lot of times it&rsquo;s causing the back pain, it&rsquo;s causing the groin pain and other symptoms that you&rsquo;re having.&rdquo; Groin pain tops his list, ahead of low back pain and pain toward the buttock. Hip impingement is one common reason, explained in <a href=\"../blog/hip-impingement-back-pain-north-palm-beach.html\">Hip Impingement: When Your Back Pain Is Coming From Your Hip</a>. If it is your spine, see <a href=\"back-pain.html\">back pain treatment</a>."),
                ("What is a labral tear, and will I need surgery?",
                 "The labrum is a ring of cartilage around the ball of the hip. Dr. McVicker compares it to a gasket between two pipes, sealing the joint so your weight spreads across the whole socket with every step. Labral irritation is one of the hip problems we treat. Whether a tear needs repair is your surgeon&rsquo;s call. When it does, he described arthroscopy as &ldquo;little cameras, little poke holes,&rdquo; and his advice was short: &ldquo;Look into it early.&rdquo; After surgery we follow your surgeon&rsquo;s protocol. <a href=\"../blog/pain-2-power-ep10-mcvicker.html\">Our Episode 10 recap</a> has the whole conversation."),
                ("What about pain on the outside of the hip?",
                 "Pain on the outside of the hip was on Dr. McVicker&rsquo;s list too, and bursitis and tendinopathy around the hip are among the conditions we treat. When hip pain starts, Dave said, &ldquo;a lot of times it is a muscle called the gluteus medius,&rdquo; the muscle that keeps your pelvis level while you stand on one leg. Standing leg abductions, in the table below, work it directly. Dave&rsquo;s everyday advice: stop sitting with your legs crossed, break up repetitive bending, and modify the task that sets it off."),
                ("Can physical therapy help hip arthritis?",
                 "Hip osteoarthritis heads the list of conditions our hip program treats, with work on mobility, glute and deep stabilizer strength, and walking mechanics. If a replacement is coming, ask your surgeon about prehab. Orthopedic surgeon Dr. Michael Leighton, MD, called it on Episode 12 &ldquo;tuning this patient up for surgery prior to surgery,&rdquo; and said &ldquo;it&rsquo;s not a one-size-fits-all situation.&rdquo; He prescribes it mostly for people who have been away from activity. If the joint needs more than therapy, we will say so plainly."),
                ("What does rehab after a hip replacement look like?",
                 "Your surgeon sets the protocol and we follow it exactly. Dr. Leighton keeps most patients in the hospital overnight, where &ldquo;they get physical therapy the day of surgery and they get physical therapy the day after surgery.&rdquo; After that, &ldquo;it&rsquo;s time for you to gradually and slowly over the next few weeks get your motion back.&rdquo; Most of the old dislocation precautions are gone, though early on he still limits bringing the knee to the chest. In a Google review, Christine H. wrote that after her hip replacement our therapists &ldquo;built my strength, stamina, and walking confidence back quickly.&rdquo; More on <a href=\"post-surgical.html\">post-surgical rehabilitation</a>."),
                ("What does the evaluation look at?",
                 "Plan on about an hour, one-on-one with your therapist, and wear shorts. We ask where it hurts and when, watch you walk and stand on one leg, and measure how far the hip bends and rotates and which positions bring the pain on. Dave said on Episode 10, &ldquo;It takes me all of 10 minutes for me to sit down with you and go over a little bit about your symptoms,&rdquo; and from there he knows which specialist you need. Treatment usually begins the same day. The <a href=\"../first-visit.html\">first visit page</a> has the details."),
                ("Which exercises can I start at home?",
                 "The ones your therapist gives you after your evaluation, usually from Dave&rsquo;s Episode 10 set in the table below. The first is a sit to stand with a band just above the knees. A sore hip shifts your weight onto the good leg without your noticing, and the band makes both sides share the work. For floor exercises, his rule: &ldquo;When you get on the floor, first make sure you&rsquo;re able to get back up.&rdquo; Full instructions are on our <a href=\"../exercises.html#hip\">home exercises page</a>. If a movement causes sharp pain, stop and call us."),
                ("When should a doctor see my hip first?",
                 "Hip pain after a fall, especially if you cannot put weight on the leg, needs a physician before therapy. Co-host Mike McGann explained why on Episode 10: &ldquo;once that hip break happens, there tends to be a really strong domino effect from there.&rdquo; A hot, swollen hip, or hip pain with a fever, also needs a physician first. After a replacement, call your surgeon about redness, drainage or fever at the incision. Once a physician has ruled those out, therapy can start with confidence."),
                ("Do I need a referral, and will insurance cover it?",
                 "In most cases Florida's direct access law lets you begin a physical therapy evaluation without a physician referral. Hip replacement patients usually arrive with a referral and protocol from their surgeon already, and Medicare requires a physician to certify your plan of care. Before your first visit our front desk verifies your Medicare or commercial benefits and tells you what your plan needs. Our <a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> explains deductibles and coinsurance."),
                ],
                "extra": "\n      <div class=\"data-table\" tabindex=\"0\" role=\"region\" aria-label=\"Dave's at-home hip set\"><table><caption>Dr. Dave Kashuba's at-home hip set, as he described it on Pain 2 Power Episode 10. Start it after your evaluation.</caption><thead><tr><th scope=\"col\">Exercise</th><th scope=\"col\">How</th><th scope=\"col\">Dose</th></tr></thead><tbody><tr><th scope=\"row\">Banded sit to stands</th><td>Band around both legs just above the knees; stand up and sit down as the band pushes your knees outward</td><td>3 sets of 10</td></tr><tr><th scope=\"row\">Standing leg abductions</th><td>Hold a chair and kick one straight leg out to the side, then lower with control</td><td>3 sets of 10 each side</td></tr><tr><th scope=\"row\">Clams</th><td>On your side, knees bent and stacked, feet together; open the top knee like a clam shell</td><td>3 sets of 10 each side</td></tr><tr><th scope=\"row\">Side lying leg raise</th><td>On your side, raise the top leg straight up and lower it slowly</td><td>3 sets of 10 each side</td></tr><tr><th scope=\"row\">Prone press up</th><td>Face down, push up onto your forearms or hands with your pelvis on the floor</td><td>Hold, then rest</td></tr></tbody></table></div>\n      ",
            },
            # Neck pain. The 2026-10-14 GSC deep dive (90 days to 2026-10-11) found
            # 13 North Palm Beach neck queries with 593 impressions at average
            # position 8.2 across our pages (337 on this page) and ZERO clicks,
            # on a 324-word page. North Palm Beach is
            # where the clinic is, so unlike the city-qualified queries this is a
            # page-content lever. Same content rules as hand-wrist: every statement
            # restates something the site already says (CONDITIONS, the FAQ, the
            # headache post, EXERCISES), no new mechanism, statistic or outcome.
            # The "doctor first" block mirrors the red flags in the headache post.
            "neck-pain": {
                "h2": "Neck pain questions, answered",
                "intro": "These are the questions people in North Palm Beach ask us most about neck pain, "
                         "answered the way we would answer them at the front desk. Your own answers come "
                         "from your evaluation.",
                "blocks": [
                ("Why does my neck get so stiff?",
                 "Usually it is sustained position. Hours on a phone, a workday hunched toward a screen or "
                 "a long drive with your head pushed forward ask the small joints at the top of the spine "
                 "to hold a load all day. They stiffen, the muscles around them guard, and the neck feels "
                 "locked, often worst first thing in the morning or at the end of a workday. Treatment "
                 "frees the stiff joints with gentle manual therapy, then works on the posture and "
                 "strength that let the stiffness come back."),
                ("What is a pinched nerve in the neck, and can therapy help?",
                 "Clinicians call it cervical radiculopathy: an irritated nerve root in the neck that can "
                 "send pain, tingling or numbness into the shoulder, arm or hand. It is one of the "
                 "conditions our neck program treats. Care follows the same pattern as the rest of the "
                 "program: gentle manual therapy and joint mobilization, strengthening for the deep neck "
                 "and upper back muscles, and changes to the positions you spend your day in. If arm "
                 "weakness is getting worse rather than better, a physician should see it first, and we "
                 "will tell you so."),
                ("Why do my neck and shoulder hurt at the same time?",
                 "The muscles that run from your shoulders up into the back of your head are shared "
                 "territory, so neck pain often spreads into the shoulder or arm. Sometimes the shoulder is "
                 "the real problem and the neck is compensating. The evaluation tests the neck and the "
                 "shoulder separately to sort out which is driving the pain, and the plan treats that one. "
                 "If it turns out to be the shoulder, see our "
                 "<a href=\"shoulder-pain.html\">shoulder pain treatment</a> page."),
                ("Can my headaches come from my neck?",
                 "Often, yes. Many stubborn, recurring headaches start in the stiff joints and tight muscles "
                 "of the upper neck rather than in the head itself. When the neck is the driver, treating it "
                 "can reduce how often the headaches come and how hard they hit. Read "
                 "<a href=\"../blog/headaches-that-start-in-the-neck.html\">The Headache That Starts in Your "
                 "Neck</a>, or see <a href=\"headache-relief.html\">headache treatment</a>."),
                ("What happens at my first visit?",
                 "Plan on about an hour, one-on-one with your therapist. We take your history, watch how your "
                 "neck moves, and measure motion, strength and the positions that bring the pain on. "
                 "Treatment usually begins the same day, often with gentle hands-on work and the first one "
                 "or two exercises of your home program. You leave knowing what is going on and what to do "
                 "between visits. The <a href=\"../first-visit.html\">first visit page</a> has the details."),
                ("Which exercises will I do at home?",
                 "That depends on your evaluation, but most neck programs work the deep neck flexors and the "
                 "upper back. Scapular retractions and shoulder shrugs, three sets of ten, are two that "
                 "Dr. Dave Kashuba, Ph.D., OTR, gives patients often, because they work against the rounded, "
                 "forward posture daily life builds in. Both are on our "
                 "<a href=\"../exercises.html\">home exercises page</a> with instructions. Start them after "
                 "your evaluation, not instead of it."),
                ("How long until my neck feels better?",
                 "Most patients notice meaningful change within the first few weeks of consistent care. How "
                 "many visits you need depends on what is driving the pain, how long you have had it and "
                 "what you want to get back to. After your evaluation your therapist proposes a visit "
                 "frequency and honest milestones, then adjusts the plan to how you actually respond."),
                ("When should a doctor check my neck first?",
                 "Neck pain after a significant fall, blow to the head or car accident should be checked by a "
                 "physician before therapy. So should neck pain that comes with fever, or with weakness or "
                 "numbness in an arm or leg that is getting worse. Ruling out the serious causes is what makes "
                 "it safe to treat the mechanical side with confidence. After a car accident, also read our "
                 "<a href=\"auto-accident.html\">car accident rehab</a> page for Florida's 14-day rule."),
                ("Do I need a referral, and will insurance cover it?",
                 "In most cases Florida's direct access law lets you begin a physical therapy evaluation "
                 "without a physician referral. Some plans still require one for coverage, and Medicare "
                 "requires a physician to certify your plan of care. Before your first visit our front desk "
                 "verifies your Medicare or commercial benefits and tells you what your plan needs. Our "
                 "<a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> explains deductibles "
                 "and coinsurance."),
                ],
            },
            # Back pain. Same deep dive: six North Palm Beach back queries, 191
            # impressions at average position 6.5 across our pages (141 on this
            # page), zero clicks, on a 362-word page. "spinal stenosis treatment
            # north palm beach" sits at 17.0. Same content rules as
            # neck-pain; the morning advice is the five-morning-habits post.
            "back-pain": {
                "h2": "Back pain questions, answered",
                "intro": "These are the questions people in North Palm Beach ask us most about back pain and "
                         "sciatica. Your own answers come from your evaluation, but this is where most "
                         "conversations start.",
                "blocks": [
                ("What is sciatica, and can physical therapy help?",
                 "Sciatica is pain that travels from the low back or buttock down the leg, often with "
                 "tingling or numbness along the way. It is one of the most common reasons people come to "
                 "our back pain program. Treatment blends hands-on work to restore mobility, core and hip "
                 "strengthening, and changes to the sitting, bending and lifting habits that keep provoking "
                 "it. Pain that runs into your leg is worth a professional look sooner rather than later."),
                ("Why is my back worst first thing in the morning?",
                 "Backs are often stiffest when you first get up: discs rehydrate overnight, muscles cool "
                 "down, and the first movements of the day feel the hardest. Rolling to your side and pushing "
                 "up with your arms, instead of sitting straight up, spares your spine a loaded crunch while "
                 "it is still waking up. "
                 "<a href=\"../blog/five-morning-habits-back-pain.html\">Five Morning Habits That Ease Back "
                 "Pain</a> has the rest of the routine."),
                ("Can physical therapy help spinal stenosis?",
                 "Spinal stenosis is one of the spinal conditions our back program treats. Care works on "
                 "mobility, on the core and hip strength that supports the spine, and on the standing and "
                 "walking daily life asks for, at a pace that respects how your back responds. If your "
                 "evaluation points toward a surgical opinion, we will say so plainly and coordinate with "
                 "your physician."),
                ("Do I need surgery for a herniated or bulging disc?",
                 "Your physician or surgeon makes that call. What we can do is treat it: herniated and "
                 "bulging discs and degenerative disc disease are all part of our back program, and so is "
                 "recovery after spine surgery, where we follow your surgeon's protocol. Our job is to tell "
                 "you honestly how you are responding and to coordinate with your doctor if the plan needs "
                 "to change."),
                ("Could the pain be coming from my hip?",
                 "Sometimes. Hip pain can masquerade as back pain, and a stiff or weak hip can push extra work "
                 "onto the low back. That is why the evaluation looks at your hips and the way you walk, not "
                 "just your spine. Read <a href=\"../blog/hip-impingement-back-pain-north-palm-beach.html\">"
                 "Hip Impingement: When Your Back Pain Is Coming From Your Hip</a>."),
                ("What happens at my first visit?",
                 "Plan on about an hour, one-on-one with your therapist. We take your history, watch you walk, "
                 "bend and sit, and measure strength, range of motion and the movements that bring the pain "
                 "on. Treatment usually begins the same day. You leave with a clear picture of what is going "
                 "on and the first exercises of your home program."),
                ("What will I do at home?",
                 "Every visit ends with a clear home program. Core, hip and glute strength is the long-term "
                 "fix for most recurring back pain, and simple moves like a bridge or a bird dog, attached to "
                 "a habit you already have such as brushing your teeth, are where many programs start. Your "
                 "therapist picks yours from the evaluation."),
                ("When should a doctor see my back first?",
                 "Back pain with loss of bladder or bowel control, numbness in the groin or inner thighs, or "
                 "leg weakness that is getting worse needs urgent medical care, not a therapy appointment. "
                 "So does back pain after a significant fall or accident, or with fever. Once a physician "
                 "has ruled those out, physical therapy can treat the mechanical side with confidence."),
                ("Do I need a referral, and will insurance cover it?",
                 "In most cases Florida's direct access law lets you begin a physical therapy evaluation "
                 "without a physician referral. Some plans still require one for coverage, and Medicare "
                 "requires a physician to certify your plan of care. Before your first visit our front desk "
                 "verifies your Medicare or commercial benefits and tells you what your plan needs. Our "
                 "<a href=\"../insurance.html#medicare-guide\">2026 Medicare guide</a> explains deductibles "
                 "and coinsurance."),
                ],
            },
            # Workers' comp. Added 2026-10-14 from docs/PATIENT-INSIGHTS-2026-10.md
            # (occupational therapy patients stay longest and many are working age)
            # and the deep dive ("work injury rehab" 15.2, "work injury
            # rehabilitation" 30.4, "comp rehab" 39.0). The three Florida rules on
            # this page were read from the 2026 Florida Statutes on flsenate.gov on
            # 2026-10-14 and are cited visibly: s. 440.185(1) 30-day notice,
            # s. 440.13(2)(a) employer furnishes care and (3)(i) carrier authorizes
            # therapy over $1,000, s. 440.191 Employee Assistance and Ombudsman
            # Office. Nick confirmed 2026-10-14 the front desk checks the carrier's
            # authorization before the first visit. Re-check after each legislative
            # session. No legal advice.
            "workers-comp": {
                "h2": "Hurt at work? How workers' comp therapy works here",
                "intro": "A work injury comes with paperwork, deadlines and more people involved than most "
                         "kinds of care. Here is how the pieces fit together in Florida, so you know what to "
                         "expect before your first visit.",
                "blocks": [
                ("What should I do first after a work injury?",
                 "Tell your employer. Under section 440.185 of the Florida Statutes, an injured employee must "
                 "advise the employer within 30 days after the injury, or after symptoms first appear. "
                 "Florida law then requires your employer to furnish the medically necessary treatment the "
                 "injury needs. Therapy is part of that care, and therapy costing more than $1,000 has to be "
                 "authorized by the insurance carrier, so authorization usually comes before the first visit."),
                ("Who decides what therapy I get?",
                 "Your treating physician prescribes therapy and the carrier authorizes it. We evaluate you, "
                 "write a plan built around your job, treat you, and send objective progress reports to your "
                 "physician, adjuster and case manager, so each decision about the next step rests on "
                 "measurements rather than guesses."),
                ("What does return-to-work therapy involve?",
                 "Treatment is functional from the first day and built around the physical demands of your "
                 "actual job. Someone who lifts and carries for a living rehearses lifting and carrying at "
                 "the heights the job requires. Someone who works at a keyboard works on sitting tolerance, "
                 "the shoulders and the hands. Graded conditioning and task simulation mean the work you "
                 "practice here resembles the work waiting for you."),
                ("How does occupational therapy help a work injury?",
                 "Many work injuries land in the hands, wrists, elbows and shoulders, which is occupational "
                 "therapy territory. Our occupational therapists retrain the tasks a job depends on, and hand "
                 "injuries can be treated by Laura Drumm, MS, OTR/L, CHT, CLT, our "
                 "<a href=\"../services/hand-therapy.html\">certified hand therapist</a>, "
                 "with custom splints made in the clinic. Physical and occupational therapy run in the same "
                 "building under one plan, so an injury that needs both does not mean two clinics. More on "
                 "our <a href=\"../services/occupational-therapy.html\">occupational therapy</a> page."),
                ("Can you help with repetitive strain and ergonomics?",
                 "Yes. Repetitive strain injuries are among the work injuries we treat, and they rarely settle "
                 "if the task that caused them stays the same. Workstation assessment, tool and equipment "
                 "recommendations, and changes to technique are part of occupational therapy here, so the "
                 "fix covers the job as well as the body."),
                ("What does my adjuster or case manager receive?",
                 "Objective progress reporting: what was measured at your evaluation, what has changed since, "
                 "and how you are tracking against the demands of your job. We coordinate with your physician "
                 "and case manager throughout, because a safe, sustainable return to work depends on everyone "
                 "working from the same information."),
                ("What should I bring to the first visit?",
                 "Photo ID, your claim number, your adjuster's name and phone number, your employer's details, "
                 "and the prescription or referral from your treating physician. Call 561-624-4263 first: our "
                 "front desk checks the authorization so the visit is covered before you arrive."),
                ("What if my claim is disputed?",
                 "That is a legal and benefits question rather than a therapy one. Florida's Department of "
                 "Financial Services runs an Employee Assistance and Ombudsman Office, set up under section "
                 "440.191, to help injured workers and employers resolve disagreements, and a Florida workers' "
                 "compensation attorney can advise on your own case. We keep treating and documenting while "
                 "your care is authorized."),
                ],
                "extra": '''
      <div class="data-table" tabindex="0" role="region" aria-label="Who does what in a Florida workers' compensation claim">
        <table>
          <caption>Who does what in a Florida workers' comp claim. Rules from the 2026 Florida Statutes, chapter 440.</caption>
          <thead><tr><th scope="col">Who</th><th scope="col">Their part</th></tr></thead>
          <tbody>
            <tr><th scope="row">You</th><td>Tell your employer about the injury within 30 days (s. 440.185)</td></tr>
            <tr><th scope="row">Your employer</th><td>Furnishes the medically necessary treatment the injury needs (s. 440.13)</td></tr>
            <tr><th scope="row">The insurance carrier</th><td>Authorizes therapy; required when it costs more than $1,000 (s. 440.13)</td></tr>
            <tr><th scope="row">Your treating physician</th><td>Prescribes therapy and reviews our progress reports</td></tr>
            <tr><th scope="row">First Rehabilitation</th><td>Evaluates, treats, and reports progress to your physician, adjuster and case manager</td></tr>
          </tbody>
        </table>
      </div>
      <h3>Sources</h3>
      <ol class="src-list">
        <li><a href="https://www.flsenate.gov/Laws/Statutes/2026/440.185" rel="noopener">2026 Florida Statutes, section 440.185</a>: notice of injury to the employer within 30 days.</li>
        <li><a href="https://www.flsenate.gov/Laws/Statutes/2026/440.13" rel="noopener">2026 Florida Statutes, section 440.13</a>: the employer's duty to furnish medically necessary treatment, and carrier authorization for therapy over $1,000.</li>
        <li><a href="https://www.flsenate.gov/Laws/Statutes/2026/440.191" rel="noopener">2026 Florida Statutes, section 440.191</a>: the Employee Assistance and Ombudsman Office.</li>
      </ol>
      <p class="fv-highlight" style="margin-top:1.4rem;">This page is general information, not legal or medical advice. It reflects the 2026 Florida Statutes, and the law can change. For questions about your claim, talk to your adjuster or a Florida workers' compensation attorney.</p>
      ''',
            },
            # Auto accident. The 2026-10-05 Search Console pull showed "auto
            # accident physical therapy near me" ranking 7.1 on the West Palm
            # Beach LOCATION page while this page sat at 23.8, so the city page
            # was winning intent it does not own. Same rules as hand-wrist:
            # symptom-first, every sentence restates something the site already
            # asserts.
            # Florida PIP and the 14-day rule were added 2026-10-14 at Nick's
            # request (docs/seo-kit/CLAUDE-CODE-PROMPT.md, driven by
            # docs/PATIENT-INSIGHTS-2026-10.md: auto patients average 24.6 visits
            # against 13.3). Every PIP statement was read from the 2026 Florida
            # Statutes, s. 627.736(1)(a), on flsenate.gov on 2026-10-14, and the
            # page cites it. Nick confirmed 2026-10-14 that the front desk checks
            # PIP coverage before the first visit. PIP repeal bills have been filed in past sessions:
            # re-check the statute after every legislative session. No legal
            # advice; fault, claims and settlements go to an attorney.
            "auto-accident": {
                "h2": "After a car accident: your questions, answered",
                "intro": "After a crash it is not always obvious what was hurt, and symptoms do not always "
                         "show up right away. The evaluation is where that gets sorted out. Here is what Florida's "
                         "PIP rules mean for therapy, what the first visits look like, and how the most common "
                         "post-accident complaints tend to present.",
                "blocks": [
                ("What is Florida's 14-day PIP rule?",
                 "Florida auto policies include personal injury protection, or PIP. Under section 627.736 of "
                 "the Florida Statutes, PIP medical benefits pay 80% of reasonable expenses for medically "
                 "necessary care, up to a $10,000 limit, but only if you receive initial services and care "
                 "within 14 days after the accident. That is why the first two weeks matter even when you "
                 "feel fine: symptoms that surface later still need that first visit to have happened in time."),
                ("Who do I need to see first?",
                 "The statute names who can provide that initial care: a medical or osteopathic physician, a "
                 "dentist, a chiropractic physician, an advanced practice registered nurse, a hospital, or the "
                 "emergency crew that transported you. Physical therapy is follow-up care, provided on referral "
                 "from one of those providers. So the order is a physician first, within 14 days, then a "
                 "referral to us. If you went to an emergency room, bring that paperwork and our front desk "
                 "will tell you what else is needed."),
                ("Is it $10,000 or $2,500?",
                 "It depends on a medical finding. PIP pays up to $10,000 when a physician, dentist, physician "
                 "assistant or advanced practice registered nurse has determined that you had an emergency "
                 "medical condition. If a provider determines you did not, reimbursement is limited to $2,500. "
                 "That determination belongs to your treating provider, not to us, and it shapes how much "
                 "therapy PIP can pay for."),
                ("What should I bring to the first visit?",
                 "Your photo ID, your auto insurance card and claim number, your adjuster's name and phone "
                 "number, the referral from your physician, and any imaging or emergency room paperwork. If an "
                 "attorney represents you, bring their contact details too. Call 561-624-4263 with the claim "
                 "number and our front desk will check the coverage before you come in."),
                ("What do the first visits look like?",
                 "The first visit is a one-on-one evaluation of about an hour. Your therapist measures motion and "
                 "strength and maps what hurts and when, and treatment usually begins the same day. Care starts "
                 "gently, calming irritated tissue and restoring basic motion, then moves to strengthening and "
                 "back to driving, lifting and work. Every visit is documented, so the record shows where you "
                 "started and how you progressed."),
                ("Pain that showed up days after the accident",
                 "Even a minor collision can leave lasting pain, and symptoms often surface days later "
                 "rather than at the scene. That delay is normal, and it is the reason early evaluation "
                 "matters. Care starts gently, calming irritated tissue and restoring basic motion before "
                 "anything is loaded."),
                ("Whiplash and a stiff, sore neck",
                 "Whiplash and neck injuries are a common reason people come to us after a collision, "
                 "and neck pain responds well to skilled physical therapy. Care usually combines gentle "
                 "manual therapy, deep neck strengthening and posture work, and most patients notice "
                 "meaningful change within the first few weeks of consistent care. More on our "
                 "<a href=\"neck-pain.html\">neck pain treatment</a> page."),
                ("Headaches that started after the crash",
                 "Many headaches start in the neck rather than the head, and headaches after whiplash "
                 "are among those we treat. When the neck is "
                 "the driver, treating the upper neck joints and the muscles around them can reduce how "
                 "often they come and how hard they hit. See <a href=\"headache-relief.html\">headache "
                 "treatment</a>."),
                ("Back pain from the impact",
                 "Back and spine injuries after a crash are treated the way we treat any back pain. "
                 "Treatment blends hands-on work to restore mobility, core and hip strengthening, and movement "
                 "retraining so everyday activity stops provoking the pain. See "
                 "<a href=\"back-pain.html\">back pain treatment</a>."),
                ("Nervous about moving normally again",
                 "Being wary of driving, lifting or turning your head after a crash is common, and it is "
                 "part of what we treat. The plan progresses at a pace you can trust, from basic motion "
                 "to full return to daily activity."),
                ("The documentation your claim needs",
                 "We document your recovery objectively from the first visit and communicate with your "
                 "physician and your representatives as your claim requires. For auto accident cases we "
                 "work directly with your adjuster or attorney’s office, and treatment is built "
                 "around what your case actually has to demonstrate."),
                ("Will insurance cover it?",
                 "PIP is the coverage the Florida rules above describe, and your plan may add other coverage "
                 "on top. The quickest way to find out what applies is to call the front desk at "
                 "561-624-4263. They will check before you come in. More in our "
                 "<a href=\"../faq.html#insurance-cost\">insurance and cost FAQ</a>."),
                ("Do you give legal advice?",
                 "No. We are a therapy clinic, not a law office. We can explain the PIP rules as the statute "
                 "states them and, with your written permission, share your records with your adjuster or "
                 "attorney. Questions about fault, a claim, a settlement or a denied bill belong with a Florida "
                 "attorney."),
                ],
                "extra": '''
      <div class="data-table" tabindex="0" role="region" aria-label="Florida PIP rules for therapy after a car accident">
        <table>
          <caption>Florida personal injury protection (PIP) medical benefits, from section 627.736(1)(a) of the 2026 Florida Statutes.</caption>
          <thead><tr><th scope="col">Rule</th><th scope="col">What it means for you</th></tr></thead>
          <tbody>
            <tr><th scope="row">14-day window</th><td>Initial care has to start within 14 days after the accident for PIP medical benefits to apply</td></tr>
            <tr><th scope="row">Who provides initial care</th><td>A physician, osteopathic physician, dentist, chiropractic physician, advanced practice registered nurse, hospital, or emergency transport crew</td></tr>
            <tr><th scope="row">Where therapy fits</th><td>Physical therapy is follow-up care, on referral from one of those providers</td></tr>
            <tr><th scope="row">What PIP pays</th><td>80% of reasonable expenses for medically necessary care</td></tr>
            <tr><th scope="row">The limit</th><td>Up to $10,000 when an emergency medical condition has been determined; $2,500 when a provider determines there was none</td></tr>
          </tbody>
        </table>
      </div>
      <h3>Source</h3>
      <ol class="src-list">
        <li><a href="https://www.flsenate.gov/Laws/Statutes/2026/627.736" rel="noopener">2026 Florida Statutes, section 627.736</a>: PIP medical benefits, the 14-day requirement, who may provide initial and follow-up care, and the $10,000 and $2,500 limits.</li>
      </ol>
      <p class="fv-highlight" style="margin-top:1.4rem;">This page is general information, not legal, medical or insurance advice. It reflects the 2026 Florida Statutes, and the law can change. For questions about your claim, talk to your insurer or a Florida attorney.</p>
      ''',
            },
        }
        cond_deep_html = ""
        if slug in COND_DEEP:
            _cd = COND_DEEP[slug]
            _cb = "".join(
                f"<h3>{t}</h3>\n      <p>{d}</p>\n      " for t, d in _cd["blocks"]
            )
            cond_deep_html = f'''
<section class="section">
  <div class="wrap">
    <div class="prose reveal">
      <h2>{_cd["h2"]}</h2>
      <p>{_cd["intro"]}</p>
      {_cb}{_cd.get("extra", "")}</div>
  </div>
</section>'''

        # Answer-first opener (2026-10-14): a short direct answer above the
        # original intro, on the pages deepened in the GSC deep dive. Pages
        # without one render byte-identical to before.
        answer_html = f'<p>{c["answer"]}</p>\n      ' if c.get("answer") else ""
        treats = "".join(f"<li>{t}</li>" for t in c["treats"])
        # Related-care internal links: primary service + neighboring conditions
        i = cond_slugs.index(slug)
        prev_s, next_s = cond_slugs[i - 1], cond_slugs[(i + 1) % len(cond_slugs)]
        sv, sv_name = svc_for.get(slug, ("physical-therapy", "Physical Therapy"))
        rel_links = (f'<p class="related-links"><strong>Related care:</strong> '
                     f'<a href="../services/{sv}.html">{sv_name}</a> &middot; '
                     f'<a href="{prev_s}.html">{CONDITIONS[prev_s]["name"]}</a> &middot; '
                     f'<a href="{next_s}.html">{CONDITIONS[next_s]["name"]}</a></p>')
        crumbs = f'<div class="crumbs"><a href="/">Home</a> / <a href="index.html">What We Treat</a> / {c["name"]}</div>'
        body = f"""
<main>
{page_hero(c["area"], c["name"], c["lede"], crumbs, cta_href="../contact.html", cta_label="Book an Evaluation")}{blog_link}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      {answer_html}<p>{c["intro"]}</p>
      <h2>Conditions we treat</h2>
      <ul class="check-list">{treats}</ul>
      <h2>Our approach</h2>
      <p>{c["approach"]}</p>
      {rel_links}
      <h2>What to expect at your first visit</h2>
      <p>Your first appointment includes a comprehensive movement-based evaluation, an honest conversation about your goals, and a proposed plan of care — including hands-on treatment that very first day whenever appropriate. We accept most major insurance plans, including Medicare, and our front desk will gladly verify your coverage before you arrive.</p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Start feeling better</h3>
      <p>Serving the Palm Beaches since 1991 — family-owned, with a 4.9★ Google rating.</p>
      <a class="btn btn-coral" href="../contact.html">Book Appointment</a>
      <div class="side-meta">
        <p>Call us directly<br><a href="tel:+15616244263">{PHONE}</a></p>
        <p style="margin-top:0.8rem;">733 US Highway 1, Suite 2A<br>North Palm Beach, FL 33408</p>
      </div>
    </aside>
  </div>
</section>
{cond_deep_html}{appt_form(heading='Get Help With ' + c['name'], sub='Tell us what is going on and our front desk will call you back within one business day.')}
{cta_band(1)}
</main>
"""
        name_plain = c["name"].replace("&amp;", "&")
        title_short = {"post-surgical": "Post-Surgical Rehab", "workers-comp": "Workers' Comp Rehab"}.get(slug, name_plain)
        cond_desc = c["lede"].replace("&amp;", "&")
        if len(cond_desc) <= 115:
            cond_desc += " Family-owned North Palm Beach clinic since 1991."
        cond_bc = breadcrumb_schema([("Home", ""), ("What We Treat", "treatments/index.html"),
                                     (c["name"], f"treatments/{slug}.html")]) + condition_schema(slug, c["name"], c["lede"], sv, sv_name)
        # seo_title/seo_desc override the generic pattern. Added for the pages
        # the 2026-08-08 GSC export shows ranking 5-20 with a ~0% CTR: the
        # position is fine, the snippet is not winning the click. Match the
        # wording people actually search ("treatment", not "relief") so Google
        # bolds it, and spend the description on a reason to pick us.
        write(f"treatments/{slug}.html",
              head(c.get("seo_title") or f"{title_short} in North Palm Beach | First Rehabilitation",
                   c.get("seo_desc") or cond_desc, depth=1, canonical=f"treatments/{slug}.html",
                   page_type="article", extra_schema=cond_bc)
              + nav(1) + body + footer(1))


# ----------------------------------------------------------------------------
# LOCATION PAGES — genuinely useful area pages served from the NPB clinic
# ----------------------------------------------------------------------------

LOCATIONS = {
    "palm-beach-gardens": {
        "city": "Palm Beach Gardens",
        "deep_eyebrow": "Why Gardens Residents Choose Us",
        # Title/desc retargeted 2026-10-16 (title and meta only; no body words, per
        # CLAUDE.md). Semrush top 10 for "physical therapy palm beach gardens" is
        # exact-match city titles; GSC 28d has it at 67 impr / pos 24.0 here and
        # "orthopedic rehabilitation palm beach gardens fl" at 51 / 11.0.
        "title": "Physical Therapy Palm Beach Gardens FL | First Rehab",
        "desc": "Physical therapy and orthopedic rehab for Palm Beach Gardens, minutes south on US-1, plus OT and certified hand therapy. Medicare accepted. 561-624-4263.",
        "h1": "Serving <em class='accent'>Palm Beach Gardens</em>",
        "kicker": "Palm Beach Gardens",
        "lede": "Complete outpatient rehabilitation for Gardens residents — physical therapy, occupational therapy, certified hand therapy, and an on-site wellness gym, minutes away in North Palm Beach.",
        "deep": True,
        "local": [
            ("Hand therapy and active-lifestyle rehab for the Gardens", [
                "Palm Beach Gardens has more golf courses per square mile than almost anywhere in the county, and it shows in who comes through our door — golfer's elbow, tennis elbow, and overuse wrist and shoulder pain from a game people intend to keep playing, not give up. Laura Drumm, CHT leads one of the area's few certified hand therapy programs, with custom splints fabricated in-clinic rather than ordered from a catalog.",
                "We also see a steady number of Gardens patients for occupational therapy — help relearning or adapting the daily activities of independent living after a fall, a stroke, or a joint replacement, led by a founder who is himself an occupational therapist. Read more about <a href=\"../treatments/hand-wrist.html\">hand and wrist therapy</a> or <a href=\"../services/occupational-therapy.html\">occupational therapy</a>.",
            ]),
            # Added 2026-09-18 from the 90-day query pull: Palm Beach Gardens
            # carries 1,626 impressions against 5 clicks across 70 queries, and
            # the page was invisible for terms we genuinely serve — "ergonomic
            # evaluation in palm beach gardens" at position 62.9, "physiotherapy
            # in palm beach gardens" at 23.4, "orthopedic rehabilitation palm
            # beach gardens fl" at 36.0, "manual therapy palm beach gardens" at
            # 21.4. Gardens borders North Palm Beach, so unlike West Palm Beach
            # this is a proximity fight we can actually win.
            #
            # DELIBERATELY NOT TARGETED: "physical therapy at home palm beach
            # gardens" and its variants (238 impressions combined). That is home
            # health care. We do not provide it, the nearest competitor does, and
            # the page will not imply otherwise.
            ("Orthopedic rehabilitation, manual therapy and ergonomic assessment", [
                "Physiotherapy and physical therapy are the same profession under two names, and Gardens patients search for both. Whichever term you use, orthopedic rehabilitation is the core of what we do: recovery after joint replacement, rotator cuff repair and spinal surgery, alongside the chronic back, neck and joint pain that has not resolved on its own. Sessions are hands-on and therapist-led, with manual therapy used where it is the right tool rather than as a default.",
                "Ergonomic and workstation assessment sits on the occupational therapy side of the clinic, and it is one of the more useful things we do for working Gardens residents. If the same wrist, neck or shoulder pain keeps returning every time you go back to your desk, the fastest route out is often changing how the task is set up rather than waiting on strength to return. Call 561-624-4263 and our front desk will check whether an assessment is covered under your plan before you come in.",
            ]),
        ],
        "drive": "Our clinic sits at 733 US Highway 1, Suite 2A in North Palm Beach — directly south of Palm Beach Gardens, a straight shot down US-1 or Alternate A1A. Most Gardens neighborhoods reach us in one short drive without touching I-95, and our front desk at 561-624-4263 will happily talk you through directions and parking before your first visit.",
        "conditions": ["back-pain", "neck-pain", "shoulder-pain", "knee-pain", "hand-wrist", "post-surgical"],
    },
    "jupiter": {
        "city": "Jupiter",
        "title": "Physical Therapy Jupiter FL | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for Jupiter residents — an easy drive south on US-1 or I-95 to North Palm Beach.",
        "h1": "Serving <em class='accent'>Jupiter</em>",
        "kicker": "Jupiter",
        "lede": "Jupiter residents choose First Rehabilitation for care no single-service clinic can match — an easy drive south on US-1 or I-95.",
        "deep": False,
        "drive": "From Jupiter, we're a straightforward drive south — US-1 through Juno Beach, or I-95 to Northlake Boulevard — to 733 US Highway 1, Suite 2A, North Palm Beach. Call 561-624-4263 and our front desk will point you right to the door.",
        "conditions": ["back-pain", "shoulder-pain", "knee-pain", "hand-wrist"],
    },
    "tequesta": {
        "city": "Tequesta",
        "title": "Physical Therapy Clinic in Tequesta FL | First Rehab",
        "desc": "Physical therapists serving the Village of Tequesta — physical and occupational therapy plus certified hand therapy, one-on-one, at our North Palm Beach clinic.",
        "h1": "Serving <em class='accent'>Tequesta</em>",
        "kicker": "Tequesta",
        "lede": "From the Village of Tequesta, our family-owned clinic is a simple drive south — and the depth of care under one roof makes the trip worth it.",
        "deep": True,
        "deep_eyebrow": "Why Tequesta Residents Choose Us",
        "local": [
            ("Physical therapists serving the Village of Tequesta", [
                "Tequesta patients have plenty of physical therapy clinics closer to home. The ones who make the drive south usually do it for a specific reason: they want the same therapist every visit, and they want physical therapy, occupational therapy, and certified hand therapy available in one place instead of being referred around.",
                "Every session here is therapist-led and one-on-one. You are not handed to an aide with a printed exercise sheet, and you are not sharing your therapist with three other patients on the hour.",
            ]),
        ],
        "drive": "From Tequesta, follow US-1 south through Jupiter and Juno Beach straight to our door at 733 US Highway 1, Suite 2A, North Palm Beach — or take I-95 to Northlake Boulevard. Call 561-624-4263 and our front desk will talk you through directions and parking.",
        "conditions": ["back-pain", "shoulder-pain", "hip-pain", "post-surgical"],
    },
    "lake-park": {
        "city": "Lake Park",
        "title": "Physical Therapy Lake Park FL | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for Lake Park — we're your next-door neighbor on US-1 in North Palm Beach. Since 1991.",
        "h1": "Serving <em class='accent'>Lake Park</em>",
        "kicker": "Lake Park",
        "lede": "Lake Park is right next door — our clinic sits just up US-1 in North Palm Beach, which makes consistent therapy attendance genuinely easy.",
        "deep": False,
        "drive": "Lake Park borders North Palm Beach, so our clinic at 733 US Highway 1, Suite 2A is essentially your neighborhood clinic — straight up US-1. Call 561-624-4263 for directions and parking guidance.",
        "conditions": ["back-pain", "knee-pain", "workers-comp", "auto-accident"],
    },
    "palm-beach": {
        "city": "Palm Beach",
        "title": "Physical Therapy for Palm Beach, FL | First Rehabilitation",
        "desc": "Physical, occupational and certified hand therapy for Palm Beach residents, minutes north on US-1. Named therapists, one-on-one care, Medicare accepted.",
        "h1": "Serving <em class='accent'>Palm Beach</em>",
        "kicker": "Palm Beach",
        "lede": "Palm Beach residents expect care that is personal, unhurried, and expert. That is exactly how this clinic has run since 1991 — one-on-one, hands-on, and led by the founder.",
        "deep": False,
        "local": [
            ("Post-surgical rehab and hand therapy for Palm Beach", [
                "Joint replacements, rotator cuff repairs, and hand or wrist surgery bring a steady stream of Palm Beach patients across the bridge to us — usually on a surgeon's referral, and usually because they want the same therapist for every visit rather than whoever is free that hour. Post-surgical protocols are exact for a reason, and we follow the surgeon's timeline closely while adjusting pace to how you're actually healing.",
                "Certified hand therapy is its own specialty for a reason: Laura Drumm, CHT, holds the credential hand surgeons look for post-op, and splints are fabricated in-clinic rather than ordered from a catalog. You can read more about <a href=\"../treatments/post-surgical.html\">post-surgical rehabilitation</a> or <a href=\"../treatments/hip-pain.html\">hip pain treatment</a>.",
            ]),
        ],
        "drive": "From the island, cross to the mainland and head north on US-1 to 733 US Highway 1, Suite 2A, North Palm Beach. Our front desk at 561-624-4263 will gladly walk you through the easiest route and parking before your first visit.",
        "conditions": ["post-surgical", "hip-pain", "hand-wrist", "back-pain"],
    },
    "west-palm-beach": {
        "city": "West Palm Beach",
        # Retargeted 2026-09-18. This is the highest-impression location page on
        # the site (1,810 impressions in the 28 days to 2026-09-15) and it was
        # converting at 0.11% from position 19.6, because the title chased
        # "physical therapy west palm beach" — a term owned by a three-clinic
        # competitor with a physical West Palm Beach address and 155 Google
        # reviews. Proximity and review count decide that query and we have
        # neither, so the page was fighting where it cannot win.
        #
        # The 90-day query pull found what it CAN win: 751 impressions and zero
        # clicks across occupational-therapy queries, nearly all West Palm Beach
        # ("physical and occupational therapy west palm beach" 150 impr at pos
        # 32.9, "occupational therapy at home west palm beach" 127 at 29.0,
        # "occupational therapist 33401" 72 at 35.4), plus "hand pain treatment
        # west palm beach" at 224 impr / pos 18.2. That competitor is staffed by
        # PTs and PTAs and offers neither OT nor hand therapy, so this is demand
        # in their own city that they structurally cannot answer — a CHT is
        # roughly three years and a national exam away for anyone starting now.
        #
        # So the title front-loads occupational and hand therapy while the h1,
        # lede and body keep physical therapy. Expect reported impressions to
        # FALL and clicks to rise; the lost impressions were converting at 0.11%.
        "title": "Occupational & Hand Therapy West Palm Beach | First Rehab",
        "desc": "Occupational therapy, certified hand therapy and physical therapy for West Palm Beach, north on US-1 or I-95. Family-owned since 1991, Medicare accepted. 561-624-4263.",
        "h1": "Serving <em class='accent'>West Palm Beach</em>",
        "kicker": "West Palm Beach",
        "lede": "West Palm Beach has no shortage of physical therapy clinics. Patients drive north to us for what most of them don't staff: occupational therapy, a Certified Hand Therapist, and a wellness gym under one family-owned roof.",
        "deep": True,
        "deep_eyebrow": "Why West Palm Beach Patients Drive North",
        "local": [
            ("Occupational therapy for West Palm Beach", [
                "Most clinics within West Palm Beach are staffed for physical therapy: physical therapists and physical therapist assistants, treating movement, strength and pain. That is genuinely what many people need. But if your problem is that you cannot dress yourself, manage a kitchen, or perform the specific tasks your job requires, the discipline you are looking for is occupational therapy, and it is a different credential with different training.",
                "Our occupational therapy program is led by our founder, David Kashuba, Ph.D., who is himself an occupational therapist and has been treating patients since 1991, alongside Joan &ldquo;Joni&rdquo; Janik, OTD. That matters on a practical level: the person setting your plan has been doing this work for over three decades, not reading it off a protocol sheet. Read more about our <a href=\"../services/occupational-therapy.html\">occupational therapy program</a>.",
                "West Palm Beach also sends us a different mix than our smaller neighbouring towns — more work injuries, more auto accident referrals, and more people who need to get back to one specific job rather than to general daily activity. For workers' compensation and auto accident cases we work directly with your adjuster or attorney's office on documentation, and treatment is built around what your case actually has to demonstrate. You can read more about our <a href=\"../treatments/workers-comp.html\">workers' comp program</a> or <a href=\"../treatments/auto-accident.html\">auto accident physical therapy</a>.",
            ]),
            ("Certified hand therapy, worth the drive north", [
                "Certified hand therapy is the other reason West Palm Beach patients make the trip. A Certified Hand Therapist has completed thousands of hours of upper-extremity practice plus a rigorous national examination, and it is the credential area hand surgeons look for when they refer a post-operative patient. Laura Drumm, CHT leads our program, and custom splints and orthoses are fabricated here in the clinic rather than ordered from a catalogue.",
                "It is a genuinely scarce specialty in Palm Beach County, which is why patients travel for it from across the county rather than choosing whichever clinic is closest. If you have hand or wrist pain, are recovering from hand surgery, or have been told you need a custom splint, call 561-624-4263 and our front desk will tell you plainly whether we are the right fit. Read more about our <a href=\"../services/hand-therapy.html\">certified hand therapist</a> or <a href=\"../treatments/hand-wrist.html\">hand and wrist treatment</a>.",
            ]),
        ],
        "drive": "From West Palm Beach, head north on US-1 or take I-95 to Northlake Boulevard; we're at 733 US Highway 1, Suite 2A in North Palm Beach. Most downtown and 33401 addresses reach us in one straight drive up US-1. Call 561-624-4263 and our front desk will point you right to the door.",
        "conditions": ["hand-wrist", "post-surgical", "workers-comp", "auto-accident", "back-pain", "neck-pain"],
    },
    "riviera-beach": {
        "city": "Riviera Beach",
        "title": "Physical Therapy Riviera Beach FL | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for Riviera Beach and Singer Island — a short drive north on US-1 to North Palm Beach.",
        "h1": "Serving <em class='accent'>Riviera Beach</em>",
        "kicker": "Riviera Beach",
        "lede": "From Riviera Beach and Singer Island, our family-owned clinic is a short, simple drive north — with the kind of one-on-one attention that keeps patients coming back.",
        "deep": False,
        "drive": "From Riviera Beach, head north on US-1 past Lake Park to 733 US Highway 1, Suite 2A, North Palm Beach; from Singer Island, cross the Blue Heron bridge and turn north. Call 561-624-4263 for directions and parking guidance.",
        "conditions": ["knee-pain", "shoulder-pain", "workers-comp", "foot-pain"],
    },
    "juno-beach": {
        "city": "Juno Beach",
        "title": "Neck Pain Therapy Juno Beach & Juno Ridge FL | First Rehab",
        "desc": "Neck pain, back pain, hip and hand therapy for Juno Beach and Juno Ridge, FL. One-on-one care at our North Palm Beach clinic, just south on US-1.",
        "h1": "Serving <em class='accent'>Juno Beach</em>",
        "kicker": "Juno Beach &amp; Juno Ridge",
        "lede": "Juno Beach and Juno Ridge neighbors are practically next door — our family-owned clinic is just down US-1 in North Palm Beach.",
        "deep": True,
        "deep_eyebrow": "Why Juno Beach Residents Choose Us",
        "drive": "Juno Beach and Juno Ridge sit immediately north of us on US-1 — our clinic at 733 US Highway 1, Suite 2A, North Palm Beach is just a few minutes down the road. Call 561-624-4263 for directions and parking guidance.",
        "local": [
            ("Neck pain care for Juno Beach and Juno Ridge", [
                "Neck pain is one of the most common reasons neighbors from Juno Beach and Juno Ridge first call us. Sometimes it builds slowly over years at a desk; sometimes it arrives overnight after a collision on US-1. Either way it tends to respond well to skilled, hands-on physical therapy.",
                "Rather than treating the sore spot in isolation, we identify the joints, muscles, and postural patterns actually driving your symptoms. Care usually combines gentle manual therapy and joint mobilization, deep neck flexor and postural strengthening, and practical coaching on how you sit, drive, and sleep. Most patients notice meaningful change within the first few weeks of consistent care.",
                'We treat chronic neck stiffness, whiplash after an auto accident, cervical radiculopathy (a pinched nerve), tension and postural neck pain, and pain that radiates into the shoulder or arm. You can read more on our <a href="../treatments/neck-pain.html">neck pain relief page</a>, or about <a href="../treatments/auto-accident.html">auto accident recovery</a> if a crash is what brought you here.',
            ]),
            ("One clinic, four kinds of care", [
                "Because Juno Beach and Juno Ridge are only minutes away, patients often keep coming back to us as their needs change — physical therapy for the neck, occupational therapy when daily tasks are the problem, a Certified Hand Therapist for the wrist and hand, and the wellness gym once formal therapy ends. Same building, same team, same records.",
            ]),
        ],
        "conditions": ["neck-pain", "back-pain", "auto-accident", "hip-pain", "foot-pain", "post-surgical"],
    },
}

def build_locations():
    import json as _json
    for slug, L in LOCATIONS.items():
        crumbs = f'<div class="crumbs"><a href="/">Home</a> / {L["city"]}</div>'
        cond_links = " &middot; ".join(
            f'<a href="../treatments/{c}.html">{CONDITIONS[c]["name"]}</a>' for c in L["conditions"]
        )
        team_cards = "".join(
            f'<div class="svc-feature reveal"><span class="svc-feature-num">{i+1:02d}</span>'
            f'<div><h3>{t["name"]}</h3><p><strong>{t["role"]}.</strong> {t["blurb"]}</p></div></div>'
            for i, t in enumerate(TEAM) if L["deep"] or i < 3
        )
        # Optional city-specific prose, rendered under "Getting here".
        # Shape: [(heading, [paragraph, ...]), ...]
        local_block = "".join(
            f'      <h2>{h}</h2>\n' + "".join(f'      <p>{p}</p>\n' for p in paras)
            for h, paras in L.get("local", [])
        )
        deep_extra = ""
        if L["deep"]:
            # Was hardcoded to Palm Beach Gardens; any other deep city would have
            # rendered Gardens copy under its own name.
            deep_eyebrow = L.get("deep_eyebrow", f'Why {L["city"]} Residents Choose Us')
            deep_extra = f'''
<section class="section on-cream">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">{deep_eyebrow}</span>
      <h2>Care No PT-Only Clinic <em class="accent">Can Offer</em></h2>
      <p class="lede">Plenty of clinics offer physical therapy. Very few pair it with occupational therapy, a Certified Hand Therapist, and a wellness gym under the same roof.</p>
    </div>
    <div class="svc-feature-grid">
      <div class="svc-feature reveal"><span class="svc-feature-num">01</span><div><h3>Occupational Therapy</h3><p>When the goal isn't just moving better but living better — dressing, cooking, working — our OTs restore the daily activities that matter. Led by a founder who is himself an occupational therapist.</p></div></div>
      <div class="svc-feature reveal"><span class="svc-feature-num">02</span><div><h3>Certified Hand Therapy</h3><p>Laura Drumm, CHT leads one of the area's few certified hand therapy programs — the credential hand surgeons look for post-op — with custom splints fabricated in-clinic.</p></div></div>
      <div class="svc-feature reveal"><span class="svc-feature-num">03</span><div><h3>On-Site Wellness Gym</h3><p>Recovery shouldn't end at discharge. Keep training in our clinic gym with a team that already knows your history.</p></div></div>
      <div class="svc-feature reveal"><span class="svc-feature-num">04</span><div><h3>One-on-One Since 1991</h3><p>Family-owned for over three decades, with hands-on, therapist-led sessions — never a hand-off to a tech and a printed sheet.</p></div></div>
    </div>
  </div>
</section>'''
        body = f"""
<main>
{page_hero(L["kicker"], L["h1"], L["lede"], crumbs, cta_href="../contact.html")}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p>{L["lede"]} We accept Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network (VACCN), workers' compensation, and self-pay — and our front desk verifies your coverage before your first visit.</p>
      <h2>Getting here from {L["city"]}</h2>
      <p>{L["drive"]}</p>
{local_block}      <h2>Our team, by name</h2>
      <p>Unlike clinics that list no practitioners at all, we're proud to tell you exactly who will guide your recovery: David Kashuba, Ph.D., OTR (CEO &amp; Occupational Therapist, treating patients since 1991), Kayla Dorsey, PT, DPT and Logan Van Sant, PT, DPT (Physical Therapists), Joan &ldquo;Joni&rdquo; Janik, OTD (Occupational Therapist), and Laura Drumm, MS, OTR/L, CHT (Certified Hand Therapist). Meet everyone on our <a href="../about.html">About page</a>.</p>
      <p class="related-links"><strong>Common conditions we treat for {L["city"]} patients:</strong> {cond_links}</p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Visit us</h3>
      <p>733 US Highway 1, Suite 2A<br>North Palm Beach, FL 33408</p>
      <p style="margin-top:0.6rem;">Monday&ndash;Friday, 8:00 AM &ndash; 5:30 PM<br>Saturday, 8:00 AM &ndash; 12:30 PM</p>
      <a class="btn btn-coral" href="../contact.html">Book Appointment</a>
      <div class="side-meta">
        <p>Call us directly<br><a href="tel:+15616244263">{PHONE}</a></p>
      </div>
    </aside>
  </div>
</section>
{deep_extra}
<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Everything Under One Roof</span>
      <h2>Four Services, <em class="accent">One Clinic</em></h2>
    </div>
    <p class="related-links reveal"><strong>Explore our care:</strong> <a href="../services/physical-therapy.html">Physical Therapy</a> &middot; <a href="../services/occupational-therapy.html">Occupational Therapy</a> &middot; <a href="../services/hand-therapy.html">Certified Hand Therapy</a> &middot; <a href="../services/wellness.html">Wellness &amp; Gym</a> &middot; <a href="../faq.html">Read our FAQ</a></p>
  </div>
</section>
{appt_form(heading='Book From ' + L['city'], sub='Tell us what you need and our front desk will call you back within one business day.')}
{cta_band(1)}
</main>
"""
        svc_ld = {"@context": "https://schema.org", "@type": "Service",
                  "@id": f"https://www.firstrehabnpb.com/locations/{slug}.html#service",
                  "serviceType": "Outpatient rehabilitation (physical, occupational, and certified hand therapy)",
                  "provider": ORG_REF,
                  "areaServed": {"@type": "City", "name": L["city"]}}
        loc_schema = '<script type="application/ld+json">' + _json.dumps(svc_ld, ensure_ascii=False) + '</script>\n'
        write(f"locations/{slug}.html",
              head(L["title"], L["desc"], depth=1, canonical=f"locations/{slug}.html",
                   extra_schema=loc_schema + breadcrumb_schema([("Home", ""), (L["city"], f"locations/{slug}.html")]))
              + nav(1) + body + footer(1))

# ----------------------------------------------------------------------------
# ABOUT / PODCAST / FAQ / CONTACT
# ----------------------------------------------------------------------------

# Team roster. `blurb` is the short card text that has always shown on the About
# page. `bio` / `specialties` / `fun_fact` are the EXPANDED profile fields the
# owner is collecting from each person — leave them empty ("" / []) until the
# real content arrives. A card only becomes expandable when `bio` is non-empty;
# with an empty bio it renders exactly like the original static card. NEVER
# invent bios, specialties, or fun facts here.
TEAM = [
    {"name": "David Kashuba, Ph.D., OTR", "slug": "david-kashuba", "role": "CEO &amp; Occupational Therapist",
     "blurb": "Founded First Rehabilitation in 1991 and still treats patients hands-on every day — leading the clinic's comprehensive, high-end approach to rehabilitation across three decades and tens of thousands of recoveries.",
     "img": "david.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Nick Kashuba", "slug": "nick-kashuba", "role": "Chief Operating Officer",
     "blurb": "Second-generation leadership keeping the clinic's family-owned values — and its promise that our people make the difference — at the center of everything we do.",
     "img": "nick.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Logan Van Sant, PT, DPT", "slug": "logan-van-sant", "role": "Physical Therapist",
     "blurb": "A Doctor of Physical Therapy dedicated to helping patients move and feel their best, with hands-on, one-on-one care.",
     "img": "logan.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Kayla Dorsey, PT, DPT", "slug": "kayla-dorsey", "role": "Physical Therapist",
     "blurb": "A Doctor of Physical Therapy with over a decade of extensive clinical experience in personalized, hands-on care.",
     "img": "kayla.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Joan &ldquo;Joni&rdquo; Janik, OTD", "slug": "joni-janik", "legal_name": "Joan Janik", "alt_name": "Joni Janik", "role": "Occupational Therapist",
     "blurb": "A Doctor of Occupational Therapy who helps patients reclaim the daily activities that matter most, restoring independence, confidence, and quality of life.",
     "img": "joni.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Laura Drumm, MS, OTR/L, CHT, CLT", "slug": "laura-drumm", "role": "Certified Hand Therapist",
     "blurb": "Leads our certified hand therapy program with surgical-grade precision — from custom splinting to post-operative tendon protocols.",
     "img": "laura.jpg", "bio": "", "specialties": [], "fun_fact": ""},
]

def build_about():
    # A card is expandable ONLY when the person's long-form bio exists.
    # Empty bio -> the exact static card the page has always shown, with no
    # expand affordance. Filling in TEAM[n]["bio"] flips the card on rebuild.
    def _team_card(i, t):
        slug = t["slug"]
        base = f'''<div class="team-photo">
          {photo("team-" + t["img"][:-4], sizes="(max-width:768px) 46vw, 300px", ratio="4/5")}
        </div>
        <h3>{t["name"]}</h3><div class="role">{t["role"]}</div><p>{t["blurb"]}</p>'''
        # /about is our best page in search (position 5.3, 4.03% CTR) and the
        # second most visited, and someone reading a specific clinician is the
        # highest-intent visitor we get — the page had no way to act on that.
        # A quiet named text link, in the slot the expandable card already
        # reserves for "Read full profile", so it never fights the grid.
        first = (t.get("alt_name") or t["name"]).split(",")[0].split()[0]
        book = (f'<a class="tc-book" href="contact.html">Book with {first} '
                f'<span class="arr">&rarr;</span></a>')
        if not t["bio"]:
            return f'<div class="team-card reveal d{i%3+1}">{base}{book}</div>'
        spec = ("".join(f'<li>{s}</li>' for s in t["specialties"]))
        spec_html = f'<h4>Specialties</h4><ul class="tp-specs">{spec}</ul>' if spec else ""
        fun_html = f'<p class="tp-fun"><strong>Fun fact:</strong> {t["fun_fact"]}</p>' if t["fun_fact"] else ""
        # Someone who has opened one clinician's profile and read to the bottom
        # is the highest-intent visitor on the site — /about is our best page in
        # search and the second most visited. The ask goes here, named, rather
        # than on all six cards where it would just compete with itself.
        cta_html = f'''<div class="tp-cta">
              <p class="tp-cta-q">Want to work with {first}?</p>
              <div class="tp-cta-act">
                <a class="btn btn-coral" href="contact.html">Book with {first} <span class="arr">&rarr;</span></a>
                <a class="tp-cta-call" href="tel:+15616244263">or call {PHONE}</a>
              </div>
            </div>'''
        return f'''<button type="button" class="team-card team-card-open reveal d{i%3+1}" data-profile="tp-{slug}" aria-haspopup="dialog">
        {base}<span class="tp-more" aria-hidden="true">Read full profile &rarr;</span></button>
        <dialog class="team-profile" id="tp-{slug}" aria-label="Profile: {t["name"]}">
          <div class="tp-inner">
            <button type="button" class="tp-close" aria-label="Close profile">&#10005;</button>
            <div class="tp-head">
              {photo("team-" + t["img"][:-4], sizes="120px", alt="")}
              <div><h3>{t["name"]}</h3><div class="role">{t["role"]}</div></div>
            </div>
            <div class="tp-body"><p>{t["bio"]}</p>{spec_html}{fun_html}</div>
            {cta_html}
          </div>
        </dialog>'''
    team_html = "".join(_team_card(i, t) for i, t in enumerate(TEAM))
    body = f"""
<main>
{page_hero("Since 1991", "Family-Owned. <em class='accent'>Patient-Devoted.</em>",
  "Three decades of healing the Palm Beaches — built on one founder's vision and carried forward by family.",
  '<div class="crumbs"><a href="/">Home</a> / About</div>')}
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our Story</span>
      <h2>One Vision, <em class="accent">Generations of Care</em></h2>
      <p style="margin-top:1.2rem;">Since 1991, First Rehabilitation of North Palm Beach has been a cornerstone of recovery for the Palm Beaches. Founded by David Kashuba, Ph.D., our mission has always been to provide a comprehensive, high-end approach to rehabilitation — one that heals the body and restores the spirit.</p>
      <p style="margin-top:1rem;">What makes us different is what happens after therapy ends. Our exclusive on-site wellness program means graduation from PT or OT isn't goodbye — it's a transition into lifelong strength, guided by the same team that got you well.</p>
      <!-- Disambiguation (Nick, 2026-10-14): a formerly connected clinic on Burns Rd kept the
           "First Rehab" name, and Google reviews meant for it have landed on our listing. One
           factual sentence, no names, nothing disparaging. Keep it that way. -->
      <p style="margin-top:1rem;font-size:0.95rem;color:var(--muted);">First Rehabilitation of North Palm Beach is an independent, family-owned clinic founded in 1991 by David Kashuba, Ph.D., OTR. We have one location, at 733 US Highway 1, Suite 2A, and are not affiliated with other clinics that use a similar name.</p>
      <div class="stat-row">
        <div><strong data-count="39" data-suffix="+">39+</strong><span>Years of Expertise</span></div>
        <div><strong data-count="180000" data-suffix="+">180,000+</strong><span>Patients Treated</span></div>
        <div><strong>4.9★</strong><span>Google Rating</span></div>
        <div><strong>Est. 1991</strong><span>Family-Owned</span></div>
      </div>
    </div>
    <div class="split-media tilt2 reveal d2">
      {photo("exterior", sizes="(max-width:900px) 92vw, 560px")}
    </div>
  </div>
</section>
<section class="section on-cream">
  <span class="sec-mark" aria-hidden="true" style="top:2rem; right:2vw;">est.<br>'91</span>
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Meet the Team</span>
      <h2>The People Behind <em class="accent">Your Recovery</em></h2>
    </div>
    <div class="team-grid">{team_html}</div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("about.html",
          head("Our Team & Story Since 1991 | First Rehabilitation NPB",
               "Family-owned since 1991. Meet the team behind First Rehabilitation of North Palm Beach — founder David Kashuba, Ph.D., and our therapists.",
               canonical="about.html",
               extra_schema=person_schema() + breadcrumb_schema([("Home", ""), ("About Us", "about.html")]))
          + nav(0) + body + footer(0))

EPISODES = [
    ("Episode 20", "Maria Kendzierski", "&ldquo;How long do you not wanna have cancer?&rdquo; That was her doctor&rsquo;s answer when Maria Kendzierski asked how long she had to keep getting MRIs.<br><br>Maria is Dave&rsquo;s cousin, and she joins Dave and Mike over Zoom from Buffalo for Breast Cancer Awareness Month. She has been diagnosed with breast cancer twice. The first time, in 2015, a yearly mammogram found stage zero lobular carcinoma in situ, followed by five years of tamoxifen.<br><br>Because of that first diagnosis she was screened every six months at Roswell Park, and in 2024 an MRI caught a stage one cancer early. Maria walks through the lumpectomy, eight rounds of chemotherapy that started on her birthday, five weeks of radiation, and ringing the bell after both.<br><br>She also talks about the people she met in the radiation waiting room, why she left most online support groups and stayed away from Dr. Google, the women under 40 she met who were already diagnosed, and why you cannot always feel a tumor yourself. The episode closes with Dave&rsquo;s joke of the week and Maria&rsquo;s reminder to get your mammograms and talk to your own doctor about when to start.", "https://open.spotify.com/episode/2u5XZXbSdyJH73raZVuZ5f", "Listen"),
    ("Episode 19", "Shannon Cake", "&ldquo;I didn&rsquo;t win anything alone. We never do.&rdquo; Dave opens by adding up every Emmy won by Peter Jennings, Walter Cronkite and Barbara Walters, and by his count Shannon Cake has more on her own: 23, plus an Edward R. Murrow Award. Shannon now hosts News Now on Newsmax 2, weekdays from 9 to 10, after decades as an investigative reporter in West Palm Beach.<br><br>Her path started with her father, who served with an armored cavalry division in Germany before moving into diplomatic and intelligence work in Singapore and Hong Kong, with China as his specialty. Shannon began in radio at the NPR affiliate at the University of Alabama, then moved into consumer investigations. A friend, former state attorney Dave Aronberg, gave her the line that kept her there: one story in an evening can sometimes do more than a lawmaker does in a career.<br><br>She tells her father&rsquo;s advice for negotiating in China: bring your own interpreter, or check your numbers at the end of the meeting. Then the talk turns to headaches. Dave is careful about the limits: physical therapy cannot stop a migraine, which he calls a systemic problem, but it can work on the triggers, and he says staying fit is key to reducing headaches.<br><br>Shannon&rsquo;s day starts around 4:30, with a 5:30 editorial meeting and air at 9, so her rule is to work out first thing, because it is the hour least likely to be interrupted. Thirty minutes on the bike, then push ups, sit ups or lifting with one of her two teenage boys whenever she can. Mike&rsquo;s version: it is not a matter of time, it is a matter of priority.<br><br>Shannon and Dave first met when she tore her rotator cuff and came to First Rehabilitation as a patient. While rehabbing she trained on the program people call the Captain Kerry workout, and Dave sets the record straight on whose workout it really is, while Mike brings up Hydrox and Oreo. The episode closes with Dave&rsquo;s joke about two antennas and a reminder to go vote.", "https://open.spotify.com/episode/3i8rIgaoTZ1MlhZtLU4Lz6", "Listen"),
    ("Episode 18", "Elyse Marrone and Danielle Armstrong", "&ldquo;I want to be healthy, healthy, healthy, dead.&rdquo; Following last week&rsquo;s screening episode with Dr. Don Goodwin, Dave and Mike turn to what you can control. Elyse Marrone is a registered dietitian, functionally and integratively trained, who sees patients in Jupiter. Danielle Armstrong owns Pilates Life on Northlake in Palm Beach Gardens. Between them they cover food, movement and recovery before, during and after a breast cancer diagnosis.<br><br>Elyse calls it the triple HD plan, and it rests on the seven pillars of health she works through with every patient: food first, exercise, sleep, stress management, supplementation, hydration and community. After a diagnosis the first place she looks is the gut, because we all get cancer all the time and our immune system fights it, and she puts 80 to 90% of that immune system in the gut. Dave adds a number of his own: 30% of postmenopausal women, he says, could avoid breast cancer through diet and exercise alone.<br><br>Danielle says that this year in particular she has worked with a lot of women in their mid 60s to mid 70s through diagnosis and treatment, keeping them active and moving. Mike ties it to everyday life: balance, muscle strength, carrying the garbage out, getting in and out of the bathtub. Danielle trained in the line of Joseph Pilates through Romana Kryzanowska, one of his direct disciples, and now works with Juno Beach&rsquo;s Lolita San Miguel, the last living elder who trained with him, who turned 92 on October 9.<br><br>Then the story of Eve Gentry, a dancer who had a radical mastectomy in the 1950s and was told she would never dance or do Pilates again. Joseph Pilates worked with her for a year until her full range of motion came back. When he took film of her exercises to a hospital in New York, they did not believe it, so it was filmed again. The hospital still turned him away, Danielle says, because he did not have the alphabet soup behind his name.<br><br>The episode closes on sleep: deep sleep, the wearables that track it, and one easy habit from Elyse, blue light blocker glasses from 8 o&rsquo;clock in the evening, which she says help the body start producing melatonin so you fall asleep faster. Along the way Dave shares how a Polish family makes Brussels sprouts, fried in bacon grease with bacon. Reach Elyse at 561-252-7857 or thenutritioninstitute.org, and Pilates Life at 561-288-8151.", "https://open.spotify.com/episode/0ko5IbgL0d2LSR3zLLApAt", "Listen"),
    ("Episode 17", "Dr. Donald Goodwin, MD", "&ldquo;Our job is to find it as small and early as possible, because the smaller the lesion, the earlier the stage, the better the prognosis.&rdquo; Breast Cancer Awareness Month opens with radiologist Dr. Don Goodwin, who has been reading images for more than 50 years. He and Dave go back decades; in 2007 they built a building together, back when they were the young guys.<br><br>Screening advice depends on who you ask. The US Preventive Services Task Force recommended starting at 50 and screening every other year until last year, when it moved the start to 40 and kept the two year interval. The American College of Radiology, the American College of Surgeons and the American Cancer Society have long said 40 and every year. Dr. Goodwin sides with annual screening, noting that incidence in women under 50 has risen about 1.5% a year over the last decade.<br><br>Dense breast tissue is where a mammogram struggles, and he says it can miss up to 60% of cancers under 10mm. Ultrasound adds detection on top, and MRI adds more: in one study of BRCA positive women, mammography found 15 cancers per thousand, ultrasound another 7, and MRI 42. Because MRI is expensive and needs an IV, it is reserved for women above a 20% lifetime risk.<br><br>He puts the radiation from a 3D mammogram at about 0.4 millisieverts, roughly two months of everyday background exposure or one flight across the country. 3D imaging has also cut callback rates from 10 to 12% to around 6 to 8%, and core needle biopsy means most benign findings no longer need an operating room. A stage 1 cancer now carries a five year survival of about 98 to 99%.<br><br>Men get breast cancer too, at roughly one in a thousand against about 12% of women, and Mike names a few who went public with it. They also cover the conflicting research on hormone replacement therapy and why lumps or tenderness in men deserve a look. Dr. Goodwin practices with TGH Imaging, formerly Palm Beach Radiology, and can be reached at 561-841-8588.", "https://open.spotify.com/episode/35csD2IOACfJhxqCHsCYjN", "Listen"),
    ("Episode 16", "Dr. Matt Butler, MD", "&ldquo;That&rsquo;s how we all interact with our environment&hellip; something that people take for granted until it starts bothering them.&rdquo; Dr. Matt Butler is a fellowship trained hand and upper extremity orthopedic surgeon with HSS, and in his words he takes care of people&rsquo;s arms, mostly the elbow, wrist and hand. He has practiced locally for more than three years, and he and Dave send patients back and forth.<br><br>Tennis elbow, he says, is almost a rite of passage in middle age: the tendon that anchors the forearm muscles to the bone starts to fray, and most people who get it do not play tennis. Most cases settle, and the ones that land in his office first usually get sent to Dave, who he says fixes about 90% of them. For the stubborn rest, he now adds a collagen patch, first developed for the shoulder, when he cleans out the worn tendon.<br><br>Dave walks through what that 90% looks like in the clinic: active release technique, blood flow restriction training, and dynamic cupping, sometimes with an actual sink plunger. Mike is the proof, since Dave treated his elbow before the show and he says it has not hurt since.<br><br>They also get into the elbow problems now showing up in young pitchers. Kids play one sport year round and throw harder than ever, so Dr. Butler sees growth plate stress fractures and has to tell tendon strain apart from a UCL tear, the Tommy John ligament, sometimes with a stress view MRI developed at HSS. Dave adds what a dropped shoulder does to a young thrower&rsquo;s elbow.<br><br>The reason Dave booked him is basal thumb arthritis, which almost every woman and many men develop. The standard surgery removes the trapezium bone, then means six to eight weeks immobilized and months of rehab, and pinch strength never fully returns. Dr. Butler now offers a joint replacement for the thumb, built like a dual mobility hip, used in Europe for about 15 years and newly FDA cleared. His office is at 561-657-4670.", "https://open.spotify.com/episode/5aTjNCuW0jZjKmenRYQCj0", "Listen"),
    ("Episode 15", "Susan Mann", "&ldquo;They can&rsquo;t be gifted if they can&rsquo;t do their schoolwork.&rdquo; Every teacher told Susan Mann her two children were gifted. Every test put them at the bottom of the scale, and nobody could explain the gap. Susan is a retired San Francisco police officer, not a clinician, and she went looking for the answer anyway.<br><br>It turned out to be auditory processing disorder and visual processing disorder. Their hearing and their vision were fine &mdash; the brain was not getting the message. As Dr. Leah Light, the audiologist who finally named it, put it to her: the eyes and the ears are only the messengers.<br><br>&ldquo;I put everything on the line,&rdquo; Susan says. Both children retested off the charts, got into the gifted school here in Palm Beach Gardens, and went on to full academic scholarships at Oxbridge Academy. She now runs Bright Minds Processing so other families do not lose years finding the same answer.<br><br>She and Dave get into why a Palm Beach County psychological education evaluation offers two boxes, ADHD or dyslexia, and cannot diagnose either processing disorder; what the therapy actually involves, which is 16 weeks, one session a week, and exercises five evenings a week at home; and the $30 screening that starts it against roughly $2,400 for the whole course.<br><br>Also in this one: why it is one in four children at any age, the fact that the testing itself comes out of the Australian school system where every child is screened, and the travel basketball team Susan is building in Palm Beach Gardens, coached by retired NBA player Dwayne McClain, where you play only if you keep up the therapy.", "https://open.spotify.com/episode/1edWCeBMgCtMgMUCnjaI4R", "Listen"),
    ("Episode 14", "Dr. Chaim Arlosoroff, M.D.", "&ldquo;These are the injuries that make it to the emergency room&hellip; or as a trauma admission.&rdquo; Orthopedic trauma surgeon Dr. Chaim Arlosoroff, on staff at St. Mary&rsquo;s Medical Center for the past 30 years, joins Dave and Mike for a September conversation about the surge in e-bike injuries he sees firsthand in the Level 1 trauma center and ER.<br><br>The numbers are stark: ER visits for e-bike injuries are up more than 400% nationwide since 2017, and Dr. Arlosoroff&rsquo;s own count for South Florida runs even higher &mdash; Palm Beach County up 130% from 2023 to 2024, Broward up 180%, and Miami-Dade over 500%. About 83% of the injured riders weren&rsquo;t wearing a helmet, and the average age is 13.<br><br>He and Dave walk through the modified &ldquo;governors&rdquo; that let bikes built for 15 to 20 mph hit 50 or 60, the skull fractures and spinal cord injuries that follow, and why they see these as motor vehicle injuries &mdash; riding on sidewalks, against traffic, without helmets &mdash; rather than bicycle accidents.<br><br>Dr. Arlosoroff&rsquo;s path to medicine started at 16, volunteering in a hospital operating room during Israel&rsquo;s 1973 Yom Kippur War, and continued through three years as an Israeli Defense Forces combat medic. He also played professional tennis, reaching a world ranking of 283 in 1981, before a full scholarship brought him to Duke University, where he was later inducted into the Duke Tennis Hall of Fame.<br><br>Dr. Arlosoroff and Dave have been friends for more than 30 years, and their practices &mdash; Dr. Arlosoroff&rsquo;s orthopedic trauma and fracture care, and First Rehabilitation&rsquo;s therapy right across the street &mdash; refer patients back and forth every week.", "https://open.spotify.com/episode/10CHQ7OeGRGXtqQAkTdI8p", "Listen"),
    ("Episode 13", "Captain Kerry Titheradge", "Twenty years ago Dave got a call from a friend&rsquo;s doctor asking whether he would take on a patient who was not on his insurance. That patient is now known worldwide as Captain Kerry from Bravo&rsquo;s Below Deck, and the two have stayed close ever since.<br><br>Dr. Dave Kashuba and Mike McGann catch up with Kerry on the rotator cuff program Dave built him back in the day, since nicknamed the &ldquo;Captain Kerry workout,&rdquo; and how a television producer stumbled onto it and turned it into a bit of a brand.<br><br>They also get into what Kerry does with the platform Below Deck gave him, from a Mental Health Mondays series on his own podcast to helping Dave&rsquo;s Remember Me foundation, which supports families facing early onset dementia.<br><br>Equal parts old friends catching up, and a good story about how one shoulder injury turned into two decades of friendship.", "https://open.spotify.com/episode/6DoHiOTVJLUtKCYNaxqzRi", "Listen"),
    ("Episode 12", "Dr. Michael Leighton, MD", "&ldquo;This is the best operation that&rsquo;s done in orthopedics&hellip; the single best operation that Medicare pays for.&rdquo; Orthopedic surgeon Dr. Michael Leighton — a friend Dave has referred patients to since 1994 — joins Dave and Mike to break down total hip replacement: the anterior versus posterior surgical approach, and why he steers heavier or older patients toward posterior while thinner, younger patients can go either way. <br><br>They cover what actually drives infection risk (under 1&ndash;2% over a lifetime, far lower than most people assume, but higher in smokers, in vapers using nicotine, and in diabetics whose A1C runs above 7.5), why dental hygiene matters before joint surgery, and the six-week window bone needs to grow into a modern non-cemented implant. <br><br>Also: the old dislocation precautions that used to keep patients in traction for a week are mostly gone, prehab isn&rsquo;t one-size-fits-all, and an eye-opening dose of Medicare economics — a single flat payment of $1,162 covers the surgery and 90 days of follow-up care, a number Dave says deserves a lot more attention than it gets.<br><br>Dr. Leighton is an orthopedic surgeon with Palm Beach Orthopedic Institute in Palm Beach Gardens, board certified by the American Board of Orthopaedic Surgery with a subspecialty certification in Orthopaedic Sports Medicine. A former Division I baseball player at Duke, he has practiced in Palm Beach County since 1994, treating Hall of Fame athletes alongside weekend pickleball players, and performs minimally invasive hip replacement (anterior and posterior) and robotic-arm assisted (Mako) knee replacement.", "https://open.spotify.com/episode/2HTkgf8nOXbTrEqrPyzYtL", "Listen"),
    ("Episode 11", "Paul Joyce", "&ldquo;You definitely have to make sure you&rsquo;re getting enough protein.&rdquo; Peptides, GLP-1s and hormone replacement therapy are on everyone&rsquo;s lips and understood by almost nobody, so Dave and Mike brought in Paul Joyce of New Life HRT, a friend of Dave&rsquo;s for 22 years and the man a lot of doctors quietly learn these protocols from before they offer them themselves. <br><br>He explains what a peptide actually is (a short chain of amino acids, usually under 50, of which he counts around 150), where the GLP-1 medicines came from (a gut hormone your body already makes, and the Gila monster version of it that stays around long enough to keep working), and why he began prescribing Ozempic off label for weight loss back in 2017, before the rest of the country caught on. <br><br>The part that matters most to a rehab clinic is what the weight takes with it. &ldquo;Yeah, you lose a lot of muscle,&rdquo; he says, and he is talking about himself as much as his patients: he started at 209 pounds, weighs 153 now, and says he took it too far. <br><br>Dave&rsquo;s warning is the one to write down, that people who are not monitored start looking frail, and that the shot will make you better without making you healthier unless the protein and the strength work come with it. <br><br>They also get into the counterfeit peptide trade, where Paul had six research only websites tested and all six came back with major flaws, from heavy metals to bacteria to a vial sold as retatrutide that turned out to be underdosed semaglutide, plus the fabricated certificates of analysis he was called to testify about in Atlanta.<br><br>Paul Joyce runs New Life HRT, where physicians go to be trained on peptide and hormone replacement protocols. He is also, as of this episode, one of Dave&rsquo;s patients: he has a completely torn rotator cuff, cancelled the shoulder replacement he had scheduled, and explains on air why he is rehabbing it instead.", "https://open.spotify.com/episode/1HXEy4xcDFRk40hwbdQrD5", "Listen"),
    ("Episode 10", "Dr. Zach McVicker, MD", "&ldquo;A lot of times it&rsquo;s causing the back pain, it&rsquo;s causing the groin pain.&rdquo; Plenty of people arrive certain their problem is their back, and the hip turns out to be the thing driving it. <br><br>Orthopedic surgeon Dr. Zach McVicker joins Dave and Mike to explain femoroacetabular impingement in plain English: the two shapes it comes in, the cam lesion where the ball is misshapen (&ldquo;instead of being round, it&rsquo;s more like an oval peg in a round hole&rdquo;) and the pincer lesion where the socket covers too much of it, which skews female and is the harder of the two to repair. <br><br>The labrum, he explains, works like a gasket between two pipes, creating the suction seal that spreads your weight across the whole dome of the joint; lose the seal and the cartilage starts taking pressure it was never meant to take. <br><br>They get into hip dysplasia, the opposite problem, where an underdeveloped socket edge-loads the cartilage and ends in arthritis; who tends to get it, from gymnasts and dancers to marathon runners to the seventy-year-olds playing tennis six days a week down here; and why arthroscopic repair, done early, keeps the hip you were born with along with the proprioception a replacement cannot give back. <br><br>Dave walks through the home program he actually hands patients for a weak gluteus medius, including sit-to-stands with a band above the knees to stop the asymmetrical weight shift, and makes his usual case for doing your homework before you choose a surgeon rather than taking advice from the Publix line.<br><br>Dr. McVicker is board certified by the American Board of Orthopaedic Surgery and fellowship trained in sports medicine at the Cedars Sinai Kerlan Jobe Institute in Los Angeles. He practices with the Paley Orthopedic and Spine Institute in Jupiter and West Palm Beach, focusing on minimally invasive arthroscopic surgery of the hip, knee, shoulder and elbow, and has served as assistant team physician for the Miami Marlins and the Jupiter Hammerheads.", "https://open.spotify.com/episode/6gVRS8Cmqd0263HdZfc37L", "Listen"),
    ("Episode 9", "Dr. Vani Sabesan, MD", "&ldquo;We&rsquo;re really good at fixing rotator cuffs. We&rsquo;re not great at getting them to heal.&rdquo; Orthopaedic shoulder surgeon Dr. Vani Sabesan — the Florida Orthopaedic Society&rsquo;s first female president — joins Dave and Mike for an unusually candid hour about the limits of surgery. <br><br>Roughly 17 million people have a rotator cuff problem, and past 60 it is closer to one in three, so the interesting question is not whether a repair can be done but whether the body will knit it back together. Hence her interest in muscle sparing technique and in biologic scaffolds, and her impatience with six weeks in a sling. <br><br>She is equally blunt about the technology arms race: robots in shoulder and joint surgery are a great marketing tool, but the science has not shown them to be the next panacea. <br><br>Along the way — why she switched to knotless sutures fourteen years ago when it was still heresy, why &ldquo;ninety is the new seventy&rdquo; in Palm Beach, the sixty-year-olds playing competitive pickleball six days a week who just want to be shot up so they can keep going, and the ninety-year-old who still trains six days a week. She has also run 28 marathons herself.", "https://open.spotify.com/episode/5yOVCx7EDEQ6IybU1C6u7i", "Listen"),
    ("Episode 8", "Dr. Ryan Simovitch", "The shoulder is the most mobile joint in the body — and that mobility is exactly why it breaks down. Orthopedic shoulder surgeon Dr. Ryan Simovitch joins Dave and Mike to explain reverse total shoulder replacement in plain English: why the rotator cuff decides which replacement you get, and how reversing the ball and socket restores stability when the cuff can no longer provide it. <br><br>They also dig into the &ldquo;constant warrior&rdquo; problem — the play-every-day crowd who train with no moderation and no preparation until something tears — plus the simple at-home shoulder routine Dave gives patients (wall slides, cross-body stretches, shoulder shrugs, and scapular retractions), the Duke anatomy class that pulled Dr. Simovitch into medicine, and why doing your own research beats taking a recommendation from the water cooler.", "https://open.spotify.com/episode/0iMqbfPeqCYGfoZKbHicdb", "Listen"),
    ("Episode 7", "Dr. Rami Elkhechen, M.D.", "Orthopedic surgery isn't always the answer — and knowing when it is may be the most important call a surgeon makes. Dr. Rami Elkhechen, M.D., a board-certified, fellowship-trained sports medicine orthopedic surgeon, then with Orthopaedic Care Specialists in North Palm Beach and now with NYU Langone Health, joins Dave and Mike to dig into exactly that. <br><br>Trained at NYU School of Medicine with a sports medicine fellowship at New Orleans' Ochsner Sports Medicine Institute — and a former assistant team physician for the Saints and Pelicans — he treats everyone from weekend athletes to trauma patients, with a focus on hip arthroscopy, shoulder surgery, cartilage preservation, and orthobiologics. <br><br>Together they unpack what actually separates a surgical candidate from someone better served by conservative care, why rehab so often decides the outcome, and how patients can take a more active role in their own recovery.", "https://open.spotify.com/episode/1cVdymVweFWtoIRropqKQ7", "Listen"),
    ("Episode 6", "Dr. Richard Weiner, M.D.", "World-renowned orthopedic surgeon Dr. Richard Weiner joins Dave and Mike for a candid conversation about joint replacement, staying active as you age, and what it really takes to get patients moving pain-free again. With more than 35 years in practice and thousands of hip and knee replacements to his name, Dr. Weiner brings a uniquely technical eye to orthopedic care — shaped by his training in both engineering and medicine at the University of Pennsylvania. A must-listen for anyone considering surgery or determined to avoid it.", "https://open.spotify.com/episode/6zhOBEvVnxwH7PvmRAu52e", "Listen"),
    ("Episode 5", "Logan Van Sant, DPT", "Doctor of Physical Therapy Logan Van Sant sits down to share what modern physical therapy really looks like — beyond the stretches and exercises most people expect. Logan digs into how the right movement, at the right time, restores strength and confidence after injury, and why the therapist-patient relationship is at the heart of every successful recovery. A genuine wealth of knowledge from one of the sharp young minds shaping PT today.", "https://open.spotify.com/episode/4HIjJt1f7U7Uv0IJCQnyxr", "Listen"),
    ("Episode 4", "Kayla Dorsey, DPT &amp; Dr. Murray Goldberg, M.D.", "A double-header of expertise. Kayla Dorsey, a Doctor of Physical Therapy with over a decade of hands-on experience, unpacks how personalized, one-on-one care changes recovery outcomes. Then Dr. Murray Goldberg — a board-certified urologist serving Palm Beach County since 1991 — joins to discuss men's health, aging well, and why staying proactive about your body pays off for decades. Two perspectives, one theme: taking ownership of your health.", "https://open.spotify.com/episode/3BRC4CtKqjyOGf1BmJrztj", "Listen"),
    ("Episode 3", "Dr. Timur Urakov, M.D.", "Spine surgery, demystified. Dr. Timur Urakov, Associate Professor of Clinical Medicine at the University of Miami, joins the show to explain how today's spine care has changed — from minimally invasive techniques to the advanced surgical technology now used to treat conditions along the entire spine. He and Dave tackle the questions patients are most afraid to ask about back and neck surgery, and when it is (and isn't) the right call.", "https://open.spotify.com/episode/1d1rzNKiSGdMhHsTHXPBQm", "Listen"),
    ("Episode 2", "Dr. Tom Saylor, M.D.", "The hand is the body's most intricate tool — and repairing it takes a specialist. Hand and upper-extremity surgeon Dr. Tom Saylor joins Dave and Mike to talk about the surgical side of restoring hand function, from carpal tunnel and tendon repairs to complex reconstruction. It's a natural fit for First Rehabilitation, home to a certified hand therapy program, and a fascinating look at how surgeon and therapist work hand-in-hand to bring patients back to full function.", "https://open.spotify.com/episode/1a4jO3BCBrYhYL8KF01hOi", "Listen"),
    ("Episode 1", "Intro to Dave's Background", "The one that started it all. In this first episode, Dr. Dave Kashuba tells his story — how he built First Rehabilitation of North Palm Beach from the ground up in 1991, what four decades and 87,000 patients of his own have taught him about healing, and the philosophy behind the name Pain 2 Power. Co-host Mike McGann draws out the moments that shaped Dave's approach to care, resilience, and why &ldquo;our people make the difference&rdquo; is more than a tagline.", "https://open.spotify.com/episode/70Yn3oyi2YcesDkivraogc", "Listen"),
]

# Episode number -> the slug of its recap post in BLOG_POSTS. Written by /episode-blog.
# EPISODES entries are 5-tuples unpacked positionally in three places, so the link lives
# here instead of becoming a sixth field. An episode with no recap simply has no entry.
# ----------------------------------------------------------------------------
# HOME EXERCISE LIBRARY
# ----------------------------------------------------------------------------
# Dave promised this on air twice (Ep 7: "all the exercises that I've been
# talking about, we're going to put them on our website"; Ep 8: "if you go onto
# my website, there's 5,000 different exercises"). Until 2026-08 the site had
# none, so listeners were being sent somewhere that did not exist.
#
# Every exercise below is one Dave actually prescribed on the show. "ep" records
# which episode, so nothing here is invented and each entry can be checked
# against a transcript on the media/ep{NN}-clips branches. Do not add an exercise
# that Dave has not described on air or approved in writing.
EXERCISES = {
    "shoulder": {
        "name": "Shoulder &amp; Upper Back",
        "lede": "Dave's at-home shoulder set. Most of what we do all day pulls the shoulders forward and inward, so this works the other direction.",
        "items": [
            ("Wall slides", "Stand facing a wall with a towel between your forearms and the wall. Start with both arms bent at 90 degrees in front of you, then slide them all the way up the wall and back down.",
             "3 sets of 10", "Approximates the humerus and stabilizes the subscapularis while it stretches. Dave uses the wall version because it is the same idea as a downward dog without asking a 90 year old to get down on the floor.", "Episode 8"),
            ("Cross-body stretch", "Take your right elbow in your left hand and draw that arm across your body. Hold, then switch sides.",
             "Hold and repeat both sides", "Stretches the posterior capsule at the back of the shoulder.", "Episode 8"),
            ("Shoulder shrugs", "Bring both shoulders straight up toward your ears, then let them down.",
             "3 sets of 10", "Simple, and it keeps the whole shoulder girdle moving.", "Episode 8"),
            ("Scapular retractions", "Draw both shoulders back and try to touch your shoulder blades together behind you.",
             "3 sets of 10", "Works directly against the forward, rounded posture that daily life builds in.", "Episode 8"),
            ("Band rows and extensions", "Anchor a resistance band and pull backward, elbows past your ribs. Then work extensions, drawing the arm behind you.",
             "Build gradually", "Dave's reasoning: everything we do all day is internal rotation, so pulling the other way is the correction. Water bottles work as a substitute, but a proper therapy band is better.", "Episode 8"),
        ],
    },
    "knee": {
        "name": "Knee",
        "lede": "Strong muscles around the knee mean fewer symptoms. All you need is a chair and a small step stool.",
        "items": [
            ("Seated leg extensions", "Sit and scoot to the front edge of a chair. Straighten one leg out in front of you, then lower it.",
             "3 sets of 10, building to 3 sets of 20", "Strengthens the quadriceps, including the vastus medialis on the inside of the knee that tracks the kneecap.", "Episode 6"),
            ("Standing heel to buttock", "Hold the back of a chair and stand tall. Bring one heel up toward your backside, as far as it goes comfortably. One leg at a time.",
             "3 sets of 10, building to 3 sets of 20", "Works the hamstring through range. Dave's note: doing both legs at once is how you end up on the floor.", "Episode 6"),
            ("Pillow sit to stands", "Hold a light pillow in both hands out in front of you. Push the pillow forward as you stand, keep it forward as you sit back down.",
             "3 sets of 10", "The pillow makes you hinge at the hip. Whatever joint starts the movement takes the brunt of the load, and hips carry weight better than knees do.", "Episode 6"),
            ("Step stool leans", "Put one foot up on a low step stool, keep the other on the floor, and hold something stable. Lean your weight forward over the raised foot, then back. No stepping up.",
             "Slow and controlled", "Loads the knee through a small, safe range without impact.", "Episode 6"),
            ("Glute bridge", "Lie on your back with your knees bent and both feet flat on the floor or the bed. Lift your hips up, pause at the top and squeeze your backside, then lower.",
             "3 sets of 10", "The glutes support the knee from above. Dave pairs this with quad work rather than doing either alone.", "Episode 7"),
        ],
    },
    "hip": {
        "name": "Hip &amp; Pelvis",
        "lede": "Behind most painful hips is a weak gluteus medius, the muscle that keeps your pelvis level while you stand on one leg.",
        "items": [
            ("Banded sit to stands", "Loop a resistance band around both legs just above the knees. Stand up and sit down as normal, letting the band push your knees outward.",
             "3 sets of 10", "A sore hip makes you shift weight onto the good leg without noticing. The band forces both sides to share the work.", "Episode 10"),
            ("Standing leg abductions", "Hold the back of a chair and kick one leg out away from your midline, keeping it straight. Lower with control.",
             "3 sets of 10 each side", "Direct work for the gluteus medius.", "Episode 10"),
            ("Clams", "Lie on your side with knees bent and stacked. Keep your feet together and open the top knee like a clam shell.",
             "3 sets of 10 each side", "Strengthens the external rotators, which are weak in almost everyone because nothing in daily life asks for them.", "Episode 10"),
            ("Side lying leg raise", "Lie on your side and raise the top leg straight up, then lower it slowly.",
             "3 sets of 10 each side", "Supports the same muscles from a different angle.", "Episode 10"),
            ("Prone press up", "Lie face down and push up onto your forearms or hands, keeping your pelvis down on the floor.",
             "Hold, then rest", "Opens the front of the hip. Before you get down on the floor, make sure you can get back up.", "Episode 10"),
        ],
    },
    "everyday": {
        "name": "Everyday Movement",
        "lede": "Dave's view: the invention of the chair is one of our demise. These are not workouts, they are the baseline.",
        "items": [
            ("Walk", "Get up and walk. Start at three minutes a day if that is where you are, and work up toward 10 or 15.",
             "Daily", "Gets blood moving, helps clear swelling and lowers a long list of risks. Good for the back and the knees at the same time.", "Episode 8"),
            ("Sit to stands", "Stand up out of a chair and sit back down, without pushing off with your hands if you can manage it.",
             "Little and often", "The single most functional movement most people stop practising.", "Episode 8"),
            ("Put the phone down", "Set it aside and stand up. Dave's whole point is that the movement you already know how to do is the one that gets skipped.",
             "As often as you notice", "Forward head and shoulder posture is partly gravity and partly how long we sit still.", "Episode 8"),
            ("Stretch before you start the day", "Dave's observation: babies stretch when they wake, dogs and cats stretch before they do anything, and we reach for glasses and coffee and go to work.",
             "Every morning", "Costs nothing and sets up everything else on this page.", "Episode 8"),
        ],
    },
}

def build_exercises():
    """The home exercise library Dave promised on air. Content lives in EXERCISES."""
    blocks = []
    for key, group in EXERCISES.items():
        cards = "".join(
            f'<div class="ex-card reveal"><span class="cond-tag">{reps}</span><h3>{name}</h3>'
            f'<p class="ex-how">{how}</p><p class="ex-why">{why}</p>'
            f'<p class="ex-src">Heard on Pain 2 Power, {ep}</p></div>'
            for name, how, reps, why, ep in group["items"])
        blocks.append(
            f'<section class="section" id="{key}"><div class="wrap">'
            f'<div class="section-head reveal"><h2>{group["name"]}</h2>'
            f'<p class="lede">{group["lede"]}</p></div>'
            f'<div class="ex-grid">{cards}</div></div></section>')
    jump = " ".join(f'<a class="faq-chip" href="#{k}">{g["name"]}</a>' for k, g in EXERCISES.items())
    crumbs = '<div class="crumbs"><a href="/">Home</a> / Home Exercises</div>'
    body = f"""
<main>
{page_hero("Home Exercise Library", "Exercises You Can Do <em class='accent'>At Home</em>",
  "The exercises Dr. Dave Kashuba talks through on Pain 2 Power, written down. A chair, a step stool and a resistance band cover almost all of it.", crumbs)}
<section class="section" style="padding-bottom:0;">
  <div class="wrap">
    <div class="ex-jump">{jump}</div>
    <p class="ex-warn"><strong>Read this first.</strong> These are general exercises, not a treatment plan and not medical advice.
    Nothing here should hurt. If an exercise causes pain, swelling or warmth in the joint, stop and call us.
    If you are recovering from surgery or an injury, follow the protocol your surgeon and therapist gave you instead of this page,
    and check with them before adding anything. When you want a program built for your body, that is what an evaluation is for:
    call {PHONE}.</p>
  </div>
</section>
{"".join(blocks)}
<section class="section" style="padding-top:0;">
  <div class="wrap">
    <p class="lede">Not sure which of these applies to you, or whether you should be doing them at all?
    A one on one evaluation answers that in a single visit. Call <strong>{PHONE}</strong> or
    <a href="contact.html">request an appointment</a>. You can also read how we structure
    <a href="services/physical-therapy.html">physical therapy</a> and
    <a href="services/wellness.html">our wellness program</a>, or hear these exercises explained on
    <a href="podcast.html">the Pain 2 Power podcast</a>.</p>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("exercises.html",
          head("Home Exercises for Knee, Hip & Shoulder Pain | North Palm Beach",
               "Free home exercises from occupational therapist Dr. Dave Kashuba, Ph.D., OTR: knee, hip, shoulder and everyday movement, with sets and reps. North Palm Beach.",
               canonical="exercises.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Home Exercises", "exercises.html")]))
          + nav(0) + body + footer(0))

# ----------------------------------------------------------------------------
# THINGS TO DO IN NORTH COUNTY (/things-to-do.html)
# ----------------------------------------------------------------------------
# Nick, 2026-10-25: a local "what to do" page, kept to North County, West Palm
# Beach through Jupiter. Every place and every fact below was checked against the
# place's OFFICIAL page (operator, city, village, county or nonprofit) on
# 2026-10-25; the URL is the page it was read on. Deliberately left out: hours,
# prices and anything else that changes often. Left OFF the list: Mounts Botanical
# Garden, the Palm Beach Lake Trail and Lake Park Harbor Marina (no official page
# could be opened to confirm them; NEVER link lakeparkmarina.com, a lapsed domain now
# serving spam), Blowing Rocks and Jonathan Dickinson were added 2026-10-26 at Nick's request as a
# Martin County group ("Hobe Sound"); JDSP's facts come from the Friends of JDSP page because
# floridastateparks.org refuses automated reads (403). Re-check before adding anything, and re-verify the list each spring.
# Movement keys -> chip labels shown on each card.
TTD_MOVE = {"walk": "Easy walk", "beach": "Beach", "trail": "Trail", "water": "On the water",
            "indoor": "Indoors", "climb": "Climb"}
THINGS_TO_DO = [
    {"key": "west-palm-beach", "area": "West Palm Beach", "loc": "west-palm-beach",
     "lede": "The southern end of North County, and the most to do on a rainy day.",
     "items": [
        ("Norton Museum of Art", "West Palm Beach", "indoor", "https://www.norton.org/about",
         "Founded in 1941 by Ralph and Elizabeth Norton, with a permanent collection of more than 8,900 works across European, American, Asian, contemporary and photography departments, plus a sculpture garden."),
        ("Palm Beach Zoo &amp; Conservation Society", "West Palm Beach", "walk", "https://www.palmbeachzoo.org/",
         "Four themed areas on Summit Boulevard: the Islands, Asia, the Tropics of the Americas and the Florida Wetlands, with koalas, tigers, jaguars, macaws and otters."),
        ("Manatee Lagoon, an FPL Eco&#8209;Discovery Center", "West Palm Beach", "walk", "https://www.visitmanateelagoon.com/",
         "Florida Power &amp; Light&rsquo;s center on North Flagler Drive about manatees and the Lake Worth Lagoon, with exhibits and a live manatee camera."),
        ("Grassy Waters Preserve", "West Palm Beach", "trail", "https://www.wpb.org/Departments/Grassy-Waters-Preserve",
         "The city&rsquo;s nature preserve off Northlake Boulevard. Five named trails, including the Cypress Boardwalk Trail through the cypress trees."),
        ("The downtown waterfront", "West Palm Beach", "walk", "https://www.wpb.org/Residents/Community-Events/Lake-Pavilion",
         "The Lake Pavilion, the Great Lawn at the foot of Clematis Street, and a waterfront promenade with docks, lawns and shaded trellises along the Intracoastal."),
        ("Ann Norton Sculpture Gardens", "West Palm Beach", "walk", "https://www.ansg.org/",
         "The historic home and studio of the artist Ann Norton, with a gallery and a palm and cycad collection that includes rare species."),
     ]},
    {"key": "palm-beach", "area": "Palm Beach", "loc": "palm-beach",
     "lede": "Across the bridge: one long shopping street and one Gilded Age house.",
     "items": [
        ("Worth Avenue", "Palm Beach", "walk", "https://worth-avenue.com/",
         "A landmark shopping street steps from the ocean, with boutiques, cafes and the Vias, the narrow side passages off the avenue."),
        ("Flagler Museum (Whitehall)", "Palm Beach", "indoor", "https://flaglermuseum.org/exhibits/past-exhibitions/the-story-of-whitehall",
         "Whitehall has been a private home, a club and a hotel, and is now a National Historic Landmark house museum with a free digital guide."),
     ]},
    {"key": "riviera-beach", "area": "Riviera Beach &amp; Singer Island", "loc": "riviera-beach",
     "lede": "Two very different beach days, one of them only reachable by boat.",
     "items": [
        ("Peanut Island Park", "Riviera Beach", "beach", "https://discover.pbc.gov/parks/Locations/Peanut-Island.aspx",
         "A county park you reach by boat only, by shuttle or water taxi. A snorkeling lagoon, swimming beaches, a paver walking path and an observation deck. There is no food concession, so pack what you need."),
        ("Ocean Reef Park", "Riviera Beach", "beach", "https://discover.pbc.gov/parks/Locations/Ocean-Reef.aspx",
         "A county beach park on Singer Island with about 700 feet of guarded beach, a dune overlook, picnic areas, a beach wheelchair and a Mobi Mat."),
     ]},
    {"key": "north-palm-beach", "area": "North Palm Beach", "loc": None,
     "lede": "Our own town, and home to the only state park in the county.",
     "items": [
        ("John D. MacArthur Beach State Park", "North Palm Beach", "beach", "https://www.village-npb.org/1117/Parks-Facilities",
         "The only state park in Palm Beach County, on an Atlantic barrier island. A 1,600 foot boardwalk crosses the estuary to 1.6 miles of beach, and there is a nature center. You can kayak or paddleboard the estuary."),
        ("Anchorage Park", "North Palm Beach", "walk", "https://www.village-npb.org/533/Anchorage-Park",
         "A 21.5 acre village park with two fishing piers, a fitness trail, sand volleyball courts, dog parks and a kayak and paddleboard launch."),
     ]},
    {"key": "palm-beach-gardens", "area": "Palm Beach Gardens", "loc": "palm-beach-gardens",
     "lede": "Paved paths, a preserve with marked trail lengths, and somewhere air conditioned.",
     "items": [
        ("Frenchman&rsquo;s Forest Natural Area", "Palm Beach Gardens", "trail", "https://discover.pbc.gov/erm/NaturalAreas/Frenchmans-Forest.aspx",
         "A 172 acre county natural area on Prosperity Farms Road. The Blazing Star trail is paved and 0.4 miles; the sandy Saw Palmetto trail runs 1.3 miles. A boardwalk crosses a cypress swamp."),
        ("The Gardens North County District Park", "Palm Beach Gardens", "walk", "https://pbgfl.gov/1024/The-Gardens-North-County-District-Park",
         "An 82 acre city park with lighted fields, two spray pads, two playgrounds, a nature trail and 23.6 acres of preserve."),
        ("Downtown Palm Beach Gardens", "Palm Beach Gardens", "walk", "https://downtownpalmbeachgardens.com/about/",
         "Formerly Downtown at the Gardens. Palm shaded lakeside walks, a pop jet fountain and the Downtown Carousel on the waterfront."),
        ("The Gardens Mall", "Palm Beach Gardens", "indoor", "https://www.thegardensmall.com/visiting/",
         "More than 150 shops on PGA Boulevard, open since 1988. A long, flat, air conditioned walk on a hot afternoon."),
     ]},
    {"key": "juno-beach", "area": "Juno Beach", "loc": "juno-beach",
     "lede": "Sea turtles, a fishing pier and the highest natural point in the county.",
     "items": [
        ("Loggerhead Marinelife Center", "Juno Beach", "walk", "https://marinelife.org/plan-your-visit/",
         "A sea turtle conservation nonprofit with an outdoor sea turtle hospital. The campus is mostly outdoors, with large shaded sections."),
        ("Juno Beach Pier", "Juno Beach", "walk", "https://marinelife.org/juno-beach-pier/",
         "A 990 foot fishing pier in county owned Juno Beach Park, run by Loggerhead Marinelife Center. A phased refurbishment began in June 2026, so check the pier&rsquo;s page for what is open before you go."),
        ("Juno Dunes Natural Area", "Juno Beach", "trail", "https://discover.pbc.gov/erm/NaturalAreas/Juno-Dunes.aspx",
         "569 acres from the ocean to the Intracoastal. On the ocean side, a paved, accessible trail climbs to a covered platform on an ancient dune, billed as the highest natural point in Palm Beach County. The west side has sandy trails of 1.8 and 2.1 miles."),
     ]},
    {"key": "jupiter", "area": "Jupiter &amp; Tequesta", "loc": "jupiter",
     "lede": "The northern edge of North County, and the longest list.",
     "items": [
        ("Jupiter Inlet Lighthouse &amp; Museum", "Jupiter", "climb", "https://www.jupiterlighthouse.org/directions-hours",
         "You can climb the 1860 lighthouse, and the site itself calls the climb strenuous; even the tower&rsquo;s base is 34 steps up a hill. The grounds are part of a 120 acre federal Outstanding Natural Area."),
        ("Riverbend Park", "Jupiter", "trail", "https://discover.pbc.gov/parks/Locations/Riverbend.aspx",
         "A 644 acre county park on Indiantown Road with nearly 10 miles of shell rock hiking and biking trails, 5 miles of waterways on the Loxahatchee River, and the site of the Loxahatchee Battlefield."),
        ("Carlin Park", "Jupiter", "beach", "https://discover.pbc.gov/parks/Locations/Carlin.aspx",
         "A 109 acre county beach park with about 3,000 feet of guarded beach, a 20 station exercise course over 1.25 miles, and the Seabreeze Amphitheater."),
        ("Jupiter Beach Park", "Jupiter", "beach", "https://discover.pbc.gov/parks/Locations/Jupiter-Beach.aspx",
         "About 1,700 feet of guarded beach beside the inlet, a jetty for saltwater fishing and a Mobi Mat."),
        ("DuBois Park", "Jupiter", "water", "https://discover.pbc.gov/parks/Locations/DuBois.aspx",
         "A county park with a snorkeling lagoon and Intracoastal beach, a canoe and kayak launch, and the DuBois Pioneer Home and Jupiter Inlet Mound, both on the National Register of Historic Places."),
        ("Coral Cove Park", "Tequesta", "beach", "https://discover.pbc.gov/parks/Locations/Coral-Cove.aspx",
         "A county beach park on Beach Road with about 600 feet of guarded beach, another 2,010 feet of unguarded beach to the south, and Intracoastal frontage."),
        ("Harbourside Place", "Jupiter", "walk", "https://www.harboursideplace.com/",
         "Waterfront shopping and dining along Jupiter&rsquo;s Intracoastal, with an amphitheater for live music."),
        ("Roger Dean Chevrolet Stadium", "Jupiter", "walk", "https://www.mlb.com/roger-dean-chevrolet-stadium/ballpark",
         "Spring training home of the Miami Marlins and St. Louis Cardinals since 1998, and home to the Jupiter Hammerheads and Palm Beach Cardinals the rest of the year."),
     ]},
    {"key": "hobe-sound", "area": "Hobe Sound", "loc": None, "county": "Just over the line in Martin County",
     "lede": "Just north of Tequesta: limestone that throws the sea in the air, and the largest state park in Southeast Florida.",
     "items": [
        ("Blowing Rocks Preserve", "Hobe Sound", "beach", "https://www.nature.org/en-us/get-involved/how-to-help/places-we-protect/blowing-rocks-preserve/",
         "A Nature Conservancy preserve on Jupiter Island with the largest Anastasia limestone shoreline on the Atlantic coast. At high tide in rough seas, waves force plumes of saltwater up to 50 feet in the air. Short trails, a 300 foot boardwalk through mangroves, and a beach with no lifeguard. In October 2026 the preserve posted a hurricane closure notice, so check before you go."),
        ("Jonathan Dickinson State Park", "Hobe Sound", "trail", "https://www.friendsofjdsp.org/pages/our-park",
         "The largest state park in Southeast Florida, over 10,500 acres along the Loxahatchee, Florida&rsquo;s first federally designated Wild and Scenic River. Paddle the river, ride the paved multi&#8209;use trail or the Camp Murphy bike loops, or take the boat only trip to the 1930s Trapper Nelson homestead. The Hobe Mountain tower is closed for restoration."),
     ]},
]


# Photos for /things-to-do.html, keyed by the place name in THINGS_TO_DO. This is a
# THIRD photo source beside PHOTOS (the clinic) and the guest headshots, and it is
# deliberately separate from PHOTOS: none of these are photos of the clinic.
# Order of preference (Nick, 2026-10-26: "both"): a still from Nick's OWN footage
# (credit None), else a Wikimedia Commons photo under CC BY / CC BY-SA / CC0 / public
# domain, credited on the image with its author, licence and a link to its Commons
# page. Never an operator's own marketing photo (copyright), never generated art.
# Files: assets/places/<key>-{800,1600}.{webp,jpg}, made by tools/place-photo.py.
PLACE_PHOTOS = {
    "Norton Museum of Art": {"key": "norton", "w": 800, "h": 600,
        "alt": "The Norton Museum of Art in West Palm Beach, its entrance banner framed by palms",
        "author": "Ebyabe", "license": "CC BY-SA 3.0", "page": "https://commons.wikimedia.org/wiki/File:West_PB_FL_Norton_MoA01.jpg"},
    "Palm Beach Zoo &amp; Conservation Society": {"key": "zoo", "w": 800, "h": 600,
        "alt": "An Indian roller perched on a branch at the Palm Beach Zoo in West Palm Beach",
        "author": "airwaves1", "license": "CC BY 2.0", "page": "https://commons.wikimedia.org/wiki/File:Coracias_benghalensis_-Palm_Beach_Zoo_-USA-8a.jpg"},
    "Manatee Lagoon, an FPL Eco&#8209;Discovery Center": {"key": "manatee-lagoon", "w": 800, "h": 600,
        "alt": "Manatee Lagoon on the Lake Worth Lagoon in West Palm Beach under a clear blue sky",
        "author": "FunctioningMemberOfSociety", "license": "CC BY 4.0", "page": "https://commons.wikimedia.org/wiki/File:Manatee_Lagoon,_West_Palm_Beach.jpg"},
    "Grassy Waters Preserve": {"key": "grassy-waters", "w": 800, "h": 600,
        "alt": "Marsh grass along open water at Grassy Waters Preserve, West Palm Beach",
        "author": "P. Vald&eacute;s", "license": "CC BY 3.0", "page": "https://commons.wikimedia.org/wiki/File:Habitat_of_Semiardistomis_viridis_(Say)_at_Grassy_Waters_Preserve,_West_Palm_Beach,_Florida,_USA_-_ZooKeys-210-019-g018.jpeg"},
    "The downtown waterfront": {"key": "wpb-waterfront", "w": 800, "h": 297,
        "alt": "The West Palm Beach skyline seen across the Intracoastal Waterway",
        "author": "Jared", "license": "CC BY 2.0", "page": "https://commons.wikimedia.org/wiki/File:West_Palm_Beach_-_Waterfront_-_Intracoastal_Waterway_%26_Downtown_Skyline_-_Panorama_(15300572403).jpg"},
    "Ann Norton Sculpture Gardens": {"key": "ann-norton", "w": 800, "h": 600,
        "alt": "Ann Norton&rsquo;s historic house in the El Cid district of West Palm Beach, with palms and cycads in front",
        "author": "Ebyabe", "license": "CC BY-SA 3.0", "page": "https://commons.wikimedia.org/wiki/File:West_PB_FL_El_Cid_HD_Norton_House02.jpg"},
    "Worth Avenue": {"key": "worth-avenue", "w": 800, "h": 535,
        "alt": "An arched arcade of shop windows on Worth Avenue, Palm Beach",
        "author": "Elisa.rolle", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:I_Worth_Avenue_Gallery,_Palm_Beach,_FL.jpg"},
    "Flagler Museum (Whitehall)": {"key": "whitehall", "w": 800, "h": 531,
        "alt": "The white columned front of Whitehall, the Flagler Museum, in Palm Beach",
        "author": "Roger Wollstadt", "license": "CC BY-SA 2.0", "page": "https://commons.wikimedia.org/wiki/File:Henry_Flagler_House.jpg"},
    "Peanut Island Park": {"key": "peanut-island", "w": 800, "h": 533,
        "alt": "A beach umbrella on white sand at Peanut Island, with boats moored offshore",
        "author": "Florida Guidebook", "license": "CC BY 2.0", "page": "https://commons.wikimedia.org/wiki/File:Peanut-Island-Web-3766_(49369642831).jpg"},
    "John D. MacArthur Beach State Park": {"key": "macarthur", "w": 800, "h": 600,
        "alt": "The long boardwalk across the estuary at John D. MacArthur Beach State Park",
        "author": "Dougtone", "license": "CC BY-SA 2.0", "page": "https://commons.wikimedia.org/wiki/File:John_D._MacArthur_Beach_State_Park_-_Riviera_Beach,_Florida_-_7020831037.jpg"},
    "Frenchman&rsquo;s Forest Natural Area": {"key": "frenchmans", "w": 800, "h": 600,
        "alt": "A wooden boardwalk through palms and cypress at Frenchman&rsquo;s Forest Natural Area, Palm Beach Gardens",
        "author": "supercraigtalbert", "license": "CC BY 2.0", "page": "https://commons.wikimedia.org/wiki/File:Frenchman%27s_Forest_Natural_Area_-_50666290803.jpg"},
    "The Gardens Mall": {"key": "gardens-mall", "w": 800, "h": 600,
        "alt": "The two level atrium inside The Gardens Mall, Palm Beach Gardens",
        "author": "*angys*", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:The_Gardens_Mall_(220709)_02.jpg"},
    "Loggerhead Marinelife Center": {"key": "loggerhead", "w": 800, "h": 600,
        "alt": "The front of Loggerhead Marinelife Center in Juno Beach",
        "author": "Ebyabe", "license": "CC BY-SA 3.0", "page": "https://commons.wikimedia.org/wiki/File:Juno_Beach_FL_Loggerhead_Marinelife_Center01.jpg"},
    "Juno Beach Pier": {"key": "juno-pier", "w": 800, "h": 450,
        "alt": "Juno Beach Pier from the air, reaching out over turquoise water beside the beach",
        "author": "", "license": "", "page": ""},
    "Juno Dunes Natural Area": {"key": "juno-dunes", "w": 800, "h": 800,
        "alt": "A pink largeflower rose gentian in bloom at Juno Dunes Natural Area",
        "author": "Bob Peterson", "license": "CC BY-SA 2.0", "page": "https://commons.wikimedia.org/wiki/File:Largeflower_Rose_Gentian_(Juno_Dunes)_(5745874652).jpg"},
    "Jupiter Inlet Lighthouse &amp; Museum": {"key": "lighthouse", "w": 800, "h": 450,
        "alt": "The red Jupiter Inlet Lighthouse from the air, above the inlet and the trees around it",
        "author": "", "license": "", "page": ""},
    "Riverbend Park": {"key": "riverbend", "w": 800, "h": 533,
        "alt": "A shell rock trail curving through oaks and palms at Riverbend Park, Jupiter",
        "author": "JupiterFlorida", "license": "CC BY 3.0", "page": "https://commons.wikimedia.org/wiki/File:Riverbend_Park_-_panoramio.jpg"},
    "DuBois Park": {"key": "dubois", "w": 800, "h": 600,
        "alt": "Jupiter Inlet seen from the rocks at DuBois Park, looking west",
        "author": "Dough4872", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:Jupiter_Inlet_from_Dubois_Park_looking_west.jpeg"},
    "Coral Cove Park": {"key": "coral-cove", "w": 800, "h": 600,
        "alt": "Waves breaking over the limestone rocks on the beach at Coral Cove Park, Tequesta",
        "author": "Anonymouskc", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:CCPbeach.jpg"},
    "Roger Dean Chevrolet Stadium": {"key": "roger-dean", "w": 800, "h": 600,
        "alt": "The arched brick entrance of the stadium in Jupiter, under its earlier Roger Dean Stadium sign",
        "author": "Jtesla16", "license": "CC BY-SA 3.0", "page": "https://commons.wikimedia.org/wiki/File:Roger_Dean_Stadium.JPG"},
    "Blowing Rocks Preserve": {"key": "blowing-rocks", "w": 800, "h": 392,
        "alt": "Atlantic waves washing over the Anastasia limestone rocks at Blowing Rocks Preserve at dawn",
        "author": "LTreadwell", "license": "CC BY-SA 4.0", "page": "https://commons.wikimedia.org/wiki/File:Blowing_Rocks_Preserve_Jupiter_Island_Florida.jpg"},
    "Jonathan Dickinson State Park": {"key": "jdsp", "w": 800, "h": 600,
        "alt": "Kayakers paddling the Loxahatchee River past mangroves in Jonathan Dickinson State Park",
        "author": "Stephen B Calvert", "license": "CC BY-SA 3.0", "page": "https://commons.wikimedia.org/wiki/File:Jonathan_Dickinson_State_Park_027.JPG"},
}

def place_img(name, lead=False):
    ph = PLACE_PHOTOS.get(name)
    if not ph:
        return ""
    k, w, h = ph["key"], ph["w"], ph["h"]
    sizes = "(min-width: 900px) 760px, 92vw" if lead else "(min-width: 900px) 380px, 92vw"
    return (f'<picture><source type="image/webp" srcset="assets/places/{k}-800.webp 800w, assets/places/{k}-1600.webp 1600w" sizes="{sizes}">'
            f'<img src="assets/places/{k}-800.jpg" srcset="assets/places/{k}-800.jpg 800w, assets/places/{k}-1600.jpg 1600w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{ph["alt"]}" style="object-position:{ph.get("focal", "50% 50%")}" loading="lazy" decoding="async"></picture>')

def place_credit(name):
    ph = PLACE_PHOTOS.get(name)
    if not ph:
        return ""
    if not ph.get("author"):
        return '<span class="place-credit">Our own footage</span>'
    return (f'<span class="place-credit">Photo: {ph["author"]}, <a href="{ph["page"]}" target="_blank" rel="noopener">'
            f'{ph["license"]}</a></span>')

def build_things_to_do():
    """North County things to do, West Palm Beach to Jupiter. Data: THINGS_TO_DO."""
    import json as _json
    blocks, ld = [], []
    for g in THINGS_TO_DO:
        cards = "".join(
            f'<article class="place-card reveal{" is-lead" if i == 0 else ""}">'
            + (f'<figure class="place-fig">{place_img(name, lead=(i == 0))}<span class="place-tag">{TTD_MOVE[mv]}</span>'
               f'{place_credit(name)}</figure><div class="place-body">' if name in PLACE_PHOTOS else
               f'<div class="place-body"><span class="cond-tag">{TTD_MOVE[mv]}</span>')
            + f'<h3>{name}</h3><p class="ex-how">{blurb}</p>'
            f'<p class="ex-src">{town} &middot; <a href="{url}" target="_blank" rel="noopener">'
            f'{"Friends of the park" if "friendsofjdsp" in url else "Official site"}</a></p></div></article>'
            for i, (name, town, mv, url, blurb) in enumerate(g["items"]))
        if g["key"] == "jupiter":
            tail = ('<p class="lede" style="margin-top:var(--space-5);">Live up here? Read about physical therapy for '
                    '<a href="locations/jupiter.html">Jupiter</a> and <a href="locations/tequesta.html">Tequesta</a> residents.</p>')
        elif g["key"] == "hobe-sound":
            tail = ('<p class="lede" style="margin-top:var(--space-5);">Coming down from Hobe Sound or Tequesta? '
                    'Read about <a href="locations/tequesta.html">physical therapy for Tequesta residents</a>.</p>')
        elif g["loc"]:
            tail = (f'<p class="lede" style="margin-top:var(--space-5);">Live in {g["area"]}? Read about '
                    f'<a href="locations/{g["loc"]}.html">physical therapy for {g["area"]} residents</a>.</p>')
        else:
            tail = ('<p class="lede" style="margin-top:var(--space-5);">Our clinic is here too, at '
                    '733 US Highway 1. <a href="first-visit.html">What to expect at your first visit</a>.</p>')
        blocks.append(
            f'<section class="section ttd-town" id="{g["key"]}"><div class="wrap">'
            f'<div class="section-head reveal"><span class="eyebrow">{g.get("county", "Palm Beach County")}</span>'
            f'<h2>Things to do in {g["area"]}</h2>'
            f'<p class="lede">{g["lede"]}</p></div>'
            f'<div class="place-grid">{cards}</div>{tail}</div></section>')
        for name, town, mv, url, blurb in g["items"]:
            ld.append({"@type": "TouristAttraction", "name": _faq_plain(name), "url": url,
                       "description": _faq_plain(blurb),
                       "address": {"@type": "PostalAddress", "addressLocality": town,
                                   "addressRegion": "FL", "addressCountry": "US"}})
    url = "https://www.firstrehabnpb.com/things-to-do.html"
    schema = '<script type="application/ld+json">' + _json.dumps({
        "@context": "https://schema.org", "@type": "ItemList", "@id": url + "#list",
        "name": "Things to do in North County, West Palm Beach to Jupiter",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": node}
                            for i, node in enumerate(ld)],
    }, ensure_ascii=False) + '</script>\n'
    jump = " ".join(f'<a class="faq-chip" href="#{g["key"]}">{g["area"]}</a>' for g in THINGS_TO_DO)
    crumbs = '<div class="crumbs"><a href="/">Home</a> / Things to Do</div>'
    body = f"""
<main>
{page_hero("North County &amp; Hobe Sound", "Things to Do, <em class='accent'>West Palm Beach to Hobe Sound</em>",
  "Parks, beaches, trails and museums from West Palm Beach up to Hobe Sound, grouped by town and tagged by how much moving each one asks of you.", crumbs, loop="juno")}
<section class="section" style="padding-bottom:0;">
  <div class="wrap">
    <p class="lede">The point of therapy is getting back to your life, and around here a lot of that life happens outdoors. So here is North County, from West Palm Beach up to Jupiter and Tequesta, plus two favorites just over the Martin County line, one town at a time. Every place carries a tag: an easy walk, a beach, a trail, time on the water, somewhere indoors, or a climb. If you are partway through recovery, pick from the gentler end and ask your therapist before you take on a sandy trail or a lighthouse staircase. That is exactly the kind of goal we like to build a plan around.</p>
    <div class="ex-jump">{jump}</div>
    <p class="ex-src">Every place below was checked against its own official site in October 2026. Hours, fees and closures change, so check before you go. We are not affiliated with any of them.</p>
  </div>
</section>
{"".join(blocks)}
<section class="section" style="padding-top:0;">
  <div class="wrap">
    <p class="lede">Want the stairs at the lighthouse or the 1.25 mile course at Carlin Park back on your list?
    Tell us at your evaluation and we will build toward it. Call <strong>{PHONE}</strong> or
    <a href="contact.html">request an appointment</a>. Between visits, the
    <a href="exercises.html">home exercise library</a> has the moves Dr. Dave Kashuba talks through on
    <a href="podcast.html">Pain 2 Power</a>.</p>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("things-to-do.html",
          head("Things to Do From West Palm Beach to Jupiter | First Rehab",
               "Parks, beaches, trails and museums from West Palm Beach to Jupiter, grouped by town and tagged by how much walking each takes. From First Rehab, North Palm Beach.",
               canonical="things-to-do.html",
               extra_schema=p2p_poster_preload("juno") + schema + breadcrumb_schema([("Home", ""), ("Things to Do", "things-to-do.html")]))
          + nav(0) + body + footer(0))


EPISODE_POSTS = {
    "Episode 20": "pain-2-power-ep20-kendzierski",           # Maria Kendzierski
    "Episode 18": "pain-2-power-ep18-marrone-armstrong",     # Elyse Marrone and Danielle Armstrong
    "Episode 17": "pain-2-power-ep17-goodwin",               # Dr. Don Goodwin
    "Episode 14": "pain-2-power-ep14-arlosoroff",            # Dr. Chaim Arlosoroff
    "Episode 13": "pain-2-power-ep13-titheradge",            # Captain Kerry Titheradge
    "Episode 12": "pain-2-power-ep12-leighton",              # Dr. Michael Leighton
    "Episode 9": "pain-2-power-ep9-sabesan",                # Dr. Vani Sabesan
    "Episode 19": "pain-2-power-ep19-cake",                # Shannon Cake
    "Episode 15": "pain-2-power-ep15-mann",                # Susan Mann
    "Episode 11": "pain-2-power-ep11-joyce",                # Paul Joyce
    "Episode 10": "pain-2-power-ep10-mcvicker",              # Dr. Zach McVicker
    "Episode 8": "reverse-shoulder-replacement-explained",   # Dr. Ryan Simovitch
    "Episode 7": "cartilage-transplant-knee-explained",      # Dr. Rami Elkhechen
    "Episode 6": "knee-arthritis-before-surgery",            # Dr. Richard Weiner
}

# ----------------------------------------------------------------------------
# PAIN 2 POWER — GUESTS (/guests.html)
# ----------------------------------------------------------------------------
# One JSON file per guest in content/guests/<slug>.json, NOT a dict here, so the
# episode watcher routine can add a researched guest without editing Python.
# Shape and rules: .claude/skills/podcast-guest/SKILL.md. Every background fact
# carries the URL it came from, and tools/guest-sync.py validate refuses a file
# that does not. GUESTS is sorted newest episode first; EPISODE_GUESTS maps an
# EPISODES label to the guests on it, for the "Meet the guest" links and the
# PodcastEpisode contributor schema.
def _load_guests():
    import glob, json as _json
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "guests", "*.json"))):
        with open(path, encoding="utf-8") as f:
            out.append(_json.load(f))
    def latest(g):
        return max(int(e.split()[-1]) for e in g["episodes"])
    titles = {e[0]: e[1] for e in EPISODES}
    def billing(g):   # "Elyse Marrone and Danielle Armstrong" -> Marrone first
        pos = titles.get(f"Episode {latest(g)}", "").find(g["name"].split()[-1])
        return pos if pos >= 0 else 10**6
    out.sort(key=lambda g: (-latest(g), billing(g), g["slug"]))
    return out

GUESTS = _load_guests()
EPISODE_GUESTS = {}
for _g in GUESTS:
    for _e in _g["episodes"]:
        EPISODE_GUESTS.setdefault(_e, []).append(_g)

def guest_display(g):
    """'Dr. Matt Butler, MD' — honorific, name, then credentials as the guest writes them."""
    name = f'{g["honorific"]} {g["name"]}'.strip()
    return f'{name}, {g["credentials"]}' if g.get("credentials") else name

GUEST_CATEGORIES = [   # (key, chip label) — the order the directory's filter chips show
    ("orthopedic-surgery", "Orthopedic Surgery"),
    ("shoulder-elbow-hand", "Shoulder, Elbow &amp; Hand"),
    ("other-specialists", "Other Specialists"),
    ("nutrition-wellness", "Nutrition &amp; Wellness"),
    ("community", "Community Voices"),
    ("our-team", "Our Therapists"),
]
GUEST_CAT_LABEL = dict(GUEST_CATEGORIES)

def guest_url(g):
    """Site-relative path of a guest's profile page."""
    return f"guests/{g['slug']}.html"

def guest_id(g):
    return f"https://www.firstrehabnpb.com/{guest_url(g)}#person"

def _podcast_schema():
    """PodcastSeries + PodcastEpisode JSON-LD from the EPISODES list."""
    import json as _json
    series = {"@context": "https://schema.org", "@type": "PodcastSeries",
              "publisher": {"@id": "https://www.firstrehabnpb.com/#organization"},
              "name": "Pain 2 Power",
              "description": "Dr. Dave Kashuba and Mike McGann cover the world of physical rehab and wellness with some of the sharpest minds in medicine.",
              "url": "https://www.firstrehabnpb.com/podcast.html",
              "image": "https://www.firstrehabnpb.com/assets/media/podcast-cover.jpg",
              "sameAs": SPOTIFY}
    graph = [series]
    for num, title, desc, url, label in EPISODES:
        if "open.spotify.com/episode/" in url:
            ep = {"@type": "PodcastEpisode", "name": _faq_plain(title),
                  "description": _faq_plain(desc.replace("<br><br>", " ")), "url": url,
                  "partOfSeries": {"@type": "PodcastSeries", "name": "Pain 2 Power"}}
            # The guest, by @id, pointing at their Person node on /guests.html.
            if EPISODE_GUESTS.get(num):
                ep["contributor"] = [{"@type": "Person", "@id": guest_id(g), "name": _faq_plain(guest_display(g))}
                                     for g in EPISODE_GUESTS[num]]
            graph.append(ep)
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def _paras(text):
    """Split an episode blurb on <br><br> into separate <p> elements.

    One 330-word <p> is a full phone screen of unbroken text — flagged by the
    Semrush crawl (2026-08-23) for both readability and passage-level retrieval,
    which works better on discrete chunks. The break points live in the EPISODES
    copy as <br><br>; keep new blurbs to roughly 40-80 words per chunk and give
    an opening quote its own break.
    """
    parts = [t.strip() for t in text.split("<br><br>")]
    return "".join(f"<p>{t}</p>" for t in parts if t)


def build_podcast():
    import re as _re
    def _episode_block(num, title, desc, url, label):
        # Episodes with a Spotify episode URL get an in-page player;
        # anything else (e.g. "coming Saturday") keeps its action button.
        m = _re.search(r"open\.spotify\.com/episode/([A-Za-z0-9]+)", url)
        if m:
            # Full Spotify episode player, shown by default (cover, date, length,
            # Save). loading="lazy" defers each iframe until it scrolls near view,
            # so the six players don't all load at once on page open.
            action = (f'<iframe class="pod-embed" '
                      f'src="https://open.spotify.com/embed/episode/{m.group(1)}?utm_source=generator&amp;theme=0" '
                      f'width="100%" height="152" frameborder="0" loading="lazy" style="border-radius:14px;" '
                      f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" '
                      f'title="{title} — Pain 2 Power on Spotify"></iframe>')
        else:
            action = f'<a class="btn btn-ink" href="{url}" target="_blank" rel="noopener">{label}</a>'
        # A recap post, when one exists, gets a link from this strong page to that new one.
        recap = ""
        slug = EPISODE_POSTS.get(num)
        if slug and slug in BLOG_POSTS:
            recap = (f'<p class="pod-recap"><a href="blog/{slug}.html">'
                     f'Read the recap: {BLOG_POSTS[slug]["title"]}</a></p>')
        for g in EPISODE_GUESTS.get(num, []):
            recap += (f'<p class="pod-recap"><a href="{guest_url(g)}">'
                      f'Meet the guest: {guest_display(g)}</a></p>')
        return f'''<div class="pod-card reveal">
          <div class="pod-head"><span class="pod-num">{num}</span><h3>{title}</h3>{_paras(desc)}{recap}</div>
          {action}
        </div>'''
    featured = _episode_block(*EPISODES[0])
    eps = "".join(_episode_block(*e) for e in EPISODES[1:])
    body = f"""
<main>
{page_hero("The Pain 2 Power Podcast", "Real Conversations That <em class='accent'>Move You Forward</em>",
  "Dr. Dave Kashuba and Mike McGann cover the world of physical rehab and wellness — with some of the sharpest minds in medicine.",
  '<div class="crumbs"><a href="/">Home</a> / Podcast</div>', loop="audio")}
<section class="section" style="padding-bottom:0;">
  <div class="wrap">
    <div class="section-head reveal" style="margin-bottom:1.6rem;">
      <h2 class="eyebrow" style="border:0;padding:0;">Latest Episode</h2>
    </div>
    <div class="pod-featured-wrap">{featured}</div>
  </div>
</section>
<section class="section">
  <div class="wrap two-col">
    <div class="reveal">
      <div class="section-head" style="margin-bottom:2rem;">
        <span class="eyebrow">Your Hosts</span>
        <h2>Dave &amp; Mike</h2>
      </div>
      <div class="hosts-stack">
        <div class="host-bio reveal">
          {photo("team-david", sizes="140px", ratio="1/1")}
          <div>
            <h3>Dave Kashuba, Ph.D.</h3>
            <div class="role">Founder &amp; Occupational Therapist</div>
            <p>Founder of First Rehabilitation and a practicing occupational therapist, Dave has personally treated more than 87,000 patients across four decades &mdash; and the practice he built has cared for more than 180,000 &mdash; bringing a lifetime of hands-on experience to every conversation about healing and resilience.</p>
          </div>
        </div>
        <div class="host-bio reveal d2">
          {photo("mike", sizes="140px", ratio="1/1")}
          <div>
            <h3>Mike McGann</h3>
            <div class="role">Co-Host</div>
            <p>Co-host Mike McGann brings more than 17 years on the Palm Beach County airwaves to the show. He's hosted music and talk programs of nearly every style and now calls Legends 100.3 home — and a lifelong love of the Great American Songbook, sparked by his mom and a little Sinatra at age seven, gives him a storyteller's ear that's perfect for drawing out every guest's journey.</p>
          </div>
        </div>
      </div>
      <div class="section-head" style="margin-bottom:2rem;">
        <span class="eyebrow">Previous Episodes</span>
        <h2>Listen &amp; Subscribe</h2>
      </div>
      {eps}
    </div>
    <aside class="side-card reveal d2">
      <h3>Where to listen</h3>
      <p>New episodes air Saturdays at 8:30 AM on <a href="https://legendsradio.com/listen-live/" target="_blank" rel="noopener">100.3 Legends Radio — listen live here</a> — and stream anytime on Spotify.</p>
      <button class="pod-facade" type="button" style="height:352px;margin-top:1.2rem;" data-embed="https://open.spotify.com/embed/show/033A1BQq9qqsygFFCq9SIu?utm_source=generator&amp;theme=0" data-height="352" data-title="Pain 2 Power on Spotify"><span class="pf-play" aria-hidden="true">&#9654;</span><span class="pf-label">Browse every episode<span class="pf-sub">Streams from Spotify — loads when you press play</span></span></button>
      <a class="btn btn-coral" href="{SPOTIFY}" target="_blank" rel="noopener">Open in Spotify</a>
      <a class="btn btn-ink" style="margin-top:0.7rem;" href="https://legendsradio.com/listen-live/" target="_blank" rel="noopener">Listen Live on Legends Radio</a>
      <div class="side-meta">
        <p>📻 Saturdays &middot; 8:30 AM<br>100.3 Legends Radio</p>
      </div>
    </aside>
  </div>
</section>
<section class="section on-cream" id="community">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Join the Show</span>
      <h2>Be Part of <em class="accent">Pain 2 Power</em></h2>
    </div>
    <div class="pod-community">
      <div class="pod-form-card reveal">
        <h3>Ask Dave</h3>
        <p>Have a question about pain, recovery, or staying strong as you age? Send it in — Dave may answer it on a future episode.</p>
        <form class="appt-form" id="ask-dave-form" novalidate>
          <div class="af-field">
            <label for="ad-name">Name <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
            <input id="ad-name" name="name" type="text" autocomplete="name" maxlength="200">
          </div>
          <div class="af-field">
            <label for="ad-email">Email <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
            <input id="ad-email" name="email" type="email" autocomplete="email" maxlength="200">
          </div>
          <div class="af-field">
            <label for="ad-question">Your question</label>
            <textarea id="ad-question" name="question" required maxlength="2000" placeholder="e.g. Why does my knee hurt more going down stairs than up?"></textarea>
          </div>
          <div class="cf-extra" aria-hidden="true"><label for="ad-website">Website</label><input id="ad-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          <p class="af-error" role="alert"></p>
          <button class="btn btn-coral" type="submit">Send Your Question <span class="arr">&rarr;</span></button>
        </form>
        <div class="af-done" id="ask-dave-form-done" hidden>
          <h3>Question received</h3>
          <p>Thank you — Dave reads every question, and yours may be answered on a future episode of Pain 2 Power. Tune in Saturdays at 8:30 AM on 100.3 Legends Radio.</p>
        </div>
      </div>
      <div class="pod-form-card reveal d2">
        <h3>Send Us a Dad Joke</h3>
        <p>Every episode of Pain 2 Power ends with a dad joke — and we're always hunting for the next groaner. Send us your best.</p>
        <form class="appt-form" id="dad-joke-form" novalidate>
          <div class="af-field">
            <label for="dj-name">First name <span style="font-weight:400;color:var(--muted);">(optional)</span></label>
            <input id="dj-name" name="first_name" type="text" autocomplete="given-name" maxlength="80">
          </div>
          <div class="af-field">
            <label for="dj-joke">Your joke</label>
            <textarea id="dj-joke" name="joke" required maxlength="500" placeholder="Why don't skeletons fight each other?&#10;They don't have the guts."></textarea>
          </div>
          <div class="cf-extra" aria-hidden="true"><label for="dj-website">Website</label><input id="dj-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          <p class="af-error" role="alert"></p>
          <button class="btn btn-ink" type="submit">Submit Your Joke <span class="arr">&rarr;</span></button>
        </form>
        <div class="af-done" id="dad-joke-form-done" hidden>
          <h3>Joke received</h3>
          <p>Thank you — our panel of highly serious joke judges will take it from here. Listen for it at the end of a future episode.</p>
        </div>
      </div>
    </div>
    <div class="joke-feed" id="joke-feed" hidden>
      <div class="section-head center reveal" style="margin-top:1rem;">
        <span class="eyebrow">From Our Listeners</span>
        <h2>The Dad Joke <em class="accent">Hall of Fame</em></h2>
      </div>
      <div class="joke-list"></div>
    </div>
  </div>
</section>
{cta_band(0)}
<script src="assets/js/podcast-extras.js?v={asset_v('assets/js/podcast-extras.js')}" defer></script>
</main>
"""
    write("podcast.html",
          head("Pain 2 Power Podcast | First Rehabilitation of North Palm Beach",
               "Dr. Dave Kashuba and Mike McGann cover the world of physical rehab and wellness. Saturdays on 100.3 Legends Radio and streaming on Spotify.",
               canonical="podcast.html", og_image="assets/media/podcast-cover.jpg",
               extra_schema=p2p_poster_preload("audio") + _podcast_schema() + _trailer_schema()
                            + breadcrumb_schema([("Home", ""), ("Podcast", "podcast.html")]))
          + nav(0) + body + footer(0))

# ----------------------------------------------------------------------------
# FAQ CONTENT — one filterable page, category bubbles, single FAQPage schema
# Answers are plain text (no HTML) so the same source feeds both the visible
# accordions and the JSON-LD. Phone numbers become tap-to-call links
# automatically via linkify_phone(); the JSON-LD is protected inside <script>.
# ----------------------------------------------------------------------------

FAQ_CATEGORIES = [
    ("physical-therapy", "Physical Therapy", [
        ("What does a physical therapist actually do?",
         "A physical therapist evaluates how your body moves — strength, mobility, balance, and mechanics — then treats the cause of pain and dysfunction with hands-on techniques, targeted exercise, and movement retraining. At First Rehabilitation that starts with a comprehensive one-on-one evaluation, and treatment usually begins the same day."),
        ("Do I need a referral to see a physical therapist in Florida?",
         "Usually not to get started — Florida's direct access law lets you begin a physical therapy evaluation without a physician referral in most cases. Some insurance plans still require a referral for coverage, and Medicare requires a physician to certify your therapy plan of care, so call 561-624-4263 and our front desk will confirm what your plan needs."),
        ("What conditions does physical therapy treat?",
         "Physical therapy at our clinic treats back and neck pain, sciatica, shoulder, hip, knee, foot, and ankle pain, arthritis, sports and overuse injuries, balance problems and fall risk, headaches driven by the neck, and recovery after surgery — including joint replacements and spine procedures. If you're not sure your condition fits, call 561-624-4263 and we'll give you an honest answer."),
        ("How is physical therapy different from a chiropractor?",
         "The biggest difference is the emphasis on active recovery: physical therapy combines hands-on treatment with progressive exercise and movement retraining designed to correct the underlying problem, then discharges you with the tools to stay well. Chiropractic care centers on spinal adjustment. Many patients have benefited from both — but if your goal is lasting strength and independence, that's exactly what physical therapy is built for."),
        ("Does physical therapy hurt?",
         "It shouldn't — the purpose of physical therapy is to reduce pain, though some soreness is normal when stiff joints and weak muscles start working again. Your therapist stays within your tolerance, tells you what each technique should feel like, and adapts the plan immediately based on your feedback."),
        ("How many physical therapy sessions will I need?",
         "It depends on your condition, its severity, and your goals — a recent ankle sprain and a total knee replacement follow very different timelines. After your first evaluation your therapist will recommend a visit frequency and set honest milestones, then re-assess continually so you're never attending sessions you don't need."),
        ("Can physical therapy help me avoid surgery?",
         "In many cases, yes — evidence supports skilled conservative care as the first step for many orthopedic conditions, and a good number of our patients improve enough that surgery is postponed or never needed. It depends on your diagnosis, and we'll always tell you the truth: if therapy isn't moving you forward, we'll coordinate with your physician about next steps."),
        ("What should I wear and bring to a physical therapy appointment?",
         "Wear comfortable clothes you can move in — shorts for knee, hip, or ankle conditions, a loose shirt for shoulder problems — plus supportive sneakers. For your first visit, bring a photo ID, your insurance card, and any referral, prescription, or imaging reports from your physician."),
        ("Is physical therapy covered by Medicare and insurance?",
         "Yes — medically necessary physical therapy is covered by Medicare and most major insurance plans. We accept Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network, workers' compensation, and self-pay; call 561-624-4263 and our front desk will verify your exact physical therapy benefits before your first visit."),
        ("How soon after surgery should I start physical therapy?",
         "That timeline belongs to your surgeon — every procedure has its own protocol, and some begin therapy within days while others protect the repair longer. We follow your surgeon's protocol exactly and coordinate with their office throughout, so bring your post-op paperwork and we'll start you right on schedule."),
        ("Will I do the same exercises every visit?",
         "No — your program progresses as you do. Exercises are advanced, swapped, and progressively loaded as your strength and mobility improve, and hands-on treatment evolves with each phase of healing. We re-evaluate constantly, because repeating the same routine forever is the sign of a plan that has stalled."),
        ("What makes First Rehabilitation's physical therapy different?",
         "One-on-one, hands-on care from a family-owned clinic that has served the Palm Beaches since 1991 — with a 4.9-star Google rating to show for it. And because occupational therapy, certified hand therapy, and a wellness gym share our roof, your physical therapy plan can flow seamlessly into whatever your recovery needs next, including staying strong after discharge."),
    ]),
    ("occupational-therapy", "Occupational Therapy", [
        ("What is occupational therapy?",
         "Occupational therapy helps you regain the ability to do the activities that occupy your daily life — dressing, bathing, cooking, writing, working, caring for your family. An occupational therapist rebuilds those skills by treating strength, coordination, and technique together, and adapts tasks or tools when needed so independence comes back faster."),
        ("What's the difference between occupational therapy and physical therapy?",
         "Physical therapy restores how your body moves — strength, range of motion, balance, and pain-free mechanics. Occupational therapy restores what you can do with that movement: the real-world daily activities like dressing, cooking, and working. Put simply, PT helps you walk to the kitchen; OT helps you cook the meal once you're there. Many patients benefit from both, and at First Rehabilitation the two teams work side by side."),
        ("What conditions and situations does occupational therapy help with?",
         "Occupational therapy helps with stroke recovery, hand and upper-extremity injuries, arthritis that interferes with daily tasks, coordination and cognitive changes, and returning to work after injury — including ergonomic guidance so the problem doesn't come back. If daily life has gotten harder to manage, OT is often the missing piece; call 561-624-4263 to talk it through."),
        ("Who can benefit from occupational therapy?",
         "Anyone whose injury, surgery, illness, or age-related changes are getting between them and everyday activities — from a retiree who wants to button a shirt without pain to a worker recovering from an injury who needs to lift confidently again. If a task that matters to you has become difficult, OT can help."),
        ("Does occupational therapy only deal with work and jobs?",
         "No — that's the most common misconception about OT. The occupation in occupational therapy means anything that occupies your time: dressing, cooking, hobbies, caring for grandkids, and yes, your job too. OT treats your ability to live your daily life, whether or not you're employed."),
        ("Does occupational therapy help after a stroke?",
         "Yes — occupational therapy is a cornerstone of stroke recovery. OT retrains the affected arm and hand, rebuilds daily living skills like dressing and grooming, addresses coordination and cognitive changes, and teaches adaptive techniques that restore independence while recovery continues."),
        ("Can occupational therapy help with arthritis or difficulty doing everyday tasks?",
         "Absolutely. OT teaches joint-protection techniques, builds strength and dexterity, and adapts the way you do painful tasks — from opening jars to gripping tools — so arthritis stops dictating your day. Small changes in technique and equipment often make a dramatic difference."),
        ("Do you provide adaptive equipment recommendations?",
         "Yes — recommending and training you on adaptive equipment is a normal part of occupational therapy here, from dressing aids and built-up grips to strategies that make home tasks safer. We only recommend what genuinely helps, and we teach you to use it properly rather than just handing you a catalog."),
        ("Is occupational therapy covered by insurance and Medicare?",
         "Yes — medically necessary occupational therapy is covered by Medicare and most major plans we accept, including Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network, and workers' compensation. Call 561-624-4263 and our front desk will verify your occupational therapy benefits before you start."),
        ("Do I need a referral for occupational therapy?",
         "It depends on your plan and situation — some insurance plans require a physician referral for occupational therapy coverage, while others don't. The fastest way to know is to call 561-624-4263; our front desk will check your plan's requirements and coordinate any needed referral with your doctor."),
        ("How long does occupational therapy take to work?",
         "It varies with your condition and goals — some patients feel the difference in daily tasks within a few weeks, while recovery from a stroke or major surgery unfolds over months. Your occupational therapist sets specific functional goals at evaluation, measures progress against them, and adjusts the plan so every visit is earning its keep."),
        ("How is occupational therapy at First Rehabilitation coordinated with PT and hand therapy?",
         "As one team under one roof — our founder is an occupational therapist, and our OTs, physical therapists, and Certified Hand Therapist coordinate assessments and treatment plans whenever your recovery needs more than one discipline. You don't carry information between separate clinics; we walk down the hall and talk to each other."),
    ]),
    ("hand-therapy", "Hand Therapy", [
        ("What is hand therapy?",
         "Hand therapy is specialized rehabilitation of the hand, wrist, and arm — the body's most intricate machinery, where dozens of small structures must glide and work together. It blends precise exercise, hands-on treatment, and custom splinting to restore function after injury, surgery, or conditions like arthritis and carpal tunnel."),
        ("What is a Certified Hand Therapist (CHT), and why does it matter?",
         "A Certified Hand Therapist has completed thousands of hours of specialized upper-extremity practice plus a rigorous national exam — one of the most demanding credentials in rehabilitation. It matters because hand recovery is unforgiving: moving too soon can compromise a surgical repair, and moving too late costs motion. That's why area hand surgeons refer post-operative patients specifically to CHTs; ours is Laura Drumm, CHT, who leads the program."),
        ("What conditions does hand therapy treat?",
         "Our hand therapy program treats carpal tunnel syndrome, tendon injuries and repairs, fractures of the hand and wrist, trigger finger, arthritis of the hands and thumbs, nerve conditions, and post-surgical swelling. Whether the cause is injury, surgery, or wear over time, treatment is matched precisely to the tissue that's healing."),
        ("Do you make custom splints or orthoses?",
         "Yes — custom splints and orthoses are fabricated right in our clinic by our hand therapy program. Each is molded to your hand for your specific condition, adjusted as healing progresses, and built to your surgeon's protocol when you're recovering from surgery."),
        ("I'm having hand surgery — when should I start hand therapy?",
         "Your surgeon sets that timeline, and it varies widely by procedure — some repairs begin protected motion within days, while others need a period of immobilization first. We work from your surgeon's protocol and coordinate with their office directly, so ideally get us your surgery details before or right after your procedure, and we'll have your plan and any needed splint ready on schedule."),
        ("Can hand therapy help carpal tunnel without surgery?",
         "Often, yes — especially when symptoms are caught early. Conservative care can include custom night splinting, nerve and tendon gliding exercises, activity and ergonomic changes, and symptom management. If your case turns out to need a surgical consult, we'll say so honestly and coordinate with your physician."),
        ("Can hand therapy help arthritis in my hands and thumbs?",
         "Yes — hand therapy is one of the most effective conservative treatments for hand and thumb arthritis. Joint-protection techniques, targeted strengthening, custom supportive splints, and smart activity modification can reduce pain and keep you doing the things arthritis threatens to take, from opening jars to gardening and golf."),
        ("Do you treat the wrist and elbow too, or only the hand?",
         "We treat the full upper extremity — hand, wrist, forearm, and elbow. The arm works as one connected chain, and conditions like tennis elbow, wrist fractures, and nerve entrapments all fall within our certified hand therapy program's scope."),
        ("How long does hand therapy recovery take?",
         "It depends on the condition and, after surgery, on the structure that's healing — tendon and nerve repairs follow strict tissue-healing timelines that can span weeks to months, while many non-surgical conditions improve faster. Your therapist will map the expected phases at your evaluation, pace treatment to the tissue rather than the calendar, and track your progress honestly."),
        ("Is hand therapy covered by insurance and Medicare?",
         "Yes — hand therapy is covered like other medically necessary therapy services under Medicare and most major plans we accept, including Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network, and workers' compensation. Call 561-624-4263 and our front desk will verify your specific benefits, including any coverage rules for custom splints."),
        ("Do I need a referral for hand therapy?",
         "It depends on your insurance plan, and post-surgical patients typically arrive with a referral and protocol from their surgeon. If you're coming on your own for something like carpal tunnel or arthritis, call 561-624-4263 — our front desk will check whether your plan requires a referral and help arrange one if needed."),
        ("Why choose a certified hand therapy program over general PT for a hand injury?",
         "Because the hand's margin for error is small: dozens of tendons, joints, and nerves work in tight quarters, and generic rehab can cost you motion or stress a repair. A Certified Hand Therapist is trained specifically in these structures and their healing timelines — it's why hand surgeons refer their patients to CHTs. At First Rehabilitation, that expertise comes from Laura Drumm, CHT, with custom in-clinic splinting and a full therapy team behind it."),
    ]),
    ("wellness-gym", "Wellness &amp; Gym", [
        ("What is the wellness and gym program at First Rehabilitation?",
         "Our wellness and gym program is an on-site fitness program inside our North Palm Beach clinic, built to keep you strong after formal therapy ends. It includes personal training, post-rehab exercise, group classes, senior functional fitness, and sports performance work — all guided by a team that knows your rehabilitation history."),
        ("Do I have to be a patient to join the wellness program?",
         "The program is designed first as a continuation for our therapy patients, so the team guiding your training already knows your history. If you haven't been a patient with us and you're interested in joining, call 561-624-4263 — our front desk will walk you through the options."),
        ("What's included in the wellness program?",
         "Personal training, post-rehab exercise programs, group classes, senior functional fitness, and sports performance training — all inside our clinic's on-site gym. Your program is built around your goals and, if you've done therapy with us, your rehab history."),
        ("Is the wellness program supervised?",
         "Yes — training is guided by the First Rehabilitation team in our on-site gym, not left to guesswork. That guidance is the whole point: form, progression, and safety are watched by people who understand how bodies recover and what yours has been through."),
        ("Who is the wellness program for?",
         "Every age and stage — from athletes working on performance to seniors focused on functional fitness and fall prevention. It's especially valuable if you've finished therapy and want to protect the progress you made."),
        ("How is this different from a regular gym?",
         "The difference is who's watching: your training is guided by a rehabilitation team that knows your injury history, your surgical repairs, and your limits — a regular gym doesn't. You get the equipment and the coaching, plus therapists down the hall if a question comes up."),
        ("How do I join the wellness program, and what does it cost?",
         "Call 561-624-4263 and our front desk will explain the current options and pricing and help you get started. We keep it simple — a conversation about your goals, then a program built for you."),
        ("Can I keep exercising at the clinic after I finish therapy?",
         "Yes — that's exactly what our wellness and gym program is for. When you're discharged from therapy, you can continue training on-site with guidance from the same team that guided your rehab, so the strength you rebuilt doesn't fade when the visits end."),
    ]),
    ("getting-started", "Getting Started", [
        ("What services does First Rehabilitation offer?",
         "We offer physical therapy, occupational therapy, certified hand therapy, and an exclusive on-site wellness and gym program — a complete continuum of care under one roof. Family-owned since 1991, we treat everything from back pain and post-surgical recovery to hand injuries, work injuries, and auto accident rehabilitation, then help you stay strong after discharge through our wellness program."),
        ("How do I schedule my first appointment?",
         "Call us at 561-624-4263, or request an appointment through the contact page or the chat assistant on this site — our front desk will follow up promptly to verify your insurance and find a time that works. We're open Monday through Friday, 8:00 AM to 5:30 PM, and Saturday, 8:00 AM to 12:30 PM, at 733 US Highway 1, Suite 2A in North Palm Beach. Free consultations are available — call to schedule one."),
        ("What happens during the first evaluation?",
         "Your first visit is a comprehensive movement-based evaluation: an honest conversation about your history and goals, a hands-on assessment of strength, mobility, and movement patterns, and a proposed plan of care. Whenever appropriate, treatment begins that very first day — and you'll leave knowing what's going on, what the plan is, and what you can start doing at home."),
        ("What should I bring to my first visit?",
         "Bring a photo ID, your insurance card, and any paperwork from your physician — a referral or prescription, imaging reports, or post-surgical protocols. If your visit relates to a work or auto injury, bring your claim information too. Our front desk verifies coverage before you arrive, so billing questions never ambush you."),
        ("What should I wear to therapy?",
         "Comfortable clothing you can move in, plus supportive shoes like sneakers. For lower-body conditions, shorts or loose pants are ideal; for shoulder, arm, or hand conditions, wear a shirt that gives easy access to the area being treated."),
        ("How long are appointments?",
         "Plan on your initial evaluation running longer than a typical follow-up visit, since it includes your history, assessment, and plan of care. Exact visit length depends on your condition and treatment plan — when you schedule, our front desk will tell you how much time to set aside."),
        ("How many visits will I need?",
         "It genuinely varies — recovery depends on your condition, how long you've had it, your goals, and how your body responds. After your evaluation, your therapist will propose a plan with an expected visit frequency and honest milestones, then adjust it based on your actual progress rather than a cookie-cutter schedule."),
        ("Will I see the same therapist each visit?",
         "We're a small, family-owned team, and we prioritize continuity — building your recovery on a relationship with a therapist who knows your history is part of how we work. When more than one of our clinicians is involved in your care, it's a coordinated team approach, never an anonymous hand-off."),
        ("How soon will I feel results?",
         "Many patients notice meaningful change within the first few weeks, but the honest answer is that it varies with your condition, how long you've had it, and consistency with your home program. Your therapist will set realistic milestones at your evaluation and track your progress objectively, so you always know whether the plan is working."),
        ("What is a home exercise program, and do I have to do it?",
         "It's a short, targeted set of exercises your therapist designs for you to do between visits — and yes, it genuinely matters, because the work you do at home reinforces and accelerates everything we do in the clinic. We keep it realistic for your schedule and update it as you progress."),
    ]),
    ("insurance-cost", "Insurance &amp; Cost", [
        ("What insurance plans do you accept?",
         "We accept most major plans: Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network (VACCN), workers' compensation, and self-pay. Coverage details differ plan to plan, so call 561-624-4263 and our front desk will verify your specific benefits before your first visit."),
        ("Do you accept Medicare?",
         "Yes — we accept both Original Medicare and Medicare Advantage plans, and we've cared for Medicare patients since 1991. Medicare covers medically necessary outpatient physical and occupational therapy; our team handles the required physician plan-of-care paperwork with your doctor, and the front desk will explain your benefits before you start."),
        ("How much does therapy cost without insurance, and do you offer self-pay?",
         "Yes, we welcome self-pay patients. Rates depend on the type of care you need, so call 561-624-4263 for current self-pay pricing — our front desk will walk you through the cost up front so there are no surprises."),
        ("Will you verify my insurance benefits before I start?",
         "Yes, always. Before your first appointment our front desk verifies your coverage and explains what your plan pays for, whether you have a copay or deductible, and whether your plan needs a referral — so you know exactly where you stand before treatment begins."),
        ("What is a copay, and will I have one?",
         "A copay is a fixed amount your insurance plan asks you to pay at each visit — the amount is set by your plan, not by the clinic, and some plans have none for therapy. Whether you'll have one depends entirely on your specific coverage, which is exactly what our front desk checks when they verify your benefits — call 561-624-4263 and we'll tell you before your first visit."),
        ("Do you treat workers' compensation cases?",
         "Yes — we've handled workers' compensation rehabilitation for decades. Treatment is built around the physical demands of your actual job, and we provide the objective progress documentation your case requires while coordinating with your physician, adjuster, and case manager for a safe return to work."),
        ("Do you treat auto accident and personal injury cases?",
         "Yes. Even a minor collision can leave lasting pain, and symptoms often surface days later, so early evaluation matters. We provide comprehensive rehabilitation from whiplash to complex multi-area injuries, document your recovery objectively, and communicate with your physician and representatives as your claim requires."),
    ]),
    ("policies-logistics", "Policies &amp; Logistics", [
        ("Where are you located, and is there parking?",
         "We're at 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408 — convenient to North Palm Beach, Palm Beach Gardens, Juno Beach, Jupiter, and West Palm Beach. Call 561-624-4263 before your first visit and our front desk will point you right to the door, including where to park."),
        ("What are your hours?",
         "We're open Monday through Friday from 8:00 AM to 5:30 PM, and Saturday from 8:00 AM to 12:30 PM; we're closed on Sunday. You can reach the front desk at 561-624-4263 during those hours, or send a request through this site anytime."),
        ("Do you offer weekend or evening appointments?",
         "Our hours are Monday through Friday, 8:00 AM to 5:30 PM, plus Saturday mornings from 8:00 AM to 12:30 PM. If those hours are tight for your schedule, call 561-624-4263 — our front desk will work with you to find the most workable time."),
        ("What is your cancellation policy?",
         "If you can't make a visit, call us at 561-624-4263 as early as you can and we'll reschedule you — consistent attendance is one of the biggest drivers of a good outcome, so we'll always help you find another time. Our front desk will go over scheduling and cancellation details when you book your first appointment."),
        ("How do I access the patient portal?",
         "Click the Portal link in the menu at the top of this site — it takes you to our patient portal, powered by SPRY. If you have any trouble logging in, call the front desk at 561-624-4263 and we'll get you set up."),
        ("How do I ask about my home exercises between visits?",
         "Just call us at 561-624-4263 — the front desk will get your question to your therapist, so you're never stuck guessing between visits. Bring the question to your next appointment too, and your therapist will review your form in person."),
    ]),
    ("about-clinic", "About Our Clinic", [
        ("How long has First Rehabilitation been in business?",
         "We've been serving the Palm Beaches since 1991 — more than three decades of family-owned, independent care under the same name and philosophy. Founder Dave Kashuba, Ph.D., an occupational therapist, has personally treated more than 87,000 patients over his career, and the practice has cared for more than 180,000."),
        ("Who owns and runs the clinic?",
         "First Rehabilitation is family-owned and operated, founded in 1991 by Dave Kashuba, Ph.D., a practicing occupational therapist. He leads a close-knit team of physical and occupational therapists — including Laura Drumm, CHT, our Certified Hand Therapist — whom you can meet on our About page."),
        ("What makes First Rehabilitation different from other clinics?",
         "We're family-owned and operated since 1991, with one-on-one, hands-on care, a 4.9-star Google rating, and a rare combination under one roof: physical therapy, occupational therapy, certified hand therapy, and a wellness gym to keep you strong after discharge. Our motto says it best — our people make the difference."),
        ("What is the Pain 2 Power podcast?",
         "Pain 2 Power is our podcast, hosted by founder Dr. Dave Kashuba with co-host Mike McGann, covering the world of physical rehab and wellness with some of the sharpest minds in medicine. New episodes air Saturdays at 8:30 AM on 100.3 Legends Radio — you can listen live at legendsradio.com — and every episode streams on Spotify or right on our Podcast page."),
        ("What areas do you serve?",
         "From our North Palm Beach clinic we serve the greater Palm Beaches: North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, and West Palm Beach. We're centrally located at 733 US Highway 1, Suite 2A, right on US Highway 1."),
        ("Are you accepting new patients?",
         "Yes — we're welcoming new patients now. Call 561-624-4263 or request an appointment through this site, and our front desk will verify your insurance and get you scheduled promptly."),
    ]),
]

# Flat list (all categories) — feeds the assistant knowledge base and the
# single comprehensive FAQPage schema.
FAQS = [qa for _sid, _title, _pairs in FAQ_CATEGORIES for qa in _pairs]

def _faq_plain(s):
    """Plain-text version of a question/answer for JSON-LD."""
    import re as _re
    return html.unescape(_re.sub(r"<[^>]+>", "", s)).strip()

def faq_schema(pairs):
    """FAQPage JSON-LD <script> for a list of (question, answer) pairs."""
    import json as _json
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": _faq_plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": _faq_plain(a)}}
            for q, a in pairs
        ],
    }
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

ORG_ID = "https://www.firstrehabnpb.com/#organization"
ORG_REF = {"@id": ORG_ID}

def person_schema():
    """Person JSON-LD for every named clinician/leader (E-E-A-T).

    Credentials were verified 2026-10-14 against the NPPES NPI Registry (licence type
    and, where listed, the credential field) plus each clinician's public profile:
    David Kashuba OTR (NPI 1679603468; Ph.D. per his own profile), Kayla Dorsey PT, DPT
    (NPI 1689128993), Logan Van Sant PT (NPI 1962367136; DPT per Nick), Joan Janik
    licensed OT (NPI 1578393849; OTD per Nick), Laura Drumm OTR (NPI 1861459695;
    MS, OTR/L, CHT, CLT per her public profile). Licence NUMBERS are deliberately
    not published. Keys are TEAM slugs, so a display-name change cannot orphan them.
    """
    import json as _json
    knows = {
        "david-kashuba": ["Occupational Therapy", "Outpatient Rehabilitation", "Clinic Leadership"],
        "nick-kashuba": ["Healthcare Operations", "Patient Experience"],
        "logan-van-sant": ["Physical Therapy", "Orthopedic Rehabilitation"],
        "kayla-dorsey": ["Physical Therapy", "Orthopedic Rehabilitation", "Post-Surgical Rehabilitation"],
        "joni-janik": ["Occupational Therapy", "Activities of Daily Living", "Stroke Recovery"],
        "laura-drumm": ["Certified Hand Therapy", "Custom Splinting", "Upper Extremity Rehabilitation"],
    }
    creds = {
        "david-kashuba": ["Doctor of Philosophy (Ph.D.)", "Occupational Therapist, Registered (OTR)"],
        "kayla-dorsey": ["Doctor of Physical Therapy (DPT)", "Licensed Physical Therapist (PT)"],
        "logan-van-sant": ["Doctor of Physical Therapy (DPT)", "Licensed Physical Therapist (PT)"],
        "joni-janik": ["Doctor of Occupational Therapy (OTD)", "Licensed Occupational Therapist"],
        "laura-drumm": ["Master of Science (MS)", "Occupational Therapist, Registered and Licensed (OTR/L)",
                        "Certified Hand Therapist (CHT)", "Certified Lymphedema Therapist (CLT)"],
    }
    people = []
    for t in TEAM:
        slug, role = t["slug"], t["role"]
        # Prefer the real long-form bio once the owner supplies it.
        desc = t["bio"] or t["blurb"]
        p = {"@type": "Person",
             "@id": f"https://www.firstrehabnpb.com/about.html#{slug}",
             "name": _faq_plain(t.get("legal_name") or t["name"].split(",")[0]),
             "jobTitle": _faq_plain(role),
             "description": _faq_plain(desc),
             "worksFor": ORG_REF,
             "knowsAbout": knows.get(slug, ["Rehabilitation"])}
        if t.get("alt_name"):
            p["alternateName"] = t["alt_name"]
        if "," in t["name"]:
            p["honorificSuffix"] = _faq_plain(t["name"].split(",", 1)[1].strip())
        if slug in creds:
            p["hasCredential"] = [{"@type": "EducationalOccupationalCredential", "name": c}
                                  for c in creds[slug]]
        people.append(p)
    data = {"@context": "https://schema.org", "@graph": people}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def therapy_schema(slug, title, lede):
    """MedicalTherapy JSON-LD for a service page, provided by our org."""
    import json as _json
    data = {"@context": "https://schema.org", "@type": "MedicalTherapy",
            "@id": f"https://www.firstrehabnpb.com/services/{slug}.html#therapy",
            "name": _faq_plain(title),
            "description": _faq_plain(lede),
            "provider": ORG_REF,
            "areaServed": ["North Palm Beach", "Palm Beach Gardens", "Jupiter", "Juno Beach",
                           "Tequesta", "Palm Beach Shores", "Riviera Beach", "West Palm Beach"]}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def condition_schema(slug, name, lede, svc_slug, svc_name):
    """MedicalCondition JSON-LD mapping condition -> treatment -> our clinic."""
    import json as _json
    data = {"@context": "https://schema.org", "@type": "MedicalCondition",
            "name": _faq_plain(name),
            "description": _faq_plain(lede),
            "possibleTreatment": {"@type": "MedicalTherapy",
                                  "@id": f"https://www.firstrehabnpb.com/services/{svc_slug}.html#therapy",
                                  "name": svc_name,
                                  "provider": ORG_REF}}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def breadcrumb_schema(items):
    """BreadcrumbList JSON-LD. items = [(name, path-from-root or "" for home)]."""
    import json as _json
    base = "https://www.firstrehabnpb.com"
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": _faq_plain(n),
                 "item": (base + "/" + u) if u else base + "/"}
                for i, (n, u) in enumerate(items)]}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def build_faq():
    total = len(FAQS)
    bubbles = (f'<button type="button" class="faq-bubble active" data-cat="all" aria-pressed="true">'
               f'All Questions <span class="fb-count">({total})</span></button>')
    bubbles += "".join(
        f'<button type="button" class="faq-bubble" data-cat="{sid}" aria-pressed="false">{title} <span class="fb-count">({len(pairs)})</span></button>'
        for sid, title, pairs in FAQ_CATEGORIES
    )
    sections = ""
    for sid, title, pairs in FAQ_CATEGORIES:
        items = "".join(
            f'<details class="faq-item reveal" data-cat="{sid}"><summary>{q}</summary><div class="faq-a">{a}</div></details>'
            for q, a in pairs
        )
        sections += f'''
  <section class="faq-cat" id="{sid}" aria-labelledby="{sid}-h" data-cat-section="{sid}">
    <div class="faq-cat-head"><h2 id="{sid}-h">{title}</h2><span class="faq-count">{len(pairs)} answers</span></div>
    <div class="faq-list">{items}</div>
  </section>'''
    body = f"""
<main>
{page_hero("Questions, Answered", "Frequently Asked <em class='accent'>Questions</em>",
  f"{total} real answers about physical therapy, occupational therapy, hand therapy, wellness, insurance, and what to expect — filter by topic or search below.",
  '<div class="crumbs"><a href="/">Home</a> / FAQ</div>')}
<div class="faq-jump-bar">
  <div class="faq-jump" role="group" aria-label="Filter FAQs by category">{bubbles}</div>
</div>
<section class="section">
  <div class="wrap">
    <div class="faq-toolbar reveal">
      <label class="sr-only" for="faq-search">Search the FAQs</label>
      <input type="search" id="faq-search" class="faq-search" placeholder="Search questions&hellip; (e.g. Medicare, referral, splint)" autocomplete="off">
      <div class="faq-tools">
        <button type="button" class="faq-tool" id="faq-expand">Expand all</button>
        <button type="button" class="faq-tool" id="faq-collapse">Collapse all</button>
      </div>
    </div>
    <p class="sr-only" aria-live="polite" id="faq-live"></p>
    <p class="faq-empty faq-hidden" id="faq-empty">No questions match your search — try a different word, or call <a href="tel:+15616244263">561-624-4263</a> and ask us directly.</p>
    {sections}
  <div class="center mt-3 reveal"><p class="lede" style="margin:0 auto 1.2rem;">Still have a question?</p>
  <a class="btn btn-ink" href="contact.html">Contact Us <span class="arr">&rarr;</span></a></div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("faq.html",
          head("Physical Therapy FAQ | First Rehabilitation North Palm Beach",
               f"{total} answers about physical therapy, occupational therapy, hand therapy, wellness, insurance, and cost at First Rehabilitation of North Palm Beach.",
               canonical="faq.html",
               extra_schema=faq_schema(FAQS) + breadcrumb_schema([("Home", ""), ("FAQ", "faq.html")]))
          + nav(0) + body + footer(0))

def build_contact():
    body = f"""
<main>
{page_hero("We're Here to Help", "Start Your <em class='accent'>Recovery Today</em>",
  "Request an appointment below, call, or stop by — our front desk will help you verify insurance and find a time that works.",
  '<div class="crumbs"><a href="/">Home</a> / Contact</div>')}
<section class="section">
  <div class="wrap contact-grid">
    {appt_form(wrapped=False)}
    <div class="reveal d2">
      <div class="contact-card" style="margin-bottom:1.5rem;">
        <h3>First Rehabilitation of North Palm Beach</h3>
        <div class="c-row"><span class="c-label">Address</span><span>733 US Highway 1, Suite 2A<br>North Palm Beach, FL 33408</span></div>
        <div class="c-row"><span class="c-label">Phone</span><a href="tel:+15616244263">{PHONE}</a></div>
        <div class="c-row"><span class="c-label">Fax</span><span>{FAX}</span></div>
        <div class="c-row"><span class="c-label">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="c-row"><span class="c-label">Hours</span><span>Monday – Friday, 8:00 AM – 5:30 PM<br>Saturday, 8:00 AM – 12:30 PM</span></div>
        <div class="c-row"><span class="c-label">Consults</span><span>Free consultations available — call to schedule</span></div>
        <div class="c-row"><span class="c-label">Portal</span><a href="{PORTAL}" target="_blank" rel="noopener">Patient Portal &rarr;</a></div>
        <a class="btn btn-coral mt-2" href="tel:+15616244263">Call to Book <span class="arr">&rarr;</span></a>
        <p style="margin-top:1rem;font-size:0.88rem;color:var(--muted);">First Rehabilitation of North Palm Beach is an independent, family-owned clinic founded in 1991 by David Kashuba, Ph.D., OTR. We have one location, at 733 US Highway 1, Suite 2A, and are not affiliated with other clinics that use a similar name.</p>
      </div>
      <iframe class="map-frame" src="{MAPS_EMBED}" title="Map to First Rehabilitation of North Palm Beach" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="min-height:300px;"></iframe>
    </div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("contact.html",
          head("Contact | First Rehabilitation of North Palm Beach",
               "Contact First Rehabilitation of North Palm Beach: 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408. Call 561-624-4263 to book your appointment.",
               canonical="contact.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Contact", "contact.html")]))
          + nav(0) + body + footer(0))

# ----------------------------------------------------------------------------
# BLOG
# ----------------------------------------------------------------------------

BLOG_POSTS = {
    "pain-2-power-ep20-kendzierski": {
        "title": "How Screening Every Six Months Caught Maria Kendzierski&rsquo;s Second Breast Cancer Early",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "Dave&rsquo;s cousin Maria Kendzierski on two breast cancer diagnoses, screening every six months at Roswell Park, chemo, radiation and why she rang the bell twice.",
        "body": """
<p>Maria Kendzierski spent years going back to Roswell Park every six months for a mammogram or an MRI, and she did not enjoy the MRIs. So she asked her doctor how long she had to keep doing them. The answer was a question: &ldquo;how long do you not want to have cancer?&rdquo; Maria&rsquo;s reply was &ldquo;fair enough.&rdquo;</p>
<p>That exchange is the heart of this week&rsquo;s Pain 2 Power. Maria is Dave&rsquo;s cousin, she has been diagnosed with breast cancer twice, and both times it was a scan, not a lump she could feel, that found it.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>A cousin from Buffalo, a survivor sweatshirt, and October</h2>
<p>Dave grew up in Buffalo in what he called a really tight close family, with 12 or 13 cousins who all hung out and, by his account, all got in trouble together. Maria was the exception, he said, smarter than the rest of them. &ldquo;She was able to talk her way out of everything.&rdquo; The family tie runs double: Maria&rsquo;s mother and Dave&rsquo;s mother are twins.</p>
<p>Maria joined Dave and Mike McGann over Zoom from Buffalo, where she still lives and still roots for the Bills and the Sabres. (&ldquo;There&rsquo;s always next year,&rdquo; she said.) She opened by pointing at what she was wearing. &ldquo;I have my survivor sweatshirt on, you can&rsquo;t see it, this is what a survivor looks like.&rdquo;</p>
<p>The timing was deliberate. October is Breast Cancer Awareness Month, and the show had already given two October episodes to it: radiologist Dr. Don Goodwin on screening, then a dietitian and a Pilates studio owner on food and movement. Dave opened with numbers of his own, saying there are over 400,000 cases diagnosed in women in America and 42,000 deaths a year. Then he explained why he had asked Maria on. Watching from far away, he said, the family prayed for her, and through all of it &ldquo;she always had a smile. She always had a good attitude.&rdquo;</p>
<h2>2015: a yearly mammogram finds something at stage zero</h2>
<p>Maria&rsquo;s first diagnosis came out of a routine she already had. &ldquo;I go every year for my checkups, my mammograms,&rdquo; she said. In 2015 that yearly mammogram showed a suspicious nodule, more tests followed, and the result was stage zero. She had never heard of stage zero. Neither had Mike.</p>
<h3>A name that sounded worse than it was</h3>
<p>The diagnosis was lobular carcinoma in situ, LCIS for short, and Maria was honest about how it landed. &ldquo;And has the word carcinoma right in it. So, of course, I&rsquo;m freaking out.&rdquo; She said her doctor told her it was just the name they give it, and that there had been efforts to change the name that had not gone anywhere. As she described it, the nodule was encapsulated within itself. They took it out, nothing had spread around it, and there was no further treatment except one medication.</p>
<h3>Five years of tamoxifen</h3>
<p>That medication was tamoxifen. Maria had come prepared, and she read from her notes: it &ldquo;blocks the effects of estrogen so that it the estrogen doesn&rsquo;t attach to cancer cells.&rdquo; She took it for five years. When the five years ended, she said, she went through a &ldquo;what now&rdquo; moment, because the medication had been her crutch. That feeling comes back later in her story.</p>
<h2>Every six months at Roswell Park, and the one word on the phone</h2>
<p>Because of the first diagnosis, Maria was screened every six months, alternating between mammograms and MRIs. She counts herself lucky on this point. Roswell Park, which she described as a world class comprehensive cancer center, is in her backyard in Buffalo. That is where her doctor gave her the line about how long she wanted to not have cancer.</p>
<p>In June or July of 2024, an MRI found something suspicious. More biopsies followed, and Maria knew what the call would sound like before it came. &ldquo;I waited for one word, unfortunately, and as soon as the radiologist said unfortunately, I didn&rsquo;t hear anything else after that.&rdquo;</p>
<p>She credits a patient portal with getting her through the next few weeks, since she could read every report as it came in. And she credits the six month schedule with the outcome. &ldquo;Thankfully though because I was going every six months, they caught it early,&rdquo; she said.</p>
<h3>Her sister, her partner in crime, and a decision already made</h3>
<p>Maria walked into the treatment conversation with two people. She introduced her sister and her partner in crime to the doctor as &ldquo;my secretary and my treasurer.&rdquo; She had already made up her mind. &ldquo;I said even if they tell me I don&rsquo;t need chemo, I&rsquo;m gonna get chemo because I want this out of me.&rdquo; She was ready for a double mastectomy if that was what it took.</p>
<p>It wasn&rsquo;t. Her doctors recommended a lumpectomy, not a mastectomy. She described the test result that settled the chemo question as her &ldquo;onco score&rdquo;: she said a score of 25 or higher meant they recommend chemo, and hers was 39. &ldquo;So it wasn&rsquo;t even my choice,&rdquo; she said.</p>
<h2>A lumpectomy in October, chemo on her birthday in November</h2>
<p>The order went like this. Lumpectomy in October. Chemotherapy starting in November, on her birthday. (&ldquo;Happy birthday to me.&rdquo;) Eight rounds. Then five weeks of radiation. She lost her long curly hair, which she waved off: it&rsquo;s just hair, and it came back. Now, she told Dave, she looks a lot more like her mom.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Maria Kendzierski's two diagnoses as she described them">
<table>
<caption>Maria Kendzierski&rsquo;s two breast cancer diagnoses and treatment, as she described them on Pain 2 Power Episode 20. Dates and details are hers, as stated on air.</caption>
<thead><tr><th scope="col">When</th><th scope="col">What she said happened</th></tr></thead>
<tbody>
<tr><th scope="row">2015</th><td>Yearly mammogram finds a suspicious nodule; diagnosed as lobular carcinoma in situ, stage zero; nodule removed</td></tr>
<tr><th scope="row">The next five years</th><td>Tamoxifen, with no further treatment</td></tr>
<tr><th scope="row">After that</th><td>A mammogram or an MRI every six months at Roswell Park in Buffalo</td></tr>
<tr><th scope="row">June or July 2024</th><td>An MRI finds something suspicious; biopsies follow, and the cancer is caught early</td></tr>
<tr><th scope="row">October 2024</th><td>Lumpectomy</td></tr>
<tr><th scope="row">November 2024 onward</th><td>Eight rounds of chemotherapy, starting on her birthday, then five weeks of radiation</td></tr>
<tr><th scope="row">Today</th><td>Rang the bell after chemo and again after radiation; still screened every six months</td></tr>
</tbody>
</table>
</div>
<h3>The shots were harder than the chemo</h3>
<p>Mike asked how the treatment affected her. Beyond being tired all the time (some days she slept 13 hours), Maria said the chemotherapy itself was not as bad as she expected. The worst part was the injections she needed to keep her white blood cell count where it had to be for the next round. For five days after each one, she said, she had muscle aches, joint aches, everything. &ldquo;I would be literally sitting in a chair just moaning. I didn&rsquo;t even realize I was moaning from pain.&rdquo; What she kept telling herself was that the pain meant the drugs were working.</p>
<p>She had also dreaded the room. She had pictured what she had seen on TV, a big room full of chairs and other people getting chemo at the same time. Her treatment looked nothing like that. She had her own little cubby, staff brought drinks and snacks, she could bring someone with her, and there was a TV. &ldquo;It certainly wasn&rsquo;t the Ritz,&rdquo; she said, but it wasn&rsquo;t as bad as she thought.</p>
<h3>Forty five minutes in the car, ten minutes on the table</h3>
<p>Radiation meant going every day for five weeks. The drive to the hospital was 45 minutes, and the treatment itself put her on the table for about 10. &ldquo;I was in the car a lot longer than from literally the time I got to the hospital,&rdquo; she said. She described her side effects as minimal and was quick to add that she knows not everyone gets off that lightly.</p>
<h2>The waiting room that changed her mind about meeting people</h2>
<p>Maria did not want to make friends at radiation. &ldquo;I didn&rsquo;t want to tell my story, I didn&rsquo;t want to hear your story,&rdquo; she said. She wanted to get in, get it done and get out. The schedule did not cooperate. Radiation runs at the same time every day, so you sit in the same waiting room with the same people, and sooner or later you talk.</p>
<p>On her first day she walked into the locker room unsure of what to do, and a woman already there asked if it was her first day. Maria still talks to her. Over those weeks she got to know the woman&rsquo;s mother and husband too, just from sitting in that waiting room. Her verdict on her own first instinct was blunt: &ldquo;bad on me for not wanting to meet people because you need to surround yourself with people.&rdquo;</p>
<p>Mike picked up on that near the end of the hour. What struck him was the change, from someone who did not want to be part of any of it to someone whose eyes fill up when a stranger rings the bell. In his words, it can &ldquo;bring us closer to humanity if you respond to it.&rdquo;</p>
<h3>The family that showed up</h3>
<p>Dave talked about Maria&rsquo;s siblings, who have done cancer research races and fundraising for years, and about how hard it was to be far away with nothing to do but pray. Maria said her siblings each took a turn going with her to chemo, and they pitched in at home because she has two dogs who could not be left alone all day. Both of her sisters told her they would have traded places with her in a heartbeat. &ldquo;And I know they would, but I&rsquo;m thankful they didn&rsquo;t have to.&rdquo;</p>
<h2>Out of the online groups, and away from Dr. Google</h2>
<p>Maria had written down a short list of things she learned, and some of it came from her oncologist. One piece of advice was to be careful with online support groups. Her explanation used a restaurant. If a meal is great, most people do not rush online to post a glowing review. If it was horrible, they do. Some cancer groups on Facebook and social media work the same way, she said: &ldquo;misery loves company.&rdquo; She left a lot of them and kept a few that she called really awesome.</p>
<p>&ldquo;I stayed away from Dr. Google,&rdquo; she said, and she was warned about that right up front. She noted that Dave knows the feeling from his own research, how you can go down so many rabbit holes. Her approach was to avoid it and let her doctors tell her what to expect.</p>
<p>It fits how we try to work at the clinic, too. If you have a question about your own situation, the best person to ask is the clinician who has actually examined you.</p>
<h3>Tough mothers, and why not me</h3>
<p>Maria said both of their mothers had a very high tolerance for pain, and that she and her siblings had no choice but to be tough. She also admitted the &ldquo;why me&rdquo; never fully goes away. Her answer to it was practical. She was working part time at a winery when she was diagnosed, so she had the time to be sick and the time to go to treatment, while her siblings all work full time. &ldquo;So why not me if it had to be one of us, let it be me.&rdquo;</p>
<p>One night, out in the backyard waiting on a dog who sometimes refuses to go to the bathroom, she looked up and asked the universe if everything was going to be okay. A shooting star crossed the sky. &ldquo;I was like, okay, I think I&rsquo;m gonna be okay.&rdquo; Mike asked how much attitude had to do with it. &ldquo;It&rsquo;s huge,&rdquo; Maria said. Mike went a step further and said he could see it as part of why her side effects were milder. That was his impression, offered as his own, and it is not a medical claim anyone on the show made.</p>
<h2>Ringing the bell twice, and the radiologist who said too soon</h2>
<p>Dave asked the question he had saved: how did it feel to ring the bell? People kept asking whether she would do it after chemo or after radiation. She did both, because she went through two different stages of treatment, and her siblings were there each time. At Roswell, she said, hearing someone ring that bell on her way to an ordinary appointment makes her eyes tear up every time. &ldquo;And this time it was me.&rdquo; People in the lobby stopped what they were doing to clap, and strangers came up to congratulate her.</p>
<p>Then came the same feeling she had after tamoxifen. &ldquo;Oh my gosh, now what?&rdquo; She had gone there every day for five weeks, and that routine had been her crutch. She still goes back every six months.</p>
<p>She also had a story she said Dave would appreciate. Her radiologist, whom she saw once a week after treatment, walked in on her first day and said, &ldquo;well, you&rsquo;re a little glow, you have a little glow to you.&rdquo; She just looked at him. His follow up was &ldquo;too soon?&rdquo; &ldquo;I get that,&rdquo; she said. Doctors in that job, as she put it, deal with a lot.</p>
<p>Looking back on the gap between her diagnosis in August and her surgery in October, she said she wanted it out of her right away. Then she reasoned that if it were that bad, they would have fast tracked her into surgery. &ldquo;I kind of put my faith in my doctors and I put my faith in God,&rdquo; she said.</p>
<h2>Under 40, and why you can&rsquo;t always feel it</h2>
<p>Two things frustrated Maria along the way, and both are about catching cancer early. The first was age. &ldquo;I met quite a few people under 40 who&rsquo;ve been diagnosed with breast cancer and they don&rsquo;t even want you to have a mammogram until you&rsquo;re 40,&rdquo; she said. &ldquo;Well guess what, people under 40 are getting breast cancer, so something needs to change.&rdquo;</p>
<p>The second is the one that stays with you. Women have to know their own bodies, she said, but self exams have limits. &ldquo;Even after they told me exactly where on my breast my tumor was, I couldn&rsquo;t feel it.&rdquo;</p>
<p>When screening should start is a conversation for you and your own doctor, and we are a therapy clinic, so we will not pretend to answer it here. If you want to hear it from a specialist, listen to Episode 17 with Dr. Don Goodwin on <a href="../podcast.html">the podcast page</a>. On that episode he walks through how the US Preventive Services Task Force moved its starting age to 40, why groups like the American College of Radiology say every year from 40, and when ultrasound or MRI gets added to a mammogram. You can also read more about him on <a href="../guests/goodwin.html">his guest page</a>. Episode 18, with dietitian Elyse Marrone and Danielle Armstrong of Pilates Life, picks up the other half: food, movement and recovery during and after treatment.</p>
<h2>Elmer, the John Deere, and the joke of the week</h2>
<p>Dave had said earlier that he came in with so many things he wanted to ask, &ldquo;but I&rsquo;m more interested in listening to you.&rdquo; He did keep one tradition. Listeners, he said, mostly send him bad dad jokes instead of questions, so he closed with one.</p>
<p>He was at the family&rsquo;s small lake house in Alabama when he saw his neighbor Elmer bending down next to a John Deere tractor, holding a box of heart shaped chocolates under one arm and flowers in the other. Elmer explained that his wife had lost the glow in her eyes, and a friend had told him what to do: &ldquo;you got to be more romantic to attract her.&rdquo; Say it out loud if it takes a second.</p>
<p>Mike said it couldn&rsquo;t be a better way to wrap it up. There were I love yous on both ends of the Zoom, and the show signed off with a reminder to get your mammograms.</p>
<p>You can read more about Maria on <a href="../guests/kendzierski.html">her guest page</a>, listen to the full episode on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch it in our <a href="../videos.html">video library</a>, or catch the show live Saturdays at 8:30 AM on 100.3 Legends Radio.</p>
<p>We are a physical, occupational and hand therapy clinic on US-1 in North Palm Beach, and cancer care belongs with your oncology team. If you are getting back to everyday life after treatment and something aches, feels stiff, or just won&rsquo;t cooperate the way it used to, ask your doctor whether therapy makes sense for you, then call us at 561-624-4263. You can read how our <a href="../services/physical-therapy.html">physical therapy</a> works, see how we stay with patients through our <a href="../services/wellness.html">wellness program</a> once therapy ends, or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep18-marrone-armstrong": {
        "title": "What You Can Control After Breast Cancer: Elyse Marrone and Danielle Armstrong",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "Jupiter dietitian Elyse Marrone and Pilates Life owner Danielle Armstrong join Dave and Mike on food, movement and sleep before, during and after breast cancer.",
        "body": """
<p>The week before, radiologist Dr. Don Goodwin had spent an hour on Pain 2 Power talking about breast cancer screening. This week Dave and Mike wanted the other half of the conversation: once you know the risk is real, what can you actually do about it? Dave brought two friends to answer. Elyse Marrone is a registered dietitian who sees patients in Jupiter, and Danielle Armstrong owns Pilates Life on Northlake in Palm Beach Gardens.</p>
<p>Between them they covered food, movement and sleep before, during and after a diagnosis, plus one of the better stories we have heard on the show, about a dancer, a radical mastectomy and Joseph Pilates himself.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Starting from 400,000 diagnoses a year</h2>
<p>Dave opened with the number he could not shake from the week before. By his count there are over 400,000 cases of breast cancer diagnosed in women in the United States. Mike called it a horrifying number and admitted it is hard to get your head around.</p>
<p>What bothered Dave more was the word &ldquo;cure.&rdquo; As he put it on air, a cure rate often means living about five years, and that, in his view, is not a cure. So he steered the hour toward the things people can influence. There are plenty of factors you can&rsquo;t control, he said. But eating well, taking care of yourself, not smoking and not drinking too much all count, and he put the share of risk those habits touch at coming up on 40%.</p>
<p>Mike had been reading about the same idea that week. We pick up cancer cells all the time, he said, and the immune system finds and clears them in small doses. Dave ran through the cells he had been reading about, the CD4 positive and CD8 positive T cells and the macrophages he called the pig of the blood, because it eats everything. The point of the whole show followed from there. Give the body the right environment and it does a lot of this work on its own.</p>
<p>Those figures are Dave&rsquo;s, as he said them on the show. If you want the screening side of the story first, it is the episode just before this one on our <a href="../podcast.html">Pain 2 Power podcast page</a>.</p>
<h2>Elyse Marrone&rsquo;s triple HD plan and the seven pillars</h2>
<p>Elyse introduced herself as a registered dietitian who is functionally and integratively trained. In practice that means she does not stop at matching your plate to the current food pyramid or whatever diet is in fashion. She looks at all seven parts of your lifestyle and asks how to get each one working. Quality of life, she said, should travel with quantity of life.</p>
<p>Then she gave the line that became the episode&rsquo;s first clip. &ldquo;So I say I want to be healthy, healthy, healthy, dead.&rdquo; She doesn&rsquo;t want the long slide down. She calls it the triple HD plan. Mike&rsquo;s summary was quick: &ldquo;We&rsquo;d rather thrive than just survive.&rdquo;</p>
<p>The seven pillars are the backbone of every appointment she runs. She does look at labs. Her view is that the labs move with the pillars, and Dave added that they can move quickly, in either direction.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Elyse Marrone's seven pillars of health and what was said about each">
<table>
<caption>The seven pillars of health as Elyse Marrone, RD/LDN, CGP, listed them on Pain 2 Power Episode 18, with what came up about each pillar during the hour. Nothing here is a recommendation for your own care.</caption>
<thead><tr><th scope="col">Pillar</th><th scope="col">What was said on the show</th></tr></thead>
<tbody>
<tr><th scope="row">Food first</th><td>Dave listed high fiber, omega-3 fatty acids, cruciferous vegetables like broccoli and cauliflower, and less alcohol and processed meat</td></tr>
<tr><th scope="row">Exercise</th><td>Dave: exercise &ldquo;makes what we eat turn into gold&rdquo;; Elyse said it can also increase deep sleep</td></tr>
<tr><th scope="row">Sleep</th><td>Deep sleep, wearables like the Oura ring and the Whoop band, and blue light blocker glasses from 8 o&rsquo;clock in the evening</td></tr>
<tr><th scope="row">Stress management</th><td>Elyse: stress raises cortisol, which can set off a cascade of events</td></tr>
<tr><th scope="row">Supplementation</th><td>Elyse checks vitamin D for the immune system and discussed DIM, an extract of Brussels sprouts</td></tr>
<tr><th scope="row">Hydration</th><td>Named as one of the seven; not discussed in detail on this episode</td></tr>
<tr><th scope="row">Community</th><td>Named as one of the seven; Mike admitted he is good at about two of the pillars</td></tr>
</tbody>
</table>
</div>
<h3>Why the first look is at the gut</h3>
<p>Dave asked what happens when someone newly diagnosed with breast cancer walks into her office. Her first step is what she calls looking at their terrain, and that usually means the gut. &ldquo;So like you said we all get cancer all the time and our immune system fights it,&rdquo; she said. &ldquo;80, 90% of your immune system is in your gut. I&rsquo;m always looking at the gut.&rdquo;</p>
<p>From there she works through the rest. What are they eating? Are they sleeping? Are they managing stress? She also makes sure vitamin D levels are where they should be.</p>
<h3>DIM, hormones and a Polish plate of Brussels sprouts</h3>
<p>Dave had mentioned cruciferous vegetables, and Elyse picked that up with DIM, short for diindolylmethane. She described it as an extract of Brussels sprouts that helps the body process estrogen down to a less toxic form, and she said she has people taking or making estrogen take it daily. That is her clinical approach as a dietitian. Supplements are a conversation for you and your own provider, so please don&rsquo;t read it as a prescription.</p>
<p>Dave saw his chance. The way a Polish family makes Brussels sprouts, he said, is fried in bacon grease, with bacon. Elyse was gracious about it (that might be the only way some people will eat them) and then made the practical point. &ldquo;But to get enough DIM you&rsquo;d have to eat many many pounds of Brussels sprouts.&rdquo; Nobody is eating pounds of them, bacon or no bacon.</p>
<p>On hormones, she was clear about her lane. She does not prescribe them. She works alongside providers who do, and keeps an eye on markers like sex hormone binding globulin so the hormones a patient is making or taking can do their job. A new breast cancer diagnosis changes that appointment, she said, because most of those patients are off hormones by then.</p>
<h2>Danielle Armstrong and the women she trains through treatment</h2>
<p>Danielle&rsquo;s path to the microphone ran through our front door. She was seeing Dr. Paula Newmark, a chiropractor in Jupiter, for a shoulder problem, and Paula sent her to Dave, who got her out of a frozen shoulder. She is a former dancer, which explains a lot about how she moves and teaches.</p>
<p>She described her clients plainly. This is a big retirement area, and people come to Pilates as gentle exercise that helps with ordinary tasks, reaching a shelf, carrying groceries. Then she described this year. &ldquo;I found this year in particular I&rsquo;ve had a lot of women, I&rsquo;d say mid 60s to mid 70s who have been diagnosed with breast cancer,&rdquo; she said. Her studio&rsquo;s job has been keeping them active through diagnosis and treatment: &ldquo;Giving them a positive environment to be able to work in and be able to do movements that are gentle for them. But still keep them strong through their process.&rdquo;</p>
<h3>Balance before the first scare</h3>
<p>Mike connected it to the daily things that get harder first. Walking. Taking the garbage out. Getting in and out of the shower or the bathtub. Balance and muscle strength sit under all of them, and so does fall prevention. Danielle&rsquo;s answer was to start early, before balance becomes a problem, and Dave added a story he has told before: President Bush Senior, he said, named balance as the one thing he wished he had worked on and not let slip away.</p>
<p>If you are in that stage right now, our <a href="strength-training-after-60-fall-prevention.html">guide to strength training after 60 and fall prevention</a> goes deeper on what a balance program involves, and the <a href="../services/wellness.html">wellness program</a> page covers our on-site gym.</p>
<h2>From M&ouml;nchengladbach to Juno Beach: Danielle&rsquo;s Pilates lineage</h2>
<p>Dave asked how she got into Pilates, and Danielle started with a fact that surprises a lot of people. Joseph Pilates was a real person. He was born in M&ouml;nchengladbach, Germany, and was a sickly child with rickets. Mike found that the most mind blowing part, because Pilates grew up to be a boxer and a circus performer.</p>
<p>During the war, Danielle said, he was on the Isle of Man rehabilitating soldiers, and he took springs from the beds to build his own version of what she described as physical therapy. Later he built his own equipment, emigrated to the United States and opened a studio in New York. When he died, his wife Clara, a nurse who also taught, took it over. After Clara, Romana Kryzanowska ran the studio. Romana was a direct disciple of Joe, and she is where Danielle&rsquo;s original training comes from.</p>
<h3>Lolita San Miguel, 92 and still traveling</h3>
<p>When Danielle moved to Florida, she met Lolita San Miguel, whom she called the last living elder who trained with Joseph Pilates. Lolita lives in Juno Beach, just up the road from our clinic. Danielle works with her, and at the time of recording Lolita was about to turn 92 on the 9th of October. She still travels. The two of them had just come back from the yearly conference in M&ouml;nchengladbach, which Lolita started.</p>
<p>Mike wanted to know whether Lolita&rsquo;s energy comes down to how she treats her body. Danielle said yes, definitely.</p>
<h2>Eve Gentry, a radical mastectomy and the alphabet soup</h2>
<p>Then Danielle told the story that ties Pilates to this episode&rsquo;s subject. Joseph Pilates had a client named Eve Gentry, a dancer, who was diagnosed with breast cancer in the 1950s (Danielle placed it around 1950 to 1955). She had a radical mastectomy and was told she would never dance or do Pilates again.</p>
<p>He worked with her anyway. It took a year for her to get full range of motion back through her pectorals. One of the hospitals in New York suggested his work belonged inside the hospital, so he filmed Eve doing her exercises. Someone took the film to the hospital, and they did not believe it. So it was filmed again, this time topless, so nobody could doubt she had had the mastectomy. The hospital still turned him away. In Danielle&rsquo;s retelling, they said: &ldquo;You don&rsquo;t have the alphabet soup behind your name. So we can&rsquo;t take you.&rdquo;</p>
<p>Mike called him way ahead of his time. Dave thought about all the senior homes and nursing homes that work could have reached.</p>
<h3>What Dave sees at the clinic after breast surgery</h3>
<p>Dave sees many women after a mastectomy. Some deal with scar tissue even after a partial mastectomy or a tumor removal, and the work is getting range of motion and strength back, along with the daily activities that go with them. His caution was about jumping straight into a hard group class. &ldquo;It&rsquo;s more important for people to have someone supervised,&rdquo; he said. He loves yoga and he loves Pilates. He wants the first steps watched.</p>
<p>That supervised start is what therapy after surgery is for. Our <a href="../treatments/post-surgical.html">post-surgical rehab page</a> explains how it works here, and the <a href="../treatments/shoulder-pain.html">shoulder pain page</a> covers stiffness and lost motion in the shoulder. Our hand therapist, Laura Drumm, MS, OTR/L, CHT, CLT, is also a certified lymphedema therapist; if swelling is part of your picture, ask the front desk about it when you call.</p>
<h2>Deep sleep, an Oura ring and blue light glasses at 8 o&rsquo;clock</h2>
<p>Mike asked the question that sounds simple: when does cancer occur? Elyse&rsquo;s answer was the shortest line of the hour. &ldquo;When the conditions are exactly right.&rdquo; Then she finished the thought. &ldquo;So we&rsquo;re going to make sure that the conditions are never exactly right.&rdquo;</p>
<p>That brought Dave to his own weak spot, which is sleep. A neurologist friend he plans to bring on the show told him total hours matter less than deep sleep, so Dave got a ring to track it. He reported nights with an hour and 49 minutes of REM against an hour and 30 minutes of deep sleep and wanted to know how that works. Elyse said she wasn&rsquo;t sure about the REM part. Deep sleep she was sure about: exercise and fasting can increase it, and she called wearables like the Oura ring or the Whoop band a great thing to have.</p>
<h3>The ring, the watch and Karen</h3>
<p>Dave&rsquo;s nightly dilemma got a laugh. At 11 o&rsquo;clock his ring tells him to get ready for bed, and his watch tells him to get up and take a brisk half hour walk. Who does he listen to? Karen, his wife. Mike voted for the walk, with some meditation on the way.</p>
<p>Elyse&rsquo;s easiest habit of the hour was the blue light blocker glasses. Wear them starting at 8 o&rsquo;clock, she said, and they help your body start producing melatonin, so you fall asleep faster and deeper. Danielle tied the whole morning together: exercise, stress and late meals all feed into how you sleep. &ldquo;It all correlates into each other,&rdquo; she said.</p>
<p>Dave&rsquo;s version was don&rsquo;t create the perfect storm. You can&rsquo;t fix all seven pillars this week. You can pick one.</p>
<h2>How to reach Elyse, Danielle and the show</h2>
<p>Both guests gave their details on air, and Mike read them back. Elyse sees patients in Jupiter, working alongside Dr. Paula Newmark at Back to Health; her number is 561-252-7857 and her website is thenutritioninstitute.org. Danielle&rsquo;s studio, Pilates Life, is on Northlake in Palm Beach Gardens, at 561-288-8151 or PilatesLifeFlorida.com. You can read more about each of them on our guest pages for <a href="../guests/marrone.html">Elyse Marrone</a> and <a href="../guests/armstrong.html">Danielle Armstrong</a>. Dave also offered to put any listener in direct contact with either of them through the clinic.</p>
<p>If you live in <a href="../locations/jupiter.html">Jupiter</a> or <a href="../locations/palm-beach-gardens.html">Palm Beach Gardens</a>, our clinic is at 733 US Highway 1, Suite 2A, in North Palm Beach. Questions about how the gym fits alongside therapy are answered in the <a href="../faq.html#wellness-gym">wellness and gym FAQ</a>.</p>
<p>Listen to the whole conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch it in our <a href="../videos.html">video library</a>, and catch the show live Saturdays at 8:30 AM on 100.3 Legends Radio. If a stiff shoulder after surgery, a balance worry or a plan to get moving again is what brought you here, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep17-goodwin": {
        "title": "What Your Mammogram Can Miss: Dr. Don Goodwin on Dense Breasts and Screening at 40",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "Radiologist Dr. Don Goodwin tells Pain 2 Power why he favors yearly mammograms from 40, what dense breasts can hide, and when ultrasound or MRI is added.",
        "body": """
<p>Most women hear two different answers about mammograms. Start at 40, or wait until 50. Go every year, or every other year. On the first Saturday of Breast Cancer Awareness Month, Dave brought in someone who has been reading those images for more than half a century to sort it out: radiologist Dr. Donald Goodwin, MD, of TGH Imaging, the practice many people around here still know as Palm Beach Radiology. His answer was clear, and so was his explanation of what a mammogram can and cannot see.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Fifty years of reading images, and a building Dave and Don put up in 2007</h2>
<p>Dave and Don go back a long way. Their businesses ran side by side for years, and in 2007 they officially built a building together and rented it out, with Don as one of the owners of Palm Beach Radiology. Dave did the arithmetic on air. Don has been a radiologist for over 50 years, Dave is coming up on 40 in his own field, and &ldquo;Remember when we started, we were the young guys.&rdquo;</p>
<p>Before handing over the microphone, Dave ran through the things that are in your own hands: keeping your weight down, exercising, and eating more fibrous vegetables like sweet potatoes, carrots, broccoli and leafy greens. Then he got to his real reason for the episode. &ldquo;But big thing is screening,&rdquo; he said, and he asked Don to walk listeners through when women should start, and how often.</p>
<p>If you only know Don&rsquo;s name from a report in your patient portal, his <a href="../guests/goodwin.html">Pain 2 Power guest page</a> has the background: the practice joined Tampa General and became TGH Imaging at the same North Palm Beach location, and Don stayed on. As he put it near the end of the show, they provide professional services for Tampa General now.</p>
<h2>Start at 40 or 50? Every year or every other year?</h2>
<p>Don started by admitting the confusion is real. The recommendation that gets the most press, he said, comes from the US Preventive Services Task Force, and it has often been at odds with what the medical societies say. That mismatch, in his words, &ldquo;always, uh, causes some consternation.&rdquo;</p>
<h3>What the task force changed last year</h3>
<p>Until last year, Don explained, the task force recommended starting screening at age 50 and going every other year after that. Last year it moved the start date from 50 to 40. It kept the every other year interval.</p>
<p>The American College of Radiology, the American College of Surgeons and the American Cancer Society, he said, have recommended starting at 40 with a mammogram every year for years, and they still do. So the two camps now agree on the starting age. They still disagree on how often.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Mammogram screening recommendations as described on the episode">
<table>
<caption>Screening recommendations as Dr. Donald Goodwin, MD described them on Pain 2 Power Episode 17. Ask your own doctor which schedule fits you.</caption>
<thead><tr><th scope="col">Who</th><th scope="col">When to start</th><th scope="col">How often</th></tr></thead>
<tbody>
<tr><th scope="row">US Preventive Services Task Force, until last year</th><td>Age 50</td><td>Every other year</td></tr>
<tr><th scope="row">US Preventive Services Task Force, now</th><td>Age 40</td><td>Every other year</td></tr>
<tr><th scope="row">American College of Radiology, American College of Surgeons, American Cancer Society</th><td>Age 40</td><td>Every year</td></tr>
<tr><th scope="row">Dr. Goodwin&rsquo;s own view</th><td>Age 40</td><td>Every year</td></tr>
</tbody>
</table>
</div>
<h3>Why Dr. Goodwin leans toward every year</h3>
<p>Don gave two reasons. The first was a trend. Breast cancer incidence, he said, has been rising by close to 1% a year since records began, and in women under 50 it has been rising by about 1.5% a year over the last 10 years. Dave asked whether better testing explains that. &ldquo;Who knows?&rdquo; Don said. &ldquo;You just don&rsquo;t know.&rdquo;</p>
<p>The second reason is the job itself. &ldquo;Our job is to find it as small and early as possible, because the smaller the lesion, the earlier the stage, the better the prognosis,&rdquo; he said. Then he made the case against waiting in one plain sentence: &ldquo;if you wait two years and, and it&rsquo;s been growing for two years, and you could have picked it up last year, well, maybe you missed an opportunity.&rdquo;</p>
<p>Mike picked up on the numbers. One and a half percent sounds small, he said, until you remember it is an annual increase. It stacks.</p>
<h2>How much radiation is in a 3D mammogram?</h2>
<p>Dave raised the worry a lot of women carry into the appointment: all that radiation, year after year. Don answered with specifics.</p>
<p>Mammography, he said, is very heavily regulated. His center is inspected every year, and the equipment goes through quality testing on a regular schedule. The expected dose from a 3D mammogram is about 0.4 millisieverts, &ldquo;which is about two months&rsquo; worth of walking around on Earth.&rdquo; He also put it another way: about the same as one transcontinental flight from here to LA.</p>
<p>He did not pretend it was zero. You cannot avoid radiation entirely, he said. There is radon in basements if you live in the Northeast, and there is radiation from the air. His point was to skip the unnecessary stuff, and he named CAT scans as the bigger exposure, anywhere from 2 to 16 millisieverts. And when Dave asked about MRI, the answer was short. &ldquo;MRs have zero radiation,&rdquo; Don said. &ldquo;It&rsquo;s all magnetic.&rdquo;</p>
<h2>Dense breasts, and what a mammogram can miss</h2>
<p>This is the part of the hour the episode title comes from, and it is worth hearing if you have ever been told your breast tissue is dense.</p>
<p>In an average risk screening population, Don said, a radiologist expects to find four, five or six cancers per thousand women screened with an annual mammogram. In women with dense breasts the mammogram is less sensitive. &ldquo;You can miss up to 60% of the cancers less than 10 millimeters in size,&rdquo; he said. So radiologists add other tools, starting with ultrasound, which he said can increase the sensitivity of cancer detection by about 50%.</p>
<h3>The BRCA study: 15, then 22, then 42 per thousand</h3>
<p>Dave asked Don to explain BRCA for listeners. Everybody has the BRCA gene, Don said, but a mutation in it makes you more likely to develop a variety of cancers, breast cancer among them, with what he called basically a 50 to 70% lifetime risk. Then he described a study done years ago on a population of BRCA positive women, screened three ways in turn.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Cancers found per thousand women by screening method in a BRCA positive study">
<table>
<caption>The BRCA positive study Dr. Goodwin described on Pain 2 Power Episode 17, cancers found per thousand women. Figures are as stated on air.</caption>
<thead><tr><th scope="col">Method</th><th scope="col">Cancers found per thousand</th></tr></thead>
<tbody>
<tr><th scope="row">Average risk women, annual mammogram (for comparison)</th><td>4 to 6</td></tr>
<tr><th scope="row">BRCA positive women, mammogram</th><td>15</td></tr>
<tr><th scope="row">Adding ultrasound</th><td>Another 7, for 22 in total</td></tr>
<tr><th scope="row">Breast MRI on the same women</th><td>42</td></tr>
</tbody>
</table>
</div>
<p>That makes MRI, in Don&rsquo;s words, &ldquo;about twice as sensitive for cancer detection as mammogram plus ultrasound.&rdquo;</p>
<h3>So why doesn&rsquo;t everyone get an MRI?</h3>
<p>Because it is very expensive, it involves an IV injection, and you have to lie still for 20 or 40 minutes, depending on the protocol. Dave said that was something Mike could never do. Mike agreed.</p>
<p>Don said MRI is reserved for the high risk population, which is now defined as greater than 20% lifetime risk. That risk can come from family history, a prior biopsy that showed some atypia, or other genetic mutations besides BRCA. He also uses it as a problem solver. Sometimes a finding on the mammogram and the ultrasound still is not clear, and the next step is, as he put it, &ldquo;let&rsquo;s get an MR.&rdquo;</p>
<h2>After the mammogram: BI-RADS scores, callbacks and core needle biopsy</h2>
<p>Mike mentioned someone he knows with dense breasts who got the same news almost every year: something questionable, more testing. Don said that is one of the real frustrations for women. You go in for a mammogram and, in his words, &ldquo;Oh, geez, they called me back again.&rdquo;</p>
<h3>What a BI-RADS score is for</h3>
<p>Dave brought up the BI-RADS score, which he described as running from zero to six. Don called it a classification of imaging findings that the government mandates, &ldquo;as it should be, because it, it f- it forces the radiologist to make a decision.&rdquo; The decision is whether a finding is benign or needs more evaluation, such as additional imaging or a biopsy. Dave&rsquo;s point was the human one: with a score on the report, the doctor has to commit, and that is why he would rather have someone with Don&rsquo;s 50 years making the call.</p>
<h3>How 3D mammography cut the callbacks</h3>
<p>Before the 3D mammogram, Don said, callback rates ran 10 to 12% of initial screenings. With 3D imaging, a lot of what used to trigger a callback can be resolved on the first set of images, and callback rates now run maybe 6 to 8%. That means fewer return visits, less radiation and, his phrase, &ldquo;less aggravation.&rdquo; Dave added less anxiety.</p>
<p>The money part is less tidy. Supplemental screening is sometimes not covered by insurance, Don said. The mammogram is covered, and then you get hit with additional tests, out of pocket payments and deductibles. He called it &ldquo;a real bummer.&rdquo; If dense tissue is part of your history, it is worth asking your insurer about supplemental imaging before the bill arrives rather than after.</p>
<h3>Biopsy without the operating room, and what stage 1 means</h3>
<p>Dave asked whether Don&rsquo;s center does core needle biopsies. It does, and Don explained why that matters with a number from early in his career. In the 1980s and 1990s, he said, about 95% of breast surgeries across the country were for benign disease. You had a lump, it got cut out, and that meant an operating room, general anesthesia and a big bill, for something that turned out not to be cancer.</p>
<p>He counts the ability to make a benign diagnosis without surgery as one of the great contributions of breast imaging. And when a finding is malignant, the surgeon knows what he is dealing with before going in. Don said the need for re-operations is much less, a sentinel node can be taken at the same time, and the surgical treatment is completed in one go. &ldquo;It&rsquo;s just much more precise and much more efficient,&rdquo; he said.</p>
<p>When a biopsy does show cancer, the pathologist runs what Don called a breast profile: the estrogen receptor, the progesterone receptor, the HER2 receptor that Dave had asked about, and Ki67, which Don described as a kind of proliferative index. In the old days, he said, everybody got the same chemotherapy. Now the aim is to match treatment to the specific tumor, getting the most effect on the tumor and the least on the rest of the body. He was careful to add that treating breast cancer is &ldquo;way out of my field,&rdquo; but that it has vastly improved over the last 10 to 20 years.</p>
<p>His example: with a stage 1 lesion, the five year survival is about 98 to 99%. Stage 1, he explained, is based on small size, usually less than two centimeters, with no nodes and no extension outside the breast. Which loops right back to his opening point about finding it small and early.</p>
<p>Mike also asked about preventive double mastectomy. Don called prophylactic mastectomy a viable alternative for some women, usually in the high risk group: BRCA positive women, people with strong family histories, or women with a cancer on one side who choose to remove the other breast at the same time as reconstruction. He noted that, generally speaking, there is no survival benefit of a mastectomy over a lumpectomy for a malignancy, and that it is probably not recommended for fibrocystic changes. These are decisions for a woman and her own surgeon.</p>
<h2>Men get breast cancer too</h2>
<p>Mike wanted the guys listening to hear this part. Breast cancer conversations center on women, he said, but men get it, and he named a few who went public: Montel Williams, the actor Tyler Mane, and Peter Criss, the drummer from Kiss. &ldquo;There&rsquo;s a lot of stigma around that and people don&rsquo;t talk about it,&rdquo; he said.</p>
<p>Don put numbers on it. Maybe 12% of women will develop breast cancer, he said, and in men it is maybe one out of 1,000. Men have breast tissue, and testosterone makes it shrink, which is part of why it is so much rarer. But men develop lumps. Some come in with a lump in the armpit, which he said means it has spread.</p>
<p>The most common reason men see him, Don said, is gynecomastia, a growth of breast tissue behind the nipple that usually shows up as tenderness and sometimes as a lump. Imaging can usually sort that out. His advice for men was direct: &ldquo;with those symptoms, you ought to get checked out because every once in a while there&rsquo;s a cancer in there.&rdquo;</p>
<h2>Hormone therapy, a bad pun, and how to reach Dr. Goodwin</h2>
<p>Dave turned to hormone replacement. Earlier guests on the show have talked about it, and Dave&rsquo;s view is that women need to watch their bloodwork closely and see someone who really knows what they are doing. Don&rsquo;s answer was measured. &ldquo;There&rsquo;s a lot of conflicting research about that,&rdquo; he said. It used to be thought that hormone replacement raised breast cancer risk, then studies said no, then yes again, then that estrogen alone did not but estrogen plus progesterone did.</p>
<p>He added that much of that data is old, that today&rsquo;s bioidentical hormones are used at lower doses, and that they have not been around long enough to know for sure. If you need hormone therapy to get along, he said, okay. His one condition: &ldquo;keep up with your screening, that&rsquo;s all.&rdquo; Mike summed up the whole hour the same way, women first and guys with symptoms too. Get screened.</p>
<p>Then came the dad joke, which Dave warned Don about, since the two of them share many bad dad jokes. A grape sees a farmer coming with a press. What did the grape do? It whined. Mike said the right response was a groan.</p>
<p>To reach Don, the number he gave on air is 561-841-8588, at TGH Imaging. Dave thanked him for coming in that early instead of going fishing.</p>
<h2>Where a therapy clinic fits after a breast cancer diagnosis</h2>
<p>We do not read mammograms at First Rehabilitation, and nothing in this post replaces the conversation you should have with your own doctor about screening. Where we come in is later. Episode 17 opened a run of breast cancer episodes. The week after Don, Dave and Mike talked with dietitian Elyse Marrone and Danielle Armstrong of Pilates Life about food and movement before, during and after a diagnosis, and Dave&rsquo;s advice there was supervised exercise over jumping straight into a hard class. We wrote about why supervision matters in <a href="gym-program-after-physical-therapy-north-palm-beach.html">our post on starting a gym program after physical therapy</a>.</p>
<p>That supervised work happens in our <a href="../services/wellness.html">on-site wellness gym</a>, with a team that knows your history and what your body has been through. The <a href="../faq.html#wellness-gym">wellness and gym FAQ</a> covers the common questions, and anything about memberships or schedules is a front desk conversation.</p>
<p>You can hear Don&rsquo;s whole conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch it as &ldquo;What Your Mammogram Can Miss&rdquo; in our <a href="../videos.html">video library</a>, and catch new episodes Saturdays at 8:30 AM on 100.3 Legends Radio. If you are rebuilding strength or range of motion after treatment or surgery and want a plan built around you, call us at 561-624-4263 or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep14-arlosoroff": {
        "title": "Leave the Governor On: Dr. Chaim Arlosoroff on E-Bike Injuries in Kids",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "St. Mary&rsquo;s trauma surgeon Dr. Chaim Arlosoroff tells Dave and Mike why the e-bike governor matters, and why the average injured rider he treats is 13.",
        "body": """
<p>Somewhere along the way, a lot of us filed the e-bike under bicycles. It has pedals, a kickstand and a basket, and a 13-year-old can ride it to school. Dr. Chaim Arlosoroff, M.D., files it somewhere else. He is an orthopedic trauma surgeon at St. Mary&rsquo;s Medical Center, and on this episode of Pain 2 Power he told Dave and Mike what the e-bike boom looks like from the trauma bay.</p>
<p>The short version is that the bikes coming through his emergency room are often not the bikes that left the store. A small part called the governor is supposed to keep them slow. Kids are taking it off. If you have a child or grandchild who rides one, or who has one on a gift list, this conversation is worth half an hour of your Saturday.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>What a St. Mary&rsquo;s trauma surgeon is seeing in Palm Beach County</h2>
<p>Dr. Arlosoroff has done orthopedic trauma at St. Mary&rsquo;s for the past 30 years. He explained that his group also covers the pediatric and adult emergency rooms there, and that St. Mary&rsquo;s is a level one trauma center taking referrals from across the region. So when injuries change, he sees it early. Up until a few years ago, he said, the bad ones were motorcycles.</p>
<p>Dave opened the topic with a national figure: ER visits for e-bike injuries in the United States up more than 400%. Dr. Arlosoroff said he had done a little research of his own on the counties around us. &ldquo;Palm Beach County from &rsquo;23 to &rsquo;24, 130% increase,&rdquo; he said. &ldquo;Broward, 180% increase.&rdquo; Miami-Dade, counting Nicklaus Children&rsquo;s Hospital, came in at more than 500% by his count.</p>
<p>Then came the two numbers that made Mike groan out loud. About 83% of the injured riders were not wearing a helmet. And the average age of the injured rider was 13.</p>
<h3>Why the hospital count is only the floor</h3>
<p>He was careful about what those figures include. &ldquo;And remember, these are serious injuries,&rdquo; he said. They are the cases that reach the emergency room, come in as a trauma alert, or get admitted. In his words, there&rsquo;s a &ldquo;gazillion of people who never make it to the hospital or go to urgent cares,&rdquo; and none of them show up in the statistics. Every sprained wrist that gets iced at home and every road rash cleaned up at an urgent care sits outside the count.</p>
<p>Dave added a story from his own clinic. A few weekends back, Dr. Arlosoroff came by looking like he was having a bad day. That one weekend, Dave said, he had treated a 14-year-old with a spinal cord injury who was not expected to walk again, and a 13-year-old who did not survive. Dave said the age twice. Thirteen.</p>

<div class="data-table" tabindex="0" role="region" aria-label="E-bike injury figures cited on Pain 2 Power Episode 14">
<table>
<caption>E-bike injury figures as Dr. Chaim Arlosoroff and Dr. Dave Kashuba stated them on Pain 2 Power Episode 14. These are their on-air numbers, not figures First Rehabilitation has verified.</caption>
<thead><tr><th scope="col">Figure</th><th scope="col">What was said on the show</th><th scope="col">Who said it</th></tr></thead>
<tbody>
<tr><th scope="row">United States ER visits</th><td>Up more than 400%</td><td>Dr. Kashuba</td></tr>
<tr><th scope="row">Palm Beach County, 2023 to 2024</th><td>130% increase</td><td>Dr. Arlosoroff</td></tr>
<tr><th scope="row">Broward County</th><td>180% increase</td><td>Dr. Arlosoroff</td></tr>
<tr><th scope="row">Miami-Dade, including Nicklaus Children&rsquo;s Hospital</th><td>More than 500% increase</td><td>Dr. Arlosoroff</td></tr>
<tr><th scope="row">Riders not wearing a helmet</th><td>About 83%</td><td>Dr. Arlosoroff</td></tr>
<tr><th scope="row">Average age of the injured rider</th><td>13</td><td>Dr. Arlosoroff</td></tr>
<tr><th scope="row">Head and neck injuries</th><td>32% of all injuries</td><td>Dr. Kashuba</td></tr>
<tr><th scope="row">Speed with the governor in place</th><td>15 to 20 miles an hour</td><td>Dr. Arlosoroff</td></tr>
<tr><th scope="row">Speed with the governor removed</th><td>50, 60, or maybe more</td><td>Dr. Arlosoroff</td></tr>
</tbody>
</table>
</div>

<h2>The governor, a small part built to hold a bike at 15 or 20 mph</h2>
<p>The single most useful thing in the hour is a word most parents have never heard. An electric bike ships with a governor, a limiter on the motor that caps its top speed. Dr. Arlosoroff put the factory range at 15 to 20 miles an hour. The trouble starts when someone changes it.</p>
<p>&ldquo;It&rsquo;s really scary that 13-year-olds can buy or get an electric bike, change something in the engine,&rdquo; he said. With the governor gone, he told Dave, &ldquo;they can fly at 50, 60, or maybe more.&rdquo; That is car speed on a frame built for a bike path, ridden by a kid who usually has a bicycle helmet on, if he has one on at all.</p>
<h3>Mike&rsquo;s math: 15 versus 50</h3>
<p>Mike put it in a line that has since become one of the episode&rsquo;s clips. When people hear the word bike, he said, they picture something you can&rsquo;t go too fast on. Plenty of kids ride without helmets, and when he was a kid nobody wore one. &ldquo;Going 15 versus 50 is the difference between a scrape and a cracked skull,&rdquo; he said. In his view people take it very lightly and don&rsquo;t understand the real responsibility of handling that piece of machinery.</p>
<p>Later he compared it to the golf carts kids drive around some neighborhoods. A 13-year-old on a golf cart is still a worry, he said, but at least it won&rsquo;t be going 50, and there&rsquo;s a little more protection somewhere. On an e-bike there&rsquo;s nothing between your head and the concrete.</p>
<h3>Sidewalks, wheelies and fire hydrants</h3>
<p>Speed was only part of it. Dr. Arlosoroff described riders who ignore almost every traffic rule, partly because they are 13. They hop on and off sidewalks, ride against traffic, merge into it without looking. Dave added wheelies to the list. Dr. Arlosoroff said he has treated people who simply hit a utility pole or a fire hydrant, or caught a curb and went over the handlebars. &ldquo;We&rsquo;re talking about major, major injuries,&rdquo; he said.</p>
<p>Dave raised the other side of the sidewalk problem: the people the riders hit. Pedestrians get hurt too. Dr. Arlosoroff said they see a lot of skull fractures, along with a lot of very serious injuries that carry severe consequences for the kid and for the family.</p>

<h2>Pedal assist in Park City and Sedona, and Dave&rsquo;s case for pedaling</h2>
<p>None of this made Dr. Arlosoroff anti e-bike. He is an avid cyclist. Here in Florida he rides a road bike and a mountain bike under his own power. He said the e-bike comes out only when he travels to steep country like Park City, Sedona, or Italy, where he rode this past summer, because it lets him reach places he would never get to otherwise. He also noted, with a smile, that he is getting a little older than David.</p>
<p>The key difference is that his rentals are pedal assist. &ldquo;Even with help, you are working hard and you&rsquo;re getting tremendous amount of exercise,&rdquo; he said. In South Florida, he said, it has become a fad, and for some people it is simply how they get around, because money is tight, they have lost a license, or for a variety of other reasons.</p>
<h3>Flat land and the hour a day</h3>
<p>Dave was blunter. He said he doesn&rsquo;t believe a kid in Florida, on flat land, needs an e-bike at all. His reason had nothing to do with crashes. &ldquo;Only 20% of the kids in the United States get enough exercise, get an hour of exercise every day,&rdquo; he said, and he compared that with the early 1970s, when by his figures most kids got that hour in. He tied the change to rising rates of fatty liver disease and type 2 diabetes in children. His suggestion was simple: get the kids on bikes they push themselves.</p>
<p>Mike told a story from a bike shop. He went in wanting to burn a few calories, and the salesman kept steering him toward an e-bike, pitching how nice it would be to just cruise the trail and take in the scenery. Mike admitted that does sound pleasant. It also seemed to him to be missing part of what makes a bicycle a bicycle.</p>
<p>If a fall has already happened, our <a href="../services/physical-therapy.html">physical therapy</a> page explains how an evaluation and a plan of care work.</p>

<h2>What a parent can actually do before the next ride</h2>
<p>Mike closed the e-bike segment by speaking straight to the parents and grandparents listening, especially anyone looking at gifts. An e-bike is a motor vehicle, he said, and it can be modified into something you would never expect. Dr. Arlosoroff added that he believes Florida has a helmet law for bike riders under a certain age, though he wasn&rsquo;t sure of the age and said it is obviously not enforced. Dave said there are efforts to tighten the rules.</p>
<p>Pulling together what the three of them said on air, the practical list is short:</p>
<ul>
<li>Put a helmet on the rider every time. Dave said a parent who skips it is endangering the child.</li>
<li>Leave the governor in place, and check that it is still there. Mike&rsquo;s words: &ldquo;Make sure that they&rsquo;re not modifying these things.&rdquo;</li>
<li>Talk about sidewalks and traffic. Riding against traffic and hopping curbs came up again and again.</li>
<li>Treat the purchase like a motor vehicle, with the rules and supervision you would give one.</li>
</ul>
<p>Dave also mentioned that some parents are now suing e-bike makers after their kids were hurt riding too fast without a helmet. He was skeptical. In his view the responsibility starts at home.</p>

<h2>Most fractures never need an operation</h2>
<p>Dave had a second reason for inviting his friend on. If your kid comes off a bike and you aren&rsquo;t sure whether the elbow is broken, he said, you may not need the ER. Dr. Arlosoroff treats injuries from the foot and ankle up through the knee, back, neck and shoulders, and he takes elective patients as well as the trauma cases at the hospital. Dave asked whether he favors a conservative approach when one is possible.</p>
<p>&ldquo;Most can be treated non-surgically,&rdquo; Dr. Arlosoroff said of fracture care and musculoskeletal injuries in general. He listed what fills his week: shoulder sprains, rotator cuff injuries, ankle sprains, and falls in older adults that end in a fractured wrist or hip. A lot of them, he said, are not serious. Many still land in the emergency room because injuries happen at all hours and people aren&rsquo;t sure what they are dealing with.</p>
<h3>From the ER splint to the therapy gym</h3>
<p>He walked through the usual path. If he sees a patient in the hospital while on call, the first treatment happens there: splinting, crutches, whatever is needed. Then the patient comes to his office for follow up. &ldquo;And eventually, a lot of time in your hands,&rdquo; he told Dave, &ldquo;and you help us look good,&rdquo; by getting people back to their regular activities.</p>
<p>That last stretch is the part we handle on US-1. Our <a href="../treatments/post-surgical.html">post surgical rehab</a> page covers what happens after an operation, and the same careful progression applies when a fracture heals without one. If the injury is a <a href="../treatments/hand-wrist.html">wrist or hand</a>, a <a href="../treatments/shoulder-pain.html">shoulder</a>, an <a href="../treatments/ankle-pain.html">ankle sprain</a> or a <a href="../treatments/hip-pain.html">hip</a>, those pages explain what therapy involves. Our post on <a href="what-to-expect-first-pt-visit.html">what to expect at your first physical therapy visit</a> answers the questions most people have before day one.</p>
<h3>Dirt bikes to the west, propellers to the east</h3>
<p>Dr. Arlosoroff said the variety is what he loves about the work. Think where we live, he said. There are the ordinary car, bicycle and motorcycle crashes. Head west and you get dirt bikes, ATVs and side by sides. To the east is the water, with boating injuries, jet skis, and propeller injuries he called devastating. He even mentioned shark bites, which he said he sees more of now that diving and spearfishing have become so popular. Some of these patients end up in surgery and some do not.</p>

<h2>A combat medic, a world ranking of 283, and a scholarship to Duke</h2>
<p>Before any of the e-bike talk, Dave made his friend of more than 30 years tell the story of how he got here. It started in 1973, when Dr. Arlosoroff was a high school sophomore in Israel and the Yom Kippur War closed his school for three or four weeks. The men were called to the reserves. His mother, a retired operating room nurse, volunteered at a local community hospital taking war injuries and brought him along to help.</p>
<p>He worked as a kind of orderly, cleaning operating rooms and wheeling patients in and out. One of the orthopedic surgeons there was the father of a boy he played junior tennis with, and that connection got him into the room to watch surgery. He expected to hate it. Instead he found that blood and guts didn&rsquo;t turn his stomach, and he was amazed watching bones put back together with pins, rods and plates.</p>
<h3>Three years as a combat medic</h3>
<p>At 18, like everyone in Israel, he went into the army, and he was selected to be a combat medic. He described an intense course of about six months followed by two and a half more years of service, seeing everything from a head cold to gunshot wounds. Through it all he kept playing tennis seriously. He was always one of the top four juniors in Israel, played on the Israel Junior Davis Cup team, and traveled to Miami to play the Orange Bowl.</p>
<h3>Sight unseen</h3>
<p>After his service he played the smaller futures and satellite tournaments for about a year. &ldquo;My highest ranking was 283 in the world in 1981,&rdquo; he said, adding that it sounds great but wasn&rsquo;t going to be his future. American players he met on tour told him about playing for a university, and a connection led to the tennis coach at Duke. &ldquo;I got an offer to get a, a four-year full scholarship, sight unseen. I mean, he&rsquo;s never seen me play,&rdquo; he said. There were no videos or smartphones then. The coach went on his ranking and results and took a chance, and it worked out well for both of them. Dave made sure listeners knew he was later inducted into the Duke Tennis Hall of Fame.</p>
<p>Mike connected the two halves. The focus it takes to reach that level as an athlete, he said, is the same focus Dr. Arlosoroff now brings to fixing bodies, and he still sounds curious about the human body as a machine.</p>

<h2>Next door on US-1, and a joke with no leg to stand on</h2>
<p>The practices sit close together in North Palm Beach, and the referrals run both ways every week. Dr. Arlosoroff described an orthopedic group that covers pretty much every subspecialty, with First Rehab &ldquo;literally right next door.&rdquo; &ldquo;It&rsquo;s a great setup.&rdquo; Dave added that the surgeon walks over to check on his own patients, and had done exactly that the day before the taping.</p>
<p>Dave&rsquo;s joke of the week came dressed as a serious story about an avalanche, a skier, a wrong-site amputation and a lawsuit. It went on long enough that both Mike and Dr. Arlosoroff admitted they were buying it. The skier sued the doctors and lost. &ldquo;He didn&rsquo;t have a leg to stand on,&rdquo; Dave said. Mike said it may be the best one Dave has ever done.</p>
<p>Listen to the full conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch it in our <a href="../videos.html">video library</a>, or read more about <a href="../guests/arlosoroff.html">Dr. Arlosoroff on his guest page</a>. The show airs live Saturdays at 8:30 AM on 100.3 Legends Radio. If you or your child is recovering from a fall, a fracture or a sprain, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>, and we will help you plan the way back.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep13-titheradge": {
        "title": "Captain Kerry Titheradge on Following Through, From a Rotator Cuff to Mental Health Mondays",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "Bravo&rsquo;s Captain Kerry Titheradge of Below Deck joins Dave and Mike on the rotator cuff program that traveled with him, Mental Health Mondays and giving back.",
        "body": """
<p>Captain Kerry Titheradge left Miami somewhere around 2:00 or 2:30 in the morning to make a Saturday radio show in North Palm Beach. He had a boat job that ran long, a business to run, and a friend who had tried to talk him out of coming. He came anyway, with a couple of minutes to spare.</p>
<p>That friend is Dr. Dave Kashuba, and the two go back more than twenty years, to a rotator cuff injury and a home program that went north with Kerry when his work did. This week&rsquo;s Pain 2 Power is the two of them and Mike McGann catching up on that shoulder, on the workout that ended up with Kerry&rsquo;s name on it, and on what Kerry does with the attention Bravo&rsquo;s Below Deck gave him.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>A phone call from a doctor, about twenty years ago</h2>
<p>Dave opened with the backstory. He studied in Australia, at Curtin University in Perth, and he says the Australians he knew on the west coast took such good care of him that he never forgot it. So when he opened the business here, and a doctor called about a young Australian with a shoulder injury, the answer was easy.</p>
<p>The catch was paperwork. Dave said he wasn&rsquo;t taking workers&rsquo; comp cases at the time, and the doctor knew it. As Dave remembers the call, the doctor said, &ldquo;Dave I know you&rsquo;re not on this insurance but can you take it?&rdquo; Dave&rsquo;s reply was that he would, &ldquo;without question,&rdquo; because of how he had been treated in Perth. (These days we do treat work injuries, and our <a href="../treatments/workers-comp.html">work injury rehab page</a> explains how that side runs.)</p>
<p>He also had a warning for listeners. If an Australian friend says he&rsquo;s coming to visit, Dave said, expect him to stay about three months. That happened too.</p>
<h3>Before he was Captain Kerry</h3>
<p>Most people know Kerry as the firm captain in charge of the boat on Below Deck. Dave wanted it on the record that he knew him before any of that, and that Kerry was at his 40th birthday. Dave is 60 plus now, he pointed out, so do the math. The reason he gave for the friendship was the drive from Miami that morning. Kerry made a commitment and kept his word.</p>
<p>Kerry&rsquo;s version was warmer still. &ldquo;Any time I needed some help, you&rsquo;ve always been there, and I genuinely see you as a very close friend of mine,&rdquo; he told Dave. Dave admitted he didn&rsquo;t know how to answer that, except &ldquo;right back at you.&rdquo;</p>
<h2>The rotator cuff program that went to the Northeast</h2>
<p>Mike steered the conversation back to the shoulder about twenty minutes in, and Kerry explained why it mattered so much at the time. He was working on deck. &ldquo;It was a rotator cuff. At the time I was working on deck. Full motion is very, very important,&rdquo; he said.</p>
<p>Dave put together what Kerry called a system. They had a few months together in the clinic to get the shoulder to a certain point, and then the job sent Kerry up to the Northeast before rehab was finished. So the program went with him. Kerry described it on air: &ldquo;you gave me what I needed to do when I was away, with bands and so forth. And I&rsquo;ve got full motion.&rdquo;</p>
<p>That shoulder has had two surgeries since. Kerry said both times, Dave and his team got him back together. If you&rsquo;re dealing with a rotator cuff of your own, our <a href="../treatments/shoulder-pain.html">shoulder pain treatment page</a> walks through what that rehab involves, and our <a href="../services/physical-therapy.html">physical therapy program</a> page covers how a plan of care gets built.</p>
<h3>Two to three visits a week, and the hours in between</h3>
<p>Mike made the point that follow through is the part people are least likely to do. Dave agreed, and said he can tell every single time. He sees people two to three times a week for an hour to an hour and a half. The other hours belong to the patient, and the exercises have to be done correctly and precisely.</p>
<p>He was just as firm about the other direction. Don&rsquo;t overdo it. Dave described the patient who figures that if ten is good, fifty must be better, and he said some exercises he sets for every other day rather than daily. Consistency was his word. And consistency was the thing he said he could see in Kerry, in rehab and as a dad.</p>
<p>Kerry had a line of his own about it, looking back: &ldquo;I remember just following everything you said to the tee.&rdquo; We wrote more about what that home program looks like once therapy ends in <a href="gym-program-after-physical-therapy-north-palm-beach.html">your gym program after physical therapy</a>, and the kind of short sets Dave hands out are on our <a href="../exercises.html">home exercises page</a>.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Captain Kerry's shoulder history as told on the episode">
<table>
<caption>Captain Kerry&rsquo;s shoulder, as he and Dave Kashuba described it on Pain 2 Power Episode 13. Details are as stated on air.</caption>
<thead><tr><th scope="col">When</th><th scope="col">What was said on the show</th></tr></thead>
<tbody>
<tr><th scope="row">About twenty years ago</th><td>A doctor calls Dave about an Australian patient with a shoulder injury, outside the insurance Dave was taking then</td></tr>
<tr><th scope="row">The first injury</th><td>A rotator cuff, while Kerry was working on deck, where full motion mattered</td></tr>
<tr><th scope="row">The first few months</th><td>Clinic visits to get the shoulder to a certain point before work took him away</td></tr>
<tr><th scope="row">Up in the Northeast</th><td>A home program with bands that Dave sent with him</td></tr>
<tr><th scope="row">Since then</th><td>Two surgeries on the same shoulder; Kerry says Dave&rsquo;s team got him back both times</td></tr>
<tr><th scope="row">Today</th><td>Kerry says he has full motion, and he trains on the program people call the Captain Kerry workout</td></tr>
</tbody>
</table>
</div>
<h2>How Dave&rsquo;s workout ended up with Kerry&rsquo;s name</h2>
<p>This part of the hour turned into a running joke. Dave said he has put time and effort his whole life into physical training and rehab, and he built a plan using blood flow restriction work so people could train in 20 to 25 minutes, three times a week. People started noticing.</p>
<p>Shannon Cake did a television story on Dave, then brought Kerry on, and the program came out of it as the Captain Kerry workout. In Dave&rsquo;s telling, twenty years of programming went away in ten seconds. Mike, who has spent a career in broadcasting, said that&rsquo;s branding for you. Shannon tells her side of the same story in <a href="pain-2-power-ep19-cake.html">our Episode 19 recap</a>.</p>
<h3>&ldquo;What size is that shirt?&rdquo;</h3>
<p>Dave also told the story from before Kerry started working out with him. At a friend&rsquo;s event, Kerry looked him over and asked what size shirt he was wearing, since it might look a little tight on him. Dave&rsquo;s answer: &ldquo;Kerry, it&rsquo;s the same size as you&rsquo;re wearing, just fits me different.&rdquo; These days, Dave said, Kerry is kicking his butt and taking it seriously. Kerry&rsquo;s reply was short. &ldquo;You still got me mate.&rdquo;</p>
<p>When Kerry rounded off the shoulder conversation, he said following Dave&rsquo;s protocols in the clinic and out of it was what got him back to health. If you want to keep training after your own rehab, our <a href="../services/wellness.html">wellness program</a> is where patients carry on once therapy ends.</p>
<h2>Mental Health Mondays, and why he talks about it on camera</h2>
<p>Most of the episode wasn&rsquo;t about shoulders at all. Dave asked Kerry to explain his own podcast and what he is trying to do with the platform television gave him.</p>
<p>Kerry said that because he isn&rsquo;t from America, he often has no idea who his famous guests are. Musicians, athletes, people from TV. He gets an honest conversation without any preconceived idea of the person, and only does the research afterward. The goal, he said, is &ldquo;just to humanise these somewhat TV stars or sporting stars, where people think that their life is great because it has to be.&rdquo; His point was that it takes a certain kind of person to get there, and they have the same struggles as everybody else, and maybe more.</p>
<p>On Mondays he does what he calls Mental Health Mondays, talking about things he&rsquo;s working through himself. The idea is to show people that there is no destination. He said he hasn&rsquo;t worked it all out yet, and that&rsquo;s part of what he shares.</p>
<h3>&ldquo;It&rsquo;s okay to be in that place&rdquo;</h3>
<p>Mike offered a line a very bright woman once gave him: you can&rsquo;t control what happens to you, but you can control how you respond. (She was bright enough, he added, to be his first ex wife.) Kerry took it a step further. Something really bad might happen to you, he said, &ldquo;and there is a moment where you are a victim, and it&rsquo;s okay to be in that place. That&rsquo;s part of healing, really. But what is staying there to do for you?&rdquo; A lot of people stay, in his view, because they don&rsquo;t know how to get out.</p>
<p>Mike asked whether the successful people Kerry has interviewed share anything. Kerry&rsquo;s answer was adversity. Not always trauma, he said, but things they pushed against that made them stronger. Mike called it trial by fire.</p>
<h3>Why Dave brought up men who don&rsquo;t reach out</h3>
<p>Dave cited some depression and suicide figures on air, and his point underneath them was about men. &ldquo;Men don&rsquo;t like to talk about it,&rdquo; he said, and that&rsquo;s what he values in Kerry: &ldquo;Someone like Kerry here, who&rsquo;s going out of his way to say hey guys, it&rsquo;s okay to talk about this.&rdquo; Dave added that people contact Kerry to thank him for it.</p>
<p>Mike thought the reason it lands is simple. &ldquo;People can tell that it&rsquo;s real,&rdquo; he said. Kerry described it in his own terms. The show put a searchlight on him, and he wants to point it everywhere else. If one person who is where he was can see that he found a way out, he said, &ldquo;if I can offer that cheat code to somebody by using this platform,&rdquo; anything less would be a disservice.</p>
<p>If you or someone close to you is struggling, please talk to your doctor. That conversation is outside what a therapy clinic does, and it matters more than any shoulder.</p>
<h2>A birthday, and a stage full of Amazon boxes</h2>
<p>Mike asked what made Kerry want to give back in the first place. Kerry said he&rsquo;d be brutally honest. Years ago, running a yacht and at the top of his game, he had a flash of it: &ldquo;I&rsquo;m just pumping diesel fumes everywhere. I&rsquo;m at service to one of the wealthiest people in the country. What am I doing for anybody else?&rdquo; Then his phone beeped, he said, and he forgot. That was as far as it went.</p>
<h3>The watch party that changed his mind</h3>
<p>What really started it came after the show began airing. During his first season he would host watch parties at local restaurants, free to come, where people could say g&rsquo;day and watch the episode with him. Adrienne Gang, from that first season, pointed out that an episode was airing on his birthday and asked if he wanted to do something for charity.</p>
<p>His first reaction: &ldquo;why would anyone give a damn about me?&rdquo; She asked what was important to him. He said single parents, since it was Christmas. So the plan became bring a present for a kid, celebrate Captain Kerry&rsquo;s birthday, and watch the episode. His fear going in was that only one present would show up and he would have failed.</p>
<p>He rocked up, he said, and &ldquo;the stage was full of Amazon boxes.&rdquo; People had sent presents in, all from a couple of posts. Asked how it felt, Kerry said, &ldquo;Full of joy, full of warmth. There&rsquo;s nothing like it.&rdquo; His takeaway was to imagine what he could do if he really thought about it.</p>
<h2>Huskies, veterans and an hour in the car</h2>
<p>Most of the charities Kerry works with, he said, are ones that aren&rsquo;t well known, and that&rsquo;s deliberate. He wants to bring attention to the ones that need it. He fosters dogs for a husky rescue and uses his following to let people know when a dog needs help or surgery.</p>
<p>He traced that back to his first rescue dog. He was going through a divorce at the time, and he wanted something constant for his kids. &ldquo;Kind of an anchor,&rdquo; he called it.</p>
<p>Another group he named works with veterans and first responders up around Port St. Lucie and Fort Pierce, taking them out fishing and diving. He met some of its people at the Miami Boat Show, where they ran into him and Captain Glenn and asked how he could help. His answer was to show up at the next event. &ldquo;It&rsquo;s very little effort for me to get in a car and drive an hour,&rdquo; he said, &ldquo;just to help others out.&rdquo; In his view, him rocking up, having a beer and saying g&rsquo;day can do a lot for people.</p>
<h2>Remember Me, and early onset dementia</h2>
<p>Kerry&rsquo;s help reaches into Dave&rsquo;s own work outside the clinic. Dave runs a 501(c)(3) nonprofit for early onset dementia called Remember Me. He said there&rsquo;s a story behind it, and he would save that for another show.</p>
<p>Here is how he described the work: &ldquo;Early onset dementia, we get people off the streets. You know, they&rsquo;re there, they need help, they need housing, they need nursing care. So we provide that for them. And Kerry offered his time and his money, just to help us out.&rdquo;</p>
<p>Dave also noted that Kerry is involved with dog rescues. Mike&rsquo;s sign off tied it together: he thanked Dave for what he does for people physically, mentally and emotionally, which he called &ldquo;so deeply intertwined.&rdquo; More on Kerry, with his clips from this episode, is on <a href="../guests/titheradge.html">Captain Kerry&rsquo;s guest page</a>.</p>
<h2>Jeopardy at 8:01, and the joke of the week</h2>
<p>The last few minutes were family. Dave said he is lucky to have his son Nick helping him in the business. Dave gave a shout out to his oldest son Brandon, an engineer at United Airlines, who flew them up to Chicago and then over to Buffalo to see Dave&rsquo;s mom. Brandon was thrilled to get them first class. He told his dad he&rsquo;d spent $17 for the seat.</p>
<p>Then the Jeopardy story. Dave calls his mom every day at 7:30. One day she didn&rsquo;t pick up, so at 7:46 he called again because he was worried. She answered, told him this wasn&rsquo;t his time, and hung up. She called back at 8:01, once championship Jeopardy was over.</p>
<p>And the joke: a Baptist minister, a priest and a rabbit sit down at a bar. The bartender comes over, looks at the rabbit, and says, &ldquo;hey, you&rsquo;re in the wrong joke.&rdquo;</p>
<p>Mike, for his part, admitted Dave keeps telling him to come by the clinic, which sits right across the street from the Legends Radio studio on US-1. He says he&rsquo;s going to make it happen one of these days.</p>
<p>You can hear the whole hour on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch it in our <a href="../videos.html">video library</a>, and catch the show live Saturdays at 8:30 AM on 100.3 Legends Radio. If a rotator cuff or a shoulder that never quite got back to full motion is what brought you here, call us at 561-624-4263 or <a href="../contact.html">request an evaluation</a>. Questions about getting started are answered on our <a href="../faq.html#getting-started">FAQ page</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep12-leighton": {
        "title": "Your Hip Replacement Starts at the Dentist: Dr. Michael Leighton on Pain 2 Power",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "Orthopedic surgeon Dr. Michael Leighton on anterior versus posterior hip replacement, the infection checks that start at your dentist, and what Medicare pays him.",
        "body": """
<p>Most people getting ready for a hip replacement think about the surgeon, the hospital and the weeks of rehab afterward. Very few think about their dentist. Orthopedic surgeon Dr. Michael Leighton, MD, thinks you should, and on Episode 12 of Pain 2 Power he explained why in about ninety seconds.</p>
<p>That was one stop in a half hour that covered the anterior and posterior approaches, why a belt line can change which operation you are a good candidate for, how hip surgery went from a week in traction to therapy the same day, and the dollar figure Medicare pays a surgeon for the whole thing. Mike guessed high. Very high.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>Why Dave brought in a surgeon he has worked with since 1994</h2>
<p>Dave introduced his guest as a friend he has been working with since 1994 and one of the best in the county. Then he went straight to his standing advice about picking an orthopedic doctor. Do the research, and choose on quality and nothing else. &ldquo;Don&rsquo;t listen to the lady at the pool,&rdquo; he said, a line Mike picked up later in the hour when he pointed out you&rsquo;re not going to get Dr. Leighton&rsquo;s years of training from the water cooler either.</p>
<p>Dr. Leighton is an orthopedic surgeon with Palm Beach Orthopedic Institute in Palm Beach Gardens. He is board certified by the American Board of Orthopaedic Surgery with a subspecialty certification in Orthopaedic Sports Medicine, and he performs both anterior and posterior hip replacement as well as robotic-arm assisted (Mako) knee replacement. You can read more about his background on <a href="../guests/leighton.html">his Pain 2 Power guest page</a>.</p>
<h3>A cup of coffee on the Duke baseball team</h3>
<p>Dave had heard from another surgeon that Dr. Leighton played Division I baseball at Duke. Dr. Leighton was quick to play it down. &ldquo;I was more like a cup of coffee on the baseball team,&rdquo; he said, and he figured out early that his future was in finishing his pre-medical studies, not in baseball.</p>
<p>What he did keep from those years was the athlete&rsquo;s view of the body. He counted the training out loud for Mike: four years of college, four years of medical school, five years of orthopedic residency, then a further year of sports medicine fellowship, where he cared for professional teams, college teams and high level athletes. Today his patients are golfing three or four times a week and playing pickleball several times a week, and he described his job as keeping that going.</p>
<h3>The friend who played Davis Cup</h3>
<p>The surgeon who had spilled the baseball story was Dr. Chaim Arlosoroff, M.D., the orthopedic trauma surgeon who came on a couple of weeks later to talk about e-bike injuries. Dr. Leighton gave the athletic credit right back. Chaim came from Israel, he said, was a Davis Cup player and played first singles at Duke. &ldquo;He was the real deal.&rdquo; Dr. Arlosoroff has <a href="../guests/arlosoroff.html">his own guest page</a> if you want that half of the story.</p>

<h2>Infection risk is low, and most of what keeps it low happens before surgery</h2>
<p>Dave opened the clinical part of the show by bragging on his guest&rsquo;s infection record. Dr. Leighton winced. His grandmother, he said, had a word for saying something like that out loud, and it meant bad luck. He would not claim he had never had an infection in his orthopedic life.</p>
<p>What he would say is reassuring. &ldquo;The good news is that the risk of infection in a total hip or a total knee replacement is actually quite low,&rdquo; he said. He put it at less than 1 or 2% over the course of your life with the implant in place, and said the surgical team does a lot around the operation to keep it there. The bigger lever, in his telling, sits with the patient in the months before.</p>
<p>Here is the pre-surgery list he walked through, in the order he raised it:</p>
<ul>
<li>No active infection anywhere: no pneumonia, no open diabetic foot ulcers, no unhealed wounds such as one left by a skin cancer</li>
<li>A visit to your dentist or periodontist to rule out an active or low grade infection in your mouth</li>
<li>Off cigarettes, and off nicotine vapes too</li>
<li>For diabetics, blood sugar under control, measured by hemoglobin A1C</li>
<li>For heavier patients, some weight off before an elective operation</li>
</ul>
<p>His first piece of advice on that list was plain honesty. If you have something a little weird that hasn&rsquo;t been healing, tell your surgeon. That is something he does not want to go into a hip replacement without addressing.</p>
<h3>Why your teeth matter to a new hip</h3>
<p>This was the part that stopped Mike. We all get bacteria in the bloodstream from time to time, Dr. Leighton explained. &ldquo;You brush your teeth, and you will get bacteria temporarily going through your bloodstream.&rdquo; Those same bacteria can settle in a newly implanted joint. So before a joint replacement, he wants patients evaluated by their dentist or periodontist and their dental hygiene up to speed.</p>
<p>Mike summed up how most of us would react: &ldquo;It&rsquo;s not the most intuitive thing in the world to think, &lsquo;I&rsquo;ve gotta get a hip replacement. I better make sure my mouth is free from infection.&rsquo;&rdquo;</p>
<h3>Cigarettes, vaping and the A1C number</h3>
<p>Smoking came next. Dr. Leighton said smokers have an increased risk of infection because smoking narrows the small blood vessels that carry blood to a fresh surgical wound. Dave asked the obvious follow up about vaping. The answer turned on nicotine: a nicotine-free vape isn&rsquo;t really the issue, he said, because it is the narrowing of the vessels you are trying to avoid. Dave, who has been doing this a long time, admitted he had never thought of that. &ldquo;I learn something new every day,&rdquo; he said.</p>
<p>For diabetics, Dr. Leighton looks at hemoglobin A1C, a score that shows how well blood sugar has been controlled over the past few months. His line was clear. If the A1C is greater than 7.5, he said, elective surgery should not be done on that patient because of the increased risk of infection.</p>

<h2>Anterior or posterior: what Dr. Leighton told us about the two approaches</h2>
<p>A total hip can be done from the front of the hip (anterior) or the back (posterior). Dr. Leighton does both and said he is &ldquo;more partial to a posterior approach.&rdquo; He was careful about what the comparisons show when they line up like with like. A small group of anterior patients get from a chair to standing faster or better in the first two to four weeks. After six weeks, the two are the same, or are supposed to be.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Anterior and posterior hip replacement as described on the episode">
<table>
<caption>Anterior and posterior total hip replacement as Dr. Michael Leighton, MD, described them on Pain 2 Power Episode 12. Paraphrased from the episode transcript; your own surgeon&rsquo;s advice comes first.</caption>
<thead><tr><th scope="col">Point he raised</th><th scope="col">Anterior approach</th><th scope="col">Posterior approach</th></tr></thead>
<tbody>
<tr><th scope="row">First two to four weeks</th><td>A small group of patients do sit to stand faster or better</td><td>No early edge on sit to stand</td></tr>
<tr><th scope="row">After six weeks</th><td>About the same</td><td>About the same</td></tr>
<tr><th scope="row">Fracture risk</th><td>Higher</td><td>Lower</td></tr>
<tr><th scope="row">Dislocation risk</th><td>Slightly lower</td><td>Slightly higher, though still very low</td></tr>
<tr><th scope="row">Wound complications in a heavier patient</th><td>Much higher</td><td>Lower</td></tr>
<tr><th scope="row">Who he tends to steer toward it</th><td>Thinner and younger patients can go either way</td><td>Larger patients, and patients 75 and older</td></tr>
</tbody>
</table>
</div>
<h3>The patient who had one of each</h3>
<p>Dr. Leighton has operated on plenty of people who had one hip done each way, and most tell him the two were about the same. One patient had both done by Dr. Leighton and liked the posterior side much better, because the recovery felt faster to him. He had chosen anterior first because his brother in another state had an anterior hip that turned out poorly, and he figured he might just have been lucky the first time around. Dave had a name for that: &ldquo;The water cooler effect.&rdquo;</p>
<h3>Why the belly matters</h3>
<p>The most practical stretch of the episode was about body size. An anterior incision sits on the front of the thigh. Picture a heavier patient sitting down with the belly resting on the front of the thigh, Dr. Leighton said. That covers the incision and keeps it moist, an environment &ldquo;not really ripe for healing,&rdquo; and wound complications run much higher. Mike added that the same patient may carry a higher diabetes risk, and Dr. Leighton agreed that stacks the risks.</p>
<p>He did not rule anyone out. A heavier patient who really wants the anterior approach can have it, he said, but he would ask them to improve their odds first. &ldquo;I need you to lose 15 or 20 pounds,&rdquo; he said, and pointed out that &ldquo;total hip replacements, unless it&rsquo;s for a fracture, are not emergency operations.&rdquo; He mentioned the GLP-1 medications as one tool that works, with a side benefit: less weight on a sore hip, and on a sore knee, feels slightly better while you wait. Paul Joyce of New Life HRT covered what those drugs can cost you in muscle on <a href="pain-2-power-ep11-joyce.html">our Episode 11 recap</a>, which is worth reading alongside this.</p>

<h2>Six weeks for bone to grow into the implant</h2>
<p>When people ask how soon they can get back to the courts, Dr. Leighton&rsquo;s general answer is about six weeks before something more rigorous like pickleball, tennis or golf. Chipping and putting can start early, whichever approach was used.</p>
<p>The reason is the hardware. Most modern hip components go in without cement, he explained, using what surgeons call ingrowth. The implant has a meshwork or roughened surface that bone actually grows onto and adheres to, which creates a solid fit. That takes about six weeks, &ldquo;and at that point is when I kind of let people and let a little rope out and let them do a little bit more.&rdquo; Cement is still used in some older patients, he said, but it is the exception now.</p>
<p>Mike&rsquo;s reaction tied it to the people who listen to this show. In years past, he said, rigorous activity after a hip replacement would have seemed finished for good. Done properly, with the steps followed, &ldquo;you&rsquo;re giving people their lives back here, doctor.&rdquo; Dr. Leighton agreed, and said the best patient who can walk into his office is the one whose bad hip is the only thing keeping them from being happy and active.</p>

<h2>From a week in traction to therapy the day of surgery</h2>
<p>Dave asked whether the old hip precautions still apply: no crossing the legs, no bending past 90 degrees, careful with rotation. He also mentioned what he teaches early on in the clinic, taking little steps to turn instead of pivoting on the new hip.</p>
<p>Dr. Leighton went back to John Charnley, whom he called the father of joint replacement surgery about 50 years ago. Charnley&rsquo;s approach removed a piece of bone called the greater trochanter and reattached it, which required strict precautions. No flexing the hip past 90 degrees, no bending to touch your toes, no internally rotating the hip, which he likened to sitting in a chair and reaching behind you for something.</p>
<h3>What changed</h3>
<p>When he was training, he said, patients stayed in the hospital for a week in balanced traction with the leg up, unable to move. They did fine in the end, though many got blood clots, because the risk of clots was not understood in those days. Since then surgeons have learned it is okay to stand, put weight on the operated leg and move the hip.</p>
<p>So he does not routinely put people in those restrictions now. Early on he still asks patients to avoid bringing the knee to the chest and the other most provocative positions. The goal is to get motion back gradually over the first few weeks while the wound heals. When Dave asked if that means patients can reach down for their shoes and socks, he said yes.</p>
<p>He liked where the field has landed. &ldquo;What&rsquo;s going on now in 2026 is an appropriate level of fear,&rdquo; he said. The surgeon names the moves to avoid, and he said the physical therapists tend to add a few more cautionary tales of their own, which he is fine with because patients need to feel comfortable doing the activities. We have written more about those early weeks in <a href="hip-impingement-back-pain-north-palm-beach.html">our hip impingement article</a> and on our <a href="../treatments/post-surgical.html">post-surgical rehabilitation page</a>. Either way, your surgeon&rsquo;s protocol is the one that counts.</p>
<h3>Why he keeps most patients overnight</h3>
<p>The operation can be done as an outpatient, Dr. Leighton said, but he generally keeps people in the hospital one night. His reasoning was about the first night home. If you go home the same day, you are looking at your partner and saying, &ldquo;You&rsquo;re gonna be my nurse overnight.&rdquo; If chest tightness or a bad headache shows up at 2 in the morning, neither of you is comfortable. In the hospital there is nursing staff, and patients get physical therapy the day of surgery and again the next day before going home. Dave noted that he sees more and more patients arriving at the clinic for outpatient therapy right after surgery.</p>

<h2>Prehab, Medicare visits, and where we come in</h2>
<p>Dave asked about prehab, the therapy some surgeons order before an operation to tune a patient up. Dr. Leighton&rsquo;s answer was that he does not prescribe it for everyone. He saves it for people who have been away from activity and are deconditioned, who need some aerobic work and whatever motion they can get back in the low back, the other hip and the knees. Two of our surgeon guests compare notes on that question in <a href="partial-vs-total-knee-replacement.html">our partial versus total knee replacement article</a>.</p>
<p>His reason was practical. A Medicare patient with hip arthritis, he pointed out to Dave, only gets so many tickets, and prehab visits count against the same yearly therapy benefit as the rehab after surgery. Dave explained that First Rehabilitation is a Medicare-certified Comprehensive Outpatient Rehabilitation Facility (CORF), and said that gives his patients more room to continue care when they hurt themselves or re-hurt themselves. How the Medicare therapy thresholds work in 2026 is laid out in plain terms in <a href="../insurance.html#medicare-guide">our Medicare guide</a>, and the front desk checks your coverage before your first visit.</p>
<h3>Thirty years of shared patients</h3>
<p>Mike asked whether any of this comes from the mailman. Dr. Leighton said no, and then talked about Dave. Dave has taken care of his patients for 30 years, he said, and it is not a case of putting someone on a bicycle in the corner and leaving them to pedal. &ldquo;He really does spend time with his patients, and does a great job.&rdquo;</p>
<p>That is how our <a href="../services/physical-therapy.html">physical therapy program</a> is meant to run for hip patients. Before surgery, the work is mobility, glute strength and walking mechanics, as described on our <a href="../treatments/hip-pain.html">hip pain page</a>. After it, we follow the surgeon&rsquo;s protocol, starting with motion. If you want a feel for the movements, Dave walks through several on our <a href="../exercises.html#hip">hip exercise page</a>, and our <a href="../faq.html#physical-therapy">physical therapy FAQ</a> covers referrals and what a visit looks like.</p>

<h2>The $1,162 question</h2>
<p>The show was wrapping up when Dr. Leighton asked for one more plug. He wanted listeners to know how a surgeon is paid for what he called the single best operation in orthopedics.</p>
<p>He set up the scenario: a healthy 66 year old Medicare patient, the operation, the hospital visits, and 90 days of care after surgery, all covered by one payment. Then he asked Mike to guess. Mike, who said he can&rsquo;t even guess ages or weights, went with 136,214. The real answer: &ldquo;$1,162, okay?&rdquo;</p>
<p>He added that this was before what he described as a recent July announcement of a further 3 to 5% cut. Rent doesn&rsquo;t go down, employees don&rsquo;t ask for less money, and the cost of running an office keeps climbing, he said. His view was that Medicare is great at covering what patients need, and does not pay surgeons a fair number for a total hip. Mike called it a powerful note and a discussion for down the line, and Dave said he hopes to have Dr. Leighton back.</p>
<p>Before that, Dave had slipped in the joke of the week, about a boy who comes home from biology class with a question about evolution. The punch line belongs to his mom, and it&rsquo;s best heard in Dave&rsquo;s delivery.</p>

<h2>Hear the whole conversation</h2>
<p>Dr. Leighton practices in Palm Beach Gardens, and on air Mike gave his office line as 561-727-1318. If you live near his office, our page for <a href="../locations/palm-beach-gardens.html">Palm Beach Gardens patients</a> explains how therapy with us works from there.</p>
<p>Listen to the full episode on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch it in our <a href="../videos.html">video library</a>, and catch the show live Saturdays at 8:30 AM on 100.3 Legends Radio. If hip pain is starting to decide how often you play, or a hip replacement is on your calendar and you want to go in prepared, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep9-sabesan": {
        "title": "Why Rotator Cuff Repairs Struggle to Heal: Dr. Vani Sabesan on Pain 2 Power",
        "date": "October 2026",
        "iso": "2026-10-25",
        "tag": "Pain 2 Power",
        "teaser": "Shoulder surgeon Dr. Vani Sabesan on why rotator cuff repairs struggle to heal after 60, knotless sutures, robots as marketing, and a crushed elbow saved.",
        "body": """
<p>Most surgeons, asked about rotator cuff repair on the radio, would talk about how well it goes. Dr. Vani Sabesan, MD, an orthopaedic shoulder surgeon with the Orthopedic Center of Palm Beach County, led with the hard part instead. &ldquo;We&rsquo;re really good at fixing them,&rdquo; she told Dave and Mike on Episode 9 of Pain 2 Power. &ldquo;We&rsquo;re not great at getting them to heal.&rdquo;</p>
<p>That one sentence explains a lot about shoulder surgery, and about why the months after it matter so much. The rest of the half hour covered how she decides when to change a technique, why she thinks a lot of new technology is marketing, a crushed elbow that came home from Nashville, and why, in her words, nobody is at the end of the line.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>Seventeen million rotator cuffs, and one in three over 60</h2>
<p>Dave brought up patch augmentations and biologics, a part of shoulder surgery he said not every surgeon is into. Dr. Sabesan started with the size of the problem. By her figure, about 17 million people suffer from a rotator cuff problem. Then she made it local. Sit in any retirement community, she said, and among the people over 60 around you, &ldquo;one out of three people are going to have a rotator cuff pathology.&rdquo;</p>
<p>So tears are common, and repairing them is something surgeons do well. Getting the repaired tendon to knit back to the bone is the part she called the weak spot. If you&rsquo;ve had a cuff repair, or someone has told you that you might need one, that is the window your surgeon and your therapist are both working around.</p>
<h3>Why age changes the healing math</h3>
<p>Her explanation was plain biology. &ldquo;I tell people in Palm Beach, 90 is the new 70,&rdquo; she said. People here stay active far longer than they used to. The tissue doesn&rsquo;t get the memo. &ldquo;Our blood cells, our biology isn&rsquo;t as good as when we were 20.&rdquo;</p>
<p>That is the gap she is trying to close. Someone in their seventies who still plays several mornings a week wants a shoulder that keeps up, but the tendon being repaired is the age it is. Wanting it badly enough doesn&rsquo;t change the tissue.</p>
<h3>What a scaffold is meant to do</h3>
<p>Her answer to that gap is a scaffold placed with the repair. She described the goal in her own terms: if you can create something that gives the tendon &ldquo;a better chance to be 20 again, or 40, or maybe even just 60 again, you&rsquo;re going to get better healing of that rotator cuff.&rdquo;</p>
<p>Mike connected it to something the show comes back to often, that the body is a self healing mechanism if you let it be. The surgeon replaces or reinforces what needs it, and the body handles the rest. Whether a scaffold or patch is right for any particular shoulder is a decision for the surgeon doing the repair. What she made clear is why the idea exists at all.</p>

<h2>Legacy, legends and evidence: how a surgeon decides to change</h2>
<p>Dave opened the interview with a question he had been waiting to ask. The week before, Dr. Ryan Simovitch had talked about what to do and avoid after a reverse total shoulder. Dave pointed out that Dr. Sabesan has her reverse patients reaching behind them to put a hand in a back pocket within a couple of weeks. What does she do differently?</p>
<p>Her answer was a framework more than a technique. &ldquo;Sometimes we build techniques based on legacy, sometimes we do legends, and sometimes we do evidence,&rdquo; she said. She trained under some of the legends of shoulder replacement, and she credited one mentor in particular with helping develop the early systems. She also said she lives by his words about evidence.</p>
<p>That is how her practice ended up testing six weeks in a sling against moving within days, a study we covered in detail in <a href="reverse-shoulder-replacement-explained.html">Total vs. Reverse Shoulder Replacement: How Surgeons Decide</a>. Her summary of the lesson was short: when the evidence shows something, &ldquo;you have to change what you do.&rdquo;</p>
<h3>Knotless sutures, fourteen years ago</h3>
<p>Dave asked about knotless rotator cuff repair, which he said makes a huge difference in the healing process. She said she started using knotless sutures about 14 years ago, at the suggestion of her residents and the device reps in her operating room. &ldquo;And at the time, it was a heresy to do it,&rdquo; she said. Mike&rsquo;s reaction was that plenty of ideas in history were called heresy before they were accepted.</p>
<p>You don&rsquo;t need to know what a knotless anchor looks like to get the point. Repair techniques keep changing, and some of the changes started as a suggestion from someone junior in the room.</p>
<h3>Taking advice from the youngest people in the room</h3>
<p>She was candid about where some of her best ideas come from. &ldquo;I have young guys in the OR, reps, students, residents, and they&rsquo;ll sort of say, hey, why don&rsquo;t you try doing it this way? It might be better.&rdquo; She takes it all with a grain of salt, she added, and looks for evidence behind it before anything changes. Then she said something about her own approach to patients: &ldquo;I mean, you listen to your patients and you hear what their needs are and you try to advance what you do, how you do it with that.&rdquo;</p>

<h2>First of many to come</h2>
<p>Mike made sure the audience knew who was sitting at the table. In the Florida Orthopaedic Society&rsquo;s history (Mike put it at 75 years; she said 73 or 74 while she was still checking the number), the society had never chosen a woman as president until her. Mike called it a huge feather in her cap.</p>
<p>She passed the credit to her students. &ldquo;Well, you know, I think it&rsquo;s not about my cap,&rdquo; she said. Her research fellows and medical students printed hats that read &ldquo;first of many to come,&rdquo; and that, she said, is the legacy she wants to leave.</p>
<p>Teaching runs through everything she said. She told the hosts she has trained probably over 100 medical students, and her mentees started a site called YourMedMom with advice for women and anyone who wants to train in orthopaedics. The name came from the way she teaches. She tells it like it is, sometimes things people don&rsquo;t want to hear, the way a mom would, and always in their interest. The reps, she said, call her a spitfire. She also called the operating room her happy place, and said two students had told her that same day it was the most fun they&rsquo;d had.</p>
<p>Dave had a personal reason to agree. His son Nick, sitting just off camera in the studio, worked as an orthopaedic trauma rep and did a lot of work with Dr. Sabesan. Dave said what stood out was that she was friendly with the reps, which he said is not always the case.</p>

<h2>The hour in numbers</h2>
<p>Dr. Sabesan used a lot of specific figures, and every one of them is hers, from her own patients and practice. Here they are in one place, with what she attached to each.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Figures Dr. Vani Sabesan gave on the episode">
<table>
<caption>Figures Dr. Vani Sabesan, MD gave on Pain 2 Power Episode 9, as stated on air. They describe her practice and her experience, not First Rehabilitation&rsquo;s.</caption>
<thead><tr><th scope="col">Figure</th><th scope="col">What she said it refers to</th></tr></thead>
<tbody>
<tr><th scope="row">About 17 million</th><td>People who suffer from a rotator cuff problem, by her estimate</td></tr>
<tr><th scope="row">One in three</th><td>People over 60 who will have a rotator cuff pathology</td></tr>
<tr><th scope="row">98 percent</th><td>Her shoulder replacement patients who said in a survey that their therapist had a huge impact on their outcome</td></tr>
<tr><th scope="row">95 percent</th><td>The same patients who said their therapist changed what they did and how they did it</td></tr>
<tr><th scope="row">14 years</th><td>Roughly how long she has used knotless sutures for rotator cuff repair</td></tr>
<tr><th scope="row">Six offices</th><td>Her practice&rsquo;s locations around Palm Beach County, by her count on the show</td></tr>
<tr><th scope="row">28 marathons</th><td>How many she has run herself; she said she won one</td></tr>
<tr><th scope="row">90 years old</th><td>A patient who came in two days before the taping and still exercises six days a week</td></tr>
</tbody>
</table>
</div>
<p>The therapy survey is the one we like best, for obvious reasons. Her comparison was a hairdresser: someone who talks to you and listens. It&rsquo;s also why every visit here is one-on-one.</p>

<h2>Tech that solves a problem, and tech that only looks good</h2>
<p>Dr. Sabesan said she loves new technology and is part of a design team building implants 3D printed to a patient&rsquo;s own anatomy. She is also skeptical of most of it. Her comparison was the iPhone. The phone itself was an incredible device, she said, but &ldquo;do I think the 16 or the 17 version of it maybe is solving a huge unmet problem? Maybe not.&rdquo; Her field is very implant driven, she said, and it can end up making technology for its own sake.</p>
<p>Her test for anything new is whether it gives the patient less pain, a faster recovery, bone that grows better or a cuff that heals. Robots in shoulder and joint surgery didn&rsquo;t pass it. She said there hasn&rsquo;t been much science showing they are the next panacea, and called them a great marketing tool.</p>
<h3>What the robot doesn&rsquo;t know</h3>
<p>Dave added the therapy side. He said he has seen worse outcomes from some robotic procedures, especially in the knee and the hip, than from a surgeon who knows the patient&rsquo;s anatomy. The robot &ldquo;knows exactly what to do, but it doesn&rsquo;t always know what not to do.&rdquo; Mike called that the modern dilemma in medicine. Dr. Sabesan compared it to AI chat tools, which can get you so far but aren&rsquo;t always accurate. &ldquo;The technology is as good as the user,&rdquo; she said.</p>
<p>If you&rsquo;re choosing a surgeon, that is a fair thing to keep in mind. The tool on the brochure matters less than the person holding it and the plan for afterward.</p>

<h2>Florida plays all year, and the pickleball courts know it</h2>
<p>Mike pointed out how unusual this part of Florida is, with a population that is active and aging at the same time. Dr. Sabesan agreed, and added the other end of it: lots of young families and young athletes. &ldquo;But the problem is, in Florida, we have the indulgence of being able to play all year round.&rdquo;</p>
<p>She was generous about Dave here. She said she sends him her difficult athletes, and that he has gotten some of them back to the MLB level and back to being recruited. Her larger point was about rehab itself: &ldquo;We really have to realize that rehab science in these sports is just as critical, probably maybe more critical than even, or as much of our surgical treatments.&rdquo; She listed Tommy John surgery, rotator cuff surgery, tennis players, pickleball players and baseball players.</p>
<p>Then she described the patients in her own neighborhood who play competitive pickleball six days a week. Some of them come to her with one request. &ldquo;They&rsquo;re like, just shoot me up. Just get anywhere that I can so I can keep going.&rdquo;</p>
<h3>What Dave listens for at the first visit</h3>
<p>Dave had a story of his own from 1990, when he was just starting out. One of his first patients told him to do whatever it took, with one condition: &ldquo;don&rsquo;t stop me from golfing.&rdquo; Dave said that was when he realized how much the game meant to people here, and the clinic&rsquo;s golf and throwing programs grew from there.</p>
<p>The goal isn&rsquo;t always a game, though. Sometimes it&rsquo;s reaching the top shelf again. Whatever you tell your therapist goes into your <a href="../glossary.html#plan-of-care">plan of care</a>, Dave said, because your own description of the problem shapes the whole assessment. He gave a shoulder example. A patient mentions that it really aches at night, and that detail starts pointing the therapist toward something like a bursitis or a tendonitis. So tell us when it hurts, what you were doing, and how you sleep. Dr. Sabesan&rsquo;s word for all of it was personalized: technology, technique and rehab all fitted to the person, which she called the best success.</p>

<h2>A crushed elbow from Nashville, and no one at the end of the line</h2>
<p>Asked for her most interesting case, Dr. Sabesan told a story she said she thought the patient would be fine with her sharing. A man who runs one of the country clubs up here was on a guys&rsquo; trip in Nashville when a drunk driver hit him. His elbow was destroyed, with severe nerve damage. At Vanderbilt Medical Center he was offered emergency surgery there, or a referral to a friend of the doctor&rsquo;s in Palm Beach, who turned out to be her. He had already looked her up and made an appointment.</p>
<p>The first surgery didn&rsquo;t heal, and a year later he still had severe nerve damage. She took him back for a revision. Six months after that, she said, he had full function back and the nerve damage had turned around, which he never thought would happen. She gave a lot of the credit to him, calling him the most optimistic guy she had ever met.</p>
<h3>Why revisions are her favorite work</h3>
<p>That case sums up how she talked about revisions. She said she probably enjoys the complex cases most, and gets sent a lot of them. &ldquo;No one is at the end of the line to me,&rdquo; she said. &ldquo;We always have a chance of salvaging, making something better.&rdquo; It comes from her own life too. &ldquo;I mean, I&rsquo;ve run 28 marathons,&rdquo; she said, and everyone should at least have a chance to do something active. When Dave asked, she added that she had won one, and that the award was handed to her by a former senior resident of hers who had taken a job in Delaware.</p>
<p>Her picture of the future was the same idea stretched across a lifetime: young athletes with careers that last, and older athletes who get to keep doing what they love. Her example was the 90-year-old who had come in two days before the taping and still exercises six days a week. If you&rsquo;re past 60 and wondering whether strength work is still worth starting, our piece on <a href="strength-training-after-60-fall-prevention.html">strength training after 60</a> is a good next read.</p>

<h2>What this means if your shoulder is the one talking</h2>
<p>None of this tells you what your shoulder needs. That takes an evaluation. But the episode does explain a few things we see every week at our clinic on US-1 in North Palm Beach.</p>
<p>After a repair or a replacement, your surgeon sets the protocol and we follow it. That protocol is built around how the tissue heals, and Dr. Sabesan&rsquo;s point about older biology is exactly why the early weeks are paced the way they are. If you haven&rsquo;t had surgery, our <a href="../treatments/shoulder-pain.html">shoulder pain treatment page</a> covers how we evaluate a sore cuff, and our <a href="../treatments/post-surgical.html">post-surgical rehab page</a> covers recovery after repairs and replacements. Elbow problems fall under our <a href="../treatments/hand-wrist.html">hand, wrist and elbow care</a>, and the wider program is described on our <a href="../services/physical-therapy.html">physical therapy page</a>. The first visit runs about an hour, one-on-one, and treatment usually starts that day. The <a href="../faq.html#getting-started">getting started questions in our FAQ</a> cover the rest.</p>
<p>You can read more about Dr. Sabesan&rsquo;s background on <a href="../guests/sabesan.html">her guest page</a>, hear the whole conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, and watch it in our <a href="../videos.html">video library</a>. The show airs live Saturdays at 8:30 AM on 100.3 Legends Radio.</p>
<p>If a rotator cuff, a stiff elbow or a recovery that has stalled is what brought you here, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>. We see people from all over the north county, including <a href="../locations/palm-beach-gardens.html">Palm Beach Gardens</a> and <a href="../locations/jupiter.html">Jupiter</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "personal-training-with-a-therapist-who-knows-your-injury-history": {
        "title": "Personal Training With a Therapist Who Knows Your Injury History",
        "date": "October 2026",
        "iso": "2026-10-17",
        "tag": "Wellness",
        "teaser": "Why training with a team that treated your injury beats a clipboard at a big box gym, told through Newsmax anchor Shannon Cake's rotator cuff rehab.",
        "body": """
<p>You finished physical therapy for a shoulder, a knee or a back. You feel good. Now you want to train properly, and the trainer at the big box gym hands you a clipboard with a box marked &ldquo;injuries&rdquo; and a pen. That box is where most of what your therapist learned about you goes to disappear.</p>
<p>Personal training with a therapist who knows your injury history works differently. The person writing your program has already seen how your joint moves, where it complains, and how far it came. This post explains what that looks like in practice, using the story Newsmax anchor Shannon Cake told on our Pain 2 Power radio show about rehabbing a torn rotator cuff with us and training on Dave&rsquo;s program along the way.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>What personal training with a therapist who knows your injury history means</h2>
<p>Our <a href="../services/wellness.html">wellness program</a> sits inside the clinic at 733 US Highway 1 in North Palm Beach. It runs one-on-one personal training, post-rehab exercise, small group classes, senior functional fitness and sports performance work. The service page describes the personal training simply: one-on-one sessions designed around your goals, your history, and any conditions we have treated together.</p>
<p>That last clause is the whole point. If you did your physical, occupational or hand therapy with us, the team already has the chart. They know which side was injured, whether there was a surgery, what your range of motion looked like on day one and on your last visit, and which exercises flared it up. Nobody has to reconstruct that from a form you filled in at a front counter.</p>
<p>It also changes who you are talking to. A general fitness trainer may be excellent at programming, but a rotator cuff that was torn eight months ago is a medical history, and reading it well is a clinical skill. Dr. Dave Kashuba, Ph.D., OTR, who founded the clinic in 1991, has spent his career on exactly that overlap.</p>
<h3>Why this is different from a referral to a gym</h3>
<p>Plenty of clinics finish your plan of care, hand you a printout and wish you well. That printout matters, and every patient here leaves with a written home exercise program. The difference with training in the same building is continuity. If your shoulder starts talking back on a Thursday, the people who treated it are down the hall, not across town at another practice that has never seen you.</p>
<h2>From rotator cuff rehab to a 25 minute workout: one patient&rsquo;s path</h2>
<p>Shannon Cake hosts News Now on Newsmax 2 and spent decades as an investigative reporter in West Palm Beach. On Episode 19 of Pain 2 Power she described how she ended up in our clinic. &ldquo;I had torn my rotator cuff and was there as a patient,&rdquo; she said. &ldquo;Dave was great and pushed me in all the right ways. He and his team both.&rdquo;</p>
<p>While she was rehabbing, the team also put her through a full workout, the program she knew as the Captain Kerry workout after another longtime patient, Captain Kerry Titheradge of Bravo&rsquo;s Below Deck. She liked it enough to report on it for television. She was no stranger to exercise either. She taught aerobics in college to help pay the bills and had done one set intensity training back when she had more time for gyms.</p>
<p>Her summary of what made it work was practical. &ldquo;You can do this in about 25 minutes with consistency if you do it the way you&rsquo;ve laid out,&rdquo; she said. &ldquo;Just go in and be really focused and concerted and move quickly, even between your sets.&rdquo;</p>
<h3>Whose workout is it, anyway</h3>
<p>Dave wanted one thing clear on air. The program carries Captain Kerry&rsquo;s name in some circles, but it is Dave&rsquo;s. &ldquo;I studied this for 35 years, putting together a program,&rdquo; he said, built on neuromuscular work and on what exercise does for pain. Captain Kerry does Dave&rsquo;s workout. Mike McGann, his co-host, compared the mix-up to Hydrox and Oreo.</p>
<p>The joke has a serious point under it. A program built by someone who has spent decades treating injuries is designed with the injured joint in mind from the start, rather than having safety bolted on afterwards.</p>
<h2>Why your injury history changes the program</h2>
<p>Two people can walk into the same gym wanting the same thing, a stronger upper body, and need completely different programs. One had a rotator cuff tear. The other had nothing wrong at all. If they both start with heavy overhead pressing, only one of them is going to have a good month.</p>
<p>Knowing the history lets a therapist trained in rehab make specific calls. Which lifts to delay. Which to swap for a cable or band version. How fast to add load. Which soreness is normal training soreness and which looks like the old problem coming back. That last judgment is the one a clipboard can&rsquo;t make.</p>
<p>Age adds to it. Shannon made the point herself on the show: strength work is probably more important for someone her age, and it is the part she has to squeeze into the nooks and crannies of the day. Our <a href="strength-training-after-60-fall-prevention.html">guide to strength training after 60</a> goes into why that matters for balance and falls.</p>
<h3>Questions to ask before you start training after an injury</h3>
<p>Whoever you train with, these are fair questions to put to them in the first session:</p>
<ul>
<li>Have you read my therapy notes, or are you working from what I tell you today?</li>
<li>Which movements are off the table for now, and what will I do instead?</li>
<li>How will we decide when to add weight to the injured side?</li>
<li>What kind of pain means stop, and who do I call if it happens?</li>
<li>If something flares up, can I be re-evaluated without starting over somewhere new?</li>
</ul>
<p>If the answers are vague, that tells you something. Inside our clinic, the last question answers itself, because the therapists who can re-evaluate you work in the same building.</p>
<h2>Fitting strength into a schedule that starts at 4:30 AM</h2>
<p>Most people who stop training after rehab don&rsquo;t stop because of the shoulder. They stop because life fills the space. Shannon&rsquo;s day starts at about 4:30, her first editorial meeting is at 5:30, and she is on the air by 9. So she does the work first. &ldquo;If you&rsquo;re gonna get your workout in, do it first thing in the morning,&rdquo; she said, because &ldquo;it&rsquo;s the hour of the day that gets least interrupted.&rdquo;</p>
<p>Her version is 30 minutes on a bike, a couple of glasses of water, and strength fitted in wherever it goes. Some days she grabs one of her two teenage boys and they lift together. Some days it is 20 or 30 push-ups and some sit-ups. She was frank that it is not always tidy: sometimes it gets interrupted and sometimes it doesn&rsquo;t happen at all.</p>
<h3>Short sessions, done consistently</h3>
<p>That frankness is useful. A 25 minute session you actually do beats an hour-long plan you abandon in March. Mike put it bluntly on the same episode: &ldquo;It&rsquo;s not a matter of not having enough time. It&rsquo;s a matter of what&rsquo;s a priority.&rdquo; His examples were doom scrolling and unboxing videos. Most of us could find 25 minutes in that pile.</p>
<p>A good trainer who knows your history builds the program around the time you really have, not the time you wish you had. Short, focused sessions with little rest between sets are what Shannon liked about Dave&rsquo;s format. They are easy to fit in, and that is what keeps people coming back.</p>
<h2>Post rehab exercise that picks up where therapy left off</h2>
<p>Here is how the wellness program describes its pieces. None of it replaces a plan of care while you still need skilled therapy.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Wellness program services and who they suit">
<table>
<caption>The six parts of the First Rehabilitation wellness program, as listed on our wellness service page. Pricing and schedules are handled by the front desk.</caption>
<thead><tr><th scope="col">Part of the program</th><th scope="col">How the service page describes it</th></tr></thead>
<tbody>
<tr><th scope="row">Personal training</th><td>One-on-one sessions designed around your goals, history, and conditions we have treated together</td></tr>
<tr><th scope="row">Post-rehab exercise</th><td>Structured programs that bridge therapy and independence</td></tr>
<tr><th scope="row">Sports performance</th><td>Strength, mobility and conditioning for active adults and athletes</td></tr>
<tr><th scope="row">Group fitness classes</th><td>Small, supportive classes that make consistency enjoyable</td></tr>
<tr><th scope="row">Senior functional fitness</th><td>Balance, strength and mobility focused on independence and fall prevention</td></tr>
<tr><th scope="row">Lifestyle and injury prevention</th><td>Long-term management and movement coaching</td></tr>
</tbody>
</table>
</div>
<p>Your own plan comes out of a conversation with the team, and if you are still mid-treatment, your therapist decides when you are ready to cross over.</p>
<p>We wrote separately about <a href="gym-program-after-physical-therapy-north-palm-beach.html">your gym program after physical therapy ends</a>, including the band program Dave sends home with patients. This post is about the step after that, when you want a person in the room.</p>
<h2>Training in North Palm Beach, a short drive from Juno Beach and Palm Beach Gardens</h2>
<p>The clinic is on US-1 in North Palm Beach, close to <a href="../locations/juno-beach.html">Juno Beach</a>, Palm Beach Gardens, Lake Park and Jupiter. A lot of the people who train with us did their therapy here first, and the convenience of staying put is a big part of why they keep going. The same parking lot, the same front desk, and a team that remembers you. Dave, as Shannon put it, knows your kids&rsquo; names.</p>
<p>It also helps with what we see most often after discharge. Patients coming off <a href="../treatments/post-surgical.html">post-surgical rehabilitation</a> are the ones most at risk of losing range of motion in the months that follow. Patients with a history of <a href="../treatments/shoulder-pain.html">shoulder pain</a>, like Shannon, need overhead work brought back in carefully rather than all at once.</p>
<h2>What this doesn&rsquo;t replace</h2>
<p>A training session isn&rsquo;t an evaluation. If something new starts hurting, swells, wakes you up at night, or simply won&rsquo;t settle, stop training it and get it looked at. In Florida you can usually start a physical therapy evaluation without a referral.</p>
<p>The money side is separate too. The wellness gym does not take insurance and is a different program from Medicare-covered therapy. Our <a href="../insurance.html#medicare-guide">Medicare guide</a> explains where therapy coverage stops. Memberships, prices and schedules are a front desk conversation, and the <a href="../faq.html#wellness-gym">wellness and gym FAQ</a> covers the common questions. We are not going to guess at numbers here.</p>
<p>If you want to hear Shannon tell the story in her own words, the full episode is on <a href="../podcast.html">the Pain 2 Power podcast page</a>, and we wrote it up in <a href="pain-2-power-ep19-cake.html">our recap of her episode</a>.</p>
<h2>Start with a conversation</h2>
<p>If you finished therapy with us, ask the front desk about personal training the next time you are in. If you did your rehab somewhere else, or you never had any and something is holding you back, an evaluation is the right first step. Either way, call <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>, and we will help you work out what makes sense.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep19-cake": {
        "title": "Shannon Cake on 23 Emmys, a Torn Rotator Cuff and Working Out First Thing",
        "date": "October 2026",
        "iso": "2026-10-17",
        "tag": "Pain 2 Power",
        "teaser": "Newsmax anchor Shannon Cake joins Dave and Mike on her start in consumer reporting, her father's interpreter story, and how she trains before a 4:30 AM news day.",
        "body": """
<p>Before Shannon Cake said a word on this week&rsquo;s Pain 2 Power, Dave had already done the math on her. Take Peter Jennings, Walter Cronkite and Barbara Walters, he told Mike, add up every Emmy the three of them won, and by his count you get 22. &ldquo;Shannon has 23 herself,&rdquo; he said.</p>
<p>She spent the next half hour handing the credit to other people, telling a story about her father and a Chinese interpreter, and explaining how a woman who is on the air by 9 every morning still gets her workout in. That last part is the one most of us can use.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Twenty three Emmys, and she gives the credit away</h2>
<p>Shannon Cake is a name most people in Palm Beach County know from local television. Today she hosts News Now on Newsmax 2, weekdays from 9 to 10 in the morning, and she has been in broadcasting for 35 years. Dave&rsquo;s introduction ran long on purpose. Beyond the Emmys, he pointed out that she won the Edward R. Murrow Award, which Mike, a broadcaster himself, called one of the holy grails of the business.</p>
<p>Her first move was to correct him, politely. &ldquo;I didn&rsquo;t win anything alone. We never do,&rdquo; she said. She started in radio, then worked inside newsroom teams with, as she put it, a lot of folks pushing the buttons. One colleague got singled out: &ldquo;an incredible photographer partner for a bulk of my career. And he really helped me, helped me see things and become, you know, the journalist I am today.&rdquo;</p>
<p>Anyone who has worked in a clinic, a kitchen or a newsroom will recognize that. The face on camera is the last step of a lot of work by people you never see.</p>
<h3>How Newsmax actually found her</h3>
<p>Dave&rsquo;s version was that Newsmax begged her to come over. She corrected that one too. &ldquo;Newsmax didn&rsquo;t beg me,&rdquo; she said. The owner, who built the company from very humble beginnings into what she called a global news operation, happened to be a viewer of her local work. They were introduced, they connected, and he offered her a position. Dave&rsquo;s reply was the best line of the opening segment: &ldquo;It&rsquo;s nice that you&rsquo;re humble that way, but I still like my story.&rdquo;</p>
<h2>From a campus radio station in Tuscaloosa to consumer investigations in West Palm Beach</h2>
<p>Mike asked what made her want to be a reporter in the first place, and the answer started with her father. He served in the military with an armored cavalry division, so the family was stationed in Germany, and later he moved into the diplomatic and intelligence side of government. The family lived in Singapore and Hong Kong, and China was his specialty. Her brother became an auditor. She became an investigative reporter. In her telling, the way their parents raised them was the common thread: you were representing the nation, and you were supposed to do the right thing.</p>
<p>&ldquo;And the injustice of consumer work really struck me at a very young age,&rdquo; she said. Her first job in radio was at the NPR affiliate at the University of Alabama in Tuscaloosa, with some sports work in that market on the side. Then a position opened in the consumer investigative division of a West Palm Beach station, and that was the job that stuck.</p>
<h3>One story, one evening</h3>
<p>The quote that kept her in that arena came from a friend. Dave Aronberg, whom she described as a former state attorney here in South Florida, met her when they were both starting out, she as a young consumer reporter and he as a young assistant attorney general. Years later she told him over lunch that maybe she had missed her calling and should have gone to law school. His answer, as she remembers it: &ldquo;with one story, one story in an evening, you can do more sometimes than a lawmaker can do their entire career.&rdquo;</p>
<p>Dave added some of what that looked like in practice. Her investigative work helped expose Medicare fraud and pushed on highway safety, and she has given her time to grassroots nonprofits including Believe With Me, which supports Gold Star families, and the Wounded Veterans Relief Fund. She also helped Remember Me, the early onset dementia foundation Dave has talked about on earlier episodes.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Shannon Cake's career as described on the episode">
<table>
<caption>Shannon Cake&rsquo;s career as she and Dave Kashuba described it on Pain 2 Power Episode 19. Awards and titles are as stated on air.</caption>
<thead><tr><th scope="col">Stage</th><th scope="col">What was said on the show</th></tr></thead>
<tbody>
<tr><th scope="row">Growing up</th><td>Military family stationed in Germany, then Singapore and Hong Kong; her father&rsquo;s specialty was China</td></tr>
<tr><th scope="row">First job</th><td>Radio at the NPR affiliate at the University of Alabama in Tuscaloosa, plus local sports work</td></tr>
<tr><th scope="row">Palm Beach County</th><td>Consumer investigative reporting at a West Palm Beach station, including Medicare fraud and highway safety stories</td></tr>
<tr><th scope="row">Recognition</th><td>23 Emmys and the Edward R. Murrow Award, per Dave&rsquo;s introduction, over 35 years in broadcasting</td></tr>
<tr><th scope="row">Today</th><td>Host of News Now on Newsmax 2, 9 to 10 AM weekdays</td></tr>
</tbody>
</table>
</div>
<h2>The interpreter who wasn&rsquo;t interpreting</h2>
<p>Dave knows her parents a little, and he asked her to tell a story he had heard secondhand. After her father retired from government (he finished at the China desk at the Pentagon, she said), he went into the import and export business, silk and steel, with two partners. Going into a negotiation in China, the other side would often offer the visiting businessman one of their own interpreters.</p>
<p>Her advice, passed down from him, was to bring your own. If you accept the kind offer, she said, &ldquo;You can rest assured that you better check your numbers at the end of the meeting. No disrespect. But it is part of business.&rdquo; Her father had an advantage most visitors did not. He spoke the language, so he knew exactly what was being said across the table. She would not say much more about how he went in, only that he was armed and ready, and that he came out with a couple of good deals.</p>
<p>Mike, who thinks about words for a living, put it neatly. Change a couple of words here and there, pick one with the same denotation but a different connotation, and watch what happens.</p>
<h2>Headaches, and what Dave says therapy can and can&rsquo;t do</h2>
<p>Dave and Shannon have a friend in common, a Palm Beach County neurologist she called one of the most brilliant on the planet, whom she saw a few years back for dizzy spells and headaches. She said they have not bothered her much in recent years. Her main takeaway from those visits was blunt: she used to blame the headaches on allergy season, and he told her a headache is a headache.</p>
<p>That gave Dave an opening to talk about the headache patients physical therapy sees all the time. He was careful about the limits. &ldquo;We can&rsquo;t stop the migraine because migraine is actually a systemic problem, but we can stop the triggering to migraines,&rdquo; he said. He added that &ldquo;exercise and staying physically fit is key to actually reducing headaches.&rdquo;</p>
<p>That matches how we describe it on our <a href="../treatments/headache-relief.html">headache treatment page</a>: we treat headaches that start in the neck, tension headaches, and neck related migraine triggers, and we do not claim to cure migraine. If yours seem to start at the base of your skull, our longer piece on <a href="headaches-that-start-in-the-neck.html">headaches that start in the neck</a> walks through what an evaluation looks for.</p>
<h2>Up at 4:30, and 30 minutes on the bike</h2>
<p>Then Dave asked the question he had invited her on to answer. How does someone with her schedule stay in shape?</p>
<p>Her answer was refreshingly unglamorous. She learned early that &ldquo;if you&rsquo;re gonna get your workout in, do it first thing in the morning.&rdquo; Nothing about the hour itself is magic for strength or weight loss, she said. &ldquo;It&rsquo;s the hour of the day that gets least interrupted.&rdquo;</p>
<p>Her day now starts at about 4:30, catching up on whatever happened overnight, because the network covers the globe. The first editorial meeting is at 5:30 and she is on the air by 9. So the bike comes first. &ldquo;If I don&rsquo;t wake up and get on that bike, even with my eyelids half closed, by the time that 30 minutes is over, I&rsquo;m definitely awake,&rdquo; she said. A couple of glasses of water, some cardio done, and then strength gets squeezed into the nooks and crannies of the day.</p>
<h3>Teenage boys, push-ups, and honesty</h3>
<p>She has two teenage boys, and some days she grabs one and says, let&rsquo;s go lift a little bit. Other days it is 20 or 30 push-ups and some sit-ups. And she was honest about the rest: &ldquo;it&rsquo;s not pretty and sometimes it gets interrupted and sometimes it doesn&rsquo;t happen at all.&rdquo; She also said strength work is probably more important for someone her age, and that it is the part she has to squeeze in.</p>
<h3>Mike&rsquo;s rule: priorities, not time</h3>
<p>Mike took it from there. &ldquo;It&rsquo;s not a matter of not having enough time. It&rsquo;s a matter of what&rsquo;s a priority,&rdquo; he said, repeating something he had heard recently. The time is usually there if you stop doom scrolling, he argued, and find something a bit more personally productive than unboxing videos.</p>
<h2>A torn rotator cuff, and the workout with Dave&rsquo;s name on it</h2>
<p>Shannon and Dave first met because she got hurt. &ldquo;I had torn my rotator cuff and was there as a patient,&rdquo; she said, describing her time at the clinic here on US-1. &ldquo;Dave was great and pushed me in all the right ways. He and his team both.&rdquo; What stuck with her was how personal it felt. He knows your kids&rsquo; names, she said, and asks after your mother if she has been sick.</p>
<p>While she was rehabbing, the team put her through the workout people know as the Captain Kerry workout, after Captain Kerry Titheradge of Bravo&rsquo;s Below Deck, a longtime patient and an earlier guest on the show. She liked it enough to do a television story on it. She used to teach aerobics in college to help pay the bills and had done one set intensity training when she had more time for gyms, so the format felt familiar. Her verdict was that &ldquo;you can do this in about 25 minutes with consistency if you do it the way you&rsquo;ve laid out,&rdquo; and the trick is to &ldquo;move quickly, even between your sets.&rdquo;</p>
<p>Dave, who had been waiting for this, wanted one correction on the record. Captain Kerry does Dave&rsquo;s workout, not the other way around. &ldquo;I studied this for 35 years, putting together a program,&rdquo; he said, built on neuromuscular work and on what exercise does for pain. As he tells it, that was his reaction when Shannon told her TV audience to try the Captain Kerry workout. The studio enjoyed it. Mike compared it to Hydrox, the cookie that came before Oreo and somehow became known as the knockoff.</p>
<p>If you are dealing with a shoulder of your own, our <a href="../treatments/shoulder-pain.html">shoulder pain page</a> covers what rotator cuff rehab involves, and our <a href="../services/wellness.html">wellness program</a> is where patients keep training once therapy ends. We wrote about that second step in more detail in <a href="personal-training-with-a-therapist-who-knows-your-injury-history.html">personal training with a therapist who knows your injury history</a>.</p>
<h2>Two antennas and a reminder to vote</h2>
<p>Dave closed with the joke of the week, which he admitted he borrowed from Mike. Two antennas on neighboring roofs start liking each other, get engaged and get married. &ldquo;I was invited to the wedding, which wasn&rsquo;t that great, but you know what? The reception was so good.&rdquo; Shannon&rsquo;s response was a heartfelt &ldquo;God bless you, Dave.&rdquo;</p>
<p>His last word was about the election. If you know someone who always votes the other way, he said, and you go vote, you cancel her vote out. Get two people to vote and you are ahead. &ldquo;I don&rsquo;t care who you vote for. People have died to give us the right to vote.&rdquo; Mike noted that Dave was literally pounding.</p>
<p>Dave promised to have her back. He said he had been asking her since April or May.</p>
<p>Listen to the full conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch past episodes in our <a href="../videos.html">video library</a>, and catch the show live Saturdays at 8:30 AM on 100.3 Legends Radio. If a shoulder, a headache or a stalled workout routine is what brought you here, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "physical-therapy-and-rehab-services-in-north-palm-beach-what-we-treat": {
        "title": "Physical Therapy and Rehab Services in North Palm Beach: What We Treat",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "October 2026",
        "iso": "2026-10-12",
        "tag": "Physical Therapy",
        "teaser": "You tweaked your back lifting a kayak onto the roof rack. Your shoulder has ached since you started playing pickleball four mornings a week. Your knee\u2026",
        "body": """
<p>You tweaked your back lifting a kayak onto the roof rack. Your shoulder has ached since you started playing pickleball four mornings a week. Your knee replacement was six weeks ago and the surgeon said to start therapy, but didn't say where. Or maybe nothing dramatic happened at all. You just noticed that getting up from the couch takes a little more effort than it used to, and you'd like to do something about it before it gets worse.</p>
<p>Whatever brought you here, the question is usually the same: is there somewhere close by that can actually help with <em>this</em>, and how soon can they see me?</p>
<p>This post walks through the conditions we see most and what treatment involves, then how the physical, occupational and hand therapy sides fit together under one roof on US-1.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>The problems that fill our schedule</h2>
<p>Physical therapy covers a lot of ground, so it helps to be specific. These are the problems we treat week in, week out.</p>
<h3>Back and neck pain</h3>
<p>Low back pain is one of the most common reasons people call us. Sometimes it's a disc, sometimes it's a strained muscle, and very often it's years of sitting at a desk with a monitor set two inches too low. Sciatica, the pain that travels from the back or buttock down the leg, is on the list too, and so is spinal stenosis. Neck pain and <a href="../treatments/headache-relief.html">the headaches that come with it</a> often trace back to the same habits. We figure out which it is before we treat it, and that sometimes means looking at your hips, since a stiff hip can masquerade as back pain.</p>
<h3>Shoulders</h3>
<p>Rotator cuff strains, tears and repairs, frozen shoulder, impingement, bursitis and tendinitis, and recovery after shoulder surgery, including reverse shoulder replacement. Shoulders don't tend to sort themselves out. They get stiffer and more guarded the longer you wait, and people start sleeping on the other side and reaching with the other arm without really noticing.</p>
<h3>Knees and hips</h3>
<p>Osteoarthritis, meniscus and ligament injuries, kneecap pain, hip bursitis, labral irritation, and the general wear that shows up after decades of walking around on them. We also work with people before surgery, so they go into a joint replacement stronger, and after it, from the first bend to full stride.</p>
<h3>Hands, wrists and elbows</h3>
<p>This is where our certified hand therapy program comes in. Laura Drumm, MS, OTR/L, CHT, CLT, leads it, and custom splints are made right in the clinic. Carpal tunnel, trigger finger, thumb arthritis, wrist fractures, tendon repairs and tennis elbow all live here.</p>
<h3>Balance, falls and neurological rehab</h3>
<p>If you've had a fall, or you've started holding the railing on stairs you used to take without thinking, tell us about it. Balance is trainable, and it responds to focused work. The same program covers vestibular work and recovery after a stroke (see <a href="post-stroke-occupational-therapy-north-palm-beach.html">how occupational therapy helps after a stroke</a>), as well as conditions like Parkinson's and multiple sclerosis, working on gait, strength, coordination and the practical business of moving through a day safely.</p>
<h3>Work injuries and car accidents</h3>
<p>Repetitive strain, lifting injuries, whiplash and soft tissue damage after a crash. These come with adjusters, case managers and reporting requirements, and we handle that side of it too. After a car accident in Florida, your personal injury protection pays for medical care only if initial care starts within 14 days of the crash (section 627.736, 2026 Florida Statutes), and therapy is follow-up care a physician refers you to. So see a doctor first. Our page on <a href="../treatments/auto-accident.html">therapy after a car accident</a> explains how it works from there.</p>

<h2>A quick map of what we treat</h2>
<p>If you'd rather scan than read, here's the short version, region by region. Each row links to the page with the detail.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Conditions we treat, by body area">
<table>
<caption>Condensed from the condition lists on our treatment pages at firstrehabnpb.com/treatments. Not a complete list; call if yours isn't here.</caption>
<thead><tr><th scope="col">Area</th><th scope="col">Common problems on our list</th><th scope="col">Read more</th></tr></thead>
<tbody>
<tr><th scope="row">Low back and spine</th><td>Low back pain and stiffness, sciatica, herniated and bulging discs, degenerative disc disease, spinal stenosis, spine surgery recovery</td><td><a href="../treatments/back-pain.html">Back pain</a></td></tr>
<tr><th scope="row">Neck and head</th><td>Stiff neck, whiplash, pinched nerve, pain into the shoulder or arm, headaches that start in the neck</td><td><a href="../treatments/neck-pain.html">Neck pain</a></td></tr>
<tr><th scope="row">Shoulder</th><td>Rotator cuff strains and repairs, frozen shoulder, impingement, bursitis, labral injuries, instability</td><td><a href="../treatments/shoulder-pain.html">Shoulder pain</a></td></tr>
<tr><th scope="row">Hip and pelvis</th><td>Hip arthritis, hip replacement rehab, bursitis, labral irritation, groin and hip flexor strains</td><td><a href="../treatments/hip-pain.html">Hip pain</a></td></tr>
<tr><th scope="row">Knee</th><td>Knee arthritis, partial and total knee replacement rehab, ACL, MCL and meniscus injuries, runner's knee</td><td><a href="../treatments/knee-pain.html">Knee pain</a></td></tr>
<tr><th scope="row">Foot and ankle</th><td>Plantar fasciitis, ankle sprains and instability, Achilles problems, recovery after a fracture</td><td><a href="../treatments/ankle-pain.html">Ankle pain</a></td></tr>
<tr><th scope="row">Hand, wrist and elbow</th><td>Carpal tunnel, wrist fractures, tendon repairs, trigger finger, thumb arthritis, tennis elbow</td><td><a href="../treatments/hand-wrist.html">Hand and wrist</a></td></tr>
<tr><th scope="row">After surgery</th><td>Knee and hip replacement, rotator cuff repair, spine, hand, foot and ankle surgery, fracture fixation</td><td><a href="../treatments/post-surgical.html">Post-surgical rehab</a></td></tr>
<tr><th scope="row">Work injuries</th><td>Lifting and overexertion, repetitive strain, slips, trips and falls on the job</td><td><a href="../treatments/workers-comp.html">Work injury rehab</a></td></tr>
</tbody>
</table>
</div>
<p>If your problem isn't on that list, call anyway. The front desk will give you an honest answer about whether it's something we treat, and if it isn't, we'll say so.</p>

<h2>Golf, tennis and pickleball: the local wear and tear</h2>
<p>North Palm Beach has a lot of people playing year-round, and we see the results: ankle sprains, hamstring strains, tennis and golfer's elbow, sore rotator cuffs, and the overuse injuries that come with repeating the same motion several thousand times a season.</p>
<p>Orthopedic shoulder surgeon Dr. Ryan Simovitch described the patient he worries about most on Episode 8 of our Pain 2 Power show, and it wasn't the weekend warrior. &ldquo;I think it's the constant warrior,&rdquo; he said, the person playing pickleball four to six days a week, where &ldquo;there's no moderation, there's no preparation.&rdquo;</p>
<p>Dr. Vani Sabesan, MD, an orthopaedic shoulder surgeon and the first female president of the Florida Orthopaedic Society, made the same point about our weather on Episode 9: in Florida &ldquo;we have the indulgence of being able to play all year round.&rdquo; She was also clear about how much the recovery side matters. &ldquo;We really have to realize that rehab science in these sports is just as critical, probably maybe more critical than even, or as much of our surgical treatments.&rdquo;</p>
<p>Golf has been part of the clinic's story for a long time. On that same episode Dave told the story of an early patient who said, &ldquo;I'll do whatever it takes, but don't stop me from golfing.&rdquo; He said that's what got him building golf and throwing programs. And tennis elbow, despite the name, is mostly not a tennis injury. Dr. Matt Butler, MD, a hand and upper extremity surgeon who was our guest on Episode 16, called it close to a rite of passage in middle age, and said that when he's the first stop for it, he usually sends the patient to Dave.</p>

<h2>What treatment actually involves</h2>
<p>A lot of people picture physical therapy as a room full of exercise bikes. Some of it is exercise, but the exercise is chosen deliberately, and it's rarely the whole picture.</p>
<h3>Manual therapy</h3>
<p>Hands-on work: joint mobilization, soft tissue release, stretching done with resistance we control. This is often what gets a stiff joint moving enough that the exercise part becomes possible. For a stubborn tennis elbow, Dave described on Episode 16 how that can include active release technique, blood flow restriction training and dynamic cupping.</p>
<h3>Therapeutic exercise</h3>
<p>Progressive strengthening and mobility work aimed at the specific weakness behind your problem, rather than general fitness. If your hip pain comes from a weak gluteus medius, that's what we train, with moves like banded sit to stands and clams. The exercises get harder as you get stronger, so you won't be doing the same routine on week six that you did on day one.</p>
<h3>Gait and balance training</h3>
<p>Retraining how you walk and how you recover when your weight shifts unexpectedly: a curb, a wet pool deck, a dog on a leash.</p>
<h3>Modalities and massage</h3>
<p>Heat and ice and electrical stimulation, used where they help with pain and inflammation. Therapeutic massage is offered alongside your therapy program too, as part of the session rather than an extra you book separately. All of these support the work rather than replace it.</p>
<h3>Home exercise programs</h3>
<p>The hour you spend with us matters less than what happens the other 167. We send you home with specific, manageable work, and we check that you can do it correctly before you leave. Our <a href="../exercises.html">home exercises page</a> has the knee, hip, shoulder and everyday sets Dave has described on air, with sets and reps.</p>

<h2>Physical, occupational or hand therapy?</h2>
<p>We're a Medicare-certified Comprehensive Outpatient Rehabilitation Facility, which in practice means physical therapy, occupational therapy and certified hand therapy happen in the same building, with the same team reading the same notes. Plenty of patients need more than one.</p>
<p>Roughly: physical therapy works on how you move, the strength, range and mechanics. Occupational therapy works on what you need to get done, from buttoning a shirt to getting back to your job. Hand therapy is the specialist end of both for the hand, wrist and elbow. You don't have to work out which you need before you call. The evaluation decides, and our post on <a href="physical-therapy-vs-occupational-therapy.html">PT versus OT</a> explains the difference in more detail.</p>
<p>And when formal therapy ends, there's somewhere to go next. Our on-site <a href="../services/wellness.html">wellness gym</a> lets patients keep training with a team that already knows their history. It's a separate program that doesn't take insurance, so the front desk explains how it works before anyone signs up.</p>

<h2>Your first visit, in brief</h2>
<p>The first appointment is an evaluation, about an hour, one-on-one. We'll ask what's happening, when it started, what makes it worse, and what you're hoping to get back to, whether that's a golf swing or a full night's sleep without rolling onto the bad shoulder. Then we assess range of motion, strength, how you move, where it hurts and where it doesn't, and build a plan with realistic milestones. Treatment usually starts that same day.</p>
<p>If we think your problem needs a different kind of care, such as imaging, a surgical consult or a specialist, we'll say so. That's part of the evaluation too.</p>
<p>In most cases Florida's direct access law lets you start a physical therapy evaluation without a referral. Some plans still want one, and Medicare needs a physician to certify your plan of care. The front desk checks your plan and verifies your benefits before your first visit. For the full walkthrough, read <a href="what-to-expect-first-pt-visit.html">what to expect at your first physical therapy visit</a>, and if you're on Medicare, our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> covers deductibles and coinsurance.</p>

<h2>Why close to home matters more than you'd think</h2>
<p>Physical therapy is rarely a one-visit fix. Most plans involve regular visits over a number of weeks, and the exact count depends on your condition and how you respond. That's a lot of trips.</p>
<p>A clinic twenty-five minutes away looks reasonable on paper. By week three, when it's raining and traffic on US-1 is backed up, it's the reason people start skipping appointments, and consistent attendance is one of the biggest drivers of a good outcome. Choosing somewhere close to home or work is one of the more practical decisions you'll make about your care. We're at 733 US Highway 1, Suite 2A, with a free lot at the building, a short drive from Palm Beach Gardens, Juno Beach and Jupiter.</p>
<p>We've been treating patients in this community since 1991, family-owned the whole time, and we're rated 4.9 stars on Google. You can <a href="../about.html">meet the team here</a>, and see the <a href="../services/physical-therapy.html">full breakdown of our physical therapy services</a> if you want detail on a specific approach.</p>

<h2>Booking an evaluation</h2>
<p>If something's been hurting for more than a couple of weeks, or you've been told to start therapy after a surgery or injury, don't wait for it to sort itself out. Most things we treat respond better when they're addressed early.</p>
<p>Call First Rehabilitation of North Palm Beach at <strong>561-624-4263</strong> to schedule an evaluation, or <a href="../contact.html">request an appointment online</a>. Tell us what's going on and we'll find you a time, Monday to Friday 8:00 AM to 5:30 PM or Saturday 8:00 AM to 12:30 PM.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "strength-training-after-60-fall-prevention": {
        "title": "Strength Training After 60: Where to Start",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "September 2026",
        "iso": "2026-09-21",
        "tag": "Wellness",
        "teaser": "Why sitting is the quiet risk as you age, and what a short daily movement habit plus supervised strength work do for fall risk and independence.",
        "body": """
<p>Somewhere between fifty and sixty, gravity starts winning arguments it used to lose. The shoulders round forward, the head drifts ahead of the spine, and most people blame age instead of the eight or ten hours a day they spend sitting down.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<p>This post is for the person who has noticed it starting. You stand up from the couch in two tries instead of one. You hold the rail on the stairs at the condo even though nobody told you to. A walk along the Intracoastal you used to love now feels like something to schedule around. None of that is an emergency, but it tells you something, and the earlier you act on it, the more there is to keep.</p>
<h2>The chair is doing more damage than the years are</h2>
<p>&ldquo;The invention of the chair is one of our demise,&rdquo; says Dr. Dave Kashuba, Ph.D., founder of First Rehabilitation and an occupational therapist who has treated patients since 1991. He means what happens to a body that spends most of the day in one position: forward head posture, tight hips, and blood flow that slows down instead of circulating. &ldquo;That's just gravity, that's how life is,&rdquo; he says of the forward drift that comes with age, &ldquo;but we want to walk every day, we want to try to get the blood flowing.&rdquo;</p>
<p>Think about a normal day for a lot of our patients. Coffee in the chair by the window. The drive down US-1 to an appointment. Lunch at a table, an afternoon with a book or a screen, dinner, then the recliner for the evening news. Every one of those is reasonable. Stack them together and the legs barely work from breakfast to bed.</p>
<p>That matters more in this part of Florida than most. Two thirds of the people we treat are 65 or older, which is why our front desk spends so much of the day on Medicare questions. Danielle Armstrong, who owns Pilates Life on Northlake in Palm Beach Gardens, described the same crowd on Episode 18 of our Pain 2 Power show. People here, she said, &ldquo;are looking for that longevity,&rdquo; and what they really want from exercise is help with ordinary life: &ldquo;Things like reaching for something on a shelf or bringing their garbage out or bringing in groceries.&rdquo;</p>
<h2>Ten minutes counts, and it beats waiting for an hour you never get</h2>
<p>The advice Dave gives patients starts small, on purpose. &ldquo;Just a little bit of exercises, ten, fifteen minutes a day, three minutes a day, and work your way up,&rdquo; he says. Put the phone down, get up, walk, do a few sit to stands, and repeat that through the day rather than saving it for one long session. The goal is motion that happens often. Perfect form on a Saturday morning matters less than ordinary movement on a Tuesday afternoon.</p>
<h3>What &ldquo;a little bit&rdquo; looks like in a real day</h3>
<p>Three minutes is not a typo. If walking to the mailbox and back is where you are, then that is the starting line, and the job is to do it again after lunch and again before dinner. Stand up during every commercial break. Do five sit to stands before you sit down to eat. Walk the length of the parking lot at Publix instead of circling for the closest spot. Each piece is tiny. Spread across a week, they add up to a habit your legs notice.</p>
<p>Dave's list on our <a href="../exercises.html#everyday">home exercises page</a> calls this the baseline, the floor you build everything else on.</p>
<h3>Sit to stands, the test you can do in your kitchen</h3>
<p>Rising from a chair without using your hands is one of the simplest tests of leg strength there is, and it is the same movement that keeps someone able to get off a low couch, a car seat, or the toilet without help. Losing it rarely announces itself. It slips a little at a time until a fall makes it obvious.</p>
<p>The same movement is also the exercise. Our therapists use three versions of it, and all three are on the exercises page with the sets and reps Dave gives patients.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Three versions of the sit to stand from our home exercises page">
<table>
<caption>Three sit to stand variations, with sets and reps as listed on our home exercises page (Dave Kashuba, Pain 2 Power Episodes 6, 8 and 10).</caption>
<thead><tr><th scope="col">Version</th><th scope="col">How to do it</th><th scope="col">Sets and reps</th><th scope="col">Why it helps</th></tr></thead>
<tbody>
<tr><th scope="row">Plain sit to stand</th><td>Stand up out of a chair and sit back down, without pushing off with your hands if you can manage it.</td><td>Little and often</td><td>The most functional movement most people stop practising.</td></tr>
<tr><th scope="row">Pillow sit to stand</th><td>Hold a light pillow out in front of you and push it forward as you stand, keeping it forward as you sit back down.</td><td>3 sets of 10</td><td>Makes you hinge at the hip, so the hips carry the load instead of the knees.</td></tr>
<tr><th scope="row">Banded sit to stand</th><td>Loop a resistance band around both legs just above the knees, then stand and sit as normal.</td><td>3 sets of 10</td><td>Stops you shifting your weight onto the good leg without noticing.</td></tr>
</tbody>
</table>
</div>
<p>If any of these causes sharp pain, or you feel unsteady doing them, stop. That is a sign to get evaluated first, which we come back to below.</p>
<h2>Balance and strength are the same project</h2>
<p>Most falls have a long run-up. Hips get a little weaker and reaction time slows down, without anyone noticing. Then one day the curb outside the restaurant is an inch higher than you expected. Supervised strength training after 60 works on both halves at once: the muscle that holds you up, and the balance reactions that catch you when something shifts under your feet.</p>
<h3>Start before there is a problem</h3>
<p>Danielle Armstrong made the point on Episode 18 that balance work belongs early, before the first scare. &ldquo;You want to start doing it early so that you know how to keep strong,&rdquo; she said. &ldquo;Prevention is better than a cure.&rdquo; Mike McGann, Dave's co-host, put it in the language of daily life: balance and muscle strength are what make walking, taking the garbage out, and getting in and out of the shower or the bathtub safe.</p>
<p>Our glossary describes <a href="../glossary.html#balance-training">balance training</a> as exercises that challenge your steadiness on purpose, like standing on one foot while reaching. Done with someone beside you, that challenge is safe. Done alone on a slippery tile floor, it can be the very thing you were trying to avoid.</p>
<h3>Sleep and recovery count too</h3>
<p>Elyse Marrone, RD/LDN, CGP, a registered dietitian who sees patients in Jupiter and joined Danielle on the same episode, said this about deep sleep: &ldquo;I know you can increase it by exercise.&rdquo; Her goal for patients is one most of ours would sign up for: &ldquo;I want to be healthy, healthy, healthy, dead.&rdquo; In other words, stay capable for as long as possible instead of sliding slowly into decline. Strength and balance are a big part of the capable half.</p>
<h2>If pain is why you have been sitting more</h2>
<p>Sometimes the sitting is protection rather than habit. A bad hip, knee, or back makes standing and walking hurt, so the chair starts to feel like the safe choice, and the muscles that would have supported those joints get weaker from disuse. We see this constantly in patients recovering from <a href="../treatments/hip-pain.html">hip pain</a>, <a href="../treatments/knee-pain.html">knee pain</a>, and <a href="../treatments/back-pain.html">back pain</a>, and it is exactly the cycle a good evaluation is built to interrupt: treat the pain that is driving the inactivity, then rebuild the strength that inactivity cost.</p>
<p>Picture how it usually goes. You stop your morning walk because a knee aches on the way back. Within a season, getting out of the car takes two hands on the door frame. The knee was the first problem. The weaker legs became the second one, and by the time most people call us, the second one is the bigger of the two.</p>
<p>Patients from <a href="../locations/juno-beach.html">Juno Beach</a> and the surrounding area often ask us the same question at discharge: what now? The exercises do not stop being useful once the pain does. They become the maintenance plan.</p>
<h2>What a fall prevention evaluation looks for</h2>
<p>If you have already had a fall, or a near miss on the stairs, start with your doctor and then an evaluation rather than the gym. The same goes for new dizziness, a recent diagnosis, or a fall you cannot explain. Balance and fall prevention are part of our <a href="../services/physical-therapy.html">physical therapy</a> program, alongside vestibular work for dizziness and neurological rehab.</p>
<p>At the first visit, which runs about an hour, your therapist watches you walk, stand and turn, and measures strength, range of motion and balance. A <a href="../glossary.html#fall-risk-screening">fall-risk screening</a> is often part of it: short tests like standing up from a chair and walking a short distance while the therapist times you. The plan then targets the specific weakness behind the wobble instead of guessing at it, and treatment usually starts that same day.</p>
<p>Every session after that is one-on-one. That matters for balance work in particular, because the exercises that help the most are the ones that feel a little uncertain, and you want a trained person within arm's reach when they do.</p>
<h2>Does Medicare cover this, and what about the gym?</h2>
<p>Coverage is simpler than most people expect. Medicare covers medically necessary physical therapy, and that includes skilled care that helps you hold on to your function or slow a decline, not only care that keeps producing gains. People are often told the opposite. Our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> explains the rule, the deductible, and what you pay per visit. Medicare does need a physician to certify your plan of care, and we handle that paperwork with your doctor. The front desk verifies your benefits before the first visit, so nothing ambushes you.</p>
<p>The flip side is that skilled therapy is the right tool only while you need a therapist's skills. Once a home program you can do safely on your own will keep your progress, we will tell you so. That is where the next step comes in.</p>
<h3>Where the on-site gym fits</h3>
<p>Our <a href="../services/wellness.html">on-site wellness program</a> picks up where formal therapy leaves off. Patients who finish physical or occupational therapy with us can keep training in the same building, with a team that already knows their history, instead of starting over with a trainer who has never seen their chart. Senior functional fitness here is about the strength and balance that keep people independent. Nobody is chasing heavier plates on a bar.</p>
<p>The program covers a range of paces on purpose. Some people want one-on-one personal training built around a specific goal or a joint we already know well. Others do better in a small group class, where it is easier to stay consistent when someone else is expecting you. The gym does not take insurance, and it is a separate program from Medicare-covered therapy. The front desk explains how it works and what it costs before you sign up.</p>
<h2>Book an evaluation</h2>
<p>If you have noticed yourself avoiding stairs or sitting more than you would like to admit, an evaluation is the place to start, ahead of any gym membership you are not sure you are ready for. Most people in Florida can begin a physical therapy evaluation without a referral, and we are open Monday through Friday from 8:00 AM to 5:30 PM and Saturday mornings until 12:30 PM at 733 US Highway 1 in North Palm Beach. Call <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>, and read more in our <a href="../faq.html#wellness-gym">wellness and gym FAQ</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "gym-program-after-physical-therapy-north-palm-beach": {
        "title": "Your Gym Program After Physical Therapy Ends",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "September 2026",
        "iso": "2026-09-21",
        "tag": "Wellness",
        "teaser": "What to do with your home exercises once physical therapy ends, and why an on-site wellness program exists to keep the progress you worked for.",
        "body": """
<p>The day your physical therapy ends is usually the day the structure goes away. The exercises that got you better sit in a folder, the appointments stop, and within a few months the strength you built starts quietly going the way it came.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<p>We see it every season. Someone finishes a course of therapy in March feeling great, heads north for the summer or just gets busy with the grandkids, and comes back in the fall with the same shoulder or the same knee asking what happened. Nothing dramatic happened. The work stopped, that's all. This post is about what a gym program after physical therapy should look like, so that the progress you paid for in time and effort sticks around.</p>
<h2>&ldquo;I do everything I can to let people not ever come to see me&rdquo;</h2>
<p>Dr. Dave Kashuba, Ph.D., founder of First Rehabilitation, says the line comes up often enough with patients that he has stopped apologizing for it. In his view, building a strong home program is the job, and he doesn't see it as bad for business. &ldquo;Cause again, reiterating the point, I do everything I can to let people not ever come to see me,&rdquo; he says.</p>
<p>That shows up in what he sends patients home with. Resistance bands over dumbbells, for a start: &ldquo;I recommend you go online and get bands, there's therapy bands that you could do,&rdquo; rather than relying on whatever weight happens to be sitting around the house. A band fits in a carry-on and hangs off a doorknob. It also comes in grades, so the program can get harder without anyone buying new equipment.</p>
<p>He said that on Episode 8 of Pain 2 Power, our Saturday morning show on 100.3 Legends Radio, and he has been saying versions of it to patients since 1991.</p>
<h2>How often you come in, and what the other hours are for</h2>
<p>A course of therapy is a few hours a week with a therapist. The rest of the week belongs to you, and that's where most of the change happens. Dave was blunt about it on Episode 13. &ldquo;I tell people I'll see them two to three times a week,&rdquo; he said, &ldquo;and those other hours they've got to be doing their exercises and they got to do them correctly, precisely.&rdquo; Then, in the same breath: &ldquo;Don't overdo.&rdquo;</p>
<h3>The band program that went north with Captain Kerry</h3>
<p>His guest that day was Captain Kerry Titheradge of Bravo's Below Deck, who first came to Dave about twenty years ago with a rotator cuff injury. Kerry's work took him away before the shoulder was finished, so Dave sent the program with him. &ldquo;You gave me what I needed to do when I was away, with bands and so forth, and I've got full motion,&rdquo; Kerry said on air. &ldquo;I've had two surgeries in there now and both times Dave and his team have got me back together.&rdquo;</p>
<p>That's what a home program is for: it travels. It works in a hotel room in the Northeast, on a boat, or at a summer place in North Carolina, as long as you actually do it.</p>
<h3>Correctly, precisely, and not fifty when ten will do</h3>
<p>The &ldquo;don't overdo&rdquo; part matters as much as the doing. Dave described the patient who decides that if ten repetitions are good, fifty must be better, and he noted that some exercises he sets for every other day rather than daily. Consistency was his word for what works. More is not automatically better, and a sore joint that keeps you off the program for a week costs more than it gained.</p>
<p>Orthopedic shoulder surgeon Dr. Ryan Simovitch made a similar point from the operating side on Episode 8. The shoulders he sees most often belong to what he called the constant warrior: someone playing pickleball four to six days a week with no moderation and no preparation, until something gives. A good post-therapy program is the preparation half of that sentence.</p>
<h2>Offset what the rest of your day already does to you</h2>
<p>Most people's daily movement runs one direction. Typing, driving, carrying groceries, looking at a phone, all of it pulls the shoulders forward and rounds the upper back. Dave's home programs are built to work the opposite way on purpose. &ldquo;It's better to offset everything that we do, our daily use, everything we do is internal again,&rdquo; he says, which is why shoulder rows, extensions, and shoulder pulls show up in nearly every program he writes, regardless of which joint sent the patient in.</p>
<p>The band work belongs after the evaluation and the hands-on treatment, once an injury has settled. Its job is to carry the gains forward.</p>
<h2>Stretching earns its place next to the band work</h2>
<p>Dave pairs the resistance work with a short stretching routine, and he is specific about why. &ldquo;Especially guys,&rdquo; he says, most people never stretch at all, they grab their glasses, a cup of coffee, and go to work. One move he gives patients is the wall slide: stand facing a wall, slide both arms up from a 90 degree bent position, and bring them back down, three sets of ten. He adds shoulder shrugs, three sets of ten, and scapular retractions, where you squeeze your shoulder blades together and hold. &ldquo;Just simple stretches like that are going to help and support it,&rdquo; he says.</p>
<p>None of these need equipment beyond a wall and, for the wall slide, a towel. That is deliberate. A home program someone will actually do on a Tuesday night beats a more elaborate one that stays in a folder. The full set, with the reasoning behind each move, is on our <a href="../exercises.html#shoulder">home exercises page</a>.</p>
<h2>What to do after you finish physical therapy so you don't lose progress</h2>
<p>Think of it as three stages rather than an on and off switch. Therapy is the first. A written <a href="../glossary.html#home-exercise-program">home exercise program</a> is the second, and every patient leaves with one. Supervised training is the third, for anyone who wants more structure than a folder and a doorknob can give.</p>
<div class="data-table" tabindex="0" role="region" aria-label="How care changes from therapy to home program to the wellness gym">
<table>
<caption>The three stages after an injury, as described on our insurance page and wellness FAQ, with visit frequency from Dave Kashuba on Pain 2 Power Episode 13.</caption>
<thead><tr><th scope="col">Stage</th><th scope="col">Who guides it</th><th scope="col">How often</th><th scope="col">How it is paid for</th></tr></thead>
<tbody>
<tr><th scope="row">Physical, occupational or hand therapy</th><td>A licensed therapist, one-on-one</td><td>Set in your plan of care; Dave says he usually sees people two to three times a week</td><td>Medicare and most major insurance when medically necessary; the front desk verifies benefits first</td></tr>
<tr><th scope="row">Home exercise program</th><td>You, from a written program your therapist teaches you</td><td>Between visits and after discharge, as your therapist writes it</td><td>A band, a wall and a towel</td></tr>
<tr><th scope="row">Wellness gym</th><td>The First Rehabilitation team, in personal training or a small group class</td><td>Arranged with the front desk</td><td>A separate program that does not take insurance; the front desk explains the cost before you sign up</td></tr>
</tbody>
</table>
</div>
<h3>Why supervision still matters once the visits stop</h3>
<p>On Episode 18, Dave was talking about women rebuilding range of motion and strength after breast cancer surgery, and he warned against jumping straight into a hard class. &ldquo;Not to get into an exercise class and doing these high level exercise,&rdquo; he said. &ldquo;It's more important for people to have someone supervised.&rdquo; The same reasoning is why our gym is supervised. People who know how bodies recover, and what yours has been through, keep an eye on your form, progression and safety.</p>
<h3>Pilates, the gym, or both</h3>
<p>Plenty of our patients add Pilates or yoga, and Dave is a fan of both. His guest on that same episode, Danielle Armstrong, owns Pilates Life on Northlake in Palm Beach Gardens. She first came to Dave as a patient herself, after her chiropractor sent her over: &ldquo;he got me out of my frozen shoulder,&rdquo; she said. She described what she does as gentle work &ldquo;aligned with physical therapy, just being able to move your body in a healthy way.&rdquo; If a class like hers keeps you moving, good. The point is to keep going after discharge in some form you enjoy enough to repeat.</p>
<h2>A post rehab exercise program for Palm Beach Gardens, Tequesta and North Palm Beach</h2>
<p>This is the gap our <a href="../services/wellness.html">on-site wellness program</a> is built to close. Graduates of our physical, occupational, and hand therapy programs can keep training in the same clinic on US-1, with a team that already knows which shoulder was the problem and which movements to avoid. A post rehab exercise program built this way picks up straight from your chart, with no generic intake form in between.</p>
<p>Dave described the clinic's approach on Episode 8 as &ldquo;no cookie cutters.&rdquo; &ldquo;Everyone gets evaluated, everyone gets treated, let's say treated differently,&rdquo; he said, because &ldquo;some people are building up their rotator, building up their knee, building up their ankle to go back running, playing sports.&rdquo; Others just want to get out of a chair and make a pot of coffee on their own. A gym program after therapy should respect that difference too.</p>
<p>We see the need most often with patients coming off <a href="../treatments/post-surgical.html">post-surgical rehabilitation</a>, where the risk of losing hard-won range of motion in the months after discharge is highest, and with <a href="../treatments/knee-pain.html">knee pain</a> patients who need ongoing strength work to keep a joint moving well. Patients from Palm Beach Gardens and <a href="../locations/tequesta.html">Tequesta</a> traveling in for therapy often ask about this before they have even finished their first course of treatment, which says something about how much the fear of backsliding weighs on people.</p>
<h2>What this replaces, and what it does not</h2>
<p>A gym program can't stand in for an evaluation, and it doesn't replace hands-on treatment while an injury is still active. If something new starts hurting, swells, or stops you sleeping, that's a reason to come back in and be assessed rather than train through it.</p>
<p>Medicare draws a similar line. Our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> explains that therapy is covered while you need a therapist's skills, including skilled care that keeps you from losing ground. Once a home program you can do safely on your own will keep your progress, skilled therapy is no longer the right tool, and we will say so plainly. The gym is what many people choose next. Pricing, scheduling and how to join are a front desk conversation, and we are not going to guess at them here.</p>
<h2>Start with an evaluation</h2>
<p>If therapy ended for you somewhere else, or your home program has quietly stopped happening, an evaluation is still the right first step. In most cases Florida lets you start a physical therapy evaluation without a referral, the first visit runs about an hour, and free consultations are available if you just want to talk it through. Call <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>, and see more answers in our <a href="../faq.html#wellness-gym">wellness and gym FAQ</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep15-mann": {
        "title": "They Were Gifted and Failing: Susan Mann on Processing Disorders",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "September 2026",
        "iso": "2026-09-19",
        "tag": "Pain 2 Power",
        "teaser": "Susan Mann of Bright Minds Processing joins Dave and Mike on the auditory and visual processing disorders she says affect one in four kids, and the 16 week fix.",
        "body": """
<p>Every teacher told Susan Mann her two children were gifted. Both were also testing near the bottom of the scale and could not get through a page of schoolwork. &ldquo;They can&rsquo;t be gifted if they can&rsquo;t do their schoolwork,&rdquo; she said. So she had them tested.</p>
<p>What she found ended with both kids on full academic scholarships and with a nonprofit she now runs out of Palm Beach County. She joined Dave and Mike on this week&rsquo;s Pain 2 Power to explain it.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Gifted on paper, failing in class</h2>
<p>Dave met Susan Mann the way he meets most people, by accident. She and her husband Michael are friends of his (she calls herself Irish Suzy, and once she starts talking you can hear why), and when Dave mentioned his own nonprofit work she started telling him about hers. &ldquo;I really have to get you on the show,&rdquo; he told her.</p>
<p>Her story starts with two bright kids who hated school. They were smart, the teachers agreed they were gifted, and their grades said otherwise. When she had them tested, both came back low. Really low, in her words. Nobody could explain the gap between what the children obviously were and what they could put on paper.</p>
<p>She kept digging, and the answer cost her plenty. &ldquo;I put everything on the line,&rdquo; she said, and she got both children to two fantastic doctors and then some. When they were retested afterward for the gifted program, they were off the charts. They got into the gifted school here in Palm Beach Gardens and went on to full academic scholarships at Oxbridge Academy.</p>
<h3>A retired cop from San Francisco</h3>
<p>Susan Mann is not a doctor, a mistake Mike made off air. After their pre-show conversation he assumed she was Dr. Susan Mann and kept calling her that. She&rsquo;s a retired police officer from San Francisco who did her own research because her kids needed it, and the doctors in this story are the specialists she found along the way.</p>
<p>That background shows up in where she wants to take the work. When Dr. Leah Light, the audiologist who treated her children, suggested taking the program into the prison system, Susan Mann&rsquo;s answer was, &ldquo;I thought that ship had sailed.&rdquo; She wants to reach third graders, middle schoolers and high schoolers, and catch them before the label sticks.</p>
<h2>Two disorders your evaluation form has no box for</h2>
<p>The turn came from her husband. He heard a radio segment describing someone who cannot follow instructions at work, who loses the second or third word of a sentence and then stands there with no idea what to do. He came home and said he thought he had auditory processing disorder. She listened and thought about her kids.</p>
<p>It runs in families, and it travels with a second condition she had never heard of. Visual processing disorder is the one where a child reads a sentence and skips it, twists the letters, or reaches the bottom of a page with no idea what they just read. Both of hers had both, badly. An audiologist in Hollywood, Dr. Leah Light, put it plainly: your kids cannot hear the teacher talk.</p>
<p>That reframed years of trouble. At swimming her children were constantly corrected for not doing what they were told. &ldquo;But they didn&rsquo;t know what they were told,&rdquo; she said.</p>
<p>Her bigger frustration is administrative. A psychological educational evaluation in Palm Beach County offers two boxes, ADHD or dyslexia. &ldquo;They are not allowed to diagnose VPD or APD, and the school does not recognize it,&rdquo; she said. Families who want an answer pay for it themselves, and she said very few of the doctors involved take any kind of insurance.</p>
<h3>What APD sounds like from the inside</h3>
<p>She has a quick screen she runs in conversation with kids. First she asks whether they like reading. A child who says they hate it gets the second question, whether they like school, and the answer is nearly always no. Then the real one: what do you hear when the teacher talks? &ldquo;Nothing. I just stare at a blank space on the wall,&rdquo; is what they tell her. Somebody in the studio reached for the Peanuts teacher, the wah wah wah, and she agreed that&rsquo;s about the sound.</p>
<p>At home it looked like this. Her daughter couldn&rsquo;t hear the words in a song. &ldquo;My son couldn&rsquo;t hear a movie,&rdquo; she said, so he interrupted every film nonstop to ask what people had said.</p>
<h3>What VPD looks like on the page and on the pool deck</h3>
<p>The visual side showed up in sport as much as school. On their first visit Dr. Light threw a ball at her kids, and it hit them in the chest before their hands closed on it. Now they catch it. At swim practice the coach held up a hula hoop and told everyone to dive through it. &ldquo;My son dived underneath the hula hoop. He was the only one,&rdquo; she said. These days, she added, he has a fantastic basketball shot.</p>
<h2>The eyes and ears are only the messengers</h2>
<p>Mike reached for face blindness as a comparison, the processing fault where someone looks straight at a face and cannot recognize it. The lesson Dr. Light gave Susan Mann was that even though we call these vision and hearing problems, the organ involved is the brain. The eyes and ears are only messengers.</p>
<p>Her description of the fix is that the wiring is off, and the therapy trains the eyes to work together at the same time, then does the same for the ears. Both sit in the same region, so work on one carries into the other. She doesn&rsquo;t dress it up, either. A neurologist once asked her what this brain training was like. &ldquo;I said, &lsquo;Yeah, it&rsquo;s like therapy,&rsquo;&rdquo; she told Mike.</p>
<p>Dave opened the show by making a related point about dyslexia, a word most people know without knowing what it means. He described it as a neurodevelopmental processing problem tied to specific areas of the brain. The testing Susan Mann uses comes out of Australia, where, Dave noted, every child in the school system is screened.</p>
<h2>Sixteen weeks, with homework five evenings a week</h2>
<p>The program runs sixteen weeks. You go in once a week, you leave with exercises to practice five evenings, and you come back for the next set until you graduate. For her own two it worked, and the daughter who couldn&rsquo;t hear the words in a song turned into a reader. &ldquo;My daughter has never put down a book since,&rdquo; she said.</p>
<div class="data-table" tabindex="0" role="region" aria-label="The Bright Minds Processing program as discussed on the episode">
<table>
<caption>The program as Susan Mann and Dave described it on Pain 2 Power Episode 15. These are Bright Minds Processing&rsquo;s details, not First Rehabilitation&rsquo;s; check brightmindsprocessing.org for current information.</caption>
<thead><tr><th scope="col">Piece of the program</th><th scope="col">What was said on air</th></tr></thead>
<tbody>
<tr><th scope="row">Screening</th><td>A $30 test, run through apps built by two Australian doctors. The public can&rsquo;t buy the apps; testers need an account with the company.</td></tr>
<tr><th scope="row">Before therapy starts</th><td>A vision check to make sure the child doesn&rsquo;t simply need glasses</td></tr>
<tr><th scope="row">Order</th><td>Vision first, then hearing</td></tr>
<tr><th scope="row">Length and rhythm</th><td>Sixteen weeks, one visit a week, exercises five evenings a week at home</td></tr>
<tr><th scope="row">Who is involved</th><td>An optometrist and an audiologist in Jupiter, a speech pathologist, an occupational therapist, and the therapists themselves, each in their own office for now</td></tr>
<tr><th scope="row">Cost</th><td>Roughly $2,400 from start to finish</td></tr>
</tbody>
</table>
</div>
<h3>What the exercises look like</h3>
<p>Mike asked what the therapy actually involves, in broad strokes. One exercise is a golf tee turned upside down and a small stick with a ball on the end. Most of us can tap the ball onto the tee without knocking it over. A child with a convergence problem cannot judge the distance, knocks the tee over, and starts again. Picture searches are another: the child cannot find the hidden pictures that the rest of us spot, and the therapy trains them to.</p>
<p>It also came up that this is the same vision therapy plenty of famous athletes pay for to sharpen their game. They just come at it for different reasons, with deeper pockets.</p>
<h3>Why the homework is the hard part</h3>
<p>Five evenings a week is where families fall down. If both parents are working, she said, nobody is home to run the exercises, and the parents who are home often don&rsquo;t know what to do with them. Her answer is an afterschool setup where the exercises simply get done.</p>
<p>The hosts floated doing it over Zoom with an online teacher. She was firm that it wouldn&rsquo;t work for these kids. &ldquo;You&rsquo;ve lost these kids so badly already,&rdquo; she said. &ldquo;They&rsquo;re already fried, done.&rdquo; What keeps them coming back is a person, a mentor and a friend, and prizes for doing the work. Mike agreed that one on one beats another screen, which already comes with built in distraction.</p>
<h2>Why the next program is a basketball team</h2>
<p>Girls will sit down and do the therapy. Boys, in her experience, fight it. So the program she is building in Palm Beach Gardens is a travel basketball team with a condition attached: you play if you keep turning up for the therapy, and once you graduate you keep your place. If a family can&rsquo;t afford it, she said, they&rsquo;ll make sure the child stays on the team. Mike called it Coach Carter, and she agreed before he finished. He also called it a carrot and a stick, with the carrot doing most of the work.</p>
<p>The coach is Dwayne McClain, a Villanova legend who, as Susan Mann put it, retired from the NBA and spent years as the Michael Jordan of Australia, including time with the Sydney Kings. That pulled Dave sideways, because Dave trained the Australian swim team in Perth, where McClain trained too. Australia is where the testing comes from as well, and Australian schools screen every child.</p>
<h2>The number Mike went and looked up</h2>
<p>Susan Mann puts the rate at one in four children, at any age. Mike brought his own research: a child who does not graduate or earn a GED is 380% more likely to end up in the juvenile justice system. Those figures belong to the guest and to Mike, not to us. What was familiar to everyone in the studio was the shape of it. A child who cannot follow the instruction gets labeled a bad listener, believes it, and stops trying.</p>
<p>Mike said it better on air. When you&rsquo;re young and labeled as someone who can&rsquo;t pick it up, &ldquo;it&rsquo;s very easy to internalize that.&rdquo; Susan Mann added the part a lot of parents of struggling kids will recognize. You get pulled out of class and put in a special class, &ldquo;and now everyone looks at you differently.&rdquo;</p>
<p>Her ambition is a template: test kids in Palm Beach County first, show the results, and push for the Australian approach in American schools. Dave&rsquo;s suggestion was that she become a teacher of the teachers, training schools, nonprofits and centers to run the screening so it doesn&rsquo;t all depend on one person. She said that&rsquo;s already possible, as long as whoever runs the test knows what they&rsquo;re doing, gets the report to the parents, and gets the referral to the right doctors.</p>
<h2>Where this brushes up against our work</h2>
<p>One thread runs straight into our building, and it arrived through her husband. After his traumatic brain injury, Susan Mann found in her research that the same processing therapy is used with brain injury and stroke patients.</p>
<p>Bright Minds Processing is her nonprofit at brightmindsprocessing.org, and we do not test for or treat auditory and visual processing disorders. We don&rsquo;t offer pediatric occupational therapy either, so for a child, the first call is the child&rsquo;s own doctor. We treat the adult side of that sentence. <a href="../services/occupational-therapy.html">Occupational therapy</a> after a stroke or brain injury covers upper extremity function, attention and memory strategies, and the daily business of dressing, cooking and getting back to work, which we wrote up separately in <a href="post-stroke-occupational-therapy-north-palm-beach.html">what post stroke occupational therapy actually involves</a>. If you&rsquo;re not sure whether a relative needs OT or PT, <a href="physical-therapy-vs-occupational-therapy.html">our plain comparison of the two</a> is a good place to start.</p>
<p>Mike caught the other parallel on air. Whatever the therapy, you have to do the work. &ldquo;It is exactly true,&rdquo; Susan Mann said.</p>
<p>The show ended the way they usually do, with Dave telling Mike about a breakthrough with his wife. He told her to embrace her mistakes. &ldquo;She ran over and hugged me for no reason,&rdquo; he said, and it took the studio a second to catch up.</p>
<p>Listen to the full conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch past episodes in our <a href="../videos.html">video library</a>, and see what people ask us most in the <a href="../faq.html#occupational-therapy">occupational therapy FAQ</a>. If someone in your family is recovering from a stroke, a brain injury, or surgery and daily tasks have become the hard part, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "post-stroke-occupational-therapy-north-palm-beach": {
        "title": "Post Stroke Occupational Therapy in North Palm Beach: What Recovery Involves",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "September 2026",
        "iso": "2026-09-19",
        "tag": "Occupational Therapy",
        "teaser": "What occupational therapy after a stroke or brain injury actually covers, from dressing and cooking to cognitive rehab and getting back to work in Palm Beach County.",
        "body": """
<p>Post stroke occupational therapy in North Palm Beach is the part of recovery that deals with your actual day. The morning you try to button a shirt with one hand that will not cooperate. The afternoon you stand at a stove and lose track of what you were doing. A stroke or a brain injury damages the wiring that carries messages around, and the arm, the hand and the attention span all pay for it downstream.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<p>This article came out of an unexpected conversation. On Episode 15 of our podcast, Susan Mann of Bright Minds Processing talked about children with auditory and visual processing disorders, which we do not treat, and mentioned in passing that after her husband&rsquo;s traumatic brain injury she found the same kind of processing work being used with brain injury and stroke patients. The full story of her kids is in <a href="pain-2-power-ep15-mann.html">our recap of that episode</a>. This page is about the adult side, and about what happens when someone you love comes home from the hospital and the hard part turns out to be Tuesday morning.</p>
<h2>The eyes and the ears are only messengers</h2>
<p>The audiologist who treated Susan Mann&rsquo;s children, Dr. Leah Light, taught her that even though we call those vision and hearing problems, the organ involved is the brain. &ldquo;They&rsquo;re only the messengers,&rdquo; Susan Mann said of the eyes and ears.</p>
<p>It&rsquo;s a useful way to think about the arm after a stroke. A stroke is an injury to the brain, so the hand that won&rsquo;t open or the arm that drifts is taking its orders from a part of the system that has been hurt. That&rsquo;s why our stroke work is task specific. Instead of exercising an arm in the abstract, the therapist rebuilds the routines that arm is needed for, and measures progress in tasks you can do again.</p>
<p>Dr. Dave Kashuba, Ph.D., OTR, our founder, is an occupational therapist himself and has been treating patients since 1991. His starting point for any plan is the same. &ldquo;What we do is we try to take each person individually and figure out a game plan for them,&rdquo; he said on Episode 10. Two people with the same diagnosis on paper can need very different first weeks.</p>
<h2>Occupational therapy after a stroke: what to expect</h2>
<p>Most families come to us with the same few questions. How long is the first visit, will anything actually happen at it, and who are we going to see?</p>
<h3>The first visit</h3>
<p>Plan on about an hour, one on one with your therapist. They&rsquo;ll listen to the story, which matters more after a stroke than almost anywhere else, watch how you move and how you handle a task, measure what can be measured, and set goals with you that are specific enough to show progress. Treatment usually begins that same day, and you leave with a plan, the start of a home program and your next appointments already on the calendar.</p>
<p>We email an intake form once the visit is booked, so the hour starts with therapy. Bring three things:</p>
<ul>
<li>A photo ID</li>
<li>Your insurance card, plus any Medigap or secondary card you carry</li>
<li>Your prescription or referral, if your physician gave you one</li>
</ul>
<p>Wear something loose that lets the therapist get to the arm and shoulder easily. There&rsquo;s a free lot right at the building at 733 US Highway 1, Suite 2A, which matters when someone is still unsteady getting in and out of the car.</p>
<h3>Who you&rsquo;ll work with</h3>
<p>Our occupational therapy is led by Dave alongside Joan &ldquo;Joni&rdquo; Janik, OTD, whose focus includes activities of daily living and stroke recovery. Laura Drumm, MS, OTR/L, CHT, CLT, our <a href="../services/hand-therapy.html">certified hand therapist</a>, joins in when the hand is the sticking point, and our physical therapists, Kayla Dorsey, PT, DPT and Logan Van Sant, PT, DPT, handle walking and balance when those need work too.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Which discipline handles which part of stroke recovery at our clinic">
<table>
<caption>How the three disciplines split stroke recovery at our clinic, as described on our insurance page under our Medicare CORF certification.</caption>
<thead><tr><th scope="col">Discipline</th><th scope="col">What it usually takes on after a stroke</th></tr></thead>
<tbody>
<tr><th scope="row">Physical therapy</th><td>Walking and balance</td></tr>
<tr><th scope="row">Occupational therapy</th><td>Dressing, cooking and the rest of the daily routine</td></tr>
<tr><th scope="row">Certified hand therapy</th><td>A weak, closed hand</td></tr>
</tbody>
</table>
</div>
<p>All three happen in the same building, under one plan, with the same notes. Dave made the point on air that it&rsquo;s worth choosing a place with &ldquo;a good physical therapy team, good occupational therapy team,&rdquo; and the reason is practical. Nobody has to carry information between separate clinics. We walk down the hall and talk.</p>
<h2>What post stroke occupational therapy actually covers</h2>
<p>Our occupational therapy program breaks into six areas, and a stroke usually pulls in several at once. The examples in the right hand column are the kind of task we actually work on.</p>
<div class="data-table" tabindex="0" role="region" aria-label="The six areas of our occupational therapy program">
<table>
<caption>The six areas of our occupational therapy program, from our occupational therapy service page, with examples drawn from our patient glossary and FAQ.</caption>
<thead><tr><th scope="col">Area</th><th scope="col">What it covers</th><th scope="col">An example of the work</th></tr></thead>
<tbody>
<tr><th scope="row">Activities of daily living</th><td>Dressing, bathing, grooming, cooking and home management</td><td>Buttoning a shirt with one hand that isn&rsquo;t cooperating</td></tr>
<tr><th scope="row">Post stroke recovery</th><td>Task specific work on upper extremity function, coordination and daily routines</td><td>Rebuilding the sequence that gets you out of the house in the morning</td></tr>
<tr><th scope="row">Cognitive rehabilitation</th><td>Memory, attention and problem solving strategies</td><td>Managing a medication schedule or following a recipe again</td></tr>
<tr><th scope="row">Hand and upper extremity function</th><td>Fine motor and functional use training, coordinated with certified hand therapy</td><td>A custom splint made in the clinic when the hand needs a position held</td></tr>
<tr><th scope="row">Ergonomics and adaptive equipment</th><td>Workstation assessment and equipment recommendations</td><td>Dressing aids and built up grips, with training in how to use them</td></tr>
<tr><th scope="row">Return to work programs</th><td>Graded conditioning and task simulation</td><td>Rehearsing the job&rsquo;s own tasks at its weights, heights and pace</td></tr>
</tbody>
</table>
</div>
<p>An evaluation sorts out which of those matter for you, and in what order. Somebody who cooks every night and somebody who needs to get back behind a desk get different plans out of the same diagnosis. Or, as Dave put it about a very different problem, &ldquo;you can&rsquo;t cookie cut what programs you&rsquo;re going to do.&rdquo;</p>
<h2>Cognitive rehabilitation after injury, and what it covers</h2>
<p>This is the piece families are least prepared for. The arm is visible. Attention isn&rsquo;t, so a person can look recovered and still struggle to follow a three step instruction, keep track of a conversation, or hold on to a task through an interruption. They&rsquo;re often embarrassed about it, too, and good at covering.</p>
<p>Cognitive rehabilitation works on memory, attention and problem solving. The target is the medication schedule, the grocery list, the recipe, the household routine. The therapist works on the real task you&rsquo;re struggling with, in the order you actually do it at home, and adapts the method until you can manage it without help.</p>
<p>If you&rsquo;re the family member doing the driving, the most useful question you can bring is simple. Which steps can my relative now do alone, and which ones should I still be helping with? Ask it every couple of weeks. The answer changes.</p>
<h2>Getting the hand and arm back to work</h2>
<p>Upper extremity recovery is where our occupational therapy and our certified hand therapy program overlap. Laura Drumm, CHT, leads the hand side, and the two run together when a stroke has left the hand weak, clumsy or partly closed: fine motor work, functional use training, and splinting when the hand needs a position held. Splints are fabricated here in the clinic and molded to the person, which saves a trip and a wait.</p>
<p>That coordination also matters when the stroke isn&rsquo;t the only thing in the chart. Plenty of people arrive with an old shoulder problem or a recent wrist injury alongside the neurological one, and the plan has to account for both. Our <a href="../treatments/hand-wrist.html">hand and wrist</a>, <a href="../treatments/shoulder-pain.html">shoulder pain</a> and <a href="../treatments/post-surgical.html">post surgical</a> pages cover how that side of the work runs.</p>
<h3>Adaptive equipment, taught rather than handed over</h3>
<p>Sometimes the fastest route back to a task is changing the tool. Dressing aids, built up grips and simple changes to how the kitchen is set up can make a task safe again while strength and coordination are still coming back. We only recommend what helps, and the therapist trains you on it in the session. Then you practice it. A gadget nobody has shown you how to use ends up in a drawer.</p>
<h2>A return to work program after injury, for people driving in from Palm Beach Gardens</h2>
<p>A return to work program is graded. It uses task simulation and conditioning that build toward the real demands of the job, rather than a blanket clearance handed out at a fixed number of weeks. For desk work that usually means a workstation assessment and adaptive equipment: screen height, chair, keyboard and mouse. For anything physical it means loading the actual movements at the weights and heights the job uses, and reporting progress in those same terms, which is what an employer or a case manager needs to see. If the injury happened on the job, our <a href="../treatments/workers-comp.html">work injury rehab</a> page explains how authorization works in Florida.</p>
<p>We see people from across the county for this. The clinic sits on US-1 in North Palm Beach, a short drive from <a href="../locations/palm-beach-gardens.html">Palm Beach Gardens</a>, Juno Beach and Jupiter, and an easy run up from <a href="../locations/west-palm-beach.html">West Palm Beach</a>. Hours are Monday through Friday 8:00 AM to 5:30 PM, with Saturday mornings 8:00 AM to 12:30 PM, which is the slot working family members tend to want when they&rsquo;re the ones doing the driving.</p>
<h2>The homework is the treatment</h2>
<p>Mike McGann, who co-hosts Pain 2 Power with Dave, made the point on air that every therapy has the same catch. You have to do the exercises. &ldquo;You&rsquo;re not gonna get a result if you don&rsquo;t,&rdquo; he said, and Susan Mann agreed without hesitation: &ldquo;It is exactly true.&rdquo;</p>
<p>Post stroke occupational therapy works the same way. The hour in the clinic sets the task and corrects it. The practice between visits is where the hour pays off. Every patient leaves with a written <a href="../glossary.html#home-exercise-program">home exercise program</a>, and that program is built around the real tasks in your house, which makes it easier for a spouse or an adult child to help without guessing.</p>
<p>When formal therapy ends, some people want to keep going with structure. Our on-site wellness gym lets former patients train with a team that already knows their history. It&rsquo;s a separate program from insurance-covered therapy and doesn&rsquo;t take insurance, so the front desk will explain how it works before anyone signs up.</p>
<h2>Starting, and what it costs</h2>
<p>We take Medicare and Medicare Advantage along with BCBS, Aetna, Humana, Tricare, the VA Community Care Network, workers&rsquo; compensation and self pay. Whether you need a referral for occupational therapy depends on your plan, so the front desk checks that, and your benefits, before you come in. Medicare requires a physician to certify your plan of care, and we handle that paperwork with your doctor.</p>
<p>One Medicare detail worries people needlessly. Occupational therapy has its own yearly checkpoint, $2,480 in 2026 according to CMS, after which the clinic adds a code confirming the care is medically necessary. It is not a cap. Medicare also doesn&rsquo;t require you to keep improving; skilled therapy that maintains function, which matters a great deal after a stroke, can qualify. Our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> walks through all of it with sources, and the <a href="../faq.html#occupational-therapy">occupational therapy FAQ</a> answers the rest.</p>
<p>You can read more about the program on our <a href="../services/occupational-therapy.html">occupational therapy page</a>, compare the two disciplines in <a href="physical-therapy-vs-occupational-therapy.html">physical therapy vs. occupational therapy</a>, and hear the conversation that prompted this article on <a href="../podcast.html">the Pain 2 Power podcast page</a>. If someone in your family has had a stroke or a brain injury and the hard part has become the daily routine rather than the diagnosis, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep11-joyce": {
        "title": "The Muscle Comes Off Too: Paul Joyce on GLP-1s and Peptides",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "August 2026",
        "iso": "2026-08-22",
        "tag": "Pain 2 Power",
        "teaser": "Paul Joyce of New Life HRT joins Dave and Mike on peptides, GLP-1s and hormone therapy, why the weight takes muscle with it, and what six lab tests found.",
        "body": """
<p>Paul Joyce has a completely torn rotator cuff and no plans to have it repaired. He plays golf most days, and the swing itself does not bother him. What used to be excruciating was turning the steering wheel on the drive over.</p>
<p>He had a shoulder replacement on the schedule and cancelled it. Now he comes to Dave instead. That is how this week&rsquo;s Pain 2 Power opened, before turning into an hour on peptides, GLP-1s and hormone replacement therapy with the man a lot of doctors learn this material from.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<p>Paul runs New Life HRT and has been a friend of Dave&rsquo;s for 22 years. If you have a neighbor at the club on a weight loss shot, or you have wondered about one yourself, this is the episode to hear. Below is the part of it that matters to a rehab clinic, plus where we stand on the rest.</p>
<h2>What a peptide actually is</h2>
<p>Mike started where these conversations should start and almost never do. What is a peptide? Paul Joyce, who runs New Life HRT, gave the short version. &ldquo;A peptide is a chain of amino acids. A short chain of amino acids, usually under 50, that are bound together,&rdquo; he said. They carry messages about repairing injury, losing weight, and mood, and he counts around 150 of them.</p>
<h3>From the gut to the Gila monster</h3>
<p>Dave filled in where the weight loss drugs came from. GLP-1 stands for glucagon like peptide, which your gut already makes, though your own clears too fast to do much. The version in the medications was modeled on a compound found in the Gila monster, which stays in the body long enough to keep working. And no, Paul confirmed, you are not injecting lizard venom. He gets asked constantly.</p>
<p>Paul has been at this longer than most. He began prescribing Ozempic off label for weight loss back in 2017, well before the rest of the country caught on, and he now trains physicians on peptide and hormone replacement protocols before they offer them in their own practices.</p>
<h2>The weight comes off with muscle attached</h2>
<p>Dave sees people well into a course of a GLP-1 who have lost the weight and started to look frail, because nothing else about how they eat or train has changed. &ldquo;It&rsquo;s going to make you better, but it&rsquo;s not gonna make you healthier if you don&rsquo;t do something more with it,&rdquo; he said.</p>
<p>Paul agreed flatly. &ldquo;You definitely have to make sure you&rsquo;re getting enough protein,&rdquo; he said, and when Dave asked whether the loss includes muscle, the answer was &ldquo;Yeah, you lose a lot of muscle.&rdquo; He was describing himself as much as his patients. He started at 209 pounds, weighs 153 now, and says he took it too far. He stopped about a month before the show and his appetite is still catching up.</p>
<h3>Why the muscle matters more after 60</h3>
<p>Lean mass matters more the older you are. Strength is what gets you off a low couch and back onto your feet after a stumble. Lose enough and a trip that used to be nothing becomes a fall. Two thirds of the people we treat are 65 or older. For them, keeping muscle is about staying independent, and looks barely come into it.</p>
<p>Holding onto muscle while the scale moves is ordinary work: resistance training and protein. The first half of that is what our <a href="../services/wellness.html">wellness gym</a> and <a href="../services/physical-therapy.html">physical therapy</a> teams do all day. Something as plain as standing up from a chair without your hands, a few times a day, is a decent start, and Dave&rsquo;s version of it is on our <a href="../exercises.html#everyday">home exercises page</a>. Our earlier post on <a href="../blog/strength-training-after-60-fall-prevention.html">strength training after 60</a> covers where to begin.</p>
<h3>Food first, says the dietitian</h3>
<p>Protein is the half we leave to the people who do it for a living. On Episode 18, registered dietitian Elyse Marrone, RD/LDN, CGP, who sees patients in Jupiter, laid out the seven pillars she works through with every patient: food first, exercise, sleep, stress management, supplementation, hydration and community. She did not talk about GLP-1s on that show. Her general point still lands here, because bloodwork follows habits: &ldquo;the labs are going to change based on those seven pillars of health,&rdquo; she said. A shot can move the scale. The food and the training decide what the weight loss is made of.</p>
<h2>Six websites, six sets of problems</h2>
<p>Then the talk turned to where people buy this stuff. Search for a peptide online and you will find it sold cheap, labeled not for human consumption, for research purposes only. Paul had six of those sites tested.</p>
<p>All six came back with flaws he called major. Heavy metals in some. One carried a low level of bacteria. One was sold as retatrutide and turned out to be underdosed semaglutide, a different drug altogether. He has since served as an expert witness in an Atlanta case against a company using a fabricated certificate of analysis, the document these sellers hold up to look legitimate and, he says, often just invent.</p>
<p>The regulated end of the supply chain looks different. Everything he uses comes from a 503A or 503B compounding pharmacy, FDA inspected and DEA licensed. Of every thousand vials produced, a hundred go to an independent lab for sterility and potency testing.</p>
<h3>Do people just skip the doctor?</h3>
<p>The hosts asked Paul straight out whether people simply go on these things without seeking professional help. His answer was short. &ldquo;Well, a lot of people go on it,&rdquo; he said, and the place they get it is those same research only websites. Put that next to the six test results and you can see why he spent so much of the hour on sourcing.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Figures Paul Joyce gave on Pain 2 Power Episode 11">
<table>
<caption>Figures Paul Joyce gave on Pain 2 Power Episode 11, as he stated them on air. First Rehabilitation has not verified them.</caption>
<thead><tr><th scope="col">Topic</th><th scope="col">What Paul said</th></tr></thead>
<tbody>
<tr><th scope="row">Size of a peptide</th><td>A short chain of amino acids, usually under 50</td></tr>
<tr><th scope="row">How many peptides</th><td>He counts around 150</td></tr>
<tr><th scope="row">Prescribing GLP-1s for weight loss</th><td>Off label since 2017</td></tr>
<tr><th scope="row">Research only websites he had tested</th><td>Six, and all six had major flaws</td></tr>
<tr><th scope="row">BPC-157 and his shoulder pain</th><td>Pain gone in about three weeks; strength did not come back with it</td></tr>
<tr><th scope="row">Golf after shoulder surgery</th><td>He expected eight months off, which is why he did not want the surgery</td></tr>
</tbody>
</table>
</div>
<h2>Is there any proof it works?</h2>
<p>To his credit, Paul did not oversell it. The question put to him on air was the skeptic&rsquo;s one: when someone is at their worst, in terrible pain with nothing working, and they start a peptide, how do you know they were not about to get better anyway? And have there been actual studies?</p>
<p>&ldquo;It&rsquo;s not FDA approved,&rdquo; Paul said. &ldquo;There&rsquo;s been studies done mostly on animals, however, there has been some human studies.&rdquo; What he leans on instead is experience: taking it himself, and what he says he has seen in a thousand patients who have used it. That is an honest description of where the evidence sits. It is also a good reason to keep a physician in the loop, and that is where we land too.</p>
<h2>Three weeks without pain, still no strength</h2>
<p>Back to that shoulder. Paul started BPC-157 while the surgery was still on the calendar, and within about three weeks, on his account, the pain was gone. The strength did not come with it. &ldquo;But I&rsquo;m still weak. I have no strength in my shoulder,&rdquo; he said. &ldquo;I can&rsquo;t even lift my arm up some ways. But there&rsquo;s no pain anymore.&rdquo;</p>
<h3>Golf every day, but not the steering wheel</h3>
<p>His reason for cancelling the replacement will make sense to half the golfers in Palm Beach County. &ldquo;I&rsquo;m an addicted golfer. I literally try to play golf every day, but the golf swing doesn&rsquo;t hurt my shoulder,&rdquo; he said. &ldquo;It&rsquo;s the craziest thing.&rdquo; Surgery, as he understood it, meant eight months without a club in his hands, and he was not willing to give that up while the swing still worked.</p>
<p>We meet that gap every week. A cuff that is fully torn does not knit itself back together because it stopped hurting, so pain leaving is the moment to start rehab rather than skip it. Paul took the first road. &ldquo;So I started going to Dave, and it&rsquo;s been a Godsend,&rdquo; he said. &ldquo;My shoulder is, like, a lot better.&rdquo; Earlier in that answer he said the pain had diminished greatly, adding, &ldquo;I have more range of motion.&rdquo;</p>
<h3>What rehab looks like when the tear stays torn</h3>
<p>Our <a href="../treatments/shoulder-pain.html">shoulder rehab</a> follows a familiar order: get back pain-free <a href="../glossary.html#range-of-motion">range of motion</a> first, then rebuild strength in the muscles around the cuff and the shoulder blade, then return to reaching, lifting, sport and sleep. With a tear that will not close, the muscles that still work have to carry more of the load, so that middle step gets most of the attention. Every session is one-on-one.</p>
<p>Whether a cuff is intact also shapes surgery if it ever comes back on the table. Orthopedic shoulder surgeon Dr. Ryan Simovitch explained on Episode 8 that the state of the rotator cuff decides which kind of shoulder replacement a person gets, and our post on <a href="../blog/reverse-shoulder-replacement-explained.html">total versus reverse shoulder replacement</a> walks through why.</p>
<h2>Where we stand on peptides and hormones</h2>
<p>BPC-157 is not FDA approved. Paul said so himself on air, and we do not prescribe, sell or advise on any of it. Peptides and hormone replacement belong in a conversation with a physician who runs your bloodwork. What comes after, the strength and the movement, is ours.</p>
<p>Elyse Marrone described her own line the same way on Episode 18. &ldquo;I don&rsquo;t prescribe hormones but I work with a lot of providers who do,&rdquo; she said. That division of labor is how it should work. The prescriber handles the prescription, the dietitian handles the plate, and a therapist handles the shoulder that still will not lift and the legs that got weaker while the scale went down. If you want our part of it, the front desk will verify your Medicare or commercial benefits before your first visit.</p>
<h2>Listen to the episode, or come see us</h2>
<p>Listen to the full conversation on <a href="../podcast.html">the Pain 2 Power podcast page</a>, watch past episodes in our <a href="../videos.html">video library</a>, and see what patients ask us most in the <a href="../faq.html#physical-therapy">physical therapy FAQ</a>. Pain 2 Power airs Saturdays at 8:30 AM on 100.3 Legends Radio. If you are dropping weight and want to keep the strength, or your shoulder hurts less than it did and still cannot do what you need, call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "partial-vs-total-knee-replacement": {
        "title": "Partial vs Total Knee Replacement: The Option Most People Never Hear About",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "August 2026",
        "iso": "2026-08-15",
        "tag": "Physical Therapy",
        "teaser": "Many people who get a total knee could have had a partial. What separates the two, why partials are offered less often, and what rehab looks like after each.",
        "body": """
<p>If a surgeon has told you it is time for a knee replacement, there is a second question to ask before you book anything, and it is about which operation you get.</p>
<p>Most people know total knee replacement exists. Far fewer know that a partial is a separate operation with a different risk profile, and that plenty of candidates never get told about it. This post walks through the difference the way a surgeon explained it to us on the radio, what decides who gets which, and what the rehab looks like on our side of the handoff.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>The numbers a surgeon gave us on air</h2>
<p>Orthopedic surgeon Dr. Richard Weiner, M.D., who has been in practice since before our clinic opened in 1991, laid this out on Episode 6 of the Pain 2 Power podcast. He trained in both engineering and medicine at the University of Pennsylvania and has thousands of hip and knee replacements behind him, so when he talks about how a knee is put together, we listen. Statistics show that over 40% of everyone receiving a total knee could have had a partial instead, he said, while in the United States only about 10% actually get one.</p>
<p>His explanation for the gap is not clinical. "Most of the surgeons who do total knees are not trained to do partials," he said, "so they don't even offer it as an option." Fewer than half of orthopedic surgeons do knee replacements at all. Of those, fewer than half do partials. Of those, fewer than half will do the lateral compartment.</p>
<p>All of which means the operation you are offered can depend on who you happen to be sitting across from. That's an uncomfortable thing to hear when you have already spent a year limping around the grocery store. It's also useful, because it tells you exactly what to ask.</p>
<h2>What makes partial and total knee replacement different operations</h2>
<p>The knee has separate compartments, including one on the inside and one on the outside. Arthritis does not always take all of them. A partial replaces only the worn one and leaves the rest of your knee alone. A total replaces the whole joint surface.</p>
<h3>What happens to the ligaments</h3>
<p>The structural difference Dr. Weiner emphasises is the ligaments. A total knee "requires dislocation of the joint," a much larger procedure, and the anterior cruciate ligament comes out. About half the time the posterior cruciate goes too. A partial preserves all of them, and that is the reason for the thing patients notice most: "a partial knee can feel like a normal knee, because all the ligaments are preserved." A total knee, in his words, never quite does. It is a tremendously successful operation and it still feels a little different.</p>
<p>He tied the feel of the knee directly to the ligaments, and the ligaments are what you will live with every time you step off a curb or turn for a ball on the pickleball court.</p>
<h3>Pain, risk, and getting back to the court</h3>
<p>His shorthand for the rest was a repeated phrase. Pain, less than half. Risk of infection, less than half. Time to get back to sport, less than half. Blood loss and clot risk, lower again, though the risks with a modern total knee are low to begin with.</p>
<p>Which compartment wears matters too. The inside of the knee goes about eight to ten times more often than the outside, which is the reason worn knees tend to look bow legged. The smaller group who wear the outside look knock kneed, and that lateral partial takes training that fewer surgeons have.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Partial versus total knee replacement as Dr. Richard Weiner described them">
<table>
<caption>Partial versus total knee replacement, as Dr. Richard Weiner, M.D. described them on Pain 2 Power, Episode 6. His comparison, not a promise about any one knee.</caption>
<thead><tr><th scope="col">Question</th><th scope="col">Partial knee</th><th scope="col">Total knee</th></tr></thead>
<tbody>
<tr><th scope="row">What gets replaced</th><td>Only the worn compartment</td><td>The whole joint surface</td></tr>
<tr><th scope="row">The joint during surgery</td><td>Not dislocated</td><td>"Requires dislocation of the joint"</td></tr>
<tr><th scope="row">Cruciate ligaments</td><td>All preserved</td><td>ACL removed; the PCL about half the time</td></tr>
<tr><th scope="row">How it feels afterward</td><td>"Can feel like a normal knee"</td><td>Very successful, but feels a little different</td></tr>
<tr><th scope="row">Pain, infection risk, return to sport</td><td>Less than half of a total, on each</td><td>The baseline he compared against</td></tr>
<tr><th scope="row">Who performs it</td><td>A smaller group of surgeons; fewer still do the outside compartment</td><td>Most surgeons who replace knees</td></tr>
<tr><th scope="row">Long term</td><td>Well under one in ten end up converted to a total</td><td>Not discussed as a conversion question</td></tr>
</tbody>
</table>
</div>
<h2>Who is a candidate for a partial knee replacement?</h2>
<p>Not everyone, and the decision is not made from a scan alone. "You don't treat an X-ray, you treat the patient," Dr. Weiner said, and his sequence starts with your symptoms and your history, then a clinical exam, then imaging, including stress X-rays that show whether the other compartments are holding up.</p>
<p>A partial only makes sense if the parts of the knee you keep are healthy enough to carry you for years. If the stress views show the other compartments starting to go, a partial just postpones the conversation.</p>
<p>The question he weighs is durability. A small share of partials, well under one in ten, eventually need converting to a total. Over 90% do not. When the odds of it lasting look good, that is what he recommends.</p>
<p>Age is less of a barrier than people assume. He described doing a partial knee for a 95 year old patient of twenty years, who had done therapy and injections for as long as they worked and then decided she wanted the knee. Ninety-five. If you're in your eighties and assume nobody is going to bring up options with you, keep that story in your back pocket.</p>
<h3>Questions to take to your surgeon</h3>
<p>A good appointment takes a short list and the nerve to ask it. Here's the one we would bring:</p>
<ul>
<li>Which compartment of my knee is worn, and are the others holding up?</li>
<li>Have I had stress X-rays, or would they change the picture?</li>
<li>Am I a candidate for a partial, and do you perform both operations?</li>
<li>If not, who would you send me to for a second look?</li>
<li>What is your therapy protocol afterward, and when do you want it to start?</li>
</ul>
<p>Dave's advice about choosing anyone who treats you applies here more than usual: do your homework, and do not take the recommendation from the person next to you in the Publix line.</p>
<h2>Surgery is still the last resort</h2>
<p>None of this is an argument for having a replacement. "Surgery is the last resort," Dr. Weiner said. "The first thing is conservative treatment."</p>
<p>That means avoiding what aggravates the joint, then therapy, then medication or a targeted injection, and only then bracing or an operation. On therapy he was direct about why it comes first: "physical therapy is key because you need to have strong muscles to stabilize the knee to have fewer symptoms." He also prefers injections to pills for a single joint, on the logic that you put the oil where it squeaks rather than exposing the whole body.</p>
<p>If you're still on the early rungs of that ladder, our post on <a href="knee-arthritis-before-surgery.html">knee arthritis treatment before surgery</a> covers the conservative side in detail, including the four exercises Dave gave listeners and the weight math Dr. Weiner shared. And if your scan shows one small damaged spot rather than worn compartments, read <a href="cartilage-transplant-knee-explained.html">how cartilage transplant knee recovery works</a>, because that is a different conversation again.</p>
<p>Dave added one aside during the Weiner interview. He told Dr. Weiner he loses money on partials, because those patients need far less rehab than a total knee does.</p>
<h2>What rehab looks like after a partial or total knee</h2>
<p>Both operations need therapy, and the partial needs less of it. The work is the same in kind: restoring range, then rebuilding the muscles that support the joint, quadriceps first and glutes and calves alongside them, because the knee is carried from above and below.</p>
<h3>Your surgeon's protocol sets the pace</h3>
<p>We don't invent a timeline. Every surgeon has a protocol, some start therapy within days and some protect the repair longer, and we follow it exactly. Bring your post-op paperwork to the first visit. The evaluation takes about an hour, one-on-one, and it measures where you are today: how far the knee bends and straightens, how you walk, how you handle a step. Treatment usually starts that same day.</p>
<p>From there, the program on our <a href="../treatments/knee-pain.html">knee pain page</a> describes the shape of it: manual therapy for joint mobility, progressive strengthening of the quadriceps, hips and glutes, and functional retraining for stairs, walking distance and getting back to whatever you came in wanting to do. For some people that's eighteen holes at a course up in Jupiter. For others it's the stairs to a second-floor condo, or getting down on the floor with a grandchild and back up again.</p>
<p>We'd be guessing if we gave you a number of visits here, and a guess is worse than no answer. A partial and a total follow different timelines, and two people with the same operation recover differently. Your therapist sets milestones at the evaluation and re-checks them as you go, so you are never coming in for visits you do not need.</p>
<h3>Should you do prehab first?</h3>
<p>Prehab means building strength before the operation. Two surgeons on our show came at it from slightly different angles.</p>
<p>Dr. Rami Elkhechen, M.D., the sports medicine surgeon from Episode 7, does it routinely and put the case simply: "The stronger your base is as you're coming in, in terms of strength and your activity level, you're probably going to come out the other side much better in terms of recovery."</p>
<p>Dr. Michael Leighton, MD, an orthopedic surgeon with Palm Beach Orthopedic Institute in Palm Beach Gardens who performs robotic-arm assisted knee replacement, was more selective when he joined us for Episode 12. Prehab, he said, "is basically tuning this patient up for surgery prior to surgery and it's not a one-size-fits-all situation." He saves it mostly for people who have been away from activity and are deconditioned.</p>
<p>Those two views fit together better than they first sound. If you have been sitting more because the knee hurts, a few weeks of targeted work before surgery is cheap insurance. If you are still walking the beach every morning, you may already be in the shape your surgeon wants. You can start with the <a href="../exercises.html#knee">knee exercises Dave walks through on the show</a> and bring the rest to an evaluation.</p>
<h2>Paying for rehab after a knee replacement</h2>
<p>Two thirds of the people we treat are 65 or older, so the Medicare questions usually come up on the first phone call. Our <a href="../insurance.html#medicare-guide">Medicare guide</a> has the full detail. The short version for outpatient therapy under Original Medicare in 2026, from CMS figures, is a yearly Part B deductible of $283, then 20% of the Medicare-approved amount per visit. There is no yearly cap on therapy when the care is medically necessary. Past $2,480 in physical therapy charges for the year, the clinic adds the <a href="../glossary.html#kx-modifier">KX modifier</a> to confirm the need is documented, and therapy carries on.</p>
<h3>Medicare Advantage and the paperwork</h3>
<p>Medicare Advantage plans cover the same benefit under their own rules, and they often want prior authorization before therapy starts. We request it for you. Either way, Medicare requires your doctor to certify the <a href="../glossary.html#plan-of-care">plan of care</a> your therapist writes after the evaluation, and we chase that signature so it does not become one more errand. Our front desk verifies Medicare and commercial benefits before your first visit, so you know where you stand before you walk in.</p>
<p>One more practical note: we're a Medicare-certified Comprehensive Outpatient Rehabilitation Facility, a CORF, which means coordinated rehab at one location with physician review of the plan. There's a free lot right at the building on US-1, so the hardest part of the trip is usually getting in and out of the car, which, as it happens, is something we practice.</p>
<h2>Bring us in early</h2>
<p>If you are weighing a knee replacement, or recovering from one, we can help with the part that decides how well it goes. Ask your surgeon whether you are a candidate for a partial and whether they perform both. Then call us, before or after, whichever comes first.</p>
<p>We see patients from North Palm Beach and across the county, including <a href="../locations/palm-beach-gardens.html">Palm Beach Gardens</a>. Call <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>. Read more about <a href="../treatments/post-surgical.html">post-surgical rehabilitation</a>, browse the <a href="../faq.html#physical-therapy">physical therapy questions in our FAQ</a>, or hear the full conversation on <a href="../podcast.html">the Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "physical-therapy-vs-occupational-therapy": {
        "title": "PT or OT: Which One Do You Actually Need?",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "August 2026",
        "iso": "2026-08-15",
        "tag": "Occupational Therapy",
        "teaser": "Physical therapy and occupational therapy overlap, but they are aiming at different things. How we decide, and what occupational therapy looks like in practice.",
        "body": """
<p>Two people come in the same week with the same shoulder. One wants to serve a tennis ball again. The other wants to reach the top shelf and get a shirt on without help.</p>
<p>Same joint, same injury on paper, and two different plans. That gap is roughly where physical therapy ends and occupational therapy begins.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>The short version</h2>
<p>Physical therapy is aimed at the body part. Restore the motion, rebuild the strength, resolve the pain, get the mechanics working again.</p>
<p>Occupational therapy is aimed at the day. The "occupation" in the name means everything that occupies your time: dressing, cooking, bathing, driving, handling a phone, getting through a shift at work. An occupational therapist starts from the task you cannot do and works backward to whatever is stopping you, which might be strength, or coordination, or memory, or simply that your kitchen is arranged for a version of you that had two working hands.</p>
<p>Dr. Dave Kashuba puts the split in patient terms. Some people, he says, are "building up their rotator, building up their knee, building up their ankle to go back running, playing sports. Other people are just wanting to get off the chair and be able to make themselves a pot of coffee without pain." Both are legitimate goals, and they get different plans.</p>
<p>Dr. Dave Kashuba, Ph.D., OTR, who founded our clinic in 1991 and still treats patients, is an occupational therapist himself. So the OT side of the building has never been an afterthought here.</p>

<h2>PT and OT side by side</h2>
<p>If you like things laid out in a grid, here's how the two compare at our clinic. The overlap is real, and plenty of people see both, but the starting points are different.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Physical therapy and occupational therapy compared">
<table>
<caption>Physical and occupational therapy at First Rehabilitation of North Palm Beach, from our service pages, team roster and patient FAQ. Medicare thresholds are CMS figures for calendar year 2026, as listed in our Medicare guide.</caption>
<thead><tr><th scope="col">Question</th><th scope="col">Physical therapy</th><th scope="col">Occupational therapy</th></tr></thead>
<tbody>
<tr><th scope="row">Where it starts</th><td>The movement: how far, how strong, how painful</td><td>The task: what you need to get done, and what's stopping you</td></tr>
<tr><th scope="row">Typical goals</th><td>Restore motion, strength and balance, and reduce pain</td><td>Get back to dressing, bathing, cooking, working and the rest of your day</td></tr>
<tr><th scope="row">Common reasons people come</th><td>Back and neck pain, joint replacements, sports injuries, balance and falls</td><td>Stroke, hand and arm injuries, arthritis that gets in the way of daily tasks, return to work, memory and attention changes</td></tr>
<tr><th scope="row">Who you'd see here</th><td>Kayla Dorsey, PT, DPT, or Logan Van Sant, PT, DPT</td><td>Dr. Dave Kashuba, Ph.D., OTR, Joan &ldquo;Joni&rdquo; Janik, OTD, or Laura Drumm, MS, OTR/L, CHT, CLT</td></tr>
<tr><th scope="row">Do you need a referral?</th><td>In most cases no, under Florida's direct access law, though some plans want one</td><td>Depends on your plan; the front desk checks</td></tr>
<tr><th scope="row">Medicare</th><td>Covered when medically necessary; KX threshold of $2,480 in 2026, shared with speech therapy</td><td>Covered when medically necessary; its own separate $2,480 KX threshold in 2026</td></tr>
</tbody>
</table>
</div>
<p>That last row trips people up, so a word on it. The KX threshold isn't a cap. Once your charges for the year pass that figure, the clinic adds a code to your claims confirming the care is medically necessary and documented, and therapy carries on. Our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> and the <a href="../glossary.html#kx-modifier">glossary entry on the KX modifier</a> explain it properly.</p>

<h2>Nobody gets a cookie cutter</h2>
<p>Dave is blunt about why the distinction matters: "no cookie cutters. Everyone gets evaluated, everyone gets treated differently. In many industries that's not politically correct, but in ours it is."</p>
<p>His reasoning goes past paperwork. "No two bodies are alike, no two human beings are alike," he said on the show. "The parts, they're generally the same, but nobody has the same set." Everyone has a slightly different angle to produce the same motion, which is why we train our therapists to look at the person rather than the diagnosis.</p>
<p>Practically, that means the evaluation decides the discipline, whatever the referral slip says. The answer might be physical therapy or occupational therapy, and often it is both, running together, with the two therapists talking to each other about the same patient.</p>

<h2>What occupational therapy actually does here</h2>
<p>Our occupational therapy program works on activities of daily living: the dressing, bathing and cooking that independence is made of. It covers upper extremity function and coordination, which is where it hands off to and borrows from our <a href="../services/hand-therapy.html">certified hand therapy program</a>. It includes post-stroke recovery, where the work is task specific rather than general conditioning. It covers cognitive rehabilitation, the memory and attention and problem solving side of living safely on your own. And it covers return to work, using graded conditioning and simulated job tasks, which is why so much of our <a href="../treatments/workers-comp.html">workers' compensation</a> work sits on the OT side.</p>
<p>Our occupational therapy is for adults. We don't offer pediatric OT, in-home visits or driving evaluations. Everything happens at the clinic.</p>
<h3>Daily living, one task at a time</h3>
<p>Activities of daily living, or ADLs, are the self-care tasks most people do without thinking. Our patient glossary's example of one is &ldquo;buttoning a shirt with one hand after shoulder surgery,&rdquo; which tells you how specific the work gets. Therapy practices the task itself, in the order you do it, and changes the method until you can do it on your own. Sometimes that means a dressing aid or a built-up grip. Sometimes it just means doing things in a different order.</p>
<h3>Hands and arms</h3>
<p>Dr. Matt Butler, MD, a fellowship trained hand and upper extremity orthopedic surgeon with HSS, explained on Episode 16 of our Pain 2 Power show why he chose the hand: &ldquo;That's how we all interact with our environment&hellip; something that people take for granted until it starts bothering them.&rdquo; That's the occupational therapy view in one sentence. When a hand or wrist is the limiting factor, our OTs and Laura Drumm's hand therapy program work as one plan, the protocol-driven repair work on one side and the daily-function retraining on the other.</p>
<h3>Back to work after an injury</h3>
<p>A lot of the people our occupational therapists see are working age, and the goal is specific: back to the job, safely, without the injury coming straight back. That usually means hands, wrists, elbows and shoulders, and the repetitive strain that comes from doing one motion all shift. Treatment rehearses the parts of your job that matter, at the loads, heights and pace the job involves, and progress gets reported in those same terms. That's also what an adjuster or case manager needs to see before a release. The glossary has a short definition of a <a href="../glossary.html#return-to-work">return-to-work program</a>.</p>
<p>Ergonomics belongs here too. Sometimes the fastest win is a different chair, a repositioned monitor, a different tool grip, or a piece of adaptive equipment that takes a task from impossible to routine, while the strength catches up.</p>
<h3>Memory, attention and the thinking side</h3>
<p>Occupational therapy also covers cognitive rehabilitation: memory, attention, sequencing and problem solving, aimed at practical things like managing medications, following a recipe or getting through a household routine. That side came up on our show in an unexpected way when Susan Mann of Bright Minds Processing joined us for Episode 15. She came to the subject through her children, and then through her husband's traumatic brain injury, and she named occupational therapists among the professionals in her local network. Our post on <a href="post-stroke-occupational-therapy-north-palm-beach.html">occupational therapy after a stroke</a> goes deeper into what that work looks like for adults.</p>

<h2>Where the two overlap</h2>
<p>Plenty of recoveries need both. Because we're a Medicare-certified Comprehensive Outpatient Rehabilitation Facility, physical therapy, occupational therapy and certified hand therapy happen in the same building, under one plan, with the same team reading the same notes. Two common cases show how that works.</p>
<h3>After a stroke</h3>
<p>One person might need a physical therapist for walking and balance, an occupational therapist for dressing and cooking, and our certified hand therapist for a hand that has gone weak or partly closed. Three disciplines, one patient, and the three people involved work down the hall from each other. Nobody is carrying notes between separate clinics.</p>
<h3>After shoulder surgery</h3>
<p>The physical therapy side follows your surgeon's protocol to bring back motion first and strength after, so you can reach, lift and sleep without guarding. The occupational therapy side deals with the weeks in between, when you need to get dressed, wash your hair and cook dinner with one arm out of action. Our <a href="../treatments/shoulder-pain.html">shoulder pain page</a> covers the PT half in more depth.</p>

<h2>The signal that you need one of us</h2>
<p>Orthopedic surgeon Dr. Richard Weiner, on our podcast, gave the cleanest version of when to stop waiting. You seek help, he said, "when your symptoms interfere with ADLs, which means activities of daily living."</p>
<p>That's a useful test because pain scores don't come into it. Pain is hard to rank and easy to talk yourself out of. Whether you can carry a laundry basket up the stairs is not. Dave says the same thing in his own words: you know it is time when you cannot do the normal things you like to do. People retire for a reason, and the reason was not a rocking chair.</p>
<p>A few everyday signs that point toward occupational therapy in particular: you've started avoiding the jar lids, the buttons or the car keys; you've rearranged the kitchen around a bad hand; you're back at work but quietly doing half the job one-handed; or someone close to you has noticed you're losing track of things you used to manage without thinking.</p>

<h2>Which one should you ask for?</h2>
<p>You do not have to decide. That is the evaluation's job, and getting it wrong is not on you.</p>
<p>Come in and tell us what you cannot do right now. If the answer is a motion, we will probably start on the <a href="../services/physical-therapy.html">physical therapy</a> side. If the answer is a task, we will probably start on the <a href="../services/occupational-therapy.html">occupational therapy</a> side. If it is both, you will see both, in the same building, with people who compare notes.</p>
<p>The first visit is about an hour, one-on-one, and treatment usually begins that day. Medically necessary physical and occupational therapy are both covered by Medicare, which requires a physician to certify your plan of care, and our front desk verifies your benefits before you come in.</p>
<p>We serve North Palm Beach and the surrounding Palm Beaches, including <a href="../locations/west-palm-beach.html">West Palm Beach</a>. Call <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>. Our <a href="../faq.html#occupational-therapy">FAQ answers more occupational therapy questions</a>, and you can hear Dave work through this on <a href="../podcast.html">the Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "pain-2-power-ep10-mcvicker": {
        "title": "When Back Pain Is Really a Hip: Dr. Zach McVicker on Pain 2 Power",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "August 2026",
        "iso": "2026-08-15",
        "tag": "Pain 2 Power",
        "teaser": "Hip surgeon Dr. Zach McVicker joins Dave and Mike on hip impingement, why it so often shows up as back pain, and when early surgery beats waiting.",
        "body": """
<p>Someone walks in convinced the problem is their back. The ache sits low, it has been there for months, and every conversation so far has been about the spine. Then you ask where exactly it hurts, and the answer is the groin.</p>
<p>That moment is the whole subject of this week's Pain 2 Power. Dr. Dave Kashuba and Mike McGann sat down with orthopedic surgeon Dr. Zach McVicker of the Paley Orthopedic and Spine Institute in Jupiter, who spends his days on the joint that keeps getting blamed on its neighbor.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Why a hip surgeon ended up on a back pain show</h2>
<p>Dave set the table with a reminder from a few shows back, when what walked in as ordinary back pain turned out to be cauda equina syndrome, a problem that could have killed the man who had it. Most days the answer is far less dramatic. The lesson holds anyway. &ldquo;If you have a good therapist, a good person looking at them, you realize that it's not back pain,&rdquo; Dave said.</p>
<p>The pattern he listens for is pain that travels toward the groin rather than down the leg. That points at femoroacetabular impingement, which everyone in the field shortens to FAI, and when Dave suspects it, Dr. McVicker is the surgeon he sends people to. Dr. McVicker is as good as anybody on a shoulder or an elbow, Dave said, &ldquo;But what he loves is hips.&rdquo;</p>
<h3>Who Dr. McVicker is</h3>
<p>Dr. McVicker is board certified by the American Board of Orthopaedic Surgery and fellowship trained in sports medicine at the Cedars Sinai Kerlan Jobe Institute in Los Angeles. He has served as assistant team physician for the Miami Marlins and the Jupiter Hammerheads, and he practices with the Paley Institute in Jupiter and West Palm Beach, focusing on minimally invasive arthroscopic surgery of the hip, knee, shoulder and elbow.</p>
<p>He joined Paley in 2022, as he remembered it, to build its sports medicine program. The institute already did plenty of hip preservation work, but until he arrived nobody there was doing arthroscopic hip surgery.</p>
<p>What hooked him on the joint is the detective work. &ldquo;Sometimes you got to think outside the box with it. And that's what I really like about it,&rdquo; he said. He called the hip &ldquo;more of a puzzle,&rdquo; the kind where you have to find the root problem before anything else in the picture makes sense.</p>
<h2>What a hip problem looks like when it's posing as something else</h2>
<p>Mike asked the question listeners actually want answered: when should somebody pick up the phone? Dr. McVicker didn't hesitate. &ldquo;I think that groin pain, number one, that's the most common symptom.&rdquo; Then he ran through the ones that send people down the wrong hallway for months.</p>
<ul>
<li>Low back pain, often the complaint people walk in with</li>
<li>SI joint type pain, which he described as pain toward the buttock</li>
<li>Pain on the outside of the hip</li>
<li>In some people, pelvic floor dysfunction, because some of the muscles involved with the pelvic floor get pulled into the hip problem</li>
<li>Trouble walking at all, which he summed up as &ldquo;It stops them in their tracks&rdquo;</li>
</ul>
<p>His rule for when to get the hips looked at was refreshingly plain. &ldquo;If people can't find a reason for these things, you know happy to take a look and see if the hips are an issue, but often times they are.&rdquo;</p>
<p>Dave added the activities that tend to light it up: anything that puts torque or weighted pivoting pressure through the joint, with golf near the top of his list. He also made a point about who is getting this diagnosis in our corner of Florida. &ldquo;We have 70 year old sports minded people that are playing tennis that are having this syndrome for the first time,&rdquo; he said. Drive past the courts along US-1 on a weekday morning and you'll see that crowd.</p>
<h3>Mike's frozen hip</h3>
<p>Mike had his own version. Around 2018 or 2019 (he and Dave spent a minute deciding whether that counted as pre-mask), X-rays for his long-running back trouble showed a hip that was frozen and had probably been stuck that way for years. Once it was worked loose, the change surprised him.</p>
<p>The hip had been causing trouble in his &ldquo;lower back, upper back, all down that side,&rdquo; he said. &ldquo;And it was just something in the hip that caused all of that.&rdquo; The point was how far one ball and socket joint can throw its problems.</p>
<h2>Cam, pincer and dysplasia: three shapes behind most of it</h2>
<p>Dave asked the question a therapist would ask. Does this look different in men and women, and does that change how you operate? It does. FAI comes in two shapes, and Dr. McVicker has a plain way of describing each. In a cam lesion the ball itself is misshapen: &ldquo;instead of being round, it's more like an oval peg in a round hole.&rdquo; In a pincer lesion the socket covers too much of the ball.</p>
<p>Later, when Mike asked what he sees most, a third shape came up. Hip dysplasia, the second most common problem in his practice, is the mirror image of a pincer. The socket is underdeveloped, so there simply isn't enough dome to spread your weight across.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Cam lesion, pincer lesion and hip dysplasia compared">
<table>
<caption>The three hip shapes Dr. Zach McVicker, MD described on Pain 2 Power Episode 10, quoted and paraphrased from the episode transcript.</caption>
<thead><tr><th scope="col">Problem</th><th scope="col">What is off about the shape</th><th scope="col">Who it tends to show up in</th><th scope="col">What he said about it</th></tr></thead>
<tbody>
<tr><th scope="row">Cam lesion</th><td>The ball is misshapen, &ldquo;more like an oval peg in a round hole&rdquo;</td><td>More often men</td><td>A mismatch between the shapes and how the joint is supposed to move</td></tr>
<tr><th scope="row">Pincer lesion</th><td>The socket covers too much of the ball</td><td>More often women</td><td>Technically more challenging to treat; the labrum is often calcified and may need reconstruction</td></tr>
<tr><th scope="row">Hip dysplasia</th><td>The socket is underdeveloped, with too little dome</td><td>Gymnasts and dancers who trained for hours a day while still growing</td><td>Edge loading that &ldquo;ends up in arthritis 100% of the time&rdquo;</td></tr>
</tbody>
</table>
</div>
<h3>The gasket</h3>
<p>The labrum is the piece Dr. McVicker wanted people to understand. Think of a gasket between two pipes, he said. In the hip it creates negative pressure, a suction seal, so that every time you walk the contact pressure spreads across the whole dome of the joint. Lose the seal and that pressure concentrates on cartilage that was never built to carry it that way.</p>
<p>Mike did the math out loud. Think about what the top half of your body weighs, carried with every step. You're asking the joint &ldquo;all of a sudden to carry so much more weight at specifically targeted areas,&rdquo; he said. Once the labrum is involved, the conversation went, it hurts with every step and people end up dragging the leg.</p>
<h3>Why the pincer side is the harder repair</h3>
<p>By the time a pincer hip reaches surgery, the labrum is often calcified, and it may need to be reconstructed rather than simply repaired. He was frank that this is the more technically demanding operation and needs a very experienced surgeon. Dysplasia, meanwhile, has its own typical patient. &ldquo;The typical one would be like a gymnast or a dancer, you know, who has been dedicating 5 hours a day for years and years and years while they're developing,&rdquo; he said.</p>
<h2>Arthroscopy early, or a replacement later</h2>
<p>Arthroscopic hip surgery is small work. Little cameras, little poke holes, and a recovery Dr. McVicker described as much less painful than a total hip, though getting back to sport takes a little longer. From the therapy side, Dave sees those athletes back running quickly. &ldquo;Once you're good, you're good,&rdquo; he said.</p>
<p>The trade Dr. McVicker cares about is a different one. A replacement gets you feeling fairly normal fairly quickly, &ldquo;but it's not your own hip. You don't have the proprioception&rdquo; that a native joint gives you, along with the balance that comes with it. Dave framed it as catching the problem before you need one of the hip replacement surgeons he planned to bring on the show, and a couple of episodes later he did exactly that with Dr. Michael Leighton, MD.</p>
<h3>The finger test</h3>
<p>Dave picked up the word proprioception and turned it into something you can try at the kitchen table. Close your eyes and put your hand out to the side. Have someone lift one of your fingers, up or down. Can you tell which way it went without looking? People lose that sense, Dave said, and in the legs losing it means missteps.</p>
<p>Missteps become falls. Mike connected the rest of the chain: &ldquo;once that hip break happens, there tends to be a really strong domino effect from there.&rdquo; Dave added that women, with wider hips and more laxity in the joint, need to be especially careful not to brush off back pain or groin pain. If balance is on your mind, our piece on <a href="strength-training-after-60-fall-prevention.html">strength training after 60 and fall prevention</a> picks up that thread.</p>
<h2>Where physical therapy fits, and a ten minute conversation</h2>
<p>Behind most painful hips Dave finds a weak gluteus medius, the muscle that keeps your pelvis level when you stand on one leg. His home program starts with sit to stands done with a resistance band looped just above the knees, so a sore hip can't shift your weight onto the good side, then adds abductions, clams and a prone press up. Every one is written out on our <a href="../exercises.html#hip">home exercise page</a>, and the reasoning behind the order is in our longer piece on <a href="hip-impingement-back-pain-north-palm-beach.html">hip impingement and back pain</a>. He added a practical note: before you get down on the floor, make sure you can get back up.</p>
<p>The day to day changes matter as much as the exercises. Dave's list was short: avoid sitting with your legs crossed, cut down on repetitive bending, and modify the tasks that set it off. For golfers that can mean changing the swing rather than giving up the game. &ldquo;There's ways to change your golf swing and modify your swing,&rdquo; he said.</p>
<h3>Sorting out which doctor you need</h3>
<p>Dave also described what happens when somebody isn't sure where to start. &ldquo;It takes me all of 10 minutes for me to sit down with you and go over a little bit about your symptoms,&rdquo; he said, and from that conversation he knows whether to send you to Dr. McVicker, to a back doctor, or to an orthopedic surgeon who specializes in something else. Free consultations are available at the clinic. You call to schedule one.</p>
<p>If you do need therapy, Florida's direct access law lets most people start a physical therapy evaluation without a referral, though some plans still want one and Medicare needs a physician to certify the plan of care. The front desk checks all of that before your first visit.</p>
<h2>The part of the episode that wasn't about anatomy</h2>
<p>Dave told a story on his guest. Sometimes at 8:30 at night he'll text about a patient, expecting nothing until morning, and the phone dings back with Dr. McVicker agreeing, disagreeing, or suggesting a next step. To Dave, that's a surgeon who cares how his patients come out.</p>
<p>Dr. McVicker put it in his own terms. This kind of problem is &ldquo;very, very complicated. It's very intertwined,&rdquo; he said, so you &ldquo;have to listen to people a little bit longer, and you have to care.&rdquo;</p>
<p>Mike put him on the spot for a favorite case. He told one that keeps repeating: a high school athlete with college plans, told nobody can treat this and the career is over. &ldquo;We've had that several times, and they go on to play college sports and they keep going on,&rdquo; he said. Then the part he clearly enjoys most. &ldquo;Getting that hug at the end when they're rehabbed and they feel great, there's nothing better than that.&rdquo;</p>
<p>Dave closed the topic his usual way. Whoever you choose, &ldquo;do your research before you go. Don't listen to the lady at the water cooler or in the Publix line.&rdquo; Then he asked Mike what one snowman said to the other. (&ldquo;Hey, do you smell carrots?&rdquo; Mike promised to use it somewhere, with credit.)</p>
<h2>Hear the whole conversation</h2>
<p>One bit of trivia from the top of the show. Mike asked whether our phone number was planned. Not exactly. It belonged to a hand therapist friend of Dave's, and when she retired he asked for it because surgeons remembered 624-HAND. Later he noticed the same digits spell 561-624-GAME, which let him get &ldquo;hips and shoulders and everything else, not just hands.&rdquo;</p>
<p>Listen to the full episode on <a href="../podcast.html">the Pain 2 Power podcast page</a> or watch it in our <a href="../videos.html">video library</a>, and if you're curious about the peptide conversation Dave teased at the end, the next week's guest was Paul Joyce, recapped in <a href="pain-2-power-ep11-joyce.html">our Episode 11 write up</a>. You can also read how we approach <a href="../treatments/hip-pain.html">hip pain</a> and <a href="../treatments/back-pain.html">back pain</a>, or see how our <a href="../services/physical-therapy.html">physical therapy program</a> is built.</p>
<p>If your back pain has never quite added up, or the ache shows up in your groin when you stand from a chair, come let us take a look. The clinic is at 733 US Highway 1, Suite 2A in North Palm Beach, with a free lot right at the building. Call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an evaluation</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "hip-impingement-back-pain-north-palm-beach": {
        "title": "Hip Impingement: When Your Back Pain Is Coming From Your Hip",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "August 2026",
        "iso": "2026-08-15",
        "tag": "Physical Therapy",
        "teaser": "Groin pain and a stubborn low back often point at the hip. How we evaluate and treat hip impingement in North Palm Beach, and the exercises that come first.",
        "body": """
<p>You have been treating your back for months. You have stretched it, rested it, maybe had it imaged, and it keeps coming back. Somewhere in there, nobody asked about your groin.</p>
<p>That is the gap where hip impingement lives. It is common and it responds well to treatment. It also spends a lot of time being mistaken for a lumbar problem, which means people do months of the wrong exercises for the wrong joint and then decide therapy doesn't work for them.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>What hip impingement actually is</h2>
<p>The hip is a ball sitting in a socket. Femoroacetabular impingement (FAI, if you want the short form your surgeon will use) means the two do not clear each other cleanly through their full range, so they collide at the edges instead of gliding.</p>
<h3>Cam and pincer: two shapes of the same problem</h3>
<p>It comes in two shapes. In a cam lesion the ball is misshapen. Orthopedic surgeon Dr. Zach McVicker, MD, who joined Dr. Dave Kashuba on Episode 10 of our Pain 2 Power podcast, puts it this way: &ldquo;instead of being round, it's more like an oval peg in a round hole.&rdquo; In a pincer lesion the shape problem is on the socket side, which covers more of the ball than it should. Cam lesions turn up more often in men, pincer lesions more often in women, and pincer cases are the more technically demanding to repair. By the time they reach a surgeon the labrum is often calcified, and it has to be reconstructed rather than simply repaired.</p>
<h3>The labrum, or why a small tear matters</h3>
<p>Around the rim of the socket sits the labrum. Dr. McVicker compares it to a gasket between two pipes. It creates a suction seal that spreads your body weight across the whole dome of the joint with every step. When that seal fails, load stops being shared and starts concentrating on cartilage that was not designed for it. In his words, &ldquo;if you lose that suction seal, you're going to lose the pressure, it starts increasing pressure on the cartilage in there.&rdquo;</p>
<p>Think about what that means over a day. Every step you take loads that joint with the weight of everything above it. Spread across the dome, that's manageable. Concentrated on one edge, it wears fast.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Three hip shape problems Dr. Zach McVicker described">
<table>
<caption>Three hip shape problems, as Dr. Zach McVicker, MD described them on Pain 2 Power, Episode 10.</caption>
<thead><tr><th scope="col">Problem</th><th scope="col">What is wrong with the shape</th><th scope="col">Who tends to get it</th><th scope="col">What he said about it</th></tr></thead>
<tbody>
<tr><th scope="row">Cam lesion</th><td>The ball is misshapen, &ldquo;an oval peg in a round hole&rdquo;</td><td>More often men</td><td>Impingement, cam and pincer together, is the most common hip problem he sees</td></tr>
<tr><th scope="row">Pincer lesion</th><td>The socket covers too much of the ball</td><td>More often women</td><td>Technically harder; the labrum is often calcified and has to be reconstructed</td></tr>
<tr><th scope="row">Hip dysplasia</th><td>The socket is underdeveloped, so load sits on the edge of the cartilage</td><td>Classically gymnasts and dancers who trained hours a day while still growing</td><td>The second most common problem he treats; edge loading &ldquo;ends up in arthritis 100% of the time&rdquo;</td></tr>
</tbody>
</table>
</div>
<h2>The symptoms people miss</h2>
<p>Groin pain is the one to know. &ldquo;I think that groin pain, number one, that's the most common symptom,&rdquo; Dr. McVicker said. It is also the detail that separates a hip problem from a back problem in the clinic, because Dave's tell is where the pain travels: toward the groin rather than down the leg.</p>
<p>Around it cluster the symptoms that get attributed elsewhere:</p>
<ul>
<li>Low back pain that never quite responds to back treatment</li>
<li>Pain over the SI joint, or aching toward the buttock</li>
<li>Soreness on the outside of the hip</li>
<li>For some people, pelvic floor dysfunction, because some of those muscles are affected by the hip</li>
<li>Trouble with walking itself, which he described bluntly: people are &ldquo;unable to walk. It stops them in their tracks.&rdquo;</li>
</ul>
<p>Pain shows up with anything that torques or pivots under load, which in Palm Beach County means golf, tennis and pickleball. Dave has seen this diagnosed for the first time in seventy-year-olds who are still on the court several days a week. It isn't only a young athlete's problem around here.</p>
<h3>Two clues Dave watches for</h3>
<p>One is the belt buckle. Watch where a man's belt buckle points. If it tips downward rather than sitting flat, just from the way the pelvis is aligned, the pelvis is already tilted, and hip pain is usually not far behind.</p>
<p>The other is for women, who Dave pointed out tend to have wider hips and more laxity in the joint. His advice on air was not to brush off back pain or groin pain, and to get it looked at rather than waiting it out.</p>
<h2>Why a hip problem shows up as back pain</h2>
<p>This is the part that confuses people, so go slowly here. Your hips and pelvis sit underneath everything else. Dr. McVicker tells patients the same thing every day: the hips and the pelvis are the foundation, &ldquo;and everything is built off of that, the curve of your spine, everything.&rdquo; Then the line that explains the referral pattern: &ldquo;pelvis is a ring. If you're causing abnormal torque across it, it's going to create problems throughout.&rdquo;</p>
<p>Put that in everyday terms. If the ring is being twisted from the hip end, the strain has to go somewhere, and the low back and the SI joint sit right next door. That's the logic behind looking at the hip when the back is what hurts, and it's why a back program alone can stall when the hip is the driver.</p>
<p>He called hip work a puzzle for that reason. &ldquo;Sometimes you got to think outside the box with it,&rdquo; he said. It also takes time to sort out. &ldquo;It's very, very complicated. It's very intertwined. So kind of have to listen to people a little bit longer.&rdquo; We'd say the same about a good evaluation on our side of the referral.</p>
<h3>How we tell the hip from the back</h3>
<p>At the evaluation we ask where it hurts and when, then we test. How far does the hip flex and rotate, and does a particular position reproduce the groin pain? How does your pelvis behave when you stand on one leg? Does pain travel down the leg, which points us toward the spine, or into the groin? Dave offers free consultations for exactly this sorting question, and as he put it on the show, it tells him &ldquo;whether to send you to Zach or send you to go see a back doctor or an orthopedic that specializes in something else.&rdquo;</p>
<h2>Hip impingement treatment in North Palm Beach: what therapy does</h2>
<p>Most painful hips we evaluate have one thing in common: a weak gluteus medius, the muscle on the side of the hip that keeps your pelvis level while you stand on one leg. Every step you take is briefly a single leg stance, so when that muscle gives up, the joint absorbs what the muscle should have.</p>
<h3>The first exercise</h3>
<p>The exercise Dave starts nearly everyone on is a sit to stand with a resistance band looped just above the knees. The band matters. A sore hip makes you shift your weight onto the good leg, and you will do it for weeks without noticing. Dave's explanation on air: &ldquo;if you have a hip problem, you have asymmetrical weight shift on one more than the other. So if you add a theraband and you do the same exercises, it stabilizes and makes you equalize.&rdquo; The movement retrains the pattern instead of reinforcing it.</p>
<h3>Building the program</h3>
<p>From there the program builds: standing leg abductions holding the back of a chair, kicking away from the midline; clams to strengthen the external rotators, which are weak in almost everybody because nothing in daily life asks for them; a side lying leg raise; and a prone cobra with the pelvis staying down on the floor to open the front of the hip. One piece of practical advice from Dave that belongs with any floor exercise: make sure you can get back up before you get down there. All five are written out with sets and reps in the hip section of our <a href="../exercises.html#hip">home exercise library</a>.</p>
<h3>Changing how you load the hip</h3>
<p>Load management does the rest. Stop sitting with your legs crossed, and break up repetitive bending. Modify the task rather than abandoning it. And rather than giving up golf, change the swing so it stops driving torque through the hip. &ldquo;There's ways to change your golf swing and modify your swing,&rdquo; Dave said, and for a lot of our patients that conversation matters more than any single exercise, because eighteen holes three mornings a week is a lot of rotation.</p>
<h2>When it is time for a surgeon</h2>
<p>Therapy is where this should start, and for many people it is where it ends. The reason we do not wait indefinitely is that a torn labral seal keeps letting the joint grind at itself.</p>
<p>Hip dysplasia raises the stakes. There the socket is underdeveloped, so the load concentrates at the edge of the cartilage rather than spreading across it. Dr. McVicker's assessment was direct: that edge loading &ldquo;ends up in arthritis 100% of the time.&rdquo; Labral tears come early, and the surrounding soft tissue takes a beating. Gymnasts, dancers and long distance runners are the classic histories.</p>
<p>Modern hip arthroscopy is small work, done through a few poke holes with a camera, and it preserves the joint you were born with. Dr. McVicker described the recovery as much less painful than a total hip, though return to sport takes somewhat longer. That is the argument for looking early rather than waiting for the conversation to become about replacement. As Dr. McVicker noted, a replacement can feel close to normal, &ldquo;but it's not your own hip. You don't have the proprioception&rdquo; that your native joint provides. That positional sense is what keeps you from missteps, and missteps are what turn into falls.</p>
<p>He also told the story of high school athletes who had been told their careers were over, and who went on to play college sports after treatment and rehab. Dr. McVicker practices with the Paley Orthopedic and Spine Institute in <a href="../locations/jupiter.html">Jupiter</a> and West Palm Beach, and he is one of the surgeons Dave sends hip patients to when a joint needs more than therapy can give it. For the full conversation, read <a href="pain-2-power-ep10-mcvicker.html">our Episode 10 recap with Dr. McVicker</a>.</p>
<h2>And if the hip is past saving</h2>
<p>Some hips get to the point where the arthritis has already won, and replacement is the right call. That is not a failure. Orthopedic surgeon Dr. Michael Leighton, MD, who joined us for Episode 12, called total hip replacement &ldquo;the best operation that's done in orthopedics.&rdquo;</p>
<p>His recovery priorities were simple and in order: &ldquo;it's first about getting motion back. Second, obviously allowing the wound to heal.&rdquo; Many of the old dislocation precautions that used to keep people in traction are mostly gone now, though he still wants patients to avoid the most provocative positions early on. He had kind words for the therapy side of that: &ldquo;providing them with guardrails like the physical therapists frequently do are really very helpful.&rdquo; Our <a href="../treatments/post-surgical.html">post-surgical rehabilitation</a> follows your surgeon's protocol exactly, from the first visit back on your feet through walking without help.</p>
<h2>Start with an evaluation</h2>
<p>If your back pain has never fully explained itself, or the ache sits in your groin when you get up from a chair, an evaluation is the fastest way to find out which joint is actually responsible. We will look at how your hip moves, how your pelvis behaves under load, and how much work that gluteus medius is really doing, then build the program from what we find. In most cases Florida lets you start a physical therapy evaluation without a referral, and our front desk checks your benefits first.</p>
<p>Call <strong>561-624-4263</strong> or <a href="../contact.html">request an appointment</a>. You can read more about our approach to <a href="../treatments/hip-pain.html">hip pain</a> and <a href="../treatments/back-pain.html">back pain</a>, see how we structure <a href="../services/physical-therapy.html">physical therapy</a>, browse the <a href="../faq.html#physical-therapy">physical therapy questions in our FAQ</a>, or hear the full conversation on <a href="../podcast.html">the Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "reverse-shoulder-replacement-explained": {
        "title": "Total vs. Reverse Shoulder Replacement: How Surgeons Decide",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "August 2026",
        "iso": "2026-08-02",
        "tag": "Shoulders &amp; Arms",
        "teaser": "A shoulder surgeon explains total vs. reverse shoulder replacement, why your rotator cuff decides which one you get, and how rehab shapes the result.",
        "body": """
<p>Most people hear &ldquo;shoulder replacement&rdquo; and picture one operation. There are actually two very different versions, and which one you get depends less on how much your shoulder hurts than on the condition of one structure: your rotator cuff. If a surgeon has just told you the word &ldquo;reverse&rdquo; and you nodded along without quite following, you're in good company. This is the explanation we wish every patient got before they walked into our North Palm Beach clinic for their first post-op visit.</p>
<p>On a recent episode of our <a href="../podcast.html">Pain 2 Power radio show</a>, Dr. Dave Kashuba and Mike McGann sat down with Dr. Ryan Simovitch, an orthopedic shoulder surgeon who helped build HSS's orthopedic program in Florida from a core group of five people to nearly seventeen surgeons and physicians. He trained at Duke, with a shoulder fellowship split between Harvard and Zurich, and has been in practice about twenty years. The following week, Dr. Vani Sabesan, MD, an orthopaedic shoulder surgeon and the Florida Orthopaedic Society's first female president, picked up the same thread and pushed it further. Between the two of them, you get a pretty complete picture of how replacement surgery works now, and what happens to your shoulder afterward.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Two buckets of patients</h2>
<p>Dr. Simovitch described his evaluation as sorting patients into two groups. He was quick to add that no two of them arrive the same way. &ldquo;Every patient has a different story,&rdquo; he said. &ldquo;And every MRI looks a little bit different.&rdquo; But the first fork in the road is simple enough to explain at a kitchen table.</p>
<h3>When the cuff still works</h3>
<p>The first group is people with shoulder arthritis whose rotator cuff is still intact. The cartilage is worn, often bone-on-bone, but the cuff muscles and tendons wrapped around the joint are still doing their job. &ldquo;Historically and even now, I'll still mostly do a regular anatomic replacement&rdquo; for this group, he said.</p>
<h3>When the cuff doesn't, or the bone has other plans</h3>
<p>The second group is people whose rotator cuff is <em>not</em> intact, whether or not arthritis is present. That might be a cuff that's deficient, or chronic cuff problems that can't be repaired another way. For them, he does a reverse.</p>
<p>A few situations push toward a reverse even when the cuff is fine: significant bone wear, a revision of a previous replacement, or severely limited function going in. So if you've been told you need a reverse and you've never had a cuff tear in your life, that's not necessarily a contradiction. Ask your surgeon which of those reasons applies to you. It's a fair question, and the answer will matter to your therapist later.</p>
<h2>What &ldquo;reverse&rdquo; actually reverses</h2>
<p>An anatomic total shoulder rebuilds the joint the way it was designed. The ball side gets a metal ball on a stem; the socket side gets a plastic socket. Natural layout, replacement parts.</p>
<p>That design has a requirement: your rotator cuff has to work. The cuff is what compresses the ball into the socket, holds it stable, and drives motion. Without it, the joint has no stability. As Dr. Simovitch explained, even when great therapists push hard to make it function for a while, the implant gets loaded in an unusual way that can cause it to fail in the near term.</p>
<p>The reverse is exactly what it sounds like. The ball goes on the socket side, and the socket goes on the ball side. Flipping the geometry builds stability into the hardware itself. The joint no longer depends on a cuff that can't do the job, and it's protected from the wear pattern that would eventually destroy an anatomic replacement in that shoulder. Here's the side-by-side.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Anatomic and reverse shoulder replacement compared">
<table>
<caption>Anatomic versus reverse total shoulder, as Dr. Ryan Simovitch described them on Pain 2 Power Episode 8.</caption>
<thead><tr><th scope="col">&nbsp;</th><th scope="col">Anatomic total shoulder</th><th scope="col">Reverse total shoulder</th></tr></thead>
<tbody>
<tr><th scope="row">Layout</th><td>Ball on the ball side, socket on the socket side, like the original joint</td><td>Ball on the socket side, socket on the ball side</td></tr>
<tr><th scope="row">Who it's usually for</th><td>Arthritis with an intact rotator cuff</td><td>A deficient or irreparable cuff, with or without arthritis</td></tr>
<tr><th scope="row">Where stability comes from</th><td>The rotator cuff holding the ball in the socket</td><td>The implant's own geometry</td></tr>
<tr><th scope="row">Other reasons to choose it</th><td>&nbsp;</td><td>Significant bone wear, revision of an earlier replacement, severely limited function beforehand</td></tr>
</tbody>
</table>
</div>
<h2>Why reverse outcomes got so much better</h2>
<p>Dave raised something he's watched change from the therapy side. Fifteen or twenty years ago, patients with a reverse struggled to get external rotation past zero degrees, with limited strength. In plain terms, they couldn't turn the arm outward, which makes combing your hair or reaching for a seatbelt a chore. Now he sees them come back with rotation and strength that look clinically excellent.</p>
<p>Dr. Simovitch credited several things working together. The detail matters, because it's why one surgeon isn't interchangeable with another. &ldquo;There's right ways, there's wrong ways, there's no between ways,&rdquo; he said. &ldquo;And if you do the right way and the right patient, generally you're going to have good outcomes or great outcomes.&rdquo;</p>
<h3>The right patient</h3>
<p>Whether the <em>posterior</em> cuff, the back portion, is intact largely determines how much external rotation you'll get. When it isn't, a tendon transfer can improve the odds.</p>
<h3>Implant choice and positioning</h3>
<p>Implants vary in how far they shift the joint outward. Get that tensioning wrong and the muscle can't perform correctly. It's the same principle behind any muscle's length-tension relationship.</p>
<h3>What gets repaired, and what doesn't</h3>
<p>Repairing the subscapularis at the front of the shoulder adds stability but can tether external rotation, so he doesn't routinely repair it in patients where he expects that trade-off to cost them motion. Dave's blunter version, on which cuff tendon he'd least mind losing in a reverse: &ldquo;If they're going to have a tear of a rotator cuff, let it be the subscap.&rdquo;</p>
<h2>Six weeks in a sling, or moving tomorrow?</h2>
<p>On Episode 9, Dave opened by describing what he sees with Dr. Sabesan's reverse patients: &ldquo;she's trying to get you to reach behind and put your hand in your pocket within a couple of weeks.&rdquo; If you've heard the older story about a long stretch of immobilization after shoulder surgery, that sounds fast. It is.</p>
<p>Dr. Sabesan explained how she got there, and it's personal. Her mother has had two reverses. &ldquo;Do you want to spend six weeks in a sling or would you rather start moving tomorrow?&rdquo; she said. &ldquo;Just because you're 76, not driving for six weeks can really disable you from your life, your lifestyle, your family.&rdquo; Her mom, as it happens, drives the grandkids to school.</p>
<p>So her practice compared the two approaches head to head: one partner kept patients in the sling for six weeks, and she had people moving within days. She reported no complications and similar outcomes, and added, &ldquo;in fact, at six weeks, they're doing a ton better.&rdquo; Her takeaway was aimed at her own profession: &ldquo;You can't sit and stay the same as a surgeon.&rdquo;</p>
<p>A word of caution before anyone in a sling reads this and takes it off. Early motion was her protocol, for her patients, built around how she does the operation. Your surgeon sets your protocol, and we follow it exactly. What's changed is that early motion is now on the table, so ask your surgeon where they land on it. Dave's own experience with her patients, for what it's worth: &ldquo;with her reverse total shoulders, I've had nothing but good ones.&rdquo;</p>
<h2>The newer ideas surgeons are working on</h2>
<p>Dr. Sabesan was refreshingly unimpressed by technology for its own sake. Her test is whether a new tool solves a patient's problem. &ldquo;Tech for tech's sake versus tech, solve your problem,&rdquo; was how she put it. Less pain, faster recovery, bone that grows better, a cuff that heals. She was equally blunt about robots in shoulder and joint surgery, calling them a great marketing tool without much science yet behind them.</p>
<p>The ideas she is excited about are ones that change what rehab looks like afterward, which is exactly why we pay attention.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Newer shoulder replacement ideas Dr. Sabesan described">
<table>
<caption>Approaches Dr. Vani Sabesan, MD described on Pain 2 Power Episode 9, in her own terms. Whether any applies to you is your surgeon's call.</caption>
<thead><tr><th scope="col">Idea</th><th scope="col">What she said it is</th><th scope="col">Why it matters for recovery</th></tr></thead>
<tbody>
<tr><th scope="row">Muscle sparing</th><td>Doing the replacement without cutting the subscapularis at the front of the shoulder</td><td>She said a cut subscap means a six-week restriction while it heals; leaving it alone means no restrictions to start</td></tr>
<tr><th scope="row">Stemless implants</th><td>Implants, some 3D printed, designed for your bone to heal into</td><td>Part of what she called making your bone grow better</td></tr>
<tr><th scope="row">Pyrocarbon</th><td>A different material that lets the surgeon resurface one side of the joint instead of both</td><td>She said it won't wear away or cause the same levels of pain as trying to do both sides</td></tr>
<tr><th scope="row">Personalized implants</th><td>Implants 3D printed to the patient's own anatomy and size, from a design team she is part of</td><td>Her hope: a better fit and a quicker return to the gym</td></tr>
</tbody>
</table>
</div>
<h3>Muscle sparing, in her words</h3>
<p>The muscle-sparing idea is the one with the most obvious rehab payoff. &ldquo;The subscap, if you cut into it, needs to heal like any other muscle you do, and that's a restriction for six weeks, and it sometimes can lead to lifelong problems,&rdquo; Dr. Sabesan said. Notice it's the same tendon Dr. Simovitch talked about from the other direction. One surgeon sometimes chooses not to repair it so it won't tether rotation; another is developing ways to avoid cutting it at all. Either way, the subscapularis is a big part of what your therapist is managing in those first weeks.</p>
<h3>When a replacement needs replacing</h3>
<p>Revisions came up too, and her answer is one we'd like every worried patient to hear. She said she probably enjoys the complex cases the most, and &ldquo;no one is at the end of the line to me.&rdquo; She also described patients back to competitive heavy lifting after shoulder surgery, which drew an honest &ldquo;That would be terrifying to me&rdquo; from across the studio table.</p>
<h2>What happens on the therapy side</h2>
<p>Two people can have &ldquo;a shoulder replacement&rdquo; and need different rehab, depending on which implant went in, what was repaired, and which protocol the surgeon follows.</p>
<h3>Why we ask for your operative report</h3>
<p>Dave's team chases down operative reports specifically to learn what was done; for a rotator cuff repair, even whether it was a double-row technique. &ldquo;It means a lot to the therapist to know what they're doing,&rdquo; he said. His argument for choosing a therapist-owned clinic is exactly this: therapists don't perform the surgery, but they need to understand it to rehab it. On Episode 9 he described the other half of that homework: &ldquo;We have to know what the doctor intends their patients to be able to do.&rdquo; When they'll be discharged, how far the surgeon trusts the therapist to progress them, how hard is too hard.</p>
<p>He also described the cost of getting it wrong in the reverse era. When external rotation wasn't coming back, therapists would end up working around it, patients drifted into a forward-shoulder position (bad for a reverse), and motion stalled around 80 to 90 degrees. He's seen scapular fractures in patients whose rehab wasn't handled carefully.</p>
<p>Dr. Simovitch put it plainly from the surgical side: &ldquo;The surgeon matters, the surgery matters, but the therapy matters just as well.&rdquo; Dr. Sabesan backed it with her own numbers. Her team surveyed their shoulder replacement patients, and nearly all of them said their therapist had a big impact on the result. Her comparison was a good hairdresser: someone who talks to you, listens, and adjusts.</p>
<h3>What it looks like here</h3>
<p>At First Rehabilitation your first visit runs about an hour, one-on-one with a therapist, and treatment usually begins that day. We take your history, read what your surgeon sent, measure where your motion and strength are, and write a <a href="../glossary.html#plan-of-care">plan of care</a> around your surgeon's protocol. If you're on Medicare, your physician certifies that plan; our front desk handles the paperwork and verifies your benefits before you come in. Our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> walks through deductibles and coinsurance.</p>
<p>Then comes the part that's on you. Captain Kerry Titheradge, of Bravo's Below Deck, first came to Dave more than twenty years ago with a rotator cuff injury. &ldquo;Full motion is very, very important,&rdquo; he said on Episode 13, since he was working on deck at the time. What he remembers about that rehab: &ldquo;I remember just following everything you said to the tee.&rdquo; Dave's warning on the same episode runs the other way. Do the exercises precisely, and don't decide that if ten repetitions are good, fifty must be better.</p>
<h2>What you can do before any of this is on the table</h2>
<p>Both Dave and Dr. Simovitch spent the back half of Episode 8 on prevention, and none of it is complicated.</p>
<p>Dr. Simovitch&rsquo;s warning is about what he calls the constant warrior: the person playing pickleball six days a week with no moderation and no preparation, who plays until something tears. (He's watched patients switch from right-handed to left-handed rather than stop.) Dr. Sabesan made the same point about Florida: the weather lets people play all year round, which is wonderful until the shoulder gets a vote.</p>
<p>His simple home routine:</p>
<ul>
<li>Wall slides: both arms at 90 degrees against a wall, slide all the way up, three sets of ten</li>
<li>Cross-body stretch: take your right elbow with your left hand and pull across your body to stretch the posterior capsule</li>
<li>Shoulder shrugs: up and down, three sets of ten</li>
<li>Scapular retractions: squeeze your shoulder blades toward each other</li>
</ul>
<p>Add resistance bands for rows and extensions. His reasoning: nearly everything we do all day is internal rotation, so pulling <em>outward</em> is what balances it. Step-by-step instructions are on our <a href="../exercises.html#shoulder">home exercises page</a>. If you already have a replacement, check with your surgeon and therapist before adding any of these, because your protocol comes first.</p>
<p>And the one he repeats most: get out of the chair. &ldquo;The invention of the chair is one of our demise.&rdquo; Ten or fifteen minutes of walking a day, sit-to-stands, whatever gets you moving.</p>
<p>His whole goal, in his words: &ldquo;I do everything I can to let people not ever come to see me.&rdquo;</p>
<h2>If your shoulder is already talking to you</h2>
<p>You don't need a diagnosis to start. If reaching overhead or getting your arm behind your back has become a problem, an evaluation tells you which path you're on, and often that path doesn't include surgery at all. If it does, we'll coordinate with your surgeon before and after, and you can hear both full conversations on our <a href="../podcast.html">podcast page</a> and watch the episodes on <a href="../videos.html">our videos page</a>.</p>
<p>Call us at <strong>561-624-4263</strong> or <a href="../contact.html">request an appointment</a>. You can read more about how we treat <a href="../treatments/shoulder-pain.html">shoulder pain</a>, what <a href="../treatments/post-surgical.html">post-surgical rehabilitation</a> involves, and what <a href="../services/physical-therapy.html">physical therapy</a> looks like here. Our <a href="../faq.html#getting-started">FAQ</a> answers the practical questions about insurance and scheduling.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "what-to-expect-first-pt-visit": {
        "title": "What to Expect at Your First Physical Therapy Visit",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "July 2026",
        "tag": "Getting Started",
        "teaser": "Nervous about your first appointment? Here's exactly how the first hour goes at First Rehabilitation — no surprises, no jargon.",
        "body": """
<p>If you've never been to physical therapy before, the first visit can feel like a mystery. This is how it works at our clinic, start to finish, so you can arrive relaxed.</p>
<p>Most of the nerves come from not knowing what's going to happen. Will they make me do something that hurts? Do I need a doctor's note? Is this going to be an hour of paperwork? The short answers are no, probably not, and no. The longer answers are below, in the order things actually happen when you come through the door at 733 US Highway 1.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>Before you walk in</h2>
<p>The first visit really starts with a phone call. When you call 561-624-4263, or send a request through the website, our front desk finds you a time and then does the unglamorous part: checking your insurance. Once you're scheduled, we email you an intake form. Fill it out at home if you can, so your hour starts with therapy rather than a clipboard. If you couldn't get to it, come a few minutes early and the front desk will help you finish it.</p>
<h3>Do you need a referral?</h3>
<p>Usually not to get started. Florida's direct access law lets most people begin a physical therapy evaluation without a physician referral. There are two catches. Some insurance plans still want a referral before they'll pay, and Medicare requires a physician, or another qualified provider such as a nurse practitioner or physician assistant, to certify your plan of care. We send that plan to your doctor and chase it until it comes back signed, so it doesn't become your errand. Our glossary has a plain-English entry on <a href="../glossary.html#direct-access">direct access</a> if you want the short definition.</p>
<h3>What the front desk checks</h3>
<p>Before your first appointment, we verify your coverage and tell you what your plan pays for, whether you have a copay or a deductible to meet, and whether you need a referral. We accept Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network, workers' compensation and self-pay.</p>
<p>If you're on Original Medicare, the 2026 numbers are a Part B deductible of $283 (Federal Register, November 19, 2025), then 20% of the Medicare-approved amount per visit (Medicare.gov). A Medigap or secondary plan may pick up some or all of that 20%. Medicare Advantage plans set their own copays and often need prior authorization, which we request for you. Our <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> has the full picture, including why the old therapy cap no longer exists.</p>

<h2>What to bring, what to wear, and how the hour runs</h2>
<p>Here's the packing list. It's short.</p>
<ul>
<li>A photo ID.</li>
<li>Every insurance card you have, including any Medigap or secondary plan, so we can sort out which one pays first.</li>
<li>Your prescription or referral, if your physician gave you one.</li>
<li>Imaging reports, and your surgeon's post-op protocol if you've had surgery.</li>
<li>Claim information, if your visit relates to a work injury or a car accident.</li>
<li>Comfortable clothes and supportive sneakers: shorts for a knee, hip or ankle, and a loose shirt for a shoulder, arm or hand.</li>
</ul>
<p>Parking is easy. There's a free lot right at our building, so you park, walk in, and you're here.</p>
<p>And this is roughly how the visit itself goes, step by step.</p>
<div class="data-table" tabindex="0" role="region" aria-label="How a first physical therapy visit runs at First Rehabilitation">
<table>
<caption>The stages of a first visit at First Rehabilitation of North Palm Beach, drawn from our Your First Visit page and patient FAQ.</caption>
<thead><tr><th scope="col">Stage</th><th scope="col">What happens</th><th scope="col">What you'll leave that stage with</th></tr></thead>
<tbody>
<tr><th scope="row">Before the day</th><td>Front desk verifies your benefits; we email an intake form</td><td>Your copay or deductible, and whether you need a referral</td></tr>
<tr><th scope="row">Arriving</th><td>Free parking at the building; front desk helps with any unfinished forms</td><td>Paperwork done, so the hour goes to you</td></tr>
<tr><th scope="row">The conversation</th><td>One-on-one with your therapist: your story, your symptoms, your goals</td><td>Goals written in your own terms</td></tr>
<tr><th scope="row">The movement evaluation</th><td>Walking, bending, reaching; strength, range of motion and balance measured</td><td>An explanation of what's driving the problem</td></tr>
<tr><th scope="row">Treatment</th><td>Usually begins the same day: hands-on care, guided movement, first home exercises</td><td>One or two exercises to do at home</td></tr>
<tr><th scope="row">Before you leave</th><td>Plan of care set; follow-up visits scheduled</td><td>Your next appointments on the calendar</td></tr>
</tbody>
</table>
</div>
<p>The whole first visit takes about an hour. Follow-ups are their own thing, and the front desk will tell you how much time to set aside when you book them.</p>

<h2>It starts with a conversation</h2>
<p>Before anyone touches anything, your therapist sits down with you. When did the pain start? What makes it better or worse? What does it keep you from doing: golf, gardening, pickleball, picking up a grandchild, sleeping through the night? Your goals shape everything that follows, so the more honestly you answer, the better your plan will be.</p>
<p>Dr. Dave Kashuba, Ph.D., OTR, who founded the clinic in 1991, explained why this conversation carries so much weight on Episode 9 of our Pain 2 Power show: &ldquo;we take everything that you say and you put it into your plan of care, because whatever you tell us subjectively is how we make our assessment and objectively treat you by your subjective complaints.&rdquo;</p>
<h3>The details that change the plan</h3>
<p>The little things you might not think to mention are often the useful ones. Dave's example on that same show was the shoulder that &ldquo;really aches at night,&rdquo; a detail that points the evaluation in a particular direction. So tell us when it hurts, what you were doing, how you sleep, what you've already tried, and what your job asks of you. If you drive up and down US-1 all day, or sit at a desk, or spend your mornings on the court, we want to know.</p>
<p>Bring your own goals, too. &ldquo;I want to walk eighteen holes&rdquo; and &ldquo;I want to get the groceries in from the car&rdquo; lead to different plans, and both are good goals. Dave put it plainly on Episode 9: for some people the goal is a game, and for others it's &ldquo;getting the ability again to reach to the top shelf.&rdquo;</p>
<h3>Why listening matters this much</h3>
<p>Orthopaedic shoulder surgeon Dr. Vani Sabesan, MD, the first female president of the Florida Orthopaedic Society, described good care on the same episode as a matter of paying attention: &ldquo;you listen to your patients and you hear what their needs are and you try to advance what you do, how you do it with that.&rdquo; Dave, when he got the microphone back, added that people &ldquo;don't realize how important it is to have your therapist take really good notes and listen.&rdquo;</p>
<p>So if you feel like your therapist is asking a lot of questions in the first fifteen minutes, that's the evaluation doing its job.</p>

<h2>Then, a movement evaluation</h2>
<p>Your therapist will watch you move: walking, bending, reaching, getting up from a chair, whatever relates to your problem. We measure strength, range of motion and balance, and we look for the specific patterns contributing to your pain. It's detective work, and the rest of your plan is built on it.</p>
<p>It also tends to look beyond the sore spot. Back pain gets a look at your hips. A knee gets a look at how the whole leg is loading. A sore shoulder gets a look at the shoulder blade and your posture. That's because the place that hurts isn't always the place that's causing it.</p>
<p>No two people move quite the same way, which is why the evaluation is individual. Dave said on Episode 8 that &ldquo;everyone has a different angle to do the same motion,&rdquo; and the clinic trains its therapists to look at the person in front of them rather than the diagnosis on the paperwork. Our <a href="../glossary.html#initial-evaluation">glossary entry on the initial evaluation</a> sums the visit up in two sentences if you want the short version.</p>
<p>If anything in the evaluation suggests you need something other than therapy, such as imaging, a surgical opinion or a different specialist, we'll tell you. We evaluate and treat; diagnosing is your physician's job, and we coordinate with them when the plan needs to change.</p>

<h2>Treatment usually begins on day one</h2>
<p>Most patients receive hands-on treatment at the very first visit. That might mean gentle manual therapy to free up a stiff joint, guided movement, and the first one or two exercises of a home program. You'll leave knowing what's going on and what you can do between visits to move things along.</p>
<p>People are often surprised by that. They expect the first appointment to be all forms and measuring. Here, the evaluation and the start of treatment happen in the same hour, one-on-one.</p>
<p>The home exercises matter more than people expect. Captain Kerry Titheradge, from Bravo's Below Deck, came to Dave as a patient about twenty years ago with a shoulder problem. On Episode 13 he remembered it this way: &ldquo;I remember just following everything you said to the tee, and you were really impressed with how quickly I got back to speed.&rdquo; Following through between visits is the part of the plan only you can do. Our <a href="../exercises.html">home exercises page</a> shows the kind of short sets Dave hands patients.</p>
<p>Dr. Sabesan compared a good therapist to &ldquo;having a hairdresser. They talk to you. They listen to you. It's the company you need.&rdquo; She said her practice surveyed its shoulder replacement patients and found that 98 percent said the therapist had a huge impact on their outcome. That's her figure, from her own patients, and it's a nice way of saying the relationship counts.</p>

<h2>Before you leave: the plan and the next visit</h2>
<p>By the end of the hour you'll have a plan of care: your goals, the treatment, how often you'll come and roughly for how long. For Medicare patients that's the document your doctor signs. Our glossary's example of a <a href="../glossary.html#plan-of-care">plan of care</a> gives you the flavor.</p>
<p>How many visits will you need? It varies. A recent ankle sprain and a knee replacement follow very different timelines, and so do two people with the same knee. Your therapist will propose a frequency and set realistic milestones, then re-check your progress along the way and adjust the plan to how you're doing. You shouldn't be coming to sessions you don't need.</p>
<p>Your follow-ups get booked before you walk out, so the recovery has a rhythm from the start. Consistent attendance is one of the biggest drivers of a good result, and it's much easier to keep a standing appointment than to remember to call.</p>

<h2>Common first-visit worries, answered</h2>
<h3>Will it hurt?</h3>
<p>It shouldn't. Some soreness is normal when stiff joints and weak muscles start working again, a bit like the day after yard work. Your therapist stays within your tolerance, tells you what each technique should feel like, and changes course straight away if something doesn't feel right. Say so. That feedback is part of the treatment.</p>
<h3>Will I see the same therapist each time?</h3>
<p>We're a small, family-owned team, and continuity is part of how we work. When more than one of our clinicians is involved, such as a physical therapist and an occupational therapist, or our certified hand therapist, it's coordinated, with people who talk to each other down the hall. If you're not sure whether you need physical or occupational therapy, our post on <a href="physical-therapy-vs-occupational-therapy.html">PT versus OT</a> explains the difference, and the evaluation sorts it out either way.</p>
<h3>What if I've just had surgery?</h3>
<p>Then your surgeon sets the timeline. Every procedure has its own protocol, and some start therapy within days while others protect the repair for longer. We follow that protocol and coordinate with the surgeon's office, so bring your post-op paperwork to the first visit, or send it ahead, and we'll start you on schedule. Our <a href="../treatments/post-surgical.html">post-surgical rehab page</a> covers the conditions we see most after an operation.</p>
<p>Call <strong>561-624-4263</strong> to book your evaluation, or <a href="../contact.html">request an appointment online</a>. We're open Monday to Friday 8:00 AM to 5:30 PM and Saturday 8:00 AM to 12:30 PM, and our <a href="../faq.html#getting-started">Getting Started FAQ</a> answers more of the questions people ask before their first visit.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "five-morning-habits-back-pain": {
        "title": "Five Morning Habits That Ease Back Pain",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "July 2026",
        "tag": "Back &amp; Spine",
        "teaser": "The first thirty minutes of your day set the tone for your spine. Small changes to how you wake, move, and sit can pay off all day long.",
        "body": """
<p>Backs are often at their stiffest first thing in the morning. Discs rehydrate overnight and muscles cool down, so the first movements of the day can feel like the hardest ones you'll make. These five habits, drawn from what we teach patients every week, make mornings kinder to your spine.</p>
<p>None of them take long, and most cost nothing. Every one of them is something our therapists walk people through at the clinic on US-1, often in the first week of care, because the way you get out of bed and through the first half hour tends to set the tone for the rest of the day.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>

<h2>Why is your back worst when you first get up?</h2>
<p>You've spent the night lying more or less still. The discs between your vertebrae have taken on fluid, the muscles along your spine have cooled off, and nothing has asked your back to move in hours. Then, within about ten minutes of waking, most of us ask it to do a whole lot at once: sit straight up, bend over a sink, lean into a car seat, hunch over a phone at the kitchen table.</p>
<p>Dr. Dave Kashuba, Ph.D., OTR, who founded our clinic in 1991 and still treats patients, pointed out on Episode 8 of our Pain 2 Power show that people are about the only creatures that skip the warm-up. &ldquo;Babies wake up, they stretch, dogs and cats wake up, they stretch before they do anything,&rdquo; he said. &ldquo;We grab our glasses, a cup of coffee, and go to work.&rdquo;</p>
<p>Morning stiffness on its own is common, and it usually eases as you get moving. What makes it worse is loading a stiff back hard and fast. The habits below are about giving your spine a gentler ramp into the day, and then building the strength that makes the ramp less necessary over time.</p>
<p>If your mornings come with leg pain, numbness or a back that never really loosens up, skip ahead to the section on when to get it checked. Those call for a proper evaluation rather than a better routine.</p>

<h2>Habit 1: Don't sit straight up out of bed</h2>
<p>Roll to your side first, drop your legs off the edge, and push up with your arms. This &ldquo;log roll&rdquo; spares your spine the loaded crunch of a straight sit-up while the tissues are still waking up. It feels a little fussy the first few times. After a week it's automatic.</p>
<p>Here's how we usually coach it, one step at a time:</p>
<ol>
<li>Lying on your back, bend your knees so your feet are flat on the mattress.</li>
<li>Roll onto your side, letting your shoulders and hips turn together so your back doesn't twist.</li>
<li>Slide your lower legs off the edge of the bed.</li>
<li>As your legs go down, push yourself up sideways with your bottom elbow and your top hand, so your trunk comes up without curling forward.</li>
<li>Sit on the edge for a breath or two before you stand.</li>
</ol>
<p>Getting back into bed at night is the same thing in reverse: sit on the edge, lower yourself onto your side using your arms, then roll onto your back. If you're a snowbird sleeping on a softer rental mattress for the season, you'll probably notice the difference this makes even more, since a deep mattress makes the straight sit-up harder work.</p>

<h2>Habit 2: Give it two gentle minutes before the coffee</h2>
<p>Before coffee, spend two minutes moving gently. Pelvic tilts lying on your back, knees rocking side to side, or a slow walk around the house all count. Motion is lotion: easy movement gets the circulation going and takes the edge off that first-hour stiffness.</p>
<p>Keep it gentle enough that nothing hurts. You're reminding your back how to move before you ask it to carry anything.</p>
<h3>Still in bed, or on the floor</h3>
<p>Pelvic tilts are the simplest start. Lie on your back with your knees bent, then flatten the small of your back gently toward the mattress and let it relax again. Knee rocks are the follow-up: keep your knees together and let them drift a little way to one side, then the other, only as far as feels easy.</p>
<p>Some people prefer to do this on the floor because the bed is too soft. That's fine, with one condition borrowed from Dave's note on our exercises page: before you get down on the floor, make sure you can get back up.</p>
<h3>On your feet</h3>
<p>If lying down isn't your thing, walk. A slow lap of the house or a trip to the end of the driveway for the paper counts, and so do a few minutes on the lanai. Dave's advice on the show was to start small and build: &ldquo;Just a little bit of exercises, 10, 15 minutes a day, three minutes a day, and work your way up.&rdquo; Our <a href="../exercises.html#everyday">everyday movement set</a> lists walking as a daily habit for exactly that reason, and notes it's good for the back and the knees at the same time.</p>

<h2>Habit 3: Rethink the couch scroll</h2>
<p>Thirty minutes slumped over a phone puts sustained load on the very structures that stiffened overnight. If you like a slow morning, and plenty of us do, sit supported rather than folded into the couch. Sit with your back against a firm chair and your feet on the floor, and raise the phone toward eye level instead of resting it in your lap.</p>
<p>Dave has a line he uses on the radio that always gets a laugh, though he means it: &ldquo;I tell everyone the invention of the chair is one of our demise.&rdquo; His fix is plain. Put the phone down, then get up and walk or do a few sit to stands. The movement you already know how to do is usually the one that gets skipped.</p>
<p>On Episode 10, talking about hips that are just starting to hurt, he listed the small changes he'd try first: &ldquo;you want to avoid sitting with your legs crossed, repetitive bending, a modification of tasks.&rdquo; The same thinking works for a cranky low back in the morning. If your routine involves sitting cross-legged with the news, unloading the whole dishwasher bent at the waist, then sitting again for the drive to work, try spreading those jobs out or changing how you do them.</p>
<p>The home office deserves a look too. A monitor set a couple of inches too low will pull you into the same slump as the couch, eight hours at a stretch. Raise the screen and bring the chair in close. Then get up every so often.</p>

<h2>Habit 4: Let warm water do some of the work</h2>
<p>A warm shower relaxes the muscles along your spine and makes the morning's movement easier. Let the water hit your lower back for a minute or two, then follow it with a gentle bend forward and back, staying well inside what's comfortable.</p>
<p>If you don't shower in the morning, a warm pack does the same job. Our patient glossary uses &ldquo;a warm pack before stretching a stiff back&rdquo; as its example of a modality, which is the clinical word for supporting treatments like heat, cold and electrical stimulation. You can read <a href="../glossary.html#modalities">the glossary entry on modalities</a> if you're curious what else falls under that heading.</p>
<p>Heat has one limit. It makes the stiffness easier to move through, but it doesn't build anything, so in the clinic we use modalities to support strengthening work rather than replace it. Think of the shower as the warm-up for habit five. And if warmth makes your back feel worse rather than looser, stop and mention it to your therapist.</p>

<h2>Habit 5: Anchor one strengthening habit</h2>
<p>The long-term fix for most recurring back pain is strength: core, hips and glutes. Attaching one simple exercise, such as a bridge or a bird dog, to something you already do every morning, like brushing your teeth, is how it sticks.</p>
<h3>A short menu to pick from</h3>
<p>You don't need all of these. Pick one or two that feel manageable and make them part of the morning. Every exercise in this table appears on our <a href="../exercises.html">home exercises page</a>, and every one of them is something Dave prescribed on air.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Morning exercise menu from our home exercises page">
<table>
<caption>Six moves from the firstrehabnpb.com home exercises page, each one prescribed by Dr. Dave Kashuba on Pain 2 Power. Doses are as listed on that page; your therapist may change them.</caption>
<thead><tr><th scope="col">Exercise</th><th scope="col">How much, as listed</th><th scope="col">What our exercises page says it does</th><th scope="col">Episode</th></tr></thead>
<tbody>
<tr><th scope="row">Walk</th><td>Daily, starting at three minutes and working up toward 10 or 15</td><td>Gets blood moving and helps the back and knees at the same time</td><td>8</td></tr>
<tr><th scope="row">Stretch before you start the day</th><td>Every morning</td><td>Costs nothing and sets up everything else</td><td>8</td></tr>
<tr><th scope="row">Sit to stands</th><td>Little and often, without pushing off with your hands if you can</td><td>The most functional movement most people stop practising</td><td>8</td></tr>
<tr><th scope="row">Glute bridge</th><td>3 sets of 10</td><td>Works the glutes; lift your hips, pause and squeeze at the top</td><td>7</td></tr>
<tr><th scope="row">Clams</th><td>3 sets of 10 each side</td><td>Strengthens the hip's external rotators, which nothing in daily life asks for</td><td>10</td></tr>
<tr><th scope="row">Standing leg abductions</th><td>3 sets of 10 each side, holding the back of a chair</td><td>Direct work for the gluteus medius</td><td>10</td></tr>
</tbody>
</table>
</div>
<h3>Why your hips get a say</h3>
<p>You'll notice half of that menu is hip work. That's on purpose. A stiff or weak hip can push extra work onto the low back, and sometimes what feels like back pain is actually coming from the hip.</p>
<p>Orthopedic surgeon Dr. Zach McVicker, MD, of Paley Orthopedic and Spine Institute, made the point on Episode 10: &ldquo;for hips, a lot of times it's causing the back pain, it's causing the groin pain and other symptoms that you're having.&rdquo; Asked which symptoms should send someone to have their hips checked, he started with groin pain, then added &ldquo;low back pain, SI joint type pain. So pain kind of towards the buttock, pain on the outside of the hip.&rdquo; If that sounds familiar, our post on <a href="hip-impingement-back-pain-north-palm-beach.html">hip impingement and back pain</a> goes further.</p>
<h3>Making it stick</h3>
<p>The habit matters more than the exercise. Ten bridges while the coffee brews, sit to stands every time you get up from the breakfast table, clams before you get dressed. Three minutes counts. A little every day does more than a long session now and then, which is the same thing Dave tells every patient leaving with a home program.</p>

<h2>When should morning back pain get a professional look?</h2>
<p>If mornings are consistently painful, if the stiffness doesn't ease as the day goes on, or if pain runs into your leg, have a professional look at it. Sciatica, discs and spinal stenosis are all on the list our <a href="../treatments/back-pain.html">back pain program</a> treats, and they respond better to a plan than to a routine you've pieced together yourself.</p>
<p>A few things shouldn't wait for a therapy appointment at all. Back pain with loss of bladder or bowel control, numbness in the groin or inner thighs, or leg weakness that keeps getting worse needs urgent medical care. So does back pain after a real fall or accident, or back pain that comes with a fever. Once a physician has ruled those out, physical therapy can treat the mechanical side with confidence.</p>
<p>Dave's view, said plainly on Episode 10, is that &ldquo;you can't cookie cut what programs you're going to do if someone comes in with back pain.&rdquo; Two people can describe the same stiff morning and need very different things. That's the job of the evaluation, and it's why nothing on this page should replace one.</p>

<h2>What we'd do at the clinic</h2>
<p>Plan on about an hour, one-on-one with your therapist. We'll ask what your mornings look like, what you do for work and fun, and what makes the pain better or worse. Then we watch you walk, bend and sit, check your hips as well as your spine, and measure strength and range of motion. Treatment usually starts the same day, and you leave with the first exercises of your home program, often one or two of the moves in the table above. Our post on <a href="what-to-expect-first-pt-visit.html">what to expect at your first visit</a> walks through the hour in more detail.</p>
<p>In most cases Florida's direct access law lets you start a physical therapy evaluation without a physician referral, though some plans still require one and Medicare needs a physician to certify your plan of care. Our front desk checks all of that, along with your benefits, before your first visit. If you're on Medicare, the <a href="../insurance.html#medicare-guide">2026 Medicare guide</a> on our insurance page explains deductibles and coinsurance.</p>
<p>If your back has been running your mornings for a while, call <strong>561-624-4263</strong> to book an evaluation, or <a href="../contact.html">request an appointment online</a>. We're at 733 US Highway 1, Suite 2A in North Palm Beach, open Monday to Friday 8:00 AM to 5:30 PM and Saturday 8:00 AM to 12:30 PM.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "why-hand-therapy-is-different": {
        "title": "Why Hand Therapy Is Its Own Specialty",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "June 2026",
        "tag": "Hand Therapy",
        "teaser": "Twenty-seven bones, over thirty muscles, and the finest motor control in the human body — here's why your hand deserves a certified specialist.",
        "body": """
<p>When people hear we have a Certified Hand Therapist on staff, they often ask whether that's simply physical therapy for a smaller body part. Fair question. The answer is no, and the difference matters a great deal for how your hand recovers, especially after surgery. Below is what sets hand therapy apart and what it looks like at our North Palm Beach clinic, plus when to ask for it by name.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>The hand is a precision instrument</h2>
<p>Your hand and wrist pack dozens of small structures into a very tight space: tendons gliding through narrow tunnels, small joints that have to line up just so, and nerves responsible for the finest motor control in your body. A little scar tissue in the wrong place can mean the difference between a full grip and one that never quite closes. Rehabilitation at that scale needs specialized training.</p>
<h3>&ldquo;Our original tool&rdquo;</h3>
<p>Dr. Matt Butler, MD, a fellowship-trained hand and upper extremity orthopedic surgeon with HSS, joined Dave and Mike on <a href="../podcast.html">Pain 2 Power</a> Episode 16 and described his job about as simply as anyone could. &ldquo;I take care of people's arms,&rdquo; he said, mostly the elbow, wrist and hand. When the talk turned to what drew him to the hand in the first place, he named the intricacy, and then this: &ldquo;That's how we all interact with our environment&hellip; something that people take for granted until it starts bothering them.&rdquo;</p>
<p>A minute later he called the hand &ldquo;our original tool,&rdquo; the one we use for working, for art, for everything in between. Think about your own morning. Keys, buttons, a coffee mug, a steering wheel on US-1, the phone you check all morning. You don't notice any of it until one of those things starts to hurt.</p>
<h3>Who ends up needing it</h3>
<p>Pretty much everyone, eventually. Dr. Butler listed the people who come through his door: &ldquo;elderly people with degenerative hand problems, workers that injured their hands at work, artists that have repetitive stress injuries.&rdquo; In the Palm Beaches you can add golfers with sore thumbs, pickleball players with cranky elbows, and the gardener who can't open a jar anymore and is quietly annoyed about it.</p>
<h2>What &ldquo;CHT&rdquo; actually means</h2>
<p>A <a href="../glossary.html#cht">Certified Hand Therapist</a> is an occupational or physical therapist who has completed years of hands-on hand and upper extremity practice and then passed a national certification exam. It's one of the most demanding credentials in rehabilitation, and it exists because hand recovery is unforgiving. Move too soon and you can compromise a surgical repair. Move too late and you lose motion to stiffness.</p>
<p>That's why hand surgeons tend to refer their post-operative patients to a CHT specifically, rather than to general rehab. They want someone who knows the anatomy they just repaired and the healing timeline it's on.</p>
<h3>Who leads ours</h3>
<p>Our hand therapy program is led by Laura Drumm, MS, OTR/L, CHT, CLT. She's an occupational therapist by training and a certified hand therapist, and she's also a certified lymphedema therapist, and swelling after hand surgery is on the list of things the program treats. Laura's work covers everything from custom splinting to post-operative tendon protocols, and patients travel to us for it from across the county, including <a href="../locations/west-palm-beach.html">West Palm Beach</a> and <a href="../locations/palm-beach.html">Palm Beach</a>.</p>
<p>It fits the rest of the clinic, too. Our founder, Dr. Dave Kashuba, Ph.D., OTR, is himself an occupational therapist and has been treating patients since 1991, and our <a href="../services/occupational-therapy.html">occupational therapy</a> program runs in the same building. So if your hand problem is getting in the way of dressing, cooking or work, those daily tasks can be worked on alongside the hand itself. (If you've ever wondered where PT ends and OT begins, we wrote about <a href="../blog/physical-therapy-vs-occupational-therapy.html">the difference between physical and occupational therapy</a>.)</p>
<h2>Custom splinting, made in-clinic</h2>
<p>One of the most visible differences is the splint. In clinical language it's an <a href="../glossary.html#orthosis">orthosis</a>: a support that protects or positions a hand, wrist or finger while it heals. Splints can be custom or ready-made. Our hand therapy program fabricates custom splints right here in the clinic.</p>
<p>Each one is molded to your hand for your specific condition. It holds the healing structures at the angle that stage of recovery calls for, and it gets adjusted as healing progresses rather than worn unchanged until the next appointment. When you're recovering from surgery, it's built to your surgeon's protocol. For carpal tunnel, a custom night splint that keeps the wrist in a neutral position while you sleep is often part of the plan. For an arthritic thumb, it might be a supportive splint you wear during the activities that flare it.</p>
<p>Coverage for custom splints varies by plan, so our front desk checks what yours covers before you come in. It's a quick phone call that saves a surprise later.</p>
<h2>Timing is everything</h2>
<p>After a tendon repair or a fracture, tissue healing follows a biological timeline, and the calendar on your fridge doesn't get a vote. Protocol-driven hand therapy walks that line, in coordination with your surgeon.</p>
<h3>After a tendon repair</h3>
<p>Repaired tendons heal on a strict schedule and the margin for error is small. Post-operative timelines vary widely by procedure: some repairs begin protected motion within days, while others need a period of immobilization first. We work from your surgeon's protocol, fabricate any splint to it, and stage motion and strengthening to the tissue. That's also why we'd love to hear from you before your operation, or just after it, so your plan and any splint you need are ready on schedule.</p>
<h3>After the cast comes off</h3>
<p>The bone healing and the hand working again are two different problems, and the second one is usually why they end up with us. Stiffness, swelling and lost grip are the real obstacles once the cast is off. Expect the early work to be about motion and swelling before it's about strength, with the pace set by what's healing rather than by a fixed number of weeks.</p>
<h2>What hand therapy treats, and how</h2>
<p>Most people arrive with a symptom, not a diagnosis: numbness that wakes them at night, a thumb that hurts every time they pinch, a finger that catches. The evaluation sorts that out. Here's roughly what care looks like for the conditions we see most.</p>
<div class="data-table" tabindex="0" role="region" aria-label="What hand therapy usually involves for common conditions">
<table>
<caption>Summarized from our hand therapy service page, our hand and wrist page and the hand therapy section of our FAQ. Your own plan comes from your evaluation.</caption>
<thead><tr><th scope="col">Condition</th><th scope="col">What care usually involves</th></tr></thead>
<tbody>
<tr><th scope="row">Carpal tunnel syndrome</th><td>Custom night splint, nerve and tendon gliding exercises, workstation and activity changes; a surgical consult recommended plainly if it's needed</td></tr>
<tr><th scope="row">Arthritis of the hand and thumb</th><td>Joint protection technique, targeted strengthening, a custom supportive splint and smarter ways to do the tasks that hurt</td></tr>
<tr><th scope="row">Tendon injuries and repairs</th><td>Surgeon's protocol, a splint built to it, then motion and strengthening staged to the healing tissue</td></tr>
<tr><th scope="row">Hand and wrist fractures</th><td>Protect what's still healing, restore motion gradually, then rebuild strength and dexterity for work and daily life</td></tr>
<tr><th scope="row">Trigger finger and nerve conditions</th><td>Splinting, graded motion and activity changes, conservatively or after surgery</td></tr>
<tr><th scope="row">Tennis elbow and the forearm</th><td>The whole upper extremity is in scope: hand, wrist, forearm and elbow</td></tr>
<tr><th scope="row">Swelling and stiffness after surgery</th><td>Treated as part of the plan from the start, rather than something to wait out</td></tr>
</tbody>
</table>
</div>
<h3>The elbow counts too</h3>
<p>Your arm works as one connected chain, so a certified hand therapist's scope runs from the fingertips to the elbow. Tennis elbow is the classic example. Dr. Butler described it as almost a rite of passage in middle age: the tendon that anchors the forearm muscles to the bone starts to fray, and most people who get it have never played tennis. Most cases settle down. The ones that land in his office first, he said, usually get sent to Dave, and he puts Dave's success rate at about nine out of ten. Dave was just as complimentary in the other direction: &ldquo;he'll do whatever it takes to keep you from having to do surgery.&rdquo;</p>
<p>Dave walked through what that looks like on his side: active release technique, blood flow restriction training, and dynamic cupping, sometimes with an actual sink plunger. (Yes, really. You'll see one in our office.) Mike was the test case, since Dave had treated his elbow before the show. &ldquo;I've had like zero pain since you did it,&rdquo; Mike said. &ldquo;I forgot that even happened.&rdquo; For the stubborn cases that don't respond to therapy, Dr. Butler described cleaning out the worn tendon and adding a collagen patch originally developed for the shoulder.</p>
<h3>Thumb arthritis</h3>
<p>This is the topic Dave booked Dr. Butler to talk about. Pain at the base of the thumb that flares with pinching, opening and twisting is common, and Dr. Butler said basal thumb arthritis develops in almost every woman and many men. Conservative hand therapy is one of the most effective options for it. When surgery does become the answer, he explained that the standard operation removes a small wrist bone called the trapezium and is followed by six to eight weeks immobilized and months of rehab, and that pinch strength never fully returns. He now also offers a thumb joint replacement, built like a dual mobility hip, which he said has been used in Europe for about fifteen years and was newly FDA cleared. Which route is right for you is a conversation for you and your surgeon. Either way, the hand that comes out the other side needs rehab.</p>
<h2>Surgeons and therapists, working hand in hand</h2>
<p>We don't diagnose, and we don't do surgery. Surgeons operate; we rehabilitate. What makes a hand recovery go well is how closely those two halves talk to each other.</p>
<p>That relationship has been a theme on the show since the beginning. Back in Episode 2, hand and upper extremity surgeon Dr. Tom Saylor, M.D., talked through the surgical side of restoring hand function, from carpal tunnel and tendon repairs to complex reconstruction. Dr. Butler and Dave send patients back and forth today. When a patient's evaluation here suggests they need a surgical opinion, we say so plainly and coordinate with their physician rather than keep them in therapy. When a patient comes from surgery, we work from the surgeon's protocol and stay in touch with their office.</p>
<p>If you've got hand surgery coming up, here's what helps us have everything ready:</p>
<ul>
<li>Your surgeon's name and the procedure, ideally before the operation</li>
<li>The referral and protocol from the surgeon's office</li>
<li>Every insurance card you carry, so we can sort out which pays first</li>
<li>The two or three everyday tasks you most want back, from buttoning a shirt to gripping a golf club</li>
</ul>
<h2>How to get started</h2>
<p>Whether you need a referral depends on your insurance plan. Post-surgical patients typically arrive with a referral and protocol from their surgeon already. If you're coming on your own for something like carpal tunnel or arthritis, call and our front desk will check whether your plan requires a referral and help arrange one if it does. Hand therapy is covered like other medically necessary therapy under Medicare and most major plans we accept, and we verify your specific benefits, including any rules about custom splints, before your first visit.</p>
<p>That first visit runs about an hour, one-on-one, and treatment usually begins the same day. The <a href="../faq.html#hand-therapy">hand therapy section of our FAQ</a> covers recovery times and coverage in more detail, and our <a href="../treatments/hand-wrist.html">hand and wrist pain page</a> walks through the most common symptoms.</p>
<p>If you're facing hand surgery or dealing with carpal tunnel or arthritis in your thumbs, ask to see our <a href="../services/hand-therapy.html">certified hand therapist</a>. Call First Rehabilitation of North Palm Beach at <strong>561-624-4263</strong> to book an evaluation, or <a href="../contact.html">request an appointment online</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "knee-arthritis-before-surgery": {
        "title": "Knee Pain: What to Try Before You Think About Surgery",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "July 2026",
        "iso": "2026-07-20",
        "tag": "Knees &amp; Joints",
        "teaser": "An orthopedic surgeon joined our Pain 2 Power podcast to talk knees: what causes the pain, the home exercises that help, and why surgery comes last.",
        "body": """
<p>If your knees ache on stairs, swell after a walk, or make you think twice about kneeling in the garden, you're in familiar company. Knee pain is one of the most common reasons people walk through our doors. On Episode 6 of our <a href="../podcast.html">Pain 2 Power radio show</a>, Dr. Dave Kashuba sat down with Dr. Richard Weiner, M.D., an orthopedic surgeon he has worked alongside since 1990, to talk about what actually helps a painful knee, and why the operating room is the last stop rather than the first.</p>
<p>This is the long version of that conversation, written down for anyone who has been told their knee is "getting there" and wants to know what to do in the meantime.</p>
<p><em>By The First Rehabilitation Team · Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>What's usually behind knee pain</h2>
<p>Three culprits come up again and again. The most common is osteoarthritis, a gradual wearing of the joint that Dr. Kashuba notes he sometimes sees in patients as young as their mid-thirties, while some ninety-year-olds have none at all. The other two are ligament injuries (a ligament connects bone to bone) and tendon problems such as tendonitis (a tendon connects muscle to bone).</p>
<p>Which one you're dealing with changes the plan completely, which is why both doctors kept returning to the same theme: a careful evaluation comes first. As Dr. Weiner put it, "you don't treat an X-ray, you treat the patient."</p>
<h3>Why the X-ray line matters</h3>
<p>Plenty of people come in clutching an imaging report that sounds alarming. "Bone on bone." "Severe degenerative change." Yet you might walk the Juno Beach pier without much trouble and only feel it on the stairs at home. Someone else can have a report that sounds mild and barely get out of a car. The picture and the person don't always match, and Dr. Weiner's point was that you treat the one in front of you. That means asking what hurts, when, and what it stops you doing, then watching you move.</p>
<p>His test for when to get help is a good one because it has nothing to do with a pain score. You seek help, he said, "when your symptoms interfere with ADLs, which means activities of daily living." Can you carry the groceries in from the car? Get up off a low couch? Make it around the course? Those answers tell us more than a number from one to ten.</p>
<h2>Knee arthritis treatment before surgery: the surgeon's own ladder</h2>
<p>Dr. Weiner spent most of a radio hour on how to keep people out of his operating room. "Surgery is the last resort," Dr. Weiner said. "The first thing is conservative treatment." He described the ladder he climbs with his own patients, one rung at a time, and noted that the vast majority of the knee patients he treats never need an operation at all.</p>
<h3>Rung one: stop aggravating it</h3>
<p>The first step is the least glamorous. Figure out what flares the knee and do less of it, or do it differently. That might mean shorter walks on softer ground for a while, swapping deep squats in the garden for a kneeling pad and a stool, or giving the third pickleball game of the morning a rest. You keep doing the things you love, with the pressure taken off long enough for the next rung to work.</p>
<h3>Rung two: therapy</h3>
<p>Then therapy, and he was blunt about why it sits so high: "physical therapy is key because you need to have strong muscles to stabilize the knee to have fewer symptoms." The knee is a hinge between two long bones. When the muscles around it are weak, the joint surfaces absorb what the muscles should have. Build those muscles back and the joint has less work to do.</p>
<h3>Rung three: medication, an injection, or a brace</h3>
<p>Next come medication or a targeted injection, and bracing. People often ask us whether they should get a knee injection or do physical therapy, as if it were one or the other. On Dr. Weiner's ladder, therapy comes first and an injection is a tool for later, when it's needed. Between pills and an injection for a single sore joint, he leans toward the injection, on the logic that you put the oil where it squeaks rather than exposing the whole body. Whether any of that is right for you is a conversation for your physician.</p>
<p>Surgery only enters the picture when all of that has been tried. If you're at that point, our post on <a href="partial-vs-total-knee-replacement.html">partial vs total knee replacement</a> covers the question most people forget to ask.</p>
<h2>What extra pounds do to a knee</h2>
<p>Citing studies, Dr. Weiner explained that each extra pound of body weight adds roughly five pounds of stress to the knee during activities like squatting and stair climbing. So losing ten pounds can take about fifty pounds of stress off each knee.</p>
<p>He listed excess weight among the main risk factors for knee arthritis, alongside genetics and past injuries. You can't change your parents, and you can't un-tear the meniscus you tore playing softball in 1987. Weight is the one on that list you have a hand on.</p>
<p>Those are encouraging numbers. Small changes buy your knees relief, and they stack with everything else in this post. A little less load plus a little more strength is a better deal for the joint than either one alone.</p>
<h2>Four simple exercises you can do at home</h2>
<p>Dr. Kashuba walked listeners through a short routine that needs nothing more than a sturdy chair and a low step stool. They're the same four that open the knee section of our <a href="../exercises.html#knee">home exercise library</a>. Move gently, stay within a comfortable range, and stop if anything sharpens the pain.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Dave's four home exercises for knee pain">
<table>
<caption>Dave's at-home knee set, as described on Pain 2 Power, Episode 6, and listed in our home exercise library.</caption>
<thead><tr><th scope="col">Exercise</th><th scope="col">How to do it</th><th scope="col">Dose</th><th scope="col">Why it helps</th></tr></thead>
<tbody>
<tr><th scope="row">Seated kick-outs</th><td>Sit at the front edge of a chair, slowly straighten one knee out in front of you, then lower it</td><td>3 sets of 10 each side, building to 3 sets of 20</td><td>Strengthens the quadriceps, including the muscle on the inside of the knee that tracks the kneecap</td></tr>
<tr><th scope="row">Standing knee curls</th><td>Hold the back of the chair, stand tall, bring one heel toward your seat as far as comfortable</td><td>3 sets of 10, building to 20</td><td>Works the hamstring through its range</td></tr>
<tr><th scope="row">Sit-to-stands with a pillow</th><td>Hold a light pillow out in front as you stand, and keep it reached forward as you sit back down</td><td>3 sets of 10</td><td>Makes you hinge at the hip, so the hip takes the load instead of the knee</td></tr>
<tr><th scope="row">Step-stool lean-ins</th><td>Hand on the chair, one foot on a low stool, rock your weight forward over that foot and back. No stepping up</td><td>Slow and controlled</td><td>Loads the knee through a small, safe range without impact</td></tr>
</tbody>
</table>
</div>
<p>A few notes from Dave that don't fit in a table. On the knee curls, do one leg at a time. His line on the show was that doing both at once is how you end up on the floor. On the sit-to-stands, the pillow is there for a reason. The joint that starts a movement takes the brunt of the load, and reaching forward makes the hips start it, which they handle far better than your knees do. On the lean-ins, resist the urge to turn it into a step-up. The point is a slow, controlled lean, repeated.</p>
<p>Round the routine out with regular walking, which both doctors recommended. And thinking has moved past strict rest: for a cranky knee, gentle movement plus elevation, ice, and light compression tends to serve you better than keeping it perfectly still.</p>
<h2>What knee arthritis therapy looks like at our North Palm Beach clinic</h2>
<p>A <a href="../services/physical-therapy.html">physical therapy</a> plan for a painful knee is built around strengthening the muscles that support the joint, including the hip and ankle, which share the load, so the knee itself has less work to do. You can read the outline on our <a href="../treatments/knee-pain.html">knee pain page</a>.</p>
<h3>The first hour</h3>
<p>Your first visit runs about an hour, one-on-one with a therapist. We take your history, watch you walk and climb a step, and measure how far the knee bends and straightens and how strong the muscles around it are. Treatment usually starts that day, with hands-on work for joint mobility and the first pieces of a <a href="../glossary.html#home-exercise-program">home exercise program</a>. You leave knowing what we found and what the plan is.</p>
<h3>Do you need a referral?</h3>
<p>Usually not to get started. Florida's <a href="../glossary.html#direct-access">direct access</a> law lets most people begin a physical therapy evaluation without a physician referral. Some insurance plans still want one for coverage, and Medicare needs a physician to certify your plan of care, so our front desk checks your benefits before your first visit and tells you what your plan requires. We see a lot of folks from up and down US-1, from <a href="../locations/juno-beach.html">Juno Beach</a> to Lake Park, and there's a free lot right at the building.</p>
<p>From there the work progresses to strength for the quadriceps, hips and glutes, and functional practice for stairs, walking distance, and whatever you came in wanting back, whether that's eighteen holes or getting down to the grandkids' level on the floor. When you finish, the wellness gym down the hall is there if you want to keep training with people who know your history. It's a separate program that doesn't take insurance, so ask the front desk how it works.</p>
<h2>When it's time to stop self-treating</h2>
<p>Home exercise has limits, and knowing them protects you. Get evaluated if your knee pain isn't settling, if swelling or warmth develops, if the knee gives way or locks up, or if symptoms start interfering with your everyday activities: walking, standing, sleeping.</p>
<p>One situation shouldn't wait. A pop followed by sudden pain and a leg you can't stand on is a day for an orthopedic specialist or the hospital.</p>
<p>The pattern both doctors agreed on: the sooner a problem is looked at, the easier it usually is to address. Waiting until the knee has stopped you golfing for a season just means more ground to make back up.</p>
<h2>If surgery does come up</h2>
<p>Sometimes the ladder runs out. If it does, you'll be better off for having climbed it, because you walk into the operation stronger and you walk out with a head start on rehab.</p>
<p>Keep two things in mind before that appointment. First, a total knee isn't the only operation on the table. Dr. Weiner made a strong case on air that many people who get a total could have had a partial, and the post on <a href="partial-vs-total-knee-replacement.html">partial vs total knee replacement</a> lays out his reasoning. Second, if your problem turns out to be a small, contained area of damaged cartilage rather than a worn-out joint, there's a different path again, covered in <a href="cartilage-transplant-knee-explained.html">our post on cartilage transplant knee recovery</a>.</p>
<p>Either way, the quadriceps you build now are the quadriceps you'll have after the operation. Nothing you do on this page is wasted if surgery does come.</p>
<h2>Start with an evaluation, not an operation</h2>
<p>Most knee pain responds to conservative care, and finding out where you stand costs you a phone call. Our therapists evaluate your knee, tell you honestly whether therapy is likely to help, and coordinate with your physician or an orthopedic specialist when you need one. Call us at <strong>561-624-4263</strong>, <a href="../contact.html">request an evaluation online</a>, browse the <a href="../faq.html#physical-therapy">physical therapy questions in our FAQ</a>, or hear the full conversation on the <a href="../podcast.html">Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "headaches-that-start-in-the-neck": {
        "title": "The Headache That Starts in Your Neck",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "July 2026",
        "iso": "2026-07-21",
        "tag": "Headaches &amp; Neck",
        "teaser": "Many stubborn, recurring headaches really start in the neck. Learn the signs, how physical therapy treats the driver, and when a headache needs a doctor first.",
        "body": """
<p>You know the headache before it fully arrives. It's the dull ache that creeps up from the base of your skull or settles behind one eye by mid-afternoon, then digs in for the rest of the day. You take something, it dulls the edge for a few hours, and by tomorrow the whole cycle starts over. That gets exhausting when the pills only ever seem to mask the problem instead of ending it. For many stubborn, recurring headaches, the source sits a few inches lower, in the neck.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>What &ldquo;the neck as a headache source&rdquo; actually means</h2>
<p>The upper part of your neck and the base of your skull share a crowded, sensitive neighborhood of joints, muscles and nerves. When the small joints at the very top of the spine get stiff, or the muscles that run from your shoulders up into the back of your head stay tight and overworked, the pain they produce doesn't always stay put. It can be felt as head pain: across the forehead, around one eye, or wrapping the back of the skull. That's what clinicians mean by referred pain. The trouble is in the neck, but you feel it up top.</p>
<h3>Cervicogenic headache</h3>
<p>A cervicogenic headache is one driven directly by the neck's joints and tissues. It's often felt on one side, and it often comes paired with a stiff, cranky neck that you may have stopped noticing because it's been that way for months.</p>
<h3>Tension-type headache</h3>
<p>A tension-type headache tends to feel like a band of pressure around the head, and it frequently rides along with the same tight muscles and locked-up posture. In real life the two blur together. Plenty of people have a bit of both.</p>
<h3>The everyday cause: sustained position</h3>
<p>The usual culprit for either one is boringly ordinary: hours on a phone or a workday hunched toward a screen, or a long drive with your head pushed forward. Each one asks the upper neck to hold a load it was never built to hold all day. The joints stiffen and the muscles guard, and then the head pain follows.</p>
<p>Dr. Dave Kashuba, Ph.D., OTR, our founder, described the slow version of this on Episode 8 of our <a href="../podcast.html">Pain 2 Power</a> show: &ldquo;as we get older, the tendency for us to have forward positioning, even the head forward positioning&hellip; that's just gravity, that's how life is.&rdquo; Gravity you can't do much about. How long you sit still in front of it is a different story.</p>
<h2>Signs your headache might be neck-driven</h2>
<p>No article can diagnose you, so treat these patterns as clues for a professional to evaluate. A headache is more likely to have a neck component when it tends to start at the base of the skull or on one side, rather than deep in the center of the head. It often builds through the day instead of hitting all at once, and it tends to get worse after a long stretch at a desk or after a drive.</p>
<p>Another telling pattern is what changes it. Neck-driven headaches frequently ease when you change position or stand up and move, and they flare again when you settle back into the same posture. They often travel with a companion, too: tightness or soreness through the neck and shoulders. If several of these sound familiar, that's a reason to get looked at.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Headache patterns that can point toward the neck">
<table>
<caption>Patterns that can point toward a neck component, drawn from this article and our headache and neck pain pages. They're clues for an evaluation, not a diagnosis.</caption>
<thead><tr><th scope="col">What you notice</th><th scope="col">Why it's worth mentioning at your evaluation</th></tr></thead>
<tbody>
<tr><th scope="row">Starts at the base of the skull, or on one side</th><td>Neck-driven headaches tend to start there rather than deep in the center of the head</td></tr>
<tr><th scope="row">Builds through the afternoon</th><td>Points toward a load that accumulates, like hours in one position</td></tr>
<tr><th scope="row">Worse after the desk or a long drive</th><td>Sustained forward-head posture is the everyday driver</td></tr>
<tr><th scope="row">Eases when you stand up and move</th><td>Changing position takes load off the upper neck</td></tr>
<tr><th scope="row">Comes with a stiff neck or sore shoulders</th><td>The muscles running from the shoulders into the back of the head are shared territory</td></tr>
<tr><th scope="row">Started after whiplash or a concussion</th><td>Headaches after either one are among the conditions our headache care covers, once a physician has cleared you</td></tr>
</tbody>
</table>
</div>
<h2>Where the neck and the headache meet in daily life</h2>
<p>When we sit down with a headache patient, a lot of the detective work is about the day they actually live, because that's where the load comes from.</p>
<h3>At the desk</h3>
<p>Laptop low, screen off to one side, phone wedged between ear and shoulder for a call. Any of those, held for an afternoon, keeps the upper neck working overtime. Part of our care is workstation coaching: where the screen sits, how you sit, and how often you get up. Nothing fancy. It just has to match how you work.</p>
<h3>Behind the wheel, and after a crash</h3>
<p>A long drive down I-95 or US-1 with your chin pushed toward the windshield is a classic setup. A car accident is a different matter. Headaches after whiplash or a concussion are among the conditions our headache care covers, but a physician should see you first. In Florida that's also about coverage: personal injury protection pays for medical care only if initial care starts within 14 days of the crash, and physical therapy is follow-up care your physician refers you to. Our <a href="../treatments/auto-accident.html">car accident rehab page</a> explains the rule.</p>
<h3>In bed</h3>
<p>Sleep position counts too. Some people wake up with the headache already on board, which tells us something about the night. Sleep-position coaching is part of how we treat neck pain, and the same conversation applies here. So does the jaw: jaw and postural contributions to head pain are on the list of things we look at.</p>
<h2>What physical therapy actually does about it</h2>
<p>The point of therapy here is to treat the driver, rather than only quiet the symptom.</p>
<h3>It starts with listening</h3>
<p>Your first visit runs about an hour, one-on-one with your therapist, and treatment usually begins that day. Before anyone touches your neck, we take your history: when the headaches come, which side, what you were doing, what helps. Dave makes a point of this. What you tell us shapes the whole assessment, and on Episode 9 he said people don't realize how important it is &ldquo;to have your therapist take really good notes and listen.&rdquo; Then we watch how your neck moves and measure motion, strength and the positions that bring the pain on. The <a href="../first-visit.html">first visit page</a> has the rest of the details.</p>
<h3>Hands-on work first</h3>
<p>Care usually starts with skilled <a href="../glossary.html#manual-therapy">manual therapy</a>. A therapist assesses the specific joints of the upper neck, finds the stiff or irritable ones, and uses gentle techniques to restore how they move, while releasing the muscles that have been guarding around them. That alone can take pressure off the structures that refer pain into the head.</p>
<h3>Then the reasons it keeps coming back</h3>
<p>Lasting change usually depends on the next step: addressing why the tension keeps rebuilding. That means working on the posture and strength gaps that let your head drift forward and your neck do all the work. Expect strengthening for the deep neck flexors and the upper back, opening up the mid-back and shoulders, and adjustments to how you sit, drive and hold your phone. Most neck programs borrow from the same small set of exercises.</p>
<div class="data-table" tabindex="0" role="region" aria-label="Posture exercises from our home exercise library">
<table>
<caption>From our home exercise library: exercises Dr. Dave Kashuba, Ph.D., OTR, described on Pain 2 Power Episode 8. Start them after your evaluation, not instead of one.</caption>
<thead><tr><th scope="col">Exercise</th><th scope="col">How</th><th scope="col">Dose</th></tr></thead>
<tbody>
<tr><th scope="row">Scapular retractions</th><td>Draw both shoulders back as if to touch your shoulder blades together</td><td>3 sets of 10</td></tr>
<tr><th scope="row">Shoulder shrugs</th><td>Bring both shoulders straight up toward your ears, then let them down</td><td>3 sets of 10</td></tr>
<tr><th scope="row">Walk</th><td>Get up and walk; start at three minutes a day if that's where you are</td><td>Daily, working up toward 10 or 15 minutes</td></tr>
<tr><th scope="row">Put the phone down</th><td>Set it aside and stand up</td><td>As often as you notice</td></tr>
<tr><th scope="row">Stretch before you start the day</th><td>A few easy stretches before the coffee and the commute</td><td>Every morning</td></tr>
</tbody>
</table>
</div>
<p>Full instructions are on our <a href="../exercises.html#shoulder">home exercises page</a>. Scapular retractions and shrugs work directly against the rounded, forward posture daily life builds in, which is why they show up in so many neck programs here.</p>
<h2>What you can do between visits</h2>
<p>Therapy visits are a few hours a week. Your neck lives with you for the other hundred and sixty-odd. On Episode 13, Dave said he sees people two to three times a week, and the rest of the time they need to be doing their exercises, and doing them correctly. If ten repetitions are prescribed, fifty is not a bonus.</p>
<p>He's also got a favorite observation about mornings. Babies stretch when they wake up, and so do dogs and cats, before they do anything at all. Most of us grab our glasses and a coffee and head straight for the desk or the car, then wonder why the neck is stiff by lunchtime. We wrote more about that first hour of the day in <a href="../blog/five-morning-habits-back-pain.html">five morning habits for back pain</a>, and most of it applies to necks too.</p>
<p>One more thing that helps us help you. Before your evaluation, jot down a week of notes on your headaches:</p>
<ul>
<li>What time each one started, and where you felt it first</li>
<li>Which side, and whether it was the same side every time</li>
<li>What you'd been doing for the hour before (desk, drive, phone, sleep)</li>
<li>What eased it, and what made it worse</li>
<li>Any medication you took for it</li>
</ul>
<p>That's the history Dave was talking about, written down while it's fresh. It makes the first visit sharper.</p>
<h2>When a headache needs a doctor first</h2>
<p>Physical therapy is a strong option for headaches that come from the neck, but not every headache belongs in that category, and some need medical care right away. A sudden, severe headache that feels like the worst of your life is an emergency and calls for urgent evaluation, not a therapy appointment. So does a headache that arrives with fever, confusion, vision loss, weakness, numbness, or trouble speaking, or one that follows a significant blow to the head.</p>
<p>If a headache is new, changing in a way that worries you, or simply different from your usual pattern, the responsible first move is to be checked by a physician. Getting the serious causes ruled out first is what makes it safe to then treat the mechanical, neck-driven piece with confidence. And if we see something during your evaluation that belongs with a doctor, we'll tell you so.</p>
<h2>Finding out what's behind yours</h2>
<p>If your headaches keep circling back and the medicine only ever buys you a few hours, find out whether your neck is part of the story. A thorough evaluation can tell us what's driving your pain and whether hands-on care, posture work and a simple home plan are likely to help. Most of our neck pain patients notice meaningful change within the first few weeks of consistent care. You can read more on our <a href="../treatments/headache-relief.html">headache treatment page</a>, and because the neck is so often the engine of the problem, on how we treat <a href="../treatments/neck-pain.html">neck pain</a>. Both live under our broader <a href="../services/physical-therapy.html">physical therapy</a> services.</p>
<p>In most cases Florida's direct access law lets you start a physical therapy evaluation without a physician referral; Medicare does require a physician to certify your plan of care, and our front desk verifies your benefits before your first visit. Our family has cared for this community since 1991, and our people make the difference. Call First Rehabilitation of North Palm Beach at <strong>561-624-4263</strong> to book an evaluation, or <a href="../contact.html">request an appointment online</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
    "cartilage-transplant-knee-explained": {
        "title": "Cartilage Transplants: Rebuilding a Knee Instead of Replacing It",
        "updated": "2026-10-14",   # deepened to the 1,700-word standard
        "date": "July 2026",
        "iso": "2026-07-28",
        "tag": "Knees &amp; Joints",
        "teaser": "A sports medicine surgeon explains cartilage transplants on our Pain 2 Power podcast: who they help, what recovery looks like, and why rehab decides it.",
        "body": """
<p>Most people hear two options for a worn-out knee: live with it, or replace the whole joint. On Episode 7 of our <a href="../podcast.html">Pain 2 Power radio show</a>, Dr. Dave Kashuba and Mike McGann sat down with Dr. Rami Elkhechen, M.D., a fellowship-trained sports medicine orthopedic surgeon now with NYU Langone Health, to talk about a third path. The goal there is to rebuild the cartilage you were born with rather than swap the joint for metal and plastic.</p>
<p>It's a narrower path than the other two, and it only suits certain knees. But if yours is one of them, you should know about it before anyone hands you a surgery date, and know how much of the result depends on the months of rehab that follow.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Why cartilage is the part to protect</h2>
<p>Dr. Elkhechen trained at NYU School of Medicine, did his sports medicine fellowship at the Ochsner Sports Medicine Institute in New Orleans, and spent time as an assistant team physician for the Saints and the Pelicans. Cartilage preservation is one of his focus areas, and he uses an analogy that sticks. Cartilage, he says, is "the gold in a vault at a bank." The ligaments, tendons, and meniscus around it are the security system, the guards and the alarm. They matter enormously, but they exist to protect the gold. "Once the cartilage is gone," he explained, "the supporting structures become secondary."</p>
<p>Dave raised the problem directly on the show: cartilage has no nerve endings. You can wear it down for years without feeling a thing, which is why so many people don't arrive until the problem is already advanced. As Dave put it, by the time someone shows up with pain, the trouble has often reached the bone underneath.</p>
<p>So the joint surface you most want to protect is also the one that gives you the least warning. That's an odd setup. It's also the reason the rest of this post spends so much time on the indirect clues.</p>
<h2>The signs to get checked</h2>
<p>Because cartilage itself can't hurt, the early clues are indirect. Dr. Elkhechen pointed to two in particular. The first is swelling inside the joint, a build-up of fluid that seems to come from nowhere. You didn't fall, you didn't twist it, and yet the knee looks puffy after a morning on the tennis court. The second is simpler: you can't do your normal activity anymore. If you're active and something you enjoy has become off-limits, that's reason enough to have it looked at.</p>
<p>After a specific tweak or twist, his advice was measured. Give it a few days of rest, ice, and anti-inflammatories. If the pain settles, you likely don't need an office visit. If it lingers, that's when to come in.</p>
<p>His broader point was about timing. Get evaluated early, because even if there's nothing to do yet, it can be monitored so the window for treatment doesn't quietly close. That window is the whole game with cartilage, as the next section explains.</p>
<h2>Who is a candidate for a cartilage transplant?</h2>
<p>Before any of this, Dr. Elkhechen was emphatic about the order of operations. It starts with X-rays and a hands-on physical exam, often an MRI, and then non-operative treatment. "We tend to try non-operative treatment as often and as much as we can before we indicate any patients for any type of surgical management," he said, adding that conservative care is frequently successful on its own.</p>
<h3>Small and contained, or worn all over?</h3>
<p>The single biggest factor is the shape of the damage. Transplants are for small, focal areas of damage: a contained spot, with healthy cartilage around it. A contained lesion is far more treatable than widespread, end-stage arthritis.</p>
<p>That distinction is also how these three knee topics on our blog sort themselves out. If your knee is wearing generally, the right starting point is <a href="knee-arthritis-before-surgery.html">knee arthritis treatment before surgery</a>, the conservative ladder an orthopedic surgeon described on Episode 6. If the wear has gone far enough that replacement is on the table, read <a href="partial-vs-total-knee-replacement.html">partial vs total knee replacement</a> before you choose. A transplant sits in its own lane: one defined spot, in a knee that is otherwise holding up.</p>
<h3>Age, health, and insurance</h3>
<p>Beyond the shape of the damage, candidates are generally people up to about age 55, sometimes 60 in good health, subject to insurance approval. Mike pointed out the difference: a knee replacement is a successful operation, but the joint always feels somewhat different afterward. A transplant aims to restore your own anatomy.</p>
<p>For a lot of active people around the Palm Beaches, the forty-something who runs along A1A before work or the fifty-something with a standing doubles game, that difference is the whole reason to ask.</p>
<h2>How the two-stage transplant works</h2>
<p>When a transplant is the right call, it happens in two stages, with a lab in between. Here's the sequence as Dr. Elkhechen laid it out.</p>
<div class="data-table" tabindex="0" role="region" aria-label="The cartilage transplant sequence as Dr. Rami Elkhechen described it">
<table>
<caption>The path to a cartilage transplant, as Dr. Rami Elkhechen, M.D. described it on Pain 2 Power, Episode 7. Timing varies by surgeon, knee and insurer.</caption>
<thead><tr><th scope="col">Step</th><th scope="col">What happens</th><th scope="col">Timing he gave</th></tr></thead>
<tbody>
<tr><th scope="row">Workup</th><td>X-rays, a hands-on physical exam, often an MRI</td><td>Before anything else</td></tr>
<tr><th scope="row">Conservative care</td><td>Non-operative treatment, tried "as often and as much as we can"</td><td>Frequently successful on its own</td></tr>
<tr><th scope="row">Stage one</th><td>Outpatient scope with a small camera; if the damage fits, a "small Tic Tac sized" piece of cartilage is harvested from a part of the joint that doesn't need it</td><td>Can take around thirty minutes</td></tr>
<tr><th scope="row">The lab</th><td>Your own cells are grown on a scaffold</td><td>Roughly six weeks</td></tr>
<tr><th scope="row">Stage two</th><td>A more involved procedure implants the new cartilage into the damaged area</td><td>After the cells are ready</td></tr>
<tr><th scope="row">Recovery</th><td>Motion early; weight-bearing and impact held back</td><td>Depends on where the lesion is and how large</td></tr>
</tbody>
</table>
</div>
<p>Notice the six weeks in the middle. That gap is useful, because it's time you can spend getting stronger, which is where the prehab conversation further down comes in.</p>
<h2>Cartilage transplant knee recovery: rehab decides the outcome</h2>
<p>This is where the conversation came home for us. Surgery puts the new cells in place. What happens over the next few months decides whether they take.</p>
<h3>Motion early</h3>
<p>"Cartilage loves range of motion," Dr. Elkhechen said, and gentle motion begins almost immediately after surgery. That can surprise people who expect to be told to keep the leg still. Moving the joint carefully, within the limits your surgeon sets, is part of the treatment.</p>
<h3>Weight held back, on purpose</h3>
<p>Weight-bearing and high-impact activity are a different story. Those are held back deliberately so the new cells can take hold. Recovery timelines depend on where and how large the lesion is. Damage under the kneecap may allow weight-bearing almost right away with the knee held straight, while other areas typically take eight to twelve weeks to reach full weight-bearing.</p>
<p>That's a long time to be careful, and it's where people get into trouble. You feel fine at week five, the knee isn't sore, the weather is perfect, and the temptation to test it with a long walk on the beach is real. The cells don't know the weather is nice. Follow the protocol.</p>
<h3>What therapy is doing in the meantime</h3>
<p>The waiting period is spent on range of motion and on strengthening the muscles around the knee, the ones, in his words, "supporting that gold." That's exactly the <a href="../glossary.html#post-surgical-rehabilitation">post-surgical rehabilitation</a> our <a href="../services/physical-therapy.html">physical therapy</a> team does: we work from your surgeon's protocol, measure your <a href="../glossary.html#range-of-motion">range of motion</a> as it comes back, and progress strength in step with what the tissue is allowed to do. When the surgeon clears more weight, the focus shifts to walking well again, which is what <a href="../glossary.html#gait-training">gait training</a> means in plain English. You can read more about our approach on the <a href="../treatments/knee-pain.html">knee pain page</a>.</p>
<h2>Prehab: getting strong before the operation</h2>
<p>Dave asked about prehab, meaning rehabilitation before surgery, and Dr. Elkhechen does it routinely, especially with ACL patients, strengthening the quadriceps and hip abductors ahead of time. His reasoning applies well beyond one procedure: "The stronger your base is as you're coming in, in terms of strength and your activity level, you're probably going to come out the other side much better in terms of recovery."</p>
<p>For a transplant, the six-week lab window is a natural place for that work. Ask your surgeon whether prehab fits your plan, and if it does, bring us the details.</p>
<h3>Knowing the why</h3>
<p>He also said patients who understand their diagnosis and their therapy plan do better: "If they're not on board with treatment, that treatment is less likely to succeed." Knowing the what and the why changes results. It's why our therapists explain what they found at the first visit, and why we'd rather you ask the same question three times than nod along.</p>
<h2>What you can do to protect your knees now</h2>
<p>Asked what prevents this kind of damage in the first place, Dave pointed to the knee's stabilizers, particularly the vastus medialis (the VMO) on the inner knee, which helps track the kneecap. His guidance was to strengthen the whole quadriceps and work the muscles both above and below the joint, including the glutes and calves.</p>
<p>One exercise he shared on air: lie on your back with your knees comfortably bent and both feet flat on the floor or bed. Lift your hips upward, pause at the top, and squeeze the glute muscles, three sets of ten. Move gently, stay within a comfortable range, and stop if anything sharpens the pain.</p>
<p>That bridge sits at the end of the knee section in our <a href="../exercises.html#knee">home exercise library</a>, next to the seated leg extensions that work the VMO. Dave pairs the two rather than doing either alone, because the knee is carried from above and below.</p>
<h2>Start with an evaluation</h2>
<p>Whether your knee needs surgery, prehab, or simply a smarter strengthening plan, the honest answer starts with someone looking at it. Our therapists evaluate your knee, tell you plainly whether therapy is likely to help, and coordinate with your physician or an orthopedic specialist when you need one. We see patients from North Palm Beach and up the coast through <a href="../locations/tequesta.html">Tequesta</a>.</p>
<p>Call First Rehabilitation of North Palm Beach at <strong>561-624-4263</strong>, <a href="../contact.html">request an appointment online</a>, or hear the full conversation on the <a href="../podcast.html">Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>
""",
    },
}

# Related reading, post -> post. Before this every blog post's only inbound link
# was its card on blog/index.html: no post linked to another, which left several
# posts with a single internal link (flagged by the Semrush crawl, 2026-08-23).
# Curated rather than tag-matched — the tags are per-topic ("Knees & Joints",
# "Pain 2 Power") and too narrow to pair posts usefully. Every post appears as a
# target at least once, so adding a post means adding it to somebody's list too.
# Unknown or missing slugs fall back to the next posts in BLOG_POSTS order.
RELATED_POSTS = {
    "pain-2-power-ep20-kendzierski": ["pain-2-power-ep17-goodwin", "pain-2-power-ep18-marrone-armstrong", "pain-2-power-ep19-cake"],
    "pain-2-power-ep18-marrone-armstrong": ["pain-2-power-ep20-kendzierski", "pain-2-power-ep17-goodwin", "strength-training-after-60-fall-prevention"],
    "pain-2-power-ep17-goodwin": ["pain-2-power-ep20-kendzierski", "pain-2-power-ep18-marrone-armstrong", "gym-program-after-physical-therapy-north-palm-beach"],
    "pain-2-power-ep14-arlosoroff": ["pain-2-power-ep12-leighton", "what-to-expect-first-pt-visit", "pain-2-power-ep10-mcvicker"],
    "pain-2-power-ep13-titheradge": ["pain-2-power-ep9-sabesan", "pain-2-power-ep19-cake", "reverse-shoulder-replacement-explained"],
    "pain-2-power-ep12-leighton": ["pain-2-power-ep10-mcvicker", "hip-impingement-back-pain-north-palm-beach", "pain-2-power-ep14-arlosoroff"],
    "pain-2-power-ep9-sabesan": ["reverse-shoulder-replacement-explained", "pain-2-power-ep13-titheradge", "pain-2-power-ep12-leighton"],
    "personal-training-with-a-therapist-who-knows-your-injury-history": ["gym-program-after-physical-therapy-north-palm-beach", "strength-training-after-60-fall-prevention", "pain-2-power-ep19-cake"],
    "pain-2-power-ep19-cake": ["personal-training-with-a-therapist-who-knows-your-injury-history", "headaches-that-start-in-the-neck", "pain-2-power-ep15-mann"],
    "strength-training-after-60-fall-prevention": ["gym-program-after-physical-therapy-north-palm-beach", "pain-2-power-ep11-joyce", "reverse-shoulder-replacement-explained"],
    "gym-program-after-physical-therapy-north-palm-beach": ["strength-training-after-60-fall-prevention", "personal-training-with-a-therapist-who-knows-your-injury-history", "reverse-shoulder-replacement-explained"],
    "pain-2-power-ep15-mann": ["post-stroke-occupational-therapy-north-palm-beach", "physical-therapy-vs-occupational-therapy", "pain-2-power-ep11-joyce"],
    "post-stroke-occupational-therapy-north-palm-beach": ["physical-therapy-vs-occupational-therapy", "pain-2-power-ep15-mann", "why-hand-therapy-is-different"],
    "pain-2-power-ep11-joyce": ["strength-training-after-60-fall-prevention", "pain-2-power-ep10-mcvicker", "pain-2-power-ep15-mann"],
    "partial-vs-total-knee-replacement": ["knee-arthritis-before-surgery", "cartilage-transplant-knee-explained", "what-to-expect-first-pt-visit"],
    "physical-therapy-vs-occupational-therapy": ["post-stroke-occupational-therapy-north-palm-beach", "why-hand-therapy-is-different", "what-to-expect-first-pt-visit"],
    "pain-2-power-ep10-mcvicker": ["hip-impingement-back-pain-north-palm-beach", "five-morning-habits-back-pain", "pain-2-power-ep11-joyce"],
    "hip-impingement-back-pain-north-palm-beach": ["pain-2-power-ep10-mcvicker", "five-morning-habits-back-pain", "what-to-expect-first-pt-visit"],
    "reverse-shoulder-replacement-explained": ["gym-program-after-physical-therapy-north-palm-beach", "partial-vs-total-knee-replacement", "what-to-expect-first-pt-visit"],
    "what-to-expect-first-pt-visit": ["physical-therapy-vs-occupational-therapy", "five-morning-habits-back-pain", "knee-arthritis-before-surgery"],
    "five-morning-habits-back-pain": ["hip-impingement-back-pain-north-palm-beach", "headaches-that-start-in-the-neck", "what-to-expect-first-pt-visit"],
    "why-hand-therapy-is-different": ["physical-therapy-vs-occupational-therapy", "what-to-expect-first-pt-visit", "reverse-shoulder-replacement-explained"],
    "knee-arthritis-before-surgery": ["partial-vs-total-knee-replacement", "cartilage-transplant-knee-explained", "pain-2-power-ep10-mcvicker"],
    "headaches-that-start-in-the-neck": ["five-morning-habits-back-pain", "pain-2-power-ep19-cake", "what-to-expect-first-pt-visit"],
    "cartilage-transplant-knee-explained": ["knee-arthritis-before-surgery", "partial-vs-total-knee-replacement", "reverse-shoulder-replacement-explained"],
}

def _related_block(slug):
    """Three-post 'Keep reading' grid for a blog post."""
    picks = [s for s in RELATED_POSTS.get(slug, []) if s in BLOG_POSTS and s != slug]
    if len(picks) < 3:                      # fall back to the next posts in order
        order = list(BLOG_POSTS)
        i = order.index(slug)
        for s in order[i + 1:] + order[:i]:
            if s not in picks and s != slug:
                picks.append(s)
            if len(picks) == 3:
                break
    picks = picks[:3]
    if not picks:
        return ""
    cards = "".join(
        f'''<a class="cond-card reveal" href="{s}.html" style="padding:1.7rem 1.5rem;">
        <span class="cond-tag">{BLOG_POSTS[s]["tag"]}</span>
        <h3 style="margin-top:0.4rem;font-size:1.15rem;">{BLOG_POSTS[s]["title"]}</h3>
        <p>{BLOG_POSTS[s]["teaser"]}</p>
        <p style="margin-top:0.9rem;font-weight:600;color:var(--ink);">Read article &rarr;</p>
        </a>''' for s in picks)
    return f'''<section class="section on-cream" style="padding-top:2.6rem;">
  <div class="wrap">
    <div class="section-head reveal" style="margin-bottom:1.4rem;">
      <span class="eyebrow">Keep Reading</span><h2>Related Articles</h2>
    </div>
    <div class="cond-grid" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.3rem;">{cards}</div>
  </div>
</section>'''

def build_blog():
    cards = "".join(
        f'''<a class="cond-card reveal" href="/blog/{slug}.html" style="padding:1.9rem 1.7rem;">
        <span class="cond-tag">{p["tag"]} &middot; {p["date"]}</span>
        <h3 style="margin-top:0.4rem;">{p["title"]}</h3>
        <p>{p["teaser"]}</p>
        <p style="margin-top:0.9rem;font-weight:600;color:var(--ink);">Read article &rarr;</p>
        </a>'''
        for slug, p in BLOG_POSTS.items()
    )
    crumbs = '<div class="crumbs"><a href="/">Home</a> / Blog</div>'
    body = f"""
<main>
{page_hero("From the Clinic", "Insights for a <em class='accent'>Stronger Life</em>",
  "Practical guidance from the First Rehabilitation team — recovery, movement, and living well in the Palm Beaches.", crumbs)}
<section class="section">
  <div class="wrap">
    <h2 class="sr-only">Latest Articles</h2>
    <div class="cond-grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.4rem;">{cards}</div>
  </div>
</section>
{cta_band(1)}
</main>
"""
    write("blog/index.html",
          head("PT & Recovery Tips Blog | First Rehab North Palm Beach",
               "Practical recovery and wellness guidance from the physical, occupational, and hand therapy team at First Rehabilitation of North Palm Beach.", depth=1, canonical="blog/index.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Blog", "blog/index.html")]))
          + nav(1) + body + footer(1))

    for slug, p in BLOG_POSTS.items():
        crumbs = f'<div class="crumbs"><a href="/">Home</a> / <a href="index.html">Blog</a> / {p["title"]}</div>'
        body = f"""
<main>
{page_hero(f'{p["tag"]} &middot; {p["date"]}', p["title"], p["teaser"], crumbs)}
<section class="section">
  <div class="wrap two-col">
    <article class="prose reveal">{p["body"]}</article>
    <aside class="side-card reveal d2">
      <h3>Talk to a therapist</h3>
      <p>Questions about your own recovery? Serving the Palm Beaches since 1991 — family-owned, 4.9★ on Google.</p>
      <a class="btn btn-coral" href="../contact.html">Book Appointment</a>
      <div class="side-meta">
        <p>Call us directly<br><a href="tel:+15616244263">{PHONE}</a></p>
      </div>
    </aside>
  </div>
</section>
{_related_block(slug)}
{appt_form(heading='Talk To Someone About This', sub='If any of this sounds like what you are dealing with, tell us and our front desk will call you back within one business day.')}
{cta_band(1)}
</main>
"""
        import json as _json
        from datetime import datetime as _dt
        seo_titles = {
            "pain-2-power-ep20-kendzierski": "Maria Kendzierski: Breast Cancer Survivor on Pain 2 Power",
            "pain-2-power-ep18-marrone-armstrong": "Elyse Marrone &amp; Danielle Armstrong: Breast Cancer Recovery",
            "pain-2-power-ep17-goodwin": "Dr. Don Goodwin on Mammograms, Dense Breasts and MRI",
            "pain-2-power-ep14-arlosoroff": "Dr. Chaim Arlosoroff on E-Bike Injuries in Kids",
            "pain-2-power-ep13-titheradge": "Captain Kerry Titheradge of Below Deck on Pain 2 Power",
            "pain-2-power-ep12-leighton": "Dr. Michael Leighton on Total Hip Replacement Surgery",
            "pain-2-power-ep9-sabesan": "Dr. Vani Sabesan: Why Rotator Cuff Repairs Struggle to Heal",
            "personal-training-with-a-therapist-who-knows-your-injury-history": "Personal Training With a Therapist Who Knows Your Injury",
            "pain-2-power-ep19-cake": "Shannon Cake on Pain 2 Power: Newsmax Anchor Interview",
            # Long-tail title tag so this post stops competing with the homepage for
            # "physical therapy North Palm Beach" (SEO-KEYWORDS.md rule 2). H1 unchanged.
            "physical-therapy-and-rehab-services-in-north-palm-beach-what-we-treat": "What Physical Therapy Treats, and Your First Visit",
            "strength-training-after-60-fall-prevention": "Strength Training After 60 in North Palm Beach",
            "gym-program-after-physical-therapy-north-palm-beach": "Gym Program After Physical Therapy | North Palm Beach",
            "pain-2-power-ep15-mann": "Susan Mann: Processing Disorders in Kids",
            "post-stroke-occupational-therapy-north-palm-beach": "Post Stroke Occupational Therapy North Palm Beach",
            "pain-2-power-ep11-joyce": "Paul Joyce: GLP-1s, Peptides and Muscle Loss",
            "partial-vs-total-knee-replacement": "Partial vs Total Knee Replacement",
            "physical-therapy-vs-occupational-therapy": "Physical Therapy vs Occupational Therapy",
            "pain-2-power-ep10-mcvicker": "Dr. Zach McVicker: Hip Pain vs Back Pain",
            "hip-impingement-back-pain-north-palm-beach": "Hip Impingement Treatment North Palm Beach",
            "what-to-expect-first-pt-visit": "Your First PT Visit: What to Expect",
            "five-morning-habits-back-pain": "Five Morning Habits That Ease Back Pain",
            "why-hand-therapy-is-different": "Why Hand Therapy Is Its Own Specialty",
            "knee-arthritis-before-surgery": "Knee Pain: What to Try Before Surgery",
            "headaches-that-start-in-the-neck": "Headache Treatment NPB: The Neck Link",
            "cartilage-transplant-knee-explained": "Cartilage Transplants vs. Knee Replacement",
            "reverse-shoulder-replacement-explained": "Reverse Shoulder Replacement Explained",
        }
        iso_date = p.get("iso") or _dt.strptime(p["date"], "%B %Y").strftime("%Y-%m")
        # reviewedBy is a property of WebPage, NOT of Article/BlogPosting. It used
        # to hang off the BlogPosting, which made validators (Semrush, 2026-08-23)
        # reject the whole item — an invalid item risks being dropped rather than
        # partially parsed. Medical-reviewer attribution is still exactly what we
        # want for E-E-A-T, so it moved to a WebPage node in the same @graph and
        # the BlogPosting points at that node via mainEntityOfPage. The Person is
        # defined in full on about.html; here it is referenced by @id only.
        page_url = f"https://www.firstrehabnpb.com/blog/{slug}.html"
        post_schema = '<script type="application/ld+json">' + _json.dumps({
            "@context": "https://schema.org",
            "@graph": [{
                "@type": "BlogPosting",
                "@id": page_url + "#article",
                "headline": _faq_plain(p["title"]),
                "description": _faq_plain(p["teaser"]),
                "datePublished": iso_date, "dateModified": p.get("updated") or iso_date,
                "image": "https://www.firstrehabnpb.com/assets/media/hero-poster.jpg",
                "author": {"@type": "Organization", "name": "First Rehabilitation of North Palm Beach"},
                "publisher": {"@type": "Organization", "name": "First Rehabilitation of North Palm Beach",
                              "logo": {"@type": "ImageObject", "url": "https://www.firstrehabnpb.com/assets/media/logo.png"}},
                "mainEntityOfPage": {"@id": page_url + "#webpage"},
            }, {
                "@type": "WebPage",
                "@id": page_url + "#webpage",
                "url": page_url,
                "publisher": {"@id": "https://www.firstrehabnpb.com/#organization"},
                "reviewedBy": {"@id": "https://www.firstrehabnpb.com/about.html#david-kashuba"},
                "lastReviewed": iso_date,
            }],
        }, ensure_ascii=False) + '</script>\n'
        post_bc = breadcrumb_schema([("Home", ""), ("Blog", "blog/index.html"), (p["title"], f"blog/{slug}.html")])
        write(f"blog/{slug}.html",
              head(f'{seo_titles.get(slug, p["title"])} | First Rehab Blog', p["teaser"].replace("&amp;","&"), depth=1, canonical=f"blog/{slug}.html", page_type="article",
                   extra_schema=post_schema + post_bc)
              + nav(1) + body + footer(1))

# ----------------------------------------------------------------------------
# SITEMAP / ROBOTS / 404
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# CAREERS
# ----------------------------------------------------------------------------
# Edit roles here — layout is automatic. Fields: title, type (display string),
# employment_type (list, schema.org values: FULL_TIME / PART_TIME / CONTRACTOR /
# OTHER), location, posted (YYYY-MM-DD; validThrough auto = +60 days), summary,
# responsibilities[], qualifications[], benefits[], linkedin (optional URL for an
# "Apply on LinkedIn" secondary button). Empty list = "no openings" message.

OPEN_POSITIONS = [
    {
        "title": "Certified Occupational Therapy Assistant (COTA)",
        "type": "Part-time (20–30 hrs/week), permanent, with benefits — can convert to full-time · On-site · Pay based on experience",
        "employment_type": ["PART_TIME"],
        "location": "North Palm Beach, FL 33408 (in person)",
        "posted": "2026-07-20",
        "summary": "Join our busy orthopedic therapy center as a Certified Occupational Therapy Assistant. Part-time to start (20–30 hrs/week) with benefits and a path to full-time. Pay based on experience.",
        "responsibilities": [
            "Implement treatment plans developed by our Occupational Therapists",
            "Lead therapeutic exercises and activities with patients",
            "Guide and support patients through therapy sessions",
            "Monitor and document patient progress and report changes to the supervising OT",
            "Collaborate with our multidisciplinary team",
            "Educate patients and families on at-home techniques",
            "Maintain accurate patient records",
        ],
        "qualifications": [
            "Occupational Therapy Assistant License (required)",
            "Previous COTA experience preferred",
            "Knowledge of anatomy, physiology, medical terminology, occupational health, and acute care",
            "Strong communication skills",
            "Team-oriented and organized",
            "Proficient with electronic medical records",
        ],
        "benefits": ["Flexible schedule", "Health/medical insurance", "Opportunities for advancement"],
        "linkedin": "",
    },
]

def build_careers():
    import json as _json
    from datetime import datetime as _dt, timedelta as _td

    why_cards = [
        ("Family-owned since 1991", "Independent and steady for more than three decades — no corporate churn, no revolving door. The founder still walks the floor."),
        ("39+ years, 180,000+ patients", "A busy, established practice with deep roots in the Palm Beaches — and the patient volume that keeps your skills sharp."),
        ("Real one-on-one care", "We're not a high-volume mill. You get the time to treat people properly — the reason most of us chose this field in the first place."),
        ("Mentorship from the founder", "Learn directly from Dr. Dave Kashuba, Ph.D., who personally trains and mentors clinicians who join the team."),
        ("A team patients know by name", "Read our 4.9★ Google reviews — patients call out our staff by name. That's the culture you'd be joining."),
        ("Four disciplines, one roof", "Physical therapy, occupational therapy, certified hand therapy, and wellness — variety in your caseload, colleagues to learn from."),
        ("Room to grow", "Opportunities for advancement as the practice grows, with part-time-to-full-time paths on select roles."),
        ("A clinic with a voice", "Our founder co-hosts the Pain 2 Power radio show Saturdays on 100.3 Legends Radio — we educate the community, not just treat it."),
        ("Rooted across the Palm Beaches", "Patients come to us from North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, and West Palm Beach — a reputation you'll be proud to represent."),
    ]
    why_html = "".join(
        f'<div class="cond-card reveal d{i%3+1}" style="padding:1.9rem 1.7rem;"><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(why_cards)
    )

    def _job_lists(r):
        out = ""
        for label, key in (("Responsibilities", "responsibilities"), ("Qualifications", "qualifications"), ("Benefits", "benefits")):
            items = r.get(key) or []
            if items:
                out += f'<h3>{label}</h3><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
        return out

    if OPEN_POSITIONS:
        jobs_html = "".join(f"""
      <details class="job reveal">
        <summary><span class="job-title">{r["title"]}</span><span class="job-meta">{r["type"]}</span></summary>
        <div class="job-body">
          <p>{r["summary"]}</p>
          {_job_lists(r)}
          <p class="job-loc">{r["location"]}</p>
          <p class="job-actions"><a class="btn btn-coral" href="#apply" data-role="{r["title"]}">Apply for this role <span class="arr">&rarr;</span></a>{f' <a class="btn btn-ink" href="{r["linkedin"]}" target="_blank" rel="noopener">Apply on LinkedIn</a>' if r.get("linkedin") else ''}</p>
        </div>
      </details>""" for r in OPEN_POSITIONS)
    else:
        jobs_html = '<p class="lede" style="text-align:center;">No current openings — but we\'re always glad to hear from great people. Send us your resume below and we\'ll keep you in mind.</p>'

    role_options = "".join(f'<option>{r["title"]}</option>' for r in OPEN_POSITIONS) + "<option>General / Future interest</option>"

    body = f"""
<main>
{page_hero("Join Our Team", "Grow <em class='accent'>With Us</em>",
  "A family-owned clinic where clinicians get real time with their patients, mentorship from the founder, and room to grow — serving the Palm Beaches since 1991.",
  '<div class="crumbs"><a href="/">Home</a> / Careers</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Why First Rehabilitation</span>
      <h2>Our People Make <em class="accent">the Difference</em></h2>
      <p class="lede">That's our tagline for patients — and it starts with how we treat the people who work here.</p>
    </div>
    <div class="cond-grid" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.4rem;">{why_html}</div>
  </div>
</section>
<section class="section on-cream" id="openings">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Open Positions</span>
      <h2>Where You Might <em class="accent">Fit In</em></h2>
    </div>
    <div class="job-list">{jobs_html}</div>
  </div>
</section>
<section class="section" id="apply">
  <div class="wrap" style="max-width:760px;">
    <div class="appt-form-card reveal">
      <h2 class="h3-size">Apply Now</h2>
      <p class="af-sub">Applications go straight to our leadership team. We read every one — and if there's no opening that fits today, we'll keep you in mind.</p>
      <form class="appt-form" id="careers-form" novalidate>
        <div class="af-field">
          <label for="cf-name">Full name *</label>
          <input id="cf-name" name="name" type="text" autocomplete="name" required maxlength="200">
        </div>
        <div class="af-two">
          <div class="af-field">
            <label for="cf-email">Email *</label>
            <input id="cf-email" name="email" type="email" autocomplete="email" required maxlength="200">
          </div>
          <div class="af-field">
            <label for="cf-phone">Phone</label>
            <input id="cf-phone" name="phone" type="tel" autocomplete="tel" maxlength="40" placeholder="561-555-1234">
          </div>
        </div>
        <div class="af-field">
          <label for="cf-position">Position *</label>
          <select id="cf-position" name="position" required>{role_options}</select>
        </div>
        <div class="af-field">
          <label for="cf-resume">Resume link</label>
          <input id="cf-resume" name="resume_url" type="url" maxlength="500" placeholder="Paste a Google Drive or Dropbox share link">
          <p class="af-note" style="margin-top:0.4rem;">Tip: in Google Drive or Dropbox, choose "Share &rarr; anyone with the link can view" and paste the link here.</p>
        </div>
        <div class="af-field">
          <label for="cf-message">Short message / cover note</label>
          <textarea id="cf-message" name="message" maxlength="3000" placeholder="Tell us a little about yourself&hellip;"></textarea>
        </div>
        <div class="cf-extra" aria-hidden="true"><label for="cf-website">Website</label><input id="cf-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <p class="af-note">Please include only the basics — no sensitive personal information. We only need enough to get back to you.</p>
        <p class="af-error" id="cf-error" role="alert"></p>
        <button class="btn btn-coral" type="submit">Send Application <span class="arr">&rarr;</span></button>
      </form>
      <div class="af-done" id="cf-done" hidden>
        <div class="af-check">&#10003;</div>
        <h3>Application received</h3>
        <p>Thank you for your interest in joining First Rehabilitation of North Palm Beach. We've emailed you a confirmation, and our team will be in touch.</p>
      </div>
    </div>
  </div>
</section>
{cta_band(0, heading='Do work that <em>actually matters.</em>', sub="Every day here ends with people moving better than they arrived. Come be part of that.")}
</main>
<script src="assets/js/careers.js?v={asset_v('assets/js/careers.js')}" defer></script>
"""

    org = {"@type": "Organization", "name": "First Rehabilitation of North Palm Beach",
           "sameAs": "https://www.firstrehabnpb.com/",
           "logo": "https://www.firstrehabnpb.com/assets/media/logo.png"}
    place = {"@type": "Place", "address": {"@type": "PostalAddress",
             "streetAddress": "733 US Highway 1, Suite 2A", "addressLocality": "North Palm Beach",
             "addressRegion": "FL", "postalCode": "33408", "addressCountry": "US"}}
    jobs_ld = ""
    for r in OPEN_POSITIONS:
        valid = (_dt.strptime(r["posted"], "%Y-%m-%d") + _td(days=60)).strftime("%Y-%m-%d")
        desc = r["summary"]
        for label, key in (("Responsibilities", "responsibilities"), ("Qualifications", "qualifications"), ("Benefits", "benefits")):
            if r.get(key):
                desc += f" {label}: " + "; ".join(r[key]) + "."
        jobs_ld += '<script type="application/ld+json">' + _json.dumps({
            "@context": "https://schema.org", "@type": "JobPosting",
            "title": r["title"], "description": desc,
            "datePosted": r["posted"], "validThrough": valid,
            "employmentType": r["employment_type"],
            "hiringOrganization": org, "jobLocation": place,
            "directApply": True,
        }, ensure_ascii=False) + '</script>\n'

    write("careers.html",
          head("Careers | First Rehabilitation of North Palm Beach",
               ("Now hiring: " + ", ".join(r["title"] for r in OPEN_POSITIONS) + ". Join a family-owned therapy clinic serving the Palm Beaches since 1991 — apply online.")
               if OPEN_POSITIONS else
               "Join a family-owned therapy clinic serving the Palm Beaches since 1991. No current openings, but we always welcome great people — send us your resume.",
               canonical="careers.html",
               extra_schema=jobs_ld + breadcrumb_schema([("Home", ""), ("Careers", "careers.html")]))
          + nav(0) + body + footer(0))

def build_first_visit():
    """Your First Visit — step-by-step what-to-expect page.
    SEO target: "what happens at physical therapy", "first physical therapy
    appointment", "what to expect physical therapy North Palm Beach".
    Content cross-links (not duplicates) the what-to-expect blog post."""
    import json as _json
    steps = [
        ("Before you come",
         '<p>Once your appointment is scheduled, we\'ll email you an intake form. Completing it ahead of time means your first visit starts on time — and starts with therapy, not paperwork.</p>'
         '<span class="fv-hint">Takes just a few minutes at home</span>'),
        ("What to bring",
         '<p>Three things: a photo ID, your insurance card, and your prescription or referral if your physician gave you one. Our front desk verifies your coverage before you arrive, so billing questions never ambush you.</p>'),
        ("Your evaluation",
         '<p>You\'ll spend about an hour one-on-one with one of our therapists. They\'ll listen to your story, watch how you move, measure strength and range of motion, and build a plan around your goals — whether that\'s golf, gardening, or picking up a grandchild.</p>'),
        ("You'll be treated the same day",
         '<p>Most people assume the first visit is only paperwork and evaluation. Not here.</p>'
         '<div class="fv-highlight"><strong>Treatment begins on day one.</strong> Most patients receive hands-on care at the very first visit — and leave already knowing what\'s going on, what the plan is, and what to do between visits.</div>'),
        ("Before you leave",
         '<p>Your follow-up visits are scheduled before you walk out the door, so your recovery has a rhythm from day one. You\'ll leave with your plan, your home exercises, and your next appointment on the calendar.</p>'),
    ]
    steps_html = "".join(
        f'''<div class="fv-step reveal"><span class="fv-dot" aria-hidden="true"></span>
        <h3><button type="button" aria-expanded="true">{title}</button></h3>
        <div class="fv-body">{body}</div></div>'''
        for title, body in steps
    )
    faq_pairs = [
        ("How long does a first physical therapy visit take?",
         "Plan on about an hour. Your first visit is a one-on-one evaluation with your therapist — and at First Rehabilitation, treatment usually begins the same day."),
        ("Will I receive treatment at my first physical therapy appointment?",
         "Yes — most patients receive hands-on treatment at the very first visit, along with the start of a home program. The first appointment is not just paperwork."),
        ("What should I bring to my first appointment?",
         "A photo ID, your insurance card, and your prescription or referral if your physician provided one. We'll email you an intake form to complete ahead of time."),
        ("What should I wear to physical therapy?",
         "Loose, comfortable clothing you can move in — and something that gives your therapist access to the area being treated, like shorts for a knee problem or a loose shirt for a shoulder."),
        ("Where do I park at First Rehabilitation?",
         "There's a free parking lot right at our building — 733 US Highway 1, Suite 2A, North Palm Beach. Park, walk in, and you're here."),
    ]
    faq_ld = '<script type="application/ld+json">' + _json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in faq_pairs]
    }, ensure_ascii=False) + '</script>\n'
    faq_html = "".join(
        f'''<details class="job reveal"><summary><span class="job-title" style="font-size:1.05rem;">{q}</span><span class="job-toggle" aria-hidden="true">+</span></summary>
        <div class="job-body"><p>{a}</p></div></details>'''
        for q, a in faq_pairs
    )
    body = f"""
<main>
{page_hero("Your First Visit", "What to Expect — <em class='accent'>Start to Finish</em>",
  "No mystery, no surprises: here's exactly how your first physical therapy visit goes at First Rehabilitation of North Palm Beach.",
  '<div class="crumbs"><a href="/">Home</a> / Your First Visit</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Five Simple Steps</span>
      <h2>Your Visit, <em class="accent">Step by Step</em></h2>
    </div>
    <div class="fv-steps"><span class="fv-progress" aria-hidden="true"></span>{steps_html}</div>
  </div>
</section>
<section class="section on-cream">
  <div class="wrap two-col">
    <div class="reveal">
      <div class="section-head" style="margin-bottom:1.6rem;">
        <span class="eyebrow">Good to Know</span>
        <h2>The Practical Details</h2>
      </div>
      <div class="fv-highlight" style="margin-bottom:1rem;"><strong>What to wear:</strong> loose, comfortable clothing you can move in — shorts for knee or hip conditions, a loose shirt for shoulders. Your therapist needs easy access to the area being treated.</div>
      <div class="fv-highlight" style="margin-bottom:1rem;"><strong>Parking:</strong> free lot right at our building. Park, walk in, and you're here.</div>
      <div class="fv-highlight" style="margin-bottom:1.6rem;"><strong>Arriving:</strong> if you weren't able to finish your intake form at home, come a few minutes early and our front desk will help you complete it.</div>
      <div class="section-head" style="margin:2.2rem 0 1.2rem;">
        <h2 style="font-size:1.5rem;">Quick Answers</h2>
      </div>
      {faq_html}
      <p class="related-links reveal" style="margin-top:1.6rem;"><strong>Read more:</strong> <a href="blog/what-to-expect-first-pt-visit.html">Our full first-visit walkthrough on the blog</a> &middot; <a href="faq.html">All 73 patient FAQs</a></p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Schedule your first visit</h3>
      <p>733 US Highway 1, Suite 2A<br>North Palm Beach, FL 33408</p>
      <p>Mon&ndash;Fri 8:00 AM&ndash;5:30 PM<br>Sat 8:00 AM&ndash;12:30 PM</p>
      <a class="btn btn-coral" href="contact.html">Schedule Your First Visit</a>
      <div class="side-meta">
        <p>Call us directly<br><a href="tel:+15616244263">{PHONE}</a></p>
      </div>
    </aside>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("first-visit.html",
          head("First Physical Therapy Visit: What to Expect | First Rehab",
               "What happens at your first physical therapy appointment in North Palm Beach — what to bring, what to wear, and why treatment starts on day one.",
               canonical="first-visit.html",
               extra_schema=faq_ld + breadcrumb_schema([("Home", ""), ("Your First Visit", "first-visit.html")]))
          + nav(0) + body + footer(0))

# ----------------------------------------------------------------------------
# PAIN 2 POWER — VIDEO EPISODES (YouTube)
# ----------------------------------------------------------------------------
# Newest first. Add a new video by putting its entry at the TOP: VIDEOS[0]
# becomes the featured player. Fields: youtube id, episode label, title, guest
# (or "" ), teaser. Empty list = the page renders its channel CTA only, never a
# fake empty state. Thumbnails come from YouTube's CDN; players are click-to-load
# (youtube-nocookie) so no third-party script runs until a visitor presses play.
VIDEOS = [
    {
        # Verified 2026-10-24 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "Two Time Breast Cancer Survivor Maria | Pain 2 Power Ep 20".
        "id": "Vm_aYietdB4",
        "uploaded": "2026-10-24T13:15:18+00:00",
        "ep": "Episode 20",
        "title": "Two Time Breast Cancer Survivor",
        "guest": "Maria Kendzierski",
        "teaser": "Dave&rsquo;s cousin Maria Kendzierski joins from Buffalo on being diagnosed with breast cancer twice: a stage zero finding at her yearly mammogram in 2015, screening every six months at Roswell Park, and the 2024 MRI that caught a stage one cancer early. Plus chemo, radiation and ringing the bell after both.",
    },
    {
        # Verified 2026-10-17 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/).
        "id": "PRxs5dmAxFs",
        "uploaded": "2026-10-17T14:00:04+00:00",
        "ep": "Episode 19",
        "title": "23 Emmys and a Torn Rotator Cuff",
        "guest": "Shannon Cake",
        "teaser": "Newsmax anchor Shannon Cake on 23 Emmys, the advice that kept her in investigative reporting, and the torn rotator cuff that first brought her to First Rehab as a patient. Plus how she fits a workout into a day that starts at 4:30 AM.",
    },
    {
        # Verified 2026-10-14 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "Pilates and Nutrition After Breast Cancer | Pain 2 Power Episode 18".
        "id": "Na5EMSn44rg",
        "uploaded": "2026-10-14T14:50:54+00:00",
        "ep": "Episode 18",
        "title": "Pilates and Nutrition After Breast Cancer",
        "guest": "Elyse Marrone and Danielle Armstrong",
        "teaser": "Registered dietitian Elyse Marrone and Danielle Armstrong, owner of Pilates Life in Palm Beach Gardens, join Dave and Mike on food, movement and recovery before, during and after a breast cancer diagnosis, from Elyse&rsquo;s seven pillars of health to how Joseph Pilates helped a dancer back after a radical mastectomy.",
    },
    {
        # Verified 2026-10-04 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "What Your Mammogram Can Miss | Pain 2 Power Ep 17: Dr. Don Goodwin".
        "id": "gpfRW1C9aeo",
        "uploaded": "2026-10-04T14:51:23+00:00",
        "ep": "Episode 17",
        "title": "What Your Mammogram Can Miss",
        "guest": "Dr. Donald Goodwin, MD",
        "teaser": "Radiologist Dr. Don Goodwin has read breast imaging for more than 50 years. He explains why most medical societies still say screen every year from 40, why dense breasts can hide up to 60% of cancers under 10mm on a mammogram, and when ultrasound or MRI should be added.",
    },
    {
        # Verified 2026-10-04 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "The Elbow Fix 90% of People Never Need Surgery For | Pain 2 Power Ep 16: Dr. Matt Butler".
        "id": "zDO-q9ClbsQ",
        "uploaded": "2026-09-26T13:00:28+00:00",
        "ep": "Episode 16",
        "title": "The Elbow Fix 90% of People Never Need Surgery For",
        "guest": "Dr. Matt Butler, MD",
        "teaser": "Hand and upper extremity surgeon Dr. Matt Butler of HSS on why most tennis elbow never needs an operation, the growth plate injuries showing up in young pitchers, and the thumb joint replacement he began offering this year after FDA clearance.",
    },
    {
        # Verified 2026-09-20 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "1 in 4 Kids Have a Processing Disorder: Susan Mann | Pain 2 Power Ep 15".
        "id": "oZJYMOL95cA",
        "uploaded": "2026-09-20T14:10:52+00:00",
        "ep": "Episode 15",
        "title": "1 in 4 Kids Have a Processing Disorder",
        "guest": "Susan Mann",
        "teaser": "Every teacher said Susan Mann&rsquo;s two children were gifted; every test put them at the bottom of the scale. A retired San Francisco police officer rather than a clinician, she kept digging until an audiologist named it: auditory and visual processing disorder. Both kids retested off the charts and took full academic scholarships to Oxbridge Academy.",
    },
    {
        # Verified 2026-09-15 against the channel feed: long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "E-Bikes Are Putting Kids in the Trauma Bay… | Pain 2 Power Ep 14".
        "id": "tEWqztCDdVI",
        "uploaded": "2026-09-15T15:11:11+00:00",
        "ep": "Episode 14",
        "title": "E-Bikes Are Putting Kids in the Trauma Bay",
        "guest": "Dr. Chaim Arlosoroff, M.D.",
        "teaser": "Orthopedic trauma surgeon Dr. Chaim Arlosoroff, on staff at St. Mary&rsquo;s Medical Center for 30 years, joins Dave and Mike on the surge in e-bike injuries he sees firsthand in the Level 1 trauma center &mdash; ER visits are up more than 400% nationwide since 2017.",
    },
    {
        # Verified 2026-09-15 against the channel feed: the only long-form entry
        # (link rel=alternate is /watch?v=, not /shorts/), titled
        # "…Captain Kerry Titheradge… | Pain 2 Power Ep 13".
        "id": "HHTgwYIzsyk",
        "uploaded": "2026-09-09T17:09:54+00:00",
        "ep": "Episode 13",
        "title": "Captain Kerry Titheradge on Mental Health, Rescue Dogs and Legacy",
        "guest": "Captain Kerry Titheradge",
        "teaser": "Twenty years after Dave built him a rotator cuff program, Bravo&rsquo;s Captain Kerry from Below Deck catches up with Dave and Mike on the workout that took his name, and what he does with the platform the show gave him.",
    },
    {
        "id": "FBaBGdzNksM",
        "uploaded": "2026-08-31T17:38:11-04:00",
        "ep": "Episode 12",
        "title": "Total Hip Replacement, Explained: Anterior vs. Posterior",
        "guest": "Dr. Michael Leighton, MD",
        "teaser": "Orthopedic surgeon Dr. Michael Leighton breaks down total hip replacement in plain English: the anterior versus posterior approach, what actually drives infection risk, and the flat Medicare payment that covers the surgery and 90 days of follow-up care.",
    },
    {
        "id": "F8jyVhOeuX0",
        "uploaded": "2026-08-31T15:15:26-04:00",
        "ep": "Episode 11",
        "title": "Peptides, GLP-1s &amp; Hormone Replacement Therapy, Explained",
        "guest": "Paul Joyce",
        "teaser": "Paul Joyce of New Life HRT joins Dave and Mike to explain what a peptide actually is, where GLP-1 medications like Ozempic came from, and why the weight they take off comes with a real cost in muscle if the protein and strength work don&rsquo;t come with it.",
    },
    {
        "id": "wdcHPvySKHk",
        # YouTube publish date, ISO-8601. Required by Google's video structured
        # data spec — without it the episode is not eligible for video rich
        # results. Read it off the channel feed
        # (youtube.com/feeds/videos.xml?channel_id=UCFzCl3RvdVahfIjKZ1SfRvQ,
        # <published> per entry) or the watch page's publishDate, and set it
        # whenever a new episode is added here.
        "uploaded": "2026-08-22T08:57:33-04:00",
        "ep": "Episode 10",
        "title": "What&rsquo;s Really Causing Your Hip Pain?",
        "guest": "Dr. Zach McVicker, MD",
        "teaser": "Plenty of people arrive certain the problem is their back, and the hip turns out to be driving it. Orthopedic surgeon Dr. Zach McVicker explains hip impingement in plain English, the cam and pincer shapes it comes in, why the labrum works like a gasket between two pipes, and why an early arthroscopic repair keeps the hip you were born with.",
    },
    {
        "id": "h_sNZv2q65E",
        "uploaded": "2026-08-08",   # premiered Aug 8, 2026; exact time not published
        "ep": "Episode 9",
        "title": "Shoulder Replacement, Muscle Sparing Surgery &amp; Why Robots Are Marketing",
        "guest": "Dr. Vani Sabesan",
        "teaser": "Orthopaedic shoulder surgeon Dr. Vani Sabesan on why we are better at fixing rotator cuffs than at getting them to heal, muscle sparing technique and the case against six weeks in a sling, and why robots in shoulder surgery are great marketing rather than better outcomes.",
    },
    {
        "id": "hv1bNdFurrc",
        "uploaded": "2026-08-01",   # premiered Aug 1, 2026; exact time not published
        "ep": "Episode 8",
        "title": "Shoulder Pain, Rotator Cuffs &amp; Replacements",
        "guest": "Dr. Ryan Simovitch",
        "teaser": "The shoulder is the most mobile joint in the body — and that mobility is exactly why it breaks down. Dave and Mike sit down with Dr. Ryan Simovitch to talk rotator cuffs, shoulder replacements, and what actually helps.",
        # Optional. Set while the radio broadcast is still upcoming; delete the
        # line once the episode has aired.
    },
]

def build_insurance():
    """Insurance & Medicare page.

    Built from a 2026-08-03 Search Console export: "physical therapist that
    accepts medicare palm beach" (142 impressions, position 31.8) and
    "physical therapy medicare palm beach" (132, position 29.5) were drawing
    real demand with no page on the site targeting them. The facts already
    existed, scattered across the FAQ; this gives them a URL.

    Every claim here is owner-confirmed and already published elsewhere on the
    site. Per the FAQ convention, this page does NOT repeat the Q&A blocks or
    carry a second FAQPage block: it cross-links to /faq.html#insurance-cost so
    there stays exactly one FAQPage in the graph."""
    plan_notes = {
        "Medicare": "Original Medicare, accepted here since 1991.",
        "Medicare Advantage": "Both HMO and PPO Advantage plans.",
        "Blue Cross Blue Shield": "Including Florida Blue plans.",
        "Aetna": "Commercial and Medicare Advantage.",
        "Humana": "Commercial and Medicare Advantage.",
        "Tricare": "For active duty families, retirees, and dependents.",
        "VA Community Care Network": "VACCN referrals welcome.",
        "Workers' Comp": "Work injury claims, coordinated with your adjuster.",
        "Self Pay": "Transparent pricing, no insurance required.",
    }
    cards = "".join(
        f'''<div class="ins-card reveal">
          <h3>{p}</h3><p>{plan_notes.get(p, "")}</p>
        </div>''' for p in PLANS)
    body = f"""
<main>
{page_hero("Insurance &amp; Medicare", "Coverage, <em class='accent'>Sorted Before You Arrive</em>",
  "We accept Medicare and most major insurance plans, and our front desk verifies your exact benefits before your first visit at our North Palm Beach clinic.",
  '<div class="crumbs"><a href="/">Home</a> / Insurance &amp; Medicare</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Plans We Accept</span>
      <h2>Most Major Insurance, <em class="accent">Including Medicare</em></h2>
      <p class="lede">Coverage details differ from plan to plan, so we check yours before you start. Call <a class="text-link" href="tel:+15616244263">{PHONE}</a> and our front desk will verify your specific physical therapy benefits.</p>
    </div>
    <div class="ins-grid">{cards}</div>
  </div>
</section>
<section class="section on-cream">
  <div class="wrap two-col">
    <div class="reveal">
      <div class="section-head" style="margin-bottom:1.6rem;">
        <span class="eyebrow">Medicare Patients</span>
        <h2>Medicare, Explained Plainly</h2>
      </div>
      <p>Medicare covers medically necessary outpatient physical and occupational therapy, and we have cared for Medicare patients in North Palm Beach since 1991. We accept both Original Medicare and Medicare Advantage plans.</p>
      <p>Medicare does require a physician to certify your plan of care. Our team handles that paperwork with your doctor so it does not become your errand, and the front desk explains your benefits before treatment begins. Our <a href="#medicare-guide">2026 Medicare guide</a> below covers deductibles, the KX threshold and Medicare Advantage in detail.</p>
      <div class="fv-highlight" style="margin:1.4rem 0;"><strong>Florida direct access:</strong> in most cases you can begin a physical therapy evaluation without a physician referral. Some plans still require one for coverage, which is exactly what we check when we verify your benefits.</div>
      <div class="section-head" style="margin:2.2rem 0 1.2rem;">
        <h2 style="font-size:1.5rem;">No Surprises on the Bill</h2>
      </div>
      <p>Before your first appointment we verify your coverage and tell you what your plan pays for, whether you have a copay or a deductible to meet, and whether your plan needs a referral. You know where you stand before treatment starts, not after.</p>
      <p>Not insured, or out of network? We offer self pay, and free consultations are available. Call and we will talk it through honestly.</p>
      <p class="related-links reveal" style="margin-top:1.6rem;"><strong>More detail:</strong> <a href="faq.html#insurance-cost">Insurance &amp; cost FAQs</a> &middot; <a href="glossary.html">Patient glossary</a> &middot; <a href="first-visit.html">What to expect at your first visit</a></p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Check your coverage</h3>
      <p>Our front desk verifies benefits before you arrive. It takes one phone call.</p>
      <p>733 US Highway 1, Suite 2A<br>North Palm Beach, FL 33408</p>
      <p>Mon&ndash;Fri 8:00 AM&ndash;5:30 PM<br>Sat 8:00 AM&ndash;12:30 PM</p>
      <a class="btn btn-coral" href="tel:+15616244263">Call {PHONE}</a>
      <div class="side-meta">
        <p>Prefer to write?<br><a href="contact.html">Request an appointment</a></p>
      </div>
    </aside>
  </div>
</section>
<section class="section" id="medicare-guide" style="scroll-margin-top:100px;">
  <div class="wrap">
    <article class="prose reveal" style="margin:0 auto;">
      <span class="eyebrow">Medicare Guide &middot; Updated for 2026</span>
      <h2>Medicare and Outpatient Therapy in 2026, in Plain English</h2>
      <p>Short version: Original Medicare Part B helps pay for medically necessary outpatient physical therapy and occupational therapy, and there is no yearly limit on how much it will pay when the care is medically necessary. After you meet the 2026 Part B deductible of $283, you pay 20% of the Medicare-approved amount for each visit. Medicare Advantage plans cover the same benefit but set their own copays, networks and approval rules.</p>
      <p>Two thirds of the people we treat are 65 or older, so these are the questions our front desk answers every single day. This guide puts the answers in one place. It is general information, and your own costs depend on your plan, so we still check your benefits before your first visit.</p>

      <h3>What you pay under Original Medicare</h3>
      <p>Part B is the piece of Original Medicare that covers outpatient care. For therapy it works in two steps. First comes the yearly deductible, $283 in 2026. Until you have paid that much toward Part B services of any kind, Medicare does not start paying its share. Plenty of patients have already met it by the time they reach us, because a doctor visit or an imaging study earlier in the year counts toward it.</p>
      <p>After that, Medicare pays 80% of the Medicare-approved amount and you are responsible for the other 20%, called <a href="glossary.html#coinsurance">coinsurance</a>. If you carry a <a href="glossary.html#medigap">Medicare Supplement (Medigap)</a> plan, it may pay some or all of that 20%, depending on which plan you have. Secondary coverage through a former employer can work the same way. Bring every card you have to the first visit and we will sort out which pays first.</p>

      <h3>Is there a cap on therapy visits?</h3>
      <p>No. Medicare used to impose a hard dollar cap on outpatient therapy each year, and many people still remember it. Congress removed that cap in 2018. What remains is a checkpoint, not a ceiling.</p>
      <p>Once your physical therapy charges for the year pass $2,480, the clinic adds a code called the <a href="glossary.html#kx-modifier">KX modifier</a> to your claims. It tells Medicare your therapist has documented why continued care is medically necessary. Occupational therapy has its own separate $2,480 threshold for 2026. A second, higher figure of $3,000 can trigger a targeted medical review, where Medicare looks more closely at the documentation. Neither number means your therapy has to stop. What matters is that the care is medically necessary and the notes show it, which is our job, not yours.</p>

      <div class="data-table" tabindex="0" role="region" aria-label="Original Medicare compared with Medicare Advantage">
        <table>
          <caption>Original Medicare figures from CMS for calendar year 2026. Medicare Advantage terms vary by plan.</caption>
          <thead><tr><th scope="col">Question</th><th scope="col">Original Medicare (Part B)</th><th scope="col">Medicare Advantage (Part C)</th></tr></thead>
          <tbody>
            <tr><th scope="row">What you pay per visit</th><td>20% of the Medicare-approved amount, after the $283 deductible</td><td>A copay or coinsurance set by your plan</td></tr>
            <tr><th scope="row">Yearly limit on therapy</th><td>None, when care is medically necessary</td><td>None on the benefit itself, though plans may limit visits per approval</td></tr>
            <tr><th scope="row">Approval before you start</th><td>Generally no prior authorization</td><td>Often required; we request it for you</td></tr>
            <tr><th scope="row">Choice of clinic</th><td>Any provider that accepts Medicare</td><td>Usually the plan's network</td></tr>
            <tr><th scope="row">Yearly out-of-pocket maximum</th><td>None, unless you add a Medigap plan</td><td>Yes, set by the plan</td></tr>
          </tbody>
        </table>
      </div>

      <h3>Do I have to keep improving for Medicare to keep paying?</h3>
      <p>No, and this one surprises people. For years, some Medicare claims were denied because a patient had stopped getting better, a rule of thumb known as the improvement standard. A 2013 court settlement, <em>Jimmo v. Sebelius</em>, made CMS restate that no improvement standard applies. What Medicare looks at is whether you need the skills of a therapist, not whether you are still gaining ground.</p>
      <p>Medicare's own description of covered physical therapy says it can help you improve, maintain your current function, or slow your rate of decline. That matters for someone living with Parkinson's disease, multiple sclerosis, arthritis or the after-effects of a stroke, where holding steady is a real achievement. If a skilled program is what keeps you walking safely or dressing yourself, that can qualify. Your therapist documents why the skilled care is needed, and that documentation is what Medicare reviews.</p>
      <p>The flip side is also true. Once a home program you can do safely on your own will keep your progress, skilled therapy is no longer the right tool, and we will tell you so plainly.</p>

      <h3>When formal therapy ends</h3>
      <p>Discharge is not the finish line. The most common way people lose what they gained is stopping cold: no exercise, back to the chair. Every patient leaves with a written <a href="glossary.html#home-exercise-program">home exercise program</a>, and patients who want more structure can move into our <a href="services/wellness.html">on-site wellness gym</a>, training with a team that already knows their history. The gym is a separate program from Medicare-covered therapy and does not take insurance, so the front desk will explain how it works and what it costs before you sign up.</p>

      <h3>Why your doctor signs your plan of care</h3>
      <p>Medicare requires your doctor, or another qualified provider such as a nurse practitioner or physician assistant, to certify that you need therapy. In practice that means signing the <a href="glossary.html#plan-of-care">plan of care</a> your therapist writes after your evaluation: your goals, the treatment, how often you will come and for how long. We send it to your doctor and follow up until it comes back signed, so it does not become one more errand on your list.</p>
      <p>That is also why the first visit matters so much. The <a href="first-visit.html">initial evaluation</a> takes about an hour, measures where you are today, and sets goals specific enough to show progress. Those measurements are what keep the documentation strong if your care runs past the KX threshold.</p>

      <h3>What a CORF is, and what it means for you</h3>
      <p>First Rehabilitation of North Palm Beach is a Comprehensive Outpatient Rehabilitation Facility, or CORF. That is a Medicare certification, not a marketing phrase. CMS defines a CORF as a facility that provides coordinated outpatient diagnostic, therapeutic and restorative services at a single fixed location, with physician consultation and review of the plan of treatment among its required core services.</p>
      <p>For a patient, the practical meaning is coordination. Physical therapy, occupational therapy and <a href="services/hand-therapy.html">certified hand therapy</a> happen in the same building, under one plan, with the same team reading the same notes. A patient recovering from a stroke might need a physical therapist for walking and balance, an occupational therapist for dressing and cooking, and a certified hand therapist for a weak, closed hand. Here, those three people work down the hall from each other.</p>

      <h3>If you have a Medicare Advantage plan</h3>
      <p>We accept Medicare Advantage plans, including HMO and PPO plans from carriers such as Humana and Aetna. The benefit is the same medically necessary therapy, but the rules come from the plan. Many require prior authorization, approve a set number of visits at a time, and ask for progress notes before approving more. Your cost is usually a copay per visit rather than 20%.</p>
      <p>None of that should land on you. When you call, we verify your plan, request any authorization it needs and tell you your copay before you arrive. If your plan approves visits in blocks, we track the count and request more before you run out, so your therapy does not stall halfway through.</p>

      <h3>Five questions to ask before your first visit</h3>
      <ol>
        <li>Have I met my Part B deductible for this year?</li>
        <li>Do I have a Medigap or secondary plan that covers the 20%?</li>
        <li>If I have Medicare Advantage, does my plan need prior authorization for therapy?</li>
        <li>Does my plan require a physician referral, or can I start with an evaluation?</li>
        <li>Will one clinic be able to handle physical, occupational and hand therapy if I need more than one?</li>
      </ol>
      <p>Our front desk can answer the first four for you with one phone call to <a href="tel:+15616244263">{PHONE}</a>. The fifth one we can answer now: yes.</p>

      <h3>Sources</h3>
      <ol class="src-list">
        <li><a href="https://www.medicare.gov/coverage/physical-therapy-services" rel="noopener">Medicare.gov, Physical therapy services</a>: Part B coverage, the 20% coinsurance, physician certification, and no yearly limit on medically necessary outpatient therapy.</li>
        <li><a href="https://www.govinfo.gov/content/pkg/FR-2025-11-19/html/2025-20251.htm" rel="noopener">Federal Register, November 19, 2025</a>: the 2026 Part B deductible of $283.</li>
        <li><a href="https://www.cms.gov/therapyservices" rel="noopener">CMS, Therapy Services</a>: the 2026 KX modifier thresholds of $2,480 and the $3,000 targeted medical review threshold.</li>
        <li><a href="https://www.cms.gov/medicare/health-safety-standards/certification-compliance/comprehensive-outpatient-rehabilitation-facilities" rel="noopener">CMS, Comprehensive Outpatient Rehabilitation Facilities</a>: the CORF definition and core services.</li>
        <li><a href="https://www.cms.gov/medicare/settlements/jimmo" rel="noopener">CMS, Jimmo Settlement</a>: the maintenance coverage standard for skilled therapy, and the end of the improvement standard.</li>
      </ol>
      <p class="fv-highlight" style="margin-top:1.4rem;">This guide is general information, not medical, legal or insurance advice. Figures are for 2026 and change each January. Your costs depend on your plan, which we verify before your first visit.</p>
    </article>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("insurance.html",
          head("Physical Therapy That Accepts Medicare | Palm Beach County",  # head() escapes; don't pre-escape
               "We accept Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare and VA Community Care in North Palm Beach. We verify your benefits first.",
               canonical="insurance.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Insurance &amp; Medicare", "insurance.html")]))
          + nav(0) + body + footer(0))


# ----------------------------------------------------------------------------
# PATIENT GLOSSARY (/glossary.html) — added 2026-10-14
# ----------------------------------------------------------------------------
# Plain-English definitions of the words patients meet on our forms, bills and
# plan of care. Modelled on the A-Z glossary pattern that works for the
# lawofficesuccess.com site Nick's friend runs, with one deliberate difference:
# the DefinedTermSet JSON-LD is generated from THIS list, so every term in the
# schema is a term a visitor can see. Nothing is in markup that is not on the page.
#
# Rules: definitions describe the general concept, never an individual's care.
# No service we have not confirmed (no functional capacity evaluations, no
# in-home therapy, no driving evaluations). No prices. Medicare figures carry the
# year and the CMS source, and must be updated every January.
# Shape: (term, definition, example-or-None, anchor slug)
GLOSSARY = [
    ("Activities of daily living (ADLs)", "The everyday self-care tasks most people do without thinking: dressing, bathing, grooming, eating and getting on and off the toilet. Occupational therapy often measures progress in ADLs.", "Buttoning a shirt with one hand after shoulder surgery.", "adls"),
    ("Balance training", "Exercises that challenge your steadiness so you are less likely to fall.", "Standing on one foot while reaching, or walking heel to toe along a line.", "balance-training"),
    ("Certified Hand Therapist (CHT)", "An occupational or physical therapist who has completed years of hands-on hand and upper extremity practice and passed a national certification exam. Hand surgeons often refer post-operative patients to a CHT.", "The therapist who guides your recovery after a wrist fracture or tendon repair.", "cht"),
    ("Coinsurance", "Your share of a covered service, shown as a percentage, after you have met your deductible. Under Original Medicare Part B it is 20% of the Medicare-approved amount.", "If the approved amount for a visit is $100, 20% coinsurance means you owe $20.", "coinsurance"),
    ("Comprehensive Outpatient Rehabilitation Facility (CORF)", "A Medicare-certified outpatient facility that provides coordinated rehabilitation at one location, with physician oversight of the plan of treatment. First Rehabilitation of North Palm Beach is a CORF.", None, "corf"),
    ("Copay", "A flat amount you pay at each visit, set by your insurance plan.", "A plan with a set copay for each specialist or therapy visit.", "copay"),
    ("Deductible", "The amount you pay for covered care each year before your plan starts paying its share. The 2026 Medicare Part B deductible is $283.", "Until you have paid $283 toward Part B services in 2026, Medicare does not begin paying its 80%.", "deductible"),
    ("Direct access", "Starting physical therapy without a physician referral. In Florida this is allowed in most cases, but some insurance plans still require a referral for coverage, so we check before your first visit.", None, "direct-access"),
    ("Discharge", "The end of formal therapy, usually when you have met your goals or your progress has leveled off.", "Finishing therapy with a written home program to keep your gains.", "discharge"),
    ("Explanation of benefits (EOB)", "A statement from your insurance company showing what was billed, what it paid and what you may owe. It is not a bill.", None, "eob"),
    ("Fall-risk screening", "Short tests of strength, balance and walking that show how likely someone is to fall.", "Standing up from a chair and walking a short distance while a therapist times you.", "fall-risk-screening"),
    ("Gait training", "Practice walking safely and smoothly after an injury, surgery or illness.", "Relearning a steady step pattern after a hip replacement.", "gait-training"),
    ("Home exercise program", "A short set of exercises your therapist teaches you to do on your own between visits.", "Three exercises, ten minutes a day, with pictures to follow.", "home-exercise-program"),
    ("In-network and out-of-network", "In-network providers have a contract with your insurance plan and usually cost you less. Out-of-network providers do not.", None, "in-network"),
    ("Initial evaluation", "Your first visit. The therapist reviews your history, tests movement, strength and daily function, and sets goals with you. At our clinic it takes about an hour, and treatment usually starts the same day.", None, "initial-evaluation"),
    ("KX modifier", "A billing code a clinic adds once a patient's yearly Medicare therapy charges pass a set amount, confirming that continued therapy is medically necessary and documented. For 2026 the amount is $2,480 for physical therapy and speech therapy combined, and a separate $2,480 for occupational therapy. It is not a cap on your care.", None, "kx-modifier"),
    ("Letter of protection (LOP)", "A written agreement, used in some injury cases, under which a provider treats you and is paid from a settlement or judgment later. It is not insurance, and it is arranged through your attorney.", None, "lop"),
    ("Manual therapy", "Hands-on techniques that move joints and soft tissue to reduce stiffness and pain.", "A therapist gently mobilizing a stiff shoulder.", "manual-therapy"),
    ("Medicare Advantage", "A private plan, sometimes called Part C, that provides Medicare benefits under its own rules for networks, copays and approvals.", "A Humana or Aetna Medicare plan that asks for prior authorization before therapy starts.", "medicare-advantage"),
    ("Medicare Part B", "The part of Original Medicare that covers outpatient care, including medically necessary physical and occupational therapy. After the yearly deductible you pay 20% of the Medicare-approved amount, and there is no yearly limit on medically necessary therapy.", None, "medicare-part-b"),
    ("Medicare Supplement (Medigap)", "Private insurance sold alongside Original Medicare that can pay some or all of the costs Medicare leaves to you, such as the 20% coinsurance. What it pays depends on the plan.", None, "medigap"),
    ("Modalities", "Supporting treatments such as heat, cold or electrical stimulation, usually paired with exercise.", "A warm pack before stretching a stiff back.", "modalities"),
    ("Neuromuscular re-education", "Exercises that retrain coordination, balance and movement patterns after an injury or a neurological event such as a stroke.", None, "neuromuscular-re-education"),
    ("Occupational therapy (OT)", "Therapy focused on doing the things your day requires: dressing, cooking, working, and using your hands and arms well.", "Relearning to cook safely after a stroke.", "occupational-therapy"),
    ("Orthosis (splint)", "A custom or ready-made support that protects or positions a hand, wrist or finger while it heals. Our hand therapy program fabricates custom orthoses in the clinic.", "A thumb splint molded to your hand after a tendon injury.", "orthosis"),
    ("Out-of-pocket maximum", "The most you pay in a year for covered care before your plan pays the rest in full. Original Medicare has no out-of-pocket maximum; Medicare Advantage plans do.", None, "out-of-pocket-maximum"),
    ("Outpatient therapy", "Therapy where you come in for a visit and go home the same day.", None, "outpatient-therapy"),
    ("Personal injury protection (PIP)", "Florida no-fault auto coverage that helps pay medical bills after a crash, regardless of who caused it, up to your policy limit.", None, "pip"),
    ("Physical therapy (PT)", "Treatment that restores movement, strength, balance and function, and helps reduce pain.", "Exercise and hands-on care after knee surgery.", "physical-therapy"),
    ("Plan of care", "A written plan listing your goals, treatments, how often you will come and how long therapy is expected to last. For Medicare, your physician or another qualified provider must certify it.", "Two visits a week for six weeks, with the goal of climbing stairs without a rail.", "plan-of-care"),
    ("Post-surgical rehabilitation", "Therapy after an operation to restore motion and strength safely, following your surgeon's protocol and timeline.", None, "post-surgical-rehabilitation"),
    ("Prior authorization", "Approval some insurance plans require before they will cover therapy. Medicare Advantage plans often require it; Original Medicare generally does not.", None, "prior-authorization"),
    ("Progress report", "A written update to your physician, and sometimes your insurer, showing how you are doing against your goals.", None, "progress-report"),
    ("Range of motion", "How far a joint can move.", "How high you can lift your arm overhead.", "range-of-motion"),
    ("Re-evaluation", "A formal check partway through therapy that compares your progress with your goals and adjusts the plan.", None, "re-evaluation"),
    ("Return-to-work program", "Occupational therapy built around what a specific job demands, using graded conditioning and task practice before a work release.", None, "return-to-work"),
    ("Therapeutic activities", "Real-life tasks used as treatment.", "Lifting a laundry basket, getting out of a low chair or reaching into a high cabinet.", "therapeutic-activities"),
    ("Therapeutic exercise", "Targeted movements that build strength, flexibility and endurance.", "Leg presses, resistance band work or a stretching routine.", "therapeutic-exercise"),
    ("Workers' compensation", "Insurance that covers medical care for injuries that happen at work. We coordinate documentation with your adjuster.", None, "workers-comp"),
]


def build_glossary():
    """A-Z patient glossary with DefinedTermSet JSON-LD generated from GLOSSARY."""
    import json as _json
    letters = []
    groups = {}
    for term, definition, example, slug in GLOSSARY:
        first = term[0].upper()
        if first not in groups:
            groups[first] = []
            letters.append(first)
        groups[first].append((term, definition, example, slug))
    jump = "".join(f'<a href="#letter-{L.lower()}">{L}</a>' for L in letters)
    sections = []
    for L in letters:
        items = "".join(
            f'<dt id="{slug}">{term}</dt><dd>{definition}'
            + (f'<span class="gloss-ex">Example: {example}</span>' if example else "")
            + "</dd>"
            for term, definition, example, slug in groups[L])
        sections.append(f'<h2 class="gloss-letter" id="letter-{L.lower()}">{L}</h2><dl class="gloss-list">{items}</dl>')
    url = "https://www.firstrehabnpb.com/glossary.html"
    terms_ld = [{"@type": "DefinedTerm", "@id": f"{url}#{slug}", "name": _faq_plain(term),
                 "description": _faq_plain(definition), "inDefinedTermSet": {"@id": url + "#termset"}}
                for term, definition, example, slug in GLOSSARY]
    schema = '<script type="application/ld+json">' + _json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "DefinedTermSet", "@id": url + "#termset",
             "name": "Physical and Occupational Therapy Glossary", "url": url,
             "publisher": ORG_REF, "hasDefinedTerm": terms_ld},
        ],
    }, ensure_ascii=False) + '</script>\n'
    body = f"""
<main>
{page_hero("Patient Resources", "Therapy Words, <em class='accent'>Explained Plainly</em>",
  "Plain-English definitions of the terms you will see on your plan of care, your insurance statements and your intake forms.",
  '<div class="crumbs"><a href="/">Home</a> / Patient Glossary</div>')}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p>Ever sit in a waiting room wondering what half the paperwork means? You are not the only one. This glossary covers the words you will hear at First Rehabilitation of North Palm Beach, from plan of care to prior authorization. If a term still does not make sense for your situation, ask your therapist or call the front desk at {PHONE}.</p>
      <nav class="gloss-jump" aria-label="Jump to letter">{jump}</nav>
      {"".join(sections)}
      <p style="margin-top:2.4rem;">Medicare figures on this page are for 2026, from the Centers for Medicare &amp; Medicaid Services. For what they mean in practice, read our <a href="insurance.html#medicare-guide">plain-English Medicare guide</a>. For everything else, see the <a href="faq.html">FAQ</a> or <a href="first-visit.html">what to expect at your first visit</a>.</p>
      <p class="fv-highlight" style="margin-top:1.4rem;">This glossary is general information, not medical or insurance advice. Coverage depends on your plan; our front desk verifies your benefits before your first visit.</p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Questions about your coverage?</h3>
      <p>Our front desk checks your benefits before your first visit, so the terms on this page turn into real numbers for your plan.</p>
      <a class="btn btn-coral" href="tel:+15616244263">Call {PHONE}</a>
      <div class="side-meta">
        <p>Prefer to write?<br><a href="contact.html">Request an appointment</a></p>
      </div>
    </aside>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("glossary.html",
          head("Physical Therapy Glossary: Terms Explained | First Rehab",
               "Plain-English definitions of physical therapy, occupational therapy and Medicare terms, from plan of care and KX modifier to coinsurance. First Rehab, North Palm Beach.",
               canonical="glossary.html",
               extra_schema=schema + breadcrumb_schema([("Home", ""), ("Patient Glossary", "glossary.html")]))
          + nav(0) + body + footer(0))


def _video_card(v, featured=False):
    # maxresdefault is the 1280x720 thumbnail; hqdefault (480x360) is far too
    # small for the featured player and renders visibly soft. Not every upload
    # has a maxres frame, so fall back automatically if it 404s.
    thumb = f'https://i.ytimg.com/vi/{v["id"]}/maxresdefault.jpg'
    fallback = f'https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg'
    watch = f'https://www.youtube.com/watch?v={v["id"]}'
    embed = f'https://www.youtube-nocookie.com/embed/{v["id"]}?autoplay=1&amp;rel=0'
    guest = f'<span class="vid-guest">{v["guest"]}</span>' if v.get("guest") else ""
    airs = f'<span class="vid-airs">{v["airs"]}</span>' if v.get("airs") else ""
    cls = "vid-card is-featured" if featured else "vid-card"
    return f'''<article class="{cls} reveal">
      <button class="vid-facade" type="button" data-embed="{embed}"
        data-title="{v["title"]} — Pain 2 Power on YouTube">
        <img src="{thumb}" alt="" loading="lazy" width="1280" height="720"
             onerror="this.onerror=null;this.src='{fallback}'">
        <span class="vid-play" aria-hidden="true"><svg viewBox="0 0 68 48"><path class="vp-bg" d="M66.5 7.7c-.8-2.9-3.1-5.2-6-6C55.2 0 34 0 34 0S12.8 0 7.5 1.7c-2.9.8-5.2 3.1-6 6C0 13 0 24 0 24s0 11 1.5 16.3c.8 2.9 3.1 5.2 6 6C12.8 48 34 48 34 48s21.2 0 26.5-1.7c2.9-.8 5.2-3.1 6-6C68 35 68 24 68 24s0-11-1.5-16.3z"/><path class="vp-tri" d="M45 24 27 14v20z"/></svg></span>
        <span class="sr-only">Play: {v["title"]}</span>
      </button>
      <div class="vid-body">
        <span class="vid-ep">{v["ep"]}</span>{airs}
        <h3>{v["title"]}</h3>
        {guest}
        <p>{v["teaser"]}</p>
        <a class="vid-yt" href="{watch}" target="_blank" rel="noopener">Watch on YouTube <span class="arr">&rarr;</span></a>
      </div>
    </article>'''

def _video_schema():
    """VideoObject JSON-LD per episode, tied to the org."""
    import json as _json
    graph = []
    for v in VIDEOS:
        node = {
            "@type": "VideoObject",
            "name": _faq_plain(f'{v["ep"]}: {v["title"]}'),
            "description": _faq_plain(v["teaser"]),
            "thumbnailUrl": f'https://i.ytimg.com/vi/{v["id"]}/maxresdefault.jpg',
            "embedUrl": f'https://www.youtube.com/embed/{v["id"]}',
            "contentUrl": f'https://www.youtube.com/watch?v={v["id"]}',
            "publisher": {"@id": "https://www.firstrehabnpb.com/#organization"},
        }
        # uploadDate is REQUIRED by schema.org and by Google's video structured
        # data spec. A VideoObject without it is not eligible for video rich
        # results, so never add an episode to VIDEOS without one.
        if v.get("uploaded"):
            node["uploadDate"] = v["uploaded"]
        graph.append(node)
    if not graph:
        return ""
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def build_videos():
    crumbs = '<div class="crumbs"><a href="/">Home</a> / Videos</div>'
    if VIDEOS:
        featured = _video_card(VIDEOS[0], featured=True)
        rest = "".join(_video_card(v) for v in VIDEOS[1:])
        more = (f'<section class="section" style="padding-top:0;"><div class="wrap">'
                f'<div class="section-head reveal" style="margin-bottom:1.6rem;">'
                f'<span class="eyebrow">More Episodes</span><h2>The Full Library</h2></div>'
                f'<div class="vid-grid">{rest}</div></div></section>') if rest else ""
        gallery = f'''<section class="section">
  <div class="wrap">
    <div class="section-head reveal" style="margin-bottom:1.6rem;">
      <span class="eyebrow">Latest Video</span><h2>Now Playing</h2>
    </div>
    <div class="vid-featured-wrap">{featured}</div>
  </div>
</section>
{more}'''
    else:
        gallery = ""
    body = f"""
<main>
{page_hero("Pain 2 Power on Video", "Watch the <em class='accent'>Conversations</em>",
  "Every Pain 2 Power episode, on camera — real talk with the surgeons, therapists, and specialists who keep the Palm Beaches moving.", crumbs, loop="video")}
{gallery}
<section class="section on-cream">
  <div class="wrap" style="text-align:center;">
    <div class="section-head center reveal"><span class="eyebrow">Never Miss One</span><h2>Subscribe on <em class="accent">YouTube</em></h2></div>
    <p class="vid-sub-copy reveal">New episodes land on our channel alongside the radio show — Saturdays at 8:30 AM on 100.3 Legends Radio, and streaming anytime.</p>
    <div class="vid-cta-row reveal">
      <a class="btn btn-coral" href="{YOUTUBE}" target="_blank" rel="noopener">Visit Our YouTube Channel <span class="arr">&rarr;</span></a>
      <a class="btn btn-ink" href="podcast.html">Listen to the Podcast</a>
    </div>
  </div>
</section>
{cta_band(0)}
</main>
<script src="assets/js/videos.js?v={asset_v('assets/js/videos.js')}" defer></script>
"""
    write("videos.html",
          head("Pain 2 Power Videos | First Rehabilitation of North Palm Beach",
               "Watch Pain 2 Power video episodes — Dr. Dave Kashuba and Mike McGann talk rehab, orthopedics, and staying active with leading Palm Beach County specialists.",
               canonical="videos.html", og_image="assets/media/podcast-cover.jpg",
               extra_schema=p2p_poster_preload("video") + _video_schema() + _trailer_schema()
                            + breadcrumb_schema([("Home", ""), ("Videos", "videos.html")]))
          + nav(0) + body + footer(0))

GUEST_LINK_LABELS = {
    "website": "Website", "profile": "Profile", "instagram": "Instagram",
    "facebook": "Facebook", "linkedin": "LinkedIn", "x": "X", "youtube": "YouTube",
    "tiktok": "TikTok", "podcast": "Podcast", "book": "Book", "other": "Link",
}
_GICON = {   # 16px line icons for the directory card action bar
    "user": '<path d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0"/>',
    "headphones": '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3" y="14" width="5" height="7" rx="1.5"/><rect x="16" y="14" width="5" height="7" rx="1.5"/>',
    "play": '<rect x="2.5" y="5" width="19" height="14" rx="3"/><path d="M10 9.5v5l4.5-2.5z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
}

def _gicon(name, size=16):
    return (f'<svg class="gi" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_GICON[name]}</svg>')

def _guest_initials(g):
    parts = [w for w in g["name"].replace(".", "").split() if w[:1].isalpha()]
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][:2].upper()

def guest_portrait(g, depth=0, size=160, cls="gp"):
    """Square headshot: the guest's official practice headshot (credited on the
    profile), a still from our own Pain 2 Power footage, a team portrait for
    staff, or initials. tools/guest-photo.py makes them (see its docstring)."""
    p = "../" * depth
    ph = g.get("photo") or {}
    alt = f"{guest_display(g)} on Pain 2 Power"
    if ph.get("registry"):
        return f'<span class="{cls}">{photo(ph["registry"], depth=depth, sizes=f"{size}px", ratio="1/1", alt=alt)}</span>'
    if ph.get("src"):
        src = ph["src"]
        big = size > 160
        w = 480 if big else 160
        return (f'<picture class="{cls}"><source type="image/webp" srcset="{p}{src}-160.webp 160w, {p}{src}-480.webp 480w" sizes="{size}px">'
                f'<img src="{p}{src}-{w}.jpg" srcset="{p}{src}-160.jpg 160w, {p}{src}-480.jpg 480w" sizes="{size}px" '
                f'width="{w}" height="{w}" alt="{alt}" loading="lazy" decoding="async"></picture>')
    return f'<span class="{cls} gp-mono" role="img" aria-label="{guest_display(g)}">{_guest_initials(g)}</span>'

def _guest_episode_links(g, depth=0):
    """[(label, spotify_url, video_id, recap_slug)] for every episode they were on, newest first."""
    by_label = {e[0]: e for e in EPISODES}
    out = []
    for e in sorted(g["episodes"], key=lambda e: -int(e.split()[-1])):
        ep = by_label.get(e)
        spot = ep[3] if ep and "open.spotify.com/episode/" in ep[3] else ""
        vid = next((v for v in VIDEOS if v["ep"] == e), None)
        post = EPISODE_POSTS.get(e)
        out.append((e, spot, vid, post if post in BLOG_POSTS else ""))
    return out

def _guest_meta_line(g):
    bits = [", ".join(g["episodes"])]
    n = len(g.get("clips", []))
    if n:
        bits.append(f"{n} clip{'s' if n != 1 else ''}")
    if g.get("location"):
        bits.append(g["location"])
    return " &middot; ".join(bits)

def _guest_haystack(g):
    aff = (g.get("affiliation") or {}).get("name", "")
    words = [g["name"], g["credentials"], g["headline"], aff, g.get("location", ""),
             _faq_plain(GUEST_CAT_LABEL[g["category"]])] + g["episodes"]
    return _faq_plain(" ".join(words)).lower().replace('"', "")

def _guest_dir_card(g):
    url = guest_url(g)
    eps = _guest_episode_links(g)
    acts = [f'<a class="gact" href="{url}">{_gicon("user")}<span>Profile</span></a>']
    spot = next((s for _, s, _, _ in eps if s), "")
    if spot:
        acts.append(f'<a class="gact" href="{spot}" target="_blank" rel="noopener" aria-label="Listen to {guest_display(g)} on Spotify">{_gicon("headphones")}<span>Listen</span></a>')
    vid = next((v for _, _, v, _ in eps if v), None)
    if vid:
        acts.append(f'<a class="gact" href="https://www.youtube.com/watch?v={vid["id"]}" target="_blank" rel="noopener" aria-label="Watch {guest_display(g)} on YouTube">{_gicon("play")}<span>Watch</span></a>')
    site = next((l for l in g.get("links", []) if l["type"] in ("website", "profile") and "firstrehabnpb.com" not in l["url"]), None)
    if site:
        acts.append(f'<a class="gact" href="{site["url"]}" target="_blank" rel="noopener" aria-label="Website: {site.get("label") or guest_display(g)}">{_gicon("globe")}<span>Website</span></a>')
    aff = (g.get("affiliation") or {}).get("name", "")
    return (f'<li class="gcard" data-guest data-cat="{g["category"]}" data-hay="{_guest_haystack(g)}">'
            f'<div class="gcard-top">{guest_portrait(g)}<div class="gcard-tx">'
            f'<p class="gcard-cat">{GUEST_CAT_LABEL[g["category"]]}</p>'
            f'<h3 class="gcard-name"><a href="{url}">{guest_display(g)}</a></h3>'
            f'<p class="gcard-role">{g["headline"]}</p>'
            + (f'<p class="gcard-aff">{aff}</p>' if aff and aff not in g["headline"] else "")
            + f'<p class="gcard-meta">{_guest_meta_line(g)}</p></div></div>'
            f'<div class="gcard-act">{"".join(acts)}</div></li>')

def _person_node(g, depth=0):
    p = {"@type": "Person", "@id": guest_id(g), "name": _faq_plain(g["name"]),
         "jobTitle": _faq_plain(g["headline"]), "description": _faq_plain(g["on_the_show"]),
         "url": f"https://www.firstrehabnpb.com/{guest_url(g)}"}
    if g["honorific"] == "Dr.":
        p["honorificPrefix"] = "Dr."
    if g.get("credentials"):
        p["honorificSuffix"] = g["credentials"]
    ph = g.get("photo") or {}
    if ph.get("src"):
        p["image"] = f"https://www.firstrehabnpb.com/{ph['src']}-480.jpg"
    aff = g.get("affiliation") or {}
    if aff.get("name"):
        org = {"@type": "Organization", "name": _faq_plain(aff["name"])}
        if aff.get("url"):
            org["url"] = aff["url"]
        p["worksFor"] = org
    same = [l["url"] for l in g.get("links", []) if "firstrehabnpb.com" not in l["url"]]
    if same:
        p["sameAs"] = same
    return p

def build_guests():
    """/guests.html directory + /guests/<slug>.html profile per guest.

    Modelled on the Executives Association members directory Nick pointed at:
    search box, filter chips with counts, portrait cards with an action bar,
    and a full profile page behind each card."""
    import json as _json
    counts = {k: sum(1 for g in GUESTS if g["category"] == k) for k, _ in GUEST_CATEGORIES}
    chips = [f'<button type="button" class="gchip" data-cat="all" aria-pressed="true">All <span>{len(GUESTS)}</span></button>']
    chips += [f'<button type="button" class="gchip" data-cat="{k}" aria-pressed="false">{lbl} <span>{counts[k]}</span></button>'
              for k, lbl in GUEST_CATEGORIES if counts[k]]
    cards = "".join(_guest_dir_card(g) for g in GUESTS)
    crumbs = '<div class="crumbs"><a href="/">Home</a> / <a href="podcast.html">Podcast</a> / Guests</div>'
    body = f"""
<main>
{page_hero("Pain 2 Power Guests", "Meet the <em class='accent'>Guests</em>",
  f"{len(GUESTS)} surgeons, specialists and people with a story worth hearing. Every guest who has joined Dr. Dave Kashuba and Mike McGann on Pain 2 Power, with their background, what they said on air and their clips from the show.", crumbs)}
<section class="section">
  <div class="wrap">
    <h2 class="sr-only">Find a guest</h2>
    <div class="gdir-tools">
      <label class="gdir-search">{_gicon("search", 18)}<span class="sr-only">Search guests</span>
        <input type="search" placeholder="Search by name, specialty or practice" autocomplete="off" data-gsearch></label>
      <div class="gchips" role="group" aria-label="Filter by specialty">{"".join(chips)}</div>
      <p class="gdir-count" aria-live="polite" data-gcount>Showing all {len(GUESTS)} guests</p>
    </div>
    <ul class="gdir-grid" data-ggrid>{cards}</ul>
    <p class="gdir-empty" data-gempty hidden>No guest matches that search. Try a name, a body part or a practice.</p>
    <p class="guest-note">Photos are each guest&rsquo;s own practice headshot, credited on their profile, or a still from the Pain 2 Power studio. Background details come from each guest&rsquo;s own practice, employer and professional pages, linked on their profile. Pain 2 Power is for general education, not medical advice; talk with your own doctor about your care.</p>
  </div>
</section>
{cta_band(0)}
</main>
<script src="assets/js/guests.js?v={asset_v('assets/js/guests.js')}" defer></script>
"""
    page = {"@type": "CollectionPage", "@id": "https://www.firstrehabnpb.com/guests.html",
            "name": "Pain 2 Power Podcast Guests", "url": "https://www.firstrehabnpb.com/guests.html",
            "publisher": {"@id": "https://www.firstrehabnpb.com/#organization"},
            "about": {"@type": "PodcastSeries", "name": "Pain 2 Power", "url": "https://www.firstrehabnpb.com/podcast.html"},
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": f"https://www.firstrehabnpb.com/{guest_url(g)}",
                 "name": _faq_plain(guest_display(g))} for i, g in enumerate(GUESTS)]}}
    ld = '<script type="application/ld+json">' + _json.dumps({"@context": "https://schema.org", "@graph": [page]}, ensure_ascii=False) + '</script>\n'
    write("guests.html",
          head("Pain 2 Power Podcast Guests | First Rehab North Palm Beach",
               "Meet the surgeons and specialists who have joined Dr. Dave Kashuba on the Pain 2 Power podcast: background, what they said on air, and their clips.",
               canonical="guests.html", og_image="assets/media/podcast-cover.jpg",
               extra_schema=ld + breadcrumb_schema([("Home", ""), ("Podcast", "podcast.html"), ("Guests", "guests.html")]))
          + nav(0) + body + footer(0))
    for i, g in enumerate(GUESTS):
        _build_guest_page(g, GUESTS[i - 1] if i else None, GUESTS[i + 1] if i + 1 < len(GUESTS) else None)

def _photo_credit(g):
    ph = g.get("photo") or {}
    if ph.get("credit"):
        return f'<p class="gp-credit">Photo courtesy of {ph["credit"]}</p>'
    if ph.get("src"):
        return '<p class="gp-credit">Photo from the Pain 2 Power studio</p>'
    return ""

def _build_guest_page(g, prev_g, next_g):
    import json as _json
    from urllib.parse import urlparse
    d, display = 1, guest_display(g)
    aff = g.get("affiliation") or {}
    cat = GUEST_CAT_LABEL[g["category"]]
    eps = _guest_episode_links(g)
    # Hero line: role, practice (linked), city.
    role = [g["headline"]]
    if aff.get("name") and aff["name"] not in g["headline"]:
        role.append(f'<a href="{aff["url"]}" target="_blank" rel="noopener">{aff["name"]}</a>' if aff.get("url") else aff["name"])
    if g.get("location"):
        role.append(g["location"])
    quote = (f'<blockquote class="guest-quote">&ldquo;{g["on_the_show_quote"]}&rdquo;</blockquote>'
             if g.get("on_the_show_quote") else "")
    facts = "".join(f'<li>{b["text"]}</li>' for b in g.get("background", []))
    bg = (f'<section class="gp-sec"><h2>Background</h2><ul class="guest-facts">{facts}</ul></section>' if facts else "")
    # Full episode video(s): click-to-load facade, same as /videos.html.
    vids = "".join(_video_card(v) for _, _, v, _ in eps if v)
    vid_sec = (f'<section class="gp-sec"><h2>Watch the episode</h2><div class="gp-vids">{vids}</div></section>' if vids else "")
    # Clips: the Shorts we posted from their episode, vertical, click-to-load.
    clips = g.get("clips", [])
    CLIPS_SHOWN = 6
    clip_html = "".join(
        f'<li class="gclip"{" data-gmore hidden" if i >= CLIPS_SHOWN else ""}><button class="vid-facade gclip-facade" type="button" '
        f'data-embed="https://www.youtube-nocookie.com/embed/{c["youtube_id"]}?autoplay=1&amp;rel=0" '
        f'data-title="{_faq_plain(c["title"])} — Pain 2 Power clip">'
        f'<img src="https://i.ytimg.com/vi/{c["youtube_id"]}/oar2.jpg" alt="" loading="lazy" width="360" height="640" '
        f'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/{c["youtube_id"]}/hqdefault.jpg\'">'
        f'<span class="gclip-play" aria-hidden="true">&#9654;</span><span class="sr-only">Play clip: {c["title"]}</span></button>'
        f'<p class="gclip-title">{c["title"]}</p></li>' for i, c in enumerate(clips))
    more_btn = (f'<button type="button" class="btn btn-ink gclips-more" data-gmore-btn>Show all {len(clips)} clips</button>'
                if len(clips) > CLIPS_SHOWN else "")
    clip_sec = (f'<section class="gp-sec"><div class="gp-sec-head"><h2>Clips from the show</h2>'
                f'<a class="text-link" href="{YOUTUBE}/shorts" target="_blank" rel="noopener">All clips on YouTube</a></div>'
                f'<ul class="gclips">{clip_html}</ul>{more_btn}</section>' if clips else "")
    # Spotify players for each episode.
    listen = ""
    for e, spot, _, recap in eps:
        import re as _re
        m = _re.search(r"episode/([A-Za-z0-9]+)", spot or "")
        if m:
            listen += (f'<iframe class="pod-embed" src="https://open.spotify.com/embed/episode/{m.group(1)}?utm_source=generator&amp;theme=0" '
                       f'width="100%" height="152" frameborder="0" loading="lazy" style="border-radius:14px;" '
                       f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" title="{e} with {display} on Spotify"></iframe>')
        if recap:
            listen += f'<p class="pod-recap"><a href="../blog/{recap}.html">Read the recap: {BLOG_POSTS[recap]["title"]}</a></p>'
    listen_sec = f'<section class="gp-sec"><h2>Listen</h2>{listen}</section>' if listen else ""
    # Aside: portrait, quick facts, links.
    rows = [("Specialty", cat)]
    if g.get("credentials"):
        rows.append(("Credentials", g["credentials"]))
    if aff.get("name"):
        rows.append(("Practice", aff["name"]))
    if g.get("location"):
        rows.append(("Location", g["location"]))
    rows.append(("On Pain 2 Power", ", ".join(g["episodes"])))
    facts_tbl = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    links = "".join(
        f'<a class="guest-link" href="{l["url"]}" target="_blank" rel="noopener">{l.get("label") or GUEST_LINK_LABELS.get(l["type"], "Link")}</a>'
        for l in g.get("links", []))
    links_html = f'<h3 class="gp-aside-h">Find {g["name"].split()[0]} online</h3><div class="guest-links">{links}</div>' if links else ""
    hosts = []
    for b in g.get("background", []):
        h = urlparse(b["source"]).netloc.replace("www.", "")
        if h and h not in [x for x, _ in hosts]:
            hosts.append((h, b["source"]))
    sources = ('<p class="guest-sources">Background sources: ' + " ".join(
        f'<a href="{u}" target="_blank" rel="noopener">{h}</a>' for h, u in hosts) + "</p>") if hosts else ""
    def _nav(o, rel):
        if not o:
            return "<span></span>"
        return (f'<a class="gp-nav-{rel}" href="{o["slug"]}.html"><span class="gp-nav-k">{"Previous" if rel == "prev" else "Next"} guest</span>'
                f'<span class="gp-nav-n">{guest_display(o)}</span></a>')
    crumbs = (f'<div class="crumbs"><a href="/">Home</a> / <a href="../podcast.html">Podcast</a> / '
              f'<a href="../guests.html">Guests</a> / {g["name"]}</div>')
    body = f"""
<main>
{page_hero(cat, display, " &middot; ".join(role), crumbs)}
<section class="section">
  <div class="wrap gp-layout">
    <div class="gp-main">
      <section class="gp-sec"><h2>On the show</h2>{quote}<p>{g["on_the_show"]}</p></section>
      {bg}
      {vid_sec}
      {clip_sec}
      {listen_sec}
      {sources}
    </div>
    <aside class="gp-aside">
      <div class="side-card gp-card">
        {guest_portrait(g, depth=d, size=480, cls="gp gp--lg")}
        {_photo_credit(g)}
        <dl class="gp-facts">{facts_tbl}</dl>
        {links_html}
      </div>
    </aside>
  </div>
  <div class="wrap gp-nav">{_nav(prev_g, "prev")}<a class="btn btn-ink" href="../guests.html">All guests</a>{_nav(next_g, "next")}</div>
</section>
{cta_band(d)}
</main>
<script src="../assets/js/videos.js?v={asset_v('assets/js/videos.js')}" defer></script>
<script src="../assets/js/guests.js?v={asset_v('assets/js/guests.js')}" defer></script>
"""
    first = (g["name"] if g["honorific"] != "Dr." else f'Dr. {g["name"]}')
    title = f"{first} | Pain 2 Power Podcast Guest"
    if len(title) > 62:
        title = f"{first} | Pain 2 Power Guest"
    desc = _faq_plain(g["on_the_show"])
    desc = (desc[:152].rsplit(" ", 1)[0] + "...") if len(desc) > 155 else desc
    og = (g.get("photo") or {}).get("src")
    profile = {"@type": "ProfilePage", "@id": f"https://www.firstrehabnpb.com/{guest_url(g)}",
               "url": f"https://www.firstrehabnpb.com/{guest_url(g)}", "name": _faq_plain(display),
               "mainEntity": {"@id": guest_id(g)},
               "isPartOf": {"@id": "https://www.firstrehabnpb.com/guests.html"}}
    ld = ('<script type="application/ld+json">'
          + _json.dumps({"@context": "https://schema.org", "@graph": [profile, _person_node(g)]}, ensure_ascii=False)
          + '</script>\n')
    write(guest_url(g),
          head(title, desc, depth=d, canonical=guest_url(g),
               og_image=(f"{og}-480.jpg" if og else "assets/media/podcast-cover.jpg"), page_type="profile",
               extra_schema=ld + breadcrumb_schema([("Home", ""), ("Podcast", "podcast.html"), ("Guests", "guests.html"), (_faq_plain(g["name"]), guest_url(g))]))
          + nav(d) + body + footer(d))

def build_meta():
    base = "https://www.firstrehabnpb.com"
    write("site.webmanifest", '''{
  "name": "First Rehabilitation of North Palm Beach",
  "short_name": "First Rehab",
  "description": "Physical therapy, occupational therapy, hand therapy & wellness since 1991.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#F6F1E7",
  "theme_color": "#0E3A47",
  "icons": [
    { "src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
''')
    pages = ["", "about.html", "contact.html", "careers.html", "faq.html", "first-visit.html", "insurance.html", "podcast.html", "videos.html", "guests.html", "blog/index.html", "treatments/index.html", "exercises.html", "glossary.html", "things-to-do.html"]
    pages += [guest_url(g) for g in GUESTS]
    pages += [f"services/{s}.html" for s in SERVICES]
    pages += [f"locations/{s}.html" for s in LOCATIONS]
    pages += [f"treatments/{s}.html" for s in CONDITIONS]
    pages += [f"blog/{s}.html" for s in BLOG_POSTS]
    from datetime import date as _date
    lastmod = _lastmods(pages, _date.today().isoformat())
    urls = "".join(f"  <url><loc>{base}/{p}</loc><lastmod>{lastmod[p]}</lastmod></url>\n" for p in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    ai_crawlers = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot",
                   "ClaudeBot", "Claude-User", "Google-Extended", "Bingbot",
                   "DuckDuckBot", "Applebot", "Applebot-Extended", "cohere-ai",
                   "meta-externalagent"]
    ai_blocks = "".join(f"User-agent: {ua}\nAllow: /\n\n" for ua in ai_crawlers)
    write("robots.txt",
          "# All crawlers welcome, including AI/answer-engine bots (explicit below).\n"
          "User-agent: *\nAllow: /\n\n"
          f"{ai_blocks}Sitemap: {base}/sitemap.xml\n")
    cond_lines = "\n".join(f"- {c['name']}: {base}/treatments/{slug}.html" for slug, c in CONDITIONS.items())
    blog_lines = "\n".join(f"- {p['title']}: {base}/blog/{slug}.html" for slug, p in BLOG_POSTS.items())
    write("llms.txt", f'''# First Rehabilitation of North Palm Beach

> Family-owned outpatient rehabilitation clinic in North Palm Beach, Florida, serving
> the Palm Beaches since 1991. NOT affiliated with any similarly named clinic; we are
> an independent practice founded and led by David Kashuba, Ph.D., occupational therapist.

## Key facts
- Address: 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408
- Phone: 561-624-4263 · Fax: 561-840-4234 · Email: firstrehabnpb@gmail.com
- Hours: Monday-Friday, 8:00 AM - 5:30 PM; Saturday, 8:00 AM - 12:30 PM
- Free consultations available (call to schedule)
- Founded: 1991 (family-owned and operated)
- Website: {base}/

## Services (all under one roof)
- Physical Therapy: {base}/services/physical-therapy.html
- Occupational Therapy: {base}/services/occupational-therapy.html
- Certified Hand Therapy (led by Laura Drumm, CHT; custom splints made in-clinic): {base}/services/hand-therapy.html
- On-site Wellness & Gym program: {base}/services/wellness.html

## Named clinicians (credentials on the About page)
David Kashuba, Ph.D., OTR (CEO, Occupational Therapist); Kayla Dorsey, PT, DPT and Logan Van Sant, PT, DPT
(Physical Therapists); Joan "Joni" Janik, OTD (Occupational Therapist); Laura Drumm, MS, OTR/L, CHT, CLT (Certified Hand
Therapist); Nick Kashuba (COO). About: {base}/about.html

## Insurance accepted
Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare,
VA Community Care Network (VACCN), workers' compensation, self-pay.
Medicare-certified Comprehensive Outpatient Rehabilitation Facility (CORF).
2026 Medicare guide (deductible, 20% coinsurance, KX threshold, Medicare Advantage):
{base}/insurance.html#medicare-guide

## Areas served
North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, Tequesta, Lake Park,
Palm Beach, Palm Beach Shores, Riviera Beach, West Palm Beach.
Area pages: {base}/locations/palm-beach-gardens.html, {base}/locations/jupiter.html,
{base}/locations/juno-beach.html, {base}/locations/tequesta.html,
{base}/locations/lake-park.html, {base}/locations/palm-beach.html,
{base}/locations/west-palm-beach.html, {base}/locations/riviera-beach.html

## Conditions treated (dedicated pages)
{cond_lines}

## Blog (patient education, reviewed by our clinical team)
{blog_lines}

## Answers to common questions
73-question FAQ (referrals, insurance, OT vs PT, certified hand therapy, costs):
{base}/faq.html
Patient glossary of therapy and insurance terms: {base}/glossary.html

## Podcast
Pain 2 Power, hosted by Dr. Dave Kashuba with Mike McGann. Saturdays 8:30 AM on
100.3 Legends Radio; all episodes: {base}/podcast.html; every guest, with their background and practice: {base}/guests.html
''')

    body = f"""
<main>
{page_hero("404", "This Page Took a <em class='accent'>Wrong Turn</em>",
  "The page you're looking for isn't here — but your recovery path is just a click away.")}
<section class="section center">
  <div class="wrap">
    <a class="btn btn-coral" href="/">Back to Home <span class="arr">&rarr;</span></a>
  </div>
</section>
</main>
"""
    write("404.html",
          head("Page Not Found | First Rehabilitation of North Palm Beach",
               "That page took a wrong turn. Find physical therapy, occupational therapy, hand therapy, and wellness services at First Rehabilitation of North Palm Beach.",
               robots="noindex") + nav(0, solid=True) + body + footer(0))

def check_episode_video_sync():
    """Warn when EPISODES and VIDEOS have drifted apart.

    Every new episode needs both an EPISODES[0] entry (Spotify) and a VIDEOS
    entry (YouTube) added together per the release-cycle doc in CLAUDE.md —
    but Episodes 11 and 12 both shipped with the Spotify half only, and the
    gap sat unnoticed for days because nothing surfaced it at build time.
    This can't catch every case (a same-day episode's YouTube video may
    genuinely not be up yet), so it warns instead of failing the build.
    """
    ep_num = lambda label: int(label.split()[-1])
    video_labels = {v["ep"] for v in VIDEOS}
    if not video_labels:
        return
    earliest_video_ep = min(ep_num(l) for l in video_labels)
    episode_labels = {e[0] for e in EPISODES if ep_num(e[0]) >= earliest_video_ep}
    missing = sorted(episode_labels - video_labels, key=ep_num, reverse=True)
    if missing:
        print(f"\n WARNING: in EPISODES (Spotify) but missing from VIDEOS (YouTube): {', '.join(missing)}")
        print("   If the YouTube video is live, add its VIDEOS entry now — see 'Automating the episode metadata' in CLAUDE.md.")

def build_staff_leads():
    # Front-desk lead inbox. Not a public page: unlinked, noindex, never in the
    # sitemap, and deliberately carries NO analytics tags (GA4 / Vercel) and no
    # intake chat, because it renders patient contact details. The page holds no
    # data or secret of its own. Access is enforced in Supabase: rows are readable
    # only by signed-in users listed in public.lead_staff, and the only write path
    # is the public.set_lead_status() RPC (see docs/LEAD-INBOX.md).
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lead Inbox | First Rehab Staff</title>
<meta name="description" content="Front-desk lead inbox for First Rehabilitation staff.">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#0E3A47">
<link rel="icon" href="../assets/icons/favicon.ico?v=6" sizes="any">
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/playfair-display-latin-700-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="../assets/fonts/inter-latin-400-normal.woff2" crossorigin>
<link rel="stylesheet" href="../assets/css/styles.css?v={asset_v('assets/css/styles.css')}">
<link rel="stylesheet" href="../assets/css/staff.css?v={asset_v('assets/css/staff.css')}">
</head>
<body>
<main id="main" class="staff-wrap">
  <div id="staff-app"><noscript><p class="staff-empty">The lead inbox needs JavaScript.</p></noscript></div>
</main>
<script src="../assets/js/staff-leads.js?v={asset_v('assets/js/staff-leads.js')}" defer></script>
</body>
</html>
"""
    full = os.path.join(ROOT, "staff/leads.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(page)
    print("wrote staff/leads.html")

if __name__ == "__main__":
    build_staff_leads()
    build_home()
    build_services()
    build_conditions()
    build_locations()
    build_about()
    build_podcast()
    build_faq()
    build_contact()
    build_blog()
    build_careers()
    build_first_visit()
    build_insurance()
    build_glossary()
    build_things_to_do()
    build_videos()
    build_guests()
    build_exercises()
    build_meta()
    check_episode_video_sync()
    print("\nDone. Open index.html or deploy the folder to Vercel.")
