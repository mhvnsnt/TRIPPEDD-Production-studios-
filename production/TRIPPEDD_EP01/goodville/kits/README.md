# Goodville Character Kits

Preston Blair-style animation kits for Goodville characters. Hand-built
(PIL, supersampled 2x) in the key-art South Park cutout language —
**never AI-generated**.

## Layout

`production/TRIPPEDD_EP01/goodville/kits/<character>/`
- `body.png` — torso + legs + shoes (no head/arms)
- `head.png` — head with permanent identity anchors (hair/hat/glasses);
  NO eyes or mouth (those are separate parts)
- `eyes_open.png`, `eyes_closed.png` — transparent, positioned
- `mouth_open.png`, `mouth_closed.png` — transparent, positioned
- `arm_L.png`, `arm_R.png` — transparent, positioned (no hands)
- `hand_L.png`, `hand_R.png` — mitten hands, transparent, positioned
- `prop.png` — signature prop (own canvas size)
- `preview.png` — full composite (draw order in manifest)
- `manifest.json` — anchors, draw order, identity checklist, palette
- `drill-log.md` — Tier B vs Tier A likeness drill (iterations, still-off)

All parts share one 600x900 canvas with positions baked in — alpha-composite
in `manifest.json → draw_order` for the full character.

`tpb-trio-promo.png` — Tier A promotional title image (the likeness target).

## The mobile home guys (owner 2026-10-11)

`dickie/` (54pc), `bubba/` (51pc), `julio/` (51pc) — individual Preston Blair
sheets for the real trio, built FROM the owner's ChatGPT trio image
(`1000173537_10_cm4h.png`, the junkyard trio). Names LOCKED: Dickie
(Ricky-based), Julio (Julian-based), Bubba (Bubbles-based). Likeness-critical
pieces extracted via smart-extract/rembg (hair shapes, facial hair, flame/wolf
graphic); dark clothing hand-built geometrically after rembg ate it;
face furniture + pose variants hand-built in SP style. Every piece eye-verified
against the source.
`build_kits.py` — the builder. Re-run to regenerate everything.

## KIT-SPEC backfill (pending)

The show-wide `kits/KIT-SPEC.md` (preston-blair-kits lane) had not landed when
these kits were built. Piece inventory here follows the original brief
(head/eyes/mouths/arms/hands/body/prop + manifest). When KIT-SPEC.md lands,
backfill any missing pieces (e.g. extra mouth shapes, clothing variants)
to match the spec.

## Characters (names TBD — owner assigns identity)

- `bubbles-based/` — lanky, big round glasses, buck teeth, messy hair under
  toque, kitty prop. Riffs the Bubbles archetype (parody).
- `ricky-based/` — slouch, greasy longer hair, striped shirt, goatee,
  cigarette prop. Riffs the Ricky archetype (parody).
- `julian-based/` — upright, tight black shirt, slicked-back hair, tumbler
  prop. Riffs the Julian archetype (parody).

Visual design only — no personalities, backstories, voices, or traits invented.
