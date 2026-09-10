#!/usr/bin/env bash
set -euo pipefail

# Production stack verification. Every component used as a production
dependency must be executable/importable before a run is allowed to proceed.
# Missing telemetry or a missing tool is a hard failure, never a soft PASS.
# Open-source versions are checked at the gate so a successful run is
# reproducible against the intended production stack, not merely importable.

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "OSS_STACK_FAIL missing-command=$1"
    exit 2
  }
}

require_cmd ffmpeg
require_cmd ffprobe
require_cmd blender
require_cmd mediainfo
require_cmd exiftool
require_cmd identify
require_cmd tesseract
require_cmd rclone

python -m scenedetect --help >/dev/null 2>&1 || {
  echo 'OSS_STACK_FAIL PySceneDetect execution failed'
  exit 2
}

python - <<'PY'
from packaging.version import Version
import cv2
import faster_whisper
import opentimelineio as otio

minimum_faster_whisper = Version("1.2.1")
installed_faster_whisper = Version(faster_whisper.__version__)
if installed_faster_whisper < minimum_faster_whisper:
    raise SystemExit(
        f"OSS_STACK_FAIL faster-whisper={installed_faster_whisper} "
        f"requires>={minimum_faster_whisper}"
    )

print(f"OSS_STACK OpenCV={cv2.__version__}")
print(f"OSS_STACK faster-whisper={installed_faster_whisper}")
print(f"OSS_STACK OpenTimelineIO={otio.__version__}")
PY

ffmpeg -version | head -n 1
ffprobe -version | head -n 1
blender --version | head -n 1
mediainfo --Version | head -n 1
exiftool -ver
identify -version | head -n 1
tesseract --version | head -n 1
rclone version | head -n 1

echo 'OSS_STACK_STATUS=PASS'
