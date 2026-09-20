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
  **Every value lives in the `:root` token block at the top — consume tokens, never
  literals.** See "Design tokens" below before touching any colour, size or easing.
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
  fail the lead queues locally + auto-retries. A THIRD, fire-and-forget copy goes to
  nick@firstrehabnpb.com (CFG.notifyEmailCc) as its own FormSubmit POST — deliberately not
  FormSubmit's _cc (undocumented on the /ajax/ endpoint) and deliberately not counted by
  deliverLead, so it can never block or fail the clinic notification. Both emails share one
  emailFields() body builder so the two inboxes can never drift apart. View leads in the Supabase dashboard →
  Table Editor → intake_leads.
- `assets/media/` — logo.png/logo-dark.png (full-size, schema/OG), logo-nav.png/
  logo-dark-nav.png (333px, header+footer). Favicons = the FULL wordmark logo on cream
  (owner insists; no monograms), regenerate via Pillow from logo.png, bump ?v= (now v5).
  hero video renditions (see Hero Video below), hero-poster.jpg, podcast-cover.jpg, photos.
- `assets/team/` — staff portraits. `assets/social/post-1..8.jpg` — homepage gallery tiles.

## Design tokens — consume them, never write a literal
Everything visual is declared once in the `:root` block at the top of `styles.css`.
Nothing below that block may contain a literal colour, a literal shadow, or an off-scale
size. `intake.css` has no `:root` of its own — it is always loaded after `styles.css`
and consumes the same tokens.

- **Colour is declared as channel triplets** (`--ink-deep-rgb: 7 30 39`) with solid
  aliases beside them (`--ink-deep: rgb(var(--ink-deep-rgb))`). Transparency is then
  `rgb(var(--ink-deep-rgb) / 0.45)`, not a hand-written `rgba()`. This exists because
  the sheet had accumulated 88 literal `rgba()` values across 11 nearly-identical
  triplets — that is how a palette silently drifts out of sync with itself.
- **Type** rides a ~1.25 fluid modular scale, `--step--2` through `--step-6`, with
  `--leading-*` and `--measure*` beside it. Do not invent a per-selector `clamp()`.
  The only two left are viewport-scaled display graphics (the hero watermark and the
  outlined section numerals), which are drawings, not text on the reading ramp.
- **Spacing** is `--space-1`…`--space-8` (4/8/16/24/32/48/64/96) plus `--space-section*`.
- **Elevation** is four rungs, `--shadow-sm|md|lg|xl`. Pick a rung; never write a shadow.
- **Motion** uses `--ease-out|quart|inout|spring` and `--dur-fast|base|slow`. The bare
  keywords `ease`, `ease-in`, `ease-out`, `ease-in-out` are banned. The three continuous
  loops (marquee, ticker, lighthouse sweep) stay `linear` on purpose — an eased loop
  visibly stutters at the seam.
- `--coral-text`, `--gold-stroke` and `--danger-text` are the AA-safe variants for text
  and thin strokes. Do not lighten them; the site passes axe WCAG 2.1 AA at both widths.
- A `var()` naming a token no `:root` defines fails SILENTLY — the property falls back to
  inherited and the page looks almost right. `--serif` and `--teal` sat broken this way in
  three rules until 2026-09-15. verify.py now fails the build on it.

## Photography — the PHOTOS registry
`PHOTOS` in build.py is the single registry of every real photograph on the site. There
are 15 of them and that is the entire library: no stock, no illustration, no AI imagery.

- Each entry carries `src`, an `object-position` **focal point chosen by looking at the
  frame**, and `alt`. A default centre crop cuts heads off; that is what focal points are for.
- Templates call `photo(name, depth=, sizes=, ratio=, eager=)`, which emits a `<picture>`
  with WebP + JPEG, a srcset, intrinsic `width`/`height`, and the focal point applied.
  **Never hardcode an image path in a template** — schema and `og:image` read the registry too.
- `python3 tools/build-images.py` derives the renditions into `assets/img/` and writes
  `manifest.json`. Run it after adding a photo. **It never upscales**: a 680px source caps
  at 680px rather than shipping a blurry 1440, and the manifest records the real cap.
- `SERVICE_MEDIA` decides what each service page leads with. Only two services have a
  genuine photograph of that service: occupational therapy gets the treatment frame, and
  wellness gets the gym. **The treatment frame is Dave, and Dave is an Occupational
  Therapist** — it is not a physical therapy photo, and it led that page in error until
  the owner caught it. A service without a scene photo leads with a CREDITED CLINICIAN PORTRAIT
  of the person who runs it, captioned with name and credential. That is the honest
  alternative to faking a scene — do not crop a staff portrait wide and pass it off as one.
- `assets/media/founder.jpg` is the clinic BUILDING, not a portrait of the founder. Its alt
  text claimed otherwise until 2026-09-15.
- If a layout wants a photograph the registry does not have, the layout is wrong. Do not
  invent a slot and fill it with a gradient, an icon, or a grey box.

## Verifying a change — `static-site-forge`
    python3 ~/.claude/skills/static-site-forge/verify.py --root . --shots out/

Runs every check and reports all failures rather than stopping at the first: BUILD (clean
generator run, no warnings), LINKS (every internal href/src resolves; host-served runtime
paths like `/_vercel/` are exempt), IMAGES (alt present, intrinsic size, no placeholder in
a photo slot), TOKENS (no literal colour outside `:root`, and no `var()` naming an
undefined token), SEO (one `h1`, no skipped heading levels, title/description/canonical,
sitemap coverage), A11Y (axe-core WCAG 2.1 AA at 393px and 1440px with animations settled)
and SHOTS (full-page screenshots into `--shots`).

Needs `npm i --no-save playwright-core axe-core`. `--skip-browser` reports A11Y and SHOTS
as SKIPPED and exits non-zero — an unrun check must never read as a pass. Exit 0 only when
everything genuinely passes.

## Branches
`main` is the trunk as of 2026-08-15. Before that the repo had NO main branch at all: the default
was `claude/site-intake-agent-popup-hdfmxw`, a session branch that became the trunk by accident,
and Vercel served production from it. `main` was created at that branch's exact commit
(`df5a4a7`), so no content moved. Keep the old branch until production has deployed from `main`
at least once. PRs target `main`.

## Workflow
1. Edit `build.py` (or CSS/JS)
2. `python3 build.py`
3. Preview locally: `python3 -m http.server 8000` → http://localhost:8000
4. Commit & push → Vercel auto-deploys

**Step 2 is enforced by CI as of 2026-09-20.** `.github/workflows/rebuild.yml` rebuilds
the site on every PR and every push to `main` and FAILS if the committed output is not
what `build.py` generates. Before it existed, a commit could change `build.py` and leave
every page a visitor sees untouched, and nothing surfaced it. The check is read-only
(`permissions: contents: read`) — it never pushes, never commits, and cannot trigger a
deploy, so a red run means "you forgot to commit something", not "the site broke".
Commit every file the build touches, `sitemap-dates.json` included; leaving that one out
is its own failure mode and the check names it.

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
- Every blog post gets a 3-card "Related Articles" block from RELATED_POSTS in build.py.
  A new post needs an entry there AND needs adding to somebody else's list, or it ships
  with one inbound link (its card on /blog/index.html) — that was the whole finding in
  the 2026-08-23 Semrush crawl. Condition and service pages also link posts topically
  via COND_BLOG / SVC_BLOG (slugs only; link text is read from BLOG_POSTS).
