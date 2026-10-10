# God Molecule — Mars Reference Contract

Status: ACTIVE / CANONICAL REFERENCE POLICY

## Purpose

Mars must remain recognizably the same person when the production system generates or transforms imagery.

The supplied photographs are identity and geometry evidence. The blue/space images are style references. They are not permission for a generator to invent a different face, erase the neck, or redesign the back of the head.

## Two different commands

### A. Direct image generation

When the showrunner asks ChatGPT to **generate an image**, that is a direct image-generation request. The image-generation tool may be used.

### B. Repository generation

When the showrunner says **use the repo / production studio / open-source stack to generate it**, do NOT substitute direct ChatGPT image generation.

Run the TRIPPEDD generative pipeline against the canonical reference set. The pipeline must record the model/backend, workflow, source hashes, seed, parameters, and output QC.

This distinction is a production contract.

## Identity lock

The pipeline must preserve:

- facial proportions and recognizable likeness
- dreadlock silhouette and hair mass
- beard/mustache structure
- complete lower jaw
- front, side, and rear neck connection
- complete back-of-head volume
- head-to-neck transition

A generated result that becomes a floating face, clips away the underside/back of the neck, invents a materially different face, or changes the hair silhouette without an explicit request is **FAIL**, not a creative variation.

## Generation hierarchy

1. **Reference-preserving edit** — preferred for likeness-sensitive 2D work.
2. **Multi-view reconstruction** — preferred when a complete 3D head is required.
3. **3D render + controlled style pass** — preferred for repeatable animation.
4. **Generative image/video variation** — allowed only inside an explicit style/change mask.
5. **Free generation** — only when the showrunner explicitly asks for a new character/design.

## Canonical Mars look

- disembodied floating head, but with complete physical head/neck geometry
- deep cobalt/blue treatment
- controlled violet/indigo shadows
- solid white eyes
- embossed/raised forehead sigil
- black/space-like background
- small sparkling stars
- retro early-3D / low-resolution / banded / limited-palette finish

The style layer may be changed. Identity geometry may not be silently changed.

## Approved weirdness

Expression changes can be deliberately modular: eyes, eyebrows, mouths, teeth, overlays, cutaway head windows, texture glitches, and other graphic elements may be swapped independently.

The face itself remains the anchor.

## Failure law

UNKNOWN is not PASS.

Every generated Mars asset must report:

- source reference hashes
- identity/reference mode
- generation backend
- model/checkpoint identifier when available
- seed and generation parameters
- output dimensions
- orientation
- alpha/background state
- QC result
- failure reasons when rejected

No artifact is canonical merely because a model produced it.
