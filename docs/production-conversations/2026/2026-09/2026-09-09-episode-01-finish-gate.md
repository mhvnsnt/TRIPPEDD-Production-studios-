# EP01 finish gate — 2026-09-09

## Live production gate
Canonical Story Runner run: `34394290662`.

Observed state at the latest check:
- 12/12 subjectivity chunk jobs completed successfully.
- Subjectivity assembly completed successfully.
- `build-ep01-story-runner` remains in progress.
- `Build Bastard terminal tag (resumable)` is the active step.
- Node dependency install, Story Runner assembly, verification, and upload have not started yet.

## Operating rule
Protect the active render. Do not cancel or blindly rerun it. Preserve all completed chunk artifacts/checkpoints. If the terminal-tag step fails, diagnose the actual failed step and rerun only the failed job when safe.

## Completion definition
EP01 is not declared finished until:
1. Bastard terminal tag succeeds.
2. Story Runner cut succeeds.
3. Verification succeeds.
4. Final Story Runner artifact is uploaded.
5. Automatic technical QC succeeds against the final artifact.

## Compute independence
After EP01 is green, validate the self-hosted Flamenco path against the same resumable chunk contract, followed by OpenCue for larger-scale dispatch. The hosted Actions path remains useful as one backend, not the only backend.
