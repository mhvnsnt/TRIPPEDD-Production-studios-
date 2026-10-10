# Meyda smoke-test proof (Wave 26 Lane A, 2026-10-07)

**Tool:** Meyda 5.6.3 — MIT (GitHub API spdx_id verified: hughrawlinson/meyda)
**Catalog entry:** `#### Meyda ✅ commercial-safe` (Wave 26 Lane A, pocket 2)

## What was run
1. `python3` synthesized `test-440.wav` — 2 s mono 16-bit PCM @ 44.1 kHz:
   440 Hz sine + 0.4 × 880 Hz harmonic. No copyrighted audio involved.
2. `npm install meyda` (33 packages, version 5.6.3).
3. `node meyda-smoke.js` — parses the WAV PCM16 payload manually, runs
   `Meyda.extract` on frame 0 (rms, energy, spectralCentroid, spectralRolloff,
   zcr, mfcc, chroma, spectralFlatness) plus a full-buffer MFCC mean over
   172 frames. Output written to `meyda-smoke-output.json`.

## Result — PASS
- chroma peak bin = **9** → A (440 Hz = A4). Correct.
- spectralRolloff ≈ 1038 Hz — consistent with 440 + 880 Hz content. Correct.
- zeroCrossingRate = 10 per 512-sample frame — matches 440 Hz (≈10 crossings
  per 11.6 ms). Correct.
- MFCC means stable across all 172 frames. Correct.

One API note: Meyda 5.6.3 names the zero-crossing extractor `zcr`
(not `zeroCrossingRate`); the script was corrected and re-run — the
committed output is from the passing run.

## Pipeline relevance
Meyda gives per-cue audio descriptors (brightness via spectral centroid,
rhythmic energy via RMS/energy, pitch class via chroma) for the cartoon's
music/scoring lane — e.g., auto-tagging score stems or matching SFX energy
to scene intensity. MIT-licensed, no GPL contamination.
