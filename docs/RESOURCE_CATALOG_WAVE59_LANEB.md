# Wave 59 Lane B re-verification outputs

Lane-scoped re-verification sections, assembled by the coordinator into `docs/RESOURCE_CATALOG.md` / `docs/LICENSE_QUARANTINE.md`. Lane B never edits those files directly.

### Wave 59 Lane B summary (2026-10-08)

THIRTIETH re-verification cycle — rows 311–320 (the NEXT 10 lowest-numbered live rows with bare-date "(verified Wave 38 Lane A, 2026-10-08)" annotations and no wave-era re-verification stamp). Fresh upstream checks via `gh api` (authenticated, spdx_id + archived + pushed_at + owner) and direct raw LICENSE-text fetches (byte counts + text heads — never assumed; SourceForge project license field for the SourceForge-only row):

| Row # | Project | Result | Evidence |
|---|---|---|---|
| 311 | CinePaint (SourceForge) | CONFIRMED — GPL-2.0 stands | SourceForge project page license field still "GNU General Public License version 2.0 (GPLv2)" (2026-10-08; fetch + SF REST check) |
| 312 | VDO.Ninja (steveseguin/vdo.ninja) | CONFIRMED — AGPL-3.0 stands | Live, not archived, pushed 2026-10-07; API spdx_id AGPL-3.0; raw LICENSE (33,893 bytes) = AGPL v3 text |
| 313 | obs-websocket (obsproject/obs-websocket) | CONFIRMED — GPL-2.0 stands | Live, not archived, pushed 2026-10-07; API spdx_id GPL-2.0; raw LICENSE (18,045 bytes) = GPL v2 June 1991 text |
| 314 | DistroAV (DistroAV/DistroAV) | CONFIRMED — GPL-2.0 stands | Live, not archived, pushed 2026-10-07; API spdx_id GPL-2.0; raw LICENSE (18,045 bytes) = GPL v2 June 1991 text |
| 315 | StreamFX (Vhonowslend/StreamFX-Public) | CONFIRMED — GPL-2.0 stands | Live, not archived, pushed 2024-12-13; API spdx_id GPL-2.0; raw LICENSE (15,087 bytes) = GPL v2 June 1991 text; Xaymar→Vhonowslend rename still intact (redirect target live) |
| 316 | obs-move-transition (exeldro/obs-move-transition) | CONFIRMED — GPL-2.0 stands | Live, not archived, pushed 2026-10-04; API spdx_id GPL-2.0; raw LICENSE (18,092 bytes) = GPL v2 June 1991 text |
| 317 | obs-source-record (exeldro/obs-source-record) | CONFIRMED — GPL-2.0 stands | Live, not archived, pushed 2026-07-05; API spdx_id GPL-2.0; raw LICENSE (18,092 bytes) = GPL v2 June 1991 text |
| 318 | LibreTime (libretime/libretime) | CONFIRMED — AGPL-3.0 stands | Live, not archived, pushed 2026-10-08; API spdx_id AGPL-3.0; raw LICENSE (34,523 bytes) = AGPL v3 text |
| 319 | ffplayout (ffplayout/ffplayout) | CONFIRMED — GPL-3.0 stands | Live, not archived, pushed 2026-10-04; API spdx_id GPL-3.0; raw LICENSE (35,149 bytes) = GPL v3 text |
| 320 | Xibo (xibosignage/xibo-cms) | CONFIRMED — AGPL-3.0 stands | Live, not archived, pushed 2026-10-08; API spdx_id AGPL-3.0; raw LICENSE (34,501 bytes) = AGPL v3 text |

**Result: 10/10 CONFIRMED as claimed. Zero corrections, zero relicenses, zero delists, zero supersedes, zero duplicates.** No NOASSERTION/404 detection gaps this cycle — all GitHub rows returned clean spdx_ids AND their raw license texts were read directly.

#### Drift watch (2026-10-08) — all clean vs cycle 29

| Item | Row | Status |
|---|---|---|
| Helm (mtytel/helm) | 68 | CLEAN — still owner-archived; owner mtytel; pushed 2022-09-24T04:23:20Z (byte-identical to baseline) |
| telxcc (kanongil/telxcc) | 236 | CLEAN — still archived; owner kanongil; pushed 2025-09-20T11:29:10Z (unchanged) |
| MB-Lab (animate1978/MB-Lab) | 118 | CLEAN — still owner-archived; pushed 2024-07-21T02:46:17Z (unchanged) |
| SubDownloader (subdownloader/subdownloader) | 195 | CLEAN — still archived; pushed 2025-02-05T11:39:33Z (unchanged); spdx GPL-3.0 |
| MPC-HC (mpc-hc/mpc-hc) | 191 | CLEAN — still archived; pushed 2020-04-24T11:04:40Z (unchanged); spdx GPL-3.0 |
| ScanTailor (scantailor/scantailor) | 206 | CLEAN — still owner-archived; pushed 2020-11-29T04:31:29Z (unchanged) |
| Strudel (tidalcycles/strudel) | 243 | CLEAN — still owner-archived; pushed 2025-06-19T15:56:31Z (unchanged); spdx AGPL-3.0 |
| subSync (sc0ty/subSync) | 253 | CLEAN — still owner-archived; pushed 2024-10-01T13:47:06Z (unchanged); spdx GPL-3.0 |
| MKVToolNix (codeberg.org/mbunkus/mkvtoolnix) | 155 | CLEAN — still canonical (not archived); updated 2026-09-28 (unchanged); raw COPYING 18,092 bytes BYTE-IDENTICAL to all prior checks. Fetch-path note: default branch is now `main` (not `master` — `master` returns 404); COPYING content unchanged |
| uzu/tidal (codeberg.org/uzu/tidal) | 101 | CLEAN — still live, not archived; raw LICENSE 35,106 bytes BYTE-IDENTICAL to all prior checks (= GPL v3 29 June 2007 text) |
| OpenBroadcaster repo-move note | 294 | CLEAN — observer/obplayer still 404s; canonical openbroadcaster/obplayer live, not archived, pushed 2026-09-23; API spdx_id AGPL-3.0; recorded AGPL-3.0 note still accurate — no relicense |

**Drift watch: 11/11 clean. No ownership changes, no relicenses, no successors, no status flips. LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined; this lane does not decide it.**

#### Delist / supersede recommendations

None this cycle.
