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
transcript estimate) and nudged onto the nearest real silence — confirmed
below -28dB at both edges on every clip.

2026-08-23: Nick flagged that the first pass (all 15-31s soundbites) was
cutting the meat of the conversation, specifically clip 02 losing the "gasket"
metaphor's payoff. Re-cut all 7 to the full setup-through-payoff exchange
instead of an isolated line — clips now run 47-80s. This trades off against
the 15-25s reach guidance from 2026-08-03; the tradeoff is deliberate per his
explicit request, but if reach suffers report back before cutting a third
pass shorter again.

Branch name matters: the daily routine builds its URLs from the episode number,
so it must be media/ep10-clips and nothing else.

At 47-80s these clips run 20-58MB, over jsDelivr's ~20MB ceiling — only
07-water-cooler.mp4 (19.7MB) still resolves there (verified 200). The other
six 403 on jsDelivr and must be fetched from the Vercel branch host
(firstrehabnpb-zywd-git-media-ep10-clips-thedesignofman.vercel.app/clips/
{name}.mp4) instead — verified 206 on a range request for all six.

2026-08-24: Nick reported captions off on every posted/scheduled reel. Root
cause: the "paced evenly across the transcript" approach from the note above
does not hold once a clip includes host banter and asides that never made it
into the condensed transcripts.md text (interjections like "Right, right,"
follow-up questions, "you know" filler). The raw clip audio runs longer and
less uniformly than the condensed caption text implies, so pacing captions
evenly across clip duration drifted them off the actual words by several
seconds in spots — confirmed via faster-whisper word-level transcription of
each clip's own audio track against the burned caption timing.

Fix: re-transcribed each clip's audio with faster-whisper (word timestamps),
regenerated captions chunked ~3-6 words per card broken on
sentence/clause boundaries, and re-burned. Old burned-in captions could not
be removed (no separate uncaptioned source survived — clips are pushed
already-cropped-and-captioned), so a solid black bar was added behind the
caption band (y 1400-1770, full width) to fully hide the old incorrect text;
new captions are drawn on top of the bar. This is a permanent style change
going forward, not just a one-time patch — it also reads cleaner against
busy backgrounds. All 7 clips (01-07) were re-rendered and pushed to this
branch 2026-08-24.

Caption text is now VERBATIM to what's actually said in each clip (including
host banter), not the condensed paraphrase in transcripts.md — that file is
now stale for caption purposes (still fine for the "what each clip says"
summary use). If future clips need condensed/paraphrased captions instead of
verbatim ASR, redo the fuzzy-match-then-time approach instead of burning the
condensed text on an even pace — that's what caused this bug.
