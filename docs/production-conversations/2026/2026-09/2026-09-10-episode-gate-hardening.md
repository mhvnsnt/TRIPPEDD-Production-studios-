# EP01 Gate Hardening — 2026-09-10

## Producer direction

Finish the next production gate and remove failures, roadblocks, cancellations, and avoidable bottlenecks without sacrificing editorial correctness.

## Changes completed

- Relaunched the canonical EP01 Story Runner from current `main` after the editorial-evidence recovery change.
- Preserved resumable subjectivity/Bastard render architecture and existing cache/checkpoint behavior.
- Hardened Story Runner dependency reuse so cached Blender archives are not re-downloaded on every render job.
- Added explicit build identity telemetry (`GITHUB_SHA`, ref, workflow, run ID, attempt, event) to the production artifact path so stale-SHA incidents are observable instead of inferred.
- Added bounded failure-diagnostic artifacts for Story Runner and Autonomous builds.
- Removed the Autonomous workflow's `push` trigger on `production/EP01/RUN-PUBLIC-BUILD`. Autonomous now starts only through `workflow_dispatch`, allowing the production self-healer to launch it after a successful canonical Story Runner and pass the exact successful `story_run_id` for verified media reuse.
- Preserved editorial independence: Autonomous still runs `TRIPPEDD_CUT_MODE=AUTONOMOUS` and builds its own editorial assembly; it does not use the Story Runner final edit as its source.
- Kept the PySceneDetect fallback evidence path: when transcript-derived comedy candidates are absent, shot-boundary evidence remains explicitly low-confidence machine-selected evidence rather than being promoted to a factual comedy claim.

## Operating laws reinforced

1. No blind reruns.
2. Missing telemetry is UNKNOWN, not healthy.
3. Technical source analysis success must not strand an episode because one editorial evidence modality is empty.
4. Expensive generated media should be reused by verified artifact/run identity when valid, not regenerated unnecessarily.
5. Autonomous and Story Runner are different cuts and must remain editorially independent.
6. Autonomous must not compete with Story Runner for the same kickoff.
7. Every completed gate must leave durable evidence sufficient to diagnose the next failure without rerunning expensive upstream work.

## Current gate sequence

`current-main Story Runner -> artifact + technical QC -> self-healer chains Autonomous with story_run_id -> independent Autonomous build -> Autonomous QC -> human editorial/showrunner greenlight`