- Episode blurbs in EPISODES are split into paragraphs on `<br><br>` by _paras(). Keep
  each chunk roughly 40-80 words and give an opening quote its own break; a single
  330-word <p> is a full phone screen and reads badly to crawlers and people alike.
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
BlogPosting + a WebPage node carrying reviewedBy Dave on posts (reviewedBy is a
property of WebPage, NOT of Article/BlogPosting — it hung off the BlogPosting until
2026-08-23 and validators rejected the whole item; the BlogPosting points at the
WebPage via mainEntityOfPage and the Person is referenced by @id only),
VideoObject with uploadDate on /videos.html (uploadDate is REQUIRED — no video rich
results without it, so every new VIDEOS entry needs one), BreadcrumbList on interior pages, JobPosting
per open role on careers, Service on location pages — all referencing the org @id.
Schema is complete as of 2026-08-23 (138 valid JSON-LD blocks). To re-verify Google's
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
- **sitemap.xml `<lastmod>` is per-page and honest — `sitemap-dates.json` is what makes it
  so, and it MUST be committed with every build.** Until 2026-09-20 the build stamped the
  build date on all 50 URLs, so any change told Google the whole site changed and the
  signal was worth nothing; sessions worked around it by hand-reverting sitemap.xml before
  staging. That workaround is now WRONG — commit sitemap.xml and sitemap-dates.json
  together, or the recorded dates never persist and every page reverts to claiming it
  changed today. `_lastmods()` hashes each generated page and carries the old date forward
  when the hash is unchanged. Asset cache-busters (`?v=`) are stripped before hashing on
  purpose: a styles.css bump rewrites that query string on all 50 pages and is not a
  content change to any of them. A page with no recorded hash is seeded from the date of
  the last commit touching it (today, if the working copy is already dirty). Delete the
  file and you silently lose every real date.

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
  not worth it). Traffic data IS pullable here, contrary to what this file said until
  2026-08-06: the Vercel MCP exposes `get_web_analytics` (project
  `prj_thAY1ZFoahuVCLksBfXAyjyzo1b1`, team `team_VWA1Ar7nCeuyUifvSyeFTT1T`). mode=count
  for totals; mode=aggregate with by=[requestPath|referrerHostname|day|deviceType|country]
  for breakdowns. Data starts 2026-07-21, the day it was enabled.
- **Google Analytics 4** is live: the standard gtag.js snippet for property
  **G-GZKFNKSP6D** is emitted by `head()` in build.py immediately after `<head>` on
  every generated page, so it is exactly once per page and never hand-edited. The
  measurement ID lives in `GA_MEASUREMENT_ID` / `GA_TAG` next to `head()` — it is
  First Rehabilitation's property ONLY and must never be copied onto another client
  site. GA4 sat empty until 2026-09-08 because no tag existed anywhere on the site;
  data starts from the deploy that carries it. GA4 and Vercel Web Analytics run side
  by side and count differently — do not expect their numbers to match.
- **Lead/application data**: query Supabase directly (intake_leads, job_applications).
  Test rows are tagged status='test' and MUST be excluded from every report
  (`where coalesce(status,'new') <> 'test'`). "Run my analytics" = pull real leads/apps.
