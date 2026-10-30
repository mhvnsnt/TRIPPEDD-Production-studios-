# TEST LOG — Sculpt Finisher (Z-2) + FlowRetopo (Z-1)

Real headless run, 2026-10-30. Raw Blender output: `test_run_raw.log`
(this folder). Machine-readable results were written by the test to
`results.json` in its output dir (hashes below).

- Blender: **4.5.3 LTS** (`~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`)
- Invocation: `flock /tmp/heavy-test.lock bash -c 'xvfb-run -a env -u PYTHONPATH
  <blender> -b --factory-startup --python test_finisher.py -- --out <out>'`
  (free RAM checked inside the lock before launch; box was shared with
  other lanes, run serialized on the lock as required)
- Test sculpt: icosphere subdivisions=5 + Clouds-texture Displace
  (strength 0.3, applied) + painted POINT vertex colors in an attribute
  named `Density`, plus a material reading that attribute (color-bake
  source). **Before: 2562 verts / 5120 tri faces.**

## Z-2 — full chain: `TEST_ALL_PASS`

Steps, in order, all OK: voxel_remesh (2562 → 1482 verts) → quadriflow
(→ 1670 verts / 1588 faces, target 1500) → uv_unwrap_pack → multires
(1 level) → bake → export.

- Finished object `BlobSculpt_FINISHED`: **1670 verts / 1588 faces, all
  quads**; original verified untouched (2562 → 2562 verts).
- Mesh check honestly reported: `non_manifold_edges=160` — all 160 are
  boundary edges (`boundary_edges=160`), i.e. QuadriFlow left open seams
  on this noisy displaced blob; no loose verts, no degenerate faces.
  The check surfacing this is the point of the report, not a pass/fail
  gate.
- Artifacts on disk (output dir, not committed — sizes + SHA-256):

| File | Bytes | SHA-256 |
|---|---|---|
| `export/BlobSculpt_FINISHED.glb` | 109168 | `2718d2382b0de111cf1eefe059825a162ee48d856d27377effaba0adae8504fc` |
| `bakes/BlobSculpt_FINISHED_Normal.png` | 222525 | `fa40bba0beb9f6907ca4a6df07b8334ff9bdbde308b5ee3454ffe40ecd6054a8` |
| `bakes/BlobSculpt_FINISHED_AO.png` | 131670 | `44e59af38fc430fd7887ed1cde79579a58a15087d43e6ed9f91b493b774e6f40` |
| `bakes/BlobSculpt_FINISHED_Color.png` | 135114 | `6a733323e5e0b86345afb7ed69540e12ecc08873bbac40f051062e7b5f98a859` |
| `results.json` | — | `c5b600c2d430efee239b5f310a225b6513102ac578dc6433d50ac7fbc13fab4d` |

Bakes: 512×512, Cycles CPU, 8 samples, selected-to-active from the
original high-res sculpt, ray distance 0.3.

## Z-1 — FlowRetopo: PASS, Instant Meshes leg RAN

- Density: read from the `Density` vertex colors — mean luminance 0.500
  → factor 1.00 → target 1200 faces (base 1200), logged.
- QuadriFlow (symmetry X, via the mesh mirror flags — Blender 4.5's
  QuadriFlow operator has no `symmetry_axis` argument): → **1188 verts /
  1122 quad faces**, non-manifold/boundary 128.
- **Instant Meshes: RAN for real.** Official free pre-built Linux binary
  (upstream README's S3 link; installed at
  `~/workspace/tools/instant-meshes/Instant Meshes`, `--help` and a
  standalone OBJ batch round-trip verified before this run). Round-trip
  inside Z-1 produced 4758 verts / 4591 quad faces with 330 boundary
  edges — worse than QuadriFlow's 128, so per the wrapper's adopt-only-
  if-cleaner rule the **QuadriFlow result was kept**, with both counts
  logged. (IM overshoots the `-f` target because its pure-quad step
  subdivides; noted, not hidden.)

## Fail-soft probe: PASS

Z-2 re-run with the export dir pointed at an existing **file**: chain
stopped at step `export` (`[Errno 17] File exists`), operator returned
`CANCELLED`, duplicate kept as `BlobSculpt_FAILED_export`, original
still 2562 verts.

## Blender 4.5 API notes found by this build (fixed in code, commented)

- `quadriflow_remesh` has no `symmetry_axis` kwarg; symmetry axis is
  `Mesh.use_mirror_x/y/z`.
- `MultiresModifier.subdivision_type` was removed (≥4.3); Catmull-Clark
  is the only type.
- Bake ray distance is `RenderBakeSettings.max_ray_distance`.
- Chain failures report `{'WARNING'}` + `CANCELLED`, not `{'ERROR'}`:
  an ERROR report raises `RuntimeError` for scripted `bpy.ops` callers
  and would break the fail-soft contract for orchestration lanes.
