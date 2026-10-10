#!/usr/bin/env python3
"""whisperx_tool.py — WhisperX transcription to word-level SRT.

WhisperX (BSD-2-Clause) upgrades word-level caption timing over faster-whisper
via wav2vec2 forced alignment. Runs fully local, no key. First run downloads
the Whisper model (~75MB tiny) and the alignment model (~360MB English) into
~/.cache.

Environment: uses the isolated venv at ~/venvs/whisperx (torch CPU + whisperx).
System pip cannot install it (Debian PyYAML conflict) — always run via the venv:
    ~/venvs/whisperx/bin/python whisperx_tool.py vo.wav -o caps.srt

Usage:
    ~/venvs/whisperx/bin/python whisperx_tool.py vo.wav -o caps.srt
    ~/venvs/whisperx/bin/python whisperx_tool.py vo.wav -o caps.srt --model base --language en

NOTE (license): WhisperX is BSD-2-Clause — safe to prototype and ship.
"""
import argparse
import json
import subprocess
import sys


def srt_time(sec: float) -> str:
    h = int(sec // 3600); m = int((sec % 3600) // 60)
    s = int(sec % 60); ms = int(round((sec - int(sec)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Transcribe audio to word-level SRT with WhisperX.")
    ap.add_argument("audio", help="Input audio file (wav/mp3).")
    ap.add_argument("-o", "--out", required=True, help="Output .srt path.")
    ap.add_argument("--model", default="tiny", help="Whisper size: tiny/base/small/medium.")
    ap.add_argument("--language", default="en")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--compute-type", default="int8")
    args = ap.parse_args()

    import whisperx

    model = whisperx.load_model(args.model, args.device, compute_type=args.compute_type)
    audio = whisperx.load_audio(args.audio)
    result = model.transcribe(audio, language=args.language, batch_size=4)

    # word-level alignment
    align_model, metadata = whisperx.load_align_model(language_code=result["language"], device=args.device)
    result = whisperx.align(result["segments"], align_model, metadata, audio, args.device, return_char_alignments=False)

    # write word-level SRT
    n_words = 0
    with open(args.out, "w") as f:
        idx = 1
        for seg in result["segments"]:
            for w in seg.get("words", []):
                if "start" not in w or "end" not in w:
                    continue
                f.write(f"{idx}\n{srt_time(w['start'])} --> {srt_time(w['end'])}\n{w['word'].strip()}\n\n")
                idx += 1
                n_words += 1
    print(f"wrote {args.out}: {n_words} word-level cues, model={args.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
