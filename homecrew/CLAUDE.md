# CLAUDE.md

Context for Claude Code working on this repo. Read this before making changes.

## What this is

Marketing site + internal field-inspection tool for **HomeCrew**, a firefighter-owned home watch company in Stuart, Florida. Home watch = scheduled inspections of vacant/seasonal homes, with a photo report sent to the owner after every visit.

Two audiences, one codebase:
- `index.html` — public marketing site. Sells to homeowners (mostly snowbirds).
- `portal.html` — internal tool. A technician signs in, looks the client up by name,
  reads the gate code and key box combination off the property record, walks a
  25-point inspection, and the app generates the client-facing report.

## Current state

**Working:** the entire public site. In the portal: real Supabase Auth, the client
directory (search by name or address, per-property access codes, visit history),
property-linked inspections, draft autosave, live scoring, report generation and
persistence to the `inspections` table.

**Not working — this is the job:** photos still live in browser memory instead of
Storage, and `send-report` has no PDF renderer or email key, so "Send to client"
returns a visible error. See `docs/ROADMAP.md` tasks 3 and 4.

**Before any of it runs against real data** the owner has to create the Supabase
project and paste the URL + anon key into `config.js` — see `docs/SETUP.md`. While
those are blank the portal runs in SAMPLE MODE: three invented clients, every code
`0000`, nothing saved. Sample mode exists to demo the flow, not to hold real data,
and the directory screen says so in red.

## Stack

Plain static HTML/CSS/JS, no build step. Two self-contained files with inline `<style>` and `<script>`.

**Do not convert this to React/Next/Vite unless the owner explicitly asks.** It's a five-page brochure site plus one form. A framework adds a build pipeline, a deploy story, and a dependency tree to maintain, in exchange for very little here. If the portal grows past ~3 screens, revisit — that's the actual threshold, not aesthetics.

The portal is now at exactly three screens (directory, inspection, report). That is
the line, not a breach of it — but the *next* screen is the trigger to reconsider.
The Supabase JS client loads from a CDN `<script>` tag, which keeps the no-build
setup intact; don't npm-install it.

Backend target is **Supabase** (Postgres + Auth + Storage + Edge Functions), hosting is **Vercel**. Both are already chosen; schema and a function skeleton are in `supabase/`.

## Conventions

- **Design tokens are CSS custom properties** in `:root` at the top of each file's `<style>`. Never hardcode a hex value — use `var(--navy)`, `var(--gold)`, etc. See `docs/BRAND.md`.
- **Two fonts only.** Montserrat for anything uppercase/display, Nunito Sans for body. Montserrat is nearly always uppercase with wide letter-spacing (`.12em`–`.22em`) — that spacing *is* the brand.
- **Icons are inline SVG**, 24×24 viewBox, `stroke: currentColor`, `fill: none`, `stroke-width: 1.6`. No icon font, no icon library.
- **No CSS framework.** No Tailwind, no Bootstrap.
- Vanilla JS, no jQuery. `var`/`function` style in `portal.html` for consistency — match it or refactor the whole file, don't mix.

## Layout gotchas

**The image fallback pattern.** Both the hero and the firefighter card have an SVG illustration on a layer *beneath* the photo (`.hero-art` / `.ff-art` at `z-index:1`, photo at `z-index:2`, gradient at `z-index:3`, text at `z-index:4`). If a photo fails to load, the illustration shows instead of a broken image. Preserve this when touching either section. It also means: if you open `index.html` without the `images/` folder present, you'll see illustrations and think the photos are missing. They aren't.

**Gradient coverage.** Both photo areas have a navy gradient over roughly the left half so white text stays readable. Any replacement photo needs its subject on the right.

## Content rules — read before editing copy

