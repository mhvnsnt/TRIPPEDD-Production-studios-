# Tongue seat + lip rim (2026-09-14)

## Tongue — rigid re-seat (not scale)

| Metric | Before | After |
|--------|--------|-------|
| Upper incisal edge (authority) | −0.97 mm | — |
| Lower crown tops (wrong target) | +0.66 mm | do not anchor here |
| Tongue dorsum | +7.68 mm | **−1.97 mm** (−9.66 mm) |
| Verts above upper incisal edge | 307 / 933 | **0 / 933** |
| Tongue thickness | ~18.6 mm | unchanged (already ~correct) |

**Gate that caught the bad target:** dorsum aimed at lower crown tops is still **above** the upper incisal edge (−0.97). Re-anchor on the edge the tongue must stay **under**, with ~1 mm clearance.

**Protected drift (must stay zero):**

| Object | Movement |
|--------|----------|
| MARS_TEETH_UPPER | 0.000000 mm |
| MARS_TEETH_LOWER | 0.000000 mm |
| MARS_MOUTH_SOCK | 0.000000 mm |
| MARS_MESH | 0.000000 mm |
| 32 GNM tongue shape keys | shifted with mesh; drift 0.000004 mm |
| tongue_root / mid / tip | move as one unit with mesh |

Shape keys are absolute positions — mesh-only shift would snap expressions back. Rigid unit preserves GNM tongue motion.

**Artifact:** `renders/_tongue/MARS_FACE_TONGUE.blend` (candidate).  
**Pixels:** `docs/evidence/mars/mouth/tongue_seated_WIDE.v001.png` (sha256 prefix `88ada58a…`).  
**Canonical:** untouched. Promote only on owner word + receipt.

**Naming note:** `MARS_TEETH_LOWER` may carry teeth **and** gums under one object — do not assume pink mass is tongue from object name alone; use pixel-ID / material class.

## Lip rim slivers — beautify_fill (partial)

300 faces within 8 mm of lip line:

| Metric | Value |
|--------|--------|
| Area median | 1.78 mm² (head median 0.436); max 136.68 |
| Smallest angle median | 32.7°; p5 3.9°; min 1.09° |
| Slivers &lt; 15° | 75 / 300 (25%) |

`bmesh.ops.beautify_fill` (or Blender beautify): **rotates edges, moves no vertices**.

| After beautify | Value |
|----------------|--------|
| Slivers | 75 → 61 |
| Worst angle | 1.09° → 1.85° |
| Vertex drift | **0.000000 mm** |

Partial: only 145/300 rim faces had both neighbours inside selection — rest cannot rotate without rewriting unmeasured faces.

## Still open (visual)

- Rim still jagged in render  
- Opening still reads as **rectangular slot**, not lip shape  
- Seam coverage / terminal straddlers still the geometry track for bridges  
- beautify helps spikes; does not replace seam extension or lip contour authority  

Pixels veto. No promotion on numbers alone.
