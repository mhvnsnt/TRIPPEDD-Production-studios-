# BUILD MAP — OUR OWN FREE VERSIONS OF THE PAID TOP-11

What this is: the study half of the owner's order — reverse engineer how the
paid creative tools *work* (their signature workflows, studied from public
documentation only) and build our own free versions of the parts we actually
need. Companion to `docs/INDUSTRY-STACK-STATUS.md` (the wire-up audit this
map is checked against).

## Method and boundaries

- **Public sources only.** Every workflow below was studied from official
  manuals/vendor docs, vendor tutorials, and reputable workflow write-ups
  (sources listed at the end). No paid binary was downloaded, decompiled,
  disassembled, decrypted, or touched in any way, and no license system was
  approached. That work is refused and outside this mission.
- **Clean-room rule.** Behavior and features go in; **our own original code**
  comes out. Nothing below specs a repackaging of anyone's code, assets,
  shaders, or preset files.
- **Donor first** (repo law). Where a free/open donor already does the job
  (a Blender add-on, a community script, a Blender built-in), the spec is
  *wire the donor in*, not hand-roll a replacement. Hand-rolled builds are
  only specced where no donor covers the gap.
- Sizes: **small** = an add-on / script / preset pack one lane can land in a
  sitting; **medium** = a real tool, several sittings; **big** = a project.

---

## 1. Autodesk Maya — rigging, animation, HumanIK retargeting

### (1) Signature workflows, in plain terms
- **HumanIK characterization.** You define a character once by mapping its
  bones onto a standard humanoid template (character stands in T-pose, you
  click which bone is the left forearm, etc.). After that, Maya *understands*
  the skeleton instead of just seeing bone names.
- **HumanIK retargeting.** Any animation recorded on any characterized
  skeleton plays on any other characterized character — different heights and
  proportions are compensated automatically (a "Match Source" stride scale,
  feet kept planted on the floor). A full-body IK control rig is generated
  for the target automatically, with pinning and body-part keying.
- **Non-destructive retarget + animation layers.** Retargeted motion lands on
  its own animation layer. The animator keys fixes on layers stacked above
  it, tweaks retarget parameters live, and only bakes at export. The source
  mocap is never edited.
- **The daily rigging loop.** Joint placement → skin weights painted →
  control rig → blend shapes (facial/expression shapes) → set-driven keys
  (one control drives many attributes) → the same rig file referenced into
  every shot.

### (2) What our wired stack already covers
- **Blender** (wired, 4.0.2/4.5.3/5.2.3): armatures, IK/FK constraint
  stacks, **Rigify** (built-in auto control-rig generator), shape keys +
  drivers (the set-driven-key equivalent), Pose Library, and **NLA strips
  with additive blending** — a rougher analog of animation layers.
- **Free donors (not yet wired):** the **Rokoko Blender plug-in** (free;
  builds a bone list between a source and target armature and retargets),
  **Quick Map** (free add-on; per-bone retarget with relative-rotation
  correction), **BlenRig 6** (free, open production rig system).
- Proof this workflow matters here: Cape Jones already runs on a Blender
  mocap pipeline (the baked `mocap_sit_canon` action) — retargeting is done
  today, by hand, per character.

### (3) Gaps
- **G-M1 — No saved characterization profiles.** Every new character ×
  skeleton pairing gets its bone mapping rebuilt manually. There is no
  one-click "apply the studio body map" for the skeletons we actually meet:
  Tripo rigs, Mixamo, Rokoko BVH, Rigify metarigs, our own canon rigs.
- **G-M2 — No proportion-compensation controls.** Stride scaling and
  feet-to-floor cleanup after a retarget are manual per-clip fixes, not two
  sliders.

### (4) Build specs
- **SPEC M-1 "Characterizer" — medium tool.** A Blender add-on holding named
  bone-mapping profiles as JSON (Mixamo, Rokoko, Tripo, Rigify, Cape Jones
  canon rig to start). Panel flow: pick source profile + target profile →
  the add-on builds the copy-rotation/copy-location constraint set with
  rest-pose offset correction, then bakes to a fresh action presented as an
  NLA-ready track (source action untouched — the Maya layers lesson).
  Behavior studied from the public HumanIK docs; implementation is original
  `bpy` code (donor UX reference: the Rokoko plug-in's bone-list flow, not
  its code). *Unlocks:* any mocap clip onto any character in minutes —
  Cape Jones 3D segments, Bannon/Western Heart fighter animation, cheap
  Tripo cast expansion.
