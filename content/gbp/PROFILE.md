# Google Business Profile: the listing itself

`README.md` in this folder covers **posts**. This file covers **the profile**, which is the part
that actually ranks in the map pack. Audited against the live listing on 2026-09-20.

## The listing is readable and writable from here

CLAUDE.md records Google Business only as a Post Bridge destination (account 81642, text or one
image, never video). That is not the whole picture. The Windsor.ai `google_my_business`
connector is connected to this account with full write access.

```
location   locations/12092306722897872463   First Rehabilitation of North Palm Beach
place id   ChIJ3fEUAhCmsYkREHNzv87U3TQ      (matches the /review redirect in vercel.json)
```

Read with `get_data`. Write actions available: `create_local_post`, `update_local_post`,
`reply_to_review`, `upload_media`, `update_location`, `update_service_items`,
`update_categories`, `update_service_area`, `update_attributes`, `update_address`,
`set_regular_hours`, `set_special_hours`, `set_open_status`.

**Treat every one of those writes as outward facing and get the owner's approval first.** A
category change moves the listing in the map pack immediately, and a wrong service item is a
public claim about what a healthcare business provides. Nothing in this file has been applied.

---

## What the audit found

**The profile is in good shape.** Somebody did real work on it. Verified present and correct:

| field | value |
|---|---|
| Primary category | Physical Therapy Clinic |
| Additional categories | Physiotherapist, Wellness Programme, Occupational therapist |
| Hours | Mon to Fri 8:00 to 17:30, Sat 8:00 to 12:30 |
| Phone | (561) 624-4263 |
| Website | firstrehabnpb.com with `utm_source=google&utm_medium=gbp` tagging |
| Description | 1991 founding, all four services, eight cities named, insurance, CTA |
| Voice of Merchant | true |
| Service items | 8, each with a real description |
| Social links | LinkedIn, Facebook, Instagram, YouTube, TikTok, X |

Reviews: **110 at 4.9**. See `content/reviews/README.md` for why that number matters and where
the 24 in older notes came from.

### Things to fix, in priority order

**1. SUPERSEDED — the backlog was 34, not 4.** The four listed here came from a 12-month query.
Widened to 24 months it was **34 unanswered reviews**, the oldest from 2024. Using the shorter
window made the problem look a tenth of its real size, which is the trap: `get_data` silently
answers only for the window you ask for.

The queue and the exact reply text for all 34 now live in `content/reviews/reply-queue.md`,
batched and tracked. Batches 1 and 2 are posted; 3 and 4 are scheduled. Work from that file,
not from this table.

**2. RESOLVED 2026-09-20.** Three service items were flagged here as possibly not describing
real services. Both parts of that turned out to need correcting.

**Hydrotherapy training was never on the listing.** This file originally said it was "attached
as a service type under the Physiotherapist category". It was not. It appeared inside the
CATEGORY DEFINITION that Google returns for Physiotherapist, which lists the service types
*available* under that category. The same block listed Breakfast, Lunch, Dinner and
Drive-through under `moreHoursTypes`, which should have been the giveaway. The clinic's actual
service items never included it. Nothing was removed because there was nothing to remove.

**Massages and Concierge Therapy are real.** Owner confirmed. They stay on the listing.

The gap was the website: neither appeared anywhere in `build.py` or on any page, so anyone
tapping either service on the Google listing landed on a site that never mentioned it. Both are
now items on `/services/physical-therapy.html`, worded from the clinic's own GBP descriptions.
They were deliberately NOT given their own service pages: CLAUDE.md's 2026-09-09 finding is that
new pages land on page two or three and add impressions nobody clicks.

**3. RESOLVED 2026-09-21.** The three accessibility attributes Nick confirmed are now set and
verified live: `has_wheelchair_accessible_entrance`, `has_wheelchair_accessible_parking` and
`has_wheelchair_accessible_restroom`. Note the id prefix: `wi_wheelchair_accessible_*` is
rejected with a 400, `has_wheelchair_accessible_*` is what Google accepts.

Not set, and still owner questions: appointment required, gender neutral toilet, veteran owned.
Each is a factual claim about the business, so none was guessed.

**4. RESOLVED — and the finding was already stale when written.** This file said every service
item sat under `gcid:physiotherapy_center`, including the occupational therapy and hand therapy
ones. Read live on 2026-09-21, both were already filed under `gcid:occupational_therapist`, and
"Occupational therapist" was already an additional category. Somebody fixed it before this file
was updated. **Read the live listing before acting on anything in this file.**

---

## OT expansion, 2026-09-21

The 45-day Search Console pull after the Wix redirect consolidation showed occupational therapy
at **391 impressions a month and zero clicks**, positions 28 to 40, almost entirely West Palm
city-qualified. CLAUDE.md records city-qualified intent as a profile lever rather than a page
lever, so the work went here rather than into more page copy.

Everything obvious was already done: the category, the West Palm service area, the service item
filing. The one real gap was **service item coverage** — OT had exactly two items (Occupational
Therapy, Hand Therapy) against four for wellness.

Six OT service items added, taking the list from 8 to 14. Every one restates a service the site
already claims in the `SVC_DEEP["occupational-therapy"]` blocks in build.py; none is a new
clinical claim:

| item | why |
|---|---|
| Stroke Rehabilitation | site claims it; distinct search intent |
| Activities of Daily Living Training | the core of what OT is |
| Ergonomic Assessment | 34 impressions at position 49 to 65, nothing on the profile matched |
| Return to Work Program | workers comp is an existing service |
| Cognitive Rehabilitation | site claims it |
| Adaptive Equipment Training | site claims it |

Verified by reading the listing back: 14 items live, nothing lost in the replace.

**ANSWERED 2026-09-21 — in-home therapy is NOT offered.** Nick: "no in home ot or pt". So
`occupational therapy at home west palm beach` (113 impressions in 45 days, the largest single
OT query) is permanently unwinnable, and so is the PT side of it. Across both, home-intent
queries are 227 impressions a month at zero clicks.

**Never add an in-home service item, and never let a description imply one.** The full record,
including why nothing on the website needs changing, is in `SEO-KEYWORDS.md` under "In-home
therapy: confirmed NOT offered".

Practical effect on sizing: OT is 391 impressions a month, of which 75 are the at-home query, so
the winnable OT pool is about 316. Subtract before planning against it.

## What only the owner can do

Nothing here needs a Google login except these:

- Deciding the remaining attribute questions in item 3 (appointment required, gender
  neutral toilet, veteran owned). Items 2 and 4 are resolved.
- Adding photos. The listing's media gallery was not audited in depth; a rehab clinic profile
  benefits from current interior, exterior, equipment and team photos, and the repo already
  holds `assets/media/clinic.jpg`, `gym.jpg` and the team portraits, which `upload_media` could
  push once approved.
- Seeding the Q&A section. Google lets a business post and answer its own questions, and the
  answers already exist in `FAQ_CATEGORIES` in `build.py`. Unanswered questions from the public
  are a visible gap on a profile.

## Rules that carry over

- Everything in `content/reviews/README.md` about HIPAA applies to `reply_to_review` exactly as
  it applies to a reply typed by hand. A public reply that confirms someone was a patient is a
  disclosure regardless of what posted it.
- Zero dashes in any profile copy, same as every caption. Only 561-624-4263 keeps its own.
- No medical advice, no promised outcomes, no invented statistics.
- Do not add `aggregateRating` to the site's own schema to mirror the review count. CLAUDE.md
  marks that deliberate and it remains correct.
