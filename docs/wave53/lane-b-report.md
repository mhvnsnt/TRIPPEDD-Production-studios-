# Wave 53 Lane B report — re-verification cycle 24 + MediaConch discrepancy

Date: 2026-10-08. Branch: `wave53-lane-b`. Worker: Lane B subagent.
Scope: quarantine table `docs/LICENSE_QUARANTINE.md` only. `production/WIZARD_GANG_EP01/` untouched.

## Selection (cycle 24)

The 10 lowest-numbered live rows with bare-date "(verified 2026-10-07)" annotations and no wave-era
re-verification stamp (verified by direct scan of all 480 rows — the stamps themselves as ground truth;
cycles 18–23 covered 183–184, 186–193, 55, 62–64, 66–67, 72–73, 75, 80, 69–70, 92, 104, 166, 194–198,
207, 209–210, 221–223, 227, 229–231, 206, 225, 232–233, 235, 237–241, 234, 242–250):

**155, 251, 252, 253, 254, 255, 256, 257, 258, 259**

Method: GitHub API (spdx_id + archived + pushed_at, gh-authenticated), GitLab API (UADE), Codeberg API
(MKVToolNix, uzu/tidal), raw LICENSE/COPYING/LICENSE.txt/License.html fetches — never assumed.
API NOASSERTION treated as a detection gap, always resolved by direct text reads.
Tooling: `tools/wave53_lane_b/cycle24_verify.py` (results in `cycle24_results.json`),
`tools/wave53_lane_b/stamp_cycle24.py`.

## Results: 10/10 CONFIRMED as claimed

| Row | Project | Claimed | Verdict + key evidence |
|-----|---------|---------|------------------------|
| 155 | MKVToolNix | GPL-2.0-or-later | CONFIRMED — codeberg.org/mbunkus/mkvtoolnix canonical, owner mbunkus, not archived, updated 2026-09-28; raw COPYING (main) = GPL v2 June 1991 text, **18,092 bytes — byte-identical size to Wave 41/42/43/45/49 checks** (sha256 8177f975…); -or-later from Debian copyright composite per standing row note |
| 251 | Performous | GPL-2.0-or-later | CONFIRMED — performous/performous live, not archived, pushed 2026-09-24; API NOASSERTION = detection gap; raw LICENSE.md = GPL v2 text (18,387 bytes) with explicit header "Performous is GNU GPLv2 or later" |
| 252 | Vocaluxe | GPL-3.0 | CONFIRMED — Vocaluxe/Vocaluxe live, not archived, pushed 2026-10-06; API spdx_id GPL-3.0; **fetch-path note**: license file is `LICENSE.txt` on branch `develop` (not LICENSE/LICENSE.md/COPYING) = GPL v3 29 June 2007 text (35,146 bytes) |
| 253 | subSync (sc0ty) | GPL-3.0 | CONFIRMED — sc0ty/subSync API spdx_id GPL-3.0; raw LICENSE = GPL v3 text; **NEW DRIFT**: repo now owner-archived (pushed 2024-10-01) — archive does not change license |
| 254 | Subler | GPLv2 | CONFIRMED — SublerApp/Subler live, not archived, pushed 2026-10-05; API NOASSERTION = detection gap; root LICENSE = composite grant: "Most files in Subler are under … GPLv2 … In combination, the GPLv2 license applies to Subler" |
| 255 | stream_closed_captioner_phoenix | GPL-3.0 | CONFIRMED — talk2megooseman/stream_closed_captioner_phoenix live, not archived, pushed 2026-08-31; API spdx_id GPL-3.0; raw LICENSE = GPL v3 text |
| 256 | xmp-cli | GPL-2.0 | CONFIRMED — libxmp/xmp-cli live, not archived, pushed 2026-07-30; API spdx_id GPL-2.0; raw COPYING = GPL v2 June 1991 text |
| 257 | UADE | GPL-2.0 | CONFIRMED — **repo-location note**: canonical upstream is gitlab.com/uade-music-player/uade, NOT GitHub (uade-team/uade 404s); active, last activity 2026-09-20; root COPYING describes a mixed-license distribution; COPYING.GPL = GPL v2 June 1991 text (18,007 bytes); COPYING.LGPL also present |
| 258 | sidplayfp | GPL-2.0-or-later | CONFIRMED — libsidplayfp/sidplayfp live, not archived, pushed 2026-10-04; API spdx_id GPL-2.0 = detection gap on -or-later; raw COPYING = GPL v2 text; per-file header `src/IniConfig.h` carries "either version 2 of the License, or (at your option) any later version" |
| 259 | ASAP | GPL-2.0 | CONFIRMED — **repo-location note**: canonical upstream is SourceForge `sourceforge.net/p/asap/code` (no official GitHub repo; jhusak/asap 404s); active, release 8.0.0 (2026-02-16); root COPYING = GPL v2 June 1991 text (18,011 bytes, read from the 8.0.0 source tree); author Piotr Fusik's own statement "My code is GPL 2+" |

