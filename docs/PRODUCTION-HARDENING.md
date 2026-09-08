# TRIPPEDD production hardening

## Rules

1. Never push to an active production-render branch.
2. Never cancel a useful render to deploy a speculative fix.
3. Expensive generated media is content-addressed and resumable.
4. Blender API compatibility is preflighted before rendering.
5. Generated media remains explicitly non-physical provenance.
6. Final MP4 is not considered complete until FFprobe/MediaInfo QC and artifact upload succeed.

## Open-source stack

- Blender 4.5 LTS for procedural 3D.
- FFmpeg/FFprobe for deterministic media operations and QC.
- OpenImageIO for image inspection/conversion acceleration.
- OpenTimelineIO for editorial interchange.
- OpenColorIO for color-management interchange.
- OpenAssetIO for asset identity/interchange.
- PySceneDetect/OpenCV for shot and visual analysis.
- faster-whisper for transcription.
- Tesseract for OCR.
- Demucs for optional audio separation.
- Natron/MLT/Kdenlive as optional editorial/compositing backends.
- Flamenco/OpenCue as optional distributed rendering infrastructure.

Optional components stay feature-gated: their absence must never break the baseline FFmpeg/Blender production path.

## Current Blender failure class

Blender 4.5 exposes light power/energy on the Light data-block. The production preflight in `scripts/verify-blender-production-api.py` inserts and verifies an `energy` F-curve on `bpy.types.Light` before a render is allowed to proceed.