- **SPEC M-2 "Retarget polish sliders" — small add-on** (lands as M-1 v2).
  Post-bake operators: stride scale (scales root motion), floor clamp
  (raycast floor plane, offset so feet plant), foot-skate cleanup pass.
  *Unlocks:* retargeted clips stop needing hand cleanup before they're
  usable in a shot.

---

## 2. SideFX Houdini — node-based procedural FX

### (1) Signature workflows, in plain terms
- **Everything is a node network.** Geometry (SOPs), simulation (DOPs), and
  render outputs (ROPs) are graphs of small operations. Nothing is ever
  "applied and gone" — you rewind the network, change an early node, and
  the whole result rebuilds. Finished networks get saved as reusable
  digital assets (HDAs) and dropped into other shots.
- **RBD destruction.** The object is fractured differently per material
  (wood splinters, stone chunks, glass shards), then held together by a
  **constraint network** — glue/soft bonds between pieces with per-bond
  strength. A Bullet solver runs it: the structure stands until impacts
  exceed bond strength, then fails progressively. Secondary fire/debris is
  birthed from the impact.
- **Pyro.** Sparse volumetric fire/smoke solved on a voxel grid, shaped by
  "microsolvers" — extra little forces (disturbance, dissipation, buoyancy
  shaping) layered into the solve so fire looks *directed*, not generic.
- **FLIP fluids.** A particle/volume hybrid for liquids: particles carry the
  motion, a grid keeps it incompressible; surface tension and viscosity are
  parameters; whitewater is a secondary particle pass.
- **Crowds.** Characters become lightweight "agents" (a rig + a library of
  clips). A finite state machine decides each agent's state
  (idle → walk → run → fall), a steering solver keeps them out of each
  other and glued to terrain, clips blend at transitions.
- **TOPs / PDG.** A task graph on top of everything: "wedge" a parameter
  (try this explosion at 20 strengths), run all variants across machines,
  collect previews, keep the best. Also how studios generate whole asset
  libraries overnight.

### (2) What our wired stack already covers
- **Blender:** rigid-body simulation (Bullet) + the bundled **Cell
  Fracture** add-on (fracture + falling pieces for simple shots),
  **Mantaflow** smoke/fire/liquid, cloth and soft-body solvers, particle
  systems including **boids** (basic flocking/steering rules), and
  **Geometry Nodes** — genuinely procedural modeling/distribution with
  simulation zones for custom effects. Headless Python already drives
  batch renders (proven by the Cape Jones render lanes).
- **Unreal Engine 5.8.2 source (VERIFIED-ACCESS, not built):** the fork we
  hold contains Chaos destruction, Niagara particles, PCG procedural
  generation, and the Mass crowd framework. Real, ours, and currently
  unusable on this 2-core VM — building it is a workstation/cloud job.

### (3) Gaps
- **G-H1 — No constraint-network destruction.** Blender fractures and
  drops; nothing holds a structure together until an impact threshold and
  then breaks it progressively. Set-piece destruction is hand-faked today.
- **G-H2 — No wedge/batch-variation system.** No "run this sim 20 ways
  tonight, show me contact sheets tomorrow" driver (the PDG lesson).
- **G-H3 — No crowd agents.** No state-machine crowd of rigged characters
  for background life (arena crowds, townsfolk).
- **G-H4 — Pyro art direction is shallow.** Mantaflow works, but there's no
  preset discipline for the shaping controls, so fire/smoke looks generic
  until hand-tuned every time.

### (4) Build specs
- **SPEC H-1 "GlueGraph destruction kit" — medium tool.** A Geometry
  Nodes + rigid-body pipeline built on Blender's own constraint API:
  per-material fracture, then a generated set of breakable rigid-body
  constraints whose strength is set by distance/material, impact-triggered
  release, bake-to-cache button. Original implementation. *Unlocks:*
  destructible sets for Cape Jones gags and Western Heart / Bannon stages
  that break like structures, not confetti.
