#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEST="${ROOT}/third_party/visual_anatomy"
mkdir -p "${DEST}"

clone_or_update() {
  local name="$1"
  local url="$2"
  local dir="${DEST}/${name}"
  if [ -d "${dir}/.git" ]; then
    git -C "${dir}" fetch --tags --prune
    git -C "${dir}" pull --ff-only
  else
    git clone "${url}" "${dir}"
  fi
}

clone_or_update blender https://github.com/blender/blender.git
clone_or_update blender-addons https://github.com/blender/blender-addons.git
clone_or_update cvat https://github.com/cvat-ai/cvat.git
clone_or_update sam2 https://github.com/facebookresearch/sam2.git
clone_or_update Open3D https://github.com/isl-org/Open3D.git
clone_or_update meshlab https://github.com/cnr-isti-vclab/meshlab.git
clone_or_update cgal https://github.com/CGAL/cgal.git
clone_or_update instant-meshes https://github.com/wjakob/instant-meshes.git
clone_or_update OpenSubdiv https://github.com/PixarAnimationStudios/OpenSubdiv.git
clone_or_update nerfstudio https://github.com/nerfstudio-project/nerfstudio.git
clone_or_update gsplat https://github.com/nerfstudio-project/gsplat.git
clone_or_update modl https://github.com/modl-org/modl.git

echo "Open-source visual-anatomy toolchain available under third_party/visual_anatomy/"
echo "Pin revisions before production promotion; do not silently float dependencies."
