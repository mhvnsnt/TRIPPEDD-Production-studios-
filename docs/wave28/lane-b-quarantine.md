# Wave 28 Lane B — quarantine spot-check (2026-10-07)

**Branch:** `wave28-lane-b` (cut from origin/main at 0f5822c). No push/merge by this lane — coordinator merges sequentially. No binaries, no force-push.
**Mandate:** 10-row fresh upstream spot-check of the never-audited quarantine pool, prioritizing the Wave-27-flagged rows (63 marytts, 66 Surge XT, 75 Dragonfly Reverb), then the oldest unaudited.

## Row selection

The never-audited pool (coordinator: 17 rows remain) was reconstructed from the Wave-25 Lane B audit-union list ("Remaining never-audited live rows: 37", docs/wave25/lane-b.md) minus Wave-26 Lane C's 10 (2, 9, 17, 20, 36, 50, 67, 80, 126, 131) minus Wave-27 Lane B's 10 (22, 23, 31, 33, 37, 68, 69, 70, 81, 82), plus the 3 auditor-flagged unmarked rows (63, 66, 75). Rows 127 / 132–134 / 136–139 carry 2026-10-07 "verified" annotations in their License cells, so they are not never-audited. This lane's 10: **63, 66, 75** (flagged) + **8, 16, 21, 29, 32, 39, 40** (the 7 lowest-numbered remaining never-audited rows — oldest first). No overlap with Wave 27's audited set (avoids merge conflicts with wave27-lane-b).

**Method:** GitHub API `spdx_id` + raw LICENSE/COPYING/README fetches — never assumed. API `NOASSERTION` treated as a machine-detection gap, resolved by reading the actual license file. Duplicate scan: project-name + repo-URL grep across the manifest.

## Results

| # | Project | Claim | Verdict | Upstream evidence (2026-10-07) |
|---|---------|-------|---------|-------------------------------|
| 63 | marytts | LGPL-3.0 | **CONFIRMED (facts only)** | marytts/marytts live, not archived. Root LICENSE.md: "under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, version 3 of the License." API NOASSERTION = detection gap on custom header. **LGPL doctrine NOT re-litigated — row stays quarantined per standing rule (rows 63, 121, 148, 154, 165, 183, 184, 212).** |
| 66 | Surge XT | GPL-3.0 | **CONFIRMED** | surge-synthesizer/surge live, not archived. API spdx_id = GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text. |
| 75 | Dragonfly Reverb | GPL-3.0 | **CONFIRMED** | michaelwillis/dragonfly-reverb live, not archived. API spdx_id = GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text. |
| 8 | Flowblade | GPL-3.0-or-later | **CONFIRMED** | jliljebl/flowblade live, not archived. API spdx_id = GPL-3.0; root LICENSE = GPL v3 text. **-or-later confirmed** by per-file header (flowblade-trunk/Flowblade/src/app.py): "or (at your option) any later version". |
| 16 | Olive | GPL-3.0 | **CONFIRMED + URL correction** | Canonical upstream is now **olive-editor/olive** — old OliveTeam/olive path 404s (org/repo moved). API spdx_id olive-editor/olive = GPL-3.0; README = Olive Video Editor (olivevideoeditor.org); live, not archived. Manifest name cell now carries the canonical path (matches catalog entry). |
| 21 | Power Sequencer | GPL-3.0-or-later | **CONFIRMED + path-case precision** | Canonical GDQuest/blender-power-sequencer (lowercase b) live, not archived. __init__.py carries `SPDX-License-Identifier: GPL-3.0-or-later` — **-or-later confirmed**. API spdx_id = GPL-3.0. Manifest name cell now carries the canonical path. |
| 29 | Avidemux | GPL-2.0 | **CONFIRMED** | mean00/avidemux2 live, not archived. Raw COPYING = GPL v2 June 1991 text. API NOASSERTION = detection gap on COPYING. |
| 32 | chaiNNer | GPL-3.0 | **CONFIRMED** | chaiNNer-org/chaiNNer live, not archived. API spdx_id = GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text. |
| 39 | LibreSprite | GPL-2.0 | **CONFIRMED** | LibreSprite/LibreSprite live, not archived. API spdx_id = GPL-2.0; raw LICENSE.txt = GPL v2 June 1991 text. |
| 40 | LiVES | GPL-3.0 | **CONFIRMED** | salsaman/LiVES live, not archived. API spdx_id = GPL-3.0; raw COPYING = GPL v3 29 June 2007 text on both the LiVES-4.0 default branch and master. |

**Result: 10/10 confirmed as claimed. Zero relicensing events, zero delists, zero supersedes, zero new rows. Duplicate scan clean on all 10 (no earlier-row duplicates by project name or repo URL).**

## Manifest changes (docs/LICENSE_QUARANTINE.md)

- 10 row License-cell annotations per the wave convention ("verified Wave 28 Lane B, 2026-10-07: …"), rows 8, 16, 21, 29, 32, 39, 40, 63, 66, 75.
- Precision fixes: row 16 name cell now `Olive (olive-editor/olive)` (canonical-URL correction — old org path 404s); row 21 name cell now `Power Sequencer (GDQuest/blender-power-sequencer)` (path-case precision).
- New "Wave 28 Lane B quarantine spot-check" note blockquote under the `## Quarantined items` header (newest-first convention).
- **Header counts independently re-verified:** 255 row records − 22 dead records (19 superseded + 2 delisted + row-111 mapping record + row 215 audit-cell supersede) − 1 (aeneas rows 1+2) = **232 distinct ✓**. Unchanged: **255 rows · 232 distinct**.

## Catalog sync (docs/RESOURCE_CATALOG.md — red-flags header bullet ONLY; Lane A's territory otherwise untouched)

- Appended the Wave-28 Lane B spot-check note to the "Quarantined (copyleft)" bullet (counts unchanged: 255 rows · 232 distinct). No other catalog edits.

## Notes for the coordinator

- **Row 151 (MediaConch, DELISTED) structural defect:** origin/main still carries the pre-existing 7-pipe row-151 defect (License-column delimiter missing). Wave-27 Lane B already repaired it on wave27-lane-b — this lane deliberately did NOT touch it, to avoid a merge collision. Once wave27 merges, the defect is gone.
- My branch is based on origin/main **without** the wave27 merges (they exist only as local branches wave27-lane-a / wave27-lane-b, not yet on origin/main). My 10 rows deliberately avoid Wave 27 Lane B's audited set {22, 23, 31, 33, 37, 68, 69, 70, 81, 82} to minimize merge friction. Expected merge behavior: my Wave-28 note blockquote sits directly under the `## Quarantined items` header; wave27-lane-b's note block targets the same spot — ordering at merge is the coordinator's call.
- Row 16 (Olive): the old `OliveTeam/olive` path 404s; canonical is `olive-editor/olive` (already what the catalog cites). If any other doc references the old path, it should be updated.
- Local `main` in this checkout has been moved to a673b03 (includes unpushed wave27 merges + workspace-sweep commits) while origin/main is still 0f5822c. Sibling wave28-lane-a shares this working tree — coordinate checkouts to avoid clobbering uncommitted work.
- LGPL doctrine: still PENDING OWNER VERDICT (re-checked 2026-10-07 — no ruling on record). Rows 63, 121, 148, 154, 165, 183, 184, 212 stay quarantined. This lane decided nothing.
