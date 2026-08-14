# Scheduling the week, and updating the site

## The release cycle

One episode owns one week. Never mix two episodes in one week.

| When (ET) | What | Where |
|---|---|---|
| **Saturday 9:00 AM** | Episode post | LinkedIn business, Facebook, Google Business |
| **Saturday** | Full episode video | YouTube — published by hand from the Descript app |
| **Sun–Fri 9:00 AM** | One clip per day, from that same episode | Instagram, Facebook, YouTube Shorts, TikTok |
| **Sun–Fri 9:00 AM** | Same takeaway, text only | Google Business, separate call |

The show airs 8:30 AM Saturday on 100.3 Legends Radio. Episodes are prerecorded, but
Saturday is the public moment.

One master routine fires all of this: `trig_01L8gTCsSXAtwCkvG4LMZuSh`, "Pain 2 Power —
daily social poster", cron `0 13 * * *` (9:00 AM ET daily), fresh session per fire. It
branches on the ET day of week — Saturday posts the episode, Sunday through Friday posts
the next unposted clip from `playlist.txt`. It was consolidated from two separate routines
on 2026-08-02 because the Routines tab was unreadable and each needed its connectors wired
separately. Do not split it back apart; add day-branches to this one instead.

This skill's job is to fill the branch that routine reads, not to replace it.

## Post Bridge

**`list_social_accounts` first, every single time.** Account IDs change on every reconnect.
YouTube was 81323, died with `invalid_grant`, came back as 81358; Google Business was
81363, came back as 81642. Last verified 2026-08-06:

| Account | ID |
|---|---|
| Instagram | 81353 |
| Facebook | 81324 |
| YouTube | 81358 |
| TikTok | 81356 |
| X | 81378 |
| Google Business | 81642 |
| LinkedIn business | 81322 |
| LinkedIn personal | 81320 — **never post** |

Rules that have each cost something:

- **Google Business takes text or one image, never video.** A clip day needs a separate
  text-only call with a LEARN_MORE CTA.
- **`create_post` returning "processing" is not proof of publication.** Always finish with
  `list_post_results` and report per platform.
- **Uploads are metered.** Reuse existing media IDs via `list_media` rather than
  re-uploading the same clip.
- **Transcode before posting.** Post Bridge accepts a `.mov` and reports
  `video/quicktime`, but HEVC-in-MOV is not something X will publish. H.264 High + yuv420p
  + AAC + faststart.

If the Post Bridge tools are simply missing, that is the per-chat connector toggle, not an
outage. `ListConnectors` reports `connected` *and* `enabledInChat`; a connector can be
authenticated to the account while switched off for the conversation, in which case its
tools do not exist and every call fails as "no such tool". This looked like an intermittent
outage across 2026-08-05/06 and cost hours. Connector changes only take effect in a new
conversation.

## Caption rules

**Zero dashes.** No em dashes, en dashes or hyphens — not in prose, bullets, compounds or
titles. Bullets use `•`. Only 561-624-4263 and 561-624-GAME keep their dashes. This is a
standing instruction from Nick (2026-08-02) and it applies to every caption on every
platform.

Lead with the joke or the hook. Details go after it, never before.

Captions are written at post time from `transcripts.md` on the episode branch. Attribute
anything clinical to the guest by name and credential exactly as stated. Never invent a
statistic, a credential or a quote, and never give individualized medical advice — route
unknowns to the front desk at 561-624-4263.

## Unattended running

`.claude/settings.json` is what lets the routine run without stopping to ask Nick to
approve each call. Each firing spawns a fresh session that clones this repo, so
`permissions.allow` must list every tool and domain the run touches. It **must** be
`.claude/settings.json`, committed — `settings.local.json` is gitignored and therefore
absent from the clone the fired session gets.

Adding a tool to the routine's prompt without adding it to that allow-list reintroduces the
approval prompt and the run stalls. `delete_post` and `delete_media` are deliberately in
`permissions.ask` so removing something still needs a human.

## Updating the site

Two edits in `build.py`, then rebuild. Neither is done by `tools/stage-episode.py`.

**`EPISODES[0]`** (~line 1516) — a 5-tuple, newest first:

```python
("Episode 10", "Dr. Zack McVicker", "&ldquo;…&rdquo; …", "https://open.spotify.com/episode/<id>", "Listen"),
```

`EPISODES[0]` automatically becomes the featured "Latest Episode" card, feeds the mini
player on every page, and joins the PodcastEpisode schema. A URL without
`open.spotify.com/episode/` renders a plain button instead of the embedded player, which is
the correct "coming Saturday" state.

**`VIDEOS[0]`** (~line 2684) — a dict, newest first:

```python
{ "id": "<youtube id>", "ep": "Episode 10", "title": "…", "guest": "Dr. Zack McVicker", "teaser": "…" },
```

Both values derive from public feeds; neither ever needs typing. Neither is reachable from
this sandbox (proxy 403), so fetch them via Supabase `pg_net` or a GitHub Actions runner:

- Newest Spotify episode id — GET `https://open.spotify.com/embed/show/033A1BQq9qqsygFFCq9SIu`,
  regex `spotify:episode:([A-Za-z0-9]{22})`. Returns exactly one id, the current episode.
  Title via `https://open.spotify.com/oembed?url=<url-encoded episode url>` → `.title`.
- Newest YouTube video — GET
  `https://www.youtube.com/feeds/videos.xml?channel_id=UCFzCl3RvdVahfIjKZ1SfRvQ`. Filter
  `link rel=alternate` on `/watch?v=` — a `/shorts/` path is a clip, not the episode.

Then `python3 build.py`, commit, push. Everything downstream is automatic: podcast page,
mini player, videos page, PodcastEpisode and VideoObject schema, sitemap.

Optionally also draft a blog post from the transcript with `/blog` in podcast-to-blog mode.
