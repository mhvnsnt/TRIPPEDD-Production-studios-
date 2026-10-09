# 2026-09-09 — Production Stall Detection Hardening

## Producer direction

The studio must never equate a GitHub Actions `in_progress` state with healthy production. A missing GitHub log blob makes the run's true progress unknown; that is a reliability failure, not a valid reason to display `RUNNING` without qualification.

## Change shipped

- Hardened `scripts/production/watch-progress.sh` to treat the measured production ledger as the source of truth.
- The watcher now emits `UNKNOWN` when measured telemetry has not appeared.
- It reports stage, measured percentage, completed/total work, elapsed time, throughput, ETA, heartbeat timestamp, and message.
- It monitors the stage heartbeat independently of GitHub's log service.
- Default stall threshold is 180 seconds and is configurable with `TRIPPEDD_PROGRESS_STALL_SECONDS`.
- If the active production stage heartbeat exceeds the threshold, the watcher emits `PRODUCTION_STALLED`, terminates the child production process, and exits with a bounded recovery code instead of allowing an apparently-running but unobservable job to consume compute indefinitely.
- EP01 Story Runner now exports `TRIPPEDD_PROGRESS_STALL_SECONDS=180` for future runs.

## Current-run limitation

The already-running canonical Story Runner run was started from an older workflow definition. Workflow edits on `main` do not retrofit into that existing runner. Therefore the current run cannot acquire this watchdog retroactively without restarting it. Its GitHub job remains `in_progress`, but absence of its log blob means health is not claimed from that state alone.

## Operating law

`UNKNOWN` is not `HEALTHY`. GitHub job state is orchestration state; the production ledger heartbeat is execution evidence. Future production builds must fail into the bounded recovery path when execution telemetry stops rather than silently remaining `in_progress`.

## Compute direction

This hardening is compatible with the studio's GitHub-first/local/farm routing. GitHub-hosted runners remain useful, while self-hosted runners can provide an alternate execution substrate without changing the production telemetry contract. GitHub documents self-hosted runners as a supported way to run Actions jobs on controlled hardware.
