# Wave 61 Lane C — FULL voice pipeline END-TO-END on real multi-speaker audio

Branch: `wave61-lane-c` · Lane dir: `tools/wave61_lane_c/`
Environment: Linux x86_64, Python 3.12.3, lane venv (`venv/`, gitignored).
Wire scripts: `wire_full_pipeline.py`, `wire_caption_burnin.py`
(MIT, original). Re-run with `./run.sh` (note: `run.sh` runs the pipeline
script only; the caption script takes a variant arg — see "Rebuild recipe").

**Pipeline:** DeepFilterNet3 denoise (Wave 56) → webrtcvad-tuned VAD
refinement agg=0 + 0.2 s hangover (Wave 59 V2c) → window grid 1.5 s/0.25 s
hop, energy gate, drop windows straddling VAD boundaries, frame labeling
inside VAD speech only / no fill → ECAPA-TDNN 192-dim embeddings
(Wave 56, recomputed fresh on the denoised audio) → eigengap E1a
speaker-count estimator (Wave 60) → forced-k SpectralCluster →
Hungarian cluster→speaker map → DER/JER (pyannote-metrics, Wave 57) →
caption burn-in (ffmpeg ASS, Wave-50 method).

**Fixture:** Wave-58 9-turn 3-Kokoro-voice dialogue
(A=`af_heart` F, B=`am_puck` M, C=`af_bella` F; A/C both female on purpose),
42.9 s @16 kHz, byte-identical to the committed Wave-58 artifact (SHA-verified).
Run on **two** inputs: clean, and a seeded 10 dB-SNR white-noise variant
(the honest stress test — the denoiser must earn its place), plus a
`noisy_bypass` ablation (no denoiser) to isolate the denoiser's effect.

## License gate (all upstream, verified live 2026-10-08)

- DeepFilterNet / DeepFilterNet3 weights — **dual MIT/Apache-2.0**
  (wired Wave 56; weights from upstream GitHub release, cached
  `~/.cache/DeepFilterNet/DeepFilterNet3/`, `model_120.ckpt.best` 8.4 MB)
- SpeechBrain ECAPA-TDNN `speechbrain/spkrec-ecapa-voxceleb` —
  **Apache-2.0** (wired Wave 56; fresh download this run, cached in
  `scratch/speechbrain_models/`, gitignored)
- webrtcvad — **MIT** (wired Wave 42/59)
- SpectralCluster 0.2.22 — **Apache-2.0** (wired Wave 57)
- pyannote-metrics 4.1 — **MIT** (wired Wave 57; installed `--no-deps`)
- scikit-learn / scipy / numpy — **BSD** (system site-packages)
- ffmpeg 8.1.2 `ass` filter (libass) — invoked as external binary
  (caption burn-in, Wave-50 donor pattern)
- eigengap E1a estimator, VAD/pipeline/caption glue — **original lane
  code, MIT** (this lane)

## Environment notes / honest failures

- `deepfilternet` → `deepfilterlib==0.5.6` sdist needs Rust/Cargo (no
  wheel). Compiled with the toolchain rustup install
  (`~/workspace/toolchain/`, rustc 1.99.0); first attempt failed with
  "rustup could not choose a version of cargo" — fixed by `rustup default
  stable` (toolchain `stable-x86_64-unknown-linux-gnu` was present but
  un-defaulted).
- The compiled `libdf/*.so` silently failed to copy into site-packages on
  the first install (RECORD listed it, files absent) — force-reinstalled;
  second install placed it. Verified by import, not assumed.
- deepfilternet 0.5.6 predates torchaudio 2.9: same venv-local
  `torchaudio/backend/common.py` shim as the Wave-56 lane (restores the
  old `AudioMetaData` dataclass used only as a type annotation in
  `df.io`). Not repo content — venv is gitignored.
- `torch.nn.functional.resample` does not exist — resampling lives in
  `torchaudio.functional.resample` (script bug caught at runtime, fixed).
- First caption run crashed at the ffmpeg waveform render: `-filter_complex
  showwaves` needs explicit stream labels (`[0:a]showwaves…[v]` + `-map`);
  fixed. First burn had overflowing captions (WrapStyle: 2 = no wrap,
  34 pt on 640 px wide) — caught by reading the burned frame, fixed to
  WrapStyle: 0 + 26 pt. Both frames re-opened and visually verified after
  the fix.
- Disk 96% full at build time; venv uses `--system-site-packages` (system
  numpy 1.26.4 / scipy 1.11.4), pip ran `--no-cache-dir` with lane-local
  `TMPDIR=scratch/pip-tmp` and `CARGO_TARGET_DIR=scratch/cargo-target`.
- `no_proxy`/`NO_PROXY` IPv6 literals stripped (httpx crash lesson).
- `denoise_deterministic` reads back the wav-quantized file and compares
  to a fresh run: max|diff| = 5.24e-05 (wav int16 quantization, not model
  nondeterminism — Wave 56 measured exact 0.0 on model output).

Versions: torch 2.14.1+cpu · torchaudio 2.11.0+cpu · deepfilternet 0.5.6 ·
deepfilterlib 0.5.6 (Rust ext, compiled locally) · speechbrain 1.1.1 ·
webrtcvad 2.0.10 · spectralcluster 0.2.22 · pyannote-metrics 4.1 ·
pyannote.core 6.0.1 · scikit-learn 1.9.1 · numpy 1.26.4 (system) ·
scipy 1.11.4 (system) · soundfile 0.14.0.

## Results (collar 0.0; collar 0.25 in result JSON)

