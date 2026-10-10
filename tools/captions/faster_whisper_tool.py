#!/usr/bin/env python3
"""faster_whisper_tool.py — faster-whisper word-level transcription to SRT.

SYSTRAN faster-whisper (MIT) via CTranslate2: fast local Whisper inference
with word-level timestamps, no API key. First run downloads the model
(~75MB tiny) from HuggingFace into ~/.cache.

Environment: uses the isolated venv at ~/venvs/wave12-captions:
    ~/venvs/wave12-captions/bin/python faster_whisper_tool.py vo.wav -o caps.srt

Usage:
    ~/venvs/wave12-captions/bin/python faster_whisper_tool.py vo.wav -o caps.srt
    ~/venvs/wave12-captions/bin/python faster_whisper_tool.py vo.wav -o caps.srt --model base --language en --karaoke

NOTE (license): faster-whisper is MIT — safe to wire. Whisper weights are MIT.
"""
import argparse
import sys
from pathlib import Path


def srt_time(sec: float) -> str:
    if sec < 0:
        sec = 0
    h = int(sec // 3600); m = int((sec % 3600) // 60)
    s = int(sec % 60); ms = int(round((sec - int(sec)) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Transcribe audio to word-level SRT with faster-whisper.")
    ap.add_argument("audio", help="Input audio file (wav/mp3).")
    ap.add_argument("-o", "--out", required=True, help="Output .srt path.")
    ap.add_argument("--model", default="tiny", help="Whisper size: tiny/base/small/medium.")
    ap.add_argument("--language", default="en")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--compute-type", default="int8")
    ap.add_argument("--karaoke", action="store_true",
                    help="Word-level cues with current word highlighted (ASS-style karaoke SRT).")
    ap.add_argument("--wav16", action="store_true",
                    help="Read input as 16kHz mono WAV via stdlib wave module "
                         "(bypasses PyAV; faster-whisper accepts a float32 numpy array).")
    args = ap.parse_args()

    from faster_whisper import WhisperModel
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    audio = args.audio
    if args.wav16:
        import wave as _wave
        import numpy as _np
        with _wave.open(args.audio, "rb") as w:
            assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == 16000, \
                f"--wav16 needs 16kHz mono s16 WAV, got {w.getnchannels()}ch/{w.getsampwidth()*8}bit/{w.getframerate()}Hz"
            audio = _np.frombuffer(w.readframes(w.getnframes()), dtype=_np.int16).astype(_np.float32) / 32768.0
    segments, info = model.transcribe(audio, language=args.language, word_timestamps=True)
    segments = list(segments)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with out.open("w", encoding="utf-8") as f:
        for seg in segments:
            words = list(seg.words or [])
            if args.karaoke and words:
                for i, w in enumerate(words):
                    n += 1
                    parts = [
                        f"<font color=\"#00FF00\">{x.word}</font>" if j == i else x.word
                        for j, x in enumerate(words)
                    ]
                    hi = " ".join(parts)
                    f.write(f"{n}\n{srt_time(seg.start)} --> {srt_time(seg.end)}\n{hi}\n\n")
            else:
                for w in words:
                    n += 1
                    f.write(f"{n}\n{srt_time(w.start)} --> {srt_time(w.end)}\n{w.word.strip()}\n\n")
    nwords = sum(len(list(s.words or [])) for s in segments)
    print(f"wrote {out}: {len(segments)} segments, {nwords} words, {n} cues "
          f"(detected language {info.language} p={info.language_probability:.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
