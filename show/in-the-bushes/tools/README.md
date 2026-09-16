# In the Bushes — deterministic opening preview

`build_origin_opening.py` is the executable bridge between the authored opening scene/motion data and a rendered preview.

## Source of truth

- `../animatic/ep01-origin-opening-v2.scene.json` — 37-second, 13-shot timing master.
- `../animatic/ep01-origin-opening-v2.motion-blocks.json` — v4 authored movement blocks.
- `../animatic/ep01-origin-opening-v2.render-plan.json` — delivery/QC contract.
- `../assets/` — original show artwork.
- `teen_performance.py` — procedural teen character performance layer.

## Local build

From the repository root:

```bash
python3 show/in-the-bushes/tools/validate_origin_opening.py
python3 show/in-the-bushes/tools/test_render_source.py
python3 show/in-the-bushes/tools/build_origin_opening.py --preview
```

For the full 1080p master:

```bash
python3 show/in-the-bushes/tools/build_origin_opening.py
```

The builder requires Python 3, FFmpeg, and either `rsvg-convert` (preferred) or ImageMagick (`magick`/`convert`). It writes generated media under `show/in-the-bushes/build/`, which remains build output rather than source art.

## Current opening contract

The active opening is **888 frames / 37 seconds / 1920×1080 / 24fps**. The causal sequence is:

**ALLEY HANGOUT → POLICE ARRIVE → “SHIT! THEY'RE COMING!” → RUN/DUCK/HIDE → REALIZE THE BEER → “WHAT DO WE DO WITH THE BEER?” → “IN THE BUSHES!” → RUN OUT OF ALLEY → THROW → TRANSFORMATION → BUSCH WAKES → PROCESSES → LOOKS AWAY → REACTION HOLD → TITLE.**

The teens must physically leave the alley before the beer throw. The spoken title phrase must occur before the throw. The look-away is its own comedy beat before the title cut.

## Animation architecture

The opening keeps background, procedural characters, props, FX, Busch and title as independent layers. Teen motion uses pose interpolation, articulated limbs, clothing/head construction, performer-specific timing and different acting behavior rather than whole-sheet translation.

Busch's current compositor placement preserves the organic character silhouette instead of stretching the authored 800×800 character art into the 16:9 frame. His wake transform is centered on the character's local placement.

OpenToonz remains the primary manual 2D escalation backend; Blender Grease Pencil is the secondary escalation path for deformation or stroke-level animation that exceeds the procedural layer. FFmpeg/FFprobe provide deterministic media delivery and QC.

## QC intent

A verified master must have exactly 888 frames at 24fps, 1920×1080, with valid media reported by FFprobe. Source smoke tests and the continuity validator run before expensive rendering. A successful source/preflight check is **not** itself a claim that the final render has succeeded.

Audio remains an editorial layer so recorded dialogue and sound can be added without changing picture timing.