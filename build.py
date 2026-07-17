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
INSTAGRAM = "https://www.instagram.com/firstrehabnpb/"
FACEBOOK = "https://www.facebook.com/FirstRehabNPB/"
LINKEDIN = "https://www.linkedin.com/company/firstrehabnpb"
MAPS_EMBED = "https://www.google.com/maps?q=733+US+Highway+1+Suite+2A+North+Palm+Beach+FL+33408&output=embed"

# ----------------------------------------------------------------------------

def head(title, desc, depth=0, canonical="", og_image="assets/media/podcast-cover.jpg", page_type="website"):
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
<link rel="icon" href="{p}assets/icons/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{p}assets/icons/icon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{p}assets/icons/icon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="{p}assets/icons/apple-touch-icon.png">
<link rel="manifest" href="{p}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/css/styles.css">
<link rel="stylesheet" href="{p}assets/css/intake.css">
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "MedicalBusiness",
  "name": "First Rehabilitation of North Palm Beach",
  "description": "Family-owned outpatient physical therapy, occupational therapy, certified hand therapy, and wellness clinic serving Palm Beach County since 1991.",
  "url": "https://www.firstrehabnpb.com",
  "logo": "https://www.firstrehabnpb.com/assets/media/logo.png",
  "image": "https://www.firstrehabnpb.com/assets/media/clinic.jpg",
  "telephone": "+1-561-624-4263",
  "faxNumber": "+1-561-840-4234",
  "email": "firstrehabnpb@gmail.com",
  "foundingDate": "1991",
  "priceRange": "$$",
  "slogan": "Our People Make the Difference",
  "medicalSpecialty": ["PhysicalTherapy", "OccupationalTherapy"],
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "733 US Highway 1, Suite 2A",
    "addressLocality": "North Palm Beach",
    "addressRegion": "FL",
    "postalCode": "33408",
    "addressCountry": "US"
  }},
  "geo": {{ "@type": "GeoCoordinates", "latitude": 26.8234, "longitude": -80.0559 }},
  "areaServed": ["North Palm Beach", "Palm Beach Gardens", "Jupiter", "Juno Beach", "West Palm Beach", "Palm Beach County"],
  "openingHoursSpecification": {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
    "opens": "08:00", "closes": "17:30"
  }},
  "aggregateRating": {{ "@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "ratingCount": "24" }},
  "sameAs": ["https://www.instagram.com/firstrehabnpb/","https://www.facebook.com/FirstRehabNPB/","https://www.linkedin.com/company/firstrehabnpb","https://open.spotify.com/show/033A1BQq9qqsygFFCq9SIu"]
}}</script>
</head>
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
  <div class="topbar">
    <div class="wrap topbar-row">
      <span class="tb-item">733 US Highway 1, Suite 2A &middot; North Palm Beach</span>
      <span class="tb-item">Mon–Fri &middot; 8:00 AM – 5:30 PM</span>
      <a class="tb-item tb-phone" href="tel:+15616244263">{PHONE}</a>
    </div>
  </div>
  <div class="wrap nav-bar">
    <a class="brand" href="{p}index.html">
      <img class="logo-dark-v" src="{p}assets/media/logo-dark.png" alt="First Rehabilitation logo">
      <img class="logo-light-v" src="{p}assets/media/logo.png" alt="First Rehabilitation logo">
      <span class="brand-sub">North Palm Beach &middot; Est. 1991</span>
    </a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
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
        <a class="nav-item" href="{p}treatments/index.html">What We Treat</a>
        <div class="dropdown"><div class="dd-cols">{cond_links}</div></div>
      </li>
      <li><a class="nav-item" href="{p}about.html">About</a></li>
      <li><a class="nav-item" href="{p}blog/index.html">Blog</a></li>
      <li><a class="nav-item" href="{p}podcast.html">Podcast</a></li>
      <li><a class="nav-item" href="{p}faq.html">FAQ</a></li>
      <li><a class="nav-item" href="{p}contact.html">Contact</a></li>
      <li><a class="nav-item" href="{PORTAL}" target="_blank" rel="noopener">Patient Portal</a></li>
      <li class="nav-cta"><a class="btn btn-coral" href="{p}contact.html">Book Appointment</a></li>
    </ul>
  </div>
