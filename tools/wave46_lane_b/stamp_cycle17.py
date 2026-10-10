#!/usr/bin/env python3
"""Wave 46 Lane B — stamp cycle-17 re-verifications into docs/LICENSE_QUARANTINE.md.

Convention (cycle 16): append '(re-verified Wave 46 Lane B, 2026-10-08: ...)'
to the audit-status column of each table row 173-182. Row 403 gets the
SUPERSEDED-by-174 dedup marker in its License column (Furnace-row-271 format).
"""
import re, sys

P = "docs/LICENSE_QUARANTINE.md"
lines = open(P).read().split("\n")

STAMPS = {
    173: ("re-verified Wave 46 Lane B, 2026-10-08: BambooTracker/BambooTracker live, not archived, "
          "pushed 2026-09-13 (active), default branch master; GitHub API spdx_id GPL-2.0 = detection gap "
          "on the -or-later README clause; raw LICENSE = GPL v2 June 1991 text (18,092 bytes) containing "
          "the standard 'any later version' clause; README license badge 'GPL-2.0 or later' (shields.io "
          "GPL--2.0%2B, alt text 'BambooTracker License: GPL-2.0 or later') — GPL-2.0-or-later stands; "
          "quarantine unchanged"),
    174: ("re-verified Wave 46 Lane B, 2026-10-08: HertzDevil/0CC-FamiTracker live, not archived, "
          "pushed 2026-03-18, default branch master; GitHub API spdx_id GPL-2.0 (license path LICENSE.txt); "
          "raw LICENSE.txt = GPL v2 June 1991 text (18,351 bytes) — GPL-2.0 stands. PRECISION FIX: the "
          "Wave-18 '404 / repo moved' note probed account spelling 'HertzDev' (no 'il') — the row's NAMED "
          "upstream HertzDevil/0CC-FamiTracker resolves live today (HTTP 200). nyanpasu64/0CC-FamiTracker "
          "(Wave-18's proposed continuation) also live, pushed 2021-09-14, API spdx_id GPL-2.0, raw LICENSE.txt "
          "18,351 bytes = GPL v2 text — both references GPL-2.0, quarantine unchanged. DEDUP: row 403 "
          "(Wave 45 Lane A) marked SUPERSEDED by this row — same upstream project HertzDevil/0CC-FamiTracker; "
          "Lane A's dedup scan missed it because Wave-18 prose had redirected this row's reference to nyanpasu64"),
    175: ("re-verified Wave 46 Lane B, 2026-10-08: kmatheussen/radium live, not archived, pushed 2026-10-07 "
          "(active), default branch master; GitHub API spdx_id GPL-2.0; raw COPYING = GPL v2 June 1991 text "
          "(17,982 bytes) — GPL-2.0 stands; quarantine unchanged"),
    176: ("re-verified Wave 46 Lane B, 2026-10-08: leafo/goattracker2 mirror live, not archived, pushed "
          "2022-11-21, default branch master; GitHub API spdx_id GPL-2.0 (license path 'copying'); raw copying "
          "file = GPL v2 June 1991 text (17,992 bytes) — GPL-2.0 stands; canonical cadaver/goattracker still "
          "404 (unchanged); quarantine unchanged"),
    177: ("re-verified Wave 46 Lane B, 2026-10-08: musescore/MuseScore live, not archived, pushed 2026-10-08 "
          "(active), default branch main; GitHub API spdx_id NOASSERTION ('Other') = detection gap; raw "
          "LICENSE.txt 36,493 bytes opens with the MuseScore GPL v3 grant ('This program is free software; "
          "you can redistribute it and/or modify it under the terms of the GNU General Public License "
          "version 3') — GPL-3.0 stands; quarantine unchanged"),
    178: ("re-verified Wave 46 Lane B, 2026-10-08: lilypond/lilypond GitHub mirror live, not archived, pushed "
          "2026-10-08 (active), default branch master; GitHub API spdx_id NOASSERTION ('Other') = detection gap; "
          "raw COPYING = GPL v3 29 June 2007 text (35,147 bytes) with 'any later version' clause — "
          "GPL-3.0-or-later stands; quarantine unchanged"),
    179: ("re-verified Wave 46 Lane B, 2026-10-08: frescobaldi/frescobaldi live, not archived, pushed "
          "2026-09-06 (active), default branch master; GitHub API spdx_id GPL-2.0; raw LICENSE = GPL v2 "
          "June 1991 text (18,008 bytes) — GPL-2.0 stands; quarantine unchanged"),
    180: ("re-verified Wave 46 Lane B, 2026-10-08: denemo/denemo live, not archived, pushed 2022-04-29 "
          "(stale but license intact), default branch master; GitHub API spdx_id GPL-3.0; raw COPYING = GPL v3 "
          "text (35,147 bytes) — GPL-3.0 stands; quarantine unchanged"),
    181: ("re-verified Wave 46 Lane B, 2026-10-08: Abjad/abjad live, not archived, pushed 2025-12-15, "
          "default branch main; GitHub API spdx_id GPL-3.0; raw LICENSE = GPL v3 text (35,150 bytes) — "
          "GPL-3.0 stands; quarantine unchanged"),
    182: ("re-verified Wave 46 Lane B, 2026-10-08: bspaans/python-mingus live, not archived, pushed "
          "2024-04-21, default branch master; GitHub API spdx_id GPL-3.0; raw LICENSE = GPL v3 text "
          "(32,473 bytes, grant text present) — GPL-3.0 stands; quarantine unchanged"),
}

ROW403_SUPERSEDE = (" **SUPERSEDED by row 174** (same upstream project HertzDevil/0CC-FamiTracker; "
                   "duplicate row added Wave 45 Lane A — Wave 46 Lane B dedup, 2026-10-08: row 174's row text "
                   "names HertzDevil/0CC-FamiTracker and the repo is live (not archived, pushed 2023-03-18, "
                   "API spdx_id GPL-2.0); Lane A's dedup scan missed it because Wave-18 prose had redirected "
                   "row 174's reference to the nyanpasu64 fork — see dedup mapping)")

def table_line(n):
    return re.compile(r"^\| %d \|" % n)

changed = []
for i, ln in enumerate(lines):
    for n, stamp in STAMPS.items():
        if table_line(n).match(ln):
            if "re-verified Wave 46 Lane B" in ln:
                continue  # idempotent
            assert ln.rstrip().endswith("| PENDING |"), f"row {n} audit col unexpected"
            lines[i] = ln.rstrip()[:-len("| PENDING |")] + f"| PENDING ({stamp}) |"
            changed.append(n)
    if table_line(403).match(ln):
        if "SUPERSEDED by row 174" not in ln:
            # insert into License column right after the license claim text
            lines[i] = ln.replace(" GPL-2.0 (verified Wave 45 Lane A,",
                                  ROW403_SUPERSEDE + " GPL-2.0 (verified Wave 45 Lane A,")
            changed.append(403)

assert set(STAMPS) <= set(changed), f"missing stamps: {set(STAMPS) - set(changed)}"
assert 403 in changed, "row 403 not marked"
open(P, "w").write("\n".join(lines))
print("stamped rows:", sorted(changed))
