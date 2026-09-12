# God Molecule / Mars — Visual Editing Lock

**Status:** HARD LOCK  
**Owner:** Marq  
**Established:** 2026-09-11

## Non-negotiable likeness rule

Unless Marq explicitly asks for a **completely new character image**, **DO NOT generate a new character or a different likeness**.

When a source image is supplied, the source image is the identity authority. Perform **image-editing / Photoshop-style transformations on the supplied image itself** rather than asking an image model to invent a new person from a description.

### Identity is immutable

Preserve the actual source likeness, including facial structure/proportions, eyes, nose, mouth, jaw, beard, dreadlocks and their arrangement, silhouette, pose, and head/neck geometry when present.

**Do not redesign, reinterpret, beautify, replace, or hallucinate the person's face.**

**SUPPLIED PHOTO / 3D HEAD → PRESERVE IDENTITY → EDIT / COMPOSITE / GRADE → MARS TREATMENT**

Not: **SUPPLIED PHOTO → AI reimagines person → new Mars character**

## Mars visual treatment

- cobalt / electric-blue skin
- indigo / violet / magenta hair information
- solid glowing white eyes
- consistent forehead sigil
- black / near-black space
- small colorful diffraction / sparkle stars
- cyan / blue rim light
- saturated blue treatment
- crunchy / painterly facial and hair detail
- retro-digital / early-CD-ROM character feel

These are treatment layers, not permission to regenerate the person.

## Tonnō pipeline lock

1. Center 4:3 crop
2. Nearest-neighbor shrink to 640×480
3. Quantize to 256 colors using median cut
4. Floyd–Steinberg dithering

The Tonnō pass is a required creative stage. Do not silently remove it.

## Claude workflow reference

Use the documented Claude workflow as the production reference:

**inspect → measure → isolate/mask → align/map → modify → render → zoom/inspect → compare → iterate**

This includes segmentation, mask comparison, gridded crops, pixel/coordinate inspection, neck-cut refinement, sigil placement, eye placement, color-LUT matching, background cleanup, and repeated comparison.

Use deterministic/open-source image-processing tools for these operations where practical. Image-generation models are not the default identity-editing mechanism.

## Canonical reference policy

The highest-likeness approved Mars renders become canonical references.

Any result that changes the person's likeness is **INVALID** and must not become a canonical reference, character-sheet source, pipeline target, or repo asset.

**Likeness outranks style.**

## Generation exception

A new character image may be generated **only when Marq explicitly asks for a completely new character image**. Otherwise, use the supplied image and perform edits to it.
