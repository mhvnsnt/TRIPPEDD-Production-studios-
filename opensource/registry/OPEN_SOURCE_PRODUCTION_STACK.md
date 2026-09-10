# TRIPPEDD Open-Source Production Stack

Status: integration registry / do not blindly vendor entire upstream repositories.

## Core production
- Blender — 3D authoring, animation, simulation, rendering
- Blender Studio Pipeline — production conventions, Kitsu integration, review
- Flamenco — distributed Blender rendering
- OpenCue — high-scale render scheduling
- OpenUSD — scene interchange/composition
- OpenColorIO — color management
- OpenImageIO — image I/O
- OpenEXR — HDR frame interchange
- OpenSubdiv — subdivision surfaces
- OpenVDB — volumetric data
- OpenShadingLanguage — programmable shading
- OpenTimelineIO — editorial interchange

## Compositing / finishing
- Natron — node compositing/VFX
- Kdenlive — non-linear editing
- MLT — media framework
- FFmpeg — media encode/decode/filter
- GStreamer — media pipelines
- VapourSynth — programmable video processing
- Frei0r — video effects API
- OpenFX — plugin interoperability

## Analysis / editorial intelligence
- FFprobe — technical media inspection
- PySceneDetect — shot detection
- faster-whisper — local transcription
- Tesseract OCR — text extraction
- OpenCV — computer vision
- MediaInfo — media metadata
- ExifTool — metadata/provenance

## AI-assisted visual generation
- ComfyUI — node-based image/video generation orchestration
- AUTOMATIC1111 Stable Diffusion WebUI — image generation workflows
- InvokeAI — controlled image generation
- Krita + AI diffusion integrations — artist-directed image workflows
- Stable Video Diffusion ecosystem — research/experimental video generation

## Audio
- Ardour — DAW
- Audacity — waveform editing
- Carla — plugin host/routing
- FluidSynth — MIDI/software synthesis
- SoX — audio processing
- Rubber Band — time/pitch processing
- Whisper/faster-whisper — dialogue transcription
- Piper — local neural TTS
- XTTS ecosystem — voice synthesis where licensing/consent permits

## Collaboration / production tracking
- Kitsu — production tracking/review
- OpenProject — project/task management
- MinIO — S3-compatible object storage
- Syncthing — peer-to-peer asset synchronization
- PostgreSQL — production metadata
- Redis — queues/cache
- NATS — event bus
- Temporal — durable workflow orchestration
- Prefect — workflow orchestration

## Studio integration rule

Upstream projects remain independently identifiable and replaceable. TRIPPEDD integrates them through adapters/contracts instead of forking their internals unnecessarily.

Every integration must expose:
- capability
- inputs/outputs
- health check
- provenance
- resource requirements
- checkpoint/retry behavior
- artifact ownership
- license metadata

Do not start the next expensive media run until the integration layer and QC gates are healthy.
