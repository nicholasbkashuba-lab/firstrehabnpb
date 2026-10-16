# Local SEO Keyword Map

The single source of keyword targets for firstrehabnpb.com. Every blog post, every Google
Business post, and every new page picks its target from this file. Nothing here was researched
on the web. Targets are derived from what the site already sells (`SERVICES`, `CONDITIONS`,
`LOCATIONS` in build.py), the 25 topic targets in BLOG-TOPICS.md, and the Search Console
observations recorded in CLAUDE.md.

No search-volume numbers appear here on purpose. We do not have a keyword tool wired in, and an
invented volume is worse than no number.

## FREEZE: no new posts as of 2026-09-09

New blog posts are frozen (Nick approved). Do not pick a target from this file for a NEW post.
The keyword map stays live for re-targeting EXISTING pages, which is the work that replaces
posting. Full reasoning in CLAUDE.md under "Blog agent". The coverage table at the bottom is
still accurate and still worth reading before touching any page's target.

## Two rules that came from real GSC data

1. **Use "treatment", not "relief", in title tags.** The 2026-08-08 export showed condition pages
   ranking 5 to 20 with near-zero CTR while titled "Relief". People search "knee pain treatment".
   The public page names still say Relief; the `seo_title` overrides say Treatment. Match the
   searcher, not the brochure. See the note at build.py:1207.
2. **Never target a primary keyword another live page already owns.** North Palm Beach has no
   location page because the homepage owns that phrase. A blog post that goes after
   "physical therapy North Palm Beach" head-on competes with our own homepage. Blog posts take the
   long tail; service and location pages take the heads.

## Geo priority

North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, Tequesta, Lake Park, West Palm Beach,
Palm Beach, Riviera Beach.

North Palm Beach is home. Palm Beach Gardens and Jupiter are the two biggest realistic gains
(both have location pages sitting around position 24 to 28). Everything below Tequesta is support.

---

## Pillar 1: Physical Therapy

Page: `/services/physical-therapy.html` · FAQ anchor: `/faq.html#physical-therapy`

**Primary (owned by the service page and the homepage, do not re-target in a post)**
physical therapy North Palm Beach

**Secondary (blog posts and GBP may target these)**
- physical therapy Palm Beach Gardens
- physical therapy Jupiter FL
- post surgical physical therapy North Palm Beach
- sports injury physical therapy Palm Beach County
- balance and fall prevention therapy for seniors North Palm Beach

**Long tail**
- how long does physical therapy take after knee replacement
- partial versus total knee replacement, and who is a candidate
- do you need a referral for physical therapy in Florida
- physical therapy before surgery instead of surgery
- what to expect at your first physical therapy visit
- knee injection versus physical therapy
- do I need an MRI before starting physical therapy
- physical therapy for back pain that runs down the leg
- how many physical therapy visits does Medicare cover

**Condition pages to link**
back-pain, neck-pain, shoulder-pain, knee-pain, hip-pain, foot-pain, ankle-pain,
headache-relief, post-surgical, auto-accident

**Location pages to link**
palm-beach-gardens, jupiter, tequesta, juno-beach, lake-park, west-palm-beach, riviera-beach,
palm-beach

**Do not claim**: in-home or mobile physical therapy. Owner confirmed 2026-09-21 that the clinic
does not do home visits, for PT or OT. See the shared note below.

---

## Pillar 2: Occupational Therapy

Page: `/services/occupational-therapy.html` · FAQ anchor: `/faq.html#occupational-therapy`

Currently the thinnest pillar on the site. One service page, one condition page that maps to it
(workers-comp), and zero blog posts. Highest marginal return of the four.

**Primary (service page)**
occupational therapy North Palm Beach

**Secondary**
- occupational therapy West Palm Beach
- return to work program after injury Palm Beach County
- post stroke occupational therapy North Palm Beach
- activities of daily living therapy for seniors Palm Beach Gardens

**Long tail**
- difference between physical therapy and occupational therapy
- what does an occupational therapist actually do
- occupational therapy after a stroke what to expect
- getting dressed and cooking again after shoulder surgery
- home and workstation setup after a hand or arm injury
- workers comp occupational therapy Florida how it works
- cognitive rehabilitation after injury what it covers

