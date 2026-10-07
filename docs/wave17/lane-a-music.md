# Wave 17 — Lane A: music/score lane (PD music/score long tail + chiptune/retro trackers)

**Branch:** `origin/wave17-lane-a` (commits f277906, c08b077), merged into `wave17-lane-c` 2026-10-07.

## Catalog
- **+50 `####` entries** in docs/RESOURCE_CATALOG.md (1753 → 1803 before Lane B's merge): PD music/score long-tail archives (LiederNet, Lester S. Levy, Duke, Sibley, etc.) and chiptune/retro trackers.
- License verification was a first-class artifact, not an afterthought.

## Quarantine: rows 170–184 (+15)
All 15 verified upstream 2026-10-07 (GitHub API spdx_id, raw LICENSE/COPYING/README fetches, repo copying files — never assumed):
- 170 Furnace — GPL-2.0-or-later
- 171 MilkyTracker — GPL (Milkyplay player library New-BSD since 0.90.85; rest stays GPL)
- 172 Schism Tracker — GPL-2.0
- 173 BambooTracker — GPL-2.0-or-later
- 174 0CC-FamiTracker — GPL-2.0
- 175 Radium — GPL-2.0
- 176 GoatTracker — GPL-2.0
- 177 MuseScore Studio — GPL-3.0 (explicit non-conflation: proprietary musescore.com cataloged separately)
- 178 LilyPond — GPL-3.0-or-later
- 179 Frescobaldi — GPL-2.0
- 180 Denemo — GPL-3.0
- 181 Abjad — GPL-3.0
- 182 mingus — GPL-3.0
- 183 Verovio — LGPL-3.0 (weak copyleft; doctrine pending owner verdict)
- 184 libgme / game-music-emu — LGPL-2.1 (weak copyleft; doctrine pending owner verdict)
- Near-misses kept OUT: VGMPlay (unverifiable, no license file), bfxr (Apache-2.0 per readme.MD, cataloged ✅), NSFPlay (maintainer-presumption only, cataloged ⚠️ documented negative).

## Tools & evidence
- `tools/music/wave17_laneA_pd_pull.py` — PD audio pull script.
- `tools/music/wave17_laneA_verify_licenses.py` — license verification script.
- `tools/music/evidence_wave17_laneA/` — license_manifest.json (365 lines), pd_pull_manifest.json, vendored license texts (DrPetter/musagi, kometbomb/klystrack, lilypond, milkytracker COPYING, musescore LICENSE, tildearrow/furnace LICENSE).
- 3 PD audio binaries (~3.8 MB total, within the 100 MB rule): `commons_A_Chantar2.ogg` (1.0 MB), `l'O_merveille!..._A_moi_les_plaisirs.ogg` (2.7 MB), `mutopia_bethena.mid` (24 KB).

## Coordinator findings at merge (recorded in the quarantine manifest)
- **Dedup misses:** rows 170/171/172 duplicate existing rows 122 (Furnace), 124 (MilkyTracker), 125 (Schism Tracker) — marked SUPERSEDED with dedup-mapping entries. Lane A's "no new duplicates" claim corrected: 12 new distinct projects, not 15.
- **Row-number collision:** Lane A's row 170 (Furnace) collided with Lane B's row 170 (Gaupol). Lane B's row was renumbered 170→185; Lane A's rows kept their numbers.