- **SPEC H-2 "WedgeRunner" — small tool.** Standalone Python + headless
  Blender: reads a JSON wedge list (parameter sets), runs each variant as
  its own process with logs, emits a contact-sheet preview page per batch.
  Extends the headless driver pattern the studio already uses. *Unlocks:*
  overnight variant libraries (debris, rocks, explosion strengths, render
  settings) and a general force multiplier for H-1/H-4 and all sim work.
- **SPEC H-3 "CrowdLite" — big project.** Geometry-Nodes/boids agent
  system: agents are instanced rigged characters with a baked clip library;
  a small Python state machine switches clips by zone triggers; boid rules
  handle avoidance. Stated honestly: the biggest spec in this map. The
  alternative donor route — build the UE fork on a real machine and use
  Mass/PCG there — may supersede it. *Unlocks:* Bannon arena crowds,
  Western Heart town life. **Defer until that work is actually scheduled.**
- **SPEC H-4 "Pyro shaping pack" — small (configuration, not code).** A
  Mantaflow preset library (named fire/smoke looks with dissipation and
  noise settings tuned per look) plus matching Cycles volume-shading and
  Natron finishing recipes. *Unlocks:* repeatable, directed fire/smoke for
  Cape Jones LED/party scenes and Wizard Gang V2 FX plates.

---

## 3. ZBrush — sculpting

### (1) Signature workflows, in plain terms
- **DynaMesh.** Sculpt like clay with zero topology anxiety: stretch, cut,
  and boolean parts together, then re-mesh on demand into a clean uniform
  surface. Overlapping junk inside the model is removed automatically.
- **Subdivision levels + sculpt layers.** Detail lives on subdivision
  levels you can step down/up; variations can be stored as switchable
  layers/morph targets.
- **ZRemesher.** One click turns a blobby sculpt into clean, animation-ready
  quad topology that follows the surface's flow, with painted density and
  guide curves where you want control. **Project All** then transfers the
  high-res detail and color onto the new low-res mesh.
- **PolyPaint.** Paint color directly onto the model's vertices — no UVs
  required — at full sculpt resolution, using alphas and brushes for pores,
  scales, wear. **Polygroups** keep parts organized; **Decimation Master**
  shrinks a sculpt for export/printing while keeping visible detail.

### (2) What our wired stack already covers (Blender sculpt mode)
- **Voxel Remesh** = the DynaMesh analog (uniform re-mesh while sculpting);
  **DynTopo** adds detail only where you stroke.
- **QuadriFlow remesh** (built in) = automatic quad retopology — real, but
  less flow-aware than ZRemesher and takes no guide curves.
- **Multires modifier + Cycles baking** = subdivision levels and the
  Project-All detail/color transfer.
- **Vertex colors + texture paint** = the PolyPaint role; alpha brushes,
  symmetry, masking all present. **Decimate modifier** = Decimation Master.

### (3) Gaps
- **G-Z1 — Retopo flow quality.** QuadriFlow doesn't follow painted flow
  guides or density maps, so Tripo/sculpt → animation-ready retopo still
  ends in manual cleanup on faces and joints.
- **G-Z2 — The finishing chain is a manual dance.** Sculpt → remesh → UV →
  project/bake → export is five separate rituals in Blender today, with
  settings re-derived every time.

### (4) Build specs
- **SPEC Z-1 "FlowRetopo wrapper" — small tool.** Donor-first: chain the
  free remeshers that exist — QuadriFlow (with symmetry) and an **Instant
  Meshes** round-trip (free external field-aligned remesher) — behind one
  Blender operator that reads density from vertex colors and returns a
  checked mesh. The spec wires donors; it does not hand-roll a remesher.
  *Unlocks:* faster sculpt/Tripo → rig-ready characters for Cape Jones and
  Bannon.
- **SPEC Z-2 "Sculpt Finisher" — small add-on.** One panel that runs the
  finishing chain end to end: voxel-remesh cleanup → QuadriFlow → UV unwrap
  + pack → multires bake (normal / AO / color from the high-res) → export
  preset (game GLB or print STL). Pure orchestration of Blender built-ins.
  *Unlocks:* every hero sculpt ships game-ready in one pass instead of five.

