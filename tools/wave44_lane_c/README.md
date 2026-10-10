# Wave44 Lane C — Tool Wiring: whisper.cpp + permissive diarization

Two permissive-licensed tools wired with real smoke-test proofs.

## 1. whisper.cpp (MIT) — ASR

- Upstream: https://github.com/ggerganov/whisper.cpp
- License: MIT (verified in upstream `LICENSE`, "Copyright (c) 2023-2026 The ggml authors")
- Wire: `scripts/build_whisper_cpp.sh` clones (shallow) and builds `whisper-cli`
  (binary lands in `vendor/whisper.cpp/build/bin/`, git-ignored, never committed).
- Transcribe: `scripts/transcribe.sh <model.ggml> <audio_16k.wav> [out-prefix]`
- Proof: `proofs/proof_asr.txt` — real run against an espeak-ng generated sample,
  transcript reproduced verbatim in `PROOFS.md`.

Model weights are NOT in git. Runtime download used for the proof:

- URL: https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
- SHA-256: `921e4cf8686fdd993dcd081a5da5b6c365bfde1162e72b08d75ac75289920b1f`

## 2. Permissive speaker diarization

`diarize_vad_cluster.py` — no gated models, no embedding checkpoints:

| Stage | Component | License |
|---|---|---|
| VAD (30 ms frames) | webrtcvad 2.0.10 | MIT (self-declared in module header) |
| Features (MFCC mean/std + delta mean + log-F0 stats per segment) | librosa | ISC |
| Clustering (agglomerative, n=2) | scikit-learn | BSD-3 |
| WAV I/O | soundfile | BSD-3 |

- Run: `scripts/run_diarization.sh <audio_16k.wav> [n_speakers]`
  (`W44_VENV` may point at a venv with the deps; else system `python3`.)
- Proof: `proofs/diar_speaker_turns.{txt,csv}` — 4 alternating two-voice turns
  correctly split into SPEAKER_00 / SPEAKER_01 (5 VAD segments, 2 speakers).

Design note: pitch (log-F0) is weighted post-scaling because the 60-dim MFCC
block otherwise buries the 3-dim F0 block; F0 is the dominant cue separating
the two synthetic voices (~85 Hz vs ~155 Hz median). Documented, not hidden —
see `PROOFS.md` §Diarization iterations.

## Deferred (honest, not wired)

- **pyannote.audio** — code is MIT, but the segmentation/embedding checkpoints
  require accepting gated HuggingFace community terms. Lane policy is
  permissive-only with no gated artifacts, so it is deferred, not wired.
- **espeak-ng** (GPL-3) — used only to *generate* the test audio samples;
  not wired, not a dependency of either tool.

## Regenerating the proof audio

```bash
# single-speaker ASR sample
espeak-ng -v en -s 150 -w asr_raw.wav "The quick brown fox jumps over the lazy dog. Open source software makes speech recognition accessible to everyone."
ffmpeg -y -i asr_raw.wav -ar 16000 -ac 1 asr_16k.wav
# two-speaker sample: alternate pitch 30 (A) / 90 (B) turns with 0.6s gaps
espeak-ng -v en -s 150 -p 30 -w turnA1.wav "Hello, welcome to the meeting. I will start with the first report."
espeak-ng -v en -s 150 -p 90 -w turnB1.wav "Thanks Alice. The budget numbers look good this quarter."
espeak-ng -v en -s 150 -p 30 -w turnA2.wav "Great. Let us move on to the project timeline."
espeak-ng -v en -s 150 -p 90 -w turnB2.wav "The timeline is on track. We should finish by Friday."
# resample each to 16kHz mono, generate 0.6s silence gap.wav, concat via concat demuxer
```
