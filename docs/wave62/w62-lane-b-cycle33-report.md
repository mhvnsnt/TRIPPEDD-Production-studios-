# WAVE 62 — LANE B — Re-verification cycle 33 report

Date: 2026-10-08 (lane: w62b, branch wave62-lane-b, base origin/main 5a6824d)
Scope: rows 341–350 of docs/LICENSE_QUARANTINE.md (audio-middleware pocket, last verified Wave 39 Lane A, 2026-10-08) + identity-drift watch list.

## Result: 10/10 rows confirmed as claimed. Zero relicenses, zero delists, zero supersedes, zero repo-moves.

## Per-row evidence (fresh 2026-10-08)

### Row 341 — munt (munt/munt) — LGPL-2.1 ✅ CONFIRMED
- GitHub API: `license: null` (NOASSERTION — detection gap, same as Wave 39), archived=false, pushed 2026-06-27T09:50:35Z, owner munt/munt unchanged, default branch master.
- Direct license-text read resolves the gap: `mt32emu/COPYING.LESSER.txt` = **26,434 bytes**, opens "GNU LESSER GENERAL PUBLIC LICENSE / Version 2.1, February 1999" (sha256 36b6d3fa47916943fd5fec313c584784946047ec1337a78b440e5992cb595f89).
- NOTE: license file is NOT at repo root — path is `mt32emu/COPYING.LESSER.txt` (root has no license file; mt32emu/COPYING.txt = 17,987 bytes also exists).
- No relicense, no repo-move, no archive.

### Row 342 — alsa-lib (alsa-project/alsa-lib) — LGPL-2.1 ✅ CONFIRMED
- GitHub API spdx_id: LGPL-2.1, archived=false, pushed 2026-08-30T18:23:40Z, owner alsa-project/alsa-lib unchanged, default branch master.
- Raw COPYING = **26,440 bytes**, LGPL-2.1 February 1999 text.
- No relicense, no repo-move.

### Row 343 — LADSPA (ladspa.org) — LGPL ✅ CONFIRMED
- Fresh fetch 2026-10-08 of http://www.ladspa.org/ (index): "LADSPA has been released under LGPL (GNU Lesser General Public License)" — upstream page text unchanged.
- Old direct license URL /licence.html now 404s (page reorganized); license statement lives on the index page instead. Fetch-path note only, not a relicense.
- Corroboration: Wikipedia LGPL-2.1-or-later; Arch/NetBSD package metadata LGPL-2.1-or-later / gnu-lgpl-v2.1.
- Site live, no ownership change possible (author Richard Furse contact intact).

### Row 344 — mpg123 (mpg123) — LGPLv2 (LGPL-2.1-only) ✅ CONFIRMED
- Old www.mpg123.de/license.shtml now 404s; canonical upstream is mpg123.de / sourceforge.net/projects/mpg123/.
- Fresh corroboration 2026-10-08: Wikipedia "License LGPL-2.1-only" (stable 1.33.7, 2 Aug 2026); Arch Linux mpg123 1.33.7-1 License(s): LGPL-2.1-only; SUSE Package Hub: LGPL-2.1-only.
- Row claim "LGPLv2" remains consistent. No relicense.

### Row 345 — libmad (underbit.com) — GPL-2.0 ✅ CONFIRMED
- Fresh fetch of underbit.com/products/mad (crawled 29 days ago): "available under the terms of the GNU General Public License (GPL)".
- Corroboration: Wikipedia GPLv2; conda-forge/libmad-feedstock Package license: GPL-2.0-only; GNU Guix: GPL 2+.
- No relicense.

### Row 346 — LAME (lame.sourceforge.net) — LGPL ✅ CONFIRMED
- Fresh 2026-10-08 (crawled <1h ago): lame.sourceforge.io — "LAME is a high quality MPEG Audio Layer III (MP3) encoder licensed under the LGPL."
- NOTE: canonical site moved lame.sourceforge.net → lame.sourceforge.io; latest release v4.0 (July 2026) — project active, no relicense. Fetch-path note only.
- Corroboration: Wikipedia GNU LGPL; FreshPorts license LGPL20+; T2 SDE License: LGPL.

