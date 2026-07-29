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
MAPS_EMBED = "https://www.google.com/maps?q=733+US+Highway+1+Suite+2A+North+Palm+Beach+FL+33408&output=embed"

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

def head(title, desc, depth=0, canonical="", og_image="assets/media/hero-poster.jpg", page_type="website", extra_schema=""):
    p = "../" * depth
    base = "https://www.firstrehabnpb.com"
    canon = f"{base}/{canonical}" if canonical else base + "/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large">
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
  "image": "https://www.firstrehabnpb.com/assets/media/clinic.jpg",
  "telephone": "+1-561-624-4263",
  "faxNumber": "+1-561-840-4234",
  "email": "firstrehabnpb@gmail.com",
  "foundingDate": "1991",
  "founder": {{ "@type": "Person", "@id": "https://www.firstrehabnpb.com/about.html#david-kashuba", "name": "David Kashuba, Ph.D.", "jobTitle": "CEO & Occupational Therapist" }},
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
  "sameAs": ["https://www.instagram.com/firstrehabnpb","https://www.facebook.com/FirstRehabNPB/","https://www.linkedin.com/company/firstrehabnpb","https://open.spotify.com/show/033A1BQq9qqsygFFCq9SIu","https://www.youtube.com/channel/UCFzCl3RvdVahfIjKZ1SfRvQ","https://maps.google.com/?cid=3809434844265673488"]
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
    <a class="brand" href="{p}index.html" aria-label="First Rehabilitation home">
      <img class="logo-dark-v" src="{p}assets/media/logo-dark-nav.png" alt="First Rehabilitation of North Palm Beach" width="111" height="68">
      <img class="logo-light-v" src="{p}assets/media/logo-nav.png" alt="First Rehabilitation of North Palm Beach" width="111" height="68">
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav-el" aria-label="Main menu">
    <ul class="nav-links">
      <li><a class="nav-item" href="{p}index.html">Home</a></li>
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
      <li><a class="nav-item" href="{p}podcast.html">Podcast</a></li>
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
}

def social_row(cls=""):
    links = "".join(
        f'<a class="soc-btn" href="{url}" target="_blank" rel="noopener" aria-label="First Rehabilitation on {name}" title="{name}">{svg}</a>'
        for name, (url, svg) in SOCIAL_ICONS.items()
    )
    return f'<div class="soc-row {cls}">{links}</div>'

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
        <h3 class="f-head">Services</h3>
        <ul>
          <li><a href="{p}services/physical-therapy.html">Physical Therapy</a></li>
          <li><a href="{p}services/occupational-therapy.html">Occupational Therapy</a></li>
          <li><a href="{p}services/hand-therapy.html">Hand Therapy</a></li>
          <li><a href="{p}services/wellness.html">Wellness &amp; Gym</a></li>
        </ul>
      </div>
      <div>
        <h3 class="f-head">Explore</h3>
        <ul>
          <li><a href="{p}treatments/index.html">What We Treat</a></li>
          <li><a href="{p}about.html">About Us</a></li>
          <li><a href="{p}first-visit.html">Your First Visit</a></li>
          <li><a href="{p}blog/index.html">Blog</a></li>
          <li><a href="{p}podcast.html">Pain 2 Power Podcast</a></li>
          <li><a href="{p}videos.html">Video Episodes</a></li>
          <li><a href="{p}faq.html">FAQ</a></li>
          <li><a href="{p}careers.html">Careers</a></li>
          <li><a href="{PORTAL}" target="_blank" rel="noopener">Patient Portal</a></li>
        </ul>
      </div>
      <div>
        <h3 class="f-head">Areas We Serve</h3>
        <ul>
          <li><a href="{p}locations/palm-beach-gardens.html">Palm Beach Gardens</a></li>
          <li><a href="{p}index.html">North Palm Beach</a></li>
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
        <h3 class="f-head">Visit Us</h3>
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
      <span><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a> &nbsp;&middot;&nbsp; <a href="{FACEBOOK}" target="_blank" rel="noopener">Facebook</a> &nbsp;&middot;&nbsp; <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a> &nbsp;&middot;&nbsp; <a href="{SPOTIFY}" target="_blank" rel="noopener">Spotify</a></span>
    </div>
  </div>
</footer>
<a class="mobile-call" href="tel:+15616244263" aria-label="Call First Rehabilitation now at 561-624-4263"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.4 21 3 13.6 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .8-.3 1l-2.2 2.2z"/></svg><span>Call Now</span></a>
<script src="{p}assets/js/main.js?v={asset_v('assets/js/main.js')}"></script>
<script src="{p}assets/js/intake.js?v={asset_v('assets/js/intake.js')}" defer></script>
<!-- Vercel Web Analytics (static-site tag; privacy-friendly, cookieless — no banner needed) -->
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments);}};</script>
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
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

def page_hero(eyebrow, title, lede, crumbs_html=""):
    return f"""
<section class="page-hero">
  <div class="hero-fallback"></div>
  <div class="beam-field" aria-hidden="true"><div class="beam" style="opacity:0.5;"></div></div>
  <div class="wrap">
    {crumbs_html}
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""

def linkify_phone(html_out):
    """Every visible mention of the clinic phone number becomes a tap-to-call link.
    Existing anchors are protected so we never nest a link inside a link."""
    import re
    protected = []
    def _protect(m):
        protected.append(m.group(0))
        return f"\x00{len(protected) - 1}\x00"
    s = re.sub(r"<(a|script)\b[^>]*>.*?</\1>", _protect, html_out, flags=re.S)
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

    social_cards = "".join(
        f'''<a class="sm-card" href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="First Rehabilitation on Instagram — photo {i}">
          <img src="assets/social/post-{i}.jpg" alt="" loading="lazy" onerror="this.closest('.sm-card').classList.add('empty')">
        </a>''' for i in range(1, 11)
        if os.path.exists(os.path.join(ROOT, f"assets/social/post-{i}.jpg"))
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

    ticker = "".join(f"<span>{s}</span>" for s in
        ["Medicare", "Medicare Advantage", "Blue Cross Blue Shield", "Aetna", "Humana", "Tricare", "VA Community Care Network", "Workers' Comp", "Self Pay"])

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
      <img src="assets/media/clinic.jpg" alt="Dr. Dave Kashuba treating a patient at First Rehabilitation" loading="lazy" onerror="this.closest('.split-media').classList.add('empty')">
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

{cta_band(0)}
</main>
"""
    write("index.html",
          head("Physical Therapy North Palm Beach | First Rehabilitation",
               "Family-owned physical therapy, occupational therapy, certified hand therapy, and wellness in North Palm Beach, FL. Serving Palm Beach County since 1991.",
               canonical="", og_image="assets/media/clinic.jpg",
               extra_schema='<link rel="preload" as="image" href="assets/media/hero-poster.jpg?v=9" fetchpriority="high">\n')
          + nav(0) + body + footer(0))

# ----------------------------------------------------------------------------
# SERVICE PAGES
# ----------------------------------------------------------------------------

