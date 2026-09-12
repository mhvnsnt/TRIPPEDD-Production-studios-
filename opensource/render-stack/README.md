# TRIPPEDD Open-Source Render Stack

This directory defines the studio's independent open-source render subsystems. TRIPPEDD does not copy fragments of these projects into the production codebase; it provisions the complete upstream projects as cooperating services/workspaces.

## Components

- **Blender / Flamenco** — Blender-native distributed render/task execution. Flamenco is the preferred backend for Blender-heavy animation work.
- **OpenCue** — horizontally scalable render/task scheduling for jobs that benefit from frame/task fan-out across multiple workers.
- **FFmpeg** — deterministic media encode/mux stage.
- **Kdenlive/MLT** — optional editorial/export backend for timelines that benefit from MLT's non-linear editing and render model.

The production controller chooses a backend per job. No backend becomes the only path: every render job keeps a local/checkpointed fallback.

## Promotion gates

A backend must pass:

1. license/provenance record;
2. clean installation/reprovisioning;
3. 20-second commercial smoke render;
4. real EP01 frame/chunk smoke render;
5. measured throughput and resource telemetry;
6. worker-loss/retry recovery;
7. artifact compatibility and QC;
8. no regression against the canonical FFmpeg path.

## Performance strategy

Do not render a 480-frame Blender job serially on one runner when the scene can be decomposed safely. The scheduler should fan out independent frame ranges/chunks, persist completed chunks, and assemble only after all chunks pass QC.

The fallback remains the existing resumable renderer. Completed frames/chunks are never discarded merely because a worker dies.
