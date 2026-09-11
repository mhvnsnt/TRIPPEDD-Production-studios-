# Here Production Runtime — Complete Stack Contract

The runtime is a co-production system, not a clip concatenator and not a collection of disconnected tools.

## Capability lanes

1. **Ingest & transport** — Drive/rclone/API fallbacks, resumable transfers, checksum and provenance.
2. **Source truth** — immutable source assets, canonical likeness/reference manifests, physical-source timeline.
3. **Asset intelligence** — ffprobe, OpenImageIO, OpenEXR, MediaInfo/QCTools, scene detection, OCR, transcription, VAD.
4. **2D creation** — Krita, OpenToonz, Synfig, SVG/raster processing.
5. **3D reconstruction** — Meshroom/AliceVision, COLMAP, TRELLIS.2 and approved experimental reconstruction backends.
6. **3D authoring** — Blender, OpenUSD, MaterialX, OpenAssetIO.
7. **Character rigging** — Tripo Face Rig, Blender rig tooling, MPFB2/MakeHuman where appropriate.
8. **Performance/facial animation** — OpenFaceFX, PantoMatrix, BlendCap, MoFace, Rhubarb/lip-sync.
9. **Image generation/editing** — ComfyUI, Diffusers, InvokeAI, DiffSynth, ControlNet, IP-Adapter; identity-safe reference conditioning only.
10. **Video generation/editing** — Wan, LTX, CogVideoX, HunyuanVideo, Open-Sora, AnimateDiff; multiple providers/backends so one model cannot block production.
11. **Simulation/VFX** — Blender simulation, Natron, Frei0r, VapourSynth and other validated effect backends.
12. **Audio** — Whisper/Faster-Whisper, Silero VAD, Demucs, Ardour and additional validated audio tools.
13. **Editorial** — OpenTimelineIO, Kdenlive, MLT, FFmpeg.
14. **Color/finishing** — OpenColorIO, OpenImageIO, OpenEXR, Natron.
15. **Render orchestration** — Flamenco, OpenCue and local worker execution with checkpoint/retry.
16. **Production management** — AYON, Kitsu, Pyblish where promoted by evidence.
17. **Observability** — OpenTelemetry, Prometheus, Grafana plus the durable production ledger.
18. **QC/delivery** — VMAF, MediaConch, QCTools, deterministic media checks and likeness/identity gates.
19. **Artifact/cache management** — source cache, dependency cache, model cache, render cache, resumable artifacts.
20. **Recovery** — every critical lane must have an alternate implementation or deterministic fallback; UNKNOWN is never PASS.

## Promotion law

An OSS project is not considered production-ready because it appears in a manifest. Promotion requires provenance/license evidence, reproducible provisioning, a real TRIPPEDD input smoke test, measured output, recovery/resume evidence, artifact compatibility, and regression evidence.

## Failure-routing law

When a capability fails, the runtime immediately attempts the next compatible implementation before escalating to the operator. The recovery attempt is logged with the failed backend, replacement backend, reason, result, elapsed time, and artifact identity.

## Mars identity law

When the production request is to edit, animate, rig, composite, or transform a supplied likeness, the supplied likeness is immutable source truth. Generative systems must not silently regenerate a different person. Outputs that fail identity/geometry gates are rejected.

## Current Tripo head target

Drive URL: https://drive.google.com/file/d/1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl/view?usp=drivesdk

Drive file ID: `1RKxHGkgoKe0hZf7a2kObqzKpgqKfkrhl`

Required acquisition gates: preserve original; identify file type; checksum; provenance; mesh/topology inventory; dimensions/units; materials/textures; facial landmarks; rig readiness; likeness integrity.

## Completion criterion

The stack is complete when an episode can travel from source/reference ingest through asset analysis, creation/reconstruction, animation/generation, audio, editorial, render, QC, recovery, and final artifact delivery without requiring a single proprietary service or a single backend to succeed. Individual OSS projects may remain optional; the production capability lanes may not.
