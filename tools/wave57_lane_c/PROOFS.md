# Wave 57 Lane C — Tool Wiring Proofs

Branch: `wave57-lane-c` · Lane dir: `tools/wave57_lane_c/`
Environment: Linux x86_64, Python 3.12.3, lane venv (`.venv/`, gitignored).
License gate (both upstream, fetched live 2026-10-08):
- SpectralCluster (wq2012, PyPI `spectralcluster` 0.2.22) —
  **Apache-2.0** (PyPI classifier `License :: OSI Approved :: Apache
  Software License`; verbatim Apache-2.0 text at upstream LICENSE). ✅ PASS
- pyannote-metrics (pyannote, PyPI `pyannote-metrics` 4.1) —
  **MIT** (verbatim MIT LICENSE at upstream, CNRS / Hervé Bredin). ✅ PASS
- pyannote.audio (gated HF model terms) explicitly NOT used — permissive-only
  rule. pyannote-metrics is a pure metric library with no model downloads.

Environment notes:
- `/tmp` is a 512 MB tmpfs: pip ran with lane-local
  `TMPDIR=tools/wave57_lane_c/.scratch` (gitignored).
- `no_proxy`/`NO_PROXY` contained IPv6 literals (`::1`, `[::1]`) that crash
  httpx (huggingface_hub's HTTP client): stripped anything containing `::`
  before pip ran. Egress proxy itself kept.
- pip's default index pulled the CUDA torch; installed CPU-only torch from
  the PyTorch CPU index first (`torch 2.14.1+cpu`).
- sklearn 1.9 removed `sklearn.metrics.contingency_matrix` (now only in
  `sklearn.metrics.cluster`); wire script uses the surviving path.
- spectralcluster 0.2.22 removed the `p_percentile`/`gaussian_blur_sigma`
  constructor kwargs from older examples; used `custom_dist="cosine"`
  (correct for speaker embeddings).

## What this wires

Closes the embed → cluster → score loop as one measured diarization stage:

1. **Embed (Wave 56, reused as committed bytes):** real SpeechBrain
   ECAPA-TDNN 192-dim embeddings (`tools/wave56_lane_c/proofs/
   speechbrain_ecapa/embeddings.pt`) on the real Wave-56 two-speaker
   fixture. Input re-verified by SHA-256 against the Wave-56 manifest
   before any work — same bytes, not re-generated.
2. **Cluster (SpectralCluster):** `SpectralClusterer(min_clusters=2,
   max_clusters=4, custom_dist="cosine")` → speaker labels per segment.
3. **Score (pyannote-metrics):** reference + hypothesis RTTMs written to
   disk, re-parsed into `pyannote.core.Annotation` objects (scoring goes
   through the artifact bytes), scored with `DiarizationErrorRate` and
   `JaccardErrorRate`. Cluster-id → speaker-id mapping via Hungarian
   assignment on the contingency matrix (no label cheating).

Fixture ground truth (from `wire_speechbrain_ecapa.py`: seg_dur=1.5 s,
gap_dur=0.2 s, order A1 gap B1 gap A2 gap B2, 16 kHz):
A1 [0.0, 1.5) spk A · B1 [1.7, 3.2) spk B · A2 [3.4, 4.9) spk A · B2 [5.1, 6.6) spk B

| # | Check | Result | Measured |
|---|-------|--------|----------|
| 1 | input embeddings.pt SHA-256 matches Wave-56 manifest | PASS | `79eff78d…` matches |
| 2 | embedding shape (4, 192) | PASS | (4, 192) |
| 3 | embeddings finite | PASS | no NaN/Inf |
| 4 | SpectralCluster finds exactly 2 clusters | PASS | labels [0, 1, 0, 1] |
| 5 | clustering deterministic across runs | PASS | re-run identical |
| 6 | speaker purity: A1/A2 one cluster, B1/B2 the other | PASS | A→c0, B→c1 (Hungarian map {0: A, 1: B}) |
| 7 | DER = 0 | PASS | DER 0.0000 — miss 0.0, FA 0.0, confusion 0.0 over 6.0 s speech |
| 8 | JER = 0 | PASS | JER 0.0000 (per-speaker perfect) |
| 9 | runs to completion | PASS | ~1.0 s end-to-end |

**9/9 PASS.** Raw numbers: `proofs/spectral_cluster/result.json`.
Production read: the stage is complete and measured — embeddings separate
the two synthetic voices with margin (Wave 56: +0.1483), and spectral
clustering recovers the speakers perfectly on this fixture. This proves the
pipeline wiring, not production diarization: only 4 segment-level
embeddings were clustered (no frame-level sliding windows, no overlap
handling, synthetic harmonic "voices"). The next real test is Wizard Gang
cast audio (2+ real Kokoro voices) at frame level.

Artifacts: `proofs/spectral_cluster/` (reference.rttm, hypothesis.rttm, result.json).

Catalog: `docs/RESOURCE_CATALOG.md` — `#### SpectralCluster (wq2012)` and
`#### pyannote-metrics` — Status →
**WIRED — run-proven (Wave 57 Lane C, 2026-10-08)**.

## SHA-256

See `SHA256SUMS` (lane dir) — covers the wire script, PROOFS.md, and all
proof artifacts. Verify with `sha256sum -c SHA256SUMS` from the lane dir.

## Versions

spectralcluster 0.2.22 · pyannote-metrics 4.1 · torch 2.14.1+cpu ·
scikit-learn 1.9.1 · scipy 1.18.1 · numpy 2.5.3.
