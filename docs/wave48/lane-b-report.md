# Wave 48 Lane B — Lane Report

**Date:** 2026-10-08 · **Branch:** `wave48-lane-b` (worktree
`/home/hatch/workspace/agent-ops/wave48-lanes/lane-b`, base `origin/main @ 38e79a7`)
**Commits:** `afadb72` (cycle 19), `beeb919` (tool wires) — both pushed to
`origin/wave48-lane-b`. **Pushed:** yes, no force-push.

## Part 1 — Re-verification cycle 19: 10/10 confirmed, zero changes

Selected the 10 oldest rows with no re-verification tag (rows 69/70 excluded:
they were confirmed in the Wave 27 spot-check even though annotated "verified"
rather than "re-verified"). Every license re-checked against upstream
(GitHub API `/license` + raw LICENSE/COPYING fetch + archived/drift check).

| Row | Project | Claimed | Verified 2026-10-08 | URL drift? |
|---|---|---|---|---|
| 55 | comic-text-detector | GPL-3.0 | ZsIsMe fork live, not archived, pushed 2026-08-25; API spdx_id GPL-3.0; original zyddnys still 404 | none |
| 62 | phonemizer | GPL-3.0 | bootphon/phonemizer live, pushed 2026-09-30; API spdx_id GPL-3.0 | none |
| 63 | marytts | LGPL-3.0 | marytts/marytts live, pushed 2025-01-17; raw LICENSE.md still "LGPL … version 3 of the License" | none |
| 64 | Fooocus | GPL-3.0 | lllyasviel/Fooocus live, pushed 2025-12-01; API spdx_id GPL-3.0 | none |
| 66 | Surge XT | GPL-3.0 | surge-synthesizer/surge live, pushed 2026-10-01; API spdx_id GPL-3.0 | none |
| 67 | Dexed | GPL-3.0 | asb2m10/dexed live, pushed 2026-09-21; API spdx_id GPL-3.0 | none |
| 72 | Ardour | GPL-2.0-or-later | Ardour/ardour live, pushed 2026-10-07; source header still "either version 2 … or (at your option) any later version"; GitHub COPYING = GPL v2 text | none |
| 73 | Audacity | GPL-3.0 | audacity/audacity live, pushed 2026-10-08; LICENSE.txt top line still "…version 3 (GPLv3)" | none |
| 75 | Dragonfly Reverb | GPL-3.0 | michaelwillis/dragonfly-reverb live, pushed 2026-05-21; API spdx_id GPL-3.0 | none |
| 80 | ComfyUI-Manager | GPL-3.0 | Comfy-Org/ComfyUI-Manager live, pushed 2026-10-08; API spdx_id GPL-3.0 | none |

**Result:** 10/10 as claimed. **Zero relicenses, zero delists, zero archive
events, zero URL drift** (nothing like the MKVToolNix→Codeberg or Helm-archived
drifts from prior cycles). All rows annotated `(re-verified Wave 48 Lane B,
2026-10-08: …)` in `docs/LICENSE_QUARANTINE.md`. LGPL doctrine still PENDING
OWNER VERDICT — row 63 (LGPL-3.0) stays quarantined.

## Part 2 — Tool wires (permissive licenses only)

- **Wire 1 — moviepy 2.1.2 (MIT):** 24 PNG frames → 2.0s @12fps H.264 MP4
  (`out.mp4`, 25,246 B) → reopened, duration/fps/frame-count exact →
  middle-frame pixel round-trip mean-abs-diff 1.655 (< 8.0 gate). License
  verified: GitHub API spdx_id MIT + raw LICENCE.txt. Honest note: ffmpeg
  (LGPL binary) used as an external subprocess via imageio-ffmpeg from the
  scratch venv — not committed; nothing GPL/AGPL linked or imported.
- **Wire 2 — OpenCV 5.0.0 (Apache-2.0):** film-restoration filters on a
  seeded synthetic frame — `fastNlMeansDenoising`: RMSE 24.15→14.50 (gate
  < noisy×0.9) — `inpaint` (Telea) scratch removal: RMSE 172.25→59.06.
  Before/after PNGs reopened and visually inspected: scratches gone.
  License verified: GitHub API spdx_id Apache-2.0 + raw LICENSE text.

Proofs: `tools/wave48_lane_b/` — `PROOFS.md`, `SHA256SUMS` (38 files, all
`sha256sum -c` OK), `wire_moviepy_video.py`, `wire_opencv_restore.py`,
`proofs_moviepy/` (incl. real `out.mp4`), `proofs_opencv/` (incl.
`inpainted.png`). Reproduce via scratch venv (see PROOFS.md). **No failures;
nothing faked.** Deferred: native FFmpeg CLI wire (covered as subprocess via
moviepy; no system-wide ffmpeg installed and none was needed).
