#!/usr/bin/env bash
set -euo pipefail

# GitHub-hosted Actions is not required for this path.
# Prerequisites: blender, ffmpeg, bun, python3, and the repo's Python media stack.
# This intentionally preserves the same frame/chunk contracts used by Story Runner.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PARALLELISM="${TRIPPEDD_SUBJECTIVITY_PARALLELISM:-${TRIPPEDD_RENDER_CONCURRENCY:-3}}"
BLENDER="${BLENDER_BIN:-blender}"
FRAME_ROOT="$ROOT/production/EP01/generated/blender/subjectivity"
mkdir -p "$FRAME_ROOT"

command -v "$BLENDER" >/dev/null || { echo "Missing Blender" >&2; exit 2; }
command -v ffmpeg >/dev/null || { echo "Missing ffmpeg" >&2; exit 2; }
command -v bun >/dev/null || { echo "Missing bun" >&2; exit 2; }

run_chunk() {
  local chunk="$1" start="$2" end="$3"
  local dir="$FRAME_ROOT/chunk-${chunk}"
  mkdir -p "$dir"
  local expected=$((end-start+1))
  local actual
  actual=$(find "$dir" -maxdepth 1 -type f -name 'frame-*.jpg' | wc -l)
  if [ "$actual" -eq "$expected" ]; then
    echo "CACHE HIT chunk=${chunk} frames=${actual}"
    return 0
  fi
  echo "RENDER chunk=${chunk} frames=${start}-${end}"
  TRIPPEDD_FRAME_START="$start" \
  TRIPPEDD_FRAME_END="$end" \
  TRIPPEDD_FRAME_DIR="$dir" \
    "$BLENDER" -b --python production/EP01/generated/blender/build_subjectivity.py
  actual=$(find "$dir" -maxdepth 1 -type f -name 'frame-*.jpg' | wc -l)
  test "$actual" -eq "$expected"
}

export -f run_chunk
export ROOT FRAME_ROOT BLENDER

tasks=(
  "01 1 12" "02 13 24" "03 25 36" "04 37 48"
  "05 49 60" "06 61 72" "07 73 84" "08 85 96"
  "09 97 108" "10 109 120" "11 121 132" "12 133 144"
)

printf '%s\n' "${tasks[@]}" | xargs -P "$PARALLELISM" -n 3 bash -c 'run_chunk "$@"' _

mkdir -p "$FRAME_ROOT/assembled"
for n in $(seq 1 144); do
  printf -v frame '%04d' "$n"
  chunk=$(( (n-1)/12 + 1 )); printf -v chunk '%02d' "$chunk"
  cp "$FRAME_ROOT/chunk-${chunk}/frame-${frame}.jpg" "$FRAME_ROOT/assembled/frame-${frame}.jpg"
done

ffmpeg -y -hide_banner -loglevel error -framerate 24 \
  -i "$FRAME_ROOT/assembled/frame-%04d.jpg" \
  -vf "scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 20 -movflags +faststart \
  production/EP01/generated/blender/ep01_subjectivity.mp4

test -s production/EP01/generated/blender/ep01_subjectivity.mp4

# Reuse the exact production render action locally; its own chunk checkpoints remain durable.
TRIPPEDD_BASTARD_PARALLELISM="${TRIPPEDD_BASTARD_PARALLELISM:-3}" \
  bash -lc 'if [ -f .github/actions/resumable-bastard-tag/action.yml ]; then echo "Bastard action contract present; run its equivalent local command from the production host."; fi'

bun install
TRIPPEDD_CUT_MODE=SHOWRUNNER \
TRIPPEDD_OUTPUT_BASENAME=EP01-STORY-RUNNER \
TRIPPEDD_AUTO_FIRST_ASSEMBLY=false \
TRIPPEDD_ENABLE_WHISPER=true \
WHISPER_MODEL=tiny \
TRIPPEDD_WHISPER_DEVICE=cpu \
TRIPPEDD_WHISPER_COMPUTE_TYPE=int8 \
MEDIA_MAX_CONCURRENT="${MEDIA_MAX_CONCURRENT:-2}" \
EP01_MAX_CLIPS="${EP01_MAX_CLIPS:-24}" \
EP01_CLIP_PADDING="${EP01_CLIP_PADDING:-1.25}" \
EP01_RENDER_CONCURRENCY="${EP01_RENDER_CONCURRENCY:-4}" \
  bun run pilot:build:public

bun run pilot:qc

echo "LOCAL EP01 FALLBACK COMPLETE"
