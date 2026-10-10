# Open-source toolchain candidates

This is a research/selection record only. No third-party code is copied into the production asset without license review and an isolated smoke test.

## Facial rigging

- ShapeUp — https://github.com/dan283/ShapeUp — FACS shape-key management, hero/combo/inbetween concepts.
- facial-animation / Tripo Face Rig — https://github.com/mdj128/facial-animation — procedural facial rigging, expression sheets, render atlas, verification scripts.
- FacialAutoRigger — https://github.com/joeedh/FacialAutoRigger — Blender facial autorigging research; MIT.
- ARKit Creator — https://github.com/tsikerdekis/ARKit-Creator-Blender-Addon — ARKit blendshape baking workflow.

## Hair / dynamics

- Blender 5.2 Geometry Nodes Hair Dynamics / XPBD — native experimental hair physics with surface attachment, pinning, bending, collision and effectors.
- HairRigAddon — https://github.com/latidoremi/HairRigAddon — mesh/particle hair control patterns; useful as reference, not authority.
- Blender APX Addon — https://github.com/ArdCarraigh/Blender_APX_Addon — APX cloth/hair import/export and XPBD-related tooling; isolate and license-review before adoption.

## Mesh quality / derived working geometry

- Remi — https://github.com/shaderko/remi-blender-addon — repair/retopo/decimation while preserving source as a separate result.
- QRemeshify — https://github.com/ksami/QRemeshify — QuadWild-based quad remeshing. Derived cages only; NEVER replace MARS_source.glb.
- BlenderKit Final Topology — https://github.com/BlenderKit/final_topology — topology/retopo utilities; evaluate only on derivatives.

## Selection policy

1. MARS_source.glb remains immutable render authority.
2. Every candidate must run in an isolated derivative scene first.
3. No global remesh, rebake, or destructive triangulation on source.
4. Numeric gates and visual gates remain separate.
5. Any visual artifact produced during evaluation should be committed under docs/evidence/visual with a manifest/hash when the GitHub write path is available.
6. A third-party tool is adopted only after license compatibility, reproducibility, performance, and source-preservation tests pass.
