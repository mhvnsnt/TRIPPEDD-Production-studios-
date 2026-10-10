# Topology Repair / Anti-Sliver Workflow

The current MARS eye defect is a source-topology problem, not a subdivision problem. The repair lane must therefore remesh the localized pathological patch before any refinement.

## Tool ladder

1. **PyMeshLab / MeshLab** — inspect, clean, repair, and establish a reproducible baseline.
2. **CGAL isotropic remeshing** — primary quality reference. Use local patch remeshing with protected feature polylines and a sizing field.
3. **CGAL Delaunay surface remeshing** — alternate high-quality triangle reconstruction when isotropic local edits are insufficient.
4. **Instant Meshes** — field-aligned retopology candidate when deformation-friendly edge flow is preferable.
5. **Open3D** — independent geometry/registration/normal/intersection checks.
6. **OpenSubdiv** — only after topology passes; never as the first repair for slivers.
7. **Blender/Rigify** — deformation and facial-rig integration only after the patch is healthy.

CGAL's remeshing algorithms explicitly support local patch remeshing, edge split/collapse/flip operations, vertex relocation, sizing fields, and protected feature polylines. The vertices can be reprojected to the original surface to retain geometric fidelity. This makes it suitable for the MARS eye patch where painted lid curves and the existing globe are protected. 

## Protected anatomy

Never allow remeshing to move these authorities without a measured transfer/reprojection result:

- painted upper/lower lid curves
- canthi
- eyebrow boundaries
- eyeball/globe surface
- iris/pupil landmarks
- position-map correspondence
- existing good facial regions
- UV islands
- existing expression/shape-key targets

## Sliver diagnosis

Do not fix a 0.72-degree triangle by adding subdivision. Subdivision multiplies the pathological topology. The repair pass should improve triangle-angle distribution and edge-length regularity first.

The eye patch should report at minimum:

- face count
- vertex count
- minimum triangle angle
- p01/p05/p50 triangle-angle percentiles
- fraction below 5/10/15 degrees
- edge-length mean/median/std/CV
- non-manifold edges
- self-intersections
- duplicate vertices
- normal flips
- protected-curve deviation in mm
- globe clearance
- UV distortion/coverage
- transferred shape-key error

## Promotion rule

A remesh is a **candidate**, not a replacement. It must beat the source on topology quality while staying within anatomy, UV, shape-key, and clearance tolerances. Rendered wireframe and shaded evidence are mandatory.

If a candidate improves topology but moves an eyelid onto the brow, changes the mouth, loses gums/teeth/tongue, damages UVs, or changes the eyeball fit, it FAILS.