SERVICES = {
    "physical-therapy": {
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
        ],
    },
    "occupational-therapy": {
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
        "title": "Hand Therapy",
        "kicker": "Restore function to your hands.",
        "lede": "Certified hand therapy for the wrist, hand, and upper extremity — one of the most precise and specialized areas of rehabilitation.",
        "intro": "Led by certified hand therapist Laura Drumm, CHT, our hand therapy program brings surgical-grade precision to rehabilitation of the hand, wrist, and upper extremity. From custom-fabricated splints to post-operative tendon protocols, every detail of care is tailored to the fine mechanics of how you grip, pinch, lift, and live.",
        "items": [
            ("Carpal Tunnel &amp; Nerve Conditions", "Conservative and post-surgical care for nerve compression, with activity modification that lasts."),
            ("Arthritis Management", "Joint protection strategies, adaptive techniques, and pain-relieving modalities for arthritic hands."),
            ("Tendon &amp; Fracture Rehabilitation", "Careful, protocol-driven recovery after tendon repair, fracture, and complex hand surgery."),
            ("Custom Splinting &amp; Orthotics", "Precision-fabricated splints made in-clinic to protect healing structures and restore function."),
            ("Post-Surgical Hand Recovery", "Coordinated care with area hand surgeons for seamless recovery from surgery to full function."),
        ],
    },
    "wellness": {
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
    # (path under assets/, object-position for the cover crop)
    svc_photo = {
        "physical-therapy": ("social/post-1.jpg", "center 30%"),
        "occupational-therapy": ("media/clinic.jpg", "center"),
        "hand-therapy": ("team/laura.jpg", "center 25%"),
        "wellness": ("media/gym.jpg", "center"),
    }
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
        crumbs = f'<div class="crumbs"><a href="../index.html">Home</a> / <a href="physical-therapy.html">Services</a> / {s["title"]}</div>'
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
        # Conditions treated with this service — internal links for SEO + discovery
        svc_conds = {
            "physical-therapy": ["back-pain", "neck-pain", "shoulder-pain", "knee-pain", "hip-pain", "ankle-pain", "post-surgical", "auto-accident"],
            "occupational-therapy": ["hand-wrist", "post-surgical", "workers-comp"],
            "hand-therapy": ["hand-wrist", "post-surgical"],
        }
        svc_cond_links = ""
        if slug in svc_conds:
            links = " &middot; ".join(
                f'<a href="../treatments/{c}.html">{CONDITIONS[c]["name"]}</a>' for c in svc_conds[slug]
            )
            svc_cond_links = f'<p class="related-links reveal"><strong>Conditions we treat with {s["title"].lower()}:</strong> {links}</p>'

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
      <div class="split-media tilt2 reveal d2">
        <img src="../assets/{svc_photo[slug][0]}" style="object-position:{svc_photo[slug][1]};" alt="{s['title']} at First Rehabilitation of North Palm Beach" loading="lazy" onerror="this.closest('.split-media').classList.add('empty')">
      </div>
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
  </div>
</section>
{cht_callout}
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
      <p>Your first appointment includes a comprehensive movement-based evaluation, an honest conversation about your goals, and a proposed plan of care — with hands-on treatment starting that very first day whenever appropriate. We accept most major insurance plans, including Medicare, and our front desk will gladly verify your coverage before you arrive.</p>
      <p>You're never a chart number here. Since 1991, our family-owned clinic has treated every patient with the individual attention that earns a 4.9&#9733; reputation across the Palm Beaches.</p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Begin with an evaluation</h3>
      <p>The first step is simple: a conversation and a movement assessment. We'll build the plan together.</p>
      <a class="btn btn-coral" href="../contact.html">Book Appointment</a>
      <div class="side-meta">
        <p>Prefer to call?<br><a href="tel:+15616244263">{PHONE}</a></p>
        <p style="margin-top:0.8rem;">Most major insurance accepted, including Medicare.</p>
      </div>
    </aside>
  </div>
</section>
{svc_faq_html}
{cta_band(1)}
</main>
"""
        svc_desc = s["lede"].replace("&amp;", "&")
        if len(svc_desc) <= 115:
            svc_desc += " Family-owned North Palm Beach clinic since 1991."
        svc_bc = breadcrumb_schema([("Home", ""), ("Services", "services/physical-therapy.html"),
                                    (s["title"], f"services/{slug}.html")]) + therapy_schema(slug, s["title"], s["lede"])
        write(f"services/{slug}.html",
              head(f'{s["title"].replace("&amp;","&")} | First Rehabilitation of North Palm Beach',
                   svc_desc, depth=1, canonical=f"services/{slug}.html",
                   extra_schema=svc_schema + svc_bc)
              + nav(1) + body + footer(1))

# ----------------------------------------------------------------------------
# CONDITION PAGES
# ----------------------------------------------------------------------------

CONDITIONS = {
    "back-pain": {
        "name": "Back Pain Relief",
        "area": "Lower Back &amp; Spine",
        "lede": "Evidence-based physical therapy for low back pain, sciatica, and spinal conditions — treating the cause, not just the symptoms.",
        "intro": "Back pain is the single most common reason people seek physical therapy, and one of the most treatable. Our approach starts with understanding <em>why</em> your back hurts — the movement patterns, postural habits, and strength deficits behind the pain — then resolving them with skilled manual therapy and progressive exercise.",
        "treats": ["Low back pain and stiffness", "Sciatica and radiating leg pain", "Herniated and bulging discs", "Degenerative disc disease", "Spinal stenosis", "Post-surgical spine recovery", "Muscle strains and spasms"],
        "approach": "Treatment typically blends hands-on manual therapy to restore mobility, targeted core and hip strengthening to support the spine, and movement retraining so daily activities stop provoking pain. You'll leave every visit with a clear home program and an honest picture of your progress.",
    },
    "neck-pain": {
        "name": "Neck Pain Relief",
        "area": "Head &amp; Neck",
        "lede": "Manual therapy, posture correction, and strengthening for neck pain, stiffness, and whiplash.",
        "intro": "Whether it crept in from years at a desk or arrived overnight after an accident, neck pain responds remarkably well to skilled physical therapy. We identify the joints, muscles, and postural patterns driving your symptoms and treat them directly.",
        "treats": ["Chronic neck pain and stiffness", "Whiplash-associated disorders", "Cervical radiculopathy (pinched nerve)", "Tension and postural neck pain", "Degenerative changes of the cervical spine", "Pain radiating to the shoulder or arm"],
        "approach": "Care usually combines gentle manual therapy and joint mobilization, deep neck flexor and postural strengthening, and workstation or sleep-position coaching. Most patients notice meaningful change within the first few weeks of consistent care.",
    },
    "shoulder-pain": {
        "name": "Shoulder Pain Relief",
        "area": "Shoulder",
        "lede": "Specialized rehabilitation for rotator cuff injuries, frozen shoulder, and everything in between.",
        "intro": "The shoulder trades stability for mobility — which is why it's so useful and so vulnerable. Our therapists restore the balance of strength and motion your shoulder depends on, whether you're recovering from surgery or trying to avoid it.",
        "treats": ["Rotator cuff strains and repairs", "Frozen shoulder (adhesive capsulitis)", "Shoulder impingement", "Bursitis and tendinitis", "Labral injuries", "Post-surgical shoulder rehabilitation", "Shoulder instability"],
        "approach": "We progress you deliberately: restoring pain-free range first, then rebuilding rotator cuff and scapular strength, then returning you to overhead reaching, lifting, sport, and sleep without guarding. Post-surgical patients follow protocols coordinated with their surgeon.",
    },
    "knee-pain": {
        "name": "Knee Pain Relief",
        "area": "Knee",
        "lede": "From arthritis to ACL recovery — rebuild strong, confident knees.",
        "intro": "Knees take the load of everything you do, and knee pain usually reflects how the whole leg is working — hips, ankles, and movement habits included. That's how we treat it: the joint, and the mechanics around it.",
        "treats": ["Knee osteoarthritis", "Total and partial knee replacement rehab", "ACL, MCL, and meniscus injuries", "Patellofemoral pain (runner's knee)", "Tendinitis and bursitis", "Post-surgical knee recovery"],
        "approach": "Expect progressive strengthening of the quadriceps, hips, and glutes, manual therapy for joint mobility, and functional retraining for stairs, walking distance, and return to activity. Joint replacement patients follow a structured pathway from first bend to full stride.",
    },
    "hip-pain": {
        "name": "Hip Pain Relief",
        "area": "Hip &amp; Pelvis",
        "lede": "Restore pain-free walking, standing, and living with targeted hip rehabilitation.",
        "intro": "Hip pain can masquerade as back pain, groin pain, or thigh pain — and vice versa. Our evaluation sorts out the true source, then treats it with the strength and mobility work the hip responds to best.",
        "treats": ["Hip osteoarthritis", "Total hip replacement rehabilitation", "Bursitis and tendinopathy", "Labral irritation", "Groin and hip flexor strains", "Gait and balance dysfunction"],
        "approach": "Care centers on restoring hip mobility, strengthening the glutes and deep stabilizers, and retraining walking mechanics. For hip replacement patients, we manage precautions early and build steadily toward confident, unassisted movement.",
    },
    "foot-pain": {
        "name": "Foot Pain Relief",
        "area": "Foot",
        "lede": "Get back on your feet — literally — with expert care for plantar fasciitis and foot pain.",
        "intro": "Foot pain changes everything downstream: how you walk, stand, exercise, and sleep. Our therapists treat the foot directly while correcting the loading patterns that caused the problem in the first place.",
        "treats": ["Plantar fasciitis and heel pain", "Foot and arch pain", "Post-fracture rehabilitation", "Tendinitis of the foot", "Balance and gait dysfunction", "Post-surgical foot recovery"],
        "approach": "Treatment blends manual therapy and targeted stretching, intrinsic foot and calf strengthening, footwear guidance, and graded return to walking and activity — so relief holds up under real life, not just in the clinic.",
    },
    "ankle-pain": {
        "name": "Ankle Pain Relief",
        "area": "Ankle",
        "lede": "Rebuild stability and strength after sprains, fractures, and chronic ankle problems.",
        "intro": "An undertreated ankle sprain is the most common reason ankles keep getting injured. We rehabilitate ankles completely — restoring not just motion and strength, but the balance and reaction time that prevent the next injury.",
        "treats": ["Acute and chronic ankle sprains", "Chronic ankle instability", "Achilles tendinitis and repair rehab", "Post-fracture rehabilitation", "Stiffness and loss of motion", "Balance deficits after injury"],
        "approach": "Expect early swelling and mobility management, progressive strengthening and balance training, and sport- or activity-specific work before you return to full speed. Our goal is an ankle you never have to think about.",
    },
    "hand-wrist": {
        "name": "Hand &amp; Wrist Therapy",
        "area": "Wrist &amp; Hand",
        "lede": "Certified hand therapy for the intricate mechanics of your hands and wrists.",
        "intro": "Few areas of the body demand more specialized rehabilitation than the hand. Our certified hand therapy program — led by Laura Drumm, CHT — provides precise, protocol-driven care for conditions and surgeries of the hand, wrist, and forearm, including custom splinting fabricated in-clinic.",
        "treats": ["Carpal tunnel syndrome", "Wrist fractures and sprains", "Tendon injuries and repairs", "Trigger finger", "Arthritis of the hand and thumb", "Post-surgical hand rehabilitation"],
        "approach": "Care is exacting by design: custom orthoses to protect healing structures, graded motion and strengthening timed to tissue healing, and functional retraining for grip, pinch, and dexterity. We coordinate closely with area hand surgeons throughout recovery.",
    },
    "headache-relief": {
        "name": "Headache Relief",
        "area": "Head &amp; Neck",
        "lede": "Physical therapy for cervicogenic headaches and tension-type headaches that start in the neck.",
        "intro": "Many chronic headaches don't start in the head at all — they start in the neck. When joint stiffness, muscle tension, and posture are the drivers, physical therapy can reduce headache frequency and intensity dramatically.",
        "treats": ["Cervicogenic headaches", "Tension-type headaches", "Headaches after whiplash or concussion", "Neck-related migraine triggers", "Jaw and postural contributions to head pain"],
        "approach": "We treat the upper cervical joints and surrounding muscles with skilled manual therapy, then address the postural and strength deficits that let tension rebuild. Most patients also receive simple daily strategies that make a measurable difference between visits.",
    },
    "post-surgical": {
        "name": "Post-Surgical Rehabilitation",
        "area": "Full Body",
        "lede": "Structured, surgeon-coordinated recovery from joint replacement, spine surgery, and beyond.",
        "intro": "Surgery is the beginning of recovery, not the end. Our post-surgical programs translate your surgeon's protocol into week-by-week progress — protecting what was repaired while steadily rebuilding the strength and confidence surgery was meant to restore.",
        "treats": ["Total knee and hip replacement", "Shoulder and rotator cuff repair", "Spinal surgery recovery", "Hand and wrist surgery", "Foot and ankle surgery", "Fracture fixation recovery"],
        "approach": "We follow your surgeon's protocol precisely, communicate progress clearly, and adjust based on how your tissue is actually healing. From first post-op visit through final clearance, you'll always know what phase you're in and what milestone comes next.",
    },
    "workers-comp": {
        "name": "Workers' Compensation Rehab",
        "area": "Work Injury",
        "lede": "Get better and get back to work — with the documentation and communication your case requires.",
        "intro": "A work injury involves more than healing: it involves adjusters, case managers, physicians, and return-to-work timelines. We've handled workers' compensation cases for decades, providing excellent clinical care alongside the clear, timely documentation every party needs.",
        "treats": ["Lifting and overexertion injuries", "Repetitive strain injuries", "Back and shoulder work injuries", "Hand and upper extremity injuries", "Slip, trip, and fall injuries", "Post-surgical work injury recovery"],
        "approach": "Treatment is functional from day one — built around the physical demands of your actual job. We provide objective progress reporting, coordinate with your physician and case manager, and prepare you for a safe, sustainable return to work.",
    },
    "auto-accident": {
        "name": "Auto Accident Recovery",
        "area": "Full Body",
        "lede": "Comprehensive rehabilitation after a car accident — from whiplash to complex multi-area injuries.",
        "intro": "Even a minor collision can leave lasting pain, and symptoms often surface days after the accident. Early, skilled rehabilitation is the best predictor of full recovery — and we make the process straightforward, including the documentation your claim requires.",
        "treats": ["Whiplash and neck injuries", "Back and spine injuries", "Shoulder and knee trauma", "Headaches after collision", "Soft tissue strains and sprains", "Anxiety about returning to movement"],
        "approach": "Care begins gently — calming irritated tissue and restoring basic motion — then progresses to strengthening and full return to daily activity. We document objectively throughout, and communicate with your physician and representatives as needed.",
    },
}

def build_conditions():
    cards = "".join(
        f'<a class="cond-card reveal" href="{slug}.html"><span class="cond-tag">{c["area"]}</span><h3>{c["name"]}</h3><p>{c["lede"]}</p></a>'
        for slug, c in CONDITIONS.items()
    )
    crumbs = '<div class="crumbs"><a href="../index.html">Home</a> / What We Treat</div>'
    body = f"""
<main>
{page_hero("What We Treat", "Overview of Treatments",
  "Twelve specialized treatment pathways — every one beginning with a thorough evaluation and a plan built for you.", crumbs)}
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
               "Explore the conditions we treat: back, neck, shoulder, knee, hip, foot, ankle, hand & wrist, headaches, post-surgical rehab, workers' comp, and auto accident recovery.", depth=1, canonical="treatments/index.html",
               extra_schema=breadcrumb_schema([("Home", ""), ("What We Treat", "treatments/index.html")]))
          + nav(1) + body + footer(1))

    cond_slugs = list(CONDITIONS)
    svc_for = {"hand-wrist": ("hand-therapy", "Certified Hand Therapy"),
               "workers-comp": ("occupational-therapy", "Occupational Therapy"),
               "post-surgical": ("physical-therapy", "Physical Therapy")}
    for slug, c in CONDITIONS.items():
        COND_BLOG = {"knee-pain": ("knee-arthritis-before-surgery", "Knee Pain: What to Try Before You Think About Surgery"),
                     "back-pain": ("five-morning-habits-back-pain", "Five Morning Habits That Ease Back Pain"),
                     "hand-wrist": ("why-hand-therapy-is-different", "Why Hand Therapy Is Its Own Specialty")}
        if slug in COND_BLOG:
            _bslug, _btitle = COND_BLOG[slug]
            blog_link = f'<section class="section" style="padding:1.6rem 0 0;"><div class="wrap"><p class="crumbs" style="margin:0;">From the blog: <a href="../blog/{_bslug}.html">{_btitle}</a></p></div></section>'
        else:
            blog_link = ""
        treats = "".join(f"<li>{t}</li>" for t in c["treats"])
        # Related-care internal links: primary service + neighboring conditions
        i = cond_slugs.index(slug)
        prev_s, next_s = cond_slugs[i - 1], cond_slugs[(i + 1) % len(cond_slugs)]
        sv, sv_name = svc_for.get(slug, ("physical-therapy", "Physical Therapy"))
        rel_links = (f'<p class="related-links"><strong>Related care:</strong> '
                     f'<a href="../services/{sv}.html">{sv_name}</a> &middot; '
                     f'<a href="{prev_s}.html">{CONDITIONS[prev_s]["name"]}</a> &middot; '
                     f'<a href="{next_s}.html">{CONDITIONS[next_s]["name"]}</a></p>')
        crumbs = f'<div class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">What We Treat</a> / {c["name"]}</div>'
        body = f"""
<main>
{page_hero(c["area"], c["name"], c["lede"], crumbs)}{blog_link}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p>{c["intro"]}</p>
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
        write(f"treatments/{slug}.html",
              head(f"{title_short} in North Palm Beach | First Rehabilitation",
                   cond_desc, depth=1, canonical=f"treatments/{slug}.html", page_type="article",
                   extra_schema=cond_bc)
              + nav(1) + body + footer(1))


# ----------------------------------------------------------------------------
# LOCATION PAGES — genuinely useful area pages served from the NPB clinic
# ----------------------------------------------------------------------------

LOCATIONS = {
    "palm-beach-gardens": {
        "city": "Palm Beach Gardens",
        "title": "Physical Therapy Palm Beach Gardens | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for Palm Beach Gardens — minutes south on US-1 in North Palm Beach. Family-owned since 1991.",
        "h1": "Serving <em class='accent'>Palm Beach Gardens</em>",
        "kicker": "Palm Beach Gardens",
        "lede": "Complete outpatient rehabilitation for Gardens residents — physical therapy, occupational therapy, certified hand therapy, and an on-site wellness gym, minutes away in North Palm Beach.",
        "deep": True,
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
        "title": "Physical Therapy Tequesta FL | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for Tequesta residents — a scenic drive down US-1 to our North Palm Beach clinic. Since 1991.",
        "h1": "Serving <em class='accent'>Tequesta</em>",
        "kicker": "Tequesta",
        "lede": "From the Village of Tequesta, our family-owned clinic is a simple drive south — and the depth of care under one roof makes the trip worth it.",
        "deep": False,
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
        "title": "Physical Therapy Palm Beach FL | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for Palm Beach residents — attentive, one-on-one care in North Palm Beach. Family-owned since 1991.",
        "h1": "Serving <em class='accent'>Palm Beach</em>",
        "kicker": "Palm Beach",
        "lede": "Palm Beach residents expect care that is personal, unhurried, and expert. That is exactly how this clinic has run since 1991 — one-on-one, hands-on, and led by the founder.",
        "deep": False,
        "drive": "From the island, cross to the mainland and head north on US-1 to 733 US Highway 1, Suite 2A, North Palm Beach. Our front desk at 561-624-4263 will gladly walk you through the easiest route and parking before your first visit.",
        "conditions": ["post-surgical", "hip-pain", "hand-wrist", "back-pain"],
    },
    "west-palm-beach": {
        "city": "West Palm Beach",
        "title": "Physical Therapy West Palm Beach | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, and certified hand therapy for West Palm Beach — north on US-1 or I-95 to our family-owned North Palm Beach clinic.",
        "h1": "Serving <em class='accent'>West Palm Beach</em>",
        "kicker": "West Palm Beach",
        "lede": "Plenty of clinics dot West Palm Beach — but patients drive north to us for what few offer: PT, OT, certified hand therapy, and a wellness gym under one family-owned roof.",
        "deep": False,
        "drive": "From West Palm Beach, head north on US-1 or take I-95 to Northlake Boulevard; we're at 733 US Highway 1, Suite 2A in North Palm Beach. Call 561-624-4263 and our front desk will point you right to the door.",
        "conditions": ["back-pain", "neck-pain", "auto-accident", "workers-comp", "post-surgical"],
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
        "title": "Physical Therapy Juno Beach FL | First Rehabilitation",
        "desc": "Physical therapy, occupational therapy, certified hand therapy, and wellness for Juno Beach — just down US-1 in North Palm Beach. Family-owned since 1991.",
        "h1": "Serving <em class='accent'>Juno Beach</em>",
        "kicker": "Juno Beach",
        "lede": "Juno Beach neighbors are practically next door — our family-owned clinic is just down US-1 in North Palm Beach.",
        "deep": False,
        "drive": "Juno Beach sits immediately north of us on US-1 — our clinic at 733 US Highway 1, Suite 2A, North Palm Beach is just a few minutes down the road. Call 561-624-4263 for directions and parking guidance.",
        "conditions": ["back-pain", "hip-pain", "foot-pain", "post-surgical"],
    },
}

def build_locations():
    import json as _json
    for slug, L in LOCATIONS.items():
        crumbs = f'<div class="crumbs"><a href="../index.html">Home</a> / {L["city"]}</div>'
        cond_links = " &middot; ".join(
            f'<a href="../treatments/{c}.html">{CONDITIONS[c]["name"]}</a>' for c in L["conditions"]
        )
        team_cards = "".join(
            f'<div class="svc-feature reveal"><span class="svc-feature-num">{i+1:02d}</span>'
            f'<div><h3>{t["name"]}</h3><p><strong>{t["role"]}.</strong> {t["blurb"]}</p></div></div>'
            for i, t in enumerate(TEAM) if L["deep"] or i < 3
        )
        deep_extra = ""
        if L["deep"]:
            deep_extra = f'''
<section class="section on-cream">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">Why Gardens Residents Choose Us</span>
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
{page_hero(L["kicker"], L["h1"], L["lede"], crumbs)}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p>{L["lede"]} We accept Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, the VA Community Care Network (VACCN), workers' compensation, and self-pay — and our front desk verifies your coverage before your first visit.</p>
      <h2>Getting here from {L["city"]}</h2>
      <p>{L["drive"]}</p>
      <h2>Our team, by name</h2>
      <p>Unlike clinics that list no practitioners at all, we're proud to tell you exactly who will guide your recovery: David Kashuba, Ph.D. (CEO &amp; Occupational Therapist, treating patients since 1991), Kayla Dorsey, DPT and Logan Van Sant (Physical Therapists), Joni Janik (Occupational Therapist), and Laura Drumm (Certified Hand Therapist). Meet everyone on our <a href="../about.html">About page</a>.</p>
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
    {"name": "David Kashuba, Ph.D.", "role": "CEO &amp; Occupational Therapist",
     "blurb": "Founded First Rehabilitation in 1991 and still treats patients hands-on every day — leading the clinic's comprehensive, high-end approach to rehabilitation across three decades and tens of thousands of recoveries.",
     "img": "david.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Nick Kashuba", "role": "Chief Operating Officer",
     "blurb": "Second-generation leadership keeping the clinic's family-owned values — and its promise that our people make the difference — at the center of everything we do.",
     "img": "nick.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Logan Van Sant", "role": "Physical Therapist",
     "blurb": "A wealth of knowledge in the physical therapy world, dedicated to helping patients move and feel their best.",
     "img": "logan.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Kayla Dorsey, DPT", "role": "Physical Therapist",
     "blurb": "A Doctor of Physical Therapy with over a decade of extensive clinical experience in personalized, hands-on care.",
     "img": "kayla.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Joni Janik", "role": "Occupational Therapist",
     "blurb": "Helps patients reclaim the daily activities that matter most — restoring independence, confidence, and quality of life.",
     "img": "joni.jpg", "bio": "", "specialties": [], "fun_fact": ""},
    {"name": "Laura Drumm", "role": "Certified Hand Therapist",
     "blurb": "Leads our certified hand therapy program with surgical-grade precision — from custom splinting to post-operative tendon protocols.",
     "img": "laura.jpg", "bio": "", "specialties": [], "fun_fact": ""},
]

def build_about():
    # A card is expandable ONLY when the person's long-form bio exists.
    # Empty bio -> the exact static card the page has always shown, with no
    # expand affordance. Filling in TEAM[n]["bio"] flips the card on rebuild.
    def _team_card(i, t):
        slug = t["name"].lower().split(",")[0].replace(" ", "-").replace(".", "")
        base = f'''<div class="team-photo">
          <img src="assets/team/{t["img"]}" alt="{t["name"]}, {t["role"]} at First Rehabilitation of North Palm Beach" loading="lazy" onerror="this.closest('.team-photo').classList.add('empty')">
        </div>
        <h3>{t["name"]}</h3><div class="role">{t["role"]}</div><p>{t["blurb"]}</p>'''
        if not t["bio"]:
            return f'<div class="team-card reveal d{i%3+1}">{base}</div>'
        spec = ("".join(f'<li>{s}</li>' for s in t["specialties"]))
        spec_html = f'<h4>Specialties</h4><ul class="tp-specs">{spec}</ul>' if spec else ""
        fun_html = f'<p class="tp-fun"><strong>Fun fact:</strong> {t["fun_fact"]}</p>' if t["fun_fact"] else ""
        return f'''<button type="button" class="team-card team-card-open reveal d{i%3+1}" data-profile="tp-{slug}" aria-haspopup="dialog">
        {base}<span class="tp-more" aria-hidden="true">Read full profile &rarr;</span></button>
        <dialog class="team-profile" id="tp-{slug}" aria-label="Profile: {t["name"]}">
          <div class="tp-inner">
            <button type="button" class="tp-close" aria-label="Close profile">&#10005;</button>
            <div class="tp-head">
              <img src="assets/team/{t["img"]}" alt="" loading="lazy">
              <div><h3>{t["name"]}</h3><div class="role">{t["role"]}</div></div>
            </div>
            <div class="tp-body"><p>{t["bio"]}</p>{spec_html}{fun_html}</div>
          </div>
        </dialog>'''
    team_html = "".join(_team_card(i, t) for i, t in enumerate(TEAM))
    body = f"""
