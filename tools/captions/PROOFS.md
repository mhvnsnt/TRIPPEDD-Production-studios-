# PROOFS — caption tools

Date: 2026-10-07.

## pysubs2 (WIRED)

pysubs2 1.9.0 (MIT), installed via pip.

Smoke test:

    python3 pysubs2_tool.py --demo -o proofs/pysubs2_demo.srt
    python3 pysubs2_tool.py proofs/pysubs2_demo.srt -o proofs/pysubs2_shifted.srt --shift 1.5

Result: 3-event demo SRT created, then shifted +1.5s — timings verified
in the output file (`00:00:00,500→00:00:02,000` etc.).

Hashes (sha256):

- `proofs/pysubs2_demo.srt`: `c71801dba0f08c02ea9beea4cd15e5668d31a96402a511a4b58a91f74c4a12a4`
- `proofs/pysubs2_shifted.srt`: `90ee24dc52763068c3a6bd243ffe26a5a64ddd0cf999c790a266ae73f3fe7753`

## stable-ts (WIRED)

stable-ts 2.19.1 (MIT) + openai-whisper 20250625 + CPU torch.

Install note: `pip install --no-deps --no-build-isolation stable-ts`;
CPU `torchaudio` from the PyTorch CPU index; `openai-whisper` (its CUDA
torch dep is already satisfied by the CPU torch — pip accepts the
`+cpu` local version).

Smoke test (input: the 3.05s Piper TTS proof WAV):

    python3 stable_ts_captions.py ~/workspace/god-molecule-studio/tools/voice/piper_test.wav \
      -o proofs/stable_ts_test.srt --model tiny

Result: `proofs/stable_ts_test.srt` — **2 segments, 8 words**, word-level
karaoke SRT (current word highlighted green), timings 0.18s–2.72s,
transcription exactly matches the spoken line
("The council does not explain itself. It declares.").

Hash (sha256):

- `proofs/stable_ts_test.srt`: `a4983efb937290ada7fcada9c98ee3f1731954c494489d75455e84ab58a1bd94`

## WhisperX (WIRED — install verified; first-run transcription deferred)

WhisperX 3.8.6 (BSD-2-Clause, verified at upstream LICENSE), installed in the
isolated venv `~/venvs/whisperx` (torch 2.14.1+cpu). System pip cannot install
it (Debian PyYAML 6.0.1 uninstall conflict) — always use the venv.

Smoke tests (2026-10-07):
- `~/venvs/whisperx/bin/python -c "import whisperx"` — OK (`WHISPERX_OK`).
- `~/venvs/whisperx/bin/whisperx --help` — OK, full CLI surface present.

Limitation (honest): the first transcription run downloads the Whisper model
(~75MB tiny) + wav2vec2 alignment model (~360MB English) from HuggingFace.
That download tripped a runtime approval gate in this sandbox, so the
end-to-end word-level transcription proof is DEFERRED to a workstation run.
`tools/captions/whisperx_tool.py` is the ready wiring script (word-level SRT).

Why it matters: word-level forced alignment fixes faster-whisper's
utterance-level timestamps ("can be inaccurate by several seconds") —
karaoke-style per-word timing for the show's comedy captions.

## Wave 12 Lane C (2026-10-07)

Environment: isolated venv `~/venvs/wave12-captions` (python 3.12). System pip is
PEP-668 externally-managed — always run via the venv.

### ttconv (WIRED)

sandflow/ttconv (BSD-2-Clause, verified via GitHub license metadata), pure Python.

Smoke tests:

    ~/venvs/wave12-captions/bin/python ttconv_tool.py --demo
    ~/venvs/wave12-captions/bin/python ttconv_tool.py proofs/pysubs2_demo.srt -o proofs/ttconv_demo.vtt --itype SRT --otype VTT
    ~/venvs/wave12-captions/bin/python ttconv_tool.py proofs/pysubs2_demo.srt -o proofs/ttconv_demo.ttml --itype SRT --otype TTML

Result: `--demo` = SRT→VTT→SRT roundtrip, 3/3 cue texts byte-identical.
Real artifacts: `proofs/ttconv_demo.vtt` (valid WEBVTT, 3 cues), `proofs/ttconv_demo.ttml`
(valid IMSC TTML, 3 `<p>` cues, timings preserved) — both converted from the real
`proofs/pysubs2_demo.srt`. Read and verified by eye.

Hashes (sha256):

- `proofs/ttconv_demo.vtt`: `a5dfc89265cfe9cac71a7b5ed425eeb3815ea0ed61ca652412710ae8ea4649ad`
- `proofs/ttconv_demo.ttml`: `5b1cc8d270628d1330f291d6e97cb17955c3e0ecb991d8c1ebb7d2eb0d6541b8`

### faster-whisper (WIRED)

faster-whisper 1.2.1 (MIT) + CTranslate2 4.8.2, CPU int8, tiny model (~75MB,
downloaded from HuggingFace on first run — no approval gate tripped this run;
strip IPv6 literals from no_proxy/NO_PROXY before huggingface_hub use, see TOOLS.md).

Smoke test (input: the 3.05s Piper TTS proof WAV, ground-truth line
"The council does not explain itself. It declares.", ffmpeg-resampled to 16kHz mono):

    ~/venvs/wave12-captions/bin/python faster_whisper_tool.py /tmp/piper_16k.wav -o proofs/faster_whisper_test.srt --model tiny --wav16
    ~/venvs/wave12-captions/bin/python faster_whisper_tool.py /tmp/piper_16k.wav -o proofs/faster_whisper_karaoke.srt --model tiny --wav16 --karaoke

Result: `proofs/faster_whisper_test.srt` — 1 segment, **8/8 words correct**,
word-level timings 0.00s–2.74s, language en p=1.00. `proofs/faster_whisper_karaoke.srt`
— same 8 words as karaoke-style cues (current word green-highlighted).

Hashes (sha256):

- `proofs/faster_whisper_test.srt`: `c165672dbe997388ea1b2f71204ae206237b282b9841e2ca59aa8435afa8dd23`
- `proofs/faster_whisper_karaoke.srt`: `57d6c7de99771a3db10e1a7ecfc42b8707a8b651a1510c40ae368e7c95e09aa7`

Honest defects / limitations (no fakes):

1. **PyAV incompatibility (worked around, not fixed):** faster-whisper 1.2.1's
   `decode_audio` passes `metadata_errors=` to `av.open()`, which PyAV 19.0.1
   rejects (`TypeError`). Workaround: `--wav16` reads 16kHz mono WAV via stdlib
   `wave` and passes a float32 numpy array straight to `model.transcribe`.
   Pinning pyav to an older version was attempted but PyPI was unreachable at
   that moment. Non-WAV inputs (mp3/m4a) are NOT covered until the PyAV pin is resolved.
2. **Karaoke SRT word tokens carry leading spaces** (whisper convention: " The",
   " Council") — the highlight join shows double spaces. Cosmetic; text is intact.
3. tiny model only smoke-tested; base/small/medium untested on CPU here.
