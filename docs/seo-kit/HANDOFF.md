> **STATUS (2026-10-14): background strategy, partly superseded.** Written before the repo was read. Platform is NOT Wix or WordPress (static build.py on Vercel; see CLAUDE.md). Facts, credentials, blog rules and priorities now live in CLAUDE.md, BLOG-PLAYBOOK.md, SEO-KEYWORDS.md and docs/*-2026-10.md. Still useful: section 4 (lawofficesuccess.com audit), section 5 (Halo 2.0 mapping), section 5b (Google 2026 landscape) and section 7 (guardrails).

# HANDOFF: First Rehabilitation of North Palm Beach, Growth, SEO & Entity Build

**Owner:** Nick Kashuba (COO). **Date:** 2026-10-14.
**Audience:** Claude Code. Use every relevant skill and tool you have. Work in phases, verify each one, and ask Nick only about blocking items listed in Section 9.

> "Perfect" is not a measurable target, so the target is this: every item in Section 8 passes, nothing on the site contradicts itself, and every claim is supportable. Do not stop at "looks good." Run the checks.

---

## 1. Mission

Grow First Rehab's new-patient volume and local authority by building recognized, trustworthy, well-structured web presence, applying the "Halo Marketing Strategy 2.0" framework (authority + familiarity + entity recognition) adapted for a healthcare clinic, using what Nick's patient data and a competitor-style site audit showed.

**North-star metric:** new initial evaluations per week. Baseline is about 22 per week (about 1,150 in roughly 12 months, from the scheduling system). Target: 30 per week.
**Supporting metrics:** branded search impressions ("First Rehab North Palm Beach"), Google Business Profile calls and direction requests, referring-physician count with 5+ patients (baseline 18), early-dropout rate, reviews per month.

## 2. Business facts (single source of truth)

- Name: First Rehabilitation of North Palm Beach ("First Rehab"). Family-owned outpatient PT/OT clinic, a Medicare-certified CORF. Founded 1991 by David Kashuba, Ph.D.
- Address: 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408. One location only.
- Services: physical therapy, occupational therapy, certified hand therapy (Laura Drumm), integrated wellness/gym program ("F.I.T. by First").
- Podcast: Pain 2 Power (co-host Mike McGann).
- Clinicians to profile (credentials as stated by Nick): Laura Drumm (certified hand therapist); David Kashuba (founder; Ph.D. and DPT); Kayla Dorsey, DPT; Logan Van Sant, DPT; Joni Janik, OTD (Doctor of Occupational Therapy; the scheduling system lists her as "Joan Janik," so confirm the display name). Licenses and certifications still need to be confirmed by each clinician.
- Payers: Medicare, plus BCBS, Humana, Aetna and others; some personal-injury/auto work.
- **Platform conflict to resolve first:** Nick says the site is WordPress, but earlier project notes describe the First Rehab site as Wix. Verify which. The PHP in `build_schema.py` output is WordPress-only; Wix would need custom-code injection.
- **Access check:** confirm who holds admin access to the website, domain/DNS, Google Business Profile, and Google Search Console (an outside SEO vendor may control some). Do not change anything you cannot roll back.

## 3. What the patient data says (aggregates only)

Sources: a patient export (1,396 records, 1,043 with visits) and screenshots of the scheduling system's reports. **Never put patient-level data in the repo.** The raw export stays out of version control.

**Who the patients are**
- Median age about 70.7; about 67% are 65+. Age bands: under 18 1%, 18-39 7%, 40-54 9%, 55-64 16%, 65-74 30%, 75-84 27%, 85+ 11%.
- 57% female, 43% male.
- Payer mix: Medicare about 48% of patients and 50% of visits; commercial and Medicare Advantage about 34%; auto/personal-injury/network about 5% of patients but 9% of visits (24.6 visits per patient vs 13.3 overall); payer blank for about 13%.
- Service line: musculoskeletal about 91%; occupational therapy about 12% (OT patients average the most visits, about 15.6; about 41% of OT patients are working-age). Wellness is not captured in this system.
- Geography (Florida patients): 33408 (North Palm Beach/Juno) 36%, 33404 (Riviera Beach/Singer Island) 14%, Palm Beach Gardens zips 33410+33418 23%, Jupiter about 8%. About 5.5% of patients list out-of-state addresses (seasonal).

**Referrals**
- 279 distinct referring physicians; 73% sent exactly one patient; 18 sent five or more; the top 10 account for 23% of referred patients.
- The export's referring-physician field is filled for only 48% of patients, but the scheduling system tags about 89% of appointments with a referring physician. Use the scheduling system's referral report as the source of truth for any referral work.

**Retention and volume**
- 47% of patients are "inactive" (stopped without being discharged); 33% discharged; 20% active.
- About 16% of treated patients stopped at three visits or fewer. 76 patients went inactive in the last 90 days.
- About 14,700 completed appointments; initial evaluations are 7.8% of appointments.
- Recorded collections about $946K over about 12 months ($704K insurance, $122K copays, $120K self-pay); March-September full months averaged about $102K per month.
- Average paid per visit $84.52 overall; self-pay $77.24 vs insurance $73.35 (self-pay barely above insurance, a pricing flag).
- Billing units: 97110 is about 49% of units; 97750 (physical performance testing) is about 1%.

**Caveats you must respect**
1. Cancellation counts include reschedules and are not a reliable loss measure. Do not build strategy on the 25% cancellation figure.
2. Most appointments are booked under David Kashuba and Kayla Dorsey for convenience, so provider-utilization numbers are meaningless. Do not use them for capacity decisions.
3. "Visits" in the export appear to be 12-month counts.
4. A possible unpaid-visit gap (collections vs appointments) is unverified. Do not publish or act on it without reconciliation.

## 4. What the competitor-style audit found (lawofficesuccess.com)

A friend's consulting site (law-firm CRM/intake advisory, not a law firm). Findings:
- Small site: about 12 blog posts, all linked and in the sitemap. No true "hidden blogs." Posts run roughly 1,900 words (newer ones longer), with an answer-first intro, 8 question-style H2s, H3s, 1-2 comparison tables, a table of contents, a 5-question FAQ, `Article`/`Person`/`BreadcrumbList` schema, and about 50 internal links per post.
- Strong patterns worth copying: topic clusters by category, heavy internal linking, an A-Z glossary (about 50 terms, definition plus example), service pages that open with the customer's own words and end with a process and FAQ, geo/service page templates, an author page with credentials and links.
- **Do NOT copy:** his sitewide FAQPage schema lists five generic questions that do not appear on the pages (a structured-data guideline violation). Also his template pages with lorem ipsum and leftover text from other clients are live in his sitemap, and his organization schema links to a LinkedIn profile under a different name than his author. Avoid all three.
- Traffic claims could not be verified.

## 5. Halo 2.0 applied to First Rehab (healthcare guardrails included)

| Halo tenet | Work to do |
|---|---|
| Authority + Entity (1, 11) | Clinician bio pages with `Person` schema (see `clinician-bios.md`); clinician bylines and "medically reviewed by"; consistent bios across site and directories |
| Familiarity + Omnichannel (2, 5) | Pain 2 Power clips to YouTube/social/GBP; one consistent message; use existing podcast-clip automation |
| Emotional + Social proof (3, 9) | Only with written HIPAA authorization for any patient story; ask every discharged patient for a Google review; reply to reviews without confirming someone is a patient |
| Community (4) | November patient education event page and follow-up; local co-promotions |
| AEO/GEO (6) | Question-style pages and a glossary written for people. Google says no special schema or AI files are needed (Section 5b). FAQ markup only where Q&As are visible and page-specific; FAQ rich results ended in May 2026 |
| Retargeting (7) | Do NOT use health-condition remarketing or the Meta pixel on the site without a privacy/HIPAA review. Use email to existing patients instead |
| Outbound value (8) | Patient newsletter; referring-physician update with outcomes (no PHI) |
| Measurement (10) | Call tracking by source, "how did you hear about us" field, Search Console, GA4 (Section 7) |

## 5b. Google landscape as of 2026-10-14 (researched; added after the first draft)

Source tags: **[G]** Google's own documentation. **[T]** trade press or industry data (Search Engine Land, SE Ranking, Whitespark). **[V]** vendor blog, unverified. Claude Code: re-check https://status.search.google.com before any launch. I could not read the dashboard directly, so the update dates below come from third-party reports of it.

**Confirmed**
- **[G] AI Overviews and AI Mode need no special optimization.** Google says there are no extra requirements, no special schema, and no AI text files (so no llms.txt effort). Standard SEO applies: the page must be indexed and snippet-eligible, crawlable, internally linked, and have good page experience. Structured data must match visible text. AI-feature traffic is counted in Search Console under the "Web" search type.
- **[T] FAQ rich results ended on 7 May 2026.** The FAQPage markup type is not deprecated and validates, but it no longer produces a visual result. The Search Console FAQ report and Rich Results Test FAQ check were scheduled for removal in June 2026 and API support in August 2026. **This corrects my earlier statement that FAQ rich results still appear for health sites.** Do not promise stars-and-dropdowns.
- **[G] Doorway abuse includes location pages.** Google's policy covers pages targeted at specific cities that funnel users to one page, and substantially similar pages. **Scaled content abuse** covers mass-producing pages without user value, including with AI. Hidden text is abuse, but accordions, tabs, and sliders are fine.
- **[G] Generative AI content guidance** (page dated 2026-10-01; the specific changes are not described): AI may be used, but "manually factcheck and review all AI-generated content," including titles, meta descriptions, structured data, and image alt text.
- **[T] March 2026 core update** (followed a March spam update): volatility was high (about 80% of top-3 URLs moved). Gainers: official, institutional, specialist/niche, and established brands. Losers: aggregators, directories, comparison sites. In health, broad consumer-health sites fell while clinical and specialist sources gained.
- **[T] Later 2026 updates:** May core update (began 21 May), spam updates in June, August, and **24 September 2026, which third-party reports say was still rolling out in early October**. Google has not named a target. No October core update had been announced as of 7 October.
- **[T] Whitespark 2026 local ranking factors:** Local pack: primary GBP category, proximity, GBP title keywords, address in the searched city, business open at search time, ratings, review count and text. Local organic: a dedicated page for each service ranks first, then city relevance and inbound links. AI visibility leans on third-party mentions and citations. Reviews and behavior signals gained weight. Predefined GBP services rose sharply. Concise, scannable service pages are favored over long copy.

**Unverified; do not cite or build strategy on them:** vendor figures for AI Overview click-through drops, zero-click rates, "X% of health searches get an AI answer," and claims that FAQ schema makes AI citation likelier.

**Decisions for First Rehab**
1. **FAQ:** keep FAQ content (patients read it) but expect no rich result. Use FAQPage markup only on pages where the same Q&As are visible and page-specific. No sitewide generic FAQ blocks. No rush to rewrite what already exists.
2. **AI visibility = ordinary SEO + specialist authority + third-party mentions.** Skip llms.txt and similar files.
3. **Location pages are the highest-risk item in this plan.** Build only the Jupiter page first. Each location page must contain facts that exist only for that area (directions, local-use conditions, timing, local physicians' referral logistics without PHI, seasonal-resident needs) and sit under a browsable /locations/ hub. Never clone with a swapped city name. Add Palm Beach Gardens or Riviera Beach/Singer Island only after Jupiter shows traction in Search Console. Set expectations: the map pack favors proximity and a physical address in the searched city, so Jupiter map-pack wins are unlikely; target organic and AI answers.
4. **Scaled content:** the 12-post plan is acceptable only with real clinician review. Log a named reviewer and review date for each post. Every post needs first-hand material (clinician explanations, how First Rehab handles a case type, local specifics) and cited primary sources (CMS, APTA, NIH). No bulk AI generation. Fact-check titles, meta, schema, and alt text.
5. **Core-update posture:** be the specialist source. Named clinician authors, primary-source citations, no thin "best PT near me" roundup pages, no directory-style pages.
6. **Spam-update timing:** record a baseline first (Search Console clicks/impressions/queries for the top pages, GA4 conversions, GBP calls and direction requests, current rankings for 20-30 target terms). Release in stages (schema and bios, then glossary, then service pages, then location page, then blog), log each change date, and avoid broad site-wide changes during an active rollout.
7. **Local / Google Business Profile checklist:** primary category Physical Therapist; add Occupational Therapist and other accurate secondary categories; fill every predefined service; list real services with descriptions; hours correct (including holidays) because "open now" is a ranking factor; business name exactly as it appears on signage (no keyword stuffing, which risks suspension); photos; regular posts; review requests after every discharge with no incentives; reply to every review without confirming patient status. Whitespark flags address visibility and proper pin placement as factors; do not hide the address.
8. **Mentions:** earn third-party references with the real name, address, and phone: APTA Florida chapter, local chambers, local news and events, referring physicians' sites, podcast guest swaps, and community sponsorships. Track new mentions monthly.
9. **Measurement additions:** in Search Console compare impressions vs clicks (stable impressions with falling clicks suggests AI features, not lost rankings); track branded queries; in GA4 create a channel group for AI referrals (chatgpt.com, perplexity.ai, copilot, gemini); watch directory-sourced traffic separately.
10. **Other levers not yet covered elsewhere:** Bing Webmaster Tools (Bing data feeds several AI assistants; lower confidence); accessibility and readability for an older audience (large tap targets, contrast, click-to-call at the top of every page); speed-to-lead (answer calls and appointment requests within a set time, script the intake call, capture "how did you hear about us"); page speed on mobile.

## 6. Work to do (phased)

**Phase 0: Recon (do first).** Audit the live site (platform, theme, plugins, existing schema, sitemap, robots, indexation, speed, accessibility, mobile). Identify duplicate or conflicting schema from SEO plugins. Check Search Console for index status and coverage. Write findings to `AUDIT.md`.

**Phase 1: Foundation.**
- Fix the entity basics: consistent name/address/phone everywhere, Google Business Profile completeness, Bing/Apple listings, Healthgrades and APTA directory listings.
- Implement the sitewide schema from `build_schema.py` (`MedicalClinic`, `Physiotherapy`, `WebSite`, `PodcastSeries`) after replacing every placeholder (domain, phone, logo, image, hours, social links). Remove duplicate plugin schema.
- Validate in Google's Rich Results Test and validator.schema.org, then run `python3 scripts/check_schema_visible_match.py <file-or-URL>` on every page type. Use `schema-library.md` as the template source for all page types (blog, service, location, glossary, event, podcast, video).

**Phase 2: Pages.**
1. Clinician bio pages (5) from `clinician-bios.md`, after collecting real data from each clinician.
2. Therapy glossary from `glossary.md` (clinician review first; confirm the service-specific terms and policy placeholders).
3. Jupiter location page from `jupiter-page.md`, under a /locations/ hub. Add Palm Beach Gardens or Riviera Beach/Singer Island only after Jupiter shows traction in Search Console, each with facts unique to that area. Google treats near-duplicate city pages as doorway abuse (Section 5b).
4. Cornerstone service pages: Medicare outpatient therapy and CORF; balance and fall prevention; hand therapy; post-surgical rehab; auto accident and personal-injury therapy (plus an attorney-facing page); a seasonal-resident page; a "for referring physicians" page.
5. FAQ page using the 15 Q&As in `first_rehab_qa_training.py`, with `FAQPage` schema that matches the visible text exactly.

**Phase 3: Blog.** About 12 posts over 90 days (one per week), each:
- Typically 1,700-2,000 words for pillar guides (length is not a ranking factor; shorter is fine when the question is simple, and service pages should be concise and scannable), on a single question, plain language (aim for roughly 8th-grade reading level), warm but clinical, no slang, no outcome guarantees.
- 40-60 word answer first; 6-8 question-style H2s with H3s; one or two comparison tables; a "when to see a PT" callout; a visible 5-question FAQ with matching schema; clinician byline and review line; 3-5 internal links to service pages and sibling posts; `Article` schema with the real author's `Person` node.
- Topic order: Medicare/CORF, fall prevention, hand therapy, post-surgical knee/shoulder/hip, auto accident therapy, Jupiter/Palm Beach Gardens, winter residents, plus patient-dropout-driven topics ("what happens if I stop therapy early").
- Follow `blog-template.md` (structure, word budgets, voice rules, pre-publish checklist) and its 12-post calendar; confirm demand in Search Console first.
- Run every draft through the writing-quality and AI-pattern-removal skills before review.

**Phase 4: Retention and referral systems (support work; coordinate with Nick before touching operations).**
- Reactivation list of recent inactive patients (built from SPRY data, kept out of the repo).
- Referring-physician outreach list from the scheduling system's referral report; target the 18 doctors with 5+ patients and the 58 with 2-4.
- Cancellation recoding: make "Reschedule" a distinct, required status linked to the new booking; count only cancels with no rebooking within 7 days as true losses.
- Pricing review of self-pay rates.

**Reddit (ongoing, about 1 hour/week):** follow `reddit-playbook.md`. Research first; participate only as named, disclosed clinicians approved by Dr. Kashuba; log everything.

**Phase 5: Measurement.** GA4 events (calls, form submits, appointment requests), Search Console, call tracking by source with a recording-consent announcement (Florida is an all-party-consent state), monthly dashboard against the metrics in Section 1.

## 7. Compliance and quality guardrails (hard rules)

1. **Structured data must match visible page content.** Never put text in schema that visitors cannot see. No "hidden blogs." No cloaking.
2. **HIPAA:** no PHI in repos, prompts, schema, or analytics. No patient stories without signed authorization. Do not install ad pixels on the site without a privacy review.
3. **Health claims:** nothing implies a cure or guaranteed result. No "best," no unsupported statistics. Every clinical page gets a named clinician review line and date.
4. **Medicare:** have counsel review any free-screening or giveaway offered to Medicare beneficiaries before launch.
5. **No fake reviews, fake local addresses, or invented credentials.** Jupiter is a service area, not an office.
6. **Reddit:** there is no Reddit schema and Reddit does not read structured data. Reddit matters only because its threads appear in Google and AI answers. Allowed: clinicians answering questions in their own name with disclosure. Not allowed: astroturfing, sockpuppets, or fake testimonials.
7. **Doorway/scaled-content rule:** no near-duplicate city pages, no bulk-generated posts. Every page must give a searcher something the other pages do not.
8. **Generative-AI rule (Google, 2026-10-01 doc):** a human clinician fact-checks everything, including titles, meta descriptions, structured data, and alt text, before publishing.
9. Do not publish template or placeholder pages (lorem ipsum or "TODO" text). Add a check that fails the build if "TODO" or "lorem" appears in any published page or schema.

## 8. Definition of done (verify all)

- [ ] Platform and access confirmed; no unrollbackable changes made.
- [ ] Sitewide and per-page schema valid (Rich Results Test and validator.schema.org), no duplicates, no errors.
- [ ] `scripts/check_schema_visible_match.py` exits 0 on every published page type (wired into the build or deploy step).
- [ ] Every FAQ in schema appears word-for-word on its page.
- [ ] No "TODO", "lorem", "REPLACE", or placeholder phone/domain strings remain in published output.
- [ ] All new pages in the sitemap, indexable, canonical correct, internal links present (3-5 per page), no orphan pages.
- [ ] Core Web Vitals and mobile checks pass; accessibility checks (headings, alt text, contrast) pass.
- [ ] Name/address/phone identical across the site, Google Business Profile, and directories.
- [ ] Clinician-reviewed and dated: every clinical page, the glossary, and each bio.
- [ ] Reading level and AI-pattern check done on all copy.
- [ ] Measurement live: GA4 events firing, Search Console connected, call tracking tested.
- [ ] Baseline snapshot recorded before the first change; each release date logged.
- [ ] Search Status Dashboard checked before each release; no broad site-wide changes during an active update rollout.
- [ ] Google Business Profile checklist (Section 5b, item 7) complete.
- [ ] Each location page passes the unique-content test; only one location page live until traction is shown.
- [ ] Each blog post has a named clinician reviewer and review date logged.
- [ ] A short `CHANGELOG.md` and a rollback note written.

## 9. Blocking questions for Nick (ask once, together)

1. Is the First Rehab site on WordPress or Wix, and who has admin access (site, DNS, Google Business Profile, Search Console)?
2. Real domain, main phone, fax, email, hours, and confirmed accepted-payer list.
3. Self-pay rates (or permission to leave them off).
4. Florida license confirmation, certifications, headshots, and preferred display names (including "Joni" vs "Joan") for Laura, David, Kayla, Logan, and Joni; and the credential format David wants displayed (Ph.D., DPT).
5. Which services are truly offered (splinting, functional capacity evaluations, fall-prevention, wellness details)?
6. Date, time, and place of the November patient education event.
7. Cancellation/no-show policy wording.

## 10. Files in this kit

- `HANDOFF.md`: this file.
- `glossary.md`: 41-term patient glossary (needs clinician review and the TODOs filled).
- `jupiter-page.md`: Jupiter service-area page draft with FAQ.
- `clinician-bios.md`: bio page template, intake sheet, and `Person` schema.
- `first_rehab_qa_training.py`: 15 Q&As and helper functions (single source for FAQ text).
- `build_schema.py`: generates sitewide schema JSON-LD, an HTML snippet, and a WordPress PHP snippet. Imports the Q&A file.
- `schema-library.md`: JSON-LD templates for every page type (blog, service, Jupiter, glossary, event, podcast/video, optional FAQ) plus rules and a "what not to build" list.
- `blog-template.md`: post skeleton, heading and voice rules, pre-publish checklist, 12-post calendar.
- `reddit-playbook.md`: what Reddit is and is not, compliant participation rules, measurement.
- `scripts/check_schema_visible_match.py`: stdlib-only checker (placeholders, invalid JSON, FAQ and glossary text not visible, review markup, duplicate `@id`). Exit code 1 on failure.
