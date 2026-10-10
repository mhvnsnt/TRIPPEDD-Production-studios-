# Wave 54 Lane B report — re-verification cycle 25 + GPL audit + drift watch

Date: 2026-10-08. Branch: `wave54-lane-b`. Worker: Lane B subagent.
Scope: quarantine table `docs/LICENSE_QUARANTINE.md` (rows 260–270 stamps + 1 correction),
catalog badge audit (LosslessCut/Avidemux/StaxRip), drift watch. `production/WIZARD_GANG_EP01/` untouched.

## Selection (cycle 25)

The next 11 oldest never-re-verified rows (the wave-53 lane-b cycle-24 range was 155, 251–259;
row 250 was covered by earlier cycles; rows 260–270 are the next live block with bare-date
"(verified 2026-10-07/08)" annotations and no wave-era re-verification stamp; 270 is the
last row with no stamp):

**260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270** (11 rows — task listed all 11 numbers)

Method: GitHub API via `gh` (authenticated; spdx_id + archived + pushed_at), GitLab API
(lazyusf2, UADE), Codeberg API (MKVToolNix, uzu/tidal), raw LICENSE/COPYING/README/DESCRIPTION
fetches, SourceForge project License fields, author's own download site (NotSo Fatso), CRAN
metadata. API NOASSERTION always treated as a detection gap and resolved by direct text reads.
Tooling: `tools/wave54_lane_b/cycle25_verify.py` (+ `cycle25_followup.py`; results in
`cycle25_results.json` / `cycle25_followup.json`), `stamp_cycle25.py`.

## Results: 10/11 CONFIRMED as claimed, 1 precision correction (row 267)

| Row | Project | Claimed | Verdict + key evidence |
|-----|---------|---------|------------------------|
| 260 | lazyusf2 | GPL-2.0-or-later | CONFIRMED — canonical GitLab `kode54/lazyusf2` (last activity 2022-03-10); no COPYING in tree (tree listing via GitLab API); per-file header `main/main.c`: "either version 2 of the License, or (at your option) any later version" |
| 261 | QMMP | GPL-2.0-or-later | CONFIRMED — canonical upstream SourceForge `qmmp-dev` (no official GitHub repo; official site qmmp.ylsoftware.com live, current release qmmp-2.4.0); SF project License field "License version 2.0 (GPLv2)"; SVN trunk/qmmp/COPYING = GPL v2 June 1991 text (18,092 bytes); trunk/qmmp/src/app/main.cpp header: "either version 2 of the License, or (at your option) any later version" |
| 262 | NotSo Fatso | GPL-2.0+ | CONFIRMED — author's site disch.zophar.net live; **direct upstream evidence**: v0.851 source tarball `Readme.txt` (Copyright (C) 2004 Disch) and per-file headers (`NSF.cpp`): "either version 2 of the License, or (at your option) any later version"; third-party corroboration: `elrinth/xmplay_gamemusic_plugin` README: "The combined plugin is GPLv2+ because NotSo Fatso is GPL-2+" |
| 263 | audapolis | AGPL-3.0 | CONFIRMED — **REPO MOVED**: `audapolis/audapolis` → `bugbakery/audapolis` (GitHub "Moved Permanently"; live, not archived, pushed 2026-06-24); API spdx_id AGPL-3.0; raw LICENSE = GNU AGPL v3 text (34,523 bytes) |
| 264 | Kaltura | AGPL-3.0 | CONFIRMED — **REPO MOVED**: `kaltura/server` now 404s on GitHub API (deleted/privatized); canonical successor `kaltura-community/server` ("The Kaltura Platform Backend", live, not archived, pushed 2024-05-17); API spdx_id AGPL-3.0; README still states "All code in this project is released under the AGPLv3 license" |
| 265 | Adlib Tracker II | GPL-3.0-or-later | CONFIRMED — `ijsf/at2` fork, live (pushed 2018-12-25); **evidence refresh**: current README carries no license statement (old README-based evidence stale); per-file header `adtrack2.pas`: "either version 3 of the License, or (at your option) any later version" |
| 266 | gbsplay | GPL-1.0-or-later | CONFIRMED — `mmitch/gbsplay` live, not archived (pushed 2026-09-28); API NOASSERTION = detection gap; root LICENCE = GNU GPL v1 February 1989 text; README "## License": "Source Code licensed under GNU GPL v1 or, at your option, any later version" |
| 267 | sc68 | GPL-2.0-or-later | **CORRECTED → GPL-3.0-or-later** — prior third-party-audit claim was wrong. Upstream evidence (2026-10-08): SourceForge project `sc68` License field "License version 3.0 (GPLv3)"; mirror `Zeinok/sc68` ("Atari ST and Amiga music player (SF Mirror)") COPYING = GPL v3 29 June 2007 text (35,147 bytes), API spdx_id GPL-3.0; `file68/src/file68.c` header: "either version 3 of the License, or (at your option) any later version". GPL family unchanged → quarantine treatment unchanged. |
| 268 | psgplay | GPL-2.0 | CONFIRMED — `frno7/psgplay` live, not archived (pushed 2026-09-08, branch `main`); sources carry `SPDX-License-Identifier: GPL-2.0` (REUSE-style `licence/` dir). Precision note: the SPDX tag leaves only/or-later ambiguous (the licence/GPL-2.0 guide lists both as valid); version 2 confirmed, which is all the quarantine needs. |
| 269 | vgmtools | GPL-2.0 | CONFIRMED — `vgmrips/vgmtools` live, not archived (pushed 2026-08-16); API spdx_id GPL-2.0; root LICENSE = GPL v2 June 1991 text (18,092 bytes, sha256 8177f975…) |
| 270 | ProTrackR2 | GPL-3.0-or-later | CONFIRMED — `pepijn-devries/protrackr2` live, not archived (pushed 2025-11-20); API spdx_id GPL-3.0 = detection gap on -or-later; DESCRIPTION field "License: GPL (>= 3)" |