---

## 4. Substance 3D Painter — layer-based texturing

### (1) Signature workflows, in plain terms
- **A Photoshop-style layer stack over PBR channels.** Paint layers (hand
  work), fill layers (whole-surface material), folders, and per-layer blend
  modes — each layer writing into base color, roughness, metalness, normal,
  and height channels at once.
- **Baked mesh maps drive everything.** The model is analyzed once: ambient
  occlusion, curvature, normals, world position, thickness, material ID.
- **Generators and smart masks.** A mask isn't painted — it's *computed*
  from the mesh maps: curvature finds edges (wear), AO finds crevices
  (dirt), position finds tops (dust), plus grunge noise. The "Mask Editor"
  generator mixes these with sliders. A **Smart Material** is a saved stack
  whose masks are all mesh-driven, so it lands correctly on *any* model.
- **Anchors** let one layer read another layer's mask/height, so paint
  chips reveal the metal authored three layers down. Export presets pack
  channels per target engine (ORM maps etc.).

### (2) What our wired stack already covers
- Blender native painting writes per-channel textures, but the layer
  workflow is a hand-maintained node tree — no real stack UI. Krita
  (wired) covers 2D paint-over work. The status doc's "Blender + Krita"
  line **undersells what free donors already provide:**
- **Donor: Ucupaint** (free, GPL; v3.0 released this week) — a real
  layer-stack texture-painting system *inside* Blender: layers, groups,
  masks, modifiers, channels derived from the shader, decal layers,
  per-channel bake targets, ORM packing.
- **Donor: ArmorPaint** (open source, 1.0) — standalone GPU texture
  painter with node-based materials and a Blender bridge plug-in.
- **Donor: Material Maker** (free) — procedural material authoring, the
  Designer-side companion.

### (3) Gaps
- **G-S1 — The donors aren't wired.** Neither Ucupaint nor ArmorPaint is in
  the stack yet; texturing still happens the slow way.
- **G-S2 — No smart-mask recipe library.** The layer machinery exists
  (Ucupaint), but the studio's own reusable edge-wear / cavity-dirt /
  top-dust stacks — the "smart materials" layer of the workflow — don't.
- **G-S3 — No export-preset discipline.** Channel packing per engine is
  improvised per asset.

### (4) Build specs
- **SPEC S-1 "Wire Ucupaint + ArmorPaint" — small (integration, not
  code).** Install both into the wired Blender builds + ArmorPaint
  standalone, smoke-test on a real asset (a Tripo character; the Cape Jones
  cowl material is the natural test case), and write the wiring note into
  the stack docs. Donor adoption per the repo's DONOR FIRST law.
- **SPEC S-2 "SmartMask preset pack" — small (content build).** A named
  library of Ucupaint layer-stack presets — edge wear, cavity dirt,
  top-down dust, paint chips — driven by baked AO/curvature/position maps,
  saved as reusable studio assets. *Unlocks:* production wear on any asset
  in minutes; Western Heart / Bannon props and fighters stop shipping flat.
- **SPEC S-3 "Texture export presets" — small script.** Bake-target
  profiles for Godot, Unreal, and Blender with correct channel packing
  (ORM etc.), one click per target. Pairs with S-1's bake targets.

---

## 5. Nuke — node compositing (checked against Natron)

### (1) Signature workflows, in plain terms
- **Node-graph comp in 32-bit linear, with channel surgery.** Images carry
  up to 1023 named channels; multi-channel EXR renders get taken apart
  with Shuffle nodes and rebuilt — the classic "beauty rebuild": diffuse +
  specular + reflection + emission graded separately, then re-summed, so
  lighting can be rebalanced *after* the render.
- **Deep compositing.** Pixels carry multiple depth samples, so CG merges
  correctly *through* volumetrics — an object can sit inside smoke with
  correct ordering, no matte edges (DeepMerge / DeepHoldout).
- **A real 3D system inside the compositor.** Cameras, cards, and geometry
  live in the comp: camera projection for set extensions and matte
  paintings, 2.5D parallax moves, particles in comp, stereo support.
