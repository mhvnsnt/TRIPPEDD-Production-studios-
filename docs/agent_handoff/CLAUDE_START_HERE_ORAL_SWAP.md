# CLAUDE — START HERE (oral)

**When you come back online, read this first. Do not ask for drag-and-drop uploads.**

## Order

**Stop fixing the shredded seam mesh. Good head stays. Swap only the interior.**

## Repo

`mhvnsnt/TRIPPEDD-Production-studios-` (main)

## One command

```bash
chmod +x tools/character/run_oral_interior_swap.sh
export TRIPPEDD_PYTHON_BIN="${TRIPPEDD_PYTHON_BIN:-./.trippedd_venv/bin/python}"
tools/character/run_oral_interior_swap.sh
```

Prereqs validated first (`validate_oral_swap_prereqs.py`).  
Output: `assets/variants/MARS_ORAL_SWAP_REVIEW.blend`

## Assets

| Role | Path |
|------|------|
| Host | `assets/rigs/MARS_ORAL.blend` (904b419) |
| Fallback host | `assets/checkpoints/before-mouth-retopo/assets/rigs/MARS_ORAL.blend` |
| Interior | `assets/rigs/MARS_FACE.blend` |

## After swap

Runner prints exact pixel-truth + survey commands. Required:

1. `--pose open` pixel truth  
2. survey v3 (world plane)  
3. mouth_proof  
4. reopen PNG + SHA  
5. promote only with receipt  

## Do not

Ask for uploads · re-cut as primary · overwrite canonical · body-rig MARS (floating head)

Detail: `docs/agent_handoff/ORAL_INTERIOR_SWAP.md`
