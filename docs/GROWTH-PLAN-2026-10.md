# First Rehab growth audit and plan, October 2026

Prepared 2026-10-14 from every source available: the patient export and SPRY screenshots
(aggregates only), Google Business Profile and GA4 through Windsor.ai, the lead table in
Supabase, Vercel, Search Console figures from the weekly sweeps (latest 2026-10-12), the
NPI Registry, CMS and Medicare.gov, a fresh crawl of lawofficesuccess.com, and Google's
own 2026 guidance. Nothing patient-identifiable is in this file.

## 1. Bottom line: the five levers, ranked

1. **Reviews (Google Business Profile).** 8 new reviews in the last 12 months, and none
   since August 14. That is under 1% of new patients. Reviews and review recency are a top
   map-pack factor, and the map pack is where "physical therapy near me" (the #1 non-brand
   GBP search, 18 to 28 people a month) and every city-qualified search gets answered.
   Asking every discharged patient, by text, with firstrehabnpb.com/review, is the single
   highest-return action available. It costs nothing.
2. **Referring physicians.** About 89% of appointments carry a referring physician in SPRY.
   279 doctors referred; 73% sent exactly one patient. Turning one-time referrers into
   repeat referrers moves more volume than any web change. The November patient education
   event with RegenOrtho and Abacoa is the natural first touch.
3. **Work the leads you already get.** 79 real website leads since July, 33 in the last 30
   days, and 0 have an outcome recorded. The front-desk account still has no app login.
   Until leads are marked contacted or booked, nobody can say which pages produce
   patients, and leads go cold.
4. **Measurement that sees conversions.** GA4 recorded no calls, booking clicks or leads
   until this PR. Now it will, once the three events are marked as key events.
5. **Depth on pages that already rank, not more pages.** Search clicks rose 27% in the
   last 28 days after depth work (position 20.2 to 16.5). The thin-page era added
   impressions and removed clicks. Long form goes where demand already exists.

## 2. What the data says

**Patients (export of 1,396 records):** median age about 71, 67% are 65 or older, 57%
female. Medicare is about half of patients and visits; commercial plus Medicare Advantage
about a third; auto and personal injury 5% of patients but 9% of visits. 36% live in 33408,
23% in Palm Beach Gardens zips, 14% in 33404 (Riviera Beach and Singer Island), 8% Jupiter,
about 5.5% list an out-of-state address. 16% stop at three visits or fewer, and 47% end
"inactive" rather than discharged. Cancellations include reschedules, so they are not a
loss measure.

**Search (sweep 2026-10-12, 28 days to Oct 9):** 161 clicks, 10,387 impressions, CTR
1.55%, average position 16.5. Gains are holding but flat week over week. City-qualified
queries earn almost no clicks even at positions 3 to 7, because the map pack answers
them. Non-city service terms ("hand therapist", Medicare queries) are winnable.

**GA4 (Sep 8 to Oct 12):** 634 sessions. Organic search 304 (66% engaged), direct 279,
organic social 34, referral 8, AI assistants 5. The homepage is 57% of landings. Old Wix
URLs were still landing visitors on a 404 page (`/sports-training`,
`/adult-wellness-programs`, `/specialist-first-rehab-npb-services-offered`, old
`/quality_auto/` image paths).

**Google Business Profile (2026, monthly):** impressions steady at roughly 1,000 to 1,100,
with September at 974. Calls peaked at 147 in January (season) and ran 88 to 110 a month
since May. Search is mostly mobile and mostly branded ("first rehab", 42 to 56 a month).
Searchers also confuse us with "PAM rehab" and other "First ..." clinics, which is another
reason review volume and a complete profile matter. The listing has a pending edit.

**Leads (Supabase):** 89% come through the contact-page form; insurance is blank on 94%;
September ran 8 to 11 a week.

## 3. How Google ranks a clinic like ours in 2026, and what we do about it

- **Local pack:** relevance (primary category, services, descriptions), distance (we
  cannot change it), prominence (reviews, recency, mentions around the web). Our lever is
  prominence: reviews, photos, posts, and consistent name, address and phone everywhere.
- **Organic:** helpful, first-hand, specific content from named, credentialed people.
  The March 2026 core update favoured official and specialist sources over aggregators.
  Our edge is real clinicians and a real CORF; we now show verified credentials.
- **Spam policies to stay clear of:** doorway pages (near-duplicate city pages),
  scaled content (bulk posts), structured data that does not match the visible page, and
  hidden text. That rules out "hidden blogs" and hidden schema entirely.
- **FAQ rich results ended 7 May 2026.** FAQ markup still validates and helps machines
  read the page, but produces no visual result. Ours stays because it matches the page.
