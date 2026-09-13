# Podcast episode QA

Objective checks on a finished episode render. No eyes required, and it caught
two real defects on Episode 14 that would have shipped.

## Run the whole battery

    python3 verify_episode.py RENDER.mp4 EDITED_MASTER.mp3 RAW_MASTER.mp3 turns.txt

`turns.txt` is one `H:MM:SS speaker_number` line per diarised speaker change, in
RAW master time. Export it from Descript with `include_speaker_labels=changes`
and `timecodes.on_speakers`.

Seven checks: format and duration, lip sync at 10 points, privacy (PII needles
plus positive controls), camera follows speaker (overall AND per five-minute
block), look consistency across angles, black/frozen frames, loudness.
Prints PASS / PASS WITH WARNINGS / FAIL.

**Validate the checker before trusting it.** Run it against a render whose
numbers you already know. Doing that on ep14 exposed a bug in the checker
itself: turns sorted by the whole tuple reordered same-second ties by speaker
id, inflating one speaker's share and dropping agreement from 91.2% to 77%.
Sort by time only, stable.

## Reference numbers (Episode 14, 2026-09-12)

| check | value |
|---|---|
| lip sync | 0.0 ms at all 10 points |
| PII needles | 11.7 to 16.0 (absent) |
| positive controls | 62.7 and 101.8 (present) |
| camera follows speaker | 90.3%, no block under 88.6% |
| luma spread across angles | 27.4 |

PSR >= 20 means the audio is present; < 12 is noise. ~82% speaker agreement is
the room-mic ceiling, so do not promise more.

## The other scripts

- `make_cuts.py turns.txt out.csv` - cut list from the transcript, with reaction
  cuts so no angle holds longer than 32s. **Use this instead of the renderer's
  mic-energy attribution**, which on ep14 gave the guest 12.5% of his own
  interview and a co-host 57.9%. Feed the CSV to `render_final_v3.py --cuts`.
- `hunt_pii.py RAW.mp3 RENDER.mp4` - searches a render for audio that must not
  be in it, with controls.
- `xcorr2.py RENDER MASTER` - lip sync across the timeline.
- `find_align.py RAW EDITED` - locates where an edited master maps into the raw,
  for recovering air-cut splice points when the edit map is wrong or missing.
- `clipcheck.py` - verifies each social clip lands at its documented master
  in-point.

## render_final_v3.py needs a --cuts flag

The skill's renderer has no `--cuts` option. Add after the `--dry-run` argument:

    ap.add_argument("--cuts", default=None)

and immediately before `share={}`:

    if a.cuts:
        import csv as _csv
        final=[]
        with open(a.cuts) as _f:
            for _r in _csv.DictReader(_f):
                final.append([float(_r["master_start"]), float(_r["master_end"]), _r["camera"]])
        final.sort(key=lambda x:x[0])
        _bad=sorted({n for _,_,n in final} - set(vids))
        if _bad: sys.exit(f"--cuts names cameras that are not here: {_bad}")
        final[0][0]=0.0
        for _i in range(len(final)-1): final[_i][1]=final[_i+1][0]
        final[-1][1]=mdur

## Two traps that cost time on ep14

- **A fresh render is RAW length** and contains whatever the air cuts remove.
  Reapply them, then re-run the privacy check.
- When cutting with `select`, pin the rate: `setpts=N/30/TB,fps=30` plus `-r 30
  -vsync cfr`. Without it ffmpeg defaults to 25fps and silently drops ~8,300
  frames while keeping the duration correct, so only a frame count catches it.
