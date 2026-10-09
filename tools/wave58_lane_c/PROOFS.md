# Wave 58 Lane C — First REAL-VOICE diarization test (frame/window level)

Branch: `wave58-lane-w58c` · Lane dir: `tools/wave58_lane_c/`
Environment: Linux x86_64, Python 3.12.3, lane venv (`venv/`, gitignored).
Wire script: `wire_real_voice_diarization.py` (MIT, original). Re-run with `--resume`
to skip TTS (reuses `dialogue.wav` + `ground_truth.json` after SHA-256 check).

License gate (all upstream, verified live 2026-10-08):
- Kokoro-82M (hexgrad) — **Apache-2.0** (HF card frontmatter; wired Wave 51)
- SpeechBrain — **Apache-2.0** (GitHub API spdx_id); model
  `speechbrain/spkrec-ecapa-voxceleb` card tagged `license:apache-2.0`, ungated (wired Wave 56)
- SpectralCluster 0.2.22 — **Apache-2.0** (wired Wave 57)
- pyannote-metrics 4.1 — **MIT** (pure metrics, no model downloads; wired Wave 57)

Environment notes / honest failures:
- `/tmp` is a 512 MB tmpfs: pip ran with lane-local
  `TMPDIR=tools/wave58_lane_c/scratch` (gitignored).
- `no_proxy`/`NO_PROXY` contained IPv6 literals (`::1`, `[::1]`) that crash
  httpx (`InvalidURL: Invalid port: ':1]'` — hit twice, once at Kokoro
  `KPipeline` init, once at SpeechBrain HF download): stripped anything
  containing `::` before pip ran AND before the script ran. Egress proxy kept.
- pip's default index pulls the CUDA torch (2.3 GB of nvidia wheels — no GPU
  here); installed CPU-only torch first (`torch 2.14.1+cpu`,
  `torchaudio 2.11.0+cpu` from the PyTorch CPU index).
