# Wave 65 Lane C — PROOFS: production diarization port

Branch: `wave65-lane-c` · Lane dir: `tools/wave65_lane_c/`
Worktree: `/home/hatch/workspace/trippedd-studio-wt-w65c` (main checkout untouched)

## Goal

Port the Wave-64 proven diarization operating point (webrtcvad
aggressiveness 0 / 10 ms frames / 0.3 s hangover pad → DER 0.0382 /
JER 0.0378 on the multi-speaker fixture, −46% vs Wave-63) into a single
production-ready wiring script, run against REAL episode audio, and
report honestly.

## What was wired

`wire_diarize_production.py` (original MIT lane code), one script for
both modes, re-run with `./run.sh [--mode fixture|production]`:

  raw audio
   → webrtcvad VAD (agg=0, 10 ms, 0.3 s pad — the proven point)
   → window grid 1.5 s / 0.25 s + energy gate (0.08) + strict VAD inclusion
   → ECAPA-TDNN embeddings on RAW audio (SpeechBrain
      spkrec-ecapa-voxceleb, CPU, single-thread, batch 8;
      QUARANTINE: denoise (DeepFilterNet) NEVER sits upstream of the
      speaker path — Wave-61 production rule honored)
   → blind eigengap speaker-count selection
   → forced-k SpectralCluster (cosine)
   → Hungarian map (GT-informed; skipped without GT)
   → DER/JER (pyannote-metrics, only when a GT RTTM exists)
   → per-speaker hypothesis segments → SRT/ASS → ffmpeg ASS burn-in
     onto the RAW mix waveform render + pixel ON/OFF checks

Donor-first: VAD (`vad_segments_gen`), grid/eigengap/frame labeling/
RTTM/scoring come from the wave63 (`wire_vad_coverage_recovery`) and
wave64 (`wire_vad_recall_experiment`) lane modules — this file only
wires the production topology and adds the real-ECAPA compute stage
(single combined venv: torch 2.14.1+cpu + speechbrain 1.1.1 + the
torch-free lane deps, numpy 1.26.4 / scipy 1.11.4 to match the Wave-64
numerical stack; manifest at `venv-pins.txt` and
`~/workspace/agent-ops/venv-manifests/wave65-lane-c.txt`).

## Fixture run (reproduction gate): 15/15 PASS

`--mode fixture`: SHA-verified Wave-58 fixture (42.9 s @16 kHz, 9 turns,
3 Kokoro voices). Checks:

- VAD: recall 0.9728 / prec 0.9938 / F1 0.9832 (matches Wave-64 exactly)
- real ECAPA recompute on RAW audio: cos vs fixture `embeddings.pt` =
  1.000000 (min/mean/max) — the torch-free parse trick re-validated
- blind eigengap k=3 (margin 1.72x), purity 1.0, map {0:B, 1:C, 2:A}
- **F1 DER = 0.0382 (miss 1.275 / FA 0.225 / conf 0.0)** vs Wave-64
  baseline 0.0382 — exact reproduction, bit-for-bit
- **F1 JER = 0.0378** vs Wave-64 baseline 0.0378 — exact reproduction
- caption path: 9 events with GT turn text, ASS (per-speaker colors),
  ffmpeg burn-in onto the raw mix; pixel ON 11.77/255 (> 2.0), OFF
  0.00/255 (< 1.0); libass stderr clean; burn frame visually verified
  (`proofs/fixture/w65_fixture_frame_check.png`: gold `[A]` caption over
  waveform at t=2.25 s)

Artifacts: `proofs/fixture/` — `result.json` (all 15 checks),
`embeddings_raw.npy` (166×192, row p = window p),
`hypothesis_F0/F1.rttm`, `captions.srt`, `captions.ass`, `waves.mp4`,
`burned_captions.mp4`, `frame_on/off.raw`, `frame_src_on/off.raw`,
`w65_fixture_frame_check.png`.

## Production run (real episode audio): 10/10 PASS

`--mode production`: `production/WIZARD_GANG_EP01/audio-orig.m4a` —
the real EP01 original episode audio (300.16 s, AAC 44.1 kHz stereo,
read-only; decoded to 16 kHz mono). This is real episode audio, not a
fixture. Checks:

- VAD: 12 segments, 295.60 s speech (98.5% of 300.2 s) — the episode is
  nearly continuous narration
- grid: 1195 windows; real ECAPA embeddings on RAW audio (1195×192)
- **blind eigengap k=3, margin 1.02x** — HONEST WEAK RESULT: the gap
  spectrum is flat (gaps 0.0006–0.0046, k=3 barely above the rest), so
  this is a low-confidence speaker count, not a "3-speaker finding".
  With one dominant continuous voice in the episode, the eigengap has
  no decisive structure — recorded, not hidden.
- **No ground truth exists for the episode audio**, so cluster labels
  stay anonymous (`SPEAKER_00/01/02`) and Hungarian map / purity /
  DER / JER are NOT measurable — honestly reported as N/A, not faked.
