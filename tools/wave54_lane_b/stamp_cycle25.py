#!/usr/bin/env python3
"""Wave 54 Lane B — stamp cycle-25 re-verification annotations into rows 260-270.
Row 267 also gets its license correction (GPL-2.0-or-later -> GPL-3.0-or-later).
No row numbers change. Pipe-safe quoting only.
"""
import re

P = "/home/hatch/workspace/agent-ops/wave54-lanes/w54b/docs/LICENSE_QUARANTINE.md"
txt = open(P).read()

def stamp(row, old_frag, new_frag):
    global txt
    assert txt.count(old_frag) == 1, f"frag not unique for row {row}: {old_frag[:60]!r}"
    txt = txt.replace(old_frag, new_frag)

ST = "re-verified Wave 54 Lane B, 2026-10-08"

# 260 lazyusf2
stamp(260,
 "| 260 | lazyusf2 | GPL-2.0-or-later (verified 2026-10-07, upstream; Wave 27 Lane A) — Nintendo 64 USF music emulator |",
 "| 260 | lazyusf2 | GPL-2.0-or-later (verified 2026-10-07, upstream; Wave 27 Lane A) (" + ST + ": CONFIRMED — canonical GitLab kode54/lazyusf2, last activity 2022-03-10; no COPYING in tree; per-file header main/main.c: \"either version 2 of the License, or (at your option) any later version\" — GPL-2.0-or-later stands; quarantine unchanged) — Nintendo 64 USF music emulator |")

# 261 QMMP
stamp(261,
 "| 261 | QMMP (Qt-based Multimedia Player) | GPL-2.0-or-later (verified 2026-10-07, upstream; Wave 27 Lane A) — audio player with chiptune plugin support |",
 "| 261 | QMMP (Qt-based Multimedia Player) | GPL-2.0-or-later (verified 2026-10-07, upstream; Wave 27 Lane A) (" + ST + ": CONFIRMED — canonical upstream SourceForge qmmp-dev (no official GitHub; official site qmmp.ylsoftware.com live); SF project License field \"License version 2.0 (GPLv2)\"; SVN trunk/qmmp/COPYING = GPL v2 June 1991 text (18,092 bytes); trunk/qmmp/src/app/main.cpp header: \"either version 2 of the License, or (at your option) any later version\" — GPL-2.0-or-later stands; quarantine unchanged) — audio player with chiptune plugin support |")

# 262 NotSo Fatso
stamp(262,
 "| 262 | NotSo Fatso | GPL-2.0+ (verified 2026-10-07, upstream; Wave 27 Lane A) — NSF/NES music player |",
 "| 262 | NotSo Fatso | GPL-2.0+ (verified 2026-10-07, upstream; Wave 27 Lane A) (" + ST + ": CONFIRMED — author site disch.zophar.net live; v0.851 source tarball Readme.txt (Copyright (C) 2004 Disch) + per-file headers: \"either version 2 of the License, or (at your option) any later version\" — GPL-2.0-or-later stands; third-party corroboration: xmplay_gamemusic_plugin README \"The combined plugin is GPLv2+ because NotSo Fatso is GPL-2+\"; quarantine unchanged) — NSF/NES music player |")

# 263 audapolis (repo moved)
stamp(263,
 "| 263 | audapolis | AGPL-3.0 (verified 2026-10-07: upstream license via linuxlinks/alternativeto/github forks; Wave 28 Lane A) — editor for spoken-word audio/video with automatic transcription, wordprocessor-like media editing |",
 "| 263 | audapolis | AGPL-3.0 (verified 2026-10-07: upstream license via linuxlinks/alternativeto/github forks; Wave 28 Lane A) (" + ST + ": CONFIRMED AGPL-3.0 — REPO MOVED: audapolis/audapolis -> bugbakery/audapolis (GitHub \"Moved Permanently\", live, not archived, pushed 2026-06-24); API spdx_id AGPL-3.0; raw LICENSE (34,523 bytes) = GNU AGPL v3 text — AGPL-3.0 stands; quarantine unchanged) — editor for spoken-word audio/video with automatic transcription, wordprocessor-like media editing |")

# 264 Kaltura (repo moved)
stamp(264,
 "| 264 | Kaltura (video platform Community Edition) | AGPL-3.0 (verified 2026-10-07: kaltura/server GitHub README states \"All code in this project is released under the AGPLv3 license\"; Wave 29 Lane A) — open-source video management/publishing platform with caption support |",
 "| 264 | Kaltura (video platform Community Edition) | AGPL-3.0 (verified 2026-10-07: kaltura/server GitHub README states \"All code in this project is released under the AGPLv3 license\"; Wave 29 Lane A) (" + ST + ": CONFIRMED AGPL-3.0 — REPO MOVED: kaltura/server 404s -> canonical now kaltura-community/server (live, not archived, pushed 2024-05-17); API spdx_id AGPL-3.0; README still states \"All code in this project is released under the AGPLv3 license\" — AGPL-3.0 stands; quarantine unchanged) — open-source video management/publishing platform with caption support |")

