#!/usr/bin/env python3
"""
HomeCrew site generator — single source of truth for every public page.

Why this exists
---------------
The site started as one long index.html, which was right for a one-page
brochure. It is now ~18 pages, and a hand-maintained nav/footer/head copied
across 18 files is how a phone number ends up wrong on three of them.

This is NOT the framework that CLAUDE.md rules out. There is no React, no
bundler, no dependency tree and nothing to install: `python3 build.py` writes
plain static HTML that Vercel serves directly. Same output as before, one place
to edit. It mirrors the generator on the firstrehabnpb site, which the owner
already knows.

Workflow
--------
1. Edit this file (or assets/css/site.css, assets/js/site.js)
2. python3 build.py
3. python3 -m http.server 8000  ->  http://localhost:8000

portal.html is deliberately NOT generated. It is an application, not a content
page, and it is hand-maintained.
"""

import hashlib
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://homecrewfl.com"

# ---------------------------------------------------------------- the business
BIZ = {
    "name": "HomeCrew",
    "legal": "HomeCrew",
    "phone_display": "561-383-0882",
    "phone_href": "+15613830882",
    "email": "HomeCrewFL@gmail.com",
    "city": "Stuart",
    "region": "FL",
    "postal": "34994",
    "facebook": "https://www.facebook.com/HomeCrewFL",
    "tagline": "We watch. You relax.",
    "standard": "Professional. Reliable. Local.",
    "sub": "Professional Residential Asset Protection",
    "lat": 27.1973,
    "lon": -80.2528,
}

COUNTY_NAMES = [
    "Indian River County",
    "St. Lucie County",
    "Martin County",
    "Palm Beach County",
    "Broward County",
]

# ------------------------------------------------------------------- cache bust
def asset_v(path):
    """Content hash so a CSS change can never be served stale from a phone."""
    full = os.path.join(ROOT, path)
    with open(full, "rb") as fh:
        return hashlib.sha1(fh.read()).hexdigest()[:10]


CSS_V = asset_v("assets/css/site.css")
JS_V = asset_v("assets/js/site.js")
ICON_V = asset_v("images/apple-touch-icon.png")


def rel(depth):
    """Prefix to reach the site root from a page `depth` folders down."""
    return "../" * depth


# ------------------------------------------------------------------------ logo
def logo_svg(w=44, h=48):
    return (
        f'<svg width="{w}" height="{h}" viewBox="0 0 44 48" aria-hidden="true" focusable="false">'
        '<path d="M22 2 L43 19 L36.5 19 L22 7.6 L7.5 19 L1 19 Z" fill="#fff"/>'
        '<rect x="17.5" y="11.5" width="9" height="9" fill="#CBA15A"/>'
        '<path d="M22 11.5v9M17.5 16h9" stroke="#0B1D2D" stroke-width="1.4"/>'
        '<rect x="7.5" y="19" width="6.5" height="23" fill="#fff"/>'
        '<rect x="30" y="19" width="6.5" height="23" fill="#fff"/>'
        '<rect x="14" y="26.5" width="16" height="6" fill="#CBA15A"/>'
        '<rect x="5" y="42" width="11.5" height="4.5" fill="#CBA15A"/>'
        '<rect x="27.5" y="42" width="11.5" height="4.5" fill="#CBA15A"/></svg>'
    )


