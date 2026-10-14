# SEO and growth research kit: START HERE

Everything from the October 2026 deep research is in this repo. This page says what each file
is, whether it is current, and which file wins when two disagree.

**Order of authority.** When two documents disagree, follow the first one on this list:
1. `CLAUDE.md` (repo rules, Nick's standing decisions)
2. `build.py` (what the site actually ships)
3. The dated audits in `docs/` listed below
4. This kit (`docs/seo-kit/`), which is background and reference

Several kit files were written before the repo was inspected, assuming a WordPress site. The
site is a static `build.py` generator on Vercel. Anything in the kit that says "WordPress",
"plugin" or "paste into the theme" is a translation job into `build.py`, never a literal step.

## The current plan and evidence (read these first)

| File | What it is |
|---|---|
| `docs/GROWTH-PLAN-2026-10.md` | The full October audit: five levers ranked, what the data says, how Google ranks a clinic in 2026, the lawofficesuccess.com re-audit (section 4), what shipped in PR #104, owner actions, 90-day targets |
| `docs/LOCAL-AUTHORITY-AUDIT-2026-10.md` | Why nearby clinics outrank us (not schema), the name collision with the other "First Rehab", every wrong citation record (NPPES, Healthgrades, LinkedIn, Yelp), directories, links, GBP changes, the brand plan and its do-not-do list |
| `docs/seo-kit/competitor-teardown-2026-10-14.md` | Per-site evidence for the above: each competitor page's title, H1, schema types and word count |
| `docs/GSC-DEEP-DIVE-2026-10.md` | Search Console deep dive, 2026-10-14: the five numbers, striking-distance queries by page, cannibalization, the Medicare baseline for the guide, hand / auto / workers' comp / brand clusters, and the title changes made from it, with a re-read date |
| `docs/PATIENT-INSIGHTS-2026-10.md` | Aggregate patient data (age, payer, zip, visits, referrals, drop-off) and the nine actions it points to. Aggregates only; patient-level data never enters the repo |
| `docs/COWORK-LOCAL-FIXES.md` | Paste-ready Cowork prompt that fixes the listings in a browser. Owner-run, not Code |
| `BLOG-PLAYBOOK.md` | How posts are written, including the 1,700 to 2,000+ word length standard and the anti-slop rules |
| `SEO-KEYWORDS.md` | The only source of keyword targets, plus the coverage table of what each page owns |

## The kit files

| File | Status | Use it for |
|---|---|---|
| `HANDOFF.md` | Background, partly superseded | Sections 4 (lawofficesuccess.com findings), 5 (Halo 2.0 framework with healthcare guardrails), 5b (Google landscape 2026) and 7 (compliance guardrails) are still useful. Its phased work list (6) and file list (10) are superseded by the growth plan and PR #104 |
| `CLAUDE-CODE-PROMPT.md` | Current | Paste-ready prompt for the next Claude Code session: Search Console research, depth on striking-distance pages, one PR |
| `competitor-teardown-2026-10-14.md` | Current | Evidence, see above |
| `schema-library.md` | Reference | JSON-LD patterns and the rules every block must follow. Most of it already ships from `build.py`; section 10 ("What not to build") is binding. The Event block (section 6) is ready for the November patient education event once it has a date |
| `glossary.md` | Implemented | Source draft for `/glossary.html`. The live version is `GLOSSARY` in `build.py`; edit there |
| `clinician-bios.md` | Reference | Intake sheet and page template if individual clinician bio pages are ever built. Credentials in it are corrected to the verified set in `CLAUDE.md` |
| `blog-template.md` | Merged into `BLOG-PLAYBOOK.md` | The 12-post calendar (section B) is still a valid topic list for when Nick lifts the blog freeze. Check every topic against `SEO-KEYWORDS.md` first |
| `jupiter-page.md` | SUPERSEDED, do not build | Written before the GSC finding that city pages earn almost no clicks. `/locations/jupiter.html` already exists, and CLAUDE.md says no new or enriched location pages |
| `reddit-playbook.md` | Current | Compliant Reddit participation: answer questions as a named clinician, disclose affiliation, no promotion, no patient details |
| `build_schema.py` | Reference only | WordPress-era schema generator. Do not run it against the site |
| `first_rehab_qa_training.py` | Reference only | Q&A knowledge base. Live FAQ content is `FAQ_CATEGORIES` in `build.py`; the chat assistant's answers are in `assets/js/intake.js` |
| `scripts/check_schema_visible_match.py` | Usable | Checks a page's JSON-LD against its visible text. Run it on any generated page you change: `python3 docs/seo-kit/scripts/check_schema_visible_match.py <page.html>` |

## Questions that keep coming up

**"Hidden" blogs or schema.** The lawofficesuccess.com re-audit (growth plan section 4) found
none: twelve posts, all in its sitemap, about one a month. What works there is depth, answer-first
intros, tables, a glossary and a visible author. Hidden text and schema describing things the page
does not show are spam under Google's policies. We do not build either.

**Is competitor schema why they rank higher?** No. See the teardown. They win the map pack on
proximity (an office in the searched town), review volume shown on the page, a big-name
affiliation and clean citations.

**The other "First Rehab" (Burns Rd).** Formerly connected, kept the name. No legal action
(Nick). Win the brand in search and on listings; never name, report or disparage them. Plan and
do-not-do list: local authority audit section 8.

**City pages.** Not enriched and not added, on GSC evidence. City intent is a Google Business
Profile lever.

**Long-form posts.** New posts are still frozen (CLAUDE.md, Blog agent). Depth goes into pages
that already rank. Nick can lift the freeze; the rules for when he does are in `BLOG-PLAYBOOK.md`.

## Facts every file must use

Clinicians (verified 2026-10-14 against NPPES): David Kashuba, Ph.D., OTR (an occupational
therapist, never "PT", "DPT" or "M.D."); Kayla Dorsey, PT, DPT; Logan Van Sant, PT, DPT; Joan
"Joni" Janik, OTD; Laura Drumm, MS, OTR/L, CHT, CLT. Phone 561-624-4263. 733 US Highway 1,
Suite 2A, North Palm Beach, FL 33408. Medicare-certified CORF. Founded 1991. No in-home or
mobile therapy. Never publish licence numbers.
