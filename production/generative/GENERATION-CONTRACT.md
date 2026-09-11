# TRIPPEDD Generative Production Contract

## Purpose

Generative tools are production components, not autonomous authors. A reference image, approved character sheet, approved audio stem, or approved shot plate is authoritative unless the user explicitly requests transformation.

## Identity lock

For a supplied person/reference:
- Preserve facial identity, skin tone, hair, body proportions, distinctive marks, wardrobe and approved character geometry.
- Do not invent a new face because a model can.
- Do not change age, ethnicity, facial structure, body shape, skin color or distinctive features unless explicitly requested.
- Every generated image/video shot carries the reference asset IDs and generation parameters used to make it.

## Shot continuity

Every shot records:
- reference image IDs
- character/asset IDs
- camera/framing
- aspect ratio and orientation
- lighting/color intent
- seed/model/checkpoint
- requested transformations
- continuity constraints
- QC results

## Generation graph

Reference image -> identity/reference conditioning -> image generation or edit -> video generation/animation -> lip sync/audio -> compositing -> QC -> editorial asset.

Primary engines:
- ComfyUI as the orchestration graph
- InstantID/IP-Adapter for identity/reference conditioning
- Wan/LTX/Open-Sora for video generation
- LivePortrait/MuseTalk for portrait motion and dialogue
- Blender/OpenUSD/MaterialX/OpenEXR/OCIO for 3D/VFX continuity
- ACE-Step/Audacity/Ardour for music and sound

## QC gates

Reject a generated shot when:
- identity similarity falls below the configured reference threshold
- orientation/aspect ratio changes unexpectedly
- an approved wardrobe/prop/mark disappears without instruction
- temporal identity flicker exceeds the configured threshold
- lip sync fails
- frame dimensions/FPS/audio contract fails
- generated content contradicts the shot brief

The system may propose alternatives, but it must not silently substitute them for the approved reference.

## Licensing

Code licenses, model licenses, checkpoints, training-data terms and commercial-use rights are tracked separately. A project is not marked production-ready merely because its GitHub code is open source.
