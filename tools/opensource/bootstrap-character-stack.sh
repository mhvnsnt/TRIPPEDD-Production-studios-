#!/usr/bin/env bash
set -euo pipefail

# Full-source checkout for the character/animation vertical slice.
# This is intentionally separate from model weights and build artifacts.
# Source checkout != validated installation; promotion still requires a real
# Mars input smoke test and measured output.

ROOT="${TRIPPEDD_OSS_ROOT:-third_party/opensource}"
mkdir -p "$ROOT"

clone_or_update() {
  local name="$1" url="$2"
  local dest="$ROOT/$name"
  if [[ -d "$dest/.git" ]]; then
    git -C "$dest" fetch --tags --prune
    git -C "$dest" pull --ff-only || true
  else
    git clone --filter=blob:none "$url" "$dest"
  fi
}

clone_or_update blender https://github.com/blender/blender.git
clone_or_update assimp https://github.com/assimp/assimp.git
clone_or_update trimesh https://github.com/mikedh/trimesh.git
clone_or_update Open3D https://github.com/isl-org/Open3D.git
clone_or_update PyMeshLab https://github.com/cnr-isti-vclab/PyMeshLab.git
clone_or_update MediaPipe https://github.com/google-ai-edge/mediapipe.git
clone_or_update OpenSeeFace https://github.com/emilianavt/OpenSeeFace.git
clone_or_update rhubarb-lip-sync https://github.com/DanielSWolf/rhubarb-lip-sync.git
clone_or_update OpenFaceFX https://github.com/Emilianavt/OpenFaceFX.git
clone_or_update PantoMatrix https://github.com/PantoMatrix/PantoMatrix.git
clone_or_update BlendCap https://github.com/jasperges/BlendCap.git
clone_or_update moface https://github.com/cgtinker/moface.git
clone_or_update OpenToonz https://github.com/opentoonz/opentoonz.git
clone_or_update synfig https://github.com/synfig/synfig.git
clone_or_update Natron https://github.com/NatronGitHub/Natron.git
clone_or_update ComfyUI https://github.com/comfyanonymous/ComfyUI.git
clone_or_update Wan2.2 https://github.com/Wan-Video/Wan2.2.git
clone_or_update LTX-Video https://github.com/Lightricks/LTX-Video.git
clone_or_update faster-whisper https://github.com/SYSTRAN/faster-whisper.git
clone_or_update demucs https://github.com/facebookresearch/demucs.git
clone_or_update OpenUSD https://github.com/PixarAnimationStudios/OpenUSD.git

printf '%s\n' "Character OSS source checkout complete: $ROOT"
