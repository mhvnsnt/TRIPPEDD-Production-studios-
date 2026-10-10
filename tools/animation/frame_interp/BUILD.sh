#!/bin/bash
# frame_interp/BUILD.sh — wire + prove the ffmpeg minterpolate frame interpolator.
# No downloads, no models. Runs interpolate.py (synthesizes keyframes, interpolates,
# verifies) and prints the JSON evidence + PASS/FAIL.
set -euo pipefail
cd "$(dirname "$0")"
command -v ffmpeg >/dev/null || { echo "ffmpeg not found"; exit 1; }
python3 interpolate.py
