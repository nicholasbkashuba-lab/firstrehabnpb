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
  page). Collects inquiry + contact info conversationally. Answers are drafted to localStorage
  at every step; submissions insert into the Supabase project "First Rehabilitation App"
  (table `intake_leads`, anon key is INSERT-only via RLS) with an email copy to the clinic
  inbox via FormSubmit, and failed sends queue locally + auto-retry. View leads in the
  Supabase dashboard → Table Editor → intake_leads.
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
