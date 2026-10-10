#!/usr/bin/env bash
# BUILD.sh — TRIPPEDD lip-sync pipeline (Lane B, Anim Pull Wave 1).
#
# What this builds: a working WAV -> viseme-timeline lip-sync pipeline on top of
# Rhubarb Lip Sync 1.14.0 (MIT; binary already staged at tools/lipsync/bin/rhubarb).
#
# Dependencies (system): espeak-ng (stand-in VO only), ffmpeg, python3.
# Rhubarb needs its acoustic-model data dir `bin/res/` next to the binary
# (already in-repo; binary + res/ total ~7.3 MB — well under the 100 MB git limit).
# No model weights to download; nothing heavy leaves the repo.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "== 1. Rhubarb binary =="
"$HERE/bin/rhubarb" --version

echo "== 2. Stand-in dialogue WAV (Static EP02 L1, espeak-ng) =="
mkdir -p "$HERE/proofs/lane-b"
espeak-ng -v en-us -s 165 -w "$HERE/proofs/lane-b/static_L1_standin_raw.wav" \
  "Ayo! You see that fire? That's the bat signal, baby - council's in session! Everybody move like you got somewhere to be!"
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \
  "$HERE/proofs/lane-b/static_L1_standin_raw.wav"

echo "== 3. Run the pipeline (Rhubarb -> TSV -> timeline JSON -> verify) =="
chmod +x "$HERE/lipsync_pipeline.sh" "$HERE/rhubarb_to_timeline.py"
"$HERE/lipsync_pipeline.sh" "$HERE/proofs/lane-b/static_L1_standin_raw.wav" "$HERE/proofs/lane-b"

echo "== 4. Hashes =="
sha256sum "$HERE/proofs/lane-b/static_L1_standin_raw.wav" \
           "$HERE/proofs/lane-b/static_L1_cues.tsv" \
           "$HERE/proofs/lane-b/static_L1_timeline.json"

echo "BUILD DONE — see proofs/lane-b/PROOFS_LANE_B.md for the proof record."
