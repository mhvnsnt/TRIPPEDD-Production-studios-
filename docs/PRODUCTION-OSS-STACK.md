# TRIPPEDD Production studios — Open-Source Production Stack

This document is the production contract for open-source media tooling. The stack is not decorative: components listed here are verified before the short proof and are intended to remain part of the real episode path.

## Core path

| Component | Role | Production use |
|---|---|---|
| FFmpeg / ffprobe | Decode, encode, media probing | Source ingest, assembly, final render/QC |
| Blender | Deterministic 3D generation/render | Subjectivity, tags, graphics, future ident scenes |
| PySceneDetect | Shot/scene boundaries | Source analysis |
| OpenCV | Frame/image analysis | Visual observations and QC |
| faster-whisper | Speech transcription | Dialogue analysis and editorial evidence |
| OpenTimelineIO | Timeline interchange | Editorial/assembly contract |
| MediaInfo | Independent media metadata check | Final artifact QC cross-check |
| ExifTool | Metadata inspection | Source/artifact evidence |
| ImageMagick | Image generation/inspection | Graphic-card and raster validation |
| Tesseract | OCR | On-screen text evidence |
| rclone | Authenticated source transport | Drive/source recovery when credentials are available |

## Hardening rules

1. A required tool that cannot execute is `FAIL`, not `UNKNOWN` and never `PASS`.
2. A source cache is reusable only when the expected media count is present and files are non-empty.
3. Public Drive transport is never allowed to overwrite or invalidate a complete restored cache.
4. The real episode runner is blocked until the 10–20 second network ident passes end-to-end.
5. A successful prior render/checkpoint is preserved and reused rather than blindly rerun.
6. Concurrency is fail-safe: production runs do not cancel one another implicitly.
7. Final media must pass independent technical validation before it can be called a production artifact.
8. Telemetry must be measured from actual work; stale/missing heartbeats cannot be reported as active progress.

## Candidate integrations

OpenColorIO is the next color-management integration target for validating consistent scene/display transforms across generated and editorial material. OpenTelemetry Collector is the next observability integration target for durable run-correlated telemetry. Motion Canvas is a candidate vector/2D ident renderer; it should only enter the critical path after a real deterministic ident implementation proves it reduces complexity rather than adding dependency risk.

## Gate order

`SOURCE GATE → INGEST → ANALYSIS → EDITORIAL → RENDER → QC → ARTIFACT`

The network ident proof must exercise this same production contract before a real episode is permitted to run.
