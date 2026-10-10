#!/usr/bin/env bash
# lipsync_pipeline.sh — TRIPPEDD lip-sync pipeline (Anim Pull Wave 1, Lane B).
#
# Usage:
#   ./lipsync_pipeline.sh <dialogue.wav> <outdir>
# Example:
#   ./lipsync_pipeline.sh proofs/lane-b/static_L1_standin_raw.wav proofs/lane-b
#
# Pipeline: dialogue WAV -> Rhubarb Lip Sync (MIT, local binary) -> TSV mouth
# cues -> rhubarb_to_timeline.py -> timeline JSON + verification.
#
# Inputs: 16-bit WAV (rhubarb resamples internally). Best on clean single-speaker VO.
# Outputs in <outdir>: <name>_cues.tsv, <name>_timeline.json.
# Prints verification summary (coverage, row count, viseme-set check, first 20 rows).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

if [ "$#" -ne 2 ]; then
  echo "usage: lipsync_pipeline.sh <dialogue.wav> <outdir>" >&2
  exit 2
fi
WAV="$1"; OUT="$2"
mkdir -p "$OUT"
BASE="$(basename "$WAV" .wav | sed 's/_standin_raw$//; s/_raw$//')"
TSV="$OUT/${BASE}_cues.tsv"
JSON="$OUT/${BASE}_timeline.json"

"$HERE/bin/rhubarb" -f tsv -o "$TSV" "$WAV" >/dev/null 2>&1
echo "rhubarb -> $TSV"
python3 "$HERE/rhubarb_to_timeline.py" "$TSV" "$WAV" "$JSON"
echo "timeline  -> $JSON"
echo "sha256: $(sha256sum "$JSON" | cut -d' ' -f1)"