<main>
{page_hero("Since 1991", "Family-Owned. <em class='accent'>Patient-Devoted.</em>",
  "Three decades of healing the Palm Beaches — built on one founder's vision and carried forward by family.",
  '<div class="crumbs"><a href="index.html">Home</a> / About</div>')}
<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our Story</span>
      <h2>One Vision, <em class="accent">Generations of Care</em></h2>
      <p style="margin-top:1.2rem;">Since 1991, First Rehabilitation of North Palm Beach has been a cornerstone of recovery for the Palm Beaches. Founded by David Kashuba, Ph.D., our mission has always been to provide a comprehensive, high-end approach to rehabilitation — one that heals the body and restores the spirit.</p>
      <p style="margin-top:1rem;">What makes us different is what happens after therapy ends. Our exclusive on-site wellness program means graduation from PT or OT isn't goodbye — it's a transition into lifelong strength, guided by the same team that got you well.</p>
      <div class="stat-row">
        <div><strong data-count="39" data-suffix="+">39+</strong><span>Years of Expertise</span></div>
        <div><strong data-count="180000" data-suffix="+">180,000+</strong><span>Patients Treated</span></div>
        <div><strong>4.9★</strong><span>Google Rating</span></div>
        <div><strong>Est. 1991</strong><span>Family-Owned</span></div>
      </div>
    </div>
    <div class="split-media tilt2 reveal d2">
      <img src="assets/media/founder.jpg" alt="Dr. Dave Kashuba, founder of First Rehabilitation of North Palm Beach" loading="lazy" onerror="this.closest('.split-media').classList.add('empty')">
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
    ("Episode 7", "Dr. Rami Elkhechen, M.D.", "Orthopedic surgery isn't always the answer — and knowing when it is may be the most important call a surgeon makes. Dr. Rami Elkhechen, M.D., a board-certified, fellowship-trained sports medicine orthopedic surgeon with Orthopaedic Care Specialists in North Palm Beach, joins Dave and Mike to dig into exactly that. Trained at NYU School of Medicine with a sports medicine fellowship at New Orleans' Ochsner Sports Medicine Institute — and a former assistant team physician for the Saints and Pelicans — he treats everyone from weekend athletes to trauma patients, with a focus on hip arthroscopy, shoulder surgery, cartilage preservation, and orthobiologics. Together they unpack what actually separates a surgical candidate from someone better served by conservative care, why rehab so often decides the outcome, and how patients can take a more active role in their own recovery.", "https://open.spotify.com/episode/1cVdymVweFWtoIRropqKQ7", "Listen"),
    ("Episode 6", "Dr. Richard Weiner, M.D.", "World-renowned orthopedic surgeon Dr. Richard Weiner joins Dave and Mike for a candid conversation about joint replacement, staying active as you age, and what it really takes to get patients moving pain-free again. With more than 35 years in practice and thousands of hip and knee replacements to his name, Dr. Weiner brings a uniquely technical eye to orthopedic care — shaped by his training in both engineering and medicine at the University of Pennsylvania. A must-listen for anyone considering surgery or determined to avoid it.", "https://open.spotify.com/episode/6zhOBEvVnxwH7PvmRAu52e", "Listen"),
    ("Episode 5", "Logan Van Sant, DPT", "Doctor of Physical Therapy Logan Van Sant sits down to share what modern physical therapy really looks like — beyond the stretches and exercises most people expect. Logan digs into how the right movement, at the right time, restores strength and confidence after injury, and why the therapist-patient relationship is at the heart of every successful recovery. A genuine wealth of knowledge from one of the sharp young minds shaping PT today.", "https://open.spotify.com/episode/4HIjJt1f7U7Uv0IJCQnyxr", "Listen"),
    ("Episode 4", "Kayla Dorsey, DPT &amp; Dr. Murray Goldberg, M.D.", "A double-header of expertise. Kayla Dorsey, a Doctor of Physical Therapy with over a decade of hands-on experience, unpacks how personalized, one-on-one care changes recovery outcomes. Then Dr. Murray Goldberg — a board-certified urologist serving Palm Beach County since 1991 — joins to discuss men's health, aging well, and why staying proactive about your body pays off for decades. Two perspectives, one theme: taking ownership of your health.", "https://open.spotify.com/episode/3BRC4CtKqjyOGf1BmJrztj", "Listen"),
    ("Episode 3", "Dr. Timur Urakov, M.D.", "Spine surgery, demystified. Dr. Timur Urakov, Associate Professor of Clinical Medicine at the University of Miami, joins the show to explain how today's spine care has changed — from minimally invasive techniques to the advanced surgical technology now used to treat conditions along the entire spine. He and Dave tackle the questions patients are most afraid to ask about back and neck surgery, and when it is (and isn't) the right call.", "https://open.spotify.com/episode/1d1rzNKiSGdMhHsTHXPBQm", "Listen"),
    ("Episode 2", "Dr. Tom Saylor, M.D.", "The hand is the body's most intricate tool — and repairing it takes a specialist. Hand and upper-extremity surgeon Dr. Tom Saylor joins Dave and Mike to talk about the surgical side of restoring hand function, from carpal tunnel and tendon repairs to complex reconstruction. It's a natural fit for First Rehabilitation, home to a certified hand therapy program, and a fascinating look at how surgeon and therapist work hand-in-hand to bring patients back to full function.", "https://open.spotify.com/episode/1a4jO3BCBrYhYL8KF01hOi", "Listen"),
    ("Episode 1", "Intro to Dave's Background", "The one that started it all. In this first episode, Dr. Dave Kashuba tells his story — how he built First Rehabilitation of North Palm Beach from the ground up in 1991, what nearly four decades and 180,000+ patients have taught him about healing, and the philosophy behind the name Pain 2 Power. Co-host Mike McGann draws out the moments that shaped Dave's approach to care, resilience, and why &ldquo;our people make the difference&rdquo; is more than a tagline.", "https://open.spotify.com/episode/70Yn3oyi2YcesDkivraogc", "Listen"),
]

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
            graph.append({"@type": "PodcastEpisode", "name": _faq_plain(title),
                          "description": _faq_plain(desc), "url": url,
                          "partOfSeries": {"@type": "PodcastSeries", "name": "Pain 2 Power"}})
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

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
        return f'''<div class="pod-card reveal">
          <div class="pod-head"><span class="pod-num">{num}</span><h3>{title}</h3><p>{desc}</p></div>
          {action}
        </div>'''
    featured = _episode_block(*EPISODES[0])
    eps = "".join(_episode_block(*e) for e in EPISODES[1:])
    body = f"""
<main>
{page_hero("The Pain 2 Power Podcast", "Real Conversations That <em class='accent'>Move You Forward</em>",
  "Dr. Dave Kashuba and Mike McGann cover the world of physical rehab and wellness — with some of the sharpest minds in medicine.",
  '<div class="crumbs"><a href="index.html">Home</a> / Podcast</div>')}
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
          <img src="assets/team/david.jpg" alt="Dr. Dave Kashuba" loading="lazy">
          <div>
            <h3>Dave Kashuba, Ph.D.</h3>
            <div class="role">Founder &amp; Occupational Therapist</div>
            <p>Founder of First Rehabilitation and a practicing occupational therapist, Dave has personally guided the care of more than 180,000 patients over 39+ years, bringing a lifetime of hands-on experience to every conversation about healing and resilience.</p>
          </div>
        </div>
        <div class="host-bio reveal d2">
          <img src="assets/media/mike.jpg" alt="Mike McGann" loading="lazy">
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
               extra_schema=_podcast_schema() + breadcrumb_schema([("Home", ""), ("Podcast", "podcast.html")]))
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
         "We've been serving the Palm Beaches since 1991 — more than three decades of family-owned, independent care under the same name and philosophy. Founder Dave Kashuba, Ph.D., an occupational therapist, has personally guided the care of more than 180,000 patients over his career."),
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
    """Person JSON-LD for every named clinician/leader (E-E-A-T)."""
    import json as _json
    knows = {
        "David Kashuba, Ph.D.": ["Occupational Therapy", "Outpatient Rehabilitation", "Clinic Leadership"],
        "Nick Kashuba": ["Healthcare Operations", "Patient Experience"],
        "Logan Van Sant": ["Physical Therapy", "Orthopedic Rehabilitation"],
        "Kayla Dorsey, DPT": ["Physical Therapy", "Orthopedic Rehabilitation", "Post-Surgical Rehabilitation"],
        "Joni Janik": ["Occupational Therapy", "Activities of Daily Living", "Stroke Recovery"],
        "Laura Drumm": ["Certified Hand Therapy", "Custom Splinting", "Upper Extremity Rehabilitation"],
    }
    creds = {
        "David Kashuba, Ph.D.": "Ph.D.",
        "Kayla Dorsey, DPT": "DPT (Doctor of Physical Therapy)",
        "Laura Drumm": "CHT (Certified Hand Therapist)",
    }
    people = []
    for t in TEAM:
        name, role = t["name"], t["role"]
        # Prefer the real long-form bio once the owner supplies it.
        desc = t["bio"] or t["blurb"]
        slug = name.lower().split(",")[0].replace(" ", "-").replace(".", "")
        p = {"@type": "Person",
             "@id": f"https://www.firstrehabnpb.com/about.html#{slug}",
             "name": _faq_plain(name),
             "jobTitle": _faq_plain(role),
             "description": _faq_plain(desc),
             "worksFor": ORG_REF,
             "knowsAbout": knows.get(name, ["Rehabilitation"])}
        if name in creds:
            p["hasCredential"] = {"@type": "EducationalOccupationalCredential", "name": creds[name]}
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
  '<div class="crumbs"><a href="index.html">Home</a> / FAQ</div>')}
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
  '<div class="crumbs"><a href="index.html">Home</a> / Contact</div>')}
<section class="section">
  <div class="wrap contact-grid">
    <div class="appt-form-card reveal">
      <h2 class="h3-size">Request an Appointment</h2>
      <p class="af-sub">Tell us a little about what you need and our front desk will call you back within one business day.</p>
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
        <div class="af-field">
          <label for="af-time">Preferred call time</label>
          <select id="af-time" name="time">
            <option>Anytime</option>
            <option>Morning</option>
            <option>Afternoon</option>
          </select>
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
    </div>
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
    "what-to-expect-first-pt-visit": {
        "title": "What to Expect at Your First Physical Therapy Visit",
        "date": "July 2026",
        "tag": "Getting Started",
        "teaser": "Nervous about your first appointment? Here's exactly how the first hour goes at First Rehabilitation — no surprises, no jargon.",
        "body": """
