#!/bin/bash
# run.sh — thin wrapper for checkpoint_render_driver.py (SPEC A-1).
# Usage: ./run.sh --blend scene.blend --output-dir frames/ --frame-start 1 --frame-end 81
#    or: ./run.sh --config my_render.json
# All arguments are passed straight through to the Python driver.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/checkpoint_render_driver.py" "$@"
