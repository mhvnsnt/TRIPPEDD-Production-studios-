# 2026-09-09 — EP01 finish push + OSS pass 2

## Producer direction

Keep the production moving toward a correct finish while continuously improving the studio with open-source infrastructure where it materially improves throughput, recovery, observability, or future network-scale production.

## EP01 live state at this pass

- Story Runner run `34394290662` remains active.
- All 12 subjectivity chunk jobs completed successfully.
- Active build job `102640267853` has completed setup, caches, media stack, subjectivity assembly, Bastard terminal tag, and Node dependency installation.
- `Build Story Runner cut` remains the only active production step; Verify and Upload have not started.
- No blind rerun or cancellation is justified. GitHub's job-log endpoint is a temporary redirect resource, so a missing live log blob is not itself evidence that the runner is stalled.

## OSS / compute pass

- Reconfirmed Flamenco as the Blender render-farm candidate and researched the current stable release: 3.9.3.
- Updated `config/compute-backends.json` to schema v2 and pinned Flamenco 3.9.3 / GPL-3.0 as the current production candidate target.
- Promotion remains evidence-gated: installation/reprovisionability, real EP01 smoke test, measured output, recovery, canonical artifact compatibility, and no regression.
- OpenCue remains the distributed render/task-farm candidate; `act` remains the workflow-reproduction candidate; local scripts remain the immediate full-production fallback.

## Operating rule

GitHub Actions remains canonical while healthy and available. When capacity or budget becomes the binding constraint, the studio should route work to local/farm backends rather than waste Actions minutes on blind retries. Completed caches/checkpoints remain reusable across backends.

## Creative integrity

Story Runner and Autonomous remain independent editorial cuts. Reusing verified Story Runner-produced media assets is allowed; reusing the finished Story Runner edit as the Autonomous editorial source is not.
