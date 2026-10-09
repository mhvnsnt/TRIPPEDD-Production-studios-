# Wave 24 Lane B — tool wiring proofs (all real, 2026-10-07)

Run with the repo venv: `~/workspace/.venv-wave17-laneb/bin/python <script>`
(scipy/intervaltree/tabulate/webrtcvad-wheels installed there for this wave;
Pillow 10.2.0 was already present).

## 1. dscore_der_demo.py — nryant/dscore diarization scoring (BSD-2-Clause)

- Vendored scorelib: `tools/captions/vendor/dscore-scorelib/` (+ `dscore-LICENSE`,
  `dscore-README.md`; cloned 2026-10-07 from https://github.com/nryant/dscore).
  dscore is **not** pip-installable — PyPI's `dscore` is an unrelated protein
  tool (installed by mistake, uninstalled, documented here honestly).
- Method: synthetic 2-speaker RTTM reference vs perfect + degraded hypotheses,
  scored with the real NIST `md-eval-22.pl` path (`scorelib.metrics.der`,
  collar 0.25 s). `validate_rttm` passes on both inputs; write→load round-trip
  asserted lossless.
- Result: perfect hypothesis **DER = 0.00%**; degraded hypothesis
  (0.5 s miss + 3.0 s speaker confusion + 1.0 s false alarm) **DER = 70.00%**.
- Proof: `wave24_der_proof.json` + `wave24_{ref,hyp_perfect,hyp_degraded}.rttm`.

## 2. webrtcvad_segments.py — webrtcvad GMM VAD (MIT wrapper / BSD core)

- Method: synthesized 6 s / 16 kHz mono WAV (two speech-like bursts at
  0.5–2.0 s and 3.0–4.5 s in near-silence), webrtcvad aggressiveness 3,
  30 ms frames, 200 ms hangover merge.
- Result: **2 segments detected** — [0.48, 2.10] and [3.00, 4.59];
  coverage 1.00/1.00, purity 0.926/0.943. Assertions: segment count == 2,
  coverage > 0.8, purity > 0.8 — all passed.
- Proof: `wave24_vad_proof.json` + `wave24_synth.wav` (192 KB).

## 3. pillow_caption_card.py — Pillow caption-card renderer (HPND)

- Method: renders a 1920×1080 episode title card + broadcast-style lower-third
  caption bar in Noto Sans Regular/Bold (OFL-1.1, system fonts), re-opens the
  PNG and pixel-verifies both text regions.
- Result: card renders correctly (visually inspected 2026-10-07); the U+266A
  music-note glyphs in `[music] ♪ synth swell ♪` draw as real glyphs, not tofu.
- Proof: `wave24_caption_card.png` (37 KB) + `wave24_caption_card.json`.

## Deferred (documented, not faked)

- **Speaches Docker smoke test**: no container runtime in this lane
  (`docker`/`podman` both absent) — deferred per the task brief. Speaches
  itself is cataloged (MIT) as an entry, not a wired tool.
- subtitle-octopus / JASSUB: browser/WASM renderers — entries only, no
  headless-browser smoke test in this lane.
- go-astisub: entries only — no Go toolchain in the sandbox.
- SCTK: entries only — requires compiling the NIST C toolkit; not attempted.
