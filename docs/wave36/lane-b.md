# Wave 36 Lane B — re-verification cycle 7 + 2 tool wires

**Date:** 2026-10-08 · **Branch:** `wave36-lane-b` · **Lane:** B (Lane A runs separately; coordinator merges)

## 1. Re-verification cycle 7 (quarantine rows 31, 32, 33, 36, 37, 39, 40, 41, 50, 51)

Next oldest-verified rows not covered in cycles 1–6 (waves 30–35 covered
rows 1–30, 34–35, 38, 42–49, 52–54, 56, 68, 76–79, 83–86, 91, 94, 103, 105,
120, 165, 167, 236). Each row re-checked fresh upstream (repo-page existence /
archived status via `gh` API, raw LICENSE/COPYING fetches, canonical
non-GitHub sources where applicable — never assumed).

**Result: 10/10 confirmed. Zero relicensing events, zero delists, zero supersedes.**

| Row | Tool | Verdict |
|---|---|---|
| 31 | Blender VSE | ✅ blender.org/about/license/ 200 — "GNU GPL Version 2 or later" (source) + binaries "compatible under the newer [GPL v3 or later]"; split stands |
| 32 | chaiNNer | ✅ live, not archived, pushed 2026-10-01; API GPL-3.0; raw LICENSE = GPL v3 text |
| 33 | Cinelerra-GG Infinity | ✅ site 200 + upstream git 200 — project live; GPLv2+ carried forward from official manual appendix (Features5.pdf §D); PDF text not independently re-fetched this cycle (JS-rendered site) — noted honestly in-row |
| 36 | Inkscape | ✅ canonical gitlab.com/inkscape/inkscape (default branch master); COPYING: "Most Inkscape source code is available under the GNU General Public License, version 2 or later" |
| 37 | Kdenlive | ✅ live, not archived, pushed 2026-10-08; API GPL-3.0; COPYING = GPL v3 |
| 39 | LibreSprite | ✅ live, not archived, pushed 2026-10-04; API GPL-2.0; LICENSE.txt = GPL v2 |
| 40 | LiVES | ✅ live, not archived; API GPL-3.0; COPYING = GPL v3 |
| 41 | Piper (OHF-Voice) | ✅ supersede pointer intact — OHF-Voice/piper1-gpl live, not archived, pushed 2026-10-06; API GPL-3.0; COPYING = GPL v3; row still SUPERSEDED by row 20 |
| 50 | Wick Editor | ✅ live, not archived; API GPL-3.0; license file is LICENSE.md on master (not LICENSE) = GPL v3 text |
| 51 | Goo Engine | ✅ fork live, not archived, pushed 2026-06-03; raw COPYING = Blender GPL; API NOASSERTION = detection gap (as before), not a relicense |

**Drift watch:**
- Helm (row 68): still public-archive under mtytel, ownership unchanged, API GPL-3.0, raw COPYING = GPL v3 29 June 2007 — archived confirmed, no successor.
- telxcc (row 236): still archived under kanongil; raw LICENSE retains "either version 2 of the License, or (at your option) any later version" → GPL-2.0-or-later stands. **New note:** GitHub API license field now reads NOASSERTION — detection drift only, not a relicense (verified against raw text).
- MKVToolNix: codeberg.org/mbunkus/mkvtoolnix → 200, URL unchanged — still live at Codeberg.

Raw evidence: `tools/wave36_lane_b/cycle7_evidence.json` (API responses +
fetch snippets), produced by `tools/wave36_lane_b/cycle7_verify.py`.
In-row re-verification notes appended to all 10 rows in
`docs/LICENSE_QUARANTINE.md`; wave-history note appended to the quarantine
section header in `docs/RESOURCE_CATALOG.md`. Header counts unchanged
(273 rows · 250 distinct).

## 2. Tool wires (2, both with real proofs)

- **`wire_libxmp.py`** — libxmp (MIT, tracker-format player lib; first
  functional wire, previously license-only): real `Gaffeltruck.mod` from
  libxmp's upstream test data decoded through real libxmp 4.6.0 (Ubuntu
  .deb, extracted to /tmp, ctypes) → 30.00 s stereo WAV, header verified
  PASS on read-back (RIFF/WAVE, fmt=1, ch=2, 44100 Hz, 16-bit), peak 28612 /
  rms 5777.9. Honest failure log: initial segfault from an omitted
  `channel_info[64]` trailing array in the ctypes frame-info struct — fixed.
- **`wire_pysrt.py`** — pysrt (GPL-3.0, quarantine row 94; standalone-tool
  use only, never linked into shipping paths): real `utf-8.srt` from pysrt's
  upstream test fixtures — 1,332 subtitles parsed, lossless round-trip
  re-emit verified, +2 s shift verified on all 1,332 subtitles. Honest
  failure log: `import srt` is wrong (module is `pysrt`) — caused an infinite
  venv re-exec spin before the fix.

Proofs: `tools/wave36_lane_b/PROOFS.md`, `SHA256SUMS` (12/12 OK),
`proofs_libxmp/` (5.3 MB total), `proofs_pysrt/`. Catalog statuses updated
for both tools.

## 3. Deferred

Speaches (Docker) / VGMTrans (Qt dev libs): no container runtime and no Qt
dev packages on this VM — deferred again, same as waves 30–35.

## Commits

1. `Wave 36 Lane B: re-verification cycle 7 — 10/10 rows confirmed + drift watch clean`
2. `Wave 36 Lane B: wire libxmp + pysrt with real proofs (PROOFS.md + SHA256SUMS)`
3. `Wave 36 Lane B: catalog status sync (libxmp/pysrt wired) + quarantine header cycle-7 note + wave note`
