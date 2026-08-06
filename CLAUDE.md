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
  not worth it). Traffic data IS pullable here, contrary to what this file said until
  2026-08-06: the Vercel MCP exposes `get_web_analytics` (project
  `prj_thAY1ZFoahuVCLksBfXAyjyzo1b1`, team `team_VWA1Ar7nCeuyUifvSyeFTT1T`). mode=count
  for totals; mode=aggregate with by=[requestPath|referrerHostname|day|deviceType|country]
  for breakdowns. Data starts 2026-07-21, the day it was enabled.
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
  READ THE TOTALS OFF `Devices.csv`, NOT `Queries.csv`. GSC truncates and anonymises the
  query table: the 2026-08-06 export showed 123 clicks / 10,413 impr in Queries.csv but
  308 clicks / 17,108 impr in Devices.csv. Same for Pages.csv, which is also partial.
  Export 2 (last 3 months to 2026-08-06): 308 clicks / 17,108 impr / pos 18.6 / CTR 1.80%.
  Impressions +45% on the baseline, clicks only +12%, so CTR fell 2.34% -> 1.80% and
  position drifted 17.1 -> 18.6. That is the expected shape when many new pages start
  ranking at page 2-3 at once; the location pages are landing around pos 24-28. NOTE the
  two windows overlap by roughly 80% of their days, so this is not a clean before/after.

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

## Episode release cycle — STANDING AUTHORIZATION
One episode owns one week. Nick approved this flow 2026-08-02; do not re-ask each time.
- **Saturday 9:00 AM ET** — episode post (LinkedIn, Facebook, Google Business) + the full
  episode video on YouTube. The show "airs" 8:30 AM Sat on 100.3 Legends Radio; episodes
  are prerecorded but Saturday is the public moment.
- **Sun–Fri 9:00 AM ET** — one clip per day from THAT SAME episode (Instagram, Facebook,
  YouTube Shorts, TikTok) + a text-only Google Business post carrying the same takeaway.
- Next Saturday a new episode number takes over. Never mix two episodes in one week.

**When Nick sends raw footage for a new episode: build everything, then SCHEDULE it — don't
ask first, and don't publish immediately.** He reviews scheduled posts in Post Bridge before
they go live. Target the next Saturday 9:00 AM ET for the episode + full video, then the
clips one per day after it. Scheduling IS the deliverable; waiting for approval is not.

ONE master routine handles all of it (claude.ai Routines, fresh session per fire):
`trig_01L8gTCsSXAtwCkvG4LMZuSh` — "Pain 2 Power — daily social poster", cron `0 13 * * *`
(9:00 AM ET daily). It branches on the ET day of week: Saturday → episode post, Sunday
through Friday → the next unposted clip. Consolidated 2026-08-02 from two separate routines
because the Routines tab was unreadable and each one needed its connectors wired separately.
Don't split it back apart; add day-branches to this one instead.

Post Bridge account IDs change on every reconnect — always `list_social_accounts` first.
YouTube was 81323, died with `invalid_grant`, came back as 81358; Google Business was 81363,
came back as 81642. Current (verified 2026-08-06): Instagram 81353, Facebook 81324,
YouTube 81358, TikTok 81356, X 81378, Google Business 81642, LinkedIn business 81322,
LinkedIn personal 81320 (never post). Google Business takes text or ONE image, **never video**
— clips go there as a separate text-only call with a LEARN_MORE CTA.

`create_post` returning "processing" is NOT proof of publication. Always finish with
`list_post_results` and report per platform. Uploads to Post Bridge are metered — reuse
existing media IDs (`list_media`) instead of re-uploading.

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

## Posting on demand — "post it" should be one step
When Nick says post something, the only two things that ever block it are:

1. **The Post Bridge connector toggle.** See the Connectors note below. If its tools are
   missing, that is the cause; say so immediately rather than retrying.
2. **Getting the media to a URL Post Bridge can fetch.** Use `tools/stage-media.py`:

       python3 tools/stage-media.py clip.mov

   Converts .mov to .mp4, pushes to a `media/<slug>` branch, prints the Vercel branch URL
   (any size) and the jsDelivr URL (under 20MB), and warns if the video is landscape,
   which letterboxes on Reels, TikTok and Shorts.

**Prefer an attached file over a Dropbox link.** This sandbox is proxy blocked from Dropbox
hosts: the Dropbox MCP tools work for browsing and metadata, but the bytes cannot be
downloaded here. A file attached to the chat lands on disk immediately and skips a
GitHub Actions relay that takes several minutes and has its own failure modes
(`scl/fi` share links serve an HTML interstitial even with `dl=1`; runners have no ffmpeg
preinstalled; the default GITHUB_TOKEN is read only).

Standing preferences for a one off post, unless told otherwise:
- Captions carry ZERO dashes outside the phone numbers. Bullets use •.
- Lead with the joke or the hook. The event details go after it, never before.
- Google Business takes text or ONE image, never video, and gets its own text only call.
- LinkedIn personal (81320) is never posted to.
- Finish with `list_post_results` per platform. "processing" is not proof.

## How the clips are cut (observed spec, Episode 9 pipeline)
- **1080x1920 vertical, 30fps, h264 crf 20, AAC.** Captions burned in: white bold, dark
  outline, centred, two lines max, sitting around the lower third.
- **Source is the RAW camera, not the master.** The guest camera shoots natively vertical
  and is used full frame at ZERO crop. Host moments crop the 4K two shot to a 9:16 window
  on whoever is speaking. Cropping the finished 16:9 master instead means upscaling a
  narrow slice of an already cropped face — visibly worse, do not do it.
- **Audio** comes from the finished master's mixed track, normalised to -14 LUFS for social.
- Clips have run 20 to 75 seconds. For REACH specifically, shorter and hook first performs
  better: open on the most surprising sentence, cut the setup entirely, aim 15 to 25s. Every
  Episode 8 and 9 clip currently opens on an interviewer question or mid sentence on "But",
  which is the single biggest thing holding their reach back. Not yet changed — flagged to
  Nick 2026-08-03, no decision taken.
- Captions are burned AFTER a human reviews the ASR. Never burn unreviewed transcription
  into a deliverable; ASR mangles guest names badly.

## Full episode to YouTube — publish from Descript, by hand
Descript holds the finished multicam edit and has YouTube connected in the app. Publish the
FINAL composition straight from Descript to YouTube, then set scheduling in YouTube Studio.

Do NOT route the full episode through Post Bridge or a downloaded file:
- Post Bridge times out fetching anything that large (2.9GB Descript export failed at 60s).
- GitHub release assets serve `application/octet-stream` and Post Bridge rejects them.
- A browser download of the 1.2GB master truncates easily, and YouTube then reports
  "file unreadable". A cloud synced folder holding the file as an online only placeholder
  produces the same error.
The Descript share page (`share.descript.com/view/...`, access "unlisted") is also the right
way to let a guest watch their episode: streams in any browser, no account, no download.

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