**Condition pages to link**
workers-comp, post-surgical, hand-wrist, shoulder-pain

**Location pages to link**
west-palm-beach, lake-park, riviera-beach, palm-beach-gardens

**Do not claim**: driving evaluations, home modification contracting, pediatric OT, or in-home
occupational therapy. The service page does not offer them, and the owner confirmed the home
visit point on 2026-09-21. See the shared note below.

---

## Pillar 3: Hand Therapy

Page: `/services/hand-therapy.html` · FAQ anchor: `/faq.html#hand-therapy`

Our strongest differentiator. Laura Drumm, CHT, and splints fabricated on-site. Very few clinics
in the county can say certified hand therapist, so say it.

**Primary (service page)**
certified hand therapy North Palm Beach

**Secondary**
- hand therapy Palm Beach Gardens
- hand therapy Jupiter FL
- carpal tunnel therapy Palm Beach Gardens
- custom hand splint North Palm Beach
- certified hand therapist near me Palm Beach County

**Long tail**
- early signs of carpal tunnel in your hands
- thumb arthritis exercises to get your grip back
- how long after tendon repair before you can use your hand
- what is a certified hand therapist and why it matters
- do I need hand therapy after carpal tunnel surgery
- trigger finger treatment without surgery
- wrist fracture recovery after the cast comes off

**Condition pages to link**
hand-wrist, post-surgical, workers-comp

**Location pages to link**
palm-beach-gardens, jupiter, palm-beach, tequesta

**Do not claim**: hand surgery. We rehabilitate, surgeons operate.

---

## Pillar 4: Wellness and Gym

Page: `/services/wellness.html` · FAQ anchor: `/faq.html#wellness-gym`

The other thin pillar, and the only one with no `seo_title` override in build.py. On-site gym
inside a therapy clinic is unusual and under-sold.

**Primary (service page)**
wellness gym North Palm Beach

**Secondary**
- gym program after physical therapy North Palm Beach
- personal training for seniors North Palm Beach
- post rehab exercise program Palm Beach Gardens
- senior functional fitness Juno Beach

**Long tail**
- what to do after you finish physical therapy so you do not lose progress
- is it safe to go back to the gym after a joint replacement
- strength training after 60 where to start
- balance exercises to prevent falls at home
- personal training with a therapist who knows your injury history
- staying in shape with arthritis
- pickleball conditioning for players over 50

**Condition pages to link**
post-surgical, knee-pain, hip-pain, back-pain

**Location pages to link**
juno-beach, palm-beach-gardens, tequesta, jupiter

**Do not claim**: memberships, prices, class schedules, or non-patient access. All four are on
the open owner-confirmation list in CLAUDE.md. Route them to the front desk instead.

---

## Podcast and show terms

Recap posts target the show and the guest, not the pillar keywords. That keeps them out of the
way of the pillar posts.

- Pain 2 Power podcast
- `<guest full name>` plus their specialty, for example "shoulder surgeon Palm Beach"
- `<guest full name>` plus "interview" or "podcast"
- 100.3 Legends Radio Pain 2 Power
- the episode's clinical topic phrased as a question, for example
  "why do rotator cuff repairs fail to heal"

Recap posts always link `../podcast.html` and `../videos.html`, plus the pillar service page and
any condition discussed. That is the whole point of them: they convert show attention into
service-page authority.

---

## Coverage: what each live post already owns

**All 17 posts were rewritten to the 1,700-word standard on 2026-10-14** (Nick: minimum 1,700
words, h2 and h3 structure, tables, conversational voice). Each kept the keyword in its row
below; the three knee posts were kept apart on purpose and now cross-link with each other's
keyword as anchor text. `dateModified` in each post's schema reads 2026-10-14.

Fill a hole rather than cannibalising. Update this table whenever a post ships.

