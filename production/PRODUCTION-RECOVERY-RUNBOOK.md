# Production Recovery Runbook

## Restart policy
1. Never delete prior production artifacts.
2. Preserve any valid media, manifests, OTIO, QC, transcripts, frames, and logs as salvage.
3. Restart stalled work from current main.
4. Do not duplicate an already-active current-main run.
5. Prefer a parallel OSS backend when the current backend is the bottleneck.
6. A PASS requires an actual workflow run, artifact, and QC evidence.

## Commercial
Target: Production Short E2E Gate.
Expected wall time: ~8 min; hard ceiling: 20 min.
Static-image masquerading as video is rejected by sampled-frame uniqueness.
Silent/near-silent audio is rejected by measured mean volume.
Four-show scope is locked: THE BASTARD, IN THE BUSHES, GOD MOLECULE, TRIPPEDD.
Smoke & Mirrors is forbidden.

## EP01
Run Story Runner first when its real-source transport succeeds.
Autonomous can reuse a verified Story Runner artifact through story_run_id, or render its own subjectivity chunks.
Both cuts remain independent deliverables.

## Backend escalation
If Blender creative render stalls: preserve frames, retry once, then route eligible motion-graphics segments through Motion Canvas/Remotion/OpenMotion.
If compositing stalls: route through Natron/Gaffer/OpenFX.
If transport stalls: use cached source checkpoint, rclone, FFmpeg, MediaInfo, or alternate transport.
If editorial assembly stalls: preserve OTIO and route through Kdenlive/MLT where compatible.
If encoding/package validation stalls: use FFmpeg/Bento4 and independently verify with MediaInfo/ffprobe.

## Do not call infrastructure presence production completion.
