# Wave 22 Lane A — wire-up proofs (2026-10-07)

Real artifacts, real runs. No fakes.

## 1. EBU-TT-D → SRT via ttconv (new this wave)
- **Input:** real IRT reference sample `ebu-tt-d-sample.xml` (IRT-Open-Source/irt-ebu-tt-d-application-samples, Apache-2.0; `ttml/cumulative-rows-001-ttml.xml`, 2744 bytes)
- **Run:** `ttconv.imsc.reader.to_model` → `ttconv.srt.writer.from_model`
- **Output:** `ebu-tt-d-sample.srt` — 8+ cues, correct cumulative-row timing (00:00:16,000 → …)
- **Note:** ttconv's public API differs from older docs (no `IMSCReader`); the working path is `imsc.reader.to_model` + `srt.writer.from_model`. See `ebu-tt-d-sample.srt`.

## 2. LOC JSON API (keyless)
- **Query:** `https://www.loc.gov/photos/?fo=json&c=10&q=military+band`
- **Result:** HTTP 200, 254,219 bytes, 63 results; first item "Military band, Christiansand, Norway" (1907), https://www.loc.gov/item/2021638059/
- **Saved:** `loc-military-band.json`

## 3. Finna API (keyless)
- **Query:** `https://api.finna.fi/v1/search?lookfor=sotilassoittokunta&limit=3`
- **Result:** HTTP 200, status OK, 2,812 records for "sotilassoittokunta" (Finnish for military band)
- **Saved:** `finna-test.json`
- **Note:** first attempt with an English query + format filter returned 0 — the API needs Finnish terms for Finnish collections; retried honestly.

## 4. noisereduce (spectral gating)
- **Test:** 2 s 440 Hz sine + white noise @16 kHz (seeded RNG)
- **Result:** noisy SNR −2.97 dB → denoised SNR +0.21 dB (**+3.18 dB improvement**), stationary mode
- **Saved:** `noisereduce-proof.txt`

## 5. Tesseract OCR (binary 5.3.4, installed via apt this wave)
- **Test:** PIL-rendered page (3 lines incl. digits), `tesseract ocr-test.png stdout`
- **Result:** 100% character-accurate transcription
- **Saved:** `ocr-test.png`, `ocr-test-result.txt`

## Failures / honest gaps
- `ultimatevocalremovergui`: no license statement in repo — skipped, not cataloged.
- `eScriptorium` (UB-Mannheim/escriptorium): NOASSERTION, no license file found — skipped.
- `BookScanWizard`: upstream repo not locatable — skipped.
- Several military-band official sites returned empty/blocked pages (esercito.it, defensie.nl music page) — those entries carry ⚠️ "verify before reuse" rather than claimed terms.
- Finna English-query attempt returned 0 records (documented above; Finnish term worked).
