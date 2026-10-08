# Wave 34 Lane B — re-verification cycle 5 proofs (2026-10-08)

Cycle rows: 48, 49, 52, 53, 54, 56, 76, 77, 78, 79 (the next 10 oldest-verified
rows not covered in cycles 1–4, i.e. Waves 30–33). Drift watch: 68 (Helm),
236 (telxcc), 155 (MKVToolNix).

Tool: `audit_row_w34.py` (copy of the wave32 tool with REPO_MAP extended for
the 10 cycle rows; rows 68/236 already in REPO_MAP; row 155 verified manually
on Codeberg since the tool is GitHub-only).

## Cycle rows — all CONFIRMED

| Row | Upstream | Status | API spdx_id | License evidence |
|-----|----------|--------|-------------|------------------|
| 48 VidCutter | ozmartian/vidcutter | live, pushed 2025-04-24 | GPL-3.0 | raw LICENSE = GPL v3 29 June 2007 text (32,422 B) |
| 49 whisper-timestamped | linto-ai/whisper-timestamped | live, pushed 2026-09-28 | AGPL-3.0 | raw LICENSE = AGPL v3 text (34,523 B) |
| 52 Blender-StellarToon | festivities/Blender-StellarToon | live, pushed 2024-03-03 (stale) | GPL-3.0 | raw LICENSE = GPL v3 text (35,149 B) |
| 53 2D-Cel-Toon-Shader-v2-Plus | mightymochi/2D-Cel-Toon-Shader-v2-Plus-Godot-3.x (GitHub rename/redirect of the base name) | live, pushed 2023-07-28 (stale) | GPL-3.0 | raw LICENSE = GPL v3 text (35,149 B) |
| 54 manga-image-translator | zyddnys/manga-image-translator | live, pushed 2026-09-25 | GPL-3.0 | raw LICENSE = GPL v3 text (35,149 B) |
| 56 libre-manga-translator | mrdhnto/libre-manga-translator | live, pushed 2026-10-05 | NOASSERTION (custom header) | root LICENSE: "Libre Manga Translator is AGPL-3.0-or-later, from v1.0.0 Stable onward" + full AGPL v3 text; docs/technical.md: License (program) = AGPL-3.0-or-later |
| 76 RobustVideoMatting | PeterL1n/RobustVideoMatting | live, pushed 2024-04-02 (stale) | GPL-3.0 | raw LICENSE = GPL v3 text (35,148 B) |
| 77 mmd_tools | MMD-Blender/blender_mmd_tools | live, pushed 2026-10-04 | GPL-3.0 | raw LICENSE = GPL v3 text (35,149 B) |
| 78 APISR | Kiteretsu77/APISR | live, pushed 2025-10-16 | GPL-3.0 | raw LICENSE = GPL v3 text (35,149 B) |
| 79 ADetailer | Bing-su/adetailer | live, pushed 2026-10-05 | AGPL-3.0 | raw LICENSE.md = AGPL v3 text (34,270 B) |

Maintenance notes: row 56 — betas through v1.0.0-Beta5 were conveyed under MIT
per the root LICENSE preamble (each tag carries its own LICENSE); the
current/stable grant is AGPL-3.0-or-later, so the row's claim stands.
Row 53 — canonical upstream path recorded as the full `-Godot-3.x` name.

## Drift watch — no further changes

- **Row 68 Helm**: mtytel/helm still owner-archived (archived=True,
  pushed 2022-09-24T04:23:20Z — unchanged), ownership unchanged (mtytel),
  API spdx_id GPL-3.0, raw COPYING = GPL v3 text (35,147 B). No official
  successor, no ownership change, no relicense.
- **Row 236 telxcc**: kanongil/telxcc still archived (archived=True,
  pushed 2025-09-20T11:29:10Z — unchanged), ownership unchanged,
  API spdx_id NOASSERTION, raw LICENSE = GPL-2.0-or-later boilerplate
  (2,091 B). No successor, no relicense.
- **Row 155 MKVToolNix**: codeberg.org/mbunkus/mkvtoolnix still canonical
  (Codeberg API: owner mbunkus, archived=False, default_branch main),
  Codeberg COPYING = GPL v2 June 1991 text (18,092 B). No further host moves,
  no relicense. Per-file header spot-check skipped — Codeberg raw fetches
  timed out from this VM (45s+ on raw.codeberg.org); the license-file evidence
  is the authoritative signal and matches the Wave-29 basis.

Proof dirs: `proofs_row48/`, `proofs_row49/`, `proofs_row52/`, `proofs_row53/`,
`proofs_row54/`, `proofs_row56/` (LICENSE + docs_technical.md + README.md),
`proofs_row68/`, `proofs_row76/`, `proofs_row77/`, `proofs_row78/`,
`proofs_row79/`, `proofs_row155/` (COPYING; common.h fetch timed out),
`proofs_row236/`. Each contains api.json (GitHub) + raw license files.
