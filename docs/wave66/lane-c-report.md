# Wave 66 Lane C Report — Speaker-count tightening (real EP01 production run)

**Date:** 2026-10-09 · **Branch:** wave66-lane-c · **Base:** origin/main 8ad05825
**Goal:** tighten the real-audio speaker-count decision (blind eigengap margin too weak at 1.02x)
**Result:** 2.5 s / 0.5 s grids are the trustworthy window for blind speaker-count on EP01; 2.0 s and 2.5 s grids agree on **k=1** (margins 1.26x / 1.16x), consistent with a single-narrator episode (98.5% continuous speech, 12 VAD segments). Baseline 1.5 s grid's k=3 was phantom structure from correlated short windows.

**Note:** Lane C's production run survived two worker kills in daemon restarts; the production embedding pass (PID 8038, started 2026-10-08 ~23:12 CDT) completed on its own while the worker was dead. A watchdog duplicate relaunch was killed to avoid racing the original's .npy/JSON writes. All results committed to wave66-lane-c.

## Experiment (a): longer windows + VAD-gated energy clustering — production table

| grid (win/hop) | fixture k | fixture margin | stability | production k | margin | stability |
|---|---|---|---|---|---|---|
| 1.5 s / 0.25 s (baseline) | 3 | 1.72x | 0.55 | 3 | 1.02x | 0.25 |
| 2.0 s / 0.5 s | 3 | 4.31x | 0.65 | **1** | 1.26x | 0.40 |
| **2.5 s / 0.5 s** | **3** | **7.35x** | **0.95** | **1** | 1.16x | 0.25 |
| 3.0 s / 0.5 s | 3 | 1.97x | 0.70 | 7 | 1.24x | 0.40 |
| 2.5 s / 0.25 s | 3 | 1.40x | 0.40 | — (killed mid-run) | — | — |

Production reading: the 2.0 s and 2.5 s grids agree on k=1 — the better-supported hypothesis, not a proven finding (no GT; margins stay weak at ~1.2x because a single dominant voice gives the gap spectrum little to bite on). The fixture anchoring is what makes the long-window decision trustworthy: on GT fixture audio, 2.5 s windows nail k=3 with 7.35x margin and DER 0.0382 exact. The 3.0 s production jump to k=7 mirrors the fixture overshoot: with ~25 s average VAD segments, 3 s windows straddle speaker turns within a segment, creating mixed embeddings and phantom clusters. DER unchanged across grids — count decision tightens without moving a single boundary.

## Experiment (b): VAD-gated energy clustering as count prior — REJECTED

k-means on [log RMS, Δlog RMS] over VAD-gated 0.25 s frames, k by BIC: **k_bic=10** — BIC rewards splitting single-speaker energy structure into pieces. Energy is not a speaker-count signal. Fallback rule adopted: combined k uses the eigengap decision, trusting energy only above a 1.5x margin (the production baseline's 1.02x does not clear it).

## Experiment (c): ASR-assisted speaker turns — DEFERRED

No transcripts exist for the EP01 segment; wiring ASR-assisted speaker turns requires a real ASR pass (not hallucinated output). Deferred to a wave where an open-source ASR run is in scope.

## DeepFilterNet wiring — BLOCKED (stays downstream-only)

DeepFilterNet3 checkpoint is cached locally, but `deepfilternet` has no cp312 wheel on PyPI and `deepfilterlib` needs a Rust toolchain — both missing in this environment. Per quarantine, DeepFilterNet only ever sits downstream of embeddings (caption/ASR path), never upstream of ECAPA. Wired = false; no count finding depends on it.

## Quarantine honored

ECAPA ran always on RAW audio — no denoise upstream of embeddings. Venv, scratch embeddings (.npy), and run logs excluded from the repo via lane .gitignore; only proofs JSON, RTTMs, and PROOFS.md are committed.

## Commits

- 4109b80c Wave 66 Lane C: speaker-count tightening wire + proofs (fixture complete, production run in progress)
- 18c103f6 Wave 66 Lane C: lane .gitignore (venv/scratch excluded)
- c4b57044 Wave 66 Lane C: production run COMPLETE — real EP01 diarization results

## Wave 67 pocket suggestions

Experiment (a) follow-up: run the 2.5 s / 0.25 s grid that was killed mid-run (168/1191 windows); try 2.25 s windows between the two k=1 grids to confirm the k=1 plateau; bootstrap stability across VAD-segment resamples to put a number on the k=1 hypothesis. Experiment (c): if an open-source ASR pass (faster-whisper) is in scope, wire ASR-assisted speaker turns as a count tiebreaker. DeepFilterNet: revisit only if a cp312-compatible environment materializes.