| Post slug | Pillar | Keyword it owns |
|---|---|---|
| `personal-training-with-a-therapist-who-knows-your-injury-history` | Wellness | personal training with a therapist who knows your injury history (Ep 19 pillar post) |
| `pain-2-power-ep19-cake` | Pain 2 Power (Ep 19) | Shannon Cake / Newsmax anchor / working out first thing in the morning |
| `partial-vs-total-knee-replacement` | Physical Therapy | partial vs total knee replacement |
| `physical-therapy-vs-occupational-therapy` | Occupational Therapy | difference between physical and occupational therapy |
| `/exercises.html` (page, not a post) | All four | home exercises for knee / hip / shoulder pain |
| `hip-impingement-back-pain-north-palm-beach` | Physical Therapy | hip impingement treatment North Palm Beach |
| `pain-2-power-ep11-joyce` | Pain 2 Power (Ep 11) | Paul Joyce / peptides and GLP-1 muscle loss |
| `pain-2-power-ep10-mcvicker` | Pain 2 Power (Ep 10) | Dr. Zach McVicker / hip surgeon Jupiter |
| `reverse-shoulder-replacement-explained` | Physical Therapy | reverse shoulder replacement recovery |
| `what-to-expect-first-pt-visit` | Physical Therapy | what to expect at your first physical therapy visit |
| `five-morning-habits-back-pain` | Physical Therapy | morning habits for back pain |
| `why-hand-therapy-is-different` | Hand Therapy | why hand therapy is different / certified hand therapist |
| `knee-arthritis-before-surgery` | Physical Therapy | knee arthritis treatment before surgery |
| `headaches-that-start-in-the-neck` | Physical Therapy | headaches that start in the neck |
| `cartilage-transplant-knee-explained` | Physical Therapy | cartilage transplant knee recovery |
| `pain-2-power-ep15-mann` | Pain 2 Power (Ep 15) | Susan Mann / Bright Minds Processing / auditory and visual processing disorders |
| `post-stroke-occupational-therapy-north-palm-beach` | Occupational Therapy | post stroke occupational therapy North Palm Beach |
| `strength-training-after-60-fall-prevention` | Wellness | strength training after 60 / balance and fall prevention |
| `gym-program-after-physical-therapy-north-palm-beach` | Wellness | gym program after physical therapy North Palm Beach |
| `physical-therapy-and-rehab-services-in-north-palm-beach-what-we-treat` | Physical Therapy | physical therapy conditions treated / what to expect (long tail). **Was a conflict until 2026-10-14:** its title targeted the homepage primary (rule 2). The title tag now reads "What Physical Therapy Treats, and Your First Visit"; the H1 is unchanged. Same day it was brought up to the playbook (dashes, 13 bolds, zero relative links, no phone, no disclaimer, and an unverified "seen within a few days" claim removed). |
| `/insurance.html#medicare-guide` (page section, not a post) | All four | physical therapy that accepts Medicare / Medicare outpatient therapy coverage 2026 / KX modifier threshold |
| `/glossary.html` (page, not a post) | All four | physical therapy and Medicare terms defined (plan of care, KX modifier, CORF, coinsurance) |
| `/treatments/shoulder-pain.html` (page) | Physical Therapy | shoulder pain treatment North Palm Beach / rotator cuff / shoulder pain at night. Deepened 2026-10-14 (306 -> 1,324 words) with Sabesan, Simovitch and Captain Kerry quotes and Dave's home shoulder set as a table. Was losing its own North Palm Beach query to the homepage (3.3) and the treatments index (7.4) |
| `/treatments/neck-pain.html` (page) | Physical Therapy | neck pain treatment North Palm Beach / stiff neck / pinched nerve in neck / neck and shoulder pain. Deepened 2026-10-14 (324 -> 1,149 words): answer-first opener, nine question h3s, links to the headache post, exercises and the Medicare guide |
| `/treatments/back-pain.html` (page) | Physical Therapy | low back pain treatment North Palm Beach / sciatica / spinal stenosis. Deepened 2026-10-14 (362 -> 1,091 words); links the morning-habits and hip-impingement posts rather than repeating them |
| `/treatments/auto-accident.html` (page) | Physical Therapy | car accident rehab / auto injury rehabilitation / Florida PIP 14-day rule. Deepened 2026-10-14 (730 -> 1,402 words) with a PIP table sourced to Fla. Stat. 627.736 (2026). Re-check the statute after every legislative session |
| `/treatments/workers-comp.html` (page) | Occupational Therapy | work injury rehab / workers' comp therapy / return to work. Deepened 2026-10-14 (314 -> 1,107 words) with a who-does-what table sourced to Fla. Stat. 440.185, 440.13, 440.191 (2026) |
| `/services/occupational-therapy.html` (page) | Occupational Therapy | adds return to work and ergonomics depth for working-age patients (1,168 -> 1,372 words), pointing claim questions at the workers' comp page so the two do not compete |
| `/services/wellness.html` (page) | Wellness | balance and fall prevention / senior functional fitness. New section 2026-10-14 (565 -> 1,051 words). Still no prices, memberships or schedules |
| `strength-training-after-60-fall-prevention` (update) | Wellness | gained "What a fall prevention evaluation looks for" and the Medicare maintenance point, 2026-10-14 (1,018 -> 1,158 words) |
| `/treatments/headache-relief.html` (page) | Physical Therapy | chronic headache treatment North Palm Beach / cervicogenic headache / whiplash headache. Deepened 2026-10-14 (313 -> 1,488 words): answer-first opener, question h3s, a when-to-get-care table, links the headache post rather than repeating it |
| `/treatments/knee-pain.html` (page) | Physical Therapy | knee pain treatment North Palm Beach / knee arthritis / meniscus / knee replacement rehab. Deepened 2026-10-14 (334 -> 1,504 words) with Pain 2 Power surgeon quotes; links the knee arthritis, knee replacement and cartilage transplant posts |
| `/treatments/hip-pain.html` (page) | Physical Therapy | hip pain treatment North Palm Beach and West Palm Beach / labral tear / hip replacement rehab. Deepened 2026-10-14 (328 -> 1,455 words) with McVicker and Leighton quotes; links the hip impingement post and the Episode 10 recap |
| `/treatments/hand-wrist.html` (page, 2026-10-16) | Hand Therapy | SYMPTOM and condition intent: hand pain / wrist pain treatment, carpal tunnel, trigger finger. The service page keeps practitioner intent; anchors pointing here now say "Hand, wrist and carpal tunnel treatment" |
| `/treatments/post-surgical.html` (page, 2026-10-16) | Physical Therapy | post surgical physical therapy / post-surgical rehab (the knee page keeps "knee replacement rehab") |
| `/treatments/foot-pain.html`, `/treatments/ankle-pain.html` (pages, 2026-10-16) | Physical Therapy | foot pain and plantar fasciitis treatment / ankle sprain and ankle pain treatment |
| `/services/wellness.html` (title, 2026-10-16) | Wellness | wellness gym North Palm Beach / post-rehab training (also targets "rehab gym near me") |
| `/locations/palm-beach-gardens.html` (title, 2026-10-16) | Physical Therapy | physical therapy Palm Beach Gardens FL / orthopedic rehabilitation Palm Beach Gardens. The homepage also ranks 4.0 for the head term; leave it |
| `/` (homepage, no change) | Physical Therapy | **physical therapy palm beach** (140 impr at 5.9, 28 days to 2026-10-09). The Semrush list assigned it to `/locations/palm-beach.html`, which ranks 31 to 35; do not retarget that page at it, the homepage already wins |
| `/services/hand-therapy.html` (page, practitioner fix) | Hand Therapy | certified hand therapist near me / hand therapist near me. 2026-10-14: answer-first intro naming Laura Drumm, CHT, three practitioner h3s and a who-does-what table (1,308 -> 1,655 words). Six internal anchors that said "hand therapy" now say "certified hand therapist" and point here, so `/locations/west-palm-beach.html` (ranking 50 to 80 for these) stops competing |

