# Review capture system

Reviews are the highest leverage thing this clinic owns that no website change can substitute
for. The 2026-09-09 Search Console analysis recorded in CLAUDE.md is blunt about it: city
qualified searches are answered by the Google map pack, the map pack ranks on proximity,
category and review signal, and an organic result cannot win that click at any position we can
reach. Depth on a page moves position. Reviews move the pack.

**Where we stand.** Read off the live Google Business Profile on 2026-09-20 via the
`google_my_business` connector, location `locations/12092306722897872463`:

| | us | FIRST Rehab of West Palm Beach |
|---|---|---|
| Google reviews | **110** | 155 |
| Average rating | **4.9** | 4.9 |
| Locations | 1 | 3 |

An earlier note in this repo put our count at 24. That was the **Yelp** listing, and using it
made the gap look roughly five times worse than it is. The real gap is 45 reviews against a
competitor spreading its total across three clinics. On a per location basis we are already
ahead. This is a winnable race, not a rebuild.

**The actual problem is velocity, not total.** Only 8 reviews landed in the 12 months to
2026-09-20, about one every six weeks, and every one of them was five stars. A clinic
discharging patients weekly should comfortably beat that. Nothing is wrong with how patients
feel about the care. What is missing is anybody asking them.

Recency also counts in the pack. Forty reviews from 2021 read differently to Google, and to a
human, than eight from this quarter.

**What this folder is.** The capture system: who asks, when, in what words, and what happens to
the answer. `scripts.md` holds the exact wording. `tools/review-kit.py` regenerates the front
desk card and QR.

---

## The three rules that are not style preferences

These are policy and law. Getting them wrong costs more than the reviews are worth.

### 1. Never filter who gets asked

Asking only the patients you expect to say something nice is **review gating**, and Google
prohibits it outright. The usual version is a feedback form that routes 4 and 5 star answers to
Google and everyone else to a private inbox. It is easy to build, it is common in healthcare
marketing, and it puts the profile at risk of having its reviews stripped.

So: every discharged patient gets the same ask, in the same words, with the same link. A patient
who is unhappy gets the card too. If that produces a two star review, the answer is to fix the
thing and respond well, not to narrow the ask.

### 2. Never offer anything in exchange

No discount, no raffle entry, no free session, no gift card, not for staff either. Google
prohibits incentivised reviews and it applies to "leave us a review and be entered to win" just
as much as cash. A review the clinic paid for is also worthless as a signal to the person
reading it.

### 3. Never confirm in public that someone is a patient

This is the HIPAA trap and it is the one most likely to be tripped by a well meaning reply. A
public response that says "thanks for trusting us with your shoulder, Carol" confirms that Carol
received care here and discloses what for. That is a disclosure of protected health information
to the entire internet, made by the covered entity, without authorisation. It does not matter
that the patient posted first. Their disclosure is theirs to make. Ours is not.

Practical rule for every public reply:

- Never use a name the reviewer did not put in their own display name, and prefer no name at all.
- Never reference a condition, body part, procedure, therapist, appointment, or date, even if the
  review names them.
- Never confirm or deny that the reviewer was ever a patient. Not in a thank you, not in a
  rebuttal, not in a correction of something factually wrong.
- Move anything specific to the phone: "please call our front desk at 561-624-4263."

A negative review that misstates facts is still not an invitation to correct the record in
public. The template in `scripts.md` is deliberately bland for that reason.

---

## When the ask happens

One ask, at discharge, plus one reminder. More than that reads as pestering and does not convert.

| moment | who | how |
|---|---|---|
| Final visit, at the desk | Front desk | Hand the card, say the line from `scripts.md` |
| Same evening | Front desk | Text the link, only if the patient gave a mobile and agreed to texts |
| Five days later | Front desk | One reminder text, only if no review appeared. Then stop. |

Discharge is the right moment because the outcome is known and the patient is in the room. A
request sent weeks later to someone who has moved on converts close to zero.

**Consent for texting.** Only text patients who gave a mobile number and agreed to be contacted
by text. That agreement should already be captured at intake. If it is not, ask at the desk
before sending anything.

---

## Where the links live

- `https://www.firstrehabnpb.com/review` and `/reviews` both 302 to the Google write a review
  dialog for place ID `ChIJ3fEUAhCmsYkREHNzv87U3TQ`. The redirect lives in `vercel.json`, which
  is hand edited and not generated by `build.py`.
- Printed material and texts should use the **firstrehabnpb.com/review** form, never the raw
  Google URL. The short form is readable, it is ours, and if Google ever changes the dialog URL
  it is one line to fix rather than a reprint.

## Regenerating the card

```
pip install Pillow qrcode opencv-python-headless
python3 tools/review-kit.py
```

Writes `assets/review/review-qr.png`, `review-card-4x6.png` and `review-card-4x6.pdf`. The
script decodes its own output and refuses to finish if the QR does not read back as the review
URL, because the first version of it produced two files that looked correct as thumbnails and
could not be scanned at all. Send the PDF to the printer, 4x6, full bleed not required.

---

## Responding to reviews

Respond to everything, positive and negative, within a couple of days. A profile where the owner
answers reads as a business that is paying attention, and Google surfaces owner responses in the
pack. Templates are in `scripts.md`. Keep every one of them inside rule 3 above.

## Measuring it

The profile is readable from here. The Windsor.ai `google_my_business` connector is live and
carries this clinic as `locations/12092306722897872463`, so review count, average, individual
reviews and whether each one has a reply can all be pulled without logging in:

```
get_data(connector="google_my_business",
         accounts="locations/12092306722897872463",
         fields=["review_total_count", "review_average_rating_total"],
         date_preset="last_2years")
```

Swap in `review_id`, `review_create_time`, `review_star_rating`, `review_reviewer` and
`review_reply_comment` to list reviews and spot the ones still unanswered. CLAUDE.md does not
mention this connector anywhere; it was found on 2026-09-20 while building this folder.

Judge the work on the live numbers:

- Google review count and average, and the count of reviews added in the last 90 days
- Whether the clinic appears in the map pack for "physical therapy north palm beach" and
  "occupational therapy west palm beach" on a phone, checked from outside the clinic wifi
- `tools/gsc.py compare` for the organic side

**Do not add `aggregateRating` to our own schema to reflect any of this.** CLAUDE.md marks that
deliberate: self serving review markup violates Google's structured data guidelines and the
Google Business Profile already carries the review signal.