def inline_svg(name):
    """The image-fallback pattern from CLAUDE.md: an illustration sits on a layer
    BENEATH the photo, so a failed image shows artwork rather than a broken icon.
    Kept as files so this generator stays readable; inlined so there is no second
    request for something that must be present the instant the photo fails."""
    with open(os.path.join(ROOT, "assets/svg", name), encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------------- nav
def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# (label, href-from-root, [children])
NAV = [
    ("Services", "services/", [
        ("Home Watch", "services/home-watch.html"),
        ("Storm Prep &amp; Response", "services/storm-prep.html"),
        ("Concierge Services", "services/concierge.html"),
        ("Estate Services", "services/estate.html"),
    ]),
    ("Reports", "reports.html", []),
    ("Pricing", "pricing.html", []),
    ("Service Area", "service-area.html",
     [(c, "areas/%s.html" % slugify(c)) for c in COUNTY_NAMES]),
    ("Resources", "blog/", [
        ("Blog", "blog/"),
        ("FAQ", "faq.html"),
    ]),
    ("About", "about.html", []),
]


def nav_html(depth, active):
    r = rel(depth)
    out = []
    for label, href, kids in NAV:
        cls = ' class="here"' if active == href else ""
        if kids:
            sub = "".join(
                f'<a href="{r}{k_href}">{k_label}</a>' for k_label, k_href in kids
            )
            out.append(
                f'<div class="nav-drop"><a href="{r}{href}"{cls}>{label}</a>'
                f'<div class="nav-sub">{sub}</div></div>'
            )
        else:
            out.append(f'<a href="{r}{href}"{cls}>{label}</a>')
    links = "".join(out)
    return f"""<header class="nav">
  <div class="nav-in">
    <a class="brand" href="{r}index.html" aria-label="HomeCrew home">
      {logo_svg()}
      <span class="brand-tx">
        <span class="brand-nm">HOMECREW</span>
        <span class="brand-sub">Professional Residential<br>Asset Protection</span>
        <span class="brand-tag">Firefighter Owned &amp; Operated</span>
      </span>
    </a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav-links" id="navlinks">
      {links}
      <a class="nav-cta" href="{r}contact.html">Schedule a Consultation</a>
      <a href="{r}portal.html" style="color:rgba(255,255,255,.62)">Crew Login</a>
    </nav>
  </div>
</header>"""


# ---------------------------------------------------------------------- footer
def footer_html(depth):
    r = rel(depth)
    areas = "".join(
        f'<li><a href="{r}areas/{slugify(c)}.html">{c}</a></li>' for c in COUNTY_NAMES
    )
    return f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>HomeCrew</h4>
        <p class="foot-p">Professional residential asset protection for Florida's east coast. Firefighter owned and operated. Fully insured and bonded.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="{r}services/home-watch.html">Home Watch</a></li>
          <li><a href="{r}services/storm-prep.html">Storm Prep &amp; Response</a></li>
          <li><a href="{r}services/concierge.html">Concierge Services</a></li>
          <li><a href="{r}services/estate.html">Estate Services</a></li>
          <li><a href="{r}reports.html">Inspection Reports</a></li>
        </ul>
      </div>
      <div>
        <h4>Service Area</h4>
        <ul>{areas}</ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{BIZ['phone_href']}">{BIZ['phone_display']}</a></li>
          <li><a href="mailto:{BIZ['email']}">{BIZ['email']}</a></li>
          <li><a href="{BIZ['facebook']}">@HomeCrewFL</a></li>
          <li><a href="{r}blog/">Blog</a></li>
          <li><a href="{r}faq.html">FAQ</a></li>
          <li><a href="{r}portal.html">Crew Login</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="standard">
    <b>{BIZ['standard']}</b>
    <span>That's the HomeCrew Standard.</span>
  </div>
  <div class="legal">&copy; <span id="yr">{date.today().year}</span> HomeCrew. All rights reserved. Stuart, Florida.</div>
</footer>
<a class="callbar" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a>
<script src="{r}assets/js/site.js?v={JS_V}" defer></script>
<!-- Vercel Web Analytics: cookieless, so no consent banner is required. -->
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>"""


# ------------------------------------------------------------------- head/meta
def head_html(title, desc, canonical, depth, extra_schema=None, page_type="website"):
    r = rel(depth)
    og_img = f"{BASE}/images/homecrew-home-watch-stuart-fl-og.jpg"
    schema = ""
    if extra_schema:
        schema = (
            '\n<script type="application/ld+json">\n'
            + json.dumps(extra_schema, indent=2, ensure_ascii=False)
            + "\n</script>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Stuart, Florida">

<meta property="og:type" content="{page_type}">
<meta property="og:site_name" content="HomeCrew">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Nunito+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/site.css?v={CSS_V}">

<link rel="icon" href="{r}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{r}images/favicon-32.png?v={ICON_V}">
<link rel="apple-touch-icon" href="{r}images/apple-touch-icon.png?v={ICON_V}">
<link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#0B1D2D">{schema}
</head>
<body>"""


def org_schema():
    return {
        "@type": ["HomeAndConstructionBusiness", "LocalBusiness"],
        "@id": f"{BASE}/#business",
        "name": BIZ["name"],
        "alternateName": "HomeCrew Home Watch",
        "description": "Firefighter owned and operated home watch, concierge and estate services for seasonal residents, vacation homeowners and frequent travelers on Florida's east coast.",
        "slogan": BIZ["tagline"],
        "url": BASE + "/",
        "image": f"{BASE}/images/homecrew-home-watch-stuart-fl-og.jpg",
        "telephone": "+1-561-383-0882",
        "email": BIZ["email"],
        "priceRange": "$$",
        "currenciesAccepted": "USD",
        "paymentAccepted": "Cash, Check, Credit Card, ACH",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": BIZ["city"],
            "addressRegion": BIZ["region"],
            "postalCode": BIZ["postal"],
            "addressCountry": "US",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lon"]},
        "areaServed": [
            {"@type": "AdministrativeArea", "name": f"{c}, Florida"} for c in COUNTY_NAMES
        ],
        "sameAs": [BIZ["facebook"]],
    }


def breadcrumbs(trail):
    """trail = [(name, url_from_base), ...] — last item is the current page."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
            for i, (n, u) in enumerate(trail)
        ],
    }


def crumb_html(depth, trail):
    r = rel(depth)
    parts = []
    for i, (name, url) in enumerate(trail):
        if i == len(trail) - 1:
            parts.append(f"<span>{name}</span>")
        else:
            href = r + (url.lstrip("/") or "index.html")
            parts.append(f'<a href="{href}">{name}</a>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<i>/</i>'.join(parts) + "</nav>"


# -------------------------------------------------------------- page furniture
def page_hero(eyebrow, h1, lede, depth, trail=None):
    crumbs = crumb_html(depth, trail) if trail else ""
    return f"""<section class="phero">
  <div class="wrap">
    {crumbs}
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <hr class="rule">
    <p class="phero-lede">{lede}</p>
  </div>
</section>"""


def cta_block(title="Let us handle the details",
              body="Tell us about your home and how long you are away. We will walk the property, recommend a visit schedule and send you a sample report &mdash; no obligation."):
    return f"""<section class="cta">
  <div class="wrap">
    <p class="eyebrow">Schedule a Consultation</p>
    <h2>{title}</h2>
    <p>{body}</p>
    <div class="cta-row">
      <a class="btn btn-gold" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a>
      <a class="btn btn-ghost" href="mailto:{BIZ['email']}">Email {BIZ['email']}</a>
    </div>
  </div>
</section>"""


PAGES = []   # (path_from_root, changefreq, priority)


def write(path, html_text, priority="0.7"):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(html_text)
    PAGES.append((path, priority))
    return path


# =============================================================================
# CONTENT
# =============================================================================

SYSTEMS = [
    ("Security", [
        "Doors &amp; locks", "Windows &amp; sliders", "Garage &amp; overhead",
        "Signs of forced entry", "Alarm &amp; camera status"]),
    ("Plumbing", [
        "Visible leaks", "Water pressure", "Water heater",
        "Drains &amp; traps", "Toilets flushed, faucets run"]),
    ("HVAC", [
        "Cooling operation", "Thermostat setpoint", "Air filter condition",
        "Interior humidity reading", "Condensate line"]),
    ("Exterior", [
        "Roof line (visual)", "Pool &amp; spa", "Landscaping",
        "Irrigation", "Exterior surfaces"]),
    ("Storm Readiness", [
        "Shutters &amp; panels", "Outdoor furniture secured", "Storm supplies on hand",
        "Drains &amp; gutters clear", "Generator &amp; fuel"]),
]

# Pricing appears here AND in the JSON-LD offer catalog. Change both together.
PACKAGES = [
    {"key": "bronze", "name": "Bronze", "price": 99, "cadence": "2 Visits Per Month",
     "flag": "", "items": [
        "Mail &amp; package pickup",
        "Interior &amp; exterior inspection",
        "Doors, windows &amp; locks checked",
        "A/C &amp; humidity check",
        "Leak &amp; moisture check",
        "Toilets flushed, faucets run",
        "Photo report after each visit"]},
    {"key": "silver", "name": "Silver", "price": 199, "cadence": "Weekly Visits",
     "flag": "", "items": [
        "Everything in Bronze",
        "Refrigerator &amp; freezer check",
        "Dishwasher run",
        "Vehicles started monthly",
        "Pool &amp; irrigation check",
        "Delivery coordination",
        "Contractors met on site",
        "Priority phone support"]},
    {"key": "gold", "name": "Gold", "price": 399, "cadence": "Weekly Visits + Concierge",
     "flag": "Most Chosen By Snowbirds", "items": [
        "Everything in Silver",
        "Grocery stocking before arrival",
        "A/C turned on before return",
        "Hurricane shutters opened &amp; closed",
        "Storm preparation checklist",
        "Post-storm inspection in 24&ndash;48 hrs",
        "All repairs coordinated",
        "Home ready when you arrive",
        "Emergency response 24/7"]},
]

CONCIERGE = [
    ("On Demand", [
        ("Emergency visit", "$75 &ndash; $150"),
        ("Meet contractor (first hour)", "$75"),
        ("Additional contractor time", "$50 / hr"),
        ("Wait for furniture delivery", "$75 / hr"),
        ("Water plants", "$25 / visit"),
    ]),
    ("Storm Season", [
        ("Hurricane prep", "$150 &ndash; $400"),
        ("Post-storm inspection", "$100 &ndash; $250"),
        ("Pressure washing coordination", "$50"),
        ("Coordinate cleaning crew", "$50"),
    ]),
    ("Arrival &amp; Departure", [
        ("Grocery shopping", "$50 + groceries"),
        ("Airport pickup / drop off", "$75 &ndash; $150"),
        ("Vehicle start / drive", "$40 &ndash; $75"),
        ("Move-in setup", "$150 &ndash; $300"),
    ]),
]

# Honest, checkable geography only. No invented drive times, no fake offices.
COUNTIES = {
    "Indian River County": {
        "blurb": "The north end of our run. Vero Beach and Sebastian sit far enough up the coast that a lot of home watch companies quietly stop before they get there.",
        "towns": "Vero Beach, Sebastian, Wabasso, Orchid, Indian River Shores",
        "note": "Barrier island properties here take the brunt of salt air. Exterior surfaces and window seals get extra attention on the sweep.",
    },
    "St. Lucie County": {
        "blurb": "Port St. Lucie, Fort Pierce and Hutchinson Island &mdash; a mix of gated golf communities and older coastal homes, each with its own failure habits.",
        "towns": "Port St. Lucie, Fort Pierce, Hutchinson Island, St. Lucie West",
        "note": "Many of these communities run their own gate systems. We keep the gate and lock box details on file so a visit never turns into a phone call from the entrance.",
    },
    "Martin County": {
        "blurb": "Home base. Stuart, Palm City, Jensen Beach, Hobe Sound and Sewall's Point are the shortest drive we make, which means the fastest response when something goes wrong.",
        "towns": "Stuart, Palm City, Jensen Beach, Hobe Sound, Sewall's Point, Rio",
        "note": "Being local is the whole product. When an alarm trips at 2am in Martin County, we are minutes away rather than hours.",
    },
    "Palm Beach County": {
        "blurb": "Jupiter down through West Palm Beach, Palm Beach Gardens and the barrier island. Heavily seasonal &mdash; a lot of these homes sit empty from May to October.",
        "towns": "Jupiter, Palm Beach Gardens, North Palm Beach, West Palm Beach, Palm Beach, Wellington",
        "note": "Long empty stretches are exactly where humidity does its quiet damage. Weekly visits are the norm here rather than the exception.",
    },
    "Broward County": {
        "blurb": "The south end of our footprint, from Deerfield Beach and Pompano down through Fort Lauderdale.",
        "towns": "Fort Lauderdale, Pompano Beach, Deerfield Beach, Coral Springs, Weston",
        "note": "Condo and high-rise units have their own access rules. We work with building management rather than around it.",
    },
}

FAQ = [
    ("What is a home watch service?",
     "Home watch is a scheduled visual inspection of a vacant or seasonally occupied home. A technician walks the interior and exterior looking for evidence of water intrusion, mold, pests, storm damage, HVAC failure and security issues, then documents the visit with photos. It is not house sitting and it is not a security patrol &mdash; it is early detection, so a small problem never becomes a five figure insurance claim."),
    ("How often should a Florida home be checked while I am away?",
     "Most Florida carriers and home watch standards call for inspections every 7 to 14 days. Humidity, power interruptions and plumbing failures move fast in this climate &mdash; a supply line that lets go on day two of a three month absence is a very different repair than one caught on day seven. Weekly visits are the most common choice for homeowners who leave for the summer."),
    ("Does home watch affect my homeowners insurance?",
     "Many Florida policies limit or exclude water damage coverage in a home left unoccupied beyond a set number of days unless it is being checked on a documented schedule. Our timestamped inspection reports give you that documentation. Ask your carrier what interval your policy requires and we will build the schedule around it &mdash; we are not insurance advisors, but we will happily send your agent a sample report."),
    ("What happens after a hurricane?",
     "Once conditions are safe, we perform a post-storm inspection within 24 to 48 hours and send a photo report covering the roof line, windows, doors, pool cage, screens and any water intrusion. If repairs are needed we coordinate vendors and stay on site so you do not have to fly back."),
    ("What areas do you serve?",
     "Five Florida counties, from our base in Stuart: Indian River County, St. Lucie County, Martin County, Palm Beach County and Broward County. That covers the coast from Vero Beach down through Fort Lauderdale. If your home is inside that footprint we can put it on a schedule."),
    ("What do I actually receive after each visit?",
     "A timestamped report with an Overall Home Health Score out of 100, each of the five systems scored separately, photos from the visit, any attention items with a note and photo attached to the specific line they relate to, recommended actions, and the arrival and departure times of the technician who walked it."),
    ("Are you licensed and insured?",
     "HomeCrew is fully insured and bonded. Proof of coverage is available on request &mdash; ask and we will send it before you sign anything."),
    ("Who actually visits my home?",
     "A HomeCrew technician who signs in as themselves. The report carries their name, so every visit is attributable to a person rather than to a company."),
    ("Can you let a contractor in while I am away?",
     "Yes. Meeting contractors and waiting for deliveries is part of concierge service, billed a la carte or included depending on your package. We stay on site rather than handing over a key."),
    ("What if you find something wrong?",
     "You hear about it that day, not at the end of the month. If it needs a vendor we coordinate one and stay on site. Anything urgent gets a phone call, not just a line in the report."),
]

BLOG_POSTS = [
    {
        "slug": "prepare-florida-home-hurricane-season-trip",
        "title": "How to prepare your Florida home before a long trip during hurricane season",
        "seo_title": "Prepare Your Florida Home for Hurricane Season",
        "desc": "A practical pre-departure checklist for Florida homeowners leaving during hurricane season, from water shutoff and A/C settings to shutters, documentation and who holds a key.",
        "date": "2026-08-05",
        "read": "8 min read",
        "lede": "Hurricane season runs June through November, which overlaps almost exactly with the months most seasonal residents are gone. Leaving is not the problem. Leaving without doing these things is.",
        "body": [
            ("h2", "Start with water, because water is what actually gets you"),
            ("p", "Wind damage is dramatic and it is what everybody pictures. Water is what quietly destroys houses. A supply line behind a washing machine that lets go in week two of a four month absence will run continuously until somebody notices, and in a closed Florida house that means mould through the drywall long before it means a puddle at the front door."),
            ("p", "Before you leave, shut off the main water supply if nothing in the home requires it. If you have an irrigation system, an ice maker or a pool autofill that needs pressure, ask a plumber about isolating just those lines rather than leaving the whole house pressurised."),
            ("ul", [
                "Find your main shutoff now, while you are not in a hurry, and photograph it",
                "Label it clearly so anyone checking the home can find it in the dark",
                "Consider a leak detection device with an automatic shutoff valve",
                "Drain and turn off the water heater if the home will be empty for months",
            ]),
            ("h2", "Set the air conditioning, do not turn it off"),
            ("p", "This is the single most common expensive mistake. Turning the A/C off to save money in an empty Florida house is how you come home to mould on the ceilings and warped cabinet doors. The air conditioner is not there for comfort while you are gone. It is there to pull moisture out of the air."),
            ("p", "Set the thermostat somewhere in the high seventies to low eighties and leave it running. The goal is to keep interior humidity down, not to keep the house cold. A humidistat, if you have one, is the better tool &mdash; it runs the system based on moisture rather than temperature, which uses far less power over a long absence."),
            ("callout", "Change the filter before you go. A filter that is already dirty in May is a restricted, straining system by August, and a frozen coil is a very expensive way to discover that."),
            ("h2", "Storm hardware, checked rather than assumed"),
            ("p", "Shutters that worked three seasons ago are not the same as shutters that work today. Tracks corrode, panels go missing, wing nuts seize, and the accordion shutter that nobody has closed since the last storm is the one that jams."),
            ("ul", [
                "Close and reopen every shutter or panel before you leave, and note anything that sticks",
                "Confirm you have every panel, and that the hardware to mount them is in one known place",
                "Bring in or secure patio furniture, planters, grills and anything else that becomes a projectile",
                "Clear gutters and roof drains &mdash; blocked drainage backs water up under roofing",
                "If you have a generator, run it, and store fuel safely with stabiliser",
            ]),
            ("h2", "Decide who can act, not just who can look"),
            ("p", "A neighbour with a key is a kind gesture. It is not a plan. When a storm is forecast, the question is not whether somebody can look at your house &mdash; it is whether somebody can put the shutters up, meet a roofer, photograph damage for a claim, and reach you with a decision at nine at night."),
            ("p", "Whoever that is, they need three things before you leave: access that actually works, written permission to authorise emergency repairs up to an agreed amount, and your insurance details. Sorting that out from a thousand miles away, during a storm, does not go well."),
            ("h2", "Document the house before you go"),
            ("p", "Walk every room with your phone and take video. Open cabinets and closets. Photograph the roof line, the pool cage, the screens and the exterior on all four sides. Photograph serial numbers on major appliances and the HVAC unit."),
            ("p", "This is the record that settles arguments later. An adjuster who can see what a room looked like in May is in a very different conversation than one who cannot. Store it somewhere that is not the house &mdash; cloud storage, or emailed to yourself."),
            ("h2", "The small things that are not small"),
            ("ul", [
                "Stop the mail and newspaper, or arrange for pickup. Nothing advertises an empty house like a full mailbox",
                "Unplug electronics that do not need power, to protect them from surges",
                "Empty the refrigerator of anything perishable if power loss is a risk, and prop the door if you shut it off",
                "Put interior lights on timers rather than leaving one burning for four months",
                "Tell your alarm company you will be away, and confirm the call list is current",
                "Check that your policy is actually in force through your return date",
            ]),
            ("h2", "What a home watch service changes about this list"),
            ("p", "Most of the above you do once, on your way out the door. The problem is that a house does not hold still for four months. Filters clog, batteries die, seals fail, storms arrive on short notice, and every one of those events happens after your checklist is finished."),
            ("p", "Scheduled inspections are how the list stays true after you leave. A technician walking the property every week catches the drip before the ceiling, runs the taps so traps do not dry out and let sewer gas in, confirms the A/C is still doing its job, and puts the shutters up when a storm is named rather than when it makes landfall."),
            ("p", "It also produces the documentation your insurer may want. Many Florida policies limit water damage coverage in a home left unoccupied beyond a set number of days unless it is being checked on a documented schedule. Ask your carrier what interval applies to your policy &mdash; and then make sure somebody is actually keeping that record."),
        ],
    },
    {
        "slug": "empty-florida-house-air-conditioning-humidity",
        "title": "Why an empty Florida house still needs air conditioning",
        "desc": "Turning the A/C off in a vacant Florida home to save money is how mould starts. What humidity actually does to an empty house, and what to set the thermostat to.",
        "date": "2026-07-28",
        "read": "5 min read",
        "lede": "It feels wasteful to cool a house nobody is living in. It is far more wasteful to remediate mould through every ceiling in that house.",
        "body": [
            ("h2", "The air conditioner is a dehumidifier that happens to cool"),
            ("p", "In a Florida summer, outdoor humidity sits high for months at a time. A closed house does not stay dry on its own &mdash; moisture moves in through the building envelope, through slab, through every opening, and it keeps coming."),
            ("p", "When your air conditioner runs, it pulls that moisture out of the air and drains it away. Switch it off and you have a sealed, warm, humid box. That is the environment mould is looking for, and it does not need a leak to get started. Interior surfaces are enough."),
            ("h2", "What actually goes wrong"),
            ("ul", [
                "Mould on ceilings, walls and behind furniture, often first in closets and corners with no air movement",
                "Wood swelling &mdash; doors that no longer close, cabinet faces that separate, floors that cup",
                "Musty odour absorbed into soft furnishings, which outlasts the humidity that caused it",
                "Corrosion on electronics and metal fittings",
                "Damage that is slow, invisible from outside, and well advanced by the time anybody opens the door",
            ]),
            ("h2", "What to set it to"),
            ("p", "Somewhere in the high seventies to low eighties is the usual advice for an unoccupied Florida home. You are not trying to keep it cold. You are trying to keep the system cycling often enough to hold humidity down, ideally under about sixty percent."),
            ("p", "If your thermostat supports a humidistat, use it. It runs the system based on moisture rather than temperature, which means on a mild dry day it does not run at all, and on a wet still day it does. Over a four month absence that difference shows up on the power bill."),
            ("callout", "A system set correctly is not the same as a system working correctly. A tripped breaker, a clogged condensate line or a frozen coil turns your careful setting into an unconditioned house, and nothing about the outside of the building will tell you it happened."),
            ("h2", "The failure nobody plans for"),
            ("p", "The condensate line is the part that catches people out. All that moisture the A/C pulls from the air has to drain somewhere. The line clogs with algae, water backs up, and either a safety switch shuts the system down or the pan overflows into the ceiling below."),
            ("p", "Either outcome is bad in an empty house. If the safety switch does its job, the A/C stops and humidity climbs for however many weeks remain. If it does not, you have water coming through a ceiling with nobody there to notice."),
            ("p", "Checking cooling operation, thermostat setpoint, filter condition, interior humidity and the condensate line is why HVAC is one of the five systems on every HomeCrew visit. Not because it is likely to fail on any given week, but because the cost of finding out late is so much higher than the cost of looking."),
        ],
    },
    {
        "slug": "home-watch-vs-neighbor-checking-in",
        "title": "Home watch vs. asking a neighbour to check in",
        "desc": "A neighbour with a key is a favour, not a plan. The practical differences between a friend looking in on your Florida home and a documented home watch inspection.",
        "date": "2026-07-20",
        "read": "6 min read",
        "lede": "This is not an argument that your neighbour is unreliable. It is an argument that you have asked them to do a job they were never set up to do.",
        "body": [
            ("h2", "What you are actually asking for"),
            ("p", "When you ask a neighbour to keep an eye on the place, both of you usually picture the same thing: they will notice if something looks obviously wrong from the street. That is genuinely useful. It is also a very small fraction of what goes wrong in an empty Florida house."),
            ("p", "Almost nothing on the list is visible from outside. A slow supply line leak, a failed condensate drain, humidity climbing because the A/C tripped a breaker, dried out P-traps letting sewer gas in, a pool losing water &mdash; all of it requires somebody inside, looking at specific things, on a schedule."),
            ("h2", "The four differences that matter"),
            ("h3", "1. A protocol instead of a glance"),
            ("p", "A friend walks through and forms a general impression. An inspection runs the same twenty five checks in the same order on every visit, so nothing depends on whether the person happened to think of it that day. Consistency is the point &mdash; it is what makes the third visit comparable to the first."),
            ("h3", "2. Documentation you can hand to an adjuster"),
            ("p", "Many Florida policies limit or exclude water damage coverage in a home left unoccupied beyond a set number of days unless it is being checked on a documented schedule. A neighbour's text saying \"all good\" is not that record. A timestamped report with photos is. Ask your carrier what interval your policy requires &mdash; we are not insurance advisors, but this is a question worth asking before you need the answer."),
            ("h3", "3. Insurance on the person doing it"),
            ("p", "If a neighbour slips on your pool deck, or accidentally causes damage while helping, the situation is uncomfortable at best. A bonded and insured company carries its own coverage. That protects you and it protects the friendship."),
            ("h3", "4. Someone whose job it is to answer at 2am"),
            ("p", "The genuinely hard part is not the looking. It is what happens next. Somebody has to be reachable, willing to drive over at an inconvenient hour, able to authorise and meet a vendor, and comfortable making a call on your behalf. That is a large thing to ask of a favour, and most people quietly stop doing it by the second season."),
            ("callout", "The most common way neighbour arrangements fail is not neglect. It is that the neighbour also travels, gets ill, or moves &mdash; and nobody thinks to tell you until the month it matters."),
            ("h2", "Where a neighbour is genuinely better"),
            ("p", "They are next door. They will notice a strange vehicle at an odd hour, or a storm shutter banging in the night, in a way no scheduled service can. Keep that. Tell them who HomeCrew is and give them a number to call."),
            ("p", "The two things are not in competition. One is presence and the other is protocol. Homes that come through a long absence without incident usually have both."),
        ],
    },
    {
        "slug": "what-25-point-home-watch-inspection-covers",
        "title": "What a 25-point home watch inspection actually covers",
        "desc": "The five systems and twenty five checks HomeCrew runs on every visit, why each one is on the list, and what the resulting report looks like.",
        "date": "2026-07-12",
        "read": "7 min read",
        "lede": "\"We check on your house\" is not a service description. This is the actual list, in the actual order, run the same way on every property.",
        "body": [
            ("p", "Every HomeCrew visit runs the same five-system sweep. The technician clears each line in the field on a phone or tablet, attaches a photo and a note to anything that is not a clean pass, and the report is generated from those entries rather than written up afterwards from memory."),
            ("h2", "System 01 &mdash; Security"),
            ("p", "Doors and locks, windows and sliders, garage and overhead doors, any sign of forced entry, and the status of alarm and camera systems. This is the fastest part of the walk and the one where a problem is most obvious, which is exactly why it goes first."),
            ("h2", "System 02 &mdash; Plumbing"),
            ("p", "Visible leaks, water pressure, the water heater, drains and traps, and running every toilet and tap. That last one sounds trivial and is not: P-traps hold a plug of water that stops sewer gas coming back up the drain, and in a hot empty house that water evaporates in weeks. Running the fixtures refills them."),
            ("h2", "System 03 &mdash; HVAC"),
            ("p", "Cooling operation, thermostat setpoint, filter condition, an interior humidity reading and the condensate line. Humidity is the number that predicts trouble in a Florida house, and the condensate line is the component most likely to quietly take the system out of service."),
            ("h2", "System 04 &mdash; Exterior"),
            ("p", "A visual check of the roof line, the pool and spa, landscaping, irrigation and exterior surfaces. Pool water level and clarity are worth watching closely &mdash; a pool that is dropping faster than evaporation explains is telling you something."),
            ("h2", "System 05 &mdash; Storm Readiness"),
            ("p", "Shutters and panels, outdoor furniture secured, storm supplies on hand, drains and gutters clear, generator and fuel. This one is checked year round rather than in June, because the time to discover a seized shutter track is not the day a storm is named."),
            ("h2", "How the score works"),
            ("p", "Each line is marked OK, Watch or Issue. Each of the five systems is scored out of 100, and those roll into an Overall Home Health Score. The score exists to make one visit comparable to the last one &mdash; a home that has been at 100 for four months and comes in at 82 is telling you something specific, and the report says exactly which lines moved."),
            ("callout", "Anything marked Watch or Issue carries its own photo and note, attached to that line. A photo of the actual stain under \"visible leaks\" is worth more than the same photo in a pile at the bottom of the report."),
            ("h2", "What arrives in your inbox"),
            ("p", "The property and visit details including arrival and departure times and the name of the technician, the overall score, each system scored separately, every attention item with its photo and note, photo highlights from the visit, recommended actions with timeframes, and the after hours contact number."),
            ("p", "It is the same document every time, which is the point. You should not have to interpret a report to find out whether your house is fine."),
        ],
    },
]


# =============================================================================
# SHARED SECTION RENDERERS
# =============================================================================

def protocol_grid():
    cols = ""
    for i, (name, items) in enumerate(SYSTEMS):
        lis = "".join(f"<li>{it}</li>" for it in items)
        cols += (f'<div class="proto-col reveal"><span class="idx">System 0{i+1}</span>'
                 f"<h3>{name}</h3><ul>{lis}</ul></div>")
    return f'<div class="proto">{cols}</div>'


def package_cards(depth):
    r = rel(depth)
    out = ""
    for i, p in enumerate(PACKAGES, start=1):
        lis = "".join(f'<li class="on">{it}</li>' for it in p["items"])
        flag = f'<div class="pkg-flag">{p["flag"]}</div>' if p["flag"] else ""
        btn = "btn-gold" if p["key"] == "gold" else "btn-ghost"
        style = "" if p["key"] == "gold" else ' style="border-color:var(--navy);color:var(--navy)"'
        out += f"""
      <div class="pkg pkg-{i} reveal">
        <div class="pkg-top"><h3>{p['name']}</h3></div>
        <div class="pkg-price"><b><sup>$</sup>{p['price']}</b><i>/month</i><span>{p['cadence']}</span></div>
        <ul>{lis}</ul>
        <a class="btn {btn}" href="{r}contact.html"{style}>Get Started</a>
        {flag}
      </div>"""
    return f'<div class="pkg-grid">{out}</div>'


def report_mock():
    """Mirrors renderReport() in portal.html. Change both together."""
    return """<div class="doc" role="img" aria-label="Example HomeCrew inspection report showing an overall home health score of 85, five system scores, one attention item with a note and photo, and a row of visit photos">
        <span class="doc-tag">Sample</span>
        <div class="doc-h">
          """ + logo_svg(26, 29) + """
          <span class="dm">HOMECREW</span>
          <span class="dt">Inspection Report<br>Visit 14 &middot; 9:05&ndash;9:47 AM</span>
        </div>
        <div class="doc-b">
          <div class="doc-score">
            <svg class="doc-ring" viewBox="0 0 110 110" aria-hidden="true">
              <circle class="trk" cx="55" cy="55" r="47"/>
              <circle class="val" cx="55" cy="55" r="47"/>
              <text x="55" y="58" text-anchor="middle" font-size="30">85</text>
              <text x="55" y="74" text-anchor="middle" font-size="10" fill="#6B7178">/100</text>
            </svg>
            <div>
              <div class="sl">Overall Home Health Score&trade;</div>
              <div class="sb">Very Good</div>
              <p>One item needs follow-up. Details are listed under Attention Items below.</p>
            </div>
          </div>
          <div class="doc-sys">
            <div><h5>Security</h5><b style="color:#246F41">100</b></div>
            <div><h5>Plumbing</h5><b style="color:#246F41">93</b></div>
            <div><h5>HVAC</h5><b style="color:#8F6611">73</b></div>
            <div><h5>Exterior</h5><b style="color:#246F41">87</b></div>
            <div><h5>Storm</h5><b style="color:#246F41">100</b></div>
          </div>
          <div class="doc-lab">Attention Items</div>
          <div class="doc-flag"><b>HVAC</b> &nbsp;Air filter condition &mdash; monitor
            <em>Filter grey at the edges, not clogged. Recommend swapping at the next visit.</em>
            <span class="doc-ph doc-ph-1"><i></i></span>
          </div>
          <div class="doc-lab">Photo Highlights</div>
          <div class="doc-ph"><i></i><i></i><i></i><i></i></div>
        </div>
      </div>"""


def county_corridor(depth, active=None):
    r = rel(depth)
    meta = {"Indian River County": "North end", "St. Lucie County": "Treasure Coast",
            "Martin County": "Home base &middot; Stuart", "Palm Beach County": "Gold Coast",
            "Broward County": "South end"}
    rows = ""
    for c in COUNTY_NAMES:
        hq = " hq" if c == "Martin County" else ""
        cur = " current" if c == active else ""
        rows += (f'<a class="co reveal{hq}{cur}" href="{r}areas/{slugify(c)}.html">'
                 f'<span class="co-node"></span><span class="co-nm">{c}</span>'
                 f'<span class="co-meta">{meta[c]}</span></a>')
    return f'<div class="corridor">{rows}</div>'


def faq_accordion(items, open_first=True):
    out = ""
    for i, (q, a) in enumerate(items):
        op = " open" if (open_first and i == 0) else ""
        out += f"<details{op}><summary>{q}</summary><p>{a}</p></details>"
    return out


def prose(blocks):
    out = ""
    for kind, val in blocks:
        if kind == "p":
            out += f"<p>{val}</p>"
        elif kind == "h2":
            out += f"<h2>{val}</h2>"
        elif kind == "h3":
            out += f"<h3>{val}</h3>"
        elif kind == "ul":
            out += "<ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>"
        elif kind == "callout":
            out += f'<aside class="callout">{val}</aside>'
    return out


def service_cards(depth, exclude=None):
    r = rel(depth)
    cards = [
        ("Home Watch", "services/home-watch.html",
         "Scheduled 25-point inspections of your empty home, with a photo report after every visit."),
        ("Storm Prep &amp; Response", "services/storm-prep.html",
         "Shutters up before the storm, a documented inspection within 24 to 48 hours after it."),
        ("Concierge Services", "services/concierge.html",
         "Contractors met, deliveries received, groceries in the fridge and the A/C on before you land."),
        ("Estate Services", "services/estate.html",
         "Estate sales, cleanouts, downsizing and donation coordination &mdash; discreet and documented."),
    ]
    out = ""
    for name, href, blurb in cards:
        if exclude and href.endswith(exclude):
            continue
        out += (f'<a class="scard reveal" href="{r}{href}"><h3>{name}</h3><p>{blurb}</p>'
                f'<span class="scard-go">Read more</span></a>')
    return f'<div class="scards">{out}</div>'


# =============================================================================
# PAGES
# =============================================================================

def build_home():
    schema = {"@context": "https://schema.org", "@graph": [
        org_schema(),
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": BASE + "/",
         "name": "HomeCrew", "publisher": {"@id": f"{BASE}/#business"}},
        {"@type": "OfferCatalog", "name": "Home Watch Packages",
         "itemListElement": [
             {"@type": "Offer", "name": p["name"],
              "price": str(p["price"]), "priceCurrency": "USD",
              "description": p["cadence"]} for p in PACKAGES]},
    ]}
    hero_photo = inline_svg("hero-illustration.svg") + """
  <div class="hero-photo">
    <picture>
      <source media="(max-width:680px)" type="image/webp" srcset="images/home-watch-stuart-fl-mobile.webp">
      <source media="(max-width:680px)" type="image/jpeg" srcset="images/home-watch-stuart-fl-mobile.jpg">
      <source type="image/webp" srcset="images/home-watch-stuart-fl.webp">
      <img src="images/home-watch-stuart-fl.jpg" width="2000" height="1150" fetchpriority="high" decoding="async"
           alt="Florida home at dusk with lit windows and palm trees, protected by HomeCrew home watch in Stuart, FL">
    </picture>
  </div>"""
    pillars = [
        ("Routine<br>Inspections", '<path d="M12 1.8 20.6 5v6.6c0 5.1-3.5 8.9-8.6 10.6C6.9 20.5 3.4 16.7 3.4 11.6V5z" stroke-linejoin="round"/><path d="m12 7.6 1.5 3.1 3.4.5-2.4 2.4.6 3.4-3.1-1.6-3.1 1.6.6-3.4-2.4-2.4 3.4-.5z" stroke-linejoin="round"/>'),
        ("Detailed<br>Photo Reports", '<rect x="1.8" y="6.4" width="20.4" height="14.4" rx="2.4"/><path d="M8.2 6.4 9.5 3.4h5l1.3 3" stroke-linejoin="round"/><circle cx="12" cy="13.6" r="4.2"/>'),
        ("Storm<br>Prep &amp; Response", '<path d="M6.4 15.4A4.1 4.1 0 0 1 6.7 7.3a5.9 5.9 0 0 1 11.1 1.2 3.7 3.7 0 0 1-.3 6.9" stroke-linejoin="round"/><path d="M13.4 11.4 9.8 17h3.4l-2.6 4.6" stroke-linejoin="round" stroke-linecap="round"/>'),
        ("Vendor<br>Coordination", '<path d="M14.7 3.6a4.4 4.4 0 0 1 5.7 5.7l-9.5 9.5-1.7 2.6-2.6-2.6 2.6-1.7 9.5-9.5" stroke-linejoin="round" stroke-linecap="round"/><path d="M9.3 3.6a4.4 4.4 0 0 0-5.7 5.7l9.5 9.5 1.7 2.6 2.6-2.6-2.6-1.7-9.5-9.5" stroke-linejoin="round" stroke-linecap="round"/>'),
        ("Security<br>You Can Trust", '<rect x="4.2" y="10.2" width="15.6" height="11.2" rx="2"/><path d="M7.8 10.2V6.9a4.2 4.2 0 0 1 8.4 0v3.3" stroke-linecap="round"/><circle cx="12" cy="14" r="1.5"/>'),
    ]
    pill_html = "".join(
        f'<div class="pill"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg><span>{n}</span></div>'
        for n, p in pillars)

    stats = [
        ('<circle cx="12" cy="12" r="9.2"/><path d="m7.6 12.2 3 3 5.8-6"/>', '<b data-count="25">25</b>', "Point Inspection"),
        ('<rect x="3.2" y="5" width="17.6" height="16" rx="2"/><path d="M3.2 9.6h17.6M8 3v4M16 3v4"/>', '<b data-count="5">5</b>', "Systems, Every Visit"),
        ('<circle cx="12" cy="12" r="9.2"/><path d="M12 6.4V12l4 2.4"/>', "<b>24/7</b>", "Emergency Response"),
        ('<path d="M12 2 20 5.5v6c0 5-3.5 8.8-8 10.5-4.5-1.7-8-5.5-8-10.5v-6z"/><path d="m9 12 2.2 2.2L15.4 10"/>',
         '<b style="font-size:17px;letter-spacing:.02em">INSURED &amp; BONDED</b>', "For Your Protection"),
    ]
    stat_html = "".join(
        f'<div class="stat"><svg viewBox="0 0 24 24" aria-hidden="true">{i}</svg><div>{b}<span>{l}</span></div></div>'
        for i, b, l in stats)

    body = f"""
<main>
<section class="hero">
  {hero_photo}
  <div class="hero-in">
    <h1>Leave Florida.<br>Not your<br><span class="gold">peace of mind.</span></h1>
    <hr class="rule">
    <p class="hero-sub">Professional home watch so you can relax.</p>
    <div class="hero-btns">
      <a class="btn btn-gold" href="contact.html">Schedule a Consultation</a>
      <a class="btn btn-ghost" href="pricing.html">See Pricing</a>
    </div>
  </div>
  <div class="scrollcue" aria-hidden="true"><i></i>Scroll</div>
  <div class="pillars"><div class="pillars-in">{pill_html}</div></div>
</section>

<section class="protect">
  <div class="wrap protect-grid">
    <div>
      <h2>We protect what matters most</h2>
      <hr class="rule">
      <p>HomeCrew provides professional home watch and property management for seasonal residents, vacation homeowners and people who travel often. We are your trusted local contact &mdash; the person who walks the property, spots the leak before the drywall goes, and picks up the phone at 2am when the alarm trips.</p>
      <p>Every visit ends with a timestamped photo report in your inbox. You always know exactly what we saw and exactly what we did.</p>
      <a class="btn btn-gold" href="services/home-watch.html">How Home Watch Works</a>
    </div>
    <div class="ff-card">
      {inline_svg("firefighter.svg")}
      <div class="ff-photo">
        <picture>
          <source type="image/webp" srcset="images/firefighter-turnout-gear.webp">
          <img src="images/firefighter-turnout-gear.jpg" width="1100" height="594" loading="lazy" decoding="async"
               alt="Firefighter turnout coats and helmet on a station rack — HomeCrew is firefighter owned and operated">
        </picture>
      </div>
      <div class="ff-in">
        <svg class="ff-shield" viewBox="0 0 24 28" aria-hidden="true"><path d="M12 1 22 5.2v9.6c0 6.2-4.6 10.6-10 12.2C6.6 25.4 2 21 2 14.8V5.2z" stroke-linejoin="round"/><path d="M12 7.6 18 12.6v6.4h-4.6v-4h-2.8v4H6.6v-6.4z" fill="#fff" stroke="none"/></svg>
        <h3>Firefighter<small>Owned &amp; Operated</small></h3>
        <p>Built on a foundation of service, integrity and attention to detail. We are trained to notice what is wrong before it becomes an emergency. Your home is in good hands.</p>
        <a class="btn btn-ghost" href="about.html" style="margin-top:20px">Our Story</a>
      </div>
    </div>
  </div>
</section>

<section class="stats" aria-label="What every client gets">
  <div class="stats-in">{stat_html}</div>
</section>

<section class="watch">
  <div class="wrap watch-in">
    <div class="watch-head">
      <div><p class="eyebrow">The Protocol</p><h2>The same 25 checks, every visit</h2></div>
      <p>Every HomeCrew visit runs the same five-system sweep, in the same order, on every property. Nothing is left to memory. The technician clears each line in the field and the report writes itself.</p>
    </div>
    {protocol_explorer()}
    {figs([("25", "Checks Per Visit"), ("5", "Systems Scored"), ("100", "Point Health Score")])}
    <div class="watch-note">
      <p><b style="color:#fff">Every system is scored out of 100 and rolled into an Overall Home Health Score&trade;.</b> You get the score, the photos and the recommended actions in one report &mdash; the same documentation your insurance carrier may ask for after a claim. <a href="reports.html" style="color:var(--gold)">See what the report looks like &rarr;</a></p>
    </div>
  </div>
</section>

<section class="secgrid">
  <div class="wrap">
    <p class="eyebrow">What We Do</p>
    <h2>Four ways we look after the place</h2>
    {service_cards(0)}
  </div>
</section>

<section class="watch">
  <div class="wrap watch-in">
    <div class="watch-head">
      <div><p class="eyebrow">How It Works</p><h2>From the first walkthrough onward</h2></div>
      <p>No contract to sign before anyone has seen the house. The walkthrough is free and takes about an hour.</p>
    </div>
    {process_list()}
  </div>
</section>

<section class="report">
  <div class="wrap report-grid">
    <div class="report-copy reveal">
      <p class="eyebrow">After Every Visit</p>
      <h2>The report in your inbox</h2>
      <p>You are a thousand miles away. A phone call saying &ldquo;everything looked fine&rdquo; is not documentation. This is.</p>
      <ul class="rep-list">
        <li><b>An Overall Home Health Score&trade;</b> out of 100, with every system scored separately</li>
        <li><b>Timestamped photos</b> from the visit &mdash; exterior, interior, mechanicals</li>
        <li><b>Attention items</b> with a photo and note attached to the exact line they relate to</li>
        <li><b>Recommended actions</b> with the timeframe each one needs</li>
        <li><b>Arrival and departure times</b>, weather, and the technician who walked it</li>
      </ul>
      <a class="btn btn-gold" href="reports.html">See a Full Report</a>
    </div>
    <div class="reveal">{report_mock()}</div>
  </div>
</section>

<section class="pkgs">
  <div class="wrap">
    <div class="pkg-head">
      <p class="eyebrow">Home Watch Packages</p>
      <h2>Choose your coverage</h2>
      <p>Flexible packages. Personalized care. Total peace of mind.</p>
    </div>
    {package_cards(0)}
    <p style="text-align:center;margin-top:34px"><a class="btn btn-ghost" href="pricing.html" style="border-color:var(--navy);color:var(--navy)">Compare Packages In Detail</a></p>
  </div>
</section>

<section class="areas">
  <div class="wrap areas-in">
    <div class="areas-head">
      <div><p class="eyebrow">Where We Work</p><h2>Five counties, one standard</h2></div>
      <p>We run north to south out of Stuart. Same protocol, same report, same phone number at 2am &mdash; whether your home is in Vero Beach or Fort Lauderdale.</p>
    </div>
    <div class="mapwrap">
      {coast_map(0)}
      <div class="map-side">{county_corridor(0)}</div>
    </div>
    <div class="areas-foot">
      <p>Not sure whether your address falls inside the footprint? Call and ask &mdash; if we cannot cover it, we will say so.</p>
      <a class="btn btn-gold" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a>
    </div>
  </div>
</section>

<section class="faq">
  <div class="wrap">
    <p class="eyebrow">Homeowner Resources</p>
    <h2>Questions we get every season</h2>
    {faq_accordion(FAQ[:5])}
    <p style="margin-top:26px"><a class="btn btn-ghost" href="faq.html" style="border-color:var(--navy);color:var(--navy)">All Questions</a></p>
  </div>
</section>

{cta_block()}
</main>
"""
    doc = (head_html("Home Watch Stuart FL | HomeCrew &mdash; Firefighter Owned",
                     "Firefighter owned home watch for seasonal Florida homeowners. Routine 25-point inspections, timestamped photo reports, storm prep and 24/7 response across five counties.",
                     BASE + "/", 0, schema)
           + nav_html(0, "") + body + footer_html(0))
    write("index.html", doc, "1.0")


# ------------------------------------------------------------------- services
SERVICES = {
    "home-watch": {
        "title": "Home Watch Services | Stuart &amp; Florida's East Coast | HomeCrew",
        "desc": "Scheduled 25-point home watch inspections for vacant and seasonal Florida homes. Five systems checked every visit, photo report after each one. Firefighter owned.",
        "eyebrow": "Service",
        "h1": "Home watch",
        "lede": "Scheduled inspections of your empty home, run to the same protocol every time, documented with photos you actually receive.",
        "schema_name": "Home Watch",
        "schema_desc": "Scheduled inspection of vacant and seasonally occupied homes, covering security, plumbing, HVAC, exterior and storm readiness, with a photographic report after every visit.",
        "body": [
            ("h2", "What it is, and what it is not"),
            ("p", "Home watch is a scheduled visual inspection of a vacant or seasonally occupied home. It is not house sitting, and it is not a security patrol. It is early detection &mdash; somebody inside the property, on a schedule, looking at the specific things that fail in Florida houses, so that a small problem never becomes a five figure claim."),
            ("p", "Almost nothing on our list is visible from the street. A supply line weeping behind a washing machine, a condensate drain backing up into a ceiling, humidity climbing because a breaker tripped, P-traps drying out and letting sewer gas in &mdash; all of it needs somebody inside, looking at particular things, in a particular order."),
            ("h2", "The five systems"),
            ("p", "Every visit runs the same sweep. The technician clears each line in the field, attaches a photo and a note to anything that is not a clean pass, and the report is generated from those entries rather than written up afterwards from memory."),
        ],
        "after_protocol": [
            ("h2", "How often"),
            ("p", "Most Florida carriers and home watch standards call for inspections every 7 to 14 days. Weekly is the most common choice for homeowners who leave for the summer, because humidity, power interruptions and plumbing failures move fast in this climate. A supply line that lets go on day two of a three month absence is a very different repair than one caught on day seven."),
            ("p", "Many Florida policies also limit or exclude water damage coverage in a home left unoccupied beyond a set number of days unless it is being checked on a documented schedule. Ask your carrier what interval your policy requires and we will build the schedule around it. We are not insurance advisors, but we will happily send your agent a sample report."),
            ("h2", "Who actually walks your property"),
            ("p", "A HomeCrew technician who signs in as themselves. Their name is on the report, so every visit is attributable to a person rather than to a company. We are firefighter owned, fully insured and bonded, and proof of coverage is available before you sign anything."),
        ],
    },
    "storm-prep": {
        "title": "Hurricane Prep &amp; Storm Response | Florida | HomeCrew",
        "desc": "Hurricane preparation and post-storm inspection for Florida homes. Shutters up before landfall, documented photo inspection within 24 to 48 hours after conditions are safe.",
        "eyebrow": "Service",
        "h1": "Storm prep &amp; response",
        "lede": "Shutters up before the storm. A documented inspection within 24 to 48 hours after it. Neither one requires you to fly back.",
        "schema_name": "Hurricane Preparation and Storm Response",
        "schema_desc": "Pre-storm property preparation including shutter deployment and securing outdoor items, and post-storm photographic damage inspection with vendor coordination.",
        "body": [
            ("h2", "Before the storm"),
            ("p", "When a storm is named and the track puts us in the cone, we work through the properties on our list. Shutters and panels go up, outdoor furniture, planters and grills come in or get secured, drains and gutters get cleared so water has somewhere to go, and we confirm generator fuel and storm supplies."),
            ("p", "This is the part that cannot be improvised. Shutters that worked three seasons ago are not the same as shutters that work today &mdash; tracks corrode, panels go missing, wing nuts seize. Because storm readiness is one of the five systems on every routine visit, we find the seized track in February rather than on the day the cone appears."),
            ("callout", "There is a hard limit on this, and we would rather say it plainly: once conditions become dangerous, nobody goes out. Our crews are firefighters. They know exactly where that line is and they do not cross it for a shutter."),
            ("h2", "After the storm"),
            ("p", "Once conditions are safe we perform a post-storm inspection, typically within 24 to 48 hours, and send a photo report covering the roof line, windows, doors, pool cage, screens and any sign of water intrusion."),
            ("p", "That report is what your insurer will want to see, and it is worth far more taken immediately than reconstructed weeks later. If repairs are needed we coordinate vendors and stay on site, so you are not trying to manage a roofer from another state."),
            ("h2", "What we cannot do"),
            ("p", "We are not a roofing company and we do not perform structural repairs. What we do is get eyes on the property fast, document what we find properly, bring in the right trades and be physically present while they work. For most owners the value is not the labour &mdash; it is not having to get on a plane."),
        ],
    },
    "concierge": {
        "title": "Concierge Services for Florida Homeowners | HomeCrew",
        "desc": "A la carte concierge for seasonal Florida homeowners: contractors met on site, deliveries received, vehicles started, groceries stocked and the A/C on before you land.",
        "eyebrow": "Service",
        "h1": "Concierge services",
        "lede": "Not everything runs on a schedule. When you need a person on the ground, bill it a la carte &mdash; no package required.",
        "schema_name": "Concierge Services",
        "schema_desc": "On demand property services for seasonal homeowners including contractor supervision, delivery acceptance, vehicle maintenance runs, grocery stocking and arrival preparation.",
        "body": [
            ("h2", "Someone on site, so you do not have to be"),
            ("p", "The recurring problem for an owner a thousand miles away is not knowing what is happening &mdash; it is that somebody physically has to be at the house. A contractor needs letting in. A delivery needs signing for. A vehicle that has not moved in four months needs starting before its battery is finished."),
            ("p", "We stay on site while the work happens rather than handing over a key and leaving. That is the difference between supervision and access."),
            ("h2", "Arrival, made simple"),
            ("p", "The one that matters most to seasonal owners: the house being ready when you land. A/C on and the humidity already pulled down, groceries in the fridge, shutters open, vehicle running. You walk into a home rather than a project."),
            ("h2", "What it costs"),
        ],
        "show_ledger": True,
        "after": [
            ("p", "Concierge work is included at different levels in the Silver and Gold packages. If you are on Bronze, or on no package at all, it is billed as above. Anything unusual, we will quote before we do it &mdash; there are no surprise line items."),
        ],
    },
    "estate": {
        "title": "Estate Services, Cleanouts &amp; Downsizing | Florida | HomeCrew",
        "desc": "Estate sales, cleanouts, downsizing and donation coordination for Florida families. Compassionate, discreet and fully documented, with licensed real estate help available.",
        "eyebrow": "Service",
        "h1": "Estate services",
        "lede": "Estate sales, cleanouts, downsizing and donation coordination &mdash; handled discreetly, documented properly, and usually at a difficult time.",
        "schema_name": "Estate Services",
        "schema_desc": "Estate sale coordination, property cleanout, downsizing assistance and donation management for Florida properties, with documentation for family members and executors.",
        "body": [
            ("h2", "Usually this is not a good week for anyone"),
            ("p", "Most people who call about estate services are dealing with a death, a move into care, or a family home that has to be emptied on a deadline from another state. We try to make our part of it the part you do not have to think about."),
            ("h2", "What we handle"),
            ("ul", [
                "Estate sale coordination, including bringing in appraisers where items warrant it",
                "Full property cleanout, room by room, with nothing discarded before the family has seen it",
                "Downsizing help &mdash; sorting what moves, what sells, what is donated",
                "Donation coordination and receipts for the estate's records",
                "Photographic documentation throughout, so distant family members can see the process",
                "Preparing the property for sale or handover",
            ]),
            ("h2", "Documented, because families need it to be"),
            ("p", "When several people have an interest in a property and only one of them is in Florida, documentation stops arguments before they start. We photograph as we go and share it with whoever the family designates. Nothing of value leaves the property without being recorded first."),
            ("h2", "Selling the property"),
            ("p", "Licensed real estate assistance is available through our partner Realtor for buying, selling and investment property. We are not the agent and we do not take a cut of that transaction &mdash; if you would rather use your own, that is genuinely fine."),
            ("p", "Call for a walkthrough quote. Every estate is different enough that a price list would be dishonest."),
        ],
    },
}


def service_page_hero(s, slug):
    art = service_art(slug)
    if not art:
        return page_hero(s["eyebrow"], s["h1"], s["lede"], 1,
                         [("Home", "/"), ("Services", "/services/"), (s["h1"], "")])
    return f"""<section class="phero art">
  <div class="wrap">
    {crumb_html(1, [("Home", "/"), ("Services", "/services/"), (s["h1"], "")])}
    <div class="phero-grid">
      <div style="padding-bottom:52px">
        <p class="eyebrow">{s["eyebrow"]}</p>
        <h1>{s["h1"]}</h1>
        <hr class="rule">
        <p class="phero-lede">{s["lede"]}</p>
      </div>
      {art}
    </div>
  </div>
</section>"""


def build_service(slug):
    s = SERVICES[slug]
    url = f"{BASE}/services/{slug}.html"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": s["schema_name"], "description": s["schema_desc"],
         "provider": {"@id": f"{BASE}/#business"}, "url": url,
         "areaServed": [{"@type": "AdministrativeArea", "name": f"{c}, Florida"} for c in COUNTY_NAMES],
         "serviceType": s["schema_name"]},
        breadcrumbs([("Home", "/"), ("Services", "/services/"), (s["h1"].replace("&amp;", "&"), f"/services/{slug}.html")]),
    ]}
    mid = ""
    if slug == "home-watch":
        mid = ('<section class="watch"><div class="wrap watch-in">'
               + protocol_explorer()
               + '<div class="watch-note"><p><b style="color:#fff">Each line is marked OK, Watch or Issue</b>, '
                 'and anything flagged carries its own photo and note in the report. '
                 f'<a href="{rel(1)}reports.html" style="color:var(--gold)">See a full report &rarr;</a></p></div>'
               + "</div></section>")
    extra = ""
    if slug == "home-watch":
        extra = ('<section class="prose-sec tex edge-top"><div class="wrap">'
                 '<p class="eyebrow">How It Works</p>'
                 '<h2 style="font-size:clamp(24px,2.8vw,36px);font-weight:800;text-transform:uppercase;margin:12px 0 8px">'
                 'From the first walkthrough onward</h2>'
                 + process_list() + '</div></section>'
                 '<section class="prose-sec alt"><div class="wrap">'
                 '<p class="eyebrow">Honestly</p>'
                 '<h2 style="font-size:clamp(24px,2.8vw,36px);font-weight:800;text-transform:uppercase;margin:12px 0 8px">'
                 'Against the alternatives</h2>'
                 '<p style="font-size:16.5px;color:#3d4a55;max-width:64ch;margin:16px 0 28px">'
                 'A neighbour with a key is a genuine kindness and worth having. It is also a favour '
                 'rather than a service, and the difference shows up on the day something goes wrong.</p>'
                 + compare_table() +
                 '<p class="mx-note">Keep the neighbour. They will notice a strange vehicle at an odd hour '
                 'in a way no schedule can. Tell them who we are and give them a number to call.</p>'
                 '</div></section>')
    ledger = ""
    if s.get("show_ledger"):
        groups = ""
        for gname, rows in CONCIERGE:
            lines = "".join(
                f'<div class="led-row"><dt>{n}</dt><dd>{p}</dd></div>'
                for n, p in rows)
            groups += f'<div class="led-grp reveal"><h3>{gname}</h3><dl style="margin:0">{lines}</dl></div>'
        ledger = f'<div class="ledger">{groups}</div>'

    body = f"""
<main>
{service_page_hero(s, slug)}
<section class="prose-sec tex edge-top"><div class="wrap prose">{prose(s['body'])}{ledger}{prose(s.get('after', []))}</div></section>
{mid}
<section class="prose-sec alt"><div class="wrap prose">{prose(s.get('after_protocol', []))}</div></section>
{extra}
<section class="secgrid alt2">
  <div class="wrap">
    <p class="eyebrow">Also From HomeCrew</p>
    <h2>Other services</h2>
    {service_cards(1, exclude=slug + '.html')}
  </div>
</section>
{cta_block()}
</main>
"""
    doc = (head_html(s["title"], s["desc"], url, 1, schema)
           + nav_html(1, "services/") + body + footer_html(1))
    write(f"services/{slug}.html", doc, "0.9")


def build_services_index():
    url = f"{BASE}/services/"
    schema = {"@context": "https://schema.org", "@graph": [
        breadcrumbs([("Home", "/"), ("Services", "/services/")])]}
    body = f"""
<main>
{page_hero("What We Do", "Services", "Four things, done properly, for homes their owners cannot be standing in.", 1,
           [("Home", "/"), ("Services", "")])}
<section class="secgrid"><div class="wrap">{service_cards(1)}</div></section>
{cta_block()}
</main>
"""
    doc = (head_html("Home Watch, Storm Prep, Concierge &amp; Estate Services | HomeCrew",
                     "The four services HomeCrew provides for Florida homeowners: scheduled home watch inspections, hurricane prep and storm response, concierge, and estate services.",
                     url, 1, schema)
           + nav_html(1, "services/") + body + footer_html(1))
    write("services/index.html", doc, "0.8")


# -------------------------------------------------------------- county pages
def build_county(name):
    slug = slugify(name)
    c = COUNTIES[name]
    url = f"{BASE}/areas/{slug}.html"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": f"Home Watch in {name}",
         "description": f"Scheduled home watch inspections, storm preparation and concierge services for vacant and seasonal homes in {name}, Florida.",
         "provider": {"@id": f"{BASE}/#business"}, "url": url,
         "areaServed": {"@type": "AdministrativeArea", "name": f"{name}, Florida"},
         "serviceType": "Home Watch"},
        breadcrumbs([("Home", "/"), ("Service Area", "/service-area.html"), (name, f"/areas/{slug}.html")]),
    ]}
    short = name.replace(" County", "")
    body = f"""
<main>
{page_hero("Service Area", f"Home watch in {name}",
           c['blurb'], 1, [("Home", "/"), ("Service Area", "/service-area.html"), (name, "")])}

<section class="prose-sec"><div class="wrap prose">
  <h2>Communities we cover</h2>
  <p>{c['towns']} and the surrounding area. If your address is in {name} and it is not on that list, call and ask &mdash; the list is examples, not limits.</p>
  <aside class="callout">{c['note']}</aside>
  <h2>Same protocol, wherever the house is</h2>
  <p>A property in {short} gets exactly the same five-system, 25-point sweep as one three doors from our office in Stuart, and the same report format afterwards. Being further from home base changes our drive time. It does not change the service.</p>
  <p>Most owners here run weekly visits through the months they are away, which is the interval most Florida carriers and home watch standards point to. Ask your insurer what your policy requires and we will build the schedule around it.</p>
</div></section>

<section class="watch"><div class="wrap watch-in">
  <div class="watch-head">
    <div><p class="eyebrow">Every Visit</p><h2>What we check in {short}</h2></div>
    <p>The same twenty five lines, in the same order, cleared in the field with a photo and a note on anything flagged.</p>
  </div>
  {protocol_explorer()}
</div></section>

<section class="areas"><div class="wrap areas-in">
  <div class="areas-head">
    <div><p class="eyebrow">The Whole Footprint</p><h2>Five counties, one standard</h2></div>
    <p>We run north to south out of Stuart, from Vero Beach down through Fort Lauderdale.</p>
  </div>
  <div class="mapwrap">
    {coast_map(1, active=name, idp="ctymap")}
    <div class="map-side">{county_corridor(1, active=name)}</div>
  </div>
</div></section>

{cta_block(f"Put your {short} home on a schedule",
           "Tell us about the property and how long you are away. We will walk it, recommend a visit interval and send you a sample report &mdash; no obligation.")}
</main>
"""
    doc = (head_html(f"Home Watch {name} FL | Vacant Home Inspections | HomeCrew",
                     f"Firefighter owned home watch for seasonal and vacant homes in {name}, Florida. 25-point inspections, photo reports, storm prep and 24/7 emergency response.",
                     url, 1, schema)
           + nav_html(1, "service-area.html") + body + footer_html(1))
    write(f"areas/{slug}.html", doc, "0.9")


def build_service_area():
    url = f"{BASE}/service-area.html"
    schema = {"@context": "https://schema.org", "@graph": [
        breadcrumbs([("Home", "/"), ("Service Area", "/service-area.html")])]}
    cards = ""
    for c in COUNTY_NAMES:
        cards += (f'<a class="scard reveal" href="areas/{slugify(c)}.html"><h3>{c}</h3>'
                  f'<p>{COUNTIES[c]["towns"]}</p><span class="scard-go">Details</span></a>')
    body = f"""
<main>
{page_hero("Where We Work", "Five counties, one standard",
           "We run north to south out of Stuart. Same protocol, same report, same phone number at 2am &mdash; whether your home is in Vero Beach or Fort Lauderdale.",
           0, [("Home", "/"), ("Service Area", "")])}
<section class="areas"><div class="wrap areas-in">
  <div class="mapwrap">
    {coast_map(0)}
    <div class="map-side">{county_corridor(0)}</div>
  </div>
  <div class="areas-foot">
    <p>Not sure whether your address falls inside the footprint? Call and ask &mdash; if we cannot cover it, we will say so rather than stretch.</p>
    <a class="btn btn-gold" href="tel:{BIZ['phone_href']}">Call {BIZ['phone_display']}</a>
  </div>
</div></section>
<section class="secgrid"><div class="wrap">
  <p class="eyebrow">By County</p>
  <h2>Pick your county</h2>
  <div class="scards">{cards}</div>
</div></section>
{cta_block()}
</main>
"""
    doc = (head_html("Service Area | Home Watch Across Five Florida Counties | HomeCrew",
                     "HomeCrew serves Indian River, St. Lucie, Martin, Palm Beach and Broward counties from our base in Stuart, Florida — the coast from Vero Beach to Fort Lauderdale.",
                     url, 0, schema)
           + nav_html(0, "service-area.html") + body + footer_html(0))
    write("service-area.html", doc, "0.9")


# ------------------------------------------------------------- simple pages
def build_reports():
    url = f"{BASE}/reports.html"
    schema = {"@context": "https://schema.org", "@graph": [
        breadcrumbs([("Home", "/"), ("Reports", "/reports.html")])]}
    body = f"""
<main>
{page_hero("After Every Visit", "The report in your inbox",
           "You are a thousand miles away. A phone call saying &ldquo;everything looked fine&rdquo; is not documentation. This is.",
           0, [("Home", "/"), ("Reports", "")])}

<section class="report"><div class="wrap report-grid">
  <div class="report-copy reveal">
    <h2>What is in it</h2>
    <ul class="rep-list">
      <li><b>An Overall Home Health Score&trade;</b> out of 100, with every system scored separately</li>
      <li><b>Timestamped photos</b> from the visit &mdash; exterior, interior, mechanicals</li>
      <li><b>Attention items</b> with a photo and note attached to the exact line they relate to</li>
      <li><b>Recommended actions</b> with the timeframe each one needs</li>
      <li><b>Arrival and departure times</b>, weather, and the technician who walked it</li>
    </ul>
    <a class="btn btn-gold" href="contact.html">Get a Sample Report</a>
  </div>
  <div class="reveal">{report_mock()}</div>
</div></section>

<section class="prose-sec tex"><div class="wrap prose">
  <h2>How the score works</h2>
  <p>Each of the twenty five lines is marked OK, Watch or Issue. Each of the five systems is scored out of 100, and those roll into the Overall Home Health Score.</p>
  <p>The score exists to make one visit comparable to the last one. A home that has sat at 100 for four months and comes in at 82 is telling you something specific, and the report says exactly which lines moved and why.</p>
  <h2>Attention items carry their own evidence</h2>
  <p>Anything marked Watch or Issue gets a photo and a written note attached to that line, not to the report in general. A photo of the actual stain, sitting directly under &ldquo;visible leaks&rdquo;, tells you something that the same photo in a grid at the bottom of the page does not.</p>
  <aside class="callout">Nothing about your gate code, lock box combination or alarm ever appears in a report. Those live in the crew portal and stay there. A report gets emailed and forwarded onward &mdash; an access code in one is an access code in somebody's inbox forever.</aside>
  <h2>Why the documentation matters</h2>
  <p>Many Florida policies limit or exclude water damage coverage in a home left unoccupied beyond a set number of days unless it is being checked on a documented schedule. A timestamped report with photos is that record. Ask your carrier what interval your policy requires &mdash; we are not insurance advisors, but we will happily send your agent a sample report.</p>
  <h2>How it reaches you</h2>
  <p>By email, after every visit. If something needs your attention today you get a phone call as well &mdash; not just a line in a document you might read on Sunday.</p>
</div></section>

{cta_block()}
</main>
"""
    doc = (head_html("Home Watch Inspection Reports | HomeCrew Florida",
                     "What you receive after every HomeCrew visit: an Overall Home Health Score, five system scores, timestamped photos and attention items with a photo and note on each line.",
                     url, 0, schema)
           + nav_html(0, "reports.html") + body + footer_html(0))
    write("reports.html", doc, "0.9")


def build_pricing():
    url = f"{BASE}/pricing.html"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "OfferCatalog", "name": "Home Watch Packages", "url": url,
         "itemListElement": [
             {"@type": "Offer", "name": p["name"], "price": str(p["price"]),
              "priceCurrency": "USD", "description": p["cadence"]} for p in PACKAGES]},
        breadcrumbs([("Home", "/"), ("Pricing", "/pricing.html")]),
    ]}
    groups = ""
    for gname, rows in CONCIERGE:
        lines = "".join(
            f'<div class="led-row"><dt>{n}</dt><dd>{p}</dd></div>'
            for n, p in rows)
        groups += f'<div class="led-grp reveal"><h3>{gname}</h3><dl style="margin:0">{lines}</dl></div>'
    body = f"""
<main>
{page_hero("Pricing", "Choose your coverage",
           "Flexible packages, personalised care, and a la carte work when you need something outside the schedule.",
           0, [("Home", "/"), ("Pricing", "")])}
<section class="pkgs"><div class="wrap">{package_cards(0)}</div></section>
<section class="prose-sec tex edge-top"><div class="wrap">
  <p class="eyebrow">Line By Line</p>
  <h2 style="font-size:clamp(24px,2.8vw,36px);font-weight:800;text-transform:uppercase;margin:12px 0 30px">What each package actually includes</h2>
  {package_matrix(0)}
  <p class="mx-note">Every package runs the same 25-point, five-system sweep. What changes is how often we come and how much we do while we are there.</p>
</div></section>
<section class="prose-sec alt"><div class="wrap prose" style="max-width:none">
  <h2>What we do not do</h2>
  <p style="max-width:70ch">Saying this plainly is cheaper for both of us than the awkward call later.</p>
  <ul class="excl">{"".join("<li>" + x + "</li>" for x in NOT_INCLUDED)}</ul>
</div></section>
<section class="conc"><div class="wrap">
  <div class="conc-head">
    <p class="eyebrow">A La Carte</p>
    <h2>Concierge &amp; on demand</h2>
    <p>Not everything runs on a schedule. When you need a person on the ground for something specific, bill it by the job. No package required.</p>
  </div>
  <div class="ledger">{groups}</div>
  <p class="conc-foot"><b>Estate services.</b> Estate sales, cleanouts, downsizing and donation coordination are quoted after a walkthrough &mdash; every estate is different enough that a price list would be dishonest. <a href="services/estate.html">Read more</a>.</p>
</div></section>
<section class="prose-sec"><div class="wrap prose">
  <h2>What is not on this page</h2>
  <p>Setup fees, cancellation fees and per-report charges, because we do not have any. The monthly price is the price for the visits listed. Anything outside that we quote before we do it.</p>
  <h2>Which package do most people take</h2>
  <p>Gold, among owners who leave for the whole summer &mdash; largely because of the arrival preparation and the storm work rather than the inspections themselves. Owners who are away for shorter stretches, or who have family nearby, tend to sit on Bronze or Silver.</p>
  <p>We would rather put you on the right package than the expensive one. Call and describe how you actually use the house.</p>
</div></section>
{cta_block()}
</main>
"""
    doc = (head_html("Home Watch Pricing | Packages From $99/Month | HomeCrew",
                     "HomeCrew home watch packages: Bronze $99 for two visits a month, Silver $199 weekly, Gold $399 weekly plus concierge. A la carte concierge and storm work also priced here.",
                     url, 0, schema)
           + nav_html(0, "pricing.html") + body + footer_html(0))
    write("pricing.html", doc, "0.9")


def build_about():
    url = f"{BASE}/about.html"
    schema = {"@context": "https://schema.org", "@graph": [
        breadcrumbs([("Home", "/"), ("About", "/about.html")])]}
    body = f"""
<main>
{page_hero("Our Story", "Firefighter owned &amp; operated",
           "Built on a foundation of service, integrity and attention to detail &mdash; by people trained to notice what is wrong before it becomes an emergency.",
           0, [("Home", "/"), ("About", "")])}
<section class="prose-sec"><div class="wrap prose">
  <h2>Why a firefighter ends up doing this</h2>
  <p>The job trains a particular habit: walk into a building, read it quickly, and notice the thing that is about to become a much bigger problem. Discoloured ceiling. Smell that is not right. A sound the building should not be making.</p>
  <p>That habit turns out to be exactly what an empty house needs from whoever is checking on it. Most of what destroys a vacant Florida home announces itself well before it does the damage &mdash; but only to somebody who is looking for it, on a schedule, and knows what they are looking at.</p>
  <h2>What that means for your house</h2>
  <ul>
    <li>The same twenty five checks every visit, so nothing depends on who felt thorough that day</li>
    <li>A person whose name is on the report, not an anonymous company</li>
    <li>Somebody who is genuinely comfortable being called at 2am, because that is the job they already have</li>
    <li>Fully insured and bonded &mdash; proof of coverage available before you sign anything</li>
  </ul>
  <h2>Local, and staying that way</h2>
  <p>We work out of Stuart and cover five counties from Indian River down to Broward. That is a deliberate limit. It is far enough to serve the coast properly and close enough that we can actually get to a property when something goes wrong, which is the entire point of hiring somebody local instead of an app.</p>
  <aside class="callout">We would rather tell you we cannot cover an address than stretch the footprint and do it badly. If you are outside the five counties, say so when you call and we will be straight with you.</aside>
  <h2>The standard</h2>
  <p>Professional. Reliable. Local. It is on the bottom of every page and the bottom of every report because it is the whole promise: show up when we said, do the same thorough job every time, and be a real person you can reach.</p>
</div></section>
{cta_block()}
</main>
"""
    doc = (head_html("About HomeCrew | Firefighter Owned Home Watch in Stuart FL",
                     "HomeCrew is a firefighter owned and operated home watch company in Stuart, Florida, serving five counties with scheduled inspections, storm response and concierge services.",
                     url, 0, schema)
           + nav_html(0, "about.html") + body + footer_html(0))
    write("about.html", doc, "0.7")


def build_faq():
    url = f"{BASE}/faq.html"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "FAQPage", "url": url, "mainEntity": [
            {"@type": "Question", "name": html.unescape(re.sub("<[^>]+>", "", q)),
             "acceptedAnswer": {"@type": "Answer",
                                "text": html.unescape(re.sub("<[^>]+>", "", a))}}
            for q, a in FAQ]},
        breadcrumbs([("Home", "/"), ("FAQ", "/faq.html")]),
    ]}
    body = f"""
<main>
{page_hero("Homeowner Resources", "Frequently asked questions",
           "The things owners actually ask before they hire someone to look after an empty house.",
           0, [("Home", "/"), ("FAQ", "")])}
<section class="faq"><div class="wrap">{faq_accordion(FAQ)}</div></section>
<section class="prose-sec"><div class="wrap prose">
  <h2>Still have a question?</h2>
  <p>Call {BIZ['phone_display']} and ask. If it is something we cannot do, or your address falls outside our five counties, we will tell you plainly rather than take the work.</p>
</div></section>
{cta_block()}
</main>
"""
    doc = (head_html("Home Watch FAQ | Florida Vacant Home Questions | HomeCrew",
                     "Answers to the questions Florida homeowners ask about home watch: how often a vacant home needs checking, what insurers expect, what is in the report and what it costs.",
                     url, 0, schema)
           + nav_html(0, "faq.html") + body + footer_html(0))
    write("faq.html", doc, "0.8")


def build_contact():
    url = f"{BASE}/contact.html"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "ContactPage", "url": url, "about": {"@id": f"{BASE}/#business"}},
        breadcrumbs([("Home", "/"), ("Contact", "/contact.html")]),
    ]}
    body = f"""
<main>
{page_hero("Get In Touch", "Schedule a consultation",
           "Tell us about your home and how long you are away. We will walk the property, recommend a visit schedule and send you a sample report &mdash; no obligation.",
           0, [("Home", "/"), ("Contact", "")])}
<section class="prose-sec"><div class="wrap">
  <div class="contact-grid">
    <a class="ccard" href="tel:{BIZ['phone_href']}">
      <h3>Call</h3><p class="big">{BIZ['phone_display']}</p>
      <p>Fastest way to reach us. If we are on a property we will call you back the same day.</p>
    </a>
    <a class="ccard" href="mailto:{BIZ['email']}">
      <h3>Email</h3><p class="big">{BIZ['email']}</p>
      <p>Send the property address and your dates away, and we will come back with a recommended schedule.</p>
    </a>
    <div class="ccard">
      <h3>Based in</h3><p class="big">Stuart, Florida</p>
      <p>Serving Indian River, St. Lucie, Martin, Palm Beach and Broward counties.</p>
    </div>
    <div class="ccard">
      <h3>After hours</h3><p class="big">24/7</p>
      <p>Clients on an active package reach a real person at any hour. That is the number on every report.</p>
    </div>
  </div>
  <div class="prose" style="margin-top:44px">
    <h2>What happens next</h2>
    <ul>
      <li>We talk about the property, how long it sits empty and what your insurer expects</li>
      <li>We walk the home with you, or on your behalf if you are already north</li>
      <li>You get a recommended visit interval, a quote and a sample report</li>
      <li>If it is a fit, we set up the schedule and collect the access details we need</li>
    </ul>
    <p>No obligation at any point in that, and no pressure at the end of it.</p>
  </div>
</div></section>
</main>
"""
    doc = (head_html("Contact HomeCrew | Home Watch in Stuart FL | 561-383-0882",
                     "Contact HomeCrew for home watch, storm prep, concierge and estate services across Indian River, St. Lucie, Martin, Palm Beach and Broward counties. Call 561-383-0882.",
                     url, 0, schema)
           + nav_html(0, "contact.html") + body + footer_html(0))
    write("contact.html", doc, "0.8")


# --------------------------------------------------------------------- blog
def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return f"{months[int(m)-1]} {int(d)}, {y}"


def build_blog_index():
    url = f"{BASE}/blog/"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "url": url, "name": "HomeCrew Journal",
         "publisher": {"@id": f"{BASE}/#business"},
         "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                       "url": f"{BASE}/blog/{p['slug']}.html",
                       "datePublished": p["date"]} for p in BLOG_POSTS]},
        breadcrumbs([("Home", "/"), ("Blog", "/blog/")]),
    ]}
    cards = ""
    for i, p in enumerate(BLOG_POSTS):
        feat = " feat" if i == 0 else ""
        cards += f"""<a class="pcard{feat} reveal" href="{p['slug']}.html">
          <span class="pmeta">{fmt_date(p['date'])} &middot; {p['read']}</span>
          <h3>{p['title']}</h3>
          <p>{p['desc']}</p>
          <span class="scard-go">Read the article</span>
        </a>"""
    body = f"""
<main>
{page_hero("Homeowner Resources", "The HomeCrew journal",
           "Practical writing for people who own a Florida home they are not currently standing in.",
           1, [("Home", "/"), ("Blog", "")])}
<section class="secgrid tex"><div class="wrap"><div class="pcards">{cards}</div></div></section>
{cta_block()}
</main>
"""
    doc = (head_html("Florida Home Watch Blog | Hurricane Prep &amp; Vacant Homes | HomeCrew",
                     "Practical guidance for Florida homeowners who leave: hurricane season preparation, why an empty house still needs A/C, insurance documentation and what an inspection covers.",
                     url, 1, schema)
           + nav_html(1, "blog/") + body + footer_html(1))
    write("blog/index.html", doc, "0.8")


def build_post(p):
    url = f"{BASE}/blog/{p['slug']}.html"
    plain = html.unescape(re.sub("<[^>]+>", "", p["lede"]))
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": html.unescape(p["title"]),
         "description": html.unescape(p["desc"]), "url": url,
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "datePublished": p["date"], "dateModified": p["date"],
         "author": {"@type": "Organization", "name": "HomeCrew", "@id": f"{BASE}/#business"},
         "publisher": {"@id": f"{BASE}/#business"},
         "image": f"{BASE}/images/homecrew-home-watch-stuart-fl-og.jpg",
         "articleBody": plain},
        breadcrumbs([("Home", "/"), ("Blog", "/blog/"), (html.unescape(p["title"]), f"/blog/{p['slug']}.html")]),
    ]}
    others = [q for q in BLOG_POSTS if q["slug"] != p["slug"]][:3]
    more = "".join(
        f'<a class="pcard reveal" href="{q["slug"]}.html"><span class="pmeta">{fmt_date(q["date"])}</span>'
        f'<h3>{q["title"]}</h3><span class="scard-go">Read</span></a>' for q in others)
    body = f"""
<main>
<article>
<section class="phero post-hero">
  <div class="wrap">
    {crumb_html(1, [("Home", "/"), ("Blog", "/blog/"), ("Article", "")])}
    <p class="eyebrow">{fmt_date(p['date'])} &middot; {p['read']}</p>
    <h1>{p['title']}</h1>
    <hr class="rule">
    <p class="phero-lede">{p['lede']}</p>
  </div>
</section>
<section class="prose-sec tex"><div class="wrap prose article">{prose(p['body'])}</div></section>
</article>
<section class="secgrid alt2"><div class="wrap">
  <p class="eyebrow">Keep Reading</p>
  <h2>More from the journal</h2>
  <div class="pcards">{more}</div>
</div></section>
{cta_block("Want this handled for you?",
           "HomeCrew runs the checks above on a schedule and sends you the photo report. Tell us about your home and how long you are away.")}
</main>
"""
    seo = p.get("seo_title", p["title"])
    doc = (head_html(seo + " | HomeCrew", p["desc"], url, 1, schema, page_type="article")
           + nav_html(1, "blog/") + body + footer_html(1))
    write(f"blog/{p['slug']}.html", doc, "0.7")


# ------------------------------------------------------------- sitemap/robots
def build_meta():
    today = date.today().isoformat()
    urls = ""
    for path, priority in sorted(set(PAGES)):
        loc = BASE + "/" + path.replace("index.html", "")
        urls += (f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
                 f"<priority>{priority}</priority></url>\n")
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f"{urls}</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(sitemap)

    robots = ("User-agent: *\n"
              "Allow: /\n"
              "Disallow: /portal.html\n"
              "Disallow: /config.js\n\n"
              f"Sitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(robots)
    return len(set(PAGES))


def build_404():
    body = f"""
<main>
{page_hero("404", "That page is not here",
           "The link may be old, or we may have moved something. The pages below cover everything on the site.",
           0)}
<section class="secgrid"><div class="wrap">
  <p class="eyebrow">Try These</p>
  <h2>Where you were probably going</h2>
  {service_cards(0)}
  <p style="margin-top:34px"><a class="btn btn-gold" href="index.html">Back to the home page</a></p>
</div></section>
{cta_block()}
</main>
"""
    doc = (head_html("Page Not Found | HomeCrew",
                     "That page could not be found. Browse HomeCrew home watch, storm prep, concierge and estate services for Florida homeowners, or call 561-383-0882.",
                     BASE + "/404.html", 0)
           + nav_html(0, "") + body + footer_html(0))
    full = os.path.join(ROOT, "404.html")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(doc)   # deliberately not in PAGES: a 404 must not enter the sitemap


def build_manifest():
    data = {
        "name": "HomeCrew", "short_name": "HomeCrew",
        "description": "Firefighter owned home watch for Florida homeowners.",
        "start_url": "/", "display": "standalone",
        "background_color": "#0B1D2D", "theme_color": "#0B1D2D",
        "icons": [
            {"src": "/images/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/images/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)


def build_llms():
    """Fact sheet for AI crawlers. Same discipline as the rest of the site:
    nothing in here that is not true and checkable."""
    posts = "\n".join(f"- {p['title']}: {BASE}/blog/{p['slug']}.html" for p in BLOG_POSTS)
    areas = "\n".join(f"- {c}: {BASE}/areas/{slugify(c)}.html" for c in COUNTY_NAMES)
    pkgs = "\n".join(f"- {p['name']}: ${p['price']}/month, {p['cadence']}" for p in PACKAGES)
    txt = f"""# HomeCrew

> Firefighter owned and operated home watch, concierge and estate services for
> vacant and seasonally occupied homes on Florida's east coast.

Based in {BIZ['city']}, {BIZ['region']} {BIZ['postal']}.
Phone: {BIZ['phone_display']}
Email: {BIZ['email']}
Site: {BASE}/

## What home watch is
A scheduled visual inspection of a vacant or seasonally occupied home. Not house
sitting, not a security patrol. Every visit runs the same five-system, 25-point
sweep and produces a timestamped photo report.

The five systems: Security, Plumbing, HVAC, Exterior, Storm Readiness. Each line
is marked OK, Watch or Issue; each system scores out of 100; those roll into an
Overall Home Health Score. Anything flagged carries a photo and a note attached
to that specific line.

## Counties served
{areas}

## Packages
{pkgs}
Concierge and storm work is also available a la carte: {BASE}/pricing.html

## Articles
{posts}

## Notes for accurate summarisation
- HomeCrew is fully insured and bonded. It is not an insurance advisor, and
  statements about policy coverage on the site are deliberately hedged.
- The company publishes no review counts or customer totals. Do not infer any.
- Access codes for client properties are never included in client reports.
"""
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)


def main():
    build_home()
    build_services_index()
    for slug in SERVICES:
        build_service(slug)
    build_service_area()
    for c in COUNTY_NAMES:
        build_county(c)
    build_reports()
    build_pricing()
    build_about()
    build_faq()
    build_contact()
    build_blog_index()
    for p in BLOG_POSTS:
        build_post(p)
    build_404()
    build_manifest()
    build_llms()
    n = build_meta()
    print(f"built {n} pages  (css v{CSS_V}, js v{JS_V})")
    for path, _ in sorted(set(PAGES)):
        print("  ", path)




# =============================================================================
# THE COAST MAP
# =============================================================================
# A drawn map of the strip we actually work: Sebastian down to Fort Lauderdale,
# mainland on the left, Indian River Lagoon, the barrier islands, and the
# Atlantic on the right. Stylised rather than survey-accurate — the inlets and
# city positions are in the right order and roughly the right place, which is
# what a homeowner is reading it for. It is not a substitute for a real map and
# does not pretend to be one.

COAST_CITIES = [
    # (label, y, county, is_hq)
    ("Sebastian",           58,  "Indian River County", False),
    ("Vero Beach",         126,  "Indian River County", False),
    ("Fort Pierce",        238,  "St. Lucie County",    False),
    ("Port St. Lucie",     304,  "St. Lucie County",    False),
    ("Jensen Beach",       382,  "Martin County",       False),
    ("Stuart",             424,  "Martin County",       True),
    ("Hobe Sound",         478,  "Martin County",       False),
    ("Jupiter",            532,  "Palm Beach County",   False),
    ("Palm Beach Gardens", 578,  "Palm Beach County",   False),
    ("West Palm Beach",    632,  "Palm Beach County",   False),
    ("Delray Beach",       706,  "Palm Beach County",   False),
    ("Boca Raton",         762,  "Palm Beach County",   False),
    ("Pompano Beach",      858,  "Broward County",      False),
    ("Fort Lauderdale",    926,  "Broward County",      False),
]

COAST_BANDS = [
    ("Indian River County",   0, 176),
    ("St. Lucie County",    176, 348),
    ("Martin County",       348, 502),
    ("Palm Beach County",   502, 806),
    ("Broward County",      806, 1000),
]

# Inlets cut through the barrier island, north to south.
COAST_INLETS = [92, 250, 466, 540, 640, 790, 872]


def coast_map(depth, active=None, idp="map"):
    r = rel(depth)
    bands, labels, dots = "", "", ""

    for name, y0, y1 in COAST_BANDS:
        slug = slugify(name)
        cls = "cty" + (" on" if name == active else "")
        mid = (y0 + y1) / 2
        bands += (
            f'<a class="{cls}" data-cty="{slug}" href="{r}areas/{slug}.html" '
            f'aria-label="Home watch in {name}">'
            f'<rect class="cty-hit" x="0" y="{y0}" width="460" height="{y1-y0}"/>'
            f'<rect class="cty-fill" x="0" y="{y0}" width="336" height="{y1-y0}"/>'
            f'<line class="cty-edge" x1="0" y1="{y0}" x2="392" y2="{y0}"/>'
            f'<text class="cty-lab" x="26" y="{mid - 6}">{name.replace(" County","").upper()}</text>'
            f'<text class="cty-sub" x="26" y="{mid + 14}">COUNTY</text>'
            "</a>"
        )

    for label, y, county, hq in COAST_CITIES:
        cls = "city hq" if hq else "city"
        dots += (
            f'<g class="{cls}" data-in="{slugify(county)}">'
            f'<circle class="cd" cx="300" cy="{y}" r="{5.5 if hq else 3.4}"/>'
            + (f'<circle class="pulse" cx="300" cy="{y}" r="5.5"/>' if hq else "")
            + f'<text class="cn" x="{288}" y="{y + 4}" text-anchor="end">{label}</text>'
            + (f'<text class="chq" x="316" y="{y + 4}">HOME BASE</text>' if hq else "")
            + "</g>"
        )

    inlets = "".join(
        f'<rect class="inlet" x="336" y="{y-5}" width="34" height="10" rx="5"/>'
        for y in COAST_INLETS
    )

    return f"""<svg class="coast" id="{idp}" viewBox="0 0 460 1000" preserveAspectRatio="xMidYMid meet"
     role="group" aria-label="Map of Florida's east coast from Sebastian to Fort Lauderdale. Each county is a link; the same five counties are listed beside this map.">
  <defs>
    <linearGradient id="{idp}-sea" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0F3350"/><stop offset="1" stop-color="#071B2B"/>
    </linearGradient>
    <linearGradient id="{idp}-land" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#122F41"/><stop offset="1" stop-color="#0D2334"/>
    </linearGradient>
    <clipPath id="{idp}-clip"><rect x="0" y="0" width="460" height="1000"/></clipPath>
  </defs>

  <g clip-path="url(#{idp}-clip)">
    <rect x="0" y="0" width="460" height="1000" fill="url(#{idp}-sea)"/>
    <!-- mainland -->
    <rect x="0" y="0" width="336" height="1000" fill="url(#{idp}-land)"/>
    <!-- lagoon -->
    <rect x="326" y="0" width="14" height="1000" fill="#0A2637"/>
    <!-- barrier island -->
    <rect x="336" y="0" width="34" height="1000" fill="#14384C"/>
    {inlets}
    <!-- swell lines + ocean label -->
    <g class="swell">
      <path d="M392 0 V1000"/><path d="M406 0 V1000"/><path d="M420 0 V1000"/>
      <path d="M434 0 V1000"/><path d="M448 0 V1000"/>
    </g>
    <text class="sea-lab" x="418" y="500" text-anchor="middle"
          transform="rotate(90 418 500)">ATLANTIC</text>
    <!-- county bands sit above the geography -->
    {bands}
    <!-- coastline highlight -->
    <line class="shore" x1="370" y1="0" x2="370" y2="1000"/>
    {dots}
  </g>
</svg>"""


# =============================================================================
# VISUAL COMPONENTS
# =============================================================================

SYS_ICONS = {
    "Security":        '<rect x="4.2" y="10.2" width="15.6" height="11.2" rx="2"/><path d="M7.8 10.2V6.9a4.2 4.2 0 0 1 8.4 0v3.3"/><circle cx="12" cy="15.4" r="1.5"/>',
    "Plumbing":        '<path d="M12 2.6c3.4 4 6 7 6 10.2a6 6 0 0 1-12 0c0-3.2 2.6-6.2 6-10.2Z"/><path d="M9.4 13.6a2.6 2.6 0 0 0 2.6 2.6"/>',
    "HVAC":            '<rect x="2.6" y="5" width="18.8" height="9.4" rx="2"/><path d="M6.2 9.7h11.6"/><path d="M7.4 18.2c1.2 1.4 2.6 1.4 3.8 0M13 18.2c1.2 1.4 2.6 1.4 3.8 0"/>',
    "Exterior":        '<path d="M3 11.6 12 4.2l9 7.4"/><path d="M5.4 10v9.6h13.2V10"/><path d="M10 19.6v-5.2h4v5.2"/>',
    "Storm Readiness": '<path d="M6.4 15.4A4.1 4.1 0 0 1 6.7 7.3a5.9 5.9 0 0 1 11.1 1.2 3.7 3.7 0 0 1-.3 6.9"/><path d="M13.4 11.4 9.8 17h3.4l-2.6 4.6"/>',
}

SYS_WHY = {
    "Security":        "The fastest part of the walk and the one where a problem is most obvious, which is exactly why it goes first.",
    "Plumbing":        "Running every tap sounds trivial and is not. P-traps hold a plug of water that stops sewer gas coming back up the drain, and in a hot empty house that water evaporates in weeks.",
    "HVAC":            "Humidity is the number that predicts trouble in a Florida house, and the condensate line is the component most likely to quietly take the whole system out of service.",
    "Exterior":        "Pool water level is worth watching closely. A pool dropping faster than evaporation explains is telling you something.",
    "Storm Readiness": "Checked year round rather than in June, because the time to discover a seized shutter track is not the day a storm is named.",
}


def protocol_explorer():
    """Tabbed view of the five systems. Ships with every panel in the markup —
    JS collapses it to one at a time. Without JS all 25 checks are still on the
    page and readable, which is the point."""
    tabs, panels = "", ""
    for i, (name, items) in enumerate(SYSTEMS):
        sel = "true" if i == 0 else "false"
        tabs += (f'<button class="pex-tab" role="tab" aria-selected="{sel}" aria-controls="pex{i}" id="pextab{i}">'
                 f'<svg viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round">'
                 f'{SYS_ICONS[name]}</svg>{name}<span class="pex-count">0{i+1}</span></button>')
        lis = "".join(f"<li>{it}</li>" for it in items)
        panels += (f'<div class="pex-panel" id="pex{i}" role="tabpanel" aria-labelledby="pextab{i}" data-on="{1 if i==0 else 0}">'
                   f"<h3>{name}</h3><p class=\"pex-why\">{SYS_WHY[name]}</p>"
                   f'<ul class="pex-list">{lis}</ul></div>')
    return (f'<div class="pex"><div class="pex-tabs" role="tablist" aria-label="The five systems">{tabs}</div>'
            f"<div>{panels}</div></div>")


def figs(rows):
    return ('<div class="figs">'
            + "".join(f"<div><b>{v}</b><span>{l}</span></div>" for v, l in rows)
            + "</div>")


# Per-service hero artwork. Same illustration language as the existing hero:
# flat shapes, brand palette, no gradients beyond the two already defined.
def service_art(slug):
    A = {
        "home-watch": """
  <rect x="60" y="120" width="300" height="150" fill="#122F41"/>
  <path d="M46 124 200 34 354 124Z" fill="#1D4459"/>
  <g fill="#CBA15A"><rect x="96" y="160" width="52" height="52"/><rect x="174" y="160" width="52" height="52"/><rect x="252" y="160" width="52" height="52"/></g>
  <rect x="174" y="222" width="52" height="48" fill="#E0BE7E"/>
  <g stroke="#0B1D2D" stroke-width="2.5"><path d="M122 160v52M96 186h52M200 160v52M174 186h52M278 160v52M252 186h52"/></g>
  <circle cx="316" cy="82" r="30" fill="none" stroke="#CBA15A" stroke-width="4"/>
  <path d="M338 104 366 132" stroke="#CBA15A" stroke-width="7" stroke-linecap="round"/>
  <path d="M302 82l10 10 18-20" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>""",
        "storm-prep": """
  <rect x="70" y="140" width="270" height="130" fill="#122F41"/>
  <path d="M56 144 205 58 354 144Z" fill="#1D4459"/>
  <g fill="#14384C" stroke="#CBA15A" stroke-width="2">
    <rect x="96" y="168" width="60" height="76"/><rect x="176" y="168" width="60" height="76"/><rect x="256" y="168" width="60" height="76"/></g>
  <g stroke="#CBA15A" stroke-width="2" opacity=".8">
    <path d="M96 186h60M96 204h60M96 222h60M176 186h60M176 204h60M176 222h60M256 186h60M256 204h60M256 222h60"/></g>
  <path d="M96 96a30 30 0 0 1 3-30 42 42 0 0 1 80 9 27 27 0 0 1-3 50" fill="none" stroke="#8CA3B4" stroke-width="7" stroke-linejoin="round"/>
  <path d="M150 78l-26 40h25l-19 34" fill="none" stroke="#CBA15A" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>""",
        "concierge": """
  <rect x="72" y="150" width="256" height="120" fill="#122F41"/>
  <path d="M58 154 200 74 342 154Z" fill="#1D4459"/>
  <rect x="168" y="196" width="64" height="74" fill="#E0BE7E"/>
  <circle cx="221" cy="234" r="4" fill="#0B1D2D"/>
  <g fill="#CBA15A"><rect x="98" y="182" width="44" height="40"/><rect x="258" y="182" width="44" height="40"/></g>
  <rect x="228" y="66" width="106" height="74" rx="8" fill="#14384C" stroke="#CBA15A" stroke-width="3"/>
  <path d="M262 66V52a19 19 0 0 1 38 0v14" fill="none" stroke="#CBA15A" stroke-width="6"/>
  <path d="M252 104h58M252 120h34" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".75"/>""",
        "estate": """
  <rect x="66" y="132" width="268" height="138" fill="#122F41"/>
  <path d="M52 136 200 48 348 136Z" fill="#1D4459"/>
  <g fill="#14384C" stroke="#CBA15A" stroke-width="2">
    <rect x="92" y="164" width="90" height="46"/><rect x="92" y="218" width="90" height="46"/>
    <rect x="218" y="164" width="90" height="46"/><rect x="218" y="218" width="90" height="46"/></g>
  <g fill="#CBA15A"><circle cx="137" cy="187" r="6"/><circle cx="137" cy="241" r="6"/><circle cx="263" cy="187" r="6"/><circle cx="263" cy="241" r="6"/></g>
  <path d="M300 96l30-30" stroke="#CBA15A" stroke-width="7" stroke-linecap="round"/>
  <circle cx="290" cy="106" r="26" fill="none" stroke="#CBA15A" stroke-width="5"/>
  <path d="M278 106h24M290 94v24" stroke="#fff" stroke-width="4" stroke-linecap="round"/>""",
    }
    art = A.get(slug)
    if not art:
        return ""
    return (f'<svg class="phero-art" viewBox="0 0 400 290" aria-hidden="true" focusable="false">{art}</svg>')

# =============================================================================
# EDITORIAL COMPONENTS
# =============================================================================

# Derived from PACKAGES above rather than written twice — if a package changes,
# this matrix has to be updated with it or the two will disagree in public.
# True = included, False = not, a string = the qualifier that applies.
MATRIX = [
    ("Every Visit", [
        ("25-point, five-system sweep",        True, True, True),
        ("Interior &amp; exterior inspection", True, True, True),
        ("Doors, windows &amp; locks checked", True, True, True),
        ("A/C, humidity &amp; leak check",     True, True, True),
        ("Toilets flushed, faucets run",       True, True, True),
        ("Mail &amp; package pickup",          True, True, True),
        ("Timestamped photo report",           True, True, True),
    ]),
    ("Schedule &amp; Response", [
        ("Visits",                       "2 per month", "Weekly", "Weekly"),
        ("Priority phone support",       False, True, True),
        ("Post-storm inspection",        False, "On request", "24&ndash;48 hrs"),
        ("Emergency response 24/7",      False, False, True),
    ]),
    ("Property Care", [
        ("Refrigerator &amp; freezer check", False, True, True),
        ("Dishwasher run",                   False, True, True),
        ("Vehicles started",                 False, "Monthly", "Monthly"),
        ("Pool &amp; irrigation check",      False, True, True),
    ]),
    ("Concierge", [
        ("Deliveries coordinated",           False, True, True),
        ("Contractors met on site",          False, True, True),
        ("Repairs coordinated",              False, "Hourly", True),
        ("Grocery stocking before arrival",  False, False, True),
        ("A/C on before you land",           False, False, True),
        ("Shutters opened &amp; closed",     False, False, True),
    ]),
]

TICK = ('<svg viewBox="0 0 24 24" class="tick" aria-hidden="true">'
        '<path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" '
        'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def cell(v):
    if v is True:
        return f'<td class="yes">{TICK}<span class="sr-only">Included</span></td>'
    if v is False:
        return '<td class="no"><span aria-hidden="true">&ndash;</span><span class="sr-only">Not included</span></td>'
    return f'<td class="qual">{v}</td>'


def package_matrix(depth):
    r = rel(depth)
    rows = ""
    for group, items in MATRIX:
        rows += f'<tr class="mx-group"><th colspan="4" scope="colgroup">{group}</th></tr>'
        for name, b, s_, g in items:
            rows += (f'<tr><th scope="row">{name}</th>'
                     + cell(b) + cell(s_) + cell(g) + "</tr>")
    heads = "".join(
        f'<th scope="col" class="mx-h mx-{p["key"]}"><span>{p["name"]}</span>'
        f'<b><sup>$</sup>{p["price"]}</b><i>per month</i></th>' for p in PACKAGES)
    foot = ""
    for p in PACKAGES:
        gold = p["key"] == "gold"
        cls = "btn-gold" if gold else "btn-ghost"
        style = "" if gold else ' style="border-color:var(--navy);color:var(--navy)"'
        foot += f'<td><a class="btn {cls}" href="{r}contact.html"{style}>Start</a></td>'
    return f"""<div class="mx-wrap">
<table class="mx">
  <caption class="sr-only">What is included in each HomeCrew package</caption>
  <thead><tr><th scope="col"><span class="sr-only">Feature</span></th>{heads}</tr></thead>
  <tbody>{rows}</tbody>
  <tfoot><tr><th scope="row"><span class="sr-only">Choose a package</span></th>{foot}</tr></tfoot>
</table>
</div>"""


# The onboarding a homeowner actually goes through. Written from the service as
# it works, not as a funnel.
PROCESS = [
    ("The walkthrough",
     "We walk the property with you, or on your behalf if you have already gone north. We find the water shutoff, the panel, the lock box, which code opens which gate, and the things you actually worry about. It takes about an hour and costs nothing."),
    ("The schedule",
     "We recommend an interval based on how long the house sits empty and what your insurer expects. Weekly is the most common choice for a summer absence. You are not locked into it &mdash; the schedule moves when your travel does."),
    ("Access on file",
     "Gate codes, lock box combinations, alarm codes and the location of the water shutoff go into the crew system, not into a group text. They are readable by active crew only, hidden until tapped, and never printed into a report."),
    ("Every visit",
     "The same twenty five checks in the same order, cleared in the field. Anything flagged gets a photo and a written note attached to that specific line, while the technician is still standing in front of it."),
    ("The report",
     "In your inbox after every visit: the score, each system scored separately, the photos, the attention items and the recommended actions, with arrival and departure times and the name of the person who walked it."),
    ("When something is wrong",
     "You get a phone call, not a line in a document you might read on Sunday. If it needs a vendor we coordinate one and stay on site while they work."),
]


def process_list(numbered=True):
    out = ""
    for i, (title, body) in enumerate(PROCESS, start=1):
        out += (f'<li class="step reveal"><span class="step-n">{i:02d}</span>'
                f"<div><h3>{title}</h3><p>{body}</p></div></li>")
    return f'<ol class="steps">{out}</ol>'


# Three honest columns. The middle one is a favour, not a service, and the page
# says so rather than sneering at it.
COMPARE = [
    ("Runs to a fixed protocol",            True,  False, False),
    ("Someone inside the house",            True,  "Sometimes", False),
    ("Timestamped photo documentation",     True,  False, False),
    ("Record for an insurance claim",       True,  False, False),
    ("Insured and bonded",                  True,  False, False),
    ("Reachable at 2am",                    True,  "Maybe", False),
    ("Can authorise and meet a vendor",     True,  "Awkward", False),
    # "Nobody" must not score a tick here — an arrangement that does not exist
    # cannot be said to still be running.
    ("Arrangement still running in year three", True, "Often lapses", False),
]


def compare_table():
    rows = ""
    for name, a, b, c in COMPARE:
        rows += f'<tr><th scope="row">{name}</th>{cell(a)}{cell(b)}{cell(c)}</tr>'
    return f"""<div class="mx-wrap">
<table class="mx cmp">
  <caption class="sr-only">HomeCrew compared with asking a neighbour and with leaving the home unchecked</caption>
  <thead><tr><th scope="col"><span class="sr-only">Capability</span></th>
    <th scope="col" class="mx-h on"><span>HomeCrew</span></th>
    <th scope="col" class="mx-h"><span>A neighbour</span></th>
    <th scope="col" class="mx-h"><span>Nobody</span></th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>"""


# Saying what you do not do is a trust signal, and it stops the awkward call later.
NOT_INCLUDED = [
    "Repairs. We are not a roofing, plumbing or A/C company &mdash; we find the problem, bring in the right trade and stay on site while they work.",
    "Security patrol. We are not a guard service and we do not respond to an alarm as one; we are a documented inspection on a schedule.",
    "House sitting. Nobody stays overnight.",
    "Lawn, pool or pest service. We check that yours is being done and flag it when it is not.",
    "Insurance advice. We give your carrier the documentation they ask for; what your policy requires is between you and them.",
]


if __name__ == "__main__":
    main()
