#!/usr/bin/env bash
# Wave 66 Lane C — speaker-count tightening experiments.
# Re-run:
#   ./run.sh                       -> fixture + real EP01 audio, all experiments
#   ./run.sh --exp a|b|c           -> single experiment lane
#   ./run.sh --only fixture|production -> single audio target
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -x "$HERE/venv/bin/python" ] || { echo "run ./install.sh first"; exit 1; }
exec "$HERE/venv/bin/python" "$HERE/wire_count_tightening.py" "$@"
