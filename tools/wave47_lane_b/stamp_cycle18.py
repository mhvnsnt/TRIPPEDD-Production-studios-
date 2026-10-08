#!/usr/bin/env python3
"""Stamp Wave 47 Lane B cycle-18 re-verification notes into the license cell
of rows 183, 184, 186-193 in docs/LICENSE_QUARANTINE.md."""
import re, sys

P = '/home/hatch/workspace/agent-ops/wave47-lanes/lane-b/docs/LICENSE_QUARANTINE.md'

NOTES = {
183: "(re-verified Wave 47 Lane B, 2026-10-08: rism-digital/verovio live, not archived (pushed 2026-10-08); API spdx_id LGPL-3.0; raw master/COPYING = GPL v3 text AND master/COPYING.LESSER = LGPL v3 text; README carries LGPL-v3 badge + license note — LGPL-3.0 stands; LGPL doctrine still pending owner verdict, quarantine unchanged)",
184: "(re-verified Wave 47 Lane B, 2026-10-08: libgme/game-music-emu live, not archived (pushed 2026-09-08); API spdx_id LGPL-2.1; raw master/license.txt = 'GNU LESSER GENERAL PUBLIC LICENSE Version 2.1, February 1999' — LGPL-2.1 stands; LGPL doctrine still pending owner verdict, quarantine unchanged)",
186: "(re-verified Wave 47 Lane B, 2026-10-08: zrythm/zrythm live, not archived (pushed 2026-10-04); API spdx_id NOASSERTION (REUSE scheme with LicenseRef-* texts, detection gap); raw LICENSES/LicenseRef-ZrythmLicense.txt (35,717 bytes) = AGPL-3.0 + 'Additional terms under Section 7 of the GNU AGPL' trademark terms — AGPL-3.0 + Section-7 trademark terms stand; quarantine unchanged)",
187: "(re-verified Wave 47 Lane B, 2026-10-08: SourceForge project page live, license field 'GNU General Public License version 2.0 (GPLv2)' — GPLv2 stands; quarantine unchanged)",
188: "(re-verified Wave 47 Lane B, 2026-10-08: mirrors nengxu/rosegarden (stale, pushed 2014-04-25) and tedfelix/rosegarden-official (active, pushed 2026-10-05) both live, not archived, API spdx_id GPL-2.0 on both; raw COPYING on both mirrors = 'GNU GENERAL PUBLIC LICENSE Version 2, June 1991'; rosegardenmusic.com live — GPL-2.0 stands; quarantine unchanged)",
189: "(re-verified Wave 47 Lane B, 2026-10-08: iina/iina live, not archived (pushed 2026-10-08); API spdx_id GPL-3.0; raw develop/LICENSE = GPL v3 29 June 2007 text — GPL-3.0 stands; quarantine unchanged)",
190: "(re-verified Wave 47 Lane B, 2026-10-08: smplayer-dev/smplayer live, not archived (pushed 2026-10-06); API spdx_id GPL-2.0; raw master/Copying.txt = 'GNU GENERAL PUBLIC LICENSE Version 2, June 1991' — GPL-2.0 stands; quarantine unchanged)",
191: "(re-verified Wave 47 Lane B, 2026-10-08: mpc-hc/mpc-hc now archived (pushed 2020-04-24) — archived-status note NEW vs original annotation; API spdx_id GPL-3.0; raw master/COPYING.txt = GPL v3 29 June 2007 text — GPL-3.0 stands; quarantine unchanged)",
192: "(re-verified Wave 47 Lane B, 2026-10-08: SourceForge project page live, license field 'GNU General Public License version 3.0 (GPLv3)' — GPLv3 stands; quarantine unchanged)",
193: "(re-verified Wave 47 Lane B, 2026-10-08: celluloid-player/celluloid live, not archived (pushed 2026-10-04); API spdx_id GPL-3.0; raw master/COPYING = GPL v3 29 June 2007 text — GPL-3.0 stands; quarantine unchanged)",
}

lines = open(P).read().split('\n')
count = 0
for i, ln in enumerate(lines):
    m = re.match(r'^\| (\d+) \|', ln)
    if m and int(m.group(1)) in NOTES:
        row = int(m.group(1))
        assert 're-verified Wave 47 Lane B' not in ln, f'row {row} already stamped!'
        # license cell is the 3rd column; find 2nd and 3rd '|' boundaries
        cells = ln.split('|')
        # cells[0]='' cells[1]=' 183 ' cells[2]=' license ... ' cells[3]=' music '
        assert len(cells) >= 5, f'unexpected shape row {row}'
        cells[2] = cells[2].rstrip() + ' ' + NOTES[row] + ' '
        lines[i] = '|'.join(cells)
        count += 1
assert count == len(NOTES), f'stamped {count}, expected {len(NOTES)}'
open(P, 'w').write('\n'.join(lines))
print(f'stamped {count} rows')
