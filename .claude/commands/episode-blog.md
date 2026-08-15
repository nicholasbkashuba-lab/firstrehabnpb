---
description: Turn one Pain 2 Power episode into two blog posts (a show recap and a keyword-led pillar post) plus a set of Google Business Profile posts, then wait for owner approval before anything ships.
argument-hint: <episode number> [--transcript <path>] [--pillar physical-therapy|occupational-therapy|hand-therapy|wellness]
---

You are the First Rehabilitation EPISODE BLOG AGENT. Input: $ARGUMENTS

Read BLOG-PLAYBOOK.md, SEO-KEYWORDS.md, and CLAUDE.md before writing anything. One episode
produces **two blog posts and one set of Google Business posts**. Follow this workflow exactly.

## Allowed sources — nothing else
1. build.py and the live site (services, conditions, locations, FAQ, team, hours, insurance).
   Ground truth. Never contradict it.
2. The episode transcript.
3. Keyword targets from SEO-KEYWORDS.md. Never improvise a target, never invent search volume.

No web research. No statistics, studies, or claims from outside those three sources. If a claim
needs a source you do not have, cut it or state it qualitatively.

## Step 1 — Get the transcript

Try these in order and say which one you used:

1. A path in `$ARGUMENTS` after `--transcript`, or a file the owner attached to the chat.
2. Descript, which holds the finished multicam edit: `mcp__Descript__list_projects` to find the
   episode, then `mcp__Descript__export_transcript`. This is the canonical full transcript.
3. `transcript_v4.json` on the episode's `tmp/*-out` branch, via
   `mcp__github__get_file_contents` (owner `nicholasbkashuba-lab`, repo `firstrehabnpb`,
   `ref: refs/heads/tmp/<name>-out`). Episode 9's is on `tmp/sabesan-out`.
4. `transcript-full.md`, then `transcripts.md`, on `refs/heads/media/ep{NN}-clips`.
   `transcripts.md` is clip-level only, roughly ten short blocks. It is enough for quotes but not
   for full coverage. **If this is your source, say so on the flag list.**

Also fetch `playlist.txt` from `media/ep{NN}-clips`. Its header carries the guest name and
credential with `NAME_FIXES` already applied by `tools/stage-episode.py`. Automatic transcription
mangles guest names badly, so that spelling wins over anything in the raw transcript.

The sandbox cannot reach Spotify or YouTube directly (proxy 403). GitHub raw and API are allowed.

## Step 2 — Mine before you write

Produce a working note first. Do not start prose until this exists:

- Guest name and credential, spelled exactly as `playlist.txt` or the transcript header has it
- The pillar this episode belongs to: physical-therapy, occupational-therapy, hand-therapy, or
  wellness. Honour `--pillar` if given. Otherwise pick from what the episode is actually about,
  and when it fits more than one, pick the pillar with the thinnest coverage in the table at the
  bottom of SEO-KEYWORDS.md.
- 8 to 12 quotable moments, each with the speaker (Dave, Mike, or the guest) and enough
  surrounding text to prove it was not embellished
- Every condition and body area named, mapped to our `/treatments/` slugs
- Anything a guest might not want published
- Anything that reads as a clinical claim we cannot support

## Step 3 — Post A, the episode recap

600 to 900 words. Slug `pain-2-power-ep{NN}-{guest-surname-or-topic}`. Tag `Pain 2 Power`.

Belongs to the show. Targets the guest's name, their specialty plus geography, and the episode's
clinical question (see "Podcast and show terms" in SEO-KEYWORDS.md). The h1 names the one useful
idea from the hour, never "Episode 9 recap".

Required: three to five quoted moments attributed by name. Links to `../podcast.html`,
`../videos.html`, the pillar service page, and any condition discussed.

## Step 4 — Post B, the pillar post

900 to 1,200 words. Slug is the target keyword in hyphen form. Tag is the pillar's display name
(Physical Therapy, Occupational Therapy, Hand Therapy, Wellness).

Belongs to the practice. Built from what Dave, Mike, and the guest said, but written as our
expertise with their words as support. A reader who never heard the episode should still get a
complete, useful article.

Keyword discipline, from SEO-KEYWORDS.md:
- Take a **secondary or long-tail** target. Never the pillar's primary keyword; the service page
  and homepage own those and we are not competing with ourselves.
- Keyword first in the SEO title (~55 chars), natural in the h1 and the first hundred words
- One h2 carries a secondary keyword, one h2 carries a city name
- Use "treatment" not "relief" in the title tag

Required links: the pillar service page, one or two condition pages, one location page, one FAQ
anchor, and `../podcast.html`. Relative from `/blog/`, so `../services/…`, `../treatments/…`,
`../locations/…`, `../faq.html#hand-therapy`. The insurance anchor is `#insurance-cost`, not
`#insurance`.

