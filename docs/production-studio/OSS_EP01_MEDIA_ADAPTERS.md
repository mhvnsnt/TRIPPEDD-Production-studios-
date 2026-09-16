# EP01 Open-Source Media Adapter Map

The goal is not to replace TRIPPEDD with a collection of AI video projects. The goal is to give each production problem a bounded adapter that can be called from the same prompt-driven production graph.

| Production problem | Candidate OSS | TRIPPEDD role |
|---|---|---|
| 2D mouth animation from supplied voice | `Charley3d/lip-sync` | Generate Blender mouth timing/visemes; return artifact metadata |
| Script/phoneme mouth fallback | `revpriest/blenderquicktalk` | Legacy fallback for simple rigs |
| Video-to-body motion | `Larenju-Rai/open-mocap-blender` | Produce retargetable motion from reference performance |
| AI-agent video-to-motion | `squall01337/mixamo-llm-mocap` | Convert an approved reference clip into structured animation |
| Previs/blocking/camera | `wassermanproductions/blockout` | Generate marks, camera choreography, reference package and Blender handoff |
| Gaussian-splat world rendering | `xy-gao/splatviz-blender` | Render splat environment with animated cameras and depth/alpha compositing |
| Prompt-to-Blender execution | `PoBruno/mcp-blender-agent` | Typed scene operations |
| Prompt-to-Blender + visual refinement | `RFingAdam/mcp-blender` | Broad Blender operations and iterative visual feedback |
| Prompt planning + controlled Blender + vision | `ahmedsayed1911/Blender-AI-Agent` | Semantic planning, controlled execution and visual review |
| Broad Blender MCP | `harveyxiacn/blender-mcp` | Alternative execution backend |
| Story/shot manifests + generative video | `koo-bros/4brospix` | Non-canonical generative shots, shot manifests and finishing experiments |

## Selection rules

1. Prefer deterministic Blender/rig animation for canonical Mars continuity.
2. Use supplied operator voice as the timing authority for dialogue shots.
3. Use phoneme/viseme systems to generate editable timing, not to invent final dialogue.
4. Use motion capture/reference-video systems when they improve blocking, then retarget into the canonical rig.
5. Use Gaussian splats for world appearance, reconstruction, transition effects and exploration where appropriate; retain a conventional 3D representation when interaction/physics/precise continuity requires it.
6. Generative video may create references, treatments, transitions and non-continuity material, but cannot silently substitute for `MARS_CANONICAL`.
7. Every adapter must return machine-readable provenance and actual artifact paths/identifiers.
8. Rendered pixels must still pass the existing TRIPPEDD evidence and QC gates.

## EP01 media path

```text
2D Mars references
  -> directional look animation
  -> operator voice recording
  -> phoneme/viseme timing
  -> direct-address shot
  -> authored zoom/flight transition
  -> Gaussian-splat / world reveal
  -> persistent world + canonical Mars
  -> mocap / semantic blocking / rig animation
  -> Kevin portal scene
  -> continued exploration
  -> dandelion end event
```

This is intentionally modular. If one OSS project becomes unavailable, the prompt contract and production graph remain stable and another adapter can take its place.