- hypothesis RTTM: 101 F1 segments (`proofs/production/hypothesis_F1.rttm`)
- caption path: 101 events (speaker labels + timestamps — pipeline
  supplies who/when, no ASR; caption text is honest about that),
  per-speaker colors, ASS; burn-in onto the raw-mix waveform;
  pixel ON 3.85/255 (> 2.0), OFF 0.00/255 (< 1.0); libass stderr clean;
  burn frame visually verified
  (`proofs/production/w65_prod_frame_check.png`: cyan `[SPEAKER_01]`
  caption over waveform at t=5.625 s)

Artifacts: `proofs/production/` — `result.json` (all 10 checks),
`embeddings_raw.npy` (1195×192), `hypothesis_F0/F1.rttm`,
`captions.srt`, `captions.ass`, `waves.mp4`, `burned_captions.mp4`,
`frame_on/off.raw`, `frame_src_on/off.raw`,
`w65_prod_frame_check.png`.

DER/JER vs the Wave-64 fixture baseline: **0.0382 / 0.0378 reproduced
exactly on the fixture** (Δ = 0.0000). On real episode audio DER/JER
cannot be computed without a GT annotation — the production run is
evidence that the pipeline runs blind end-to-end on real audio, with
the weak eigengap margin flagged rather than rounded up.

## License audit (wired path — no new third-party tool wired)

| component | license | role |
|---|---|---|
| webrtcvad 2.0.10 | MIT | VAD (WIRED since Wave 49) |
| SpectralCluster 0.2.22 | Apache-2.0 | forced-k clustering (WIRED since Wave 57) |
| pyannote-metrics 4.1 (+ pyannote-core) | MIT | DER/JER scoring (WIRED since Wave 57) |
| SpeechBrain 1.1.1 spkrec-ecapa-voxceleb | Apache-2.0 | ECAPA embeddings (WIRED since Wave 56/58) |
| scikit-learn, numpy, scipy, ffmpeg/libass | BSD / LGPL sys tool | utils / captions |

No catalog status flips: every upstream reused here was already
`WIRED — run-proven`. The combined venv + weight-fetch + production
wiring is original MIT lane code. Quarantine code is never imported.
No GPL components. `production/` was read, never written.

## Honest failures / deferred items

1. **Truncated weight download**: first run's `embedding_model.ckpt`
   landed at 81.16 MB of 83.32 MB (proxy cut the stream; urllib saw
   silent EOF) and SpeechBrain crashed on the corrupt zip. Fixed by
   `X-Linked-Size`/`Content-Length` verification + up to 4 retries
   before promote — recorded in the script, not hidden. (Improvement
   over the Wave-64 fetcher, which would have silently kept a
   truncated file.)
2. **numpy 2.x conflict**: pip's resolver installed numpy 2.5.3, which
   broke the system matplotlib that pyannote.core imports at module
   load (noisy ImportError traceback; scoring still worked). Fixed by
   pinning the Wave-64 numerical stack (numpy 1.26.4 / scipy 1.11.4 /
   pandas 2.1.4) in `install.sh`; clean imports verified. The
   pyannote-metrics 4.1 metadata conflicts (wants pandas>=2.2.3,
   scipy>=1.15.1) are advisory-only — Wave-64 ran the same combo via
   system-site-packages.
3. **Weak eigengap on real episode audio** (margin 1.02x): honest blind
   outcome on 98.5%-continuous single-dominant-voice audio, reported
   as low-confidence, not rounded into a claim.
4. **Downstream denoise not run**: `deepfilternet` still has no cp312
   manylinux wheel and this VM has no Rust toolchain (same Wave-64
   blocker); the DF3 checkpoint bytes remain in `~/.cache/DeepFilterNet`
   from Wave-62. Burn-in goes onto the raw mix; the speaker path never
   sees denoised audio either way — the Wave-61 quarantine holds
   trivially. Denoise stays a downstream-caption-path-only stage.
5. `hyperparams.yaml` is re-downloaded on every run because the local
   patched copy (1973 bytes) fails the pristine size check (1919) —
   harmless (re-patched deterministically), noted as an inefficiency.
6. GT-informed Hungarian map needs a GT RTTM; the production run is
   blind by design — labels stay anonymous until a human annotates the
   episode.

## Environment / rebuild recipe

```bash
./install.sh   # single combined venv: torch 2.14.1+cpu, torchaudio,
               # speechbrain 1.1.1, webrtcvad 2.0.10, spectralcluster
               # 0.2.22, scikit-learn 1.9.1, pyannote.metrics 4.1
               # (+ numpy 1.26.4 / scipy 1.11.4 / pandas 2.1.4 pins)
./run.sh --mode fixture      # 15/15: baseline reproduction
./run.sh --mode production   # 10/10: real EP01 audio, blind run
```

Timings (CPU): fixture ~37 s (embeddings cached) / ~530 s (with
ECAPA recompute + weight fetch); production ~835 s (1195-window ECAPA
recompute dominates, single-thread batch 8 — no OOM).

## Proof artifacts (all under `tools/wave65_lane_c/proofs/`)

See `SHA256SUMS` (covers proofs + wire script + install/run.sh +
venv-pins.txt). Fixture and production subdirs listed above.
