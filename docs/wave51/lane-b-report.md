# Wave 51 Lane B — Re-verification Cycle 22 (2026-10-08)

Worktree: `~/workspace/agent-ops/wave51-lanes/w51b` · branch `wave51-lane-b` (from trippedd-studio main @ 444486a).
Parent coordinator checkpoint untouched per brief. Cycle 21 (Wave 50 Lane B) covered rows 207, 209, 210, 221, 222, 223, 227, 229, 230, 231.

## Selection
Next 10 lowest-numbered live rows with baseline-only "(verified 2026-10-07)" annotations and no wave-era re-verification stamp (dead/superseded/dedup records excluded; row 155 excluded as standing drift watch). Method: every upstream checked live via HTTP — GitHub repo API (archived flag, owner, pushed_at, default branch) + raw license-file text read and byte-compared. GitHub API `spdx_id: NOASSERTION` treated as a detection gap, never as evidence — resolved by reading the actual file text (rows 206, 225, 235).

## Per-row verdicts

| Row | Project / upstream | Claimed | Verdict | Evidence |
|-----|--------------------|---------|---------|----------|
| 206 | ScanTailor — scantailor/scantailor | GPL-3.0-or-later | CONFIRMED | raw COPYING (464 bytes) = explicit grant "either version 3 of the License, or (at your option) any later version". **Archive-status note NEW vs original annotation: repo now owner-archived, pushed 2020-11-29T04:31:29Z. License unaffected.** GitHub API spdx_id NOASSERTION (detection gap — resolved by raw text read). |
| 225 | NormCap — dynobo/normcap | GPL-3.0-or-later | CONFIRMED | live, not archived (pushed 2026-10-07). Raw LICENSE (724 bytes) = GPL-3.0-or-later grant "either version 3 of the License, or (at your option) any later version". API spdx_id NOASSERTION (detection gap — resolved by raw text read). |
| 232 | spreads — DIYBookScanner/spreads | AGPL-3.0 | CONFIRMED | live, not archived (dormant, pushed 2016-04-21). **Fetch-path note: license file is LICENSE.txt, not LICENSE.** Raw LICENSE.txt (34,520 bytes) = "GNU AFFERO GENERAL PUBLIC LICENSE Version 3" text. |
| 233 | spreadpi — DIYBookScanner/spreadpi | GPL-2.0 | CONFIRMED | live, not archived (dormant, pushed 2015-06-12). Raw LICENSE (18,092 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text. API spdx_id GPL-2.0 agrees. |
| 235 | QCTools — bavc/qctools | GPL-3.0 | CONFIRMED | live, not archived (pushed 2026-07-06). Root License.html carries the GPLv3 "either version 3 of the License, or (at your option) any later version" grant. API spdx_id NOASSERTION (detection gap — resolved by raw text read). |
| 237 | UltraStar-Deluxe — UltraStar-Deluxe/USDX | GPL-2.0 | CONFIRMED | live, not archived (pushed 2026-10-07). **Fetch-path note: grant lives in LICENSE (COPYRIGHT.txt is only the author list).** Raw LICENSE (18,047 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2" text. |
| 238 | AtomicParsley — wez/atomicparsley | GPL-2.0 | CONFIRMED | live, not archived (pushed 2024-12-04). Raw COPYING (15,123 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text. |
| 239 | libADLMIDI — Wohlstand/libADLMIDI | GPL-3.0 | CONFIRMED | live, not archived (pushed 2026-10-03). **Fetch-path note: grant lives in LICENSE.txt (GPL v3); LICENSE.LGPL-2.1.txt is a secondary dual-license option per README — primary claim GPL-3.0 stands.** Raw LICENSE.txt (35,149 bytes) = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007" text. |
| 240 | ChibiTracker — reduz/chibitracker | GPL-2.0 | CONFIRMED | live, not archived (pushed 2023-02-02). Raw COPYING (15,131 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text. |
| 241 | JSIDPlay2 — kenchis/JSIDPlay2 | GPL-2.0 | CONFIRMED | live, not archived (pushed 2024-12-29). Raw LICENSE (18,092 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text. |

**Result: 10/10 CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes, zero new rows, zero duplicates.**
Findings/notes: 1 new archive-status note (row 206: scantailor/scantailor now owner-archived — license classification unaffected); 3 fetch-path notes (232: LICENSE.txt not LICENSE; 237: LICENSE not COPYRIGHT.txt; 239: LICENSE.txt vs LICENSE.LGPL-2.1.txt dual). Zero license-family changes.

## Drift watch (cycle 22 — 7/7 clean)

- **Helm (row 68)** — STILL owner-archived under mtytel. pushed_at 2022-09-24T04:23:20Z — unchanged. API spdx_id GPL-3.0. No ownership change, no successor, no relicense.
- **telxcc (row 236)** — STILL archived under kanongil. pushed_at 2025-09-20T11:29:10Z — unchanged. Raw LICENSE (2,091 bytes) — "either version 2 of the License, or (at your option) any later version" boilerplate intact. API spdx_id NOASSERTION (detection gap as before).
- **MKVToolNix (row 155)** — still canonical at codeberg.org/mbunkus/mkvtoolnix. Codeberg API 200, owner mbunkus, not archived, updated 2026-09-28. Raw COPYING on branch main = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text, 18,092 bytes — byte-identical to Waves 41/42/43 checks. No host moves, no relicense; GPL-2.0-or-later composite stands.
- **codeberg.org/uzu/tidal** — active, not archived, owner uzu, updated 2026-07-02. Raw LICENSE on branch main = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007" text, 35,106 bytes — unchanged. GPL-3.0 intact.
- **MB-Lab (row 118)** — STILL archived (animate1978/MB-Lab), pushed 2024-07-21T02:46:17Z — unchanged. license.txt GPL-3.0 grant intact. No relicense.
- **SubDownloader (row 195)** — STILL owner-archived (subdownloader/subdownloader), pushed 2025-02-05T11:39:33Z — unchanged. GPL-3.0 unaffected.
- **MPC-HC (row 191)** — STILL archived (mpc-hc/mpc-hc), pushed 2020-04-24T11:04:40Z — unchanged. API spdx_id GPL-3.0. License unaffected.

## Files changed
- `docs/LICENSE_QUARANTINE.md` — 10 rows stamped "(re-verified Wave 51 Lane B, 2026-10-08: …)" in the License column with upstream evidence (rows 206, 225, 232, 233, 235, 237, 238, 239, 240, 241).
- `docs/wave51/lane-b-report.md` — this report (cycle-22 proofs).

Header counts: no row additions/removals in this cycle (475 rows / 450 distinct per Wave-50 coordinator header; lane made zero structural changes).
