#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENDOR="$ROOT/.trippedd/oss"
mkdir -p "$VENDOR"
clone_or_update() {
  local id="$1" url="$2" ref="$3" dir="$VENDOR/$1"
  if [ ! -d "$dir/.git" ]; then git clone --filter=blob:none --no-tags "$url" "$dir"; fi
  git -C "$dir" fetch --depth=1 origin "$ref" 2>/dev/null || true
  git -C "$dir" fetch --depth=1 --tags origin 2>/dev/null || true
  git -C "$dir" checkout --detach "$ref"
}
clone_or_update comfyui https://github.com/Comfy-Org/ComfyUI.git master
clone_or_update opencue https://github.com/AcademySoftwareFoundation/OpenCue.git v1.19.1
clone_or_update openassetio https://github.com/OpenAssetIO/OpenAssetIO.git main
clone_or_update opencolorio https://github.com/AcademySoftwareFoundation/OpenColorIO.git main
clone_or_update kdenlive https://github.com/KDE/kdenlive.git master
echo "TRIPPEDD_OSS_UMBRELLA=PASS"
