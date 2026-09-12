# TRIPPEDD Open-Source Expansion Roadmap

Status: ACTIVE ENGINEERING POLICY

The studio should prefer mature, inspectable open-source components over proprietary black boxes when they materially improve production capability. Integrations must be executable and verified; a name in a manifest is not an integration.

## Production layers

### 1. Source ingest and truth

- FFmpeg / FFprobe
- gdown for public Drive ingest
- SHA-256 source identity
- technical preflight
- physical source timeline
- immutable evidence records

### 2. Analysis

- PySceneDetect for shot boundaries
- OpenCV for frame sampling
- Tesseract for OCR
- faster-whisper wrapper for transcription
- shared checksum/version evidence cache
- comedy/continuity/subjectivity signal extraction

### 3. Editorial interchange

- OpenTimelineIO as canonical interchange
- Kdenlive/MLT project/export validation
- Story Runner and Autonomous as independent editorial lanes
- compare view against physical chronology

### 4. Generated media

- Blender for procedural 3D
- Natron for compositing where required
- OpenColorIO for deterministic color management
- generated-material provenance on every artifact
- resumable/checkpointed renders

### 5. Audio

- Ardour integration for multitrack/post workflows
- FFmpeg audio normalization and muxing
- loudness analysis and technical QC
- music/foley/SFX provenance

### 6. Asset interoperability

- OpenAssetIO manager abstraction
- filesystem-backed manager first
- asset manifests with repository/path/checksum/license/purpose
- explicit generated/source/editorial roles

### 7. Render orchestration

- local deterministic render runner first
- OpenCue adapter as optional distributed backend
- job dependencies, retries, artifacts, and render provenance

### 8. Programming

- program clock
- episodes
- cold opens
- bumps
- IDs
- fake commercials
- PSAs
- viewer cards
- promos
- tags
- shorts
- interstitials
- recurring micro-programs

### 9. Delivery

- master profile
- YouTube profile
- social profiles
- archive profile
- every deliverable independently ffprobe-validated
- master never overwritten by derivative generation

## Non-negotiable engineering rules

1. No fake AVAILABLE states.
2. No placeholder function that silently succeeds.
3. No TODO presented as production capability.
4. Every external tool has a real executable/library health check.
5. Every integration has at least one executable test or validation path.
6. Version changes invalidate the relevant evidence cache.
7. Generated material never masquerades as physical source truth.
8. Human editorial authority remains explicit.
9. Failed optional analysis is recorded rather than silently converted into evidence.
10. CI must exercise the same production interfaces that local execution uses whenever practical.

## Expansion order

Current priority is to harden the existing ingest/evidence/editorial/render path before adding complexity that cannot yet be exercised. After EP01 Autonomous is secured, expand audio provenance, technical preflight, frame-level QC, deterministic delivery, OpenAssetIO, OCIO, Kdenlive/MLT validation, Natron, and OpenCue in that order of practical value.

The objective is not to collect open-source names. The objective is a production pipeline in which each tool performs real work and leaves inspectable evidence behind.
