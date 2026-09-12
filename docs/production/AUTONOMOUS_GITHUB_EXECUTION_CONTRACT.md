# TRIPPEDD Autonomous GitHub Execution Contract

This is the execution escape hatch for production. It does not bypass GitHub authorization or the ChatGPT connector. It makes production independent of either one.

## Control plane

GitHub `workflow_job` webhook -> TRIPPEDD supervisor -> GitHub App installation token -> repository JIT runner -> one production job -> teardown.

GitHub's JIT runner API requires repository Administration: write permission. The supervisor must hold the App private key outside the repository and mint short-lived installation tokens at runtime.

## Required invariants

1. No PAT or private key is committed to this repository.
2. No production job depends on a ChatGPT session remaining connected.
3. A queued job must be reconciled independently of webhook delivery.
4. Every JIT runner is ephemeral and processes one job only.
5. Runner logs and production artifacts are copied to durable storage before teardown.
6. Stale attempts are cancelled only after their checkpoint/artifacts are preserved.
7. A recovery attempt gets a fresh runner; it never resumes on a contaminated runner.
8. Missing/invalid MP4, JSON, OTIO, or QC evidence is FAIL, never PASS.
9. Old telemetry cannot satisfy a new attempt.
10. The 20-second commercial gate remains the cheap E2E proof before an episode run.

## Routing

Production workflows may target a custom label through `vars.TRIPPEDD_RUNNER_LABEL`. The proof gate retains a GitHub-hosted fallback so the pipeline can be validated without the autonomous runner infrastructure. Episode production must set the custom label once the supervisor is live.

## Reconciliation

The supervisor must reconcile queued, in-progress, and completed `workflow_job` state. Webhook delivery is an accelerator, not the source of truth.

## Security

Use a GitHub App, not a long-lived PAT. Keep the App private key on the execution host/secret manager. Generate JIT configuration immediately before runner startup. Destroy the runner and wipe its workspace after the job.

## Proof order

connector/control-plane health -> source gate -> 20-second E2E -> artifact/QC verification -> pilot/EP01 recovery.

Never spend an episode-scale render before the proof gate is green.
