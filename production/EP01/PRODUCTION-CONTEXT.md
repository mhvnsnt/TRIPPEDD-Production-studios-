# EP01 Production Context

This file is the durable production memory for future agents and production conversations. Read it before changing the EP01 pipeline.

## Current priority

Finish the real EP01 deliverable. Do not substitute status reports for artifacts.

## Canonical production direction

- Physical source footage is authoritative for what actually happened.
- OpenTimelineIO is the editorial interchange format.
- FFmpeg/ffprobe are deterministic media foundations.
- Technical QC is mandatory.
- VMAF/perceptual QC is reference-gated; never invent a reference or score.
- Human editorial lock and showrunner greenlight remain human-controlled.
- Generated material must be explicitly labeled as generated and carry provenance.
- Bannon / The Bastard terminal tag is **2D cinematic comic-book art** at this stage. Do not reintroduce the old 3D Bastard renderer unless explicitly directed.

## Reliability requirements

- Every expensive stage must have resumable checkpoints or immutable cache reuse.
- Long-running production steps must expose bounded timeouts and heartbeats where practical.
- Source analysis must not wait forever on one clip; bounded failure should let usable evidence continue.
- Failed workflow jobs get at most one automatic retry; repeated failures become a concrete blocker with run ID, step, timestamp, and root cause.
- Never claim an episode is finished until the actual MP4, OTIO, JSON/provenance, manifest, technical QC, and uploaded artifact exist and validate.
- Do not blindly rerun a deterministic failure.

## First-assembly performance policy

The first assembly is an evidence-driven rough cut. Full Whisper transcription is deferred when it is the bottleneck; visual/scene/OCR evidence can produce the initial source-driven assembly. Full transcription remains available as a later analysis stage.

The fast first-assembly runner serializes source analysis workers to avoid CPU oversubscription and bounds any individual source analysis at 20 minutes. This is a performance/reliability optimization, not a removal of evidence requirements.

## Open-source policy

Prefer real, maintained, interoperable open-source tools. Candidates are promoted only after license/version evidence, installation smoke, real input exercise, output validation, provenance/artifact identity, failure behavior, and resumability evidence.

Currently valuable OSS foundations include FFmpeg/ffprobe, MediaInfo, OpenCV, PySceneDetect, Tesseract, faster-whisper, OpenTimelineIO, OpenAssetIO, Blender, and the production QC/toolchain stack recorded in `config/studio-toolchain.json`.

## Autonomous production

The repository contains a bounded production self-healer and an autonomous OSS/pipeline co-builder specification. Autonomous changes must remain evidence-gated and must create focused PRs rather than speculative TODOs. The agent must not override human editorial decisions or secrets.

## Recent production fixes

- ImageMagick rasterizer portability preflight catches the previous 2D Bastard failure before expensive rendering.
- Subjectivity rendering is resumable and checkpointed.
- Blender exit codes are explicitly propagated.
- Artifact manifests hash the deliverable and generated dependencies.
- Workflow-level stale concurrency was removed from the Showrunner workflow.
- Fast first assembly now defers Whisper and bounds source analysis.
