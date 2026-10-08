# Wave 45 Lane C — permissive ASR/diarization-adjacent tool wiring

Target: wire 1–2 permissive-licensed ASR/diarization-adjacent tools with REAL proofs.

## License verification (upstream, checked 2026-10-08)

| Tool | License | Evidence |
|------|---------|----------|
| sherpa-onnx (k2-fsa) | **Apache-2.0** | PyPI `license: Apache licensed, as found in the LICENSE file`; GitHub license API SPDX `Apache-2.0` — https://github.com/k2-fsa/sherpa-onnx/blob/master/LICENSE |
| WhisperX (m-bain) | **BSD-2-Clause** | PyPI `license: BSD-2-Clause`; GitHub license API SPDX `BSD-2-Clause` — https://github.com/m-bain/whisperX/blob/main/LICENSE |

Both are permissive → wired. GPL/AGPL tools are never linked/imported here.

## Fixture

`fixtures/fixture.wav` — REAL audio, generated with espeak-ng (no fake results):
```
espeak-ng -v en -s 150 -w fixtures/fixture.wav \
  "The quick brown fox jumps over the lazy dog. This is a test of the speech recognition pipeline. Speaker one says hello."
```
8.43 s, mono, 22050 Hz.

## Smoke tests

| Script | Tool / model | Proof artifact |
|--------|--------------|----------------|
| `sherpa_smoke.py` | sherpa-onnx, whisper `tiny.en` int8 | `proofs/sherpa_smoke_proof.json` |
| `whisperx_smoke.py` | WhisperX, `tiny.en` | `proofs/whisperx_smoke_proof.json` |

Run: `/home/hatch/workspace/.venv-wave45/bin/python <script>` (venv lives OUTSIDE the repo so it is never committed; `models/` is gitignored — binaries stay out of git per the no->100MB-binary rule).

## Known honest gaps

- WhisperX diarization is NOT wired: it requires gated pyannote.audio models + a HuggingFace auth token, unavailable in this lane.
- WhisperX word-alignment may fail if the align-model download fails; the script records the error instead of pretending.

See `PROOFS.md` for exact commands, outputs, and artifact hashes.
