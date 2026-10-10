# Wave 41 Lane B — re-verification cycle 12 + drift watch + 1 tool wire

**Date:** 2026-10-08 · **Branch:** `wave41-lane-b` · **Lane:** B (coordinator merges)

## 1. Re-verification cycle 12 (quarantine rows 112, 113, 114, 115, 116, 117, 118, 119, 121, 122)

Twelfth RE-VERIFICATION cycle — the NEXT 10 never-reverified rows by oldest
last-verification annotation (skipping the 110 done in Waves 30–40 cycles 1–11;
dead/superseded records excluded). Selection = 10 lowest row numbers among live
rows whose verification annotations are bare-date `(verified: ..., 2026-10-07)`
with no wave-era stamp (earliest verification era).

Fresh upstream checks per row: GitHub repo API record (existence / archived /
pushed_at / spdx_id / owner, authenticated), raw license-file fetches with
per-row grant-hosting paths (README.rst, CLAUDE.md, CONTRIBUTING.md, policy.md,
LICENSE.CODE.md, avisynth license.rst) — never assumed. Verifier:
`tools/wave41_lane_b/cycle12_verify.py` (adapted from the cycle-11 donor tool;
adds per-row EXTRA_PATHS probing + GitHub-authenticated API); mechanical
verdicts confirmed by direct license-text reads. Evidence in
`tools/wave41_lane_b/proofs_rowNN/`.

**Result: 10/10 confirmed as claimed. Zero relicensing events, zero delists,
zero supersedes.**