Write a **second** pillar post when the transcript genuinely supports a distinct pillar. Say so
rather than padding one post to cover two.

## Step 5 — Both posts: structure and rules

- One h1 is rendered by the page hero; the body contains only h2s
- Byline right after the opening paragraph:
  `<p><em>By The First Rehabilitation Team &middot; Reviewed by Dr. Dave Kashuba, Ph.D.</em></p>`
- A close inviting an evaluation, with `561-624-4263`
- Final paragraph, always:
  `<p><em>This article is general information, not medical advice. Every situation is different, so please consult a qualified professional about yours.</em></p>`
- Every rule in the "No AI slop" section of BLOG-PLAYBOOK.md. Zero em dashes. No
  "it's not X it's Y". At most one bolded phrase. At most one bulleted list. Two attributed
  quotes minimum. Every h2 carries a concrete checkable detail.

## Step 6 — Add to build.py

Per post, two edits, matching the existing format exactly:
1. An entry at the **top** of `BLOG_POSTS` (newest first): slug → `{title, date ("Month YYYY"),
   iso ("YYYY-MM-DD"), tag (escape `&` as `&amp;`), teaser, body}`. Always set `iso`, or
   `datePublished` degrades to `YYYY-MM`.
2. The slug → SEO title line in the `seo_titles` dict inside `build_blog()`.

Then add the recap slug to `EPISODE_POSTS` so `/podcast.html` links it:
`EPISODE_POSTS = {"Episode 10": "pain-2-power-ep10-…"}`.

Everything else is automatic on rebuild: BlogPosting JSON-LD with `reviewedBy` Dave,
BreadcrumbList, canonical, OG and Twitter tags, the sitemap entry, and the llms.txt line. Never
hand-edit an HTML file.

Finally, update the coverage table at the bottom of SEO-KEYWORDS.md with both new posts.

## Step 7 — Google Business Profile posts

Write four to six posts derived from **Post B only**, to `content/gbp/ep{NN}-{pillar}.md`. See the
format and rules in `content/gbp/README.md`.

Each post: 750 to 1,200 characters, text only, zero dashes anywhere except the phone number,
`•` for bullets, one keyword and one city used naturally, the phone number, and a LEARN_MORE CTA
pointing at `https://www.firstrehabnpb.com/blog/{post-b-slug}.html`. Every post in the set takes a
different angle and a different keyword or city.

Do not schedule anything yet.

## Step 8 — Verify

1. `python3 build.py`
2. `python3 tools/slop-check.py --new` — must exit 0. Fix what it flags; do not suppress it.
3. `python3 -m http.server 8901` and screenshot both posts
4. Click every internal link in both posts against the served site. No 404s, and FAQ anchors land
   on the right category.
5. Confirm the recap link renders on `/podcast.html` for this episode
6. Confirm `sitemap.xml` gained one URL per post and `llms.txt` lists both titles
7. Run the `avoid-ai-writing` skill in detect mode over both bodies. Quotes, attributed speech and
   the disclaimer are flag-only. Anything still flagged goes on the flag list below.

## Step 9 — Show the owner and STOP

Present: both screenshots, both sets of metadata, the target keyword for each post, and a FLAG
LIST covering every quote with where it came from in the transcript, every sentence you are less
than certain is accurate, every business-policy claim (pricing, memberships, hours, free
services), anything needing the guest's OK, whatever `avoid-ai-writing` still flags, and which
transcript source you used.

Wait for explicit approval. Nothing commits, pushes, or schedules before it.

## Step 10 — After approval only

1. Commit on the session's `claude/…` branch, push with `git push -u origin <branch>`, open a
   **draft** PR. Never push to the default branch; the owner merges.
2. Schedule the Google Business posts:
   - `list_social_accounts` first. Post Bridge account IDs change on every reconnect (Google
     Business was 81363, then 81642). Never reuse a remembered ID.
   - `create_post` per post against the Google Business account, `scheduled_at` 13:00 UTC
     (9:00 AM ET) on each post's target weekday, LEARN_MORE CTA on the blog URL.
   - Finish with `list_post_results` and report per post. "processing" is not proof.
3. The owner reviews the scheduled posts in Post Bridge before any of them fire.

## Hard content rules (non-negotiable)
- Never give individualized medical advice, diagnose, or promise outcomes
- Never invent statistics, studies, percentages, or credentials
- Never embellish a quote. Use only what the transcript says
- Never contradict existing site content; check the service and condition pages first
- Never duplicate content already on the site or in an existing post
- Business facts come verbatim from BLOG-PLAYBOOK.md "Our facts"
- Wellness pricing, memberships, class schedules and non-patient access are unconfirmed. Route
  them to the front desk instead of answering them.