- **Studio tooling culture.** Sub-graphs get packaged as shareable gizmos;
  comp scripts are plain text; Keylight/Primatte-class keyers and a deep
  tracking ecosystem are assumed.

### (2) What our wired stack already covers (Natron 2.5.0)
Natron is deliberately Nuke-shaped: node graph, 32-bit linear pipeline,
multi-channel EXR with shuffle-style channel ops, roto/paint, keyers, the
OpenFX plug-in ecosystem (openfx-misc / openfx-arena bundles), point
tracking, Python scripting, and group/gizmo-style packaging. Per Natron's
own Nuke-transition guide, the headline missing area is 3D.

### (3) Gaps (sourced from Natron's docs and roadmap)
- **G-N1 — No 3D system in comp.** No camera/card projection natively; the
  community's PMCard3D/PMcamera scripts add a minimal version. This one
  matters here specifically: **pan-and-zoom parallax is Pipeline One's
  signature move** for Wizard Gang, and Cape Jones's TV-parallel gag is a
  card trick.
- **G-N2 — No deep compositing.** Deep is on Natron's roadmap for a future
  4.0; 2.5 doesn't have it. CG-through-smoke shots can't merge the deep
  way.
- **G-N3 — Our comp recipes aren't packaged.** The studio's grade looks
  (LOOK 1 Pale Wash / LOOK 2 Deep Saturation) and LED glow recipes live as
  per-shot graphs, not as named, reusable gizmos.

### (4) Build specs
- **SPEC N-1 "Card projection kit" — small tool.** Donor-first: adopt
  PMCard3D/PMcamera from the Natron CommunityScripts into our Natron
  install, plus a written recipe for the other route — camera-mapped
  planes projected in Blender, comped in Natron — with a decision rule for
  which route a shot takes. *Unlocks:* parallax cards and set extensions
  without leaving the free stack.
- **SPEC N-2 "Deep-enough pipeline" — medium (pipeline, little code).**
  An honest workaround, not a deep engine: render Cycles volumes, holdout
  mattes, and depth as separate EXR layers and composite with depth-aware
  merge recipes in Natron. Covers what our stylized shows actually board;
  if a true deep shot ever gets scheduled, this spec gets revisited, not
  silently stretched. *Unlocks:* characters sitting inside fog/smoke gags
  with clean edges.
- **SPEC N-3 "Studio gizmo pack" — small.** Package the existing cape-jones
  grades and LED recipes as named Natron groups with documented knobs.
  *Unlocks:* episode-to-episode look consistency without rebuilding graphs.

---

## 6. Cinema 4D — MoGraph

### (1) Signature workflows, in plain terms
- **The Cloner.** Take any object and distribute it — along a line, grid,
  spline, or scattered over a surface — with count and spacing animatable.
- **Effectors.** Sixteen stackable "influence" objects (Plain, Random,
  Step, Shader, Sound, Formula, Delay, Spline, Target…) that transform the
  clones: each contributes position/rotation/scale/color changes, blended
  by **Fields** — spatial falloff masks (a sphere of influence, a noise
  field, a decaying box). Stacking and reordering effectors *is* the
  animation; most MoGraph work has almost no keyframes.
- **Fracture / Voronoi Fracture.** An object is treated as a set of pieces,
  each piece a "clone" effectors can push around — break-apart logos,
  exploding type. The **Tracer** turns motion paths into splines; MoText
  and MoSpline do kinetic typography.

### (2) What our wired stack already covers (Blender Geometry Nodes)
The *capability* is largely present: Distribute Points / Instance on
Points is the Cloner core; proximity, weight, and noise falloffs are the
Fields concept; simulation zones add dynamics; rigid bodies + Cell
Fracture cover break-apart geometry; particle paths can be converted to
curves. What doesn't exist is the *artist surface*: a named, ordered
effector stack with falloff widgets an animator can drive without opening
the node graph.

### (3) Gaps
- **G-C1 — No effector-stack UX.** Every MoGraph-style shot is a fresh
  Geometry Nodes build by whoever's on the lane.
- **G-C2 — Fracture + per-piece effector control isn't one preset.** The
  pieces exist (Cell Fracture, GN) but not as a single "explode this logo"
  setup. (Shares its fracture core with SPEC H-1 — cross-referenced so the
  two lanes build it once.)

