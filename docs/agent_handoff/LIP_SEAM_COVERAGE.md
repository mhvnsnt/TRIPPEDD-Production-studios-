# Lip rim shards = seam **coverage**, not resolution

## Law

A fully split seam **cannot** have a face on both sides (duplicate verts share no face).  
If straddling faces exist, the **cut did not reach those lateral positions**.

## Measured (candidate, not canonical)

| Signal | Range / value |
|--------|----------------|
| Split pairs | x −22.5 … +22.1 mm — **ZERO beyond ±25 mm** |
| Straddling faces | x −28.3 … +33.9 mm — **9 of 43 beyond \|x\| 25** |
| Straddler median area | 13.98 mm² vs head median 0.44 mm² |

Worst bridges sit **exactly where there is no split**.

## Attempts (measured, not fixed)

| Attempt | Result |
|---------|--------|
| Densify rim | 326→2,328 verts near rim; straddlers **32→38**; pixel-identical. Subdividing a bridge makes more bridges. `_dense_rim_REJECTED.blend` |
| `--residual-rounds` | Refused (already split); banked worse |
| `--drop-bridges` | Removes 10 of 14 qualifying; keeps 4 visible at rest (safety). 32→27, area −5%, **render unchanged**. Real, not the visual fix |

Second group **inside** split span (x −20…−15 and +15…+20): cut chain passes through without separating every adjacent face — different defect, do not treat as pure end-extension.

## Instrument correction

Shard finder ±34 mm fan hit the **nose** → false “42 skin faces in open mouth.”  
At real aperture (±26 mm): **zero** skin faces; every `MARS_MESH` hit inside mouth is `MARS_ORAL_MAT` (cavity wall). Object name alone cannot answer skin vs cavity.

## Standing

- Canonical: untouched, verifying `same`
- Candidate: mouth_proof 8/8, crater 44→4/483 cells
- **Visual FAIL on open-mouth rim** — **not promoted**

## Next (coverage, not densify)

1. Extend / complete the seam cut **past ±25 mm** to the true commissure span where straddlers live  
2. Re-measure split-pair x-span vs straddler x-span (must overlap)  
3. Open-mouth pixel truth (`--pose open`) + SHA  
4. Only then consider drop-bridges as cleanup, not primary  
