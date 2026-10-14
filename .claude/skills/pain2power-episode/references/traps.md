# Render and disk traps, Episodes 13 to 18

Each of these cost a session real time. The fuller write-ups live in CLAUDE.md
("Cutting the full multicam") and in each `tools/relay-work/ep*/README.md`.

## Sync and attribution
- **Mic energy alone puts the wrong person on screen.** Every mic in that studio hears
  everyone. Stock attribution gave the guest 12.5% (Ep 14) and 17% (Ep 15) of their own
  interview. Use `tools/podcast-attrib.py` (pitch) or ECAPA embeddings (Ep 16, Ep 18).
- **Two guests, four voices (Ep 18):** one camera's mic sat by a guest and heard her
  loudest 92% of the time. Shots used embeddings only there.
- **Validate attribution against named moments** in the transcript ("Dave, what size is
  that shirt") before trusting any percentage. Report the real number from a contact
  sheet; ~80 to 90% is normal, and claiming perfect is worse than saying 82%.
- **A RAW radio mp3 contains outtakes**: grep for "edit". Chapters then shift; Ep 18's
  chapters after 20:35 are 12 s earlier than the RAW file.

## Rendering
- iPhone footage is HLG/BT.2020 10-bit: tonemap through linear light (CLAUDE.md filter) or
  it ships grey. 60 fps cameras: `-skip_frame noref` to halve decode time.
- **The 30 min default background timeout kills a full render.** Launch with an explicit
  long timeout.
- Re-rendering only some shots: stream-copied pieces each report ~1/3 frame short and the
  concat demuxer stacks that into seconds of drift. Join with a list that states every
  file's exact `duration nf/30`. Never re-timestamp raw .h264.
- Punch-in crop from a 4K two-shot: 1.6x (2400x1350) with headroom, checked on a frame
  from every shot that uses it.

## Disk (~27 GB usable)
- Three 4K cameras ran to 41 GB on Ep 18. Range-fetch only the byte windows needed into a
  sparse file (`tools/relay-work/ep18-pilates/mike_slice.py`) and punch bytes back out with
  `fallocate -p` once used. Each Dropbox temp link is single use.
- Delete decoded audio, proxies and pip caches as soon as their step is verified.

## Clips
- Caption MarginV is in ASS script units (PlayResY 288), not pixels. A pixel value renders
  NO captions and still encodes cleanly; look at a frame.
- Post Bridge stores an uploaded copy. After any re-cut, re-upload and update_post every
  scheduled post that used the old file (compare `list_media` size_bytes).
- A wrong or private Instagram collaborator handle fails the whole post on every platform.
