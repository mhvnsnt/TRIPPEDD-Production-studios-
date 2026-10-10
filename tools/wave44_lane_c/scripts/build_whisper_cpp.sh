#!/usr/bin/env bash
# Build whisper.cpp (MIT, https://github.com/ggerganov/whisper.cpp) -> whisper-cli.
# Usage: build_whisper_cpp.sh [DEST]
#   DEST defaults to <repo>/tools/wave44_lane_c/vendor/whisper.cpp (git-ignored).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOL_DIR="$(dirname "$HERE")"
DEST="${1:-$TOOL_DIR/vendor/whisper.cpp}"
if [ -d "$DEST/build/bin" ] && [ -x "$DEST/build/bin/whisper-cli" ]; then
  echo "whisper-cli already built at $DEST/build/bin/whisper-cli"
  exit 0
fi
mkdir -p "$(dirname "$DEST")"
if [ ! -d "$DEST/.git" ]; then
  git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git "$DEST"
fi
grep -q "MIT License" "$DEST/LICENSE" || { echo "LICENSE check failed: not MIT"; exit 1; }
echo "license OK: whisper.cpp is MIT"
cmake -S "$DEST" -B "$DEST/build" -DCMAKE_BUILD_TYPE=Release
cmake --build "$DEST/build" -j"$(nproc)" --target whisper-cli
echo "built: $DEST/build/bin/whisper-cli"
