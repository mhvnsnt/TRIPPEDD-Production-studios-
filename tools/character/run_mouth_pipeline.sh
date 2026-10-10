#!/usr/bin/env bash
# THE MOUTH PIPELINE — one command, fail-closed, ends in published evidence.
#
# Safe to put on an agent's MCP allowlist: it takes no free-form arguments, it
# refuses to continue past a failed gate, and it cannot report success without
# frames and measurements on disk. Every stage prints what it MEASURED.
#
#   bash tools/character/run_mouth_pipeline.sh [--engine BLENDER_EEVEE_NEXT] [--samples 48]
#
# Stages, in the only order that works. Topology BEFORE bones BEFORE weights
# BEFORE shapes: a boolean evaluated after the armature cuts a hole wherever the
# cutter happens to be, which is how a mouth that never opened kept passing a
# hole-detection test for three passes.
set -euo pipefail
cd "$(dirname "$0")/../.."

ENGINE="BLENDER_EEVEE_NEXT"; SAMPLES="48"
while [ $# -gt 0 ]; do
  case "$1" in
    --engine) ENGINE="$2"; shift 2;;
    --samples) SAMPLES="$2"; shift 2;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done

BLENDER="vendor/blender/blender"
VENV="./.trippedd_venv/bin/python"
[ -x "$BLENDER" ] || { echo "Blender missing. Run tools/provision_render_tools.sh" >&2; exit 10; }

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

step "0/5  canonical Mars, by provenance and hash"
bash tools/character/fetch_mars_canonical.sh

step "1/5  measure the mouth on the real surface"
# MediaPipe's 478 landmarks raycast onto the scan. His mouth line is rolled 5.61
# degrees and his ears sit at -1.23 and +1.60 mouth widths; anatomy laid out on
# world axes lands visibly crooked in a head that is not.
"$BLENDER" -b -P tools/character/measure_mouth.py -- --lod LOD2 | grep -vE "^Fra:|INFO:"

step "2/5  carve the oral cavity out of the head"
# Not an object placed near the mouth -- a VOID, so it has no front surface that
# can protrude. Gated on: the cutter being a closed, outward-facing solid; the
# exterior outside the mouth zone being vertex-identical to the scan; and NO
# oral geometry ending up in front of the lip surface.
"$BLENDER" -b -P tools/character/oral_cavity.py -- --lod LOD2 | grep -vE "^Fra:|INFO:"

step "3/5  rig the face on the measured mandible boundary"
# Gated on the lips actually separating by more than 3% of head height.
"$BLENDER" -b -P tools/character/rig_face.py -- | grep -vE "^Fra:|INFO:"

step "4/5  prove it, in pixels and in numbers"
"$BLENDER" -b -P tools/character/mouth_proof.py -- --engine "$ENGINE" --samples "$SAMPLES" \
  | grep -vE "^Fra:|INFO:|^Saved:|^Time:"

step "5/5  publish, so every other agent can SEE it"
"$VENV" tools/character/contact_sheet.py --view front || true
"$VENV" tools/character/contact_sheet.py --view mouth || true
"$VENV" tools/character/contact_sheet.py --view profile || true
"$VENV" tools/publish_evidence.py --src renders/_mouth_proof --set mouth

VERIFIED=$("$VENV" -c "import json;print(json.load(open('renders/_mouth_proof/mouth_proof.json'))['verified'])")
echo
if [ "$VERIFIED" = "True" ]; then
  echo "MOUTH_ANATOMY_VERIFIED — evidence in docs/evidence/mouth/"
else
  echo "NOT VERIFIED — gate failures are listed in docs/evidence/mouth/README.md" >&2
  echo "Finding the geometry is not the same as the geometry being right." >&2
  exit 44
fi
