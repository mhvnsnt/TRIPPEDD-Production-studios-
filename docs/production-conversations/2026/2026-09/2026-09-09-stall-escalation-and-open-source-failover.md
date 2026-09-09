# 2026-09-09 — Stall Escalation + Open-Source Compute Failover

## Producer direction

Keep working toward a finished EP01 while continuing to upgrade the production studio and bring in open-source infrastructure when it materially improves throughput, observability, recovery, or compute independence.

## Live EP01 finding

Canonical Story Runner run `34394290662` remains `in_progress` with build job `102640267853` at `Build Story Runner cut`. The completed work is preserved: all 12 subjectivity chunks succeeded, subjectivity assembly succeeded, Bastard terminal tag succeeded, and dependencies/media setup succeeded. The job log endpoint currently returns `BlobNotFound`, so `in_progress` is not treated as proof of health. No Story Runner artifact is present yet.

## Recovery change

`production-self-healer.yml` was hardened so stale active runs are allowed a bounded replay through attempt 3 instead of becoming stranded after attempt 2. A genuinely stale run is still cancelled only after an active job has exceeded the 60-minute backstop. Attempt-3 stale runs are explicitly escalated and never silently labeled healthy.

Commit: `6f0a7c432dc44927ec078837297a4286adb125ef`

## Open-source compute direction

The compute registry continues to use GitHub-hosted execution first while preserving local/farm paths. Blender Flamenco 3.9.3 remains the current stable open-source render-farm target; it is preferred over experimental 3.10-beta1 for production. Self-hosted GitHub runners remain the workflow-compute failover path when an owned machine is available, while Flamenco/OpenCue provide render-farm expansion rather than arbitrary library accumulation.

## Operating law

No blind reruns. Preserve completed artifacts and caches. A run is healthy only when measurable progress/heartbeat evidence exists. When observability is absent beyond the bounded threshold, recover explicitly rather than assuming `in_progress` means alive.
