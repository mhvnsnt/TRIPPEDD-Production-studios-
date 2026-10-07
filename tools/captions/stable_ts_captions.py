#!/usr/bin/env python3
"""stable_ts_captions.py — stable-ts transcription to word-level SRT.

stable-ts (Whisper + word-level alignment) runs fully local, no key.
First run downloads the model (~75MB for tiny, ~500MB for base) into
$STABLE_TS_CACHE / ~/.cache.

Usage:
    python3 stable_ts_captions.py vo.wav -o caps.srt
    python3 stable_ts_captions.py vo.wav -o caps.srt --model base --language en

NOTE (license): stable-ts is GPL-3.0. Runs as a separate local process —
never linked into shipping code — and stays quarantined per
docs/LICENSE_QUARANTINE.md until a license audit clears it (owner law).
"""
import argparse
import sys


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Transcribe audio to word-level SRT with stable-ts.")
    ap.add_argument("audio", help="Input audio file (wav/mp3).")
    ap.add_argument("-o", "--out", required=True, help="Output .srt path.")
    ap.add_argument("--model", default="tiny",
                    help="Whisper size: tiny/base/small/medium.")
    ap.add_argument("--language", default="en")
    ap.add_argument("--word-level", action="store_true", default=True,
                    help="Emit word-level timestamps (default on).")
    args = ap.parse_args()

    import stable_whisper

    model = stable_whisper.load_model(args.model)
    result = model.transcribe(args.audio, language=args.language,
                              word_timestamps=True)
    # to_srt_vtt writes the file; word-level when result has word timings
    result.to_srt_vtt(args.out, word_level=args.word_level)
    n_seg = len(result.segments or [])
    n_words = sum(len(s.words or []) for s in (result.segments or []))
    print(f"wrote {args.out}: {n_seg} segments, {n_words} words, "
          f"model={args.model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