### (4) Build specs
- **SPEC C-1 "EffectorKit" — medium tool.** A Geometry Nodes asset library
  + a small panel: named, documented node groups replicating the effector
  set — Plain (offset), Random, Step (sequential ramp across clones),
  Shader (image-driven), Sound (audio spectrum baked to curves, driving
  instance parameters), Delay (temporal smoothing in a simulation zone) —
  each with a Falloff control (sphere / box / noise), applied to an
  instanced collection in a fixed documented order. Original GN
  construction. *Unlocks:* the bump/title cards that sit between scenes in
  every Cape Jones and Wizard Gang episode — MoGraph's home turf — plus
  logo stings and object-crowd gags, on demand instead of per-shot R&D.
- **SPEC C-2 — folded into SPEC H-1** (shared fracture core) with an
  "explode pieces" effector preset added to EffectorKit when both land.

---

## 7. Toon Boom Harmony — 2D cutout rigging + deformers

### (1) Signature workflows, in plain terms
- **Node-view puppet assembly.** Drawings hang under **pegs** (transform
  nodes) in a node graph; pivots and hierarchy make the puppet. A library
  of **drawing substitutions** (mouths, hands, poses) swaps per frame.
- **Five deformer families.** Bone and Game Bone chains (solid parts,
  flexible joints), Curve (bend a part along a bézier), Envelope (a
  freeform cage around a drawing), Free Form. **Kinematic Output** pins a
  child part to a deform point so it rides the bend *without* deforming,
  and zones of influence control how far each deform reaches.
- **Master Controllers.** Custom on-screen widgets — sliders, 2D point
  pickers — wired by the rigger to drive many pegs/deformers at once, so
  the animator operates "head turn" or "arm pose" as one control.
- **Palette discipline.** Colors are palette entries shared scene-wide:
  recolor the palette and every drawing updates; model sheets stay
  enforced.

### (2) What our wired stack already covers
**Tahoma2D 1.6.3 (wired)** and OpenToonz 1.8.0 (installed) come from the
Toonz lineage and cover more of this than expected: a stage schematic
(node-graph assembly), the **Skeleton Tool** for IK cutout models, the
**Plastic Tool** — a triangulated mesh + in-mesh skeleton with per-vertex
rigidity that plays the Bone/Curve/Envelope roles in one system — indexed
**palettes** with palette-level recoloring, and drawing levels on an
exposure sheet for substitutions. **Rhubarb (wired)** produces phoneme
timings for lip sync. The Wizard Gang puppet cast already lives in this
ecosystem.

### (3) Gaps
- **G-T1 — No master-controller widgets.** Animators drive skeleton/plastic
  points individually; there is no single pose/turn control surface per
  puppet, so posing is slower and less consistent between animators.
- **G-T2 — Lip sync stops one step short.** Rhubarb outputs *when* each
  phoneme happens, but turning that into mouth-drawing exposures on the
  character's mouth level is still hand work.
- **G-T3 — Influence zones are coarser.** Plastic's per-vertex rigidity
  painting covers the Envelope job at higher setup cost than Harmony's
  shaped zones + kinematic pinning. **Accepted gap** (see below).

### (4) Build specs
- **SPEC T-1 "Puppet Control Sheets" — medium tool.** A rig convention +
  helper tooling for Tahoma2D: standardized control levels driving grouped
  parts, a named pose-library exposure workflow, and per-show puppet
  template files so every Wizard Gang / 2D Cape Jones character ships with
  the same control layout. Honest scope note: Tahoma2D's in-app scripting
  surface is limited — parts of this may land as Python-driven scene-file
  generation rather than true in-app widgets; that gets verified at build
  time, not assumed. *Unlocks:* consistent, faster posing across the whole
  puppet cast.
- **SPEC T-2 "Rhubarb→MouthSwap bridge" — small tool.** Standalone Python:
  Rhubarb's phoneme output → the mouth level's exposure plan (scene/cell
  mapping for Tahoma2D), using the shows' standard mouth sets (Wizard
  Gang's mouth-only clean transparent PNGs). Connects two already-wired
  tools. *Unlocks:* dialogue scenes stop being hand-timed — this is the
  exact step the owner's scene-by-scene method waits on (he records, then
  lip sync happens in post).
