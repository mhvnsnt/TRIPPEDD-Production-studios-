# Wave 60 Lane B — re-verification cycle 31 report (2026-10-08)

Scope: docs/LICENSE_QUARANTINE.md rows 321–330 (the 10 oldest live rows with bare-date
"(verified Wave 38 Lane A, 2026-10-08)" annotations and no wave-era re-verification stamp),
plus standing drift watch (Helm, telxcc, MKVToolNix COPYING, uzu/tidal LICENSE, MB-Lab,
SubDownloader, MPC-HC, ScanTailor, Strudel, subSync).

## Environment notes
- VM egress proxy was DOWN for this entire lane (hatch-egress-proxy:3128 connection refused;
  curl/gh/got all failed). All upstream verification ran through the browser-tool channel
  (GitHub API, Codeberg API, raw.githubusercontent, GitHub repo-details crawl) — full
  evidence, no assumptions.
- Disk was 100% full at lane start (64K free); purged regenerable pip caches (~4.1 GB freed).
  Documented here per the disk cleanup law; nothing user-owned was touched.

## Result: 10/10 CONFIRMED — zero relicenses, zero delists, zero supersedes, zero repo moves

| Row | Project (owner/repo) | Claimed | Verified | Evidence |
|-----|----------------------|---------|----------|----------|
| 321 | Firebot (crowbartools/Firebot) | GPL-3.0 | GPL-3.0 | API spdx_id; live, not archived, pushed 2026-10-08T13:43:02Z |
| 322 | Twitchat (Durss/Twitchat) | GPL-3.0 | GPL-3.0 | API spdx_id; live, not archived, pushed 2026-10-07T17:08:53Z |
| 323 | Imaginary Teleprompter (ImaginarySense/Imaginary-Teleprompter) | GPL-3.0 | GPL-3.0 | API spdx_id (evidence upgraded from Wave-38 README statement); live, pushed 2022-02-19 |
| 324 | Transparent-Twitch-Chat-Overlay (baffler/Transparent-Twitch-Chat-Overlay) | GPL-3.0 | GPL-3.0 | Direct API fetch hit transient 403; verified via GitHub repo-details crawl: License field "GNU General Public License v3.0 (GPL-3.0)", public, not archived, not forked; README badge → raw LICENSE |
| 325 | tvheadend (tvheadend/tvheadend) | GPL-3.0 | GPL-3.0 | API spdx_id; live, not archived, pushed 2026-10-08T18:12:14Z |
| 326 | MythTV (MythTV/mythtv) | GPL-2.0 | GPL-2.0 | API spdx_id; live, not archived, pushed 2026-10-01T20:31:55Z |
| 327 | Jellyfin (jellyfin/jellyfin) | GPL-2.0 | GPL-2.0 | API spdx_id; live, not archived, pushed 2026-10-08T18:29:31Z |
| 328 | Kodi (xbmc/xbmc) | GPL-2.0-or-later | GPL-2.0-or-later | API NOASSERTION detection gap persists (known); resolved by direct raw read: master/LICENSE.md "SPDX-License-Identifier: GPL-2.0-or-later"; live, pushed 2026-10-08T17:25:47Z |
| 329 | OvenMediaEngine (OvenMediaLabs/OvenMediaEngine) | AGPL-3.0 | AGPL-3.0 | API spdx_id; live, not archived, pushed 2026-10-08T15:03:46Z; owner still OvenMediaLabs (AirenSoft move note intact) |
| 330 | Janus (meetecho/janus-gateway) | GPL-3.0 | GPL-3.0 | API spdx_id; live, not archived, pushed 2026-10-06T13:19:18Z |

- Detection gaps resolved: 1 NOASSERTION by direct text read (328); 1 transient 403 via alternate evidence path (324).
- No canonical-URL moves → no docs/RESOURCE_CATALOG.md changes needed.

## Drift watch: 10/10 clean (vs cycle 30)
- Helm (68) mtytel/helm — STILL owner-archived, pushed 2022-09-24T04:23:20Z, owner mtytel, spdx GPL-3.0
- telxcc (236) kanongil/telxcc — STILL archived, pushed 2025-09-20T11:29:10Z, owner kanongil, API NOASSERTION
- MKVToolNix (155) codeberg.org/mbunkus/mkvtoolnix — canonical, NOT archived, updated 2026-09-28; raw COPYING **18,092 bytes — BYTE-IDENTICAL**
- uzu/tidal (101) codeberg.org/uzu/tidal — live, NOT archived, updated 2026-07-02; raw LICENSE **35,106 bytes — BYTE-IDENTICAL**
- MB-Lab (118) animate1978/MB-Lab — STILL owner-archived, pushed 2024-07-21T02:46:17Z
- SubDownloader (195) subdownloader/subdownloader — STILL archived, pushed 2025-02-05T11:39:33Z, spdx GPL-3.0
- MPC-HC (191) mpc-hc/mpc-hc — STILL archived, pushed 2020-04-24T11:04:40Z, spdx GPL-3.0
- ScanTailor (206) scantailor/scantailor — STILL archived, pushed 2020-11-29T04:31:29Z
- Strudel (243) tidalcycles/strudel — STILL archived, pushed 2025-06-19T15:56:31Z, owner tidalcycles, spdx AGPL-3.0
- subSync (253) sc0ty/subSync — STILL owner-archived, pushed 2024-10-01T13:47:06Z, spdx GPL-3.0
- No ownership changes, no relicenses, no successors anywhere on the watch list.

## Changes made (this lane)
- docs/LICENSE_QUARANTINE.md: rows 321–330 stamped "+ re-verified Wave 60 Lane B,
  2026-10-08 (cycle 31: 10/10 confirmed, zero relicenses)" with per-row dated evidence.
- docs/LICENSE_QUARANTINE.md: added "Wave 60 Lane B re-verification cycle (2026-10-08):
  THIRTY-FIRST re-verification cycle" blockquote with full evidence summary + drift watch.
- Header counts unchanged: 576 rows · 550 distinct (zero row additions/removals/delists).
- LGPL doctrine still PENDING OWNER VERDICT — untouched by this lane.
