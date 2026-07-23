#!/usr/bin/env python3
"""
Palm Beach Neurology & Premier Research Institute — static site generator.
Run `python3 build.py`; every page regenerates in place.

Engineered on the First Rehabilitation of North Palm Beach design system
(same editorial luxury: Playfair Display + Inter, film grain, scroll
choreography, interactive anatomy map) and re-themed to the Palm Beach
Neurology brand — beachy warm sand + deep coastal teal + sea-green, with a
synapse field replacing the lighthouse beam and a brain/nervous-system map
replacing the body map.

------------------------------------------------------------------------------
PENDING OWNER VERIFICATION (facts gathered from Google/Healthgrades because the
live site blocks automated access — CONFIRM before pointing the real domain here):
  * Provider roster & exact credentials/titles (see DOCTORS below)
  * "Premier" vs "Premiere" Research Institute spelling (their title tag uses
    "Premiere"; standard English is "Premier") -> set BRAND_SUB accordingly
  * Office hours (shown as "Call for hours" until confirmed)
  * In-house diagnostics offered (EMG/EEG/Ees, infusions, imaging)
  * Patient Portal login URL (PORTAL placeholder below)
  * Fax number, email, social links
  * Exact appointment offerings (FREE Memory Screen 30min + New Patient 1hr are
    confirmed from their live Appointments page screenshot)
------------------------------------------------------------------------------
"""
import os, html, hashlib as _hashlib, json as _json, re as _re

ROOT = os.path.dirname(os.path.abspath(__file__))

BRAND = "Palm Beach Neurology"
BRAND_SUB = "& Premiere Research Institute"
LEGAL = "Palm Beach Neurology & Premiere Research Institute"
TAGLINE = "Stay Sharp. Stay in Control."
PHONE = "561-845-0500"
PHONE_TEL = "+15618450500"
EMAIL = "info@palmbeachneurology.com"             # VERIFY
ADDR_STREET = "4631 N Congress Ave"
ADDR_CITY = "West Palm Beach"
ADDR_STATE = "FL"
ADDR_ZIP = "33407"
RESEARCH_URL = "https://www.premiereresearchinstitute.com/"
FORMS_PDF = "assets/forms/new-patient-paperwork.pdf"
PORTAL = "patient-center.html"                     # interim -> replace with real EMR portal login URL
BASE = "https://www.palmbeachneurology.com"
THEME_COLOR = "#0F3A46"
MAPS_EMBED = ("https://www.google.com/maps?q=4631+N+Congress+Ave+West+Palm+Beach+FL+33407&output=embed")
MAPS_LINK = ("https://www.google.com/maps/search/?api=1&query=4631+N+Congress+Ave+West+Palm+Beach+FL+33407")

# ----------------------------------------------------------------------------
# ASSET CACHE-BUSTING
# ----------------------------------------------------------------------------
def _v(path):
    with open(path, "rb") as f:
        return _hashlib.sha256(f.read()).hexdigest()[:8]
ASSET_V = {}
def asset_v(path):
    if path not in ASSET_V:
        try:
            ASSET_V[path] = _v(os.path.join(ROOT, path))
        except FileNotFoundError:
            ASSET_V[path] = "1"
    return ASSET_V[path]

FAVICON_V = "1"

# ----------------------------------------------------------------------------
# ORG SCHEMA + <head>
# ----------------------------------------------------------------------------
ORG_ID = f"{BASE}/#organization"
ORG_REF = {"@id": ORG_ID}

def _org_schema_str():
    data = {
        "@context": "https://schema.org",
        "@type": ["MedicalClinic", "Physician", "MedicalBusiness"],
        "@id": ORG_ID,
        "name": LEGAL,
        "alternateName": ["Palm Beach Neurology", "Premiere Research Institute", "PBN"],
        "description": ("Comprehensive neurology practice in West Palm Beach, Florida — one of the "
                        "most experienced neurological practices in the country, with 25+ years "
                        "caring for the brain, spine, and nervous system, plus an on-site clinical-"
                        "research institute. We treat the patient, not just the disease."),
        "url": BASE + "/",
        "logo": f"{BASE}/assets/media/logo.png",
        "image": f"{BASE}/assets/media/og-cover.jpg",
        "telephone": "+1-" + PHONE,
        "email": EMAIL,
        "medicalSpecialty": ["Neurologic"],
        "priceRange": "$$",
        "isAcceptingNewPatients": True,
        "slogan": "Treating the patient, not just the disease.",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDR_STREET,
            "addressLocality": ADDR_CITY,
            "addressRegion": ADDR_STATE,
            "postalCode": ADDR_ZIP,
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 26.7717, "longitude": -80.0925},
        "hasMap": MAPS_LINK,
        "areaServed": [{"@type": "City", "name": c} for c in [
            "West Palm Beach", "Palm Beach", "Palm Beach Gardens", "Wellington",
            "Royal Palm Beach", "Lake Worth", "Boynton Beach", "Jupiter",
            "North Palm Beach", "Greenacres"]],
        "sameAs": [RESEARCH_URL],
    }
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>"

def head(title, desc, depth=0, canonical="", og_image="assets/media/og-cover.jpg",
         page_type="website", extra_schema=""):
    p = "../" * depth
    canon = f"{BASE}/{canonical}" if canonical else BASE + "/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{html.escape(LEGAL)}">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="West Palm Beach">
<meta property="og:type" content="{page_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{html.escape(BRAND)}">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{BASE}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}/{og_image}">
<meta name="theme-color" content="{THEME_COLOR}">
<link rel="icon" href="{p}assets/icons/favicon.ico?v={FAVICON_V}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/icons/icon-32.png?v={FAVICON_V}">
<link rel="icon" type="image/png" sizes="16x16" href="{p}assets/icons/icon-16.png?v={FAVICON_V}">
<link rel="apple-touch-icon" sizes="180x180" href="{p}assets/icons/apple-touch-icon.png?v={FAVICON_V}">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/playfair-display-latin-700-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{p}assets/fonts/inter-latin-400-normal.woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/styles.css?v={asset_v('assets/css/styles.css')}">
{_org_schema_str()}
{extra_schema}</head>
<body>
"""

# ----------------------------------------------------------------------------
# NAV / FOOTER / SHARED
# ----------------------------------------------------------------------------
def nav(depth=0, solid=False):
    p = "../" * depth
    cls = "site-header solid" if solid else "site-header"
    cond_links = "".join(
        f'<a href="{p}conditions/{slug}.html">{c["nav"]}</a>' for slug, c in CONDITIONS.items())
    return f"""
<header class="{cls}">
  <a class="skip-link" href="#main">Skip to main content</a>
  <div class="wrap nav-bar">
    <a class="brand" href="{p}index.html" aria-label="{html.escape(BRAND)} home">
      {brand_mark('nav')}
      <span class="brand-text">
        <span class="brand-name">Palm Beach Neurology</span>
        <span class="brand-sub">Premier Research Institute</span>
      </span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav-el" aria-label="Main menu">
    <ul class="nav-links">
      <li><a class="nav-item" href="{p}index.html">Home</a></li>
      <li>
        <a class="nav-item" href="{p}conditions/index.html">Conditions</a>
        <div class="dropdown"><div class="dd-cols">{cond_links}</div></div>
      </li>
      <li><a class="nav-item" href="{p}services.html">Services</a></li>
      <li><a class="nav-item" href="{p}our-doctors.html">Our Doctors</a></li>
      <li><a class="nav-item" href="{p}clinical-research.html">Research</a></li>
      <li>
        <a class="nav-item" href="{p}appointments.html">Patients</a>
        <div class="dropdown">
          <a href="{p}appointments.html">Appointments</a>
          <a href="{p}patient-center.html">Patient Center &amp; Forms</a>
          <a href="{p}faq.html">FAQ</a>
        </div>
      </li>
      <li><a class="nav-item" href="{p}contact.html">Contact</a></li>
    </ul>
    </nav>
    <a class="btn btn-coral nav-cta-btn" href="{p}appointments.html">Request Appointment</a>
  </div>
</header>
"""

def footer(depth=0):
    p = "../" * depth
    cond_links = "".join(
        f'<li><a href="{p}conditions/{slug}.html">{c["nav"]}</a></li>'
        for slug, c in list(CONDITIONS.items())[:7])
    areas = ["West Palm Beach", "Palm Beach", "Palm Beach Gardens", "Wellington",
             "Royal Palm Beach", "Lake Worth", "Jupiter", "Boynton Beach"]
    area_links = "".join(f"<li>{a}</li>" for a in areas)
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="f-brand">
        {brand_mark('footer')}
        <div class="brand-name">Palm Beach Neurology</div>
        <div class="brand-tag">Treating the patient, not just the disease.</div>
        <p>Board-certified neurology and on-site clinical research in West Palm Beach —
        advanced, compassionate care for the brain, spine, and nervous system for more than 25 years.</p>
      </div>
      <div>
        <h3 class="f-head">Conditions</h3>
        <ul>{cond_links}<li><a href="{p}conditions/index.html">All Conditions &rarr;</a></li></ul>
      </div>
      <div>
        <h3 class="f-head">Practice</h3>
        <ul>
          <li><a href="{p}services.html">Services</a></li>
          <li><a href="{p}our-doctors.html">Our Doctors</a></li>
          <li><a href="{p}clinical-research.html">Clinical Research</a></li>
          <li><a href="{p}appointments.html">Appointments</a></li>
          <li><a href="{p}patient-center.html">Patient Center</a></li>
          <li><a href="{p}faq.html">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h3 class="f-head">Areas We Serve</h3>
        <ul class="f-areas">{area_links}</ul>
      </div>
      <div>
        <h3 class="f-head">Visit Us</h3>
        <ul class="f-contact">
          <li>{ADDR_STREET}<br>{ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}</li>
          <li>Phone: <a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <span>&copy; 2026 {html.escape(LEGAL)}. All rights reserved.</span>
      <span>Board-certified neurology &middot; West Palm Beach, FL</span>
    </div>
  </div>
</footer>
<a class="mobile-call" href="tel:{PHONE_TEL}" aria-label="Call {html.escape(BRAND)} now at {PHONE}"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.4 21 3 13.6 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg><span>Call Now</span></a>
<script src="{p}assets/js/main.js?v={asset_v('assets/js/main.js')}"></script>
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
"""

