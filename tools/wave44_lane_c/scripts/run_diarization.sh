#!/usr/bin/env bash
# Run permissive-license speaker diarization on a 16kHz mono WAV.
# Usage: run_diarization.sh <audio_16k.wav> [n_speakers]
# Python deps (all permissive: MIT/BSD-3/ISC): webrtcvad, librosa, scikit-learn, soundfile.
# Set W44_VENV to a venv containing them; otherwise uses `python3` from PATH.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"
PY="${W44_VENV:+$W44_VENV/bin/python}"
PY="${PY:-python3}"
"$PY" "$TOOL_DIR/diarize_vad_cluster.py" "$1" "${2:-2}"
