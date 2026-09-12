# Episode 14 (Arlosoroff) - FINAL v2 render

Rebuilt 2026-09-12 from the raw cameras in Dropbox /Pain2Power/Arlosoroff/,
not from the previous render.

    cat ep14v2.chunk_* > ep14-arlosoroff-FINAL-v2.mp4
    sha256sum -c ep14v2.sha256

1,092,959,506 bytes
sha256 fcd419bb509cb4c81b18c10ed32a93e5ffbb1fdf2e0349778a794cafbd147e1e
27:38.91, 1920x1080, 30fps, bt709, 49,766 frames, -17.4 LUFS

## How it differs from tmp/ep14-video

Air cuts are ALREADY APPLIED, so this is the publishable length (27:38.91),
not the raw 28:51. Audio is the edited master.

QA (qa/verify_episode.py) - RESULT: PASS, all checks clean:
- lip sync 0.0 ms at all 10 points  (the earlier render drifted +36.7 ms
  after the second splice; that is fixed)
- privacy: 4/4 PII needles absent, both positive controls present (62.7, 101.8)
- camera follows speaker 90.3%, no five-minute block below 88.6%
- look consistency: luma spread 27.4 across angles (earlier render 30.4)
- 0 black frames, 0 frozen frames

## How it was cut

Mic-energy attribution gave the guest 12.5% of his own interview, so cuts were
driven from the diarised transcript instead via a new --cuts flag on
render_final_v3.py. 115 shots, avg 15.1s, longest 31.8s.

Splices measured, not taken from spotify.md (whose p2 range is wrong):
published 1309.10 and 1320.30; keep raw 0-1309.10 | 1339.95-1351.15 | 1392.47-1731.09.
