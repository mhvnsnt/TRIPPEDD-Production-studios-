#!/usr/bin/env bash
# Wave 65 Lane C — production diarization port. Re-run:
#   ./run.sh                 -> fixture baseline reproduction (DER/JER vs wave64)
#   ./run.sh --mode production -> real EP01 episode audio, blind run
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -x "$HERE/venv/bin/python" ] || { echo "run ./install.sh first"; exit 1; }
exec "$HERE/venv/bin/python" "$HERE/wire_diarize_production.py" "$@"
