# Wave 32 Lane B — tool wiring proofs

## Tool wired: `audit_row_w32.py` (quarantine-row upstream license verifier)

**What it is:** reusable verifier for re-verification cycles on `docs/LICENSE_QUARANTINE.md`.
Given a row number it (1) pulls the manifest's claimed license, (2) fetches the GitHub
repo API record (existence / archived / pushed_at / spdx_id) into `api.json`, (3) fetches
raw license files (tries `master` then `main`) into `proofs_rowNN/`, (4) prints a
mechanical verdict (CONFIRMED / NEEDS REVIEW / REPO MISSING) — the lane auditor still
makes the final call. Cycle coverage: 42 rows in `REPO_MAP` (Waves 30–31 + Wave 32
cycle 3 + prior-attempt rows).

**Smoke test (this run, 2026-10-08):** `python3 audit_row_w32.py --row NN` for
rows 30, 34, 35, 38, 42, 43, 44, 45, 46, 47 — all completed, proofs on disk,
checksums verified (`sha256sum -c SHA256SUMS`: 50/50 OK).

**Two heuristic fixes made while wiring (honest, documented):**
1. Case-insensitive license-text matching — Praat's README §2.1 says "version 3 or
   later" (lowercase); the old uppercase-only check missed it.
2. Removed the 4000-byte haystack truncation — Praat's license clause sits past byte
   4000 of its README; truncating would have hidden real evidence.
3. Fixed a wrong upstream URL the prior attempt left in the map: row 24's
   `SUC-DriverOld/so-vits-svc` fork → canonical `svc-develop-team/so-vits-svc`.

## Cycle-3 results (rows 30, 34, 35, 38, 42, 43, 44, 45, 46, 47) — 10/10 confirmed

| row | project | upstream state 2026-10-08 | evidence in proofs_rowNN/ | verdict |
|-----|---------|---------------------------|---------------------------|---------|
| 30 | Blender Grease Pencil | blender/blender live, pushed today, API NOASSERTION (detection gap on COPYING) | COPYING (GPL umbrella) + doc_license_GPL-license.txt (GPL v2 June 1991 text) | CONFIRMED GPL-2.0-or-later source / GPL-3.0-or-later binaries |
| 34 | GIMP | GNOME/gimp live, pushed 2026-10-07, API NOASSERTION | COPYING (GPL v3 text) + LICENSE ("GIMP application core … licensed under the GNU GENERAL PUBLIC LICENSE") + gnu.org edu page "version 3 or later" | CONFIRMED GPL-3.0-or-later |
| 35 | HandBrake | live, pushed 2026-10-06, API NOASSERTION | LICENSE ("Most files … under GPL Version 2 (GPLv2)"; some files GPLv2+/LGPLv2.1+/BSD) + COPYING (GPL v2 June 1991) | CONFIRMED GPL-2.0 |
| 38 | Kitsu | blender/kitsu live not archived (pushed 2022-07-05, stale), API AGPL-3.0 | LICENSE (AGPL v3 text); drift note: canonical cgwire/kitsu also AGPL-3.0, active (pushed 2026-10-07) | CONFIRMED AGPL-3.0 |
| 42 | Praat | praat/praat → 301 → praat/praat.github.io (repo-moved, same account), live, pushed 2026-10-06, API license None | README.md §2.1: "the whole of Praat is distributed under the General Public License, version 3 or later"; en.wikipedia infobox GPL-3.0-or-later | CONFIRMED GPL-3.0-or-later (whole-distribution license) |
| 43 | Seed-VC | Plachtaa/seed-vc **ARCHIVED by owner**, pushed 2025-04-20, API GPL-3.0 | LICENSE (GPL v3 text); NEW archived-upstream note — quarantine unchanged | CONFIRMED GPL-3.0 |
| 44 | StoryPencil | olstflow/storypencil_for4.4_fix live not archived, pushed 2025-05-01, API license None (no root LICENSE) | README.md line 37: "License: GPL-3.0"; drift note: README describes itself as "Unofficial fix for the official Storypencil add-on" (now at projects.blender.org/extensions/storypencil) | CONFIRMED GPL-3.0 (auditor override of mechanical NEEDS REVIEW) |
| 45 | StoryToolkitAI | octimot/StoryToolkitAI live, pushed 2026-07-28, API GPL-3.0 | LICENSE (GPL v3 text, © 2022 Octavian Mot) | CONFIRMED GPL-3.0 |
| 46 | SubtitleComposer | maxrd2/subtitlecomposer live, pushed 2025-11-04, API NOASSERTION | root LICENSE is a REUSE pointer → LICENSES/GPL-2.0-or-later.txt (GPL v2 text fetched, 17277 bytes) | CONFIRMED GPL-2.0-or-later |
| 47 | Upscayl | upscayl/upscayl live, pushed 2026-10-05, API AGPL-3.0 | LICENSE (AGPL v3 text) | CONFIRMED AGPL-3.0 |

Zero relicensing events, zero delists, zero supersedes, zero new rows, zero duplicates.

## Recovered artifacts from the interrupted prior Lane B attempt

`proofs_row16/18/19/21/22/23/25/26/28/29/68/236/` (GitHub API dumps + raw license
fetches, written 2026-10-08 ~05:31–05:33 by the previous Lane B instance before it
died) were spot-checked and are genuine fetch artifacts — committed here as
supporting evidence, checksums included. **No verdicts are claimed on those rows by
this lane** (that worker's wave note was never finished); their proofs serve as
pre-fetched evidence for a future re-verification cycle. `audit_row_w32.py` itself
is the previous instance's tool, adopted, bug-fixed, and wired as this wave's tool.

## Drift watch (2026-10-08)

- **Helm (row 68):** mtytel/helm still owner-archived (ownership unchanged, pushed
  2022-09-24, API spdx GPL-3.0, 233 forks). No official successor, no ownership
  change. New maintenance signal: ammatwain/helm landed a real build-maintenance
  commit 2026-10-07 ("fix: update JUCE code for modern GCC and FreeType") — a
  build-compatibility fork, not a community successor (0 stars); AJ-Gonzalez/helm-apple-silicon
  (Apple-silicon maintenance fork) still the freshest recurring fork (pushed 2026-09-21).
- **telxcc (row 236):** kanongil/telxcc still archived + reachable (owner unchanged,
  14 forks; most-recent fork push 2026-03-17 xylographe/telxcc, 0 stars). No
  standout successor.

## Speaches Docker / VGMTrans environment re-check (2026-10-08)

- `docker`: not installed; no docker server. Speaches Docker still unrunnable.
- Qt6 dev libs / qmake: absent (`dpkg -l | grep -i qtbase` = 0, no /usr/include/qt6,
  no qmake). VGMTrans still unbuildable.
- Both confirmed absent by direct checks, not assumed. Documented as blocked again.

## Artifacts

- `tools/wave32_lane_b/audit_row_w32.py` — the wired tool
- `tools/wave32_lane_b/proofs_rowNN/` — per-row `api.json` + raw license files
- `tools/wave32_lane_b/SHA256SUMS` — 50/50 verified