</header>
"""

SOCIAL_ICONS = {
    "Instagram": (INSTAGRAM, '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>'),
    "Facebook": (FACEBOOK, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.7h2.6l.4-3h-3V8.4c0-.87.24-1.46 1.49-1.46h1.59V4.25c-.27-.04-1.22-.12-2.32-.12-2.3 0-3.86 1.4-3.86 3.98v2.22H7.8v3h2.6V21h3.1z"/></svg>'),
    "LinkedIn": (LINKEDIN, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 8.5H3.86V20h3.08V8.5zM5.4 3.5a1.78 1.78 0 1 0 0 3.56 1.78 1.78 0 0 0 0-3.56zM20.14 13.28c0-3.3-1.76-4.98-4.1-4.98-1.88 0-2.72 1.03-3.19 1.76V8.5H9.77V20h3.08v-6.07c0-1.6.72-2.55 2.06-2.55 1.29 0 2.15.86 2.15 2.55V20h3.08v-6.72z"/></svg>'),
    "Spotify": (SPOTIFY, '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm4.44 14.5a.7.7 0 0 1-.96.24c-2.63-1.6-5.94-1.97-9.84-1.08a.7.7 0 1 1-.31-1.37c4.27-.97 7.94-.54 10.87 1.25.33.2.44.63.24.96zm1.3-2.96a.87.87 0 0 1-1.2.3c-3.01-1.85-7.6-2.38-11.16-1.3a.87.87 0 1 1-.5-1.67c4.07-1.23 9.12-.63 12.57 1.48.4.25.53.78.29 1.19zm.12-3.09C14.27 8.3 8.3 8.1 4.86 9.15a1.05 1.05 0 1 1-.6-2c3.94-1.2 10.5-.97 14.63 1.48a1.05 1.05 0 0 1-1.07 1.82z"/></svg>'),
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
  <div class="beam-field"><div class="beam" style="opacity:0.35;"></div></div>
  <div class="wrap">
    <div class="footer-grid">
      <div class="f-brand">
        <img src="{p}assets/media/logo-dark.png" alt="First Rehabilitation logo">
        <div class="brand-name">First Rehabilitation</div>
        <div class="brand-tag">Heal. Strengthen. Thrive.</div>
        <p>Family-owned outpatient rehabilitation serving the Palm Beaches since 1991. Physical therapy, occupational therapy, certified hand therapy, and wellness — all under one roof.</p>
        {social_row()}
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{p}services/physical-therapy.html">Physical Therapy</a></li>
          <li><a href="{p}services/occupational-therapy.html">Occupational Therapy</a></li>
          <li><a href="{p}services/hand-therapy.html">Hand Therapy</a></li>
          <li><a href="{p}services/wellness.html">Wellness &amp; Gym</a></li>
        </ul>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="{p}treatments/index.html">What We Treat</a></li>
          <li><a href="{p}about.html">About Us</a></li>
          <li><a href="{p}blog/index.html">Blog</a></li>
          <li><a href="{p}podcast.html">Pain 2 Power Podcast</a></li>
          <li><a href="{p}faq.html">FAQ</a></li>
          <li><a href="{PORTAL}" target="_blank" rel="noopener">Patient Portal</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit Us</h4>
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
<script src="{p}assets/js/main.js"></script>
<script src="{p}assets/js/intake.js" defer></script>
</body>
</html>
"""

