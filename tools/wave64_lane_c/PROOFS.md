# Wave 64 Lane C — PROOFS: VAD-recall experiment

Branch: `wave64-lane-c` · Lane dir: `tools/wave64_lane_c/`
Environment: Linux x86_64, Python 3.12.3, lane venv (`venv/`, gitignored,
`--system-site-packages`, system numpy 1.26.4 / scipy 1.11.4).
Wire script: `wire_vad_recall_experiment.py` (original lane code, MIT).
Re-run with `./run.sh`. Torch-free: Wave-58 `embeddings.pt` is parsed raw
float32 from the torch zip container (Waves 59/60 trick), SHA-verified.

## Question

Wave-63 closed the labeling side: fill-within-VAD-speech (F1) reached DER
**0.0712** / JER 0.0700 (miss 2.67 / FA 0.12 / conf 0.0) on the Wave-58
fixture (42.9 s @16 kHz, 9 turns, 3 Kokoro voices — A=af_heart F,
B=am_puck M, C=af_bella F; A/C both female on purpose). The residual
2.67 s miss equals the VAD's own recall ceiling (webrtcvad
aggressiveness 0, 10 ms frames, 0.2 s hangover pad: recall 0.9351 ×
39.3 s GT speech ≈ 2.55 s). No labeling policy can recover speech the
VAD never marked. Can tuning the VAD itself recover the miss without FA
exploding?

## Answer: yes — 0.3 s hangover pad, DER 0.0382 (min-DER 0.0344 at pad 0.35)

The single dominant lever is the **hangover pad** (edge extension of raw
webrtcvad speech runs). Aggressiveness, frame size, explicit
trigger/hangover logic, energy-gate tightening, and the window-inclusion
criterion are all second-order or inert on this fixture.

### Phase A — VAD-quality grid (96 configs: agg 0–3 × 10/20/30 ms × pad 0–0.5 s)

Pad curve (agg=0, 10 ms frames; frame-level vs GT):

| pad (s) | recall | precision | F1 | n_seg |
|---|---|---|---|---|
| 0.00 | 0.8249 | 1.0000 | 0.9041 | 15 |
| 0.10 | 0.8891 | 1.0000 | 0.9413 | 10 |
| 0.20 (Wave-63) | 0.9351 | 1.0000 | 0.9665 | 9 |
| 0.25 | 0.9557 | 0.9979 | 0.9763 | 9 |
| **0.30** | **0.9728** | **0.9938** | **0.9832** | 9 |
| 0.35 | 0.9850 | 0.9840 | 0.9845 | 9 |
| 0.40 | 0.9931 | 0.9716 | 0.9823 | 9 |
| 0.50 | 1.0000 | 0.9427 | 0.9705 | 6 ← segments merge across gaps |

- Aggressiveness (10 ms, pad 0.3): agg 0/1 identical (rec 0.9728, F1
  0.9832 — the pad absorbs their decision differences); agg 2/3 HURT
  (rec 0.9499/0.9410 — aggressive modes chop low-energy onsets/offsets).
  Without pad, agg 2/3 collapse to rec 0.755–0.793.
- Frame size (agg 0, pad 0.3): 10 ms best (F1 0.9832); 20/30 ms slightly
  worse (0.9762/0.9783).
- Wave-63 baseline (agg 0, 10 ms, pad 0.2) ranks 13th of 96 by VAD F1.

### Phase B — explicit trigger/hangover (t_on × t_off × merge-gap, no pad)

Best: t_on=1, any t_off (3–20), merge-gap 0.25/0.4 → recall **0.8435**,
precision 1.0, F1 0.9151. Barely above the unpadded raw VAD (0.8249):
internal-silence bridging does NOT extend segment edges, and the recall
lives at the edges (low-energy onsets/offsets webrtcvad misses). Full
pipeline DER on the best Phase-B config: **0.1730** (miss 6.8) — the
pad-merge mechanism strictly dominates explicit hangover here.

