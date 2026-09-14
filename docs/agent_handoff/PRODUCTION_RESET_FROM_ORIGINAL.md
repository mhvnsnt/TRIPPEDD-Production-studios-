# PRODUCTION RESET — original model + GNM + linework

## Decision (owner)

We have gone far enough on a **corrupted progressive assembly** (seam cuts, densify,
bridge drops, weight damage, false instruments). That lineage is **frozen**.

**Start over from the original model** that did not accumulate those errors.
Place GNM, use owner linework, run the perfected gates. Salvage good *pieces*
as donors — do not keep the broken whole as the working authority.

## What stays (salvage as donors / evidence)

| Piece | Keep as |
|-------|--------|
| Owner facial linework PNGs + index | **Authority** for lids/brows/nostrils |
| ICT / `assets/donor/gnm_eyes` | Eye globe donor |
| GNM oral npz + provision chain | Oral anatomy donor |
| Tongue seat measurements (under upper incisal) | Placement rule |
| Eye clearance contract / ladder / gate | Measurement law |
| Known-good `MARS_ORAL.blend` @ 904b419 | Optional cavity reference only |
| Pixel-truth / survey v3 / receipt law | Evidence law |
| Show canon: MARS = **floating head** | Non-negotiable |

## What stops (do not continue as primary path)

- Further surgery on current shredded `MARS_FACE` seam topology as the main job  
- Densify / residual-rounds / re-boolean to "fix" rim spikes on the broken mesh  
- Treating progressive candidate blends as canonical  
- Body-rig framing (wrong show)  

Historical scripts remain in repo for evidence; they are **not** the default queue.

## Clean restart pipeline

```text
ORIGINAL SOURCE
  assets/source_models/MARS_LOD2.glb   (or earliest clean scan GLB)
       ↓
IMMUTABLE SNAPSHOT
  assets/variants/MARS_RESET_BASE_<date>.blend  (copy only; never edit in place)
       ↓
WELD / MANIFOLD CHECK (measure; repair only if measured)
       ↓
OWNER LINEWORK registration (eyes / lids / brows / nostrils)
       ↓
GNM ORAL place (provision → build donor → bridge behind lip plane)
  — no synthetic radial jaw on skin
  — tongue under upper incisal edge rule
       ↓
ICT / gnm_eyes place + clearance ladder
       ↓
OPEN-MOUTH + REST pixel truth (linear buffer)
       ↓
SHA + receipt + mouth_proof / eye gates
       ↓
PROMOTE only if pixels pass
```

### Commands (physical session)

```bash
# 1. Snapshot from original GLB (example — adapt to your import path)
#    Import MARS_LOD2.glb → save assets/variants/MARS_RESET_BASE.blend

# 2. GNM oral onto clean host (existing chain — not seam surgery)
export TRIPPEDD_PYTHON_BIN=./.trippedd_venv/bin/python
tools/character/provision_oral_donors.sh
# build bridge against RESET base + measured mouth frame

# 3. Eyes from donor + linework authority
#    assets/references/mars_facial_linework/
#    assets/donor/gnm_eyes/

# 4. Gates
#    eye_clearance_ladder / eye_clearance_gate --verify-renders
#    render_mars_oral_pixel_truth.py --pose open
#    survey_oral_aperture.py (world plane v3)
```

Optional: if RESET base has no cavity yet, `oral_cavity.py` on the **clean** mesh
*before* rig shape keys — not on the shredded progressive face.

## Component preservation

Eyes, lids, brows, nostrils, teeth, gums, tongue, sock remain **named protected
components**. On reset:

- Prefer **re-placing donors** onto clean head  
- Do not drag corrupted vertex groups from progressive `MARS_FACE` as authority  
- Fingerprint before/after any merge  

## Show canon (always)

MARS is a **floating head**. Pipeline priority:

```text
eyes → eyelids → brows → nostrils → mouth/oral → hair → expressions
```

Not full-body Rigify as the episode premise.

## Success criteria to move on

1. Reset base blend exists under `assets/variants/` with provenance  
2. GNM interior visible in **open-mouth** pixels + SHA  
3. Linework-aligned eye/lid placement measured  
4. No dependence on progressive seam-shredded mesh for daily work  
5. Owner accepts visual for EP01 floating-head closeups  

Then: hair, Episode 1 staging, Gaussian worlds — **not** another month of rim shards.
