#!/usr/bin/env python3
"""Wave 45 Lane C smoke test: sherpa-onnx (Apache-2.0) offline whisper ASR.

Runs sherpa-onnx offline-recognizer with whisper tiny.en on the real
espeak-ng fixture WAV and writes a JSON proof artifact. Exit non-zero on
any failure (no simulated success).
"""
import json
import time
import wave
from pathlib import Path

import numpy as np
import sherpa_onnx

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "fixture.wav"
MODELS = HERE / "models"
PROOFS = HERE / "proofs"


def read_wav(path: Path):
    with wave.open(str(path)) as w:
        assert w.getnchannels() == 1, "fixture must be mono"
        sr = w.getframerate()
        samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    return samples, sr


def main():
    t0 = time.time()
    samples, sr = read_wav(FIXTURE)

    recognizer = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=str(MODELS / "tiny.en-encoder.int8.onnx"),
        decoder=str(MODELS / "tiny.en-decoder.int8.onnx"),
        tokens=str(MODELS / "tiny.en-tokens.txt"),
        num_threads=4,
        debug=False,
        language="en",
        task="transcribe",
    )

    stream = recognizer.create_stream()
    stream.accept_waveform(sr, samples)
    recognizer.decode_stream(stream)
    text = stream.result.text.strip()
    elapsed = time.time() - t0

    PROOFS.mkdir(exist_ok=True)
    proof = {
        "tool": "sherpa-onnx",
        "tool_license": "Apache-2.0",
        "tool_license_url": "https://github.com/k2-fsa/sherpa-onnx/blob/master/LICENSE",
        "model": "sherpa-onnx-whisper-tiny.en (int8)",
        "model_url": "https://huggingface.co/csukuangfj/sherpa-onnx-whisper-tiny.en",
        "fixture": str(FIXTURE.relative_to(HERE)),
        "fixture_duration_s": round(len(samples) / sr, 2),
        "transcript": text,
        "transcript_words": len(text.split()),
        "elapsed_s": round(elapsed, 2),
    }
    out = PROOFS / "sherpa_smoke_proof.json"
    out.write_text(json.dumps(proof, indent=2))
    print(json.dumps(proof, indent=2))
    if not text:
        raise SystemExit("FAIL: empty transcript")


if __name__ == "__main__":
    main()
