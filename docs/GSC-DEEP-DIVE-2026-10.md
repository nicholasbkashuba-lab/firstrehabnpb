# Search Console deep dive, October 2026

Pulled 2026-10-14 with `tools/gsc.py` against the URL-prefix property
`https://www.firstrehabnpb.com/` (the only one that has data). Aggregates only; the raw
exports stay out of the repo. Windows end 2026-10-11 because Search Console finalises on a
three-day lag.

- **28-day totals** (Sep 14 to Oct 11) come from the zero-dimension API row, so they are exact.
- **Query-level figures** come from the query table, which Google truncates and anonymises.
  Over 90 days the query table holds 19,290 of the site's 33,902 impressions, so treat every
  query figure below as directional. Positions are impression-weighted averages, and where
  one query ranks several of our URLs the variants (UTM-tagged homepage, `/about` vs
  `/about.html`) are merged.
- **Excluded everywhere:** home-visit queries (the clinic does not offer in-home therapy),
  `site:` lookups, and a stray phone number.

## The five numbers

| Metric, last 28 days | Previous 28 days | Last 28 days | Change |
|---|---|---|---|
| Clicks | 133 | **156** | +17% |
| Impressions | 11,356 | **10,601** | -7% |
| CTR | 1.17% | **1.47%** | +0.30 pts |
| Average position | 20.2 | **16.6** | 3.6 places better |
| Striking-distance queries (pos 4 to 20, 10+ impressions, non-brand) | | **68** (28 days); **142** over 90 days | |

Of the 142 striking-distance queries over 90 days, **69 are not city-qualified** (North Palm
Beach counts as home, not as a city qualifier, because the clinic is there). Those 69 carry
3,939 impressions and 14 clicks. The other 73 name a town we serve from North Palm Beach,
and CLAUDE.md already records that those are a Google Business Profile lever, not a
page-content one. 90-day totals for context: 434 clicks, 33,902 impressions, CTR 1.28%,
position 18.9.

Fewer impressions, more clicks and a better position is the shape the September depth
work was meant to produce: thin location-page impressions falling away while pages that
can win the click move up.

## 1. Striking distance, by the page that ranks

Non-city queries only, 90 days.

| Page | Queries | Impressions | What they are |
|---|---|---|---|
| `/` (homepage) | 25 | 1,778 | Generic: "physical rehabilitation services" (pos 14.8), "physical therapy palm beach county" (16.7), "physical therapy rehabilitation" (18.7), plus North Palm Beach condition queries the homepage is answering instead of the condition page (shoulder 6.4, headache 4.1 to 8.6) |
| `/locations/west-palm-beach.html` | 11 | 766 | "near me" terms with no city in them: "physical therapy near me" 387 at 14.2, "auto accident physical therapy near me" 148 at 9.8 (6.9 on this page) |
| `/treatments/neck-pain.html` | 13 | 631 | North Palm Beach neck queries: stiff neck, pinched nerve, neck and shoulder pain, cervical pain. Zero clicks |
| `/locations/palm-beach.html` | 3 | 217 | "physical rehabilitation specialist" 138 at 14.5 |
| `/treatments/back-pain.html` | 4 | 125 | North Palm Beach low back and stenosis. Zero clicks |
| Old Wix URLs (`/blank-10`, `/blank-3`, `/blank-11`) | 4 | 200 | Headache, shoulder and neck queries still credited to redirected URLs. All three are 301'd in `vercel.json`; Google is still consolidating |
| `/services/hand-therapy.html` | 3 | 93 | "certified hand therapist near me" 50 at 17.9 |
| `/treatments/auto-accident.html` | 1 | 57 | "car accident rehab" at 18.2 |
| `/treatments/workers-comp.html` | 1 | 13 | "work injury rehab" at 15.2 |

The neck and back clusters are the clearest content targets: home-market intent, positions 4
to 10, a page that exists for exactly that intent, and zero clicks on pages of 324 and 362
words.

## 2. Cannibalization

Queries where two of our pages split the impressions (each holding at least a fifth):

