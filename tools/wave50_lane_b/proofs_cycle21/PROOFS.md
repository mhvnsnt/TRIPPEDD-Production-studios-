# Wave 50 Lane B — re-verification cycle 21 + drift watch proofs

Date: 2026-10-08. Auditor: Wave 50 Lane B (lane-b checkout, branch wave50-lane-b).
Method: GitHub REST API (`/repos/{owner}/{repo}` — license.spdx_id, archived, pushed_at, owner) +
raw license-file fetch (`raw.githubusercontent.com/{repo}/HEAD/{LICENSE|COPYING|...}`) with
license-text signal detection. Codeberg API for row 155. Nothing assumed — every claim re-checked live.

## Cycle 21: 10 oldest never-re-verified live rows — 10/10 CONFIRMED

| Row | Project | Claimed | API spdx_id | Archived | Pushed | License file fetched | Verdict |
|-----|---------|---------|-------------|----------|--------|----------------------|---------|
| 207 | 4lex4/scantailor-advanced | GPL-3.0 | GPL-3.0 | no | 2023-09-13 | LICENSE = GPL v3 29 June 2007 text | CONFIRMED |
| 209 | ruven/iipsrv | GPL-3.0 | GPL-3.0 | no | 2026-10-05 | COPYING = GPL v3 29 June 2007 text | CONFIRMED |
| 210 | tify-iiif-viewer/tify | AGPL-3.0 | AGPL-3.0 | no | 2026-10-06 | LICENSE = AGPL v3 text | CONFIRMED |
| 221 | paperless-ngx/paperless-ngx | GPL-3.0 | GPL-3.0 | no | 2026-10-08 | LICENSE = GPL v3 29 June 2007 text | CONFIRMED |
| 222 | manisandro/gimagereader | GPL-3.0 | GPL-3.0 | no | 2026-09-29 | COPYING = GPL v3 29 June 2007 text | CONFIRMED |
| 223 | GNOME/ocrfeeder | GPL-3.0 | GPL-3.0 | no | 2026-09-17 | COPYING = GPL v3 29 June 2007 text | CONFIRMED |
| 227 | chnm/scripto | GPL-3.0 | None (NOASSERTION) | no | 2017-07-06 | none — README.md at HEAD: "License: [GNU GPL v3](http://www.gnu.org/licenses/gpl-3.0.txt)" | CONFIRMED (detection gap, same pattern as rows 72/73/88) |
| 229 | benwbrum/fromthepage | AGPL-3.0 | AGPL-3.0 | no | 2026-10-07 | LICENSE = AGPL v3 text | CONFIRMED |
| 230 | djvulibre/djvulibre | GPL-2.0 | GPL-2.0 | no | 2017-03-23 | COPYING = GPL "Version 2, June 1991" text (preamble's LGPL mention is not a relicense) | CONFIRMED |
| 231 | pymupdf/PyMuPDF | AGPL-3.0 | AGPL-3.0 | no | 2026-10-08 | COPYING = AGPL v3 text | CONFIRMED |

Zero relicensing events, zero delists, zero supersedes, zero repo-moves.

## Drift watch: 10 previously-flagged risky rows — 10/10 STABLE

| Row | Repo | Status |
|-----|------|--------|
| 68 | mtytel/helm | still owner-archived (pushed 2022-09-24), ownership mtytel unchanged, spdx GPL-3.0 — no successor, no drift |
| 236 | kanongil/telxcc | still archived (pushed 2025-09-20), ownership kanongil unchanged; API NOASSERTION = detection gap — GPL-2.0-or-later stands |
| 155 | codeberg.org/mbunkus/mkvtoolnix | still canonical, owner mbunkus, not archived — no host moves, no relicense |
| 195 | subdownloader/subdownloader | still owner-archived (pushed 2025-02-05), spdx GPL-3.0 — archive does not change license |
| 43 | Plachtaa/seed-vc | still owner-archived (pushed 2025-04-20), spdx GPL-3.0 — unchanged |
| 24 | svc-develop-team/so-vits-svc | still archived (pushed 2023-11-11), spdx AGPL-3.0 — unchanged |
| 103 | DISTRHO/DISTRHO-Ports | still canonical, live, not archived (pushed 2025-09-14); no further org moves |
| 42 | praat/praat.github.io | still canonical, live (pushed 2026-10-06); no redirect change — GPL-3.0-or-later stands |
| 16 | olive-editor/olive | live, not archived (pushed 2024-12-05), spdx GPL-3.0 — unchanged |
| 148 | mkiol/dsnote | live, not archived (pushed 2026-10-03, active), spdx MPL-2.0 — unchanged |

## Header counts

Independent direct recount: 467 row numbers present (1–467, no gaps); 23 dead/superseded markers
per standing convention (rows 33, 111, 174, 234 stay live); −1 aeneas rows-1+2; −1 Furnace
rows-122+271 dup → 442 distinct. **Counts UNCHANGED from Wave 49 coordinator: 467 rows · 442 distinct.**

## Artifacts

- `results.json` — cycle-21 per-row evidence (API payloads, license-file signals, SHA-256)
- `drift_results.json` — drift-watch per-row evidence
- `../../audit_cycle21.py` — cycle-21 audit script
- `../../drift_watch_cycle21.py` — drift-watch audit script