### Row 347 — Audiere (audiere.sourceforge.net) — LGPL ✅ CONFIRMED
- Fresh 2026-10-08: audiere.sourceforge.net/home.php (crawled 151 days ago): "Audiere is open source and licensed under the LGPL."
- SourceForge project page: "GNU Library or Lesser General Public License version 2.0 (LGPLv2)"; Wikipedia: LGPL; final release 1.9.4 (2006) — dormant but unchanged.
- No relicense.

### Row 348 — TiMidity++ (timidity.sourceforge.net) — GPL-2.0 ✅ CONFIRMED
- Wikipedia 2026-10-08: License GPL-2.0-or-later; Fedora Packages: GPL-2.0-only; upstream tarball COPYING = GPL-2.0 text (row's original evidence).
- Stable 2.15.0 (29 Aug 2018) — unchanged since Wave 39. No relicense, no repo-move.

### Row 349 — FFTW (fftw.org) — GPL ✅ CONFIRMED
- Upstream fftw.org License-and-Copyright: "FFTW is licensed under GPLv2 or higher"; Fedora: GPL-2.0-or-later AND MIT AND BSD-2-Clause (MIT/BSD are build-script components, composite still GPL-family).
- No relicense.

### Row 350 — zita-resampler (kokkinizita.linuxaudio.org) — GPL-3+ ✅ CONFIRMED
- Fresh 2026-10-08 read of Debian copyright (sources.debian.org, zita-resampler 1.8.0-2, 1,283 bytes): "Files: * … License: GPL-3+" (either v3 or any later version).
- Upstream kokkinizita.linuxaudio.org still canonical source. No relicense.

## Notes
- LGPL doctrine still PENDING OWNER VERDICT — rows 341/342/343/344/346/347 stay quarantined; this lane does not decide it (facts-only verification).
- Zero row additions/removals, zero duplicates touched.

## Identity-drift watch (fresh 2026-10-08, ~20:55Z)

| Row | Repo | Status |
|---|---|---|
| 68 | mtytel/helm | STILL owner-archived — pushed 2022-09-24T04:23:20Z, owner mtytel unchanged, spdx GPL-3.0. No successor, no ownership change, no relicense. |
| 236 | kanongil/telxcc | STILL archived — pushed 2025-09-20T11:29:10Z, owner kanongil unchanged, spdx NOASSERTION. No successor, no relicense. |
| 118 | animate1978/MB-Lab | STILL archived — pushed 2024-07-21T02:46:17Z, owner unchanged, spdx NOASSERTION. No relicense. |
| 195 | subdownloader/subdownloader | STILL archived — pushed 2025-02-05T11:39:33Z, owner unchanged, spdx GPL-3.0. No relicense. |
| 191 | mpc-hc/mpc-hc | STILL owner-archived — pushed 2020-04-24T11:04:40Z, owner mpc-hc unchanged, spdx GPL-3.0. No relicense. |
| 206 | scantailor/scantailor | STILL archived — pushed 2020-11-29T04:31:29Z, owner unchanged, spdx NOASSERTION. No relicense. |
| 243 | tidalcycles/strudel | STILL archived — pushed 2025-06-19T15:56:31Z, owner tidalcycles unchanged, spdx AGPL-3.0. No relicense. |
| 253 | sc0ty/subSync | STILL archived — pushed 2024-10-01T13:47:06Z, owner sc0ty unchanged, spdx GPL-3.0. No relicense. |
| 155 | MKVToolNix | Canonical codeberg.org/mbunkus/mkvtoolnix, NOT archived, default branch main. COPYING = GPL v2 June 1991 text, **18,092 bytes byte-identical** ✅. No host moves, no relicense. |
| 101 | uzu/tidal | codeberg.org/uzu/tidal active, NOT archived, default branch main. LICENSE = GPL v3 29 June 2007 text, **35,106 bytes byte-identical** ✅. No relicense. |

## Header counts
Unchanged by this lane (no rows added/removed): counts per latest refresh stand.
