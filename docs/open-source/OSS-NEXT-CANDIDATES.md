# OSS next candidates

## MiDaS — monocular depth
Repository: https://github.com/isl-org/MiDaS

MIT-licensed source for monocular depth estimation. Use only as a derivative measurement lane for depth ordering, segmentation seeds, camera/reconstruction assistance and compositing. Do not treat predicted depth as canonical MARS geometry. Before pinning: record the exact upstream commit, model-weight license/provenance, inference command, input/output hashes and a depth-error QC receipt.

## Shatter It — procedural fracture
Repository: https://github.com/gyomh/shatter-it

GPLv3 Blender 5+ addon for Voronoi shattering and rigid-body setup. Use only on duplicated/derived scene objects. Before pinning: record exact upstream commit, dependency/license inventory, Blender version, fragment-count/determinism measurements, collision smoke test, and actual-pixel fracture evidence.

## Adoption rule

Neither candidate is a production-authoritative submodule until its source commit and all required licensing/QC evidence are known. `UNKNOWN` remains `NEVER PASS`.
