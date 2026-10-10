#!/usr/bin/env python3
"""Wave 53 Lane B: stamp cycle-24 re-verification annotations into the table."""
import re

PATH = "docs/LICENSE_QUARANTINE.md"
text = open(PATH).read()

STAMPS = {
    155: (
        "quarantine unchanged) | captions (drift watch Wave 43 Lane B",
        "quarantine unchanged) (re-verified Wave 53 Lane B, 2026-10-08: codeberg.org/mbunkus/mkvtoolnix still canonical, owner mbunkus, not archived, updated 2026-09-28; raw COPYING on branch main = GPL v2 June 1991 text (18,092 bytes — byte-identical to Wave 41/42/43/45/49 checks) — no host moves, no relicense; GPL-2.0-or-later composite stands; quarantine unchanged) | captions (drift watch Wave 43 Lane B",
    ),
    251: (
        "| 251 | Performous | GPL-2.0-or-later (verified 2026-10-07: LICENSE.md text, Wave 26 Lane B) — karaoke game with word-level lyric timing and on-screen lyric rendering | captions/karaoke |",
        "| 251 | Performous | GPL-2.0-or-later (verified 2026-10-07: LICENSE.md text, Wave 26 Lane B) — karaoke game with word-level lyric timing and on-screen lyric rendering (re-verified Wave 53 Lane B, 2026-10-08: performous/performous live, not archived, pushed 2026-09-24; GitHub API NOASSERTION = detection gap; raw LICENSE.md = GPL v2 text (18,387 bytes) with header 'Performous is GNU GPLv2 or later' — GPL-2.0-or-later stands; quarantine unchanged) | captions/karaoke |",
    ),
    252: (
        "| 252 | Vocaluxe | GPL-3.0 (verified 2026-10-07: GitHub API spdx_id, Wave 26 Lane B) — karaoke game with real-time lyric line rendering and pitch display | captions/karaoke |",
        "| 252 | Vocaluxe | GPL-3.0 (verified 2026-10-07: GitHub API spdx_id, Wave 26 Lane B) — karaoke game with real-time lyric line rendering and pitch display (re-verified Wave 53 Lane B, 2026-10-08: Vocaluxe/Vocaluxe live, not archived, pushed 2026-10-06; GitHub API spdx_id GPL-3.0; license file is LICENSE.txt on branch develop (fetch-path note); raw LICENSE.txt = GPL v3 29 June 2007 text (35,146 bytes) — GPL-3.0 stands; quarantine unchanged) | captions/karaoke |",
    ),
    253: (
        "| 253 | subSync (sc0ty) | GPL-3.0 (verified 2026-10-07: GitHub API spdx_id, Wave 26 Lane B) — automatic subtitle synchronization to audio waveforms | captions/packaging |",
        "| 253 | subSync (sc0ty) | GPL-3.0 (verified 2026-10-07: GitHub API spdx_id, Wave 26 Lane B) — automatic subtitle synchronization to audio waveforms (re-verified Wave 53 Lane B, 2026-10-08: sc0ty/subSync GitHub API spdx_id GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text — GPL-3.0 stands; NEW DRIFT: repo now owner-archived (pushed 2024-10-01); archive does not change license; quarantine unchanged) | captions/packaging |",
    ),
    254: (
        "| 254 | Subler | GPLv2 (verified 2026-10-07: LICENSE text, Wave 26 Lane B) — macOS MP4/M4V muxer for tagging and adding subtitle tracks | captions/packaging |",
        "| 254 | Subler | GPLv2 (verified 2026-10-07: LICENSE text, Wave 26 Lane B) — macOS MP4/M4V muxer for tagging and adding subtitle tracks (re-verified Wave 53 Lane B, 2026-10-08: SublerApp/Subler live, not archived, pushed 2026-10-05; GitHub API NOASSERTION = detection gap; root LICENSE = composite grant: 'Most files in Subler are under ... GPLv2 ... In combination, the GPLv2 license applies to Subler' — GPLv2 claim stands; quarantine unchanged) | captions/packaging |",
    ),
    255: (
        "| 255 | stream_closed_captioner_phoenix | GPL-3.0 (verified 2026-10-07: GitHub API spdx_id, Wave 26 Lane B) — Twitch live closed-captioner extension (talk2megooseman) | captions/live |",
        "| 255 | stream_closed_captioner_phoenix | GPL-3.0 (verified 2026-10-07: GitHub API spdx_id, Wave 26 Lane B) — Twitch live closed-captioner extension (talk2megooseman) (re-verified Wave 53 Lane B, 2026-10-08: talk2megooseman/stream_closed_captioner_phoenix live, not archived, pushed 2026-08-31; GitHub API spdx_id GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text — GPL-3.0 stands; quarantine unchanged) | captions/live |",
    ),
    256: (
        "| 256 | xmp-cli (extended-module player CLI) | GPL-2.0 (verified 2026-10-07, upstream; Wave 27 Lane A) — command-line tracker-module player | trackers |",
        "| 256 | xmp-cli (extended-module player CLI) | GPL-2.0 (verified 2026-10-07, upstream; Wave 27 Lane A) — command-line tracker-module player (re-verified Wave 53 Lane B, 2026-10-08: libxmp/xmp-cli live, not archived, pushed 2026-07-30; GitHub API spdx_id GPL-2.0; raw COPYING = GPL v2 June 1991 text — GPL-2.0 stands; quarantine unchanged) | trackers |",
    ),
    257: (
        "| 257 | UADE (Unix Amiga Delitracker Emulator) | GPL-2.0 (verified 2026-10-07, upstream; Wave 27 Lane A) — Amiga music emulator for classic tracker formats | trackers |",
        "| 257 | UADE (Unix Amiga Delitracker Emulator) | GPL-2.0 (verified 2026-10-07, upstream; Wave 27 Lane A) — Amiga music emulator for classic tracker formats (re-verified Wave 53 Lane B, 2026-10-08: canonical upstream is gitlab.com/uade-music-player/uade — NOT GitHub (uade-team/uade 404s; repo-location note); active, last activity 2026-09-20; root COPYING describes mixed-license distribution; COPYING.GPL = GPL v2 June 1991 text (18,007 bytes); COPYING.LGPL also present — GPL-2.0-family claim stands; quarantine unchanged) | trackers |",
    ),
    258: (
        "| 258 | sidplayfp | GPL-2.0-or-later (verified 2026-10-07, upstream; Wave 27 Lane A) — C64 SID music player/emulator | trackers |",
        "| 258 | sidplayfp | GPL-2.0-or-later (verified 2026-10-07, upstream; Wave 27 Lane A) — C64 SID music player/emulator (re-verified Wave 53 Lane B, 2026-10-08: libsidplayfp/sidplayfp live, not archived, pushed 2026-10-04; GitHub API spdx_id GPL-2.0 = detection gap on -or-later; raw COPYING = GPL v2 June 1991 text; per-file header src/IniConfig.h: 'either version 2 of the License, or (at your option) any later version' — GPL-2.0-or-later stands; quarantine unchanged) | trackers |",
    ),
    259: (
        "| 259 | ASAP (Another Slight Atari Player) | GPL-2.0 (verified 2026-10-07, upstream; Wave 27 Lane A) — Atari 8-bit music player | trackers |",
        "| 259 | ASAP (Another Slight Atari Player) | GPL-2.0 (verified 2026-10-07, upstream; Wave 27 Lane A) — Atari 8-bit music player (re-verified Wave 53 Lane B, 2026-10-08: canonical upstream is SourceForge sourceforge.net/p/asap/code — no official GitHub repo (jhusak/asap 404s; repo-location note); active, release 8.0.0 (2026-02-16); root COPYING = GPL v2 June 1991 text (18,011 bytes, from 8.0.0 tree); author Piotr Fusik's own statement 'My code is GPL 2+' — GPL-2.0 stands; quarantine unchanged) | trackers |",
    ),
}

