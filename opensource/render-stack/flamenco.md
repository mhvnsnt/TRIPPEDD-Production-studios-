# Flamenco render-farm backend

Upstream: https://flamenco.blender.org/
Source: Blender Projects / studio/flamenco
Role: primary Blender render-farm scheduler for TRIPPEDD.

Flamenco is free/open-source, cross-platform render management used in
production by Blender Studio, including scaling across hundreds of machines.

TRIPPEDD contract:
- OpenCue remains the alternative distributed scheduler.
- Flamenco is the preferred Blender-native farm path.
- Blender scene files remain authoritative for scene rendering.
- OTIO remains editorial truth.
- Shared storage and identical Blender executable paths are explicit farm
  prerequisites.
- Jobs must carry episode/scene/shot/frame-range/provenance metadata.
- Worker success requires an actual rendered frame plus QC, not job submission.

Production status: backend candidate until a real manager/worker smoke render
passes in the TRIPPEDD environment.
