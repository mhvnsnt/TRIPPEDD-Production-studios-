# EP01 Prompt-Driven Production Skeleton

This is the first operator-facing shot sequence for turning the existing EP01 creative material into production work without waiting for autonomous agents.

The exact dialogue remains editable creative source. The sequence below is a production skeleton, not a canon rewrite.

## Opening language

The intended opening beat is a 2D/graphic introduction of Mars that establishes four directional looks before the direct-to-camera beat:

1. look left;
2. look away from camera;
3. look right;
4. look at camera.

The final 2D/clip-art treatment can use still-image animation, limited head/eye motion, mouth sprites, or a generated talking-head pass. The production compiler should preserve the source images as named references rather than treating generated frames as canonical character replacement.

## Voice / dialogue workflow

The operator supplies the final voice recording. Dialogue should therefore be stored as script text plus an external voice artifact, with timing/phoneme data generated from the actual supplied recording.

Recommended flow:

```text
approved dialogue text
  +
operator voice WAV
  -> timing / phoneme extraction
  -> 2D mouth or Blender viseme animation
  -> rendered intro shot
```

Useful OSS options include Rhubarb Lip Sync, Blender Lip Sync 2D, and Blender face-rig workflows. The existing canonical Mars rig remains authoritative for any 3D portion.

## Opening shot skeleton

### SHOT EP01-OPEN-001 — directional setup

Purpose: establish Mars as a graphic/2D character before the world reveal.

Coverage:
- left look;
- away look;
- right look;
- camera look.

Artifact targets:
- source image references;
- animation timing data;
- rendered preview;
- final voice timing if applicable.

### SHOT EP01-OPEN-002 — direct address

Action: Mars settles into a direct-to-camera pose and addresses the viewer.

Dialogue source: operator-supplied final script/voice recording.

Do not invent final dialogue in the production compiler. Store creative wording separately so the operator can revise it without changing the shot contract.

### SHOT EP01-OPEN-003 — space launch

Action: Mars rapidly moves away from camera and becomes smaller in frame.

Production strategy:
- begin with the established 2D/graphic representation;
- animate scale/translation/camera movement;
- transition to the next world-reveal shot through an authored transition rather than an unexplained asset swap.

### SHOT EP01-WORLD-001 — world transition

Action: graphic/purple-square imagery progressively resolves into a spatial world.

Preferred experimental path:

```text
2D graphic elements
  -> depth / point-cloud cues
  -> Gaussian-splat environment
  -> persistent 3D world representation
```

Gaussian-splat rendering is an optional environment representation. It must retain a stable world/scene identity and provenance and must not silently replace the deterministic scene representation when downstream interaction requires ordinary 3D geometry.

### SHOT EP01-WORLD-002 — exploration

Action: Mars is placed into the established world and begins showing the viewer around.

This is the first major canonical 3D proof slice:
- MARS_CANONICAL;
- persistent world definition;
- camera coverage;
- environment lighting;
- actual animation;
- supplied dialogue/voice;
- rendered pixels;
- visual QC;
- physical QC where applicable.

### SHOT EP01-KEVIN-001 — forehead-room reveal

Action: the forehead symbol/door mechanism opens as an actual spatial portal into a small persistent room containing Kevin.

Production requirements:
- Kevin becomes a separately tracked character asset;
- Kevin's room becomes a persistent location asset;
- portal mechanism is an animation/control surface, not a texture-only trick;
- opening/closing motion must be reproducible;
- continuity must preserve Kevin and the room across later appearances.

The exact Kevin design, dialogue, blocking and room dressing remain creative inputs to be supplied by the operator.

### SHOT EP01-KEVIN-002 — Kevin exits/reappears

Action: the portal opens, Kevin appears and addresses Mars/viewer, then the portal closes and restores the forehead symbol.

Animation decomposition:

```text
portal open
  -> face/forehead deformation
  -> spatial reveal
  -> Kevin blocking
  -> dialogue/lip sync
  -> Kevin retreat
  -> portal close
  -> canonical Mars facial state restored
```

### SHOT EP01-WORLD-003 — continued exploration

Mars continues through the world after the Kevin beat. New locations and props are added through persistent world definitions rather than one-off scene scripts.

### SHOT EP01-END-001 — dandelion transition / episode end

Action: Mars is pulled/sucked into a dandelion-like event and the episode ends.

This should be authored as a deterministic shot first, with generative video available as a treatment/reference option if it produces a better result without compromising continuity.

## OSS execution candidates

### 2D / talking intro

- `Charley3d/lip-sync` — Blender lip-sync addon using offline speech recognition, phoneme timing and shape-key/sprite approaches.
- Rhubarb Lip Sync — phoneme timing source for mouth sprites and face rigs.
- `revpriest/blenderquicktalk` — older Blender script-driven lip-sync option worth retaining as a fallback/reference.

### 3D animation

- `Larenju-Rai/open-mocap-blender` — offline/real-time pose and hand tracking with Blender retargeting.
- `squall01337/mixamo-llm-mocap` — video-to-animation pipeline designed to be scriptable by an AI agent.
- `wassermanproductions/blockout` — previs/blocking and camera choreography with Blender handoff.

### Gaussian splats / world transition

- `xy-gao/splatviz-blender` — Blender Gaussian-splat renderer with animated-camera support and depth/alpha compositing.
- COLMAP / gsplat / existing TRIPPEDD reconstruction adapters remain candidate world-capture backends.

### Prompt-to-Blender execution

- `PoBruno/mcp-blender-agent`
- `RFingAdam/mcp-blender`
- `ahmedsayed1911/Blender-AI-Agent`
- `harveyxiacn/blender-mcp`

These are execution adapters. TRIPPEDD remains authoritative for canon, production graph, provenance, QC and evidence.

## Operator prompt examples

```text
Build EP01 opening shot 001 using the approved Mars 2D references. Make him look left, away, right, then into camera. Do not replace the canonical Mars identity.
```

```text
Use my supplied voice recording for the Mars direct-address shot. Match the mouth animation to the recording and give me a first rendered pass.
```

```text
Take the purple-square transition and develop it into the first persistent Gaussian-splat world. Keep the world identity stable so we can continue building it in later prompts.
```

```text
Put MARS_CANONICAL into the world and block his first exploration sequence. Give me three camera options and a preview render.
```

```text
Add Kevin as a separate character living behind the forehead portal. Build his room as a reusable location and animate the portal opening, Kevin's entrance, dialogue beat, and closure.
```

## Evidence rule

Every completed prompt operation must eventually resolve to actual production artifacts. A successful natural-language response is not evidence. A render manifest is not pixel evidence. Actual pixels must be retrievable and reopened, then pass visual and physical gates before the work is promoted.