def brand_mark(variant="nav"):
    """Inline SVG brain-flower mark (no external logo file needed). Two-tone
    teal/sea-green petals forming a brain, echoing the practice's logo."""
    cls = {"nav": "brand-mark", "footer": "brand-mark f-mark", "hero": "brand-mark hero-mark"}[variant]
    petals = ""
    import math
    for i in range(6):
        ang = math.radians(i * 60 - 90)
        cx = 32 + 15 * math.cos(ang)
        cy = 32 + 15 * math.sin(ang)
        fill = "var(--sea)" if i % 2 == 0 else "var(--leaf)"
        petals += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="11.5" fill="{fill}" opacity="0.9"/>'
    return (f'<svg class="{cls}" viewBox="0 0 64 64" role="img" aria-label="{html.escape(BRAND)} logo" '
            f'width="52" height="52">{petals}'
            f'<circle cx="32" cy="32" r="12" fill="var(--ink)"/>'
            f'<path d="M27 27c-2 0-3.4 1.4-3.4 3.2 0 .5.1 1 .3 1.4-1 .5-1.6 1.5-1.6 2.6 0 1.7 1.4 3 3.2 3 '
            f'M37 27c2 0 3.4 1.4 3.4 3.2 0 .5-.1 1-.3 1.4 1 .5 1.6 1.5 1.6 2.6 0 1.7-1.4 3-3.2 3 '
            f'M32 24.5v15" fill="none" stroke="var(--cream)" stroke-width="1.5" stroke-linecap="round"/>'
            f'</svg>')

def cta_band(depth=0,
             heading='Clarity for the mind starts with <em>one conversation.</em>',
             sub="Request an appointment today — new patients are welcome, and our team will help verify your insurance and find a time that works."):
    p = "../" * depth
    return f"""
<section class="cta-band">
  <div class="hero-fallback"></div>
  {neuro_field(0.6)}
  <div class="wrap cta-inner reveal">
    <h2>{heading}</h2>
    <p>{sub}</p>
    <div class="hero-ctas" style="justify-content:center;">
      <a class="btn btn-coral" href="{p}appointments.html">Request Appointment <span class="arr">&rarr;</span></a>
      <a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a>
    </div>
  </div>
</section>
"""