**Cycle totals: 10 CONFIRMED as claimed, 1 precision-corrected (row 267 GPL-2.0-or-later →
GPL-3.0-or-later, still GPL family). Zero delists, zero supersedes, zero new rows, zero
duplicates.** All 11 stamped in the table with dated "re-verified Wave 54 Lane B, 2026-10-08"
annotations. Two repo-move notes landed (263: audapolis/audapolis → bugbakery/audapolis;
264: kaltura/server → kaltura-community/server); one evidence refresh (265: README → per-file
header).

## SPECIAL: LosslessCut / Avidemux / StaxRip GPL audit (Lane A flag from Wave 53)

Each tool's catalog entry was checked against its actual upstream license file (raw fetch, not
assumed):

| Tool | Upstream license evidence (2026-10-08) | Audit outcome |
|------|----------------------------------------|---------------|
| **LosslessCut** (`mifi/lossless-cut`) | raw LICENSE = GPL v2 June 1991 text (17,958 bytes); API spdx_id GPL-2.0; quarantine row 13 already exists (GPL-2.0-only) | **Flag VALID.** Catalog heading falsely read "✅ commercial-safe" despite the GPL license. **Corrected**: heading → "🚫 copyleft — QUARANTINED (standalone-tool use only)", added quarantine-row-13 pointer + dated correction note. Status QUARANTINED (GPL/AGPL) was already present; now consistent. |
| **Avidemux** (`mean00/avidemux2`) | raw COPYING = GPL v2 June 1991 text (18,010 bytes); API NOASSERTION = detection gap (resolved by text read); quarantine row 29 already exists (GPL-2.0) | **Flag VALID.** Same badge contradiction. **Corrected**: heading → "🚫 copyleft — QUARANTINED (standalone-tool use only)", added quarantine-row-29 pointer + dated correction note. |
| **StaxRip** (`staxrip/staxrip`) | raw License.txt = full MIT text (1,081 bytes, "Copyright (C) 2002-2026 StaxRip Authors"); API spdx_id MIT (pushed 2026-09-27) | **Flag was a FALSE POSITIVE.** StaxRip is MIT, not GPL-family. No quarantine treatment applies. **No correction** to the ✅ commercial-safe badge — added a dated MIT re-verification note to the entry closing the Wave-53 flag. |

Net catalog changes: 2 badges flipped to 🚫 with quarantine pointers (LosslessCut, Avidemux);
1 entry annotated with dated MIT re-verification (StaxRip). No quarantine-row additions needed
(LosslessCut row 13 and Avidemux row 29 already existed).

## Drift watch (2026-10-08) — all clean, no status changes