**Cycle totals: 10/10 confirmed. Zero relicenses, zero delists, zero supersedes, zero new rows, zero
duplicates.** All 10 stamped in the table with dated "re-verified Wave 53 Lane B, 2026-10-08" annotations.

## Drift watch (2026-10-08) — all clean, no successors, no ownership changes

- **Helm (68)**: mtytel/helm STILL owner-archived (pushed 2022-09-24T04:23:20Z — unchanged); owner mtytel; API spdx_id GPL-3.0.
- **telxcc (236)**: kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z — unchanged); owner kanongil; API NOASSERTION detection gap; raw LICENSE re-fetched (2,091 bytes) — "-or-later" boilerplate intact; no standout successor, no relicense.
- **MB-Lab (118)**: animate1978/MB-Lab STILL owner-archived (pushed 2024-07-21T02:46:17Z — unchanged); API NOASSERTION; license.txt grant intact.
- **SubDownloader (195)**: subdownloader/subdownloader still owner-archived (pushed 2025-02-05T11:39:33Z; API spdx_id GPL-3.0).
- **MPC-HC (191)**: mpc-hc/mpc-hc still owner-archived (pushed 2020-04-24T11:04:40Z; API spdx_id GPL-3.0).
- **MKVToolNix (155)**: codeberg.org/mbunkus/mkvtoolnix still canonical (Codeberg API 200), owner mbunkus, not archived, updated 2026-09-28; raw COPYING 18,092 bytes byte-identical.
- **uzu/tidal (TidalCycles successor)**: still live, not archived, owner uzu, updated 2026-07-02; raw LICENSE = GPL v3 text, **35,106 bytes — byte-identical to Wave 38/41/42/43/45/47/48/49/50 checks** (sha256 804821a9…); tidalcycles/Tidal STILL archived (pushed 2025-06-13T19:22:15Z, spdx_id GPL-3.0).

## SPECIAL: MediaConch (row 151) discrepancy — RESOLVED, no reversal

**Finding: NO upstream relicense reversal happened. The BSD-2-Clause relicense stands; the
"GPLv3+/MPLv2+" reading comes from the stale, abandoned repo — not a current license document.**

Evidence (all fetched fresh 2026-10-08):
1. **Canonical active repo** `MediaArea/MediaConch_SourceCode` (pushed 2026-08-11 — active): GitHub API spdx_id = **BSD-2-Clause**; root `LICENSE` (1,328 bytes) = full BSD 2-Clause text, "Copyright (c) 2015-2018, MediaArea.net SARL"; root `License.html` = the same BSD-2-Clause grant.
2. The current `License.html`'s "Alternate open source licenses" section grants the *user* the option to relicense under Apache-2.0-or-later, LGPL-2.1-or-later, GPL-2.0-or-later, or MPL-2.0-or-later — a downstream permission, not a project relicense. It does not make the project copyleft.
3. mediaarea.net/en/MediaConch Licensing section still reads "BSD-style license."
4. The "GPLv3+/MPLv2+" text ("All the code in this repository is licensed under GPLv3+ / MPLv2+") lives ONLY in `SourceCode/License.html` of the **stale** repo `MediaArea/MediaConch` (last pushed 2021-09-29 — abandoned) — the exact PREFORMA-era stale file Wave-21 already documented in the delist note.

**Row classification: unchanged — DELISTED/CLEARED (permissive relicense).** Row note extended with the
dated finding.

## Header counts (independent direct recount)

480 row numbers present, no gaps. 27 lines match SUPERSEDED/DELISTED markers, of which 4 stay live per
standing convention (rows 33, 111, 174, 234) → 23 true dead/superseded markers. −1 aeneas rows-1+2,
−1 Furnace rows-122+271 dup.

**480 rows · 455 distinct — matches the Wave 52 coordinator header exactly. Unchanged.**
This cycle made zero row additions/removals, zero delists, zero relicenses, zero license-family changes.

## Files changed

- `docs/LICENSE_QUARANTINE.md` — 10 cycle-24 stamps, row-151 drift note, Doctrine entry prepended.
- `docs/wave53/lane-b-report.md` — this report.
- `tools/wave53_lane_b/cycle24_verify.py`, `stamp_cycle24.py`, `cycle24_results.json` — tooling + results.

## Open items / notes for coordinator

- LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined; this lane did not decide it.
- Row 249 has a literal extra pipe in the table (9 pipes vs 8) — pre-existing, not from this lane (verified via git stash comparison). Flagging for a future table-repair pass.
- New repo-location notes landed in rows 257 (UADE → GitLab canonical) and 259 (ASAP → SourceForge canonical); catalog cross-references for those two may want a URL refresh in a future pass.
- Row 253 (subSync) newly owner-archived upstream — recorded in the stamp; classification unaffected.
