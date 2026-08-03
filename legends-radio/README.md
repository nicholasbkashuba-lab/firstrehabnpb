# Legends Radio 100.3 FM — website (redesign concept)

A dynamic, premium marketing + streaming site for **Legends Radio 100.3 FM (WLML-FM)**,
"Where Legendary Music Lives" — the Great American Songbook, live & local from Florida's
Palm Beaches. Built as a self-contained static site with the same philosophy as the rest
of this repo: **`build.py` is the single source of truth.**

> This lives in the `legends-radio/` subfolder so it can be previewed on this project's
> Vercel deploy at `/legends-radio/` without touching the First Rehab site. It is designed
> to move to its own domain unchanged (all internal links are relative).

## What's in the box
- **8 pages + 404**: Home, Listen Live, Shows & Schedule, On-Air Personalities, Events,
  About, Advertise, Contact.
- **A persistent live player** wired to the real WLML stream
  (`https://ice3.securenetsystems.net/WLML`), with volume persistence, animated
  equalizer + spinning vinyl, OS media-session metadata, and a pop-out fallback if the
  stream can't play cross-origin.
- **A client-side "On Air Now / Up Next" engine** computed in the station's Eastern time,
  so the hero card, the sticky player, and the weekly schedule grid always show the show
  that's actually on — no backend required.
- **Art Deco / supper-club design system** (midnight + gold + oxblood, Playfair Display +
  Inter, self-hosted): cinematic hero lighting, film grain, legends marquee, schedule grid
  with a live progress bar, host medallions, scroll reveals, count-ups.
- **SEO**: unique title/description/canonical, Open Graph + Twitter cards, JSON-LD
  (`RadioStation` + `BroadcastService` + `Person` + `ItemList` + `BreadcrumbList`),
  `sitemap.xml`, `robots.txt`, `site.webmanifest`, favicons + Apple touch icon + OG image.
- **Fully accessible & fast**: skip link, focus states, `prefers-reduced-motion` support,
  self-hosted fonts, no third-party trackers, no external runtime dependencies.

## Architecture
- **`build.py`** — all content (station facts, hosts, shows, weekly schedule, events,
  artists) + the page templates + SEO file generation. Edit it, then rebuild.
- **`assets/css/legends.css`** — the whole design system (hand-written).
- **`assets/js/legends.js`** — player, On-Air engine, schedule tabs, reveals, counters,
  marquee cloning, mobile nav, forms. Zero dependencies. Consumes `window.LEGENDS_*`
  data injected by `build.py`.
- **`assets/img/`** — SVG emblem/favicon + generated PNGs (favicon, apple-touch, OG,
  media-session artwork). No fabricated photos of real people.
- **`assets/fonts/`** — self-hosted Playfair Display + Inter (woff2).

## Build & preview
```bash
cd legends-radio
python3 build.py
# from the repo root:
python3 -m http.server 8000   # →  http://localhost:8000/legends-radio/
```
CSS/JS links carry build-time content-hash cache-busters (`asset_v()`), matching the
convention in the rest of this repo.