| Variant | denoise | k̂ (E1a, blind) | DER | JER | miss | FA | conf | purity |
|---|---|---|---|---|---|---|---|---|
| clean | DeepFilterNet | **3** (margin 2.7x) | **0.1285** | 0.1284 | 5.05 | 0.0 | 0.0 | 1.0000 |
| noisy (10 dB) | DeepFilterNet | **2** (margin 1.4x) | 0.4275 | 0.5635 | 6.05 | 0.0 | 10.75 | 0.6767 |
| noisy_bypass | none | **3** (margin 3.2x) | 0.2239 | 0.2623 | 6.30 | 0.25 | 2.25 | 0.9318 |

GT-mean embedding cosine (diagnostic, GT-informed — not part of the blind
pipeline):

| Variant | cos(A,B) | cos(A,C) | cos(B,C) |
|---|---|---|---|
| clean | 0.1535 | 0.6326 | 0.1537 |
| noisy+denoise | 0.3465 | **0.7438** | 0.2835 |
| noisy_bypass | 0.0816 | **0.5905** | 0.0785 |

Denoiser SNR on the noisy variant: **10.0 → 17.3 dB (Δ +7.3 dB)** —
the denoiser works. Clean no-op: RMS delta 2.49% (< 5%), corr 0.99934.

VAD (tuned agg=0 + 0.2 s pad) on the denoised audio: clean 9 segments
recall 0.9226 / prec 1.0000; noisy 10 segments recall 0.9201 / prec 0.9937
— the Wave-59 tuning transfers to denoised audio.

## The honest reading

1. **Clean-path end-to-end works: DER 0.1285 / JER 0.1284** (0.0762 @collar
   0.25), confusion 0.0 s, purity 1.0, all 3 speakers mapped, eigengap
   correctly selects k=3 blind. The residual 0.1285 is pure boundary miss
   (5.05 s) — frames near turn boundaries not covered by any kept window.
   This confirms the Wave-60 follow-up hypothesis (est-k + V2c boundaries
   under ~0.09–0.13 on real voices).
2. **The denoiser improves SNR (+7.3 dB) but HURTS diarization.**
   noisy+denoise DER 0.4275 vs noisy_bypass DER 0.2239 — the denoiser
   costs +0.20 DER. Mechanism (measured, GT-informed diagnostic):
   DeepFilterNet pushes all speaker means toward each other
   (cos A/C: 0.5905 bypass → 0.7438 denoised; cos A/B: 0.082 → 0.347),
   collapsing the eigengap margin 3.2x → 1.4x and flipping the blind
   count estimate 3 → 2, which merges the two female voices (confusion
   2.25 → 10.75 s). SNR improvement ≠ speaker-feature preservation.
   **Production consequence: do NOT put DeepFilterNet upstream of the
   embedding stage for multi-speaker work** — or gate it by a
   speaker-separability check. This is the wave's headline finding.
3. **The eigengap estimator is fragile to processing, not to noise.**
   Raw 10 dB-white-noisy embeddings: k=3 with 3.2x margin (bypass) —
   ECAPA is robust to white noise at 10 dB. Denoised embeddings: k=2.
   The estimator's failure mode is processing artifacts, matching the
   Wave-60 warning that the margin must be re-measured on harder inputs.
4. Eigengap margin shrinks with fewer windows even on clean audio
   (13x in Wave 60 with 160 windows → 2.7x here with 92 VAD-kept
   windows) — the V2c window-dropping that fixes boundaries starves the
   count estimator. Still selects k=3 correctly on clean.

## Caption burn-in

`wire_caption_burnin.py [noisy|clean]` — hypothesis RTTM (speaker + timing
from THIS pipeline) + Wave-58 GT turn texts (the WORDS; no ASR stage is
wired — documented). SRT + ASS (per-speaker colors) burned with ffmpeg
libass onto a showwaves waveform render of the denoised audio.

| Variant | caption checks | pixel ON | pixel OFF | caption content |
|---|---|---|---|---|
| noisy | 10/10 PASS | 9.87/255 | 0.00/255 | 9 events; A's turns labeled **[C]** — the burn-in faithfully shows the pipeline's real A/C-merge error |
| clean | 10/10 PASS | 11.73/255 | 0.00/255 | 9 events; A/B/C all correct |

Burned frames opened and read by the lane author (not just pixel metrics):
clean @2.3 s shows gold "[A] Alright, we're rolling…" correctly wrapped in
two lines; noisy @2.3 s shows the same turn in pink as [C] — the merge made
visible. `proofs/caption_burnin_{noisy,clean}/proof_frame_on.png`.

## Checks

| # | Check | Result | Measured |
|---|---|---|---|
| 1 | fixture SHAs match wave58 committed artifacts | PASS | dialogue.wav / ground_truth.json / reference.rttm |
| 2 | fixture duration / 3 voices / 9 turns | PASS | 42.90 s |
| 3 | noisy variant calibrated | PASS | input SNR 10.0 dB |
| 4 | denoise SNR gain on noisy input | PASS | 10.0 → 17.3 dB (Δ +7.3 dB) |
| 5 | denoise clean no-op: RMS delta < 5% | PASS | 2.49% |
| 6 | denoise clean no-op: corr > 0.99 | PASS | 0.99934 |
| 7 | denoise deterministic across runs | PASS | max\|diff\| = 5.24e-05 (wav-quant) |
| 8 | tuned VAD recall ≥ 0.90 on noisy+denoised | PASS | 0.9201 |
| 9 | tuned VAD precision ≥ 0.99 on noisy+denoise
...[truncated 3559 chars]