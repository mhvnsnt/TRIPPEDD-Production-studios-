#!/usr/bin/env python3
"""Wave 55 Lane B — stamp cycle-26 re-verification annotations into rows 271-280.
Row 272 also gets precision correction (GPL -> GPL-2.0) + canonical-move note.
No row numbers change. Pipe-safe.
"""
import re

P = "/home/hatch/workspace/agent-ops/wave55-lanes/w55b/docs/LICENSE_QUARANTINE.md"
txt = open(P).read()

def stamp(row, old_frag, new_frag):
    global txt
    assert txt.count(old_frag) == 1, f"frag not unique for row {row}: {old_frag[:60]!r}"
    txt = txt.replace(old_frag, new_frag)

ST = "re-verified Wave 55 Lane B, 2026-10-08"

# 271 Furnace (SUPERSEDED by row 122 — stamp still applies)
stamp(271,
 "| 271 | Furnace (tildearrow/furnace) | GPL-2.0-or-later (verified 2026-10-08: upstream README footnotes",
 "| 271 | Furnace (tildearrow/furnace) | GPL-2.0-or-later (" + ST + ": CONFIRMED — tildearrow/furnace live, not archived, pushed 2026-10-07T23:11:31Z (branch master), owner tildearrow; README still carries the grant \"redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version\" — GPL-2.0-or-later stands; quarantine unchanged; SUPERSEDED-by-row-122 pointer intact) (verified 2026-10-08: upstream README footnotes")

# 272 Open Cubic Player — precision correction GPL -> GPL-2.0 + canonical move
stamp(272,
 "| 272 | Open Cubic Player | GPL (verified 2026-10-08: upstream manual states the program source is covered under the GNU GPL; Wave 34 Lane A)",
 "| 272 | Open Cubic Player | GPL-2.0 (" + ST + ": PRECISION CORRECTION + CANONICAL MOVE — \"GPL\" precision was under-specified; SourceForge project opencubicplayer now redirects: SF REST API short_description states \"Moved repository to https://github.com/mywave82/opencubicplayer\"; canonical mywave82/opencubicplayer live, not archived, pushed 2026-08-24T08:42:09Z, owner mywave82; GitHub API spdx_id GPL-2.0; root COPYING = GNU GPL Version 2, June 1991 text (18,092 bytes) — GPL-2.0 confirmed; GPL family unchanged, quarantine treatment unchanged) (verified 2026-10-08: upstream manual states the program source is covered under the GNU GPL; Wave 34 Lane A)")

# 273 SubsAI
stamp(273,
 "GPL-3.0 (verified Wave 35 Lane B, 2026-10-08: GitHub API spdx_id absadiki/subsai = GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text; repo live, not archived, pushed 2026-04-20; 1,678 stars)",
 "GPL-3.0 (verified Wave 35 Lane B, 2026-10-08: GitHub API spdx_id absadiki/subsai = GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text; repo live, not archived, pushed 2026-04-20; 1,678 stars) (" + ST + ": CONFIRMED — absadiki/subsai live, not archived, pushed 2026-04-20T01:29:19Z (branch main), owner absadiki; GitHub API spdx_id GPL-3.0; raw LICENSE = GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007 text (35,149 bytes) — GPL-3.0 stands; quarantine unchanged)")

# 274 PyKaraoke
stamp(274,
 "LGPL-2.0 (verified Wave 36 Lane A, 2026-10-08: SourceForge license field \"GNU Library or Lesser General Public License version 2.0 (LGPLv2)\"; author Kelvin Lawson's mailing-list statement confirms LGPL was deliberately chosen to allow import into other apps)",
 "LGPL-2.0 (verified Wave 36 Lane A, 2026-10-08: SourceForge license field \"GNU Library or Lesser General Public License version 2.0 (LGPLv2)\"; author Kelvin Lawson's mailing-list statement confirms LGPL was deliberately chosen to allow import into other apps) (" + ST + ": CONFIRMED — SourceForge project pykaraoke live; project License field still \"License version 2.0 (LGPLv2)\" — LGPL-2.0 stands; quarantine unchanged; weak-copyleft doctrine still PENDING OWNER VERDICT)")

# 275 Lyriks
stamp(275,
 "| 275 | Lyriks (simon0302010/Lyriks) | GPL-3.0 (verified Wave 36 Lane A, 2026-10-08: GitHub API spdx_id GPL-3.0)",
 "| 275 | Lyriks (simon0302010/Lyriks) | GPL-3.0 (verified Wave 36 Lane A, 2026-10-08: GitHub API spdx_id GPL-3.0) (" + ST + ": CONFIRMED — simon0302010/Lyriks live, not archived, pushed 2025-07-09T06:15:31Z (branch main), owner simon0302010; GitHub API spdx_id GPL-3.0; raw LICENSE = GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007 text (35,149 bytes) — GPL-3.0 stands; quarantine unchanged)")

