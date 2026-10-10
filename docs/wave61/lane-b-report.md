# WAVE 61 — Lane B report (re-verification cycle 32)

Date: 2026-10-08 · Lane B · worktree `~/workspace/agent-ops/wave61-lanes/w61b` · branch `wave61-lane-b`

## Scope
Cycle 32 = rows 331–340 of `docs/LICENSE_QUARANTINE.md` (the next 10 oldest never-reverified rows), verified LIVE upstream on 2026-10-08. Each row was re-checked against the live upstream license source — GitHub API `spdx_id`, raw license file, or (for NOASSERTION/null detection gaps) a direct read of the license text. Zero assumption.

## Rows verified: 10/10 — zero relicenses, zero delists, zero supersedes

| Row | Project (upstream) | License | Live evidence (2026-10-08) |
|-----|--------------------|---------|----------------------------|
| 331 | voctoweb (voc/voctoweb) | GPL-3.0 | GitHub API spdx_id `GPL-3.0`; live, not archived, pushed 2026-10-06T06:25:45Z |
| 332 | voctopublish (voc/voctopublish) | GPL-3.0 | GitHub API spdx_id `GPL-3.0`; live, not archived, pushed 2026-09-15T06:41:17Z |
| 333 | VoxForge (voxforge.org) | GPL | Site live (HTTP 200); front page still carries the exact Wave-38 statement: "We will make available all submitted audio files under the GPL license, and then 'compile' them into acoustic models for use with Open Source speech recognition engines" |
| 334 | libsndfile (libsndfile/libsndfile) | LGPL-2.1 | GitHub API spdx_id `LGPL-2.1`; live, not archived, pushed 2026-09-01T09:08:12Z |
| 335 | JACK2 (jackaudio/jack2) | GPL-2.0 | GitHub API spdx_id `GPL-2.0`; live, not archived, pushed 2026-01-07T21:37:45Z |
| 336 | ChucK (ccrma/chuck) | GPL-2.0 | GitHub API spdx_id `GPL-2.0`; live, not archived, pushed 2026-07-10T19:10:37Z |
| 337 | KFR (kfrlib/kfr) | GPL-2.0 | GitHub API spdx_id `GPL-2.0`; live, not archived, pushed 2026-10-08T11:22:13Z |
| 338 | FAAD2 (knik0/faad2) | GPL-2.0 | GitHub API `NOASSERTION` (detection gap persists) → resolved by raw COPYING: "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991" + "Any non-GPL usage of this software or parts of this software is strictly forbidden." Live, not archived, pushed 2026-10-01T15:59:45Z |
| 339 | HISE (christophhart/HISE) | GPL-3.0 | GitHub API `NOASSERTION` (detection gap persists) → resolved by raw README license section: "HISE is licensed under the GPL v3". Live, not archived, pushed 2026-10-05T09:54:07Z |
| 340 | pygame (pygame/pygame) | LGPL-2.1 | GitHub API license `null` (detection gap) → resolved by raw `docs/LGPL.txt`: "GNU LESSER GENERAL PUBLIC LICENSE / Version 2.1, February 1999". Live, not archived, pushed 2025-11-01T03:05:13Z |

All 10 rows stamped with dated cycle-32 notes in the license cell; quarantine status on every row remains **PENDING** (no change).

## Drift watch — all 13 items checked live 2026-10-08, NO CHANGE

All still owner-archived with unchanged pushed_at / owner / spdx (except piper1-gpl, which is active — unchanged from baseline):

| Item | Row | Status this cycle |
|------|-----|-------------------|
| Helm | 68 | mtytel/helm STILL owner-archived (pushed 2022-09-24T04:23:20Z — unchanged, owner mtytel); API spdx_id GPL-3.0; no successor, no ownership change, no relicense |
| telxcc | 236 | kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z — unchanged, owner kanongil); API NOASSERTION; raw LICENSE 2,091 bytes BYTE-IDENTICAL, "-or-later" boilerplate intact |
| MB-Lab | 118 | animate1978/MB-Lab STILL owner-archived (pushed 2024-07-21T02:46:17Z — unchanged, owner animate1978); API NOASSERTION; license.txt 3,519 bytes BYTE-IDENTICAL, GPL-3.0 grant intact |
| SubDownloader | 195 | subdownloader/subdownloader STILL owner-archived (pushed 2025-02-05T11:39:33Z — unchanged, owner subdownloader); API spdx_id GPL-3.0 |
| MPC-HC | 191 | mpc-hc/mpc-hc STILL owner-archived (pushed 2020-04-24T11:04:40Z — unchanged, owner mpc-hc); API spdx_id GPL-3.0 |
| ScanTailor | 206 | scantailor/scantailor STILL owner-archived (pushed 2020-11-29T04:31:29Z — unchanged, owner scantailor); API NOASSERTION; raw COPYING 464 bytes BYTE-IDENTICAL |
| Strudel | 243 | tidalcycles/strudel STILL owner-archived (pushed 2025-06-19T15:56:31Z — unchanged, owner tidalcycles); API spdx_id AGPL-3.0 |
| subSync | 253 | sc0ty/subSync STILL owner-archived (pushed 2024-10-01T13:47:06Z — unchanged, owner sc0ty); API spdx_id GPL-3.0 |
| piper1-gpl | 20 | OHF-Voice/piper1-gpl live, NOT archived, pushed 2026-10-06T21:23:53Z (active); API GPL-3.0; README "Looking for Maintainers" banner still present — watch item persists |
| so-vits-svc | 24 | svc-develop-team/so-vits-svc STILL archived (pushed 2023-11-11T13:11:31Z — unchanged, owner svc-develop-team); API spdx_id AGPL-3.0 |
| Seed-VC | 43 | Plachtaa/seed-vc STILL owner-archived (pushed 2025-04-20T05:27:10Z — unchanged, owner Plachtaa); API spdx_id GPL-3.0 |
| MKVToolNix | 155 | codeberg.org/mbunkus/mkvtoolnix still canonical, owner mbunkus, not archived, updated 2026-09-28; raw COPYING on branch main = GPL v2 June 1991 text, **18,092 bytes — BYTE-IDENTICAL** to all prior checks |
| uzu/tidal | 101 | codeberg.org/uzu/tidal still live, owner uzu, not archived, updated 2026-07-02; raw LICENSE on branch main = GPL v3 text, **35,106 bytes — BYTE-IDENTICAL** to all prior checks; tidalcycles/Tidal still archived |

All 13 drift rows carry new `(drift watch Wave 61 Lane B, 2026-10-08: …)` notes (append-only; original numbering retained).

## Files changed
- `docs/LICENSE_QUARANTINE.md` — 10 cycle-32 row stamps + 13 drift-watch notes
- `docs/wave61/lane-b-report.md` — this report

No binaries added; no rows added/removed; no license-family changes; LGPL doctrine still PENDING OWNER VERDICT.