<p>If you've never been to physical therapy before, the first visit can feel like a mystery. Here's the honest walkthrough of how it works at our clinic, so you can arrive relaxed and ready.</p>
<h2>It starts with a conversation</h2>
<p>Before anyone touches anything, your therapist sits down with you. When did the pain start? What makes it better or worse? What does it keep you from doing — golf, gardening, picking up a grandchild, sleeping through the night? Your goals shape everything that follows, so the more honestly you answer, the better your plan will be.</p>
<h2>Then, a movement evaluation</h2>
<p>Your therapist will watch you move: walking, bending, reaching, whatever relates to your condition. We measure strength, range of motion, and balance, and we identify the specific patterns contributing to your pain. This is detective work, and it's the foundation of your entire recovery.</p>
<h2>Treatment usually begins on day one</h2>
<p>Most patients receive hands-on treatment at the very first visit — gentle manual therapy, guided movement, and the first one or two exercises of a home program. You'll leave knowing what's going on, what the plan is, and what you can do between visits to speed things along.</p>
<h2>What to bring and wear</h2>
<p>Comfortable clothes you can move in (shorts for knee and hip conditions, a loose shirt for shoulders), your insurance card, and any imaging or referral paperwork your physician provided. Our front desk verifies coverage before you arrive, so billing questions never ambush you.</p>
<p>Ready to get started? Call us at 561-624-4263 or <a href="../contact.html">request an appointment online</a> — and our <a href="../faq.html">FAQ</a> answers 73 real patient questions.</p>
""",
    },
    "five-morning-habits-back-pain": {
        "title": "Five Morning Habits That Ease Back Pain",
        "date": "July 2026",
        "tag": "Back &amp; Spine",
        "teaser": "The first thirty minutes of your day set the tone for your spine. Small changes to how you wake, move, and sit can pay off all day long.",
        "body": """
