# Wave 45 Lane C — PROOFS

Lane C wired 2 permissive ASR tools with REAL runs on a REAL fixture audio file.
Nothing here is simulated: every command below was executed and its output is
recorded in `proofs/`. All runs on the lane worktree
`~/workspace/agent-ops/wave45-lanes/c`, branch `wave45-lane-c`.

## 1. License verification (upstream, 2026-10-08)

Checked BEFORE any install, via PyPI JSON API and GitHub license API:

- **sherpa-onnx** → `Apache-2.0`
  - `curl https://pypi.org/pypi/sherpa-onnx/json` → `info.license: "Apache licensed, as found in the LICENSE file"`
  - `curl https://api.github.com/repos/k2-fsa/sherpa-onnx/license` → `spdx_id: Apache-2.0`
- **WhisperX** → `BSD-2-Clause`
  - PyPI `info.license: "BSD-2-Clause"`; GitHub license API `spdx_id: BSD-2-Clause`
- **faster-whisper** → `MIT`
  - PyPI `info.license: "MIT"`; GitHub license API `spdx_id: MIT` (also `ctranslate2: MIT`)

All three clear the permissive gate (MIT/Apache-2.0/BSD). No GPL/AGPL code was
linked or imported.

## 2. Fixture (real audio)

```
espeak-ng -v en -s 150 -w fixtures/fixture.wav \
  "The quick brown fox jumps over the lazy dog. This is a test of the speech recognition pipeline. Speaker one says hello."
ffmpeg -y -i fixtures/fixture.wav -ar 16000 fixtures/fixture_16k.wav
```

`fixture.wav`: 371,878 bytes, mono, 22050 Hz, 8.43 s of real synthesized speech.
`fixture_16k.wav`: same audio at 16 kHz (for faster-whisper).

## 3. sherpa-onnx (Apache-2.0) — WIRED ✅

Install: `pip install sherpa-onnx numpy soundfile` in `/home/hatch/workspace/.venv-wave45`
(venv outside repo; never committed).

Model: `sherpa-onnx-whisper-tiny.en` (int8, ~103 MB total) from
`https://huggingface.co/csukuangfj/sherpa-onnx-whisper-tiny.en`
(files land in `models/`, which is gitignored — not committed).

Run: `/home/hatch/workspace/.venv-wave45/bin/python sherpa_smoke.py`

Output (recorded verbatim in `proofs/sherpa_smoke_proof.json`):
```
"The quick roundfoc jump over the lazy log. This is a test on the speech
 recognition pipeline. Speaker 1 says the low."
```
22 words, 2.54 s wall-clock. (Errors like "roundfoc"/"lazy log" are honest
tiny.en output on synthetic speech — not corrected or faked.)

One real bug hit during wiring: newer sherpa-onnx `OfflineStream` has no
`input_finished()` — script calls `recognizer.decode_stream(stream)` directly.

## 4. faster-whisper (MIT) — WIRED ✅

Install: `pip install faster-whisper sherpa-onnx soundfile` (lean venv, ~506 MB
installed; model `tiny.en` auto-downloaded from HF into `~/.cache/huggingface`,
not into the repo).

Run: `/home/hatch/workspace/.venv-wave45/bin/python faster_whisper_smoke.py`
(with IPv6 literals stripped from `no_proxy`/`NO_PROXY` per the documented
httpx quirk)

Output (recorded verbatim in `proofs/faster_whisper_smoke_proof.json`):
```
segment 0.00–3.32:  "The quick round fox jump over the lazy log."
segment 3.32–6.56:  "This is a test on the speech recognition pipeline."
segment 6.56–8.20:  "Speak at one sense below."
detected_language: en (p=1.0), 2.2 s wall-clock
```
Real transcription with real timestamps on the real fixture.

One real bug hit during wiring: this env's PyAV 19.0.1 rejects faster-whisper's
`av.open(..., metadata_errors="ignore")` call (`TypeError`). Worked around by
passing float32 16 kHz audio directly to `transcribe()` (documented in the
script header) — no result simulation.

## 5. WhisperX (BSD-2-Clause) — NOT WIRED ❌ (honest failure)

License gate: PASSED (BSD-2-Clause). Install: FAILED in this environment.

What happened: `pip install whisperx` pulled its torch+transformers dependency
chain; pip's download cache (`TMPDIR=~/workspace/.pip-tmp` on the home disk)
grew to ~4.4 GB and the VM disk (`/dev/mapper/rv`, 100 GB) hit 99% full during
the download. Per the disk-cleanup law the install process was killed and the
temp dirs (`~/.venv-wave45`, `~/.pip-tmp`, `~/.cache/pip`) were removed,
restoring the disk to ~92%. The `whisperx_smoke.py` scaffold was removed from
the tree (not run — import never succeeded).

Exact error signature during the failed run: `OSError: [Errno 28] No space
left on device` from pip. This is an environment constraint, not a license or
code failure; WhisperX remains a valid permissive candidate on a machine with
more headroom. faster-whisper (MIT) was substituted as the second wired tool.

Also noted: WhisperX diarization needs gated pyannote.audio models + an HF
auth token, unavailable in this lane — diarization is out of scope either way.

## 6. Artifact hashes

See `SHA256SUMS` (generated with `sha256sum` over every committed file in this
lane dir) and `proof_manifest.json`.

## 7. Environment notes for future waves

- `/tmp` is a 512 MB tmpfs (95% full at start); pip installs must use
  `TMPDIR` on the home disk.
- `no_proxy`/`NO_PROXY` contain IPv6 literals (`::1`, `[::1]`) that crash
  httpx (`InvalidURL: Invalid port: ':1]'`) inside huggingface_hub — strip
  entries containing `::` before any HF download.
- venv lives at `/home/hatch/workspace/.venv-wave45`, OUTSIDE the repo, and is
  never committed. `models/` (sherpa-onnx ONNX files, ~103 MB) is gitignored.
