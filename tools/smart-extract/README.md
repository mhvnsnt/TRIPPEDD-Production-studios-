# Smart Extraction Pipeline — "sense → loop → trace → cut → verify"

**Location:** `tools/smart-extract/` (TRIPPEDD-Production-studios-)
**Status:** THE standard for character extraction on ALL shows and repos.
**Law:** SMART-WAY LAW (owner 2026-10-11) — flood-fill masking, eyeballed crops,
blurred-edge cutouts, and "good enough" extractions are BANNED.

## Why this exists

The Goodville promo's likeness pass regressed because the character parts were
garbage going in — dumb flood-fill masking produced blurred edges, bad crops, and
stray chunks (the brown hair artifact that floated next to Amos Jr.'s head).
Bad inputs, bad outputs. This pipeline replaces the dumb method with a smart one.

## The pipeline

```
INPUT  →  SENSE  →  TRACE + CUT  →  VERIFY (loop)  →  POSITION
```

### 1. INPUT
Key art image + character name + requested parts.

### 2. SENSE (vision pass)
Use `muse.visual_grounding` (bbox mode) to locate each part in the key art.
Output: bounding boxes in 0-1000 normalized coordinates → converted to pixels
in the parts spec JSON. **Never eyeball a crop.**

### 3. TRACE + CUT (rembg, never flood-fill)
`extract.py` crops to the spec bbox (with padding) and runs **rembg**:
- **Model ladder:** `isnet-anime` (cartoon-domain specialist) → `isnet-general-use`
  → the VERIFY loop picks the winner per part. Different parts need different
  models — the ladder handles it automatically.
- **Alpha cleanup:** removes small disconnected specks (detached chunks).
- **Context matters:** full-body crops beat tight crops — the model needs to see
  what it's cutting. White-on-light (tank top on pale background) is the known
  hard case; the ladder + color check handles it.

### 4. VERIFY (the loop — mandatory, not optional)
Automated checks per part:
- `non_empty` — did anything extract?
- `components` / `detached_chunks` — connected-component analysis catches stray chunks
- `fringe_ratio` — semi-transparent edge band (flags blurred/halo edges)
- `color_dist` / `color_flag` — mean-RGB distance from source crop (catches
  inversions and wrong-subject picks, e.g. black torso where the tank is white)

Then **read every output PNG with your own eyes**. Automated checks catch specks;
eyes catch likeness. If anything's off, adjust (model, crop, padding) and re-run.
The loop runs until clean.

### 5. POSITION from measurement
Part placement derived from key-art coordinates/anchors in the manifest.
Never eyeballed.

## Usage

```bash
# 1. SENSE: get bboxes via visual grounding, write parts_spec.json
# 2. CUT:
python3 tools/smart-extract/extract.py \
  --image assets/references/ep01/source/key_art.png \
  --spec my_parts_spec.json \
  --character amos_jr \
  --outdir /tmp/extract_out

# 3. VERIFY: read every PNG in /tmp/extract_out/<character>/
# 4. Manifest at /tmp/extract_out/<character>/manifest.json has anchors
```

Spec format — see `proving_run_spec.json`. Bboxes in pixels.

## Proving run (2026-10-11)

Re-extracted Amos Jr. + old head from the Goodville key art.

| Part | Before (flood-fill) | After (smart pipeline) |
|------|---------------------|------------------------|
| Amos head | blurred fringe, bad crop | clean edges, 1 component, all anchors |
| Amos full body | n/a (never extracted) | shaggy hair, goatee, white tank, tattoo, BEER can — all correct |
| Old head head | ghostly/simplified geometry | bald, side hair, aviators, cigarette — from key art |
| Old head body | black trapezoid placeholder | key-art jacket, collar/zipper/pocket |

**Before/after on the critical case:** the old pipeline's `armL.png` was 94%
brown hair pixels (bad extraction → floating chunk artifact in the promo).
The smart pipeline's full-body extraction has the correct white tank, the real
hair on the head where it belongs, and zero detached chunks.

## What couldn't be automated

- **SENSE bboxes** still need the agent's visual-grounding pass — no fully
  automatic part detector exists in the free stack. The spec format makes the
  handoff clean.
- **Eye verification** is mandatory and human (or agent-eyes). The automated
  checks catch technical defects; only eyes catch likeness drift.
- **White-on-light** remains the hardest case — the ladder usually solves it,
  but review these outputs extra carefully.
- **Fringe metric** is conservative (flags feathered model edges). When it
  flags but eyes say clean, trust eyes and note it.
