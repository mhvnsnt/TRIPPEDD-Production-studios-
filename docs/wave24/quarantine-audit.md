# Quarantine audit — Wave 24 Lane C (2026-10-07)

Lane C of the TRIPPEDD Resource Pull Program WAVE 24 (quarantine audit).
Mandate: re-verify rows 232–234; fresh 10-row spot-check of older unaudited rows;
watch for relicensing events; dedup support for Lane A/B flags.
No git touched; results recorded here only (coordinator merges).

## Rows excluded from spot-check selection (already audited in recent waves)

- Wave 16 Lane D: 13, 49, 63(noted), 77, 80, 90, 98, 108, 109, 121(noted), 146–159
- Wave 17 Lane C: 160–169, 27, 47, 72, 89, 106
- Wave 18 Lane B: 173–184
- Wave 19 Lane B: 1, 3, 4, 5, 6, 10, 123, 186–200
- Wave 20 Lane C / Wave 19–20 verification notes: rows 1–27
- Wave 21 Lane E: 201, 202, 203, 204, 61, 100, 108, 145, 73, 151
- Wave 22 Lane B: 205, 208, 211, 212, 213, 214, 228, 59, 60, 71
- Wave 23 Lane D: 206, 207, 210, 215, 221, 222, 223, 225, 227, 229, 230, 231
- This wave: 232–234 (re-verified below)
- Dead rows (superseded/delisted/dedup-note) skipped: 41, 58, 65, 110, 111,
  151, 152, 158, 159, 169, 170, 171, 172, 185, 215, 216, 217, 218, 219, 220, 224, 226

## Part 1 — Rows 232–234 re-verified (Wave 23 Lane B additions)

| # | Project | Claimed | Upstream evidence (2026-10-07) | Verdict |
|---|---------|---------|--------------------------------|---------|
| 232 | spreads (DIYBookScanner/spreads) | AGPL-3.0 | GitHub license API `spdx_id` = **AGPL-3.0**; raw LICENSE.txt head reads "GNU AFFERO GENERAL PUBLIC LICENSE / Version 3, 19 November 2007". Repo exists, not archived. | CONFIRMED |
| 233 | spreadpi (DIYBookScanner/spreadpi) | GPL-2.0 | GitHub license API `spdx_id` = **GPL-2.0**; raw LICENSE head reads "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991". Repo exists, not archived. | CONFIRMED |
| 234 | YASW (Yet Another Scan Wizard) | GPL-3.0 | Project page live at https://sourceforge.net/projects/yascanw/ (this lane re-fetched it): License field = **"GNU General Public License version 3.0 (GPLv3)"**. Status Beta, C++/Qt, dormant, but the project page and license field still exist. | CONFIRMED |

**Result: 3/3 confirmed.** No license changes, no relicensing events on rows 232–234.

## Part 2 — Fresh 10-row spot-check (older unaudited rows)

Selected the stalest rows: Wave-2/Wave-3-vintage verification notes and rows that
never had any verification note (62, 64, 74).

| # | Project | Claimed | Upstream evidence (2026-10-07) | Verdict |
|---|---------|---------|--------------------------------|---------|
| 28 | Allosaurus | GPL-3.0 | Canonical upstream is **xinjli/allosaurus** — GitHub license API `spdx_id` = **GPL-3.0**, raw LICENSE confirms. Note: the often-cited `Jim-Schwoebel/allosaurus` fork now 404s; the surviving emgixiii/andrewkuo/hapaxhypatia forks all point at xinjli as canonical (CI badge references `xinjli/allosaurus`). Project exists; license unchanged. | CONFIRMED + upstream-path precision note (see Corrections) |
| 34 | GIMP | GPL-3.0-or-later | Repo GNOME/gimp exists (API `spdx_id` NOASSERTION = detection gap, as with rows 26/228). Raw LICENSE: core licensed under the GNU GPL, "see the 'COPYING' file"; raw COPYING = "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007" (the v3-or-later document). Project active. | CONFIRMED |
| 35 | HandBrake | GPL-2.0 | Raw LICENSE: "HandBrake License — Most files in HandBrake are under the GNU General Public License Version 2 (GPLv2) license; read the file COPYING for details. Some files are under the GNU GPL Version 2 or any later version (GPLv2+), the GNU LGPL 2.1 or later, or BSD/MIT/X11-style licenses." Project-level classification GPL-2.0 stands (not a relicense — this is the long-standing wording). | CONFIRMED |
| 42 | Praat | GPL-3.0-or-later | Repo `praat/praat` now redirects to `praat/praat.github.io` (license API 404 = detection gap — no LICENSE file, license stated in-repo). The repo root contains the full source tree (fon, foned, gram, main, melder…). Raw README.md §2.1: "Most of the source code of Praat is distributed on GitHub under the General Public License, version 2 or later, or version 3 or later. However, as Praat includes software written by others, the whole of Praat is distributed under the General Public License, version 3 or later." Matches the claimed GPL-3.0-or-later exactly. | CONFIRMED |
| 48 | VidCutter | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** (ozmartian/vidcutter). | CONFIRMED |
| 51 | Goo Engine | GPL-3.0 | Repo exists (GradientGamer-XD/goo-engine, not archived, pushed 2026-06-03). Raw COPYING: "Blender uses the GNU General Public License… Please read this file for the full license. doc/license/GPL-license.txt"; row's existing README quote ("Blender as a whole is licensed under the GNU General Public License, Version 3") still applies — this is a Blender fork, license follows Blender GPL. | CONFIRMED |
| 55 | comic-text-detector | GPL-3.0 | Original `zyddnys/comic-text-detector` repo no longer resolves on GitHub (404) — it was the manga-image-translator text-detection module. License confirmed via two live sources: fork **ZsIsMe/comic-text-detector** (GitHub license API `spdx_id` = **GPL-3.0**) and the parent project **zyddnys/manga-image-translator** (API `spdx_id` = **GPL-3.0**). | CONFIRMED |
| 62 | phonemizer | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** (bootphon/phonemizer). First recorded verification of this row. | CONFIRMED |
| 64 | Fooocus | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** (lllyasviel/Fooocus). First recorded verification of this row. | CONFIRMED |
| 74 | CHOW Tape Model (chowdsp) | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** at the canonical repo **jatinchowdhury18/AnalogTapeModel** (raw LICENSE). Upstream-path correction: no repo exists at `jatinchowdhury18/CHOWTapeModel` (404) and nothing tape-related under the Chowdhury-DSP org — the canonical location has always been `jatinchowdhury18/AnalogTapeModel`. First recorded verification of this row. | CONFIRMED + repo-path correction (see Corrections) |

