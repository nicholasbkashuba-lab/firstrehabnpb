---
name: podcast-episode
description: Cut a Pain 2 Power episode end to end — pull the raw cameras and board audio from Dropbox into Descript, sync and edit the full episode, cut hook-first vertical clips, stage them to the branch the daily routine reads, and schedule the week in Post Bridge. Use whenever Nick sends new podcast footage or says "new episode", "cut the podcast", "edit the podcast", "make clips", "edit episode N", "here is the raw footage", or names a podcast guest with footage attached or in Dropbox. Not for one-off social posts — that is tools/stage-media.py. Not for writing a blog post from a transcript — that is /blog.
---

# Pain 2 Power — episode pipeline

One episode owns one week. Saturday 9:00 AM ET the episode posts and the full video goes
up on YouTube; Sunday through Friday one clip per day comes out of that same episode. Your
job is to take raw footage and land it in that shape, scheduled but not published.

Nick has standing authorization for this (2026-08-02). **Build everything, then schedule
it. Do not ask first, and do not publish immediately.** He reviews scheduled posts in Post
Bridge before they go live. Scheduling is the deliverable; waiting for approval is not.

Three steps stay human on purpose, and you should say so rather than fake them: reviewing
the ASR before captions are burned in, reordering `playlist.txt`, and publishing the full
episode to YouTube from the Descript app.

## Before anything else: can Descript reach the footage?

This is the step that has failed most often, so settle it first with the smallest file in
the set rather than discovering it 12 GB into a camera.

Descript pulls media from a URL. **A Dropbox link only works if it is "Anyone with the
link".** The Dropbox MCP cannot create one — `create_shared_link` is hard-locked to
`audience: no_one`, and its own description says to use the web UI for public links. Every
other route was tried on 2026-08-14 and every one failed:

| Attempt | Result |
|---|---|
| `create_shared_link` URL, `dl=0` | HTML preview page |
| same, `dl=1` | HTML preview page |
| `dl.dropboxusercontent.com` host swap | HTTP 403 |
| public *folder* link + filename subpath | HTML preview page |
| same on the raw-content host | HTTP 403 |
| `download_link` single-use temp URL | HTTP 403 — Descript's URL validation is itself an HTTP request, and it consumes the single use before the download starts |

And this sandbox cannot check any of it locally: every Dropbox host returns `CONNECT
tunnel failed, response 403` through the proxy, so Descript is the only probe you have.
Each guess costs a round trip. Do not iterate blindly — go straight to the fix.

**The fix, once, in the Dropbox web UI:** set the episode folder's sharing to *Anyone with
the link · Can view*. Files inside inherit it, `create_shared_link` then returns a link
that works, and the whole import becomes automatable. Ask Nick to do it for the folder he
drops footage into and it never needs doing again.

If Nick would rather not make a folder public, the fallback is that he imports the four
files in the Descript app by hand and gives you the project id. Everything downstream in
this skill still applies.

→ `references/descript.md` for the import payload shape, the multicam `tracks` form, and
the agent phrasings that worked.

## Phase 1 — import and sync

Create one project per episode, named `Pain 2 Power — {Guest} (multicam)`. Import the
three cameras plus the board audio, and build a `Sequences/Multicam - 3 Angles` sequence
from them. Mirror Episode 9's media key naming so later phases can address media by a
stable name.

Import and transcription of three 4K files is the long pole — hours, not minutes. Start it
before you do anything else, then write captions or the episode log while it runs.

**Sync everything to the board audio, not to a camera.** Ask the project agent to align by
waveform first; Descript does this natively and when it works the problem disappears. If
it will not, fall back to measuring the offsets yourself:

```
python3 "${SKILL_DIR}/scripts/sync_offsets.py" --episode 10
```

That relays a mono 16 kHz WAV of each camera out through a GitHub Actions runner (a few MB
each, nothing near the 100 MB blob limit) and FFT cross-correlates it against the board
audio. Measure at two points far apart to prove there is no drift; a real peak scores in
the hundreds. Episode 9's guest camera came out at `-83.15s` and held to within 0.1s across
22 minutes.

Write the measured offsets into `episodes/ep{NN}-{guest}.md`. They are the one number
nobody can rediscover without redoing the work.

## Phase 2 — the full episode

