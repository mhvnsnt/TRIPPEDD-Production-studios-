# Wave 57 Lane B — re-verification cycle 28 report

**Date:** 2026-10-08 · **Lane:** B (Lane B is the re-verification lane) · **Branch:** `wave57-lane-b`

## Scope

Rows 291–300 — the 10 oldest never-reverified live rows (bare-date "(verified Wave 37/38 Lane A, 2026-10-08)" annotations, no wave-era stamp):

- 291 AntennaPod (AntennaPod/AntennaPod) — GPL-3.0
- 292 BUTT (danielnoethen.de/butt) — GPL-2.0
- 293 Rivendell (ElvishArtisan/rivendell) — GPL-2.0
- 294 OpenBroadcaster (openbroadcaster) — AGPL-3.0
- 295 ExifTool (exiftool/exiftool) — GPL-3.0
- 296 QPrompt (Cuperino/QPrompt-Teleprompter) — GPL-3.0
- 297 OpenDCP (tmeiczin/opendcp) — GPL-3.0
- 298 Redmine (redmine/redmine) — GPL-2.0
- 299 OpenProject (opf/openproject) — GPL-3.0
- 300 Leantime (Leantime/leantime) — AGPL-3.0

## Method

Fresh upstream checks per row: GitHub API (repo existence, archived flag, pushed_at, owner, spdx_id), `/license` endpoint content fetch (path + byte size + SPDX), raw LICENSE/COPYING/COPYRIGHT.txt/LICENSES/GPLv2.txt/doc/COPYING byte-count fetches; SourceForge project license field + author-site HTTP for BUTT (non-GitHub canonical). NOASSERTION always treated as detection gap and resolved by direct text reads. Nothing assumed.

## Result: 10/10 CONFIRMED as claimed

- **Zero relicenses** (no ArchiveBox-Wave-56-style reversal this cycle)
- **Zero delists, zero supersedes, zero new rows, zero duplicates**
- 1 repo-move note: row 294 — `observer/obplayer` now 404s; canonical upstream is `openbroadcaster/obplayer` (live, pushed 2026-09-23, API spdx_id AGPL-3.0, raw COPYING 34,521 bytes = AGPL v3 text). Same project, same license — evidence pointer updated in the row stamp, not a relicense.
- 2 NOASSERTION detection gaps resolved by direct text reads: row 293 (REUSE-style LICENSES/ dir; grant at LICENSES/GPLv2.txt on default branch **v4**, not master — fetch-path note added), row 298 (API surfaces the 918-byte LICENSE.txt pointer; grant at doc/COPYING, 18,092 bytes = GPL v2 text).
- 1 fetch-path note: row 297 grant file is COPYRIGHT.txt (31,703 bytes, carries GPL v3 text).

All 10 rows stamped in-table with dated `(re-verified Wave 57 Lane B, 2026-10-08: ...)` annotations; cycle header note added to `docs/LICENSE_QUARANTINE.md`. Table integrity verified: 8 pipes on every stamped row (no broken columns), stamp text contains zero literal pipes.

## Drift watch (7) — all clean vs cycle 27

| Item | Row | Status |
|------|-----|--------|
| Helm | 68 | mtytel/helm STILL owner-archived, pushed 2022-09-24T04:23:20Z, owner mtytel — no successor, no ownership change, no relicense |
| telxcc | 236 | kanongil/telxcc STILL archived, pushed 2025-09-20T11:29:10Z, owner kanongil — no change |
| MB-Lab | 118 | animate1978/MB-Lab STILL owner-archived, pushed 2024-07-21T02:46:17Z — no change |
| SubDownloader | 195 | subdownloader/subdownloader STILL archived, pushed 2025-02-05T11:39:33Z — no change |
| MPC-HC | 191 | mpc-hc/mpc-hc STILL archived, pushed 2020-04-24T11:04:40Z — no change |
| MKVToolNix | 155 | codeberg.org/mbunkus/mkvtoolnix still canonical, not archived, updated 2026-09-28; raw COPYING **18,092 bytes byte-identical** to Waves 41–56 checks |
| uzu/tidal | 101 | codeberg.org/uzu/tidal still live, not archived, updated 2026-07-02; raw LICENSE **35,106 bytes byte-identical** to Waves 38–56 checks |

## Files delivered

- `docs/LICENSE_QUARANTINE.md` — 10 row stamps + cycle-28 header note
- `docs/wave57/lane-b/README.md` — proof index
- `docs/wave57/lane-b/cycle28_raw_results.json` — raw API payloads for all 10 rows + 7 drift items
- `docs/wave57/lane-b/row293_LICENSES_GPLv2.txt` — raw GPL v2 from rivendell@v4
- `tools/wave57_lane_b/cycle28_verify.py` — verification harness
- `tools/wave57_lane_b/stamp_cycle28.py` — row stamping + header note
- This report: `docs/wave57/lane-b-report.md`

## Standing notes

- Header counts unchanged by this lane (zero row additions/removals/delists).
- LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined; this lane does not decide it.
- Did not touch `production/` or `WIZARD_GANG_EP01/`.