## Title changes, 2026-10-14 (GSC deep dive)

From `docs/GSC-DEEP-DIVE-2026-10.md`, section 8. Each of these pages had impressions at a
position that should earn clicks, and earned none. Judge each on CTR at roughly the same
position, 28 days after deploy (around 2026-11-15), with `gsc.py compare --days 28`. Do not
change them again before that read.

| Page | Before | After | 90-day baseline (to 2026-10-11) |
|---|---|---|---|
| `/treatments/neck-pain.html` | Neck Pain Treatment in North Palm Beach \| First Rehab | Neck Pain & Pinched Nerve Treatment in North Palm Beach | 13 North Palm Beach neck queries, 593 impr, pos 8.2, 0 clicks |
| `/treatments/back-pain.html` | Low Back Pain Treatment in North Palm Beach \| First Rehab | Low Back Pain & Sciatica Treatment \| North Palm Beach | 6 North Palm Beach back queries, 191 impr, pos 6.5, 0 clicks |
| `/treatments/auto-accident.html` | Auto & Car Accident Physical Therapy \| North Palm Beach | Car Accident Rehab & PIP Physical Therapy \| North Palm Beach | 229 impr, pos 21.0, 0 clicks |
| `/treatments/workers-comp.html` | Workers' Comp Rehab in North Palm Beach \| First Rehabilitation (generated, 67 chars) | Work Injury Rehab & Workers' Comp Therapy \| North Palm Beach | 181 impr, pos 39.8, 0 clicks |
| `/treatments/headache-relief.html` (second pass, same day) | Headache Treatment in North Palm Beach \| First Rehab | Chronic Headache Treatment in North Palm Beach \| First Rehab | homepage answering North Palm Beach headache queries at 4.1 to 8.6 instead of this page |
| `/treatments/hip-pain.html` (second pass, same day) | Hip Pain Relief in North Palm Beach \| First Rehabilitation (generated) | Hip Pain & Labral Tear Treatment \| North Palm Beach | "hip pain treatment west palm beach" 134 impr split between old `/blank-2` (75) and this page (58) |

