# Rocket Cloud Recovery Continuation Runbook

## Purpose

Rocket's cloud/Blender runtime is temporarily unavailable. This document is the durable instruction packet for Rocket to resume immediately when its cloud runtime returns. It is intentionally execution-oriented: Rocket must continue the production-control work without waiting for a new owner prompt, while never fabricating Blender execution or visual evidence.

## Ownership

- **Rocket:** command-center UI, control-plane adapters, job lifecycle, cloud/Blender launch integration, render/validation dispatch, logs, retries, artifact/evidence ingestion, and live production-state presentation.
- **Blender/GLB runtime:** geometry, rig, animation, renders, measurements, and evidence bytes are production authority.
- **Claude:** visual/geometry authority for MARS surgical work when its runtime is available.
- **TRIPPEDD repo:** durable contracts, schemas, queues, manifests, provenance, handoff packets, and integration surfaces.

## Hard constraints

1. `UNKNOWN` is never `PASS`.
2. Never fabricate a render, measurement, hash, Blender result, or successful job while the runtime is unavailable.
3. Never replace production implementation with a dashboard mock.
4. Never make `/command-center` the production runtime; it is the control/observation surface.
5. Never overwrite `main` silently. Keep Rocket changes reviewable through its normal branch/PR flow.
6. Do not replace `MARS_CANONICAL` or protected oral components with generated placeholders.
7. Do not bypass the canonical component preservation law.
8. Prefer existing donors/tools before writing bespoke geometry or repair logic.

## Resume sequence when cloud returns

### Phase 1 — establish reality

- Reconnect the cloud/Blender worker.
- Run a no-op health/capabilities probe.
- Record worker identity, Blender version, available engines, GPU/CPU mode, and repository commit.
- Mark runtime `AVAILABLE` only after a real probe succeeds.
- If unavailable, leave state `UNAVAILABLE` and continue only with control-plane work.

### Phase 2 — consume the durable queue

Read, in order:

- `docs/agent_handoff/CLAUDE_TOOL_BULLETIN.md`
- `docs/agent_handoff/TOOL_QUEUE.json`
- `docs/agent_handoff/CANONICAL_COMPONENT_PRESERVATION_LAW.md`
- `docs/agent_handoff/DONOR_FIRST_EXECUTION_LAW.md`
- `docs/evidence/MARS_ORAL_KNOWN_GOOD_RECOVERY.json`

Do not invent a competing queue in the UI.

### Phase 3 — wire real runtime state into Command Center

Replace `UNAVAILABLE` only with actual backend evidence:

1. repository manifests / deterministic receipts
2. worker/job API
3. render outputs
4. QC/evidence receipts
5. realtime transport only if actually used by production

Required visible states: `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `BLOCKED`, `UNAVAILABLE`.

Every terminal job should expose:

- job ID
- requested commit/ref
- worker ID
- start/end timestamps
- command or operation identifier
- exit/status result
- log location
- artifact paths
- artifact hashes
- evidence manifest
- retry count
- failure reason when applicable

### Phase 4 — make retries safe

Implement bounded retry semantics around real jobs:

- retry failed jobs only when the failure is retryable;
- never retry a deterministic validation failure as if it were transient;
- preserve every attempt receipt;
- never turn `FAILED` into `PASS` because a later attempt was not observed;
- cancellation must remain distinguishable from failure;
- a stuck worker must be reported as `BLOCKED`/`UNAVAILABLE`, not `SUCCEEDED`.

### Phase 5 — MARS handoff readiness

When Claude/Blender is available, the Command Center must be able to launch and observe the existing MARS routes without rewriting them:

- rig-face AST preflight
- oral render-visibility persistence gate
- pixel-truth render
- oral aperture survey
- canonical lip-crease candidate analysis
- component registration/provenance
- protected-component integrity checks

Rocket must not invent new MARS geometry logic merely to make the UI appear complete.

### Phase 6 — evidence ingestion

For every real render/validation result, ingest the actual JSON/PNG/MP4/Blend artifact references and hashes. Preserve provenance back to the job, commit, worker, and operation. Visual evidence outranks a numerical-only claim.

Blender supports background/command-line rendering and automation, including remote/headless rendering; the worker adapter should use the production runtime's real Blender invocation rather than a simulated renderer.

## Continuous-work rule

After each completed safe task, immediately take the next unblocked task from `TOOL_QUEUE.json` or the command-center integration queue. Do not wait for the owner to repeat the prompt. Stop only when:

- an owner decision is genuinely required,
- the next action would mutate protected canonical assets without a validated route,
- the real runtime is required and unavailable, or
- the repository has reached a clean, evidenced handoff point.

When blocked by unavailable cloud/Blender, continue hardening contracts, adapters, schemas, evidence ingestion, retry logic, UI state mapping, and tests. Do not fake the blocked runtime work.

## Handoff receipt

When Rocket resumes after cloud recovery, publish a receipt containing:

- cloud runtime status
- worker identity/version
- repo commit
- commands actually executed
- artifacts actually produced
- artifact SHA-256 values
- gates actually run
- failures/retries/cancellations
- next queue item

A UI status without this receipt is not production evidence.
