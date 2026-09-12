#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."

PY=.trippedd_venv/bin/python
if [ ! -x "$PY" ]; then
  PY=python3
fi

echo "Installing pinned open-source face landmark authority..."
"$PY" -m pip install --disable-pip-version-check --upgrade "mvmp==1.4.2" "trimesh>=4.0,<5"

"$PY" - <<'PY'
import mvmp
print("MVMP import OK:", getattr(mvmp, "__version__", "1.4.2"))
PY

echo "Face authority runtime ready."
echo "Run:"
echo "  $PY tools/character/measure_face_mvmp.py --debug renders/_rig_measure/mvmp_debug"