Descriptions changed on the same four pages (all 150 to 160 characters, phone number kept),
and on headache, knee and hip in the second pass (152 to 163 characters). Knee kept its title;
the H1s, and the hip page's name "Hip Pain Relief", did not change.
`/exercises.html` changed its description only, for accuracy: it called Dr. Kashuba a
physical therapist. **Not changed on purpose:** `/insurance.html`, so the Medicare guide in
PR #104 can be measured on the two Medicare queries (baseline in the deep dive, section 3).

## Title changes, 2026-10-16 (Semrush + GSC)

Search Console from the portal's weekly snapshots (Supabase `gsc_query_page_rows`, four weekly
snapshots, 2026-09-12 to 2026-10-09, 28 days); Semrush `phrase_organic` top 10 (US database,
national SERP, read for page type and title pattern only) for four terms. Every page changed
here was outside the 2026-10-14 measurement windows above. Re-read around **2026-11-16** with
`gsc.py compare --days 28`; judge on CTR and position for the listed queries, not clicks alone.

| Page | Before | After | Evidence |
|---|---|---|---|
| `/treatments/post-surgical.html` | Post-Surgical Rehab in North Palm Beach \| First Rehabilitation (generated) | Post-Surgical Physical Therapy & Rehab \| North Palm Beach | Semrush top 10 for "post surgical physical therapy" is PT-clinic condition pages titled that way. GSC: 20 impr at 17.4 |
| `/treatments/foot-pain.html` | Foot Pain Relief in North Palm Beach \| First Rehabilitation (generated) | Foot Pain & Plantar Fasciitis Treatment \| North Palm Beach | Rule 1 ("treatment", not "relief"); the generated description carried an em dash. "foot palm pain treatment west palm beach fl" 18 impr at 8.3 |
| `/treatments/ankle-pain.html` | Ankle Pain Relief in North Palm Beach \| First Rehabilitation (generated) | Ankle Sprain & Ankle Pain Treatment \| North Palm Beach | Rule 1 |
| `/treatments/hand-wrist.html` | Hand & Wrist Pain Treatment \| North Palm Beach FL | Hand, Wrist & Carpal Tunnel Treatment \| North Palm Beach | "wrist pain treatment west palm beach" 51 at 17.2; "hand pain treatment west palm beach" split hand-wrist 42 at 23.5 / hand-therapy 30 at 23.0 / WPB page 24 at 9.0; 0 clicks. Semrush: bare "wrist pain treatment" is Cleveland Clinic, Mayo, NYU, NHS, not winnable |
| `/services/wellness.html` | Wellness & Gym \| First Rehabilitation of North Palm Beach (generated) | Wellness Gym & Post-Rehab Training \| North Palm Beach | The only service page with no override; ~59 impr at 8.2 to 8.5, 0 clicks |
| `/locations/palm-beach-gardens.html` | Physical Therapy for Palm Beach Gardens, FL \| First Rehab | Physical Therapy Palm Beach Gardens FL \| First Rehab | 781 impr, 1 click, pos ~19; "physical therapy palm beach gardens" 67 at 24.0, "orthopedic rehabilitation palm beach gardens fl" 51 at 11.0 (now in the description). Semrush top 10: dedicated city pages with exact-match titles (Gold Coast, PBOI, Select, CORA) plus Zocdoc. Title and meta only; no body words (CLAUDE.md) |