The board audio is the audio bed for the **entire** finished video. Episode 9 used camera
audio and Nick judged it bad, so this is not a preference.

- Mute every camera's audio track. Check this by ear through an angle switch, where a live
  camera track pops audibly.
- **Start the cut where the host starts the show.** The board feed begins when the radio
  show begins, so its own head is the true start; everything before it is room noise and
  setup.
- Remove filler words and dead air, switch angles on speaker changes, and produce a
  `FINAL 1080p` composition.
- `publish_project` at `unlisted`. That `share.descript.com` URL is both Nick's review copy
  and how the guest watches their own episode — it streams in any browser with no account
  and no download.

**Publish the full episode to YouTube from the Descript app, by hand.** Do not try to route
it any other way. Post Bridge times out fetching anything that large (a 2.9 GB export died
at 60s), GitHub release assets serve `application/octet-stream` and get rejected, and a
browser download of a 1.2 GB master truncates and YouTube then calls the file unreadable.

## Phase 3 — clips, hook first

Ten or so clips, of which only six air. Export the transcript with timecodes and pick the
moments.

**Open on the surprising sentence. Cut the setup entirely. Aim 15 to 25 seconds.** Every
Episode 8 and 9 clip opened on an interviewer question or mid-sentence on "But", and that
was identified as the single biggest thing holding their reach back; Nick settled it on
2026-08-14. If a candidate's first words are a question, it is not a hook — either move the
in-point or drop the clip.

Vertical 1080×1920, 30fps, captions burned in white bold with a dark outline, two lines
max, lower third. The guest camera shoots natively vertical, so it is used full frame at
zero crop — never crop the finished 16:9 master instead, which upscales a narrow slice of
an already-cropped face.

**A human reads the ASR before any caption is burned.** ASR mangles guest names badly and a
burned-in caption cannot be fixed later. Corrections live in one place,
`scripts/name_fixes.py` — add each new guest there rather than fixing by hand.

Then stage them:

```
python3 tools/stage-episode.py {NN} <clips-dir> --transcripts <text-dir> \
  --guest "Dr. Zack McVicker" --credential "..."
```

**The branch name is load bearing.** It must be `media/ep{NN}-clips`, because the daily
routine builds its fetch URLs from the episode number. Episode 9 first went to
`media/sabesan-clips` and would have posted nothing all week.

Reorder `playlist.txt` by hand afterwards. It is seeded numerically, six weekday slots means
only the top six air, and the strongest clip is rarely the first one rendered.

→ `references/clips.md` for the caption spec, the `.ass` style line, and the selection rules.

## Phase 4 — schedule the week, update the site

`list_social_accounts` first, every time — Post Bridge account IDs change on every
reconnect. Then schedule Saturday's episode post and the six daily clips.

Captions carry **zero dashes** outside the phone numbers. No em dashes, en dashes or
hyphens, in prose, bullets, compounds or titles. Bullets use `•`. Only 561-624-4263 and
561-624-GAME keep theirs.

Google Business takes text or one image, never video, so a clip day needs a separate
text-only call carrying the same takeaway. Never post to LinkedIn personal. Finish with
`list_post_results` and report per platform — `create_post` returning "processing" is not
proof of publication.

Once the episode is live, add it to the site: `EPISODES[0]` in `build.py` needs the Spotify
URL, `VIDEOS[0]` needs the YouTube id, and both derive automatically from public feeds.
Then `python3 build.py`, commit, push.

→ `references/scheduling.md` for the day-by-day platform map, the account IDs, the two feed
URLs and the exact `build.py` edits.

## Running the scripts

Set `SKILL_DIR` to the absolute path of the directory containing this SKILL.md — your
harness reported that path when it read this file. The scripts are always a direct sibling
of it, at `${SKILL_DIR}/scripts/`. Resolve it once and use it; do not assume the working
directory.

`sync_offsets.py` needs `numpy`, and audio work needs `ffmpeg`. Neither ships in this
sandbox; `pip3 install numpy` and `apt-get install -y ffmpeg` both work.

## Episode log

Each episode leaves a note in `episodes/` — project id, measured offsets, the clip list and
what actually shipped. Read the most recent one before starting a new episode; it is
usually faster than re-deriving what the last one settled.