<p>Backs are often at their stiffest first thing in the morning — discs rehydrate overnight, muscles cool down, and the first movements of the day can feel like the hardest. These five habits, drawn from what we teach patients every week, make mornings kinder to your spine.</p>
<h2>1. Don't sit up straight out of bed</h2>
<p>Roll to your side first, drop your legs off the edge, and push up with your arms. This "log roll" spares your spine the loaded crunch of a straight sit-up while tissues are still waking up.</p>
<h2>2. Give it two gentle minutes</h2>
<p>Before coffee, spend two minutes moving gently: a few pelvic tilts lying on your back, knees rocking side to side, or a slow walk around the house. Motion is lotion — easy movement restores circulation and eases that first-hour stiffness.</p>
<h2>3. Rethink the couch scroll</h2>
<p>Thirty minutes slumped over a phone puts sustained load on the very structures that stiffened overnight. If you like a slow morning, sit supported — back against a chair, phone raised — rather than folded into the couch.</p>
<h2>4. Warm water helps more than you'd think</h2>
<p>A warm shower relaxes paraspinal muscles and makes the morning's movement easier. Let the water hit your lower back for a minute or two and follow it with a gentle forward and backward bend.</p>
<h2>5. Anchor one strengthening habit</h2>
<p>The long-term fix for most recurring back pain is strength — core, hips, and glutes. Attaching one simple exercise (a bridge, a bird-dog) to an existing habit like brushing your teeth makes it stick.</p>
<p>If mornings are consistently painful, or pain radiates into your leg, that's worth a professional look. Our <a href="../treatments/back-pain.html">back pain program</a> starts with finding the <em>why</em> — and most patients are surprised how treatable it is.</p>
""",
    },
    "why-hand-therapy-is-different": {
        "title": "Why Hand Therapy Is Its Own Specialty",
        "date": "June 2026",
        "tag": "Hand Therapy",
        "teaser": "Twenty-seven bones, over thirty muscles, and the finest motor control in the human body — here's why your hand deserves a certified specialist.",
        "body": """