# 265 Adlib Tracker II (evidence refresh: README claim stale, per-file header now)
stamp(265,
 "| 265 | Adlib Tracker II | GPL-3.0-or-later (verified 2026-10-08: fork README of official sources states \"source codes are distributed under the GNU GPL 3+ license\" — ijsf/at2; GitHub API detection gap; Wave 31 Lane A) — classic DOS OPL2/OPL3 FM tracker |",
 "| 265 | Adlib Tracker II | GPL-3.0-or-later (verified 2026-10-08: fork README of official sources states \"source codes are distributed under the GNU GPL 3+ license\" — ijsf/at2; GitHub API detection gap; Wave 31 Lane A) (" + ST + ": CONFIRMED GPL-3.0-or-later — EVIDENCE REFRESH: ijsf/at2 current README carries no license statement (old README claim stale); per-file header adtrack2.pas: \"either version 3 of the License, or (at your option) any later version\" — GPL-3.0-or-later stands; quarantine unchanged) — classic DOS OPL2/OPL3 FM tracker |")

# 266 gbsplay
stamp(266,
 "| 266 | gbsplay | GPL-1.0-or-later (verified 2026-10-08: upstream README states GNU GPL v1 or any later version — mmitch/gbsplay; GitHub API returned NOASSERTION; Wave 31 Lane A) — Game Boy Sound (.gbs) music player |",
 "| 266 | gbsplay | GPL-1.0-or-later (verified 2026-10-08: upstream README states GNU GPL v1 or any later version — mmitch/gbsplay; GitHub API returned NOASSERTION; Wave 31 Lane A) (" + ST + ": CONFIRMED — mmitch/gbsplay live, not archived (pushed 2026-09-28); API still NOASSERTION; LICENCE = GPL v1 February 1989 text; README License section: \"Source Code licensed under GNU GPL v1 or, at your option, any later version\" — GPL-1.0-or-later stands; quarantine unchanged) — Game Boy Sound (.gbs) music player |")

# 267 sc68 — LICENSE CORRECTION: GPL-2.0-or-later -> GPL-3.0-or-later
stamp(267,
 "| 267 | sc68 | GPL-2.0-or-later (verified 2026-10-08 via third-party license audit; upstream re-verify before use; Wave 31 Lane A) — Atari ST .sc68 music player |",
 "| 267 | sc68 | GPL-3.0-or-later (" + ST + ": PRECISION CORRECTION — prior \"GPL-2.0-or-later\" claim from third-party audit was wrong; upstream evidence: SourceForge project sc68 License field \"License version 3.0 (GPLv3)\"; mirror Zeinok/sc68 (\"Atari ST and Amiga music player (SF Mirror)\") COPYING = GPL v3 29 June 2007 text (35,147 bytes), API spdx_id GPL-3.0; file68/src/file68.c header: \"either version 3 of the License, or (at your option) any later version\" — GPL-3.0-or-later confirmed; GPL family unchanged, quarantine treatment unchanged) — Atari ST .sc68 music player |")

# 268 psgplay
stamp(268,
 "| 268 | psgplay | GPL-2.0 (verified 2026-10-08 via third-party license audit; upstream re-verify before use — frno7/psgplay; Wave 31 Lane A) — Atari ST SNDH/PSG music player |",
 "| 268 | psgplay | GPL-2.0 (verified 2026-10-08 via third-party license audit; upstream re-verify before use — frno7/psgplay; Wave 31 Lane A) (" + ST + ": CONFIRMED — frno7/psgplay live, not archived (pushed 2026-09-08, branch main); sources carry \"SPDX-License-Identifier: GPL-2.0\" (REUSE-style licence/ dir); version 2 confirmed — GPL-2.0 stands (only/or-later unresolved from SPDX tag; both listed valid in licence/GPL-2.0 guide); quarantine unchanged) — Atari ST SNDH/PSG music player |")

# 269 vgmtools
stamp(269,
 "| 269 | vgmtools | GPL-2.0 (verified 2026-10-08 via GitHub API — vgmrips/vgmtools; Wave 31 Lane A) — VGM utility suite incl. vgm2mid |",
 "| 269 | vgmtools | GPL-2.0 (verified 2026-10-08 via GitHub API — vgmrips/vgmtools; Wave 31 Lane A) (" + ST + ": CONFIRMED — vgmrips/vgmtools live, not archived (pushed 2026-08-16); API spdx_id GPL-2.0; root LICENSE = GPL v2 June 1991 text (18,092 bytes, sha256 8177f975...) — GPL-2.0 stands; quarantine unchanged) — VGM utility suite incl. vgm2mid |")

# 270 ProTrackR2
stamp(270,
 "| 270 | ProTrackR2 | GPL-3.0-or-later (verified 2026-10-08: CRAN lists \"License GPL (>= 3)\"; Wave 31 Lane A) — R package for ProTracker MOD manipulation/playback |",
 "| 270 | ProTrackR2 | GPL-3.0-or-later (verified 2026-10-08: CRAN lists \"License GPL (>= 3)\"; Wave 31 Lane A) (" + ST + ": CONFIRMED — pepijn-devries/protrackr2 live, not archived (pushed 2025-11-20); API spdx_id GPL-3.0 (detection gap on -or-later); DESCRIPTION field \"License: GPL (>= 3)\" — GPL-3.0-or-later stands; quarantine unchanged) — R package for ProTracker MOD manipulation/playback |")

open(P, "w").write(txt)

# sanity: pipe counts
bad = []
for i, l in enumerate(txt.splitlines(), 1):
    if re.match(r"^\| \d+ \|", l) and l.count("|") != 8:
        bad.append((i, l.count("|")))
print("rows with pipe-count != 8:", bad if bad else "none")
print("stamps done")
