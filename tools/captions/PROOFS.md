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
