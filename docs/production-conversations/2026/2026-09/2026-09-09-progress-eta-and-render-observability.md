# 2026-09-09 — Measured progress, ETA, and renderer observability

## Producer direction
Upgrade every production progress bar so it reports measured percentage, elapsed time, observed throughput, and ETA whenever the underlying worker exposes enough evidence to calculate it. Never fabricate a percentage or ETA.

## Implemented
- `ProductionProgressLedger` schema v2 now records `startedAt`, `elapsedMs`, `ratePerSecond`, `etaSeconds`, and human-readable `etaLabel`.
- ETA is derived from observed completed-work deltas, not a timer pretending to represent work.
- Active Production UI now displays percentage, elapsed time, throughput, ETA, status, artifact size, and the current message.
- Added an FFmpeg progress parser using FFmpeg's machine-readable `-progress pipe:1` interface.
- Pilot renderer now feeds measured FFmpeg progress into the ledger for timed segment renders.
- Source and generated segment stages retain cache reuse and concurrency; progress is reported at sub-unit granularity while a segment is actually rendering.

## Open-source direction
Continue expanding the production capability registry around open-source components that materially improve rendering, editorial interchange, compositing, animation, VFX, audio, and distributed compute. FFmpeg remains the measured encoding telemetry source; OpenTimelineIO remains the interchange foundation; Flamenco and OpenCue remain the primary render-farm candidates for self-hosted compute.

## Live EP01 protection
Canonical Story Runner run `34394290662` remains active. Its build job is currently on `Build Bastard terminal tag (resumable)`. The live run was created before these latest renderer changes, so it is intentionally not restarted. New telemetry applies to subsequent executions. The active run's completed subjectivity work remains protected.

## Operating law
No blind reruns. No fake progress. Preserve checkpoints. Upgrade the pipeline around live production without destroying useful active work.