def page_hero(eyebrow, title, lede, crumbs_html=""):
    return f"""
<section class="page-hero">
  <div class="hero-fallback"></div>
  {neuro_field(0.5)}
  <div class="wrap">
    {crumbs_html}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""

# ----------------------------------------------------------------------------
# SIGNATURE MOTIF: synapse field (aura + neural constellation)
# ----------------------------------------------------------------------------
def neuro_field(opacity=0.6):
    import random
    rng = random.Random(7)          # fixed seed -> deterministic, reproducible build
    W, H = 1200, 620
    nodes = []
    # loose grid with jitter so the constellation feels organic but even
    for gx in range(6):
        for gy in range(3):
            x = 90 + gx * 205 + rng.randint(-45, 45)
            y = 90 + gy * 210 + rng.randint(-45, 45)
            nodes.append((x, y))
    edges = []
    for i, (x1, y1) in enumerate(nodes):
        d = sorted(range(len(nodes)),
                   key=lambda j: (nodes[j][0]-x1)**2 + (nodes[j][1]-y1)**2)
        for j in d[1:3]:
            if (min(i, j), max(i, j)) not in edges:
                edges.append((min(i, j), max(i, j)))
    def _edge(k, a, b):
        cls = ' class="edge-lit"' if k % 5 == 0 else ''
        return f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}"{cls}/>'
    lines = "".join(_edge(k, a, b) for k, (a, b) in enumerate(edges))
    circ = ""
    for k, (x, y) in enumerate(nodes):
        cls = "node"
        if k % 3 == 0:
            cls += " pulse"
        if k % 4 == 0:
            cls += " lit"
        dur = 3.6 + (k % 5) * 0.6
        r = 2.6 if k % 3 else 3.6
        circ += f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}" style="--pulse-dur:{dur}s"/>'
    return (f'<div class="neuro-field" aria-hidden="true" style="opacity:{opacity}">'
            f'<div class="neuro-aura"></div>'
            f'<svg class="neuro-net" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
            f'{lines}{circ}</svg></div>')

# ----------------------------------------------------------------------------
# BRAIN / NERVOUS-SYSTEM MAP (interactive)
# ----------------------------------------------------------------------------
def brainmap_svg():
    # (key, x, y, label) — positions over a top-down brain + descending spine
    spots = [
        ("migraine",   170,  92, "Headache &amp; Migraine"),
        ("memory",     120, 150, "Memory &amp; Alzheimer's"),
        ("epilepsy",   224, 158, "Epilepsy"),
        ("movement",   170, 205, "Parkinson's"),
        ("stroke",     108, 214, "Stroke"),
        ("ms",         236, 118, "Multiple Sclerosis"),
        ("spine",      170, 384, "Neck &amp; Back"),
        ("neuropathy", 112, 556, "Neuropathy"),
    ]
    spot_links = {
        "migraine": "conditions/headaches-migraine.html",
        "memory": "conditions/memory-alzheimers.html",
        "epilepsy": "conditions/epilepsy-seizures.html",
        "movement": "conditions/parkinsons-movement.html",
        "stroke": "conditions/stroke.html",
        "ms": "conditions/multiple-sclerosis.html",
        "spine": "conditions/back-neck-pain.html",
        "neuropathy": "conditions/neuropathy.html",
    }

    def _chip(x, y, lbl):
        plain = html.unescape(lbl)
        w = round(len(plain) * 6.6 + 18)
        rx = x + 16 if x < 170 else x - 16 - w
        rx = max(20, min(rx, 320 - w))
        ry = y - 10
        return (f'<g class="bm-chip"><rect x="{rx}" y="{ry}" width="{w}" height="20" rx="10"/>'
                f'<text x="{rx + w/2}" y="{ry + 14}" text-anchor="middle">{lbl}</text></g>')

    spots_svg = "".join(
        f'''<a href="{spot_links[k]}" class="bm-spot" data-bm="{k}" aria-label="{lbl}">
        <circle class="hit" cx="{x}" cy="{y}" r="18" fill="#000" fill-opacity="0" pointer-events="all"/>
        <circle class="halo" cx="{x}" cy="{y}" r="10"/>
        <circle class="core" cx="{x}" cy="{y}" r="6"/>
        {_chip(x, y, lbl)}
        <title>{lbl}</title></a>''' for k, x, y, lbl in spots
    )

    # Top-down brain: two hemispheres, central fissure, suggested gyri
    brain = """
    <path class="bm-silhouette" d="M170,44
      C210,44 244,60 260,92 C276,122 274,146 268,164
      C282,178 286,204 272,224 C285,242 281,272 258,286
      C246,300 224,306 200,302 C190,314 150,314 140,302
      C116,306 94,300 82,286 C59,272 55,242 68,224
      C54,204 58,178 72,164 C66,146 64,122 80,92
      C96,60 130,44 170,44 Z"/>
    <path class="bm-fissure" d="M170,50 C177,96 163,132 170,172 C177,210 165,252 170,300"/>
    <path class="bm-gyrus" d="M120,86 C108,104 122,116 110,134"/>
    <path class="bm-gyrus" d="M148,74 C138,96 152,110 142,132"/>
    <path class="bm-gyrus" d="M220,86 C232,104 218,116 230,134"/>
    <path class="bm-gyrus" d="M192,74 C202,96 188,110 198,132"/>
    <path class="bm-gyrus" d="M100,150 C92,168 106,180 96,198"/>
    <path class="bm-gyrus" d="M240,150 C248,168 234,180 244,198"/>
    <path class="bm-gyrus" d="M132,196 C124,214 140,224 130,244"/>
    <path class="bm-gyrus" d="M208,196 C216,214 200,224 210,244"/>
    """
    # Brainstem + spine (rounded vertebrae) + a peripheral nerve branch
    stem = '<path class="bm-spine" d="M170,300 C170,320 168,336 170,352"/>'
    verts = "".join(
        f'<rect class="bm-vert" x="{170-11}" y="{y}" width="22" height="15" rx="6"/>'
        for y in range(356, 520, 22))
    nerve = ('<path class="bm-nerve" d="M170,470 C150,486 128,500 112,548"/>'
             '<path class="bm-nerve" d="M170,486 C190,502 210,516 226,560"/>')

    defs = ('<defs><linearGradient id="bmFig" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%" stop-color="rgba(243,236,220,0.20)"/>'
            '<stop offset="100%" stop-color="rgba(243,236,220,0.06)"/></linearGradient></defs>')
    return (f'<svg viewBox="0 0 340 600" role="group" '
            f'aria-label="Interactive brain and nervous-system map — choose an area of concern">'
            f'{defs}{brain}{stem}{verts}{nerve}{spots_svg}</svg>')

# ----------------------------------------------------------------------------
# UTIL
# ----------------------------------------------------------------------------
def _plain(s):
    return _re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&rsquo;", "'").replace("&ldquo;", '"').replace("&rdquo;", '"')

def linkify_phone(html_out):
    """Turn visible mentions of the phone number into tap-to-call links WITHOUT
    touching the <head> (meta/title/schema) or the insides of any tag/attribute —
    we only rewrite text nodes in the body, and never nest inside an existing link."""
    idx = html_out.find("</head>")
    head_part, rest = (html_out[:idx + 7], html_out[idx + 7:]) if idx != -1 else ("", html_out)
    protected = []
    def _protect(m):
        protected.append(m.group(0))
        return f"\x00{len(protected) - 1}\x00"
    # Protect existing anchors/scripts wholesale, then every remaining tag, so the
    # phone replacement can only land in real text between tags.
    rest = _re.sub(r"<(a|script)\b[^>]*>.*?</\1>", _protect, rest, flags=_re.S)
    rest = _re.sub(r"<[^>]+>", _protect, rest)
    rest = rest.replace(PHONE, f'<a href="tel:{PHONE_TEL}">{PHONE}</a>')
    rest = _re.sub(r"\x00(\d+)\x00", lambda m: protected[int(m.group(1))], rest)
    return head_part + rest

def write(path, content):
    if path.endswith(".html"):
        content = linkify_phone(content)
        content = content.replace("<main>", '<main id="main">', 1)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)

def breadcrumb_schema(items):
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": _plain(n),
                 "item": (BASE + "/" + u) if u else BASE + "/"}
                for i, (n, u) in enumerate(items)]}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>\n"

# ============================================================================
# CONTENT — CONDITIONS
# ============================================================================
CONDITIONS = {
    "headaches-migraine": {
        "name": "Headache &amp; Migraine",
        "nav": "Headache &amp; Migraine",
        "tag": "Headache Medicine",
        "lede": "Chronic migraine, tension headache, cluster headache, and post-traumatic "
                "headache — evaluated and managed by neurologists who take head pain seriously.",
        "intro": "Recurring headaches are not something to simply live with. Our neurologists "
                 "distinguish migraine from tension-type, cluster, and secondary headaches, then "
                 "build a plan that may combine trigger management, acute and preventive "
                 "medications, and the newer CGRP-targeted therapies and Botox for chronic migraine.",
        "symptoms": ["Throbbing or one-sided head pain", "Aura, light &amp; sound sensitivity",
                     "Nausea with headaches", "Headaches 15+ days a month", "\"Worst headache of my life\""],
        "approach": [
            ("Careful diagnosis", "We separate primary headache disorders from secondary causes and order imaging only when it will change the plan."),
            ("Preventive strategy", "Daily preventives, CGRP monoclonal antibodies, and Botox for chronic migraine — matched to your pattern."),
            ("Acute relief", "A rescue plan that actually works, so an attack doesn't cost you a day."),
        ],
    },
    "epilepsy-seizures": {
        "name": "Epilepsy &amp; Seizures",
        "nav": "Epilepsy &amp; Seizures",
        "tag": "Epilepsy",
        "lede": "Seizures and epilepsy diagnosed with EEG and imaging, then managed toward the "
                "goal every patient shares — no seizures, no side effects.",
        "intro": "A first seizure, or seizures that keep breaking through, deserve a neurologist's "
                 "evaluation. We use EEG and MRI to characterize seizure type, then tailor "
                 "anti-seizure medication and lifestyle guidance — and coordinate advanced options "
                 "for seizures that remain difficult to control.",
        "symptoms": ["Convulsions or staring spells", "Sudden confusion or déjà vu",
                     "Loss of awareness", "Unexplained falls", "Recurrent unusual sensations"],
        "approach": [
            ("Characterize the seizures", "EEG and high-resolution MRI to define seizure type and, when possible, the source."),
            ("Medication that fits your life", "Effective seizure control with the fewest side effects and drug interactions."),
            ("Safety &amp; driving guidance", "Clear counseling on triggers, safety, and Florida driving rules."),
        ],
    },
    "parkinsons-movement": {
        "name": "Parkinson's &amp; Movement Disorders",
        "nav": "Parkinson's &amp; Movement",
        "tag": "Movement Disorders",
        "lede": "Parkinson's disease, essential tremor, dystonia, and other movement disorders — "
                "diagnosed early and managed to keep you steady and independent.",
        "intro": "Tremor, stiffness, and slowness can have many causes. Our neurologists "
                 "distinguish Parkinson's disease from essential tremor and related conditions, "
                 "and manage them with medication, Botox for dystonia and tremor, and coordinated "
                 "therapy — helping you stay active and independent for as long as possible.",
        "symptoms": ["Resting tremor", "Stiffness or slow movement", "Shuffling or balance changes",
                     "Cramping or twisting postures", "Handwriting getting smaller"],
        "approach": [
            ("Precise diagnosis", "Sorting Parkinson's from essential tremor and mimics — the diagnosis drives everything."),
            ("Medication optimization", "Fine-tuned dopaminergic and symptomatic therapy as needs change over time."),
            ("Botox &amp; procedures", "Targeted injections for dystonia and tremor, and referral pathways for advanced therapies."),
        ],
    },
    "memory-alzheimers": {
        "name": "Memory Loss, Alzheimer's &amp; Dementia",
        "nav": "Memory &amp; Alzheimer's",
        "tag": "Cognitive Neurology",
        "lede": "Memory concerns evaluated thoroughly — because treatable causes are common, and "
                "early answers open the most doors, including new disease-modifying therapies.",
        "intro": "Not all memory loss is Alzheimer's, and not all of it is permanent. We evaluate "
                 "cognition carefully, screen for reversible contributors, and — when appropriate — "
                 "discuss the latest disease-modifying treatments and clinical-trial options through "
                 "our on-site research institute.",
        "symptoms": ["Forgetfulness affecting daily life", "Repeating questions", "Word-finding trouble",
                     "Getting lost in familiar places", "Personality or mood changes"],
        "approach": [
            ("Thorough cognitive work-up", "Testing plus a search for reversible causes — medications, thyroid, B12, sleep, mood."),
            ("A clear plan for the family", "Diagnosis, expectations, safety, and support — explained without jargon."),
            ("Access to new therapies", "Disease-modifying options and clinical trials via our Premier Research Institute."),
        ],
    },
    "multiple-sclerosis": {
        "name": "Multiple Sclerosis",
        "nav": "Multiple Sclerosis",
        "tag": "Neuroimmunology",
        "lede": "MS and related conditions managed with modern disease-modifying therapy and a "
                "long-term partnership focused on protecting function.",
        "intro": "Multiple sclerosis care has changed dramatically. We diagnose MS with MRI and "
                 "clinical evaluation, then match you to a modern disease-modifying therapy, manage "
                 "relapses and symptoms, and monitor over time — with access to MS clinical trials "
                 "through our research institute.",
        "symptoms": ["Numbness or tingling", "Vision changes in one eye", "Weakness or imbalance",
                     "Fatigue", "Heat-sensitive symptoms"],
        "approach": [
            ("Confident diagnosis", "MRI and clinical criteria to diagnose MS and rule out mimics."),
            ("Modern DMTs", "Selecting and monitoring disease-modifying therapy to reduce relapses and protect the brain."),
            ("Symptom &amp; relapse care", "Practical management of fatigue, spasticity, and flares."),
        ],
    },
    "stroke": {
        "name": "Stroke &amp; TIA",
        "nav": "Stroke &amp; TIA",
        "tag": "Vascular Neurology",
        "lede": "Stroke and TIA (\"mini-stroke\") follow-up and prevention — finding the cause and "
                "lowering the risk of the next one.",
        "intro": "After a stroke or TIA, the priority is preventing the next event. Our neurologists "
                 "investigate the underlying cause — blood pressure, heart rhythm, carotid disease, "
                 "and more — and build a prevention plan, while coordinating rehabilitation to help "
                 "you recover function.",
        "symptoms": ["Sudden weakness or numbness", "Face drooping", "Trouble speaking",
                     "Sudden vision loss", "Sudden severe dizziness"],
        "note": "A stroke is an emergency — call 911 immediately if symptoms are happening now.",
        "approach": [
            ("Find the cause", "Targeted testing of vessels, heart rhythm, and risk factors to explain why it happened."),
            ("Prevent the next one", "Medication and risk-factor management proven to lower recurrence."),
            ("Support recovery", "Coordinated referrals for rehabilitation and ongoing neurologic follow-up."),
        ],
    },
    "neuropathy": {
        "name": "Neuropathy &amp; Nerve Pain",
        "nav": "Neuropathy",
        "tag": "Peripheral Nerve",
        "lede": "Numbness, tingling, and burning in the hands and feet — diagnosed with EMG/nerve "
                "testing and managed to protect sensation and relieve pain.",
        "intro": "Peripheral neuropathy has dozens of causes, from diabetes to vitamin deficiencies "
                 "to nerve compression. We use nerve-conduction studies and EMG to characterize it, "
                 "search for the treatable cause, and manage nerve pain so it stops running your day.",
        "symptoms": ["Numbness or tingling in feet/hands", "Burning or electric pain",
                     "Weakness or balance trouble", "Sensitivity to touch", "Symptoms worse at night"],
        "approach": [
            ("Nerve testing", "EMG and nerve-conduction studies to define the type and severity."),
            ("Find the cause", "A focused search for reversible contributors so we treat the source, not just the symptom."),
            ("Pain relief", "Evidence-based medications and strategies to calm nerve pain."),
        ],
    },
    "neuromuscular": {
        "name": "Neuromuscular Disorders",
        "nav": "Neuromuscular",
        "tag": "Neuromuscular",
        "lede": "Muscle weakness, myasthenia gravis, ALS, and related neuromuscular conditions — "
                "diagnosed precisely and managed with expertise.",
        "intro": "Weakness that doesn't add up deserves a neuromuscular evaluation. Using EMG and "
                 "targeted testing, we diagnose conditions affecting the nerves and muscles — from "
                 "myasthenia gravis to inflammatory myopathies — and manage them with the newest "
                 "available therapies.",
        "symptoms": ["Muscle weakness or wasting", "Drooping eyelids or double vision",
                     "Difficulty swallowing", "Muscle cramps or twitching", "Fatigable weakness"],
        "approach": [
            ("EMG &amp; diagnosis", "Electrodiagnostic testing to localize and characterize the problem."),
            ("Targeted treatment", "Immune and symptomatic therapies matched to the specific diagnosis."),
            ("Ongoing partnership", "Close monitoring as we adjust care over time."),
        ],
    },
    "sleep-disorders": {
        "name": "Sleep Disorders",
        "nav": "Sleep Disorders",
        "tag": "Sleep Neurology",
        "lede": "Insomnia, restless legs, and sleep problems tied to neurologic conditions — "
                "because the brain heals when you sleep.",
        "intro": "Sleep and neurology are deeply connected. We evaluate insomnia, restless legs "
                 "syndrome, and sleep disturbances that accompany migraine, Parkinson's, and memory "
                 "disorders — and coordinate sleep studies when they're needed.",
        "symptoms": ["Trouble falling or staying asleep", "Restless, crawling leg sensations",
                     "Excessive daytime sleepiness", "Acting out dreams", "Unrefreshing sleep"],
        "approach": [
            ("Understand the sleep problem", "Sorting primary sleep disorders from neurologic causes."),
            ("Coordinated testing", "Referral for sleep studies when the history points to it."),
            ("Restorative plan", "Behavioral and medical strategies to rebuild healthy sleep."),
        ],
    },
    "back-neck-pain": {
        "name": "Neck &amp; Back Pain, Radiculopathy",
        "nav": "Neck &amp; Back Pain",
        "tag": "Spine Neurology",
        "lede": "Pinched nerves, sciatica, and spine-related pain evaluated from the neurologic "
                "angle — nerve, not just joint.",
        "intro": "When neck or back pain comes with numbness, tingling, or weakness, the nerves are "
                 "involved. We evaluate radiculopathy and spine-related nerve problems with exam and "
                 "EMG, clarify what's compressing the nerve, and guide you to the right treatment — "
                 "medical or surgical.",
        "symptoms": ["Pain radiating down an arm or leg", "Numbness or tingling", "Weakness in a limb",
                     "Sciatica", "Pain with certain positions"],
        "approach": [
            ("Localize the nerve", "Exam and EMG to pinpoint which nerve root is involved."),
            ("Clarify the cause", "Correlating imaging with your symptoms — so the plan targets the real problem."),
            ("Right-size the treatment", "From conservative care to the right specialist referral when needed."),
        ],
    },
}
# Extra list-only entries for the home map sidebar
BM_EXTRA = [("sleep-disorders", "Sleep Disorders"), ("neuromuscular", "Neuromuscular")]

def condition_schema(slug, c):
    data = {"@context": "https://schema.org", "@type": "MedicalCondition",
            "name": _plain(c["name"]),
            "description": _plain(c["lede"]),
            "possibleTreatment": {"@type": "MedicalTherapy", "name": "Neurologic evaluation and management",
                                  "provider": ORG_REF}}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>\n"

def build_conditions():
    slugs = list(CONDITIONS.items())
    # ---- Hub ----
    cards = "".join(
        f'''<a class="cond-card reveal d{i%3+1}" href="{slug}.html">
          <span class="cond-tag">{c["tag"]}</span>
          <h3>{c["name"]}</h3>
          <p>{_plain(c["lede"])[:120]}…</p>
        </a>''' for i, (slug, c) in enumerate(slugs))
    body = f"""
