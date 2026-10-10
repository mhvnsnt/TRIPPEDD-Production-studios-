# Wave 16 Lane D — quarantine spot-check (rows 146–159 + older unaudited rows) + Speaches Docker

**Date:** 2026-10-07 · **Worker:** Wave 16 Lane D · **Branch:** `wave16-lane-d`

## Scope
- Rows 146–159 spot-checked against upstream (GitHub API `spdx_id`, root LICENSE/COPYING files, official license pages).
- 10 older rows re-verified: 13, 49, 63, 77, 80, 90, 98, 108, 109, 121.
- LGPL doctrine question (rows 63, 121, 148, 154): NOT decided — owner has not ruled. Noted as pending only.
- I did **not** edit `docs/LICENSE_QUARANTINE.md` or `docs/RESOURCE_CATALOG.md`; corrections are in PROPOSED EDITS below for the coordinator.

---

## Rows 146–159 — verdicts

| # | Project | Upstream checked | Verdict |
|---|---------|-----------------|---------|
| 146 | subsai (absadiki) | GitHub API spdx_id | **CONFIRMED** — GPL-3.0 |
| 147 | noScribe (kaixxx) | GitHub API spdx_id | **CONFIRMED** — GPL-3.0 |
| 148 | dsnote / Speech Note (mkiol) | GitHub API spdx_id | **CONFIRMED** — MPL-2.0 (weak copyleft — see LGPL-doctrine note below) |
| 149 | Subtitld (subtitld) | GitHub API spdx_id | **CONFIRMED** — GPL-3.0 |
| 150 | Penguin-Subtitle-Player (carsonip) | GitHub API spdx_id | **CONFIRMED** — GPL-3.0 |
| 151 | MediaConch (MediaArea) | MediaConch_SourceCode root LICENSE + per-file headers + mediaarea.net/MediaConch project page + docs-repo SourceCode/License.html | **RELICENSED (partial)** — upstream GUI source is now **BSD-2-Clause**: `MediaArea/MediaConch_SourceCode` root LICENSE is the BSD 2-Clause text, `Source/CLI/*.cpp|h` file headers say "governed by a BSD-style license", and the official project page now reads "All software and source code developed by MediaArea is under a BSD-2-Clause license." BUT the stale `SourceCode/License.html` in the docs repo still says "All the code in this repository is licensed under GPLv3+ / MPLv2+." Upstream is self-contradictory. Recommendation: KEEP quarantined until a dep-tree audit confirms every shipped component (MediaInfoLib, policyCheckWeb, web UI) is under the BSD relicensing and no GPL component remains. Do NOT delist on this wave. |
| 152 | lossless-cut (mifi) | GitHub API spdx_id + root LICENSE fetched | **CONFIRMED, but DUPLICATE** — license verified GPL-2.0; upstream LICENSE is the GPL-2.0-only text. Same project as **row 13**. Row 152 → SUPERSEDED by row 13 (see PROPOSED EDITS). |
| 153 | MeGUI | SourceForge project page ("License version 2.0 (GPLv2)") | **CONFIRMED** — GPLv2 |
| 154 | GPAC / MP4Box (gpac) | GitHub API spdx_id | **CONFIRMED** — LGPL-2.1 (weak copyleft — see LGPL-doctrine note below) |
| 155 | MKVToolNix | Debian copyright mirror (sources.debian.org/src/mkvtoolnix) = GPL-2+; GitLab raw fetch blocked by Cloudflare challenge | **CONFIRMED** — GPL-2.0-or-later. Propose tightening the row's bare "GPL v2" to "GPL-2.0-or-later". |
| 156 | VidCoder (RandomEngy) | GitHub API spdx_id | **CONFIRMED** — GPL-2.0 |
| 157 | mpv (mpv-player) | GitHub API spdx_id (NOASSERTION, "Other") — license stated in-repo | **CONFIRMED as stated** — row's "GPLv2+ (repo Copyright file)" stands; no change |
| 158 | VLC (videolan) | GitHub API spdx_id | **CONFIRMED, but DUPLICATE** — GPL-2.0, same project as **row 90**. Row 158 → SUPERSEDED by row 90. |
| 159 | Bazarr (morpheus65535) | GitHub API spdx_id | **CONFIRMED, but DUPLICATE** — GPL-3.0, same project as **row 98**. Row 159 → SUPERSEDED by row 98. |

**Rows 146–159 duplicates:** 152→13, 158→90, 159→98. (Note: rows 13/90/98 predate 146–159, so the older rows are the canonical ones per the dedup-mapping convention.)
**Rows 146–159 relicensing events:** 1 — MediaConch (151), BSD-2-Clause relicensing with stale docs; quarantine standing unchanged pending dep-tree audit.