def cta_band(depth=0, heading='Life is too short to <em>live in pain.</em>', sub="Start your recovery today with a team dedicated to your long-term wellness and total healing."):
    p = "../" * depth
    return f"""
<section class="cta-band">
  <div class="hero-fallback"></div>
  <div class="beam-field"><div class="beam"></div><div class="beam b2"></div></div>
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
  <div class="beam-field"><div class="beam" style="opacity:0.5;"></div></div>
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
        ("shoulder", 205, 116, "Shoulder"),
        ("back", 150, 205, "Back &amp; Spine"),
        ("handwrist", 227, 328, "Hand &amp; Wrist"),
        ("hip", 190, 316, "Hip"),
        ("knee", 172, 442, "Knee"),
        ("ankle", 161, 570, "Ankle"),
        ("foot", 172, 598, "Foot"),
    ]
    spot_links = {
        "headache": "treatments/headache-relief.html", "neck": "treatments/neck-pain.html",
        "shoulder": "treatments/shoulder-pain.html", "back": "treatments/back-pain.html",
        "handwrist": "treatments/hand-wrist.html", "hip": "treatments/hip-pain.html",
        "knee": "treatments/knee-pain.html", "ankle": "treatments/ankle-pain.html",
        "foot": "treatments/foot-pain.html",
    }
    spots_svg = "".join(
        f'''<a href="{spot_links[k]}" class="bm-spot" data-bm="{k}" aria-label="{lbl}">
        <circle class="halo" cx="{x}" cy="{y}" r="10"/>
        <circle class="core" cx="{x}" cy="{y}" r="6"/>
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
    return f'<svg viewBox="40 0 220 640" role="img" aria-label="Interactive body map — choose where it hurts">{silhouette}{spots_svg}</svg>'

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

    quotes = [
        ("The personalized care and expert hands of the team at First Rehab made all the difference in my recovery. They truly treat you like family.", "Sarah M.", "North Palm Beach"),
        ("After my surgery, I was nervous about the rehab process. David and his crew were patient, encouraging, and highly skilled. I'm back to my daily routine faster than expected.", "James R.", "Jupiter"),
        ("The Hand Therapy program is top-notch. They created custom splints for me and guided my recovery with so much precision. Highly recommend First Rehab!", "Linda K.", "Palm Beach Gardens"),
    ]
    quotes_html = "".join(
        f'''<figure class="quote-card reveal d{i+1}"><div class="stars">★★★★★</div><blockquote>{q}</blockquote><figcaption><strong>{n}</strong> &nbsp;{c}</figcaption></figure>'''
        for i, (q, n, c) in enumerate(quotes)
    )

    social_cards = "".join(
        f'''<a class="sm-card" href="{INSTAGRAM}" target="_blank" rel="noopener">
          <img src="assets/social/post-{i}.jpg" alt="Life at First Rehabilitation of North Palm Beach" loading="lazy" onerror="this.closest('.sm-card').classList.add('empty')">
        </a>''' for i in range(1, 9)
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
        ["Medicare", "Medicare Advantage", "Blue Cross Blue Shield", "Aetna", "Humana", "Tricare", "Workers' Comp", "Self Pay"])

    journey_svg = '''<svg class="journey-path" viewBox="0 0 1200 260" preserveAspectRatio="none" aria-hidden="true">
      <path d="M40,80 C240,80 220,170 400,170 C580,170 560,80 740,80 C920,80 900,170 1160,170"/>
    </svg>'''

    body = f"""
<main>
<section class="hero">
  <div class="hero-media">
    <div class="hero-fallback"></div>
    <video autoplay muted loop playsinline poster="assets/media/hero-poster.jpg" onerror="this.remove()">
      <source src="assets/media/lighthouse.mp4" type="video/mp4">
    </video>
  </div>
  <div class="hero-scrim"></div>
  <div class="beam-field"><div class="beam"></div><div class="beam b2"></div></div>
  <div class="wrap hero-inner">
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
    <div class="hero-badges">
      <span class="hb">★ 5.0 Google Rated</span>
      <span class="hb">Medicare Accepted</span>
      <span class="hb">Family-Owned Since 1991</span>
      <span class="hb">Certified Hand Therapy</span>
    </div>
    <div class="hero-meta">
      <div><strong data-count="35" data-suffix="+">0</strong><span>Years of Expertise</span></div>
      <div><strong data-count="80000" data-suffix="+">0</strong><span>Patients Treated</span></div>
      <div><strong>4-in-1</strong><span>Programs, One Roof</span></div>
      <div><strong>Est. 1991</strong><span>Family-Owned</span></div>
    </div>
  </div>
  <div class="scroll-hint"><span></span></div>
</section>

<div class="ins-strip"><div class="ticker">{ticker}</div></div>

<section class="section" id="pathways">
  <span class="sec-mark" style="top:2rem; right:2vw;">04</span>
  <div class="wrap">
    <div class="section-head reveal">
      <span class="eyebrow">What We Offer</span>
      <h2>One Clinic.<br><em class="accent">Four Pathways.</em></h2>
      <p class="lede">From your first appointment to lifelong wellness — we're with you every step.</p>
    </div>
    <div class="pathways">{pathways_html}</div>
  </div>
</section>

