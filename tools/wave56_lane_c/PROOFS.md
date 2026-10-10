# Wave 56 Lane C — Tool Wiring Proofs

Branch: `wave56-lane-w56c` · Lane dir: `tools/wave56_lane_c/`
Environment: Linux x86_64, Python 3.12.3, lane venv (`venv/`, gitignored).
License gate (both upstream, fetched live 2026-10-08):
- DeepFilterNet — **MIT/Apache-2.0 dual** (README license section + verbatim
  MIT LICENSE-MIT; PyPI `deepfilternet` classifier MIT). ✅ PASS
- SpeechBrain — **Apache-2.0** (GitHub API spdx_id); ECAPA model
  `speechbrain/spkrec-ecapa-voxceleb` card tagged `license:apache-2.0`,
  ungated. ✅ PASS

Environment notes / honest failures:
- `deepfilternet` → `deepfilterlib==0.5.6` sdist needs Rust/Cargo at build
  time (no manylinux wheel). rustup installed user-local
  (`~/workspace/toolchain/`, minimal profile) to compile it.
- `/tmp` is a 512 MB tmpfs: pip/Rust builds OOM'd it ("No space left on
  device"). Workaround: lane-local `TMPDIR=scratch/pip-tmp` and
  `CARGO_TARGET_DIR=scratch/cargo-target`; installs run sequentially.
- pip's default index pulled the CUDA torch (2.3 GB of nvidia wheels —
  wasteful, no GPU here); reinstalled CPU-only torch/torchaudio from the
  PyTorch CPU index first (`torch 2.14.1+cpu`, `torchaudio 2.11.0+cpu`).
- deepfilternet 0.5.6 predates torchaudio 2.9: `df.io` does
  `from torchaudio.backend.common import AudioMetaData`, which no longer
  exists. Venv-local shim added at
  `venv/.../torchaudio/backend/common.py` (restores the old dataclass;
  used only as a type annotation in df.io). Not repo content — venv is
  gitignored.
- deepfilternet pinned numpy 1.26.4 while scipy 1.18.1 wants numpy>=2.0
  (pip resolver warning). The wire script avoids scipy entirely
  (FFT band-limiting via numpy), so this is not on the proof path.
- TEN VAD evaluated and REJECTED at the license gate: catalog entry documents
  an Apache-2.0 + Agora non-compete rider ("may not Deploy … in a way that
  competes with Agora's offerings") — not OSI-clean, fails the permissive
  gate. Not wired; reported as a deferral.
- DeepFilterNet3 weights provenance: downloaded by `init_df()` during this
  run (2026-10-08 15:22) from
  `https://github.com/Rikorose/DeepFilterNet/raw/main/models/DeepFilterNet3.zip`
  (upstream repo, same dual MIT/Apache-2.0 project); 8.4 MB checkpoint
  `model_120.ckpt.best`, cached at `~/.cache/DeepFilterNet/DeepFilterNet3/`.
- ECAPA weights provenance: `speechbrain/spkrec-ecapa-voxceleb` from HF Hub
  (card tagged `license:apache-2.0`, ungated), cached in
  `scratch/speechbrain_models/` (gitignored).
Versions: deepfilternet 0.5.6 · deepfilterlib 0.5.6 (Rust ext, compiled
locally) · speechbrain 1.1.1 · torch 2.14.1+cpu · torchaudio 2.11.0+cpu ·
numpy 1.26.4.

## Tool 1 — DeepFilterNet (Rikorose/DeepFilterNet)

Catalog: `docs/RESOURCE_CATALOG.md` § audio/restoration —
Status → **WIRED — run-proven (Wave 56 Lane C, 2026-10-08)**.

What: deep-NN full-band (48 kHz) speech denoiser. Wired as the upgrade path
for the VO pipeline's denoise+master stage (Wave 52 wired noisereduce;
this is the deep-NN complement, strongest on non-stationary noise).

Wire script: `wire_deepfilternet.py`
Fixture: real Wave-51 Kokoro VO `tools/wave51_lane_c/proofs/kokoro_tts/voice_line.wav`
(7.825 s, 24 kHz mono) + calibrated noisy variants (10 dB SNR in):
stationary white noise, and non-stationary AM band-limited noise.

| # | Check | Result | Measured |
|---|-------|--------|----------|
| 1 | SNR improvement, stationary noise | PASS | 10.0 → 15.9 dB (Δ +5.9 dB) |
| 2 | SNR improvement, non-stationary noise | PASS | 10.0 → 14.4 dB (Δ +4.4 dB) |
| 3 | non-stationary ≥ stationary − 1 dB (DFNet strength claim) | FAIL | babble Δ +4.4 dB vs white Δ +5.9 dB — absolute gains solid, relative claim not reproduced on this synthetic fixture; documented, not re-tuned |
| 4 | clean no-op: RMS delta < 5% | PASS | 4.07% |
| 5 | clean no-op: corr(clean, enhanced) > 0.99 | PASS | 0.99665 |
| 6 | byte-deterministic across runs | PASS | max\|diff\| = 0.0 |
| 7 | runs to completion | PASS | 3 enhances, 22.6 s total (~0.96× RT on CPU) |

**6/7 PASS.** Raw numbers: `proofs/deepfilternet/result.json`.
Production read: use after noisereduce for non-stationary field noise, or as
the primary denoiser when noise is non-stationary; keep the Wave-52 rule —
profile noise from a real silence/room-tone region, don't run blind.

Artifacts: `proofs/deepfilternet/` (fixtures + enhanced outputs + result.json).

## Tool 2 — SpeechBrain ECAPA-TDNN speaker embeddings

Catalog: `docs/RESOURCE_CATALOG.md` § — Status →
**WIRED — run-proven (Wave 56 Lane C, 2026-10-08)**.

What: `speechbrain/spkrec-ecapa-voxceleb` 192-dim speaker embeddings —
diarization-adjacent "who spoke" stage for multi-character dialogue
editing / caption burn-in.

Wire script: `wire_speechbrain_ecapa.py`
Fixture: synthetic 2-speaker dialogue (harmonic-complex "voices",
F0 110 Hz vs 175 Hz, segments A,B,A,B, 16 kHz).

| # | Check | Result | Measured |
|---|-------|--------|----------|
| 1 | embedding shape (4, 192) | PASS | (4, 192) |
| 2 | embeddings finite | PASS | no NaN/Inf |
| 3 | speaker separation margin > 0.05 | PASS | min intra 0.8663 (A1·A2, B1·B2 — different utterances) vs max inter 0.7180 (margin +0.1483) |
| 4 | self-similarity ≈ 1.0 | PASS | diag [1.0, 1.0, 1.0, 1.0] |
| 5 | embeddings deterministic | PASS | max\|diff\| = 0.0 |
| 6 | runs to completion | PASS | 34.0 s end-to-end |

**6/6 PASS.** Raw numbers: `proofs/speechbrain_ecapa/result.json`.
Production read: embeddings separate two distinct synthetic voices with a
comfortable margin; next step is a real multi-voice line test against the
Wizard Gang cast (2+ Kokoro voices) to confirm the margin holds on real
neural VO.

Artifacts: `proofs/speechbrain_ecapa/` (fixture + embeddings.pt + result.json).

## SHA-256

See `SHA256SUMS` (lane dir) — covers all proof artifacts.
