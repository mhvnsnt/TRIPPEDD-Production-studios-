# Wave 24 Lane B — quarantine flags (proposed rows for docs/LICENSE_QUARANTINE.md)

Date: 2026-10-07 · Worker: subagent Lane B. All four verified from upstream sources
(GitHub API `spdx_id` or repo LICENSE/README text) — never assumed. Dedup: grepped
`docs/LICENSE_QUARANTINE.md` for each name — zero hits, all new. Per the program
convention these are PROPOSED rows only; the coordinator appends them to the manifest
(the manifest was NOT edited by this lane).

| # | Name | License (verified) | Upstream URL | Lane | One-line note |
|---|------|--------------------|--------------|------|---------------|
| — | QCTools | GPL-3.0 (verified 2026-10-07 via root License.html: "GPLv3" / "General Public License" grant text) | https://github.com/bavc/qctools | captions/QC | BAVC's video QC analyzer (bitstream + filter graphs); subtitle-stream QC angle, but GPL-3.0 bars shipping integration |
| — | telxcc | GPL-2.0 (verified 2026-10-07 via root LICENSE: "General Public License ... either version 2 of the License"; README: "(c) Forers, s. r. o. ... Licensed under the GPL") | https://github.com/kanongil/telxcc (fork; original Forers/telxcc) | captions/teletext | VBI teletext subtitle extractor (DVB teletext → SRT); zvbi (LGPL, entries file) is the permissive-adjacent alternative |
| — | UltraStar-Deluxe (USDX) | GPL-2.0 (verified 2026-10-07 via GitHub API `spdx_id` on UltraStar-Deluxe/USDX; pushed 2026-10-07, active) | https://github.com/UltraStar-Deluxe/USDX | captions/karaoke | Karaoke game with word-level lyric timing; GPL-2.0 kills any pipeline reuse — kashi/SOFA (MIT) cover the timing need |
| — | AtomicParsley | GPL-2.0 (verified 2026-10-07 via GitHub API `spdx_id` on wez/atomicparsley) | https://github.com/wez/atomicparsley | captions/packaging | MP4 metadata editor (incl. subtitle-track metadata); mp4v2 (MPL, ⚠️ entry) / GPAC (LGPL, ⚠️ entry) cover the use case |

Notes:
- zvbi was checked as a quarantine candidate but verified **LGPL-2.1+** — filed as
  a ⚠️ weak-copyleft audit-gate entry in `lane-b-entries.md`, not a quarantine row
  (per the Wave-12/16 standing convention).
- noScribe, LosslessCut, mpv, VLC, MKVToolNix, Bazarr, Gaupol, ProjectX,
  SubtitleComposer, Jubler, Gnome Subtitles, xy-VSFilter, VideoSubFinder,
  SubDownloader, VisualSubSync: already rows in the manifest — not re-flagged.
