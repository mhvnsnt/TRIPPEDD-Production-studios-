# TRIPPEDD Autonomous Production Architecture

Status: production hardening specification
Date: 2026-09-10

## Purpose

Decouple TRIPPEDD production execution from any single ChatGPT/GitHub connector session. GitHub remains the source of truth and authorization boundary; production execution is delegated to an authenticated, ephemeral runner controlled by the TRIPPEDD supervisor.

## Target architecture

```
GitHub
  |
  | workflow_job webhook
  v
TRIPPEDD supervisor
  |
  +-- authenticate as GitHub App
  +-- obtain short-lived installation token
  +-- request JIT runner configuration
  v
ephemeral production runner
  |
  +-- checkout
  +-- ingest / analysis / editorial
  +-- FFmpeg / FFprobe / Blender / Whisper / OTIO / QC
  +-- checkpoints / heartbeats / artifacts
  v
deliverables
  |
  +-- MP4
  +-- JSON
  +-- OTIO
  +-- QC report
  +-- hashes / provenance
  v
runner teardown
```

## Security boundary

This is an authorization-preserving workaround, not a GitHub security bypass.

The GitHub App must be installed by an authorized account and must receive only the repository permissions required by the controller. Private keys and webhook secrets must never be committed to the repository.

## Runner lifecycle

1. A production workflow is queued.
2. The controller receives the `workflow_job` event.
3. The controller authenticates as the installed GitHub App.
4. The controller requests a just-in-time runner configuration.
5. The runner registers with the production label.
6. The workflow executes exactly one production job.
7. Logs and required artifacts are persisted outside the ephemeral runner.
8. The runner is removed/destroyed after the job.
9. The supervisor reconciles desired state and actual state.

## Hardening requirements

### Source gate
- Validate the real external source path before expensive rendering.
- Explicitly record expected versus available sources.
- Partial source availability must never be reported as complete.
- Fail closed on missing authentication or stale source transport.

### Attempt isolation
- Every production attempt receives a unique attempt ID.
- Heartbeats and progress belong to that attempt only.
- Old telemetry cannot make a new attempt appear healthy.

### Checkpointing
- Preserve successful intermediate artifacts.
- Checkpoint before cancellation/restart.
- Resume only from validated checkpoints.
- Never overwrite a known-good artifact with an unverified partial artifact.

### Watchdog
- Detect stale progress from measured telemetry, not elapsed wall time alone.
- Bound retries.
- On stale execution: checkpoint -> preserve -> cancel -> provision fresh runner -> resume.
- Escalate after the retry budget is exhausted.

### Deliverable gate
A production run cannot claim PASS until all required deliverables exist and validate:
- MP4 duration
- resolution
- frame rate
- audio presence/format where required
- OTIO structure
- JSON schema
- QC result
- content hashes/provenance

### Recovery
Recovery must distinguish:
- failed job
- cancelled job
- stale/stuck job
- missing artifact
- invalid artifact
- source transport failure

Each state must have a bounded recovery action and an auditable event.

## Commercial proof gate

The 20-second commercial test is the mandatory cheap end-to-end proof before another expensive episode run.

The test must:
1. Use a deterministic source.
2. Run the actual production path.
3. Produce MP4 + JSON + OTIO + QC + provenance.
4. Validate every output.
5. Exercise the recovery simulator.
6. Leave a machine-readable PASS/FAIL result.

### FFmpeg construction rule

The source filter belongs in the lavfi input definition. The output filter chain belongs in `-vf`.

Correct pattern:

```text
color=c=black:s=1280x720:r=24:d=20,format=yuv420p
```

Do not construct a command where the source filter is accidentally swallowed by or concatenated into the output `-vf` expression.

## Routing

The production workflow should support:

```text
runs-on: ${{ vars.TRIPPEDD_RUNNER_LABEL || 'ubuntu-latest' }}
```

The intended production label is:

```text
trippedd-production
```

The fallback label must remain suitable for cheap CI validation only; production workloads should require an explicitly configured production runner label once the autonomous controller is deployed.

## Observability

Persist:
- desired state
- autonomous state
- event log
- attempt ID
- runner ID
- workflow/run ID
- checkpoint ID
- artifact manifest
- artifact hashes
- start/end timestamps
- heartbeat/progress timestamps
- recovery reason and action

Never infer success from a workflow being merely 'completed'. Deliverable validation is authoritative.

## Open-source execution stack

The production environment is intended to use maintained/open tooling where practical:
- FFmpeg / FFprobe
- Blender
- Whisper-compatible transcription
- OpenTimelineIO
- MediaInfo
- ExifTool
- ImageMagick
- OpenCV
- PySceneDetect
- rclone

Exact versions should be pinned in the runner image/bootstrap layer and upgraded through controlled tests.

## Current operational rule

**HARDEN -> 20-SECOND PROOF -> VERIFY ARTIFACTS -> VERIFY RECOVERY -> SALVAGE PILOT/EP01 ASSETS -> ONLY THEN RESUME EXPENSIVE EPISODE PRODUCTION.**

No blind rerun.
