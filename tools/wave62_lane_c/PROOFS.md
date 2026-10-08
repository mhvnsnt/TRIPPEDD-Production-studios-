# Wave 62 Lane C — PROOFS: diarization pipeline rebuilt (denoise downstream)

**Production rule applied (Wave 61):** denoising is moved DOWNSTREAM of the
embedding stage — or off the speaker path entirely. The speaker path
(VAD → ECAPA embeddings → eigengap speaker count → clustering) sees RAW
audio only. DeepFilterNet3 is applied ONLY to per-speaker output segments
AFTER diarization (caption/cleanup path).

## 1. Rebuilt production topology (wired in `wire_diarization_rebuilt.py`)

```
raw audio (Wave-58 fixture: 42.9 s @16 kHz, 9 turns, 3 Kokoro voices —
           A=af_heart F, B=am_puck M, C=af_bella F; A/C both female on purpose)
  -> tuned webrtcvad VAD (aggressiveness 0 + 0.2 s hangover pad; Wave-59 winner)
  -> window grid 1.5 s / 0.25 s hop + energy gate (8% of max; Wave-58)
     -> drop windows straddling VAD boundaries (Wave-59 V2c)
  -> ECAPA-TDNN 192-dim embeddings computed on RAW audio
     (Wave-58 committed embeddings.pt, SHA-verified; kept windows are
      bit-identical raw slices of Wave-58's grid — no recompute, no denoise)
  -> eigengap E1a speaker-count estimator (Wave-60: symmetric normalized
     Laplacian, k-NN(7) cosine affinity, absolute gap)
  -> forced-k SpectralCluster (Apache-2.0)
  -> frame labeling inside VAD speech only, NO fill (Wave-59 V2c)
  -> hypothesis RTTM -> DER/JER via pyannote-metrics (MIT)

THEN, downstream (separate process, `wire_downstream_caption.py` /
`wire_step5_caption_burnin.py`):
  per-speaker hypothesis segments (raw audio) -> DeepFilterNet3 denoise
  -> denoised per-speaker wavs + caption burn-in onto the denoised mix.
  Denoise NEVER touches the embedding input.
```

Ablation control (same script, `mode=upstream`): DeepFilterNet BEFORE the
embedding stage with ECAPA recomputed on denoised audio (the Wave-61
topology), on clean AND on a seeded 10 dB-SNR white-noise variant
(seed 20261008, same noise as Wave-61), plus a `noisy_bypass` control
(no denoise, ECAPA on noisy audio).

## 2. Environment

- Linux x86_64, Python 3.12, lane venv (`venv/`, gitignored — see `.gitignore`).
- Rebuild recipe: `./install.sh` (torch 2.14.1+cpu FIRST from the CPU
  index, then webrtcvad, spectralcluster, soundfile, scikit-learn,
  pyannote-core + pyannote-metrics==4.1 + sortedcontainers,
  speechbrain==1.1.1, deepfilternet==0.5.6 with the lane-local Rust
  toolchain). Full pin list saved at
  `~/workspace/agent-ops/venv-manifests/wave62-lane-c.txt`.
- Key pins: torch==2.14.1+cpu, torchaudio==2.11.0+cpu,
  speechbrain==1.1.1, DeepFilterNet==0.5.6 / DeepFilterLib==0.5.6,
  webrtcvad==2.0.10, spectralcluster==0.2.22, pyannote-metrics==4.1,
  numpy==1.26.4, scikit-learn==1.9.1, soundfile==0.14.0.
- DeepFilterNet3 full-band weights reused from `~/.cache/DeepFilterNet/`;
  SpeechBrain ECAPA `speechbrain/spkrec-ecapa-voxceleb` downloaded fresh
  to lane `scratch/` (documented source; weights not committed).
- Compatibility note (documented): `df.io` does
  `from torchaudio.backend.common import AudioMetaData`, but torchaudio
  2.x removed `torchaudio.backend`. Both wire scripts inject a
  `torchaudio.backend.common` shim module (dataclass only) into
  `sys.modules` BEFORE `from df.enhance import ...` — never
  `import torchaudio.backend` (ModuleNotFoundError).

## 3. Re-measured DER/JER — rebuilt topology vs Wave-60 baseline

