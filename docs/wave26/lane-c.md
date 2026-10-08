# Wave 26 Lane C — quarantine spot-check on never-audited rows (2026-10-07)

Lane C of the TRIPPEDD Resource Pull Program WAVE 26 (quarantine audit).
Mandate: fresh 10-row spot-check of never-audited live rows from the quarantine
manifest, verifying each license against upstream (GitHub API spdx_id, raw
LICENSE/COPYING/README fetches, PyPI metadata); watch for relicensing events
(Wave 16/17 caught real ones); dedup support for Lane A/B flags.
Branch `wave26-lane-c`, cut from `origin/main`; worked in a sparse worktree
(`/tmp/w26-lane-c`, docs minus the 280M evidence dir). Corrections applied to
`docs/LICENSE_QUARANTINE.md` in place.

## Row selection

10 rows covering 10 families, drawn from the never-audited pool, prioritizing
rows the catalog cross-references (aeneas ×7, piper-tts ×7, Hydrogen ×4,
FlowFrames/OpenShot/Flowblade ×2): TTS (20), captions/lipsync (2), drum
machine (126), frame interpolation (9), video editor (17), vector graphics
(36), 2D animation (50), synth plugin (67), ComfyUI tooling (80),
municipal/state archive (131).

## Verdict table

| # | Project | Claimed | Upstream evidence (2026-10-07) | Verdict |
|---|---------|---------|--------------------------------|---------|
| 2 | aeneas | AGPL-3.0 | GitHub license API `spdx_id` = **AGPL-3.0** at canonical `readbeyond/aeneas` (LICENSE linked `blob/master/LICENSE`). | CONFIRMED |
| 9 | FlowFrames | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** at `n00mkrad/flowframes` (root LICENSE on main). | CONFIRMED |
| 17 | OpenShot | GPL-3.0-or-later | GitHub license API `spdx_id` = NOASSERTION (detection gap — license lives in `COPYING`, not a detected LICENSE file). Raw COPYING on develop = GPLv3 text; raw README §Copyright & License: "under the terms of the GNU General Public License … **either version 3 of the License, or (at your option) any later version**". | CONFIRMED |
| 20 | piper-tts | GPL-3.0-or-later | PyPI `piper-tts` 1.8.0 (latest) metadata `license` = **GPL-3.0-or-later**, `home_page` = `http://github.com/OHF-voice/piper1-gpl` (same homepage as the Wave 9 dedup record). GitHub license API `spdx_id` = GPL-3.0 at `OHF-Voice/piper1-gpl` (root COPYING = GPLv3 text). No relicense — the "-gpl" repo split is the same lineage, not a license change. | CONFIRMED |
| 36 | Inkscape | GPL-2.0-or-later (source); binaries GPL-3.0-or-later | **Upstream-path note:** canonical upstream is now **`gitlab.com/inkscape/inkscape`** (GitLab API: public, active — last activity 2026-10-07). The GitHub `inkscape/inkscape` repo still exists but is a stale mirror (description "Code Repository: https://gitlab.com/inkscape/inkscape", last pushed 2022-03-03; license API 404 = detection gap). GitLab `COPYING` head: "**Most Inkscape source code is available under the GNU General Public License, version 2 or later.**" inkscape.org/about/license/ embeds the GPLv2 text with the same version-2-or-later grant. | CONFIRMED + upstream-path precision note (see Corrections) |
| 50 | Wick Editor | GPL-3.0 | **Upstream-path note:** the manifest's verification source (`blackjaguar0w0-lang/wick-editor-animate`) is a **fork**. Canonical upstream = **`Wicklets/wick-editor`** (not a fork, 846 stars): GitHub license API `spdx_id` = **GPL-3.0** (root LICENSE.md). License classification unchanged. | CONFIRMED + upstream-path precision note (see Corrections) |
| 67 | Dexed | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** at `asb2m10/dexed` (root LICENSE). First recorded verification of this row. | CONFIRMED |
| 80 | ComfyUI-Manager | GPL-3.0 | GitHub license API `spdx_id` = **GPL-3.0** at `Comfy-Org/ComfyUI-Manager` (the post-migration org path; root LICENSE.txt). Matches the Wave 7 correction (not AGPL). | CONFIRMED |
| 126 | Hydrogen | GPL-2.0-or-later | GitHub license API `spdx_id` = GPL-2.0 (normalization; the -or-later clause confirmed in-repo). Raw README §License: "Hydrogen is distributed under **GPLv2+** (./COPYING)". Raw COPYING = GPLv2 text. | CONFIRMED |
| 131 | NYC Parks Photo Archive | All rights reserved; commercial license-fee regime (NOT GPL family; reference only) | Rights-restricted regime still in force: the NYC Parks Photo Archive fee schedule is still published (static.nycgovparks.org + nycgovparks.org) with reproduction-rights fees — $30–$60/image nonprofit/scholarly, **$50–$80/image commercial** (+150% worldwide surcharge). No open-license change. | CONFIRMED |