<section class="section on-ink" id="bodymap">
  <div class="beam-field"><div class="beam" style="opacity:0.55;"></div></div>
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
  <span class="sec-mark" style="bottom:2rem; left:2vw;">VI</span>
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
        <div><strong data-count="35" data-suffix="+">0</strong><span>Years of Expertise</span></div>
        <div><strong data-count="80000" data-suffix="+">0</strong><span>Patients Treated</span></div>
        <div><strong>5.0★</strong><span>Google Rating</span></div>
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
      <h2>5.0 <span style="color:var(--coral);">★</span> on Google</h2>
    </div>
    <div class="quote-grid">{quotes_html}</div>
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
          head("First Rehabilitation of North Palm Beach | PT, OT, Hand Therapy & Wellness Since 1991",
               "Family-owned outpatient physical therapy, occupational therapy, certified hand therapy, and wellness in North Palm Beach, FL. Serving Palm Beach County since 1991.",
               canonical="", og_image="assets/media/clinic.jpg")
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
            ("Lymphedema Care", "Specialized management to reduce swelling and restore comfortable movement."),
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

def build_services():
    for slug, s in SERVICES.items():
        items = "".join(
            f'<div class="cond-card reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in s["items"]
        )
        gym_banner = ""
        if slug == "wellness":
            gym_banner = '''<div class="split-media reveal" style="aspect-ratio:16/8;margin-bottom:2.5rem;">
              <img src="../assets/media/gym.jpg" alt="The wellness gym floor at First Rehabilitation" loading="lazy">
            </div>'''
        crumbs = f'<div class="crumbs"><a href="../index.html">Home</a> / <a href="physical-therapy.html">Services</a> / {s["title"]}</div>'
        body = f"""
<main>
{page_hero("Our Services", s["title"], s["lede"], crumbs)}
<section class="section">
  <div class="wrap">
  {gym_banner}
  <div class="two-col">
    <div class="prose reveal">
      <h2><em class="accent">{s["kicker"]}</em></h2>
      <p>{s["intro"]}</p>
      <h2>What this program includes</h2>
      <div class="cond-grid" style="grid-template-columns:1fr;gap:0.9rem;">{items}</div>
    </div>
    <aside class="side-card reveal d2">
      <h3>Begin with an evaluation</h3>
      <p>Your first visit includes a movement-based evaluation, a discussion of your goals, and a clear plan for getting you back to full life.</p>
      <a class="btn btn-coral" href="../contact.html">Book Appointment</a>
      <div class="side-meta">
        <p>Prefer to call?<br><a href="tel:+15616244263">{PHONE}</a></p>
        <p style="margin-top:0.8rem;">Most major insurance accepted, including Medicare.</p>
      </div>
    </aside>
  </div>
  </div>
</section>
{cta_band(1)}
</main>
"""
        write(f"services/{slug}.html",
              head(f'{s["title"].replace("&amp;","&")} | First Rehabilitation of North Palm Beach',
                   s["lede"].replace("&amp;", "&"), depth=1, canonical=f"services/{slug}.html")
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
        "treats": ["Carpal tunnel syndrome", "Wrist fractures and sprains", "Tendon injuries and repairs", "Trigger finger", "Arthritis of the hand and thumb", "Post-surgical hand rehabilitation", "Lymphedema of the upper extremity"],
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
    <div class="cond-grid" style="grid-template-columns:repeat(auto-fill,minmax(300px,1fr));">{cards}</div>
  </div>
</section>
{cta_band(1)}
</main>
"""
    write("treatments/index.html",
          head("What We Treat | First Rehabilitation of North Palm Beach",
               "Explore the conditions we treat: back, neck, shoulder, knee, hip, foot, ankle, hand & wrist, headaches, post-surgical rehab, workers' comp, and auto accident recovery.", depth=1, canonical="treatments/index.html")
          + nav(1) + body + footer(1))

    for slug, c in CONDITIONS.items():
        treats = "".join(f"<li>{t}</li>" for t in c["treats"])
        crumbs = f'<div class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">What We Treat</a> / {c["name"]}</div>'
        body = f"""
<main>
{page_hero(c["area"], c["name"], c["lede"], crumbs)}
<section class="section">
  <div class="wrap two-col">
    <div class="prose reveal">
      <p>{c["intro"]}</p>
      <h2>Conditions we treat</h2>
      <ul class="check-list">{treats}</ul>
      <h2>Our approach</h2>
      <p>{c["approach"]}</p>
      <h2>What to expect at your first visit</h2>
      <p>Your first appointment includes a comprehensive movement-based evaluation, an honest conversation about your goals, and a proposed plan of care — including hands-on treatment that very first day whenever appropriate. We accept most major insurance plans, including Medicare, and our front desk will gladly verify your coverage before you arrive.</p>
    </div>
    <aside class="side-card reveal d2">
      <h3>Start feeling better</h3>
      <p>Serving the Palm Beaches since 1991 — family-owned, with a 5.0★ Google rating.</p>
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
        write(f"treatments/{slug}.html",
              head(f"{name_plain} in North Palm Beach | First Rehabilitation",
                   c["lede"].replace("&amp;", "&"), depth=1, canonical=f"treatments/{slug}.html", page_type="article")
              + nav(1) + body + footer(1))

# ----------------------------------------------------------------------------
# ABOUT / PODCAST / FAQ / CONTACT
# ----------------------------------------------------------------------------

TEAM = [
    ("David Kashuba, Ph.D.", "CEO &amp; Occupational Therapist", "Founded First Rehabilitation in 1991 and still treats patients hands-on every day — leading the clinic's comprehensive, high-end approach to rehabilitation across three decades and tens of thousands of recoveries.", "david.jpg"),
    ("Nick Kashuba", "Chief Operating Officer", "Second-generation leadership keeping the clinic's family-owned values — and its promise that our people make the difference — at the center of everything we do.", "nick.jpg"),
    ("Logan Van Sant", "Physical Therapist", "A wealth of knowledge in the physical therapy world, dedicated to helping patients move and feel their best.", "logan.jpg"),
    ("Kayla Dorsey, DPT", "Physical Therapist", "A Doctor of Physical Therapy with over a decade of extensive clinical experience in personalized, hands-on care.", "kayla.jpg"),
    ("Joni Janik", "Occupational Therapist", "Helps patients reclaim the daily activities that matter most — restoring independence, confidence, and quality of life.", "joni.jpg"),
    ("Laura Drumm", "Certified Hand Therapist", "Leads our certified hand therapy program with surgical-grade precision — from custom splinting to post-operative tendon protocols and lymphedema care.", "laura.jpg"),
]

def build_about():
    team_html = "".join(
        f'''<div class="team-card reveal d{i%3+1}">
        <div class="team-photo">
          <img src="assets/team/{img}" alt="{name}, {role} at First Rehabilitation of North Palm Beach" loading="lazy" onerror="this.closest('.team-photo').classList.add('empty')">
        </div>
        <h3>{name}</h3><div class="role">{role}</div><p>{bio}</p></div>'''
        for i, (name, role, bio, img) in enumerate(TEAM)
    )
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
        <div><strong data-count="35" data-suffix="+">0</strong><span>Years of Expertise</span></div>
        <div><strong data-count="80000" data-suffix="+">0</strong><span>Patients Treated</span></div>
        <div><strong>5.0★</strong><span>Google Rating</span></div>
        <div><strong>Est. 1991</strong><span>Family-Owned</span></div>
      </div>
    </div>
    <div class="split-media tilt2 reveal d2">
      <img src="assets/media/founder.jpg" alt="First Rehabilitation of North Palm Beach" loading="lazy" onerror="this.closest('.split-media').classList.add('empty')">
    </div>
  </div>
</section>
<section class="section on-cream">
  <span class="sec-mark" style="top:2rem; right:2vw;">est.<br>'91</span>
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
          head("About Us | First Rehabilitation of North Palm Beach",
               "Family-owned since 1991. Meet the team behind First Rehabilitation of North Palm Beach — founder David Kashuba, Ph.D., and our therapists.",
               canonical="about.html")
          + nav(0) + body + footer(0))