- **AI Overviews and AI Mode:** Google says no special schema or AI files are needed.
  What gets cited is clear, specific, sourced content. The Medicare guide and the glossary
  are built for that, and llms.txt now points to both.

## 4. lawofficesuccess.com, re-audited 2026-10-14

Twelve blog posts in total, all in the Yoast sitemap, about one a month, newest
September 17. **There are no hidden blogs.** What works there: few, deep posts (around
1,900 words), answer-first intros, question-style headers, comparison tables, an A to Z
glossary, heavy internal linking, and an author with a visible identity. What not to copy:
a sitewide FAQ schema block whose questions are not on the pages, and template pages left
live with placeholder text. "The Reddit thing" is most likely a Reddit profile listed as
part of an author's public identity; Reddit reads no schema.

What we took: the glossary (now live, with markup generated from the visible list), the
long-form standard (applied first to the Medicare guide), tables, sources, and stronger
author identity through verified credentials.

## 5. Shipped in this PR

- Verified clinician credentials on every page and in Person schema (NPI Registry plus
  public profiles), with Joan "Joni" Janik's legal name in schema and stable @ids.
- GA4 now receives `call_tap`, `book_click` and `generate_lead`.
- 301s for the old Wix URLs still landing visitors on the 404 page.
- The 404 page no longer emits two conflicting robots tags.
- A 2026 Medicare guide on /insurance.html (about 1,400 words; the page is now about 1,850),
  with a comparison table, five official sources, CORF explained, and maintenance therapy
  under the Jimmo settlement.
- /glossary.html: 39 patient terms with DefinedTermSet markup generated from the page.
- The October 12 post brought up to the playbook, with its title tag moved off the
  homepage's primary keyword.
- BLOG-PLAYBOOK.md: the 1,700 to 2,000+ word pillar standard, and when to use it.

## 6. Owner actions (no code), in order

1. **Reviews:** text every discharged patient firstrehabnpb.com/review, and keep the QR card
   at the front desk. Target 6 to 8 new reviews a month. Reply to each without confirming
   the reviewer is a patient.
2. **Lead inbox:** create the Supabase app login for firstrehabnpb@gmail.com, then mark this
   week's leads. Docs: docs/LEAD-INBOX.md.
3. **GA4:** Admin, Events, mark `call_tap`, `book_click` and `generate_lead` as key events.
4. **Google Business Profile:** check what the pending edit is; add photos monthly; keep the
   weekly GBP posts running.
5. **YouTube:** upload the Episode 18 full video so the site's video schema can include it.
6. **Physician referrals:** pull SPRY's referral report; call the 58 doctors who sent 2 to 4
   patients and the 18 who sent 5 or more; invite them to the November event.
7. **Discharge and reactivation:** a scripted call or text at visit 3 and again for patients
   who went inactive in the last 90 days (from SPRY, kept out of the repo).

## 7. Decisions for Nick

- **New long-form pillar guides:** the blog freeze from 2026-09-09 is still in place for new
  posts. Lifting it for 1,700+ word pillar guides on topics no page owns (hand therapy for
  carpal tunnel, knee replacement recovery timeline) is your call. The rules for doing it
  are written.
- **City pages:** you chose "enrich them" before I had the Search Console finding that city
  queries earn about one click per thousand impressions even at positions 3 to 7. Adding
  words does not fix a map-pack problem, so I did not enrich them. The lever for those
  towns is the Business Profile (reviews, service area, categories).

## 8. Next 90 days and how we will know

| Metric | Baseline | Target by mid-January |
|---|---|---|
| New Google reviews per month | under 1 | 6 to 8 |
| Leads with an outcome recorded | 0% | 90%+ within 3 days |
| Website leads per month | 33 | 45 |
| GSC clicks per 28 days | 161 | 220 |
| GBP calls per month | 88 to 110 | 130+ in season |
| Initial evaluations per week | about 22 | 30 |

January is high season, so compare with last January (147 GBP calls), not with October.

## 9. Competitor teardown

Why nearby clinics outrank us, the name collision with a similarly named clinic, and the
verified list of wrong NPI, Healthgrades, LinkedIn and Yelp records: `docs/LOCAL-AUTHORITY-AUDIT-2026-10.md`.

## 10. Guardrails

No PHI in the repo, analytics or schema. No patient stories without signed authorization.
No ad pixels or health-condition remarketing without a privacy review. Free offers to
Medicare patients get a compliance review first. No fake reviews, no invented credentials,
no fake addresses, no hidden content, and schema only for what the page shows.