**Result: 10/10 confirmed as claimed.** Zero relicensing events, zero delists,
zero supersedes, zero quarantine-standing changes on any row.

## Relicensing events

**None found.** All 10 rows still carry their quarantined copyleft (or, for row
131, rights-restricted) terms. Watch-list items that turned out clean:
- Row 20 (piper-tts): the `piper1-gpl` repo name and OHF-Voice org move looked
  like a possible relicense trail — PyPI 1.8.0 still declares GPL-3.0-or-later
  with the same homepage; no event.
- Row 36 (Inkscape): GitHub→GitLab migration (2017-era) means the GitHub path
  is a dead mirror — identity drift only, not relicensing. Canonical path
  recorded for future waves.
- Row 50 (Wick Editor): manifest cited a fork as the verification source —
  canonical path recorded; license unaffected.

## Lane A/B quarantine flags (dedup support)

**No new candidates.** As of this lane's write (2026-10-07 ~21:05 EDT),
`docs/wave26/` contains only this report — no `lane-a-quarantine-flags.md` or
`lane-b-quarantine-flags.md` exists, and no flag list was handed to this lane.
Nothing appended. If Lane A/B flags land after this audit, a follow-up pass can
run the duplicate scan (grep manifest for project name + repo rename redirects,
per the Wave 19 Lane B dedup lesson).

## Corrections applied to docs/LICENSE_QUARANTINE.md (in place)

1. **Row 67 (Dexed):** added first-verification note — GitHub API spdx_id
   GPL-3.0 at `asb2m10/dexed`, verified 2026-10-07 (Wave 26 Lane C).
2. **Row 36 (Inkscape):** extended the verification note to record the canonical
   upstream as **`gitlab.com/inkscape/inkscape`** (GitLab COPYING: "Most Inkscape
   source code is available under the GNU General Public License, version 2 or
   later", verified 2026-10-07) — the GitHub `inkscape/inkscape` repo is a stale
   mirror (last pushed 2022-03-03; license API 404). Classification unchanged
   (GPL-2.0-or-later source / GPL-3.0-or-later binaries).
3. **Row 50 (Wick Editor):** corrected the verification source to the canonical
   **`Wicklets/wick-editor`** (non-fork; GitHub API spdx_id GPL-3.0, verified
   2026-10-07) — the previously cited `blackjaguar0w0-lang/wick-editor-animate`
   is a fork. Classification unchanged (GPL-3.0).
4. **Header:** prepended a Wave 26 Lane C blockquote to the wave-note chain.
   Header counts **unchanged** (238 rows · 215 distinct — no rows added, removed,
   superseded, or delisted this wave).
5. **Catalog `RESOURCE_CATALOG.md` "License red flags" section:** NOT refreshed —
   counts unchanged, so per mandate the section stays as Wave 25 Lane B left it
   (already reconciled to 238 rows / 215 distinct).

## LGPL doctrine status

**Still PENDING OWNER VERDICT (re-checked 2026-10-07).** No LGPL/MPL/CeCILL
items among this wave's 10 rows. Rows 63 (marytts), 121 (AivisSpeech),
148 (dsnote, MPL-2.0), 154 (GPAC), 165 (Csound), 183 (Verovio), 184 (libgme),
212 (OpenSlide) stay quarantined. This lane does not decide the doctrine.

## Tally

- Fresh spot-check: 10/10 CONFIRMED (rows 2, 9, 17, 20, 36, 50, 67, 80, 126, 131)
- Row 67: first-ever verification
- Relicensing events: 0
- Delists / supersedes recommended: 0
- Corrections applied: 3 (rows 36, 50 upstream-path precision; row 67 first-verified note)
- New rows appended: 0 (no Lane A/B flags arrived)
- Remaining never-audited live rows: 37 − 10 = **27**
  (rows 8, 16, 21, 22, 23, 29, 31, 32, 33, 37, 39, 40, 44, 45, 46, 68, 69, 70,
  81, 82, 127, 132, 133, 134, 136, 137, 138, 139)

## Commits

- `wave26-lane-c` — this lane report (`docs/wave26/lane-c.md`) + manifest
  corrections (row table notes, header blockquote). Pushed to origin at end of
  lane.
