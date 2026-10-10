# Wave44 Lane C — PROOFS

Lane C wired two permissive-licensed tools with real, rerun-able proofs.
All outputs below are from actual command runs on 2026-10-08; artifacts live
in `proofs/` with SHA-256 in `SHA256SUMS`. Nothing is faked or hand-written.

## Environment

- VM: linux x86_64, cmake + gcc, espeak-ng, ffmpeg present
- whisper.cpp: shallow clone of https://github.com/ggerganov/whisper.cpp (commit at 2026-10-08), built with `cmake -DCMAKE_BUILD_TYPE=Release`, target `whisper-cli`
- License check: upstream `LICENSE` begins "MIT License / Copyright (c) 2023-2026 The ggml authors"
- Python deps in an isolated venv: webrtcvad 2.0.10 (MIT), librosa (ISC),
  scikit-learn 1.9.1 (BSD-3), soundfile (BSD-3). Note: installed `webrtcvad.py`
  was one-line patched for setuptools>=81 (`pkg_resources` removed upstream;
  version pinned inline as `2.0.10`). Patch is documented here, not hidden.
- Model (runtime download, NOT in git): `ggml-tiny.en.bin`
  URL: https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
  SHA-256: `921e4cf8686fdd993dcd081a5da5b6c365bfde1162e72b08d75ac75289920b1f`

## Proof 1 — whisper.cpp ASR

Audio generated with espeak-ng (GPL-3 tool, used only as a test-signal
generator — not wired, not a dependency), resampled to 16 kHz mono:

```bash
espeak-ng -v en -s 150 -w asr_raw.wav "The quick brown fox jumps over the lazy dog. Open source software makes speech recognition accessible to everyone."
ffmpeg -y -i asr_raw.wav -ar 16000 -ac 1 asr_16k.wav
whisper-cli -m ggml-tiny.en.bin -f asr_16k.wav -otxt -of proofs/proof_asr
```

Actual output (`proofs/proof_asr.txt`, timestamped line in file):

```
The quick round fox jump over the lazy log. Open source software make speech recognition accessible to everyone.
```

Intended text: "The quick brown fox jumps over the lazy dog. Open source
software makes speech recognition accessible to everyone."

The tiny model makes small errors ("round"/"log"/"make") — honest tiny-model
behavior, shown as-is, not corrected. Timings log: `proofs/proof_asr.timings.log`
(total ~2.1 s for 7.95 s of audio).

## Proof 2 — permissive diarization

Two-voice sample: same espeak-ng voice at pitch 30 (Speaker A) and pitch 90
(Speaker B), four alternating turns with 0.6 s silence gaps, 16 kHz mono:

```bash
python3 diarize_vad_cluster.py diar_16k.wav 2
```

Actual output (`proofs/diar_speaker_turns.txt`):

```
file: diar_16k.wav
voiced segments: 5, speakers requested: 2
   start      end    dur  speaker
    0.00     4.44   4.44  SPEAKER_00
    5.31     9.09   3.78  SPEAKER_01
    9.96    10.41   0.45  SPEAKER_00
   10.71    13.29   2.58  SPEAKER_00
   14.19    17.79   3.60  SPEAKER_01
```

Ground truth vs result:

| Turn | Audio span | True speaker | Diar output |
|---|---|---|---|
| A1 "Hello, welcome to the meeting…" | 0.00–4.72 | A | SPEAKER_00 ✓ |
| B1 "Thanks Alice…" | 5.32–9.37 | B | SPEAKER_01 ✓ |
| A2 "Great. Let us move on…" | 9.97–13.58 | A | SPEAKER_00 ✓ (two VAD segments, same label) |
| B2 "The timeline is on track…" | 14.18–18.05 | B | SPEAKER_01 ✓ |

All four turns assigned to the correct cluster (4/4). VAD correctly splits at
the silence gaps; the mid-turn split of A2 (9.96–10.41 / 10.71–13.29) keeps the
same speaker label.

### Diarization iterations (honest record)

1. First run: MFCC mean/std + delta only → all turns collapsed into one cluster.
   Measured per-segment F0 medians: A-turns ~85 Hz, B-turns ~155–160 Hz —
   pitch, not spectral envelope, separates these two voices.
2. Added log-F0 mean/std/median (librosa.pyin) but kept equal-per-dim scaling →
   still collapsed (60 MFCC dims vs 3 F0 dims).
3. Weighting F0 dims *before* StandardScaler → no effect (scaling undoes it).
4. Weighting F0 dims ×8 *after* scaling → correct [0 1 0 0 1]. Shipped with the
   rationale documented in the code.

## pyannote.audio — deferred, not wired

pyannote.audio's code is MIT, but its segmentation and speaker-embedding
checkpoints require accepting gated HuggingFace community terms. Lane policy:
permissive licenses only, no gated artifacts. The VAD+MFCC+F0+clustering stack
above is the permissive replacement.

## Failures / environment notes

- `/tmp` (512 MB tmpfs) was full of other lanes' scratch → all work relocated to
  the lane worktree `.scratch/` (untracked); pip needed `TMPDIR` pointed there.
- webrtcvad 2.0.10 needs `pkg_resources`, removed in setuptools>=81 → one-line
  patch to the installed module (version pinned inline). Recorded here.
