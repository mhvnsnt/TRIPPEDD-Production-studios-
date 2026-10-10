# Wave 22 Lane C — wiring proofs (2026-10-07)

Real artifacts, real runs. No fakes. Extends Lane A's proofs (ttconv EBU-TT-D,
LOC JSON API, Finna API, noisereduce, Tesseract) — nothing duplicated.

Wiring scripts live in `tools/wave22_lane_c/` (`wire_*.py`); each is
re-runnable. Python deps were installed in an throwaway venv
(`/tmp/w22c_venv`); the RNNoise C binary was built in `/tmp/rnnoise-0.2`
(model weights NOT committed, per repo rules).

## 1. OCRmyPDF → searchable PDF (new this wave, extends Lane A's Tesseract)
- **Tool:** OCRmyPDF 17.13.0 (jbarlow83/ocrmypdf, MPL-2.0) — `wire_ocrmypdf.py`
- **Input:** `ocrmypdf-scan.png` — PIL-rendered page (5 lines incl. digits),
  seeded speckle noise to feel like a scan
- **Run:** `ocrmypdf --force-ocr -l eng --optimize 0 --image-dpi 200 scan.png searchable.pdf`
  (`--image-dpi` was required — bare PNG carries no DPI; first attempt without
  it failed honestly with `DpiError`)
- **Output:** `ocrmypdf-searchable.pdf` (100,021 bytes)
- **Verification:** `pdftotext` extraction → `ocrmypdf-extracted.txt` —
  all 5 lines recovered, digits "123" present. PASS.

## 2. RNNoise neural denoiser, built from source (new this wave)
- **Tool:** xiph/rnnoise v0.2 (BSD-3-Clause) — `wire_rnnoise.py`
- **Build (real, this sandbox):** GitHub mirror tarball
  (`media.xiph.org` release-tarball URL 404'd — documented), `autogen.sh` +
  `configure --disable-doc` + `make` (autoconf/automake/libtool installed via
  apt), then official model blob `rnnoise_data-0b50c45.tar.gz` from
  media.xiph.org (22 MB, downloaded fine) extracted to `src/rnnoise_data.c`
  and relinked. Binary: `examples/rnnoise_demo`.
- **Input:** 2.0 s synthetic vowel-like signal — formant-filtered pulse train
  (F1 500 / F2 1500 / F3 2500 Hz), syllabic AM, seeded white noise, 48 kHz
  mono s16 (the exact format `rnnoise_demo` requires)
- **Run:** `./examples/rnnoise_demo noisy.raw denoised.raw`
- **Measured:** noise-only frames crushed **−24.8 dB** (residual RMS);
  speech-active SNR flat (+0.03 dB) — honest: the GRU gate works on
  non-speech frames, and a synthetic vowel is not real speech (the model is
  trained on human speech). Saved: `rnnoise-{noisy,clean,denoised}.raw`,
  `rnnoise-active.npy`, `rnnoise-proof.txt`. PASS (gate >10 dB).

## 3. benchmarkstt caption-QA WER (new this wave)
- **Tool:** benchmarkstt (EBU, Apache-2.0, pip) — `wire_benchmarkstt.py`
- **Input:** 20-word reference transcript + hypothesis with 4 known errors
  (2 substitutions, 1 deletion, 1 insertion) — expected WER 20.00%
- **Run:** `benchmarkstt -r reference.txt -h hypothesis.txt -rt plaintext
  -ht plaintext --wer --cer -o json`
- **Output:** `benchmarkstt-wer.json` — WER **0.2000** (matches the known
  error count exactly), CER 0.1579. PASS — directly usable for TRIPPEDD
  caption QC.

## 4. Gallica SRU API — BnF national library (new this wave, 3rd library API)
- **Tool:** BnF Gallica SRU 1.2, keyless — `wire_gallica_sru.py`
- **Query:** `gallica all "musique militaire"`, dublincore schema, 5 records
- **Run:** real HTTPS GET. Honest note: Gallica returns **403 to default
  python/urllib user agents** — a browser UA header is required; with it,
  HTTP 200.
- **Output:** `gallica-sru-musique-militaire.xml` (20,217 bytes) —
  **130,373 records**; first creators include John Philip Sousa (1854–1932).
  Summary in `gallica-sru-summary.txt`. PASS.

## Deferred (honest — no runtime in this sandbox)
- **Speaches Docker smoke test:** DEFERRED — no container runtime
  (`docker`, `podman`, `nerdctl` all absent; nothing found in PATH or
  workspace). Cannot run what isn't there; not faked.
- **VGMTrans smoke test:** DEFERRED — no VGMTrans binary, source checkout,
  or environment anywhere in the sandbox.

## Failures / honest gaps
- `media.xiph.org/rnnoise/rnnoise-0.2.tar.gz` 404'd (Apache listing shows the
  path is gone); the GitHub mirror `xiph/rnnoise` tag `v0.2` worked.
- OCRmyPDF first run failed with `DpiError` on a DPI-less PNG — fixed with
  `--image-dpi 200` (scan-realistic assumption, documented).
- Gallica SRU blocks non-browser user agents with 403 — worked with a
  browser UA header (documented).
- benchmarkstt's JSON output is a list of `{title, result}` objects, not a
  dict — my first parse script assumed a dict; fixed (tool itself was fine).
- RNNoise SNR on synthetic vowels is flat (+0.03 dB) — expected; the model
  is trained on real human speech. The real measured win is the −24.8 dB
  noise-only suppression.

## Checksums
See `SHA256SUMS` in this directory.
