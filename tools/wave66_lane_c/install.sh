#!/usr/bin/env bash
# Wave 66 Lane C — build the lane venv for speaker-count tightening.
#
# Disk discipline (disk was >80% at wave start): torch/torchaudio 2.14.1+cpu
# are REUSED READ-ONLY from the cipher lane venv via a .pth entry — no
# second 1.7 GB torch install. The cipher venv is never modified. Everything
# else is pinned to the Wave-64/65 proven numerical stack.
#
# Runs: ./install.sh   then   ./run.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ ! -x "$HERE/venv/bin/python" ]; then
  python3 -m venv --system-site-packages "$HERE/venv"
fi
V="$HERE/venv/bin/python"

# Torch: installed directly in this venv. (The original plan reused
# torch/torchaudio 2.14.1+cpu read-only from the cipher lane venv via .pth,
# but a VM/service restart on 2026-10-09 wiped that venv's site-packages
# entirely — donor gone, so we install our own. The cipher venv was NOT
# modified by this lane at any point.)
"$V" -m pip install --no-cache-dir \
  --index-url https://download.pytorch.org/whl/cpu \
  "torch==2.14.1+cpu" "torchaudio==2.11.0+cpu"

"$V" -m pip install --upgrade pip
# Real ECAPA torch environment (Wave-65 pins; torch itself comes from .pth).
"$V" -m pip install "speechbrain==1.1.1" "soundfile==0.14.0" "sentencepiece==0.2.2"
# Torch-free lane deps (already WIRED components).
"$V" -m pip install "webrtcvad==2.0.10" "spectralcluster==0.2.22" \
  "scikit-learn==1.9.1" "pyannote.metrics==4.1" "pyannote.core==6.0.1" \
  "sortedcontainers==2.4.0"
# Proven Wave-64 numerical stack LAST (system numpy is 2.5.3 here and the
# resolver upgrades numpy/scipy/pandas during the steps above; the wave64
# exact-repro baseline needs numpy 1.26.4 / scipy 1.11.4 — pin after).
"$V" -m pip install "numpy==1.26.4" "scipy==1.11.4" "pandas==2.1.4"
# faster-whisper 1.2.1 (MIT) is already in system site-packages; verify the
# venv sees it (do NOT pip-install a second copy).
"$V" -m pip freeze > "$HERE/venv-pins.txt"
mkdir -p ~/workspace/agent-ops/venv-manifests
cp "$HERE/venv-pins.txt" ~/workspace/agent-ops/venv-manifests/wave66-lane-c.txt
"$V" -c 'import torch, speechbrain, webrtcvad, spectralcluster, faster_whisper, numpy; print("OK torch", torch.__version__, "| numpy", numpy.__version__)'
echo "venv-pins.txt -> ~/workspace/agent-ops/venv-manifests/wave66-lane-c.txt"
