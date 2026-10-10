# Wave 21 Lane D wire-up proofs — IMSC tooling depth

Lane: D (EBU-TT Live / IMSC tooling depth) · Date: 2026-10-07
Driver: `tools/captions/imsc13_wireup.py` (re-runnable, stdlib + venv binaries)
Venv: `~/venvs/wave21-laneD-captions` — ttconv 1.2.3, imschrm 1.1.0 (both pip-installed)

## Proof 1 — WebVTT → IMSC TTML conversion (ttconv, BSD-2-Clause)
- Input: `sample.vtt` (3 cues, incl. an italic span)
- Command: `tt convert -i sample.vtt -o sample_imsc.ttml --itype VTT --otype TTML`
- Result: exit 0. Output `sample_imsc.ttml` is an IMSC TTML doc (IMSC styling
  namespace `http://www.w3.org/ns/ttml/profile/imsc1#styling`, EBU-TT style
  attrs, clock-time timings preserved).
- Note: ttconv 1.2.3's canonical model is constrained by the **IMSC 1.3 Text
  Profile** (per current upstream README) — the catalog's Wave 12 ttconv entry
  predates this; conversion target is current.

## Proof 2 — IMSC Hypothetical Render Model validation (imscHRM, BSD-2-Clause)
- `imschrm sample_imsc.ttml` → exit 0 (conforms).
- `imschrm dur001-pass.ttml` (W3C w3c/imsc-hrm-tests pass sample) → exit 0.
- `imschrm dur001-fail.ttml` (W3C w3c/imsc-hrm-tests fail sample) → exit 1,
  stderr: "ERROR:imschrm.hrm:Rendering time exceeded at 3.000s (doc #2)
  available time: 0.500s | HRM time: 0.514 …" — validator discriminates
  conforming vs non-conforming documents, not a rubber stamp.

## Files
- `sample.vtt` — input captions
- `sample_imsc.ttml` — ttconv IMSC TTML output (HRM-conformant)
- `dur001-pass.ttml`, `dur001-fail.ttml` — W3C imsc-hrm-tests samples
- Driver re-run: `~/venvs/wave21-laneD-captions/bin/python tools/captions/imsc13_wireup.py`

## Failures / honest notes
- None on this lane's wire-up. imscHRM is a pure validator (no false-pass on the
  fail sample); ttconv 1.2.3 installed cleanly from PyPI.
