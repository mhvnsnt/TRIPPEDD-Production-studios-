# MARS Mesh Quality Law

## Problem
Rigging operations must not silently replace the authoritative render surface with a triangulated or decimated proxy. Large visible triangles are a visual regression even when polygon count increases.

## Canonical roles
1. **Render surface** — highest-quality supplied MARS geometry and textures. Preserve topology, UVs, normals, material assignments, and texture resolution unless a measured gate authorizes a change.
2. **Deformation cage** — separate low-resolution control surface for rig/Surface Deform work. It is never the canonical render mesh.
3. **Donor/anatomy geometry** — eyes, oral structures, lashes, and other inserts. These must not force a global remesh of the render surface.

## Hard rules
- Never voxel-remesh or globally triangulate the canonical render surface to solve a local rigging problem.
- Never use triangle count as a proxy for visual quality.
- Preserve the uploaded/source mesh as an immutable baseline and compare every rebuild against it.
- Prefer quad-preserving local topology edits, shrinkwrap, corrective shapes, Surface Deform, lattice, and weighted deformation over destructive remeshing.
- If a proxy cage is required, bind it to the render surface and keep the render surface at source resolution.
- Texture coordinates and texture bytes are first-class evidence. A geometry rebuild that changes UVs/material slots is a regression unless explicitly measured and approved.
- Compare silhouette, curvature, normal continuity, UV preservation, material-slot identity, and projected texture detail before/after.
- Any visual regression is FAIL even if numerical geometry gates pass.

## Quality target
The goal is not PS1-level geometry. The goal is a high-quality supplied model rendered with intentional stylization. Low-poly behavior may be a deliberate art direction choice later; accidental large triangles are not.
