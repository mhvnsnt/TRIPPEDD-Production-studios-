# Connector-Independent GitHub Execution

TRIPPEDD is deliberately not dependent on the ChatGPT GitHub connector being available during a production run.

This is **not a security bypass**. It is a legitimate execution boundary using a GitHub App installation that is explicitly authorized for the repository.

## Runtime

```
workflow_job: queued
        |
        v
TRIPPEDD supervisor
  - verify HMAC signature
  - deduplicate delivery ID
  - enforce repository allowlist
  - match production runner label
        |
        v
GitHub App installation token
        |
        v
generate JIT runner configuration
        |
        v
one-job ephemeral runner
        |
        v
TRIPPEDD production
```

GitHub's REST API supports repository-level JIT runner configuration using a GitHub App installation access token, with repository Administration: write permission. GitHub also documents that JIT runners process at most one job and are then removed.

## Hardened rules

1. `TRIPPEDD_ALLOWED_REPOSITORY` is mandatory. Missing allowlist fails closed.
2. The App private key must be owner-only readable.
3. The runner installation must contain an executable `run.sh`.
4. The JIT configuration is never written to disk.
5. Installation access tokens are requested only for the target repository.
6. Webhooks require HMAC-SHA256 verification.
7. GitHub delivery IDs are deduplicated for 24 hours.
8. Only queued `workflow_job` events carrying the configured production label can provision a runner.
9. The production artifact/QC path remains independent of the ChatGPT session.
10. Ephemeral runner hosts must be treated as disposable/clean between jobs.

## Proof contract

The hardened bridge check is:

`TRIPPEDD_CONNECTOR_INDEPENDENT_BRIDGE_HARDENING=PASS`

with explicit checks for repository allowlisting, private-key protection, JIT credential non-persistence, and webhook authentication/idempotency.
