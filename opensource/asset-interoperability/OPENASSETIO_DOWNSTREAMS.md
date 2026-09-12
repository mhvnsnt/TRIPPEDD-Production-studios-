# OpenAssetIO downstream integration candidates

Research-backed downstream pieces for the TRIPPEDD asset boundary.

- OpenAssetIO-ComfyUI: OpenAssetIO-aware workflow nodes for resolve/publish.
- OpenAssetIO OTIO plugin: prototype media-linker path for assetized OTIO.
- FPT OpenAssetIO manager: reference manager/plugin pattern for production tracking.
- OpenAssetIO Test CMake: CI-oriented consumer test for CMake/package integration.

Adoption rule: downstream projects remain upstream-owned and versioned; TRIPPEDD integrates them through adapters. Promote only after an isolated health test and representative media test.

The OpenAssetIO project itself uses downstream integration testing as part of its compatibility strategy, which supports this approach.
