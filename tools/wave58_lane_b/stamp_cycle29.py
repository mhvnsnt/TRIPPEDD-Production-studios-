#!/usr/bin/env python3
"""Stamp Wave 58 Lane B cycle-29 re-verification notes into LICENSE_QUARANTINE.md rows 301-310,
and insert the cycle header note before the Wave 57 blockquote. Idempotent-ish: skips rows already
carrying a Wave-58 stamp."""
import re

PATH = "docs/LICENSE_QUARANTINE.md"

STAMPS = {
 301: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — sourcefabric/airtime live, not archived, pushed 2021-07-14; GitHub API spdx_id AGPL-3.0; raw LICENSE (34,520 bytes) = "GNU AFFERO GENERAL PUBLIC LICENSE Version 3, 19 November 2007" — AGPL-3.0 stands; quarantine unchanged)',
 302: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — taigaio/taiga-back live, not archived, pushed 2026-09-28; GitHub API spdx_id MPL-2.0; raw LICENSE (16,725 bytes) = Mozilla Public License Version 2.0 — MPL-2.0 stands (AGPL-to-MPL relicense already recorded, no new change); quarantine unchanged)',
 303: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — artraweditor/ART live, not archived, pushed 2026-10-07; GitHub API NOASSERTION = detection gap (custom LICENSE.txt header); raw LICENSE.txt (33,345 bytes) = "ART is free software ... under the terms of the GNU General Public License ... either version 3 of the License, or (at your option) any later version" + full GPL v3 text ("Version 3, 29 June 2007") — GPL-3.0 stands; quarantine unchanged)',
 304: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — ggarra13/mrviewer live, not archived, pushed 2024-01-26; GitHub /license endpoint 404 = detection gap (grant file is docs/LICENSE.txt, not root); raw docs/LICENSE.txt (18,092 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" — GPL-2.0 stands; quarantine unchanged)',
 305: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — beku/Argyll-Releases live, not archived, pushed 2016-02-24; GitHub API spdx_id AGPL-3.0; raw License.txt (34,521 bytes) = AGPL v3 text — AGPL-3.0 stands; quarantine unchanged)',
 306: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — eoyilmaz/displaycal-py3 live, not archived, pushed 2026-07-29; GitHub API spdx_id GPL-3.0; raw LICENSE.txt (35,147 bytes) = GPL v3 text — GPL-3.0 stands; quarantine unchanged)',
 307: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — LuminanceHDR/LuminanceHDR live, not archived, pushed 2026-05-20; GitHub API spdx_id GPL-2.0; raw LICENSE (17,984 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" — GPL-2.0 stands; quarantine unchanged)',
 308: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — videolan/x265 live, not archived, pushed 2023-09-11; GitHub API spdx_id GPL-2.0; raw COPYING (18,120 bytes) = GPL v2 June 1991 text (18,120 vs canonical 18,092 = formatting-only difference) — GPL-2.0 stands; quarantine unchanged)',
 309: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — aqsis/aqsis live, not archived, pushed 2025-08-22; GitHub API spdx_id GPL-2.0; raw COPYING (17,992 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" — GPL-2.0 stands; quarantine unchanged)',
 310: '(re-verified Wave 58 Lane B, 2026-10-08: CONFIRMED — aferrero2707/PhotoFlow live, not archived, pushed 2021-02-05; GitHub API spdx_id GPL-3.0; raw LICENSE (35,121 bytes) = GPL v3 text — GPL-3.0 stands; quarantine unchanged)',
}

