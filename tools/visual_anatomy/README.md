# Visual Anatomy Worker Architecture

The worker boundary exists so Claude and other agents can use full open-source tools without hand-editing canonical MARS geometry blindly.

## Preferred flow

reference image
  -> immutable hash
  -> CVAT/SAM-assisted annotation
  -> coordinate/curve/mask export
  -> deterministic transparent overlay
  -> independent visual review
  -> 3D correspondence
  -> protected mesh patch/remesh
  -> UV/shape-key transfer
  -> rig/animation
  -> collision and deformation gates
  -> rendered proof

## Critical distinction

AI may propose geometry. It does not get authority to replace the reference image or canonical MARS mesh.

For the transparent-linework workflow, preserve the supplied image exactly and store annotations separately. A generated look-alike image is not an annotation.

## Mesh repair

For the current Tripo eye topology defect, compare MeshLab/PyMeshLab, CGAL isotropic remeshing and Instant Meshes on a derived patch. OpenSubdiv comes after the base patch is healthy.

Protect:
- eyelid curves
- eye globe placement
- iris/pupil
- eyebrow boundaries
- existing good mouth/nose geometry
- UVs
- existing shape keys

Reject any repair that improves triangle statistics but moves protected anatomy beyond tolerance.

## Hair

Hair is instance data, not one connected blob:
- HAIR_ROOT
- HAIR_LOCK_N
- root
- centerline
- tip
- motion vector
- collision surface

NECK, EAR_L, EAR_R and FACE_SKIN are explicit exclusion regions.

## Provenance

Every worker result should record source project, revision, model/checkpoint, parameters, reference hash, output hash and gate results.