pyannote-metrics, Wave-58 fixture, reference = Wave-58 `reference.rttm`.

| variant | mode | eigengap k̂ (margin) | DER @c0.0 | JER @c0.0 | miss | FA | conf | purity |
|---|---|---|---|---|---|---|---|---|
| **main_clean (PRODUCTION)** | raw embeddings, no upstream denoise | 3 (2.11x) | **0.1158** | **0.1156** | 4.55 | 0.00 | 0.00 | 1.0000 |
| main_clean @collar 0.25 | — | — | 0.0628 | 0.0625 | 2.33 | 0.00 | 0.00 | — |
| upstream_clean (ablation) | denoise BEFORE embeddings | 3 (2.67x) | 0.1285 | 0.1284 | 5.05 | 0.00 | 0.00 | 1.0000 |
| upstream_noisy (ablation) | denoise before embeddings, 10 dB noise | **2 (k-flip!)** | 0.4275 | 0.5635 | 6.05 | 0.00 | 10.75 | 0.6767 |
| bypass_noisy (ablation) | NO denoise, 10 dB noise | 3 (3.24x) | 0.2239 | 0.2623 | 6.30 | 0.25 | 2.25 | 0.9318 |

**Honest baseline comparison (FAIL check recorded, not hidden):**
Wave-60 baseline = DER 0.0941 / JER 0.0844. The rebuilt production
topology measures **DER 0.1158 / JER 0.1156** — WORSE by +0.0217 DER.
The error decomposition explains it exactly; this is a VAD-coverage
trade-off, not a diarization-quality regression:

- Wave-60 (0.0941): full-window fill labeling → miss **0.0** / FA **3.70** /
  confusion **0.0** / purity 1.0. Residual DER is pure boundary false-alarm.
- Wave-62 rebuilt (0.1158): Wave-59 V2c topology — tuned VAD + dropped
  boundary-straddling windows (94 of 160 kept) + frame labeling inside
  VAD speech only, NO fill → miss **4.55** / FA **0.00** / confusion
  **0.00** / purity 1.0000. Residual DER is pure miss from the dropped
  coverage; false-alarm and confusion are both zero.

@ collar 0.25 the rebuilt topology scores 0.0628/0.0625 (boundary errors
forgiven). Speaker separation itself is intact: eigengap blind k=3,
all three voices mapped (A/B/C), frame purity 1.0, zero confusion.

## 4. Ablation: upstream denoise collapses speaker separation (Wave-61 re-confirmed)

Measured numbers are byte-equal to Wave-61's donor results:

| | Wave-61 | Wave-62 (this lane) |
|---|---|---|
| upstream_clean DER | 0.1285 | **0.1285** |
| upstream_noisy DER | 0.4275 | **0.4275** |
| bypass_noisy DER | 0.2239 | **0.2239** |

- Upstream denoise on 10 dB-noisy audio costs **+0.2036 DER**
  (0.4275 vs 0.2239 no-denoise) and flips blind speaker count **3 → 2**
  (eigengap margin collapses to 1.4x; purity drops to 0.6767).
- Mechanism re-measured (GT-informed diagnostic): GT-mean cosine
  cos(A,C) rises **0.6243 → 0.6326** on clean (0.5905 → 0.7438 on noisy) —
  the denoiser pushes the two female speaker means together.
