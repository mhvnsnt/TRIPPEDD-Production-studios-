# 2026-09-09 — Compute failover and Actions-minute protection

## Producer direction

GitHub Actions minutes must not be the single point of failure for episode production. The studio should keep finishing the current episode while building a path that can continue when hosted runner capacity or minutes are unavailable.

## Live EP01 state

Canonical Story Runner run `34394290662` reached 12/12 successful subjectivity chunks and assembled the 144-frame subjectivity sequence. The build job is now in the resumable Bastard terminal-tag stage. No restart was issued.

## Compute strategy

TRIPPEDD now defines four complementary open/self-hosted compute paths:

1. **GitHub Actions** — canonical hosted orchestration while capacity is available.
2. **Local production fallback** — direct execution on a production workstation/server, with the same frame contracts and resumable chunking.
3. **Flamenco** — Blender-focused self-hosted render management for network workers. Blender Studio documents Flamenco as free/open-source, cross-platform and self-hostable, and uses it in production.
4. **OpenCue** — distributed render/task management for larger multi-machine or hybrid farms.
5. **act** — local Docker execution of compatible GitHub Actions workflows for workflow parity/testing; it is not treated as the render farm itself.

## Implemented

- `config/compute-backends.json` records the backend policy and promotion gates.
- `scripts/production/local-ep01-fallback.sh` provides a direct local EP01 pipeline that does not require GitHub-hosted runners.
- `scripts/production/local-bastard-tag.sh` reproduces the resumable 12-chunk Bastard frame contract locally and assembles the final H.264 tag.

## Cost-control law

Do not start a second hosted run merely because a step is slow. Preserve completed artifacts, inspect measured state, and use local/farm execution when hosted capacity is exhausted or intentionally unavailable.

## Evidence gates

A backend becomes production-grade only after installation/provisioning, a real EP01 smoke test, measured artifact output, recovery validation, and compatibility with the canonical deliverables. The studio does not claim a service is production-ready merely because its repository exists.
