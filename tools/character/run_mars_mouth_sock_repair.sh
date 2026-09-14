#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BLENDER="${TRIPPEDD_BLENDER_BIN:-${ROOT}/vendor/blender/blender}"
IN_BLEND="${1:-${ROOT}/assets/rigs/MARS_FACE.blend}"
OUT_BLEND="${2:-${ROOT}/assets/variants/MARS_MOUTH_SOCK_SURGICAL_CANDIDATE.blend}"
OUT_DIR="${TRIPPEDD_MOUTH_SOCK_OUT:-${ROOT}/.artifacts/mars-mouth-sock-repair}"
REPORT="$OUT_DIR/mouth_sock_surgical.json"
PIXEL_DIR="$OUT_DIR/pixel_truth"

mkdir -p "$OUT_DIR"

# First produce the measured face/ray evidence. This must identify the sock
# before geometry is allowed to change.
"$BLENDER" -b "$IN_BLEND" --python "$ROOT/tools/character/repair_mars_mouth_sock.py" -- \
  --report-only --report "$REPORT"

# Apply exactly the faces identified by that measured pass.
"$BLENDER" -b "$IN_BLEND" --python "$ROOT/tools/character/repair_mars_mouth_sock.py" -- \
  --apply --report "$REPORT" --out "$OUT_BLEND"

# Actual open-mouth pixel truth. This is deliberately downstream of the
# surgical edit; ray evidence alone cannot establish visual success.
"$BLENDER" -b "$OUT_BLEND" --python "$ROOT/tools/character/render_mars_oral_pixel_truth.py" -- \
  --output-dir "$PIXEL_DIR" --pose open

if ! grep -q '"status": "PASS"' "$PIXEL_DIR/mars_oral_pixel_truth.json" 2>/dev/null; then
  echo "MARS_MOUTH_SOCK_REPAIR: PIXEL_TRUTH_FAIL"
  exit 1
fi

if [[ ! -s "$PIXEL_DIR/mars_oral_pixel_truth.png" ]]; then
  echo "MARS_MOUTH_SOCK_REPAIR: IMAGE_UNAVAILABLE"
  exit 1
fi

SHA256="$(sha256sum "$PIXEL_DIR/mars_oral_pixel_truth.png" | awk '{print $1}')"
printf '%s\n' "$SHA256" > "$PIXEL_DIR/mars_oral_pixel_truth.sha256"

# Reopen the exact candidate and verify that the artifact exists. Promotion is
# intentionally left to the existing mouth-proof/receipt chain.
REOPEN="$OUT_DIR/reopen.txt"
"$BLENDER" -b "$OUT_BLEND" --python-expr \
  "import bpy; print('REOPEN_OK', bpy.data.filepath)" 2>&1 | tee "$REOPEN"
if ! grep -q 'REOPEN_OK' "$REOPEN"; then
  echo "MARS_MOUTH_SOCK_REPAIR: REOPEN_FAIL"
  exit 1
fi

echo "MARS_MOUTH_SOCK_REPAIR: PIXEL_PASS"
echo "CANDIDATE=$OUT_BLEND"
echo "PIXEL_TRUTH=$PIXEL_DIR/mars_oral_pixel_truth.png"
echo "PIXEL_SHA256=$SHA256"
echo "PROMOTION=NOT_PERFORMED"