### Phase C — full pipeline on top-6 Phase-A + top-4 Phase-B + baseline

(Windows → 0.08 energy gate → VAD-kept windows → fixture ECAPA
embeddings → blind eigengap → forced-k SpectralCluster → GT-informed
Hungarian map → F0 no-fill + F1 fill-within-VAD → pyannote-metrics.)

| VAD config | kept | k (margin) | F1 DER | miss | FA | conf | DER c0.25 |
|---|---|---|---|---|---|---|---|
| **pad 0.35 (min-DER)** | 103 | 3 (1.74x) | **0.0344** | 0.325 | 1.025 | 0.0 | 0.0054 |
| **pad 0.30 (RECOMMENDED)** | 102 | 3 (1.72x) | **0.0382** | 1.275 | **0.225** | 0.0 | 0.0081 |
| pad 0.40 | 106 | 3 (2.68x) | 0.0433 | 0.250 | 1.450 | 0.0 | 0.0108 |
| pad 0.20 = Wave-63 baseline | 94 | 3 (2.11x) | 0.0712 | 2.675 | 0.125 | 0.0 | 0.0283 |
| hangover t_off=3/5 (no pad) | 81 | 3 (2.87x) | 0.1730 | 6.800 | 0.000 | 0.0 | 0.1228 |

(agg 1 rows duplicate agg 0 rows bit-for-bit after the 0.3+ s pad-merge;
F0 no-fill DER also improves 0.1158 → 0.0712 at pad 0.3 from the extra
kept windows. Purity 1.0 and blind k=3 hold for every config.)

Reading:
1. **The pad is the whole game.** 0.2 → 0.3 s recovers 1.4 s of miss
   (2.675 → 1.275) for +0.1 s FA; DER 0.0712 → 0.0382 (−46%).
2. **0.35 is the DER minimum (0.0344) but FA jumps 4.5×** (0.225 →
   1.025): the pad starts eating the true 0.4 s inter-turn gaps. At
   0.4+ the trade reverses (DER worsens); at 0.5, segments merge across
   gaps (9 → 6 segments).
3. **Recommended production operating point: pad 0.3** — min DER
   subject to FA ≤ 0.5 s (the knee: 90% of the DER gain at 22% of the
   FA cost of pad 0.35).
4. The raw VAD misses ≈0.3–0.4 s per turn edge (low-energy
   onset/offset); the optimal pad ≈ the VAD's edge-miss depth — a
   portable tuning principle, not a fixture constant.

### Phase D — energy-gate × window-inclusion on the recommended config

Gate 0.08/0.10/0.12/0.16 × inclusion strict/center/≥50%-overlap: **all 12
cells DER 0.0382, miss 1.275, FA 0.225, conf 0.0.** The F1
fill-within-VAD labeling makes the pipeline invariant to the
window-inclusion rule (kept windows vary 102→160, labels don't — the
fill propagates the same anchors within the same VAD segments). Gate
*loosening* (< 0.08) is untestable torch-free: the 6 sub-gate windows
have no rows in `embeddings.pt` — deferred to the task-2 torch venv,
which recomputes ECAPA embeddings for all 166 grid windows.

## Checks: 11/11 PASS

fixture SHAs · generalized VAD bit-identical to Wave-63 at baseline
settings (recall 0.9351, prec 1.0, 9 segments) · baseline pipeline
reproduces Wave-63 exactly (F1 DER 0.0712, F0 DER 0.1158) · min-DER
k=3, purity 1.0 · min-DER beats Wave-63 (0.0344 < 0.0712) ·
recommended beats Wave-63 (0.0382 < 0.0712, FA 0.225 ≤ 0.5) ·
recommended k=3, purity 1.0 · Phase-D best == recommended ·
winner RTTMs written.

Timings: 47.7 s total on CPU (96-config VAD grid + 11 full pipeline
runs + scoring; no torch anywhere).

## Environment / rebuild recipe

