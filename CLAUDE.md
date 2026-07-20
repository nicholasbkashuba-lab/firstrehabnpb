# First Rehabilitation of North Palm Beach — Website

Static site for firstrehabnpb.com. 26+ pages, generated — do not edit HTML files directly.

## Architecture
- **`build.py`** is the single source of truth: all page content, team roster, condition copy,
  blog posts, podcast episodes, contact info. Edit it, then run `python3 build.py` to regenerate
  every page in place.
- `assets/css/styles.css` — the whole design system (deep teal #0E3A47, cream #F6F1E7,
  coral #F4A261, gold #E9C46A; Playfair Display + Inter). Signature elements: rotating
  lighthouse beam on dark sections, film grain, interactive body map, social marquee.
- `assets/js/main.js` — nav, scroll reveals, counters, marquees, body-map tap panel.
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
  lighthouse.mp4 (hero video), podcast-cover.jpg, photos.
- `assets/team/` — staff portraits. `assets/social/post-1..8.jpg` — homepage gallery tiles.

## Workflow
1. Edit `build.py` (or CSS/JS)
2. `python3 build.py`
3. Preview locally: `python3 -m http.server 8000` → http://localhost:8000
4. Commit & push → Vercel auto-deploys

## Conventions
- Phone 561-624-4263 · 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408
- Tagline: "Our people make the difference." · Motto headline: Heal. Strengthen. Thrive.
- New blog post: add to BLOG_POSTS dict. New episode: add to EPISODES list (it also
  needs its Spotify episode URL). New team member: add to TEAM + photo in assets/team/.
- Keep quotes/testimonials verbatim; don't invent credentials or clinical claims.
- Intake agent copy lives in `assets/js/intake.js` (STEPS object). It is plain JS served
  to every visitor — never put secret keys in it (the Supabase publishable key is safe by design).

## SEO — keep this maximized on every change
The build already emits, for every page: a unique `<title>` and meta description, a
`rel=canonical` URL, Open Graph + Twitter Card tags, MedicalBusiness JSON-LD schema
(address, hours, geo, 5.0 rating, areaServed), favicons/apple-touch/manifest, `sitemap.xml`,
and `robots.txt`. When adding or changing pages, preserve all of it:

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
