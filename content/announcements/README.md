# Next guest announcement drafts

One file per episode: `content/announcements/ep{NN}-announcement.md`.

## Slot

**Friday 4:00 PM ET (20:00 UTC)**, the day before the show airs. Instagram, Facebook,
LinkedIn business, X. The podcast cover art is the image.

## The image: our logo with the guest drawn in (Nick, 2026-10-14, EVERY Friday)

**Which image goes where (Nick, 2026-10-30, every episode):** the cartoon cover below is the FRIDAY
announcement image. The SATURDAY episode-is-live post uses the photo of the guest standing outside the
studio, never the cartoon.

Every Friday announcement uses the ORIGINAL Pain 2 Power logo, `assets/media/podcast-cover.jpg`
(Mike left, Dave right, "WITH MIKE AND DAVE" banner), with that week's guest added as a matching
cartoon caricature standing in the MIDDLE between them. Nothing else on the logo changes.

- Source only `assets/media/podcast-cover.jpg`. `content/announcements/pain2power-cover.jpg` is
  NOT the logo: it is the variant made for Dr. Arlosoroff's episode, with him in the white coat, and using it
  is the mistake Nick caught on Episode 19.
- Reference for the guest: a clear, front-facing frame from the guest's own camera (or Zoom tile).
- How it was made for Episode 19: Higgsfield `gpt_image_2_5` (variant sunburst, quality high,
  2k, 1:1), two references (logo, guest frame), two variants for Nick to pick from. About 3 credits.
  The prompt that worked: keep the logo exactly, add "a cartoon caricature of the woman in the
  second reference photo, drawn in exactly the same bold black outlined, warm, hand drawn
  caricature style" centered between the two men, "nudge the two men slightly outward".
- Show Nick both variants before scheduling; the post uses the one he picks.

Not Google Business: Friday 9:00 AM already carries that day's pillar GBP post and Saturday
carries the episode post. A third post the same week spams the profile.

Not a replacement for Friday's clip, which still goes out at 9:00 AM. That is why the
announcement sits at 4:00 PM rather than sharing the morning slot.

## Rules

- **Nothing from inside the episode.** Not a quote, not a topic, not a takeaway. The show has
  not aired when this posts, Nick sells Saturday as the live moment, and a teaser assembled
  from the transcript gives away a show people are meant to tune in for. The hook is the
  airing itself.
- **Name and credential only**, exactly as the guest should be introduced. Never invent a
  title, specialty, affiliation or accolade. If the credential has not been supplied, the
  draft ships with the slot marked and the post does not schedule until it is filled.
- **Zero dashes.** No em dashes, en dashes, or hyphens in prose, compounds, or headings.
  Only 561-624-4263 and 561-624-GAME keep theirs. Same rule as every caption.
- **`•` for bullets.** Never `-` or `*`.
- **Lead with the hook or the joke.** Airing details go after it, never before.
- **Airing details in every post:** 8:30 AM Saturday on 100.3 Legends Radio, streaming after
  on Spotify and YouTube.
- **The phone number appears in every post.**
- LinkedIn personal (81320) is never posted to.
- No medical advice, no promised outcomes, no invented statistics.

## File format

```markdown
# Episode 14 · Guest Name

air_date: 2026-09-12
post_at: 2026-09-11 16:00 ET
platforms: instagram, facebook, linkedin-business, x
image: assets/media/podcast-cover.jpg

---
platform: instagram, facebook, linkedin-business

...caption...
---
platform: x

...shorter caption...
---
```