for row, (anchor, replacement) in STAMPS.items():
    count = text.count(anchor)
    assert count == 1, f"row {row}: anchor found {count} times"
    text = text.replace(anchor, replacement)
    print(f"row {row} stamped")

# Row 151 MediaConch drift note — append after existing Wave-44 note in the License cell
anchor151 = "no relicense reversal; CLEARED status stands) | captions"
replacement151 = (
    "no relicense reversal; CLEARED status stands) "
    "(drift watch Wave 53 Lane B, 2026-10-08: FRESH upstream check — canonical repo MediaArea/MediaConch_SourceCode pushed 2026-08-11, GitHub API spdx_id BSD-2-Clause; "
    "root LICENSE (1,328 bytes) = BSD 2-Clause text 'Copyright (c) 2015-2018, MediaArea.net SARL'; root License.html = BSD-2-Clause grant + OPTIONAL relicense paths "
    "(Apache-2.0+/LGPL-2.1+/GPL-2.0+/MPL-2.0+ at the user's choice — not a project relicense); mediaarea.net MediaConch page Licensing section still 'BSD-style license'; "
    "the 'GPLv3+/MPLv2+' text lives ONLY in the STALE MediaArea/MediaConch repo's SourceCode/License.html (PREFORMA-era file; repo abandoned, pushed 2021-09-29) — "
    "NO upstream relicense reversal; DELISTED/CLEARED status stands) | captions"
)
count = text.count(anchor151)
assert count == 1, f"row 151: anchor found {count} times"
text = text.replace(anchor151, replacement151)
print("row 151 drift note appended")

open(PATH, "w").write(text)
print("STAMPED OK")

# pipe-count sanity: every row line must still have 7 pipes
bad = []
for ln in text.splitlines():
    m = re.match(r'^\| (\d+) \|', ln)
    if m and ln.count('|') != 7:
        bad.append((m.group(1), ln.count('|')))
print("pipe-check bad rows:", bad if bad else "NONE — all rows have 7 pipes")