# 276 snes_spc (evidence path refreshed: slack.net page gone)
stamp(276,
 "LGPL-2.1 (verified Wave 36 Lane A, 2026-10-08: slack.net/~ant audio libraries page states GNU LGPL; fork READMEs pin \"LGPL 2.1 (see license.txt)\")",
 "LGPL-2.1 (verified Wave 36 Lane A, 2026-10-08: slack.net/~ant audio libraries page states GNU LGPL; fork READMEs pin \"LGPL 2.1 (see license.txt)\") (" + ST + ": CONFIRMED LGPL-2.1 — EVIDENCE-PATH NOTE: original slack.net/~ant/audio/libraries.html now 404s (author's old host gone); fresh confirmation from the live lineage repo libgme/game-music-emu (\"Blargg's video game music emulation library\", live, pushed 2026-09-08) — gme/ dir ships Snes_Spc.cpp/Spc_Dsp.cpp etc., root license.txt = GNU LESSER GENERAL PUBLIC LICENSE Version 2.1, February 1999 text (26,938 bytes) — LGPL-2.1 stands; quarantine unchanged; weak-copyleft doctrine still PENDING OWNER VERDICT)")

# 277 OpenKJ
stamp(277,
 "| 277 | OpenKJ (OpenKJ/OpenKJ) | GPL-3.0 (verified Wave 36 Lane A, 2026-10-08: GitHub API spdx_id GPL-3.0)",
 "| 277 | OpenKJ (OpenKJ/OpenKJ) | GPL-3.0 (verified Wave 36 Lane A, 2026-10-08: GitHub API spdx_id GPL-3.0) (" + ST + ": CONFIRMED — OpenKJ/OpenKJ live, not archived, pushed 2025-12-15T20:29:22Z (branch master), owner OpenKJ; GitHub API spdx_id GPL-3.0; raw LICENSE = GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007 text (35,141 bytes) — GPL-3.0 stands; quarantine unchanged)")

# 278 Capture2Text
stamp(278,
 "GPL-3.0 (verified Wave 36 Lane A, 2026-10-08: SourceForge license field \"GNU General Public License version 3.0 (GPLv3)\"; source headers carry GPL-3.0-or-later boilerplate)",
 "GPL-3.0 (verified Wave 36 Lane A, 2026-10-08: SourceForge license field \"GNU General Public License version 3.0 (GPLv3)\"; source headers carry GPL-3.0-or-later boilerplate) (" + ST + ": CONFIRMED — SourceForge project capture2text live; project License field still \"License version 3.0 (GPLv3)\" — GPL-3.0 stands; quarantine unchanged; MIT-rewrite disambiguation (paivikero/capture2text, unrelated) unaffected)")

# 279 GBDK-2020
stamp(279,
 "GPL-2.0+LE (verified Wave 37 Lane A, 2026-10-08: LICENSE file — library/SDCC parts GPLv2 with linking exception; compiled ROM binaries explicitly exempt from license/credit requirements)",
 "GPL-2.0+LE (verified Wave 37 Lane A, 2026-10-08: LICENSE file — library/SDCC parts GPLv2 with linking exception; compiled ROM binaries explicitly exempt from license/credit requirements) (" + ST + ": CONFIRMED — gbdk-2020/gbdk-2020 live, not archived, pushed 2026-10-06T23:31:25Z (branch develop), owner gbdk-2020; LICENSE (3,456 bytes) = \"Overview of Licenses in GBDK-2020\" — For the End User Q&A: \"There is no requirement to include or credit any of the GBDK-2020 licenses or authors\" for compiled ROM binaries; see LICENSES folder for grant details — GPL-2.0-with-linking-exception stands; quarantine unchanged)")

# 280 devkitSMS
stamp(280,
 "GPL-2.0+exception (verified Wave 37 Lane A, 2026-10-08: LICENSES.txt — libraries public domain/Unlicense; crt0 startup GPLv2 with special exception)",
 "GPL-2.0+exception (verified Wave 37 Lane A, 2026-10-08: LICENSES.txt — libraries public domain/Unlicense; crt0 startup GPLv2 with special exception) (" + ST + ": CONFIRMED — sverx/devkitSMS live, not archived, pushed 2026-09-29T16:08:29Z (branch master), owner sverx; LICENSES.txt (1,332 bytes): \"devkitSMS/crt0/crt0_sms.s is licensed under GPL2 with a special exception\"; ihx2sms public domain — GPL-2.0-with-exception stands; quarantine unchanged)")

open(P, "w").write(txt)

# sanity: pipe counts on row lines
bad = []
for i, l in enumerate(txt.splitlines(), 1):
    if re.match(r"^\| \d+ \|", l) and l.count("|") != 8:
        bad.append((i, l.count("|")))
print("rows with pipe-count != 8:", bad if bad else "none")
print("stamps done")
