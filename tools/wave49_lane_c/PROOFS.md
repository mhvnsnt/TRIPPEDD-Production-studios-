# Wave 49 Lane C — wire-up proofs (2026-10-08)

Two permissive-licensed audio-pipeline tools wired with REAL runs on synthetic
ground-truth audio (no network, no mic, no model weights at proof time).

Environment: Python 3.12.3 venv, pip-installed `webrtcvad-wheels` + `audiostretchy`
(+ numpy for measurement). ffmpeg/ffprobe  present on the VM (used only for the
environment re-check, not needed by these two tools).

## 1. webrtcvad — voice activity / silence detection
- **Upstream:** https://github.com/wiseman/py-webrtcvad (installed via `webrtcvad-wheels` fork for py3.12 wheels)
- **License:** MIT (Python wrapper) + BSD (WebRTC VAD core) — verified 2026-10-08
  from upstream LICENSE (raw.githubusercontent.com): wrapper is MIT, bundled
  WebRTC code under BSD. Both permissive; matches the catalog's 2026-10-07 read.
- **Script:** `wire_webrtcvad.py`
- **Proof:** synthetic 16 kHz mono WAV (5 s: silence 1 s / voiced 1.5 s / silence
  1 s / voiced 1.5 s, harmonic pseudo-vowels at 120/165 Hz with 4 Hz syllabic AM).
  WebRTC VAD, aggressiveness=2, 30 ms frames, canonical ring-buffer collector.
  - GT silence regions: 2.9% / 14.7% frames flagged speech (second silence has
    ring-buffer spill from the preceding voiced region — expected)
  - GT voiced regions: 96.1% / 100.0% frames flagged speech
  - Collector emitted exactly the 2 voiced segments (0.900–2.820 s, 3.420–4.980 s),
    aligned to ground truth within tolerance → **PASS**
- **Artifacts:** `proofs/input/vad_test.wav`, `proofs/vad/result.json`

## 2. audiostretchy — pitch-preserving time-stretch
- **Upstream:** https://github.com/twardoch/audiostretchy (TDHS C core by David Bryant)
- **License:** BSD-3-Clause — verified 2026-10-08 via GitHub API
  (`spdx_id: BSD-3-Clause`, LICENSE.txt fetched at commit on main). The C core is
  BSD-style; the catalog's "pedalboard Apache-2.0" note refers to the newer
  rewrite path, not the installed 1.3.5 TDHS build. Either way permissive.
- **Script:** `wire_audiostretchy.py`
- **Proof:**
  - *Pitch probe:* pure 440 Hz sine (2 s, 44.1 kHz mono) stretched ratio=1.5 →
    3.073 s (expect 3.000 s, within 5%), dominant FFT peak 440.0 Hz in every
    1 s window → **no chipmunking, PASS**
  - *Silence-mode probe:* tone 2.5 s + digital silence 0.5 s + tone 0.5 s:
    - full ratio=1.5 → audio extent 5.273 s (expect 5.25 s), gap 0.70 s (expect 0.75 s)
    - ratio=1.5 + gap_ratio=1.0 → audio extent 5.023 s (expect 5.00 s), gap 0.45 s (expect 0.50 s)
    → silence stretches independently of audio, **PASS**
- **Artifacts:** `proofs/input/sine440.wav`, `proofs/input/tone_gap_tone.wav`,
  `proofs/stretch/sine440_stretched_1.5x.wav`, `proofs/stretch/gap_full_1.5x.wav`,
  `proofs/stretch/gap_silence_separate.wav`, `proofs/stretch/result.json`

### Known quirk (honest documentation, not a failure)
In silence mode audiostretchy pre-allocates the output buffer to
`output_capacity(nframes, ratio)` and `save_wav` writes the whole buffer, so
silence-mode outputs are zero-padded with digital silence to the full-ratio
duration. The proof trims trailing digital silence before asserting extents;
downstream users should do the same (or `ffmpeg -af silenceremove`).

## Deferred (honest, not attempted to force)
- **Speaches Docker smoke test** — still deferred: no container runtime on the VM
  (no docker/podman/nerdctl/crictl, no /var/run/docker.sock), re-checked 2026-10-08.
- **VGMTrans build** — still deferred: no Qt dev libraries (no qtbase5-dev/qt6-base-dev,
  no qmake/qmake6), re-checked 2026-10-08. Compilers (cmake/g++/make) are present.
- **LGPL doctrine** — pending owner verdict; not decided here.
