#!/bin/bash
# install_gizmos.sh — install the TRIPPEDD Natron gizmo pack (PyPlugs).
# Usage:
#   install_gizmos.sh [PYPLUGS_DIR]
# Default PYPLUGS_DIR is this box's wired Natron 2.5.0 install.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${1:-$HOME/workspace/tools/natron/Natron-2.5.0-Linux-x86_64-no-installer/Plugins/PyPlugs}"
if [ ! -d "$DEST" ]; then
  echo "PyPlugs dir not found: $DEST" >&2
  echo "Pass the target Natron Plugins/PyPlugs directory as arg 1." >&2
  exit 1
fi
for f in "$HERE"/CJLook1PaleWash.py "$HERE"/CJLook2DeepSaturation.py \
         "$HERE"/CJLedDeepPurpleGlow.py "$HERE"/CJLedPartyGlow.py \
         "$HERE"/TrippeddCard25D.py; do
  cp -v "$f" "$DEST/"
done
# Community donor (SPEC N-1): PM_Card3D + PM_Camera live in subfolders
# (each plugin imports its *Ext.py companion from its own folder).
KIT="$(dirname "$HERE")"
for plug in PM_Card3D PM_Camera; do
  mkdir -p "$DEST/$plug"
  cp -v "$KIT/card-kit/community-donor/$plug/"*.py "$KIT/card-kit/community-donor/$plug/"*.png "$DEST/$plug/"
done
echo "Installed. Restart Natron / re-run NatronRenderer — PyPlugs load at startup."
