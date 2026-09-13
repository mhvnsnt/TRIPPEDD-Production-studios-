# Production Resume — 2026-09-12

## Current authority

`main` is the current production line. The existing Express/Vite runtime remains the production authority. The Next.js surface is an operator/evidence cockpit and must not be treated as a replacement backend.

## Subscription-free preview

Rocket is not a durable dependency: its current session reports exhausted credits. The repo now has a static Next.js export path and a GitHub Pages workflow:

- `next.config.ts` uses `output: 'export'`.
- `.github/workflows/production-cockpit-pages.yml` builds `out/` and deploys it with the official GitHub Pages actions.
- The cockpit is intended to expose the current work and committed evidence without requiring Rocket credits.

## Visual work being resumed

The active character problems remain:

1. Correct eyeball placement inside the head.
2. Correct upper/lower eyelid placement against the painted face texture.
3. Eyebrow placement and independence from eyelid travel.
4. Nostrils and nose placement.
5. Mouth/oral-cavity placement and visibility.
6. Hair segmentation and subsequent physical motion.
7. Motion must be rendered as a sequence/video, not inferred from a still.

The repository already contains `tools/character/motion_proof.py` and `tools/character/measure_hair.py`. The motion proof renders each frame, tracks measured lid-line vertices, and attempts to emit an MP4. The hair measurement uses trimesh connected components and geometric lock measurements before bone/physics work.

## Face authority rules

The face toolchain must remain fail-closed. MediaPipe semantic landmarks are the face/lid/brow authority; ICT-FaceKit provides named FACS shapes; GNM supplies anatomical donor information. Darkness heuristics and arbitrary pixel guesses are not authority. When a metric disagrees with the actual picture, the picture is the defect report and the metric must be investigated.

## Evidence policy

Committed images are evidence to inspect, not automatic PASS. Moving features require a rendered sequence. A single frame cannot establish motion.

## Branch cleanup status

PRs #41, #42, and #45 are historical work branches with overlapping/older bases and currently report non-mergeable. Their work should be treated as source material unless it is already present on `main`; do not overwrite newer production work merely to force a historical branch merge. PR #48 was an attempted main-to-facial-branch synchronization and is intentionally not a production integration path.

## Current cockpit

`app/page.tsx` now exposes:

- face authority status;
- eye-placement status;
- hair/motion next steps;
- direct links to the measured tools;
- a visual evidence gallery sourced from the latest facial-toolchain evidence branch.

This page is deliberately honest about structural-vs-visual gates: evidence is shown, but no screenshot is promoted to PASS merely because it exists.
