#!/usr/bin/env bash
# Wave 64 Lane C — VAD-recall experiment.
# Torch-free (embeddings parsed raw float32 from the torch zip container,
# the Waves 59/60 trick). Re-run with ./run.sh.
set -euo pipefail
cd "$(dirname "$0")"

# httpx crash lesson (Waves 58/59): strip IPv6 literals from no_proxy
export no_proxy; no_proxy=$(printf '%s' "${no_proxy:-}" | tr ',' '\n' | grep -v '::' | paste -sd,)
export NO_PROXY="$no_proxy"

PY=./venv/bin/python
if [ ! -x "$PY" ]; then
  echo "venv missing: run ./install.sh first" >&2
  exit 1
fi

mkdir -p proofs/vad_recall
"$PY" wire_vad_recall_experiment.py
echo "Wave 64 Lane C VAD-recall experiment complete."