<main>
{page_hero("What We Treat", "Conditions We <em class='accent'>Care For</em>",
  "From migraine and memory loss to epilepsy, Parkinson's, MS, stroke, and neuropathy — "
  "comprehensive neurologic care for the brain, spine, and nervous system, all in West Palm Beach.",
  '<div class="crumbs"><a href="../index.html">Home</a> / Conditions</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Comprehensive Neurology</span>
      <h2>Choose a <em class="accent">Condition</em></h2>
      <p class="lede">Every pathway begins with a thorough evaluation by a board-certified neurologist.</p>
    </div>
    <div class="cond-grid">{cards}</div>
  </div>
</section>
{cta_band(1)}
</main>
"""
    write("conditions/index.html",
          head("Neurology Conditions in West Palm Beach | Palm Beach Neurology",
               "Neurologic conditions treated at Palm Beach Neurology in West Palm Beach: migraine, "
               "epilepsy, Parkinson's, Alzheimer's, MS, stroke, neuropathy, and more.",
               depth=1, canonical="conditions/index.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Conditions", "conditions/index.html")]))
          + nav(1) + body + footer(1))

    # ---- Individual pages ----
    for i, (slug, c) in enumerate(slugs):
        symptoms = "".join(f"<li>{s}</li>" for s in c["symptoms"])
        approach = "".join(
            f'<div class="svc-feature reveal d{j%3+1}"><span class="svc-feature-num">{j+1:02d}</span>'
            f'<div><h3>{t}</h3><p>{d}</p></div></div>'
            for j, (t, d) in enumerate(c["approach"]))
        others = [(s2, c2) for s2, c2 in slugs if s2 != slug][:5]
        related = "".join(f'<a href="{s2}.html">{c2["nav"]}</a> ' for s2, c2 in others)
        note = (f'<p class="af-note" style="background:var(--cream);border:1px solid var(--line-gold);'
                f'border-radius:14px;padding:1rem 1.2rem;color:var(--ink);font-weight:600;">'
                f'⚠ {c["note"]}</p>') if c.get("note") else ""
        body = f"""
<main>
{page_hero(c["tag"], c["name"].replace("&amp;", "&amp;"), c["lede"],
  f'<div class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">Conditions</a> / {c["nav"]}</div>')}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <h2>Understanding {c["name"]}</h2>
      <p>{c["intro"]}</p>
      {note}
      <h2>Signs it's time to see a neurologist</h2>
      <ul class="check-list">{symptoms}</ul>
      <p style="margin-top:1.4rem;">If these sound familiar, a focused neurologic evaluation is the
      fastest route to answers. <a class="text-link" href="../appointments.html">Request an appointment &rarr;</a></p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Start here</h3>
      <p>New patients are welcome. Our team will help verify your insurance and get you scheduled.</p>
      <a class="btn btn-coral" href="../appointments.html">Request Appointment <span class="arr">&rarr;</span></a>
      <div class="side-meta">
        <p style="margin-bottom:0.4rem;">Prefer to call?</p>
        <a href="tel:{PHONE_TEL}">{PHONE}</a>
      </div>
    </aside>
  </div>
</section>
<section class="section on-cream">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Our Approach</span>
      <h2>How We Treat <em class="accent">{c["nav"]}</em></h2>
    </div>
    <div class="svc-feature-grid">{approach}</div>
    <div class="related-links reveal" style="margin-top:2.4rem;">
      <strong>Related conditions:</strong><br>{related}
    </div>
  </div>
</section>
{cta_band(1)}
</main>
"""
        write(f"conditions/{slug}.html",
              head(f"{_plain(c['nav'])} Treatment in West Palm Beach | Palm Beach Neurology",
                   f"{_plain(c['lede'])} Board-certified neurology care at Palm Beach Neurology, West Palm Beach FL.",
                   depth=1, canonical=f"conditions/{slug}.html", page_type="article",
                   extra_schema=condition_schema(slug, c) + breadcrumb_schema(
                       [("Home", ""), ("Conditions", "conditions/index.html"), (_plain(c["nav"]), f"conditions/{slug}.html")]))
              + nav(1) + body + footer(1))

# ============================================================================
# CONTENT — DOCTORS  (roster PENDING OWNER VERIFICATION — see header note)
# ============================================================================
# Authoritative roster supplied by the owner from the practice's Our Doctors page.
# Post-nominals are the doctors' own; focus areas beyond what a fellowship implies
# (FAHS -> headache, FAAN -> academy fellow) are conservative and can be refined.
DOCTORS = [
    {"name": "Paul Winner", "creds": "DO, FAAN, FAHS",
     "focus": ["Headache &amp; Migraine", "Clinical Research"],
     "bio": "A nationally recognized leader in headache medicine and neurological clinical research — "
            "a Fellow of the American Academy of Neurology and the American Headache Society."},
    {"name": "Reed Stone", "creds": "MD, FAAN",
     "focus": ["General Neurology"],
     "bio": "A Fellow of the American Academy of Neurology, bringing broad experience across general "
            "neurology and a deeply patient-centered approach to care."},
    {"name": "Arnaldo Da Silva", "creds": "MD, FAHS",
     "focus": ["Headache &amp; Migraine"],
     "bio": "A Fellow of the American Headache Society, focused on the diagnosis and treatment of "
            "headache and migraine disorders."},
    {"name": "Tara Becker", "creds": "MD",
     "focus": ["General Neurology"],
     "bio": "Board-certified neurologist providing comprehensive, compassionate evaluation and care "
            "for conditions of the nervous system."},
    {"name": "Robert Coppola", "creds": "DO",
     "focus": ["General Neurology"],
     "bio": "Caring for the full range of neurologic conditions with a personalized, patient-first "
            "approach to diagnosis and long-term management."},
    {"name": "Manisha Korb", "creds": "MD",
     "focus": ["General Neurology"],
     "bio": "Dedicated to thorough diagnosis and individualized, long-term management across the "
            "breadth of general neurology."},
    {"name": "Michael Alosilla", "creds": "MD",
     "focus": ["General Neurology"],
     "bio": "Focused on accurate diagnosis and individualized treatment for patients living with "
            "neurologic disorders."},
    {"name": "Carl Sadowsky", "creds": "MD, FAAN",
     "focus": ["Memory &amp; Cognitive Disorders", "Clinical Research"],
     "bio": "A Fellow of the American Academy of Neurology with a focus on memory and cognitive "
            "disorders, including Alzheimer's disease and clinical research."},
    {"name": "Jose Zuniga", "creds": "MD",
     "focus": ["General Neurology"],
     "bio": "Board-certified neurologist committed to caring for patients with respect, empathy, "
            "and professionalism."},
]

def _doc_slug(name):
    return _plain(name).lower().replace(",", "").replace(".", "").replace(" ", "-")

def person_schema():
    people = []
    for d in DOCTORS:
        people.append({
            "@type": "Physician",
            "@id": f"{BASE}/our-doctors.html#{_doc_slug(d['name'])}",
            "name": "Dr. " + _plain(d["name"]),
            "honorificPrefix": "Dr.",
            "honorificSuffix": _plain(d["creds"]),
            "jobTitle": "Neurologist",
            "medicalSpecialty": "Neurologic",
            "description": _plain(d["bio"]),
            "worksFor": ORG_REF,
        })
    data = {"@context": "https://schema.org", "@graph": people}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>\n"

def build_doctors():
    def initials(name):
        parts = _plain(name).replace(",", "").split()
        return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()
    cards = ""
    for i, d in enumerate(DOCTORS):
        focus = "".join(f"<span>{f}</span>" for f in d["focus"])
        cards += f'''
        <article class="team-card reveal d{i%3+1}" id="{_doc_slug(d['name'])}">
          <div class="team-photo empty" role="img" aria-label="Portrait of Dr. {_plain(d['name'])}">
            <span class="team-initials" aria-hidden="true">{initials(d['name'])}</span>
          </div>
          <h3>Dr. {d["name"]}</h3>
          <div class="role">{d["creds"]}</div>
          <div class="pw-tags" style="justify-content:center;margin-top:0.7rem;">{focus}</div>
          <p>{d["bio"]}</p>
        </article>'''
    body = f"""
<main>
{page_hero("Meet the Team", "Our <em class='accent'>Doctors</em>",
  "Board-certified neurologists with more than 25 years of combined experience caring for the "
  "brain, spine, and nervous system — right here in West Palm Beach.",
  '<div class="crumbs"><a href="index.html">Home</a> / Our Doctors</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Clinical Neuroscience Professionals</span>
      <h2>Expertise You Can <em class="accent">Trust</em></h2>
      <p class="lede">Our clinical neuroscience professionals are board-certified neurologists trained
      to diagnose and treat diseases and conditions of the nervous system — focused on diagnosis,
      treatment, prevention, rehabilitation, and education for you and your family.</p>
    </div>
    <div class="team-grid">{cards}</div>
  </div>
</section>
<section class="section on-ink">
  {neuro_field(0.5)}
  <div class="wrap" style="position:relative;z-index:1;">
    <div class="split">
      <div class="reveal">
        <span class="eyebrow on-dark">More Than a Clinic</span>
        <h2>A research institute <em class="accent">under the same roof</em></h2>
        <p style="margin-top:1.2rem;">Our physicians are active in clinical research through the
        Premier Research Institute — giving our patients access to tomorrow's therapies for
        Alzheimer's, migraine, and MS, today.</p>
        <div class="mt-2"><a class="btn btn-ghost" href="clinical-research.html">Explore Clinical Research <span class="arr">&rarr;</span></a></div>
      </div>
      <div class="reveal d2">
        <div class="stat-row">
          <div><strong data-count="25" data-suffix="+">25+</strong><span>Years of Expertise</span></div>
          <div><strong>Board</strong><span>Certified Neurologists</span></div>
          <div><strong>On-site</strong><span>Clinical Research</span></div>
          <div><strong>New</strong><span>Patients Welcome</span></div>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("our-doctors.html",
          head("Our Doctors | Neurologists in West Palm Beach | Palm Beach Neurology",
               "Meet the board-certified neurologists of Palm Beach Neurology in West Palm Beach, FL — "
               "25+ years caring for the brain, spine, and nervous system.",
               canonical="our-doctors.html",
               extra_schema=person_schema() + breadcrumb_schema([("Home", ""), ("Our Doctors", "our-doctors.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# CLINICAL RESEARCH
# ============================================================================
def build_research():
    trials = [
        ("Alzheimer's &amp; Memory", "Studies of investigational treatments aimed at slowing memory "
         "loss — including options for people with early symptoms and those at risk."),
        ("Migraine", "Trials of new approaches to prevent and treat migraine for people who haven't "
         "found lasting relief."),
        ("Multiple Sclerosis", "Research into next-generation therapies to reduce relapses and "
         "protect long-term function in MS."),
    ]
    trial_cards = "".join(
        f'<div class="svc-feature reveal d{i%3+1}"><span class="svc-feature-num">{i+1:02d}</span>'
        f'<div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(trials))
    steps = [("Screen", "A no-cost screening visit to see whether a study is a fit for you."),
             ("Enroll", "If you qualify and choose to join, our team walks you through informed consent."),
             ("Participate", "Study visits with close monitoring by our physicians and research staff."),
             ("Contribute", "You help advance care for the next generation of patients — and may access tomorrow's therapies today.")]
    steps_html = "".join(
        f'<div class="svc-step reveal d{i%4+1}"><div class="svc-step-dot">{i+1}</div>'
        f'<h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))
    body = f"""
<main>
{page_hero("Premiere Research Institute", "Clinical <em class='accent'>Research</em>",
  "Our on-site research institute gives Palm Beach patients access to carefully monitored clinical "
  "trials — tomorrow's therapies for Alzheimer's, migraine, and MS, available today.",
  '<div class="crumbs"><a href="index.html">Home</a> / Clinical Research</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Why It Matters</span>
      <h2>Advancing Neurology, <em class="accent">Right Here</em></h2>
      <p class="lede">Clinical trials are how every treatment we use today came to be. Participating
      can give you access to investigational therapies and expert oversight — at no cost to you.</p>
    </div>
    <div class="svc-feature-grid">{trial_cards}</div>
    <p style="max-width:70ch;margin-top:1.6rem;">Participants receive ongoing expert care throughout
    every study. Eligibility and available trials change over time, and participation is always
    voluntary — talk with our team to learn what is currently enrolling and whether it may be right for you.</p>
    <div class="mt-2"><a class="text-link" href="{RESEARCH_URL}" target="_blank" rel="noopener">Visit the Premiere Research Institute &rarr;</a></div>
  </div>
</section>
<section class="section on-ink">
  {neuro_field(0.55)}
  <div class="wrap" style="position:relative;z-index:1;">
    <div class="section-head center reveal">
      <span class="eyebrow on-dark">How It Works</span>
      <h2>From Screening to <em class="accent">Contribution</em></h2>
    </div>
    <div class="svc-process">{steps_html}</div>
    <div class="center mt-3 reveal">
      <a class="btn btn-coral" href="appointments.html">Ask About Research <span class="arr">&rarr;</span></a>
    </div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("clinical-research.html",
          head("Clinical Research &amp; Trials | Palm Beach Neurology, West Palm Beach",
               "The Premiere Research Institute at Palm Beach Neurology runs clinical trials in "
               "Alzheimer's, migraine, and MS in West Palm Beach, FL. Learn how to participate.",
               canonical="clinical-research.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Clinical Research", "clinical-research.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# APPOINTMENTS  (their real offerings: FREE Memory Screen + New Patient)
# ============================================================================
def build_appointments():
    options = [
        ("FREE Memory Screen", "30 min",
         "A brief, no-cost screening designed to assess memory and cognitive function and identify "
         "potential memory problems or early signs of conditions like mild cognitive impairment (MCI) "
         "or dementia — simple, structured tests of memory, attention, and thinking skills.", "Free · 30 min"),
        ("New Patient Appointment", "1 hour",
         "A comprehensive first visit to develop a complete medical profile, identify any risk "
         "factors, and create a personalized care plan. Please bring a list of current medications, "
         "past medical records, previous test results, and insurance information.", "New patients welcome"),
    ]
    opt_cards = "".join(
        f'''<div class="cond-card reveal d{i+1}" style="padding:2rem 1.9rem;">
          <span class="cond-tag">{badge}</span>
          <h3>{t}</h3>
          <p style="margin-top:0.5rem;">{d}</p>
          <p style="margin-top:1rem;font-weight:700;color:var(--ink);">⏱ {dur}</p>
        </div>''' for i, (t, dur, d, badge) in enumerate(options))
    body = f"""
<main>
{page_hero("Get Started", "Request an <em class='accent'>Appointment</em>",
  "New patients are welcome. Choose a free memory screen or a full new-patient visit, then send "
  "the request below — our front desk will call you back to confirm and verify insurance.",
  '<div class="crumbs"><a href="index.html">Home</a> / Appointments</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Appointment Options</span>
      <h2>Two Ways to <em class="accent">Begin</em></h2>
    </div>
    <div class="cond-grid" style="max-width:820px;margin:0 auto;grid-template-columns:1fr 1fr;">{opt_cards}</div>
    <div class="cht-callout reveal" style="margin:2.6rem auto 0;text-align:center;">
      <h3>Save time — complete your new-patient forms first</h3>
      <p style="margin:0 auto;">Fill out your new patient paperwork before your appointment to save
      time in the waiting room. Questions about any of the forms? Call our office at {PHONE}.</p>
      <div class="mt-2"><a class="btn btn-ink" href="{FORMS_PDF}" download>Download New Patient Paperwork (PDF)</a></div>
    </div>
  </div>
</section>
<section class="section on-cream">
  <div class="wrap contact-grid">
    <div class="appt-form-card reveal">
      <h2 class="h3-size">Request an Appointment</h2>
      <p class="af-sub">Tell us a little about what you need and our front desk will call you back to confirm.</p>
      <form class="appt-form" id="appt-form" data-endpoint="https://formsubmit.co/ajax/{EMAIL}" novalidate>
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
          <label for="af-type">Appointment type</label>
          <select id="af-type" name="type">
            <option>New Patient Appointment</option>
            <option>FREE Memory Screen</option>
            <option>Follow-up</option>
            <option>Clinical research inquiry</option>
          </select>
        </div>
        <div class="af-field">
          <label for="af-reason">Reason for visit *</label>
          <textarea id="af-reason" name="reason" required maxlength="2000" placeholder="e.g. frequent migraines, memory concerns, numbness in the feet…"></textarea>
        </div>
        <div class="af-field">
          <label style="display:flex;gap:0.6rem;align-items:flex-start;font-size:0.92rem;font-weight:500;text-transform:none;letter-spacing:0;color:var(--text);cursor:pointer;">
            <input type="checkbox" name="trials" value="yes" style="margin-top:0.2rem;width:18px;height:18px;accent-color:var(--coral);flex-shrink:0;">
            <span>Yes! I'd also like to learn more about clinical trials.</span>
          </label>
        </div>
        <p class="af-note">This is a contact request, not a medical record — please don't include
        detailed health history or sensitive information here. We only need the basics to call you back.</p>
        <p class="af-error" id="af-error" role="alert"></p>
        <button class="btn btn-coral" type="submit">Send Request <span class="arr">&rarr;</span></button>
      </form>
      <div class="af-done" id="af-done" hidden>
        <div class="af-check">&#10003;</div>
        <h3>Request received!</h3>
        <p id="af-done-msg">Thank you — our front desk will call you back to confirm. If you haven't
        heard from us within 48 hours, please call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>
      </div>
    </div>
    <div class="reveal d2">
      <div class="contact-card" style="margin-bottom:1.5rem;">
        <h3>Palm Beach Neurology</h3>
        <div class="c-row"><span class="c-label">Address</span><span>{ADDR_STREET}<br>{ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}</span></div>
        <div class="c-row"><span class="c-label">Phone</span><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
        <div class="c-row"><span class="c-label">Hours</span><span>Monday – Friday<br>Call for current hours</span></div>
        <div class="c-row"><span class="c-label">Portal</span><a href="{PORTAL}">Patient Portal &rarr;</a></div>
        <a class="btn btn-coral mt-2" href="tel:{PHONE_TEL}">Call to Book <span class="arr">&rarr;</span></a>
      </div>
      <iframe class="map-frame" src="{MAPS_EMBED}" title="Map to Palm Beach Neurology" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="min-height:300px;"></iframe>
    </div>
  </div>
</section>
</main>
"""
    write("appointments.html",
          head("Request an Appointment | Palm Beach Neurology, West Palm Beach FL",
               "Request a neurology appointment in West Palm Beach — free memory screen or new-patient "
               "visit. Call 561-845-0500 or send a request online. New patients welcome.",
               canonical="appointments.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Appointments", "appointments.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# CONTACT
# ============================================================================
def build_contact():
    body = f"""
<main>
{page_hero("We're Here to Help", "Contact <em class='accent'>Palm Beach Neurology</em>",
  "Call, request an appointment, or stop by our West Palm Beach office. Our team is glad to help "
  "you get scheduled and verify your insurance.",
  '<div class="crumbs"><a href="index.html">Home</a> / Contact</div>')}
<section class="section">
  <div class="wrap contact-grid">
    <div class="reveal">
      <div class="contact-card">
        <h2 class="h3-size">Palm Beach Neurology &amp; Premier Research Institute</h2>
        <div class="c-row"><span class="c-label">Address</span><span>{ADDR_STREET}<br>{ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}</span></div>
        <div class="c-row"><span class="c-label">Phone</span><a href="tel:{PHONE_TEL}">{PHONE}</a></div>
        <div class="c-row"><span class="c-label">Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="c-row"><span class="c-label">Hours</span><span>Monday – Friday · Call for current hours</span></div>
        <div class="c-row"><span class="c-label">Portal</span><a href="{PORTAL}">Patient Portal &rarr;</a></div>
        <div class="hero-ctas" style="margin-top:1.6rem;">
          <a class="btn btn-coral" href="appointments.html">Request Appointment <span class="arr">&rarr;</span></a>
          <a class="btn btn-ink" href="tel:{PHONE_TEL}">Call Now</a>
        </div>
      </div>
    </div>
    <div class="reveal d2">
      <iframe class="map-frame" src="{MAPS_EMBED}" title="Map to Palm Beach Neurology" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("contact.html",
          head("Contact | Palm Beach Neurology, West Palm Beach FL",
               f"Contact Palm Beach Neurology: {ADDR_STREET}, {ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}. "
               f"Call {PHONE} to schedule with a board-certified neurologist.",
               canonical="contact.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Contact", "contact.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# FAQ
# ============================================================================
FAQ_CATEGORIES = [
    ("visit", "Your Visit", [
        ("Do I need a referral to see a neurologist?",
         "It depends on your insurance plan. Many PPO plans let you self-refer, while some HMO and "
         "Medicare Advantage plans require a referral from your primary care physician. Call us at "
         f"{PHONE} and our team will help you check before your visit."),
        ("What should I bring to my first appointment?",
         "Please bring your photo ID, insurance card, a list of your current medications, any recent "
         "brain or spine imaging (MRI/CT) on disc or through your portal, and any relevant records or "
         "referral paperwork. A family member is welcome — especially for memory-related visits."),
        ("How long is a new-patient appointment?",
         "New-patient neurology visits are scheduled for about one hour so your neurologist has time "
         "to review your history, examine you, and explain the plan."),
        ("What is the FREE Memory Screen?",
         "It's a no-cost, confidential 30-minute screening of memory and thinking — a simple first "
         "step if you or a loved one has noticed changes. It isn't a diagnosis, but it helps us decide "
         "whether a fuller evaluation is worthwhile."),
    ]),
    ("insurance", "Insurance &amp; Billing", [
        ("Which insurance plans do you accept?",
         "We accept many major insurance plans, including Medicare. Because coverage varies by plan, "
         f"the fastest way to confirm is to call us at {PHONE} with your card handy and we'll verify "
         "your benefits."),
        ("Do you see new patients?",
         "Yes — we are accepting new patients. You can request an appointment online or call the office."),
        ("How much will my visit cost?",
         "Your cost depends on your specific insurance plan, deductible, and the services provided. "
         "Our front desk will help you understand your coverage before your visit whenever possible."),
    ]),
    ("care", "Our Care", [
        ("What conditions do you treat?",
         "We care for the full range of neurologic conditions — headache and migraine, epilepsy and "
         "seizures, Parkinson's and movement disorders, Alzheimer's and memory loss, multiple "
         "sclerosis, stroke and TIA, neuropathy, neuromuscular disorders, sleep problems, and "
         "spine-related nerve pain."),
        ("Do you offer testing like EEG and EMG?",
         "Our neurologists use tools such as EEG (for seizures) and EMG/nerve-conduction studies "
         "(for neuropathy and neuromuscular conditions) as part of the work-up. Ask our team about "
         "what's available and what your evaluation may involve."),
        ("What clinical trials are available?",
         "Through our on-site Premier Research Institute, we run carefully monitored trials in areas "
         "such as Alzheimer's, migraine, and MS. Available studies change over time — ask us what's "
         "currently enrolling."),
    ]),
    ("urgent", "Urgent Symptoms", [
        ("When is a symptom an emergency?",
         "Call 911 immediately for sudden weakness or numbness on one side, face drooping, trouble "
         "speaking, sudden severe headache, sudden vision loss, or a first-time seizure that won't "
         "stop. These can be signs of a stroke or other emergency and shouldn't wait for an office visit."),
        ("I had a mini-stroke (TIA) — how soon should I be seen?",
         "A TIA is a warning sign and should be evaluated promptly. Call your physician or seek "
         "emergency care right away, and let us help you with prompt neurologic follow-up and "
         "prevention planning."),
    ]),
]
FAQS = [qa for _s, _t, pairs in FAQ_CATEGORIES for qa in pairs]

def faq_schema(pairs):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": _plain(q),
                 "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
                for q, a in pairs]}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + "</script>\n"

def build_faq():
    total = len(FAQS)
    bubbles = (f'<button type="button" class="faq-bubble active" data-cat="all" aria-pressed="true">'
               f'All Questions <span class="fb-count">({total})</span></button>')
    bubbles += "".join(
        f'<button type="button" class="faq-bubble" data-cat="{sid}" aria-pressed="false">{title} <span class="fb-count">({len(pairs)})</span></button>'
        for sid, title, pairs in FAQ_CATEGORIES)
    sections = ""
    for sid, title, pairs in FAQ_CATEGORIES:
        items = "".join(
            f'<details class="faq-item reveal" data-cat="{sid}"><summary>{q}</summary><div class="faq-a">{a}</div></details>'
            for q, a in pairs)
        sections += f'''
  <section class="faq-cat" id="{sid}" aria-labelledby="{sid}-h" data-cat-section="{sid}">
    <div class="faq-cat-head"><h2 id="{sid}-h">{title}</h2><span class="faq-count">{len(pairs)} answers</span></div>
    <div class="faq-list">{items}</div>
  </section>'''
    body = f"""
<main>
{page_hero("Questions, Answered", "Frequently Asked <em class='accent'>Questions</em>",
  f"{total} straight answers about referrals, insurance, what to expect, and when a symptom is urgent — "
  "filter by topic or search below.",
  '<div class="crumbs"><a href="index.html">Home</a> / FAQ</div>')}
<div class="faq-jump-bar">
  <div class="faq-jump" role="group" aria-label="Filter FAQs by category">{bubbles}</div>
</div>
<section class="section">
  <div class="wrap">
    <div class="faq-toolbar reveal">
      <label class="sr-only" for="faq-search">Search the FAQs</label>
      <input type="search" id="faq-search" class="faq-search" placeholder="Search questions… (e.g. referral, Medicare, memory)" autocomplete="off">
      <div class="faq-tools">
        <button type="button" class="faq-tool" id="faq-expand">Expand all</button>
        <button type="button" class="faq-tool" id="faq-collapse">Collapse all</button>
      </div>
    </div>
    <p class="sr-only" aria-live="polite" id="faq-live"></p>
    <p class="faq-empty faq-hidden" id="faq-empty">No questions match your search — try a different word, or call <a href="tel:{PHONE_TEL}">{PHONE}</a> and ask us directly.</p>
    {sections}
    <div class="center mt-3 reveal"><p class="lede" style="margin:0 auto 1.2rem;">Still have a question?</p>
    <a class="btn btn-ink" href="contact.html">Contact Us <span class="arr">&rarr;</span></a></div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("faq.html",
          head("Neurology FAQ | Palm Beach Neurology, West Palm Beach",
               "Answers about referrals, insurance, first visits, testing, and urgent symptoms at "
               "Palm Beach Neurology in West Palm Beach, FL.",
               canonical="faq.html",
               extra_schema=faq_schema(FAQS) + breadcrumb_schema([("Home", ""), ("FAQ", "faq.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# HOME
# ============================================================================
def build_home():
    # Brain-map sidebar list (all conditions incl. list-only extras).
    # The figure spots use short keys; the JS matches data-bm across figure + list,
    # so list items get the spot key where one exists (2 list-only entries do not).
    bm_order = ["headaches-migraine", "memory-alzheimers", "epilepsy-seizures", "parkinsons-movement",
                "multiple-sclerosis", "stroke", "neuropathy", "back-neck-pain", "sleep-disorders", "neuromuscular"]
    key_to_slug = {"migraine": "headaches-migraine", "memory": "memory-alzheimers",
                   "epilepsy": "epilepsy-seizures", "movement": "parkinsons-movement",
                   "stroke": "stroke", "ms": "multiple-sclerosis", "spine": "back-neck-pain",
                   "neuropathy": "neuropathy"}
    slug_to_key = {v: k for k, v in key_to_slug.items()}

    def _bm_item(slug):
        c = CONDITIONS[slug]
        dbm = f' data-bm="{slug_to_key[slug]}"' if slug in slug_to_key else ''
        return (f'<a class="bm-item"{dbm} href="conditions/{slug}.html">'
                f'<span>{c["nav"]}</span><span class="bm-tag">{c["tag"]}</span></a>')
    bm_list_html = "".join(_bm_item(s) for s in bm_order)

    bm_data = {}
    for key, slug in key_to_slug.items():
        c = CONDITIONS[slug]
        bm_data[key] = {"name": _plain(c["name"]), "tag": _plain(c["tag"]), "lede": _plain(c["lede"]),
                        "treats": [_plain(s) for s in c["symptoms"][:4]],
                        "url": f"conditions/{slug}.html"}
    bm_json = _json.dumps(bm_data)

    ticker = "".join(f"<span>{s}</span>" for s in
        ["Headache &amp; Migraine", "Epilepsy", "Parkinson's", "Memory &amp; Alzheimer's",
         "Multiple Sclerosis", "Stroke", "Neuropathy", "Neuromuscular", "Sleep", "Clinical Research"])

    pathways = [
        ("01", "Comprehensive Neurology", "The whole nervous system, one practice.",
         "Board-certified neurologists evaluating and managing conditions of the brain, spine, "
         "and peripheral nerves — with the time to get the diagnosis right.",
         ["Headache", "Epilepsy", "Movement", "Neuropathy"], "conditions/index.html", ""),
        ("02", "Memory &amp; Cognitive Care", "Answers when memory changes.",
         "Thorough evaluation of memory and thinking — including a free memory screen — with access "
         "to the newest disease-modifying therapies.",
         ["Free Memory Screen", "Alzheimer's", "Dementia"], "conditions/memory-alzheimers.html", ""),
        ("03", "Clinical Research", "Tomorrow's therapies, today.",
         "Our on-site Premier Research Institute offers carefully monitored trials in Alzheimer's, "
         "migraine, and MS — expert oversight, at no cost to participants.",
         ["Alzheimer's", "Migraine", "MS"], "clinical-research.html",
         '<span class="badge-inline">On-site</span>'),
    ]
    pathways_html = "".join(
        f'''<a class="pathway reveal" href="{url}">
          <span class="pw-num">{num}</span>
          <div><h3>{title}{badge}</h3><span class="pw-kicker">{kick}</span></div>
          <div class="pw-body"><p>{desc}</p>
            <div class="pw-tags">{"".join(f"<span>{t}</span>" for t in tags)}</div></div>
          <span class="pw-go">&rarr;</span>
        </a>''' for num, title, kick, desc, tags, url, badge in pathways)

    body = f"""
<main>
<section class="hero">
  <div class="hero-media">
    <div class="hero-fallback"></div>
    {neuro_field(1)}
  </div>
  <div class="hero-scrim"></div>
  <div class="wrap hero-inner">
    <div class="hero-panel">
      <span class="eyebrow on-dark">Compassionate Neurological Care · South Florida</span>
      <h1>
        <span class="line"><span>Clarity</span></span>
        <span class="line"><span>for the</span></span>
        <span class="line"><span><em class="accent">mind.</em></span></span>
      </h1>
      <p class="hero-tag">&ldquo;Treating the patient, not just the disease.&rdquo;</p>
      <p class="hero-sub">Board-certified neurologists caring for the brain, spine, and nervous
      system for more than 25 years — with an on-site research institute bringing tomorrow's
      therapies to the Palm Beaches today.</p>
      <div class="hero-ctas">
        <a class="btn btn-coral" href="appointments.html">Request Appointment <span class="arr">&rarr;</span></a>
        <a class="btn btn-ghost" href="#bodymap">Explore Conditions</a>
      </div>
    </div>
    <div class="hero-meta">
      <div><strong data-count="25" data-suffix="+">25+</strong><span>Years of Expertise</span></div>
      <div><strong>Board</strong><span>Certified Neurologists</span></div>
      <div><strong>On-site</strong><span>Clinical Research</span></div>
      <div><strong>New</strong><span>Patients Welcome</span></div>
    </div>
  </div>
  <div class="scroll-hint"><span></span></div>
</section>

<div class="ins-strip"><div class="ticker">{ticker}</div></div>

<section class="section on-paper">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">{TAGLINE}</span>
      <h2>Committed to Your <em class="accent">Brain Health</em></h2>
      <p class="lede" style="max-width:64ch;">Palm Beach Neurology is a comprehensive neurological
      practice committed to preventing and treating every element of neurological disease. As one of
      the most experienced neurological practices in the United States, our physicians and staff stay
      on the cutting edge of research and patient care — treating every patient with respect, empathy,
      and professionalism.</p>
    </div>
  </div>
</section>

<section class="section" id="pathways">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">What We Do</span>
      <h2>Neurology in <em class="accent">West Palm Beach</em></h2>
      <p class="lede">Advanced, compassionate care for the nervous system — plus a research institute
      under the same roof.</p>
    </div>
    <div class="pathways">{pathways_html}</div>
  </div>
</section>

<section class="section on-ink" id="bodymap">
  {neuro_field(0.6)}
  <div class="wrap" style="position:relative;z-index:1;">
    <div class="section-head reveal">
      <span class="eyebrow on-dark">Where Does It Start?</span>
      <h2>Explore the <em class="accent">Nervous System</em></h2>
      <p class="lede">Tap an area of the brain, spine, or nerves to see what we treat there — every
      pathway begins with a thorough evaluation.</p>
    </div>
    <div class="bodymap-grid three">
      <div class="bodymap-fig reveal">{brainmap_svg()}</div>
      <div class="bm-list reveal d2">{bm_list_html}</div>
      <aside class="bm-panel reveal d3" id="bm-panel" aria-live="polite">
        <div class="bm-panel-default">
          <span class="eyebrow on-dark">Your Guide</span>
          <h3>Select a glowing point</h3>
          <p>Tap any point on the figure — or any condition in the list — and we'll show you what we
          treat there and how we approach it.</p>
        </div>
      </aside>
    </div>
  </div>
  <script type="application/json" id="bm-data">{bm_json}</script>
</section>

<section class="section on-cream">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our Story</span>
      <h2>25 Years of Neurologic <em class="accent">Excellence</em></h2>
      <p style="margin-top:1.2rem;">For more than 25 years, Palm Beach Neurology has combined
      state-of-the-art techniques with a personal approach — treating the patient, not just the
      disease. Our board-certified neurologists take the time to reach the right diagnosis and build
      a plan around your life.</p>
      <p>Because we house the Premier Research Institute under the same roof, our patients can reach
      tomorrow's therapies today — through carefully monitored clinical trials in Alzheimer's,
      migraine, and MS.</p>
      <div class="stat-row">
        <div><strong data-count="25" data-suffix="+">25+</strong><span>Years of Expertise</span></div>
        <div><strong>Board</strong><span>Certified Neurologists</span></div>
        <div><strong>On-site</strong><span>Research Institute</span></div>
        <div><strong>Personal</strong><span>Patient-First Care</span></div>
      </div>
      <div class="mt-2"><a class="text-link" href="our-doctors.html">Meet our doctors &rarr;</a></div>
    </div>
    <div class="reveal d2">
      <div class="split-media" style="aspect-ratio:4/5;display:grid;place-items:center;background:linear-gradient(160deg,var(--ink),var(--ink-deep));">
        {neuro_field(0.9)}
        <div style="position:relative;z-index:1;text-align:center;padding:2rem;">
          {brand_mark('hero')}
          <p style="font-family:var(--font-display);font-style:italic;color:var(--gold);font-size:1.5rem;margin-top:1rem;max-width:22ch;">The brain deserves a specialist's full attention.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section on-paper">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Getting Started Is Simple</span>
      <h2>Your First <em class="accent">Visit</em></h2>
    </div>
    <div class="svc-process">
      <div class="svc-step reveal d1"><div class="svc-step-dot">1</div><h3>Reach Out</h3><p>Request an appointment online or call — new patients are welcome.</p></div>
      <div class="svc-step reveal d2"><div class="svc-step-dot">2</div><h3>We Verify</h3><p>Our team confirms your insurance and helps gather any records.</p></div>
      <div class="svc-step reveal d3"><div class="svc-step-dot">3</div><h3>Comprehensive Visit</h3><p>A full hour with a neurologist to examine you and explain the plan.</p></div>
      <div class="svc-step reveal d4"><div class="svc-step-dot">4</div><h3>A Clear Plan</h3><p>Diagnosis, next steps, and follow-up — in plain language.</p></div>
    </div>
    <div class="center mt-3 reveal"><a class="btn btn-coral" href="appointments.html">Request Appointment <span class="arr">&rarr;</span></a></div>
  </div>
</section>

{cta_band(0)}
</main>
"""
    write("index.html",
          head("Neurologist in West Palm Beach | Palm Beach Neurology",
               "Board-certified neurology and on-site clinical research in West Palm Beach, FL. "
               "We treat migraine, epilepsy, Parkinson's, memory loss, MS, stroke & neuropathy. "
               "New patients welcome — call 561-845-0500.",
               canonical="", og_image="assets/media/og-cover.jpg")
          + nav(0) + body + footer(0))

# ============================================================================
# SERVICES  (their site lacks a services list — built from their 5 care pillars)
# ============================================================================
def build_services():
    pillars = [
        ("Diagnosis", "Accurate answers start here. Detailed neurologic examination plus testing "
         "such as EEG, EMG/nerve-conduction studies, cognitive evaluation, and imaging review to "
         "pinpoint what's really going on."),
        ("Treatment", "Personalized, state-of-the-art treatment matched to your diagnosis — including "
         "expert medication management and, where appropriate, Botox and infusion therapies."),
        ("Prevention", "Stopping the next event before it happens — stroke-risk reduction, migraine "
         "prevention, and proactive brain-health strategies."),
        ("Rehabilitation", "Restoring function after stroke, injury, or a new diagnosis, coordinated "
         "with the right therapists and specialists."),
        ("Education", "You and your family, fully informed. We explain your condition and your plan "
         "in plain language so you can make confident decisions."),
    ]
    pillar_html = "".join(
        f'<div class="svc-feature reveal d{i%3+1}"><span class="svc-feature-num">{i+1:02d}</span>'
        f'<div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(pillars))
    care = [(c["nav"], c["tag"], f"conditions/{slug}.html") for slug, c in CONDITIONS.items()]
    care += [("Clinical Trials", "Premiere Research Institute", "clinical-research.html"),
             ("Free Memory Screen", "No-cost cognitive screen", "appointments.html")]
    care_html = "".join(
        f'''<a class="cond-card reveal d{i%3+1}" href="{url}">
          <span class="cond-tag">{tag}</span><h3>{name}</h3></a>''' for i, (name, tag, url) in enumerate(care))
    body = f"""
<main>
{page_hero("Comprehensive Neurologic Care", "Our <em class='accent'>Services</em>",
  "From diagnosis to treatment, prevention, rehabilitation, and education — complete care for the "
  "brain, spine, and nervous system, all under one roof in West Palm Beach.",
  '<div class="crumbs"><a href="index.html">Home</a> / Services</div>')}
<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Five Pillars of Care</span>
      <h2>How We <em class="accent">Help</em></h2>
      <p class="lede">Our physicians focus on providing the highest quality of healthcare services
      across every stage of your neurologic care.</p>
    </div>
    <div class="svc-feature-grid">{pillar_html}</div>
  </div>
</section>
<section class="section on-cream">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="eyebrow">Areas of Care</span>
      <h2>What We <em class="accent">Treat</em></h2>
      <p class="lede">Comprehensive neurology — choose an area to learn more.</p>
    </div>
    <div class="cond-grid">{care_html}</div>
    <p class="af-note" style="max-width:72ch;margin:2rem auto 0;text-align:center;">Testing and
    procedures available as part of your evaluation may include EEG, EMG and nerve-conduction studies,
    cognitive testing, and coordinated imaging. Ask our team what your work-up will involve.</p>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("services.html",
          head("Neurology Services in West Palm Beach | Palm Beach Neurology",
               "Comprehensive neurology services in West Palm Beach: diagnosis, treatment, prevention, "
               "rehabilitation & education for headache, epilepsy, Parkinson's, memory loss, MS, "
               "stroke, neuropathy & more.",
               canonical="services.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Services", "services.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# PATIENT CENTER  (new-patient info, forms download, portal, what to bring)
# ============================================================================
def build_patient_center():
    bring = ["Photo ID and insurance card(s)", "A list of your current medications and dosages",
             "Past medical records and previous test results", "Any brain or spine imaging (MRI/CT) on disc",
             "A referral, if your plan requires one", "A written list of your questions and concerns",
             "A family member or caregiver — especially for memory-related visits"]
    bring_html = "".join(f"<li>{b}</li>" for b in bring)
    body = f"""
<main>
{page_hero("Patient Center", "New <em class='accent'>Patients</em>",
  "Everything you need for a smooth first visit — your paperwork, what to bring, and how to reach "
  "the patient portal. We're glad you're here.",
  '<div class="crumbs"><a href="index.html">Home</a> / Patient Center</div>')}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <h2>Your first visit</h2>
      <p>The purpose of a new-patient appointment is to develop a complete medical profile, identify
      any risk factors, and create a personalized care plan. This foundational visit helps build a
      relationship between you and your physician and ensures your ongoing care is tailored to your
      unique needs.</p>
      <h2>What to bring</h2>
      <ul class="check-list">{bring_html}</ul>
      <h2>New patient paperwork</h2>
      <p>To help your visit go smoothly, you can complete your new-patient paperwork before you arrive —
      it saves time in the waiting room. If you have questions about any of the forms, call our office
      at {PHONE}.</p>
      <p><a class="btn btn-coral" href="{FORMS_PDF}" download>Download New Patient Paperwork (PDF)</a></p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Patient Portal</h3>
      <p>Access your information and manage your care online.</p>
      <a class="btn btn-ink" href="#" aria-label="Patient portal login (link pending)">Portal Login &rarr;</a>
      <div class="side-meta">
        <p style="margin-bottom:0.4rem;">Ready to schedule?</p>
        <a href="appointments.html" class="text-link">Request an appointment &rarr;</a>
      </div>
      <div class="side-meta">
        <p style="margin-bottom:0.4rem;">Insurance</p>
        <p style="font-size:0.9rem;color:var(--muted);">We accept many major plans, including Medicare.
        Call <a href="tel:{PHONE_TEL}">{PHONE}</a> to verify your coverage.</p>
      </div>
    </aside>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("patient-center.html",
          head("Patient Center &amp; New Patient Forms | Palm Beach Neurology",
               "New patient information, downloadable paperwork, patient portal, and what to bring "
               "to your first neurology visit at Palm Beach Neurology in West Palm Beach, FL.",
               canonical="patient-center.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("Patient Center", "patient-center.html")]))
          + nav(0) + body + footer(0))

# ============================================================================
# META (sitemap / robots / llms / manifest / 404)
# ============================================================================
def build_meta():
    write("site.webmanifest", _json.dumps({
        "name": LEGAL, "short_name": "PB Neurology",
        "description": "Board-certified neurology & clinical research in West Palm Beach, FL.",
        "start_url": "/", "display": "standalone",
        "background_color": "#F3ECDC", "theme_color": THEME_COLOR,
        "icons": [{"src": "/assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }, indent=2) + "\n")

    pages = ["", "services.html", "our-doctors.html", "clinical-research.html", "appointments.html",
             "patient-center.html", "contact.html", "faq.html", "conditions/index.html"]
    pages += [f"conditions/{s}.html" for s in CONDITIONS]
    from datetime import date as _date
    lastmod = _date.today().isoformat()
    urls = "".join(f"  <url><loc>{BASE}/{p}</loc><lastmod>{lastmod}</lastmod></url>\n" for p in pages)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")

    ai_crawlers = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot",
                   "Claude-User", "Google-Extended", "Bingbot", "Applebot", "meta-externalagent"]
    ai_blocks = "".join(f"User-agent: {ua}\nAllow: /\n\n" for ua in ai_crawlers)
    write("robots.txt",
          "# All crawlers welcome, including AI/answer-engine bots.\n"
          "User-agent: *\nAllow: /\n\n" + ai_blocks + f"Sitemap: {BASE}/sitemap.xml\n")

    cond_lines = "\n".join(f"- {_plain(c['name'])}: {BASE}/conditions/{slug}.html" for slug, c in CONDITIONS.items())
    doc_lines = "; ".join(_plain(d["name"]) for d in DOCTORS)
    write("llms.txt", f"""# {LEGAL}

> Board-certified neurology practice in West Palm Beach, Florida, with 25+ years caring for the
> brain, spine, and nervous system, plus an on-site clinical-research institute (Premiere Research
> Institute). We treat the patient, not just the disease.

## Key facts
- Address: {ADDR_STREET}, {ADDR_CITY}, {ADDR_STATE} {ADDR_ZIP}
- Phone: {PHONE}
- Accepting new patients; free memory screens available
- Website: {BASE}/

## Doctors
{doc_lines}
Our Doctors: {BASE}/our-doctors.html

## Services & conditions treated (dedicated pages)
Full services: {BASE}/services.html
{cond_lines}

## Clinical research
Premiere Research Institute — trials in Alzheimer's, migraine, and MS: {BASE}/clinical-research.html
Institute website: {RESEARCH_URL}

## Appointments & new patients
Free Memory Screen (30 min) and New Patient Appointment (1 hr): {BASE}/appointments.html
Patient Center & new-patient forms: {BASE}/patient-center.html

## Common questions
{BASE}/faq.html
""")

    body = f"""
<main>
{page_hero("404", "This Page Took a <em class='accent'>Wrong Turn</em>",
  "The page you're looking for isn't here — but our team is a click away.")}
<section class="section center">
  <div class="wrap">
    <a class="btn btn-coral" href="/index.html">Back to Home <span class="arr">&rarr;</span></a>
  </div>
</section>
</main>
"""
    write("404.html",
          head("Page Not Found | Palm Beach Neurology",
               "That page took a wrong turn. Find neurology care at Palm Beach Neurology in West Palm Beach, FL.",
               extra_schema='<meta name="robots" content="noindex">\n') + nav(0, solid=True) + body + footer(0))

if __name__ == "__main__":
    build_home()
    build_conditions()
    build_services()
    build_doctors()
    build_research()
    build_appointments()
    build_patient_center()
    build_contact()
    build_faq()
    build_meta()
    print("\nDone. Open index.html or deploy the folder to Vercel.")
