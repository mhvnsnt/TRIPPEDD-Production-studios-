# Rocket Command Center Contract

## Role

Rocket is the TRIPPEDD web/control-plane agent. It does not replace Claude's visual authority or the Blender/GLB production runtime.

Rocket should build the interface and integration layer that lets the production agents observe, launch, validate, and review real work.

## Canonical boundaries

- `MARS_CANONICAL` and production geometry remain canonical.
- Blender, GLB, render outputs, evidence bytes, manifests, and deterministic validators remain production authority.
- Rocket UI state must never masquerade as production evidence.
- Do not invent placeholder MARS measurements when the real artifact is unavailable.
- `UNKNOWN` is never `PASS`.

## Command Center required views

The `/command-center` surface should expose:

1. Overview — current production state and blockers.
2. Render Queue — real jobs, status, logs, outputs, failures, retry state.
3. QC / Evidence — actual artifact paths, hashes, measurements, visual evidence, and gate results.
4. Tool Queue — `docs/agent_handoff/TOOL_QUEUE.json` as the shared work queue.
5. GitHub / PR — branches, commits, PRs, CI state, and review state.
6. Artifacts — manifests and provenance.
7. Agent Handoff — Claude/Rocket bulletin plus last known agent activity.
8. Production Control — safe launch/cancel/retry controls where a real backend exists.

## Live-data rule

Do not replace real production data with hard-coded demo state. If an API/backend is not wired yet, label the state `UNAVAILABLE` and expose the missing integration rather than fabricating success.

Preferred integration order:

`repo manifests / deterministic receipts` → `worker/job API` → `render outputs` → `QC evidence` → `Supabase/realtime if actually used by the production runtime`.

Supabase is optional infrastructure, not the source of truth by itself.

## Rocket → GitHub handoff

Rocket changes should remain reviewable through its normal GitHub branch/PR flow. Do not silently overwrite `main`. Before merging a Rocket PR:

- verify the changed files,
- verify TypeScript/build checks,
- verify existing production routes still work,
- verify no evidence or canonical-character files were replaced by placeholders,
- verify the command center reads the current repository state.

## Current priority

Finish the command center enough that Claude's actual MARS work can be observed without owner babysitting. Next useful lane after the shell UI is live-data wiring to real manifests, queues, QC receipts, render outputs, and GitHub state.