```bash
python3 -m venv --system-site-packages venv
./install.sh   # webrtcvad, spectralcluster, scikit-learn,
               # pyannote.metrics==4.1 + pyannote.core + sortedcontainers
./run.sh
```

Installed: webrtcvad==2.0.10, spectralcluster==0.2.22,
scikit-learn==1.9.1, pyannote.metrics==4.1, pyannote.core==6.0.1,
sortedcontainers==2.4.0; system numpy 1.26.4 / scipy 1.11.4. Full pin
list: `venv-pins.txt` (also appended to
`~/workspace/agent-ops/venv-manifests/wave64-lane-c.txt`).

## License audit (wired path only — no new third-party tool wired)

| component | license | role |
|---|---|---|
| webrtcvad 2.0.10 | MIT | VAD (already WIRED — run-proven, Wave 49) |
| SpectralCluster 0.2.22 | Apache-2.0 | forced-k clustering (already WIRED, Wave 57) |
| pyannote-metrics 4.1 (+ pyannote-core) | MIT | DER/JER scoring (already WIRED, Wave 57) |
| Wave-58 `embeddings.pt` (SpeechBrain ECAPA) | Apache-2.0 | fixture embeddings (already WIRED, Wave 56/58) |
| scikit-learn, numpy, scipy | BSD | utils |

No catalog status flips: every upstream reused here was already
`WIRED — run-proven`. The generalized VAD + sweep harness is original
MIT lane code. Quarantine code is never imported. No GPL components.

## Proof artifacts (all under `tools/wave64_lane_c/proofs/vad_recall/`)

- `vad_recall_result.json` — all 96 Phase-A configs, 36 Phase-B configs,
  11 Phase-C pipeline runs, 12 Phase-D cells, checks, winner configs.
- `hypothesis_recommended_F0/F1.rttm` — production operating point
  (agg 0, 10 ms, pad 0.3, gate 0.08, strict inclusion).
- `hypothesis_minder_F0/F1.rttm` — min-DER config (pad 0.35).
- SHA-256 over every file above: `SHA256SUMS`.

## Honest failures / deferred items

1. Gate loosening (< 0.08) crashed the first full run (`IndexError`:
   sub-gate windows have no embedding rows in `embeddings.pt`). Fixed
   by restricting Phase D to tightening-only; loosening moves to the
   task-2 torch venv with real ECAPA recompute on all 166 windows.
2. Phase B (explicit hangover) underperforms badly (DER 0.1730) — not a
   bug: without edge padding, VAD recall caps at 0.8435. Recorded, not
   hidden.
3. The min-DER pad=0.35 config is reported but NOT recommended: FA
   1.025 s is 4.5× the recommended config's for a −10% DER gain.

---

# Task 2 — FULL end-to-end pipeline (raw → VAD → ECAPA-TDNN → eigengap → forced-k → Hungarian → DER/JER → ASS caption burn-in)

Status: COMPLETE, 14/14 + 5/5 checks PASS.

Wire scripts: `wire_e2e_step1_ecapa.py` (torch venv `venv_torch/`,
gitignored: torch==2.14.1+cpu, torchaudio==2.11.0+cpu,
speechbrain==1.1.1) and `wire_e2e_step2_pipeline.py` (torch-free lane
venv). VAD = the task-1 recommended config (agg 0, 10 ms, 0.3 s pad).

## Step 1 — real ECAPA-TDNN recompute (5/5 PASS)

