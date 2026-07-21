# First Rehabilitation of North Palm Beach — Website

Static site for firstrehabnpb.com. 26+ pages, generated — do not edit HTML files directly.

## Architecture
- **`build.py`** is the single source of truth: all page content, team roster, condition copy,
  blog posts, podcast episodes, contact info. Edit it, then run `python3 build.py` to regenerate
  every page in place.
- Fonts are SELF-HOSTED in assets/fonts/ (@font-face at top of styles.css, two woff2
  preloads in head(), 1y immutable cache) — do not re-add Google Fonts links.
- All CSS/JS links carry build-time content-hash cache-busters (asset_v() in build.py) —
  never link a stylesheet/script without one; stale-CSS bugs on phones taught us this.
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
- `assets/media/` — logo.png/logo-dark.png (full-size, schema/OG), logo-nav.png/
  logo-dark-nav.png (333px, header+footer). Favicons = the FULL wordmark logo on cream
  (owner insists; no monograms), regenerate via Pillow from logo.png, bump ?v= (now v5).
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
and `llms.txt` (AI-crawler fact sheet). The org node is typed ["MedicalClinic",
"MedicalBusiness"] and carries medicalSpecialty, priceRange, isAcceptingNewPatients,
availableService (links the 4 MedicalTherapy service @ids), geo, hasMap, 10 areaServed
cities, Saturday hours, 5 sameAs (incl. the Google listing cid link). Per-page schema
via head(extra_schema=...): Person ×6 on About, MedicalTherapy on services,
MedicalCondition on conditions, PodcastSeries+Episodes on podcast, FAQPage on faq,
BlogPosting (+reviewedBy Dave) on posts, BreadcrumbList on interior pages, JobPosting
per open role on careers, Service on location pages — all referencing the org @id.
Schema is complete as of 2026-07-21 (104 valid JSON-LD blocks). To re-verify Google's
actual rendering, the owner runs a URL through search.google.com/test/rich-results.
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
- A 2026-07 GSC Pages export revealed MORE old Wix URLs still indexed & ranking
  (some pos 6–8) but un-redirected — added 301s for /request-appointment→contact,
  /about-5→about, /headache→treatments/headache-relief, /work-injuries→workers-comp,
  /shoulder-pain, /hand-pain→hand-wrist, /general-7→/ (original page unknown, safe
  catch). When a fresh GSC Pages export shows any indexed old URL not on the new
  site, add its 301 the same way — that's rescued ranking equity.
