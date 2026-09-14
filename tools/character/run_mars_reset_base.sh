#!/usr/bin/env bash
# Step 1 of production reset: clean GLB → variants/MARS_RESET_BASE.blend
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BLENDER="${TRIPPEDD_BLENDER_BIN:-$ROOT/vendor/blender/blender}"
if [[ ! -x "$BLENDER" ]]; then BLENDER="${TRIPPEDD_BLENDER_BIN:-blender}"; fi

GLB="${1:-$ROOT/assets/source_models/MARS_LOD2.glb}"
# Prefer LOD2 for daily work; full source is large
if [[ ! -s "$GLB" ]]; then
  GLB="$ROOT/assets/source_models/MARS_source.glb"
fi
OUT="${2:-$ROOT/assets/variants/MARS_RESET_BASE.blend}"

echo "GLB=$GLB"
echo "OUT=$OUT"
"$BLENDER" -b -P "$ROOT/tools/character/import_mars_reset_base.py" -- \
  --glb "$GLB" \
  --out "$OUT" \
  --report "$ROOT/docs/evidence/mars/reset/mars_reset_base_import.json"

echo "MARS_RESET_BASE: done (not promoted)"
echo "Next: GNM oral onto this base + linework + eyes — see PRODUCTION_RESET_FROM_ORIGINAL.md"