Recomputed 192-dim SpeechBrain ECAPA embeddings for ALL 166 grid
windows on RAW fixture audio (single-thread, batch 8 — no OOM).
Weights = upstream `speechbrain/spkrec-ecapa-voxceleb` bytes fetched via
direct HTTPS into `scratch/ecapa_weights/` (huggingface_hub xet stalls
on this VM's proxy); `hyperparams.yaml` patched to fully-local
`pretrained_path` so the Pretrainer never touches the hub
(`HF_HUB_OFFLINE=1`). Two bugs caught and fixed: the pretrainer wanted
4 files (classifier.ckpt + label_encoder.txt were missing from the
fetch list) and `encode_batch()` takes no `normalize_wav` kwarg in
speechbrain 1.1.1.

- **cosine(recomputed, fixture embeddings.pt) = 1.000000 (min/max/mean)**
  — the real compute reproduces the Wave-58 fixture embeddings
  bit-for-bit in angle. The torch-free parse trick used in task 1 (and
  Waves 59/60/63) is validated end-to-end.
- GT-mean cosines on the recompute: A/B 0.1524, A/C 0.6259, B/C 0.1416
  — byte-matching Wave-63 step-4's raw-audio control row.

## Step 2 — pipeline + gate-loosening + caption burn-in (14/14 PASS)

| energy gate | energy-speech windows | kept (strict VAD) | k | F1 DER | miss | FA | conf |
|---|---|---|---|---|---|---|---|
| 0.02 (loosened) | 164 | 102 | 3 | **0.0382** | 1.275 | 0.225 | 0.0 |
| 0.04 (loosened) | 163 | 102 | 3 | **0.0382** | 1.275 | 0.225 | 0.0 |
| 0.08 (Wave-58) | 160 | 102 | 3 | **0.0382** | 1.275 | 0.225 | 0.0 |

Gate loosening is an honest negative: the extra 3–4 sub-gate windows
are all inter-turn-gap windows that the strict VAD-inclusion drops, so
kept stays 102 and DER is unchanged. The VAD — not the energy gate — is
the binding coverage constraint (consistent with Phase D's invariance).

- End-to-end hypothesis RTTM is **byte-identical** to the task-1
  torch-free recommended RTTM (diff-verified) — real ECAPA in the loop
  changes nothing, as the cosine-1.0 check predicted.
- DER 0.0382 / JER 0.0378 (collar 0.0); 0.0081 / 0.0077 at collar 0.25.
  Blind eigengap k=3 (margin 1.72x), purity 1.0, map {0:B, 1:C, 2:A}.
- Caption path: `captions_e2e.srt` + `captions_e2e.ass` (per-speaker
  colors, GT turn text — pipeline supplies who/when, no ASR), ffmpeg
  burn-in onto the **RAW mix** → `burned_captions_e2e.mp4` (1.7 MB).
  Pixel gates: caption-ON band diff 11.77/255 (> 2.0), caption-OFF
  0.00/255 (< 1.0); libass stderr clean; caption frame visually
  verified (cyan [B] caption over waveform at t=5 s).

## Quarantine accounting (downstream denoise)

Denoise NEVER touches the speaker path in either task: embeddings are
computed on raw audio (step-1 cosine-1.0 proof). The downstream
DeepFilterNet3 caption-path stage was NOT run in this lane:
`deepfilternet` ships a pure-Python wheel but its `DeepFilterLib`
dependency has no cp312 manylinux wheel and this VM has no Rust
toolchain to build it (Wave-62's lane-local Rust toolchain was cleaned
up); the DF3 checkpoint bytes remain cached in
`~/.cache/DeepFilterNet/` from Wave-62. The burn-in therefore goes onto
the raw mix, and the quarantine holds trivially — recorded here, not
hidden. Re-running the downstream denoise only needs a cp311 (or Rust)
environment; the hypothesis RTTM it would consume is committed above.

## Task-2 proof artifacts (under `tools/wave64_lane_c/proofs/end_to_end/`)

- `embeddings_all166.npy` — real-compute ECAPA embeddings, all 166
  windows (SHA in `SHA256SUMS`).
- `ecapa_recompute_result.json` — step-1 checks + cosine validation.
- `end_to_end_result.json` — gate sweep, DER/JER, pixel checks.
- `hypothesis_e2e_F1.rttm` — final hypothesis (byte-identical to the
  task-1 recommended RTTM).
- `captions_e2e.srt` / `captions_e2e.ass` / `waves_e2e.mp4` /
  `burned_captions_e2e.mp4` (+ frame_on/off.raw pixel evidence).
