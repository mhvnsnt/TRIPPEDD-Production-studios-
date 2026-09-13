# Claude Tool Bulletin — MARS / visual anatomy / topology

**Purpose:** Persistent handoff channel for tools discovered by other agents. Claude should read this at the beginning of every relevant turn and use the listed capabilities without waiting for the owner to repeat a prompt.

**Update law:** When another agent adds a tool, adapter, contract, benchmark, or evidence source, update this bulletin in the same change. When Claude discovers a better open-source route, add it here too.

## MARS assembly law — ONE CANONICAL CHARACTER

**Default is one canonical MARS model.** Claude MUST NOT silently create or continue separate competing MARS head/body/face models when the work can be performed by attaching, replacing, merging, or transferring a component into the canonical model.

The current recovery work is explicitly an **assembly operation**: preserve the model with the correct eyes, eyebrows, hair and other proven features, take the mouth/oral anatomy from the previously correct GLB, and attach/merge that mouth into the canonical model. Do not fork the character again merely because a component is easier to fix in isolation.

### Mandatory rules
1. **Canonical source is identified before editing.** Record the canonical model path/hash in the run receipt.
2. **Parts-first, character-second:** a component may be worked on separately temporarily, but its destination is the canonical model unless the owner explicitly requests a separate model.
3. **No silent model forks.** Creating `MARS_v2`, `MARS_fixed`, `MARS_final2`, etc. as competing authorities is forbidden without an explicit owner decision.
4. **Known-good parts are assets, not new identities.** If one GLB has the correct mouth and another has the correct eyes/hair, transfer the proven component between them and preserve the recipient's other proven anatomy.
5. **Never discard a known-good feature just to simplify tooling.** Prefer mesh/object transfer, vertex/attribute transfer, rig/weight transfer, or controlled merge.
6. **Assembly must be measured.** After attachment, verify placement, scale, normals, topology boundaries, materials, UVs, jaw/mouth motion, eyes, brows, hair and exclusions. A successful Blender operation is not a visual PASS.
7. **Evidence names the assembled authority.** Render the assembled canonical character and publish actual pixels plus hashes before declaring the assembly usable.
8. **Separate diagnostic candidates must be labelled CANDIDATE and never become canonical automatically.**
9. **If a truly separate model is required for an experiment, say why in the manifest and define the merge-back/selection rule before proceeding.**
10. **Owner override is the only way to authorize permanent separation.**

### Assembly decision order
`CANONICAL_MARS` → identify known-good source component → validate component → transfer/attach → reconcile materials/UVs → reconcile armature/weights/shape keys → run physical gates → render visual proof → publish evidence → promote component into canonical model.

**Do not reverse this into:** generate another whole character → pick whichever looks better later. That is precisely the drift this law prevents.

## Continuous-work law
When Claude finishes a subtask and no owner decision is required, it should immediately continue to the next useful task from the bulletin/tool-discovery queue rather than stopping for another prompt. It must leave a receipt/evidence trail so the next turn can resume without reconstructing context.

If the current route fails, immediately try the next viable open-source route. A failure is a routing signal, not a stopping point.

## Current mission
Fix MARS without replacing the immutable visual reference. Current high-risk failures: source-bad facial topology, eye correspondence, oral anatomy separation, hair/neck classification, and component assembly consistency. Prefer deterministic measured geometry over hand placement.

## Immediate topology stack

### PyMeshLab / MeshLab
**Use for:** reproducible mesh inspection, cleanup, local repair, comparison of source and candidate patches.
**Rule:** diagnose/compare; never accept a repair merely because polygon count increased.

### CGAL
**Use for:** isotropic remeshing, local patch repair, edge operations, feature preservation, Delaunay alternatives.
**Preferred use:** current eye patch with protected painted lid curves and measured target edge scale.
**Promotion gates:** triangle-angle improvement, no self-intersections/non-manifold defects, protected-lid displacement within tolerance, surface error bounded, UV/shape transfer preserved.

### Instant Meshes
**Use for:** deformation-oriented retopology / quad-dominant candidate generation. Independent candidate only.

### Open3D
**Use for:** independent mesh validation, normals, intersections, geometry statistics and measurement. Second-opinion validator.

### OpenSubdiv
**Use for:** subdivision only after base topology is healthy. Never use it to hide source slivers.

