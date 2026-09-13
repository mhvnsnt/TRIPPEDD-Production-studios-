# Agent queue

This file is the handoff surface for Jules, Claude Code, browser IDEs, and future workers.

## Rules

- Work from `main` unless a task explicitly names another branch.
- Never force-push or force-merge divergent history.
- Read `AGENTS.md` first.
- UNKNOWN is never PASS.
- A UI screenshot is not render evidence.
- Face/linework work must preserve source-image provenance and SHA-256 hashes.
- Every task must leave a test, measurement, or concrete artifact behind.
- Optional open-source dependencies must fail closed when unavailable.

## Priority queue

### P0 — locate authoritative Mars linework bytes
**Goal:** Find the exact committed files `6b9612a8-1f78-4b39-96a6-175b9fb18fc3.png` and `f4724cea-263e-4b09-9438-0328c8c0749d.png` in the accessible Git history/repositories.

**Do:** search repository code, commit history, branches, and accessible related repositories. Record exact repo/ref/path/commit/SHA-256. Do not recreate or redraw the linework.

**Stop:** if bytes cannot be accessed, record `SOURCE_BYTES_UNAVAILABLE`; do not infer the markings.

### P0 — linework registration
Use the exact source bytes to produce an overlay against the MARS mesh/reference image, semantic landmark JSON, registration error, and a rendered proof image. Numerical registration cannot override a visibly wrong overlay.

### P1 — motion proof
Extend the existing motion proof path so linework-derived eyelid/brow/nostril landmarks are checked across a short rendered sequence, not only a still.

### P1 — toolchain adapters
Add optional Open3D/scikit-image/libigl adapters behind explicit availability gates. Do not make large research dependencies mandatory for baseline boot.

### P1 — evidence cockpit
Expose source path, commit, SHA-256, dimensions, registration status, and motion-proof status in the production cockpit.

### P2 — dependency gardening
Periodically verify upstream licenses/releases and remove redundant or broken dependencies. Prefer fewer working paths over many nominal integrations.
