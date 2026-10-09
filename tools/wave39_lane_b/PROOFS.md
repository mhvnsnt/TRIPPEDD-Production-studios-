# Wave 39 Lane B — re-verification cycle 10 proofs

## Tool wired: `cycle10_verify.py` (quarantine-row upstream license verifier)

Given a row number it (1) pulls the manifest's claimed license, (2) fetches the
GitHub repo API record (existence / archived / pushed_at / spdx_id) into
`api.json`, (3) fetches raw license files (8 candidate paths × master/main)
into `proofs_rowNN/`, (4) prints a mechanical verdict (CONFIRMED / NEEDS REVIEW)
— the lane auditor makes the final call. SourceForge rows fetch the project
page license field; mirror-only rows (dvbsnoop) check each mirror's API record.

**Run (this wave, 2026-10-08):**
`python3 tools/wave39_lane_b/cycle10_verify.py --all`
for rows 57, 59, 60, 71, 145, 201, 202, 203, 204, 205 — all completed, fresh
fetch artifacts on disk. Full machine-readable verdicts: `cycle10_results.json`.

## Cycle-10 results — 10/10 confirmed as claimed

| row | project | upstream state 2026-10-08 | evidence in proofs_rowNN/ | verdict |
|-----|---------|---------------------------|---------------------------|---------|
| 57 | ChatTTS | 2noise/ChatTTS live, not archived, pushed 2026-04-10, API AGPL-3.0 | LICENSE (AGPL v3 19 November 2007) | CONFIRMED AGPL-3.0 |
| 59 | DiffSVC | prophesier/diff-svc live, not archived, pushed 2026-06-06, API AGPL-3.0 | LICENSE.md (AGPL v3 text) | CONFIRMED AGPL-3.0 |
| 60 | Trelby | trelby/trelby live, not archived, pushed 2025-10-21 (stale), API GPL-2.0 | LICENSE (GPL v2 June 1991) | CONFIRMED GPL-2.0 |
| 71 | LMMS | LMMS/lmms live, not archived, pushed 2026-09-27, API GPL-2.0 | LICENSE.txt (GPL v2 June 1991) | CONFIRMED GPL-2.0 |
| 145 | Bento4 | axiomatic-systems/Bento4 live, not archived, pushed 2026-06-27; no root LICENSE (by design) | Ap4File.h header grant + README.md dual-license section (manual review) | CONFIRMED dual GPL-2.0-or-later / commercial |
| 201 | open-subs/opensubs | open-subs/opensubs live, not archived, pushed 2026-10-08, API AGPL-3.0 | LICENSE (AGPL v3 text) | CONFIRMED AGPL-3.0 |
| 202 | ProjectX | sourceforge.net/projects/project-x live (registered 2004-07-21) | sf_project_page.html — license field "GNU General Public License version 2.0 (GPLv2)" | CONFIRMED GPL-2.0 |
| 203 | CasparCG Server | CasparCG/server live, not archived, pushed 2026-09-30, API GPL-3.0 | LICENSE (GPL v3 29 June 2007) | CONFIRMED GPL-3.0 |
| 204 | dvbsnoop | no official repo; 3 independent mirrors all API GPL-2.0 (cotdp pushed 2026-10-07) | api_*.json per mirror | CONFIRMED GPL-2.0 (mirrors agree) |
| 205 | Calamari OCR | Calamari-OCR/calamari live, not archived, pushed 2026-06-23, API GPL-3.0 | LICENSE (GPL v3 29 June 2007) | CONFIRMED GPL-3.0 |

Zero relicensing events, zero delists, zero supersedes, zero new rows, zero
duplicates. `docs/LICENSE_QUARANTINE.md` updated append-only with
"(re-verified Wave 39 Lane B, 2026-10-08: …)" notes on all 10 rows, and the
manifest header carries the cycle-10 note. Header counts unchanged:
294 rows · 271 distinct.

### Manual review note (row 145, Bento4)
The mechanical tool returned NEEDS REVIEW because Bento4 ships no root LICENSE
file — unchanged from the Wave-15/21 findings. Resolved by direct reads: the
per-file header grant in `Ap4File.h` ("either version 2, or (at your option)
any later version" under Bento4|GPL) and the README "License" section
("dual-license model", commercial tier via bento4.com About page). Dual
GPL-2.0-or-later / commercial stands; quarantine unaffected.

## Identity-drift watch (fresh vs prior-wave snapshots)

- **Helm (row 68):** mtytel/helm STILL owner-archived — pushed
  2022-09-24T04:23:20Z, ownership unchanged (mtytel), API spdx_id GPL-3.0.
  Top forks by stars: DatanoiseTV/helm (6★, stale 2020-11), poweraudio/helm
  (3★, pushed 2024-09-08), mekayama/helm (2★, stale 2015), AJ-Gonzalez/
  helm-apple-silicon (2★, pushed 2026-09-21 — freshest recurring maintenance
  fork), rockola/helm (2★, stale 2019). No official successor, no ownership
  change, no relicense. Evidence: `drift_watch_github.json`.
- **telxcc (row 236):** kanongil/telxcc STILL archived — pushed
  2025-09-20T11:29:10Z, ownership unchanged (kanongil), API spdx_id NOASSERTION
  (detection gap; raw LICENSE still the GPL-2.0-or-later boilerplate per prior
  waves). Top forks: braincoded/telxcc (1★, stale 2014), xylographe/telxcc
  (0★, pushed 2026-03-17 — most recent fork activity), carlanton/teletext-ingest
  (0★, 2017). No standout successor, no relicense. Evidence:
  `drift_watch_github.json`.
- **MKVToolNix (row 155):** codeberg.org/mbunkus/mkvtoolnix HTTP 200; Codeberg
  COPYING = GPL v2 June 1991 text (18,092 bytes); Codeberg API: owner mbunkus,
  not archived, default branch main. No further host moves, no relicense;
  GPL-2.0-or-later composite stands. Evidence: `drift_mkvtoolnix_page.html`,
  `drift_mkvtoolnix_COPYING`, `drift_watch_codeberg.json`.
- **codeberg.org/uzu/tidal** (TidalCycles successor, per row 101): HTTP 200;
  LICENSE = GPL v3 29 June 2007 text (35,106 bytes); Codeberg API: owner uzu,
  not archived, default branch main, 281 stars. Active, no relicense.
  Evidence: `drift_uzu_tidal_LICENSE`, `drift_watch_codeberg.json`.