- **G-T3: no spec.** Plastic rigidity painting covers it at more setup
  minutes per rig; revisit only if a specific shot fails because of it.

---

## 8. Arnold — production rendering (vs Cycles)

### (1) Signature workflows, in plain terms
What studios actually buy Arnold for: **predictability at scale** — an
unbiased CPU path tracer that returns the same image on every farm node,
with aiStandardSurface as the shared material language, adaptive sampling
and production denoising, **deep EXR output**, a full AOV system including
**per-light AOVs** (relight in comp), built-in Cryptomatte, and
stand-in/procedural instancing that lets enormous scenes (forests, cities,
fur) render without loading everything. Hair and volume shaders are
specialists, not afterthoughts.

### (2) What our wired stack already covers (Cycles, Blender 4.5/5.x)
Nearly all of it, at our scale: GPU+CPU path tracing, adaptive sampling,
OpenImageDenoise, full render passes **including light groups** (per-light
AOVs), built-in **Cryptomatte**, **light linking and shadow linking**,
volumetrics, a dedicated hair BSDF, OSL on CPU, USD interchange — plus the
ACES pipeline already landed in the cape-jones work. Cycles is
production-proven beyond us (feature animation has shipped on it).

### (3) Gaps — small, and stated plainly
- **G-A1 — No stand-in/procedural discipline for huge sets.** Our scenes
  load full geometry. Hasn't bitten at our shot scale. **No build spec** —
  accepted; revisit if a city/forest shot gets boarded.
- **G-A2 — Render fragility on this VM.** Long Cycles renders die when the
  2-core VM restarts; the Cape Jones lane survived by rendering one frame
  per Blender invocation with a frame inventory — as folklore, not as a
  reusable tool. The standing owed upgrade (Scene 1 at full 960×540) is
  blocked on exactly this.
- **G-A3 — Material translation is tribal knowledge.** Arnold recipes from
  tutorials don't map 1:1 onto Principled in anyone's head yet.

### (4) Build specs
- **SPEC A-1 "Checkpoint render driver" — small tool.** Formalize the
  proven pattern: chunked Cycles rendering (frame/tile granularity),
  resume-from-first-missing, hash-verified frame inventory, free-RAM gate,
  optional sample wedges via SPEC H-2. *Unlocks:* the owed 960×540 Scene 1
  re-render becomes safe to start, and every future long render survives
  the VM.
- **SPEC A-2 "Material translation sheet" — small (doc + presets).** A
  studio cheat-sheet + starter node pack mapping common aiStandardSurface
  recipes to Principled/OpenPBR equivalents. Doc-first, tiny build.

---

## 9. Recommended build order — ranked by value to the actual shows

Ranking weighs the owner's production method (scene by scene; dialogue
recorded by him, then lip-synced in post; bump cards between scenes) and
which productions each spec serves: **Cape Jones (CJ), Wizard Gang (WG),
Western Heart (WH), Bannon (BN).**

| # | Spec | Size | Serves | Why this rank |
|---|---|---|---|---|
| 1 | **T-2 Rhubarb→MouthSwap bridge** | small | WG, CJ | Automates the exact hand-step every dialogue scene waits on |
| 2 | **M-1 Characterizer** (+M-2 sliders) | medium | CJ, BN, WH | Any mocap onto any character in minutes; feeds three productions |
| 3 | **S-1 + S-2 Ucupaint wire + SmartMask pack** | small | all four | Mostly donor adoption; texturing speed on every 3D asset |
| 4 | **A-1 Checkpoint render driver** | small | CJ first | Unblocks the owed 960×540 Scene 1 upgrade; de-risks all rendering |
| 5 | **C-1 EffectorKit** | medium | CJ, WG | Bump/title cards are structural to every episode; MoGraph on demand |
| 6 | **H-2 WedgeRunner** | small | all four | Force multiplier for every sim/render spec below it |
| 7 | **N-1 + N-3 Natron card kit + gizmo pack** | small | WG, CJ | Pipeline One's parallax signature + locked-in LOOK 1/LOOK 2 in comp |
| 8 | **H-1 GlueGraph destruction** | medium | CJ, WH, BN | Set-piece destruction gags and destructible game stages |
| 9 | **Z-2 Sculpt Finisher** (+Z-1 wrapper) | small | CJ, BN | One-pass sculpt → game-ready; steady value, lower urgency |
| 10 | **T-1 Puppet Control Sheets** | medium | WG | Cast-wide posing consistency; convention-heavy, lands slower |
| 11 | **H-4 Pyro shaping pack** | small | CJ, WG | Nicer fire/smoke presets; Mantaflow already covers the basics |
| 12 | **H-3 CrowdLite** | big | BN, WH | Highest cost on the map; build only when arena/town work is scheduled — the UE Mass route may supersede |
| 13 | **N-2 Deep-enough comp pipeline** | medium | CJ, WG | Only when a CG-through-smoke shot is actually boarded |

