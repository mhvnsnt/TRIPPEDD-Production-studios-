# God Molecule / Mars — canonical asset pipeline

## Non-negotiable identity rule
When a real person's reference is supplied, edit/animate the supplied source. Do not silently regenerate a replacement person. Identity changes require an explicit production instruction.

For Mars:
- preserve approved facial geometry and likeness;
- preserve the complete head, neck, jaw, beard, dreads, and back-of-head silhouette;
- preserve canonical front/left/right/back references;
- allow requested transformations such as expression, eye/mouth/teeth effects, lighting, color, materials, environment, motion, camera, or deliberately surreal effects.

## Two parallel production lanes

### 2D/photo lane
Source photo/reference -> non-destructive mask/edit -> Mars grade -> Tonnō pass when required -> controlled generative enhancement -> likeness QC -> shot.

### 3D lane
Tripo/scan source -> immutable source archive -> Blender intake audit -> scale/landmark measurement -> topology/normal validation -> rig -> facial controls/shape keys -> animation -> Mars materials/lighting -> render -> likeness QC.

### Hybrid lane
3D head supplies geometry and continuity while 2D/generated plates supply graphic or psychedelic inserts. Both lanes share canonical reference images and shot IDs.

## 3D head readiness gates
1. Geometry: complete neck/back/jaw/head silhouette.
2. Measurements: bounds, centerline, eye/jaw/forehead landmarks, source scale.
3. Topology: non-manifold edges, degenerate faces, normals, UVs, material slots.
4. Rig: head/jaw/neck controls work before facial generation.
5. Face: blink, brow, jaw, mouth and phoneme controls test independently.
6. Turntable: front -> left -> back -> right -> front at constant camera/lighting.
7. Likeness QC: compare rendered landmarks and silhouette against canonical references; reject unrequested drift.
8. Only then add procedural/generative expressions and psychedelic transformations.

## Open-source tool roles
- Blender: canonical 3D host, rigging, shape keys, animation, rendering, tracking.
- MPFB2: Blender character utilities; optional helper, never a replacement for Mars source geometry.
- OpenToonz: 2D frame/cutout animation and graphic inserts.
- Synfig: vector/cutout rigs and economical expression animation.
- Natron: compositing, roto, tracking, color and VFX.
- ComfyUI / InvokeAI: reference-controlled image editing/generation.
- LTX / Wan / DiffSynth: motion/video generation after identity lock.

## 3D head intake
The production runner should locate the supplied GLB/GLTF/OBJ/FBX/Blend/USD asset from the production asset store and pass it to tools/asset_pipeline/scan_head.py.

The scanner is read-only against the source and produces a JSON audit containing mesh objects, vertex/polygon counts, materials, armature/bones, shape keys, world-space bounds/dimensions, and a SHA-256 source hash.

The current Library search found Mars image references and the turntable concept sheet, but did not surface the actual Tripo 3D head model. No substitute mesh should be silently used.
