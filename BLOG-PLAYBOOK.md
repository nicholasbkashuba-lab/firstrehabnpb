# First Rehabilitation Blog Playbook

How every blog post gets written for firstrehabnpb.com. The `/blog` command
(.claude/commands/blog.md) automates this; these are the rules in plain English.

## What the writer may use — and only this
- Facts already in build.py and on the live site (services, conditions, hours, team,
  insurance, contact). This is ground truth.
- Whatever the owner supplies: a topic, or a Pain 2 Power episode transcript.
- **No web research.** No scraped statistics, studies, or claims. If a claim needs a
  source we don't have, cut it or say it qualitatively.

## Voice
Warm, plain-spoken, expert but never condescending. Short paragraphs. Second person
("you"). No hype, no exclamation marks. Write like a good clinician explaining
something across a table, not like a marketer.

## Anatomy of a post (700–1,100 words)
1. A hook naming the reader's real problem
2. One h1 title (the page hero), 3–5 h2 sections, scannable paragraphs
3. Byline: "By The First Rehabilitation Team · Reviewed by our clinical team"
   (a named person only when the owner says so)
4. At least two internal links (service, condition, FAQ, or podcast page)
5. A close inviting the reader to book an evaluation — phone 561-624-4263
6. Disclaimer, every post: general information, not medical advice; consult a
   qualified professional about your situation.

## Metadata
- SEO title ~55 characters, keyword first, "North Palm Beach" where it fits naturally
- Meta description ~155 characters (doubles as the card teaser)
- Category tag, teaser, lowercase-hyphen slug
- Article JSON-LD, canonical, OG/Twitter, and the sitemap entry are generated
  automatically by `python3 build.py` — never edit HTML files by hand

## Non-negotiables
- NEVER individualized medical advice, diagnoses, or promised outcomes
- NEVER invented statistics, studies, percentages, or credentials
- NEVER contradict existing site content; check service/condition pages first
- NEVER duplicate content already on the site
- Every uncertain sentence gets FLAGGED to the owner before publishing
- Every post is PREVIEWED at localhost and APPROVED by the owner before it is
  pushed — and it is pushed to a preview branch, never straight to the default branch

## Podcast-to-blog mode
When the input is a Pain 2 Power transcript: extract the 3–5 most useful patient
takeaways; attribute insights to the guest by name and credential; quote only what the
transcript actually says; link the episode page and relevant service/condition pages;
flag anything the guest might not want published (owner gets their OK first).

## Our facts (use verbatim; invent nothing)
- Family-owned since 1991 · "Our people make the difference."
- 733 US Highway 1, Suite 2A, North Palm Beach, FL 33408 · 561-624-4263
- Hours: Mon–Fri 8:00 AM–5:30 PM, Sat 8:00 AM–12:30 PM
- 4.9★ from 107 Google reviews
- Services: physical therapy, occupational therapy, certified hand therapy
  (Laura Drumm, CHT), on-site wellness/gym
- Insurance: Medicare + Medicare Advantage, BCBS, Aetna, Humana, Tricare,
  workers' comp, self-pay · SPRY patient portal
- Pain 2 Power podcast: Dave Kashuba & Mike McGann, Saturdays 8:30 AM,
  100.3 Legends Radio + Spotify
- Serves North Palm Beach, Palm Beach Gardens, Jupiter, Juno Beach, West Palm Beach
