> **STATUS (2026-10-14): merged into BLOG-PLAYBOOK.md** ("Length standard" section: 1,700 to 2,000+ word pillar guides, depth first). The 12-post calendar below is still a valid topic backlog, but check SEO-KEYWORDS.md coverage first and respect the new-post freeze in CLAUDE.md unless Nick lifts it.

# Blog Template and 12-Post Calendar

## A. Post template

Copy this skeleton for every post. Word budgets add up to roughly 1,800 words for a pillar guide. Length is not a ranking factor: cut sections when the question is simple, and never pad.

```
---
title: (H1; matches the title tag, under about 60 characters if possible)
slug:
primary_question: (the exact question a patient would type)
search_intent: informational | local | insurance | comparison
audience: (for example: adult child of a 70-year-old, post-surgery patient, snowbird)
author: (named clinician)
reviewer: (named clinician who is not the author when possible)
review_date:
sources: (3 or more primary sources: CMS/Medicare.gov, APTA, NIH/PubMed, state law pages)
first_hand_element: (a clinician explanation or "how we handle this at First Rehab"; must be real)
internal_links: (3 to 5: one service page, one sibling post, glossary term, bio, contact)
cta: (call, request appointment, event signup)
---
```

**Structure**

1. **Answer first (about 50 words).** Direct answer under the H1, with no warm-up.
2. **Table of contents** (auto-generated).
3. **H2: What is [topic], in plain English?** (about 150 words) Link a glossary term.
4. **H2: Who gets this, and why?** (about 200 words) Causes, risk factors, age ranges.
5. **H2 with a comparison table.** (about 150 words plus table) Examples: "Surgery vs. therapy first," "PT vs. OT," "Week-by-week recovery." Columns should answer real questions, not repeat the text.
6. **H2: What treatment actually looks like** (about 250 words) Typical visit flow and what the therapist does. Use H3s per phase.
7. **Callout box: When to see a doctor right away.** Red flags (clear, short, no diagnosis).
8. **H2: How long does it take?** (about 150 words) Ranges, with "depends on" factors. No guarantees.
9. **H2: Cost and coverage** (about 150 words) Medicare, Medicare Advantage, commercial plans, self-pay. Link the glossary entries (copay, deductible, prior authorization).
10. **H2: How we do it at First Rehab** (about 150 words) The first-hand section: named clinician, our process, what patients tell us they want. Never a patient story without written authorization.
11. **H2: FAQ (5 questions, 40 to 70 words each).** Visible Q&As. Markup optional.
12. **Sources** (visible list) and **reviewer line** ("Medically reviewed by [Name, credentials] on [date]").
13. **CTA** with phone and appointment request.

**Heading rules.** One H1. H2s as questions or plain statements a patient would say. H3s only for real sub-points. Vary structure between posts (steps, myths vs. facts, timeline, comparison) so posts don't read as clones.

**Voice.** Conversational and warm, as if a therapist were explaining it across the table. Contractions are fine. Everyday phrases like "get back to your garden" are fine. No slang, no jokes about pain, no fear tactics. Aim for roughly an 8th-grade reading level. Short paragraphs. Define jargon once, with a glossary link.

**Hard bans.** No guarantees ("you'll be pain-free"), no "best," no unsourced statistics, no diagnosis, no individual medical advice, no patient information, no invented quotes. No AI tells: "it's not X, it's Y" reveals, "no X, no Y, no Z" lists, filler openers, rule-of-three padding.

**Pre-publish checklist**
- [ ] Every fact has a source, and the source says what we say it says
- [ ] A clinician fact-checked the title, meta description, headings, schema, and image alt text
- [ ] Reviewer name and date match the visible line and the schema
- [ ] At least one first-hand element is real
- [ ] 3 to 5 internal links, no orphan page
- [ ] Reading level checked
- [ ] FAQ markup (if used) matches visible Q&As word for word
- [ ] No "TODO" or placeholder text

## B. 12-post calendar (one per week)

Confirm demand in Search Console and a keyword tool before committing. Reviewer suggestions follow clinical specialty; the clinician decides.

| # | Working title | Intent | Author / reviewer (suggested) | Links to |
|---|---|---|---|---|
| 1 | Does Medicare Cover Physical Therapy in Florida? What a CORF Means for You | Insurance | Dr. Kashuba / a DPT | Medicare service page, glossary (CORF, KX modifier, plan of care) |
| 2 | Fall Prevention After 65: A Therapist's Balance Checklist | Informational | A DPT / second DPT | Balance service page, glossary (fall-risk screening) |
| 3 | Carpal Tunnel or Trigger Finger? What Hand Therapy Can Do | Informational | Laura Drumm / Joni Janik | Hand therapy page, Laura's bio |
| 4 | Knee Replacement Recovery: A Week-by-Week Timeline | Informational | A DPT / second DPT | Post-surgical page |
| 5 | Rotator Cuff Surgery Rehab: What to Expect | Informational | A DPT / second DPT | Post-surgical page |
| 6 | Hurt in a Car Accident in Florida? How PIP and Physical Therapy Work | Insurance/local | Dr. Kashuba / clinician | Auto/PI page, glossary (PIP, LOP) |
| 7 | Do You Need a Doctor's Referral for Physical Therapy in Florida? | Informational | A DPT (verify current Florida rules) | Services hub, glossary (direct access) |
| 8 | Physical Therapy vs. Occupational Therapy: Which Do You Need? | Comparison | Joni Janik / a DPT | PT and OT pages |
| 9 | Winter in Palm Beach? A Snowbird's Guide to Physical Therapy | Local | Dr. Kashuba / clinician | Seasonal-resident page |
| 10 | What Happens If You Stop Physical Therapy Early? | Informational | A DPT / second DPT | Services hub, wellness page |
| 11 | Pickleball, Golf, and Tennis Injuries: Prevention Tips from Palm Beach Therapists | Local | A DPT / second DPT | Sports/ortho page, wellness page |
| 12 | Hip Replacement Recovery: What to Do and What to Avoid | Informational | A DPT / second DPT | Post-surgical page |

**Cadence.** Publish after the foundation pages (bios, glossary, service pages) are live. Stagger releases, log each date, and check the Search Status Dashboard first (Section 5b of `HANDOFF.md`).

**Cluster rule.** Each post links up to one service page and sideways to at least one sibling post. Service pages link back to their posts, so every post is reachable in two clicks from the blog hub.