**Accepted gaps (no build planned):** Arnold stand-in/procedural rendering
(G-A1), Harmony-style shaped influence zones (G-T3), Maya graph-editor
parity (Blender's is adequate for our shots), Nuke's USD 3D system
(projection needs are covered by SPEC N-1's two routes).

---

## Sources (public documentation & write-ups, accessed 2026-10-30)

- Maya / HumanIK: Autodesk official docs — *HumanIK in Maya*,
  *Retargeting character animation*, *Example workflow: Non-destructive
  retargeting* (download.autodesk.com); Meshcapade's public HumanIK
  retargeting guide.
- Houdini: SideFX — *Destruction FX in SOPS* tutorial, Houdini FX product
  page (Pyro / FLIP / Bullet RBD / crowds feature descriptions);
  TOPs/PDG overview (bsm3d.com, summarizing SideFX docs).
- ZBrush: Maxon help-derived guides — DynaMesh / ZRemesher / PolyPaint /
  Decimation workflow summaries (3dx.info, fpnotebook ZBrush notes,
  ZBrush Characters & Creatures handbook).
- Substance 3D Painter: Adobe official docs — *Layer stack*
  (experienceleague.adobe.com); Adobe Substance 3D tutorial *Fast
  Texturing in Painter with Generators*; Painter 12.0 announcement
  (blog.adobe.com).
- Nuke: Foundry official docs — *Key Concepts* (learn.foundry.com: node
  workflow, 1023 channels, 32-bit pipeline, 3D compositing); Nuke Lead
  workflow write-up (saturation.io: deep compositing, camera projection,
  multi-pass).
- Natron: Natron official docs — *Nuke to Natron transition guide*
  ("What's not in Natron: mainly 3D functions; PMCard3D/PMcamera community
  scripts"); Natron community roadmap (3D + deep compositing slated for a
  future 4.0).
- Cinema 4D / MoGraph: Maxon official — MoGraph Basics and MoGraph /
  Effectors help pages (maxon.net, help.maxon.net: Cloner, 16 effectors,
  Fields, Fracture, Voronoi Fracture, Tracer).
- Toon Boom Harmony: Toon Boom official docs (docs.toonboom.com) — *How to
  Use Deformers* (Bone/Game Bone/Curve/Envelope/Free Form), *Rigging Tool
  Properties*, *About Rigging Drawings to Deformations* (Kinematic Output),
  Master Controller widget documentation.
- Tahoma2D / OpenToonz: Tahoma2D official docs — *Create animations using
  Plastic tool*, *Interface Overview* (Skeleton tool, Plastic tool, FX
  schematic) (tahoma2d.readthedocs.io).
- Arnold vs Cycles: renderer comparisons (cglounge.studio — Cycles
  production use, light/shadow linking in Blender 4.0; foro3d.com;
  softauthentic.com — Arnold AOVs, Cryptomatte, adaptive sampling,
  procedurals).
- Donors: Ucupaint (linuxlinks.com; 80.lv — Ucupaint 3.0 release;
  gamefromscratch.com), ArmorPaint 1.0 (creativebloq.com), Rokoko Blender
  plug-in + Quick Map retargeting (addons.cgdive.com; strayspark.studio
  animation add-on roundup).
