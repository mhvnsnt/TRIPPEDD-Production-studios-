# 2026-09-09 — Terminal progress + compute failover hardening

## Producer direction

The producer asked to keep working toward a real EP01 finish, make rendering progress observable with truthful loading/progress indicators, report the Bastard terminal-tag state and Story Runner handoff, avoid unnecessary restarts, and keep improving the production studio with useful open-source infrastructure. The producer specifically wants the episode finished for real and does not want progress estimated from invented timers.

## Live production evidence

Canonical EP01 Story Runner run: `34394290662`.

At the latest live check:
- 12/12 subjectivity chunk jobs completed successfully.
- Subjectivity assembly completed successfully.
- `Build Bastard terminal tag (resumable)` is the active step.
- `Install Node dependencies`, `Build Story Runner cut`, `Verify Story Runner`, and `Upload Story Runner` remain downstream.
- The job logs endpoint is currently returning `BlobNotFound`, so no exact live frame percentage is claimed from inaccessible logs.

The active run is not being cancelled or rerun. Existing completed artifacts and checkpoints remain protected.

## Progress observability upgrade

The existing production progress ledger already provides measured stage counts, percentages, heartbeats, and artifact metadata. The Bastard renderer itself already emits per-frame completion messages.

The missing piece was a visible aggregate progress signal around the parallel twelve-chunk terminal-tag renderer. Updated `.github/actions/resumable-bastard-tag/action.yml` now emits GitHub `notice` telemetry based on actual frame files on disk:
- aggregate `0/144` through `144/144` frame progress;
- per-chunk `0/12` through `12/12` progress;
- cache-hit progress;
- byte totals sampled from completed frame directories;
- batch-complete notices;
- explicit 100% / MP4-assembly and MP4-complete notices.

This does not affect the already-running job because GitHub Actions executes the checked-out revision for that run. It is the observability contract for the next execution/recovery and is intentionally separate from the active run.

GitHub documents `::notice` workflow commands as runner-visible annotations emitted from stdout, which is appropriate for this live-progress telemetry.

## Open-source / no-hosted-minutes path

`config/compute-backends.json` already defines GitHub Actions, local execution, Flamenco, OpenCue, and `act` as distinct compute roles with evidence-gated promotion requirements.

The local EP01 fallback had a real gap: it rendered subjectivity, but its Bastard section only printed that the action contract existed instead of actually executing the local Bastard renderer. That made the fallback incomplete.

Fixed `scripts/production/local-ep01-fallback.sh` so the local fallback now actually invokes `scripts/production/local-bastard-tag.sh`, verifies the terminal MP4 and `.blend`, then proceeds into Story Runner build and QC.

Flamenco remains the preferred open-source Blender render-farm candidate; its current stable release is 3.9.3 and it is free/open source, self-hostable, cross-platform, and used in production at Blender Studio. It remains subject to real-EP01 smoke, measured output, recovery, and canonical-artifact compatibility gates before being promoted to the default backend.

## Operating rule

No blind production reruns. Preserve live work. Improve the pipeline around the active render, reuse completed checkpoints, and only recover/replay when measured evidence establishes failure or a genuinely dead run.