EPISODES = [
    ("Episode 6 &middot; Coming Saturday", "Dr. Richard Weiner, M.D.", "World-renowned orthopedic surgeon Dr. Richard Weiner joins the show — a board-certified surgeon with more than 35 years in practice and thousands of joint replacements to his name.", SPOTIFY, "Notify Me"),
    ("Episode 5", "Logan Van Sant, DPT", "Logan is a wealth of knowledge in the physical therapy world.", "https://open.spotify.com/episode/4HIjJt1f7U7Uv0IJCQnyxr", "Listen"),
    ("Episode 4", "Kayla Dorsey, DPT &amp; Dr. Murray Goldberg, M.D.", "Kayla is a Doctor of Physical Therapy with over 10 years of extensive experience. Dr. Goldberg is a board-certified urologist practicing in Palm Beach County since 1991.", "https://open.spotify.com/episode/3BRC4CtKqjyOGf1BmJrztj", "Listen"),
    ("Episode 3", "Dr. Timur Urakov, M.D.", "Associate Professor of Clinical Medicine at the University of Miami specializing in spine surgery, treating conditions along the entire spine with advanced surgical technology.", "https://open.spotify.com/episode/1d1rzNKiSGdMhHsTHXPBQm", "Listen"),
    ("Episode 2", "Dr. Tom Saylor, M.D.", "Hand and upper extremity surgeon Dr. Tom Saylor on the surgical side of restoring hand function.", "https://open.spotify.com/episode/1a4jO3BCBrYhYL8KF01hOi", "Listen"),
    ("Episode 1", "Intro to Dave's Background", "Dr. Dave Kashuba's story — and an overview of what Pain 2 Power is all about.", "https://open.spotify.com/episode/70Yn3oyi2YcesDkivraogc", "Listen"),
]

