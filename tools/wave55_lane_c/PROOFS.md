# Wave 55 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed tools wired with REAL runs. Both extend the Wave
51–54 cartoon-voice pipeline one stage further:

**text -> VO (Kokoro, Wave 51) -> lip-sync (Rhubarb) -> denoise + loudness
master (Wave 52) -> SUBTITLES (faster-whisper, Wave 53) ->
FORMAT NORMALIZATION + SRT RETIME (Wave 54) ->
SAMPLE-RATE CONVERSION + DEGRADATION-STRESS (this lane)**.

Both wire scripts are original MIT-licensed code (this directory); external
libraries are pip-installed, never embedded. Nothing from
`tools/quarantine` is linked or imported anywhere in the wire paths.
Licenses re-verified upstream 2026-10-08 via GitHub API (`spdx_id`):
bmcfee/resampy = **ISC**, iver56/audiomentations = **MIT** — both
permissive, no GPL/LGPL/NC anywhere in the wire paths (librosa is ISC,
scipy/numpy/soundfile are BSD-3-Clause).

Environment: Python 3.12.3, lane-local venv (`tools/wave55_lane_c/venv/`,
gitignored), `TMPDIR=$HOME/.tmp-pip`. resampy 0.4.3 + audiomentations
0.43.1 (PyPI wheels, no model weights, no network). Real input: the
Wave-52 proof WAVs (real noisereduce + pyloudnorm outputs from the real
Kokoro VO take — 7.825 s, 24 kHz). Proof artifacts total ~2.9 MB —
nothing near the 100 MB binary limit.

## 1. resampy — sample-rate-conversion stage (ISC)

- **Upstream:** bmcfee/resampy — ISC re-verified 2026-10-08 via GitHub
  API; catalog entry flipped `not-started` -> `WIRED — run-proven` this wave.
- **Script:** `wire_resampy.py` — resamples the real denoised VO
  24 kHz -> 48 kHz (kaiser_best), measures tone SNR, round-trips, checks
  same-rate identity, resamples the stereo podcast master, checks
  determinism and filter-variant behavior.
- **Proof (real input, real sinc SRC):**
  - Source: 187800 frames, 24 kHz mono, 7.825000 s.
  - 1 kHz tone 24k->48k: **SNR 130.77 dB** vs ideal (lag-compensated) —
    real polyphase sinc resampling, not a copy.
  - Real VO 24k->48k: 187800 -> **375600 frames exactly**, duration
    7.825000 s preserved, finite output (min -0.358, max 0.517).
  - Same-rate 24k->24k: bit-identity (max diff 0.0).
  - Stereo podcast master 24k->48k: (187800,2) -> (375600,2), channels
    preserved — written as proof WAV.
  - Determinism: two full runs -> bit-identical float32.
  - kaiser_fast vs kaiser_best: outputs genuinely differ (both real ops).
  - 11/11 checks PASS.
- **HONEST FINDING — downsample roll-off (measured, not assumed):** the
  first draft asserted a transparent 24->48->24 round-trip and FAILED
  (full-band round-trip SNR only 24.23 dB, max abs err 7.54e-02). Tone
  sweep of the 48k->24k kaiser_best anti-alias filter: 10.0 kHz 0.00 dB,
  10.5 kHz -0.26 dB, 10.75 kHz -1.67 dB, 11.0 kHz -5.82 dB,
  11.5 kHz -29.46 dB => **-3 dB point ≈ 10,830 Hz** (well below the
  12 kHz output Nyquist). Content above ~10.8 kHz does not survive the
  downsample. Below the roll-off the stage IS transparent: 10 kHz
  lowpassed VO round-trips at **SNR 92.03 dB, max abs err 2.47e-05**.
  Pipeline consequence: upsample 24k->48k for video deliverables is safe;
  keep the 24 kHz master as the archive source of truth — never
  round-trip back. This is upstream filter design, not a wire defect.
- **Artifacts:** `proofs/resampy/vo_denoised_clean_48k.wav`,
  `proofs/resampy/master_podcast_16lufs_48k.wav`,
  `proofs/resampy/result.json`.

## 2. audiomentations — degradation-stress / take-variation stage (MIT)

- **Upstream:** iver56/audiomentations — MIT re-verified 2026-10-08 via
  GitHub API; catalog entry flipped `not-started` -> `WIRED — run-proven`
  this wave.
- **Script:** `wire_audiomentations.py` — applies seeded Gain,
  AddGaussianNoise, PitchShift, and a 4-stage degradation chain
  (noise + AirAbsorption + HighPassFilter + Gain) to the real denoised VO;
  measures exact gain, noise amplitude vs upstream implementation, pitch
  shift on a synthetic tone; checks seeded determinism; writes a degraded
  variant and a take-2 variation.
- **Proof (real input, real augmentations):**
  - Gain -6 dB: measured RMS ratio **0.501187** = 10^(-6/20) to 6
    decimals — exact dB gain.
  - Seeded Gaussian noise: bit-identical across reseeds; measured noise
    RMS 0.005002 vs parameter 0.005000 (implementation verified in
    installed source: `noise = amplitude * randn(...)`, Gaussian
    std = amplitude — the first draft wrongly assumed uniform noise and
    failed; corrected against the actual source).
  - Degraded SNR **20.09 dB** vs predicted-from-params 20.10 dB —
    matches within 0.01 dB.
  - PitchShift +2 semitones on 440 Hz tone: dominant freq **494.50 Hz**
    vs expected 493.88 Hz — real resampling pitch.
  - 4-stage degradation chain: 187800 frames preserved, finite,
    RMS 0.0506 -> 0.0341; proof WAV 375,644 bytes.
  - Take-2 variant (pitch -1.5 st, gain +1.5 dB): frames preserved,
    genuinely differs from source.
  - 10/10 checks PASS.
- **HONEST FINDING — dual RNG:** audiomentations draws from BOTH
  `np.random` AND Python's `random` module — HighPassFilter consumes
  `random` even with a fixed cutoff range (isolated by per-transform
  determinism test). Seeding only numpy leaves the chain
  non-deterministic (max diff 0.041 observed); seeding both gives
  bit-identical output. Future pipeline code must seed both.
- **Artifacts:** `proofs/audiomentations/vo_degraded_variant_seed1234.wav`,
  `proofs/audiomentations/vo_take2_variant.wav`,
  `proofs/audiomentations/result.json`.

## What the pipeline can now do end-to-end

The audio leg is now closed on both ends: ASR -> SRT (Wave 53) ->
normalization (Wave 54) for captions; and mastering (Wave 52) -> **48 kHz
video-deliverable SRC with a measured transparency guarantee below
10.8 kHz** (resampy) + **seeded degradation variants for stress-testing
the denoise chain and generating alternate VO takes** (audiomentations) —
all permissive-licensed, all run-proven on the same real VO take.
