#!/usr/bin/env python3
"""sherpa_tts.py — offline neural TTS via sherpa-onnx (Apache-2.0).

Matcha-TTS acoustic model (LJSpeech-trained single female voice), CPU-only,
no network at synthesis time, no API key.

Environment: uses the isolated venv at ~/venvs/sherpa (sherpa-onnx 1.13.8).
System pip cannot install it (Debian PyYAML conflict) — always run via the venv:
    ~/venvs/sherpa/bin/python sherpa_tts.py "line to speak" -o out.wav

Usage:
    ~/venvs/sherpa/bin/python sherpa_tts.py "The council does not explain itself." -o proofs/sherpa_test.wav
    ~/venvs/sherpa/bin/python sherpa_tts.py lines.txt -o ep_vo.wav --speed 1.05

NOTE (license): sherpa-onnx runtime is Apache-2.0 — safe to prototype and ship.
The bundled Matcha voice (csukuangfj/matcha-icefall-en_US-ljspeech, trained on
the public-domain LJSpeech dataset) carries NO explicit license statement from
its author — treated as ❓; verify/clear with the owner before shipping anything
commercial that embeds this voice.
"""
import argparse
import os
import sys
import wave

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "matcha-icefall-en_US-ljspeech")


def main() -> int:
    ap = argparse.ArgumentParser(description="Offline TTS via sherpa-onnx (Matcha).")
    ap.add_argument("text", help="Text to speak, or @file.txt for multi-line batch.")
    ap.add_argument("-o", "--out", required=True, help="Output .wav path (16 kHz mono).")
    ap.add_argument("--speed", type=float, default=1.0, help="Speaking speed (default 1.0).")
    ap.add_argument("--threads", type=int, default=4)
    args = ap.parse_args()

    import sherpa_onnx

    tts_config = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            matcha=sherpa_onnx.OfflineTtsMatchaModelConfig(
                acoustic_model=os.path.join(MODEL_DIR, "model-steps-3.onnx"),
                vocoder=os.path.join(MODEL_DIR, "vocos-22khz-univ.onnx"),
                lexicon="",
                tokens=os.path.join(MODEL_DIR, "tokens.txt"),
                data_dir=os.path.join(MODEL_DIR, "espeak-ng-data"),
                dict_dir=os.path.join(MODEL_DIR, "espeak-ng-data"),
            ),
            num_threads=args.threads,
            debug=False,
            provider="cpu",
        ),
        rule_fsts="",
        max_num_sentences=1,
    )
    tts = sherpa_onnx.OfflineTts(tts_config)

    if args.text.startswith("@"):
        with open(args.text[1:], encoding="utf-8") as f:
            texts = [ln.strip() for ln in f if ln.strip()]
    else:
        texts = [args.text]

    samples_list = []
    for t in texts:
        audio = tts.generate(t, sid=0, speed=args.speed)
        samples_list.extend(audio.samples)

    import numpy as np

    samples = np.array(samples_list, dtype=np.float32)
    samples = np.clip(samples, -1.0, 1.0)
    pcm = (samples * 32767).astype(np.int16).tobytes()

    with wave.open(args.out, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(tts.sample_rate)
        wf.writeframes(pcm)

    dur = len(samples_list) / tts.sample_rate
    print(f"wrote {args.out}: {len(texts)} line(s), {dur:.2f}s, {tts.sample_rate} Hz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
