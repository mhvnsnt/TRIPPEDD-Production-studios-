# Wave 57 Lane B — cycle 28 proofs (rows 291–300 + drift watch)

All fetched 2026-10-08 (CDT). "Never assumed" rule: every claim below rests on a
live upstream response recorded in `cycle28_raw_results.json`.

## Per-row evidence

| Row | Project | Evidence (claim → upstream) |
|-----|---------|------------------------------|
| 291 | AntennaPod | AntennaPod/AntennaPod: HTTP 200, not archived, pushed 2026-10-04T09:48:49Z, owner AntennaPod. API spdx_id GPL-3.0. Raw LICENSE (36,447 B) opens "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007". |
| 292 | BUTT | SourceForge project page (sourceforge.net/projects/butt/) license field: "License version 2.0 (GPLv2)". Author site danielnoethen.de/butt HTTP 200. |
| 293 | Rivendell | ElvishArtisan/rivendell: HTTP 200, not archived, pushed 2026-08-26T13:40:15Z. Default branch is **v4** (not master — fetch-path note). Raw LICENSES/GPLv2.txt on v4 (17,992 B, saved alongside) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991". API license null = detection gap (REUSE-style LICENSES/ dir). |
| 294 | OpenBroadcaster | **Repo move.** observer/obplayer → HTTP 404. Canonical is **openbroadcaster/obplayer**: HTTP 200, live, not archived, pushed 2026-09-23, API spdx_id AGPL-3.0. Raw COPYING (34,521 B) = "GNU AFFERO GENERAL PUBLIC LICENSE". Same project, same AGPL-3.0 — not a relicense. |
| 295 | ExifTool | exiftool/exiftool: HTTP 200, not archived, pushed 2026-05-27, owner exiftool. API spdx_id GPL-3.0. Raw LICENSE (35,149 B) = GPL v3 text. Upstream Artistic/GPL dual-license note intact. |
| 296 | QPrompt | Cuperino/QPrompt-Teleprompter: HTTP 200, not archived, pushed 2026-10-05T02:26:07Z, owner Cuperino. API spdx_id GPL-3.0. Raw COPYING (35,142 B) = GPL v3 text. Cuperino/QPrompt still 301-redirects to repo id 306907376. |
| 297 | OpenDCP | tmeiczin/opendcp: HTTP 200, not archived, pushed 2020-04-28T01:05:21Z. API spdx_id GPL-3.0. Grant file is COPYRIGHT.txt (31,703 B) — carries GPL v3 text ("This License refers to version 3 of the GNU General Public License"). |
| 298 | Redmine | redmine/redmine: HTTP 200, not archived, pushed 2026-10-08T10:30:09Z. API spdx_id NOASSERTION persists (detection gap — API surfaces the 918-byte LICENSE.txt pointer file). Raw doc/COPYING (18,092 B) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991". |
| 299 | OpenProject | opf/openproject: HTTP 200, not archived, pushed 2026-10-08T14:46:21Z, owner opf. API spdx_id GPL-3.0. Raw LICENSE (35,149 B) = GPL v3 text. |
| 300 | Leantime | Leantime/leantime: HTTP 200, not archived, pushed 2026-10-07T16:40:03Z, owner Leantime. API spdx_id AGPL-3.0. Raw LICENSE (34,523 B) = AGPL v3 text. |

## Drift watch (all clean vs cycle 27)

- Helm (68): mtytel/helm still owner-archived, pushed 2022-09-24T04:23:20Z, owner mtytel.
- telxcc (236): kanongil/telxcc still archived, pushed 2025-09-20T11:29:10Z, owner kanongil.
- MB-Lab (118): animate1978/MB-Lab still owner-archived, pushed 2024-07-21T02:46:17Z.
- SubDownloader (195): subdownloader/subdownloader still archived, pushed 2025-02-05T11:39:33Z.
- MPC-HC (191): mpc-hc/mpc-hc still archived, pushed 2020-04-24T11:04:40Z.
- MKVToolNix (155): codeberg.org/mbunkus/mkvtoolnix still canonical, not archived, updated 2026-09-28; raw COPYING 18,092 bytes — byte-identical to Wave 41/42/43/45/49/53/55/56 checks.
- uzu/tidal (101): codeberg.org/uzu/tidal still live, not archived, updated 2026-07-02; raw LICENSE 35,106 bytes — byte-identical to Wave 38/41/42/43/45/47/48/49/50/53/55/56 checks.

No ownership changes, no relicenses, no successors, no delists.

## Files

- `cycle28_raw_results.json` — raw GitHub/Codeberg/SF API payloads + repo metadata for all 10 rows and all 7 drift items.
- `row293_LICENSES_GPLv2.txt` — raw GPL v2 text from ElvishArtisan/rivendell@v4 (17,992 B).
- Tools that produced these: `tools/wave57_lane_b/cycle28_verify.py`, `tools/wave57_lane_b/stamp_cycle28.py`.