---

## Older rows re-verified (10)

| # | Project | Upstream checked | Verdict |
|---|---------|-----------------|---------|
| 13 | LosslessCut (mifi/lossless-cut) | GitHub API spdx_id + root LICENSE (GPLv2 text) | **CONFIRMED** — GPL-2.0-only. Canonical row for row 152's duplicate (see PROPOSED EDITS: harmonize license string). |
| 49 | whisper-timestamped (linto-ai) | GitHub API spdx_id | **CONFIRMED** — AGPL-3.0, repo not archived |
| 63 | marytts | (not re-verified — LGPL doctrine pending owner) | **PENDING** — LGPL-3.0; delist recommendation still awaiting owner verdict. NOT decided on this wave. |
| 77 | mmd_tools (MMD-Blender/blender_mmd_tools) | GitHub API spdx_id | **CONFIRMED** — GPL-3.0 |
| 80 | ComfyUI-Manager (ltdrdata → Comfy-Org) | GitHub API on `Comfy-Org/ComfyUI-Manager` | **CONFIRMED** — GPL-3.0 at the new canonical location `Comfy-Org/ComfyUI-Manager` (row already notes the move; propose updating the parenthetical to the new org as primary). |
| 90 | VLC (VideoLAN) | GitHub API spdx_id | **CONFIRMED** — GPL-2.0. Canonical row for row 158's duplicate. |
| 98 | Bazarr | GitHub API spdx_id | **CONFIRMED** — GPL-3.0. Canonical row for row 159's duplicate. |
| 108 | opensubtitles-api (Ivshti legacy JS client) | README license header ("either version 3 of the License, or (at your option) any later version") | **CONFIRMED** — GPL-3.0-or-later (GitHub spdx_id null — license stated in-repo, as before) |
| 109 | CCExtractor | GitHub API spdx_id (GPL-2.0); root COPYING 404 at master (no license file at repo root — license via spdx metadata) | **CONFIRMED** — GPL-2.0 (spdx). Note: no COPYING at root; GitHub spdx metadata is the current verification anchor. |
| 121 | AivisSpeech (Aivis-Project/AivisSpeech) | (not re-verified — LGPL doctrine pending owner) | **PENDING** — LGPL-3.0 per policy.md; stays quarantined meanwhile. NOT decided on this wave. |

**New duplicates found this wave:** rows 13/152 (LosslessCut), 90/158 (VLC), 98/159 (Bazarr).

---

## LGPL / weak-copyleft doctrine — STILL PENDING OWNER VERDICT

- Row 63 (marytts, LGPL-3.0), row 121 (AivisSpeech, LGPL-3.0), row 148 (dsnote, MPL-2.0), row 154 (GPAC, LGPL-2.1): all treated as **quarantined until the owner rules** on the Wave 8 Lane B delist recommendation. This wave makes no doctrine decision.
- No owner verdict recorded in `docs/LICENSE_QUARANTINE.md` as of 2026-10-07.

---

## Speaches Docker attempt — STILL DEFERRED (no Docker in sandbox)

- Check run: `docker --version` → `docker: command not found`; `podman --version` → `podman: command not found`.
- Same outcome as prior waves (no container runtime in this sandbox). Speaches smoke test cannot be run here; remains deferred to a Docker-capable environment.
- For the record: Speaches (ghcr.io/speaches-ai/speaches) is the Wave-14-flagged caption candidate (MIT, STT+diarization+TTS in one container). No verification claim made — NOT faked.

---

## PROPOSED EDITS (for the coordinator — do not apply unilaterally)

1. **Dedup — row 152 → row 13:** append to row 152's audit-status/note column: "SUPERSEDED by row 13 (mifi/lossless-cut — same project listed twice; Wave 16 Lane D, 2026-10-07)." Correct row 152's license string from "GPL-2.0" to "GPL-2.0-only" for consistency with row 13 (upstream LICENSE is the GPL-2.0-only text).
2. **Dedup — row 158 → row 90:** append: "SUPERSEDED by row 90 (VideoLAN VLC — same project listed twice; Wave 16 Lane D, 2026-10-07)."
3. **Dedup — row 159 → row 98:** append: "SUPERSEDED by row 98 (Bazarr — same project listed twice; Wave 16 Lane D, 2026-10-07)."
4. **Row 151 (MediaConch) note:** append to license column: "(RELICE
...[truncated 1096 chars]