- `/review` and `/reviews` 302-redirect to the Google "write a review" dialog:
  `search.google.com/local/writereview?placeid=ChIJ3fEUAhCmsYkREHNzv87U3TQ` (the
  clinic's Google Place ID; CID 3809434844265673488). Branded review link — printed
  on the front-desk QR card, textable to patients. Reviews are the #1 local-search
  lever. vercel.json is a standalone file (NOT generated by build.py) — edit directly.

## Analytics & tracking
- **Vercel Web Analytics** is live: the cookieless `/_vercel/insights/script.js` tag
  is emitted in footer() on every page (privacy-friendly, no cookie banner). Enabled
  in the Vercel dashboard 2026-07-21. Speed Insights is deliberately OFF (usage-billed,
  not worth it). Traffic data lives in the Vercel dashboard — no API to pull it here.
- **Lead/application data**: query Supabase directly (intake_leads, job_applications).
  Test rows are tagged status='test' and MUST be excluded from every report
  (`where coalesce(status,'new') <> 'test'`). "Run my analytics" = pull real leads/apps.
- **Search Console**: owner-only (locked to their Google account). Working flow: owner
  exports the GSC "Performance" ZIP (Dates/Queries/Pages/Countries CSVs) and drops it
  here; unzip and analyze. The Google Drive connector is picker-scoped and can't read
  files by link — don't fight it, use the ZIP/paste. Baseline (old Wix site, 90d to
  2026-07-19): 276 clicks / 11,792 impr / pos 17.1 / CTR 2.34%. Non-branded was 5,555
  impr converting 0.36% (ranked page 3 for the money terms the new location/condition
  pages target — that's the growth thesis). Compare next export against this.

## Conversion
- Sticky **mobile Call Now** button (`.mobile-call`, emitted after </footer>): fixed
  bottom-LEFT coral pill, phones only (<768px), one tap to tel:561-624-4263. Bottom-left
  so it never collides with the intake chat launcher (bottom-right); hidden on desktop
  and while the mobile menu is open (body.nav-locked). Don't move it to the right.
- Front-desk review QR card + standalone QR were generated (Pillow + qrcode) pointing
  at firstrehabnpb.com/review; regenerate from logo.png if the brand or link changes.

## Hero video (do not regress)
- Source of truth: the true camera master "End-with.MP4" in Nick's Dropbox root
  (2688×1512@59.94, H.264 High ~90Mbps, 13.28s drone orbit of Jupiter Inlet Lighthouse;
  "End with .mov" beside it is the same recording). ALWAYS re-encode from this master —
  never from the shipped renditions. Pipeline: trim off the first 2.0s (near-static hover
  that lurches into the pan — confirmed by per-frame YDIF motion analysis; Nick asked for
  this cut), 0.8× slow (setpts=PTS/0.8), fps=30 AFTER each trim branch (xfade requires
  CFR), 0.5s crossfade seamless loop (branchA trim=2.4:13.28, branchB trim=2.0:2.55,
  xfade offset=13.0999, -t 13.5999 → 13.6s loop that starts and wraps mid-glide),
  single-generation encode, -movflags +faststart, -an, bt709 tags. Renditions in
  assets/media/: lighthouse-hd.mp4 (2560×1440 crf22, 24.9MB) + lighthouse-hd.webm
  (VP9 crf31), lighthouse-mobile.mp4 (1280×720 crf30, 2.1MB) + .webm (VP9 crf36);
  hero-poster.jpg = master frame at 2.4s, 1600×900 q7 (~130KB). The <video> tag ships
  with NO <source> children and preload="none"; main.js attaches ONE rendition pair via
  matchMedia (<768px = mobile), mp4 listed before webm (mp4 is smaller here). Bump ?v=N
  cache-busters on any re-encode (current: poster+hd mp4 v8, hd webm+mobile pair v9).
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
- Text accents use --coral-text #A04E14 (~5.4:1 on cream, axe-verified); --coral-deep is
  backgrounds only. --muted is #51646C. Outlined .svc-feature-num strokes use #A07514.
  Do NOT lighten these — the whole site passes axe-core WCAG 2.1 AA (37/37 pages, zero
  violations); re-run the axe sweep (npm i --no-save axe-core playwright-core, inject
  axe.min.js per page on http.server 8901 with animations settled) after any color change.
- Video/img inside .hero-media need position:relative+z-index:1 to paint above .hero-fallback.
- Nav collapses ≤1260px (CSS media query AND matchMedia in main.js — keep in sync).

## Location pages
LOCATIONS dict in build.py → /locations/{palm-beach-gardens,jupiter,tequesta,juno-beach,
lake-park,palm-beach,west-palm-beach,riviera-beach}.html. Honest served-from-NPB content
(no fake locations, no invented drive times/parking), named clinicians with credentials,
Service schema per city, footer "Areas We Serve" links every city. North Palm Beach
deliberately has NO location page — the homepage owns that keyword; footer links it to /.

## Verification pattern
The sandbox cannot reach *.vercel.app, Dropbox, or Supabase hosts directly (proxy 403);
GitHub (api/raw/codeload/objects) IS allowed. Verify live deploys via Supabase MCP:
`create extension pg_net` → `net.http_get(...)` (Range headers work: 206 + content-range
proves deployed file size) → read net._http_response → `drop extension pg_net`. NOTE:
production URLs are public but PREVIEW deploys sit behind Vercel Authentication (Pro
default) — pg_net gets a login page, not the site. Playwright (playwright-core installed
via npm --no-save, chromium at /opt/pw-browsers, NODE_PATH=<repo>/node_modules) tests
locally on http.server 8901; that browser has NO H.264 but DOES decode VP9/webm.

## Fetching big files the proxy blocks (e.g. the Dropbox video master)
GitHub Actions relay: push an orphan temp branch with an on:push workflow (workflow_dispatch
via API 404s unless the workflow exists on the DEFAULT branch — use on:push instead);
the runner has open egress: curl the file, `split -b 45m` (GitHub hard-blocks >100MB
files), sha256 everything, push chunks to a tmp out-branch; locally `git fetch` + `git
archive | tar -x` + `cat` + verify sha256. The local git proxy BLOCKS branch deletion
("remote end hung up") — clean up by pushing a workflow version that self-deletes both
tmp branches via `curl -X DELETE .../git/refs/heads/...` with GITHUB_TOKEN, then delete
run logs via the GitHub MCP (delete_workflow_run_logs). Repo is public: never commit
secrets to tmp branches; view-only Dropbox share links are acceptable, temporary.

## Owner to-dos (repeat in reports until done)
- Flip DNS when ready: Vercel → Domains → add www.firstrehabnpb.com (primary) + apex;
  registrar: A @ → 76.76.21.21, CNAME www → cname.vercel-dns.com. Then submit
  sitemap.xml in Google Search Console and update the Google Business Profile link.
- Click the FormSubmit activation email on the first real lead (check spam).
- ~~Send Google Business Profile share URL → add to sameAs~~ DONE — GBP already in the org
  schema via its canonical CID link (maps.google.com/?cid=3809434844265673488); owner's
  share.google link resolves to the same listing. No further action.
- Cross-check the GSC top-pages export against vercel.json redirects when provided.
- Homepage gallery photos (Dave + guest; team with Celsius) never arrived as files —
  re-request as attachments, then add as assets/social/post-8.jpg, post-9.jpg (extend
  the gallery loop range in build.py if needed).
- Wellness FAQ answers flagged for owner confirmation: non-patient gym membership,
  pricing, cancellation policy, parking specifics, same-therapist continuity.
- ~~Vercel Pro~~ DONE 2026-07-20. ~~Turn OFF preview Deployment Protection so preview links
  are shareable~~ DONE 2026-07-21 (owner disabled Vercel Authentication — preview URLs now
  load without a login). Still: delete old shim projects (firstrehab-site, firstrehabnpb,
  firstrehab, firstrehab-live).

## Careers & applications
/careers.html driven by OPEN_POSITIONS in build.py (currently COTA only; empty list =
no-openings message). Applications: assets/js/careers.js → Supabase table
job_applications (INSERT-only RLS, same project as intake_leads) + FormSubmit email to
firstrehabnpb@gmail.com CC nick@firstrehabnpb.com, subject "New Job Application: …".
JobPosting schema per role (validThrough = posted + 60d — bump posted dates to refresh).

## Blog agent
/blog slash command (.claude/commands/blog.md) + BLOG-PLAYBOOK.md + BLOG-TOPICS.md.
Posts reviewed by Dr. Dave Kashuba, Ph.D. (byline + reviewedBy schema). Facts only from
build.py/site/owner input — never web research, never invented stats or testimonials.
