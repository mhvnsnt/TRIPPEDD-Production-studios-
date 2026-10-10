# Oral interior swap — stop healing the shredded seam mesh

## Problem Gemini correctly named

`split_lip_seam` / repeated boolean work compromised topology and **vertex weights**.
Shards, gray pull-through, and spikes under deformation are weight/topology corruption,
not something a rim densify or beautify alone will fix.

## Solution: two good halves, one assembly

| Piece | Source |
|-------|--------|
| **Host** — head surface, cavity walls, sock, skin weights | `assets/rigs/MARS_ORAL.blend` (anchor commit **904b419**) or `assets/checkpoints/before-mouth-retopo/.../MARS_ORAL.blend` |
| **Interior** — improved teeth / gums / **seated tongue** | Current `assets/rigs/MARS_FACE.blend` (or tongue candidate blend) |

Do **not** re-cut the host lips to import a “perfect opening.”  
Do **not** try to re-weight the shredded shell.  
Bring the new interior **into** the good host.

## Repo paths (already committed — Gemini does not need an upload)

```text
https://github.com/mhvnsnt/TRIPPEDD-Production-studios-

assets/rigs/MARS_ORAL.blend              # ~5 MB known-good oral host
assets/rigs/MARS_FACE.blend              # current face+oral
assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend
docs/evidence/MARS_ORAL_KNOWN_GOOD_RECOVERY.json
```

## Run

```bash
# inventory names if needed
blender -b -P tools/character/swap_oral_interior_onto_donor_head.py -- \\
  --list-only \\
  --host assets/rigs/MARS_ORAL.blend \\
  --interior assets/rigs/MARS_FACE.blend

tools/character/run_oral_interior_swap.sh
# or:
blender -b -P tools/character/swap_oral_interior_onto_donor_head.py -- \\
  --host assets/rigs/MARS_ORAL.blend \\
  --interior assets/rigs/MARS_FACE.blend \\
  --out assets/variants/MARS_ORAL_SWAP_REVIEW.blend
```

## After swap

1. Open-mouth pixel truth (`--pose open`)  
2. Survey with world-consistent lip plane (v3)  
3. mouth_proof  
4. Reopen PNG + SHA  
5. Promote only with receipt — **never** default-write canonical  

## Canon reminder

MARS is a **floating head**. Oral work is face/oral only — not a body-rig project.
