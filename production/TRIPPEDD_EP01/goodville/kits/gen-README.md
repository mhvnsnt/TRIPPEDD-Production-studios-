# gen/ — Generated + Curated Piece Library (owner 2026-10-11)

**Purpose:** Double/triple each kit's piece count with additional variants and templates.
Owner directive: "Generate some pieces with the downloaded kits as base but using my
characters and kit pieces I made as generation goals... this will double or triple the pack."

## What's in here

**AI-generated variants** (`*_gen.png`):
- Created with `tools/image-gen/likeness_gen.py` (FLUX Kontext, image-conditioned)
- Source: the character's own pieces (eyes_open, mouth_smile, etc.)
- Method: variant instructions ("same eyes but squinting") on the character's likeness
- Each verified by human eyes; drifted outputs discarded (documented below)

**Curated SP templates** (`mouth_sp_*.png`, `eyes_sp_*.png`):
- From `~/workspace/tools/sp-studio-parts/` (South Park Avatars app, fan-made)
- Pre-styled South Park pieces for use as generation templates or direct swaps
- Mouths are universally interchangeable (proven); eyes are style references

## Licensing

- **AI-generated variants:** Transformative outputs from our own character pieces. Ours.
- **SP templates:** Fan-made, unlicensed (no license file in source repo). Used as
  GENERATION BASES and style references per the PULL-IN DIRECTIVE. Direct pixel use
  in shipped kits needs owner sign-off. Our show is parody; the parts belong to the fan artist.

## Rules

- Originals NEVER modified. Everything here is additive.
- All pieces are movable layers (paper-cutout method). Nothing baked in.
- Generated pieces must seat on the character's measured anchors.

## Discarded (likeness drift / wrong style)

- crown-hoodie: X-eyes (came back cross-eyed), tongue-out (photorealistic), wide-yell (anime)
- headband-girl: 3 eye variants (lash artifacts), 2 mouths (generated full faces)
- red-cap-guy: 3 eye variants (model ignored instructions)
- dickie/bubba/sten: squint variants (anime/bad-crop/glitch)
- old-head: pupil shifts N/A (wears aviators, no visible pupils)
