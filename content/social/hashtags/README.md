# Hashtags: researched every week, for every post

Nick, 2026-10-30: "for every post i need u to research popular hashtags for that week that will make the post
go viral or give it a higher chance to do so."

**Who does it:** the daily poster routine, every SATURDAY, for the seven days that follow (Sunday through
Saturday). It writes `YYYY-Www.md` here (ISO week of that Sunday's Monday), then re-tags every scheduled post
in the window with update_post. Any session that schedules a post sooner uses the current week's file.
Every other day the routine checks tomorrow's posts against the limits below.

## Hard limits (a post over these can fail or lose reach)

| Platform | Hashtags | Where |
|---|---|---|
| Instagram | **5 at most.** Instagram cut the cap from 30 to 5 on posts and Reels (announced by @creators, 2025-12-18). Count the shared caption AND any `platform_configurations.instagram.caption`. | last line of the caption |
| TikTok | 3 to 5 | end of `platform_configurations.tiktok.caption` |
| YouTube Shorts | the `youtube.tags` field (up to 8) plus whatever the shared caption carries | tags field |
| X | 0 to 2, only if they read naturally | `twitter.caption` |
| Facebook | uses the shared caption's line (same 5 as Instagram) | |
| LinkedIn | 3 | last line |
| Google Business | none; they do nothing there | |

## How to pick the five

1. **One or two TIMELY tags that genuinely fit the clip.** This week's health observance (November: National
   Diabetes Month, National Family Caregivers Month `#NFCMonth`, Movember), a season or holiday (`#Halloween`,
   `#FallBack` the week clocks change, `#Thanksgiving`), or a trend the clip actually belongs to.
2. **Two TOPIC tags** a person following that subject would search: `#BreastCancerSurvivor`, `#Neuropathy`,
   `#10000Steps`, `#HandTherapy`.
3. **`#Pain2Power`** on every podcast post (it is how the show is found and counted).
4. **One LOCAL tag**: `#NorthPalmBeach`, `#PalmBeach`, `#JupiterFL`, `#PalmBeachGardens`.
5. TikTok swaps one topic tag for a TikTok-native community tag: `#HealthTok`, `#FitTok`, `#WalkingTok`, `#PodcastClips`.

**Never:** an unrelated trending tag (a platform shows the post to that tag's audience, they scroll past, and
the post is ranked down); `#FYP` / `#ForYou` (they do nothing); election or political tags; a contest tag
unless we are entering; a tag that implies a medical claim the clip does not make. Rotate sets week to week:
the identical block on every post reads as spam.

## Where to research (in this order)

- TikTok Creative Center, hashtags, United States, last 7 days, industries Health and Sports & Outdoor:
  `https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?period=7&countryCode=US&industryId=27000000000`
  (the top 3 show without a login; most weeks they are entertainment and do not fit, which is a finding too).
- The week's health observances and their official tags, from the organization that runs each one
  (NIDDK / ADA for diabetes, Caregiver Action Network for #NFCMonth, movember.com), not third-party calendars.
- Seasonal and local dates (holidays, clock changes, Palm Beach County events the post mentions).
- Write down what each source showed, including "nothing relevant", so the next week starts from evidence.
