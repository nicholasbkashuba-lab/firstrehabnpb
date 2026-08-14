# Descript — import, sync, edit, publish

Drive: **Nicholas Kashuba's Drive**, `07fb1237-87ac-4257-a2bf-523c674527e3`.
Episode 9 reference project: `6918397b-9b32-47f6-95dd-310aa655b867`.

## The media URL problem

Descript fetches media server-side from a URL, and validates the URL with its own HTTP
request before downloading. Two consequences that cost an afternoon on 2026-08-14:

- **The link must be genuinely public.** Anything requiring Dropbox auth returns 403 or an
  HTML preview page. See the table in SKILL.md for every variant that was tried.
- **Single-use links do not survive validation.** Dropbox's `download_link` gives a real
  direct URL, but the validation probe consumes the single use and the download then 403s.
  Do not reach for it.

The working arrangement is a Dropbox folder set to *Anyone with the link · Can view* in the
web UI. Per-file `create_shared_link` calls then return usable URLs, and `&dl=1` is not
needed — the raw host serves bytes once the object is public.

The other route that always works is direct upload: pass `content_type` and `file_size`
instead of `url` and `import_media` returns `upload_urls`, a map of media key →
`{upload_url, asset_id, artifact_id}`. PUT each file with
`Content-Type: application/octet-stream`, and the byte count must match the declared
`file_size` exactly. Useless from this sandbox, which cannot read the Dropbox bytes, but it
is the path if footage ever arrives as a local attachment.

## Import payload

One project per episode. Mirror Episode 9's key naming so later phases address media by a
stable name rather than a filename that changes every week.

```jsonc
{
  "project_name": "Pain 2 Power — McVicker (multicam)",
  "team_access": "edit",
  "add_media": {
    "mikecam":       { "url": "<public url>", "language": "en" },
    "mckvickercam":  { "url": "<public url>", "language": "en" },
    "davecam":       { "url": "<public url>", "language": "en" },
    "rawaudio":      { "url": "<public url>", "language": "en" },

    "Sequences/Multicam - 3 Angles": {
      "tracks": [
        { "media": "rawaudio",      "offset": 0 },
        { "media": "mikecam",       "offset": -12.34, "mute": true },
        { "media": "mckvickercam",  "offset": -11.90, "mute": true },
        { "media": "davecam",       "offset": -12.05, "mute": true }
      ]
    }
  }
}
```

`offset` is in seconds and `mute: true` is what enforces "board audio only" — it silences
the camera's own track while keeping its picture. Setting it here, at import, is more
reliable than asking the agent to mute tracks afterwards.

Keys containing `/` create folders in the project, which is why the sequence sorts under
`Sequences/`.

`import_media` returns immediately with a `job_id`. Poll `wait_for_job` (max 300s per
call, so expect several). Three 4K cameras take hours. Confirm with `get_project` that each
camera's `duration` looks right before building on top of it.

## What Episode 9's project looked like when finished

Worth matching, because it is the shape that worked:

```
media_files:
  cam-a-4-46-01                            video   1807.96s   (host two-shot, = show clock)
  cam-b-4-47-22                            video    886.02s
  cam-c-4-47-25                            video   1729.37s   (guest, vertical, zero crop)
  Sequences/Multicam - 3 Angles            sequence 1807.96s
  FINAL — Sabesan Episode (1080p).mp4      video   1694.13s
compositions:
  Pain 2 Power — Sabesan (multicam)        1807.96s
  FINAL 1080p                              1694.17s
  …then one composition per clip, each named as a headline
publishes:
  FINAL 1080p → https://share.descript.com/view/S3jYorNVwUZ   (unlisted)
```

Note the FINAL is ~114s shorter than the raw sequence — that is the head trim plus filler
removal.

## prompt_project_agent

Natural language, targeted at a `composition_id`. Returns a `job_id`; poll `wait_for_job`
and show the user `project_url`. Phrasings that did the work:

- *"Align the three camera tracks to the rawaudio track by matching their audio waveforms.
  Report the offset in seconds you applied to each."* — ask it to report, so the numbers
  land in the episode log even when Descript does the aligning.
- *"Mute the audio on every camera track. The rawaudio track is the only audio source for
  this composition."*
- *"Trim the start of the composition to the first word spoken on the rawaudio track. Remove
  everything before it."*
- *"Remove filler words and silences longer than 0.8 seconds across the whole composition."*
- *"Switch to whichever camera shows the person currently speaking, cutting on speaker
  changes."*
- *"Create a new vertical 1080x1920 composition named '<headline>' containing only
  {start}s to {end}s, with burned-in captions."*

Use `model: claude-opus` for clip selection and headline writing; `auto` is fine for the
mechanical passes.

## Publish

`publish_project` with `access_level: "unlisted"`, `resolution: "1080p"`. Republishing the
same composition reuses its share URL and overwrites the content, so a re-cut does not
invalidate a link already sent to a guest. Video and audio publishes of the same
composition get separate URLs.

`get_project` lists existing publishes with their `share_url` — read it before republishing
rather than triggering a render to find a link you already have.

## The full episode goes to YouTube by hand

Descript has YouTube connected in the app. Publish the FINAL composition from there, then
set scheduling in YouTube Studio. Every automated route has been tried and fails: Post
Bridge times out on the fetch, GitHub release assets serve the wrong content type and are
rejected, and browser downloads of a multi-GB master truncate into a file YouTube calls
unreadable.
