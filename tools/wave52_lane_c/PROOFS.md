# Wave 52 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed audio tools wired with REAL runs, extending the Wave 51
pipeline one stage further: **text -> VO (Kokoro) -> lip-sync (Rhubarb) ->
denoise + loudness master (this lane)**. Both wire scripts are original
MIT-licensed code (this directory); external libs/binaries are invoked, never
embedded.

Environment: Python 3.12.3, numpy 1.26.4, scipy 1.11.4 (system),
noisereduce 3.0.3 + pyloudnorm + soundfile 0.14.0 (lane-local venv,
`tools/wave52_lane_c/venv/`, gitignored), ffmpeg 8.1.2 / ffprobe (Ubuntu
build). Lane-local pip used `TMPDIR=~/tmp/pip-tmp` (`/tmp` is a 512 MB
tmpfs). No network needed after install. Disk was at 96% — all artifacts are
small WAVs (~2.6 MB total), nothing near the 100 MB binary limit.

## 1. noisereduce — spectral-gating denoise (MIT)

- **Upstream:** timsainb/noisereduce — MIT verified 2026-10-08 via GitHub API
  (`spdx_id: MIT`), consistent with the catalog entry (Wave 22 Lane A,
  previously `not-started` -> now `WIRED — run-proven`).
- **License:** MIT (upstream). Wire script MIT.
- **Script:** `wire_audio_mastering.py` (stages 2a–2c) — profiles stationary
  noise from the input's own silence regions, denoises, and measures with
  segmental ground truth (silence-region floor + speech-region fidelity).
- **Proof (no network):** real input = Wave 51 Kokoro VO WAV
  (`tools/wave51_lane_c/proofs/kokoro_tts/voice_line.wav`: 7.825 s, 24 kHz
  mono, 187,800 frames, RMS 0.0511 — verified to match Wave 51's proof).
  - **Controlled noise test:** calibrated −40 dBFS white noise injected
    (seeded RNG, deterministic) -> denoised with the true noise reference:
    - silence-region noise floor: **0.01002 -> 0.00045 (−27.0 dB suppression)**
    - speech-region fidelity: corr(denoised, clean) = **0.9800**
    - honest caveat: musical-gate artifacts remain (speech-region error RMS
      0.0253 vs speech RMS 0.0771) — spectral gating is a blunt tool, best
      for hiss/hum on field recordings, not transparent restoration.
  - **Correct-usage test on the clean VO** (noise profile from the file's own
    0.78 s of silence): RMS 0.0511 -> 0.0506 (delta **−1.1%**),
    corr = **0.99979** — a safe near-no-op pass.
  - **NEGATIVE CONTROL (documented misuse):** stationary mode with NO noise
    profile removed **70.6%** of the clean VO's RMS — the gate treats program
    material as noise. **Production rule: never run blind; always supply a
    silence/room-tone profile.**
  - Metric honesty note: global "SNR vs pristine" was tried first and
    REJECTED — it penalizes the gate for doing its job (any benign bin
    change counts as error). Segmental metrics (floor suppression +
    speech correlation) are the recorded proof.
  - Determinism: repeat denoise -> byte-identical PCM16.
- **Artifacts:** `proofs/audio_mastering/vo_noisy_40db.wav`,
  `vo_denoised_noisy.wav`, `vo_denoised_clean.wav`, `result.json`.

## 2. pyloudnorm — ITU-R BS.1770 loudness mastering (MIT)

- **Upstream:** csteinmetz1/pyloudnorm — MIT verified 2026-10-08 via GitHub
  API (`spdx_id: MIT`). NEW catalog entry (appended this wave).
- **License:** MIT (upstream). Wire script MIT.
- **Script:** `wire_audio_mastering.py` (`master()`) — dual-pass:
  1. pyloudnorm loudness gain to target on the FINAL channel layout;
  2. true-peak safety to −1.0 dBTP via ffmpeg `alimiter` (external binary —
     the repo's already-wired FFmpeg; nothing linked). Linear attenuation was
     tried first and REJECTED: it cannot un-clip samples already flattened
     at the PCM16 rail — limiting must happen in float domain (FLOAT32
     intermediate) before PCM16 quantization.
- **Proof (no network):** chain of record = denoised clean VO.
  - **Podcast master** (`master_podcast_16lufs_stereo.wav`, dual-mono
    stereo): ebur128-measured **−17.0 LUFS** vs −16.0 target (within the
    ±1.0 tolerance for the peak-limited path — the limiter cost ~1 LU),
    true peak **−2.0 dBFS** (≤ −1.0 dBTP ceiling), 2 ch, 7.825 s, LRA 2.9.
  - **Broadcast master** (`master_broadcast_24lufs_mono.wav`, mono):
    **−23.9 LUFS** vs −24.0 target (±0.5, no limiting needed),
    true peak **−4.3 dBFS**, 1 ch, 7.825 s, LRA 3.0.
  - **Independent cross-check:** ffmpeg `ebur128` (second BS.1770
    implementation) agrees with pyloudnorm's meter to **0.12 LU**
    (−25.32 vs −25.20 LUFS pre-normalization).
  - Bugs caught during wire-up (both fixed, both documented as production
    rules in the script): (a) loudness gain computed on mono then upmixed
    to stereo measured **+3 LU hot** — BS.1770 sums dual-mono channels;
    gain MUST be computed on the final layout. (b) PCM16 clipping before
    peak limiting breaks the linear math — limit in float32 first.
  - Determinism: two identical dual-pass runs -> byte-identical SHA-256.
- **Artifacts:** `proofs/audio_mastering/master_podcast_16lufs_stereo.wav`
  (0.75 MB), `master_broadcast_24lufs_mono.wav` (0.38 MB), `result.json`.

## Checks

13/13 PASS (`result.json`): input matches Wave 51 VO ground truth ·
pyloudnorm/ebur128 agreement · clean-denoise safety · −27 dB floor
suppression · speech fidelity · podcast loudness/true-peak/layout ·
broadcast loudness/true-peak/layout · byte-determinism (master + denoise).

## Catalog updates

- `noisereduce`: `not-started` -> `WIRED — run-proven (Wave 52 Lane C)` +
  wiring proof note.
- `pyloudnorm`: NEW `####` entry appended (`## Wave 52 Lane C — wired tools`).
- Quarantine: untouched — no GPL code linked or imported anywhere in this
  lane (noisereduce/pyloudnorm/soundfile are MIT/BSD; ffmpeg used only as an
  external binary).

## Deferred / not attempted

- Caption/subtitle burn-in was already wired pixel-verified in Wave 50 Lane C
  (`tools/wave50_lane_c/wire_caption_burnin.py`) — not duplicated; this lane
  took the audio-mastering candidate from the mission brief instead.
- Non-stationary denoise mode was spot-checked (SNR got worse on the
  stationary-noise control, as expected) — not pursued; stationary is the
  documented path for hiss/hum.