### Remi Blender addon
**Use for:** one-Blender orchestration of difficult-mesh repair, Instant Meshes retopology, PyMeshLab/CGAL integrations and rebake workflows. It is an orchestration/artist-control layer, not an authority; preserve upstream notices/licenses.

## Visual correspondence tools

### Position-map correspondence
`docs/evidence/place/position_map.npz` is direct image-pixel → 3D surface correspondence. Use before arbitrary raycasts or guessed facial coordinates.

### Painted eye authority
`docs/evidence/blink_own/painted_lid_lines.json` is authoritative painted lid trace. Do NOT use known-bad `linework_3d.json` as the eye ruler.

### Immutable reference pixels
`docs/evidence/annotations/REFERENCE_PIXELS.json` plus `docs/evidence/annotations/` define pixel authority. Never regenerate, repaint, restyle, sharpen, beautify, or replace these pixels.

## Annotation / AI proposal stack

### CVAT Community
Human/AI-assisted polygons, masks, keypoints, curves and QA. Annotations are proposals/evidence layers, never permission to alter immutable reference.

### Segment Anything 2
Segmentation proposals for facial regions/hair/oral components. Verify against semantic anatomy and actual pixels.

### MediaPipe / ONNX face mesh
Landmark proposals and independent facial correspondence. Landmark names alone never determine anatomy.

### MVMP
Multi-view MediaPipe landmarks projected back to real 3D mesh. Compare against position-map and painted traces; do not replace either authority.

## Facial rig / assembly references

### Blender Rigify
Face/eye/jaw/tongue deformation-control reference. Eye closure follows measured anatomical axis, not contour winding.

### ICT-FaceKit
Facial shape/eye rig donor experiments. Preserve side naming based on where shapes actually land.

### mdj128/facial-animation
Procedural facial rigging architecture with separated upper/lower teeth and tongue. Useful for the current mouth-integration problem. Do not import another character identity over MARS.

### ARKit Creator Blender addon
Optional shape-key baking aid when multiple selected meshes need coordinated facial-shape generation. It must not replace canonical assembly or visual QC.

### BlenderGR2rs
Evaluate for deterministic armature/skin-weight transfer when the mouth component and canonical MARS use different skeleton/weight structures. Source mesh remains untouched; ambiguous mapping must fail closed.

## Oral anatomy rule
Mouth must be structural, not a texture sheet. Preserve distinct `ORAL_CAVITY`, `TEETH_UPPER`, `TEETH_LOWER`, `GUM_UPPER`, `GUM_LOWER`, and `TONGUE`, with jaw-open render evidence. Physical coverage alone is insufficient; actual pixels must read as separated anatomy.

## Hair rule
Hair is individual lock instances, not one blob. Existing evidence defines `LOCK_0001..LOCK_0025`, root→tip direction, and explicit neck/ear exclusions. Do not let remeshing or segmentation reclassify neck skin as hair.

## Candidate workflow — do this without waiting for another prompt
1. Read `CLAUDE.md`, this bulletin, and the current evidence manifest.
2. Identify the current real failure from measured evidence.
3. Identify/lock the canonical MARS model before making component changes.
4. Prefer transfer/merge into canonical MARS over creating another whole-character model.
5. Select at least two independent open-source candidates when topology is involved.
6. Run/implement candidate comparison on the real patch where the environment permits.
7. Reject candidates that improve statistics while damaging protected anatomy.
8. Publish comparison renders/meshes/metrics under `docs/evidence/<set>/` with SHA-256.
9. Leave canonical mesh untouched until a candidate passes physical + visual gates; then promote the component into canonical MARS.
10. If no owner decision is required, immediately continue to the next useful queue item.
11. Update this bulletin whenever a new tool/candidate becomes available.

## Evidence rule
No bytes = no evidence. A statement that an overlay/render exists without publishing actual pixels is not PASS. `UNKNOWN` is never PASS.

## Tool discovery queue
When the current stack is insufficient, actively investigate and evaluate additional complete open-source projects in:
- quad/field-aware retopology
- isotropic/adaptive surface remeshing
- mesh boolean/self-intersection repair
- UV/attribute/shape-key transfer
- facial landmark/segmentation proposals
- hair curve/strand extraction and simulation
- oral/teeth/tongue facial deformation
- mesh QA and differential geometry
- transparent annotation/overlay generation
- multi-mesh assembly, armature/weight transfer and shape-key preservation

The goal is not collecting names. Each adopted tool needs concrete role, upstream provenance, integration point, and measurable promotion gate.
