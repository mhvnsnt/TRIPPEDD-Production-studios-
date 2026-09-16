# Depth / Fracture Evidence Contract

This contract wires the pinned MiDaS and Shatter It upstreams into production without making either derivative output an authority over canonical MARS geometry.

## MiDaS

Upstream: `third_party/oss/MiDaS`

Authority: `DERIVATIVE_DEPTH_EVIDENCE`

Required receipt fields:

- exact 40-hex upstream commit
- separately verified model-weight provenance/license status
- exact inference command
- input SHA256
- output SHA256
- depth-error QC measurements against a characterized reference where available
- visual-evidence SHA256
- `canonicalSourceMutated: false`

MiDaS depth may assist camera geometry, segmentation, occlusion reasoning, or reconstruction. It may not rewrite `MARS_source.glb` or become anatomical truth.

## Shatter It

Upstream: `third_party/oss/shatter-it`

Authority: `DERIVATIVE_FRACTURE_OUTPUT`

Required receipt fields:

- exact 40-hex upstream commit
- Blender version
- dependency/license inventory
- exact command
- deterministic result declaration
- fragment count
- collision/rigid-body smoke-test result
- input/output SHA256
- visual-evidence SHA256
- `canonicalSourceMutated: false`

Shatter It may fracture duplicated/derived scene objects only. Canonical MARS geometry remains untouched. Fragment count, determinism, collision behavior, and actual pixels are required before production adoption.

## Gate

`tools/oss/depth_fracture_gate.py` is fail-closed. `UNKNOWN` is never `PASS`. A receipt with missing provenance, hashes, numerical QC, visual evidence, or canonical-source protection cannot pass.
