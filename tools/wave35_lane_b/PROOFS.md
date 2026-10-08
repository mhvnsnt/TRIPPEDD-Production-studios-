# Wave 35 Lane B — PROOFS (re-verification cycle 6)

Sixth re-verification cycle on `docs/LICENSE_QUARANTINE.md`: the NEXT 10
oldest-verified rows (skipping the 50 done in Waves 30–34; these rows' licenses
had only ever been verified back in Waves 6–16). Fresh upstream checks
2026-10-08 via `tools/wave35_lane_b/audit_row_w35.py` (REPO_MAP extended from
the wave34 tool) + manual reads where the tool's mechanical spdx norm map
doesn't cover the claim (row 86 CeCILL-2.1, row 165 LGPL-2.1).

## Results: 10/10 confirmed — zero relicensing events, zero delists, zero supersedes

| row | project | claim | evidence |
|-----|---------|-------|----------|
| 83 | stable-diffusion-webui-forge (lllyasviel) | AGPL-3.0 | API spdx_id AGPL-3.0; raw LICENSE.txt = AGPL v3 text (36,431 B); repo live, not archived, pushed 2025-07-31 |
| 84 | OneTrainer (Nerogar/OneTrainer) | AGPL-3.0 | API spdx_id AGPL-3.0; raw LICENSE.txt = AGPL v3 text (34,523 B); live, not archived, pushed 2026-10-05 |
| 86 | G'MIC (GreycLab) | CeCILL-2.1 | API NOASSERTION (detection gap); raw COPYING = "CeCILL FREE SOFTWARE LICENSE AGREEMENT Version 2.1 dated 2013-06-21" (44,161 B); live, pushed 2026-10-08 |
| 91 | RawTherapee | GPL-3.0 | API spdx_id GPL-3.0; raw LICENSE = GPL v3 29 June 2007 text (32,473 B); live, pushed 2026-10-07 |
| 94 | pysrt (byroot) | GPL-3.0 | API spdx_id GPL-3.0; license file is LICENCE.txt (French spelling) = GPL v3 text (35,142 B); live, pushed 2023-05-09 |
| 103 | TAL-NoiseMaker | GPL-2.0 | REPO-MOVED: falkTX/DISTRHO-Ports 404s → canonical now DISTRHO/DISTRHO-Ports (org transfer), live, not archived, pushed 2025-09-14; ports-juce5/tal-noisemaker vendored source present; source/TalCore.cpp carries the GPL "either version 2 ... or (at your option) any later version" boilerplate — GPL-2.0-family stands |
| 105 | FAVE-align (Forced-Alignment-and-Vowel-Extraction/new-fave) | GPL-3.0 | API spdx_id GPL-3.0; raw LICENSE = GPL v3 text (35,149 B); README "License: GPL v3" badge; live, pushed 2026-03-15 |
| 120 | Style-Bert-VITS2 | AGPL-3.0 | canonical litagin/style-bert-vits2 STILL 404s (deleted/moved — same as Wave 13); lineage holds via tegnike/Style-Bert-VITS2-API (live, pushed 2024-11-06, API spdx_id AGPL-3.0) + litagin02/Style-Bert-VITS2-Editor (live, pushed 2024-08-10, API spdx_id AGPL-3.0) |
| 165 | Csound | LGPL-2.1 | API spdx_id LGPL-2.1; raw COPYING = GNU LESSER GENERAL PUBLIC LICENSE Version 2.1 text (26,428 B); live, pushed 2026-10-07 — FACTS-ONLY, LGPL doctrine still PENDING OWNER VERDICT |
| 167 | DCP-o-matic (cth103) | GPL-2.0 | API spdx_id GPL-2.0; raw COPYING = GPL v2 June 1991 text (17,992 B); live, pushed 2026-10-05 |

## Identity-drift watch

- **Helm (row 68):** mtytel/helm STILL owner-archived — pushed 2022-09-24T04:23:20Z, ownership unchanged (mtytel), API spdx_id GPL-3.0; no successor, no ownership change, no relicense.
- **telxcc (row 236):** kanongil/telxcc STILL archived — pushed 2025-09-20T11:29:10Z, ownership unchanged; no successor, no relicense.
- **MKVToolNix (row 155):** still canonical on codeberg.org/mbunkus/mkvtoolnix (default branch is `main`), owner mbunkus, not archived, Codeberg COPYING = GPL v2 June 1991 text (18,092 B — byte-identical size to Wave 34); no host moves, no relicense; GPL-2.0-or-later composite stands.

## Notes

- Row 86: the tool mechanically reported NEEDS REVIEW because CeCILL is outside
  its spdx norm map — the auditor (this lane) manually confirmed the CeCILL
  v2.1 text in the fetched COPYING.
- Row 165: same mechanical NEEDS REVIEW for LGPL-2.1 — confirmed manually from
  the fetched COPYING; facts only, doctrine unchanged.
- Row 103: the only row with a canonical-path change this cycle (org transfer).
  The GPL-2.0-family classification is unaffected.
- Proofs per row live in `proofs_row<nn>/` (api.json + fetched license text);
  SHA256SUMS covers all 26 files in this directory (26/26 verified).
