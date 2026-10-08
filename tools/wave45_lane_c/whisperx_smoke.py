#!/usr/bin/env python3
"""Wave 45 Lane C smoke test: WhisperX (BSD-2-Clause) transcribe + align.

Runs WhisperX with the `tiny.en` model on the real espeak-ng fixture WAV,
attempts word-level alignment with the bundled wav2vec2 align model, and
writes a JSON proof artifact. Diarization is intentionally NOT wired:
it requires gated pyannote.audio models + a HuggingFace token, which are
unavailable in this lane — documented as an honest gap in PROOFS.md.
Exit non-zero on transcription failure (no simulated success).
"""
import json
import time
from pathlib import Path

import torch
import whisperx

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "fixture.wav"
PROOFS = HERE / "proofs"

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if torch.cuda.is_available() else "int8"


def main():
    t0 = time.time()
    model = whisperx.load_model("tiny.en", device, compute_type=compute_type)
    audio = whisperx.load_audio(str(FIXTURE))
    result = model.transcribe(audio, batch_size=8, language="en")
    segs = result["segments"]

    aligned = False
    align_error = None
    try:
        align_model, metadata = whisperx.load_align_model(
            language_code=result["language"], device=device
        )
        result = whisperx.align(
            segs, align_model, metadata, audio, device, return_char_alignments=False
        )
        aligned = True
    except Exception as e:  # model download or memory issues -> honest gap
        align_error = f"{type(e).__name__}: {e}"

    elapsed = time.time() - t0
    text = " ".join(s["text"] for s in segs).strip()

    PROOFS.mkdir(exist_ok=True)
    proof = {
        "tool": "whisperx",
        "tool_license": "BSD-2-Clause",
        "tool_license_url": "https://github.com/m-bain/whisperX/blob/main/LICENSE",
        "model": "tiny.en",
        "device": device,
        "compute_type": compute_type,
        "fixture": str(FIXTURE.relative_to(HERE)),
        "segments": [
            {
                "start": round(s["start"], 2),
                "end": round(s["end"], 2),
                "text": s["text"],
                "words": [
                    {"word": w["word"], "start": round(w["start"], 2), "end": round(w["end"], 2)}
                    for w in s.get("words", [])
                ],
            }
            for s in segs
        ],
        "full_text": text,
        "word_alignment": aligned,
        "word_alignment_error": align_error,
        "diarization": "NOT_WIRED_REQUIRES_GATED_PYANNOTE_MODEL_AND_HF_TOKEN",
        "elapsed_s": round(elapsed, 2),
    }
    out = PROOFS / "whisperx_smoke_proof.json"
    out.write_text(json.dumps(proof, indent=2))
    print(json.dumps(proof, indent=2))
    if not text:
        raise SystemExit("FAIL: empty transcript")


if __name__ == "__main__":
    main()
