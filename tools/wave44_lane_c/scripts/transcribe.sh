#!/usr/bin/env bash
# Transcribe a 16kHz mono WAV with whisper.cpp's whisper-cli.
# Usage: transcribe.sh <model.ggml> <audio_16k.wav> [out-prefix]
#   Model weights are NOT in git; download at runtime, e.g.:
#   https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"
WHISPER_BIN="${W44_WHISPER_BIN:-$TOOL_DIR/vendor/whisper.cpp/build/bin/whisper-cli}"
[ -x "$WHISPER_BIN" ] || { echo "missing whisper-cli; run scripts/build_whisper_cpp.sh first"; exit 1; }
MODEL="$1"; AUDIO="$2"; OUT="${3:-transcript}"
[ -f "$MODEL" ] || { echo "model not found: $MODEL"; exit 1; }
"$WHISPER_BIN" -m "$MODEL" -f "$AUDIO" -otxt -of "$OUT"
echo "transcript: ${OUT}.txt"
