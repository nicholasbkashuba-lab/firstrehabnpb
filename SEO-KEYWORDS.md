# Local SEO Keyword Map

The single source of keyword targets for firstrehabnpb.com. Every blog post, every Google
Business post, and every new page picks its target from this file. Nothing here was researched
on the web. Targets are derived from what the site already sells (`SERVICES`, `CONDITIONS`,
`LOCATIONS` in build.py), the 25 topic targets in BLOG-TOPICS.md, and the Search Console
observations recorded in CLAUDE.md.

No search-volume numbers appear here on purpose. We do not have a keyword tool wired in, and an
invented volume is worse than no number.

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

**Do not claim**: driving evaluations, home modification contracting, or pediatric OT. The
service page does not offer them.

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

Fill a hole rather than cannibalising. Update this table whenever a post ships.

| Post slug | Pillar | Keyword it owns |
|---|---|---|
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

**Ep 11 note (2026-08-22):** the Paul Joyce recap is a Pain 2 Power post, not a Wellness pillar post,
so the Wellness hole below is still open. The transcript does hold a real Wellness pillar angle that
nothing on the site covers yet: keeping muscle and strength while losing weight on a GLP-1, built on
Dave's "it's going to make you better, but it's not gonna make you healthier" and Paul's "you lose a
lot of muscle". Awaiting owner sign-off on the angle before it is written.

**Holes as of 2026-08-15, end of day:** Occupational Therapy now has one post. **Wellness still has
zero**, and it is the only pillar with none, so it is the next thing to write. Two Wellness posts
are already sourced from the Episode 8 transcript and waiting: "the invention of the chair is one
of our demise", and the TheraBand home program behind Dave's "I do everything I can to let people
not ever come to see me". Hand Therapy has one. Physical Therapy has seven and needs nothing.
Locations referenced from a post: Palm Beach Gardens, Jupiter, West Palm Beach.

`/exercises.html` is not a blog post but it targets long-tail exercise searches across all four
pillars, so check it before writing an exercise-led post that would compete with it.
