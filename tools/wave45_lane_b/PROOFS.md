# Wave 45 Lane B — re-verification cycle 16 PROOFS (2026-10-08)

Tool: `audit_row_w45.py` (GitHub API repo + license endpoints, raw license-file fetches) with
manual follow-ups where the mechanical path needed it (cycle16_results.json holds full records).
GitHub API access via `gh` CLI (logged in, mhvnsnt). NOASSERTION = detection gap, resolved by
direct license-text read per standing convention.

## Row 154 — GPAC / MP4Box (LGPL-2.1) — CONFIRMED
- gpac/gpac live, not archived, pushed 2026-10-07T17:46:57Z (active), default branch master.
- GitHub API /license: spdx_id LGPL-2.1 ("GNU Lesser General Public License v2.1").
- Raw COPYING (master): 26,428 bytes, opens "GNU LESSER GENERAL PUBLIC LICENSE / Version 2.1, February 1999".
- LGPL doctrine still PENDING OWNER VERDICT — FACTS ONLY, row stays quarantined.

## Row 156 — VidCoder (GPL-2.0) — CONFIRMED
- RandomEngy/VidCoder live, not archived, pushed 2026-09-27T14:15:05Z (active), default branch "beta".
- GitHub API /license: spdx_id GPL-2.0, path **License.txt** (capital L — raw fetch needed this exact casing).
- Raw License.txt (beta): 18,431 bytes CRLF; "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".

## Row 157 — mpv (GPLv2+) — CONFIRMED
- mpv-player/mpv live, not archived, pushed 2026-10-08T00:13:30Z (active), default branch master.
- GitHub API /license: spdx_id NOASSERTION ("Other") = detection gap.
- Root **Copyright** file (4,096 bytes): "mpv as a whole is licensed under the GNU General Public License
  GPL version 2 or later (called GPLv2+ in this document, see LICENSE.GPL for full license text)
  by default. The mpv program is licensed the GNU Lesser General Public License LGPL version 2
  or later (LGPLv2.1+ ...) if built witho[ut GPL-only parts]".
- Raw LICENSE.GPL: 17,984 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- GPLv2+ project grant CONFIRMED; quarantine unchanged.

## Row 158 — VLC (GPL-2.0, SUPERSEDED by row 90) — CONFIRMED
- videolan/vlc live, not archived, pushed 2026-10-07T15:56:27Z (active), default branch master.
- GitHub API /license: spdx_id GPL-2.0.
- Raw COPYING: 18,092 bytes (canonical), "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- Supersede pointer to row 90 intact.

## Row 159 — Bazarr (GPL-3.0, SUPERSEDED by row 98) — CONFIRMED
- morpheus65535/bazarr (canonical post-rename path) live, not archived, pushed 2026-10-08T01:16:50Z (active).
- GitHub API /license: spdx_id GPL-3.0.
- Raw LICENSE: 35,147 bytes, "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007".
- Supersede pointer to row 98 intact.

## Row 160 — SoX (GPL-2.0-or-later apps / LGPL-2.1-or-later libsox) — CONFIRMED
- SourceForge project page https://sourceforge.net/projects/sox/ (200): license field =
  "License version 2.0 (GPLv2), GNU Library or Lesser General Public License version 2.0 (LGPLv2)".
- GNU Guix package record (git.savannah.gnu.org/cgit/guix.git, gnu/packages/audio.scm):
  `(license (list license:gpl2+ license:lgpl2.1+))` with comment "sox.c is distributed under GPL,
  while the files that make up libsox are licensed under LGPL".
- Same two evidence sources as the original Wave verification. Composite claim stands.
- LGPL doctrine still PENDING OWNER VERDICT — FACTS ONLY, row stays quarantined.

## Row 161 — Sonic Visualiser (GPL-2.0-or-later) — CONFIRMED
- sonic-visualiser/sonic-visualiser live, not archived, pushed 2025-12-07T16:09:55Z, default branch "default".
- GitHub API /license: spdx_id GPL-2.0 = detection gap on the -or-later README clause (standing convention).
- README.md grant (direct): "Sonic Visualiser is free software; you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by the Free Software Foundation;
  either version 2 of the License, or (at your option) any later version."
- Raw COPYING: 15,128 bytes, GPL v2 June 1991 text.

## Row 162 — Rubber Band Library (GPL-2.0) — CONFIRMED
- breakfastquay/rubberband live, not archived, pushed 2025-03-03T15:56:58Z, default branch "default".
- GitHub API /license: spdx_id GPL-2.0.
- Raw COPYING: 30,260 bytes, "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".
- Free grant is GPL; commercial dual-license model noted in the row claim — unchanged.

## Row 163 — TarsosDSP (GPL-3.0) — CONFIRMED
- JorenSix/TarsosDSP live, not archived, pushed 2026-06-18T11:18:04Z (active), default branch master.
- GitHub API /license: spdx_id GPL-3.0.
- Raw LICENSE: 35,149 bytes, "GNU GENERAL PUBLIC LICENSE / Version 3, 29 June 2007".

## Row 164 — ChucK (GPL-2.0) — CONFIRMED
- ccrma/chuck live, not archived, pushed 2026-07-10T19:10:37Z (active), default branch "main".
- GitHub API /license: spdx_id GPL-2.0, path **LICENSE.GPL**.
- Raw LICENSE.GPL: 18,092 bytes (canonical), "GNU GENERAL PUBLIC LICENSE / Version 2, June 1991".

## Drift watch (2026-10-08)
- **Helm (row 68)** — mtytel/helm STILL owner-archived, pushed 2022-09-24T04:23:20Z (unchanged);
  ownership unchanged (mtytel); API spdx_id GPL-3.0; no official successor, no ownership change, no relicense.
- **telxcc (row 236)** — kanongil/telxcc STILL archived, pushed 2025-09-20T11:29:10Z (unchanged);
  owner kanongil; API NOASSERTION (detection gap); no successor, no relicense.
- **MKVToolNix (row 155)** — codeberg.org/mbunkus/mkvtoolnix still canonical (Codeberg API 200),
  owner mbunkus, NOT archived, updated 2026-09-28; raw COPYING on branch main = GPL v2 June 1991
  text, 18,092 bytes (byte-identical to Wave 41/42/43 checks) — no host moves, no relicense.
- **MB-Lab (row 118)** — animate1978/MB-Lab STILL owner-archived, pushed 2024-07-21T02:46:17Z (unchanged);
  API NOASSERTION (grant lives in license.txt — established prior waves); no relicense.
- **TidalCycles successor** — codeberg.org/uzu/tidal exists, NOT archived, 281 stars, default branch main,
  updated 2026-07-02; description "Uzu language for live coding algorithmic patterns".
  Active successor — no drift signal.

## Integrity findings
- None. Zero relicensing events, zero delists, zero supersedes, zero new rows.
- Fetch-path notes worth keeping: VidCoder license is `License.txt` (capital L); ChucK license is
  `LICENSE.GPL`; mpv grant lives in the `Copyright` file (+ LICENSE.GPL); Sonic Visualiser
  README carries the -or-later clause directly.
