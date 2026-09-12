# In the Bushes — Open-Source Animation Stack

## Purpose

Use mature open-source animation tools to solve the project's actual production problems without replacing the deterministic story/timing system or adding unnecessary dependencies.

## Primary backend: OpenToonz

OpenToonz remains the primary traditional/cutout 2D production backend. It is a full open-source 2D animation system with reusable levels, Xsheet timing, effects and rendering. The official repository documents the project and its licensing: files outside `thirdparty` and the Mypaint brush library are under the Modified BSD license; those bundled areas have their own licenses and must not be copied into this project casually.

Official source: https://github.com/opentoonz/opentoonz

## Secondary escalation backend: Blender Grease Pencil

Blender 4.5 LTS Grease Pencil is the preferred escalation path when a shot needs:

- true stroke/point interpolation;
- deforming character parts;
- inherited/parented cutout motion;
- traditional frame-by-frame breakdowns;
- procedural 2D/3D staging;
- a more robust render/compositing pass.

Blender's current documentation explicitly supports traditional 2D, cutout animation, deformation and inherited animation. Its Interpolate Sequence tool can generate in-between keyframes between Grease Pencil drawings.

Official documentation: https://docs.blender.org/manual/en/4.5/grease_pencil/introduction.html

## Deterministic delivery layer

The current Python/SVG/FFmpeg pipeline remains the default for the low-fi opening because it is reproducible and cheap to execute. FFmpeg creates delivery video and FFprobe performs media validation.

## Integration rule

Open-source software is an **escalation path**, not an excuse to rebuild the entire pipeline. The authored scene JSON and motion-block JSON remain the source of truth for story timing and causal order.

When a shot fails because the procedural SVG rig cannot produce convincing deformation or interpolation, promote that shot to Blender Grease Pencil or OpenToonz rather than adding increasingly fragile one-off transforms to the Python compositor.

## Current production problems this stack addresses

1. **Characters looked too much like stick figures.** The procedural teen rig now uses developed character silhouettes, clothing, heads, hands, legs and shoes.
2. **Pose transitions could snap.** Numeric body/head/limb values now interpolate between pose states.
3. **The three teens could act like synchronized puppets.** Performer-specific delay and tempo values stagger their reactions.
4. **The render environment was not proven.** `tools/render_preflight.py` now fails fast when required SVG rasterization, FFmpeg, FFprobe, or source assets are missing.
5. **The pipeline could confuse a build description with a verified render.** Preflight is deliberately separate from render success; a render must produce media and pass FFprobe/QC before being called verified.
6. **Open-source tooling could be pulled in inconsistently.** This document records the approved roles of OpenToonz and Blender instead of copying third-party source into the production repo.

## Provenance rule

Do not vendor OpenToonz, Blender, FFmpeg, or their third-party libraries into this repository merely to claim they were "pulled in." Use official releases/source repositories and record versions when an actual production environment uses them. Only project-specific adapters, scripts, presets and original assets belong in this repository.