Descriptions rewritten on all six (153 to 160 characters), each restating what the page already
says. The wellness description claims no price, membership, insurance or non-patient access.

**Internal links, same day.** The "Conditions we treat with ..." line on the service pages now
uses descriptive anchors (`COND_ANCHOR` in build.py) instead of brochure names ("Foot Pain Relief",
"Hand & Wrist Therapy"), and the physical therapy page adds foot pain and headache to its list.
Foot and ankle had no in-body inbound link before this. Condition names, H1s and nav labels
are unchanged.

**Semrush, the other finding.** "hand therapist near me" is the ASHT directory plus hospital and
clinic hand therapy service pages, so `/services/hand-therapy.html` is the right page type. It
was not touched: it is inside its 2026-10-14 window.

**Left alone on purpose:** neck, back, auto accident, workers' comp, headache and hip (2026-10-14
window), the homepage (CTR test, read 2 around 2026-11-02), `/insurance.html` (Medicare guide
measurement), hand therapy service page (window), shoulder, knee and occupational therapy (deepened
2026-10-14), and every other location page (city intent is a Business Profile lever). The
physical therapy service page title already matches the rehabilitation-services cluster
("physical rehabilitation services" 52 at 10.4, but on the homepage); its title was not changed.

## Hand therapy push, 2026-09-09

Acted on the 2026-09-09 Search Console pull. `/services/hand-therapy.html` sat at position 25.3
with "hand therapist" (95 impr) at 28.7 and "hand therapy" at 73.7 — real demand, ranking
nowhere, and unlike the city-qualified location terms these carry no map pack in the way.

Changed: the service page `seo_title` now leads with "Certified Hand Therapist" rather than
"Hand Therapy", because the noun people actually search is the practitioner; the `seo_desc`
names the specific conditions; the page gained a condition-by-condition section (702 -> 1,200
words) and `/treatments/hand-wrist.html` was deepened (422 -> 546).

Judge it on position for "hand therapist" and "hand therapist near me" (the latter was already
at 11.1, the closest thing to a winnable term the pull showed). Give it 4-8 weeks. Do not read
anything into clicks alone at this volume.

Honest expectation: bare "hand therapy" at position 73.7 is a national informational term owned
by professional bodies and hospital systems. It is not a realistic target for one clinic and
should not be treated as one. The winnable set is the practitioner and near-me variants, plus
the specific conditions.

**Ep 11 note (2026-08-22):** the Paul Joyce recap is a Pain 2 Power post, not a Wellness pillar post,
so the Wellness hole below is still open. The transcript does hold a real Wellness pillar angle that
nothing on the site covers yet: keeping muscle and strength while losing weight on a GLP-1, built on
Dave's "it's going to make you better, but it's not gonna make you healthier" and Paul's "you lose a
lot of muscle". Awaiting owner sign-off on the angle before it is written.

**Ep 15 note (2026-09-16):** the Susan Mann episode is about auditory and visual processing
disorders in children. There is no honest pillar post in that subject for us: the OT block above
says plainly **do not claim pediatric OT**, and Bright Minds Processing is the guest's own nonprofit,
not a service we offer. The pillar post therefore takes the ADULT thread in the transcript instead,
Susan Mann's finding that the same processing therapy is used with brain injury and stroke patients,
which lands on post stroke OT, a service the OT page really does list (Post-Stroke Recovery and
Cognitive Rehabilitation). The recap states in the body that we do not test for or treat APD or VPD.
Do not write a pediatric processing post off this episode.

