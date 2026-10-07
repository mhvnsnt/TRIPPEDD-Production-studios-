# Wave 17 — Lane C: quarantine spot-check + coordinator merge

**Branch:** `wave17-lane-c` (this branch; merge-ready for main).

## Part 1 — Quarantine spot-check (2026-10-07)

**15-row upstream spot-check** (GitHub API spdx_id / raw license files / vendor & distro records — never assumed): the 10 fresh Wave-16 rows (160–169) + 5 older rows never spot-checked before (27, 47, 72, 89, 106).

| Row | Project | Result |
|-----|---------|--------|
| 160 | SoX | ✅ confirmed (Debian copyright "GPL-2+ or LGPL-2.1+"; SourceForge field GPLv2+LGPLv2) |
| 161 | Sonic Visualiser | ✅ confirmed (API GPL-2.0) |
| 162 | Rubber Band Library | ✅ confirmed (API GPL-2.0) |
| 163 | TarsosDSP | ✅ confirmed (API GPL-3.0) |
| 164 | ChucK | ✅ confirmed (API GPL-2.0) |
| 165 | Csound | ✅ confirmed (API LGPL-2.1 — stays quarantined, doctrine pending) |
| 166 | OpenStreetMap geodata | ✅ confirmed (openstreetmap.org/copyright: Open Database License) |
| 167 | DCP-o-matic | ✅ confirmed (API GPL-2.0) |
| 168 | ChapterTool | ✅ confirmed (API GPL-3.0) |
| **169** | **Subtitle Edit** | **🔥 RELICENSED → MIT → DELISTED** (see below) |
| 27 | Video2X | ✅ confirmed (API AGPL-3.0) |
| 47 | Upscayl | ✅ confirmed (API AGPL-3.0) |
| 72 | Ardour | ✅ confirmed (root COPYING is the GPL-2 text) |
| 89 | OBS Studio | ✅ confirmed (API GPL-2.0) |
| 106 | Jubler | ✅ confirmed (API AGPL-3.0) |

**Result: 14/15 confirmed, 1 relicensed.**

### Row 169 relicense event (the finding of this audit)
Upstream SubtitleEdit/subtitleedit is now **MIT** — root LICENSE is the MIT text (Copyright (c) 2026 Nikolaj Olsson), GitHub API spdx_id MIT, relicense landed 2026-02/03 in the Avalonia codebase switch ("Switch to Subtitle Edit 5 (Avalonia) codebase" + "Minor clean + update license"). Row renamed from the mislabeled "Subtitle Edit (Subtitle Workshop)", Audit status DELISTED via the documented-compatible-relicense audit path. Older 4.x tags remain GPL-3.0 — pin if backporting.

**Root cause of the stale row:** the Wave-16 Lane C "verification" had quoted the WRONG project's README (dekked/subtitleworkshop — which is row 113, still GPL-3.0, still quarantined). Lesson for future waves: verify against the NAMED repo, never a same-name project.

### Docker smoke-test
**Still deferred** — no container runtime on this VM (no docker/podman/nerdctl binary, no docker socket). Speaches Docker probing remains blocked on infrastructure, not licensing.

### LGPL doctrine
**PENDING OWNER VERDICT** — re-checked, no ruling on record. Rows 63 (marytts), 121 (AivisSpeech), 154 (GPAC), 165 (Csound), 183 (Verovio), 184 (libgme) stay quarantined. Weak-copyleft watchlist unchanged.

## Part 2 — Coordinator merge

Merged `origin/wave17-lane-a` then `origin/wave17-lane-b` into `wave17-lane-c`, resolving conflicts by unioning both sides' appended entries (never dropping).

### Row-number collision (the headline issue)
Both lanes numbered their first new row **170** (Lane A: Furnace; Lane B: Gaupol) because they branched from the same base without seeing each other. Resolution: Lane B's row renumbered **170 → 185** (next free number); the mapping is recorded in the row note, the dedup mapping, the catalog entry, and the merge notes. Same-day collision — no cross-references to 170 existed yet, so nothing else broke.

### Duplicates caught at merge time
- Lane A rows 170/171/172 duplicate rows 122/124/125 (Furnace/MilkyTracker/Schism Tracker) → marked SUPERSEDED. Lane A's "no new duplicates" claim corrected.
- Lane B row 185 (Gaupol) duplicates row 99 (Gaupol) → marked SUPERSEDED.
- Net new distinct projects from Lane A: 12. From Lane B: 0.

### Final counts
- Catalog: **1842 `####` entries** (1753 + 50 Lane A + 39 Lane B).
- Quarantine: **185 rows · 171 distinct projects** (AGPL 23 · GPL 139 · LGPL-2.1 3 · LGPL-3.0 4 · MPL-2.0 1 · GPLv3+/MPLv2+ 1 · CeCILL-2.1 1 · ODbL-1.0 1 · CC BY-SA 1 · CC BY-NC-ND 1 · municipal/state rights-restricted 10).

## Wave 18 targets
- Re-run the 15-row spot-check cadence on the newest rows (173–184 + any Wave-18 additions).
- Dep-tree audit for row 169's MIT delist if Subtitle Edit becomes a shipping candidate (upstream deps not audited this pass).
- Docker smoke-test for Speaches remains blocked until a container runtime exists.
- Dedup discipline: every lane must grep the manifest before appending — Wave 17 caught 4 duplicates post-hoc that the lanes' own scans missed (rows 122/124/125/99).