def build_podcast():
    import re as _re
    def _episode_block(num, title, desc, url, label):
        # Episodes with a Spotify episode URL get an in-page player;
        # anything else (e.g. "coming Saturday") keeps its action button.
        m = _re.search(r"open\.spotify\.com/episode/([A-Za-z0-9]+)", url)
        if m:
            action = (f'<iframe class="pod-embed" '
                      f'src="https://open.spotify.com/embed/episode/{m.group(1)}?utm_source=generator&amp;theme=0" '
                      f'width="100%" height="152" frameborder="0" '
                      f'allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" '
                      f'loading="lazy" title="{title} — play on-site"></iframe>')
        else:
            action = f'<a class="btn btn-ink" href="{url}" target="_blank" rel="noopener">{label}</a>'
        return f'''<div class="pod-card reveal">
          <img class="pod-art" src="assets/media/podcast-cover.jpg" alt="Pain to Power with Mike and Dave — cover art">
          <div><div class="pod-num">{num}</div><h3>{title}</h3><p>{desc}</p></div>
          {action}
        </div>'''
    eps = "".join(_episode_block(*e) for e in EPISODES)
    body = f"""
<main>
{page_hero("The Pain 2 Power Podcast", "Real Conversations That <em class='accent'>Move You Forward</em>",
  "Dr. Dave Kashuba and Mike McGann cover the world of physical rehab and wellness — with some of the sharpest minds in medicine.",
  '<div class="crumbs"><a href="index.html">Home</a> / Podcast</div>')}
<section class="section">
  <div class="wrap two-col">
    <div class="reveal">
      <div class="section-head" style="margin-bottom:2rem;">
        <span class="eyebrow">Your Hosts</span>
        <h2>Dave &amp; Mike</h2>
      </div>
      <div class="hosts-stack">
        <div class="host-bio reveal">
          <img src="assets/team/david.jpg" alt="Dr. Dave Kashuba">
          <div>
            <h3>Dave Kashuba, Ph.D.</h3>
            <div class="role">Founder &amp; Occupational Therapist</div>
            <p>Founder of First Rehabilitation and a practicing occupational therapist, Dave has personally guided the care of more than 80,000 patients over 39+ years, bringing a lifetime of hands-on experience to every conversation about healing and resilience.</p>
          </div>
        </div>
        <div class="host-bio reveal d2">
          <img src="assets/media/mike.jpg" alt="Mike McGann">
          <div>
            <h3>Mike McGann</h3>
            <div class="role">Co-Host</div>
            <p>Co-host Mike McGann brings more than 17 years on the Palm Beach County airwaves to the show. He's hosted music and talk programs of nearly every style and now calls Legends 100.3 home — and a lifelong love of the Great American Songbook, sparked by his mom and a little Sinatra at age seven, gives him a storyteller's ear that's perfect for drawing out every guest's journey.</p>
          </div>
        </div>
      </div>
      <div class="section-head" style="margin-bottom:2rem;">
        <span class="eyebrow">All Episodes</span>
        <h2>Listen &amp; Subscribe</h2>
      </div>
      {eps}
    </div>
    <aside class="side-card reveal d2">
      <h3>Where to listen</h3>
      <p>New episodes air Saturdays at 8:30 AM on 100.3 Legends Radio and stream anytime on Spotify.</p>
      <iframe style="border-radius:14px;margin-top:1.2rem;" src="https://open.spotify.com/embed/show/033A1BQq9qqsygFFCq9SIu?utm_source=generator&amp;theme=0" width="100%" height="352" frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy" title="Pain 2 Power on Spotify"></iframe>
      <a class="btn btn-coral" href="{SPOTIFY}" target="_blank" rel="noopener">Open in Spotify</a>
      <div class="side-meta">
        <p>📻 Saturdays &middot; 8:30 AM<br>100.3 Legends Radio</p>
      </div>
    </aside>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("podcast.html",
          head("Pain 2 Power Podcast | First Rehabilitation of North Palm Beach",
               "Dr. Dave Kashuba and Mike McGann cover the world of physical rehab and wellness. Saturdays on 100.3 Legends Radio and streaming on Spotify.",
               canonical="podcast.html")
          + nav(0) + body + footer(0))

FAQS = [
    ("What services does First Rehabilitation provide?", "We provide physical therapy, occupational therapy, certified hand therapy, and an exclusive on-site wellness and gym program — a full continuum of care under one roof."),
    ("Do you accept my insurance?", "We accept most major health insurance plans, including Medicare, Medicare Advantage, Blue Cross Blue Shield, Aetna, Humana, Tricare, workers' compensation, and self-pay. Call our front desk and we'll gladly verify your specific coverage."),
    ("Do I need a referral to start therapy?", "It depends on your insurance plan. Many patients can begin under Florida's direct access provisions, while some plans require a physician referral. Call us and we'll walk you through exactly what your plan needs."),
    ("What should I expect at my first visit?", "Your initial visit includes a movement-based evaluation, a discussion of your activity goals, and a proposed plan of care that may include hands-on treatment and home exercises starting day one."),
    ("How do I schedule an appointment?", "Call us at 561-624-4263 or use the contact page to request an appointment — our team will follow up promptly to find a time that works."),
    ("What should I wear to my appointments?", "Comfortable clothing you can move in. For lower-body conditions, shorts or loose pants are ideal; for shoulder or arm conditions, a shirt that allows easy access to the area being treated."),
    ("What is certified hand therapy?", "Certified Hand Therapists (CHTs) complete thousands of hours of specialized training in rehabilitation of the hand, wrist, and upper extremity. Our program, led by Laura Drumm, CHT, includes custom splinting fabricated in-clinic."),
    ("What is the wellness program?", "Our on-site wellness and gym program lets patients continue training after discharge from therapy — with personal training, group classes, and senior functional fitness guided by a team that knows your history."),
    ("Do your therapists work together on my care?", "Yes. When appropriate, our PTs, OTs, and hand therapist coordinate assessments and treatment plans so your recovery reflects a genuine team-based approach."),
    ("Where are you located?", "733 US Highway 1, Suite 2A, North Palm Beach, FL 33408 — serving North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, and the greater Palm Beaches."),
]

def build_faq():
    items = "".join(
        f'<details class="faq-item reveal"><summary>{q}</summary><div class="faq-a">{a}</div></details>'
        for q, a in FAQS
    )
    body = f"""
