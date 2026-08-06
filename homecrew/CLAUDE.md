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
directory (search by name or address, faceted filters, per-property access codes,
visit history), the route screen with turn-by-turn handoff to Google/Apple Maps,
property-linked inspections with a photo and collapsible note on every one of the
25 lines, live scoring, report generation, photos in private Storage, an outbox
that retries failed submissions, and cross-device draft sync.

**Not working — this is the job:** `send-report` has no PDF renderer or email key,
so "Send to client" returns a visible error and the crew sends the PDF by hand.
That is the honest failure mode and the only remaining engineering task. See
`docs/ROADMAP.md` task 4.

**The backend is live.** Supabase project `Home Crew` (`fuznycuqxbrwkaiuayjs`),
all six migrations applied, keys in `config.js`. What is still empty is the
data: crew accounts, clients and properties are entered by the owner — see
`docs/SETUP.md` steps 4 and 5. Until a crew account exists, a correct password
still gets "not an active crew member", which is the intended answer.

Blank keys in `config.js` drop the portal into SAMPLE MODE: three invented
clients, every code `0000`, nothing saved. It exists to demo the flow, not to
hold real data, and the directory screen says so in red. If the Supabase client
script fails to load, the portal does **not** fall back to sample mode — it
disables sign-in and says it is broken. A portal quietly showing fake data to
someone standing at a real house is worse than one that admits it is down.

## Stack

Plain static HTML/CSS/JS. **`build.py` is the single source of truth for every
public page** — all copy, services, counties, packages, FAQ and blog posts live
in it. Edit it, run `python3 build.py`, and all 22 pages regenerate in place.
Never edit a generated `.html` file directly; the next build overwrites it.

This is not the framework the next section rules out. There is no React, no
bundler, no dependency tree and nothing to install — the output is plain static
HTML. It mirrors the generator on the firstrehabnpb site. It arrived when the
site went from one page to 22, because a hand-maintained nav and footer copied
across 22 files is how a phone number ends up wrong on three of them.

**`portal.html` is NOT generated.** It is an application, hand-maintained, with
inline `<style>` and `<script>`. The public site shares `assets/css/site.css`
and `assets/js/site.js`, both linked with content-hash cache busters from
`asset_v()` — never link either without one.

**Do not convert this to React/Next/Vite unless the owner explicitly asks.** It's a five-page brochure site plus one form. A framework adds a build pipeline, a deploy story, and a dependency tree to maintain, in exchange for very little here. If the portal grows past ~3 screens, revisit — that's the actual threshold, not aesthetics.

The portal is at four screens (route, clients, inspection, report), which is one
past the threshold written above. It is still not a framework problem — the file
is long but flat, and every screen is `showView()` plus a render function. What a
fifth screen would actually justify is splitting `portal.html` into
`portal.html` + `portal.js`, not adopting React. Reach for that first.
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
- Migration `0003` closed `is_owner()` and `is_active_crew()` to signed-out callers. Do not "finish the job" by revoking EXECUTE from `authenticated` too — RLS policy expressions run with the caller's privileges, so that makes every table return "permission denied" instead of an empty result. Verified on the live project; the header comment in `0003_function_hardening.sql` has the details. The two remaining Supabase advisories are accepted for this reason.
- Migration `0002` moved credential reads from "any authenticated user" to **active crew only**, and dropped the `properties_field` view, which never actually protected anything (the base-table policy allowed the same select). Deactivating a crew row is now a real revocation. Read the header comment in that file before rewriting those policies.
- Migration `0006` gives `inspection_drafts` the only policy set here with **no
  `is_owner()` branch** — a technician's in-progress draft is private from the
  owner too, deliberately. The reasoning is in that file's header; read it before
  "fixing" the omission. It also revokes EXECUTE on `touch_draft()` from `public`,
  `anon` **and** `authenticated`: Supabase's default privileges grant to the
  latter two directly, so revoking PUBLIC alone leaves a function exposed at
  `/rest/v1/rpc/`. That is the mirror image of the 0003 trap — there the revoke
  was too broad, here it has to be broader than it looks. Safe for this one
  because Postgres checks EXECUTE on a trigger function when the trigger is
  created, not on every write (verified against the live project).
- **Draft photos are deletable by their owner, filed photos are not.** The
  storage delete policy is scoped to `drafts/<caller uid>/%` precisely so it
  cannot become a way to erase a filed inspection's evidence. Don't widen it.

## Verifying changes

**There is a test suite now**: `node test/durability.js` with a local server on
port 8912 (`NODE_PATH` pointing at a tree with `playwright-core`). 50 scenarios,
each one a way a technician's work could be lost — photos across a reload, two
houses open at once, offline submit queued, outbox surviving a reload while still
offline, two devices on one draft, conflict resolution, a filed inspection
cleaning up its own draft photos. `test/fake-supabase.js` is the double; the
comment at its top explains why `__fail` and `__failInsert` are separate flags
(conflating them produced two false failures once).