- **Search Console**: there is NO Claude connector for GSC — it is not in the MCP
  registry, so don't go looking for one to toggle. Use `tools/gsc.py`, which queries the
  Search Console API directly with a service-account key (setup:
  `docs/SEARCH-CONSOLE-SETUP.md`). `sites` / `verify` / `summary` / `queries` / `pages` /
  `compare` / `raw`. Auth comes from `$GSC_SERVICE_ACCOUNT_JSON`, `--key`, or
  `~/.config/gsc/service-account.json`; the key is a secret and the repo is public, so
  never commit it (.gitignore covers the usual names).
  **Ownership verification is emitted by `head()`** via `GSC_VERIFICATION` in build.py
  (added 2026-09-09). It sits empty until the token is pasted, and an empty value emits no
  tag at all, so the build is unaffected either way. Paste from Search Console -> Settings
  -> Ownership verification -> HTML tag, copying ONLY the `content="..."` value. Use the
  OWNER's token, not a service account's: the tag is what keeps Nick's ownership permanent,
  while the service account is a delegated user under Users and permissions and does not
  need to own the property. Once pasted, rebuild and the tag ships on all 48 pages plus
  404.html, and every future build renews it.
  Why this exists: the property lost verification some time before 2026-09-09 and every API
  route went 403 — no queries, no page data, no index coverage, no sitemap submission, and
  the homepage title/description CTR test started 2026-09-03 had no way to be read.
  Verification had never been carried by the site (a DNS record or a leftover Wix token), so
  nothing in this repo kept it alive and nothing warned when it lapsed. Note that
  re-verifying the property restores the OWNER's access only — the service account still has
  to be re-added separately under Users and permissions, which is the step that looks like
  the fix has failed.
  A service account CAN mint its own token via the Site Verification API
  (`siteVerification/v1/token`, scope `.../auth/siteverification`), but that API is not
  enabled on the `design-of-man-seo` Cloud project (403), and it would verify the SERVICE
  ACCOUNT as owner rather than Nick. Not the right tool here; do not reach for it.

  **The property is `https://www.firstrehabnpb.com/` — a URL-prefix property, NOT
  `sc-domain:firstrehabnpb.com`** (verified 2026-08-14 via `gsc.py sites`, service account
  `claude-gsc-reader@design-of-man-seo.iam.gserviceaccount.com`, siteFullUser —
  re-confirmed 2026-09-09; the `firstrehabnpb-seo` address recorded here previously was wrong). The two
  are different properties with different data; querying the domain form returns nothing,
  which reads as "no search traffic" rather than "wrong property". Always run `gsc.py
  sites` and use exactly what it prints.
  Setting the key: the cloud environment's **Environment variables** box is `.env` format,
  one KEY=value per line, so a pretty-printed JSON key is rejected outright ("Couldn't
  parse"). Either minify it to one line, or — simpler — write it from the **Setup script**
  box with a heredoc to `~/.config/gsc/service-account.json`, which gsc.py reads by
  default and which accepts multi-line content. Signing shells out to `openssl`
  and everything else is stdlib — no pip step, so it runs from a fresh clone in a
  routine. Do NOT switch it to the `cryptography` package: the system copy imports fine
  but dies with a pyo3 panic that subclasses BaseException and escapes normal handling.
  Google API hosts ARE reachable from the sandbox (unlike Dropbox/Supabase/*.vercel.app),
  so no pg_net or Actions relay is needed here.
  The old flow — owner exports the "Performance" ZIP (Dates/Queries/Pages/Countries CSVs)
  and drops it here — still works as a fallback if the key is unavailable. The Google
  Drive connector is picker-scoped and can't read files by link; don't fight it.
  Two traps the API removes, which still apply to any CSV export: READ THE TOTALS OFF
  `Devices.csv`, NOT `Queries.csv` (GSC truncates/anonymises the query table — the
  2026-08-06 export showed 123 clicks / 10,413 impr in Queries.csv vs 308 / 17,108 in
  Devices.csv; Pages.csv is partial too), and watch for overlapping windows. `gsc.py
  summary` reads totals from a zero-dimension API row (true by construction, nothing to
  truncate) and `compare` builds non-overlapping windows. Default window ends 3 days back
  because GSC finalises data on a lag.
  Baseline (old Wix site, 90d to
  2026-07-19): 276 clicks / 11,792 impr / pos 17.1 / CTR 2.34%. Non-branded was 5,555
  impr converting 0.36% (ranked page 3 for the money terms the new location/condition
  pages target — that's the growth thesis). Compare next pull against this.
  Export 2 (last 3 months to 2026-08-06): 308 clicks / 17,108 impr / pos 18.6 / CTR 1.80%.
  Impressions +45% on the baseline, clicks only +12%, so CTR fell 2.34% -> 1.80% and
  position drifted 17.1 -> 18.6. That is the expected shape when many new pages start
  ranking at page 2-3 at once; the location pages are landing around pos 24-28. NOTE the
  two windows overlap by roughly 80% of their days, so this is not a clean before/after.

  **API pull 2026-09-09, first clean non-overlapping compare** (28d to 09-06 vs the 28d
  before it): 105 clicks / 11,672 impr / CTR 0.90% / pos 20.2, against 122 clicks / 9,654
  impr / CTR 1.26% / pos 20.1. Impressions +21%, clicks -14%. Two months of adding pages
  has added impressions and REMOVED clicks. This is what froze new blog posts.

  **The location-page growth thesis above is now disproven — do not keep investing in it.**
  City-qualified queries ("physical therapy west palm beach", "neck pain juno ridge fl", and
  89 others in the same pull) earned 1,144 impressions and ONE click in 28 days. That is not
  a ranking problem: /locations/juno-beach.html sits at position 7.3 overall and ranks 3.6 to
  6.3 for the Juno Ridge neck-pain terms, and still earns 0.2% CTR. The location pages are
  40%+ of all site impressions (WPB 1,883 / PBG 1,222 / PB 788 / Juno 408) at 0.2-0.4% CTR.
  The most likely cause is that city-qualified local searches are answered by the map pack,
  which lists clinics IN that city, so an organic result saying "served from North Palm
  Beach" cannot win the click at any position we can reach. NOT verified from here — the
  sandbox cannot see a live SERP — but the click data holds whatever the cause. Practical
  rule: city-qualified intent is a Google Business Profile lever (service areas, categories,
  reviews), not a page-content lever. Do not write more location pages, and do not "fix" the
  existing ones by adding words.
  What IS winnable, from the same pull: non-city service terms where the clinic has a real
  claim. "hand therapist" 95 impr at pos 28.7, "hand therapy" 40 impr at pos 73.7,
  "carpal tunnel syndrome therapies near me" 25 impr at pos 37.2. Laura Drumm CHT and
  on-site splint fabrication are a genuine differentiator and these rank nowhere. That is
  where depth pays.
  Also note branded vs non-branded: branded 31 clicks / 550 impr (5.6% CTR), non-branded
  6 clicks / 1,786 impr (0.34%). The Wix baseline was 0.36% non-branded. Non-branded CTR has
  not moved in the rebuild. Both figures come from the truncated query table, so treat them
  as directional, not exact.

## Conversion
- **The appointment form is on 37 pages, not one** (changed 2026-09-09). `appt_form()` in
  build.py renders the five-field card; `build_contact()` embeds it bare (`wrapped=False`)
  inside its two-column grid, and the service, condition, location and blog templates embed
  the wrapped `<section id="request">` version above `cta_band`. Before this it existed only
  on /contact.html — which had produced 34 of the site's 41 lifetime leads while every
  service, condition, location and blog page produced ZERO. Those pages were never short of
  CTAs (three to five phone/contact links each); they were short of somewhere to convert.
  intake.js binds by `getElementById('appt-form')`, so exactly ONE form may appear per page —
  do not add a second, and do not suffix the ids. The lead's `page` column records
  `location.pathname`, so per-page attribution works with no extra wiring; query it to judge
  whether this change paid off.
- **The chat auto-invite holds while that form is on screen** (added 2026-09-09, Nick approved).
  On a phone the teaser card pins to the bottom of the viewport, which is exactly where the
  form's Send Request button sits — the assistant was covering the thing it exists to help
  with. `watchApptForm()` in intake.js puts an IntersectionObserver on `#appt-form` and
  `showAutoInvite()` defers while it is visible, then fires the moment the reader scrolls it
  away, so the invite is delayed and never lost. It only claims the once-per-session
  `KEYS.auto` slot when it actually appears — setting that on a deferred run would silently
  burn it. The launcher bubble is untouched and stays tappable throughout.
  Measured: contact.html is UNCHANGED, because its hero pushes the form below the fold at
  393x740 so the form is not in view when the invite fires. Do not "simplify" this to a
  pathname test — the whole point is that it keys off what is actually on screen.
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
  Do NOT lighten these — the whole site passes axe-core WCAG 2.1 AA (43/43 pages at both
  393px and 1440px, zero violations); re-run the axe sweep (npm i --no-save axe-core
  playwright-core, inject axe.min.js per page on http.server 8901 with animations settled)
  after any color change.
- Video/img inside .hero-media need position:relative+z-index:1 to paint above .hero-fallback.
- Nav collapses ≤1260px (CSS media query AND matchMedia in main.js — keep in sync).
- A sticky bar whose height grows with its contents will eventually swallow a phone
  screen. .faq-jump-bar is sticky inside <main>, so it stays pinned for the WHOLE page:
  its nine chips wrapped to nine rows and 494px at 393px wide, pinning over a 740px
  screen and leaving 172px to read 73 answers through. It reads as "the page will not
  scroll" — that is exactly how it was reported. Below 1100px it is now one horizontal
  scroll row (flex-wrap: nowrap + overflow-x: auto + overscroll-behavior-x: contain),
  ~66px whatever the category count; above 1100px the centred two-row wrap is unchanged.
  Keep .faq-cat scroll-margin-top matched to header + bar at BOTH layouts (212px / 152px)
  or /faq.html#category deep links land behind the bar. Same trap applies to any new
  sticky element: measure it pinned at 393×740, not just at desktop.
- Filtering a long list scrolls the ground out from under the reader: hiding items
  shortens the page, the browser clamps scrollY and its scroll anchoring lands you
  somewhere arbitrary. main.js scrolls to the chosen topic's first question after the
  filter runs, measuring AFTER the DOM changes — a pre-click scrollY is already stale.

## Location pages
LOCATIONS dict in build.py → /locations/{palm-beach-gardens,jupiter,tequesta,juno-beach,
lake-park,palm-beach,west-palm-beach,riviera-beach}.html. Honest served-from-NPB content
(no fake locations, no invented drive times/parking), named clinicians with credentials,
Service schema per city, footer "Areas We Serve" links every city. North Palm Beach
deliberately has NO location page — the homepage owns that keyword; footer links it to /.

## Verification pattern
The sandbox cannot reach *.vercel.app, Dropbox, or Supabase hosts directly (proxy 403);
GitHub (api/raw/codeload/objects) IS allowed. **The production domain
https://www.firstrehabnpb.com/ IS reachable directly** — plain `curl` returns 200 (verified
2026-09-09). This file previously implied otherwise and sent two sessions through pg_net for
checks a one-line curl does faster. Use curl for anything on the live domain, including
polling a deploy: `until curl -s <url> | grep -q '<marker>'; do sleep 10; done` in a
BACKGROUND bash task (foreground sleep is blocked). Reserve the pg_net dance below for hosts
the proxy really does block. Verify live deploys via Supabase MCP:
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

## Keeping the site's newest episode current — AUTOMATED
Nick, 2026-09-20: "watch for the newest episode and post it onto our website every
Saturday." The daily routine now does this. `tools/episode-sync.py` is the mechanism.

    python3 tools/episode-sync.py check       # read-only; exit 1 means the site is behind
    python3 tools/episode-sync.py add-video   # mechanical, adds VIDEOS, rebuilds

**The feeds are the source; the website is the DESTINATION.** Do not scrape
firstrehabnpb.com looking for the episode link, and do not reach for the Spotify for
Creators dashboard (`creators.spotify.com/home/show/033A1BQq9qqsygFFCq9SIu`) — it needs
Nick's login, so a routine cannot read it. The public show embed and the YouTube channel
feed both answer unauthenticated and are what the script uses.

**Spotify and YouTube do NOT arrive together.** Episode 15 was on Spotify before 9:00 AM
ET Saturday; Nick uploaded the video at 10:10 AM. So the Saturday run will often add
EPISODES and not VIDEOS, and a later day backfills the video. That is why `check` runs
EVERY day rather than only Saturday. A missing VIDEOS entry is a CORRECT build warning,
not noise — never invent a YouTube id or an uploadDate to silence it, because uploadDate
is what video rich results key off.

**What the script will not do: write the EPISODES blurb.** That is five paragraphs from
the episode transcript, and a generated one reads generated. `check` reports the gap and
stops. `add-video` fills in everything mechanical and leaves the teaser as an explicit
PLACEHOLDER so an unreviewed one cannot ship silently.

The routine pushes straight to `main` once the build is clean, because Nick wants the
episode live rather than waiting in a PR. It pushes a branch instead if the build warns
or the diff touches anything beyond build.py and regenerated HTML.

## Episode release cycle — STANDING AUTHORIZATION
Nick approved this flow 2026-08-02 and revised it 2026-09-18; do not re-ask each time.
- **Friday 5:00 PM ET** — the announcement post for tomorrow's guest. A studio photo, the
  guest's background, and "tomorrow 8:30 AM on 100.3 Legends Radio". Instagram, Facebook,
  LinkedIn business, X, plus its own text-and-one-image Google Business call.
  The slot has moved twice: PR #78 set it at 4:00 PM ET, Episode 14's actually ran at
  8:00 AM ET at Nick's request, and 5:00 PM is the current standing time. Any of them is
  fine on the day; what matters is that it lands on FRIDAY.
  **Default: an announcement carries nothing said inside the episode** (PR #78). It has not
  aired, Nick sells Saturday as the live moment, and a teaser assembled from the transcript
  gives away the show. The hook is the airing itself. NICK OVERRODE THIS for Episode 15 on
  2026-09-18 — "Listen to the podcast to write about her background" — so that announcement
  does carry the guest's story. Treat the no-spoiler rule as the default and his instruction
  for a given week as the exception, rather than quietly picking one.
  Drafts live in `content/announcements/ep{NN}-announcement.md`; rules in that folder's README.
- **Saturday 9:00 AM ET** — the episode-is-live post carrying the Spotify link (LinkedIn,
  Facebook, Google Business) + the full episode video on YouTube. The show "airs" 8:30 AM
  Sat on 100.3 Legends Radio; episodes are prerecorded but Saturday is the public moment.
- **Every day, 9:00 AM ET** — ONE clip from the mixed queue (Instagram, Facebook, YouTube
  Shorts, TikTok).

**"One episode owns one week" is DEAD as of 2026-09-18 — Nick killed it, and the reason
matters.** Under that rule a single guest ran six days straight while a second lane ran
somebody else, so the feed read as a broadcast and five days carried two posts each.
Clips now come from ONE pool spanning every episode, with a hard rule that the same guest
never appears on consecutive days. `tools/clip-queue.py` owns that arithmetic:

    python3 tools/clip-queue.py import --posts <dump.json> --write   # after staging
    python3 tools/clip-queue.py plan  --days 30 --boost "<new guest>"
    python3 tools/clip-queue.py audit --posts <dump.json>            # find what is wrong

The order is seeded, so the same inputs give the same calendar and a human can review it.
A new episode's guest gets `--boost` so a fresh episode still gets a push rather than
queueing behind whoever has the most clips banked. Post Bridge is only reachable through
MCP tools, never a plain HTTP key, so the script emits a plan and the session applies it
with update_post, then records it with `clip-queue.py mark`.

**`update_post` SILENTLY IGNORES `is_draft` on a post that is already scheduled.** It
returns 200 with `is_draft` still false. Parking a scheduled post as a draft does not
work, and if you edited the caption in the same call you have now left a live post
carrying a note meant for internal eyes. `delete_post` is the only way to pull one.

**The weekday Google Business slot changed 2026-08-15 (Nick approved).** It used to carry a
text-only clip takeaway written by the routine. It now carries keyword-led SEO posts derived
from the episode's PILLAR blog post, drafted by `/episode-blog` to `content/gbp/ep{NN}-{pillar}.md`
and pre-scheduled in Post Bridge once Nick approves the blog. Same volume, real search intent.
**The routine must NOT post its own weekday Google Business text or the profile double-posts** —
if you find that call back in the routine prompt, remove it. The Saturday episode post to Google
Business stays. Format rules are in content/gbp/README.md: 750–1,200 chars, text only, zero
dashes, `•` bullets, one keyword + one city each, phone number, LEARN_MORE CTA on the blog URL,
and a different angle per post.

**When Nick sends raw footage for a new episode: build everything, then SCHEDULE it — don't
ask first, and don't publish immediately.** He reviews scheduled posts in Post Bridge before
they go live. Target the next Saturday 9:00 AM ET for the episode + full video, then the
clips one per day after it. Scheduling IS the deliverable; waiting for approval is not.

ONE master routine handles all of it (claude.ai Routines, fresh session per fire):
`trig_01R5iPGmt45aWsNkwNoX5zDc` — "Pain 2 Power — daily social poster", cron `0 13 * * *`
(9:00 AM ET daily). It branches on the ET day of week: Saturday → episode-is-live post,
every other day → the next clip off the mixed queue, and it checks whether an announcement
is owed for tomorrow. Consolidated 2026-08-02 from two separate routines
because the Routines tab was unreadable and each one needed its connectors wired separately.
Don't split it back apart; add day-branches to this one instead.

**The ID above was `trig_01L8gTCsSXAtwCkvG4LMZuSh` until 2026-09-18 and that one is DEAD** —
`list_triggers` shows it gone from the account entirely. It was recreated as
`trig_01R5iPGmt45aWsNkwNoX5zDc` on 2026-09-10 (same name, same cron, fresh session per fire);
this file went on naming the dead one for eight days. Re-confirmed live 2026-09-18, last run
SUCCEEDED 13:03 UTC. If a session reports the routine missing, check `list_triggers` before
concluding anything — the ID here is a record, not a guarantee.

Two things to know before touching it:
- **`list_triggers` does NOT return a routine's prompt.** Editing means rewriting the whole
  prompt from scratch; there is nothing to read back and patch. Keep this file current,
  because it IS the backup of that prompt.
- **`create_trigger` cannot attach connectors on this org** — the API rejects the
  `connectors` parameter outright, so a routine created from here fires with NO `mcp__*`
  tools and cannot reach Post Bridge at all. **Post Bridge has to be attached by hand in
  the claude.ai Routines UI.** Check this first if a firing reports "no such tool".

**Add the GUEST as an Instagram collaborator on every clip from their episode** (Nick,
2026-09-11). `platform_configurations.instagram.collaborators: ["handle"]` puts the post on
the guest's own profile and shares its likes and comments, which is the entire point.
Instagram only; no equivalent on Facebook, TikTok or YouTube. Max 3 handles, and **a private
or misspelled handle fails the WHOLE post**, so confirm it with Nick rather than guessing.
Known: Captain Kerry is `capt_kerry` (set by an earlier session, not independently verified).

**Re-check the media on scheduled posts after ANY re-cut of a clip.** Post Bridge stores an
uploaded COPY, not a reference to the branch, so re-cutting a clip and pushing it does not
change what a scheduled post will publish. On 2026-09-11 four of five scheduled Episode 13
posts still pointed at pre-fix uploads showing the wrong speaker, and would have published
them. Compare `list_media` size_bytes against the file on the media branch; a mismatch means
the post is stale. Fix with `upload_media` then `update_post`, and pass
`platform_configurations` back IN FULL or the collaborators and YouTube title are dropped.

Post Bridge account IDs change on every reconnect — always `list_social_accounts` first.
YouTube was 81323, died with `invalid_grant`, came back as 81358; Google Business was 81363,
came back as 81642. Current (verified 2026-08-06): Instagram 81353, Facebook 81324,
YouTube 81358, TikTok 81356, X 81378, Google Business 81642, LinkedIn business 81322,
LinkedIn personal 81320 (never post). Google Business takes text or ONE image, **never video**
— clips go there as a separate text-only call with a LEARN_MORE CTA.

`create_post` returning "processing" is NOT proof of publication. Always finish with
`list_post_results` and report per platform. Uploads to Post Bridge are metered — reuse
existing media IDs (`list_media`) instead of re-uploading.

**Add the GUEST as an Instagram collaborator on every clip post from their episode**
(Nick, 2026-09-11). `platform_configurations.instagram.collaborators: ["handle"]` — the post
then also appears on the guest's own profile and shares its likes and comments, which is the
whole reason to do it. It is an invite, so it shows on their profile once they accept.
Instagram only; there is no equivalent field for Facebook, TikTok or YouTube, so a clip post
carries it on the IG leg alone. Max 3 handles.
**A private or misspelled handle fails the WHOLE post**, so confirm the handle with Nick
rather than guessing it, and never copy one from memory. Known: Episode 13 Captain Kerry is
`capt_kerry` (set by an earlier session; not independently verified).

**Re-check the media on scheduled posts after ANY re-cut of a clip.** Post Bridge stores an
uploaded copy, not a reference to the branch, so re-cutting a clip and pushing it does NOT
change what a scheduled post will publish. On 2026-09-11 four of the five scheduled Episode 13
posts were still pointing at the original pre-fix uploads, the ones showing the wrong speaker,
and would have published those. Compare `list_media` size_bytes against the file on the media
branch; a mismatch means the post is stale. Fix with `upload_media` (the Vercel branch host
serves any size) then `update_post` with the new media id, and pass
`platform_configurations` back in full or the collaborators and YouTube title are dropped.

**The routine runs unattended — `.claude/settings.json` is what makes that true.** Each
firing spawns a fresh session that clones this repo, and without a permission allow-list
every Post Bridge call stops and asks Nick to approve it. `permissions.allow` pre-approves
the eight posting/reading tools plus the five domains the routine fetches (raw
.githubusercontent, jsDelivr, Spotify, the site, YouTube). `delete_post` and `delete_media`
are deliberately in `permissions.ask` so removing something still needs a human.
It MUST be `.claude/settings.json`, committed — `settings.local.json` is gitignored and so
is absent from the clone the fired session gets. Adding a tool to the routine's prompt
without adding it here reintroduces the approval prompt.

**Captions carry ZERO dashes** (Nick, 2026-08-02): no em dashes, en dashes, or hyphens in
prose, bullets, compounds, or titles. Bullets use •. Only 561-624-4263 / 561-624-GAME keep
their dashes.

## iPhone HDR footage: tonemap it, don't just transcode it
Video shot on a recent iPhone is Dolby Vision: HEVC Main 10, `yuv420p10le`, BT.2020
primaries, HLG transfer (`arib-std-b67`). Two consequences, both learned the hard way on
the 2026-08-05 oyster clip:
- **Transcode or X rejects it.** Post Bridge accepts a `.mov` upload happily and reports
  `video/quicktime`, but HEVC-in-MOV is not something X/Twitter will publish. Convert to
  H.264 High + yuv420p + AAC + faststart before posting anywhere.
- **Tonemap through linear light or it ships washed out.** A bare `-pix_fmt yuv420p` keeps
  the HLG-encoded values while tagging them BT.709: lifted blacks, milky whites, grey
  skin. It looks like a bad camera, not a bad convert, so it is easy to ship. Use:

      -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
      -color_primaries bt709 -color_trc bt709 -colorspace bt709

  Detect with `ffprobe -show_entries stream=color_transfer,color_primaries,pix_fmt`; a
  source reading `arib-std-b67` / `bt2020` / `yuv420p10le` needs the filter.
  **`tools/stage-media.py` does NOT do this yet** — it converts with a bare `-pix_fmt
  yuv420p`, so every HDR phone clip through it ships flat. Add the filter there.

YouTube decides Shorts eligibility from the media itself — vertical and under 3 minutes is
enough. There is no API flag and Post Bridge exposes no toggle, so "make it a Short" is a
property of the file, not the request. Confirm after posting via the channel feed: the
video's `link rel=alternate` reads `/shorts/<id>` for a Short, `/watch?v=<id>` otherwise.

## Automating the episode metadata (verified 2026-08-02)
Both feeds are public and machine-readable, so the Spotify link and YouTube id never need
typing. Neither is reachable from the sandbox (proxy 403) — fetch via Supabase `pg_net` or a
GitHub Actions runner.
- Newest Spotify episode id: GET `https://open.spotify.com/embed/show/033A1BQq9qqsygFFCq9SIu`,
  regex `spotify:episode:([A-Za-z0-9]{22})`. Returns exactly one id, the current episode.
  Title via `https://open.spotify.com/oembed?url=<url-encoded show url>` → `.title`
  (e.g. "Episode 8: Dr. Ryan Simovitch, MD").
- Newest YouTube video: GET `https://www.youtube.com/feeds/videos.xml?channel_id=UCFzCl3RvdVahfIjKZ1SfRvQ`.
  Shorts vs full episodes are distinguishable by the `link rel=alternate` path: `/shorts/<id>`
  for Shorts, `/watch?v=<id>` for long-form. Filter on that.
- Site update = add `EPISODES[0]` (Spotify URL) + a `VIDEOS` entry (YouTube id) in build.py,
  rebuild, push. Both values now derive automatically from the two feeds above.

## Staging a new episode — DO THIS FIRST, every time
`python3 tools/stage-episode.py <NN> <clips-dir> --transcripts <text-dir> --guest "..." --credential "..."`

Creates branch `media/ep{NN}-clips` with clips/, playlist.txt, transcripts.md and a
README, pushing in small batches (a single ~200MB push gets reset by the git proxy).

**The branch name is load bearing.** The daily routine builds its fetch URLs from the
episode number, so anything other than `media/ep{NN}-clips` is invisible to it. Episode 9
was first pushed to `media/sabesan-clips` and would have posted nothing all week.

Three things the script does NOT do, by design:
- **Reorder playlist.txt.** Seeded numerically; a human reorders it. Six weekday slots
  and ~10 clips means only the top six air, so order decides the week. The strongest clip
  is rarely the first one rendered.
- **Add the episode to build.py.** `EPISODES[0]` and a `VIDEOS` entry are still manual,
  and EPISODES needs the Spotify URL, which does not exist until the episode publishes.
- **Write captions.** The routine does that at post time, from transcripts.md.

Name corrections live in `NAME_FIXES` at the top of the script — ASR renders "Sabesan" as
"Sebastian" and "Vani" as "Bonnie". Add new guests there rather than fixing by hand.

Verify before the week starts: fetch playlist.txt off raw.githubusercontent, and range
request one clip off the Vercel branch host. Both must return 200/206.

**Clip upload hosts.** jsDelivr serves clips under ~20MB; anything larger needs the Vercel
branch host `firstrehabnpb-zywd-git-media-ep{NN}-clips-thedesignofman.vercel.app`. That
host embeds the Vercel TEAM SLUG, renamed to `thedesignofman` on 2026-08-03. The old
`-first-rehabilitation` host now 404s. If the team is renamed again, update the URL in the
routine prompt or every clip over 20MB fails to upload. raw.githubusercontent and GitHub
release assets both serve `application/octet-stream` and are rejected by Post Bridge.

**SHOW NICK THE CLIPS BEFORE ANYTHING IS SCHEDULED** (his ask, 2026-09-18). He wants to
view them in the Claude conversation, not on an external link and not in Dropbox. Send
each clip into the chat as a playable file with its draft caption and its assigned slot
underneath, in one pass, and wait. Until now clips were cut, captioned and scheduled
without him ever seeing one before it published.

## The whole episode, end to end
What a new episode actually costs now, in order:

1. `tools/stage-episode.py <NN> <clips-dir> --transcripts <dir> --full-transcript <path>`
   -> branch `media/ep{NN}-clips` (the name is load bearing; the routine builds URLs from it)
2. Reorder `playlist.txt` by hand. The strongest clip is rarely the one rendered first.
3. Cut the multicam: `podcast-multicam` skill, run order lock_rate -> build_warp2 ->
   sync_preview (checkpoint, never skip) -> render_final_v3 --dry-run -> render, with
   `tools/podcast-attrib.py` supplying `--cuts`. **Re-tune the attribution per episode**
   and audit with a contact sheet. This is the one step that stays a judgment call.
4. `tools/dropbox-put.py put <master> "/Pain2Power/<Guest>/Final/..."`
5. Write clip captions from `transcript-full.md`.
6. **Send every clip into the chat for Nick to review.** Wait.
7. Create the approved clips as posts, then `clip-queue.py import --write`,
   `clip-queue.py plan --boost "<guest>"`, apply with update_post, `clip-queue.py mark`.
8. Friday announcement post, Saturday episode-is-live post once the Spotify URL exists.
9. `/episode-blog <NN>` for the GBP set (blog posts themselves are still frozen).

Steps 2, 3, 5 and 6 need a human. Everything else is mechanical.

NOTE: `stage-episode.py` does NOT feed `clip-queue.py` directly, and deliberately so. The
queue keys off Post Bridge post ids, which do not exist until step 7, so there is nothing
to import at staging time. Do not "fix" this by inventing clip ids at step 1; they would
have to be reconciled against Post Bridge later anyway.

## Posting on demand — "post it" should be one step
When Nick says post something, the only two things that ever block it are:

1. **The Post Bridge connector toggle.** See the Connectors note below. If its tools are
   missing, that is the cause; say so immediately rather than retrying.
2. **Getting the media to a URL Post Bridge can fetch.** Use `tools/stage-media.py`:

       python3 tools/stage-media.py clip.mov

   Converts .mov to .mp4, pushes to a `media/<slug>` branch, prints the Vercel branch URL
   (any size) and the jsDelivr URL (under 20MB), and warns if the video is landscape,
   which letterboxes on Reels, TikTok and Shorts.

**A Dropbox link is fine; so is an attached file.** This paragraph used to say the sandbox
was proxy blocked from Dropbox and that only a chat attachment would do. That is wrong and
cost at least two sessions planning a GitHub Actions relay nobody needed. Dropbox bytes
download here via the connector's `download_link` (2.35 GB of Episode 15 pulled directly,
hashes verified 2026-09-17), and uploads go back up through `tools/dropbox-put.py`. A chat
attachment is still the fastest path for one small file, nothing more.

Standing preferences for a one off post, unless told otherwise:
- Captions carry ZERO dashes outside the phone numbers. Bullets use •.
- Lead with the joke or the hook. The event details go after it, never before.
- Google Business takes text or ONE image, never video, and gets its own text only call.
- LinkedIn personal (81320) is never posted to.
- Finish with `list_post_results` per platform. "processing" is not proof.

## How the clips are cut (observed spec, Episode 9 pipeline)
- **1080x1920 vertical, 30fps, h264 crf 20, AAC.** Captions burned in: white bold, centred,
  two lines max.
- **CAPTION STYLE — Nick specified this as the standard for EVERY episode, not just one.**
  White text on a SOLID BLACK box, sitting LOW in the frame. The reference he pointed at is
  the Episode 11 Paul Joyce clip `05-top-of-the-range.mp4` on `media/joyce-recut` (the
  testosterone one) — pull a frame off it if there is ever any doubt. Exact style:

      FontName=Arial,FontSize=10,PrimaryColour=&H00FFFFFF,BackColour=&H00000000,
      BorderStyle=4,Outline=0,Shadow=0,Bold=1,Alignment=2,MarginV=35

  Two things he corrected, twice each, so do not let them drift back:
  - **Low.** MarginV=35 puts the text ~88% down. It first shipped near the vertical middle,
    then at 60 (~80% down), and he asked for lower both times. 35 is the approved value.
  - **Solid black box.** `BorderStyle=4` with `BackColour=&H00000000` — alpha `00` is OPAQUE
    in ASS. A semi transparent box (`&H90000000`) is what it looked like before and is wrong.
  `MarginV` is in ASS script units — libass defaults SRT to PlayResY=288, NOT the 1920 pixel
  height. A pixel-scale value like 880 pushes the text clean off the canvas and the file still
  encodes fine with NO captions at all, which is easy to ship if you only check the exit code.
  Always eyeball a real frame before shipping.
- **Caption TEXT comes from the reviewed `transcripts.md` on the episode's media branch, never
  from raw ASR.** Time it by fuzzy-matching the reviewed words against word-level ASR
  timestamps. Enforce monotonic non-overlapping cues or two captions render on top of
  each other.
- **Source is the RAW camera, not the master.** The guest camera shoots natively vertical
  and is used full frame at ZERO crop. Host moments crop the 4K two shot to a 9:16 window
  on whoever is speaking. Cropping the finished 16:9 master instead means upscaling a
  narrow slice of an already cropped face — visibly worse, do not do it.
- **Audio** comes from the finished master's mixed track, normalised to -14 LUFS for social.
- **Audit who is on screen against who is actually talking, before clips ship.** The Episode 13
  multicam showed the wrong person a lot, and it hit the GUEST hardest: Kerry was on screen for
  only 52% of his own speech (Mike was shown 41% of it) while the two hosts sat at 88 to 90%.
  Three of the five staged clips were wrong, one for its entire 45 seconds. Eyeballing does not
  catch this and wardrobe guessing gets it backwards — measure it:
  sync each camera to the master by audio cross correlation, take the speaker at each moment
  from whichever camera's own close mic is hottest (normalise each by its median so mic gain
  cancels), classify who is on screen from the master's own frames, then compare. Validate the
  speaker detector against segments where the transcript names someone ("he goes Dave, what
  size is that shirt") before trusting a single number. Expect ~82% agreement as normal for
  room mics; the corrected Episode 13 episode reached 92.9%, with Kerry at 95.8%.
  NOTE the master is an EDIT, so the camera offset does not drift smoothly — it STEPS at each
  cut (Episode 13: four cuts, at show 191.0 / 576.5 / 666.0 / 945.5s). Fit one offset per
  plateau and split any shot that spans a cut, or lip sync breaks at that boundary.
- Clips have run 20 to 75 seconds. For REACH specifically, shorter and hook first performs
  better: open on the most surprising sentence, cut the setup entirely, aim 15 to 25s. Every
  Episode 8 and 9 clip currently opens on an interviewer question or mid sentence on "But",
  which is the single biggest thing holding their reach back. Not yet changed — flagged to
  Nick 2026-08-03, no decision taken.
- Captions are burned AFTER a human reviews the ASR. Never burn unreviewed transcription
  into a deliverable; ASR mangles guest names badly.

## Full episode to YouTube — Nick uploads it himself
**Nick uploads the full episode to YouTube himself.** Do not build a publish path for it,
and do not route it through Post Bridge: Post Bridge times out fetching anything that
large (a 2.9GB export failed at 60s) and rejects GitHub release assets, which serve
`application/octet-stream`.

The deliverable from here is the finished file, not a publish. **Put it in Dropbox at
`/Pain2Power/<Guest>/Final/Pain to Power - <Guest> - multicam.mp4`** with
`tools/dropbox-put.py` and tell Nick it is there; he takes it from there and sets
scheduling in YouTube Studio. Do NOT hand him a PowerShell paste to reassemble chunks on
his own PC — that was the old handoff and it is retired.

This section used to say "publish from Descript, by hand" and was wrong — corrected
2026-09-16 by Nick. **Descript is being cancelled** (see below); nothing in the episode
pipeline may depend on it.

## Descript is gone — what that means for the pipeline
Nick cancelled the Descript subscription on 2026-09-16. Nothing about the edit depended
on it, and this is the record of what did:

- **The clips and the full multicam are cut by SCRIPT, not in Descript.** Episode 14's
  finished video (`tmp/ep14-video`, 27:38.96, 105 shots) was rendered by the multicam
  script from the raw cameras. That capability is ours and is unaffected.
- **Masters and raw sources live in Dropbox and git, never in Descript.** Ep 15's source
  is `/Pain2Power/Susan Mann/P2P-Susan mann 9-19 RAW.mp3`. Anything that was only in
  Descript was a derivative of something we already hold.
- **Speaker attribution was the only thing Descript was load bearing for, and it is now
  SOLVED without it.** The multicam script picks the camera by microphone energy, which does
  not work here: all three cameras sit in one small studio, every mic hears everyone, and the
  script z-scores each camera by its own standard deviation. On Episode 14 that put the guest
  on screen for 12.5% of his own interview; on Episode 15 it gave the guest 17% and dropped
  her from the last five minutes entirely. Episode 14 solved it with `--cuts` fed by
  Descript's diarisation of the board mix.
  **No diarisation service is needed.** `tools/podcast-attrib.py` derives speaker turns from
  PITCH on the board mix, which is how Episode 9 did it before Descript was ever involved
  (see `transcript_v4.json` on `tmp/sabesan-out`: it carries `f0` and `voiced` alongside
  `spk`). Full detail in "Cutting the full multicam" below. Do not go shopping for pyannote
  or an ASR vendor; read that section first.

## Cutting the full multicam — the pipeline EXISTS, do not rebuild it
The `podcast-multicam` skill carries the whole thing: `lock_rate.py`,
`build_warp2.py`, `sync_preview.py`, `sync_probe.py`, `render_final_v3.py`.
Two sessions have now wasted time concluding "the pipeline was never committed"
because only the RENDERED OUTPUT survives on the tmp branches. Load the skill first.

Run order, in a folder holding the cameras and the audio master, nothing else
(a stray video file gets adopted as a fourth camera): lock_rate -> build_warp2 ->
**sync_preview (checkpoint, never skip)** -> render_final_v3 --dry-run -> render.
Needs ffmpeg with zscale+tonemap, ffprobe, numpy. **This sandbox ships neither
ffmpeg nor numpy** — `pip install numpy` and drop a johnvansickle static ffmpeg
into /usr/local/bin.

**Dropbox bytes ARE reachable from the sandbox** (verified 2026-09-17: all 2.35 GB
of Episode 15 pulled directly via `download_link`, hashes verified). The note
elsewhere in this file saying otherwise cost a session's worth of planning an
Actions relay that was never needed. Verify with Dropbox's own content_hash, which
is sha256 over concatenated sha256s of 4 MB blocks, NOT a plain sha256 of the file.

### The stock speaker attribution is not shippable, and this is why
`render_final_v3.py` picks the camera by z-scored mic energy. In this studio all
three mics hear everyone and Dave shares a desk with the guest, so his mic hears
the guest nearly as well as hers does. On Episode 15 that gave the GUEST 17% of
her own interview, zero screen time in the final five minutes, and one 176-second
static shot. Episode 14 hit the identical failure (guest on screen 12.5%).

`tools/podcast-attrib.py` fixes it and is the thing to reuse:
- pitch off the board mix separates a female guest from male hosts (f0 gate,
  Schmitt trigger so a value near the threshold cannot flap, plus a short sustain
  so a music bed cannot latch the gate)
- a calibrated bias splits the two male hosts on camera-mic energy
- reaction cuts break any shot over ~34s at the quietest nearby point
- `render_final_v3.py` was patched to take `--cuts cuts_final.json`

Episode 15 result: 118 shots, avg 14.3s, longest 36s, guest 44.1% / Dave 28.1% /
Mike 27.8%, everyone present in every five-minute block. Tunables that worked:
`THR=175 BIAS=0.15 SUSTAIN=0.3 ENT=0.62 EXT=0.40`. **Re-tune per episode**; a
1.5s sustain crushed the guest to 15%, and the parameters depend on who is in
the room and where they sit.

**Verify without watching**: contact sheet, one frame per minute tiled, audited
against `transcript-full.md`. Episode 15 scored ~22/28 frames on the right person,
about 79%, against the skill's stated ~82% ceiling. Say the real number; do not
claim perfection. Coverage per five-minute block matters more than the overall
percentages.

Finished masters go to DROPBOX first, via `tools/dropbox-put.py put <file>
"/Pain2Power/<Guest>/Final/..."`, which verifies the upload against Dropbox's
content_hash. That is the delivery. Chunking to a `tmp/` branch (`split -b 45m`, pushed
in small batches or the git proxy resets it) is now only a BACKUP, and only worth doing
while an episode is still in flight. Episode 15's chunks are on `tmp/ep15-video`.
See docs/DROPBOX-SETUP.md for the one-time credential.

## Connectors — check this before assuming a tool is broken
`ListConnectors` reports `connected` AND `enabledInChat`. A connector can be connected to the
account while switched OFF for the current conversation, in which case its tools simply do not
exist and every call fails as "no such tool". That looked like an intermittent Post Bridge
outage across 2026-08-05/06 and cost hours; it was the per chat toggle the whole time.
Connector changes only take effect on a NEW conversation, not mid chat.

## Episode masters
Rendered masters exceed GitHub's 100MB blob limit, so they ship split: `split -b 45m` (or 90m)
into `master.chunk_NN` on a `tmp/` branch alongside `master.sha256`. Reassemble with
`cat master.chunk_* > master.mp4` and ALWAYS verify the sha256 before using it.
- Sabesan (Episode 9) 1080p master: `tmp/sabesan-out`, 13 chunks, 1,221,256,866 bytes,
  sha256 `947a6eaa6a8dfb0f63779b968b7024decc64b9b9258cb98d27c41f854649050a`, 27:50.1,
  1920x1080 30fps bt709. Verified intact 2026-08-02. `audio_master.flac` beside it is the
  lossless audio so an EQ choice can still be applied without re-decoding the AAC.
- The 4K master was rendered once but never uploaded (GitHub 500 on 5 GB). `final4k2.py`
  re-renders it if needed.

## Recovering camera sync when the clip pipeline is gone
The Episode 9 clip pipeline (`pipeline/tighten23.py`) was never committed — only its
`__pycache__` survives on `tmp/sabesan-out` — so cutting more clips meant re-deriving which
raw camera is which and how each lines up with the transcript. The method is general and
takes one Actions run:

**Correlate a finished clip against the raw camera.** Every shipped clip's show-time range
can be recovered by fuzzy-matching `transcripts.md` against `transcript_v4.json` (match on
word blocks, not exact strings — transcripts.md carries the NAME_FIXES corrections). Then
FFT cross correlate that clip's audio against the camera's audio: the peak gives the
camera time of a known show time, so the difference is the camera's offset. Use two clips
far apart to prove there is no drift, and check SNR — a real peak scores in the hundreds.

Episode 9 (Sabesan), Dropbox `/Podcast - Sabesan/`, all three cameras verified 2026-08-06:
- **`Video Jul 30 2026, 4 47 25 PM.mov` (6.16 GB) is the GUEST camera.** HEVC 3840x2160
  with `rotation=-90`, so it decodes to 2160x3840 — vertical, and exactly 2x the 1080x1920
  target, so clips are a clean downscale at ZERO crop. 8-bit bt709, not HDR, so it needs
  no tonemapping. `camera_time = show_time - 83.15` (measured -83.20 and -83.10, 22 min
  apart, SNR 195/119).
- `Video Jul 30 2026, 4 46 01 PM.mov` (5.80 GB) is the host two shot, landscape, and its
  audio is 1808.0s — exactly the transcript length, so this camera IS the show timeline
  (offset ~0). Useful as the reference clock.
- `Mobile Uploads/Video Jul 30 2026, 4 47 22 PM.mov` (6.22 GB) is the third angle.
Note ffprobe reports `width,height` plus side data, so a naive `[ "$H" -gt "$W" ]` shell
test breaks on the trailing comma. Read `rotation` instead; that is what decides
orientation.

## Owner to-dos (repeat in reports until done)
- ~~Flip DNS~~ DONE. Confirmed live 2026-08-06: https://www.firstrehabnpb.com/ serves the
  new site (200 via pg_net) and Google has indexed the new URLs — /contact.html,
  /about.html and the /locations/*.html pages all appear in the GSC export with
  impressions. The Wix redirects are doing their job; legacy URLs still carry ~4,800
  impressions. Still worth confirming: sitemap.xml submitted in Search Console, and the
  Google Business Profile website link pointing at the new site.
- ~~Click the FormSubmit activation email~~ DONE — owner confirmed leads are arriving by email.
- ~~Send Google Business Profile share URL → add to sameAs~~ DONE — GBP already in the org
  schema via its canonical CID link (maps.google.com/?cid=3809434844265673488); owner's
  share.google link resolves to the same listing. No further action.
- **Connect Search Console via service account** (~10 min, one time, owner only — needs
  their Google account). Follow `docs/SEARCH-CONSOLE-SETUP.md`: create a Cloud project,
  enable the Search Console API, make a service account, download the JSON key, then add
  its `client_email` as a user under Search Console → Settings → Users and permissions.
  Step 4 is the one people skip; without it the key authenticates but sees no properties.
  Then `python3 tools/gsc.py verify`. After that no more manual ZIP exports.
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

**NEW POSTS ARE FROZEN as of 2026-09-09 (Nick approved).** Do not write, draft or ship a new
blog post — `/blog` and `/episode-blog` included — until the freeze is lifted. Reason, from the
2026-09-09 analysis: the site carries ~12,400 monthly search impressions at average position
20.1 and converts them at 0.94%. Impressions grew 32% while clicks grew 1%, because every new
page lands on page two or three and adds impressions nobody clicks, which drags site-wide CTR
down. Thirteen posts have produced zero leads between them. Publishing more of them makes the
CTR number worse, not better.

What replaces it: work the queries already sitting at position 8-15 — the ones one push from
page one — by deepening the pages that own them. That is the move that worked. The two location
pages given real content in PR #66 both moved up (West Palm Beach 23.4 -> 20.3, Juno Beach
8.6 -> 7.1) in the same window. Depth moves positions; breadth does not.

The freeze covers NEW posts only. Still allowed, and still wanted:
- Editing, expanding or re-targeting an EXISTING post or page.
- `EPISODE_POSTS`, `RELATED_POSTS`, `COND_BLOG` / `SVC_BLOG` internal-link work.
- The Google Business Profile posts `/episode-blog` produces — those are not blog posts and
  are not frozen. An episode week still needs its GBP set.
- Anything Nick asks for directly. He can lift the freeze at any time; when he does, delete
  this block rather than leaving a stale rule in place.

Note that a frozen backlog is not a lost one: the Wellness and OT pillar holes recorded below
are real and still worth filling once ranking work has caught up.

Two commands. `/blog <topic>` writes one post from a topic or a BLOG-TOPICS.md slug.
`/episode-blog <NN>` (.claude/commands/episode-blog.md) turns ONE Pain 2 Power episode into
TWO posts plus a Google Business set, because an episode is worth both:
- **Post A, the recap** (600–900 words, tag "Pain 2 Power", slug `pain-2-power-ep{NN}-…`)
  belongs to the show. Targets the guest's name + specialty + geography. Links podcast.html,
  videos.html, the pillar service page.
- **Post B, the pillar post** (900–1,200 words, tag = one of Physical Therapy / Occupational
  Therapy / Hand Therapy / Wellness) belongs to the practice. Same transcript, written as our
  expertise with the guest's words as support. Takes a SECONDARY or long-tail keyword from
  SEO-KEYWORDS.md, never a pillar's primary (the service pages and homepage own those).
  More than one Post B when the transcript genuinely supports a second pillar; older episodes
  get mined the same way when a pillar needs coverage.

Posts reviewed by Dr. Dave Kashuba, Ph.D. (byline + reviewedBy schema). Facts only from
build.py/site/owner input — never web research, never invented stats or testimonials.

**SEO-KEYWORDS.md is the only source of keyword targets.** Four pillar blocks (primary /
secondary / long tail / geo / internal links / do-not-claim), plus a coverage table at the
bottom recording what each live post owns. Update that table whenever a post ships. Two rules
in it came from real GSC data: use "treatment" not "relief" in title tags, and never target a
keyword one of our own pages already owns. Current holes: OT and Wellness have zero posts.

**Anti-AI-slop rules live in BLOG-PLAYBOOK.md** ("No AI slop") and are enforced by
`python3 tools/slop-check.py` (`--new` skips the seven pre-rules posts, which are warn-only
via its BASELINE set; `--slug`, `--file` for one target; exit 1 on a violation). Zero em
dashes in prose, no "it's not X it's Y", one bold phrase and one list max, two attributed
quotes minimum, a concrete checkable detail per h2. Keep the checker's BANNED list in sync
with the playbook. A draft also gets an `avoid-ai-writing` detect pass; quotes and the
disclaimer are flag-only.

`EPISODE_POSTS` in build.py maps an episode number to its recap slug and renders a
"Read the recap" link on /podcast.html (`.pod-recap` in styles.css). Episodes 8, 7 and 6 are
already mapped to existing posts. Add the new slug there when a recap ships.

Full-episode transcripts: `tools/stage-episode.py --full-transcript <path>` now writes
`transcript-full.md` (timestamped [mm:ss], NAME_FIXES applied) onto the load-bearing
`media/ep{NN}-clips` branch. Before this, full transcripts landed on ad hoc branches like
`tmp/sabesan-out` that nothing knew to look for, so drafts fell back to clip-level text.
`/episode-blog` resolves a transcript in this order: owner-supplied path →
`transcript_v4.json` on a `tmp/*-out` branch → `transcript-full.md` → `transcripts.md`
(clip-level, must be declared on the flag list). The Descript `export_transcript` step that
used to sit second in this chain was removed 2026-09-16 when the subscription was cancelled.
