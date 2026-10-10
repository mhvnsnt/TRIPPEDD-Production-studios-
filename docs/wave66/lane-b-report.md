# WAVE 66 — LANE B — Re-verification cycle 37 report

Date: 2026-10-08 (lane: w66b, branch wave66-lane-b, base origin/main 8ad05825)
Scope: rows 381–390 of docs/LICENSE_QUARANTINE.md (broadcast/VANC/caption/retro-devkit pocket; last verified Wave 41/42 Lane A, 2026-10-08) + identity-drift watch list.

NOTE ON SCOPE: the task brief said "rows 381–390 of docs/RESOURCE_CATALOG.md"; RESOURCE_CATALOG.md has no numbered rows — the numbered-row convention across Wave 62–66 Lane B reports (cycles 33/34/35/36: rows 341–350, 351–360, 361–370, 371–380) is the LICENSE_QUARANTINE.md numbered table, and the previous cycle ended at row 380. Continuing with quarantine rows 381–390 as the established convention. (The quarantine table is docs/LICENSE_QUARANTINE.md — the brief's old RESOURCE_QUARANTINE.md name does not exist; nothing created.)

## Result: 10/10 rows CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes. 1 archiving-drift annotation (row 388).

## Per-row evidence (fresh 2026-10-08, ~21:25–21:55 CDT)

### Row 381 — stoth68000/libklvanc — LGPL-2.1 ✅ CONFIRMED
- GitHub API: spdx_id None (still — the known detection gap; repo has no LICENSE root key, uses `lgpl-2.1.txt`), archived=false, pushed 2026-09-23T10:31:32Z, branch master. Active.
- Raw fetch: `lgpl-2.1.txt` @ master = **26,530 B**, canonical "GNU LESSER GENERAL PUBLIC LICENSE / Version 2.1, February 1999" text (header check passes, sha256 4fbd65380cdd255951079008b364516c). LGPL-2.1 stands.

### Row 382 — stoth68000/klvanc-tools — LGPL-2.1 ✅ CONFIRMED
- GitHub API: spdx_id None (same org detection gap), archived=false, pushed 2024-07-08T20:31:18Z, branch master.
- Raw fetch: `lgpl-2.1.txt` @ master = 26,530 B, **byte-identical** (sha256 4fbd6538…) to the libklvanc copy, canonical LGPL 2.1 text. LGPL-2.1 stands.

### Row 383 — grahowe/EAS-Tools-Decoder — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2026-02-28T01:45:24Z, branch main. No relicense, no repo-move.

### Row 384 — opensteno/plover — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-09-20T13:33:20Z, branch main. Canonical path opensteno/plover live. No relicense, no repo-move.

### Row 385 — uli/huc — Mixed ✅ CONFIRMED
- GitHub API: spdx_id NOASSERTION (matches Mixed; repo has no single SPDX), archived=false, pushed 2022-08-02T22:10:59Z, branch master.
- Root `LICENSE` file re-read verbatim: MagicKit assembler "freeware" statement · TGEmu licensed under GNU Public License (v2 text confirmed at tgemu/src/license) · GCC-derived test cases GPL · Ulrich Hecht changes BSD-2-Clause. Matches the row's Mixed claim exactly — no drift.

### Row 386 — OpenOrbis/OpenOrbis-PS4-Toolchain — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2026-02-27T10:58:14Z, branch master. No relicense, no repo-move.

### Row 387 — Halofreak1990/OpenXDK — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2016-08-15T22:43:43Z, branch master. Dormant but unchanged. No relicense, no repo-move.

### Row 388 — rust-wiiu/wut — GPL-3.0 ⚠️ ARCHIVING DRIFT (license confirmed) ✅
- GitHub API: spdx_id GPL-3.0, **archived=True**, pushed 2025-06-23T20:25:46Z, branch main.
- License claim intact — GPL-3.0 stands. The Wave 41 Lane A annotation did not record archive status, so the archive's age is unknown (cannot distinguish "archived before Wave 41" from "newly archived"); flagging it now as a URL-drift-class annotation honestly. No successor declared (description: "Wii U Toolchain (WUT) bindings & API", no homepage). NOT delisted, NOT relicensed, NOT superseded.

### Row 389 — BrunoRNS/SNES-IDE — GPL-3.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-3.0, archived=false, pushed 2025-11-17T20:34:19Z, branch main. No relicense, no repo-move.

### Row 390 — catalinii/minisatip — GPL-2.0 ✅ CONFIRMED
- GitHub API: spdx_id GPL-2.0, archived=false, pushed 2026-10-09T01:56:28Z (today), branch master. Active.

## Row annotations changed
- Rows 381–390: re-verification stamps appended (history untouched).
- Row 388: new archiving-drift annotation.
- Zero row additions/removals, zero duplicates touched, zero quarantine rows filed.

## Notes
- LGPL doctrine still PENDING OWNER VERDICT — rows 381/382 LGPL-2.1 facts verified only; both stay quarantined; this lane does not decide it.
- Row 388 (rust-wiiu/wut) is the first cycle where the archived-flag appeared without prior annotation: the Wave-41 record neither asserted nor denied archive status, so honest reporting is "newly noted," not "newly archived."

## Identity-drift watch (fresh 2026-10-08, ~21:40–21:55 CDT) — 11/11 clean

| Row | Repo | Status |
|---|---|---|
| 68 | mtytel/helm | STILL owner-archived — pushed 2022-09-24T04:23:20Z unchanged, spdx GPL-3.0. No successor, no relicense. |
| 236 | kanongil/telxcc | STILL archived — pushed 2025-09-20T11:29:10Z unchanged, spdx NOASSERTION. No relicense. |
| 118 | animate1978/MB-Lab | STILL archived — pushed 2024-07-21T02:46:17Z unchanged, spdx NOASSERTION. No relicense. |
| 195 | subdownloader/subdownloader | STILL archived — pushed 2025-02-05T11:39:33Z unchanged, spdx GPL-3.0. No relicense. |
| 191 | mpc-hc/mpc-hc | STILL owner-archived — pushed 2020-04-24T11:04:40Z unchanged, spdx GPL-3.0. No relicense. |
| 206 | scantailor/scantailor | STILL archived — pushed 2020-11-29T04:31:29Z unchanged, spdx NOASSERTION. No relicense. |
| 243 | tidalcycles/strudel | STILL archived — pushed 2025-06-19T15:56:31Z unchanged, spdx AGPL-3.0. No relicense. |
| 253 | sc0ty/subSync | STILL archived — pushed 2024-10-01T13:47:06Z unchanged, spdx GPL-3.0. No relicense. |
| 155 | MKVToolNix | Canonical codeberg.org/mbunkus/mkvtoolnix, NOT archived (pushed 2026-09-28). COPYING = GPL v2 June 1991 text, **18,092 bytes byte-identical** ✅ (sha256 8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643). No host moves, no relicense. FETCH-PATH NOTE: Codeberg default branch is now `main` (was master in earlier wave tooling); `.../raw/branch/master/...` 404s — use `main`. |
| 101 | uzu/tidal | codeberg.org/uzu/tidal active, NOT archived. LICENSE = GPL v3 29 June 2007 text, **35,106 bytes byte-identical** ✅ (sha256 804821a9171f6eb0e0d26635922480bf479c2d646c2609f6273a85191949b8df). No relicense. |
| 294 | openbroadcaster/obplayer | Canonical path intact — active, pushed 2026-09-23T04:21:06Z, spdx AGPL-3.0. No relicense, no further moves. |

## Header counts
Unchanged by this lane (no rows added/removed): counts per latest coordinator refresh stand.
