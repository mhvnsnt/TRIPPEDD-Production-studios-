# animatic.py smoke-test proof — Wave 10 Lane A

**Wire-up:** `../animatic.py` builds an animatic MP4 from a timing CSV
(`panel,duration_s,caption`): each panel held for its duration at
1920x1080 with burnt-in caption + shot timecode, concatenated via ffmpeg.

**Proof (2026-10-07):**
- 3 synthetic test panels (ffmpeg `testsrc2`, clearly labeled "synthetic
  test panel" in the captions) + `shots.csv` (2.0s / 3.0s / 1.5s)
- Result: `ANIMATIC_OK` — expected 6.50s, actual 6.50s, 1920x1080 h264
- `animatic_frame.png` — frame at t=3s, **visually verified**: caption
  "SHOT 02 - synthetic test panel" burnt in at bottom, "SHOT 02 AT 2.0S"
  timecode at top-left

Test panels are synthetic by design (the tool takes real storyboard panels
as input); the proof demonstrates timing accuracy, caption burn-in, and
concat correctness.
