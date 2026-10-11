# EP02 AI-SLOP AUDIT — Full Episode Analysis

**Date:** 2026-10-09  
**File:** wizard-gang-ep02-realanim-cut.mp4 (4:24)  
**Method:** 35 frame samples across full timeline, visual inspection

## SUMMARY

The episode has REAL character animation (verified). But it suffers from
inconsistent art style — some shots hold 2D cartoon, others drift into
semi-realistic 3D rendering. This inconsistency is the #1 AI tell.

## AI TELLS BY CATEGORY

### 1. STYLE DRIFT (3D/Realistic Creep)
The worst offense. The show is supposed to be 2D cartoon (🎨 cartoony base,
🖌️ painterly for dramatic beats). Instead:

- **~100s (war fund hat):** Cipher's skin has 3D subsurface scattering, realistic
  muscle definition, cinematic rim lighting. Looks like a 3D render, not 2D.
- **~190s (bridge exchange):** Both figures have photorealistic muscle shading,
  detailed pores, realistic fabric folds. Full 3D character render style.
- **~52s (robed lineup):** Red figure's face has AI-morphed gold teeth, skin
  has 3D volumetric shading instead of flat 2D colors.

**Good examples (holding 2D):**
- ~55s, ~64s (council table): Flat colors, bold outlines, proper 2D
- ~118s (Theory sketching): Clean anime style, perfect
- ~145s (Echo claw machine): 2D anime, holding the line

### 2. HAND ANATOMY
Classic AI tell. Hands morph between frames:
- Fingers merge into blobby masses in council scenes
- The money-hand at ~100s has 6+ finger-like protrusions
- Hands holding dice/cards lose individual finger definition

### 3. FACE MORPHING
- The red robed figure's face at ~52s: gold grill morphs between frames,
  teeth count changes
- Static's beard density shifts between shots
- Eye shapes warp slightly during dialogue

### 4. INCONSISTENT DETAIL DENSITY
AI adds random detail that wasn't in the still:
- Tattoos appear/disappear between frames on Cipher
- Background elements (posters, signs) have gibberish text
- The "IT SEES" tag is legible in still but becomes scribbles in motion

### 5. LIGHTING INCONSISTENCY
- Candle flames don't cast consistent light on faces
- Character shadows shift direction between cuts
- The bridge scene has moonlight from two different angles

### 6. TEXTURE POP
- Skin goes from flat 2D to detailed pores mid-shot
- Fabric goes from solid color to visible weave
- This happens WITHIN single clips, not just between shots

## TIMELINE OF BREAKS

| Time | Shot | Issue |
|------|------|-------|
| 52s | 10-1 | Red figure face morph, 3D skin shading |
| 100s | 12-3 | Full 3D render style, realistic hands |
| 190s | 20-1 | Photorealistic muscles, cinematic lighting |
| Various | Council | Hand blobs, finger merges |

## ROOT CAUSE

The video generation model is adding "cinematic quality" on top of the 2D
stills. My prompts said "real character motion" but didn't explicitly forbid
3D/realistic rendering. The model interprets "high quality" as "photorealistic."

## FIX REQUIRED

1. Regenerate problem shots with explicit style lock:
   "2D cartoon animation, flat cel-shaded colors, bold black outlines,
   anime/cartoon style, NOT 3D, NOT photorealistic, NOT CGI, NOT cinematic rendering"

2. Or: run problem segments through a 2D style transfer filter

3. The good shots (55s, 64s, 118s, 145s) prove the model CAN hold 2D —
   it's a prompting issue, not a capability issue.
