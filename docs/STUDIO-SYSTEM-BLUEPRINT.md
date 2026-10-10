# TRIPPEDD Studio System Blueprint

The repository is intentionally a **production control system**, not a dump of third-party source. Large production tools belong in reproducible environments, containers, caches, or external services; the repo owns the orchestration, adapters, contracts, provenance, authored UI, and recovery logic.

## Studio operating model

TRIPPEDD is a creator-owned **network/studio machine**, not a single-show editor. It must support a broad programming canvas—live-action sketch, scripted comedy, narrative, animation, stop-motion/hybrid work, music-driven pieces, reality/unscripted, documentary/personality formats, specials, social-native work, games/interactive extensions, and mixed-media experiments.

The studio runs on two simultaneous trajectories:

- **Vertical slice:** make each production deeper, faster, more reliable, measurable, salvageable, and easier to finish.
- **Horizontal expansion:** add new formats, media types, production pathways, distribution surfaces, and reusable development capabilities without rebuilding the studio.

The detailed network/development model lives in `docs/TRIPPEDD-NETWORK-STUDIO-OPERATING-MODEL.md`; the machine-readable capability matrix lives in `config/production-capability-registry.json`.

## Capability map

### Physical source / ingest
- FFmpeg + FFprobe — deterministic media inspection/transcode
- MediaInfo — container/codec metadata
- ExifTool + BWF MetaEdit — metadata and broadcast-audio provenance
- OpenCV — frame/vision analysis
- PySceneDetect — shot boundaries
- Faster-Whisper — speech transcription
- Tesseract — OCR

### Editorial / story
- OpenTimelineIO — timeline interchange and adapters
- Fountain + Markdown + JSON Schema — script/story representations
- Graphviz + Mermaid — production/story graphs
- Kdenlive / MLT / Olive / Shotcut — open editorial/render backends where a real job benefits from them

### Animation / 2D / 3D / VFX
- Blender — procedural 3D, animation, rendering, compositing hooks
- OpenAssetIO — asset identity/interchange
- OpenColorIO — deterministic color management
- OpenUSD + MaterialX — scene/material interchange
- OpenVDB — volumetric data
- Natron — node compositing
- Embree — CPU ray-tracing acceleration where applicable

### Audio
- Demucs — source separation
- Audacity / Ardour — audio editing backends
- Rubber Band — time/pitch processing
- aubio — beat/onset/pitch analysis

### Render / compute
- Blender Flamenco — Blender-native render distribution candidate
- OpenCue — larger render-farm orchestration candidate
- GitHub Actions — current cloud execution backbone
- Durable frame/segment checkpoints — current recovery primitive

### QC / publishing
- Pyblish — structured publish validation
- Netflix VMAF — perceptual video quality assessment alongside PSNR/SSIM/MS-SSIM
- FFprobe / MediaInfo — hard technical delivery gates
- Provenance manifests — source/hash/tool/version tracking

### Production management
- Kitsu / Zou — production tracking candidate
- OpenAssetIO — asset identity boundary
- ProductionGraph — TRIPPEDD's authored layer joining people, requirements, evidence, approvals and work

### AI/media
- Google GenAI — current AI orchestration
- ONNX Runtime / PyTorch — model execution candidates when a concrete analysis/generation job justifies them
- Faster-Whisper / Demucs / OpenCV — local media intelligence

### Observability
- JSONL production events
- measured stage ledgers
- OpenTelemetry candidate for distributed tracing
- Prometheus/Grafana candidate for sustained render infrastructure

### Authored interface
- React + Vite
- Tailwind CSS
- Motion
- Lucide
- React Flow candidate for production graphs
- Three.js / React Three Fiber candidate for authored spatial studio views

## Promotion gates

A tool does not become production infrastructure because it is popular. Promotion requires:

1. License/maintenance review.
2. Installation or deterministic resolution.
3. Real-input smoke test.
4. Integration at a specific production boundary.
5. Measured output and provenance.
6. Failure/recovery behavior.
7. No regression to the canonical EP01 path.

## Current acceleration priorities

1. Parallelize independent Blender frame chunks without changing existing checkpoint keys.
2. Skip Blender startup entirely when a restored chunk already contains all valid frames.
3. Add VMAF as a perceptual QC layer when a reference/candidate pair exists.
4. Add Pyblish-style publish validators around final artifacts.
5. Add OpenAssetIO/OpenColorIO contracts around asset and color boundaries.
6. Add Demucs as an evidence-preserving audio-isolation branch, never overwriting source audio.
7. Evaluate Flamenco before introducing heavier distributed render infrastructure.
8. Build an authored React/visual layer around the production graph instead of treating the UI as a generic dashboard.
9. Make finished productions reusable: retain source lineage, talent, characters, performances, shots, dialogue, music, assets, concepts and derivative opportunities.
10. Expand the ProductionGraph beyond episodes so sketches, scripted projects, animation, music, reality, experimental work and interactive projects can share infrastructure without sharing the same creative process.
11. Keep third-party binaries out of Git history; provision them reproducibly and cache them.

## Size philosophy

A 1 MB Git repository is not evidence that the production system is small. The current repo contains orchestration/source code while media, Blender installations, model weights, node modules, Python environments, Actions artifacts and caches live outside Git. The correct goal is not artificial repo bloat; the goal is a substantially richer **capability graph** and a reproducible runtime that can provision the heavy tools on demand.
