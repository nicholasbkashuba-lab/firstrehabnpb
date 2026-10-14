---
name: pain2power-episode
description: Turn a new Pain 2 Power recording into a finished release. Input is a Dropbox folder /Pain2Power/<Guest>/ holding the 100.3 Legends radio mp3 and the camera files. Output is the multicam master in Dropbox, 8 to 10 captioned vertical clips plus a 20 to 30 second sizzle reel of the episode, all reviewed by Nick before they are scheduled, YouTube and Spotify titles and descriptions, the Saturday episode post, and the Spotify and YouTube links on the website. Use when Nick pastes a Pain2Power Dropbox link or says "do the same thing for this podcast", "new episode", "edit the podcast", "create the full edited podcast, clips, and posts", "make the clips", "schedule the clips", "sizzle reel of this week's episode", "youtube title and description", "spotify description", "where is the final", "find the spotify link", "find the youtube link", or "put the episode on the website". Also loaded by the Pain 2 Power episode watcher routine when a new folder appears. Not for a one-off social post (CLAUDE.md "Posting on demand") or for blog posts (/episode-blog, and new posts are frozen).
---

# Pain 2 Power episode

CLAUDE.md is the source of truth for every rule this skill points at; read it first. This
file is the order of work, the questions Nick must answer, and the mistakes that have
already cost him time. The newest worked example is `tools/relay-work/ep18-pilates/`
(README first). Reuse it; do not rebuild the pipeline.

## What "done" means

