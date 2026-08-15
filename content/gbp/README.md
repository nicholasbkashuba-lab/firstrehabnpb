# Google Business Profile post drafts

Google Business Profile is the strongest local ranking surface we own, and it used to be spent on
clip takeaways with no keyword intent. It now carries keyword-led posts derived from each pillar
blog post.

One file per pillar post: `content/gbp/ep{NN}-{pillar}.md`. Written by `/episode-blog`, scheduled
only after the owner approves the blog.

## Slot

Weekdays and Sunday, 9:00 AM ET (13:00 UTC). These fill the Google Business slot that the daily
clip routine used to write itself. The routine still posts the Saturday episode announcement to
Google Business; it no longer posts weekday text there. Do not restore that call, or the profile
double-posts.

## Rules

- **750 to 1,200 characters.** Google Business allows 1,500. Long enough to carry a keyword and a
  real thought, short enough to read on a phone.
- **Text only.** Google Business takes text or one image, never video.
- **Zero dashes.** No em dashes, en dashes, or hyphens in prose, compounds, or headings. Only
  561-624-4263 and 561-624-GAME keep theirs. Same rule as every social caption.
- **`•` for bullets.** Never `-` or `*`.
- **One keyword and one city per post, used naturally.** Both come from SEO-KEYWORDS.md. Never
  the pillar's primary keyword, which the service page owns.
- **Every post in a set is a different angle.** Six restatements of one idea reads as spam to a
  human and adds nothing for Google. Different keyword, different city, different opening.
- **The phone number appears in every post.**
- **LEARN_MORE CTA** on `https://www.firstrehabnpb.com/blog/{post-slug}.html`. Until the post is
  merged and live, point at the pillar service page instead and note it in the file.
- No medical advice, no promised outcomes, no invented statistics. Same rules as the blog.
- Wellness pricing, memberships, class schedules, and non-patient gym access are unconfirmed.
  Route them to the front desk rather than answering them.

## File format

```markdown
# Episode 10 · Hand Therapy

source_post: carpal-tunnel-early-signs-palm-beach-gardens
pillar: hand-therapy
cta_url: https://www.firstrehabnpb.com/blog/carpal-tunnel-early-signs-palm-beach-gardens.html
cta_type: LEARN_MORE

---
slot: sunday
keyword: carpal tunnel therapy Palm Beach Gardens

Waking up with numb fingers is not something to wait out.

...post body...

Call 561-624-4263.
---
slot: monday
keyword: certified hand therapist near me Palm Beach County

...
---
```

## Scheduling

Run only after the blog post is approved.

1. `list_social_accounts` first. Post Bridge account IDs change on every reconnect. Google
   Business was 81363, then 81642. Never reuse a remembered ID.
2. `create_post` per post, `scheduled_at` at 13:00 UTC on the slot's date, LEARN_MORE CTA on
   `cta_url`.
3. `list_post_results` and report per post. A `create_post` that returns "processing" is not proof
   of publication.
4. The owner reviews everything in Post Bridge before it fires.
