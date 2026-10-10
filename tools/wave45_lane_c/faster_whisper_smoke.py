#!/usr/bin/env python3
"""Wave 45 Lane C smoke test: faster-whisper (MIT) transcription.

Runs faster-whisper with the `tiny.en` model on the real espeak-ng fixture
WAV and writes a JSON proof artifact. Exit non-zero on transcription failure
(no simulated success).
"""
import json
import time
from pathlib import Path

from faster_whisper import WhisperModel

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "fixture.wav"
FIXTURE_16K = HERE / "fixtures" / "fixture_16k.wav"  # 16 kHz copy (av bypass)
PROOFS = HERE / "proofs"


def load_audio_16k(path: Path):
    import wave

    import numpy as np

    with wave.open(str(path)) as w:
        assert w.getframerate() == 16000 and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(
            np.float32
        ) / 32768.0


def main():
    t0 = time.time()
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    # NOTE: pass float32 16 kHz audio directly to avoid the
    # `av.open(metadata_errors=...)` incompatibility in this env's PyAV 19.0.1.
    audio = load_audio_16k(FIXTURE_16K)
    segments, info = model.transcribe(audio, language="en", beam_size=5)
    segs = list(segments)
    elapsed = time.time() - t0

    text = " ".join(s.text for s in segs).strip()
    PROOFS.mkdir(exist_ok=True)
    proof = {
        "tool": "faster-whisper",
        "tool_license": "MIT",
        "tool_license_url": "https://github.com/SYSTRAN/faster-whisper/blob/master/LICENSE",
        "model": "tiny.en (ctranslate2 converted)",
        "fixture": str(FIXTURE.relative_to(HERE)),
        "detected_language": info.language,
        "detected_language_probability": round(info.language_probability, 3),
        "segments": [
            {
                "start": round(s.start, 2),
                "end": round(s.end, 2),
                "text": s.text,
            }
            for s in segs
        ],
        "full_text": text,
        "elapsed_s": round(elapsed, 2),
    }
    out = PROOFS / "faster_whisper_smoke_proof.json"
    out.write_text(json.dumps(proof, indent=2))
    print(json.dumps(proof, indent=2))
    if not text:
        raise SystemExit("FAIL: empty transcript")


if __name__ == "__main__":
    main()
