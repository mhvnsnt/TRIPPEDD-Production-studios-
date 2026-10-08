#!/bin/bash
# spritesheet_packer/BUILD.sh — pack EP02 stills thumbnails into a sheet + atlas,
# then prove the atlas is pixel-exact.
set -euo pipefail
cd "$(dirname "$0")"
python3 packer.py
python3 verify_atlas.py
