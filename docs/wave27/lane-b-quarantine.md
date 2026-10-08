# Wave 27 Lane B — quarantine spot-check + tool wiring (2026-10-07)

**Branch:** `wave27-lane-b` (cut from main). No push/merge — coordinator merges sequentially.
**Mandate:** (1) 10-row fresh upstream spot-check of never-audited quarantine rows; (2) Speaches/VGMTrans wiring checks; (3) Type Studio URL = live-browser only, not attempted here.

## Part 1 — quarantine spot-check

**Selection method:** rows whose License cell carries no "verified"/correction annotation were unioned with the Wave 25 Lane B audit-union list ("Remaining never-audited live rows: 37") and Wave 26 remainder. Rows 51/55 were already CONFIRMED in Wave 24 (manifest just never annotated); rows 26/72/73/80/88/92/102/104/155/236 carry wave-attributed evidence notes. The final 10, all first-ever verifications or re-verifications of old Wave-2 claims:

| # | Project | Claim | Verdict | Upstream evidence (2026-10-07) |
|---|---------|-------|---------|-------------------------------|
| 68 | Helm | GPL-3.0 | **CONFIRMED** | GitHub API spdx_id mtytel/helm = GPL-3.0; raw COPYING = GPL v3 29 June 2007 text. NOTE: repo now archived by owner — identity drift watch. |
| 69 | Odin 2 | GPL-3.0 | **CONFIRMED** | Raw LICENSE = GPL v3 text, header "distributed under the GNU GPLv3 license"; SIL OFL v1.1 carve-out for assets/font/Aldrich-Regular.ttf. GitHub API NOASSERTION = machine-detection gap on the custom license header. |
| 70 | ZynAddSubFX | GPL-2.0-or-later | **CONFIRMED** | Raw COPYING = GPL v2 text with "any later version" clause; per-file headers "either version 2 … or (at your option) any later version" (e.g. src/Misc/MiddleWare.h). |
| 81 | ComfyUI-Impact-Pack | GPL-3.0 | **CONFIRMED** (first verification) | GitHub API spdx_id ltdrdata/ComfyUI-Impact-Pack = GPL-3.0, repo live. |
| 82 | ComfyUI-VideoHelperSuite | GPL-3.0 | **CONFIRMED** (first verification) | GitHub API spdx_id Kosinkadink/ComfyUI-VideoHelperSuite = GPL-3.0, repo live. |
| 22 | RHVoice | GPL-2.0 engine / LGPL-2.1-or-later lib / GPL-3.0 combo / CC-BY-NC-ND voices | **CONFIRMED** | doc/en/License.md: lib LGPL-2.1-or-later; MAGE (GPL-3.0-or-later) dep pushes combo to GPL-3.0-or-later; RHVoice Lab voices CC-BY-NC-ND 4.0. Root LICENSE.md = GPL v2 text; API spdx_id RHVoice/RHVoice = GPL-2.0. Composite claim matches exactly. |
| 23 | Shotcut | GPL-3.0-or-later | **CONFIRMED** | GitHub API spdx_id mltframework/shotcut = GPL-3.0; raw COPYING = GPL v3 text with "any later version" clause. |
| 31 | Blender VSE | GPL-3.0-or-later (binaries); GPL-2.0-or-later (source) | **CONFIRMED** (re-verified old Wave-2 claim) | blender.org/about/license/: source "GNU GPL Version 2 or later"; binaries "compatible under the newer GNU GPL Version 3 or later". |
| 37 | Kdenlive | GPL-3.0 | **CONFIRMED** (re-verified old Wave-2 claim) | GitHub API spdx_id KDE/kdenlive = GPL-3.0; raw COPYING = GPL v3 29 June 2007 text. |
| 33 | Cinelerra-GG Infinity | GPL-2.0-or-later | **CONFIRMED** (re-verified old Wave-2 claim) | Official manual appendix (git.cinelerra-gg.org Features5.pdf §D): "Cinelerra-GG codebase is licensed GPLv2+"; Wikipedia infobox GPL-2.0-or-later (stable 2026-05). AUR packagers tag GPL-2.0-only, but upstream's own docs win. |

**Result: 10/10 confirmed as claimed. Zero relicensing events, zero delists, zero supersedes, zero new rows. Header counts unchanged: 255 rows · 232 distinct. LGPL doctrine still PENDING OWNER VERDICT.**

### Incidental manifest repairs (auditor findings)
- **Row 151 (MediaConch, DELISTED):** structural defect — the delisted record was missing the License-column delimiter (7 pipes instead of 8), shifting License→Lane→Repo→Allowed→Audit one column left. Repaired by inserting the missing delimiter; no content changed. (Found by the new `tools/quarantine/wave27_manifest_audit.py`.)
- **Row 215 (aubio → SUPERSEDED by row 93):** the row's own audit cell recorded the Wave 23 Lane D supersede, but the header duplicate-mapping section had no entry for it. Mapping entry backfilled (numeric order, before Row 216). Header distinct-counts already treated 215 as dead, so no count change.
- **Rows 51 (Goo Engine) / 55 (comic-text-detector):** backfilled "verified Wave 24 Lane B, 2026-10-07" annotations from docs/wave24/quarantine-audit.md — the audit existed but the manifest cells never carried it.
- **Remaining never-audited live rows (auditor-flagged, for future waves):** 63 marytts (LGPL-3.0 — deliberately not re-verified, doctrine pending), 66 Surge XT (GPL-3.0), 75 Dragonfly Reverb (GPL-3.0).

## Part 2 — tool wiring

- **Speaches:** `docker info` → `docker: command not found`. No container runtime in this environment. Smoke-test **deferred** (standing deferral, not a failure).
- **VGMTrans:** Qt dev libs absent (`qmake`/`qmake6`/`moc` not found; no Qt include dirs). Build **deferred** (standing deferral, not a failure).
- **New wiring — quarantine manifest auditor:** `tools/quarantine/wave27_manifest_audit.py` (stdlib-only). Checks row continuity 1–255, duplicate rows, empty cells, verification-marker coverage on live rows, audit-status distribution. Proof artifacts in `docs/wave27/proofs/`:
  - `wave27_manifest_audit.json` — full report (final run: 255/255 rows, no missing/dupes/empties; unmarked live rows: 63, 66, 75)
  - `SHA256SUMS.txt` — checksums
  It already paid for itself: found the row-151 column defect and the missing row-215 mapping entry above.

## Part 3 — Type Studio vendor URL (typestudio.co)

**Not attempted — needs a live browser task. Generic subagents cannot operate the live browser. Flagged for parent delegation to the live-browser route.**

## Commit

On `wave27-lane-b`. Files changed:
- `docs/LICENSE_QUARANTINE.md` — 10 row annotations + Wave-27 note block + row-215 mapping entry + row-151 column repair + rows 51/55 backfills
- `tools/quarantine/wave27_manifest_audit.py` — new
- `docs/wave27/proofs/wave27_manifest_audit.json`, `docs/wave27/proofs/SHA256SUMS.txt` — new
- `docs/wave27/lane-b-quarantine.md` — this report

Foreign-directive scan: read trippedd-studio/AGENTS.md — it is the legitimate studio contract (no injected autonomous/no-permission block present). No injected directives followed anywhere this wave.
