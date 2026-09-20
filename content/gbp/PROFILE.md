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

### Four things to fix, in priority order

**1. Four reviews have no reply.** All five stars, the oldest sitting unanswered since October
2025.

| date | reviewer | rating |
|---|---|---|
| 2026-04-06 | Crystal | 5 |
| 2026-02-11 | Blake Perez | 5 |
| 2025-10-07 | Romina Griffis | 5 |
| 2025-10-03 | scott ferris | 5 |

Owner responses are surfaced in the pack and a half answered profile reads as inattentive.
Templates are in `content/reviews/scripts.md`. `reply_to_review` can post these once approved.

**2. Three service items may not describe real services.** These are public claims about what a
healthcare business offers, and none of them appears anywhere in `SERVICES` in `build.py` or on
the site:

- **Massages**: "Therapeutic massage offered alongside our physical, occupational and hand
  therapy programs"
- **Concierge Therapy**: "Premium one on one therapy with added flexibility and availability"
- **Hydrotherapy training**: attached as a service type under the Physiotherapist category

If the clinic genuinely offers these, the gap is on the website, not the profile, and they
should be added to `SERVICES`. If it does not, they should come off the listing. Only the owner
can settle which. Do not guess either way.

**3. No accessibility attributes are set.** The only attributes on the listing are the six social
URLs. For an outpatient rehab clinic treating post surgical, post stroke and older patients,
accessibility is a filter people actually use, and Google shows these prominently. Candidates:

- Wheelchair accessible entrance, car park, lift, toilet
- Accepts new patients
- Appointment required
- Gender neutral toilet
- Identifies as veteran owned or similar, if applicable

Every one of these is a factual claim about the building. **Ask the owner before setting any of
them.** Claiming a wheelchair accessible toilet that is not one is worse than claiming nothing.

**4. Service items are all filed under `gcid:physiotherapy_center`.** Including the occupational
therapy and hand therapy ones. Mapping the OT service to the Occupational therapist category
would reinforce the exact association the site work is chasing, given the competitor has no OT
at all. Lower impact than the three above, and worth doing in the same pass.

---

## What only the owner can do

Nothing here needs a Google login except these:

- Deciding the factual questions in items 2 and 3 above
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
