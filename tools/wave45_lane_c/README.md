# Wave 45 Lane C — permissive ASR/diarization-adjacent tool wiring

Target: wire 1–2 permissive-licensed ASR/diarization-adjacent tools with REAL proofs.

## License verification (upstream, checked 2026-10-08)

| Tool | License | Evidence |
|------|---------|----------|
| sherpa-onnx (k2-fsa) | **Apache-2.0** | PyPI `license: Apache licensed, as found in the LICENSE file`; GitHub license API SPDX `Apache-2.0` — https://github.com/k2-fsa/sherpa-onnx/blob/master/LICENSE |
| faster-whisper (SYSTRAN) | **MIT** | PyPI `license: MIT`; GitHub license API SPDX `MIT` — https://github.com/SYSTRAN/faster-whisper/blob/master/LICENSE |

Candidate that did NOT wire: **WhisperX (m-bain)** — license verified permissive (**BSD-2-Clause** via PyPI + GitHub license API), so it cleared the license gate, but the install failed in THIS environment: its dependency chain (torch + transformers + deps) pulled ~4.4 GB of pip downloads and drove the VM disk to 99%. The install was killed and temps cleaned per the disk-cleanup law; documented as an honest failure in `PROOFS.md`.

Both are permissive → wired. GPL/AGPL tools are never linked/imported here.

## Fixture

Real audio, generated with espeak-ng (no fake results):

```
espeak-ng -v en -s 150 -w fixtures/fixture.wav \
  "The quick brown fox jumps over the lazy dog. This is a test of the speech recognition pipeline. Speaker one says hello."
ffmpeg -i fixtures/fixture.wav -ar 16000 fixtures/fixture_16k.wav
```

`fixture.wav`: 8.43 s, mono, 22050 Hz. `fixture_16k.wav`: same audio resampled to 16 kHz (needed by faster-whisper to bypass a PyAV incompatibility in this env — see PROOFS.md).

## Smoke tests

| Script | Tool / model | Proof artifact |
|--------|--------------|----------------|
| `sherpa_smoke.py` | sherpa-onnx, whisper `tiny.en` int8 | `proofs/sherpa_smoke_proof.json` |
| `faster_whisper_smoke.py` | faster-whisper, `tiny.en` | `proofs/faster_whisper_smoke_proof.json` |

Run: `/home/hatch/workspace/.venv-wave45/bin/python <script>` (venv lives OUTSIDE the repo so it is never committed; `models/` is gitignored — binaries stay out of git per the no->100MB-binary rule).

Environment quirks (recorded for future waves):
- `/tmp` is a 512 MB tmpfs that fills fast; use `TMPDIR=~/workspace/.pip-tmp` for pip.
- `no_proxy` contains IPv6 literals that crash httpx (huggingface_hub): strip entries containing `::` before any HF download.

## Known honest gaps

- WhisperX diarization is NOT wired: it requires gated pyannote.audio models + a HuggingFace auth token, unavailable in this lane.
- WhisperX word-alignment may fail if the align-model download fails; the script records the error instead of pretending.

See `PROOFS.md` for exact commands, outputs, and artifact hashes.
