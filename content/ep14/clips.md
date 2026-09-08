# Episode 14 — Dr. Chaim Arlosoroff — clip plan

Guest: **Dr. Chaim Arlosoroff**, orthopedic trauma surgeon, St. Mary's (level-one
trauma centre, 30 years) and Orthopaedic Care Specialists — next door to the clinic.
Hosts: Dave Kashuba and Mike McGann. Topic: **e-bike injuries**.
Airs Saturday 12 September, 8:30 AM on Legends 100.3.

Timestamps are **RAW master time** (`P2P-Dr Arlosoroff 9-12 RAW.mp3`, 28:51.09).
Every clip below sits before 21:49, so these times are unchanged in the edited
master too. They come from paragraph-level transcript anchors and want tightening
against a word-level SRT before cutting — treat them as ±1s.

## Ordering note

Six weekday slots, and order decides the week. These are ranked strongest first
rather than chronologically.

Each one opens **on the surprising line, not the question that set it up**. Every
Episode 8 and 9 clip opened on an interviewer question or mid-sentence, and that was
flagged as the single biggest thing holding their reach back (2026-08-03, no decision
taken since). This plan applies the fix; if you would rather keep the old house style,
say so and I will re-cut the in-points.

| day | clip | in–out | len | opens on |
|---|---|---|---|---|
| Sun | 15 versus 50 | 14:24–14:42 | 18s | "Going 15 versus 50 is the difference between a scrape and a cracked skull." |
| Mon | The average age is 13 | 10:45–11:13 | 28s | "The average age of the injuries is 13." |
| Tue | The county numbers | 09:55–10:22 | 27s | "Miami-Dade — over 500% increase in injuries." |
| Wed | Nobody is moving | 13:55–14:25 | 30s | "Only 20% of kids in the United States get an hour of exercise a day." |
| Thu | Sight unseen | 07:23–07:55 | 32s | "I got a four-year full scholarship to Duke. He had never seen me play." |
| Fri | The honest caveat | 15:50–16:25 | 30s | "I'm an avid biker myself." |

## The clips

**Sun — 15 versus 50** (Mike). The tightest hook in the episode and completely
self-contained. "People don't grasp the full difference between a bicycle that
you're pedaling and one you've modified to go 50 miles an hour. Going 15 versus 50
is the difference between a scrape and a cracked skull."

**Mon — The average age is 13** (Dr. Arlosoroff). "About 83% of these injuries, no
helmet was worn. And the average age of the injuries is 13." Runs into the governor
point: 13-year-olds buying a bike, removing the limiter, and going 50 or 60.

**Tue — The county numbers** (Dr. Arlosoroff). His own research, local and specific:
Palm Beach County +130% ('23 to '24), Broward +180%, Miami-Dade including Nicklaus
Children's over +500%. Land on "and remember, these are serious injuries" — the ones
that reach a trauma centre, not the ones that don't.

**Wed — Nobody is moving** (Dave). Only 20% of US kids get an hour of exercise a day
and 21% are morbidly obese, against over 80% and under 5% in 1970–75. Ends on the
line that makes it an argument rather than a statistic: get the kids on self-propelled
bikes.

**Thu — Sight unseen** (Dr. Arlosoroff). World No. 283 in 1981, then a four-year full
Duke scholarship from a coach who had never watched him play. The one clip with no
injury content — it carries the week on personality, and Duke Tennis Hall of Fame is
a strong caption line.

**Fri — The honest caveat** (Dr. Arlosoroff). He rides e-bikes himself, in Park City,
Sedona, Italy — but pedal-assist, where you are still working hard. Stops the week
reading as blanket condemnation and makes the other five clips more credible.

## Held back for a decision

**The two patients** (12:50–13:20, Dave). A 14-year-old with a spinal cord injury who
will not walk again, and a 13-year-old whose organs were being harvested. It is the
most powerful thirty seconds in the episode and the hardest to place on a clinic's
feed. Your call — I have not scheduled it.

## Caption burn-in style — CHANGED, approved 2026-09-08

Nick picked a **solid black box behind white lettering**, not the outline style used
up to Episode 13. Compared side by side on a real frame from this episode, the
outline softens against the guest's white coat; the box never depends on what is
behind it. Apply the box to every clip in this set.

- White bold text, **solid opaque black box**, no outline, no shadow
- Centred, two lines maximum, sitting LOW in the frame (`y=h*0.72`), approved 2026-09-08.
  This is a deliberate move down: Episodes 8-13 sat mid-frame at ~46%. A box carries more
  visual weight than a shadow, and mid-frame it lands across the speaker's chest.
- Box hugs each line with even padding rather than running full width

Burning a `.srt` with libass — `BorderStyle=3` is what makes the box opaque, and
`Outline` becomes the box padding rather than a stroke:

```
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Inter,64,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,3,8,0,2,60,60,320,1
```

```bash
ffmpeg -i clip.mp4 -vf "subtitles=clip.srt:force_style='BorderStyle=3,Outline=8,Shadow=0,\
Fontsize=64,Bold=-1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Alignment=2,MarginV=320'" \
  -c:v libx264 -preset veryfast -crf 20 -c:a copy out.mp4
```

Or with `drawtext`, if the caption text is baked per segment rather than from a
subtitle file:

```
drawtext=fontfile=Inter-Bold.ttf:fontsize=64:fontcolor=white:box=1:boxcolor=black:\
boxborderw=28:x=(w-tw)/2:y=h*0.72
```

**Open: which font.** The previews that settled this used DejaVu Sans Bold, the only bold
face in the sandbox. The real font is recorded nowhere in the repo and cannot be read off
a rendered frame with confidence, so it has to come from whichever tool cut the Episode
8-13 clips. `Inter` appears in the style block above as a placeholder because the site
runs Inter; replace it before cutting.

## Caption rules for this set

- Zero dashes anywhere in prose. Bullets use `•`. Only 561-624-4263 and
  561-624-GAME keep their dashes.
- Lead with the hook, details after.
- Do not state a credential the transcript does not support. Confirmed on tape:
  orthopedic trauma at St. Mary's for 30 years, Orthopaedic Care Specialists,
  Duke Tennis Hall of Fame, world No. 283 in 1981, Israeli combat medic.
- Google Business takes text or one image, never video, and needs its own call.

## Source note

Cut from the RAW cameras, not from the finished master: `Arlosoroff.MP4` is the
guest angle (720p, shot upside down, needs a 180 rotation), `Mike.mov` and `Dave.mov`
are 4K. `Dave.mov` is HLG/BT.2020 HDR and must be tone-mapped or he will look washed
out against the other two at every cut.