**Result: 10/10 confirmed.** No relicensing events among the 10.

## Part 3 — Relicensing events

**None found.** All 13 rows checked this wave (232–234 + 10 spot-checks) still carry
their quarantined copyleft licenses. No delist/keep recommendations this wave.

Notable non-relicense observations (informational only, no action):
- Row 35 (HandBrake): the raw LICENSE discloses mixed-file licensing (mostly GPLv2,
  some GPLv2+/LGPLv2.1+/BSD/MIT/X11). This is the project's long-standing wording,
  not a relicense; the manifest's project-level "GPL-2.0" classification remains correct.
- Row 28 (Allosaurus): the Jim-Schwoebel/allosaurus fork is dead (404) — but the
  canonical xinjli/allosaurus is still GPL-3.0. Identity drift, not relicensing.
- Row 55 (comic-text-detector): original zyddnys repo gone (404) — license survives
  via the surviving fork and the GPL-3.0 parent project. Identity drift, not relicensing.
- Row 42 (Praat): source code repo moved (praat/praat → praat/praat.github.io);
  GitHub license API returns 404 (detection gap) — license anchored on the README
  §2.1 statement instead, per this lane.

## Part 4 — Dedup support for Lane A/B quarantine flags

**Nothing to check yet.** As of this lane's write (2026-10-07 ~20:30 EDT),
`docs/wave24/lane-a-quarantine-flags.md` and `docs/wave24/lane-b-quarantine-flags.md`
do not exist — the only file in `docs/wave24/` is `w24_netlabel_batch4.json`
(unrelated to quarantine). No flag files to dedup against the 234 rows.
If Lane A/B flags land after this audit, a follow-up pass can run the duplicate scan
against them (grep manifest for project name + repo rename redirects, per the
Wave 19 Lane B dedup lesson).

## Corrections for coordinator (apply to LICENSE_QUARANTINE.md)

1. **Row 28 (Allosaurus):** extend the row's verification note to record the
   canonical upstream as **xinjli/allosaurus** (GitHub API spdx_id GPL-3.0, raw
   LICENSE, verified 2026-10-07) — the previously implied Jim-Schwoebel/allosaurus
   path now 404s. Quarantine classification unchanged (GPL-3.0).
2. **Row 74 (CHOW Tape Model):** correct the repo path to
   **jatinchowdhury18/AnalogTapeModel** (GitHub API spdx_id GPL-3.0, verified
   2026-10-07; no repo exists at jatinchowdhury18/CHOWTapeModel; nothing
   tape-related under the Chowdhury-DSP org). License classification unchanged (GPL-3.0).
3. **Rows 62 (phonemizer), 64 (Fooocus):** both FIRST-verified this wave
   (bootphon/phonemizer GPL-3.0, lllyasviel/Fooocus GPL-3.0, via GitHub license API,
   2026-10-07). Recommend adding the verified notes to the rows.
4. **No new rows recommended.** No relicensing events; no new duplicate pairs found
   this wave.

## LGPL doctrine status

**Still PENDING OWNER VERDICT (re-checked 2026-10-07).** No LGPL/MPL/CeCILL items
among this wave's 13 rows. Rows 63 (marytts), 121 (AivisSpeech), 148 (dsnote),
154 (GPAC), 165 (Csound), 183 (Verovio), 184 (libgme), 212 stay quarantined.
No doctrine action taken.

## Tally

- Re-verified 232–234: 3/3 CONFIRMED
- Fresh spot-check: 10/10 CONFIRMED (rows 28, 34, 35, 42, 48, 51, 55, 62, 64, 74)
- Relicensing events: 0
- Duplicate pairs found in lane flags: 0 (no flag files present this wave)
- Corrections for coordinator: 4 (rows 28, 74, 62, 64 — all precision/record notes,
  zero classification changes; no delists recommended)
