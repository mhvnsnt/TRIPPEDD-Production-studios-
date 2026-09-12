# 2026-09-10 — All-step production telemetry upgrade

## Decision

EP01 generated subjectivity rendering now emits measured progress telemetry directly from the Blender frame loop.

## Contract

Each chunk reports:

- a 20-character progress bar;
- percentage derived from completed frames / expected frames;
- completed / total work;
- elapsed wall-clock time;
- measured frames-per-second;
- ETA derived from measured rate;
- current frame and operation;
- emitted artifact bytes;
- explicit completion telemetry.

Checkpoint hits are counted as completed work rather than re-rendered work.

## Safety

This change is additive and does not cancel or restart the active EP01 Story Runner run. It lands on a dedicated Development Workstream and can be merged independently because the current Story Runner workflow does not trigger on this script path.

The existing fail-closed watcher remains authoritative for the main editorial build: missing or stale measured telemetry is UNKNOWN, not healthy.

## OSS direction

Render orchestration remains feature-gated. Flamenco 3.9.3 is currently the stable Blender render-management release; OpenCue v1.19.1 remains the broader render-farm candidate. Neither is promoted to the canonical EP01 path until real-input smoke, artifact, recovery, and regression evidence exists.
