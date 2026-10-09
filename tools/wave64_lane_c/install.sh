#!/usr/bin/env bash
# Wave 64 Lane C — VAD-recall experiment (torch-free lane).
#   python3 -m venv --system-site-packages tools/wave64_lane_c/venv
#   ./install.sh   (once)
#   ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

# httpx crash lesson (Waves 58/59): strip IPv6 literals from no_proxy
export no_proxy; no_proxy=$(printf '%s' "${no_proxy:-}" | tr ',' '\n' | grep -v '::' | paste -sd,)
export NO_PROXY="$no_proxy"

PY=./venv/bin/python
if [ ! -x "$PY" ]; then
  echo "venv missing: python3 -m venv --system-site-packages venv first" >&2
  exit 1
fi
"$PY" -m pip install --no-cache-dir -U pip
"$PY" -m pip install --no-cache-dir webrtcvad spectralcluster scikit-learn
"$PY" -m pip install --no-cache-dir --no-deps "pyannote.metrics==4.1" \
  pyannote.core sortedcontainers
"$PY" -m pip freeze | sort | tee venv-pins.txt
echo "install.sh done."
