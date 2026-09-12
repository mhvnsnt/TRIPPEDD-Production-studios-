# Render backend research — 2026-09-09

## Decision
TRIPPEDD will not depend exclusively on GitHub-hosted Actions for production rendering. The canonical production contract remains checkpointed and backend-neutral so work can move between hosted Actions and self-hosted render infrastructure without discarding completed frames.

## Open-source backends
- **Blender Flamenco** is the first self-hosted render-farm target. It is free/open source, cross-platform, self-hostable, and Blender Studio uses it in production. It supports a Manager plus Workers and shared project storage.
- **OpenCue** is the scale-out render-management target for larger multi-machine VFX/animation workloads. It provides queueing/resource allocation and supports on-prem, cloud, and hybrid deployments.

## Integration rule
Do not introduce either backend into the canonical EP01 render while EP01 is actively running. First complete the current Story Runner production. Then validate the backend against the existing resumable 12-frame chunk contract using a real EP01-compatible test input. A backend is production-ready only after installation, real render, artifact/provenance validation, and recovery/resume validation.

## EP01 protection
The active canonical run `34394290662` remains authoritative. No cancellation or blind rerun is permitted. Its completed subjectivity chunks and assembly are preserved while the Bastard terminal tag renders.

## Next implementation gates
1. Finish EP01 terminal tag and Story Runner cut.
2. Verify final media and automatic technical QC.
3. Remove avoidable hosted-runner work, especially unconditional Blender installation after cache restore.
4. Wire Flamenco as the first self-hosted compute backend behind the existing compute-backend registry.
5. Add OpenCue as a scale-out backend after Flamenco passes real-input recovery tests.
