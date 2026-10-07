# Wave 22 Lane B — license quarantine spot-check (2026-10-07)

**Lane:** B (quarantine audit) · **Branch:** `wave22-lane-b`
**Mandate:** fresh 10-row sample against upstream sources; no repeats of rows audited in Waves 17–21 lanes.

## Sample

Rows recently spot-checked (excluded): 173–184, 169 (W18); 186–198, 1/3/4/5/6/10 (W19); 199–200, 26, 57 (W20 Lane C); 201–204, 61/73/100/108/145/151 (W21 Lane E).

**Audited this wave:** 205, 208, 211, 212, 213, 214, 228 (Wave-22 new rows — append-time verified by Lane A but never spot-audited by an audit lane) + 59, 60, 71 (older rows, PENDING, never verified — first verification this wave).

## Verdicts: 10/10 CONFIRMED · 0 corrections · 0 delists · 0 relicenses

| # | Project | Claim | Verdict + source |
|---|---------|-------|------------------|
| 205 | Calamari OCR | GPL-3.0 | **CONFIRMED** — `gh api repos/Calamari-OCR/calamari/license`: spdx_id `GPL-3.0` (path LICENSE) |
| 208 | unpaper | GPL-2.0-only | **CONFIRMED** — unpaper/unpaper README: `SPDX-License-Identifier: GPL-2.0-only`; "The entire `unpaper` project is licensed under GNU GPL v2" (some per-file MIT/Apache-2.0 under REUSE). NOTE: gh license API 404s for this repo (REUSE-style `LICENSES/` dir, no top-level LICENSE file) — README is the authoritative claim. Canonical upstream is now the `unpaper/unpaper` org; `Flameeyes/unpaper` is the author's older personal fork with the identical README claim |
| 211 | Internet Archive BookReader | AGPL-3.0 | **CONFIRMED** — `gh api repos/internetarchive/bookreader/license`: spdx_id `AGPL-3.0` |
| 212 | OpenSlide | LGPL-2.1 | **CONFIRMED** — `gh api repos/openslide/openslide/license`: spdx_id `LGPL-2.1` (path COPYING.LESSER). **Stays quarantined** — LGPL doctrine pending owner verdict; this lane does not decide |
| 213 | pedalboard (Spotify) | GPL-3.0 | **CONFIRMED** — `gh api repos/spotify/pedalboard/license`: spdx_id `GPL-3.0` |
| 214 | matchering | GPL-3.0 | **CONFIRMED** — `gh api repos/sergree/matchering/license`: spdx_id `GPL-3.0` |
| 228 | Zotero | AGPL-3.0 | **CONFIRMED** — COPYING in zotero/zotero: "distributes the Zotero source code under the GNU Affero General Public License, version 3 (AGPLv3)". GitHub API returns spdx `NOASSERTION` (machine-detection gap) — read the file directly; no relicense |
| 59 | DiffSVC | AGPL-3.0 | **CONFIRMED — FIRST verification** (row had no verified note) — `gh api repos/prophesier/diff-svc/license`: spdx_id `AGPL-3.0` (path LICENSE.md) |
| 60 | Trelby | GPL-2.0 | **CONFIRMED — FIRST verification** (row had no verified note) — `gh api repos/trelby/trelby/license`: spdx_id `GPL-2.0` |
| 71 | LMMS | GPL-2.0 | **CONFIRMED — FIRST verification** (row had no verified note) — `gh api repos/LMMS/lmms/license`: spdx_id `GPL-2.0` (path LICENSE.txt) |

## Findings for the coordinator (NOT in sample — no rows touched)

**7 duplicate pairs added by Wave 22 Lane A without a dedup scan** (same failure mode as Wave 17 Lane A). Same upstreams confirmed via row cells:

- 216 Essentia (MTG/essentia) ↔ 85 essentia (MTG)
- 217 Audacity (audacity/audacity) ↔ 73 Audacity
- 218 Ardour (ardour.org/copying.html) ↔ 72 Ardour
- 219 SoX (sourceforge sox) ↔ 160 SoX (Sound eXchange)
- 220 Rubber Band Library (breakfastquay/rubberband) ↔ 162 Rubber Band Library
- 224 Parselmouth (YannickJadoul/Parselmouth) ↔ 92 Parselmouth
- 226 Tenacity (tenacityteam/tenacity) ↔ 127 Tenacity

**Recommend** the coordinator mark the newer rows (216, 217, 218, 219, 220, 224, 226) SUPERSEDED by the older rows per the append-only convention — this lane did not change them (outside mandate). **Precision note:** row 218's `GPL-2.0-or-later` (ardour.org/copying.html: "General Public License version 2 or newer") is more precise than row 72's bare `GPL-2.0` — whichever row survives the dedup should carry the -or-later clause.

## Header counts — refreshed

Wave 22 Lane A appended rows 205–231 (+27) but did **not** refresh the header (still said 204 rows). Recomputed with a documented method and refreshed:

- **Before (stale):** 204 rows · 189 distinct · AGPL 24 · GPL 142 · LGPL-2.1 3 · LGPL-3.0 4 · MPL-2.0 1 · CeCILL-2.1 1 · ODbL-1.0 1 · CC BY-SA 1 · CC BY-NC-ND 1 · municipal/state 10
- **After:** **231 rows · 216 distinct** (231 − 14 dead records − 1 aeneas rows-1+2) · **AGPL 31 · GPL 164 · LGPL-2.1 4 · LGPL-3.0 3 · MPL-2.0 1 · CeCILL-2.1 1 · ODbL-1.0 1 · CC BY-SA 1 · CC BY-NC-ND 1 · municipal/state 10** (live-row sum = 217 ✓ = 231 − 14)
- **Method:** live rows only (SUPERSEDED/DELISTED in name or license cell + row 111 dedup-note excluded); primary license = identifier before the first " — "/parenthetical; dual-license rows counted under the first-mentioned license (e.g. 219 SoX → GPL, 116 JUCE → AGPL, 160 SoX → GPL, 22 RHVoice → GPL).
- **Reconciliation note:** the Wave-21 published arithmetic could not be fully reproduced (it sums to 188 over 190 live rows; recompute of rows 1–204 gives AGPL 25 / GPL 144 / LGPL-3.0 3 vs published 24 / 142 / 4 — only 3 LGPL-3.0 license cells exist in the whole table: 63, 121, 183 — so the published "4" was itself off by one). My recompute is internally consistent; the method is documented above so any future lane can re-derive it.
- **Caveat:** the 7 suspected Wave-22 duplicate pairs are not yet marked, so the formula still treats them as live projects. If the coordinator marks them SUPERSEDED: distinct → 209, AGPL → 30 (216), GPL → 158.

## LGPL doctrine — still PENDING OWNER VERDICT

Re-checked the manifest scope section 2026-10-07 — **no owner ruling on record**. Weak-copyleft rows stay quarantined: 63 (marytts), 121 (AivisSpeech), 154 (GPAC), 165 (Csound), 183 (Verovio), 184 (libgme), 212 (OpenSlide). This lane does not decide the doctrine.

## Foreign-directive scan

Reviewed `AGENTS.md` — only an internal "Autonomous tool bulletin" section (production contract: read CLAUDE_TOOL_BULLETIN.md before visual/mesh/rig work; keep working through safe lanes). No injected "autonomous / no-permission" directive block, no secrets, nothing to ignore this wave.

## Relicense watch

None in this sample — all 10 claims held at their quarantined license. (Waves 10/16/17/21 each caught real relicenses; this block is clean.)