<main>
{page_hero("Questions, Answered", "Frequently Asked <em class='accent'>Questions</em>",
  "Everything you need to know before your first visit — and if you don't see your question, just call us.",
  '<div class="crumbs"><a href="index.html">Home</a> / FAQ</div>')}
<section class="section">
  <div class="wrap"><div class="faq-list">{items}</div>
  <div class="center mt-3 reveal"><p class="lede" style="margin:0 auto 1.2rem;">Still have a question?</p>
  <a class="btn btn-ink" href="contact.html">Contact Us <span class="arr">&rarr;</span></a></div>
  </div>
</section>
{cta_band(0)}
</main>
"""
    write("faq.html",
          head("FAQ | First Rehabilitation of North Palm Beach",
               "Answers to common questions about physical therapy, occupational therapy, hand therapy, insurance, and what to expect at First Rehabilitation of North Palm Beach.",
               canonical="faq.html")
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
      <h3>Request an Appointment</h3>
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
        <p class="af-error" id="af-error"></p>
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
        <div class="c-row"><span class="c-label">Hours</span><span>Monday – Friday<br>8:00 AM – 5:30 PM</span></div>
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
               canonical="contact.html")
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
<p>Ready to get started? Call us at 561-624-4263 — we'll take it from there.</p>
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
<p>If mornings are consistently painful, or pain radiates into your leg, that's worth a professional look. Our back pain program starts with finding the <em>why</em> — and most patients are surprised how treatable it is.</p>
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
<p>If you're facing hand surgery, dealing with carpal tunnel, or fighting arthritis in your thumbs, ask about our certified hand therapy program — it's one of the things that makes First Rehabilitation different.</p>
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
    <div class="cond-grid" style="grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:1.4rem;">{cards}</div>
  </div>
</section>
{cta_band(1)}
</main>
"""
    write("blog/index.html",
          head("Blog | First Rehabilitation of North Palm Beach",
               "Practical recovery and wellness guidance from the physical, occupational, and hand therapy team at First Rehabilitation of North Palm Beach.", depth=1, canonical="blog/index.html")
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
      <p>Questions about your own recovery? Serving the Palm Beaches since 1991 — family-owned, 5.0★ on Google.</p>
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
        write(f"blog/{slug}.html",
              head(f'{p["title"]} | First Rehabilitation Blog', p["teaser"].replace("&amp;","&"), depth=1, canonical=f"blog/{slug}.html", page_type="article")
              + nav(1) + body + footer(1))

# ----------------------------------------------------------------------------
# SITEMAP / ROBOTS / 404
# ----------------------------------------------------------------------------

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
    pages = ["", "about.html", "contact.html", "faq.html", "podcast.html", "blog/index.html", "treatments/index.html"]
    pages += [f"services/{s}.html" for s in SERVICES]
    pages += [f"treatments/{s}.html" for s in CONDITIONS]
    pages += [f"blog/{s}.html" for s in BLOG_POSTS]
    urls = "".join(f"  <url><loc>{base}/{p}</loc></url>\n" for p in pages)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")

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
               "Page not found.") + nav(0, solid=True) + body + footer(0))

