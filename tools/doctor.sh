#!/usr/bin/env bash
# TWO SECONDS, NOT A TURN.
#
# Blender lives behind a symlink into a scratch directory, so a routine cleanup
# can delete the whole toolchain and the next command fails with
# "No such file or directory" a minute into a render. That cost a session turn.
# The disk filling does the same thing and reports itself as "Page crashed".
# Both are one check each.
#
#   bash tools/doctor.sh          # report
#   bash tools/doctor.sh --fix    # and repair what can be repaired
set -uo pipefail
cd "$(dirname "$0")/.."
FIX=0; [ "${1:-}" = "--fix" ] && FIX=1
BAD=0
say() { printf '%-34s %s\n' "$1" "$2"; }

AVAIL=$(df -BM --output=avail / | tail -1 | tr -dc '0-9')
if [ "$AVAIL" -lt 2000 ]; then
  say "disk free" "${AVAIL}M  LOW -- Blender and pip both fail here, and Chromium reports it as a page crash"
  BAD=1
else
  say "disk free" "${AVAIL}M"
fi

if [ -x vendor/blender/blender ]; then
  say "blender" "$(vendor/blender/blender --version 2>/dev/null | head -1)"
else
  say "blender" "MISSING (vendor/blender -> $(readlink vendor/blender 2>/dev/null || echo 'no link'))"
  BAD=1
  if [ "$FIX" = 1 ]; then
    echo "  fixing: bash tools/provision_render_tools.sh"
    bash tools/provision_render_tools.sh >/dev/null 2>&1 \
      && say "blender" "restored: $(vendor/blender/blender --version | head -1)"
  fi
fi

[ -x vendor/rhubarb/rhubarb ] && say "rhubarb" "present" || say "rhubarb" "MISSING (viseme timing only)"

PY=./.trippedd_venv/bin/python
if [ -x "$PY" ]; then
  "$PY" - <<'PYEOF'
import importlib, sys
need = {"numpy": "arrays", "scipy": "TPS warp", "igl": "winding numbers / signed distance",
        "trimesh": "mesh io", "pycpd": "non-rigid fit", "PIL": "pixel counting",
        "pymeshlab": "REMESHING + repair (mouth/eye topology)", "mediapipe": "landmarks"}
for m, why in need.items():
    try:
        importlib.import_module(m); print("%-34s ok   (%s)" % ("py:" + m, why))
    except Exception:
        print("%-34s MISSING  (%s)" % ("py:" + m, why))
PYEOF
else
  say "venv" "MISSING .trippedd_venv"; BAD=1
fi

for p in vendor/ict/ict_facs.npz assets/donor/gnm_oral/mouth_sock.npz \
         renders/_rig_measure/mouth_anatomy.json assets/rigs/MARS_FACE.blend; do
  [ -e "$p" ] && say "$(basename "$p")" "present" || { say "$(basename "$p")" "MISSING"; BAD=1; }
done

if ./.trippedd_venv/bin/python tools/session/client.py ping >/dev/null 2>&1; then
  say "blender session" "LIVE on ${TRIPPEDD_SESSION_PORT:-9876} -- use it, do not launch Blender"
else
  say "blender session" "not running (bash tools/session/start.sh <blend>)"
fi

echo
[ "$BAD" = 0 ] && echo "TOOLCHAIN OK" || echo "TOOLCHAIN INCOMPLETE -- rerun with --fix, or read the lines above"
exit 0
