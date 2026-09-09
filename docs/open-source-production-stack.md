# Open-Source Production Stack

This document records open-source systems that can deepen the production pipeline without replacing the deterministic FFmpeg/OpenTimelineIO path until they are installed, benchmarked, and verified in CI.

## Render orchestration

- **Flamenco** — self-hosted Blender render management; a strong fit for Blender-heavy burst rendering and resumable job dispatch.
- **OpenCue** — production-proven render management from the Academy Software Foundation ecosystem; suitable for larger heterogeneous farms, scheduling, resource tags, and future browser-based operations.
- **OpenCueWeb** — browser UI for OpenCue job/frame monitoring and administration; keep it as an operations-plane integration rather than a render dependency.

## Media processing

- **VapourSynth** — programmable frame/video processing layer for deterministic transforms, restoration, filtering, and analysis.
- **zimg** — high-quality resize/colorspace primitives that can back selected media transforms when benchmarks show an advantage over the existing FFmpeg path.
- **frei0r** — portable open video-effect plugin API and collection; useful for optional effect stages while preserving a deterministic FFmpeg fallback.
- **MLT** — multitrack audio/video engine that can support alternate editorial/render backends without replacing OpenTimelineIO as the interchange contract.

## Color and image pipeline

- **OpenColorIO** — production-oriented color management and ACES-compatible color transforms.
- **OpenImageIO** — professional image I/O and processing for large VFX/animation-oriented image workflows.
- **OpenEXR** — high-dynamic-range image interchange for generated/compositing intermediates.
- **OpenAssetIO** — asset-reference/interchange abstraction for eventually connecting the studio pipeline to external asset managers without hard-coding one provider.

## Audio and speech analysis

- **Silero VAD** — lightweight voice-activity detection that can precede transcription to reduce dead-air processing and improve segment boundaries.
- **SoX** — scriptable audio inspection/transformation utility for deterministic preprocessing.
- **Rubber Band** — high-quality time/pitch processing for optional audio conform operations.
- **Audacity** — human-facing open-source audio inspection/editing fallback; not part of unattended rendering.

## Media validation and packaging

- **Bento4** — ISO-BMFF/MP4 inspection and manipulation tools for deeper container validation.
- **MKVToolNix** — container inspection/muxing toolkit for diagnostics and alternate packaging workflows.

## Integration policy

1. The production critical path remains FFmpeg/FFprobe + OpenTimelineIO + the verified generator scripts.
2. Optional tools are capability probes first: absence is explicit and must not fail the production build.
3. A new backend must pass deterministic output, checksum/provenance, and performance tests before it can replace an existing path.
4. Distributed rendering is an execution backend, not an editorial source of truth. Physical-source evidence remains authoritative.
5. Models and third-party assets require license metadata before they become production dependencies.
6. Active production runs must not be interrupted merely to install or benchmark an optional tool.

## Current expansion targets

The next safe integration layers are:

- a content-addressed render manifest shared by GitHub-hosted, Flamenco, and OpenCue workers;
- a VAD -> Whisper transcription pipeline with reusable transcript artifacts;
- optional VapourSynth/zimg processing behind a feature flag and golden-media tests;
- Bento4/MKVToolNix deep container QC after FFprobe QC;
- OpenColorIO/OpenImageIO capability probes for future color/image stages.
