---
name: pain2power-episode
description: Turn a new Pain 2 Power recording into a finished release. Input is a Dropbox folder /Pain2Power/<Guest>/ holding the 100.3 Legends radio mp3 and the camera files. Output is the multicam master in Dropbox, 8 to 10 captioned vertical clips that Nick reviews before they are scheduled, YouTube and Spotify titles and descriptions, the Saturday episode post, and the Spotify and YouTube links on the website. Use when Nick pastes a Pain2Power Dropbox link or says "do the same thing for this podcast", "new episode", "edit the podcast", "create the full edited podcast, clips, and posts", "make the clips", "schedule the clips", "youtube title and description", "spotify description", "where is the final", "find the spotify link", "find the youtube link", or "put the episode on the website". Also loaded by the Pain 2 Power episode watcher routine when a new folder appears. Not for a one-off social post (CLAUDE.md "Posting on demand") or for blog posts (/episode-blog, and new posts are frozen).
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
| **Sizzle reel** | EVERY episode (Nick, 2026-10-28: "do this every time we do pods"). `tools/sizzle/reel_ep{NN}.py`, about 25 s, 9:16: guest hook with name card, a title card, two or three more lines (Mike and Dave each with a name card), tune in end card. Cut from the RAW cameras like `reel_ep21.py`; `run.py` writes it and runs `qa_center.py`, which must PASS. Shown to Nick with the clips, then scheduled 12:00 PM ET on air day (the noon reel lane, outside the daily clip queue). Ep 18 is on `media/ep18-sizzle`, Ep 19's moments are `tools/sizzle/episodes/ep19.json` |
| Cover | the original logo with the guest as a matching cartoon (`content/announcements/README.md`), two variants, Nick picks; used Friday AND Saturday |
| Saturday post | LinkedIn business + Facebook, and a separate Google Business call, `content/announcements/ep{NN}-saturday-episode-post.md` |
| Friday announcement | only if Nick says yes this week (he skipped Episode 18's) |
| Website | EPISODES[0] once Spotify has it, VIDEOS once YouTube has it (the watcher routine does this) |
| Guest profile | `content/guests/<slug>.json` on /guests.html, via the `podcast-guest` skill (the watcher routine does this once the episode is in EPISODES) |
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
8b. **Sizzle reel.** Every episode, no asking: copy `tools/sizzle/reel_ep21.py` to
   `reel_ep{NN}.py`, pick the moments from the transcript, `run.py reel_ep{NN} 9x16`, PASS on
   `qa_center.py`. It goes to Nick in the same pass as the clips.
9. **Show Nick every clip in the chat** with SendUserFile, each with its caption and
   proposed date, in one pass. Wait for his OK. Nothing is scheduled before that.
10. **Schedule** per CLAUDE.md "Episode release cycle": one clip a day at 9:00 AM ET,
    woven into the mixed queue with `tools/clip-queue.py`, never the same guest on
    consecutive days. Upload media first; MEDIA IS MANDATORY. Pass platform_configurations
    back IN FULL on every update_post. Finish with `clip-queue.py audit` showing 0 problems.
11. **Copy.** YouTube and Spotify files above, the Saturday post, and (only if he said yes)
    the Friday announcement. Every fact checked against the transcript with a timestamp.
12. **Branch, commit, push, draft PR.** Merge when Nick says "merge it"; he usually does
    right after reviewing, so expect it rather than asking.

## House style that Nick has had to correct more than once

- **Captions:** one line, at most 4 words per cue, MarginV=75 (low, inside the Instagram 4:5 feed crop and above the Reels/TikTok UI; 12 got cut off, 2026-10-20), solid
  black box, each cue starting on its first word's own timestamp. Two line cues showed the
  rest of the sentence before it was said; he caught it on Episode 18.
- **Framing:** the subject is CENTRED in every shot of every video (Nick, 2026-10-14), and the
  camera does NOT chase their head (Nick, 2026-10-28: "i dont like how much the camera move
  with their head"). Vertical crops HOLD still and only reframe when the person really moves:
  the face averaged over 3 s drifts past 10% of the crop width (1 s glide), or a lean past 18%
  holds for a full second (`DZ, GLIDE, BIG, PERSIST` in `tools/relay-work/ep21-stone/clips21.py`;
  Episode 21 clips reframe about once each). Two tighter versions (following every frame, then
  a 0.5 s trigger) both passed QA and both read as chasing heads. A guest who keeps turning his
  head between the hosts will show 11 to 17% face box offsets for a second at a time in
  profile; with his body centred that is correct framing, not a reason to move the camera.
  The 16:9 master uses a FIXED crop per shot centred on that shot's median face, never motion.
  Check with `tools/sizzle/qa_center.py <clip> --min-run 1.0`: one frame head turns are ignored,
  any off centre stretch of a second or more fails. Ship only on PASS.
- **Caption speed and place, in one line:** clips use the house box style above (one line, at
  most four words, MarginV=75, each cue on its own first word, held until the next cue). The
  sizzle reel uses the engine's word pop captions, which sit at y=1420 of 1920, the same
  safe height.
- **Zero dashes** in captions, titles and descriptions. Only 561-624-4263 and 561-624-GAME
  keep theirs. Bullets are •.
- **Guest names come from the guest's own site**, never ASR or the Dropbox folder name
  (ASR gave "Elise Maroney" for Elyse Marrone; the Spotify title is the check).
- **Instagram collaborators** (Nick, 2026-10-14): `legendsradio100.3` on every clip, the
  guest's own handle once he confirms it (a verified `instagram_handle` in
  `content/guests/<slug>.json` is the one to put to him), and `mic_mcgann` on clips where Mike features.
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
