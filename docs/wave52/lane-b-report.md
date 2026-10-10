# Wave 52 Lane B — Re-verification Cycle 23 (2026-10-08)

Worktree: `~/workspace/agent-ops/wave52-lanes/w52b` · branch `wave52-lane-b` (from trippedd-studio main @ b3ed54a).
Cycle 22 (Wave 51 Lane B) covered rows 206, 225, 232, 233, 235, 237, 238, 239, 240, 241.

## Selection
Next 10 lowest-numbered live rows with baseline-only "(verified 2026-10-07)" annotations and no wave-era re-verification stamp (dead/superseded/dedup records excluded; standing drift-watch rows 68, 118, 155, 191, 195, 236 excluded). Rows: 234, 242, 243, 244, 245, 246, 247, 248, 249, 250. Method: every upstream checked live via HTTP — GitHub repo API (archived flag, owner, pushed_at, default branch) + raw license-file text read and byte-compared. GitHub API `spdx_id: NOASSERTION` treated as a detection gap, never as evidence — resolved by reading the actual file text (row 245). SourceForge rows verified via the project-page License field (row 249 claim cross-checked against the Wikipedia infobox).

## Per-row verdicts

| Row | Project / upstream | Claimed | Verdict | Evidence |
|-----|--------------------|---------|---------|----------|
| 234 | YASW — sourceforge.net/projects/yascanw/ | GPL-3.0 | CONFIRMED | Project page License field still "GNU General Public License version 3.0 (GPLv3)"; project active (Beta, tibob42). |
| 242 | Cardinal — DISTRHO/Cardinal | GPL-3.0 | CONFIRMED | live, not archived (pushed 2026-07-28T11:06:35Z). API spdx_id GPL-3.0. Raw LICENSE (32,472 bytes) = GNU GPL v3 29 June 2007 text. |
| 243 | Strudel — tidalcycles/strudel | AGPL-3.0 | CONFIRMED | live — **NOW OWNER-ARCHIVED** (pushed 2025-06-19T15:56:31Z; archive-status note NEW vs baseline). API spdx_id AGPL-3.0. Raw LICENSE (34,523 bytes) = GNU AGPL v3 text. License unaffected. |
| 244 | BespokeSynth — BespokeSynth/BespokeSynth | GPL-3.0 | CONFIRMED | live, not archived (pushed 2026-10-08T04:15:40Z). API spdx_id GPL-3.0. Raw LICENSE (35,141 bytes) = GNU GPL v3 29 June 2007 text. |
| 245 | Cmajor — cmajor-lang/cmajor | GPL-3.0-or-later | CONFIRMED | **REPO MOVED: SoundStacks/cmajor → cmajor-lang/cmajor** (GitHub "Moved Permanently", new repo id 496299024); live, not archived (pushed 2026-10-08T09:41:22Z). API spdx_id NOASSERTION (detection gap — resolved by raw text read). Raw LICENSE.md (1,115 bytes) = dual "GPLv3 (or later)"/Commercial license statement. |
| 246 | Psycle — sourceforge.net/projects/psycle/ | GPL-2.0 | CONFIRMED | Project page License field still "GNU General Public License version 2.0 (GPLv2), Public Domain" — unchanged since baseline (current code GPL-2.0; only Arguru's v1.0 sources were PD). Project active (5 months ago). |
| 247 | FamiTracker original — famitracker.com / jsr | GPL-2.0 | CONFIRMED | Maintained-fork license documentation: nyanpasu64/0CC-FamiTracker 0CC-readme.txt — "This program and its source code are licensed under the GNU General Public License Version 2", based on vanilla FamiTracker 0.5.0 beta 5 (original NSF driver still not under GPL — source-available, no grant). famitracker.com itself WAF-blocks direct fetch; fork docs suffice for the claim. |
| 248 | Aldrin — sourceforge.net/projects/aldrin/ | GPL-2.0 | CONFIRMED | Project page License field still "GNU General Public License version 2.0 (GPLv2)" (Beta, unchanged). |
| 249 | SoundTracker Unix — Michael Krause | GPL-2.0-or-later | CONFIRMED | Wikipedia SoundTracker (Unix) infobox (crawled 5 days ago) still "License | GPL-2.0-or-later", repository sourceforge.net/p/soundtracker/git/. SF project-page License field says GPLv2 (coarse field, same as baseline — not a relicense). Git tree web view 403'd to us this pass; claim held via infobox. |
| 250 | mikmod player — sezero/mikmod (`mikmod/`) | GPL-2.0 | CONFIRMED | live, not archived (pushed 2026-10-07T09:08:01Z, default branch master). README in `mikmod/` (5,394 bytes): "The MikMod module player is covered by the GNU General Public License … either version 2 of the licence, or (at your option) any later version" — precision note: grant is v2-or-later, covering the GPL-2.0 claim. |

**Result: 10/10 CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes, zero new rows, zero duplicates.**
Findings/notes: 1 new archive-status note (row 243: tidalcycles/strudel now owner-archived — license classification unaffected); 1 repo move (row 245: SoundStacks/cmajor → cmajor-lang/cmajor — GitHub redirect resolves, license unaffected); 1 precision note (row 250: README grant is v2-or-later, covers the GPL-2.0 claim — not a relicense). Zero license-family changes.

## Drift watch (cycle 23 — 7/7 clean)

- **Helm (row 68)** — STILL owner-archived under mtytel. pushed_at 2022-09-24T04:23:20Z — unchanged. API spdx_id GPL-3.0. No ownership change, no successor, no relicense.
- **telxcc (row 236)** — STILL archived under kanongil. pushed_at 2025-09-20T11:29:10Z — unchanged. API spdx_id NOASSERTION (detection gap as before).
- **MKVToolNix (row 155)** — still canonical at codeberg.org/mbunkus/mkvtoolnix. Codeberg API 200, owner mbunkus, not archived, updated 2026-09-28. Raw COPYING on branch main = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" text, 18,092 bytes — byte-identical to Waves 41/42/43 checks. No host moves, no relicense; GPL-2.0-or-later composite stands.
- **codeberg.org/uzu/tidal** — active, not archived, owner uzu, updated 2026-07-02. Raw LICENSE on branch main = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007" text, 35,106 bytes — unchanged. GPL-3.0 intact.
- **MB-Lab (row 118)** — STILL archived (animate1978/MB-Lab), pushed 2024-07-21T02:46:17Z — unchanged. API spdx_id NOASSERTION. No relicense.
- **SubDownloader (row 195)** — STILL owner-archived (subdownloader/subdownloader), pushed 2025-02-05T11:39:33Z — unchanged. API spdx_id GPL-3.0. GPL-3.0 unaffected.
- **MPC-HC (row 191)** — STILL archived (mpc-hc/mpc-hc), pushed 2020-04-24T11:04:40Z — unchanged. API spdx_id GPL-3.0. License unaffected.

## Files changed
- `docs/LICENSE_QUARANTINE.md` — 10 rows stamped "(re-verified Wave 52 Lane B, 2026-10-08: …)" in the License column with upstream evidence (rows 234, 242, 243, 244, 245, 246, 247, 248, 249, 250).
- `docs/wave52/lane-b-report.md` — this report (cycle-23 proofs).

Header counts: no row additions/removals in this cycle; no structural changes to the quarantine doc (lane made zero count changes).