| Query (90 days) | Pages splitting it |
|---|---|
| physical therapist that accepts medicare palm beach (540) | `/` 173 at 19.0, `/insurance.html` 159 at 9.4 |
| physical therapy medicare palm beach (441) | `/` 186 at 16.0, `/insurance.html` 167 at 9.0 |
| hand pain treatment west palm beach (336) | `/services/hand-therapy.html` 172 at 14.7, `/treatments/hand-wrist.html` 73 at 33.4 |
| wrist pain treatment west palm beach (246) | hand-therapy 106 at 27.8, hand-wrist 86 at 19.0 |
| shoulder pain treatment north palm beach (101) | `/` 44 at 3.3, `/treatments/index.html` 38 at 7.4; the shoulder page itself only 8 at 8.1 |
| north palm beach neck pain treatment (105) | neck page 64 at 10.0, `/` 23 at 1.5 |
| neck pain relief north palm beach fl (86) | neck page 51 at 8.6, `/locations/juno-beach.html` 25 at 9.9 |
| hip pain treatment west palm beach (134) | old `/blank-2` 75, `/treatments/hip-pain.html` 58 |

Plus a long tail of "physical therapy west palm beach" variants split between the homepage
and the West Palm Beach page, all at positions 17 to 47. Those are city-qualified and stay
a Business Profile matter.

What changed for this: the Medicare split is resolving on its own (next section). The new
benefits line on every therapy service page and on the neck and back pages links to
`/insurance.html#medicare-guide`, which adds internal signal to the page that should own
Medicare intent. The shoulder page losing its own North Palm Beach query to the homepage
is recorded as the next depth candidate, not changed here.

## 3. Medicare: the baseline for the Medicare guide

The Medicare guide is in PR #104, which is not merged yet, so everything below is the
**before** picture.

| Query | 90 days | Last 28 days |
|---|---|---|
| physical therapist that accepts medicare palm beach | 540 impr, pos 20.6, 0 clicks (insurance page 159 at 9.4) | 140 impr, 0 clicks; insurance page 59 at 8.9 |
| physical therapy medicare palm beach | 441 impr, pos 18.2, 0 clicks (insurance page 167 at 9.0) | 109 impr, 0 clicks; insurance page 44 at **4.5**, homepage 43 at 17.2 |

