# 2026-09-09 — Six-hour EP01 finish push

## Producer directive

Finish EP01 within the requested six-hour window, delivering both canonical cuts: Story Runner and Autonomous. Continue expanding TRIPPEDD vertically and horizontally while protecting the active production path.

## Execution changes

- Tightened the production self-healer stale-run backstop from 110 minutes to 60 minutes so a genuinely stalled render is recovered inside the six-hour delivery window rather than consuming most of the window.
- Preserved the recovery law: completed subjectivity artifacts and durable caches are retained; only the stalled run is cancelled/replayed.
- Added automatic production chaining: after a successful canonical Story Runner run, the self-healer dispatches the Autonomous Cut on current `main` when no Autonomous run has already started after that success.
- The existing resumable Bastard terminal-tag action remains the recovery mechanism for the generated terminal tag, with independent frame chunks, bounded parallelism, cache reuse, measured frame progress, elapsed time, rate, ETA, and MP4 assembly telemetry.

## Current EP01 evidence

Canonical Story Runner run `34394290662` has all 12 subjectivity chunks successfully uploaded. Its build job remains on `Build Bastard terminal tag (resumable)`. GitHub is not exposing a live log blob for that legacy job, so no frame percentage or ETA is asserted for it. If it reaches the 60-minute stale threshold, the new self-healer policy recovers it and reuses checkpoints rather than restarting the episode from zero.

## Open-source compute direction

Flamenco remains the first self-hosted render-farm promotion candidate because it is actively used by Blender Studio and directly supports Blender render workloads. OpenCue remains the horizontal distributed render/task path. Both stay behind real-EP01 smoke-test, measured-output, recovery, artifact-compatibility, and no-regression gates.

## Delivery rule

No blind reruns. No fabricated progress. Preserve salvageable work. Keep both cuts moving toward complete technical artifacts and QC, with human editorial/showrunner approval remaining the final creative gate.