**Holes as of 2026-09-21:** No pillar has zero posts anymore. Occupational Therapy has two, the
second being the Episode 15 pillar post on post stroke OT, which takes the "post stroke
occupational therapy North Palm Beach" secondary and also works in the "cognitive rehabilitation
after injury" and "return to work program after injury" long tails. Wellness has two, both sourced
from the Episode 8 transcript and both approved directly by Nick as an exception to the 2026-09-09
freeze: `strength-training-after-60-fall-prevention` (Dave's "the invention of the chair is one of
our demise", the "personal training for seniors North Palm Beach" secondary, the "balance exercises
to prevent falls at home" and "strength training after 60 where to start" long tails) and
`gym-program-after-physical-therapy-north-palm-beach` (the TheraBand home program behind Dave's "I
do everything I can to let people not ever come to see me", the "gym program after physical therapy
North Palm Beach" secondary, the "what to do after you finish physical therapy so you do not lose
progress" long tail). Hand Therapy has one. Physical Therapy has seven and needs nothing.
Locations referenced from a post: Palm Beach Gardens, Jupiter, West Palm Beach, Juno Beach, Tequesta.

`/exercises.html` is not a blog post but it targets long-tail exercise searches across all four
pillars, so check it before writing an exercise-led post that would compete with it.

## Homepage title/meta CTR test (started 2026-09-03)

The homepage carries more impressions than every other page combined but converts them poorly.
Rewrote the title and description to add differentiators (since 1991, one-on-one, 4.9 stars,
Medicare) while keeping "Physical Therapy North Palm Beach" front-loaded. Judge it on CTR at
roughly the same position, not on clicks alone.

| window | impressions | clicks | CTR | avg position |
|---|---|---|---|---|
| baseline, 2026-06-03 to 2026-08-31 (90d) | 13,011 | 207 | 1.59% | 15.1 |
| read 1: 2026-09-08 to 2026-10-05 (28d), bare `/` row | 2,871 | 52 | 1.81% | 13.2 |
| read 1, same window, `/` + GBP-tagged `/?utm_…` row combined | 4,999 | 120 | 2.40% | 9.7 |
| read 2: 28d ending ~2026-11-02 | | | | |

How to read the rows: the baseline window had no GBP-tagged homepage row (the profile link
gained `utm_campaign=profile` around the start of the test), so that traffic used to be counted
inside the bare `/` row. The **combined** row is therefore the like-for-like comparison, but its
position (9.7) is pulled up by branded GBP clicks. The **bare** row is the cleaner CTR read: up
1.59% → 1.81%, though its position also improved (15.1 → 13.2), so part of the gain is position,
not the snippet. Read 1 (2026-10-12 sweep) is a cautious positive; keep the new title through read 2.

Before: `Physical Therapy North Palm Beach | First Rehabilitation` /
`Family-owned physical therapy, occupational therapy, certified hand therapy, and wellness in
North Palm Beach, FL. Serving Palm Beach County since 1991.`
After: `Physical Therapy North Palm Beach | First Rehab, Since 1991` /
`Family-owned physical, occupational and certified hand therapy in North Palm Beach since 1991.
One-on-one care, 4.9★ on Google, Medicare accepted. Book today.`
If CTR has not moved after read 2, revert the title first (Google rewrites titles more than
descriptions) and keep the description.

## Competitor push: occupational + hand therapy in West Palm Beach, 2026-09-18

Acted on the 90-day Search Console pull to 2026-09-15, prompted by the owner flagging
FIRST Rehab of West Palm Beach (thefirstrehab.com) as the competitor to beat.

**Who they are.** Three Palm Beach County clinics (West Palm Beach at 1920 Palm Beach Lakes
Blvd, Lake Worth/Atlantis at 5055 S Congress, and Palm Beach Gardens), 155 Google reviews at
4.9, "over twenty years". Services are outpatient physical therapy, workers' compensation
(a provider for all major networks), sports and auto injury, pain management, MedX, and home
health care. Their public team page lists physical therapists and physical therapist
assistants.

**The asymmetry.** They offer no occupational therapy, no hand therapy, and have no Certified
Hand Therapist. A CHT is roughly three years of upper-extremity practice plus a national
exam, so that gap cannot be closed quickly even deliberately. Their name also collides with
ours, which is why our branded query set carries their cities.

**Where NOT to fight.** "physical therapy west palm beach" and its variants. They hold a
physical West Palm Beach address and 155 reviews; proximity and review count decide the map
pack and we have neither. Our West Palm Beach page drew 1,810 impressions at position 19.6
and converted 0.11% chasing exactly that.

**Where the demand actually is.** 751 impressions and ZERO clicks across 35 occupational
therapy queries, nearly all of them West Palm Beach:

| query | impr | pos |
|---|---|---|
| physical and occupational therapy west palm beach | 150 | 32.9 |
| physical therapy and occupational therapy west palm | 147 | 33.7 |
| occupational therapy at home west palm beach | 127 | 29.0 |
| occupational therapy treatment west palm beach | 108 | 33.5 |
| occupational therapist 33401 | 72 | 35.4 |
| occupational therapist west palm beach | 52 | 31.9 |
| hand pain treatment west palm beach | 224 | 18.2 |

**Changed.** `/services/occupational-therapy.html` got the SVC_DEEP treatment already applied
to hand therapy (834 -> 1,305 words). `/locations/west-palm-beach.html` was promoted to
`deep: True`, its title retargeted from "Physical Therapy for West Palm Beach" to
"Occupational & Hand Therapy West Palm Beach", `hand-wrist` added to its conditions, and two
city-specific sections added (794 -> 1,200 words). Palm Beach Gardens picked up a block for
orthopedic rehabilitation, manual therapy, physiotherapy-as-a-synonym and ergonomic
assessment (939 -> 1,107 words).

**Expect impressions on the West Palm Beach page to FALL.** The physical-therapy impressions
it loses were converting at 0.11%. Judge this change on clicks and on the occupational
therapy query positions, not on impression count.

**Palm Beach Gardens is the opposite case.** It borders North Palm Beach, so proximity is
winnable there and physical therapy IS the demand: 1,626 impressions against 5 clicks across
70 queries, led by "physical therapy palm beach gardens" (376 impr, pos 24.0). Newly targeted
long tail: "ergonomic evaluation in palm beach gardens" (22 impr, pos 62.9 — occupational
therapy work we already do and were invisible for), "physiotherapy in palm beach gardens"
(25 impr, 23.4), "orthopedic rehabilitation palm beach gardens fl" (51 impr, 36.0), "manual
therapy palm beach gardens" (23 impr, 21.4).

**Do not target: "physical therapy at home palm beach gardens"** and its variants, 238
impressions combined. That is home health care. We do not provide it and the competitor does.
Ranking for it would earn a call we have to turn away.

**Still open.** Occupational therapy has one blog post (`post-stroke-occupational-therapy-
north-palm-beach`). The West Palm Beach OT cluster above has no post behind it and is the
highest marginal return on the site.

---

## In-home therapy: confirmed NOT offered, and it is 227 impressions a month

Nick, 2026-09-21: "no in home ot or pt".

This matters because it is the largest block of demand the site draws that it can never convert.
On the clean 45 days after the Wix redirect consolidation, home-intent queries ran **340
impressions, 227 a month, and ZERO clicks** — 2.9% of all site impressions:

| impr | pos | query |
|---|---|---|
| 113 | 28.3 | occupational therapy at home west palm beach |
| 93 | 27.9 | physical therapy at home palm beach gardens |
| 88 | 39.5 | palm beach gardens physical therapy at home |
| 19 | 41.4 | physical therapy at home services palm beach |
| 16 | 26.1 | at home physical therapy services palm beach |
| 11 | — | six more, all "at home" or "in home" |

**Nothing on the site claims home visits, and nothing needs fixing.** Checked every page: every
"at home" on the site is a home exercise programme, an intake form filled in at home, or the
careers page describing at-home techniques taught to families. We appear for these queries
incidentally, on pages that happen to carry a city name and the word home, at position 28 to 40.

Two practical consequences:

1. **Write this demand off. Do not target it, and never add it to a page, a service item or the
   Google listing to capture it.** Claiming a service the clinic does not provide on a healthcare
   listing is the worst version of an SEO win.
2. **Subtract it before sizing any OT opportunity.** OT is 391 impressions a month, but 75 of
   those are the "at home" query alone, so the winnable OT pool is nearer 316. An OT plan that
   counts the full 391 is overstating itself by 19%.

If the clinic ever does start home visits, this becomes a real differentiator and the note should
be deleted rather than left stale.
