# Gaussian Splat World / Environment Stack

This lane adds a complete open-source capture → reconstruction → Gaussian training/rasterization → Blender animation handoff path to the TRIPPEDD umbrella. It is an environment lane, not a replacement for the canonical Blender production runtime.

## Whole upstream projects

### gsplat
Repository: https://github.com/nerfstudio-project/gsplat

Pinned at commit `28e794ca44a4c25ffc39175370c5ee7b38bfcc36` under `third_party/oss/gsplat`. Apache-2.0.

Use as the high-performance CUDA Gaussian rasterization/training core. Its upstream examples cover COLMAP captures, fitting a 2D image with 3D Gaussians, and large-scene rendering. The large-scene path is particularly important for the C-generated Gaussian-splat world concept: the environment can remain a splat representation while cameras and animated geometry are authored in Blender.

### OpenSplat
Repository: https://github.com/WebODM/OpenSplat

Pinned at commit `687cc91bbe665cff928998536b6e8bd5bbeb942e` under `third_party/oss/OpenSplat`. AGPL-3.0.

Use as the portable C++ CPU/GPU training/conversion/reference implementation. It accepts camera poses and sparse points from COLMAP/OpenSfM/ODM/OpenMVG/nerfstudio formats and produces splat scene data. Because AGPL is materially different from the Apache-2.0 gsplat lane, this remains an explicitly isolated alternative/reference implementation until distribution architecture is decided.

## World pipeline

`capture frames/video`
→ `camera + sparse reconstruction`
→ `COLMAP/compatible scene package`
→ `OpenSplat or gsplat`
→ `Gaussian world artifact`
→ `world manifest + camera calibration + hashes`
→ `Blender environment adapter`
→ `animation / camera / lighting / compositing`
→ `actual-pixel evidence`

The pipeline must support both:

1. **2D-origin worlds** — a single image, plate, matte, concept image or generated map becomes a depth-aware Gaussian/geometry environment for animation and camera movement.
2. **3D-origin worlds** — phone/video/photo capture becomes a reconstructed Gaussian environment that can be combined with Blender geometry, characters, particles, fluids, cloth and lighting.

## Blender boundary

Gaussian worlds are treated as **environment data**, not canonical character geometry. Blender remains the animation and composition authority.

Adapters must provide:

- world import/reference without mutating source captures;
- camera pose/calibration transfer;
- world scale and coordinate-system metadata;
- source/output SHA-256 values;
- deterministic command and upstream commit;
- splat count and bounding-volume measurements;
- representative front/side/three-quarter camera renders;
- actual-pixel evidence showing the Gaussian world in the production scene;
- rollback to the original capture package.

A splat world must never silently become the authoritative MARS mesh. Character geometry remains governed by the existing mesh, face-linework, rig, collision and visual evidence laws.

## C-generated world lane

The phrase “C-generated Gaussian world” is implemented as a portable compute lane rather than a single hard-coded renderer:

- C/C++ OpenSplat remains available for CPU/GPU portable reconstruction/training.
- CUDA gsplat provides high-throughput rasterization/training where NVIDIA acceleration is available.
- COLMAP-compatible camera/sparse-point data is the interchange contract.
- Blender receives camera/world references through a thin adapter instead of copying upstream internals.
- Future GPU/CPU backends can be added as isolated whole repositories without changing the production evidence contract.

## 2D ↔ 3D bridge

The world system should preserve the relationship between:

- source image pixels;
- camera calibration;
- sparse 3D points;
- Gaussian centers/covariances/colors;
- optional depth/geometry derivatives;
- Blender camera transforms;
- rendered evidence pixels.

This allows an animator to use a 2D plate as the starting point, move into a 3D Gaussian environment, add true Blender geometry where needed, and return to a 2D composite without losing provenance.

## Integration gates

1. `LICENSE_OK`
2. `UPSTREAM_COMMIT_PINNED`
3. `CAPTURE_HASH_RECORDED`
4. `CAMERA_CALIBRATION_RECORDED`
5. `WORLD_OUTPUT_HASH_RECORDED`
6. `COORDINATE_SYSTEM_RECORDED`
7. `WORLD_SCALE_RECORDED`
8. `GAUSSIAN_COUNT_RECORDED`
9. `NUMERICAL_QC`
10. `ACTUAL_PIXEL_EVIDENCE_QC`
11. `BLENDER_HANDOFF_QC`
12. `SOURCE_PRESERVATION_QC`
13. `NO_STALE_SCENE_OR_CACHE`
14. `UNKNOWN_NEVER_PASS`

## Agent division of labor

Claude/Jules can perform the visual/surgical Blender work: camera solving, scene composition, geometry placement, animation, rigging, and actual visual review.

The support lane provides the complete upstream projects, pinned provenance, interchange contracts, adapters, evidence receipts, and deterministic orchestration so the visual agent can work from a rich toolbox instead of rebuilding infrastructure by hand.

## Next expansion targets

Keep filling the world stack with complete open-source projects for:

- photogrammetry and camera solving;
- Gaussian editing/compression/viewer tooling;
- depth estimation and monocular 2D-to-3D conversion;
- terrain/biome/river/world generation;
- procedural cities and architecture;
- vegetation/scattering;
- atmospheric/weather systems;
- texture/material generation;
- camera tracking;
- compositing and color management;
- 2D/Grease Pencil animation;
- USD/glTF/scene interchange.

Every candidate follows the same whole-repository policy: pin the complete upstream project, preserve its license, add a narrow adapter, and do not call the integration production-ready until reproducible numerical and actual-pixel evidence exists.
