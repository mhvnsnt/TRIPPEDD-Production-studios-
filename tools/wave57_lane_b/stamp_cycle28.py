#!/usr/bin/env python3
"""Stamp Wave 57 Lane B cycle-28 re-verification notes into LICENSE_QUARANTINE.md rows 291-300,
and insert the cycle header note. Idempotent-ish: skips rows already carrying a Wave-57 stamp."""
import re, sys

PATH = "docs/LICENSE_QUARANTINE.md"
DATE = "2026-10-08"

STAMPS = {
 291: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — AntennaPod/AntennaPod live, not archived, pushed 2026-10-04; GitHub API spdx_id GPL-3.0; raw LICENSE (36,447 bytes) = "GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007" — GPL-3.0 stands; quarantine unchanged)',
 292: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — SourceForge project page license field "License version 2.0 (GPLv2)"; author site danielnoethen.de/butt live (HTTP 200) — GPL-2.0 stands; quarantine unchanged)',
 293: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — ElvishArtisan/rivendell live, not archived, pushed 2026-08-26; GitHub API NOASSERTION = detection gap (REUSE-style LICENSES/ dir); default branch is v4 (fetch-path note: license file NOT on master); raw LICENSES/GPLv2.txt on v4 (17,992 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" — GPL-2.0 stands; quarantine unchanged)',
 294: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — REPO MOVE: observer/obplayer now 404s; canonical upstream is openbroadcaster/obplayer (live, not archived, pushed 2026-09-23); GitHub API spdx_id AGPL-3.0; raw COPYING (34,521 bytes) = "GNU AFFERO GENERAL PUBLIC LICENSE" — AGPL-3.0 stands; NOT a relicense, evidence pointer updated; quarantine unchanged)',
 295: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — exiftool/exiftool live, not archived, pushed 2026-05-27; GitHub API spdx_id GPL-3.0; raw LICENSE (35,149 bytes) = GPL v3 text — GPL-3.0 stands (upstream Perl Artistic/GPL dual-license note intact); quarantine unchanged)',
 296: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — Cuperino/QPrompt-Teleprompter live, not archived, pushed 2026-10-05; GitHub API spdx_id GPL-3.0; raw COPYING (35,142 bytes) = GPL v3 text; Cuperino/QPrompt still 301-redirects to the canonical repo id 306907376 — repo-move note intact; GPL-3.0 stands; quarantine unchanged)',
 297: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — tmeiczin/opendcp live, not archived, pushed 2020-04-28; GitHub API spdx_id GPL-3.0; fetch-path note: grant file is COPYRIGHT.txt (31,703 bytes) carrying GPL v3 text ("refers to version 3 of the GNU General Public License") — GPL-3.0 stands; quarantine unchanged)',
 298: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — redmine/redmine live, not archived, pushed 2026-10-08; GitHub API NOASSERTION persists = detection gap (API surfaces the 918-byte LICENSE.txt pointer file); raw doc/COPYING (18,092 bytes) = "GNU GENERAL PUBLIC LICENSE Version 2, June 1991" — GPL-2.0 stands; quarantine unchanged)',
 299: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — opf/openproject live, not archived, pushed 2026-10-08; GitHub API spdx_id GPL-3.0; raw LICENSE (35,149 bytes) = GPL v3 text — GPL-3.0 stands; quarantine unchanged)',
 300: '(re-verified Wave 57 Lane B, 2026-10-08: CONFIRMED — Leantime/leantime live, not archived, pushed 2026-10-07; GitHub API spdx_id AGPL-3.0; raw LICENSE (34,523 bytes) = AGPL v3 text — AGPL-3.0 stands; quarantine unchanged)',
}

