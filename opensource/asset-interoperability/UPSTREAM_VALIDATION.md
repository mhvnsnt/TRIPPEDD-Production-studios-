# Upstream validation — OpenAssetIO / OTIO

## Status
- OpenAssetIO: production-grade upstream; current release line includes v1.0.2.
- OpenAssetIO-MediaCreation: companion trait/specification package.
- OpenAssetIO/otio-openassetio: **alpha / isolated adapter only**.
- OpenRV integration: candidate only; upstream issue #1501 remains open.

## TRIPPEDD promotion rule
An upstream project is not considered integrated merely because it is cloned.
Promotion requires:
1. pinned revision;
2. successful upstream tests;
3. TRIPPEDD adapter healthcheck;
4. representative media/asset round-trip;
5. artifact provenance;
6. production workflow consumption.

The OTIO/OpenAssetIO bridge therefore remains isolated until its round-trip passes.
