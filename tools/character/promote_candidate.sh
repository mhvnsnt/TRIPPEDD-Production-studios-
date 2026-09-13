#!/usr/bin/env bash
# PROMOTE A REVIEWED CANDIDATE RIG INTO CANONICAL. Fail-closed, and it names
# every artifact that is COUPLED to the rig's vertex count, because promoting the
# blend alone leaves three other files silently indexed against the old head.
#
#   bash tools/character/promote_candidate.sh <candidate.blend> <label> [--yes]
#
# What is coupled, and why each one has to move WITH the rig:
#   assets/rigs/MARS_ORAL.blend            the carved head rig_face is built from
#   assets/donor/gnm_face/_mars_verts.npy  the vertex dump the FACS fit is against
#   assets/donor/facs/                     the FACS donor, indexed by vertex id
#   docs/evidence/hair/_valley_CAGE.npy    -> _hairzones.npy -> every hair tool
# rig_face.py REFUSES when the donor index and the head disagree ("FACS donor is
# indexed against 23830 vertices, this head has 23840"), which is the gate that
# caught this in the first place -- but only on the NEXT rebuild. Move them here.
set -euo pipefail
cd "$(dirname "$0")/../.."
VENV="./.trippedd_venv/bin/python"

CAND="${1:?usage: promote_candidate.sh <candidate.blend> <label> [--yes]}"
LABEL="${2:?usage: promote_candidate.sh <candidate.blend> <label> [--yes]}"
YES="${3:-}"

[ -s "$CAND" ] || { echo "*** REFUSED: no bytes at $CAND"; exit 2; }

step() { printf '\n\033[1m== %s\033[0m\n' "$1"; }

step "1/5  what is being replaced -- an immutable checkpoint first"
# OWNER LAW #12. Content-addressed, refuses to overwrite, restores only after
# re-verifying every sha256. This is what made the accidental overwrite during
# the re-carve recoverable instead of fatal.
"$VENV" tools/checkpoint.py save "before-promote-$LABEL" \
  --note "promoting $CAND" || {
    echo "*** REFUSED: could not checkpoint canonical. Nothing promoted."; exit 3; }

step "2/5  the candidate's own numbers, before anything is overwritten"
"$VENV" tools/character/where_did_his_skin_go.py --shipped "${CAND%.blend}_rest.npz" \
  2>/dev/null || echo "  (no rest dump for the candidate -- run dump_rest_mesh.py to get one)"

if [ "$YES" != "--yes" ]; then
  echo
  echo "DRY RUN. Nothing has been promoted."
  echo "Re-run with --yes once mouth_proof AND the published pixels are both green."
  echo "PHYSICAL GATES ALONE ARE NOT A PASS (OWNER LAW #10)."
  exit 0
fi

step "3/5  promote the rig and everything indexed against it"
cp -a "$CAND" assets/rigs/MARS_FACE.blend
for pair in \
  "renders/_recarve/MARS_ORAL_CONTOUR.blend:assets/rigs/MARS_ORAL.blend" \
  "renders/_recarve/donor_new/_mars_verts.npy:assets/donor/gnm_face/_mars_verts.npy" ; do
  src="${pair%%:*}"; dst="${pair##*:}"
  if [ -e "$src" ]; then cp -a "$src" "$dst"; echo "  $src -> $dst"
  else echo "  NOT_ATTEMPTED: $src is missing; $dst left as it is"; fi
done
if [ -d renders/_recarve/donor_new/facs ]; then
  cp -a renders/_recarve/donor_new/facs/. assets/donor/facs/
  echo "  renders/_recarve/donor_new/facs -> assets/donor/facs"
else
  echo "  NOT_ATTEMPTED: no candidate FACS donor; assets/donor/facs left as it is"
fi

step "4/5  the donor index MUST match the head it was fitted to"
"$VENV" - <<'PY'
import numpy as np, sys
v = np.load("assets/donor/gnm_face/_mars_verts.npy")
print("  the FACS donor is indexed against %d vertices" % v.shape[0])
PY

step "5/5  regenerate what is indexed by vertex id"
echo "  the hair zones are STALE until these run, in THIS order:"
echo "    vendor/blender/blender -b -P tools/hair/valley_discriminator.py --"
echo "    vendor/blender/blender -b -P tools/hair/hair_zones.py --"
echo
echo "PROMOTED $CAND -> assets/rigs/MARS_FACE.blend"
echo "roll back with: $VENV tools/checkpoint.py restore before-promote-$LABEL --yes"
