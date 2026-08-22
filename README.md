Episode 10 social clips — Dr. Zach McVicker. Vertical 9:16, captioned, full quality.

playlist.txt sets the posting order. transcripts.md carries what each clip
actually says. transcript-full.md is the whole episode with [mm:ss] stamps;
/episode-blog reads that one.

Clips were cut directly from `podcast-final-v3.mp4`, the file actually published
to YouTube (2560x1440, 28:45) — not the earlier 1920x1080/29:38 Descript export,
which runs about 53s longer from untrimmed dead air scattered through the
episode. Cut points were located by FFT cross-correlating short audio probes
from the reviewed transcript against v3's own audio track (SNR 13-35 on every
clip, well above noise floor), then verified against extracted preview frames.
Cropped to 9:16 (centered, full height kept, no face crop), captions burned in
(white bold, dark outline, centered, lower third), paced evenly across each
clip's spoken text rather than word-level ASR-synced — if a caption drifts
against the speaker by more than a beat on review, nudge it before it posts.

Every in/out point was verified against the actual waveform (not just the
transcript estimate) and nudged onto the nearest real silence — 5 of the 7
clips had cuts landing 0.1-0.2s into a word or a beat early on the exit; all
7 now open and close on genuine pauses (confirmed below -28dB at both edges).
01, 03 and 06 run 27-31s, longer than the 15-25s window that's performed best
for reach on this show (flagged 2026-08-03, still true) — tighten further if
reach on those three underperforms.

Branch name matters: the daily routine builds its URLs from the episode number,
so it must be media/ep10-clips and nothing else.
