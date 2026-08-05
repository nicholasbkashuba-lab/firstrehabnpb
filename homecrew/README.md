# HomeCrew

Marketing site and crew inspection portal for HomeCrew — a firefighter-owned home watch company serving Stuart, FL and the Treasure Coast.

## Quick start

```bash
npm run dev          # serves on http://localhost:3000
```

No build step, no dependencies. Static HTML/CSS/JS.

- `index.html` — public marketing site
- `portal.html` — crew login → client directory → inspection form → generated client report

The portal runs in **sample mode** until `config.js` has real Supabase keys: any
email signs you in, three invented clients appear, every code is `0000` and
nothing is saved. See `docs/SETUP.md` to point it at a real project.

## Working with Claude Code

Read **`CLAUDE.md`** first — it has the conventions, layout gotchas, content rules and security requirements. Claude Code picks it up automatically.

Then **`docs/ROADMAP.md`** for the ordered task list. Tasks 1, 2 and 5 are done;
photo upload to Storage (3) and PDF email delivery (4) are what is left.

## Structure

```
├── CLAUDE.md                 # project context for Claude Code — read first
├── index.html                # public site (inline CSS/JS, no build)
├── portal.html               # crew portal (inline CSS/JS, no build)
├── images/                   # optimized WebP + JPEG, desktop + mobile crops
├── config.js                 # Supabase URL + anon key (safe to commit; see SETUP)
├── supabase/
│   ├── migrations/0001_init.sql            # schema + RLS + storage bucket
│   ├── migrations/0002_client_directory.sql # access codes + crew-only RLS
│   └── functions/send-report/              # PDF + email delivery (skeleton)
├── docs/
│   ├── BRAND.md              # colors, type, voice, logo, assets
│   ├── SETUP.md              # owner steps: create the project, add crew + clients
│   └── ROADMAP.md            # ordered build tasks
├── vercel.json               # security headers + asset caching
└── .env.example
```

## Status

**Done:** entire public site. In the portal — Supabase Auth, client directory with
per-property access codes, property-linked inspections, draft autosave, live
scoring, report generation and persistence.

**Not done:** photos still live in browser memory instead of Storage, and report
email delivery is a skeleton, so "Send to client" errors rather than pretending.

## Before shipping

1. **Create the Supabase project and fill in `config.js`** — `docs/SETUP.md`. Nothing in the portal touches real data until this is done.
2. Replace `firefighter-turnout-gear.jpg` with a real photo of the owner in gear (current one is an upscaled low-res placeholder).
3. Set up the Google Business Profile — for "home watch near me" it outranks the website itself. NAP must match the footer exactly.
4. Validate JSON-LD at `search.google.com/test/rich-results`.
5. Submit `sitemap.xml` in Search Console.

## Contact

HomeCrew — Stuart, FL · 561-383-0882 · HomeCrewFL@gmail.com · homecrewfl.com
