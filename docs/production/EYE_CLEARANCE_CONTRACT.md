# Eye Clearance Contract (Mars)

**Status:** ACTIVE — parallel track with live Blender seating/ladder work.

## Authority

- Donor: `assets/donor/gnm_eyes/eye_{L,R}.npz` (ICT-FaceKit assembly)
- Manifest: `assets/donor/gnm_eyes/manifest.json`
- Each eye = 1926 verts = eyeball + occlusion + lacrimal
- Linework plates remain visual authority for lid placement

## Hard rules (fail-closed)

1. **Class filter is mandatory**  
   Penetration / clearance samples MUST be restricted to the **globe** (eyeball) vertex class only.  
   Socket / occlusion / lacrimal verts are ignored for eyelid	o globe distance.

2. **Rest penetration before blink travel**  
   If any globe verts are inside the lid surface (or lid verts inside the globe) at rest (0.00 aperture travel), that is a seating error, not a blink failure.  
   Resolve rest clearance first. Do not trust blink numbers until rest is clean.

3. **Local travel, not global aperture**  
   Required lid travel is measured along the measured lid curve length, not a single global aperture denominator.

4. **No invented geometry**  
   Do not replace the donor. Do not invent a new sphere. Use the existing ICT assembly.

5. **No PASS from numbers alone**  
   Ladder receipt + rendered frames (reopened bytes) are both required.

## Current seating baseline (as of last measured re-seat)

| Metric | Value |
|--------|-------|
| Centre depth | 14.24 mm |
| Nearest vertex → lid | 0.49 mm |

These numbers supersede the previous 82 mm / 55 mm placement error.

## Surface constraint (first path)

Native Blender Shrinkwrap on lid vertex groups:

- Target: globe mesh (globe class only if split)
- Wrap Method: Nearest Surface Point (or Project if needed)
- Snap Mode: **Outside Surface**
- Offset: start at measured nearest-vertex clearance (~0.3–0.5 mm)
- Modifier order: Shrinkwrap **before** any Solidify

This is the production-first constraint. Corrective shape keys / vector fields come only after the constrained ladder is clean.

## Ladder receipt (what the live track must emit)

Per eye, per step (open / intermediate / closed):

```json
{
  "eye": "L|R",
  "step": "open|intermediate|closed",
  "minClearanceMM": 0.0,
  "penetrationSamples": 0,
  "localTravelMM": 0.0,
  "renderPath": "renders/.../frame_....png",
  "renderSHA256": "...",
  "classFilter": "globe_only"
}
```

Aggregate:

- rest penetration samples (must be 0 or documented residual)
- left / right independence
- full open	o closed sequence with eyes present

## Open-source references (next layer only)

After clearance is clean:

- ICT-FaceKit (already our donor source)
- Google GNM (already in pipeline)
- AniEyelid (SIGGRAPH Asia 2024) — contact / animatable lids reference
- Example-based facial rigging (corrective shape personalization)
- Native Blender Shrinkwrap patterns for eyelid	o eyeball

## Parallel split

| Track | Focus |
|-------|--------|
| Live Blender | Seating, class filter, ladder, renders |
| This contract | Measurement rules, Shrinkwrap path, fail-closed gates |

Do not mark clearance permanently NOT_ATTEMPTED while the donor and tools exist on main.
