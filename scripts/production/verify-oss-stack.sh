#!/usr/bin/env bash
set -euo pipefail

# OSS production stack verification. Keep this deterministic and fail closed:
# the episode runner must not claim the media stack is available unless each
# required open-source component actually imports/executes.

command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
command -v blender >/dev/null

python -m scenedetect --help >/dev/null
python - <<'PY'
import cv2
import faster_whisper
import opentimelineio as otio
print(f"OSS_STACK OpenCV={cv2.__version__}")
print("OSS_STACK faster-whisper=IMPORT_OK")
print(f"OSS_STACK OpenTimelineIO={otio.__version__}")
PY

ffmpeg -version | head -n 1
ffprobe -version | head -n 1
blender --version | head -n 1

echo 'OSS_STACK_STATUS=PASS'