- On clean audio upstream denoise also hurts-or-neutral: 0.1285 ≥ 0.1158.
- **Conclusion (Wave-61 finding confirmed with this wave's own numbers):
  DeepFilterNet must NEVER sit upstream of ECAPA embeddings. It is
  quarantined to the downstream per-speaker caption path.**

## 5. Downstream denoise value case (production path)

DeepFilterNet3 applied ONLY to per-speaker segments cut on the
main_clean hypothesis boundaries (speaker identity already fixed):

- Per-speaker denoised wavs: `denoised_spk_A.wav` (11.0 s),
  `denoised_spk_B.wav` (11.5 s), `denoised_spk_C.wav` (12.25 s);
  mixed to `downstream_denoised_mix.wav` on hypothesis timing.
- Clean no-op (denoise should be ~transparent on clean):
  RMS delta **2.53%** (< 5%, PASS), corr(raw, denoised mix) = **0.99901**
  (> 0.99, PASS).
- 10 dB-noise value case: downstream denoise moves SNR
  **10.0 → 16.5 dB (Δ +6.5 dB, PASS)** — the caption path gets the full
  denoise benefit WITHOUT touching the speaker path.

## 6. Caption burn-in (Wave-61 donor pattern, torch-free standalone)

- SRT + per-speaker-color ASS (A=gold FFD700, B=cyan 00E5FF, C=pink
  FF7AC8) written from hypothesis RTTM timing + GT turn texts
  (words; pipeline supplies who/when — no ASR stage wired).
- ffmpeg `showwaves` waveform render of the downstream-denoised mix
  (640×360 @30 fps) + libass burn-in → `burned_captions.mp4`.
- Pixel verification (Wave-50 method): caption-ON band diff **11.73/255**
  (> 2.0, PASS), caption-OFF band diff **0.00/255** (< 1.0, PASS),
  libass stderr clean. **5/5 checks PASS.**

## 7. Honest failure log

1. **Step-4 ECAPA diagnostic on the downstream-denoised mix — NOT
   COMPLETED.** The ECAPA process was SIGKILLed (OOM killer, `Killed`)
   4 times: twice inside the full stage-2 script (alongside
   DeepFilterNet3), twice as a standalone low-thread process. The shared
   VM was memory-constrained during those runs. This was a GT-informed
   bonus diagnostic ("quarantined effect" check); the production topology
   measurements and the ablation do not depend on it. It is omitted from
   the proof set rather than simulated.
2. `ref_rttm_sha` fixture check initially FAILED on a one-nibble
   transcription typo in the asserted hash (`...4f9e...` vs the true
   on-disk/git-HEAD `...4f3e...`); fixed, now PASS.
3. `init_denoiser()` initially did a bare `import torchaudio.backend`
   (removed in torchaudio 2.x); replaced with shim-only injection.
4. Stage 1 exited 1 on the honest baseline check (`set -e` stopped
   `run.sh`); stage 2 was completed via the standalone resume/step-5
   scripts with the already-denoised wavs reused.

## 8. License audit (wired path only)

| component | license | role |
|---|---|---|
| webrtcvad 2.0.10 | MIT | VAD |
| SpeechBrain 1.1.1 / spkrec-ecapa-voxceleb | Apache-2.0 | ECAPA embeddings |
| SpectralCluster 0.2.22 | Apache-2.0 | forced-k clustering |
| pyannote-metrics 4.1 (+ pyannote-core) | MIT | DER/JER scoring |
| DeepFilterNet 0.5.6 (Rikorose/DeepFilterNet) | dual MIT / Apache-2.0 | downstream-only denoise |
| scikit-learn, numpy, soundfile, ffmpeg | BSD / LGPL-libs / LGPL-GPL | utils / render |

Quarantine code is never imported. No GPL components in the wired path.

## 9. Proof artifacts (all under `tools/wave62_lane_c/proofs/`)

- `rebuilt_pipeline/rebuilt_pipeline_result.json` — all variants, checks,
  eigengap spectra, GT-mean cosines, honest findings.
- `rebuilt_pipeline/hypothesis_{main_clean,upstream_clean,upstream_noisy,bypass_noisy}.rttm`
- `rebuilt_pipeline/fixture_noisy_white.wav` (seeded 10 dB variant),
  `out_upstream_{clean,noisy}_conditioned.wav` (denoised inputs, ablation only).
- `downstream/denoised_spk_{A,B,C}.wav`, `downstream_denoised_mix.wav`,
  `downstream_denoised_noisy_mix.wav`.
- `downstream/captions.srt`, `captions.ass`, `waves.mp4`,
  `burned_captions.mp4`, `caption_result.json`,
  `frame_{on,off,src_on,src_off}.raw` (pixel-verification frames).
- SHA-256 over every file above: `SHA256SUMS`.

Scripts: `wire_diarization_rebuilt.py` (stage 1: rebuilt topology +
ablation), `wire_downstream_caption.py` (stage 2: downstream denoise;
`--resume` reuses denoised wavs without loading DF),
`wire_step4_ecapa_diagnostic.py` (step-4 attempt — incomplete, see §7),
`wire_step5_caption_burnin.py` (torch-free caption burn-in).
`install.sh` / `run.sh` reproduce the environment and the run.