## Facts & sourcing
Station facts are grounded in public sources (WLML-FM / legendsradio.com): call sign,
100.3 FM, licensed to Lake Park FL, founded 2014 by Dick Robinson, studio at 760 US
Highway 1 Ste 102 North Palm Beach, business line 561-469-6700, request line
561-685-9565, `info@legendsradio.com`. Confirmed shows/hosts: **The Morning Lounge**
(Jill & Rich Switzer), **Middays** (Walt Pinto), **Afternoons** (Lorna O'Connell),
**American Standards by the Sea** (Dick Robinson), **The Golf & Travel Show**
(Dan Shube & Doris Muscarella). No credentials, quotes, or events were invented.

## Owner to-dos
- **Canonical domain** — `BASE` in `build.py` is `https://www.legendsradio.com`. If this
  is deployed somewhere else permanently, update `BASE` and rebuild.
- **Live stream** — the player uses the real SecureNetSystems mount. It plays in a normal
  browser; if SecureNet ever hotlink-protects it, the pop-out button opens
  `legendsradio.com/listen-live`. Hosting on the `legendsradio.com` domain makes the
  referer match and is the most robust option.
- **Contact/advertise/request forms** — they POST to
  `formsubmit.co/ajax/info@legendsradio.com`. FormSubmit sends a **one-time activation
  email** to that inbox on the first submission (check spam); click it once to turn the
  forms on. (Or swap in a real backend endpoint.)
- **Schedule** — confirmed hosted shows: The Morning Lounge (Jill & Rich Switzer),
  Middays w/ Walt Pinto (Legends at Lunch @ noon), Afternoons w/ Lorna O'Connell,
  American Standards by the Sea (Dick Robinson), Legends of Jazz (Gregory "Popeye"
  Alexander), Late Nights with Legends, The Golf & Travel Show (Dan Shube & Doris
  Muscarella), Inspired To Be (Sherrye Fenton). The **overnight/weekend music blocks**
  (Nonstop Legends, Legends Evenings, Saturday Morning Swing, etc.) are descriptive
  placeholders — replace with the real grid in `SCHEDULE`.
- **Host photos** — medallions use monogram initials (no fabricated portraits). Add real
  portraits and wire them in when available.
- **Events** — cards route to the station's Eventbrite (no fabricated dates). The
  "Live Concerts at Abacoa" series and tribute acts are real; specific show dates live on
  Eventbrite (verify before hard-coding any date).
- **Now Playing** — shows the current *show* (always accurate). If SecureNet exposes a
  CORS-enabled now-playing endpoint, live track/artist metadata could be layered on.

### Confirm with owner (from the 2026-07 research audit)
The current legendsradio.com blocks bots, so these were third-party-sourced — please verify:
- **Afternoon-drive host** — sourced as Lorna O'Connell, but older indexed snippets show
  other names on `/afternoons/`. Confirm the current live host.
- **"Inspired To Be" (Sherrye Fenton)** air day/time (listed as "Weekly · See schedule").
- **Overnight hours** outside the confirmed 11 PM–1 AM Late Nights block (assumed automated).
- **ASbtS affiliate count** — used "75+"; confirm exact number.
- **Brand assets** — the script wordmark, red palette, and red/white/blue musical-note
  flag emblem are recreated from the owner-supplied logo; drop in the official vector /
  exact hex values to make them pixel-perfect.
- **Excluded as historical (not current on-air):** Angela Manfredi, Steve Ketelaar, Taylor
  Morgan, Paul Cavenaugh, Toni May — confirm none should be reinstated.
- **Studio address** — using 760 US Highway 1, Ste 102, North Palm Beach 33408 (license
  city is Lake Park); confirm the correct public studio/mailing address.

## 2026-08 — lineup correction + real station imagery

The original build sourced its lineup from third-party pages because
legendsradio.com returns 403 to automated clients. Those sources were stale.
The lineup was re-derived from the station's **own** pages (fetched via a
GitHub Actions relay, which has open egress) and from the station's current
"Your Weekdays Lineup" graphic.

Corrected weekday lineup (per the station's own graphic, July 2026):

| Slot | Host | Show |
|---|---|---|
| 6a–10a  | Jill & Rich Switzer | The Morning Lounge |
| 10a–2p  | Mike McGann         | Middays with Mike McGann |
| 2p–7p   | Steve Ketelaar      | Legends Afternoons |
| 7p–9p   | Alex Donner         | Evenings with Alex Donner |
| 9p–11p  | Bob Merrill         | Legends After Dark |
| 11p–1a  | Dick Robinson       | American Standards by the Sea |

Also on air: Gregory "Popeye" Alexander (Legends of Jazz), Cindy Hite
(Cindy on Legends), Lauren May, Bob Merrill (Sunday Legends Brunch),
The Sounds of Sinatra.

**Removed as not-current:** Walt Pinto, Lorna O'Connell, Sherrye Fenton /
"Inspired To Be", and The Golf & Travel Show (Dan Shube & Doris Muscarella).
Steve Ketelaar had previously been excluded as "historical" — he is in fact
the current afternoon host.

### Owner confirmations still needed
- **Morning Lounge start time.** The lineup graphic says 6a; the Morning
  Lounge page says "Weekdays 5:00 AM – 10:00 AM". The site currently uses 6a.
- **Host bios.** Only Jill & Rich and Dick Robinson have substantive bios.
  The rest are deliberately minimal factual lines — no credentials were
  invented. Please supply proper bios.
- **Weekend/specialty slot times** for Legends of Jazz, Cindy on Legends,
  Lauren May and Sounds of Sinatra are not published on the station site.

### Image provenance
`assets/hosts/*` are the station's own photographs, taken from
legendsradio.com for use on the station's own new site. **Advertiser creative
was deliberately excluded** (Alaina's Cafe, Harbourside/BurgerFi, Uncle
Eddie's, Bake Me A Wish etc.) — that artwork belongs to the advertisers, not
the station. Confirm the station holds rights to each host portrait before
launch.
