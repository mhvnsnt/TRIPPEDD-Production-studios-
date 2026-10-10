#!/usr/bin/env bash
# Wave 63 Lane C — VAD-coverage recovery on the Wave-62 rebuilt topology.
# Torch-free (embeddings parsed raw float32 from the torch zip container).
#
#   python3 -m venv --system-site-packages tools/wave63_lane_c/venv
#   (install the pip list in PROOFS.md once, then:)
#   ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

# httpx crash lesson (Waves 58/59): strip IPv6 literals from no_proxy
export no_proxy; no_proxy=$(printf '%s' "${no_proxy:-}" | tr ',' '\n' | grep -v '::' | paste -sd,)
export NO_PROXY="$no_proxy"

PY=./venv/bin/python
if [ ! -x "$PY" ]; then
  echo "venv missing: run the install recipe from PROOFS.md first" >&2
  exit 1
fi

mkdir -p proofs/coverage
"$PY" wire_vad_coverage_recovery.py
echo "Wave 63 Lane C VAD-coverage recovery complete."
