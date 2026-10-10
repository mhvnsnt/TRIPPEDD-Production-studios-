# Wave 47 Lane B — re-verification cycle 18 + 2 tool wires

**Date:** 2026-10-08 · **Branch:** `wave47-lane-b` · **Lane:** B

## 1. Re-verification cycle 18 (quarantine rows 183, 184, 186–193)

Next 10 never-reverified rows by lowest row number with bare-date
"(verified: ..., 2026-10-07)" annotations (row 185 SUPERSEDED skipped).
Fresh upstream checks: GitHub API spdx_id + archived flag + pushed_at, raw
license-file fetches, SourceForge license fields — never assumed — via
`tools/wave47_lane_b/cycle18_verify.py` + `stamp_cycle18.py` + manual passes.

**Result: 10/10 confirmed as claimed. Zero relicenses, zero delists, zero supersedes.**

| Row | Tool | Verdict |
|---|---|---|
| 183 | Verovio | ✅ live, not archived, pushed 2026-10-08; API LGPL-3.0; master/COPYING = GPL v3 text + COPYING.LESSER = LGPL v3 text; README LGPL-v3 badge — LGPL-3.0 stands (weak copyleft, doctrine still pending) |
| 184 | libgme | ✅ live, not archived, pushed 2026-09-08; API LGPL-2.1; raw master/license.txt = LGPL v2.1 text — LGPL-2.1 stands (fetch-path note: file is license.txt). LGPL doctrine still pending |
| 186 | Zrythm | ✅ live, not archived, pushed 2026-10-04; API NOASSERTION (REUSE-scheme detection gap); raw LicenseRef-ZrythmLicense.txt (35,717 B) contains "Additional terms under Section 7 of the GNU AGPL" trademark terms — stands |
| 187 | CheeseTracker | ✅ SourceForge live, license field "GNU General Public License version 2.0 (GPLv2)" — stands |
| 188 | Rosegarden | ✅ both mirrors live (nengxu stale 2014, tedfelix active pushed 2026-10-05); API GPL-2.0 on both; raw COPYING = GPL v2 text on both; rosegardenmusic.com live — stands |
| 189 | IINA | ✅ live, not archived, pushed 2026-10-08; API GPL-3.0; develop/LICENSE = GPL v3 text — stands |
| 190 | SMPlayer | ✅ live, not archived, pushed 2026-10-06; API GPL-2.0; master/Copying.txt = GPL v2 text — stands |
| 191 | MPC-HC | ✅ **archived-status note NEW vs original annotation** (mpc-hc/mpc-hc now archived, pushed 2020-04-24); API GPL-3.0; COPYING.txt = GPL v3 text — GPL-3.0 stands |
| 192 | MPC-BE | ✅ SourceForge live, license field "GNU General Public License version 3.0 (GPLv3)" — stands |
| 193 | Celluloid | ✅ live, not archived, pushed 2026-10-04; API GPL-3.0; master/COPYING = GPL v3 text — stands |

**Drift watch (all unchanged):** Helm (68) still owner-archived (pushed 2022-09-24,
owner mtytel, GPL-3.0); telxcc (236) still archived (2025-09-20, kanongil,
NOASSERTION detection gap); MB-Lab (118) still archived; OHF-Voice/piper1-gpl
(41) live, pushed 2026-10-06; MycroftAI/mimic3 (14) live, AGPL-3.0;
so-vits-svc (24) archived; Seed-VC (43) archived; tidalcycles/Tidal still
archived; codeberg.org/mbunkus/mkvtoolnix 200, not archived. No ownership
changes, no relicenses, no successors.

Header counts unchanged (no row changes this cycle). LGPL doctrine still
PENDING OWNER VERDICT — rows 183/184 stay quarantined.

## 2. Tool wires (2, both permissive, both real proofs)

- **`wire_stb_image.py`** — stb_image + stb_image_write (public domain / MIT
  dual; header "public domain image loader" verified 2026-10-08): 256×128 RGB
  fixture → `stbi_load` → `stbi_write_bmp`; BMP pixels byte-identical to the
  fixture (98,304 bytes). First run PASS.
- **`wire_miniaudio.py`** — miniaudio v0.11.25 (public domain OR MIT-0; header
  verified 2026-10-08): 44,100-frame 440 Hz WAV fixture → `ma_decoder` →
  `raw_decoded.pcm` byte-identical to fixture samples → `ma_encoder` WAV →
  re-decode → PCM **MATCH**. Honest failure logged: first run failed at
  encoder init — `ma_encoder_init_file` arg order in 0.11.x is
  (path, config, encoder); fixed, rerun PASS.

Proofs: `tools/wave47_lane_b/PROOFS.md`, `SHA256SUMS` (8/8 OK),
`proofs_stb_image/` (4 files), `proofs_miniaudio/` (4 files),
`vendor/` headers (provenance). Catalog status updated for miniaudio.

## Commits

1. `e5756eb` Wave 47 Lane B: re-verification cycle 18
2. `ea83c7d` Wave 47 Lane B: wire stb_image + miniaudio with real proofs
