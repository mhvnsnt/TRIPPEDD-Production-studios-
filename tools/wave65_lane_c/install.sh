#!/usr/bin/env bash
# Wave 65 Lane C — build the single combined production venv:
# torch-free lane deps (webrtcvad, SpectralCluster, pyannote-metrics)
# PLUS the real ECAPA torch environment (torch CPU, torchaudio, speechbrain).
# Runs: ./install.sh   then  ./run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ ! -x "$HERE/venv/bin/python" ]; then
  python3 -m venv --system-site-packages "$HERE/venv"
fi
V="$HERE/venv/bin/python"
"$V" -m pip install --upgrade pip
# Real ECAPA torch environment (Wave-64 pins, still current).
"$V" -m pip install --index-url https://download.pytorch.org/whl/cpu \
  "torch==2.14.1+cpu" "torchaudio==2.11.0+cpu"
"$V" -m pip install "speechbrain==1.1.1" "soundfile==0.14.0" \
  "sentencepiece==0.2.2"
# Torch-free lane deps (already WIRED components).
"$V" -m pip install "webrtcvad==2.0.10" "spectralcluster==0.2.22" \
  "scikit-learn==1.9.1" "pyannote.metrics==4.1" "pyannote.core==6.0.1" \
  "sortedcontainers==2.4.0"
# Pin the proven Wave-64 numerical stack (numpy 1.x): pip's resolver pulls
# numpy 2.x here, which breaks the system matplotlib that pyannote.core
# imports (and differs from the wave64 recipe). Advisory-only metadata
# conflicts with pyannote-metrics 4.1 (wants pandas>=2.2.3/scipy>=1.15.1)
# are non-blocking — wave64 ran the same combination via system-site-packages.
"$V" -m pip install "numpy==1.26.4" "scipy==1.11.4" "pandas==2.1.4"
"$V" -m pip freeze > "$HERE/venv-pins.txt"
mkdir -p ~/workspace/agent-ops/venv-manifests
cp "$HERE/venv-pins.txt" ~/workspace/agent-ops/venv-manifests/wave65-lane-c.txt
"$V" -c 'import torch, speechbrain, webrtcvad, spectralcluster; print("OK torch", torch.__version__)'
