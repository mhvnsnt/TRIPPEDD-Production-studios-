#!/usr/bin/env bash
set -euo pipefail

ROOT="${TRIPPEDD_OPENSOURCE_ROOT:-.trippedd/opensource}"
mkdir -p "$ROOT"

clone_or_update() {
  local name="$1" url="$2" ref="$3"
  local dir="$ROOT/$name"
  if [ -d "$dir/.git" ]; then
    git -C "$dir" fetch --depth=1 origin "$ref"
    git -C "$dir" checkout --detach FETCH_HEAD
  else
    git clone --depth=1 --branch "$ref" "$url" "$dir"
  fi
}

# Full upstream projects, pinned by release/tag. These remain independently
# inspectable and are not reduced to copied snippets.
clone_or_update "flamenco" "https://projects.blender.org/studio/flamenco.git" "v3.9.3"
clone_or_update "opencue" "https://github.com/AcademySoftwareFoundation/OpenCue.git" "v1.19.1"

echo "TRIPPEDD_OPEN_SOURCE_RENDER_STACK=READY"
printf 'Flamenco: '; git -C "$ROOT/flamenco" rev-parse HEAD
printf 'OpenCue: '; git -C "$ROOT/opencue" rev-parse HEAD