Every other Medicare or insurance query is under 10 impressions. `/insurance.html` overall,
last 28 days: 205 impressions, 0 clicks, position 6.7. Over the last 28 days the insurance
page has overtaken the homepage for both queries, which is the right page winning. Its
title already matches the query ("Physical Therapy That Accepts Medicare | Palm Beach
County"), so it was left alone: changing it now would make the guide's effect unreadable.
Re-read both queries 28 days after #104 deploys.

## 4. Hand therapy and CHT

72 queries, 1,094 impressions, 6 clicks over 90 days.

| Query | 90 days | Last 28 days |
|---|---|---|
| hand therapist | 263 impr at 30.8 | 157 at 32.9 |
| certified hand therapist near me | 50 at 17.9, 1 click (hand page 28 at 6.5) | 29 at 25.4 (hand page 12 at 6.2) |
| hand therapist near me | 69 at 37.7, 2 clicks (hand page 16 at 13.4) | 51 at 47.3 |
| carpal tunnel syndrome therapies near me | 76 at 28.2 | 18 at **18.6** |
| hand therapy | 62 at 62.6 | 14 at 62.0 |

Compared with the 2026-09-09 pull ("hand therapist" 95 impressions at 28.7, "carpal tunnel
syndrome therapies near me" 25 at 37.2): demand for "hand therapist" has grown but position
has not moved, while carpal tunnel moved from 37 to about 19. Where the hand page itself
ranks for the near-me practitioner terms it sits at 6 to 13; the averages are dragged down
by the West Palm Beach page also ranking at 50 to 80. The hand page was deepened in
September; it gets four to eight weeks before it is touched again, so it is not changed
in this PR.

## 5. Auto accident, PIP, workers' comp and return to work

- **Auto:** 30 queries, 607 impressions, 0 clicks. The auto page holds "car accident rehab"
  (57 at 18.2) and "auto injury rehabilitation" (47 at 24.7), 229 impressions in all (excluding `site:` lookups) at
  an average of 21.0. The biggest auto query, "auto accident physical therapy near me" (148),
  ranks the West Palm Beach page at 6.9 instead. No query mentions PIP yet. The question
  "what should I expect during my first rehabilitation appointment after a car accident?"
  ranks the auto page at 4.9 (31 impressions), which is exactly what the new "first visits"
  section answers.
- **Workers' comp and work injury:** 16 queries, 174 impressions, 0 clicks. "work injury
  rehabilitation" 58 at 30.4, "comp rehab" 57 at 39.0, "work injury rehab" 13 at 15.2. The
  workers' comp page draws 181 impressions at an average of 39.8.
- **Return to work / ergonomics:** "ergonomic evaluation in palm beach gardens" 34 at 44.5
  (city-qualified). No non-city return-to-work query has volume yet; the OT and workers'
  comp depth is a bet on the patient data (occupational therapy patients stay longest and
  many are working age), not on existing search demand.

## 6. Brand

28 branded queries, 1,766 impressions, 128 clicks over 90 days.

- **9 of them, 536 impressions (30% of branded impressions) and 8 clicks, look meant for the
  other, similarly named clinic:** "first rehab palm beach gardens" (192), "first rehab west
  palm beach" (117), "first rehab of palm beach gardens" (85), "first rehab of west palm
  beach" (64), "first rehab palm beach lakes" (31), "first rehab lake worth" and "of lake
  worth" (38), "first rehab lakewood" (5), "first rehabilitation west palm beach" (4). They
  name towns where that clinic has offices and we do not.
- Another 48 impressions are unrelated businesses that share the words ("first rehab usa",
  "first rehab life", "health first rehab").
- The plan for this is in `docs/LOCAL-AUTHORITY-AUDIT-2026-10.md` section 8. Nothing on the
  site names or mentions the other clinic, and nothing in this PR does.

## 7. Branded vs non-branded

From the query table, so directional:

| Window | Branded | Non-branded |
|---|---|---|
| Last 28 days | 43 clicks / 559 impr / **7.7%** / pos 5.0 | 13 clicks / 6,674 impr / **0.19%** / pos 21.7 |
| 90 days | 128 / 1,766 / 7.3% / pos 5.5 | 29 / 17,524 / 0.17% / pos 23.2 |
| CLAUDE.md baseline, 28 days to 2026-09-06 | 31 / 550 / 5.6% | 6 / 1,786 / 0.34% |
| Wix baseline, 90 days to 2026-07-19 | | 0.36% |

Branded CTR is up (5.6% to 7.7%). Non-branded clicks doubled (6 to 13), but the non-branded
impression count in the September baseline came from a much smaller slice of the query
table, so the CTR comparison is not like for like. What can be said: non-branded CTR is
still about 0.2%, the same as the Wix site, and the site-wide click gain is mostly branded
and Business Profile traffic.

## 8. Title and description rewrite candidates

Pages with impressions but CTR far below what their position should earn. Most pages that
look like candidates on the page report (contact, about, services, FAQ, treatments index)
are actually sitelinks under branded searches, so their low CTR is not a snippet problem.
Measured at query level, excluding brand and `site:`:

| Page | Evidence (90 days) | Action in this PR |
|---|---|---|
| `/treatments/neck-pain.html` | 13 North Palm Beach neck queries, 593 impr at 8.2 across our pages, 0 clicks | Title and description rewritten; page deepened 324 to 1,149 words |
| `/treatments/back-pain.html` | 6 North Palm Beach back queries, 191 impr at 6.5, 0 clicks | Title and description rewritten; page deepened 362 to 1,091 words |
| `/treatments/auto-accident.html` | 229 impr at 21.0, 0 clicks | Title and description name PIP; page deepened 730 to 1,402 words |
| `/treatments/workers-comp.html` | 181 impr at 39.8, 0 clicks; title was 67 characters and the description carried an em dash | Title and description rewritten; page deepened 314 to 1,107 words |
| `/insurance.html` | 205 impr at 6.7, 0 clicks (28 days) | **Left alone** so the Medicare guide can be measured |
| `/exercises.html` | Mostly `site:` lookups | Description fixed for accuracy only: it called Dr. Kashuba a physical therapist; he is an occupational therapist |

Every title change, with before and after, is in `SEO-KEYWORDS.md` under "Title changes,
2026-10-14".

## What to re-read, and when

Around 2026-11-15 (four weeks after deploy), with `gsc.py compare --days 28`:
1. The North Palm Beach neck and back clusters: position and CTR on the condition pages.
2. "car accident rehab", "auto injury rehabilitation" and any PIP query on the auto page;
   whether the auto page starts taking "auto accident physical therapy near me" from the
   West Palm Beach page.
3. "work injury rehab" and "work injury rehabilitation".
4. The two Medicare queries on `/insurance.html`, once #104 is live.
5. Whether the old `/blank-*` URLs have dropped out.
