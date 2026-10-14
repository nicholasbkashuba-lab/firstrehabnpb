# Paste-ready prompt for a new Claude Code session

Open a new Claude Code session on the `nicholasbkashuba-lab/firstrehabnpb` repo and paste
everything inside the block. Written 2026-10-14. It works whether or not PR #104 is merged.

```text
You are continuing the SEO and growth work on firstrehabnpb.com (First Rehabilitation of North
Palm Beach). The research is done and lives in this repo. Your job is to measure with Search
Console, deepen the pages that can win, and open one PR. Do not merge it.

STEP 0. SET UP AND READ (do not skip)
- If PR #104 (branch claude/seo-maximize-2026-10) is not merged into main yet, branch from
  claude/seo-maximize-2026-10. Otherwise branch from main. Name the branch
  claude/gsc-depth-2026-10.
- Read, in this order: CLAUDE.md, docs/seo-kit/README.md, docs/GROWTH-PLAN-2026-10.md,
  docs/LOCAL-AUTHORITY-AUDIT-2026-10.md, docs/seo-kit/competitor-teardown-2026-10-14.md,
  docs/PATIENT-INSIGHTS-2026-10.md, BLOG-PLAYBOOK.md, SEO-KEYWORDS.md. CLAUDE.md wins any
  conflict, then build.py, then the dated audits, then the rest of docs/seo-kit/.

STEP 1. SEARCH CONSOLE RESEARCH
- Use tools/gsc.py. ALWAYS pass --property https://www.firstrehabnpb.com/ . The script's
  default (sc-domain:firstrehabnpb.com) is the wrong property and returns nothing, which looks
  like "no traffic". Run `python3 tools/gsc.py verify --property https://www.firstrehabnpb.com/`
  first. If auth fails, stop and report exactly what failed; do not guess figures.
- Pull and save to a scratch file (never commit raw exports):
  a. summary and compare (28 days vs the previous 28) for the site.
  b. queries with --dimensions query,page, 90 days, limit 1000.
  c. pages, 90 days.
- Analyse and write up in docs/GSC-DEEP-DIVE-2026-10.md (aggregates only):
  1. Striking distance: queries at average position 4 to 20 with real impressions, grouped by
     the page that ranks. These are the depth targets.
  2. Cannibalization: any query where two of our pages split impressions.
  3. Medicare, insurance and "accepts medicare" queries: where /insurance.html ranks now, as the
     baseline for the new Medicare guide (shipped 2026-10-14).
  4. Hand therapy and CHT queries ("hand therapist", "hand therapy", "carpal tunnel", "splint"):
     positions and owning pages.
  5. Auto accident / PIP / workers' comp / return-to-work queries.
  6. Brand: every query containing "first rehab". Note how many look like they were meant for
     the other clinic (Burns Rd, PBG, West Palm, Atlantis). Report it; never name or disparage
     them on the site.
  7. Branded vs non-branded clicks and CTR, against the baselines in CLAUDE.md.
  8. Pages with impressions but CTR far below their position's norm: title and meta description
     rewrite candidates (titles front-load the keyword plus "North Palm Beach", 50 to 60 chars;
     descriptions 150 to 160; use "treatment", not "relief").
  Exclude the home-visit queries (the clinic does NOT offer in-home therapy; see CLAUDE.md) and
  do not count city-qualified queries as a page-content opportunity.

STEP 2. DEEPEN WHAT CAN WIN (edit build.py, never the HTML)
Pick the five to eight best targets from step 1, then make these changes. Depth, never new
pages. The blog freeze on NEW posts still stands.
- Deepen the page that already owns each striking-distance query: answer-first intro,
  question-style h2s, a table where it genuinely helps, real specifics from build.py facts,
  official sources where a rule or number is stated. 1,700 to 2,000+ words only where the topic
  deserves it (see BLOG-PLAYBOOK.md "Length standard").
- From docs/PATIENT-INSIGHTS-2026-10.md:
  - Auto accident page (/treatments/auto-accident.html): Florida PIP basics
    and the 14-day rule, with an official Florida source, what documentation the clinic provides,
    and what the first visits look like. No legal advice; recommend a lawyer for legal questions.
  - /services/occupational-therapy.html and /treatments/workers-comp.html: return-to-work, ergonomics and what OT does
    for working-age patients.
  - One visible line on each service page: the front desk verifies Medicare, Medigap and
    commercial benefits before the first visit. Only if it is true as stated in build.py or
    CLAUDE.md; otherwise list it as a question for Nick.
  - Balance and fall prevention depth on the existing wellness page and strength-after-60 post.
- Rewrite titles and descriptions for the step 1 item 8 candidates. Record every title change
  in SEO-KEYWORDS.md with the date, so the next pull can measure it.
- Update the SEO-KEYWORDS.md coverage table for every page you changed.

STEP 3. VERIFY
- python3 build.py (no new warnings; the Episode 18 VIDEOS warning is expected until the
  YouTube video is live, and you must not invent one).
- python3 tools/slop-check.py --new
- python3 docs/seo-kit/scripts/check_schema_visible_match.py on every page you changed.
- The static-site-forge verify.py if it is installed (see CLAUDE.md "Verifying a change");
  otherwise run axe-core with playwright-core at 393px and 1440px on the changed pages.
- Commit every file the build touches, sitemap-dates.json included.

STEP 4. PR AND REPORT
Open a PR against main titled "GSC deep dive and depth on striking-distance pages". In the
body: the step 1 findings in plain numbers, every page changed and why, the title changes,
and a short "Questions for Nick" list. Do not merge. Report the PR link and the five numbers
that matter: clicks, impressions, CTR and position for the last 28 days, plus the count of
striking-distance queries.

HARD RULES
- No patient information anywhere: repo, analytics, schema or copy.
- Never commit the Search Console key or any secret; the repo is public.
- No new blog posts, no new or enriched location pages, no hidden text, no schema for things
  the page does not show, no review or aggregateRating markup.
- Verified credentials only: David Kashuba, Ph.D., OTR (occupational therapist, never PT, DPT
  or M.D.); Kayla Dorsey, PT, DPT; Logan Van Sant, PT, DPT; Joan "Joni" Janik, OTD; Laura
  Drumm, MS, OTR/L, CHT, CLT. Never publish licence numbers.
- Zero em dashes in prose. Keep quotes and testimonials verbatim. No invented stats,
  outcomes or claims.
- Never name, mention or disparage the other "First Rehab" clinic.
- Phone 561-624-4263. 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408.
```
