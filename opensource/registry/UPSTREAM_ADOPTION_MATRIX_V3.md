# Upstream Adoption Matrix V3

## Tier A — directly useful now
OpenRV, OpenTimelineIO, AYON, QuadPype, OpenMontage, PipelineKit, 4brospix, OpenToonz, Flamenco, OpenCue, ComfyUI, OpenUSD, Ardour, GStreamer.

## Tier B — useful after isolated adapter tests
BB_Kitsu-Pipeline, OpenStudioHub, Ateru, Pencil2D, Synfig, Kdenlive, MLT, Audacity.

## Horizontal infrastructure
PostgreSQL, MinIO, NATS, Temporal, Redis.

## Vertical media infrastructure
Blender, Natron, OpenColorIO, OpenImageIO, OpenEXR, OpenVDB, FFmpeg, VapourSynth.

## Guardrails
1. Never replace a working backend merely because an upstream project is newer.
2. Every adoption gets an isolated health test.
3. Every media backend gets a representative 20-second media test before episode use.
4. Every AI backend must expose provenance/workflow metadata when technically available.
5. Generated media is an input to production, not automatically the final editorial decision.
6. Human story decisions remain locked for Story Runner unless explicitly delegated.
7. Autonomous Cut may execute approved policy, but every irreversible delivery remains QC-gated.
8. Preserve all salvageable prior commercial/episode artifacts.

## Target outcome
TRIPPEDD becomes an umbrella studio where specialized upstream systems cooperate as replaceable production departments rather than a monolithic home-grown reimplementation.
