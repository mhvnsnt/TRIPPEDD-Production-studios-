# TRIPPEDD Compute Fabric v1 — God Molecule

Purpose: keep heavy generation/rendering out of the God Molecule Studio/API process.

## Hard rules

- The cockpit/API never performs heavy Blender, video-model, Gaussian-splat, or photogrammetry work synchronously.
- A job is real only after a worker produces a physical artifact and QC verifies it.
- OOM is a worker failure, never an application failure.
- MARS_CANONICAL is the immutable identity source of truth.
- Telemetry frames are diagnostics only and can never satisfy CREATIVE_FINAL.
- Every worker records tool/version, input hashes, output hashes, resource telemetry, and recovery attempts.

## Job flow

Studio -> TRIPPEDD API -> durable queue -> specialized worker -> artifact store -> QC/provenance -> Studio.

Recommended first implementation:
- Redis + Celery for the immediate worker queue.
- Blender Flamenco for Blender render jobs.
- MinIO/S3-compatible storage for large intermediate/final artifacts.
- Prometheus + OpenTelemetry for resource/job telemetry.
- Docker/NVIDIA Container Toolkit on GPU workers where NVIDIA hardware exists.
- Optional Temporal/OpenCue/Kubernetes lanes after the first worker path is green.

## Worker classes

render_cpu: Blender-safe CPU jobs, asset inspection, mesh optimization, proxy/LOD generation.

render_gpu: Blender GPU/EEVEE/Cycles jobs and GPU-accelerated compositing.

video_generation: Wan 2.2, LTX, HunyuanVideo, CogVideoX and other registered video models. Select by verified hardware profile rather than blindly launching every model.

character_animation: MARS_CANONICAL facial/body animation, OpenFaceFX, Rhubarb, PantoMatrix, LivePortrait/EchoMimic/Wan Animate lanes.

environment: seeded world generation, COLMAP/Meshroom, Nerfstudio, gsplat/SuGaR and OpenUSD interchange.

finishing: Tonnō, OpenColorIO/OpenImageIO/OpenEXR, Natron, FFmpeg and editorial/QC.

## Recovery ladder

1. Retry the same worker once for transient failure.
2. If OOM: lower representation/LOD, environment density, texture resolution, samples, then frame count.
3. Route to a larger GPU/CPU worker if available.
4. Route to an alternate implementation/model.
5. Preserve the failed run and telemetry.
6. Never convert failure into PASS.

## First real target

GM-SHOT-0001:
seed 742918 + MARS_CANONICAL + minimal environment -> real frames -> QC -> CREATIVE_FINAL.

The memory-safe proof may use a reduced Mars render representation, but the original canonical asset remains preserved and hashed. The reduction must be measured and traceable.

## Generator pool

The registry can contain many generators, but promotion requires:
- reproducible install
- adapter
- input/output contract
- smoke execution
- artifact verification
- resource telemetry
- failure/recovery path
- license/provenance record

Current video-generation candidates include Wan 2.2, LTX-2.x, HunyuanVideo, CogVideoX and Mochi. Wan 2.2 provides T2V/I2V/TI2V plus Animate/S2V variants and has ComfyUI/Diffusers integrations; actual hardware requirements must be evaluated per worker profile.

## Definition of done

CREATIVE_FINAL=true only when the requested artifact physically exists, is non-empty, passes media/identity/QC checks, and its manifest records the exact inputs and worker execution.

This file is an architecture contract, not a claim that every worker is already installed.
