# Gaussian / Procedural World Stack

## Purpose

Give the production runtime a complete open-source environment lane for both measured 2D imagery and generated worlds. The lane is intentionally hybrid: a shot can begin as photographs/video, a hand-authored 2D plate, a procedural map, or a mixture, then become a camera-aware 3D Gaussian environment and/or conventional Blender geometry.

## Whole-project upstreams

- `gsplat` — CUDA Gaussian rasterization and 2D-to-3D Gaussian fitting.
- `OpenSplat` — portable C++ CPU/GPU Gaussian reconstruction and scene export.
- `Worldsmith` — deterministic terrain, climate, rivers, biomes and heightmap generation.
- `bene-proggen-maps` — procedural cities, streets, buildings, terrain, dungeons and export.
- `SkySplat-Blender` — Blender-side 3DGS/video/camera workflow. It remains REVIEW_REQUIRED because its documented workflow depends on external COLMAP and Brush binaries.

## Division of labor

The environment stack supplies tools and reproducible inputs. Claude's visual lane owns the hands-on Blender work: camera placement, character/environment integration, rigging, materials, animation, composition, and visual correction. This repository owns the machinery that makes those operations reproducible, measurable and recoverable.

## Canonical flow

`2D/video/procedural source -> source manifest -> reconstruction/procgen -> Gaussian or mesh world -> Blender handoff -> animation -> render -> actual-pixel evidence`

A Gaussian world is not treated as an editable substitute for canonical character geometry. It is a world/environment representation that can coexist with conventional Blender geometry, collision proxies and animated characters.

## Evidence law

Every adopted world output must carry source and output hashes, exact command/version, reconstruction parameters, numerical QC, camera/coordinate metadata, and actual rendered evidence. Missing measurements or visual evidence remain `UNKNOWN`.

## Dependency law

Whole upstream repositories are pinned as gitlinks. We do not silently copy a few files and call that integration. External binaries and dependencies must be separately licensed/audited before becoming production-authoritative.
