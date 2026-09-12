# TRIPPEDD Production Studios — Open-Source Production Stack

Status: `IMPLEMENTED / EXPANDING`

## Objective

TRIPPEDD is treated as a production system, not a demo UI. Every automated capability must be backed by a real executable, library, service, interchange format, generated artifact, or explicit human gate.

The studio uses open-source projects as infrastructure while keeping showrunner/editorial authority separate from machine inference.

## Stack

### Media foundation

- **FFmpeg / FFprobe** — deterministic decode, encode, muxing, filtering and technical verification.
- **OpenCV** — frame sampling and visual analysis.
- **PySceneDetect** — shot/scene boundary discovery.
- **Tesseract** — OCR for visible text and production evidence.
- **faster-whisper** — speech/transcript evidence.

### Editorial interchange

- **OpenTimelineIO** is the canonical machine-readable editorial interchange layer.
- OTIO describes editorial structure and references media; it is not a media container.
- Kdenlive 26.08 has native OTIO import/export for multi-track timelines and markers, so the studio does not depend on the deprecated adapter.

### Generation / finishing

- **Blender** — procedural 3D, animation, generated subjectivity, headless rendering.
- **Kdenlive / MLT** — human editorial authoring and alternate render backend.
- **Natron** — optional node-based compositing/VFX backend.
- **OpenColorIO** — optional studio color-management layer.

### Asset and render infrastructure

- **OpenAssetIO** — asset-centric interoperability boundary for production tools and asset management.
- **OpenCue** — optional distributed render-management layer for scaling generated/VFX jobs beyond one GitHub runner. The current OpenCue release line includes a Rust distributed scheduler and a feature-complete browser-based OpenCueWeb interface.

### Audio

- FFmpeg remains the deterministic audio processing baseline.
- Demucs is optional and explicitly treated as a capability, not a required dependency, because the original upstream repository is archived.

## Reality rules

1. A tool is never marked `AVAILABLE` unless its executable/library health check succeeds.
2. Optional tooling is allowed to be absent, but absence is explicit.
3. Generated material must carry provenance and cannot silently become physical-source evidence.
4. The physical source timeline remains authoritative for claims about what physically happened.
5. Technical QC does not equal showrunner greenlight.
6. Editorial locks remain human-controlled gates.

## Pipeline target

```text
SOURCE INGEST
    |
    v
TECHNICAL PREFLIGHT
    |
    +--> FFPROBE / HASH / CONTAINER CHECK
    |
    v
CHECKSUM-KEYED EVIDENCE CACHE
    |
    +--> SCENES ----+
    +--> FRAMES ----+
    +--> OCR -------+----> PHYSICAL SOURCE TIMELINE
    +--> TRANSCRIPT-+
    +--> AUDIO -----+
                      |
          +-----------+-----------+
          |                       |
          v                       v
   STORY RUNNER              AUTONOMOUS
   SHOWRUNNER CUT            CUT
          |                       |
          +-----------+-----------+
                      v
              OTIO COMPARISON
                      |
                      v
            EDITORIAL / VFX / AUDIO
              |      |       |
              v      v       v
           KDENLIVE BLENDER NATron
              \      |       /
               \     |      /
                v    v     v
                 FFmpeg
                    |
                    v
                 QC GATES
                    |
          +---------+---------+
          |                   |
     TECHNICAL QC       SHOWRUNNER LOCK
          |                   |
          +---------+---------+
                    v
              MASTER / MEZZANINE
                    |
                    v
             DELIVERY PROFILES
             /       |       \
         YOUTUBE   SOCIAL   ARCHIVE
```

## Current implementation gap list

The studio is deliberately moving from scaffolding to verified capabilities. The remaining items are tracked as engineering work rather than pretending they already exist:

- exact physical-event placement for generated sequences;
- parallel Story Runner and Autonomous jobs over the shared evidence cache;
- audio provenance and loudness QC;
- frame-level black/silence/title checks;
- render checkpoints and resumable generated segments;
- OpenCue submission adapter;
- OpenAssetIO manager integration;
- OCIO configuration/version pinning;
- Kdenlive/MLT project export and render validation;
- Natron project generation where compositing is actually needed;
- automated delivery packaging/verification implementation around the delivery profiles.

These are real TODOs, not fake `AVAILABLE` features.
