# HomeCrew

Marketing site and crew inspection portal for HomeCrew — a firefighter-owned home watch company serving Stuart, FL and the Treasure Coast.

## Quick start

```bash
python3 build.py                 # regenerate all 22 pages
python3 -m http.server 8000      # http://localhost:8000
```

No dependencies, no bundler. `build.py` writes plain static HTML.
**Never edit a generated `.html` directly — edit `build.py` and rebuild.**

- `build.py` — every page's content and structure lives here
- `portal.html` — crew login → client directory → inspection form → generated client report (hand-maintained, not generated)

The Supabase backend is live and `config.js` is wired. What is left is data —
crew accounts and client records, entered by the owner: `docs/SETUP.md` steps 4
and 5. With blank keys the portal falls back to **sample mode**: any email signs
you in, three invented clients appear, every code is `0000`, nothing is saved.

## Working with Claude Code

Read **`CLAUDE.md`** first — it has the conventions, layout gotchas, content rules and security requirements. Claude Code picks it up automatically.

Then **`docs/ROADMAP.md`** for the ordered task list. Tasks 1, 2 and 5 are done;
photo upload to Storage (3) and PDF email delivery (4) are what is left.

## Structure

```
├── CLAUDE.md                 # project context for Claude Code — read first
├── build.py                  # SINGLE SOURCE OF TRUTH for all 22 public pages
├── portal.html               # crew portal (hand-maintained, inline CSS/JS)
├── assets/css/site.css       # the whole design system
├── assets/js/site.js         # nav, scroll reveals, counters
├── services/ areas/ blog/    # generated — do not edit by hand
├── images/                   # optimized WebP + JPEG, favicons, app icons
├── config.js                 # Supabase URL + anon key (safe to commit; see SETUP)
├── supabase/
│   ├── migrations/0001_init.sql            # schema + RLS + storage bucket
│   ├── migrations/0002_client_directory.sql # access codes + crew-only RLS
│   ├── migrations/0003_function_hardening.sql # close helpers to signed-out callers
│   └── functions/send-report/              # PDF + email delivery (skeleton)
├── docs/
│   ├── BRAND.md              # colors, type, voice, logo, assets
│   ├── SETUP.md              # owner steps: create the project, add crew + clients
│   └── ROADMAP.md            # ordered build tasks
├── vercel.json               # security headers + asset caching
└── .env.example
```

## Status

**Done:** 22 page public site — services, pricing, reports, five county pages,
blog, FAQ, about, contact — with per-page schema, sitemap, `llms.txt`, favicons
and a 404. Passes axe WCAG 2.1 AA with zero violations across all 24 pages.
In the portal — Supabase Auth, client directory with per-property access codes,
property-linked inspections with a photo and note on each of the 25 lines, draft
autosave, live scoring, report generation and persistence.

**Not done:** photos still live in browser memory instead of Storage, and report
email delivery is a skeleton, so "Send to client" errors rather than pretending.

## Before shipping

1. **Add crew accounts and client records** — `docs/SETUP.md` steps 4 and 5. The project, schema and keys are done; the tables are empty.
2. Replace `firefighter-turnout-gear.jpg` with a real photo of the owner in gear (current one is an upscaled low-res placeholder).
3. Set up the Google Business Profile — for "home watch near me" it outranks the website itself. NAP must match the footer exactly.
4. Validate JSON-LD at `search.google.com/test/rich-results`.
5. Submit `sitemap.xml` in Search Console.

## Contact

HomeCrew — Stuart, FL · 561-383-0882 · HomeCrewFL@gmail.com · homecrewfl.com
