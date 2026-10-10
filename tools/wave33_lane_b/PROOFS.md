# Wave 33 Lane B — re-verification cycle 4 proofs

## Tool wired: `audit_row_w33.py` (quarantine-row upstream license verifier)

Verbatim copy of the Wave 32 Lane B donor `../wave32_lane_b/audit_row_w32.py`
(DONOR FIRST — no rewrite). Given a row number it (1) pulls the manifest's
claimed license, (2) fetches the GitHub repo API record (existence / archived /
pushed_at / spdx_id) into `api.json`, (3) fetches raw license files (tries
`master` then `main`) into `proofs_rowNN/`, (4) prints a mechanical verdict
(CONFIRMED / NEEDS REVIEW / REPO MISSING) — the lane auditor still makes the
final call.

**Run (this wave, 2026-10-08):**
`python3 ../wave32_lane_b/audit_row_w32.py --row NN --out-dir tools/wave33_lane_b/proofs_rowNN`
for rows 16, 18, 19, 21, 22, 23, 25, 26, 28, 29, 68, 236 — all completed, fresh
fetch artifacts on disk. Full run log: `audit_run.log`.

## Cycle-4 results (rows 16, 18, 19, 21, 22, 23, 25, 26, 28, 29, 68, 236) — 12/12 confirmed

| row | project | upstream state 2026-10-08 | evidence in proofs_rowNN/ | verdict |
|-----|---------|---------------------------|---------------------------|---------|
| 16 | Olive | olive-editor/olive live, not archived, pushed 2024-12-05 (stale), API GPL-3.0 | LICENSE (GPL v3 29 June 2007, "any later version" clause) | CONFIRMED GPL-3.0 |
| 18 | Papagayo-NG | morevnaproject-org/papagayo-ng live, not archived, pushed 2023-04-25 (stale), API spdx None (detection gap) | gpl.txt (GNU GPL Version 2, June 1991) | CONFIRMED GPL-2.0 |
| 19 | Pencil2D | pencil2d/pencil live, not archived, pushed 2026-10-05, API GPL-2.0 | LICENSE.TXT (GPL v2 June 1991) | CONFIRMED GPL-2.0-only |
| 21 | Power Sequencer | GDQuest/blender-power-sequencer live, not archived, pushed 2026-01-16, API GPL-3.0 | LICENSE (GPL v3 29 June 2007) | CONFIRMED GPL-3.0(-or-later) |
| 22 | RHVoice | RHVoice/RHVoice live, not archived, pushed 2026-09-28, API GPL-2.0 | LICENSE.md (GPL v2) + doc/en/License.md (lib LGPL-2.1-or-later; MAGE GPL-3.0-or-later dep) | CONFIRMED (engine/combo claim) |
| 23 | Shotcut | mltframework/shotcut live, not archived, pushed 2026-10-06, API GPL-3.0 | COPYING (GPL v3 29 June 2007, "any later version" clause) | CONFIRMED GPL-3.0-or-later |
| 25 | Synfig Studio | synfig/synfig live, not archived, pushed 2026-10-03, API GPL-3.0 | LICENSE (GPL v3 29 June 2007) | CONFIRMED GPL-3.0 |
| 26 | TupiTube | e7appew/tupitube.desk live, not archived, pushed 2018-02-02 (stale), API GPL-2.0 | COPYING (GPL v2 June 1991) | CONFIRMED GPL-2.0-family (-or-later still unconfirmed) |
| 28 | Allosaurus | xinjli/allosaurus live, not archived, pushed 2024-04-26, API GPL-3.0 | LICENSE (GPL v3 29 June 2007) | CONFIRMED GPL-3.0 |
| 29 | Avidemux | mean00/avidemux2 live, not archived, pushed 2026-10-07, API NOASSERTION (detection gap on COPYING) | COPYING (GPL v2 June 1991) | CONFIRMED GPL-2.0 |
| 68 | Helm | mtytel/helm still owner-archived, pushed 2022-09-24, API GPL-3.0 | COPYING (GPL v3 29 June 2007) | CONFIRMED GPL-3.0 |
| 236 | telxcc | kanongil/telxcc still owner-archived, pushed 2025-09-20, API NOASSERTION | LICENSE ("either version 2 of the License, or (at your option) any later version") | CONFIRMED GPL-2.0-or-later |

Zero relicensing events, zero delists, zero ownership transfers, zero new rows,
zero duplicates. `docs/LICENSE_QUARANTINE.md` updated append-only with
"(re-verified Wave 33 Lane B, 2026-10-08: …)" notes on all 12 rows.

## Identity-drift watch (fresh vs Wave 32 snapshots)

Compared each fresh `api.json` against the Wave 32 pre-fetched snapshot
(owner login, archived, pushed_at, spdx_id, license-sha, default_branch) and
sha256'd every raw license file old-vs-new:
- **No ownership transfers, no archival changes, no license-file changes, no
  default-branch changes on any of the 12 rows.**
- Rows 68 (Helm) and 236 (telxcc) remain owner-archived with no official
  successor or new notable fork activity since Wave 32.
- All pushed_at values unchanged since the snapshot — no upstream pushes landed
  between the two checks.

## Speaches Docker / VGMTrans

Skipped per lane brief (no container runtime / no Qt dev libs) — not in this
wave's row set.

## Catalog additions

None. All 12 rows remain strong copyleft (GPL-2.0 / GPL-3.0 / AGPL-family) and
stay quarantined — nothing newly commercial-safe. Pre-append dedup greps run
against docs/RESOURCE_CATALOG.md; no `####` entries added.

## Foreign-directive scan

Scanned docs/LICENSE_QUARANTINE.md, docs/RESOURCE_CATALOG.md, AGENTS.md and the
wired scripts for injected "autonomous / no-permission" directive blocks —
only hit was a legitimate prior-wave scan note in LICENSE_QUARANTINE.md. Clean;
nothing to ignore this wave.

## Artifacts

- `tools/wave33_lane_b/audit_row_w33.py` — the wired tool (verbatim donor copy)
- `tools/wave33_lane_b/proofs_rowNN/` — per-row `api.json` + raw license files (fresh 2026-10-08)
- `tools/wave33_lane_b/audit_run.log` — full fetch/verdict transcript
- `tools/wave33_lane_b/SHA256SUMS` — checksums for everything above