Run it after any change to persistence, sync or submission. Then manually:
1. `python3 build.py`, then `python3 -m http.server 8000`
2. Public site: check 1440px, 900px, 390px. Nav collapses to a burger under 1040px.
3. Portal: sign in, search the directory by name and by address, open a profile,
   reveal a code and confirm it re-hides, then "Start inspection" and check the
   address/email prefilled from the record.
4. Clear all 25 lines, confirm scores compute, generate a report, print preview it.
5. Mark items "Watch"/"Issue" and confirm they surface in Attention Items.
6. Reload mid-inspection — the draft must come back with the ticks intact.
7. Confirm no access code appears anywhere in the generated report.
8. Rich Results Test on the public pages.
9. Re-run BOTH axe sweeps after any colour or markup change — the generated
   pages, and separately the signed-in portal driven through every view (see
   the warning under Accessibility about why a cold load of `portal.html`
   proves nothing). The site passes
   **WCAG 2.1 AA with zero violations across all 24 pages** (23 generated plus
   the portal) and it stays that way:
   `npm i --no-save axe-core playwright-core`, serve on a local port, inject
   `axe.min.js` per page with animations disabled and `.reveal` forced visible.

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

## Accessibility — do not regress this

Zero axe violations across the 22 generated pages **and across every signed-in
portal view**, verified at 1440px and 390px.

**Read this before trusting a past "the portal is clean".** An earlier sweep
loaded `portal.html` cold and reported zero violations — which was true and
useless. Every view but the login screen is `display:none` until you sign in,
and axe skips hidden elements, so "the portal passes" really meant "the login
screen passes". Auditing the actual app found four real defects the crew would
have hit daily: `.crumb` gold at 2.2:1, the selected OK and Watch chips carrying
white text at 3.4:1 and 2.5:1, the report's section headings at 2.4:1, and
unlabelled photo caption inputs (critical — 25 identical unnamed text boxes).
A portal sweep must drive the app: sign in, open a client, open a property,
mark lines, attach a photo, generate the report. Anything less audits a form
with a password box on it.

The colour tokens are the load bearing part:

- `--gold` **#CBA15A is for dark backgrounds and borders only** (7.15:1 on navy,
  2.4:1 on white). Light-background text uses `--gold-text` **#7E5F27**
  (5.9:1 white, 5.4:1 paper). `.eyebrow` defaults to `--gold-text`; the dark
  sections opt back into `--gold` by selector. Do not "fix" an eyebrow that
  looks dull on a white section by switching it to `--gold`.
- `--gray` is **#5A6167**, not #6B7178. The old value failed at 4.13:1 on the
  paper-2 stats band.
- Status colours come in two families and the split is deliberate, in the
  portal exactly as on the public site. **#2E9E5B / #D89A2B are decoration
  only** — dots, borders, the score ring. Anything carrying white text, or
  standing as text on a light surface, uses **#246F41 (green) and #8F6611
  (amber)**, exposed in the portal as `--ok-deep` / `--watch-deep`. White on
  #2E9E5B is 3.4:1 and on #D89A2B is 2.5:1; both fail. #C0392B (red) is 5.4:1
  with white and needs no deep variant. `band()` in `portal.html` returns the
  deep values because every one of its callers paints text.
- The portal has `--gold-text` #7E5F27 now, same as the public site, for the
  same reason: `--gold` is 7.2:1 on navy and 2.2:1 on `--paper`. `.crumb` and
  the report's `h4` headings use it. `--gray` in the portal is #5A6167 (it was
  #6B7178); every use is on a light surface, so this is strictly an improvement.
- Dim white text on navy is `.62` alpha minimum, not `.45`.
- Concierge price rows use a `::after` pseudo-element for the dotted leader. The
  old `<span class="led-dots">` sat between `<dt>` and `<dd>` and broke the
  definition-list structure rule. Do not put an element back in there.

## Site structure

22 generated pages: home, `services/` index plus four service pages, `reports`,
`pricing`, `service-area` plus five county pages, `about`, `faq`, `contact`,
`blog/` index plus four posts. Also generated: `sitemap.xml`, `robots.txt`,
`llms.txt`, `site.webmanifest` and `404.html` (deliberately kept out of the
sitemap).

Adding a page: write a `build_*()` function, call it from `main()`, and pass a
unique `title` (~50-70 chars), `desc` (~110-175 chars) and `canonical` to
`head()`. `write()` adds it to the sitemap automatically. Interior pages get a
`BreadcrumbList`; service pages get `Service`; county pages get `Service` with
that county as `areaServed`; posts get `BlogPosting`.

New blog post: add a dict to `BLOG_POSTS`. Body is a list of `(kind, value)`
tuples — `p`, `h2`, `h3`, `ul`, `callout`. Add `seo_title` if the headline runs
past about 60 characters. Content rules from above still apply: facts only,
nothing invented, insurance claims stay hedged.