- **The stats bar no longer carries invented numbers.** `100+ homes` and `5★ rating` were placeholder data from a design mockup and are gone, replaced with facts about the service itself (25 points, 5 systems, 24/7, insured & bonded). Do not put a home count or a star rating back in — here or in the schema markup — without real, verifiable figures from the owner. Fabricated review data is an FTC problem and can get a Google listing penalized.
- **Service area is five counties**: Indian River, St. Lucie, Martin, Palm Beach, Broward (owner's call, 2026-08). They appear in four places — the meta description, `areaServed` on the LocalBusiness node *and* on both Service nodes, the FAQ answer in JSON-LD and its visible twin, and the footer list. Change all of them together.
- Pricing in `index.html` (Bronze $99 / Silver $199 / Gold $399) appears in **two** places: the visible cards *and* the `hasOfferCatalog` block in the JSON-LD. Change both or Google will flag the mismatch.
- Same for NAP (name, address, phone): footer, schema, and Google Business Profile must match character-for-character. It's a local ranking factor.
- The FAQ answers make claims about Florida insurance policies. They're hedged deliberately ("many policies", "ask your carrier"). Don't tighten them into guarantees.

## SEO — already done, don't undo

`index.html` has a `@graph` JSON-LD block covering LocalBusiness, WebSite, WebPage, two Services, an OfferCatalog, and FAQPage. Plus OG/Twitter cards, canonical, geo meta, semantic headings.

If you edit the JSON-LD, validate at `search.google.com/test/rich-results` before committing. It's one blob — a trailing comma silently kills all of it.

`portal.html` is `noindex` and disallowed in `robots.txt`. Keep it that way.

## Security — the part that matters most

This app will hold **client home addresses, alarm details, and photos of vacant properties**. That's a burglary kit if it leaks. Treat it accordingly:

- Row Level Security on every table, no exceptions. The migration enables it — don't disable it to make something work.
- Storage bucket is **private**. Serve photos via signed URLs with short expiry, never public URLs.
- Only ever use the Supabase **anon** key client-side. The service role key goes in Edge Function secrets and nowhere else — never in `portal.html`, never in `config.js`, never in a committed `.env`. `config.js` holding the URL and anon key IS safe to commit; that is what it is for.
- Emailed reports contain addresses and interior photos. Confirm the recipient address comes from the property record, not from a form field a technician could typo. The portal enforces this: "Send to client" refuses on an inspection with no `property_id`, and the Edge Function reads the address off the property row rather than the request body.
- **Access codes never enter a client report.** Gate code, key box combination, alarm and garage codes render masked in the directory, reveal on tap, and re-hide after 30 seconds. `renderReport()` reads none of them — keep it that way. A report is emailed and then forwarded onward; a code in one is a code in somebody's inbox forever.
- Migration `0002` moved credential reads from "any authenticated user" to **active crew only**, and dropped the `properties_field` view, which never actually protected anything (the base-table policy allowed the same select). Deactivating a crew row is now a real revocation. Read the header comment in that file before rewriting those policies.

## Verifying changes

No test suite. Manually:
1. `npm run dev`, open `localhost:3000`
2. Public site: check 1440px, 900px, 390px. Nav collapses to a burger under 1040px.
3. Portal: sign in, search the directory by name and by address, open a profile,
   reveal a code and confirm it re-hides, then "Start inspection" and check the
   address/email prefilled from the record.
4. Clear all 25 lines, confirm scores compute, generate a report, print preview it.
5. Mark items "Watch"/"Issue" and confirm they surface in Attention Items.
6. Reload mid-inspection — the draft must come back with the ticks intact.
7. Confirm no access code appears anywhere in the generated report.
8. Rich Results Test on the public page.

## Public site sections

Order: hero → why → stats → protocol (`#home-watch`) → report preview (`#report`)
→ pricing → concierge → coverage (`#areas`) → FAQ → contact.

**`#report` is a mock of the real thing.** The document on the right of that section
mirrors what `renderReport()` in `portal.html` emits — score ring, five system
scores, attention items, photo grid. If the report layout changes in the portal,
change it here too. It is the promise the marketing site makes on the portal's behalf.

**Motion is decoration and is guarded.** Scroll reveals and the stat counters sit
behind both `prefers-reduced-motion` and an `IntersectionObserver` feature check; if
either says no, everything renders static and visible. Never let a reveal be the only
thing making content readable.
