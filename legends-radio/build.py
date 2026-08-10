#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LEGENDS RADIO 100.3 FM — static site generator (redesign concept).
Single source of truth: edit the content below, then `python3 build.py`.

Aesthetic: Art Deco / supper-club glamour for the Great American Songbook.
Everything is self-contained (self-hosted fonts, hand-built CSS/JS, no trackers
beyond nothing). SEO: unique title/desc/canonical, OG/Twitter, JSON-LD
(RadioStation + Person + ItemList + Breadcrumbs), sitemap, robots, manifest.

Facts are grounded in public sources (WLML-FM / legendsradio.com). Programming
blocks that aren't publicly confirmed are descriptive music blocks, not invented
hosted shows — see OWNER TO-DOS at the bottom of this file.
"""
import hashlib, json, os, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://www.legendsradio.com"   # canonical production home (see OWNER TO-DOS)
# Path the site is served from. As a subfolder deploy it MUST be "/legends-radio/" so
# relative assets resolve even when the URL has no trailing slash (Vercel trailingSlash:false
# strips it). For a root-domain deploy (legendsradio.com) set this to "/" and rebuild.
SITE_BASE_PATH = "/legends-radio/"
BUILT = datetime.date.today().isoformat()

# ---------------------------------------------------------------------------
# STATION
# ---------------------------------------------------------------------------
STATION = {
    "name": "Legends Radio 100.3 FM",
    "short": "Legends Radio",
    "call": "WLML-FM",
    "freq": "100.3",
    "slogan": "Where Legendary Music Lives",
    "flourish": "The One and Only…",
    "entertainment": "A Dick Robinson Entertainment Station",
    "heard": "Heard at 100.3 in Palm Beach County",
    "tagline": "The Great American Songbook — live & local from the Palm Beaches.",
    "market": "West Palm Beach / the Palm Beaches",
    "license_city": "Lake Park, FL",
    "founded": "2014",
    "founded_iso": "2014-02-22",
    "parent": "Robinson Entertainment, LLC",
    "phone": "561-469-6700",
    "phone_e164": "+15614696700",
    "request": "561-685-9565",
    "request_e164": "+15616859565",
    "email": "info@legendsradio.com",
    "addr_street": "760 US Highway 1, Suite 102",
    "addr_city": "North Palm Beach",
    "addr_region": "FL",
    "addr_zip": "33408",
    "geo_lat": 26.8172,
    "geo_lng": -80.0561,
    "stream": "https://ice3.securenetsystems.net/WLML",
    "popout": "https://legendsradio.com/listen-live/",
    "instagram": "https://www.instagram.com/legendsradio100.3/",
    "facebook": "https://www.facebook.com/legendsradio",
    "twitter": "https://twitter.com/Legends_Radio",
    "soundcloud": "https://soundcloud.com/legendsradio",
    "tunein": "https://tunein.com/radio/Legends-Radio-1003-s218849/",
    "app_ios": "https://apps.apple.com/us/app/legends-radio-100-3-fm/id6575388465",
    "app_android": "https://play.google.com/store/apps/details?id=com.wlml1.player",
    "eventbrite": "https://www.eventbrite.com/o/8860760162",
    "venue": "Downtown Abacoa Amphitheater · 1267 Main St, Jupiter, FL 33458",
    "spgas": "Society for the Preservation of the Great American Songbook",
}
AREA_SERVED = ["West Palm Beach", "Palm Beach", "North Palm Beach", "Palm Beach Gardens",
               "Jupiter", "Lake Park", "Juno Beach", "Wellington", "Boca Raton", "Stuart"]

# Artists (Great American Songbook staples the station is documented to play).
ARTISTS = ["Frank Sinatra", "Ella Fitzgerald", "Tony Bennett", "Dean Martin", "Nat King Cole",
           "Michael Bublé", "Diana Krall", "Harry Connick Jr.", "Barbra Streisand", "Rod Stewart",
           "Vic Damone", "Jack Jones", "Bobby Darin", "Peggy Lee", "Sammy Davis Jr.",
           "Michael Feinstein", "Sarah Vaughan", "Nancy Wilson"]

# ---------------------------------------------------------------------------
# HOSTS  (confirmed on-air talent + roles; bios use documented facts only)
# ---------------------------------------------------------------------------
HOSTS = [
    {
        "slug": "jill-rich-switzer", "name": "Jill & Rich Switzer", "mono": "J&R",
        "role": "Weekday Mornings", "show": "The Morning Lounge", "slot": "Weekdays · 6–10 AM",
        "photo": "assets/hosts/jill-rich.jpg",
        "persons": ["Jill Switzer", "Rich Switzer"],
        "bio": "South Florida's first couple of the Songbook open every weekday. Jill is one of "
               "the region's most sought-after vocalists — a songwriter and published author — while "
               "Rich is a gifted pianist and composer. Together they also perform their acclaimed "
               "cabaret, <em>Supper Club with Jill &amp; Rich</em>.",
    },
    {
        "slug": "mike-mcgann", "name": "Mike McGann", "mono": "MM",
        "role": "Weekday Middays", "show": "Middays with Mike McGann", "slot": "Weekdays · 10 AM – 2 PM",
        "photo": "assets/hosts/mike-mcgann.jpg",
        "persons": ["Mike McGann"],
        "bio": "Mike carries the middays on Legends 100.3, keeping the Great American Songbook "
               "playing straight through the middle of the day.",
    },
    {
        "slug": "steve-ketelaar", "name": "Steve Ketelaar", "mono": "SK",
        "role": "Weekday Afternoons", "show": "Legends Afternoons with Steve Ketelaar",
        "slot": "Weekdays · 2–7 PM",
        "photo": "assets/hosts/steve-ketelaar.webp",
        "persons": ["Steve Ketelaar"],
        "bio": "Steve rides the afternoon drive on Legends 100.3, carrying the standards from "
               "mid-afternoon through the evening commute.",
    },
    {
        "slug": "alex-donner", "name": "Alex Donner", "mono": "AD",
        "role": "Weekday Evenings", "show": "Evenings with Alex Donner", "slot": "Weekdays · 7–9 PM",
        "photo": "assets/hosts/alex-donner.jpg",
        "persons": ["Alex Donner"],
        "bio": "Alex hosts the evening hours on Legends 100.3 — supper-club standards for the "
               "front end of the night.",
    },
    {
        "slug": "bob-merrill", "name": "Bob Merrill", "mono": "BM",
        "role": "Weeknights & Sundays", "show": "Legends After Dark", "slot": "Weeknights · 9–11 PM",
        "photo": "assets/hosts/bob-merrill.jpg",
        "persons": ["Bob Merrill"],
        "bio": "Bob hosts <em>Legends After Dark</em> on weeknights and returns for the "
               "<em>Sunday Legends Brunch</em>.",
    },
    {
        "slug": "dick-robinson", "name": "Dick Robinson", "mono": "DR",
        "role": "Founder · Late Nights", "show": "American Standards by the Sea",
        "slot": "Weeknights · 11 PM – 1 AM",
        "photo": "assets/hosts/american-standards.jpg",
        "persons": ["Dick Robinson"],
        "bio": "Founder of Legends Radio and of the Connecticut School of Broadcasting. His "
               "<em>American Standards by the Sea</em> is the station's flagship programme, "
               "syndicated well beyond the Palm Beaches.",
    },
    {
        "slug": "popeye-alexander", "name": 'Gregory "Popeye" Alexander', "mono": "PA",
        "role": "Legends of Jazz", "show": "Legends of Jazz", "slot": "Weekly",
        "photo": "assets/hosts/popeye-alexander.jpg",
        "persons": ["Gregory Alexander"],
        "bio": "Popeye hosts <em>Legends of Jazz</em>, the station's dedicated jazz programme.",
    },
    {
        "slug": "cindy-hite", "name": "Cindy Hite", "mono": "CH",
        "role": "Cindy on Legends", "show": "Cindy on Legends", "slot": "Weekly",
        "photo": "assets/hosts/cindy-hite.jpg",
        "persons": ["Cindy Hite"],
        "bio": "Cindy hosts <em>Cindy on Legends</em> on Legends 100.3.",
    },
    {
        "slug": "lauren-may", "name": "Lauren May", "mono": "LM",
        "role": "On Air", "show": "Legends 100.3", "slot": "Weekly",
        "photo": "assets/hosts/lauren-may.jpg",
        "persons": ["Lauren May"],
        "bio": "Lauren May is part of the on-air team at Legends 100.3.",
    },
]

# ---------------------------------------------------------------------------
# WEEKLY SCHEDULE  (Eastern). Keys: 0=Sun … 6=Sat. Fully covers every hour so
# "On Air Now" always resolves. Confirmed hosted shows carry a host; the rest
# are descriptive commercial-free music blocks (see OWNER TO-DOS).
# ---------------------------------------------------------------------------
_OVERNIGHT = {"show": "Nonstop Legends", "host": "Commercial-free standards, all night", "tag": "Overnight"}
_LATENIGHT = {"show": "Dick Robinson's American Standards by the Sea", "host": "Dick Robinson", "tag": "Standards", "slug": "dick-robinson"}
_WEEKDAY = [
    {"start": "00:00", "end": "01:00", **_LATENIGHT},
    {"start": "01:00", "end": "06:00", **_OVERNIGHT},
    {"start": "06:00", "end": "10:00", "show": "The Morning Lounge", "host": "Jill & Rich Switzer", "tag": "Live", "slug": "jill-rich-switzer"},
    {"start": "10:00", "end": "14:00", "show": "Middays with Mike McGann", "host": "Mike McGann", "tag": "Live", "slug": "mike-mcgann"},
    {"start": "14:00", "end": "19:00", "show": "Legends Afternoons with Steve Ketelaar", "host": "Steve Ketelaar", "tag": "Live", "slug": "steve-ketelaar"},
    {"start": "19:00", "end": "21:00", "show": "Evenings with Alex Donner", "host": "Alex Donner", "tag": "Live", "slug": "alex-donner"},
    {"start": "21:00", "end": "23:00", "show": "Legends After Dark", "host": "Bob Merrill", "tag": "Live", "slug": "bob-merrill"},
    {"start": "23:00", "end": "24:00", **_LATENIGHT},
]
SCHEDULE = {
    1: _WEEKDAY, 2: _WEEKDAY, 3: _WEEKDAY, 4: _WEEKDAY, 5: _WEEKDAY,
    6: [  # Saturday
        {"start": "00:00", "end": "08:00", **_OVERNIGHT},
        {"start": "08:00", "end": "08:30", "show": "Saturday Morning Swing", "host": "Big band & swing", "tag": "Music"},
        {"start": "08:30", "end": "09:00", "show": "Pain 2 Power", "host": "Mike McCannon & David Kashuba", "tag": "Talk"},
        {"start": "09:00", "end": "12:00", "show": "Saturday Morning Swing", "host": "Big band & swing", "tag": "Music"},
        {"start": "12:00", "end": "18:00", "show": "Legends Weekend", "host": "The best of the Songbook", "tag": "Music"},
        {"start": "18:00", "end": "20:00", "show": "American Standards by the Sea", "host": "Dick Robinson", "tag": "Signature", "slug": "dick-robinson"},
        {"start": "20:00", "end": "24:00", "show": "Saturday Night Standards", "host": "After-dark classics", "tag": "Music"},
    ],
    0: [  # Sunday
        {"start": "00:00", "end": "07:00", **_OVERNIGHT},
        {"start": "07:00", "end": "10:00", "show": "Sunday Legends Brunch", "host": "Bob Merrill", "tag": "Live", "slug": "bob-merrill"},
        {"start": "07:30", "end": "10:00", "show": "Sunday Morning Standards", "host": "An easy start to Sunday", "tag": "Music"},
        {"start": "10:00", "end": "12:00", "show": "American Standards by the Sea", "host": "Dick Robinson", "tag": "Signature", "slug": "dick-robinson"},
        {"start": "12:00", "end": "18:00", "show": "Sunday Serenade", "host": "Afternoon standards", "tag": "Music"},
        {"start": "18:00", "end": "20:00", "show": "Legends Evenings", "host": "Standards for the evening", "tag": "Music"},
        {"start": "20:00", "end": "22:00", "show": "Legends of Jazz", "host": "Gregory “Popeye” Alexander", "tag": "Jazz", "slug": "popeye-alexander"},
        {"start": "22:00", "end": "24:00", **_OVERNIGHT},
    ],
}
DAYS = [("0", "Sun"), ("1", "Mon"), ("2", "Tue"), ("3", "Wed"), ("4", "Thu"), ("5", "Fri"), ("6", "Sat")]

# Signature / specialty programs (for Shows page cards)
SIGNATURE = [
    {"name": "The Morning Lounge", "host": "Jill & Rich Switzer", "slot": "Weekdays · 6–10 AM",
     "blurb": "Wake up in the Palm Beaches with live music, warm conversation, and the Songbook's brightest mornings."},
    {"name": "Middays with Mike McGann", "host": "Mike McGann", "slot": "Weekdays · 10 AM–2 PM",
     "blurb": "The full music library, wide open — plus the daily Legends at Lunch at noon."},
    {"name": "Legends Afternoons with Steve Ketelaar", "host": "Steve Ketelaar", "slot": "Weekdays · 2–7 PM",
     "blurb": "Timeless company from the afternoon through the golden-hour drive home."},
    {"name": "American Standards by the Sea", "host": "Dick Robinson", "slot": "Sat 6–8 PM · Sun 10 AM–12 PM",
     "blurb": "Dick Robinson's internationally-syndicated salute to Sinatra, Bennett, Streisand and more — produced in part aboard his yacht <em>Airwaves</em> and heard on 75+ stations."},
    {"name": "Legends of Jazz", "host": "Gregory “Popeye” Alexander", "slot": "Sundays · 8–10 PM",
     "blurb": "The Songbook's cooler, smokier side — jazz vocals and instrumentals with a real player at the helm."},
    {"name": "Evenings with Alex Donner", "host": "Alex Donner", "slot": "Weekdays · 7–9 PM",
     "blurb": "Destinations, equipment, and expert interviews for the golfer and traveler in all of us."},
    {"name": "Legends After Dark", "host": "Bob Merrill", "slot": "Weeknights · 9–11 PM",
     "blurb": "Encore hours of American Standards by the Sea to carry you into the small hours."},
    {"name": "Cindy on Legends", "host": "Cindy Hite", "slot": "Weekly · See schedule",
     "blurb": "Uplifting conversation and guests — a reminder that Legends is about companionship as much as music."},
    {"name": "Pain 2 Power", "host": "Mike McCannon & David Kashuba", "slot": "Saturdays · 8:30 AM",
     "blurb": "A weekly dose of health, healing, and the mindset to turn pain into power — Legends' hometown wellness half-hour."},
    {"name": "Legends at Lunch", "host": "Daily at noon", "slot": "Weekdays · 12 PM",
     "blurb": "A midday set of the greatest recordings ever made — the perfect soundtrack to your lunch hour."},
]

NAV = [("index.html", "Home"), ("listen.html", "Listen Live"), ("shows.html", "Shows"),
       ("hosts.html", "On-Air"), ("podcast.html", "On-Demand"), ("events.html", "Events"),
       ("about.html", "About"), ("advertise.html", "Advertise"), ("contact.html", "Contact")]

# ---------------------------------------------------------------------------
# ASSET CACHE-BUSTING
# ---------------------------------------------------------------------------
def asset_v(relpath):
    p = os.path.join(ROOT, relpath)
    try:
        with open(p, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:10]
    except FileNotFoundError:
        return "0"

# ---------------------------------------------------------------------------
# ICONS (inline SVG, currentColor)
# ---------------------------------------------------------------------------
def _svg(body, vb="0 0 24 24"):
    return ('<svg viewBox="%s" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % (vb, body)
IC = {
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.14v13.72a1 1 0 0 0 1.54.84l10.29-6.86a1 1 0 0 0 0-1.68L9.54 4.3A1 1 0 0 0 8 5.14z"/></svg>',
    "pause": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>',
    "vol": _svg('<path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a9 9 0 0 1 0 14"/>'),
    "external": _svg('<path d="M15 3h6v6M21 3l-9 9M10 5H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/>'),
    "phone": _svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/>'),
    "mail": _svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
    "pin": _svg('<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
    "clock": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "mic": _svg('<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10a7 7 0 0 0 14 0M12 17v4"/>'),
    "radio": _svg('<path d="M4 10h16a1 1 0 0 1 1 1v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-8a1 1 0 0 1 1-1z"/><circle cx="8" cy="15" r="2.5"/><path d="M16 6 8 10M15 15h3M15 18h3"/>'),
    "cal": _svg('<rect x="3" y="4.5" width="18" height="17" rx="2"/><path d="M3 9h18M8 2.5v4M16 2.5v4"/>'),
    "arrow": _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "chevron": _svg('<path d="m9 6 6 6-6 6"/>'),
    "headphones": _svg('<path d="M3 14v-2a9 9 0 0 1 18 0v2"/><path d="M21 15a2 2 0 0 1-2 2h-1v-5h1a2 2 0 0 1 2 2zM3 15a2 2 0 0 0 2 2h1v-5H5a2 2 0 0 0-2 2z"/>'),
    "speaker": _svg('<rect x="5" y="2" width="14" height="20" rx="2"/><circle cx="12" cy="14" r="4"/><path d="M12 6h.01"/>'),
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z"/></svg>',
    "note": _svg('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'),
    "wave": _svg('<path d="M2 12h2M6 8v8M10 5v14M14 8v8M18 6v12M22 12h0"/>'),
    "heart": _svg('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 1 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>'),
    "megaphone": _svg('<path d="m3 11 15-6v14l-15-6zM3 11v4M18 7a4 4 0 0 1 0 10"/><path d="M7 15v4a2 2 0 0 0 2 2h1"/>'),
    "users": _svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
    "ticket": _svg('<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2 2 2 0 0 0 0 4 2 2 0 0 1-2 2H5a2 2 0 0 1-2-2 2 2 0 0 0 0-4z"/><path d="M13 6v12"/>'),
    "check": _svg('<path d="M20 6 9 17l-5-5"/>'),
    "insta": _svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.5"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/>'),
    "facebook": _svg('<path d="M15 3h-3a4 4 0 0 0-4 4v3H5v4h3v7h4v-7h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>'),
    "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.53 3H20l-5.9 6.74L21 21h-5.4l-4.23-5.53L6.5 21H4l6.3-7.2L3.3 3h5.53l3.82 5.05zM16.6 19.5h1.37L7.5 4.42H6.03z"/></svg>',
    "soundcloud": _svg('<path d="M4 15v-4M7 16V9M10 16V7M13 16V8a4 4 0 0 1 8 0.5 3 3 0 0 1-.5 6H13"/>'),
    "apple": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.4 12.9c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9s-1.8-.8-3-.8c-1.5 0-3 .9-3.8 2.3-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2-.1 1.6-.7 3-.7s1.8.7 3 .7 2-1.1 2.8-2.2c.9-1.3 1.2-2.5 1.3-2.6-.1 0-2.5-1-2.5-3.8zM14.2 6.2c.6-.8 1.1-1.9 1-3-1 0-2.1.6-2.8 1.4-.6.7-1.1 1.8-1 2.9 1.1.1 2.2-.5 2.8-1.3z"/></svg>',
    "googleplay": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.6 2.3 13.4 12 3.6 21.7a1 1 0 0 1-.6-.9V3.2a1 1 0 0 1 .6-.9zM15 10.4l2.8-2.8 3.6 2a1.2 1.2 0 0 1 0 2.1l-3.6 2L15 13.6 16.4 12 15 10.4zM4.9 22.2 14 13.6l2 1.9-9.2 5.2a1.2 1.2 0 0 1-1.9-.5zM4.9 1.8a1.2 1.2 0 0 1 1.9-.5L16 6.5l-2 1.9z"/></svg>',
}

def deco_bar():
    return '<div class="hero-rays" aria-hidden="true"></div>'

# ---------------------------------------------------------------------------
# SHARED COMPONENTS
# ---------------------------------------------------------------------------
def brand():
    return (
        '<a class="brand" href="index.html" aria-label="Legends Radio 100.3 FM home">'
        '<img class="logo" src="assets/img/legends-emblem.svg" alt="" width="46" height="46" loading="eager">'
        '<span class="brand-txt">'
        '<span class="brand-word"><span class="brand-script">Legends</span><span class="brand-radio">radio</span></span>'
        '<small>100.3 FM · Palm Beach County</small></span>'
        '</a>'
    )

def header(active):
    items = ""
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        aria = ' aria-current="page"' if href == active else ""
        items += '<a href="%s"%s%s>%s</a>' % (href, cls, aria, label)
    return (
        '<a class="skip-link" href="#main">Skip to content</a>'
        '<div class="scroll-rail" id="scroll-rail" aria-hidden="true"></div>'
        '<header class="site-header"><div class="container"><nav class="nav" aria-label="Primary">'
        + brand() +
        '<div class="nav-links" id="nav-links">' + items +
        '<a class="btn btn-primary btn-sm mobile-only-cta" href="listen.html" style="margin-top:1.5rem">Listen Live</a>'
        '</div>'
        '<div class="nav-cta">'
        '<a class="btn btn-ghost btn-sm" href="tel:%s" aria-label="Call the studio">%s <span>Studio</span></a>'
        '<button class="btn btn-primary btn-sm" data-play data-play-label-text="Listen Live" aria-pressed="false">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '</div>'
        '<button class="nav-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav-links">'
        '<span></span><span></span><span></span></button>'
        '</nav></div></header>'
    ) % (STATION["phone_e164"], IC["phone"])

def player():
    return (
        '<div class="player" role="region" aria-label="Live radio player">'
        '<button class="player-play" data-play aria-pressed="false" aria-label="Play or pause the live stream">'
        '<span class="ic-play">' + IC["play"] + '</span><span class="ic-pause">' + IC["pause"] + '</span>'
        '</button>'
        '<div class="vinyl-wrap player-vinyl"><div class="vinyl" style="--s:52px"></div><div class="sheen"></div></div>'
        '<div class="player-meta">'
        '<span class="p-live"><span class="dot-live"></span> On Air Now</span>'
        '<span class="p-show">Nonstop Legends</span>'
        '<span class="p-host">The Great American Songbook</span>'
        '</div>'
        '<span class="eq player-eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>'
        '<span class="player-freq">100.3<span style="font-size:.62em;letter-spacing:.1em"> FM</span></span>'
        '<div class="player-vol">' + IC["vol"] +
        '<input type="range" min="0" max="100" value="85" aria-label="Volume"></div>'
        '<a class="player-pop" href="' + STATION["popout"] + '" target="_blank" rel="noopener" '
        'aria-label="Open pop-out player">' + IC["external"] + '</a>'
        '<audio id="legends-audio" preload="none"></audio>'
        '</div>'
    )

def social_links(cls="foot-social"):
    s = STATION
    return (
        '<div class="%s">'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Instagram">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Facebook">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="X (Twitter)">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="SoundCloud">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="TuneIn">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Apple App Store">%s</a>'
        '<a href="%s" target="_blank" rel="noopener" aria-label="Google Play">%s</a>'
        '</div>'
    ) % (cls, s["instagram"], IC["insta"], s["facebook"], IC["facebook"], s["twitter"], IC["x"],
         s["soundcloud"], IC["soundcloud"], s["tunein"], IC["radio"],
         s["app_ios"], IC["apple"], s["app_android"], IC["googleplay"])

def footer():
    s = STATION
    nav_cols = ""
    listen_links = [("listen.html", "Listen Live"), ("shows.html", "Show Schedule"),
                    ("hosts.html", "On-Air Personalities"), ("podcast.html", "On-Demand & Podcasts"),
                    ("events.html", "Events")]
    station_links = [("about.html", "About the Station"), ("advertise.html", "Advertise With Us"),
                     ("contact.html", "Contact"), (s["eventbrite"], "Buy Event Tickets")]
    def col(title, links):
        li = "".join(
            '<li><a href="%s"%s>%s</a></li>' % (h, (' target="_blank" rel="noopener"' if h.startswith("http") else ""), t)
            for h, t in links)
        return '<div class="footer-col"><h4>%s</h4><ul>%s</ul></div>' % (title, li)
    maps = "https://www.google.com/maps/search/?api=1&query=" + \
           html.escape("%s, %s, %s %s" % (s["addr_street"], s["addr_city"], s["addr_region"], s["addr_zip"]))
    return (
        '<footer class="site-footer"><div class="container"><div class="footer-grid">'
        '<div class="footer-brand">' + brand() +
        '<p>' + s["short"] + ' 100.3 FM is a full-power, live &amp; local station in Florida\'s Palm Beaches, '
        'devoted to preserving and celebrating the Great American Songbook.</p>'
        '<p style="color:var(--gold);font-weight:600;font-size:.82rem;letter-spacing:.03em;margin-top:.9rem">'
        + s["entertainment"] + ' · ' + s["heard"] + '.</p>' + social_links() + '</div>'
        + col("Listen", listen_links) + col("Station", station_links) +
        '<div class="footer-col footer-contact"><h4>Studio</h4><ul>'
        '<li>' + IC["pin"] + '<a href="' + maps + '" target="_blank" rel="noopener">' + s["addr_street"] + '<br>' +
        s["addr_city"] + ', ' + s["addr_region"] + ' ' + s["addr_zip"] + '</a></li>'
        '<li>' + IC["phone"] + '<a href="tel:' + s["phone_e164"] + '">' + s["phone"] + ' · Studio</a></li>'
        '<li>' + IC["mic"] + '<a href="tel:' + s["request_e164"] + '">' + s["request"] + ' · Request Line</a></li>'
        '<li>' + IC["mail"] + '<a href="mailto:' + s["email"] + '">' + s["email"] + '</a></li>'
        '</ul></div>'
        '</div><div class="footer-bottom">'
        '<span>© <span id="year">' + BUILT[:4] + '</span> ' + s["parent"] + ' · ' + s["name"] + ' (' + s["call"] + '). '
        + s["entertainment"] + '. Licensed to ' + s["license_city"] + '.</span>'
        '<span><span class="footer-freq">100.3 FM</span> · ' + s["slogan"] + '</span>'
        '</div></div></footer>'
    )

# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def org_schema():
    s = STATION
    return {
        "@type": ["RadioStation", "LocalBusiness"],
        "@id": BASE + "/#station",
        "name": s["name"], "alternateName": s["call"],
        "url": BASE + "/", "slogan": s["slogan"],
        "description": "Legends Radio 100.3 FM (WLML-FM) is a live, local Great American Songbook "
                       "station serving West Palm Beach and the Palm Beaches.",
        "logo": BASE + "/assets/img/favicon.png",
        "image": BASE + "/assets/img/legends-og.png",
        "telephone": s["phone_e164"], "email": s["email"],
        "foundingDate": s["founded_iso"],
        "parentOrganization": {"@type": "Organization", "name": s["parent"]},
        "address": {"@type": "PostalAddress", "streetAddress": s["addr_street"],
                    "addressLocality": s["addr_city"], "addressRegion": s["addr_region"],
                    "postalCode": s["addr_zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": s["geo_lat"], "longitude": s["geo_lng"]},
        "broadcastFrequency": {"@type": "BroadcastFrequencySpecification",
                               "broadcastFrequencyValue": s["freq"], "broadcastSignalModulation": "FM"},
        "areaServed": [{"@type": "City", "name": c} for c in AREA_SERVED],
        "sameAs": [s["instagram"], s["soundcloud"], s["tunein"], s["app_ios"], s["app_android"]],
    }

def breadcrumb(title, filename):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": BASE + "/" + filename},
        ],
    }

def jsonld(*nodes):
    graph = [org_schema()]
    for n in nodes:
        if n:
            graph.append(n)
    doc = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">%s</script>' % json.dumps(doc, ensure_ascii=False)

# ---------------------------------------------------------------------------
# DOCUMENT SHELL
# ---------------------------------------------------------------------------
CSS_V = None
JS_V = None

def document(filename, title, desc, body, active, extra_schema=None, og_image="legends-og.png"):
    canonical = BASE + "/" + ("" if filename == "index.html" else filename)
    og_url = BASE + "/assets/img/" + og_image
    sched_json = json.dumps({str(k): v for k, v in SCHEDULE.items()}, ensure_ascii=False)
    data_script = (
        "window.LEGENDS_SCHEDULE=" + sched_json + ";"
        "window.LEGENDS_STREAM=" + json.dumps(STATION["stream"]) + ";"
        "window.LEGENDS_POPOUT=" + json.dumps(STATION["popout"]) + ";"
        "window.LEGENDS_ARTWORK=" + json.dumps(BASE + "/assets/img/legends-artwork.png") + ";"
    )
    schema = jsonld(breadcrumb(title.split(" | ")[0], filename) if filename != "index.html" else None,
                    extra_schema)
    return (
        "<!doctype html><html lang=\"en\"><head>"
        "<meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<base href=\"" + SITE_BASE_PATH + "\">"
        "<title>" + html.escape(title) + "</title>"
        "<meta name=\"description\" content=\"" + html.escape(desc) + "\">"
        "<link rel=\"canonical\" href=\"" + canonical + "\">"
        "<meta name=\"theme-color\" content=\"#0A0B16\">"
        # Open Graph / Twitter
        "<meta property=\"og:type\" content=\"website\">"
        "<meta property=\"og:site_name\" content=\"" + STATION["name"] + "\">"
        "<meta property=\"og:title\" content=\"" + html.escape(title) + "\">"
        "<meta property=\"og:description\" content=\"" + html.escape(desc) + "\">"
        "<meta property=\"og:url\" content=\"" + canonical + "\">"
        "<meta property=\"og:image\" content=\"" + og_url + "\">"
        "<meta property=\"og:image:width\" content=\"1200\"><meta property=\"og:image:height\" content=\"630\">"
        "<meta name=\"twitter:card\" content=\"summary_large_image\">"
        "<meta name=\"twitter:title\" content=\"" + html.escape(title) + "\">"
        "<meta name=\"twitter:description\" content=\"" + html.escape(desc) + "\">"
        "<meta name=\"twitter:image\" content=\"" + og_url + "\">"
        # icons + manifest
        "<link rel=\"icon\" href=\"assets/img/favicon.svg\" type=\"image/svg+xml\">"
        "<link rel=\"icon\" href=\"assets/img/favicon.png\" sizes=\"any\">"
        "<link rel=\"apple-touch-icon\" href=\"assets/img/apple-touch-icon.png\">"
        "<link rel=\"manifest\" href=\"site.webmanifest\">"
        # fonts preload (glamour serif + body sans)
        "<link rel=\"preload\" href=\"assets/fonts/playfair-display-latin-600-normal.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>"
        "<link rel=\"preload\" href=\"assets/fonts/inter-latin-500-normal.woff2\" as=\"font\" type=\"font/woff2\" crossorigin>"
        "<link rel=\"stylesheet\" href=\"assets/css/legends.css?v=" + CSS_V + "\">"
        + schema +
        "</head><body>"
        + header(active) +
        "<main id=\"main\">" + body + "</main>"
        + footer()
        + player()
        + "<script>" + data_script + "</script>"
        + "<script src=\"assets/js/legends.js?v=" + JS_V + "\" defer></script>"
        "</body></html>"
    )

# ---------------------------------------------------------------------------
# SECTION HELPERS
# ---------------------------------------------------------------------------
def eyebrow(text, centered=False):
    return '<span class="eyebrow%s">%s</span>' % (" centered" if centered else "", html.escape(text))

def marquee():
    spans = "".join("<span>%s</span>" % html.escape(a) for a in ARTISTS)
    return ('<div class="marquee" aria-hidden="true"><div class="marquee-track">' + spans + '</div></div>'
            '<div class="sr-only">Legends Radio plays the Great American Songbook: '
            + html.escape(", ".join(ARTISTS)) + '.</div>')

def listen_options_grid():
    tiles = [
        ("headphones", "Online", "Stream free right here — one tap on the Listen Live player.",
         '<button class="btn btn-ghost btn-sm" data-play data-play-label-text="Play Stream"><span data-play-label>Play Stream</span></button>'),
        ("radio", "On Your Radio", "Tune to <strong>100.3 FM</strong> across the Palm Beaches.", ""),
        ("speaker", "Smart Speaker", "Say &ldquo;Alexa, play Legends Radio&rdquo; or ask Google.", ""),
        ("note", "Mobile App", "Take Legends anywhere on iOS &amp; Android.",
         '<a class="btn btn-ghost btn-sm" href="%s" target="_blank" rel="noopener">Get the App %s</a>' % (STATION["app_ios"], IC["external"])),
    ]
    cards = ""
    for i, (ic, h, p, cta) in enumerate(tiles):
        cards += ('<div class="card listen-tile reveal reveal-d%d"><div class="ic">%s</div>'
                  '<h3>%s</h3><p>%s</p>%s</div>') % (i % 4, IC[ic], h, p, ("<div class='mt-2'>%s</div>" % cta if cta else ""))
    return '<div class="listen-grid">' + cards + '</div>'

def cta_band(heading, sub, primary=None, secondary=None):
    p = ('<a class="btn btn-primary btn-lg" href="%s">%s</a>' % primary) if primary else ""
    s = ('<a class="btn btn-ghost btn-lg" href="%s">%s</a>' % secondary) if secondary else ""
    return (
        '<section class="section"><div class="container"><div class="cta-band reveal">'
        + eyebrow("Tune In", True) +
        '<h2>' + heading + '</h2><p class="lede mx-auto" style="margin-inline:auto">' + sub + '</p>'
        '<div class="hero-actions" style="justify-content:center;margin-top:1.8rem">'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>' + s +
        '</div></div></div></section>'
    )

def newsletter_block():
    return (
        '<section class="section-tight surface"><div class="container">'
        '<div class="split" style="align-items:center">'
        '<div class="reveal"><span class="eyebrow">Stay in the loop</span>'
        '<h2 style="margin:.6rem 0 .8rem">Never miss a note.</h2>'
        '<p class="lede">Concerts, supper clubs, giveaways, and new shows — straight to your inbox from the Palm Beaches.</p></div>'
        '<div class="reveal reveal-d1"><form class="subscribe" data-endpoint="https://formsubmit.co/ajax/'
        + STATION["email"] + '" data-success="You’re on the list — see you on 100.3!" aria-label="Newsletter signup">'
        '<input type="email" name="email" placeholder="you@example.com" required aria-label="Email address">'
        '<input type="hidden" name="_subject" value="New Legends newsletter signup">'
        '<button class="btn btn-primary" type="submit">Subscribe ' + IC["arrow"] + '</button>'
        '</form><p class="form-note" style="margin-top:.7rem">No spam — just the music. Unsubscribe anytime.</p>'
        '<div class="form-status" role="status"></div></div>'
        '</div></div></section>'
    )

def page_hero(eb, h1, sub, filename):
    crumbs = ('<nav class="breadcrumb" aria-label="Breadcrumb"><a href="index.html">Home</a>'
              '<span>/</span><span style="color:var(--muted)">%s</span></nav>') % html.escape(h1)
    return ('<section class="page-hero">' + deco_bar() + '<div class="container">'
            + eyebrow(eb, True) + '<h1>' + h1 + '</h1>'
            '<div class="rule-deco" aria-hidden="true"><i></i></div>'
            '<p>' + sub + '</p>' + crumbs +
            '</div></section>')

def emblem_big():
    # Art Deco round emblem used inside deco frames
    return (
        '<div class="vinyl-wrap"><div class="vinyl" style="--s:min(340px,64vw)"></div>'
        '<div class="sheen"></div></div>'
    )

EQ7 = '<span class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span>'

EVENTS = [
    {"title": "Live Concerts at Abacoa", "tag": "Free Concert Series", "icon": "ticket",
     "blurb": "Legends Radio &amp; Robinson Entertainment present a free tribute-concert series at the Downtown Abacoa Amphitheater in Jupiter — showtime 7:30 PM, all ages, with optional Preferred Reserved Seating."},
    {"title": "American Songbook Tributes", "tag": "On Stage", "icon": "note",
     "blurb": "From PHD (Petty · Hall &amp; Oates · Steely Dan) to a Chicago tribute and ’60s–’70s celebrations, the concert lineup rotates all season long across the Palm Beaches."},
    {"title": "Supper Club with Jill &amp; Rich", "tag": "Live Cabaret", "icon": "mic",
     "blurb": "An intimate evening of the Great American Songbook performed live by morning hosts Jill &amp; Rich Switzer — the classics the way they were meant to be heard."},
    {"title": "SPGAS Benefactors Gala", "tag": "Black Tie · Give Back", "icon": "heart",
     "blurb": "The Society for the Preservation of the Great American Songbook's signature gala — honoring legends like Marilyn Maye, from Club Colette to the Kravis Center."},
]

ON_DEMAND = [
    {"title": "American Standards by the Sea", "host": "Dick Robinson", "icon": "wave",
     "blurb": "Dick Robinson's syndicated Songbook program, produced in part aboard the yacht <em>Airwaves</em>. "
              "Catch it weeknights at 11 PM — or stream on demand.",
     "cta": "Listen on SoundCloud", "url": STATION["soundcloud"]},
    {"title": "The Legends Radio Archive", "host": "On SoundCloud", "icon": "headphones",
     "blurb": "Interviews, features, and moments from the studio — the station's growing on-demand library, "
              "free to stream anytime.",
     "cta": "Browse the archive", "url": STATION["soundcloud"]},
    {"title": "The Sounds of Sinatra", "host": "Legends 100.3", "icon": "mic",
     "blurb": "The Chairman of the Board, hour after hour — the Sinatra songbook as only Legends plays it.",
     "cta": "Visit the show", "url": "https://thegolfandtravelshow.com/"},
    {"title": "Cindy on Legends", "host": "Cindy Hite", "icon": "heart",
     "blurb": "Cindy Hite's programme on Legends 100.3, available to stream between broadcasts.",
     "cta": "Follow on SoundCloud", "url": STATION["soundcloud"]},
]

def host_card(h, idx=0, full=False):
    persons = ""
    img = ('<img src="%s" alt="%s, %s on Legends Radio 100.3 FM" loading="lazy" decoding="async">'
           % (h["photo"], html.escape(h["name"]), html.escape(h["role"]))) if h.get("photo") else ""
    bio = ('<p class="host-bio">%s</p>' % h["bio"]) if full else ""
    return (
        '<article class="card host-card reveal reveal-d%d">'
        '<div class="host-medallion">%s<span class="mono">%s</span></div>'
        '<span class="host-role">%s</span>'
        '<h3>%s</h3>'
        '<div class="host-show">%s</div>'
        '<div class="host-slot">%s</div>%s'
        '</article>'
    ) % (idx % 4, img, h["mono"], html.escape(h["role"]), html.escape(h["name"]),
         html.escape(h["show"]), html.escape(h["slot"]), bio)

def show_card(sig, idx=0):
    return (
        '<article class="card reveal reveal-d%d">'
        '<span class="pill">%s</span>'
        '<h3 style="margin:.9rem 0 .3rem">%s</h3>'
        '<p style="color:var(--gold);font-weight:600;font-size:.92rem;margin-bottom:.6rem">%s</p>'
        '<p style="color:var(--muted);font-size:.95rem">%s</p>'
        '</article>'
    ) % (idx % 4, html.escape(sig["slot"]), html.escape(sig["name"]),
         html.escape(sig["host"]), sig["blurb"])

def event_card(ev, idx=0):
    return (
        '<article class="card reveal reveal-d%d" style="display:flex;flex-direction:column">'
        '<div style="width:56px;height:56px;display:grid;place-items:center;border-radius:15px;margin-bottom:1.2rem;'
        'background:linear-gradient(160deg,rgba(178,61,75,.28),rgba(138,44,56,.12));'
        'border:1px solid rgba(178,61,75,.42);color:var(--gold-bright)">%s</div>'
        '<span class="pill" style="align-self:flex-start">%s</span>'
        '<h3 style="margin:.8rem 0 .45rem">%s</h3>'
        '<p style="color:var(--muted);font-size:.95rem;flex:1">%s</p>'
        '<div class="mt-3"><a class="link-arrow" href="%s" target="_blank" rel="noopener">Dates &amp; tickets on Eventbrite %s</a></div>'
        '</article>'
    ) % (idx % 4, IC[ev["icon"]], ev["tag"], ev["title"], ev["blurb"], STATION["eventbrite"], IC["arrow"])

def np_card():
    return (
        '<div class="np-card">'
        '<div class="np-head"><span class="pill pill-live"><span class="dot-live"></span> On Air Now</span>' + EQ7 + '</div>'
        '<div class="np-body">'
        '<div class="vinyl-wrap"><div class="vinyl" style="--s:96px"></div><div class="sheen"></div></div>'
        '<div class="np-info">'
        '<div class="np-show" id="np-show">Nonstop Legends</div>'
        '<div class="np-host" id="np-host">The Great American Songbook</div>'
        '<div class="np-time" id="np-time"></div>'
        '</div></div>'
        '<div class="np-foot"><span class="np-next" id="np-next">Streaming live from the Palm Beaches</span>'
        '<button class="btn btn-primary btn-sm" data-play data-play-label-text="Listen"><span class="ic-play" style="display:inline-flex">'
        + IC["play"] + '</span> <span data-play-label>Listen</span></button></div>'
        '</div>'
    )

# ===========================================================================
# PAGES
# ===========================================================================
def home_page():
    hero = (
        '<section class="hero">'
        + deco_bar() +
        '<div class="hero-beam b1" aria-hidden="true"></div><div class="hero-beam b2" aria-hidden="true"></div>'
        '<div class="hero-vignette" aria-hidden="true"></div>'
        '<div class="container"><div class="hero-inner">'
        '<div class="hero-copy reveal">'
        '<p class="script-line" style="font-size:clamp(1.9rem,4vw,3rem);margin-bottom:.5rem;display:flex;align-items:center;gap:.5rem">'
        'The One and Only…<img class="deco-flag" src="assets/img/legends-flag.svg" alt="" width="46" height="29"></p>'
        '<div class="hero-badge"><span class="freq">100.3 FM</span><span class="sep"></span>'
        '<small>Live &amp; Local · Palm Beach County</small></div>'
        '<h1>Where <span class="accent foil">Legendary</span><br>Music Lives</h1>'
        '<p class="hero-sub">The Great American Songbook, on the air 24/7 from Florida\'s Palm Beaches — '
        'Sinatra to Bublé, Ella to Krall, all day and all night.</p>'
        '<div class="hero-actions">'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '<a class="btn btn-ghost btn-lg" href="shows.html">Explore the Lineup ' + IC["arrow"] + '</a>'
        '</div>'
        '<div class="hero-meta">'
        '<div><b>2014</b><span>On the Air Since</span></div>'
        '<div><b>75+</b><span>Stations Coast&nbsp;to&nbsp;Coast</span></div>'
        '<div><b>24/7</b><span>Worldwide Stream</span></div>'
        '</div></div>'
        '<div class="hero-visual reveal reveal-d2">' + np_card() + '</div>'
        '</div></div></section>'
    )
    stats = (
        '<section class="section-tight"><div class="container-wide"><div class="stats">'
        '<div class="stat"><div class="num">100.3</div><div class="lbl">FM · Live &amp; Local</div></div>'
        '<div class="stat"><div class="num" data-count="75" data-suffix="+"></div><div class="lbl">Syndicated Stations</div></div>'
        '<div class="stat"><div class="num">2014</div><div class="lbl">On the Air Since</div></div>'
        '<div class="stat"><div class="num">24/7</div><div class="lbl">Worldwide Stream</div></div>'
        '</div></div></section>'
    )
    intro = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="split-media reveal"><div class="deco-frame">' + emblem_big() + '</div></div>'
        '<div class="reveal reveal-d1">' + eyebrow("The Legends Sound") +
        '<h2 style="margin:.7rem 0 1rem">The greatest music ever made — '
        '<span class="serif-italic text-gold">all day, every day.</span></h2>'
        '<p class="lede">There was a time when a song was a story, an orchestra swelled behind a '
        'velvet voice, and the whole room leaned in. That music never went away — it just needed a home.</p>'
        '<p style="margin-top:1rem;color:var(--muted)">Legends 100.3 is a full-power, live and local FM station '
        'in the Palm Beaches, spinning Frank Sinatra, Ella Fitzgerald, Tony Bennett, Michael Bublé, Diana Krall '
        'and the entire Great American Songbook — hosted by real people who love it as much as you do.</p>'
        '<div class="mt-3"><a class="link-arrow" href="about.html">Our story ' + IC["arrow"] + '</a></div>'
        '</div></div></div></section>'
    )
    shows = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">On the Air</span>'
        '<h2>Signature shows, real hosts</h2>'
        '<p class="lede mx-auto">Live and local, morning to midnight — company for every hour of your day.</p></div>'
        '<div class="grid grid-3">'
        + show_card(SIGNATURE[0], 0) + show_card(SIGNATURE[1], 1) + show_card(SIGNATURE[3], 2) +
        '</div><div class="center mt-4"><a class="btn btn-ghost" href="shows.html">See the full weekly schedule ' + IC["arrow"] + '</a></div>'
        '</div></section>'
    )
    hosts = (
        '<section class="section surface-deep"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Your Hosts</span>'
        '<h2>The voices of the Palm Beaches</h2></div>'
        '<div class="grid grid-4">'
        + "".join(host_card(h, i) for i, h in enumerate(HOSTS[:4])) +
        '</div><div class="center mt-4"><a class="btn btn-ghost" href="hosts.html">Meet the whole on-air team ' + IC["arrow"] + '</a></div>'
        '</div></section>'
    )
    events = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Out on the Town</span>'
        '<h2>Legends, live and in the room</h2>'
        '<p class="lede mx-auto">The music leaves the studio all season long across Palm Beach County.</p></div>'
        '<div class="grid grid-3">'
        + "".join(event_card(e, i) for i, e in enumerate(EVENTS[:3])) +
        '</div><div class="center mt-4"><a class="btn btn-ghost" href="events.html">All events &amp; tickets ' + IC["arrow"] + '</a></div>'
        '</div></section>'
    )
    listen = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Four Ways to Listen</span>'
        '<h2>However you tune in, we’re there</h2></div>'
        + listen_options_grid() +
        '</div></section>'
    )
    body = hero + marquee() + stats + intro + shows + hosts + events + listen + newsletter_block() + cta_band(
        "Pour a drink. Turn it up.",
        "The Great American Songbook is playing right now on 100.3 FM — and streaming worldwide.",
        secondary=("shows.html", "Browse Shows"))
    return document("index.html",
                    "Legends Radio 100.3 FM | Great American Songbook · Palm Beaches",
                    "Legends Radio 100.3 FM (WLML) streams the Great American Songbook live from the Palm Beaches — "
                    "Sinatra, Ella, Bublé, Krall and more, 24/7. Listen live online, on 100.3 FM, or on the app.",
                    body, "index.html",
                    extra_schema={"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/",
                                  "name": STATION["name"], "publisher": {"@id": BASE + "/#station"}})

def listen_page():
    hero = page_hero("Listen Live", "Tune the Palm Beaches in.",
                     "One tap and the Great American Songbook is playing — online, on your phone, on your radio, "
                     "or through your smart speaker.", "listen.html")
    big = (
        '<section class="section"><div class="container"><div class="cta-band reveal" style="text-align:center">'
        '<div class="np-head" style="justify-content:center;gap:1rem"><span class="pill pill-live"><span class="dot-live"></span> Streaming Live</span></div>'
        '<div style="display:flex;flex-direction:column;align-items:center;gap:1.4rem;margin-top:1.4rem">'
        '<div class="vinyl-wrap"><div class="vinyl" style="--s:min(240px,58vw)"></div><div class="sheen"></div></div>'
        '<div><div class="np-show" id="np-show" style="font-size:1.8rem">Nonstop Legends</div>'
        '<div class="np-host" id="np-host" style="font-size:1rem;margin-top:.3rem">The Great American Songbook</div>'
        '<div class="np-time" id="np-time" style="margin-top:.4rem"></div></div>'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '<p class="form-note">Or tune to <strong>100.3 FM</strong> across the Palm Beaches · Prefer a pop-out? '
        '<a href="' + STATION["popout"] + '" target="_blank" rel="noopener" style="color:var(--gold);text-decoration:underline">open the player</a></p>'
        '</div></div></div></section>'
    )
    ways = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Ways to Listen</span>'
        '<h2>Legends goes wherever you do</h2></div>' + listen_options_grid() +
        '<div class="grid grid-2 mt-4">'
        '<a class="btn btn-ghost btn-lg btn-block" href="' + STATION["app_ios"] + '" target="_blank" rel="noopener">'
        + IC["apple"] + ' Download for iPhone</a>'
        '<a class="btn btn-ghost btn-lg btn-block" href="' + STATION["app_android"] + '" target="_blank" rel="noopener">'
        + IC["googleplay"] + ' Get it on Google Play</a>'
        '</div></div></section>'
    )
    request = (
        '<section class="section"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("Request Line") +
        '<h2 style="margin:.7rem 0 1rem">Got a request or a dedication?</h2>'
        '<p class="lede">Ask for your favorite standard, send a shout-out, or dedicate a song to someone you love. '
        'Call the request line or drop us a note — our hosts read them on the air.</p>'
        '<div class="mt-3"><a class="btn btn-wine btn-lg" href="tel:' + STATION["request_e164"] + '">'
        + IC["phone"] + ' Call ' + STATION["request"] + '</a></div></div>'
        '<div class="reveal reveal-d1"><form class="form card" data-endpoint="https://formsubmit.co/ajax/'
        + STATION["email"] + '" data-success="Thanks — we’ve got your request. Keep it locked on 100.3!">'
        '<input type="hidden" name="_subject" value="Song request / dedication — legendsradio.com">'
        '<div class="field"><label for="rq-name">Your name</label><input id="rq-name" name="name" required placeholder="First &amp; last"></div>'
        '<div class="field"><label for="rq-song">Your request or dedication</label>'
        '<textarea id="rq-song" name="request" required placeholder="&ldquo;Fly Me to the Moon&rdquo; for my wife Rose on our anniversary…"></textarea></div>'
        '<div class="field"><label for="rq-email">Email <span style="text-transform:none;color:var(--muted-2)">(optional)</span></label>'
        '<input id="rq-email" type="email" name="email" placeholder="you@example.com"></div>'
        '<button class="btn btn-primary" type="submit">Send to the Studio ' + IC["arrow"] + '</button>'
        '<div class="form-status" role="status"></div></form></div>'
        '</div></div></section>'
    )
    body = hero + big + marquee() + ways + request
    return document("listen.html",
                    "Listen Live | Legends Radio 100.3 FM · Palm Beaches",
                    "Listen to Legends Radio 100.3 FM live online, on the iOS & Android app, on your radio at "
                    "100.3 FM, or via smart speaker. The Great American Songbook, streaming 24/7.",
                    body, "listen.html",
                    extra_schema={"@type": "BroadcastService", "name": STATION["name"],
                                  "broadcastDisplayName": "Legends 100.3", "provider": {"@id": BASE + "/#station"},
                                  "broadcastFrequency": {"@type": "BroadcastFrequencySpecification",
                                                         "broadcastFrequencyValue": "100.3", "broadcastSignalModulation": "FM"}})

def shows_page():
    hero = page_hero("Shows & Schedule", "The week on Legends 100.3.",
                     "Live hosts by day, standards by night, and specialty programs all weekend — here’s "
                     "everything on the air, with the current show highlighted in real time.", "shows.html")
    sig = (
        '<section class="section"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Signature Programs</span>'
        '<h2>Shows worth setting your day around</h2></div>'
        '<div class="grid grid-3">' + "".join(show_card(s, i) for i, s in enumerate(SIGNATURE)) + '</div>'
        '</div></section>'
    )
    # weekly grid
    tabs = '<div class="sched-tabs" role="tablist" aria-label="Choose a day">'
    for val, label in DAYS:
        tabs += '<button role="tab" data-day="%s" aria-selected="false">%s</button>' % (val, label)
    tabs += '</div>'
    panels = ""
    for val, label in DAYS:
        rows = ""
        day = SCHEDULE[int(val)]
        for i, slot in enumerate(day):
            live_tag = ('<span class="live-badge"><span class="dot-live"></span> Live Now</span>'
                        '<span class="s-tag">%s</span>') % html.escape(slot.get("tag", "Music"))
            rows += (
                '<div class="sched-row" data-day="%s" data-idx="%d" data-start="%s" data-end="%s">'
                '<div class="s-time">%s – %s</div>'
                '<div><div class="s-show">%s</div><div class="s-host">%s</div></div>'
                '<div class="s-meta-right" style="text-align:right">%s</div>'
                '<span class="s-progress"></span>'
                '</div>'
            ) % (val, i, slot["start"], slot["end"], fmt12(slot["start"]), fmt12(slot["end"]),
                 html.escape(slot["show"]), html.escape(slot["host"]), live_tag)
        panels += '<div data-sched-day="%s" class="sched-list" hidden>%s</div>' % (val, rows)
    grid = (
        '<section class="section surface"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Weekly Schedule</span>'
        '<h2>What’s on, right now</h2>'
        '<p class="lede mx-auto">All times Eastern. The live show is highlighted automatically.</p></div>'
        + tabs + panels +
        '<p class="form-note center mt-4">Programming is subject to change — for the very latest, visit '
        '<a href="https://legendsradio.com" target="_blank" rel="noopener" style="color:var(--gold)">legendsradio.com</a>.</p>'
        '</div></section>'
    )
    # ItemList schema for signature shows
    item_list = {"@type": "ItemList", "name": "Legends Radio Shows",
                 "itemListElement": [{"@type": "ListItem", "position": i + 1,
                                      "item": {"@type": "RadioSeries", "name": s["name"]}}
                                     for i, s in enumerate(SIGNATURE)]}
    body = hero + sig + grid + cta_band("Hear it live",
                                        "Whatever’s on right now, it’s the best music ever made — playing on 100.3 FM.",
                                        secondary=("hosts.html", "Meet the Hosts"))
    return document("shows.html",
                    "Shows & Schedule | Legends Radio 100.3 FM",
                    "The full weekly schedule for Legends Radio 100.3 FM — The Morning Lounge, Middays, "
                    "Afternoons, American Standards by the Sea and more. All times Eastern, live show highlighted.",
                    body, "shows.html", extra_schema=item_list)

def hosts_page():
    hero = page_hero("On-Air Personalities", "The people behind the music.",
                     "Live and local means real voices you get to know — the hosts who make Legends 100.3 "
                     "feel like the best table in the room.", "hosts.html")
    grid = (
        '<section class="section"><div class="container"><div class="grid grid-3">'
        + "".join(host_card(h, i, full=True) for i, h in enumerate(HOSTS)) +
        '</div></div></section>'
    )
    # Person schema for each named individual
    persons = []
    for h in HOSTS:
        for name in h["persons"]:
            persons.append({"@type": "Person", "name": name, "jobTitle": "Radio Host",
                            "worksFor": {"@id": BASE + "/#station"}})
    body = hero + grid + newsletter_block() + cta_band(
        "Say hello on the air",
        "Call the request line, send a dedication, or just tell us what you want to hear next.",
        secondary=("contact.html", "Contact the Studio"))
    return document("hosts.html",
                    "On-Air Personalities | Legends Radio 100.3 FM",
                    "Meet the hosts of Legends Radio 100.3 FM — Jill & Rich Switzer, Mike McGann, "
                    "Steve Ketelaar, Alex Donner, Bob Merrill and Dick Robinson — live & local in the Palm Beaches.",
                    body, "hosts.html", extra_schema={"@type": "ItemList",
                                                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": p}
                                                                          for i, p in enumerate(persons)]})

def about_page():
    hero = page_hero("Our Story", "Keeping the Songbook alive.",
                     "Legends 100.3 was signed on the air in 2014 with a single mission: preserve and celebrate "
                     "the greatest music ever recorded — and give it a proud home in the Palm Beaches.", "about.html")
    story = (
        '<section class="section"><div class="container"><div class="split reverse">'
        '<div class="split-media reveal"><div class="deco-frame">' + emblem_big() + '</div></div>'
        '<div class="reveal reveal-d1">' + eyebrow("Since 2014") +
        '<h2 style="margin:.7rem 0 1rem">A station built to remember.</h2>'
        '<p class="lede">Legends Radio was founded by <strong>Dick Robinson</strong> — a broadcasting legend whose '
        'nearly 70-year career began in Massachusetts in 1958 and made him one of the biggest DJs in New England at '
        'WDRC in Hartford. In 1964 he founded the Connecticut School of Broadcasting.</p>'
        '<p style="margin-top:1rem;color:var(--muted)">In 2014, Robinson Entertainment won the 100.3 frequency and '
        'signed Legends on the air to bring “great music and great companionship back to the airwaves” — from the '
        'studios here in North Palm Beach, full-power across the Palm Beaches and streaming worldwide.</p>'
        '<p style="margin-top:1rem;color:var(--muted)"><strong>Locally owned, family-led.</strong> Dick runs the '
        'station with his children — James, Jill, and COO Missy Robinson. Not a national network, not a corporate '
        'boardroom: just a family that loves this music as much as the audience does. That’s the difference you can hear.</p>'
        '</div></div></div></section>'
    )
    quote = (
        '<section class="section surface"><div class="container"><div class="quote reveal">'
        '<div class="mark">&ldquo;</div>'
        '<blockquote>To celebrate timeless music, honor legendary artists, and serve Palm Beach County with '
        'integrity, class, and heart.</blockquote>'
        '<cite>— The Legends Radio Mission</cite></div></div></section>'
    )
    airwaves = (
        '<section class="section"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("The Flagship") +
        '<h2 style="margin:.7rem 0 1rem">American Standards <span class="serif-italic text-gold">by the Sea</span></h2>'
        '<p class="lede">Dick Robinson’s internationally-syndicated, two-hour salute to Sinatra, Bennett, Streisand '
        'and the legends — produced in part aboard his motor yacht <em>Airwaves</em>.</p>'
        '<p style="margin-top:1rem;color:var(--muted)">What began in the Palm Beaches now airs on <strong>75+ stations '
        'nationwide</strong>. Dick is also Founder &amp; Chairman of the <strong>' + STATION["spgas"] + '</strong> '
        '(SPGAS), the 501(c)(3) devoted to keeping this music alive for the next generation.</p>'
        '<div class="mt-3"><a class="link-arrow" href="shows.html">Hear it Sat 6–8 PM &amp; Sun 10 AM–12 PM ' + IC["arrow"] + '</a></div>'
        '</div>'
        '<div class="reveal reveal-d1"><div class="deco-frame" style="aspect-ratio:1/1">' + emblem_big() + '</div></div>'
        '</div></div></section>'
    )
    facts = (
        '<section class="section surface"><div class="container-wide"><div class="stats">'
        '<div class="stat"><div class="num">WLML</div><div class="lbl">FM · Lake Park, FL</div></div>'
        '<div class="stat"><div class="num">100.3</div><div class="lbl">Megahertz</div></div>'
        '<div class="stat"><div class="num" data-count="75" data-suffix="+"></div><div class="lbl">Syndicated Stations</div></div>'
        '<div class="stat"><div class="num">45+</div><div class="lbl">Our Loyal Audience</div></div>'
        '</div></div></section>'
    )
    partners = ["Palm Beach North Chamber of Commerce", "Abacoa", "Cultural Council for Palm Beach County", STATION["spgas"]]
    community = (
        '<section class="section" id="community"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">Community &amp; Partners</span>'
        '<h2>Rooted in Palm Beach County</h2>'
        '<p class="lede mx-auto">Legends is a proud member and media partner of the organizations that make the '
        'Palm Beaches sing — on the air, on stage, and in the community.</p></div>'
        '<div style="display:flex;flex-wrap:wrap;gap:.9rem;justify-content:center;max-width:820px;margin-inline:auto">'
        + "".join('<span class="pill" style="font-size:.86rem;padding:.7em 1.2em">%s</span>' % p for p in partners) +
        '</div></div></section>'
    )
    music = (
        '<section class="section surface-deep"><div class="container">'
        '<div class="section-head center"><span class="eyebrow centered">The Music</span>'
        '<h2>The Great American Songbook</h2>'
        '<p class="lede mx-auto">The timeless standards, swing, and vocal jazz that defined American music — '
        'performed by the artists who made them immortal.</p></div>'
        + marquee() +
        '</div></section>'
    )
    body = hero + story + quote + airwaves + facts + community + music + cta_band(
        "This is your station",
        "Live &amp; local in the Palm Beaches, streaming to the world. Come listen.",
        secondary=("hosts.html", "Meet the Team"))
    return document("about.html",
                    "About | Legends Radio 100.3 FM · Great American Songbook",
                    "Legends Radio 100.3 FM (WLML) was founded in 2014 by broadcaster Dick Robinson to preserve "
                    "the Great American Songbook — live & local from the Palm Beaches, streaming worldwide.",
                    body, "about.html")

def events_page():
    hero = page_hero("Events", "The music, out on the town.",
                     "All season long, Legends 100.3 brings the Great American Songbook off the dial and into the "
                     "Palm Beaches — supper clubs, live broadcasts, and community nights.", "events.html")
    grid = (
        '<section class="section"><div class="container"><div class="grid grid-3">'
        + "".join(event_card(e, i) for i, e in enumerate(EVENTS)) + '</div>'
        '<div class="center mt-4"><a class="btn btn-primary btn-lg" href="' + STATION["eventbrite"] + '" target="_blank" rel="noopener">'
        + IC["ticket"] + ' See upcoming dates &amp; get tickets</a>'
        '<p class="form-note mt-2">Free concerts at the <strong>Downtown Abacoa Amphitheater</strong>, Jupiter · '
        'Dates are announced on Eventbrite and on the air. Follow us on '
        '<a href="' + STATION["instagram"] + '" target="_blank" rel="noopener" style="color:var(--gold)">Instagram</a> so you never miss one.</p></div>'
        '</div></section>'
    )
    host_event = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("Host With Legends") +
        '<h2 style="margin:.7rem 0 1rem">Bringing Legends to your event</h2>'
        '<p class="lede">Planning a gala, grand opening, or charity night? A live Legends broadcast or a Songbook '
        'performance sets a tone nothing else can — timeless, elegant, unmistakably Palm Beach.</p>'
        '<div class="mt-3"><a class="btn btn-ghost btn-lg" href="contact.html">Talk to us ' + IC["arrow"] + '</a></div></div>'
        '<div class="reveal reveal-d1"><div class="deco-frame" style="aspect-ratio:1/1">' + emblem_big() + '</div></div>'
        '</div></div></section>'
    )
    body = hero + grid + host_event + newsletter_block()
    return document("events.html",
                    "Events | Legends Radio 100.3 FM · Palm Beaches",
                    "Legends Radio 100.3 FM events across Palm Beach County — supper clubs, live broadcasts, and "
                    "community nights celebrating the Great American Songbook. Dates & tickets on Eventbrite.",
                    body, "events.html")

def podcast_page():
    hero = page_hero("On-Demand", "Miss a show? Not anymore.",
                     "Legends on your schedule — American Standards by the Sea, studio interviews, and specialty "
                     "shows, streaming free between broadcasts.", "podcast.html")
    cards = ""
    for i, p in enumerate(ON_DEMAND):
        cards += (
            '<article class="card reveal reveal-d%d" style="display:flex;flex-direction:column">'
            '<div class="ic" style="width:54px;height:54px;display:grid;place-items:center;border-radius:14px;'
            'border:1px solid var(--line);background:rgba(231,197,114,.06);color:var(--gold);margin-bottom:1.1rem">%s</div>'
            '<h3 style="font-size:1.25rem;margin-bottom:.25rem">%s</h3>'
            '<p style="color:var(--gold);font-weight:600;font-size:.9rem;margin-bottom:.7rem">%s</p>'
            '<p style="color:var(--muted);font-size:.95rem;flex:1">%s</p>'
            '<div class="mt-3"><a class="link-arrow" href="%s" target="_blank" rel="noopener">%s %s</a></div>'
            '</article>'
        ) % (i % 4, IC[p["icon"]], p["title"], p["host"], p["blurb"], p["url"], p["cta"], IC["external"])
    grid = ('<section class="section"><div class="container"><div class="grid grid-2">' + cards + '</div>'
            '<p class="form-note center mt-4">More on the way — the on-demand library grows every week. Follow '
            '<a href="' + STATION["soundcloud"] + '" target="_blank" rel="noopener" style="color:var(--gold)">SoundCloud</a> '
            'and <a href="' + STATION["instagram"] + '" target="_blank" rel="noopener" style="color:var(--gold)">Instagram</a> for the latest.</p>'
            '</div></section>')
    body = hero + grid + cta_band("Prefer it live?",
                                  "The Great American Songbook is playing right now on 100.3 FM.",
                                  secondary=("shows.html", "See the Schedule"))
    return document("podcast.html",
                    "On-Demand & Podcasts | Legends Radio 100.3 FM",
                    "Stream Legends Radio on demand — American Standards by the Sea, the Legends Radio archive, "
                    "The Sounds of Sinatra, and Cindy on Legends. Free between broadcasts.",
                    body, "podcast.html")

def advertise_page():
    hero = page_hero("Advertise", "Reach the Palm Beaches.",
                     "Legends 100.3 delivers a loyal, affluent, engaged audience across the Palm Beaches — on FM, "
                     "streaming, mobile, and in the community. Let’s put your brand in legendary company.", "advertise.html")
    why = [
        ("users", "A loyal, affluent audience", "Legends reaches engaged adults 45+ across one of the country’s most affluent markets — listeners who trust the station and stay for hours."),
        ("radio", "Live, local &amp; multi-platform", "One buy reaches listeners on 100.3 FM, the worldwide stream, the iOS &amp; Android apps, and the station’s social channels."),
        ("mic", "Host endorsements that land", "Real hosts, real trust. Live reads and endorsements from voices your customers invite into their day carry weight a banner never will."),
        ("megaphone", "Syndicated reach", "Programs like <em>American Standards by the Sea</em> extend your message to 75+ stations nationwide."),
        ("ticket", "Events &amp; sponsorships", "Put your brand on stage with supper clubs, live broadcasts, and community nights across Palm Beach County."),
        ("heart", "Community goodwill", "Align with a station the Palm Beaches genuinely love — and the causes it champions."),
    ]
    cards = "".join(
        '<article class="card reveal reveal-d%d"><div class="ic" style="width:52px;height:52px;display:grid;place-items:center;'
        'border-radius:14px;border:1px solid var(--line);background:rgba(231,197,114,.06);color:var(--gold);margin-bottom:1rem">%s</div>'
        '<h3 style="font-size:1.2rem;margin-bottom:.4rem">%s</h3><p style="color:var(--muted);font-size:.95rem">%s</p></article>'
        % (i % 4, IC[ic], t, p) for i, (ic, t, p) in enumerate(why))
    grid = ('<section class="section"><div class="container">'
            '<div class="section-head center"><span class="eyebrow centered">Why Legends</span>'
            '<h2>Legendary company for your brand</h2></div>'
            '<div class="grid grid-3">' + cards + '</div></div></section>')
    form = (
        '<section class="section surface"><div class="container"><div class="split">'
        '<div class="reveal">' + eyebrow("Let’s Talk") +
        '<h2 style="margin:.7rem 0 1rem">Start the conversation</h2>'
        '<p class="lede">Tell us a little about your business and goals. Our team will follow up with a custom '
        'plan — on-air, streaming, digital, and events.</p>'
        '<ul class="stack-sm mt-3" style="color:var(--muted)">'
        '<li>' + IC["phone"] + ' <a href="tel:' + STATION["phone_e164"] + '" style="color:var(--gold)">' + STATION["phone"] + '</a> · Sales &amp; Studio</li>'
        '<li style="margin-top:.6rem">' + IC["mail"] + ' <a href="mailto:' + STATION["email"] + '" style="color:var(--gold)">' + STATION["email"] + '</a></li>'
        '</ul></div>'
        '<div class="reveal reveal-d1"><form class="form card" data-endpoint="https://formsubmit.co/ajax/'
        + STATION["email"] + '" data-success="Thank you — a Legends representative will reach out shortly.">'
        '<input type="hidden" name="_subject" value="New advertising inquiry — legendsradio.com">'
        '<div class="row"><div class="field"><label for="ad-name">Name</label><input id="ad-name" name="name" required></div>'
        '<div class="field"><label for="ad-co">Company</label><input id="ad-co" name="company" required></div></div>'
        '<div class="row"><div class="field"><label for="ad-email">Email</label><input id="ad-email" type="email" name="email" required></div>'
        '<div class="field"><label for="ad-phone">Phone</label><input id="ad-phone" type="tel" name="phone"></div></div>'
        '<div class="field"><label for="ad-msg">What are you hoping to promote?</label>'
        '<textarea id="ad-msg" name="message" required placeholder="Tell us about your business, timing, and goals…"></textarea></div>'
        '<button class="btn btn-primary" type="submit">Request a Media Kit ' + IC["arrow"] + '</button>'
        '<div class="form-status" role="status"></div></form></div>'
        '</div></div></section>'
    )
    body = hero + why_stats() + grid + form
    return document("advertise.html",
                    "Advertise on Legends Radio 100.3 FM | Palm Beach Radio Advertising",
                    "Advertise on Legends Radio 100.3 FM and reach an affluent, loyal audience across the Palm "
                    "Beaches — FM, streaming, mobile, syndication, and events. Request a media kit today.",
                    body, "advertise.html")

def why_stats():
    return (
        '<section class="section-tight"><div class="container-wide"><div class="stats">'
        '<div class="stat"><div class="num">45+</div><div class="lbl">Core Audience</div></div>'
        '<div class="stat"><div class="num">4</div><div class="lbl">Platforms · FM · Stream · App · Events</div></div>'
        '<div class="stat"><div class="num" data-count="75" data-suffix="+"></div><div class="lbl">Syndicated Stations</div></div>'
        '<div class="stat"><div class="num">24/7</div><div class="lbl">Always On</div></div>'
        '</div></div></section>'
    )

def contact_page():
    s = STATION
    hero = page_hero("Contact", "Say hello.",
                     "Requests, dedications, advertising, events, or just to tell us what you love — we’d love to "
                     "hear from you.", "contact.html")
    maps_q = html.escape("%s, %s, %s %s" % (s["addr_street"], s["addr_city"], s["addr_region"], s["addr_zip"]))
    maps_link = "https://www.google.com/maps/search/?api=1&query=" + maps_q
    info = (
        '<section class="section"><div class="container"><div class="grid grid-2" style="gap:2.4rem;align-items:start">'
        '<div class="reveal">'
        '<div class="card"><h3 style="margin-bottom:1.2rem">Studio &amp; Offices</h3>'
        '<ul class="footer-contact" style="font-size:1rem">'
        '<li>' + IC["pin"] + '<a href="' + maps_link + '" target="_blank" rel="noopener">' + s["addr_street"] + '<br>' +
        s["addr_city"] + ', ' + s["addr_region"] + ' ' + s["addr_zip"] + '</a></li>'
        '<li>' + IC["phone"] + '<div><a href="tel:' + s["phone_e164"] + '">' + s["phone"] + '</a><br>'
        '<span style="color:var(--muted-2);font-size:.85rem">Studio &amp; Sales</span></div></li>'
        '<li>' + IC["mic"] + '<div><a href="tel:' + s["request_e164"] + '">' + s["request"] + '</a><br>'
        '<span style="color:var(--muted-2);font-size:.85rem">On-Air Request Line</span></div></li>'
        '<li>' + IC["mail"] + '<a href="mailto:' + s["email"] + '">' + s["email"] + '</a></li>'
        '</ul>' + social_links("foot-social") + '</div>'
        '<div class="mt-3 deco-frame" style="aspect-ratio:16/10;padding:2.2rem;text-align:center;'
        'display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.1rem">'
        '<div style="width:66px;height:66px;display:grid;place-items:center;border-radius:50%;'
        'border:1px solid var(--line);background:rgba(231,197,114,.06);color:var(--gold);position:relative;z-index:1">'
        '<span style="width:30px">' + IC["pin"] + '</span></div>'
        '<div style="position:relative;z-index:1"><div style="font-family:var(--serif);font-size:1.5rem;color:#fff">North Palm Beach, Florida</div>'
        '<div style="color:var(--muted);font-size:.92rem;margin-top:.3rem">' + s["addr_street"] + ' · ' + s["addr_zip"] + '</div></div>'
        '<a class="btn btn-primary btn-sm" href="' + maps_link + '" target="_blank" rel="noopener" style="position:relative;z-index:1">'
        + IC["pin"] + ' Get Directions</a></div></div>'
        '<div class="reveal reveal-d1"><form class="form card" data-endpoint="https://formsubmit.co/ajax/'
        + s["email"] + '" data-success="Thank you — we’ll be in touch soon. Keep it locked on 100.3!">'
        '<input type="hidden" name="_subject" value="New message from legendsradio.com">'
        '<div class="row"><div class="field"><label for="c-name">Name</label><input id="c-name" name="name" required></div>'
        '<div class="field"><label for="c-email">Email</label><input id="c-email" type="email" name="email" required></div></div>'
        '<div class="row"><div class="field"><label for="c-phone">Phone</label><input id="c-phone" type="tel" name="phone"></div>'
        '<div class="field"><label for="c-topic">Reason</label><select id="c-topic" name="topic">'
        '<option>General</option><option>Song Request / Dedication</option><option>Advertising</option>'
        '<option>Events</option><option>Careers</option></select></div></div>'
        '<div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" required></textarea></div>'
        '<button class="btn btn-primary" type="submit">Send Message ' + IC["arrow"] + '</button>'
        '<div class="form-status" role="status"></div></form></div>'
        '</div></div></section>'
    )
    body = hero + info
    return document("contact.html",
                    "Contact | Legends Radio 100.3 FM · Palm Beaches",
                    "Contact Legends Radio 100.3 FM in North Palm Beach — studio " + s["phone"] + ", request line "
                    + s["request"] + ", or " + s["email"] + ". Requests, advertising, events and more.",
                    body, "contact.html")

def not_found_page():
    body = (
        '<section class="page-hero" style="min-height:70vh;display:flex;align-items:center">'
        + deco_bar() + '<div class="container">'
        + eyebrow("404", True) +
        '<h1 style="font-size:clamp(3rem,9vw,6rem)">Off the dial</h1>'
        '<p>We couldn’t tune in that page — but the music’s still playing.</p>'
        '<div class="hero-actions" style="justify-content:center;margin-top:2rem">'
        '<button class="btn btn-primary btn-lg" data-play data-play-label-text="Listen Live">'
        '<span class="eq eq-mini" aria-hidden="true"><i></i><i></i><i></i></span>'
        '<span data-play-label>Listen Live</span></button>'
        '<a class="btn btn-ghost btn-lg" href="index.html">Back Home ' + IC["arrow"] + '</a>'
        '</div></div></section>'
    )
    return document("404.html", "Page Not Found | Legends Radio 100.3 FM",
                    "That page is off the dial — head back home and keep listening to Legends Radio 100.3 FM.",
                    body, "")

# ---------------------------------------------------------------------------
def fmt12(hhmm):
    h, m = int(hhmm[:2]), int(hhmm[3:5])
    if h == 24:
        h = 0
    ap = "PM" if h >= 12 else "AM"
    h12 = h % 12 or 12
    return ("%d:%02d %s" % (h12, m, ap)) if m else ("%d %s" % (h12, ap))

# ===========================================================================
# SEO FILES
# ===========================================================================
PAGES = ["index.html", "listen.html", "shows.html", "hosts.html", "podcast.html", "events.html",
         "about.html", "advertise.html", "contact.html"]

def build_sitemap():
    urls = ""
    for p in PAGES:
        loc = BASE + "/" + ("" if p == "index.html" else p)
        pri = "1.0" if p == "index.html" else ("0.9" if p in ("listen.html", "shows.html") else "0.7")
        urls += ("<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq>"
                 "<priority>%s</priority></url>") % (loc, BUILT, pri)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>'

def build_robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE

def build_manifest():
    return json.dumps({
        "name": STATION["name"], "short_name": "Legends 100.3",
        "description": "The Great American Songbook, live from the Palm Beaches.",
        "start_url": "index.html", "display": "standalone",
        "background_color": "#0A0B16", "theme_color": "#0A0B16",
        "icons": [
            {"src": "assets/img/favicon.png", "sizes": "512x512", "type": "image/png"},
            {"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
        ],
    }, indent=2)

# ===========================================================================
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return len(content)

def main():
    global CSS_V, JS_V
    CSS_V = asset_v("assets/css/legends.css")
    JS_V = asset_v("assets/js/legends.js")
    pages = {
        "index.html": home_page(), "listen.html": listen_page(), "shows.html": shows_page(),
        "hosts.html": hosts_page(), "podcast.html": podcast_page(), "events.html": events_page(),
        "about.html": about_page(), "advertise.html": advertise_page(), "contact.html": contact_page(),
        "404.html": not_found_page(),
    }
    total = 0
    for path, content in pages.items():
        total += write(path, content)
    write("sitemap.xml", build_sitemap())
    write("robots.txt", build_robots())
    write("site.webmanifest", build_manifest())
    print("Built %d pages + sitemap/robots/manifest (%d KB) · css v=%s js v=%s"
          % (len(pages), total // 1024, CSS_V, JS_V))
    print("Preview:  python3 -m http.server 8000  →  http://localhost:8000/legends-radio/")

if __name__ == "__main__":
    main()
