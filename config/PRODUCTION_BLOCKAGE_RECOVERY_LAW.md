# Production Blockage Recovery Law

## Rule

A production blockage is an engineering problem to attack, not a stopping point.

Whenever a runtime, connector, dependency, model, file transport, render, ingest, or delivery path blocks a production operation:

1. **Record the blockage immediately** with the exact error, capability, affected artifact, and current fallback.
2. **Immediately search for a bypass**: an existing installed capability, open-source replacement, alternate transport, alternate codec, alternate runtime, local/offline path, or deterministic fallback.
3. **Prefer a working open-source tool over a manual workaround** when it can remove the recurring class of failure.
4. **Build the bypass into the production runtime**, not just the current run, when it is reusable.
5. **Run a real-input smoke test** against the blocked operation before declaring the bypass usable.
6. **Preserve the original path** unless it is proven broken; use capability routing/fallback rather than destructive replacement.
7. **Retry/resume from the latest durable checkpoint** instead of restarting unrelated completed work.
8. **Expose UNKNOWN instead of inventing PASS** when evidence is unavailable.
9. **Report progress and the active recovery action together**. Never report a blockage as the end of the work when a plausible recovery path is available.
10. **Escalate to the operator only when the remaining action genuinely requires an external credential, user authorization, physical file access, or an unavailable capability that cannot be safely substituted.**

## Required recovery order

`existing runtime capability -> alternate installed backend -> open-source replacement -> local/offline transport -> alternate protocol/format -> deterministic fallback -> operator action`

## Drive-specific rule

A Google Drive URL is an asset locator, not a reason to stop. The runtime must support Drive through a dedicated authenticated transport layer. `rclone` is the primary open-source transport candidate because it supports Drive OAuth and unattended/service-account operation. The Google Drive API is the secondary direct API path. If one transport fails, route to the other before escalating.

## Safety / provenance

Bypasses must not silently mutate source assets. Downloads must be checksummed, provenance-recorded, and copied into immutable ingest storage before downstream processing. The original Drive URL and file ID remain part of the asset lineage.

## Success condition

A blockage is considered recovered only after the replacement path produces a measured artifact or a truthful, durable UNKNOWN with the next executable recovery step recorded.