<p>When people hear we have a Certified Hand Therapist on staff, they often ask: isn't that just physical therapy for a smaller body part? Not quite — and the difference matters enormously for your recovery.</p>
<h2>The hand is a precision instrument</h2>
<p>Your hand and wrist contain twenty-seven bones, a web of tendons gliding through tight tunnels, and nerves responsible for the finest motor control in your body. A few millimeters of scar tissue in the wrong place can mean the difference between a full grip and a permanent limitation. Rehabilitation at this scale demands specialized training.</p>
<h2>What "CHT" actually means</h2>
<p>A Certified Hand Therapist has completed thousands of hours of specialized upper-extremity practice and passed a rigorous national examination. It's one of the most demanding credentials in rehabilitation — and it's why hand surgeons refer their post-operative patients specifically to CHTs.</p>
<h2>Custom splinting, made in-clinic</h2>
<p>One of the most visible differences: custom orthoses. Our hand therapy program, led by Laura Drumm, CHT, fabricates precision splints in the clinic, molded to your hand, to protect healing structures at exactly the right angles at exactly the right stage of recovery.</p>
<h2>Timing is everything</h2>
<p>After a tendon repair or fracture, tissue healing follows a strict biological timeline. Move too soon and you risk the repair; too late and you lose motion to stiffness. Protocol-driven hand therapy walks that line precisely, in coordination with your surgeon.</p>
<p>If you're facing hand surgery, dealing with <a href="../treatments/hand-wrist.html">carpal tunnel</a>, or fighting arthritis in your thumbs, ask about our <a href="../services/hand-therapy.html">certified hand therapy program</a> — it's one of the things that makes First Rehabilitation different.</p>
""",
    },
    "knee-arthritis-before-surgery": {
        "title": "Knee Pain: What to Try Before You Think About Surgery",
        "date": "July 2026",
        "iso": "2026-07-20",
        "tag": "Knees &amp; Joints",
        "teaser": "An orthopedic surgeon joined our Pain 2 Power podcast to talk knees: what causes the pain, the home exercises that help, and why surgery comes last.",
        "body": """
<p>If your knees ache on stairs, swell after a walk, or make you think twice about kneeling in the garden, you're in familiar company — knee pain is one of the most common reasons people walk through our doors. On a recent episode of our <a href="../podcast.html">Pain 2 Power radio show</a>, Dr. Dave Kashuba sat down with Dr. Richard Weiner, M.D., an orthopedic surgeon he has worked alongside since 1990, to talk about what actually helps a painful knee — and why the operating room is the last stop, not the first.</p>
<p><em>By The First Rehabilitation Team · Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>What's usually behind knee pain</h2>
<p>Three culprits come up again and again. The most common is osteoarthritis — a gradual wearing of the joint that Dr. Kashuba notes he sometimes sees in patients as young as their mid-thirties, while some ninety-year-olds have none at all. The other two are ligament injuries (a ligament connects bone to bone) and tendon problems such as tendonitis (a tendon connects muscle to bone). Which one you're dealing with changes the plan completely, which is why both doctors kept returning to the same theme: a careful evaluation comes first. As Dr. Weiner put it, "you don't treat an X-ray, you treat the patient."</p>
<h2>Surgery is the last resort — an orthopedic surgeon says so</h2>
<p>It says something when a surgeon spends most of a radio hour talking about how to keep people out of his operating room. Dr. Weiner described the ladder he climbs with his own patients: first, avoiding the activities that aggravate the knee; then therapy — "physical therapy is key because you need to have strong muscles to stabilize the knee to have fewer symptoms" — then medication or targeted injections, and bracing. Surgery only enters the conversation when all of that has genuinely been tried, and he noted that the vast majority of the knee patients he treats never need an operation at all.</p>
<p>That matches how we work. A <a href="../services/physical-therapy.html">physical therapy</a> plan for a painful knee is built around strengthening the muscles that support the joint — including the hip and ankle, which share the load — so the knee itself has less work to do. You can read more about our approach on our <a href="../treatments/knee-pain.html">knee pain page</a>.</p>
<h2>The weight-and-knees math worth knowing</h2>
<p>One number from the episode stuck with us. Citing studies, Dr. Weiner explained that each extra pound of body weight adds roughly five pounds of stress to the knee during activities like squatting and stair climbing — so losing ten pounds can take about fifty pounds of stress off each knee. He listed excess weight among the main risk factors for knee arthritis, alongside genetics and past injuries. None of that is a lecture; it's leverage. Small changes buy your knees real relief.</p>
<h2>Four simple exercises you can do at home</h2>
<p>Dr. Kashuba walked listeners through a short routine that needs nothing more than a sturdy chair and a low step stool. Move gently, stay within a comfortable range, and stop if anything sharpens the pain.</p>
<p><strong>Seated kick-outs.</strong> Sit at the front edge of a chair and slowly straighten one knee out in front of you, then lower it. Work toward three sets of ten on each side, building over time to three sets of twenty.</p>
<p><strong>Standing knee curls.</strong> Hold the back of the chair, stand tall, and bring one heel up toward your seat as far as comfortable. Same target: three sets of ten, building to twenty.</p>
<p><strong>Sit-to-stands with a pillow.</strong> Hold a light pillow out in front of you as you stand up from the chair, and keep it reached forward as you sit back down. Reaching forward makes you hinge at the hips — and the joint that starts the movement takes the brunt of the load, which your hips handle far better than your knees.</p>
<p><strong>Step-stool lean-ins.</strong> With a hand on the chair for balance, place one foot on a low step stool and gently rock your weight forward over that foot, then back. No stepping up — just a slow, controlled lean, repeated.</p>
<p>Round the routine out with regular walking, which both doctors recommended. And thinking has moved past strict rest: for a cranky knee, gentle movement plus elevation, ice, and light compression tends to serve you better than keeping it perfectly still.</p>
<h2>When it's time to stop self-treating</h2>
<p>Home exercise has limits, and knowing them protects you. Get evaluated if your knee pain isn't settling, if swelling or warmth develops, if the knee gives way or locks up, or if symptoms start interfering with your everyday activities — walking, standing, sleeping. And one situation shouldn't wait: a pop followed by sudden pain and a leg you can't stand on is a day for an orthopedic specialist or the hospital, not a stretching session.</p>
<p>The pattern both doctors agreed on: the sooner a problem is looked at, the easier it usually is to address.</p>
<h2>Start with an evaluation, not an operation</h2>
<p>Most knee pain responds to conservative care — and finding out where you stand costs you a phone call. Our therapists evaluate your knee, tell you honestly whether therapy is likely to help, and coordinate with your physician or an orthopedic specialist when you need one. Call us at 561-624-4263, or hear the full conversation on the <a href="../podcast.html">Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different — please consult a qualified professional about yours.</em></p>
""",
    },
    "headaches-that-start-in-the-neck": {
        "title": "The Headache That Starts in Your Neck",
        "date": "July 2026",
        "iso": "2026-07-21",
        "tag": "Headaches &amp; Neck",
        "teaser": "Many stubborn, recurring headaches really start in the neck. Learn the signs, how physical therapy treats the driver, and when a headache needs a doctor first.",
        "body": """
