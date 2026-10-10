#!/usr/bin/env python3
"""Wave 56 Lane B — stamp cycle-27 re-verification notes into rows 281-290
and drift-watch notes into rows 68/118/155/191/195/206/236/243/253 (+101 note
inside row 101 handled as text). No row content otherwise changed."""
import re

P = "docs/LICENSE_QUARANTINE.md"
lines = open(P).read().split("\n")

CYCLE27 = {
 281: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — Lameguy64/PSn00bSDK live, not archived, pushed 2025-01-28; GitHub API NOASSERTION = detection gap; raw LICENSE.md (76,885 bytes) = full MPL-2.0 text ("licensed under the MPL 2.0 ... use the SDK in a closed-source project (larger work) but requires you to share [changes]") — MPL-2.0 stands; quarantine unchanged)',
 282: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — Lameguy64/mkpsxiso live, not archived, pushed 2026-07-09; GitHub API spdx_id GPL-2.0; /license endpoint LICENSE.md (18,431 bytes) = GPL v2 text — GPL-2.0 stands; quarantine unchanged)',
 283: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — vhelin/wla-dx live, not archived, pushed 2026-10-07; GitHub API NOASSERTION = detection gap (SPDX-styled license file); raw LICENSE (18,849 bytes) carries "Valid-License-Identifier: GPL-2.0-or-later" + "either version 2 of the License, or (at your option) any later version" x3 — GPL-2.0-or-later stands; quarantine unchanged)',
 284: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — batari-Basic/batari-Basic live, not archived, pushed 2026-01-08; GitHub API NOASSERTION = detection gap; raw LICENSE.txt (22,888 bytes): "The batari Basic language source code is provided under the GPL v2 license" + auto-generated 6507 assembly CC0 — GPL-2.0 stands, games-exempt note intact; quarantine unchanged)',
 285: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — dasm-assembler/dasm live, not archived, pushed 2026-07-07; GitHub API spdx_id GPL-2.0; /license endpoint LICENSE (17,987 bytes) = GPL v2 text — GPL-2.0 stands; quarantine unchanged)',
 286: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — 7800-devtools/7800basic live, not archived, pushed 2026-09-24; GitHub API NOASSERTION = detection gap; raw LICENSE.txt (48,866 bytes): "language source GPL v2; included/generated 6502 assembly CC0" header + GPL v2 + LGPL v2.1 + CC0 texts — GPL-2.0 stands; quarantine unchanged)',
 287: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — aoineko-fr/MSXgl live, not archived, pushed 2026-10-03; GitHub API spdx_id CC-BY-SA-4.0; /license endpoint LICENSE.md (20,137 bytes) = CC BY-SA 4.0 text — CC-BY-SA-4.0 stands; share-alike bar intact; quarantine unchanged)',
 288: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — lronaldo/cpctelera live, not archived, pushed 2026-05-06; GitHub API spdx_id LGPL-3.0; /license endpoint LICENSE (7,650 bytes) = LGPL v3 additional-permissions text — LGPL-3.0 stands; quarantine unchanged)',
 289: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — dciabrin/ngdevkit live, not archived, pushed 2026-07-19; GitHub API spdx_id LGPL-3.0; raw COPYING (35,147 bytes) = GPL v3 text (expected: LGPL v3 incorporates GPL v3 per sec.0); README badge + grant "GNU Lesser General Public License" — LGPL-3.0 stands; quarantine unchanged)',
 290: '(re-verified Wave 56 Lane B, 2026-10-08: CONFIRMED — AzuraCast/AzuraCast live, not archived, pushed 2026-10-05; GitHub API spdx_id AGPL-3.0; raw LICENSE.md (34,283 bytes) = "GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007" — AGPL-3.0 stands; quarantine unchanged)',
}

