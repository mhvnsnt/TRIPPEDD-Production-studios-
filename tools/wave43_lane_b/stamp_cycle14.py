#!/usr/bin/env python3
"""Wave 43 Lane B — stamp cycle-14 re-verification + drift-watch into the table.
Appends stamps to the license cell (column 3) of each target row.
Rows 134-140 are rights-restricted (no license cell change to classification).
"""
import re, sys

PATH = "/home/hatch/workspace/agent-ops/wave43-lanes/lane-b/docs/LICENSE_QUARANTINE.md"

STAMPS = {
    # (a) cycle-11 gap — fresh upstream re-checks 2026-10-08
    61:  "(re-verified Wave 43, 2026-10-08: dimkanovikov/KITScenarist live, GitHub API spdx_id GPL-3.0, raw license 35,149 bytes; NOTE repo now owner-archived, pushed 2023-08-01 — GPL-3.0 stands; quarantine unchanged)",
    168: "(re-verified Wave 43, 2026-10-08: tautcony/ChapterTool live, GitHub API spdx_id GPL-3.0, raw license 32,472 bytes, pushed 2026-10-08 (active) — GPL-3.0 stands; quarantine unchanged)",
    199: "(re-verified Wave 43, 2026-10-08: rjungemann/mml2vgm live, GitHub API spdx_id GPL-3.0, raw LICENSE.txt 35,148 bytes, pushed 2026-06-14 — GPL-3.0 stands; quarantine unchanged)",
    200: "(re-verified Wave 43, 2026-10-08: SudoMaker/TinyVGM live, GitHub API spdx_id AGPL-3.0, raw LICENSE 34,523 bytes, pushed 2023-06-25 — AGPL-3.0 stands; quarantine unchanged)",
    208: "(re-verified Wave 43, 2026-10-08: unpaper/unpaper live (pushed 2024-07-11); GitHub API spdx_id null — REUSE scheme, no top-level LICENSE file; README (3,261 bytes, fetched) carries SPDX-License-Identifier: GPL-2.0-only + 'The entire unpaper project is licensed under GNU GPL v2' — GPL-2.0-only stands; quarantine unchanged)",
    211: "(re-verified Wave 43, 2026-10-08: internetarchive/bookreader live, GitHub API spdx_id AGPL-3.0, raw license 34,520 bytes, pushed 2026-10-07 — AGPL-3.0 stands; quarantine unchanged)",
    212: "(re-verified Wave 43, 2026-10-08: openslide/openslide live, GitHub API spdx_id now LGPL-2.1 (COPYING.LESSER = LGPL v2.1 text, 26,419 bytes, pushed 2026-10-04) — API now agrees with the row's LGPL-2.1 claim; NOT a relicense; stays quarantined — LGPL doctrine pending owner verdict)",
    213: "(re-verified Wave 43, 2026-10-08: spotify/pedalboard live, GitHub API spdx_id GPL-3.0, raw license 35,149 bytes, pushed 2026-10-07 — GPL-3.0 stands; quarantine unchanged)",
    214: "(re-verified Wave 43, 2026-10-08: sergree/matchering live, GitHub API spdx_id GPL-3.0, raw license 35,149 bytes, pushed 2026-10-07 — GPL-3.0 stands; quarantine unchanged)",
    # (b) cycle 14 — rows 134-143
    134: "(re-verified Wave 43, 2026-10-08: HathiTrust catalog record LIVE (live page render; bot fetch 403) — Use and Reproduction Note still 'may not be reproduced for any reason without the express written consent of the Hennepin County Library' — rights-restricted stands; reference only)",
    135: "(re-verified Wave 43, 2026-10-08: Austin History Center Reproduction Policies page LIVE (live page render; bot fetch 403) — one-time-use-only, written permission required, no alteration without special permission, use fees — terms unchanged; rights-restricted stands)",
    136: "(re-verified Wave 43, 2026-10-08: Center for Sacramento History 'Using our collections' page live (200) — use fees still $10-$200/image + scanning fees — terms unchanged; rights-restricted stands)",
    137: "(re-verified Wave 43, 2026-10-08: Arizona Memory Project item page live (200) — 'Copyright and/or publication rights ... retained by this institution', permission required for re-use — terms unchanged; rights-restricted stands)",
    138: "(re-verified Wave 43, 2026-10-08: Maryland State Archives use page live (200) — 'Permission is required for any and all materials'; fee schedule $75 commercial / $150 front cover — terms unchanged; rights-restricted stands)",
    139: "(re-verified Wave 43, 2026-10-08: CPL Digital Collections copyright text current at cpldc/cpldc-jekyll HEAD — reproduction of protected items 'requires the written permission of the copyright owners', no PD statement — terms unchanged; rights-restricted stands)",
    140: "(re-verified Wave 43, 2026-10-08: kingcounty.gov terms unchanged per current crawl — 'no one is permitted to sell this information except in accordance with a written agreement with King County'; direct EN-page fetch failed (empty body), no evidence of change — rights-restricted stands)",
    141: "(re-verified Wave 43, 2026-10-08: cvqluu/simple_diarizer live, GitHub API spdx_id GPL-3.0, raw license 35,144 bytes, pushed 2024-05-02 — GPL-3.0 stands; quarantine unchanged)",
    142: "(re-verified Wave 43, 2026-10-08: LibreTranslate/LibreTranslate live, GitHub API spdx_id AGPL-3.0, raw license 34,523 bytes, pushed 2026-09-28 — AGPL-3.0 stands; quarantine unchanged)",
    143: "(re-verified Wave 43, 2026-10-08: UlionTse/translators live, GitHub API spdx_id GPL-3.0, raw license 35,148 bytes, pushed 2026-01-26 — GPL-3.0 stands; quarantine unchanged)",
    # (c) identity-drift watch
    68:  "(drift watch Wave 43 Lane B, 2026-10-08: mtytel/helm STILL owner-archived, pushed 2022-09-24T04:23:20Z — unchanged; ownership unchanged (mtytel); GitHub API spdx_id GPL-3.0; raw COPYING 35,147 bytes; no official successor, no ownership change, no relicense; quarantine unchanged)",
    155: "(drift watch Wave 43 Lane B, 2026-10-08: codeberg.org/mbunkus/mkvtoolnix still canonical (Codeberg API 200), owner mbunkus, not archived, pushed 2026-09-28; raw COPYING on branch main = GPL v2 June 1991 text (18,092 bytes — byte-identical to Wave 41/42 checks) — no further host moves, no relicense; GPL-2.0-or-later stands; quarantine unchanged)",
    236: "(drift watch Wave 43 Lane B, 2026-10-08: kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z — unchanged, owner kanongil); GitHub API spdx_id NOASSERTION (detection gap); raw LICENSE re-fetched (2,091 bytes): '-or-later' boilerplate intact — no successor, no relicense; GPL-2.0-or-later stands; quarantine unchanged)",
}

lines = open(PATH).read().splitlines(keepends=False)
stamped = 0
problems = []
for i, ln in enumerate(lines):
    m = re.match(r"^\| (\d+) \|", ln)
    if not m:
        continue
    n = int(m.group(1))
    if n not in STAMPS:
        continue
    parts = ln.split(" | ")
    if len(parts) not in (6, 7) or parts[0] != f"| {n}":
        problems.append(f"row {n}: split={len(parts)} (expected 6|7) — NOT stamped")
        continue
    # license cell is index 2 in both shapes (drift rows glue it to "| synth")
    if "Wave 43" in parts[2]:
        problems.append(f"row {n}: already has a Wave 43 stamp — skipped")
        continue
    parts[2] = parts[2] + " " + STAMPS[n]
    lines[i] = " | ".join(parts)
    stamped += 1

open(PATH, "w").write("\n".join(lines) + "\n")
print(f"stamped={stamped} expected={len(STAMPS)}")
for p in problems:
    print("PROBLEM:", p)
sys.exit(0 if (stamped == len(STAMPS) and not problems) else 1)