<p>You know the headache before it fully arrives — the dull ache that creeps up from the base of your skull or settles behind one eye by mid-afternoon, then digs in for the rest of the day. You take something, it dulls the edge for a few hours, and by tomorrow the whole cycle starts over, which is exhausting when the pills only ever seem to mask the problem instead of ending it. Here is the idea that surprises a lot of people: for many stubborn, recurring headaches, the real source is not the head at all. It is the neck.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>What "the neck as a headache source" actually means</h2>
<p>The upper part of your neck and the base of your skull share a crowded, sensitive neighborhood of joints, muscles, and nerves. When the small joints at the very top of the spine get stiff, or the muscles that run from your shoulders up into the back of your head stay tight and overworked, the pain they produce does not always stay put. It can be felt as head pain — across the forehead, around one eye, or wrapping the back of the skull. That is what clinicians mean by referred pain: the trouble is in the neck, but you feel it up top.</p>
<p>Two common patterns fit this picture. A <strong>cervicogenic headache</strong> is one driven directly by the neck's joints and tissues, often felt on one side and often paired with a stiff, cranky neck. A <strong>tension-type headache</strong> tends to feel like a band of pressure around the head, and it frequently rides along with the same tight muscles and locked-up posture. In real life the two blur together, and the everyday cause is usually the same: sustained position. Hours on a phone, a workday hunched toward a screen, a long drive with your head pushed forward — each one asks the upper neck to hold a load it was never built to hold all day. The joints stiffen, the muscles guard, and the head pain follows.</p>
<h2>Signs your headache might be neck-driven</h2>
<p>No article can diagnose you, and these patterns are not a checklist to self-label with. They are simply clues worth having evaluated by a professional. A headache is more likely to have a neck component when it tends to start at the base of the skull or on one side rather than deep in the center of the head. It often builds through the day rather than hitting all at once, and it tends to get worse after a long stretch at a desk or after a drive.</p>
<p>Another telling pattern is what changes it. Neck-driven headaches frequently ease when you change position or stand up and move, and they flare again when you settle back into the same posture. They often travel with a companion, too — tightness or soreness through the neck and shoulders that you had stopped noticing. If several of these sound familiar, that is a reason to get looked at, not a reason to reach for a diagnosis on your own.</p>
<h2>What physical therapy actually does about it</h2>
<p>The point of therapy here is to treat the driver, not just quiet the symptom. It usually starts with skilled hands-on work: a therapist assesses the specific joints of the upper neck, finds the stiff or irritable ones, and uses gentle manual techniques to restore how they move, while releasing the muscles that have been guarding around them. That alone can take pressure off the structures that refer pain into the head.</p>
<p>More durable relief usually depends on the next step — addressing the reasons the tension keeps rebuilding. That means working on the posture and the strength gaps that let your head drift forward and your neck do all the work: waking up the deep muscles that support the neck, opening the mid-back and shoulders, and adjusting how you sit, drive, and hold your phone. You also leave with simple daily strategies to use between visits, small habits that keep the gains from slipping. You can read more about how we approach this on our <a href="../treatments/headache-relief.html">headache relief page</a>, and because the neck is so often the engine of the problem, the same care overlaps closely with how we treat <a href="../treatments/neck-pain.html">neck pain</a>. Both live under our broader <a href="../services/physical-therapy.html">physical therapy</a> services.</p>
<h2>When a headache needs a doctor first</h2>
<p>Physical therapy is a strong option for headaches that come from the neck — but not every headache belongs in that category, and some need medical care right away. A sudden, severe headache that feels like the worst of your life is an emergency and calls for urgent evaluation, not a therapy appointment. So does a headache that arrives with fever, confusion, vision loss, weakness, numbness, or trouble speaking, or one that follows a significant blow to the head.</p>
<p>If a headache is new, changing in a way that worries you, or simply different from your usual pattern, the responsible first move is to be checked by a physician. Getting the serious causes ruled out is not a detour — it is what makes it safe to then treat the mechanical, neck-driven piece with confidence.</p>
<h2>Let's find out what's really behind yours</h2>
<p>If your headaches keep circling back and the medicine only ever buys you a few hours, it is worth learning whether your neck is part of the story. A thorough evaluation can tell us what is driving your pain and whether hands-on care, posture work, and a simple home plan are likely to help. Our family has cared for this community since 1991, and our people make the difference. Call First Rehabilitation of North Palm Beach at <strong>561-624-4263</strong> to book an evaluation, or <a href="../contact.html">request an appointment online</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different — please consult a qualified professional about yours.</em></p>
""",
    },
    "cartilage-transplant-knee-explained": {
        "title": "Cartilage Transplants: Rebuilding a Knee Instead of Replacing It",
        "date": "July 2026",
        "iso": "2026-07-28",
        "tag": "Knees &amp; Joints",
        "teaser": "A sports medicine surgeon joined our Pain 2 Power podcast to explain cartilage transplants — who they help, what recovery looks like, and why rehab decides the outcome.",
        "body": """
