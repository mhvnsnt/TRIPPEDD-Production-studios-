# Wave 19 Lane B notes — quarantine audit (2026-10-07)

Mandate: fresh upstream spot-check of quarantine rows 186–198 + 5+ oldest never-audited rows; fold in Lane A's 4 flags; refresh counts; leave LGPL doctrine alone (owner ruling pending).

## Spot-check rows 186–198 (fresh upstream, 2026-10-07) — 13/13 CONFIRMED

| Row | Project | License | Evidence |
|-----|---------|---------|----------|
| 186 | Zrythm | AGPL-3.0 (+S7 trademark) | raw LICENSES/LicenseRef-ZrythmLicense.txt re-fetched: AGPL v3 "or any later version, with the additional terms below"; API still NOASSERTION |
| 187 | CheeseTracker | GPLv2 | SourceForge project page: "GNU General Public License version 2.0 (GPLv2)" |
| 188 | Rosegarden | GPL-2.0 | API spdx_id nengxu/rosegarden |
| 189 | IINA | GPL-3.0 | API spdx_id iina/iina |
| 190 | SMPlayer | GPL-2.0 | API spdx_id smplayer-dev/smplayer |
| 191 | MPC-HC | GPL-3.0 | API spdx_id mpc-hc/mpc-hc |
| 192 | MPC-BE | GPLv3 | SourceForge project page: "GNU General Public License version 3.0 (GPLv3)" |
| 193 | Celluloid | GPL-3.0 | API spdx_id celluloid-player/celluloid |
| 194 | VideoSubFinder | GPL-2.0 | API spdx_id SWHL/VideoSubFinder |
| 195 | SubDownloader | GPL-3.0 | API spdx_id subdownloader/subdownloader (unrelated MIT namesake beatfreaker/ noted) |
| 196 | Av1an | GPL-3.0 | API spdx_id rust-av/Av1an (moved master-of-zen → rust-av) |
| 197 | VisualSubSync | GPL-2.0 | API spdx_id Red5goahead/VisualSubSync-Enhanced |
| 198 | xy-VSFilter | GPL-2.0 | API spdx_id Cyberbeing/xy-VSFilter |

Zero delists, zero corrections, zero supersedes in this block.

## Oldest never-audited rows (6, all PENDING, no prior "verified" note) — 6/6 CONFIRMED

Repo-identity drift was the story — five of six upstreams moved or renamed since listing; licenses unchanged, all still correctly quarantined. In-cell verified notes added to each row:

- **1 aeneas** → readbeyond/aeneas (was readthedocs/aeneas): AGPL-3.0
- **3 AnimeEffects** → AnimeEffectsDevs/AnimeEffects (was hidefuku/AnimeEffects): GPL-3.0
- **4 AUTOMATIC1111 SD WebUI** → AUTOMATIC1111/stable-diffusion-webui: AGPL-3.0
- **5 ComfyUI** → Comfy-Org/ComfyUI (was comfyanonymous/ComfyUI, org renamed): GPL-3.0
- **6 Enve** → Hope2333/enve active continuation (was MaurycyLiebner/enve): GPL-3.0
- **10 fSpy** → perarnia/fSpy (was stuffmatic/fSpy, org renamed): GPL-3.0

## Lane A flags — PRE-ADD dedup caught 2 duplicates (only 2 new rows)

- Flag #1 **0CC-FamiTracker** = existing **row 174** (GPL-2.0). No new row.
- Flag #2 **j0CC-FamiTracker** = existing **row 123 lineage**. `gumball2415/j0cc-famitracker` → server-side redirect to `Dn-Programming-Core-Management/Dn-FamiTracker` (rename/transfer confirmed 2026-10-07). Same codebase as AlbenBustamante/Dn-FamiTracker (its README links Gumball2415/Dn-FamiTracker downloads). No new row. Row 123 audit note extended with rename chain; README license re-verified: GPL-2.0-or-later + GPLv3-only FDS-emulation dependency (shipped binary effectively GPLv3) — classification unchanged.
- Flag #3 **mml2vgm (rjungemann)** → **NEW row 199**, GPL-3.0 (API spdx_id + raw LICENSE.txt fetched).
- Flag #4 **TinyVGM (SudoMaker)** → **NEW row 200**, AGPL-3.0 (API spdx_id + raw LICENSE fetched).

**Dedup lesson (echo of Wave 17 Lane C):** Lane A's scan checked names but not existing rows for the same forks/lineages. Future lanes: grep the manifest AND follow repo rename redirects before flagging.

## Counts

- Rows: 198 → **200** · distinct projects: 184 → **186**
- Families: AGPL 25 · GPL 152 · LGPL-2.1 3 · LGPL-3.0 3 · MPL-2.0 1 · GPLv3+/MPLv2+ 1 · CeCILL-2.1 1 · ODbL-1.0 1 · CC BY-SA 1 · CC BY-NC-ND 1 · municipal/state rights-restricted 10
- `grep -c '^| [0-9]'` on the manifest = 200. Manifest H2 header and catalog "License red flags" bullet refreshed to match. (Note: the Wave-17 quoted count block inside the manifest header is a historical record — left as-is.)

## Commits

- `e9ade5b` — Wave 19 Lane B: quarantine spot-check rows 186–198 + 6 oldest unaudited rows; +2 new rows (199 mml2vgm GPL-3.0, 200 TinyVGM AGPL-3.0); 2 Lane-A flags deduped to rows 174/123
- (catalog + notes commit follows)

Files touched: docs/LICENSE_QUARANTINE.md, docs/RESOURCE_CATALOG.md (red-flags bullet only), docs/wave19/lane-b-notes.md. No production files touched; parent's uncommitted WIZARD_GANG_EP01 files untouched.
