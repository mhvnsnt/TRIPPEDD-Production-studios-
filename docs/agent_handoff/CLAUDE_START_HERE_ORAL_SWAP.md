# CLAUDE — START HERE (oral)

**When you come back online, read this first. Do not ask for drag-and-drop uploads.**

## Order

**Stop fixing the shredded seam mesh. Good head stays. Swap only the interior.**

## Repo

`mhvnsnt/TRIPPEDD-Production-studios-` (main)

## Assets (already committed)

| Role | Path |
|------|------|
| **Host** (good cavity + lips + weights) | `assets/rigs/MARS_ORAL.blend` (anchor **904b419**) |
| Checkpoint host | `assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend` |
| **Interior** (current teeth / seated tongue) | `assets/rigs/MARS_FACE.blend` |
| Recovery law | `docs/evidence/MARS_ORAL_KNOWN_GOOD_RECOVERY.json` |

## Script (already on main — commit family `a9af64db`)

```bash
# optional inventory
blender -b -P tools/character/swap_oral_interior_onto_donor_head.py -- \
  --list-only \
  --host assets/rigs/MARS_ORAL.blend \
  --interior assets/rigs/MARS_FACE.blend

tools/character/run_oral_interior_swap.sh
# → assets/variants/MARS_ORAL_SWAP_REVIEW.blend
```

Or:

```bash
blender -b -P tools/character/swap_oral_interior_onto_donor_head.py -- \
  --host assets/rigs/MARS_ORAL.blend \
  --interior assets/rigs/MARS_FACE.blend \
  --out assets/variants/MARS_ORAL_SWAP_REVIEW.blend
```

## Steps the script performs

1. Open known-good **host**  
2. Delete **only** teeth / gums / tongue  
3. Append current teeth / gums / seated tongue from **interior**  
4. Parent to host armature (jaw / tongue bones)  
5. Save **review-only** under `assets/variants/` — **never** overwrite canonical by default  

## After the swap (required before any promote)

1. Open-mouth pixel truth: `--pose open`  
2. `survey_oral_aperture.py` v3 (world plane)  
3. mouth_proof  
4. Reopen PNG + SHA-256  
5. Receipt only — pixels veto numbers  

## Do not

- Ask the owner to upload .blend/.glb  
- Re-run densify / residual-rounds / re-cut as the primary fix  
- Treat rim beautify as solving weight corruption  
- Call Rigify working on MARS without weights + pixels  
- Invent body-rig work — **MARS is a floating head**  

## Parallel agents

- **Google AI Studio:** Studio UI / mesh viewer / export (PAT)  
- **Grok:** handoff + swap tooling on main  
- **Claude:** physical Blender execution of this swap + proof pixels  

Detail: `docs/agent_handoff/ORAL_INTERIOR_SWAP.md`