| Row | Tool | Verdict |
|---|---|---|
| 112 | WhisperSubTranslate | ✅ Blue-B/WhisperSubTranslate live, not archived, pushed 2026-10-04; API spdx NOASSERTION (detection gap — no root LICENSE file); README 'License' section: "GPL-3.0" — README-hosted grant by design — GPL-3.0 stands |
| 113 | Subtitle Workshop | ✅ dekked/subtitleworkshop live, not archived, pushed 2013-03-24 (stale); no machine license file (API null) — license file is README.rst (not README.md); README.rst line 179: "released under the GNU/GPL 3 license" — GNU/GPL 3 stands |
| 114 | whisper-subs | ✅ ashlcx/whisper-subs live, not archived, pushed 2026-09-13; API spdx_id GPL-3.0; CLAUDE.md line 288: "License is GPL-3.0" — GPL-3.0 stands |
| 115 | jev-subtitle-translator | ✅ GeekLinkDev/jev-subtitle-translator live, not archived, pushed 2026-09-29; API spdx_id GPL-3.0; CONTRIBUTING.md: "Contributions are accepted under the repository license, GPL-3.0-or-later" — GPL-3.0-or-later stands; canonical path capitalization GeekLinkDev (row's lowercase redirects) |
| 116 | JUCE | ✅ juce-framework/JUCE live, not archived, pushed 2026-10-08; API NOASSERTION (detection gap on pointer doc); root LICENSE.md: modules dual-licensed AGPLv3 + commercial JUCE licence (JUCE 9 EULA referenced) — AGPL-3.0 open-source tier stands |
| 117 | AviSynth+ | ✅ AviSynth/AviSynthPlus live, not archived, pushed 2026-10-05; license.rst MOVED (docs/English/license.rst → distrib/docs/english/source/avisynthdoc/license.rst) — "either version 2 of the License, or (at your option) any later version" + special avisynth.h independent-module linking exception intact; avs_core/include/avisynth.h lines 68/85-87 confirm -or-later grant + exception — GPL-2.0-or-later stands |
| 118 | MB-Lab | ✅ animate1978/MB-Lab license.txt lines 5-10: "released under GNU General Public License 3 … either version 3 of the License" — GPL-3.0 stands. **NEW DRIFT: repo now ARCHIVED** (owner-archived, pushed 2024-07-21) |
| 119 | MakeHuman app | ✅ makehumancommunity/makehuman live, not archived, pushed 2024-08-19; LICENSE.CODE.md = GNU Affero GPL v3 text (19 November 2007) — AGPL-3.0 code tier stands; CC0 assets carve-out unchanged |
| 121 | AivisSpeech | ✅ Aivis-Project/AivisSpeech live, not archived, pushed 2026-07-12; API spdx_id LGPL-3.0; policy.md gone from root — evidence now STRONGER: new root LICENSE = GNU LGPL v3 29 June 2007 text — LGPL-3.0 stands, facts-only (LGPL doctrine still PENDING OWNER VERDICT; row stays quarantined) |
| 122 | Furnace | ✅ tildearrow/furnace live, not archived, pushed 2026-10-07; API NOASSERTION (detection gap); README footnotes carry the GPL v2-or-later boilerplate — GPL-2.0-or-later stands. **DUPLICATE NOTE: same upstream as row 271** (tildearrow/furnace, verified Wave 32 Lane A) — cross-notes added to both rows; coordinator to dedupe; "355 distinct" may be overstated by 1 |

In-row `(re-verified Wave 41 Lane B, 2026-10-08: …)` annotations appended to all
10 rows + the row-122/271 duplicate cross-notes (history rows untouched;
annotations only). Wave-history blockquote appended to the quarantine section
header in `docs/LICENSE_QUARANTINE.md`.

## 2. Identity-drift watch

- **Helm (row 68):** mtytel/helm STILL owner-archived — pushed 2022-09-24T04:23:20Z,
  ownership unchanged (mtytel), API spdx_id GPL-3.0. Fork shape unchanged in kind:
  DatanoiseTV/helm 6★ stale 2020-11 (top), poweraudio/helm 3★ pushed 2024-09-08,
  AJ-Gonzalez/helm-apple-silicon 2★ pushed 2026-09-21 (freshest recurring
  maintenance fork). No official successor, no ownership change, no relicense.
- **telxcc (row 236):** kanongil/telxcc STILL archived — pushed
  2025-09-20T11:29:10Z, ownership unchanged (kanongil), API spdx_id NOASSERTION
  (detection gap). Top forks unchanged in shape: braincoded 1★ stale 2014,
  wazerstar 0★ pushed 2020-11-27, hamza-u/teletext_decoder 0★ 2018. No standout
  successor, no relicense.
- **MKVToolNix (row 155):** still canonical on codeberg.org/mbunkus/mkvtoolnix —
  page HTTP 200, COPYING on branch `main` = GPL v2 June 1991 text (18,092 bytes,
  byte-identical size to the cycle-11 check); owner mbunkus, no further host
  moves, no relicense; GPL-2.0-or-later composite stands.
- **uzu/tidal (TidalCycles successor, row 101):** HTTP 200, LICENSE = GPL v3
  29 June 2007 text (35,106 bytes); active development, no relicense.

Drift watch evidence: `tools/wave41_lane_b/drift_watch.json`.

## 3. Header counts (direct recount)

- 378 table rows parsed; row numbers 1–378 all present, no gaps.
- **378 rows · 355 distinct** — unchanged (no row changes this cycle; the
  row-122/271 duplicate is noted, not yet actioned, so the formula
  378 − 22 dead − 1 aeneas rows-1+2 stands as-is).
- Catalog red-flags section: no status changes among quarantined projects this
  cycle → left as-is (synced by the Wave-40 coordinator).

## 4. Table repair (row 145)

Row 145 (Bento4) had a literal pipe inside the Wave-39 annotation quote
(`Bento4|GPL`) that split the markdown table into extra columns (the status
cell rendered as 'trippedd'). Repaired to `Bento4/GPL` and closed the
split quote — content of all earlier entries preserved verbatim. All 378 rows
now parse as clean 7-cell rows.

## 5. Tool wiring: Furnace headless render (quarantine rows 122/271)

`tools/wave41_lane_b/wire_furnace/wire_furnace.py` — downloads the official
upstream Furnace v0.6.8.3 Linux x86_64 release to a local cache (the
quarantined binary is NEVER committed to git), then:

1. `furnace -version` → exit 0 (binary identity)
2. `furnace -console -output proof_render.wav "Exquisite Invitation.fur"` →
   exit 0 — headless-rendered the upstream 882-byte demo song to
   `proof_render.wav`: **10,164,220 bytes, RIFF/WAVE PCM 16-bit stereo
   44100 Hz, 57.62 s, 10,164,176 data bytes**; content check peak 25,877 /
   RMS 6,451 → real non-silent rendered audio, not a stub.
3. `proof_manifest.json` (WAV header facts, rc codes, SHA-256) +
   `SHA256SUMS` (3/3 OK via `sha256sum -c`) + `PROOFS.md`.

Standalone-tool use only — the GPL binary is never linked or imported into
shipping paths. Honest notes: one harmless ALSA `/dev/snd/seq` warning in a
MIDI-less environment (render path doesn't use MIDI); the proof is the tool
executing correctly headless, not project audio.

## 6. Honest failures / constraints

- The cycle-12 tool's mechanical verdicts needed manual review for 8/10 rows
  (README/CLAUDE.md/CONTRIBUTING.md/README.rst-hosted grants, JUCE dual-tier
  pointer doc, AviSynth+ license.rst path move, MB-Lab archived repo) — the
  mechanical text matching can't see grant clauses hosted outside license
  files; every row was closed by a direct license-text read, never assumed.
- First drift-watch run failed the Codeberg license fetches with HTTP 401 —
  the GitHub Bearer token was being sent to codeberg.org; fixed to scope the
  Authorization header to github.com hosts only. Second run then 404'd on
  MKVToolNix COPYING — branch drift (raw URL used `master`, file lives on
  `main`); corrected. Both are now baked into the tool.
- The cycle12_results.json got overwritten by a `--drift`-only re-run
  (0 rows); the per-row `proofs_rowNN/row.json` files from the full run carry
  the authoritative records and are committed.
- No re-verification was possible for rows past 378 — manifest ends at row 378.

## Commits

- `ea073b3` — cycle-12 re-verification + drift watch + header recount + row-145 repair
- `2867453` — Furnace wire with real proof

**Branch:** `wave41-lane-b` (pushed to origin; coordinator merges).
LGPL doctrine still PENDING OWNER VERDICT — weak-copyleft rows stay quarantined;
this lane does not decide it.
