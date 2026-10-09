# OpenCue render-farm integration

Upstream: https://github.com/AcademySoftwareFoundation/OpenCue
Role: horizontal render orchestration for Blender/Toucan/FFmpeg and other
TRIPPEDD render backends.

OpenCue is an open-source render management system designed for VFX and
animation production. It decomposes jobs into tasks, schedules them across
render hosts, and exposes monitoring and Python APIs. The project documents
Blender integrations and production-scale scheduling. 

TRIPPEDD contract:
- OpenCue owns dispatch/resource scheduling, not editorial truth.
- OTIO remains editorial truth.
- Blender remains the primary scene renderer.
- Toucan remains the independent OTIO conformance renderer.
- Every submitted render carries episode/scene/shot/frame-range/provenance.
- Failed/stale jobs remain observable and resumable through TRIPPEDD watchdogs.
- No production promotion occurs until an actual frame render + artifact QC passes.

Initial deployment mode: isolated render-farm backend and smoke test. Do not
claim farm capacity until Cuebot/RQD and a real Blender test job succeed.
