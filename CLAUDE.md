# First Rehabilitation of North Palm Beach — Website

Static site for firstrehabnpb.com. 26+ pages, generated — do not edit HTML files directly.

## Architecture
- **`build.py`** is the single source of truth: all page content, team roster, condition copy,
  blog posts, podcast episodes, contact info. Edit it, then run `python3 build.py` to regenerate
  every page in place.
- `assets/css/styles.css` — the whole design system (deep teal #0E3A47, cream #F6F1E7,
  coral #F4A261, gold #E9C46A; Playfair Display + Inter). Signature elements: rotating
  lighthouse beam on dark sections, film grain, interactive body map, social marquee.
- `assets/js/main.js` — hero video source picker, nav (Escape closes mobile menu),
  scroll reveals, counters (reduced-motion aware), seamless marquees, body-map attract
  cycle + tap panel, FAQ filter bubbles/search/expand (arrow keys switch categories).
- `assets/js/intake.js` + `assets/css/intake.css` — the intake assistant (chat popup on every
  page). "Ask a question" serves SET ANSWERS from the FAQ array in intake.js (no AI, no
  external API — edit those answers there and keep them factually accurate: no medical
  advice, route unknowns to the front desk at 561-624-4263). Appointment requests collect
  contact info conversationally; answers are drafted to localStorage at every step;
  submissions deliver two ways at once (deliverLead): insert into the Supabase project
  "First Rehabilitation App" (table `intake_leads`, anon key is INSERT-only via RLS) AND
  email firstrehabnpb@gmail.com via FormSubmit — either channel succeeding counts; if both
  fail the lead queues locally + auto-retries. View leads in the Supabase dashboard →
  Table Editor → intake_leads.
- `assets/media/` — logo.png (light backgrounds), logo-dark.png (dark backgrounds),
  hero video renditions (see Hero Video below), hero-poster.jpg, podcast-cover.jpg, photos.
- `assets/team/` — staff portraits. `assets/social/post-1..8.jpg` — homepage gallery tiles.

## Workflow
1. Edit `build.py` (or CSS/JS)
2. `python3 build.py`
3. Preview locally: `python3 -m http.server 8000` → http://localhost:8000
4. Commit & push → Vercel auto-deploys

## Conventions
- Phone 561-624-4263 · 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408
- Tagline: "Our people make the difference." · Motto headline: Heal. Strengthen. Thrive.
- New blog post: add to BLOG_POSTS dict. New episode: add to the TOP of EPISODES with
  its Spotify episode URL — EPISODES[0] automatically becomes the featured "Latest
  Episode" card on the podcast page and joins the PodcastEpisode schema.
  New team member: add to TEAM + photo in assets/team/ (also feeds Person schema).
- Main FAQ content lives in FAQ_CATEGORIES in build.py (8 filterable categories, 73 Q&As).
  Answers are PLAIN TEXT (they feed both the accordions and the single FAQPage JSON-LD,
  which must stay in sync — it's generated from the same data, so just rebuild). Service
  pages cross-link to /faq.html#category anchors instead of duplicating Q&As.
- Keep quotes/testimonials verbatim; don't invent credentials or clinical claims.
- Intake agent copy lives in `assets/js/intake.js` (STEPS object). It is plain JS served
  to every visitor — never put secret keys in it (the Supabase publishable key is safe by design).

## SEO — keep this maximized on every change
The build already emits, for every page: a unique `<title>` and meta description, a
`rel=canonical` URL, Open Graph + Twitter Card tags, MedicalBusiness JSON-LD schema
(stable @id https://www.firstrehabnpb.com/#organization with legalName/alternateName/
founder/hasMap/City areaServed), favicons/apple-touch/manifest, `sitemap.xml`, `robots.txt`,
and `llms.txt` (AI-crawler fact sheet). Per-page schema via head(extra_schema=...):
Person ×6 on About, MedicalTherapy on services, MedicalCondition on conditions,
PodcastSeries+Episodes on podcast, FAQPage on faq, BlogPosting on posts, BreadcrumbList
on interior pages, Service on location pages — all referencing the org @id.
DELIBERATE: no aggregateRating in our own schema (self-serving review markup violates
Google's guidelines — the Google Business Profile carries the review signal). Do not re-add.
When adding or changing pages, preserve all of it:

- Every new page MUST pass a unique `title`, `desc`, and `canonical=` to `head()`.
  Titles: ~50–60 chars, front-load the keyword + "North Palm Beach". Descriptions: ~150–160 chars.
- Add every new page's URL to the `pages` list in `build_meta()` so it enters sitemap.xml.
- Blog posts and condition pages pass `page_type="article"`. Keep one `<h1>` per page
  (the page hero), with `<h2>`s for structure — never skip heading levels.
- Keep image `alt` text descriptive and location-aware where natural.
- Don't remove the JSON-LD block, canonical tags, or the sitemap/robots/manifest generation.
- If the domain ever changes from firstrehabnpb.com, update `base` in `head()` and `build_meta()`.
- After any build, sitemap.xml must list every live page and robots.txt must point to it.

Local SEO priorities for this business: "physical therapy North Palm Beach", "hand therapy
Palm Beach Gardens", "occupational therapy Jupiter FL", plus each condition + location.

## Redirects — DO NOT REMOVE
`vercel.json` carries 301 redirects mapping every URL of the old Wix site
(including the /blank-N condition pages and /service-page/ booking URLs) to its
new equivalent. These preserve the search rankings earned by the old site.
Google takes months to transfer ranking signals to the new URLs — keep these
redirects in place permanently, or at absolute minimum 12 months after the
domain switch (July 2027). Removing them early throws away that equity.

## Hero video (do not regress)
- Source of truth: 2688×1512@60 upload; pipeline = 0.8× slow (setpts=PTS/0.8), fps=30 AFTER
  each trim branch (xfade requires CFR), 0.5s crossfade seamless loop, single-generation
  encode, -movflags +faststart, -an. Renditions in assets/media/: lighthouse-hd.mp4
  (2560×1440 crf22, 8.8MB) + lighthouse-hd.webm (VP9 fallback), lighthouse-mobile.mp4
  (1280×720 crf30, 1.7MB) + .webm. The <video> tag ships with NO <source> children and
  preload="none"; main.js attaches ONE rendition pair via matchMedia (<768px = mobile),
  mp4 listed before webm (mp4 is smaller here). Bump ?v=N cache-busters on any re-encode.
- Mobile (<768px) the hero STACKS: video at native 16:9 (zero crop), panel below on ink.
  Do not restore full-bleed cover on phones — it crops ~70% of the frame.
- Perf: no backdrop-filter over the playing video, beams stay out of the hero, poster is
  1600×900 ~130KB and preloaded with fetchpriority=high.

## CSS gotchas (each was a shipped bug — don't reintroduce)
- Header backdrop-filter makes it the containing block for fixed descendants: the mobile
  menu overlay must keep the `body.nav-locked .site-header { backdrop-filter: none }`
  override or it shrinks to the header box when opened after scrolling (iOS + Chromium).
- Desktop dropdown hover/focus rule applies translateX(-50%); mobile keeps the
  `transform: none` override or tapped submenus slide half off-screen.
- Mobile menu uses justify-content: flex-start (centered flex clips the top of an
  overflowing list unreachably) + overscroll-behavior: contain.
- Marquees/tickers: spacing must be per-item margins (not flex gap) and tilt classes are
  assigned in JS before cloning — both keep the -50% loop seamless.
- Text accents use --coral-text #B65717 (AA 4.8:1); --coral-deep is for backgrounds only.
- Video/img inside .hero-media need position:relative+z-index:1 to paint above .hero-fallback.
- Nav collapses ≤1260px (CSS media query AND matchMedia in main.js — keep in sync).

## Location pages
LOCATIONS dict in build.py → /locations/{palm-beach-gardens,jupiter,juno-beach}.html.
Honest served-from-NPB content (no fake locations, no invented drive times/parking),
named clinicians with credentials, Service schema per city, footer "Areas We Serve" links.

## Verification pattern
The sandbox cannot reach *.vercel.app directly (proxy 403). Verify live deploys via
Supabase MCP: `create extension pg_net` → `net.http_get(...)` → read net._http_response
→ `drop extension pg_net`. Playwright (playwright-core, chromium at /opt/pw-browsers)
tests locally on http.server 8901; that browser has NO H.264 but DOES decode VP9/webm.

## Owner to-dos (repeat in reports until done)
- Flip DNS when ready: Vercel → Domains → add www.firstrehabnpb.com (primary) + apex;
  registrar: A @ → 76.76.21.21, CNAME www → cname.vercel-dns.com. Then submit
  sitemap.xml in Google Search Console and update the Google Business Profile link.
- Click the FormSubmit activation email on the first real lead (check spam).
- Send Google Business Profile share URL → add to sameAs in the org schema.
- Cross-check the GSC top-pages export against vercel.json redirects when provided.
- Homepage gallery photos (Dave + guest; team with Celsius) never arrived as files —
  re-request as attachments, then add as assets/social/post-8.jpg, post-9.jpg (extend
  the gallery loop range in build.py if needed).
- Wellness FAQ answers flagged for owner confirmation: non-patient gym membership,
  pricing, cancellation policy, parking specifics, same-therapist continuity.
- Vercel Pro recommended (Hobby is non-commercial per Vercel ToS); delete old shim
  projects (firstrehab-site, firstrehabnpb, firstrehab, firstrehab-live).