DRIFT = {
 68: '(drift watch Wave 56 Lane B, 2026-10-08: mtytel/helm STILL owner-archived (pushed 2022-09-24T04:23:20Z — unchanged; owner mtytel; API spdx_id GPL-3.0; COPYING 35,147 bytes = GPL v3 text) — no successor, no ownership change, no relicense; quarantine unchanged)',
 118: '(drift watch Wave 56 Lane B, 2026-10-08: animate1978/MB-Lab STILL owner-archived (pushed 2024-07-21T02:46:17Z — unchanged, owner unchanged; API NOASSERTION detection gap; license.txt 3,519 bytes, GPL-3.0 grant intact) — no relicense; quarantine unchanged)',
 155: '(drift watch Wave 56 Lane B, 2026-10-08: codeberg.org/mbunkus/mkvtoolnix still canonical (Codeberg API 200), owner mbunkus, not archived, updated 2026-09-28; raw COPYING on branch main = GPL v2 June 1991 text (18,092 bytes — BYTE-IDENTICAL to Wave 41/42/43/45/49/53/55 checks) — no host moves, no relicense; GPL-2.0-or-later composite stands; quarantine unchanged)',
 191: '(drift watch Wave 56 Lane B, 2026-10-08: mpc-hc/mpc-hc STILL owner-archived (pushed 2020-04-24T11:04:40Z — unchanged, owner mpc-hc; API spdx_id GPL-3.0; COPYING.txt 35,147 bytes) — GPL-3.0 stands; quarantine unchanged)',
 195: '(drift watch Wave 56 Lane B, 2026-10-08: subdownloader/subdownloader STILL owner-archived (pushed 2025-02-05T11:39:33Z — unchanged, owner unchanged; API spdx_id GPL-3.0; COPYING 32,472 bytes) — GPL-3.0 stands; quarantine unchanged)',
 206: '(drift watch Wave 56 Lane B, 2026-10-08: scantailor/scantailor STILL owner-archived (pushed 2020-11-29T04:31:29Z — unchanged, owner scantailor; API NOASSERTION detection gap; raw COPYING 464 bytes = GPL-3.0-or-later grant) — GPL-3.0-or-later stands; quarantine unchanged)',
 236: '(drift watch Wave 56 Lane B, 2026-10-08: kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z — unchanged, owner kanongil; API NOASSERTION detection gap; raw LICENSE 2,091 bytes, "-or-later" boilerplate intact) — no successor, no relicense; quarantine unchanged)',
 243: '(drift watch Wave 56 Lane B, 2026-10-08: tidalcycles/strudel STILL owner-archived (pushed 2025-06-19T15:56:31Z — unchanged, owner tidalcycles; API spdx_id AGPL-3.0; LICENSE 34,523 bytes) — AGPL-3.0 stands; quarantine unchanged)',
 253: '(drift watch Wave 56 Lane B, 2026-10-08: sc0ty/subSync STILL owner-archived (pushed 2024-10-01T13:47:06Z — unchanged, owner sc0ty; API spdx_id GPL-3.0; LICENSE 35,149 bytes) — GPL-3.0 stands; quarantine unchanged)',
}

def stamp(lines, row, note, anchor):
    """Insert note right after the closing paren of anchor's verification annotation."""
    for i, ln in enumerate(lines):
        if re.match(rf"^\| {row} \|", ln) and anchor in ln:
            j = ln.index(anchor)
            k = ln.index(")", j)
            lines[i] = ln[:k+1] + " " + note + ln[k+1:]
            print(f"stamped row {row} line {i+1}")
            return
    raise SystemExit(f"anchor not found for row {row}")

for row, note in CYCLE27.items():
    stamp(lines, row, note, "verified Wave 37 Lane A, 2026-10-08:")

# drift anchors: use a unique, already-present marker per row
drift_anchors = {
 68: "GitHub API spdx_id mtytel/helm",
 118: "license.txt",
 155: "Wave 53 Lane B, 2026-10-08: codeberg.org/mbunkus/mkvtoolnix",
 191: "mpc-hc/mpc-hc now archived",
 195: "NOW OWNER-ARCHIVED",
 206: "NOW OWNER-ARCHIVED",
 236: "now ARCHIVED by the owner",
 243: "NOW OWNER-ARCHIVED",
 253: "repo now owner-archived",
}
for row, note in DRIFT.items():
    stamp(lines, row, note, drift_anchors[row])

# uzu/tidal lives in the row-101 drift note area; anchor on the Wave-49 note tail
note101 = "(drift watch Wave 56 Lane B, 2026-10-08: codeberg.org/uzu/tidal still live (Codeberg API 200), owner uzu, not archived, updated 2026-07-02T08:30:35+02:00; raw LICENSE on branch main = GPL v3 text (35,106 bytes — BYTE-IDENTICAL to Wave 38/41/42/43/45/47/48/49/50/53/55 checks) — GPL-3.0 stands; tidalcycles/Tidal unchanged; quarantine unchanged)"
for i, ln in enumerate(lines):
    if re.match(r"^\| 101 \|", ln):
        anchor = "(35,106 bytes) — GPL-3.0 stands; no relicense; quarantine unchanged)"
        j = ln.index(anchor) + len(anchor)
        lines[i] = ln[:j] + " " + note101 + ln[j:]
        print(f"stamped row 101 line {i+1}")
        break
else:
    raise SystemExit("row 101 anchor not found")

open(P, "w").write("\n".join(lines))
print("done")
