#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=$(cd "$(dirname "$BASH_SOURCE")/../../.." && pwd)
STACK_ROOT=$ROOT/.trippedd/generative
mkdir -p "$STACK_ROOT"

clone_or_update() {
  local name="$1" url="$2" ref="$3"
  local dir="$STACK_ROOT/$name"
  if [ -d "$dir/.git" ]; then
    git -C "$dir" fetch --depth=1 origin "$ref"
    git -C "$dir" checkout --detach FETCH_HEAD
  else
    git clone --depth=1 --recursive --branch "$ref" "$url" "$dir"
  fi
}

clone_or_update "meshroom" "https://github.com/alicevision/meshroom.git" "v2025.1.0"
clone_or_update "alicevision" "https://github.com/alicevision/AliceVision.git" "develop"
clone_or_update "colmap" "https://github.com/colmap/colmap.git" "main"
clone_or_update "trellis2" "https://github.com/microsoft/TRELLIS.2.git" "main"
clone_or_update "comfyui" "https://github.com/comfyanonymous/ComfyUI.git" "master"
clone_or_update "wan2.1" "https://github.com/Wan-Video/Wan2.1.git" "main"

{
  echo "TRIPPEDD_GOD_MOLECULE_GENERATIVE_STACK=READY"
  for name in meshroom alicevision colmap trellis2 comfyui wan2.1; do
    printf '%s=' "$name"
    git -C "$STACK_ROOT/$name" rev-parse HEAD
  done
} | tee "$STACK_ROOT/STACK-MANIFEST.txt"