- numpy pin dropped: pyannote-metrics 4.1 requires `numpy>=2.2.2`, conflicting
  with the Wave-56 numpy==1.26.4 pin (that pin existed only for DeepFilterNet,
  not on this lane's path). Resolved unpinned → numpy 2.5.3, no conflict.
- pyannote-metrics 4.1's `DER.compute_components()` keys are
  `['confusion','total','correct','false alarm','missed detection']` —
  NOT `['miss',...]`; script fixed for this version.
- Two runs died mid-write (one `httpx` no_proxy crash, one service restart
  truncating `result.json` at 1755 bytes) — rerun cleanly; final numbers are
  from a single clean run, identical across re-runs (DER/JER stable to 4dp).

Versions: torch 2.14.1+cpu · torchaudio 2.11.0+cpu · speechbrain 1.1.1 ·
kokoro 0.9.4 · spectralcluster 0.2.22 · pyannote-metrics 4.1 · numpy 2.5.3 ·
soundfile 0.14.0 · scipy · scikit-learn 1.9.1 · espeak-ng 1.51 (system, Kokoro G2P).

## What this wires

The full embed → cluster → score diarization stage on REAL voices at
window/frame level — the honest step up from Wave 57, whose DER=0.0000 was
measured segment-level on a SYNTHETIC 4-segment fixture (harmonic-complex tones).

1. **TTS (real voices):** original 9-turn dialogue, 3 Kokoro voices —
   A=`af_heart` (F), B=`am_puck` (M), C=`af_bella` (F) — rendered seeded
   (reproducible), concatenated with 0.4 s silence gaps. A and C are BOTH
   female voices on purpose: harder than an F/M split. Audio sanity:
   peak 0.95 (no clip), per-turn spectral centroids consistent per voice
   (A~2.4 kHz, B~1.9 kHz, C~2.0 kHz). 42.9 s total, 16 kHz.
2. **Embed:** SpeechBrain ECAPA-TDNN 192-dim, sliding windows 1.5 s / 0.25 s
   hop; silence windows gated by energy (rms ≥ 8% of max) → 160 speech windows
   of 166 embedded (speech windows ONLY are clustered).
3. **Cluster:** SpectralClusterer(min_clusters=2, max_clusters=4,
   custom_dist="cosine") on speech-window embeddings.
4. **Frame labels:** each 0.25 s frame takes the label of the window centered
   on it; silence frames break runs; contiguous runs → segments.
5. **Score:** reference + hypothesis RTTMs re-parsed into
   `pyannote.core.Annotation`, scored with `DiarizationErrorRate` and
   `JaccardErrorRate`. Cluster→speaker map via Hungarian assignment on
   frame-level contingency (no label cheating).

| # | Check | Result | Measured |
|---|-------|--------|----------|
| 1 | 3 distinct Kokoro voices rendered (9 turns) | PASS | af_bella/af_heart/am_puck, 9 turns |
| 2 | ground truth spans full audio | PASS | audio 42.90 s, last turn end 42.50 s |
| 3 | embedding shape (N_speech_windows, 192) | PASS | (160, 192) |
| 4 | embeddings finite | PASS | no NaN/Inf |
| 5 | silence gate sane | PASS | thr 0.0109 vs max_rms 0.136 |
| 6 | cluster count within [2,4] | PASS | **2 clusters** (merged the two female voices) |
| 7 | clustering deterministic across runs | PASS | re-run identical |
| 8 | Hungarian cluster→speaker map exists | PASS | {0→B, 1→C}; speaker A unmapped |
| 9 | frame-level purity ≥ 0.80 | **FAIL** | 0.6879 over 157 speech frames |
| 10 | DER finite & reported (collar 0.0) | PASS | **DER 0.4084** (miss 0.0 s, FA 3.7 s, confusion 12.35 s / 39.3 s) |
| 11 | JER finite & reported (collar 0.0) | PASS | **JER 0.5478** |

**10/11 PASS.** Collar 0.25 (standard boundary forgiveness): DER 0.3556, JER 0.5170.

Timings: ECAPA load 1.2 s · embed 17.8 s · cluster 2.2 s · total 30.1 s
(CPU; TTS ~5 min on first run, skipped with `--resume`).

## The honest gap vs Wave 57

| Setup | Voices | Level | DER | JER |
|---|---|---|---|---|
| Wave 57 (segment-level, synthetic tones) | 2 synthetic | segment | 0.0000 | 0.0000 |
| **This wave (auto k, real Kokoro voices)** | **3 (F+M+F)** | **window/frame** | **0.4084** | **0.5478** |
| This wave, k forced = 3 (diagnostic) | 3 (F+M+F) | window/frame | 0.3359 | 0.4054 |

Three real findings, none flattering:
1. **Auto cluster-count selection merges the two female voices.**
   SpectralCluster chose k=2; Hungarian mapped {0→B, 1→C} and speaker A's
   turns (~12 s) became pure confusion. The male voice separates cleanly;
   af_heart vs af_bella do not at 1.5 s windows with automatic k.
2. **The embeddings DO separate all three voices — when k is given.**
   Forced k=3 recovered the exact map {0→B, 1→C, 2→A}, purity 0.7580,
   DER 0.3359 / JER 0.4054. So the information is in the ECAPA embeddings;
   the failure is in the count-selection step, not the embedding step.
3. **Even with perfect k, window-level DER ≈ 0.34, not 0.00.**
   The remaining gap vs Wave 57 is structural: boundary windows straddle
   speaker changes (FA 3.7 s at collar 0), and 0.25 s frame quantization
   inflates confusion. Real diarization needs VAD-boundary refinement and/or
   overlap handling — that is the next lane, not this one.

## Artifacts

`proofs/real_voice_diarization/`: `dialogue.wav` (42.9 s, 16 kHz mono) ·
`ground_truth.json` (per-turn speaker/voice/start/end + wav SHA-256) ·
`embeddings.pt` (160×192 float32) · `reference.rttm` · `hypothesis.rttm` ·
`result.json` (all numbers + check list).

Catalog updates: `docs/RESOURCE_CATALOG.md` — SpeechBrain entry → WIRED —
run-proven (Wave 58 Lane C); SpectralCluster / pyannote-metrics entries were
already WIRED (Wave 57) — left untouched, no duplicates added.
