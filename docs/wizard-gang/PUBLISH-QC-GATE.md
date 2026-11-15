# Pre-publish QC gate — Wizard Gang page (phase 3a, 2026-11-13)

Home repo: **mhvnsnt/wizard-gang-voice-pipe**,
`tools/ai-qc/publish_gate.py` (+ `publish_gate.sh`, `PUBLISH-QC-GATE.md`).
Landing PR: https://github.com/mhvnsnt/wizard-gang-voice-pipe/pull/7

## Where it sits

Between media selection and draft creation in the runner playbook
(playbook "Each run" steps 4–5). Nothing that fails the gate gets drafted.
Pipeline V1 / EP01 v10 is frozen and untouched by this work.

## What it runs

- **Audio:** duration, VAD speech coverage, silence gaps ≥2s, clipping,
  volume anomalies, overlap regions, voice identity vs `--expect-voice`
  (MFCC centroids from `--ref-dir`, default `~/workspace/voice-delivery`).
- **Video (mp4):** MP4/h264 format (page rule), audio stream, duration
  warning >90s, full audio gate on its soundtrack, frozen frames ≥3s,
  glitch/blocky frames, grading jumps, still regions ≥4s, camera shake,
  talking regions (face landmarker), OCR subtitle + watermark scan.
- **Image (png/jpg):** page-accepted format (webp FAILs on purpose —
  playbook rule webp→png), decode + dimensions, face presence INFO only.
- **Mesh (glb/obj):** `mesh_qc` audit.

Output: JSON report + `VERDICT: PASS|FAIL` line. Exit 0 PASS / 1 FAIL /
2 usage. SHA-256 of every input is recorded in the report.

## Rules (never fake a pass)

- SKIP always carries a reason and is never a PASS.
- Face/mouth checks on cartoon art are INCONCLUSIVE, never pass/fail —
  MediaPipe is trained on real faces (verified: council still → 0 faces).
- OCR checks SKIP while the tesseract binary is absent (logged gap).

## Proof (2026-11-13, real WG artifacts; reports in voice-pipe `tools/ai-qc/proof/`)

| Asset | Result |
|---|---|
| `voice-cipher-c1-v3.mp3` (`--expect-voice cipher`) | **PASS** — 6 pass, 1 warn (volume drops), 0 fail. Reproduced byte-identically by a second run through the wrapper |
| `cipher_pose_comparison.png` | **PASS** — 3 pass, 0 fail; 0 real-face detections (INFO only) |
| `static-heyyo-final.mp4` (`--expect-voice static`) | **PASS** — 11 pass, 3 warn, 0 fail, 3 skip. Voice-match predicted static |
| `static-heyyo-glitch.mp4` (pocket-studio glitch render, `--expect-voice static`) | **FAIL** — 6 pass, 1 warn, 1 fail, 3 skip. The single FAIL is `audio-load: No usable temporary directory found` — the disk quota wall made every temp dir unwritable, so the audio track could not be extracted. **Not a clip defect:** format, frozen-frames, glitch-scan, grading-shifts and still-regions all PASS. Report: `tools/ai-qc/proof/proof-gate-video-static-heyyo-glitch-20261113.json` |

Calibration notes: `glitch-scan` and `camera-shake` WARN on the clean
source clip (flat-colour cartoon blocks trip the blocky detector;
the promo has intentional motion) — WARN means "look", not "bad".

## Known gaps

1. tesseract not installed on this VM (apt broken) — OCR checks SKIP.
2. Voice-match needs a local `--ref-dir` with the voice refs.
3. MediaPipe needs the EGL shim on this VM — `setup-egl-shim.sh`
   fetches official Ubuntu libEGL/libGLES .debs (sha256-verified) into
   local-only `egl-libs/` (gitignored, never committed).
4. Disk quota wall vs temp files — the gate extracts video audio via a
   temp file. When the VM's quota wall is up, every temp dir becomes
   unwritable and the gate FAILs on `audio-load: No usable temporary
   directory found`. That FAIL means the environment, not the asset —
   retry when the wall clears, or set `TMPDIR` to a writable location.
   (Proven 2026-11-13 on the glitch clip; also swallowed two earlier
   gate runs at the report-write stage.)
