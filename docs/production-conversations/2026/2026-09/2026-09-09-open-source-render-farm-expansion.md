# 2026-09-09 — Open-source render-farm expansion

## Producer direction

Keep EP01 moving to completion. If a production stage is genuinely stalled, salvage completed work and recover only the stalled portion. Continue upgrading the studio while production runs; open-source additions must materially improve throughput, recovery, observability, or future studio scale.

## Current EP01 state

Canonical Story Runner run `34394290662` has all 12 subjectivity chunks completed and uploaded. The build job is/was blocked at `Build Bastard terminal tag (resumable)`. The run predates the terminal-tag telemetry hardening, so its live logs do not expose trustworthy frame-level progress. Do not invent a percentage or ETA for this legacy run.

Recovery law: preserve completed chunks and caches; never restart the whole episode merely because one render stage stalls. A recovered terminal-tag attempt must reuse independent frame/chunk checkpoints and report measured frames, elapsed time, rate, bytes, and ETA.

## Open-source direction

TRIPPEDD's compute-backend registry already defines GitHub Actions as canonical while capacity is available, local execution as the direct fallback, Flamenco as the Blender render-farm fallback, OpenCue as the distributed render/task fallback, and `act` as workflow reproduction rather than a render farm.

Fresh research confirms Flamenco 3.9.3 is the current stable release. Flamenco is free/open source GPL-3.0, self-hosted, cross-platform, used in production at Blender Studio, exposes an OpenAPI API, and its Worker supports Blender rendering, FFmpeg frame-to-video, file management, and arbitrary exec tasks. Flamenco also exposes MQTT farm/job/task/worker events, making it suitable for future production telemetry integration.

OpenCue v1.19.1 is the current stable documented release. Its 2026 work includes a Rust distributed scheduler, event-driven monitoring, and OpenCueWeb; it is appropriate for the horizontal scale path rather than being inserted into the critical EP01 path before a real-input smoke test.

## Promotion rule

No open-source component becomes production-critical merely because it is promising. It must pass: license review, installation/reprovisioning, real EP01 input smoke test, measured output, failure recovery, canonical artifact compatibility, and no regression.

## Operating principle

Vertical trajectory: faster, deeper, more observable, more recoverable production. Horizontal trajectory: more media formats, render backends, studio workflows, and reusable network infrastructure. Both continue while EP01 is being finished.
