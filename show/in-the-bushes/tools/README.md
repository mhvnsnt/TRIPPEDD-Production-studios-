# In the Bushes — deterministic opening preview

`build_origin_opening.py` is the first executable bridge between the authored opening scene/motion data and a rendered preview.

## Source of truth

- `../animatic/ep01-origin-opening-v2.scene.json` — 29.5-second shot timing.
- `../animatic/ep01-origin-opening-v2.motion-blocks.json` — authored movement blocks.
- `../animatic/ep01-origin-opening-v2.render-plan.json` — delivery/QC contract.
- `../assets/` — original show artwork.

## Local build

From the repository root:

```bash
python3 show/in-the-bushes/tools/build_origin_opening.py --preview
```

For a 1080p master:

```bash
python3 show/in-the-bushes/tools/build_origin_opening.py
```

The builder requires Python 3, FFmpeg, and either `rsvg-convert` (preferred) or ImageMagick (`magick`/`convert`). It writes generated media under `show/in-the-bushes/build/`, which is intended to remain a build output rather than source art.

## Why this exists

The opening should feel like animation rather than a slideshow. The builder keeps background, characters, props, and FX as independent layers and consumes explicit motion blocks. It preserves the locked story order: **IN THE BUSHES! → throw → beer soaks bush → delayed transformation → Busch looks away → reaction hold → title.**

This is a preview/backend bridge, not a replacement for the OpenToonz production scene. OpenToonz remains the primary 2D authoring backend in the render plan; this path gives the team a deterministic, scriptable proof and a place to validate timing before a full production scene is authored.

## QC intent

A successful build must produce exactly 708 frames at 24fps, 1920×1080 for the master, with the title isolated to S11. Audio is not synthesized by this script; dialogue and sound remain an editorial layer so recorded performances can be dropped in without changing picture timing.
