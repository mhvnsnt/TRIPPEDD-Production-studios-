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
- Hardened the resumable Bastard terminal-tag action so future runs report aggregate frame percentage, observed frames/second, ETA, bytes, cache-hit progress, and MP4 assembly percentage.
- Bastard progress remains checkpoint-based: the 12 independent v4 chunk caches are preserved and reused.

## Open-source direction
Continue expanding the production capability registry around open-source components that materially improve rendering, editorial interchange, compositing, animation, VFX, audio, and distributed compute. FFmpeg remains the measured encoding telemetry source; OpenTimelineIO remains the interchange foundation; Flamenco and OpenCue remain the primary render-farm candidates for self-hosted compute.

Flamenco is currently the first render-farm integration target because its current stable release is 3.9.3, it is GPL-3.0 open source, self-hosted, cross-platform, API-driven, and supports Blender and FFmpeg task types. Its Manager also exposes job/task/worker events through MQTT, giving TRIPPEDD a viable route to ingest farm telemetry into the same measured production ledger. The integration must still pass real-EP01 smoke, measured output, recovery, artifact compatibility, and no-regression gates before promotion.

## Live EP01 protection
Canonical Story Runner run `34394290662` remains active. Its build job is currently on `Build Bastard terminal tag (resumable)`. The live run was created before the latest Bastard telemetry changes, so it is intentionally not restarted. New telemetry applies to subsequent executions. The active run's completed subjectivity work remains protected.

## Operating law
No blind reruns. No fake progress. Preserve checkpoints. Upgrade the pipeline around live production without destroying useful active work.