# ----------------------------------------------------------------------------
# AI ASSISTANT KNOWLEDGE BASE (api/kb.json — consumed by api/chat.js)
# ----------------------------------------------------------------------------

def build_kb():
    import json, re
    plain = lambda s: re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&middot;", "·")
    kb = {
        "clinic": {
            "name": "First Rehabilitation of North Palm Beach",
            "founded": 1991,
            "founder": "David (Dave) Kashuba, Ph.D., occupational therapist",
            "tagline": "Our people make the difference.",
            "address": "733 US Highway 1, Suite 2A, North Palm Beach, FL 33408",
            "phone": PHONE, "fax": FAX, "email": EMAIL,
            "hours": "Monday–Friday, 8:00 AM – 5:30 PM. Closed weekends.",
            "patient_portal": PORTAL,
            "service_area": "North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, and the greater Palm Beaches",
            "google_rating": "5.0 stars",
        },
        "insurance_accepted": ["Medicare", "Medicare Advantage", "Blue Cross Blue Shield", "Aetna",
                               "Humana", "Tricare", "Workers' Compensation", "Self-pay"],
        "services": {plain(s["title"]): {"summary": plain(s["lede"]),
                     "includes": [plain(t) for t, _ in s["items"]]} for s in SERVICES.values()},
        "conditions_treated": {plain(c["name"]): [plain(t) for t in c["treats"]] for c in CONDITIONS.values()},
        "team": [{"name": n, "role": plain(r), "bio": plain(b)} for n, r, b, _ in TEAM],
        "podcast": {
            "name": "Pain 2 Power", "hosts": "Dr. Dave Kashuba and Mike McGann",
            "airs": "Saturdays 8:30 AM on 100.3 Legends Radio, streaming on Spotify",
            "episodes": [plain(f"{n}: {t}") for n, t, _, _, _ in EPISODES],
        },
        "faq": [{"q": plain(q), "a": plain(a)} for q, a in FAQS],
    }
    write("api/kb.json", json.dumps(kb, indent=1))

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    build_home()
    build_services()
    build_conditions()
    build_about()
    build_podcast()
    build_faq()
    build_contact()
    build_blog()
    build_meta()
    build_kb()
    print("\nDone. Open index.html or deploy the folder to Vercel.")
