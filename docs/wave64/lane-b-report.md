# WAVE 64 — LANE B — Re-verification cycle 35 report

Date: 2026-10-08 (lane: w64b, branch wave64-lane-b, base origin/main d3711177)
Scope: rows 361–370 of docs/LICENSE_QUARANTINE.md (broadcast pocket, last verified Wave 40 Lane A, 2026-10-08) + identity-drift watch list.

## Result: 10/10 rows CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes, zero repo-moves.

## Per-row evidence (fresh 2026-10-08, ~19:10–19:25 CDT)

### Row 361 — multimon-ng (EliasOenal/multimon-ng) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-09-27T05:36:57Z, default branch master. Active, no relicense, no repo-move.

### Row 362 — DVBlast (videolan/dvblast) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-06-15T12:57:04Z, default branch master. Active (canonical VideoLAN project; code.videolan.org mirror also live). No relicense, no repo-move.

### Row 363 — MuMuDVB (braice/MuMuDVB) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-09-13T13:35:25Z, default branch mumudvb2. Active, no relicense, no repo-move.

### Row 364 — VDR (vdr-projects/vdr) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-10-05T12:30:31Z (3 days ago), default branch master. Row notes upstream git.tvdr.de — GitHub mirror live and consistent. No relicense, no repo-move.

### Row 365 — Astra-4 (cesbo/astra-4) — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=true (owner-archived, unchanged), pushed 2019-07-26T06:58:09Z, default branch astra-4. Still archived as the row claims ("research/reference only"). No relicense, no successor, no ownership change.

### Row 366 — ODR-DabMux (opendigitalradio/ODR-DabMux) — GPL-3.0 ✅ CONFIRMED
- GitHub API: archived=false, pushed 2026-06-17T12:22:48Z, default branch master, license **NOASSERTION** (detection gap, same class as munt wave 62).
- Gap resolved via direct text read: `COPYING` = **35,147 bytes**, opens "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007" — GPL-3.0 confirmed, consistent with row claim.
- No relicense, no repo-move, no archive.

### Row 367 — Superdesk (superdesk/superdesk) — AGPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id AGPL-3.0, archived=false, pushed 2026-10-06T08:44:52Z (2 days ago), default branch develop. Active, no relicense, no repo-move.

### Row 368 — Newscoop (sourcefabric/Newscoop) — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2018-07-10T07:26:15Z, default branch v4.4. Dormant but unchanged since Wave 40. No relicense, no archive, no repo-move.

### Row 369 — Icecast (xiph/Icecast-Server) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-08-19T16:47:41Z, default branch master. Active, no relicense, no repo-move.

### Row 370 — DVBInspector (EricBerendsen/dvbinspector) — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2026-05-28T18:34:56Z, default branch master. Active, no relicense, no repo-move.

## Notes
- LGPL doctrine still PENDING OWNER VERDICT — no GPL rows in this cycle are affected; this lane does not decide it (facts-only verification).
- Zero row additions/removals, zero duplicates touched.
- licenseURL notes: none needed — all upstreams resolve at their recorded hosts/repos. VDR's git.tvdr.de primary is noted in the row already; the vdr-projects/vdr GitHub mirror is the verified secondary path.

## Identity-drift watch (fresh 2026-10-08)

| Row | Repo | Status |
|---|---|---|
| 68 | mtytel/helm | STILL owner-archived — pushed 2022-09-24T04:23:20Z unchanged, spdx GPL-3.0. No successor, no ownership change, no relicense. |
| 236 | kanongil/telxcc | STILL archived — pushed 2025-09-20T11:29:10Z unchanged, spdx NOASSERTION. No relicense. |
| 118 | animate1978/MB-Lab | STILL archived — pushed 2024-07-21T02:46:17Z unchanged, spdx NOASSERTION. No relicense. |
| 195 | subdownloader/subdownloader | STILL archived — pushed 2025-02-05T11:39:33Z unchanged, spdx GPL-3.0. No relicense. |
| 191 | mpc-hc/mpc-hc | STILL owner-archived — pushed 2020-04-24T11:04:40Z unchanged, spdx GPL-3.0. No relicense. |
| 206 | scantailor/scantailor | STILL archived — pushed 2020-11-29T04:31:29Z unchanged, spdx NOASSERTION. No relicense. |
| 243 | tidalcycles/strudel | STILL archived — pushed 2025-06-19T15:56:31Z unchanged, spdx AGPL-3.0. No relicense. |
| 253 | sc0ty/subSync | STILL archived — pushed 2024-10-01T13:47:06Z unchanged, spdx GPL-3.0. No relicense. |
| 155 | MKVToolNix | Canonical codeberg.org/mbunkus/mkvtoolnix, NOT archived. COPYING = GPL v2 June 1991 text, **18,092 bytes byte-identical** ✅ (sha256 8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643). No host moves, no relicense. |
| 101 | uzu/tidal | codeberg.org/uzu/tidal active, NOT archived. LICENSE = GPL v3 29 June 2007 text, **35,106 bytes byte-identical** ✅ (sha256 804821a9171f6eb0e0d26635922480bf479c2d646c2609f6273a85191949b8df). No relicense. |

## Header counts
Unchanged by this lane (no rows added/removed): counts per latest refresh stand.
