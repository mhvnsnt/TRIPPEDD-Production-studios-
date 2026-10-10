# In the Bushes — Animation Pipeline

**Status:** Active production tooling
**Branch:** `co-producer`

## Goal

Give *In the Bushes* a real, reproducible 2D animation path instead of treating animation as a future placeholder.

## Open-source stack

### Primary 2D animation: OpenToonz

OpenToonz is the primary traditional/cutout 2D animation backend for this show. It provides raster/vector drawing, timeline/xsheet animation, compositing, FX, and cutout-style workflows. It is open source and explicitly permits commercial and non-commercial use. See the official project: https://github.com/opentoonz/opentoonz

### Procedural / reusable animation: Blender Grease Pencil

Blender is the secondary procedural animation backend. Grease Pencil supports frame-by-frame drawing, object transforms, deformation, parenting, modifiers, and 2D animation inside a 3D scene. This is useful for reusable Busch rigs, camera moves, transformation effects, and automated scene generation.

### Media/render: FFmpeg + FFprobe

FFmpeg remains the deterministic media renderer/encoder and FFprobe remains the inspection tool.

## Production architecture

```text
story / dialogue
      ↓
shot + timing data
      ↓
reusable Busch assets
      ↓
OpenToonz / Blender animation
      ↓
compositing + camera + FX
      ↓
FFmpeg render
      ↓
QC / provenance
      ↓
master / clips / shorts
```

## First animation target

The first actual animated sequence is the opening/title-card beat:

1. Nighttime ambience.
2. Teenagers panic.
3. Someone shouts **“IN THE BUSHES!”**
4. Beer is thrown into the bush.
5. Beer hits and soaks the foliage.
6. Busch transforms / wakes up.
7. Busch looks away and reacts.
8. Brief hold.
9. **IN THE BUSHES** title card appears.

The look-away is a deliberate comedic timing beat and must remain visible before the title card.

## Animation philosophy

The show is intentionally economical. We should prefer:

- reusable Busch poses
- held frames
- mouth swaps
- eye swaps
- small branch gestures
- object translation
- camera pushes/pans
- shake/impact presets
- limited transformation FX
- sound-driven timing

over bespoke full animation for every frame.

## Asset strategy

Busch should become a reusable production asset with named states:

- `busch_idle`
- `busch_confused`
- `busch_drunk`
- `busch_look_away`
- `busch_reaction`
- `busch_wake`
- `busch_transform`
- `busch_surprised`

The asset library should be versioned with the show so future episodes can reuse the same character language.

## Interchange

Use OpenTimelineIO for editorial timing where practical. Keep source artwork and project files separate from delivery renders. Every generated render should retain provenance back to its scene data and asset versions.

## Immediate build order

1. Create Busch design/asset sheets.
2. Build the reusable Busch rig/pose library.
3. Build the nighttime bush environment.
4. Implement the beer impact and transformation preset.
5. Implement the look-away/reaction beat.
6. Implement the title-card transition.
7. Render a first 10–20 second proof.
8. Expand the proof into the complete origin opening.

## Source/licensing note

Open-source software is infrastructure, not creative source material. Do not copy third-party characters, artwork, scenes, or distinctive designs into the show. The show remains an original TRIPPEDD Production Studios property.
