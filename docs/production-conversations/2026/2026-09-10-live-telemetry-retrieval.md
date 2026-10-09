# Live Production Telemetry Retrieval — 2026-09-10

## Decision

TRIPPEDD production cannot depend on GitHub Actions log blobs as its live telemetry API. A running Actions job can legitimately report an unavailable log blob even while the job is still executing. Therefore the production ledger remains canonical and is mirrored to a durable, retrievable GitHub Issue comment.

## Canonical data

The production ledger is still the source of truth. Each active stage reports measured:

- percentage
- completed / total work
- elapsed time
- throughput
- ETA
- current operation
- heartbeat
- artifact size when available

Missing measurements remain `UNKNOWN`.

## Durable retrieval channel

Issue #16 (`TRIPPEDD Live Production Telemetry`) is the live retrieval channel. `scripts/production/publish-live-telemetry.sh` updates one stable comment identified by `<!-- trippedd-live-telemetry -->`; it does not create an unbounded comment stream.

`scripts/production/watch-progress.sh` now starts the publisher asynchronously so a slow GitHub API call cannot block or distort the production command. The ledger is still local/canonical; publication is best-effort and observable.

The EP01 Story Runner workflow grants `issues: write` and passes `GITHUB_TOKEN` to the build/watcher environment.

## Why not treat the Actions log API as canonical?

The repository has repeatedly returned `BlobNotFound` for a live job's log endpoint. That is a transport/retrieval failure, not evidence that the production process is healthy or dead. The system therefore separates execution health from log transport health.

## Open-source observability direction

OpenTelemetry is the long-term vendor-neutral instrumentation layer for TRIPPEDD. It supports metrics, traces and logs and can export to Prometheus or another backend. The immediate GitHub Issue channel is deliberately simpler and requires no external hosted service, while the architecture leaves room for OTLP/Prometheus as a second independent telemetry sink.

Reference: https://opentelemetry.io/

## Operating law

> If the measured ledger cannot be retrieved, do not invent a percentage. If the process cannot expose measured progress through at least one durable channel, it is not eligible to be called actively healthy.

## Current EP01 note

Run `34428807358` predates the final nonblocking publisher hardening, so its live fractional production percentage remains `UNKNOWN` through the current retrieval tools. The active run is left untouched to avoid wasting completed work. The next production run will publish its measured ledger through Issue #16 from startup.
