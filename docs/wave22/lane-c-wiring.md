# Wave 22 Lane C — tool wiring + smoke tests (2026-10-07)

Branch: `wave22-lane-c`. Scope: `tools/wave22_lane_c/` + `docs/wave22/` only.

## What was wired (4 real proofs, zero duplication of Lane A)

Lane A already proved: ttconv EBU-TT-D→SRT, LOC JSON API, Finna API,
noisereduce (spectral gating), Tesseract OCR. Lane C extended each lane
instead of repeating it:

| # | Tool | What it proves | Proof artifacts |
|---|------|----------------|-----------------|
| 1 | **OCRmyPDF 17.13.0** (MPL-2.0) | Scan PNG → searchable PDF; text layer extracted with `pdftotext`, all 5 lines + digits "123" recovered | `proofs/ocrmypdf-searchable.pdf`, `ocrmypdf-scan.png`, `ocrmypdf-extracted.txt` |
| 2 | **RNNoise v0.2** (BSD-3, xiph) | Built from source (autotools) + official model blob; real `rnnoise_demo` binary suppresses noise-only frames **−24.8 dB** | `proofs/rnnoise-{noisy,denoised,clean}.raw`, `rnnoise-active.npy`, `rnnoise-proof.txt` |
| 3 | **benchmarkstt** (EBU, Apache-2.0) | Caption-QA WER on a 20-word ref/hyp pair with 4 known errors → **WER 0.2000 exactly**, CER 0.1579 | `proofs/benchmarkstt-wer.json`, `-reference.txt`, `-hypothesis.txt` |
| 4 | **Gallica SRU** (BnF, keyless) | 3rd national-library API after LOC/Finna: `"musique militaire"` → **130,373 records**, incl. John Philip Sousa holdings | `proofs/gallica-sru-musique-militaire.xml`, `gallica-sru-summary.txt` |

Wiring scripts: `tools/wave22_lane_c/wire_*.py` (re-runnable). Full run
narrative + checksums: `tools/wave22_lane_c/proofs/PROOFS.md`,
`tools/wave22_lane_c/proofs/SHA256SUMS`.

## Honest failures / gotchas encountered
- `media.xiph.org/rnnoise/rnnoise-0.2.tar.gz` **404s** — used the GitHub
  mirror (`xiph/rnnoise` tag `v0.2`); the model blob on media.xiph.org
  downloaded fine.
- OCRmyPDF rejects DPI-less PNGs (`DpiError`) — needs `--image-dpi 200`.
- Gallica SRU returns **403 to default python/urllib user agents** — a
  browser UA header is required.
- RNNoise SNR on the synthetic vowel is flat (+0.03 dB): expected, the GRU
  model is trained on real human speech; the measured win is the −24.8 dB
  noise-only suppression.
- benchmarkstt JSON output is a list of `{title, result}` objects, not a
  dict (my first parse script, not the tool).

## Deferred (no runtime — not faked)
- **Speaches Docker smoke test** — no `docker`/`podman`/`nerdctl` in the
  sandbox; nothing to run.
- **VGMTrans smoke test** — no binary, checkout, or environment present.

## Reuse notes for TRIPPEDD
- OCRmyPDF is the natural "searchable PDF" stage on top of Lane A's
  Tesseract — national-library digitization pipeline.
- benchmarkstt drops straight into caption QC for promo/entrance-kit videos.
- RNNoise gives a real-time neural denoiser alongside noisereduce's
  spectral gating; `rnnoise_demo` wants 48 kHz mono s16 PCM.
- Gallica SRU is keyless but UA-gated; pattern generalizes to other SRU
  endpoints (the catalog's NLS/BNE/DDB rows).

## Environment side effects (outside repo, not committed)
- apt: `autoconf automake libtool` installed (needed for RNNoise build).
- `/tmp/rnnoise-0.2` — full RNNoise build tree incl. 22 MB model blob
  (ephemeral, not in repo).
- `/tmp/w22c_venv` — pip venv with `ocrmypdf`, `benchmarkstt`,
  `pdfminer.six` (ephemeral, not in repo).
- No binaries >100 MB committed; proofs dir is 892 KB total.