HEADER_NOTE = ("> Wave 57 Lane B re-verification cycle (2026-10-08): TWENTY-EIGHTH re-verification cycle — "
 "rows 291–300 (the NEXT 10 lowest-numbered live rows with bare-date \"(verified Wave 37/38 Lane A, 2026-10-08)\" "
 "annotations and no wave-era re-verification stamp). Fresh upstream checks (GitHub API spdx_id + archived + pushed_at + owner; "
 "/license endpoint content fetches; raw LICENSE/COPYING/COPYRIGHT.txt/LICENSES/GPLv2.txt/doc/COPYING byte-count fetches — never assumed; "
 "NOASSERTION treated as detection gap, always resolved by direct text reads; SourceForge project license field + author-site HTTP for BUTT), "
 "via `tools/wave57_lane_b/cycle28_verify.py` + `tools/wave57_lane_b/stamp_cycle28.py`: rows 291 (AntennaPod, GPL-3.0 — live, pushed 2026-10-04; "
 "API spdx_id GPL-3.0; raw LICENSE 36,447 bytes = GPL v3 text), 292 (BUTT, GPL-2.0 — SF project page license field \"License version 2.0 (GPLv2)\"; "
 "danielnoethen.de/butt live HTTP 200), 293 (Rivendell, GPL-2.0 — live, pushed 2026-08-26; API NOASSERTION detection gap (REUSE-style LICENSES/ dir); "
 "default branch is v4, NOT master — fetch-path note; raw LICENSES/GPLv2.txt on v4 17,992 bytes = GPL v2 June 1991 text), "
 "294 (OpenBroadcaster, AGPL-3.0 — REPO MOVE: observer/obplayer 404s; canonical is openbroadcaster/obplayer, live, pushed 2026-09-23; "
 "API spdx_id AGPL-3.0; raw COPYING 34,521 bytes = AGPL v3 text — NOT a relicense, evidence pointer updated), "
 "295 (ExifTool, GPL-3.0 — live, pushed 2026-05-27; API spdx_id GPL-3.0; raw LICENSE 35,149 bytes = GPL v3 text; dual-license Artistic/GPL note intact), "
 "296 (QPrompt, GPL-3.0 — live, pushed 2026-10-05; API spdx_id GPL-3.0; raw COPYING 35,142 bytes = GPL v3 text; Cuperino/QPrompt 301-redirect intact), "
 "297 (OpenDCP, GPL-3.0 — live, pushed 2020-04-28; API spdx_id GPL-3.0; fetch-path note: grant file is COPYRIGHT.txt, 31,703 bytes = GPL v3 text), "
 "298 (Redmine, GPL-2.0 — live, pushed 2026-10-08; API NOASSERTION persists (detection gap — 918-byte LICENSE.txt pointer); raw doc/COPYING 18,092 bytes = GPL v2 text), "
 "299 (OpenProject, GPL-3.0 — live, pushed 2026-10-08; API spdx_id GPL-3.0; raw LICENSE 35,149 bytes = GPL v3 text), "
 "300 (Leantime, AGPL-3.0 — live, pushed 2026-10-07; API spdx_id AGPL-3.0; raw LICENSE 34,523 bytes = AGPL v3 text). "
 "**Result: 10/10 CONFIRMED as claimed. Zero relicenses, zero delists, zero supersedes, zero new rows, zero duplicates. "
 "1 repo-move note (294: observer/obplayer → openbroadcaster/obplayer — same project, same AGPL-3.0); 2 NOASSERTION detection gaps resolved by direct text reads (293, 298); "
 "2 fetch-path notes (293: default branch v4; 297: grant file COPYRIGHT.txt).** Drift watch (2026-10-08) all clean: Helm (68) mtytel/helm STILL owner-archived "
 "(pushed 2022-09-24T04:23:20Z, owner mtytel); telxcc (236) kanongil/telxcc STILL archived (pushed 2025-09-20T11:29:10Z, owner kanongil); "
 "MB-Lab (118) animate1978/MB-Lab STILL owner-archived (pushed 2024-07-21T02:46:17Z); SubDownloader (195) subdownloader/subdownloader STILL archived "
 "(pushed 2025-02-05T11:39:33Z); MPC-HC (191) mpc-hc/mpc-hc STILL archived (pushed 2020-04-24T11:04:40Z); MKVToolNix (155) codeberg.org/mbunkus/mkvtoolnix "
 "still canonical, not archived, updated 2026-09-28; raw COPYING 18,092 bytes BYTE-IDENTICAL to Wave 41/42/43/45/49/53/55/56 checks; "
 "uzu/tidal (row 101) codeberg.org/uzu/tidal still live, not archived, updated 2026-07-02; raw LICENSE 35,106 bytes BYTE-IDENTICAL to "
 "Wave 38/41/42/43/45/47/48/49/50/53/55/56 checks. No ownership changes, no relicenses, no successors. Header counts unchanged. "
 "LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined, this lane does not decide it.\n")

def main():
    with open(PATH) as f:
        lines = f.readlines()

    # 1. insert header note right before the Wave 56 blockquote line
    inserted = False
    for i, ln in enumerate(lines):
        if ln.startswith("> Wave 56 Lane B re-verification cycle"):
            lines.insert(i, HEADER_NOTE + "\n")
            inserted = True
            break
    if not inserted:
        sys.exit("header anchor not found")

    # 2. stamp rows 291-300
    stamped = 0
    for i, ln in enumerate(lines):
        m = re.match(r"^\|\s*(\d+)\s*\|", ln)
        if not m:
            continue
        row = int(m.group(1))
        if row in STAMPS and "Wave 57 Lane B" not in ln:
            # insert stamp right after the original "(verified ...)" annotation,
            # i.e. append inside the License cell before the closing of that cell's first segment.
            # Simplest robust approach: append stamp right before " — " description separator
            # or before the cell boundary " | " that ends the license cell.
            lic = STAMPS[row]
            # Find the end of the license cell: the license cell is the 3rd pipe-delimited cell.
            # We append the stamp just before the first " | " that follows the verified annotation.
            # Strategy: insert before " — " if present in license cell region, else before next " |".
            anchor = ln.find(" — ")
            if anchor == -1:
                # find the 3rd pipe (end of license cell)
                p = [pos for pos, ch in enumerate(ln) if ch == "|"]
                anchor = p[2] if len(p) > 2 else len(ln)
            lines[i] = ln[:anchor] + " " + lic + ln[anchor:]
            stamped += 1

    with open(PATH, "w") as f:
        f.writelines(lines)
    print(f"header inserted; rows stamped: {stamped}")

if __name__ == "__main__":
    main()
