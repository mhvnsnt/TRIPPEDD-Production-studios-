#!/usr/bin/env bash
# Fetch the persistent-session addon. Upstream, not hand-rolled (OWNER LAW #3).
#
#   ahujasid/blender-mcp -- MIT. A socket server that lives INSIDE Blender and
#   executes commands on the main thread through bpy.app.timers.
#
# It refuses background mode and says so itself:
#   "cannot start server in background mode (blender -b) - commands would never
#    execute. Run Blender with a GUI, or use a virtual display: xvfb-run -a blender"
# Xvfb is installed in this container, so that is exactly what tools/session/start.sh does.
set -euo pipefail
cd "$(dirname "$0")/../.."
mkdir -p vendor
if [ ! -f vendor/blender-mcp/src/blender_mcp/bundled/addon.py ]; then
  echo "fetching ahujasid/blender-mcp (MIT) ..."
  rm -rf vendor/blender-mcp
  git clone --depth 1 -q https://github.com/ahujasid/blender-mcp vendor/blender-mcp
fi
test -f vendor/blender-mcp/src/blender_mcp/bundled/addon.py
echo "session addon: $(wc -l < vendor/blender-mcp/src/blender_mcp/bundled/addon.py) lines, $(head -3 vendor/blender-mcp/LICENSE | tail -1 | cut -c1-40)"
command -v Xvfb >/dev/null || { echo "Xvfb missing -- the session needs a virtual display" >&2; exit 1; }
echo "SESSION_TOOLCHAIN_OK"
