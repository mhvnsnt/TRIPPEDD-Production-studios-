#!/usr/bin/env bash
# Fetch the render/animation binaries this pipeline needs.
#
# Neither is in apt — `apt-get install blender` returns "Unable to locate
# package" on this image, and Rhubarb has no package at all. Both ship portable
# Linux builds that just run, so the answer is to fetch them rather than to
# report the toolchain as unavailable.
#
# Binaries are NOT repo content: they land in vendor/, which is gitignored.
# Everything that matters about them (version, role, the calls we make) is in
# the tools that use them.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p vendor

BLENDER_VER=4.2.1
RHUBARB_VER=1.13.0

if [ ! -x vendor/blender/blender ]; then
  echo "fetching Blender ${BLENDER_VER} (Cycles renderer, bpy scripting)..."
  curl -fsSL -o /tmp/blender.tar.xz \
    "https://download.blender.org/release/Blender${BLENDER_VER%.*}/blender-${BLENDER_VER}-linux-x64.tar.xz"
  tar xf /tmp/blender.tar.xz -C vendor
  ln -sfn "blender-${BLENDER_VER}-linux-x64" vendor/blender
  rm -f /tmp/blender.tar.xz
fi
vendor/blender/blender --version | head -1

if [ ! -x vendor/rhubarb/rhubarb ]; then
  echo "fetching Rhubarb Lip Sync ${RHUBARB_VER} (audio -> viseme timing)..."
  curl -fsSL -o /tmp/rhubarb.zip \
    "https://github.com/DanielSWolf/rhubarb-lip-sync/releases/download/v${RHUBARB_VER}/rhubarb-lip-sync-${RHUBARB_VER}-linux.zip"
  unzip -qo /tmp/rhubarb.zip -d vendor
  # NOTE the capitalisation: the archive extracts to Rhubarb-Lip-Sync-x.y.z-Linux,
  # not the lowercase name in the download URL. A lowercase glob finds nothing
  # and reads as a failed download.
  ln -sfn "Rhubarb-Lip-Sync-${RHUBARB_VER}-Linux" vendor/rhubarb
  rm -f /tmp/rhubarb.zip
fi
vendor/rhubarb/rhubarb --version | head -1

# MediaPipe needs libGLESv2, which is not in apt under any name on this image.
# Chromium ships one; borrow it rather than calling facial landmarking blocked.
if [ ! -e .trippedd_libs/libGLESv2.so.2 ]; then
  CHROME_GL=$(find "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}" -name libGLESv2.so 2>/dev/null | head -1)
  if [ -n "$CHROME_GL" ]; then
    mkdir -p .trippedd_libs
    ln -sf "$CHROME_GL" .trippedd_libs/libGLESv2.so.2
    ln -sf "$(dirname "$CHROME_GL")/libEGL.so" .trippedd_libs/libEGL.so.1
    echo "linked libGLESv2 from Chromium for MediaPipe"
  fi
fi

echo
echo "ready. Run facial landmarking with:"
echo "  LD_LIBRARY_PATH=\"\$PWD/.trippedd_libs:\$LD_LIBRARY_PATH\" .trippedd_venv/bin/python tools/character/measure_face.py --stage 2"
