# PROOFS — sherpa-tts (WIRED)

Date: 2026-10-07. sherpa-onnx 1.13.8 (Apache-2.0 ✅) + Matcha acoustic model
+ Vocos vocoder, isolated venv `~/venvs/sherpa`.

## Install

- `python3 -m venv ~/venvs/sherpa` then `pip install sherpa-onnx` (1.13.8,
  bundles onnxruntime) + `numpy`.
- Model fetch via `curl` (the sandbox `httpx` stack stalls under the egress
  proxy — `curl` works) into `models/matcha-icefall-en_US-ljspeech/`:
  - `model-steps-3.onnx` (74 MB, Matcha acoustic, LJSpeech female voice) —
    from https://huggingface.co/csukuangfj/matcha-icefall-en_US-ljspeech
  - `vocos-22khz-univ.onnx` (54 MB) — from the sherpa-onnx GitHub release
    tag `vocoder-models` (upstream Vocos repo gemelo-ai/vocos is MIT ✅)
  - `tokens.txt` + `espeak-ng-data/` (phonemizer data)
- Note: this checkpoint of the Matcha model requires a **separate vocoder**
  (`OfflineTtsMatchaImpl` errors without one); the official release tarball
  does not bundle it. The ONNX model needs NO `model.safetensors`/`pytorch`
  conversion — runs as-is on CPU.

Disk note: the sandbox `/tmp` is a 512 MB tmpfs — fetch large files directly
into the repo, not `/tmp`. Also purged a stale 4.2 GB `~/.cache/pip` to make
room (regenerable cache, Wave-1/2 residue).

## Smoke test

    ~/venvs/sherpa/bin/python sherpa_tts.py \
        "The council does not explain itself. It declares." \
        -o proofs/sherpa_test.wav

Result: `proofs/sherpa_test.wav` — **3.84 s, 22050 Hz, 169,516 bytes**, real
audible speech (RMS 0.0566, peak 0.5056 — speech-like, not silence or noise).
Same test line as the Piper/st stable-ts proofs, so it's directly comparable.

sha256: `a40034bc696e7da5607a494c55eddc6ae191f6f566059c34ece8c5590c89c813`

## License verdict

- sherpa-onnx runtime: **Apache-2.0 ✅** (verified at upstream LICENSE).
- Vocos vocoder: **MIT ✅** (upstream gemelo-ai/vocos LICENSE, Charactr Inc.).
- Matcha voice weights: **❓ UNKNOWN** — no license statement from the author;
  training data is public-domain LJSpeech. Prototype-only until the owner clears
  the voice for commercial use.

## Why this tool exists

The sandbox egress proxy blocks the WebSocket upgrade to
`speech.platform.bing.com`, so edge-tts synthesis fails here (see
`PROOFS_edge_tts.md`). sherpa-tts is fully offline — no network, no key.
