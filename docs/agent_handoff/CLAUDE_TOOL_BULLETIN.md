# Claude Tool Bulletin — MARS / visual anatomy / topology

**Purpose:** This file is the persistent handoff channel for tools discovered by other agents. Claude should read it at the beginning of every relevant turn and use the listed capabilities without waiting for the owner to repeat a prompt.

**Update law:** When another agent adds a tool, adapter, contract, benchmark, or evidence source, update this bulletin in the same change. When Claude discovers a better open-source route, add it here too.

## Current mission
Fix MARS without replacing the immutable visual reference. The current high-risk failures are source-bad facial topology, eye correspondence, oral anatomy separation, and hair/neck classification. Prefer deterministic measured geometry over hand placement.

## Immediate topology stack

### PyMeshLab / MeshLab
**Use for:** reproducible mesh inspection, cleanup, local repair, comparison of source and candidate patches.
**Repo/bootstrap:** `third_party/visual_anatomy/meshlab`, `tools/visual_anatomy/`
**Rule:** use it to diagnose/compare; never accept a repair merely because polygon count increased.

### CGAL
**Use for:** isotropic remeshing, local patch repair, edge operations, feature preservation, Delaunay alternatives.
**Repo/bootstrap:** `third_party/visual_anatomy/cgal`
**Preferred use:** the current eye patch with protected painted lid curves and a measured target edge scale.
**Promotion gates:** triangle-angle improvement, no self-intersections/non-manifold defects, protected-lid displacement within tolerance, surface error bounded, UV/shape transfer preserved.

### Instant Meshes
**Use for:** deformation-oriented retopology / quad-dominant candidate generation.
**Repo/bootstrap:** `third_party/visual_anatomy/instant-meshes`
**Use as:** an independent candidate, not an automatic replacement. Compare against CGAL/PyMeshLab.

### Open3D
**Use for:** independent mesh validation, normals, intersections, geometry statistics and measurement.
**Repo/bootstrap:** `third_party/visual_anatomy/Open3D`
**Role:** second-opinion validator so the remesher cannot certify its own failure.

### OpenSubdiv
**Use for:** subdivision only after base topology is healthy.
**Repo/bootstrap:** `third_party/visual_anatomy/OpenSubdiv`
**DO NOT:** use subdivision to hide source slivers. Current MARS eye source has 324/585 triangles below 15° and a minimum angle of about 0.72°; this is a base-topology problem.

## Visual correspondence tools

### Position-map correspondence
`docs/evidence/place/position_map.npz` is the direct image-pixel -> 3D surface correspondence. Use this before arbitrary raycasts or guessed facial coordinates. It is paired with `docs/evidence/place/MARS_place_plate.png` and `place_plate.json`.

### Painted eye authority
`docs/evidence/blink_own/painted_lid_lines.json` is the authoritative painted lid trace. Do **NOT** use the known-bad `linework_3d.json` as the eye ruler. `PAINTED_FLAT_EYES.png` and `ARBITER_linework_vs_painted.png` are the visual evidence.

### Immutable reference pixels
`docs/evidence/annotations/REFERENCE_PIXELS.json` plus the files in `docs/evidence/annotations/` define the pixel authority. Never regenerate, repaint, restyle, sharpen, beautify, or replace these pixels. Annotation belongs on a transparent layer.

## Annotation / AI proposal stack

### CVAT Community
**Use for:** human/AI-assisted polygons, masks, keypoints, curves and QA.
**Repo/bootstrap:** `third_party/visual_anatomy/cvat`
**Rule:** annotations are proposals/evidence layers, never permission to alter the immutable reference.

### Segment Anything 2
**Use for:** segmentation proposals for facial regions/hair/oral components.
**Repo/bootstrap:** `third_party/visual_anatomy/sam2`
**Rule:** use as proposal generation; verify against semantic anatomy and actual pixels.

### MediaPipe / ONNX face mesh
**Use for:** landmark proposals and independent facial correspondence.
**Repo/bootstrap:** adapter/registry entry; do not allow landmark names alone to determine anatomy.

### MVMP
**Use for:** multi-view MediaPipe landmarks projected back to a real 3D mesh. Useful as an independent correspondence proposal.
**Rule:** compare against position-map and painted traces; do not replace either authority.

## Facial rig references

### Blender Rigify
Use the face/eye/jaw/tongue architecture as a reference for deformation controls and eyelid behavior. Eye closure must follow the measured anatomical axis, not contour traversal winding.

### ICT-FaceKit
Use for facial shape/eye rig donor experiments already present in the project. Preserve side naming based on where shapes actually land.

### mdj128/facial-animation
Use as an architectural reference/candidate for procedural facial rigging, including separated upper/lower teeth and tongue. Do not import a character identity over MARS; extract useful architecture only.

## Oral anatomy rule
Mouth must be structural, not a texture sheet. Candidate architecture must preserve distinct `ORAL_CAVITY`, `TEETH_UPPER`, `TEETH_LOWER`, `GUM_UPPER`, `GUM_LOWER`, and `TONGUE`, with jaw-open render evidence. Physical coverage alone is insufficient; actual pixels must read as separated anatomy.

## Hair rule
Hair is individual lock instances, not one blob. Existing evidence defines `LOCK_0001..LOCK_0025`, root->tip direction, and explicit neck/ear exclusions. Do not let remeshing or segmentation reclassify neck skin as hair.

## Candidate workflow — do this without waiting for another prompt
1. Read `CLAUDE.md`, this bulletin, and the current evidence manifest.
2. Identify the current real failure from measured evidence.
3. Select at least two independent open-source candidates when topology is involved.
4. Run/implement the candidate comparison on the real patch where the environment permits.
5. Reject candidates that improve triangle statistics while damaging protected anatomy.
6. Publish comparison renders/meshes/metrics under `docs/evidence/<set>/` with SHA-256.
7. Leave the canonical mesh untouched until a candidate passes both physical and visual gates.
8. Record failures as useful evidence and immediately try the next viable open-source route.
9. Update this bulletin when a new tool/candidate becomes available.

## Evidence rule
No bytes = no evidence. A statement that an overlay/render exists without publishing its actual pixels is not a PASS. `UNKNOWN` is never PASS.

## Tool discovery queue
When the current stack is insufficient, actively investigate and evaluate additional complete open-source projects in these categories:
- quad/field-aware retopology
- isotropic/adaptive surface remeshing
- mesh boolean/self-intersection repair
- UV transfer and attribute/shape-key transfer
- facial landmark/segmentation proposals
- hair curve/strand extraction and simulation
- oral/teeth/tongue facial deformation
- mesh QA and differential geometry
- transparent annotation/overlay generation

The goal is not to collect names. Each adopted tool needs a concrete role, upstream provenance, integration point, and measurable promotion gate.
