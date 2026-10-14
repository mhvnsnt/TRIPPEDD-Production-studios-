# Goodville clean cutouts (mask-cut, not rectangle crops)

Owner complaint (2026-10-14): pieces were "ugly rectangular cut-outs" — background chunks,
grey smears, ghost faces and neighbour characters baked into stickers, arms and heads.

What this folder is: an **additive** mask-cut copy of every character piece in
`kits/amos-jr`, `kits/old-head`, `kits/scene-pieces`, `promo-15s/assets`, `scenes/dino-punch`
and `tools/smart-extract/proving_run`. Originals are untouched (nothing deleted).
Paths mirror the repo, e.g. `clean-cutouts/production/TRIPPEDD_EP01/goodville/kits/amos-jr/head_34R.png`.

Method (`maskcut.py`): rembg **u2net** subject mask on a white-padded upscale → intersected with
the existing alpha → ghost/smear kill (semi-transparent residue < ~45% opacity dropped) →
crumb removal (fragments < 4% of the main body dropped) → 1px edge erode + 0.6px feather.
Background plates (sky, street, buildings, finished frames) are intentionally NOT mask-cut.

Proof: `PROOF-before-after-1.png`, `PROOF-before-after-2.png` (left = original, right = cut, on a checkerboard).
Per-piece numbers: `maskcut-report.json` (border opacity before/after, area kept, status).

## Still needs a human/editor pass (flagged honestly)
| Piece | Problem | Use instead |
|---|---|---|
| `proving_run/oldhead_body.png`, `kits/old-head/body_*.png` | the SOURCE is a translucent ghost image (grey smear + a green neighbour). Cutting can't invent clean pixels. | `proving_run/oldhead_head.png` (clean) until the body is redrawn from the key art |
| `promo-15s/assets/amosjr_body.png` | source mostly white-on-white; mask eats the tank top | `kits/amos-jr/body_full.png` (clean) |
| `kits/scene-pieces/amos_punch_arm.png` | the piece itself contains a chunk of torso (wrong content, not a bg problem) | `kits/amos-jr/arm_punch.png` (clean, fist + can) |
| Amos torsos `torso_*` | ghost double-eyes baked into the face | patch the head from `body_full.png` (done in the segment's timeline) |
| a few eyes/mouths marked `REVIEW_kept_original` | tiny line-art pieces the model can't see; originals were already clean | originals |