HEADER_NOTE = (
"> Wave 58 Lane B re-verification cycle (2026-10-08): TWENTY-NINTH re-verification cycle — "
"rows 301–310 (the NEXT 10 lowest-numbered live rows with bare-date \"(verified Wave 38 Lane A, 2026-10-08)\" "
"annotations and no wave-era re-verification stamp). Fresh upstream checks (GitHub API spdx_id + archived + pushed_at + owner; "
"/license endpoint content fetches; raw LICENSE/LICENSE.txt/License.txt/COPYING/docs/LICENSE.txt byte-count fetches — never assumed; "
"NOASSERTION + license-endpoint-404 treated as detection gaps, always resolved by direct text reads), "
"via `tools/wave58_lane_b/cycle29_verify.py` + `tools/wave58_lane_b/stamp_cycle29.py`: "
"rows 301 (Airtime, AGPL-3.0 — live, pushed 2021-07-14; API spdx_id AGPL-3.0; raw LICENSE 34,520 bytes = AGPL v3 text), "
"302 (Taiga, MPL-2.0 — live, pushed 2026-09-28; API spdx_id MPL-2.0; raw LICENSE 16,725 bytes = MPL 2.0 text; no new relicense), "
"303 (ART, GPL-3.0 — live, pushed 2026-10-07; API NOASSERTION detection gap (custom license-header preamble); raw LICENSE.txt 33,345 bytes = GPL v3 text), "
"304 (mrViewer, GPL-2.0 — live, pushed 2024-01-26; /license endpoint 404 detection gap (grant file is docs/LICENSE.txt); raw 18,092 bytes = GPL v2 June 1991 text), "
"305 (ArgyllCMS, AGPL-3.0 — live, pushed 2016-02-24; API spdx_id AGPL-3.0; raw License.txt 34,521 bytes = AGPL v3 text), "
"306 (DisplayCAL, GPL-3.0 — live, pushed 2026-07-29; API spdx_id GPL-3.0; raw LICENSE.txt 35,147 bytes = GPL v3 text), "
"307 (LuminanceHDR, GPL-2.0 — live, pushed 2026-05-20; API spdx_id GPL-2.0; raw LICENSE 17,984 bytes = GPL v2 June 1991 text), "
"308 (x265, GPL-2.0 — live, pushed 2023-09-11; API spdx_id GPL-2.0; raw COPYING 18,120 bytes = GPL v2 text, formatting-only size diff), "
"309 (Aqsis, GPL-2.0 — live, pushed 2025-08-22; API spdx_id GPL-2.0; raw COPYING 17,992 bytes = GPL v2 June 1991 text), "
"310 (PhotoFlow, GPL-3.0 — live, pushed 2021-02-05; API spdx_id GPL-3.0; raw LICENSE 35,121 bytes = GPL v3 text). "
"**Result: 10/10 CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes, zero new rows, zero duplicates. "
"2 NOASSERTION/404 detection gaps resolved by direct text reads (303, 304); 1 formatting-only byte-size note (308).** "
"Drift watch (2026-10-08) all clean vs cycle 28: Helm (68) mtytel/helm STILL owner-archived (pushed 2022-09-24T04:23:20Z, owner mtytel); "
"telxcc (236) kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z, owner kanongil); "
"MB-Lab (118) animate1978/MB-Lab STILL owner-archived (pushed 2024-07-21T02:46:17Z); "
"SubDownloader (195) subdownloader/subdownloader STILL archived (pushed 2025-02-05T11:39:33Z); "
"MPC-HC (191) mpc-hc/mpc-hc STILL archived (pushed 2020-04-24T11:04:40Z); "
"Strudel (243) tidalcycles/strudel STILL owner-archived (pushed 2025-06-19T15:56:31Z, owner tidalcycles); "
"ScanTailor (206) scantailor/scantailor STILL owner-archived (pushed 2020-11-29T04:31:29Z, owner scantailor); "
"subSync (253) sc0ty/subSync STILL owner-archived (pushed 2024-10-01T13:47:06Z, owner sc0ty); "
"MKVToolNix (155) codeberg.org/mbunkus/mkvtoolnix still canonical, not archived, updated 2026-09-28; raw COPYING 18,092 bytes BYTE-IDENTICAL to prior checks; "
"uzu/tidal (row 101) codeberg.org/uzu/tidal still live, not archived, updated 2026-07-02; raw LICENSE 35,106 bytes BYTE-IDENTICAL to prior checks. "
"No ownership changes, no relicenses, no successors. Header counts unchanged. "
"LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined, this lane does not decide it.\n"
)

def main():
    with open(PATH) as f:
        lines = f.readlines()

    inserted = False
    for i, ln in enumerate(lines):
        if ln.startswith("> Wave 57 Lane B re-verification cycle"):
            lines.insert(i, HEADER_NOTE + "\n")
            inserted = True
            break
    if not inserted:
        raise SystemExit("anchor for Wave 57 header not found")

    # insert the stamp right after the existing "(verified Wave 38 Lane A, 2026-10-08: ...)"
    # annotation inside the license cell, matching the Wave 57 placement pattern
    anchor = re.compile(r"\(verified Wave 38 Lane A, 2026-10-08:[^)]*\)")
    for row, stamp in STAMPS.items():
        for i, ln in enumerate(lines):
            m = re.match(r"^\| (\d+) \|", ln)
            if m and int(m.group(1)) == row:
                if "Wave 58 Lane B" in ln:
                    print(f"row {row}: already stamped, skipping")
                else:
                    new, n = anchor.subn(lambda mm: mm.group(0) + " " + stamp, ln, count=1)
                    if n != 1:
                        raise SystemExit(f"row {row}: anchor not found (n={n})")
                    lines[i] = new
                    print(f"row {row}: stamped")
                break

    with open(PATH, "w") as f:
        f.writelines(lines)
    print("header inserted:", inserted)

if __name__ == "__main__":
    main()
