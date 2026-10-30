#!/usr/bin/env bash
# Install the pinned Ucupaint release into the studio's wired Blender 4.5.3
# as a Blender extension (user_default repo). Idempotent.
#
# Pinned donor (SPEC S-1, DONOR FIRST):
#   Ucupaint 3.0.0 by Yusuf Umar (ucupumar) - GPL-3.0-or-later
#   Source: https://github.com/ucupumar/ucupaint (release tag 3.0.0)
#   Asset:  ucupaint-3.0.0.zip
#   SHA-256 of the asset as downloaded 2026-10-30 is verified below; the
#   install aborts on any mismatch. The zip is NOT committed to this repo:
#   this script fetches the pinned release from the official GitHub repo.
set -euo pipefail

UCUPAINT_VERSION="3.0.0"
UCUPAINT_ZIP="ucupaint-${UCUPAINT_VERSION}.zip"
UCUPAINT_SHA256="71ab7eb4948fc4896b11eebf97dae78755cceacd2e72a3de29bb22908593f21d"
BLENDER="${BLENDER_453:-$HOME/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender}"
CACHE_DIR="$HOME/workspace/tools/ucupaint"

if [ ! -x "$BLENDER" ]; then
  echo "ERROR: Blender 4.5.3 not found at $BLENDER (set BLENDER_453)" >&2
  exit 1
fi

mkdir -p "$CACHE_DIR"
cd "$CACHE_DIR"

if [ ! -f "$UCUPAINT_ZIP" ]; then
  if command -v gh >/dev/null 2>&1; then
    gh release download "$UCUPAINT_VERSION" --repo ucupumar/ucupaint \
      --pattern "$UCUPAINT_ZIP" --clobber
  else
    curl -fL -o "$UCUPAINT_ZIP" \
      "https://github.com/ucupumar/ucupaint/releases/download/${UCUPAINT_VERSION}/${UCUPAINT_ZIP}"
  fi
fi

echo "${UCUPAINT_SHA256}  ${UCUPAINT_ZIP}" | sha256sum -c -

# Blender's own extension CLI: installs into
# ~/.config/blender/4.5/extensions/user_default/ucupaint and enables it.
xvfb-run -a env -u PYTHONPATH "$BLENDER" --command extension install-file \
  -r user_default -e "$CACHE_DIR/$UCUPAINT_ZIP"

echo "Ucupaint ${UCUPAINT_VERSION} installed for Blender 4.5.3."
echo "Verify: $BLENDER -b --python-expr \"import addon_utils; print(addon_utils.check('bl_ext.user_default.ucupaint'))\""
