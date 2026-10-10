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

### clip-05 (street crew) — ✅ PASS
- 2026-10-10: Extracted 100 frames @ 10fps 640x360. Created 3 cartoon keyframes.
- 2026-10-10: EbSynth started with multi-keyframe anchoring (0, 49, 99). Process DIED in runtime restart (~09:30 CDT). /tmp partial output LOST.
- 2026-10-10 09:38 CDT: Resumed. Found end keyframe was BLACK (clip fades to black at frame 100). Rebuilt end keyframe from frame 80. Restarted EbSynth.
- 2026-10-10 09:45 CDT: **EbSynth output FAILED QC** — heavy smearing/artifacts on group scene (patch matching failed with 9 characters + camera movement).
- 2026-10-10 09:47 CDT: **Pivoted to direct cartoon filter** (bilateral + adaptive edge + saturation boost) applied to every frame. Result: clean 2D cartoon, characters recognizable, no artifacts. **QC PASS.**
- Final: clip-05-cartoon-30fps.mp4 (1280x720, 30fps, 10s). Awaiting owner approval before timeline insertion.

### clip-15 (basketball) — ✅ PASS
- 2026-10-10: INTRA-CLIP DRIFT confirmed — frame 1 is 2D cartoon, frame 20+ is photorealistic. Same content, style changes mid-clip.
- 2026-10-10: Applied direct cartoon filter to all 300 frames @ 30fps. Intra-clip drift FIXED — entire clip now consistent 2D cartoon. Hollow's mask, dragon suit all clean. **QC PASS.**
- Final: clip-15-cartoon-30fps.mp4 (1280x720, 30fps, 10s). Awaiting owner approval before timeline insertion.

### clip-22 (podcast) — ✅ PASS
- 2026-10-10: INTRA-CLIP DRIFT confirmed — frame 1 is 2D cartoon, frame 50 is photorealistic (realistic skin, pores).
- 2026-10-10: Applied direct cartoon filter to all 300 frames @ 30fps. Intra-clip drift FIXED. Static recognizable, tattoos clear, ON AIR sign readable. **QC PASS.**
- Final: clip-22-cartoon-30fps.mp4 (1280x720, 30fps, 10s). Awaiting owner approval before timeline insertion.

## Method Note

EbSynth (patch-based style propagation) FAILED on clip-05's complex group scene — smearing artifacts. Direct per-frame cartoon filtering (OpenCV: bilateralFilter + adaptiveThreshold edges + HSV saturation boost) proved superior for these shots: faster (~20s per 100 frames vs ~60min), no temporal artifacts, consistent style. EbSynth remains available for shots where the cartoon filter alone isn't enough, but wasn't needed here.

## Kaggle Staging

Prepared inputs for owner to run on Kaggle notebook:
- ~/workspace/video-fix-tools/kaggle-staging/
- clip-15 (basketball): driving video ready, needs 2D character reference
- clip-22 (podcast): driving video ready, needs 2D character reference

## Notes

- EbSynth: CPU ~40s/frame @ 640x360.
- If EbSynth output on clip-05 is good, apply to clip-15 and clip-22 as well.
- If EbSynth isn't enough for faces, escalate to Kaggle/Wan character replacement.
