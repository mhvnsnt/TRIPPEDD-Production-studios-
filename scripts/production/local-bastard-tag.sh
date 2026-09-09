#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
BLENDER="${BLENDER_BIN:-blender}"
PARALLELISM="${TRIPPEDD_BASTARD_PARALLELISM:-3}"
FRAME_ROOT="$ROOT/production/EP01/generated/blender/bastard_tag_frames"
mkdir -p "$FRAME_ROOT"

command -v "$BLENDER" >/dev/null || { echo "Missing Blender" >&2; exit 2; }

run_chunk() {
  local chunk="$1" start="$2" end="$3" dir="$FRAME_ROOT/chunk-$1"
  mkdir -p "$dir"
  local expected=$((end-start+1))
  local actual
  actual=$(find "$dir" -maxdepth 1 -type f -name 'frame-*.png' | wc -l)
  if [ "$actual" -eq "$expected" ]; then
    echo "CACHE HIT bastard chunk=${chunk} frames=${actual}"
    return 0
  fi
  TRIPPEDD_FRAME_START="$start" TRIPPEDD_FRAME_END="$end" TRIPPEDD_FRAME_DIR="$dir" \
    "$BLENDER" -b --python production/EP01/generated/blender/build_bastard_tag.py
  actual=$(find "$dir" -maxdepth 1 -type f -name 'frame-*.png' | wc -l)
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
  cp "$FRAME_ROOT/chunk-${chunk}/frame-${frame}.png" "$FRAME_ROOT/assembled/frame-${frame}.png"
done

ffmpeg -y -hide_banner -loglevel error -framerate 24 \
  -i "$FRAME_ROOT/assembled/frame-%04d.png" \
  -vf "scale=1920:1080:flags=lanczos,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 20 -movflags +faststart \
  production/EP01/generated/blender/ep01_bastard_tag.mp4

test -s production/EP01/generated/blender/ep01_bastard_tag.mp4
test -s production/EP01/generated/blender/ep01_bastard_tag.blend
echo "LOCAL BASTARD TAG COMPLETE"
