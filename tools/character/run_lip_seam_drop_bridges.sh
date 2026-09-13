#!/usr/bin/env bash
# Run the lip-seam split WITH --drop-bridges (the operation the pale shards need).
# Default: review-out only. Canonical is never the default write target.
#
# Usage:
#   tools/character/run_lip_seam_drop_bridges.sh [rig.blend]
#   tools/character/run_lip_seam_drop_bridges.sh path/to/rig.blend --measure-only
#
# Extra args after the optional blend path are passed through to split_lip_seam.py.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BLENDER="${TRIPPEDD_BLENDER_BIN:-${ROOT}/vendor/blender/blender}"
if [[ ! -x "$BLENDER" ]]; then
  BLENDER="${TRIPPEDD_BLENDER_BIN:-blender}"
fi

RIG="${1:-$ROOT/assets/rigs/MARS_FACE.blend}"
if [[ "${#}" -gt 0 && "$1" == -* ]]; then
  RIG="$ROOT/assets/rigs/MARS_FACE.blend"
  EXTRA=("$@")
else
  shift || true
  EXTRA=("$@")
fi

REVIEW="${TRIPPEDD_SEAM_REVIEW:-$ROOT/assets/variants/MARS_FACE_SEAM_DROP_BRIDGES_REVIEW.blend}"
REPORT="${TRIPPEDD_SEAM_REPORT:-$ROOT/docs/evidence/oral/lip_seam_drop_bridges.json}"
mkdir -p "$(dirname "$REVIEW")" "$(dirname "$REPORT")"

echo "RIG=$RIG"
echo "REVIEW_OUT=$REVIEW"
echo "REPORT=$REPORT"
echo "FLAG=--drop-bridges (default on in this runner)"

# --drop-bridges is the whole point of this runner. --review-out keeps canonical safe.
# Pass --measure-only via EXTRA to inspect without writing.
exec "$BLENDER" -b "$RIG" -P "$ROOT/tools/character/split_lip_seam.py" -- \
  --drop-bridges \
  --bridge-behind-mm "${BRIDGE_BEHIND_MM:-1.0}" \
  --review-out "$REVIEW" \
  --report "$REPORT" \
  "${EXTRA[@]}"
