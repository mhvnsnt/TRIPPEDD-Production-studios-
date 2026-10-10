# Quarantine spot-check — Wave 23 Lane D (2026-10-07)

Lane D of the TRIPPEDD Resource Pull Program WAVE 23 (quarantine audit).
Mandate: fresh spot-check of rows NOT audited in Waves 21–22; do NOT edit
LICENSE_QUARANTINE.md (coordinator merges).

## Rows audited in the last two waves (excluded from selection)

- Wave 21 Lane E: 201, 202, 203, 204, 61, 100, 108, 145, 73, 151
- Wave 22 Lane B: 205, 208, 211, 212, 213, 214, 228, 59, 60, 71

## Rows spot-checked this wave (12)

The 10 highest row numbers not yet audited (210, 215, 221, 222, 223, 225, 227, 229, 230, 231)
plus two older unaudited rows (206, 207). Superseded/dead rows (216, 217, 218, 219, 220, 224, 226)
were skipped — their upstream projects are already covered via their canonical rows.

| # | Project | Claimed license | Verified license | Verdict |
|---|---------|-----------------|------------------|---------|
| 231 | PyMuPDF (pymupdf/PyMuPDF) | AGPL-3.0 | AGPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 230 | DjVuLibre (djvulibre/djvulibre) | GPL-2.0 | GPL-2.0 (GitHub API spdx_id) | CONFIRMED |
| 229 | FromThePage (benwbrum/fromthepage) | AGPL-3.0 | AGPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 227 | Scripto (chnm/scripto) | GPL-3.0 | GPL-3.0 — README license section: "License: [GNU GPL v3]"; GitHub license API returns 404 (no LICENSE file detected — machine-detection gap, same pattern as row 228 Zotero) | CONFIRMED |
| 225 | NormCap (dynobo/normcap) | GPL-3.0 | **GPL-3.0-or-later** — root LICENSE: "either version 3 of the License, or (at your option) any later version" | PRECISION FIX — was GPL-3.0 → GPL-3.0-or-later (the row's existing note already quoted the -or-later clause; claim text needs it) |
| 223 | OCRFeeder (GNOME/ocrfeeder) | GPL-3.0 | GPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 222 | GImageReader (manisandro/gimagereader) | GPL-3.0 | GPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 221 | paperless-ngx (paperless-ngx/paperless-ngx) | GPL-3.0 | GPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 215 | aubio (aubio/aubio) | GPL-3.0 | GPL-3.0 (GitHub API spdx_id) — but same upstream as row 93 | **DUPLICATE** — recommend marking row 215 SUPERSEDED by row 93 (aubio) per append-only convention (Wave 22 Lane A's dedup scan missed row 93) |
| 210 | Tify (tify-iiif-viewer/tify) | AGPL-3.0 | AGPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 207 | ScanTailor Advanced (4lex4/scantailor-advanced) | GPL-3.0 | GPL-3.0 (GitHub API spdx_id) | CONFIRMED |
| 206 | ScanTailor (scantailor/scantailor) | GPL-3.0 | **GPL-3.0-or-later** — root COPYING: "either version 3 of the License, or (at your option) any later version" (GPL3.txt ships alongside; GitHub license API NOASSERTION = detection gap) | PRECISION FIX — was GPL-3.0 → GPL-3.0-or-later |

## Corrections for coordinator (apply to LICENSE_QUARANTINE.md)

1. **Row 225 (NormCap):** precision-fix claim "GPL-3.0" → "GPL-3.0-or-later" (root LICENSE verified 2026-10-07: "either version 3 of the License, or (at your option) any later version"). Quarantine classification unchanged — still strong copyleft.
2. **Row 206 (ScanTailor):** precision-fix claim "GPL-3.0" → "GPL-3.0-or-later" (root COPYING verified 2026-10-07; identical "or any later version" clause). Quarantine classification unchanged.

## Duplicates for coordinator

- **Row 215 (aubio) → SUPERSEDED by row 93 (aubio).** Same upstream project aubio/aubio, same license GPL-3.0, re-added Wave 22 Lane A without a dedup scan (Lane A's wave-22 dedup scan missed row 93 — same failure mode as the 216/218/219/220/224/226 pairs already marked SUPERSEDED). Never renumber; keep row 215 in place with a dedup-mapping entry per the append-only convention.

## Deferrals

- **Speaches Docker / VGMTrans:** still deferred — no container runtime materialized in this sandbox (`which docker podman nerdctl` → all absent, exit 1, 2026-10-07). Docker-based license verification remains unavailable until a runtime exists.

## LGPL doctrine status

- **Still PENDING OWNER VERDICT (re-checked 2026-10-07).** No LGPL items in this wave's 12 rows; nothing decided, nothing delisted. Weak-copyleft rows (63, 121, 154, 165, 183, 184, 212) stay quarantined.

## Failures / gaps

- GitHub license API has no detectable LICENSE for chnm/scripto (404) and scantailor/scantailor (NOASSERTION) — both resolved via primary sources (README license section; raw COPYING fetched and read). No unresolved failures.
- No relicensing events found among the 12 rows.

## Tally

- CONFIRMED: 9 (231, 230, 229, 227, 223, 222, 221, 210, 207)
- PRECISION FIX (still quarantined, license text refined): 2 (225, 206)
- DUPLICATE (recommend SUPERSEDED): 1 (215 → row 93)