- **Helm (68)**: mtytel/helm STILL owner-archived (pushed 2022-09-24T04:23:20Z — unchanged); owner mtytel; API spdx_id GPL-3.0.
- **telxcc (236)**: kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z — unchanged); owner kanongil; API NOASSERTION.
- **MKVToolNix (155)**: codeberg.org/mbunkus/mkvtoolnix still canonical (Codeberg API 200), owner mbunkus, not archived; raw COPYING (main) = GPL v2 June 1991 text, **18,092 bytes — byte-identical to Wave 41/42/43/45/49/53 checks** (sha256 8177f975…).
- **uzu/tidal (TidalCycles successor)**: still live, not archived, owner uzu; raw LICENSE = GPL v3 text, **35,106 bytes — byte-identical to Wave 38/41/42/43/45/47/48/49/50/53 checks** (sha256 804821a9…).
- **MB-Lab (118)**: animate1978/MB-Lab STILL owner-archived (pushed 2024-07-21T02:46:17Z — unchanged); API NOASSERTION.
- **SubDownloader (195)**: subdownloader/subdownloader STILL owner-archived (pushed 2025-02-05T11:39:33Z — unchanged); API spdx_id GPL-3.0.
- **MPC-HC (191)**: mpc-hc/mpc-hc STILL owner-archived (pushed 2020-04-24T11:04:40Z — unchanged); API spdx_id GPL-3.0.
- **ScanTailor (206)**: scantailor/scantailor STILL owner-archived (pushed 2020-11-29T04:31:29Z — unchanged); API NOASSERTION.
- **Strudel (243)**: tidalcycles/strudel STILL owner-archived (pushed 2025-06-19T15:56:31Z — unchanged); API spdx_id AGPL-3.0.
- **subSync (253)**: sc0ty/subSync STILL owner-archived (pushed 2024-10-01T13:47:06Z — unchanged); API spdx_id GPL-3.0.
- **Cmajor (245)**: cmajor-lang/cmajor live, not archived (pushed 2026-10-08T09:41:22Z — active today); API NOASSERTION (detection gap — raw LICENSE.md dual GPLv3-or-later/commercial read in Wave 52).
- **UADE (257)**: gitlab.com/uade-music-player/uade, last activity 2026-09-20 (unchanged since Wave 53), branch master.
- **ASAP (259)**: sourceforge.net/projects/asap/ License field still "License version 2.0 (GPLv2)" — unchanged.

## Header counts (independent direct recount)

530 row numbers present, no gaps. 27 lines carry death markers, of which 4 stay live per standing
convention (rows 33, 111, 174, 234) → 23 dead/superseded. −1 aeneas rows-1+2, −1 Furnace rows-122+271 dup.

**530 rows · 505 distinct — matches the Wave 53 coordinator header exactly. Unchanged.**
This cycle made zero row additions/removals, zero delists, zero supersedes, and one license
precision correction inside the GPL family (row 267).

## Files changed

- `docs/LICENSE_QUARANTINE.md` — 11 cycle-25 stamps (rows 260–270), row-267 precision correction, 2 repo-move notes.
- `docs/RESOURCE_CATALOG.md` — LosslessCut + Avidemux badge flips to 🚫 with quarantine pointers; StaxRip MIT re-verification note.
- `docs/wave54/lane-b-report.md` — this report.
- `tools/wave54_lane_b/cycle25_verify.py`, `cycle25_followup.py`, `stamp_cycle25.py`, `cycle25_results.json`, `cycle25_followup.json` — tooling + raw results.

## Open items / notes for coordinator

- LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined; this lane did not decide it.
- Row 267's correction (GPL-2.0-or-later → GPL-3.0-or-later) is version-precision inside the GPL family; no family-count change. Recommend the coordinator confirm the live-row GPL-family subtotals at merge (they don't split by version, so no change expected).
- Rows 263/264 canonical upstream paths changed (audapolis → bugbakery/audapolis; kaltura/server → kaltura-community/server). Catalog cross-references for those two tools may want a URL refresh in a future pass (lane boundary — not touched).
- Rows 328–338 carry pre-existing literal-pipe anomalies (7 pipes vs 8) — verified pre-existing via git stash comparison, not from this lane. Flagging for a future table-repair pass (like the Wave-53 row-249 repair).
- The Wave-53 GPL-audit flag is fully closed: 2 valid (badges fixed), 1 false positive (StaxRip is MIT; entry annotated).
