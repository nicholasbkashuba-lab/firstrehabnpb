# First Rehabilitation Blog Playbook

How every blog post gets written for firstrehabnpb.com. The `/blog` command
(.claude/commands/blog.md) automates this; these are the rules in plain English.

## What the writer may use — and only this
- Facts already in build.py and on the live site (services, conditions, hours, team,
  insurance, contact). This is ground truth.
- Whatever the owner supplies: a topic, or a Pain 2 Power episode transcript.
- Keyword targets from SEO-KEYWORDS.md. That file is the only place a target comes
  from; do not improvise one and do not invent search volumes.
- **No web research.** No scraped statistics, studies, or claims. If a claim needs a
  source we don't have, cut it or say it qualitatively.

## Voice
Warm, plain-spoken, expert but never condescending. Short paragraphs. Second person
("you"). No hype, no exclamation marks. Write like a good clinician explaining
something across a table, not like a marketer.

## No AI slop
The tells below are what make a post read as machine-written, which is the last thing a
medical site can afford. These are hard rules, checkable by `python3 tools/slop-check.py`.

**Banned outright**
- Em dashes, en dashes, and ` -- ` in prose. Use a comma, a period, or parentheses.
  Only the phone numbers keep their hyphens. This matches the zero-dash rule already in
  force for social captions.
- "It's not X, it's Y" in every form, including the split-sentence version
  ("The problem isn't the tear. The problem is the healing.") and the stacked version
  that negates three things before the reveal.
- "isn't just", "more than just", "not only … but also".
- Rhetorical tricolons: "faster, safer, stronger".
- "In today's world", "In the world of", "When it comes to", "At the end of the day",
  "Here's the thing", "The truth is", "It's worth noting", "That said", "Simply put",
  "Let's be clear", "Whether you're a … or a …".
- delve, robust, leverage, seamless, crucial, vital, landscape, journey, navigate,
  unlock, empower, holistic approach, game changer, tailored, cutting edge,
  state of the art, testament to, treasure trove.
- Emoji anywhere. Exclamation marks. Bold sprinkled mid-paragraph: one bolded phrase per
  post at most, and zero is better.
- "In conclusion" and any closing paragraph that summarises what the reader just read.
- Hedge stacks: "may potentially help to some degree".

**Required**
- At least two direct quotes attributed by name, with the credential spelled exactly as
  the transcript spells it.
- Every h2 section carries one concrete, checkable detail: a person, a place, a piece of
  equipment, a real exercise, a number of visits. A section that could have been written
  without reading anything gets cut.
- Sentence length varies. At least one sentence under eight words per two hundred words.
- At most one bulleted list per post, and only for genuinely list-shaped content.
- Second person. Contractions are fine and help.

**Final pass.** Run the `avoid-ai-writing` skill in detect mode on the finished body.
Quotes, attributed speech, and the fixed disclaimer are flag-only and never rewritten.
Anything still flagged goes on the owner's flag list rather than being quietly smoothed.

## Anatomy of a post (700–1,100 words)
1. A hook naming the reader's real problem
2. One h1 title (the page hero), 3–5 h2 sections, scannable paragraphs
3. Byline: "By The First Rehabilitation Team · Reviewed by Dr. Dave Kashuba, Ph.D."
   (a named person only when the owner says so)
4. At least two internal links (service, condition, FAQ, or podcast page)
5. A close inviting the reader to book an evaluation — phone 561-624-4263
6. Disclaimer, every post: general information, not medical advice; consult a
   qualified professional about your situation.

## Metadata
- Pick the target keyword from SEO-KEYWORDS.md before writing, and check the coverage
  table at the bottom of that file so the new post fills a hole instead of competing
  with one of ours
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

## Podcast-to-blog mode: every episode makes two posts
Run with `/episode-blog <NN>`. One transcript, two posts, because they do different jobs
and chase different searches.

**Post A, the recap.** 600–900 words, tag "Pain 2 Power", slug
`pain-2-power-ep{NN}-{guest-or-topic}`. Belongs to the show. Targets the guest's name,
their specialty plus geography, and the episode's clinical question. Three to five quoted
moments attributed by name. Links `../podcast.html`, `../videos.html`, the pillar service
page, and any condition discussed. The h1 names the one useful idea, never "Episode 9 recap".

**Post B, the pillar post.** 900–1,200 words, tag is the pillar (Physical Therapy,
Occupational Therapy, Hand Therapy, or Wellness). Belongs to the practice. Built from what
Dave, Mike, and the guest said, but written as our expertise with their words as support,
not as a recap. Takes its keyword from SEO-KEYWORDS.md: primary keyword first in the SEO
title, natural in the h1 and the first hundred words, one h2 carrying a secondary keyword,
one h2 carrying a city. Links the pillar service page, one or two condition pages, one
location page, one FAQ anchor, and `../podcast.html`.

Write a second pillar post when the transcript genuinely supports a distinct pillar. Say
so rather than padding one post to cover two. Older episodes can be mined the same way
whenever a pillar needs coverage.

**Both posts.** Quote only what the transcript says, never embellish. Attribute by name and
credential exactly as written. Flag anything a guest might not want published; the owner
gets their OK first.

## Google Business Profile posts
Every pillar post produces four to six Google Business posts, drafted to
`content/gbp/ep{NN}-{pillar}.md` and scheduled only after the blog is approved.

750–1,200 characters, text only (Google Business takes text or one image, never video),
zero dashes, `•` for bullets, one keyword and one city used naturally per post, the phone
number, and a LEARN_MORE button pointing at the live post. Each post in a set takes a
different angle and a different keyword or city, so the profile feed does not read as one
message repeated six times.

These fill the weekday 9:00 AM ET Google Business slot. The daily clip routine no longer
posts its own text there.

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
