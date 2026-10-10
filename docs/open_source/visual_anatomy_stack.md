# Visual Anatomy / Rigging Open-Source Stack

This lane prevents agents from hand-authoring geometry or regenerating reference images when deterministic/open-source tools can measure, segment, annotate, remesh, or validate them.

## Immutable-reference rule

The supplied MARS reference image is immutable. Annotation tools may add transparent overlays, masks, points, curves, labels, IDs, and vectors, but MUST NOT regenerate or alter the reference pixels.

## Full projects

- Blender — modeling, UV, animation, cloth, geometry nodes, rendering.
- Rigify — Blender modular rig generation, including facial/eye/jaw mechanisms.
- CVAT Community — self-hosted image/video/3D annotation, masks, polygons, keypoints, QA and APIs.
- Segment Anything 2 — interactive segmentation and tracking backend.
- Open3D — mesh, point-cloud processing, registration and reconstruction.
- MeshLab/PyMeshLab — mesh inspection, cleaning and remeshing.
- CGAL — robust computational geometry and isotropic remeshing.
- Instant Meshes — automatic field-aligned remeshing/topology reconstruction.
- OpenSubdiv — production subdivision surfaces after base topology passes.
- Nerfstudio + gsplat — scene reconstruction and Gaussian-splat environments.
- modl — local image generation/editing, masking, composition and analysis.

## MARS semantic regions

FACE_SKIN; EYEBALL_L; EYEBALL_R; EYELID_UPPER_L; EYELID_LOWER_L; EYELID_UPPER_R; EYELID_LOWER_R; EYEBROW_L; EYEBROW_R; NOSE; NOSTRIL_L; NOSTRIL_R; UPPER_LIP; LOWER_LIP; ORAL_CAVITY; TEETH_UPPER; TEETH_LOWER; GUM_UPPER; GUM_LOWER; TONGUE; HAIR_ROOT; HAIR_LOCK_0001...N; EAR_L; EAR_R; NECK.

Semantic ownership overrides mesh connectivity. Neck is an explicit negative constraint for hair. Every visible dread/lock gets an independent instance ID.

## Hard gates

- Reference pixels unchanged.
- Neck cannot be classified as hair.
- Existing good eyes/mouth/nose geometry is never replaced without evidence.
- Remeshing must preserve protected anatomical curves and transfer UV/shape data.
- Topology quality is measured by triangle-angle, aspect-ratio and edge-length distributions, not polygon count alone.
- A numerical PASS cannot override a rendered visual FAIL.
- UNKNOWN remains UNKNOWN.

## Worker boundary

AI models propose coordinates, masks and curves. Deterministic tooling renders and validates the overlay. A generated replacement image is never accepted as annotation evidence.
