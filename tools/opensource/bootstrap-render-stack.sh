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

# Full upstream working trees. They stay independent under the TRIPPEDD
# umbrella and are integrated through adapters rather than copied snippets.
# Stable release refs are used where the upstream publishes them; moving
# branches are explicitly recorded in the run manifest when no stable tag is
# available. A production run fails closed if a required backend is missing.
clone_or_update "flamenco" "https://projects.blender.org/studio/flamenco.git" "v3.9.3"
clone_or_update "opencue" "https://github.com/AcademySoftwareFoundation/OpenCue.git" "v1.19.1"
clone_or_update "opentimelineio" "https://github.com/AcademySoftwareFoundation/OpenTimelineIO.git" "v0.18.1"
clone_or_update "opencolorio" "https://github.com/AcademySoftwareFoundation/OpenColorIO.git" "main"
clone_or_update "openimageio" "https://github.com/AcademySoftwareFoundation/OpenImageIO.git" "main"
clone_or_update "openexr" "https://github.com/AcademySoftwareFoundation/openexr.git" "main"
clone_or_update "openvdb" "https://github.com/AcademySoftwareFoundation/openvdb.git" "master"
clone_or_update "natron" "https://github.com/NatronGitHub/Natron.git" "master"
clone_or_update "kitsu" "https://github.com/cgwire/kitsu.git" "main"
clone_or_update "comfyui" "https://github.com/comfyanonymous/ComfyUI.git" "master"
clone_or_update "vapoursynth" "https://github.com/vapoursynth/vapoursynth.git" "master"
clone_or_update "mlt" "https://github.com/mltframework/mlt.git" "master"
clone_or_update "meshroom" "https://github.com/alicevision/meshroom.git" "v2025.1.0"
clone_or_update "alicevision" "https://github.com/alicevision/AliceVision.git" "develop"
clone_or_update "colmap" "https://github.com/colmap/colmap.git" "main"
clone_or_update "trellis2" "https://github.com/microsoft/TRELLIS.2.git" "main"
clone_or_update "wan2.1" "https://github.com/Wan-Video/Wan2.1.git" "main"

{
  echo "TRIPPEDD_OPEN_SOURCE_RENDER_STACK=READY"
  for name in flamenco opencue opentimelineio opencolorio openimageio openexr openvdb natron kitsu comfyui vapoursynth mlt meshroom alicevision colmap trellis2 wan2.1; do
    printf '%s=' "$name"
    git -C "$ROOT/$name" rev-parse HEAD
  done
} | tee "$ROOT/STACK-MANIFEST.txt"
