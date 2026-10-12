# Owner Mask Workflow (owner 2026-10-11)

When the assistant's auto-cut is wrong, the owner hand-edits a mask and shares it.

## How it works
1. Assistant generates a mask PNG (white = keep/fill, black = skip)
2. Owner edits the mask in any image editor, sends it back
3. Assistant runs: `python3 mask_pipeline.py <character.png> <owner_mask.png> <tile.png> <output.png>`
4. For pure cutouts (no pattern): `python3 mask_pipeline.py <character.png> <owner_mask.png> --cutout <output.png>`

## Convention
- White pixels = apply pattern / keep
- Black pixels = skip / transparent
- Owner masks are saved in the character's kit as `<piece>_mask_owner.png`

## History
- 2026-10-11: Julio's palm shirt — owner hand-drew two mask versions, both applied via this pipeline.
