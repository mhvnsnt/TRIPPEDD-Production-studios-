# OpenAssetIO + OpenTimelineIO bridge

TRIPPEDD should treat the upstream OpenAssetIO/otio-openassetio project as the
experimental horizontal bridge between asset identity and OTIO media references.

Upstream: https://github.com/OpenAssetIO/otio-openassetio
License: Apache-2.0
Maturity: alpha / isolated-adapter only.

Contract:
1. OTIO remains the editorial interchange format.
2. OpenAssetIO remains the asset-identity resolver.
3. The bridge may resolve an assetized OTIO reference.
4. An unresolved identity is a QC failure; it must never silently become a guessed filesystem path.
5. This adapter is not promoted to episode production until its upstream tests and a real TRIPPEDD OTIO round-trip pass.

This is deliberately a real upstream dependency, not a copied implementation.
