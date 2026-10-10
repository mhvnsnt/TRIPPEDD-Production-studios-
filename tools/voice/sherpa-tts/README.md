# sherpa-tts (WIRED)

**Date:** 2026-10-07. **Lane:** voice. **Status:** wired with real proof.

## What it is

Offline neural TTS: the [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
runtime (ONNX-runtime TTS/ASR/VAD toolkit) + a Matcha-TTS acoustic model
(`matcha-icefall-en_US-ljspeech`, single female voice, 22.05 kHz). Runs fully
local on CPU — no API key, no network at synthesis time. Replaces the
edge-tts lane (blocked by the sandbox egress proxy — see `PROOFS_edge_tts.md`).

## License

- **sherpa-onnx runtime: Apache-2.0** ✅ — verified at upstream
  (https://raw.githubusercontent.com/k2-fsa/sherpa-onnx/master/LICENSE,
  "Apache License, Version 2.0, January 2004"). Safe to prototype and ship.
- **Vocos vocoder (`vocos-22khz-univ.onnx`): MIT** ✅ — upstream Vocos repo
  (gemelo-ai/vocos) LICENSE is MIT ("Copyright (c) 2023 Charactr Inc.");
  sherpa-onnx's ONNX export carries no separate statement. Safe.
- **Matcha voice (`model-steps-3.onnx`, csukuangfj/matcha-icefall-en_US-ljspeech): ❓ UNKNOWN**
  — the model card (https://huggingface.co/csukuangfj/matcha-icefall-en_US-ljspeech)
  states the training data is LJSpeech (public-domain LibriVox recordings) but
  the weight author publishes NO license statement. Treat as prototype-only;
  clear with the owner before embedding this voice in anything commercial.

## Install

```bash
python3 -m venv ~/venvs/sherpa
~/venvs/sherpa/bin/pip install sherpa-onnx          # 1.13.8, bundles onnxruntime
```

Model files were fetched via `curl` from HuggingFace (the sandbox's `httpx`
stack stalls under the egress proxy — `curl` works) into
`models/matcha-icefall-en_US-ljspeech/`:

- `model-steps-3.onnx` (~104 MB), `tokens.txt`
- `espeak-ng-data/` (phonemizer data: en dict, phondata, lang/gmw/en*)

Do NOT use system pip (Debian PyYAML conflict) — always the `~/venvs/sherpa` venv.

## Usage

```bash
~/venvs/sherpa/bin/python sherpa_tts.py "The council does not explain itself. It declares." \
    -o proofs/sherpa_test.wav
~/venvs/sherpa/bin/python sherpa_tts.py @lines.txt -o episode_vo.wav --speed 1.05
```

Output: 16-bit mono WAV at the model sample rate.

## See also

- `PROOFS.md` — install + smoke-test evidence
- `PROOFS_edge_tts.md` — the edge-tts lane failure record (why this tool exists)
