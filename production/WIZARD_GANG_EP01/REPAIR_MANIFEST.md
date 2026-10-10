# EP02 Visual Repair Manifest (CORRECTED)

**Goal:** Convert photorealistic drifted shots to 2D cartoon (Shadow Wizard Money Gang base).
**Master:** wizard-gang-ep02-full-5min.mp4 — DO NOT replace until owner approves repaired shots.
**QC:** Every repaired shot checked against AI_SLOP_FIELD_GUIDE.md before marking done.

**Correction 2026-10-10:** Full clip contact sheet review shows only 3 shots are truly
photorealistic. The earlier "19 shots" audit overstated the drift — most clips hold
2D cartoon style well. Focusing repair effort on the 3 real offenders.

## Triage

| # | Clip | Description | Issue | Type | Method | Status |
|---|------|-------------|-------|------|--------|--------|
| 1 | clip-05 | street crew lineup | PHOTOREALISTIC - worst | C | EbSynth test → Kaggle if needed | EbSynth running |
| 2 | clip-15 | basketball (Hollow) | PHOTOREALISTIC - worst | C | Kaggle/Wan | pending |
| 3 | clip-22 | podcast studio (Static) | PHOTOREALISTIC - worst | C | Kaggle/Wan | pending |

**Borderline (painterly/2D, acceptable per approved styles):**
- clip-01: council chamber (painterly — APPROVED for dramatic beats)
- clip-07: static at table (2D with realistic shading — borderline, monitor)
- clip-13: dice game (2D — acceptable)
- clip-21: skate park (2D — acceptable)
- clip-24: fireworks rooftop (2D — acceptable)
- clip-25: pier kiko (2D cinematic — acceptable)

**Clean 2D (no repair needed):**
clip-02, 03, 04, 06, 08, 09, 10, 11, 12, 14, 16, 17, 18, 19, 20, 23, 26, 27, 28

## Repair Log

### clip-05 (street crew)
- 2026-10-10: Extracted 100 frames @ 10fps 640x360. Created 3 cartoon keyframes.
- 2026-10-10: EbSynth running with multi-keyframe anchoring (0, 49, 99). ETA ~65 min.

## Kaggle Staging

Prepared inputs for owner to run on Kaggle notebook:
- ~/workspace/video-fix-tools/kaggle-staging/
- clip-15 (basketball): driving video ready, needs 2D character reference
- clip-22 (podcast): driving video ready, needs 2D character reference

## Notes

- EbSynth: CPU ~40s/frame @ 640x360.
- If EbSynth output on clip-05 is good, apply to clip-15 and clip-22 as well.
- If EbSynth isn't enough for faces, escalate to Kaggle/Wan character replacement.
