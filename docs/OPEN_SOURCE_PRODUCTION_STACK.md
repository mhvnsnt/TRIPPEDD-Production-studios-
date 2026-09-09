# Open-Source Production Stack

This document records OSS components that are candidates for the self-hosted TRIPPEDD production platform.

## Promotion rule

A component is **not production-ready** because it is listed here or because an executable exists. Promotion requires:

1. license/version evidence;
2. installation or service startup;
3. a real input;
4. a real output or library exercise;
5. output validation;
6. provenance and artifact identity;
7. failure behavior;
8. resumability where applicable;
9. CI evidence.

Optional components may remain unavailable on a minimal deployment. A missing optional dependency is explicit and does not become a fake AVAILABLE state.

## Capability families

### Asset and production management

- Kitsu / Zou / Gazu — production tracking and API automation.
- AYON — studio pipeline and application integration.
- OpenAssetIO — asset-resolution and interchange abstraction.
- QuadPype — open-source studio pipeline candidate.
- Avalon — open-source animation/VFX pipeline candidate.
- Stalker — production asset-management library candidate.
- OpenPipeline — pipeline conventions and workflow candidate.

### Media and analysis

- FFmpeg / FFprobe — deterministic media foundation.
- GStreamer — media-graph execution.
- OpenCV — image/video analysis.
- PySceneDetect — shot-boundary analysis.
- Faster-Whisper — transcription.
- Silero VAD / pyannote.audio — speech/activity analysis.
- Tesseract — OCR.
- CVAT — annotation and computer-vision dataset workflows.
- FiftyOne — dataset inspection and model-analysis workflows.

### Scene, image, color and simulation

- OpenUSD — scene description and composition.
- MaterialX — material interchange.
- Open Shading Language — programmable shading.
- OpenVDB — volumetric data.
- OpenImageIO / OpenEXR — image and HDR interchange.
- OpenColorIO — color management.
- VapourSynth / zimg — deterministic video processing.
- OpenFX / frei0r — effects/plugin interchange.

### Editorial and compositing

- OpenTimelineIO — editorial interchange.
- MLT / Kdenlive — editorial/render pipeline candidates.
- Natron — node-based compositing candidate.

### Rendering and execution

- Blender — procedural 3D/rendering.
- Flamenco — Blender-oriented distributed rendering.
- OpenCue — general production render management.
- GitHub/self-hosted workers — baseline execution backend.

### QC and review

- MediaConch — policy/conformance validation.
- QCTools — audiovisual quality analysis.
- FFprobe / MediaInfo — technical inspection.
- OpenRV / xSTUDIO — review/playback candidates.

### Audio post

- SoX — deterministic command-line audio processing.
- Rubber Band — time/pitch processing.
- Demucs — source separation candidate.
- Audacity / Ardour / PipeWire/JACK ecosystem — interactive and routing candidates.

### Storage and workflow infrastructure

- MinIO / S3-compatible object storage — content-addressed artifact store candidate.
- Dagster — asset-aware orchestration candidate.
- Temporal — durable workflow execution candidate.
- Airflow — scheduled DAG candidate.
- OpenTelemetry — portable telemetry.
- Prometheus — metrics.
- Grafana — dashboards.
- Loki — structured log storage.
- Tempo — trace storage.

## Architecture rule

The deterministic path remains available even when optional OSS components are absent:

`physical source -> evidence graph -> analysis -> OTIO/OpenUSD -> deterministic media/render -> QC -> review -> approved master`

Optional components improve a capability; they do not silently replace the deterministic fallback until their integration gate passes.