<p>Most people hear two options for a worn-out knee: live with it, or replace the whole joint. On a recent episode of our <a href="../podcast.html">Pain 2 Power radio show</a>, Dr. Dave Kashuba and Mike McGann sat down with Dr. Rami Elkhechen, M.D., a fellowship-trained sports medicine orthopedic surgeon now with NYU Langone Health, to talk about a third path — one where the goal isn't to replace your knee with metal and plastic, but to rebuild the cartilage you were born with.</p>
<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>
<h2>Why cartilage is the part worth protecting</h2>
<p>Dr. Elkhechen uses an analogy that sticks. Cartilage, he says, is "the gold in a vault at a bank." The ligaments, tendons, and meniscus around it are the security system — the guards and the alarm. They matter enormously, but they exist to protect the gold. "Once the cartilage is gone," he explained, "the supporting structures become secondary."</p>
<p>Here's the catch, and Dave raised it directly on the show: cartilage has no nerve endings. You can wear it down for years without feeling a thing, which is why so many people don't arrive until the problem is already advanced. As Dave put it, by the time someone shows up with pain, the trouble has often reached the bone underneath.</p>
<h2>The signs worth getting checked</h2>
<p>Because cartilage itself can't hurt, the early clues are indirect. Dr. Elkhechen pointed to two in particular. The first is <strong>swelling inside the joint</strong> — a build-up of fluid that seems to come from nowhere. The second is simpler: <strong>you can't do your normal activity anymore</strong>. If you're active and something you enjoy has become off-limits, that's reason enough to have it looked at.</p>
<p>After a specific tweak or twist, his advice was measured, not alarmist: give it a few days of rest, ice, and anti-inflammatories. If the pain settles, you likely don't need an office visit. If it lingers, that's when to come in. And his broader point was about timing — get evaluated early, because even if there's nothing to do yet, it can be monitored so the window for treatment doesn't quietly close.</p>
<h2>What a cartilage transplant actually involves</h2>
<p>Before any of this, Dr. Elkhechen was emphatic about the order of operations: it starts with X-rays and a hands-on physical exam, often an MRI, and then <em>non-operative</em> treatment. "We tend to try non-operative treatment as often and as much as we can before we indicate any patients for any type of surgical management," he said, adding that conservative care is frequently successful on its own.</p>
<p>When a transplant is the right call, it happens in two stages. In the first — an outpatient procedure that can take around thirty minutes — the surgeon looks inside the knee with a small camera and, if the damage fits the criteria, harvests a piece of cartilage "almost a small Tic Tac sized" from a part of the joint that doesn't need it. That sample goes to a lab where your own cells are grown on a scaffold, a process that takes roughly six weeks. A second, more involved procedure then implants the new cartilage into the damaged area.</p>
<p>Who's a candidate? Generally people up to about age 55 — sometimes 60 in good health, subject to insurance approval — and, importantly, those with <strong>small, focal areas of damage</strong>. A contained lesion is far more treatable than widespread, end-stage arthritis. Mike drew out the distinction that matters most: a knee replacement is a genuinely successful operation, but the joint always feels somewhat different afterward. A transplant aims to restore your own anatomy.</p>
<h2>Rehab is not the afterthought — it's the outcome</h2>
<p>This is where the conversation came home for us. "Cartilage loves range of motion," Dr. Elkhechen said, and gentle motion begins almost immediately after surgery. Weight-bearing and high-impact activity are a different story: those are held back deliberately so the new cells can take hold. Recovery timelines depend on where and how large the lesion is — damage under the kneecap may allow weight-bearing almost right away with the knee held straight, while other areas typically take <strong>eight to twelve weeks</strong> to reach full weight-bearing.</p>
<p>Meanwhile, therapy isn't idle. That waiting period is spent on range of motion and on strengthening the muscles around the knee — the ones, in his words, "supporting that gold." That's exactly the work our <a href="../services/physical-therapy.html">physical therapy</a> team does after surgery, and you can read more about our approach on the <a href="../treatments/knee-pain.html">knee pain page</a>.</p>
<h2>Prehab: getting strong before the operation</h2>
<p>Dave asked about prehab — rehabilitation <em>before</em> surgery — and Dr. Elkhechen does it routinely, especially with ACL patients, strengthening the quadriceps and hip abductors ahead of time. His reasoning applies well beyond one procedure: "The stronger your base is as you're coming in, in terms of strength and your activity level, you're probably going to come out the other side much better in terms of recovery."</p>
<p>He also made a point we'd underline twice. Patients who understand their diagnosis and their therapy plan do better: "If they're not on board with treatment, that treatment is less likely to succeed." Knowing the what and the why isn't a nicety — it changes results.</p>
<h2>What you can do to protect your knees now</h2>
<p>Asked what prevents this kind of damage in the first place, Dave pointed to the knee's stabilizers — particularly the vastus medialis (the VMO) on the inner knee, which helps track the kneecap. His guidance was to strengthen the whole quadriceps and work the muscles both above and below the joint, including the glutes and calves.</p>
<p>One exercise he shared on air: lie on your back with your knees comfortably bent and both feet flat on the floor or bed. Lift your hips upward, pause at the top, and squeeze the glute muscles — three sets of ten. Move gently, stay within a comfortable range, and stop if anything sharpens the pain.</p>
<h2>Start with an evaluation</h2>
<p>Whether your knee needs surgery, prehab, or simply a smarter strengthening plan, the honest answer starts with someone looking at it. Our therapists evaluate your knee, tell you plainly whether therapy is likely to help, and coordinate with your physician or an orthopedic specialist when you need one. Call First Rehabilitation of North Palm Beach at <strong>561-624-4263</strong>, <a href="../contact.html">request an appointment online</a>, or hear the full conversation on the <a href="../podcast.html">Pain 2 Power podcast</a>.</p>
<p><em>This article is general information, not medical advice. Every situation is different — please consult a qualified professional about yours.</em></p>
""",
    },
}

def build_blog():
    cards = "".join(
        f'''<a class="cond-card reveal" href="{slug}.html" style="padding:1.9rem 1.7rem;">
        <span class="cond-tag">{p["tag"]} &middot; {p["date"]}</span>
        <h3 style="margin-top:0.4rem;">{p["title"]}</h3>
        <p>{p["teaser"]}</p>
        <p style="margin-top:0.9rem;font-weight:600;color:var(--ink);">Read article &rarr;</p>
        </a>'''
        for slug, p in BLOG_POSTS.items()
    )
    crumbs = '<div class="crumbs"><a href="../index.html">Home</a> / Blog</div>'
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
        crumbs = f'<div class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">Blog</a> / {p["title"]}</div>'
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
{cta_band(1)}
</main>
"""
        import json as _json
        from datetime import datetime as _dt
        seo_titles = {
            "what-to-expect-first-pt-visit": "Your First PT Visit: What to Expect",
            "five-morning-habits-back-pain": "Five Morning Habits That Ease Back Pain",
            "why-hand-therapy-is-different": "Why Hand Therapy Is Its Own Specialty",
            "knee-arthritis-before-surgery": "Knee Pain: What to Try Before Surgery",
            "headaches-that-start-in-the-neck": "Headache Treatment in North Palm Beach: The Neck Link",
            "cartilage-transplant-knee-explained": "Cartilage Transplants: An Alternative to Knee Replacement",
        }
        iso_date = p.get("iso") or _dt.strptime(p["date"], "%B %Y").strftime("%Y-%m")
        post_schema = '<script type="application/ld+json">' + _json.dumps({
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": _faq_plain(p["title"]),
            "description": _faq_plain(p["teaser"]),
            "datePublished": iso_date, "dateModified": iso_date,
            "image": "https://www.firstrehabnpb.com/assets/media/hero-poster.jpg",
            "author": {"@type": "Organization", "name": "First Rehabilitation of North Palm Beach"},
            "reviewedBy": {"@type": "Person", "@id": "https://www.firstrehabnpb.com/about.html#david-kashuba",
                           "name": "David Kashuba, Ph.D.", "jobTitle": "CEO & Occupational Therapist"},
            "publisher": {"@type": "Organization", "name": "First Rehabilitation of North Palm Beach",
                          "logo": {"@type": "ImageObject", "url": "https://www.firstrehabnpb.com/assets/media/logo.png"}},
            "mainEntityOfPage": f"https://www.firstrehabnpb.com/blog/{slug}.html",
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
                out += f'<h4>{label}</h4><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
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
  '<div class="crumbs"><a href="index.html">Home</a> / Careers</div>')}
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
  '<div class="crumbs"><a href="index.html">Home</a> / Your First Visit</div>')}
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
        "id": "hv1bNdFurrc",
        "ep": "Episode 8",
        "title": "Shoulder Pain, Rotator Cuffs &amp; Replacements",
        "guest": "Dr. Ryan Simovitch",
        "teaser": "The shoulder is the most mobile joint in the body — and that mobility is exactly why it breaks down. Dave and Mike sit down with Dr. Ryan Simovitch to talk rotator cuffs, shoulder replacements, and what actually helps.",
    },
]

def _video_card(v, featured=False):
    thumb = f'https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg'
    watch = f'https://www.youtube.com/watch?v={v["id"]}'
    embed = f'https://www.youtube-nocookie.com/embed/{v["id"]}?autoplay=1&amp;rel=0'
    guest = f'<span class="vid-guest">{v["guest"]}</span>' if v.get("guest") else ""
    cls = "vid-card is-featured" if featured else "vid-card"
    return f'''<article class="{cls} reveal">
      <button class="vid-facade" type="button" data-embed="{embed}"
        data-title="{v["title"]} — Pain 2 Power on YouTube">
        <img src="{thumb}" alt="" loading="lazy" width="480" height="360">
        <span class="vid-play" aria-hidden="true"><svg viewBox="0 0 68 48"><path class="vp-bg" d="M66.5 7.7c-.8-2.9-3.1-5.2-6-6C55.2 0 34 0 34 0S12.8 0 7.5 1.7c-2.9.8-5.2 3.1-6 6C0 13 0 24 0 24s0 11 1.5 16.3c.8 2.9 3.1 5.2 6 6C12.8 48 34 48 34 48s21.2 0 26.5-1.7c2.9-.8 5.2-3.1 6-6C68 35 68 24 68 24s0-11-1.5-16.3z"/><path class="vp-tri" d="M45 24 27 14v20z"/></svg></span>
        <span class="sr-only">Play: {v["title"]}</span>
      </button>
      <div class="vid-body">
        <span class="vid-ep">{v["ep"]}</span>
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
        graph.append({
            "@type": "VideoObject",
            "name": _faq_plain(f'{v["ep"]}: {v["title"]}'),
            "description": _faq_plain(v["teaser"]),
            "thumbnailUrl": f'https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg',
            "embedUrl": f'https://www.youtube.com/embed/{v["id"]}',
            "contentUrl": f'https://www.youtube.com/watch?v={v["id"]}',
            "publisher": {"@id": "https://www.firstrehabnpb.com/#organization"},
        })
    if not graph:
        return ""
    data = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">' + _json.dumps(data, ensure_ascii=False) + '</script>\n'

def build_videos():
    crumbs = '<div class="crumbs"><a href="index.html">Home</a> / Videos</div>'
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
  "Every Pain 2 Power episode, on camera — real talk with the surgeons, therapists, and specialists who keep the Palm Beaches moving.", crumbs)}
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
               extra_schema=_video_schema() + breadcrumb_schema([("Home", ""), ("Videos", "videos.html")]))
          + nav(0) + body + footer(0))

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
    pages = ["", "about.html", "contact.html", "careers.html", "faq.html", "first-visit.html", "podcast.html", "videos.html", "blog/index.html", "treatments/index.html"]
    pages += [f"services/{s}.html" for s in SERVICES]
    pages += [f"locations/{s}.html" for s in LOCATIONS]
    pages += [f"treatments/{s}.html" for s in CONDITIONS]
    pages += [f"blog/{s}.html" for s in BLOG_POSTS]
    from datetime import date as _date
    lastmod = _date.today().isoformat()
    urls = "".join(f"  <url><loc>{base}/{p}</loc><lastmod>{lastmod}</lastmod></url>\n" for p in pages)
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
David Kashuba, Ph.D. (CEO, Occupational Therapist); Kayla Dorsey, DPT and Logan Van Sant
(Physical Therapists); Joni Janik (Occupational Therapist); Laura Drumm (Certified Hand
Therapist); Nick Kashuba (COO). About: {base}/about.html

## Insurance accepted
Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare,
VA Community Care Network (VACCN), workers' compensation, self-pay.

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

## Podcast
Pain 2 Power, hosted by Dr. Dave Kashuba with Mike McGann. Saturdays 8:30 AM on
100.3 Legends Radio; all episodes: {base}/podcast.html
''')

    body = f"""
<main>
{page_hero("404", "This Page Took a <em class='accent'>Wrong Turn</em>",
  "The page you're looking for isn't here — but your recovery path is just a click away.")}
<section class="section center">
  <div class="wrap">
    <a class="btn btn-coral" href="index.html">Back to Home <span class="arr">&rarr;</span></a>
  </div>
</section>
</main>
"""
    write("404.html",
          head("Page Not Found | First Rehabilitation of North Palm Beach",
               "That page took a wrong turn. Find physical therapy, occupational therapy, hand therapy, and wellness services at First Rehabilitation of North Palm Beach.",
               extra_schema='<meta name="robots" content="noindex">\n') + nav(0, solid=True) + body + footer(0))

if __name__ == "__main__":
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
    build_videos()
    build_meta()
    print("\nDone. Open index.html or deploy the folder to Vercel.")