| Deliverable | Where it lands |
|---|---|
| Multicam master | Dropbox `/Pain2Power/<Guest>/Final/Pain to Power - <Guest> - multicam.mp4`, content_hash verified |
| YouTube copy | `content/youtube/ep{NN}-youtube.md`: 3 titles, one recommended; description; chapters on the EDITED timeline; tags |
| Spotify copy | `content/spotify/ep{NN}-spotify.md`: "Episode NN: <Guest>", plain description, no chapters |
| Clips | branch `media/ep{NN}-clips` (name is load bearing), scheduled in Post Bridge after Nick approves |
| Clip captions | `content/clips/ep{NN}-clip-captions.md` with the post id and date of every clip |
| Sizzle reel | `tools/sizzle/episodes/ep{NN}.json` + the rendered 9:16 reel, posted on air day (step 10) |
| Saturday post | LinkedIn business + Facebook, and a separate Google Business call, `content/announcements/ep{NN}-saturday-episode-post.md` |
| Friday announcement | only if Nick says yes this week (he skipped Episode 18's) |
| Website | EPISODES[0] once Spotify has it, VIDEOS once YouTube has it (the watcher routine does this) |
| Tools | `tools/relay-work/ep{NN}-<slug>/` scripts + README of what was different this time |

## Order of work

1. **Claim and check access.** `python3 tools/dropbox-put.py mkdir "/Pain2Power/<Guest>/Final"`
   before anything else. Final/ is the lock `tools/episode-watch.py` reads, so this stops
   the watcher from starting a second session on the same episode. Then
   `python3 tools/dropbox-put.py whoami`. If it fails, the environment Setup script lost the
   credential. Say exactly that; never ask Nick to recreate the Dropbox app.
2. **Is the upload finished?** `python3 tools/dropbox-put.py ls "/Pain2Power/<Guest>"`.
   Wait until nothing has changed for 45 minutes, then ffprobe every camera's duration
   against the mp3. Phones upload a camera hours after the mp3, and rendering from a
   partial file wastes a whole render.
3. **Episode number and links.** `python3 tools/episode-sync.py links` lists every episode
   with its Spotify and YouTube URL; this one is the newest number plus one. Spotify's
   numbering is the one that counts. Branch names have drifted from it before
   (`media/ep16-clips` holds Goodwin, who is Episode 17), so check before naming anything.
   **Never ask Nick for a Spotify or YouTube link.** Run
   `episode-sync.py links --episode NN`. If a link is missing, the episode is not out yet,
   and the watcher routine adds it to the site within three hours of it appearing.
4. **Ask everything at once, early** (one short message, he is on his phone):
   the guest's Instagram handle, whether he wants a Friday announcement this week, and
   the studio or group photo for the Saturday post if the folder has none. Asking at the
   moment each one blocks costs him three interruptions. Then work to the end without
   further approvals: "I don't want it to ask for any approvals, I just want it to finish
   fully." Give one ETA when the render starts; do not send progress pings ("stop
   checking in").
5. **Transcribe** the RAW mp3 (faster-whisper, word timestamps). Look for gaps Whisper
   skipped (Episode 18 lost 43 s at 3:11). Grep for "edit that"/"cut that": the hosts
   expect those outtakes removed.
6. **Multicam.** Sync each camera to the mp3, attribute speakers (pitch gate for a woman
   guest, ECAPA embeddings when the room is all men or two guests share a voice range),
   plan shots, render from the RAW cameras with the HLG tonemap. Read
   `references/traps.md` before rendering.
7. **Deliver the master** with `tools/dropbox-put.py put`, then send Nick the Dropbox path
   the moment it lands, unprompted. "Where is the final cut?" is the question he has asked
   most, across five episodes; Arlosoroff's sat undelivered for a week. He uploads to YouTube
   himself, so this is the handoff. Never hand him chunks to reassemble or a PowerShell paste.
8. **Clips.** Hook-first, 15 to 45 s, cut from the RAW cameras, captions in the house style
   (below). Stage with `tools/stage-episode.py` (add the guest to NAME_FIXES first,
   pass `--full-transcript`).
8b. **Sizzle reel** (Nick, 2026-10-14: "post a sizzle reel of the current week's episode each
   time"). Pick four to six lines from the transcript: the strongest one first, each complete
   on its own, guest and host both present, the guest's name on their first line. Write
   `tools/sizzle/episodes/ep{NN}.json` (the format is in `tools/sizzle/weekly.py`; Episode 18's
   is the worked example), check every in-point and every camera switch on a frame
   (`scdet=threshold=12` finds the switches), then
   `SIZZLE_EP=ep{NN} python3 run.py reel_week 9x16 16x9` from `tools/sizzle` with the master
   linked at `$SIZZLE_WORK/src/ep{NN}/master.mp4`. About 20 to 30 seconds. Look at a contact
   sheet before sending it anywhere.
   What Nick rejected on the first Episode 18 reel, so pick against it: a line that is only
   information (Lolita "lives in Juno Beach" had no punch), a line played over a wide shot
   with a mic in front of the speaker, and a line whose speaker is not the one on screen.
   What worked: a hook, a two-line title slam (`{"card": "TOPIC · ANGLE"}`) naming what the
   episode is about, one number or claim said on air, a story with its payoff line, and a
   laugh to close. Name cards go where the face is not (`name_at` when a camera frames a face
   at the top). No zoom and no push-in (`z` 1.0, the default): Nick said the zooming was too
   much, and a 9:16 crop of the 16:9 master is already close. The top text sits high.
9. **Show Nick every clip and the sizzle reel in the chat** with SendUserFile, each with its
   caption and proposed date, in one pass. Wait for his OK. Nothing is scheduled before that.
10. **Schedule** per CLAUDE.md "Episode release cycle": one clip a day at 9:00 AM ET,
    woven into the mixed queue with `tools/clip-queue.py`, never the same guest on
    consecutive days. Upload media first; MEDIA IS MANDATORY. Pass platform_configurations
    back IN FULL on every update_post. Finish with `clip-queue.py audit` showing 0 problems.
    The **sizzle reel** posts on air day (the Saturday) at 12:00 PM ET, outside the 9 AM clip
    queue: Instagram, Facebook, TikTok, YouTube Shorts and X, the 9:16 file, a hook-first caption
    that ends on where to listen, and the same collaborators as the clips. 12:00 PM ET is 16:00
    UTC under daylight time and 17:00 UTC after the clocks go back.
11. **Copy.** YouTube and Spotify files above, the Saturday post, and (only if he said yes)
    the Friday announcement. Every fact checked against the transcript with a timestamp.
12. **Branch, commit, push, draft PR.** Merge when Nick says "merge it"; he usually does
    right after reviewing, so expect it rather than asking.

## House style that Nick has had to correct more than once

- **Captions:** one line, at most 4 words per cue, MarginV=12 (the very bottom), solid
  black box, each cue starting on its first word's own timestamp. Two line cues showed the
  rest of the sentence before it was said; he caught it on Episode 18.
- **Zero dashes** in captions, titles and descriptions. Only 561-624-4263 and 561-624-GAME
  keep theirs. Bullets are •.
- **Guest names come from the guest's own site**, never ASR or the Dropbox folder name
  (ASR gave "Elise Maroney" for Elyse Marrone; the Spotify title is the check).
- **Instagram collaborators** (Nick, 2026-10-14): `legendsradio100.3` on every clip, the
  guest's own handle once he confirms it, and `mic_mcgann` on clips where Mike features.
  Instagram allows 3. Check the first published clip's `list_post_results`: a handle that
  fails takes the whole post down on every platform.
- **Never put a punch-in crop on screen unchecked**: look at a frame from every shot that
  uses it (Elyse's chin left the frame at 5:54).
- **Never invent** a credential, statistic or clinical claim. Attribute numbers to whoever
  said them on air. Clinical topics carry the "talk to your own doctor" line.
- **Updates are short.** One screen on a phone: what is done, what is waiting on him.
- **Spotify description:** write it from what the guest says on air about their own
  background. If the episode does not cover it, say so rather than researching it online.

## When something is missing

- No studio photo: the Saturday post waits; never make a graphic in its place.
- No IG handle: schedule without collaborators and say so; a guessed handle fails the post.
- Post Bridge tools missing: the connector is off for this chat (CLAUDE.md "Connectors").
  Finish everything else and say that scheduling is blocked on that toggle.
- Disk full mid-render: delete caches and finished intermediates; see `references/traps.md`.

`references/traps.md` has the render and disk traps from Episodes 13 to 18.
