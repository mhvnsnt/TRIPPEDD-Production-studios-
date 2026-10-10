# Prompt Production Mode

## Purpose

TRIPPEDD should be operable by creative prompts before the autonomous production agents are mature enough to drive the entire studio themselves.

The operator-facing contract is:

```text
creative prompt
  -> production intent
  -> typed scene/world/shot operations
  -> controlled Blender execution
  -> actual render artifacts
  -> visual + physical inspection
  -> evidence
```

The prompt is a **creative input**, not production evidence.

## Open-source execution targets

The first execution adapter should support an MCP-connected Blender session. Candidate open-source implementations include:

- `PoBruno/mcp-blender-agent` — typed Blender operations covering modeling, rigging, animation, materials, geometry nodes, rendering, and export.
- `RFingAdam/mcp-blender` — broad Blender MCP coverage plus viewport/render feedback and self-refinement workflows.
- `ahmedsayed1911/Blender-AI-Agent` — prompt planning, validated generation, read-only vision review, semantic motion, and artifact export.
- `koo-bros/4brospix` — experimental story/shot manifests, ComfyUI/video generation, Blender layout, and render organization.

These are adapters/inspiration, not authorities. TRIPPEDD owns production state, identity, provenance, gates, and evidence.

## Prompt contract

A prompt may express:

- episode/segment intent;
- location or world intent;
- characters and canonical identities;
- props and set dressing;
- camera language;
- lighting/look intent;
- blocking and animation intent;
- dialogue/performance intent;
- shot count and coverage;
- references to existing canon or previously published assets.

The compiler must resolve that request into existing production entities where possible. It must not silently create a replacement for a `LOCKED_CANON` asset.

## Execution boundary

The model must not receive unrestricted authority to mutate production truth.

The preferred boundary is:

```text
Prompt
  -> TRIPPEDD production intent
  -> validated Scene IR / production graph operations
  -> MCP Blender adapter
  -> Blender
```

The adapter may create or modify scene content, but every mutation must remain attributable to:

- production intent ID;
- scene/shot ID;
- upstream asset versions;
- executor/tool version;
- resulting Blender scene artifact.

## Render/refinement loop

For interactive prompt-driven work, the adapter should support:

1. Build or modify the requested scene.
2. Save the `.blend` artifact.
3. Render a bounded preview.
4. Return actual viewport/render pixels.
5. Run read-only visual inspection.
6. Apply bounded corrections.
7. Re-render.
8. Stop after the configured iteration budget or a successful visual gate.

A successful model response is never sufficient evidence of completion.

## Canonical Mars rule

For God Molecule, prompts such as:

> Put Mars in the motel room and animate him walking to the bathroom.

must resolve `MARS_CANONICAL` rather than generating a new face/character approximation.

The resulting scene must use the canonical identity and the existing world/scene contracts. If the requested action cannot be executed without replacing canonical identity, the operation blocks instead of silently substituting a generated character.

## Animation strategy

Prompt-driven animation should be decomposed rather than delegated to a single generative video model:

```text
intent
 -> blocking
 -> rig controls / semantic motion
 -> IK / constraints
 -> keyframes or retargeted motion
 -> interaction constraints
 -> camera coverage
 -> preview render
 -> visual review
```

Generative video can be used for appropriate non-continuity shots, references, or compositing elements, but it must not silently replace canonical 3D production when continuity is required.

## World-building strategy

A prompt can request a new world/location, but the compiler should first search the production graph and world registry for an existing reusable definition.

For a new location, create a persistent definition containing at minimum:

- world/scene ID;
- deterministic seed where procedural generation is used;
- units/up-axis;
- environment recipe;
- reusable geometry/assets;
- materials/look rules;
- lighting rules;
- camera conventions;
- continuity dependencies;
- provenance.

The first scene generated from a new world is a proof slice. It does not automatically become canon merely because Blender generated it.

## Safety and fail-closed rules

The prompt production adapter must block when:

- the requested canonical asset cannot be resolved;
- required Blender execution is unavailable;
- the scene artifact was not saved;
- rendered bytes cannot be reopened;
- evidence refers to a different scene/shot;
- an upstream asset changed after evidence was produced;
- visual QC fails;
- physical QC fails when applicable;
- the operation would replace locked canon without explicit authorized override.

## User experience target

The eventual operator experience should be as close as possible to:

```text
User: Make the EP01 motel cold open. Mars wakes up, sits on the bed,
looks toward the door, gets up and walks to the bathroom. Use the
established motel world and cinematic night lighting. Give me the
coverage and a first rendered pass.
```

TRIPPEDD should turn that into production work rather than returning only a plan.

The operator should receive:

- what was actually created;
- the Blender scene artifact;
- rendered pixels/previews;
- any failures or blocked operations;
- evidence and provenance;
- the next actionable production state.

## Relationship to autonomy

Prompt Production Mode is not a competing architecture to autonomous agents.

It is the **human-operated front end of the same production graph**. Later autonomous agents should call the same typed operations and gates instead of inventing a separate execution path.

This allows creative production to begin immediately while the autonomous studio is still being hardened.
