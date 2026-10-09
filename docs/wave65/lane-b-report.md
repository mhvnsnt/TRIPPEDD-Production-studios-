# WAVE 65 — LANE B — Re-verification cycle 36 report

Date: 2026-10-08 (lane: w65b, branch wave65-lane-b, base origin/main 1aa9dbe3)
Scope: rows 371–380 of docs/LICENSE_QUARANTINE.md (broadcast/caption/tracker pocket, last verified Wave 40/41 Lane A, 2026-10-08) + identity-drift watch list.

NOTE ON SCOPE: the task brief said "rows 371–380 of docs/RESOURCE_CATALOG.md"; RESOURCE_CATALOG.md has no numbered rows — the numbered-row convention across Wave 62–64 Lane B reports (cycles 33/34/35: rows 341–350, 351–360, 361–370) is the LICENSE_QUARANTINE.md numbered table, and the previous cycle ended at row 370. Continuing with quarantine rows 371–380 as the established convention.

## Result: 10/10 rows CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes. 2 URL-drift annotations (rows 374, 378).

## Per-row evidence (fresh 2026-10-08, ~20:25–20:55 CDT)

### Row 371 — XMLTV (XMLTV/xmltv) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-06-22T15:48:22Z, default branch master. Active, no relicense, no repo-move.

### Row 372 — OpenCaster (aventuri/opencaster) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2024-05-04T11:14:33Z, default branch master. Dormant but unchanged since Wave 40. No relicense, no repo-move.

### Row 373 — Kainote (bjakja/Kainote) — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2026-09-26T10:08:36Z, default branch master. Active, no relicense, no repo-move.

### Row 374 — PgcEdit (r0lz/pgcedit) — GPL ⚠️ URL DRIFT (license confirmed via homepage) ✅
- GitHub API: r0lz/pgcedit returns **404**. Owner account gone/renamed — `users/r0lz` now resolves to `r0lZ` with 0 public repos. The GitHub mirror is dead.
- License still confirmed at canonical evidence path: official homepage https://download.videohelp.com/r0lz/pgcedit/ still states **"PgcEdit is free and open source (GPL license)"** (fresh search 2026-10-08).
- Project itself ACTIVE: current version v9.5 released 2025-10-25. NOT delisted, NOT relicensed, NOT superseded.
- Row annotation updated honestly (mirror-deletion note + homepage re-verification stamp). No quarantine row filed — license claim unchanged, project live.

### Row 375 — xmodits (B0ney/xmodits) — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2024-08-26T20:04:02Z, default branch ver-0.12.1. No relicense, no repo-move.

### Row 376 — CheeseCutter (theyamo/CheeseCutter) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-03-29T08:44:52Z, default branch master. Active, no relicense, no repo-move.

### Row 377 — TIATracker (steux/tiatracker) — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2024-02-08T16:43:56Z, default branch master. No relicense, no repo-move.

### Row 378 — komposter (jhalme/komposter → electronoora/komposter) — GPL-2.0 ⚠️ REPO-MOVED ✅
- GitHub API on jhalme/komposter returns **301 Moved Permanently** → repositories/32145666 = **electronoora/komposter**. Owner renamed; old path dead.
- License on new path: spdx_id **GPL-2.0**, archived=false, pushed 2020-12-21T14:36:11Z (last commit predates the move — content unchanged).
- Row header + annotation updated to electronoora/komposter honestly. NOT delisted, NOT relicensed, NOT superseded.

### Row 379 — superkabuki/threefive_is_scte35 — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed **2026-10-08T06:09:27Z** (today), default branch main. Active, no relicense, no repo-move.

### Row 380 — futzu/umzz — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2024-07-15T20:43:32Z, default branch main. No relicense, no repo-move.

## Row annotations changed
- Row 374: GitHub mirror deletion + homepage re-verification stamp.
- Row 378: owner path jhalme/komposter → electronoora/komposter + re-verification stamp.
- Zero row additions/removals, zero duplicates touched, zero quarantine rows filed.

## Notes
- LGPL doctrine still PENDING OWNER VERDICT — no GPL rows in this cycle are affected; this lane does not decide it (facts-only verification).
- PgcEdit is the first cycle where a cataloged GitHub mirror vanished while the project lives on: the row's license evidence was always the homepage, so the claim survived; the mirror path is now dead bystander info.

## Identity-drift watch (fresh 2026-10-08, ~20:40–20:50 CDT)

| Row | Repo | Status |
|---|---|---|
| 68 | mtytel/helm | STILL owner-archived — pushed 2022-09-24T04:23:20Z unchanged, spdx GPL-3.0, owner mtytel unchanged. No successor, no relicense. |
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
Unchanged by this lane (no rows added/removed): counts per latest coordinator refresh stand.
