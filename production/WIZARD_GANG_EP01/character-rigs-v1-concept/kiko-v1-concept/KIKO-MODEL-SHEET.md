# KIKO TANAKA — CHARACTER MODEL SHEET

**Show:** Wizard Gang
**Character:** Kiko Tanaka (based on Keiji Mutoh / The Great Muta)
**Date created:** 2026-10-10
**Version:** v1
**Status:** draft (worker-verified, owner approval pending)

> **Likeness law (from EP02_LIKENESS_BIBLE.md):** OLDER Keiji Mutoh / Great Muta ONLY.
> Young versions are REJECTED — never generate or use them.

---

## 1. TURNAROUND

| View | File | Status |
|------|------|--------|
| Front | `turnaround-front.png` | TODO |
| 3/4 | `turnaround-34.png` | TODO |
| Side | `turnaround-side.png` | TODO |
| Back | `turnaround-back.png` | TODO |

**Proportions:**
- Mature heavyweight wrestler build: broad shoulders, thick neck, heavy jaw
- Head: large, squared jaw, weathered lined face (unmasked) / segmented silver-black mask (masked, primary)
- Stance in reference cards: upright, squared-off, arms at sides, imposing

**Canonical versions (from likeness bible):**
1. Masked (primary): silver/black segmented mask, mature heavyweight build, white pants with black trim, black boots — the classic Muta look. → `kiko-masked.png`
2. Masked (alt): red/black horned demon mask, red tribal tattoos, black pants with red trim. → `kiko-masked-horned-alt.png`
3. Unmasked (older): older Mutoh, short dark hair, mature lined face, black singlet, black tights, boots. NO face paint. → `kiko-unmasked-older.png`

---

## 2. EXPRESSION SHEET

Covered by eye-expression cards (mask eye-hole glint style). See Section 4.
His emotion reads through the glowing glints in the mask's dark eye holes —
glint shape, angle, size, and intensity, same principle as Ashes' glint set.

---

## 3. MOUTH CHART (Preston Blair)

All 10 cards generated from ONE base head shot (`kiko-head-base.png`) via
mouth-region-only edits — pixel-aligned across the set. The mask covers the
upper face; the animated region is the visible mature lower face (jaw, lips,
chin) below the mask. Heavy gray-black stubble texture preserved on every card.

| Viseme | Sounds | Description for KIKO | File |
|--------|--------|---------------------|------|
| Rest | silence | Relaxed closed mouth, calm neutral line | `visemes/viseme-rest.png` |
| Ah | ah, eye, hat | Jaw dropped, open oval, upper+lower teeth and dark interior visible | `visemes/viseme-ah.png` |
| Ee | egg, eat, tree | Wide toothy grin, lips pulled tight, both rows bared | `visemes/viseme-ee.png` |
| Oh | oh, goat, hot | Rounded small oval ring, lips slightly pursed | `visemes/viseme-oh.png` |
| Oo | oo, you | Tight pucker pushed forward, tiny dark gap | `visemes/viseme-oo.png` |
| M/B/P | m, b, p | Lips pressed firmly in a flat line — NO teeth, NO gap. Non-negotiable | `visemes/viseme-mbp.png` |
| F/V | f, v | Upper front teeth resting on lower lip | `visemes/viseme-fv.png` |
| L | l, t, d, n, th | Slightly open, tongue tip up behind upper teeth | `visemes/viseme-l.png` |
| Hiss | s, k, g, z | Teeth pressed nearly together, tense hiss gap | `visemes/viseme-hiss.png` |
| TH | th | Tongue tip protruding between upper and lower teeth | `visemes/viseme-th.png` |

All in `~/workspace/character-rigs/kiko/visemes/`. Worker-verified (my own eyes on
every card): each viseme shows the correct mouth shape and everything else is
unchanged from the base.

**M/B/P is non-negotiable.** Every b, p, m sound in dialogue MUST use the closed
shape. The audience catches a missed lip-closure instantly.

---

## 4. EYE EXPRESSIONS

**Eye style:** Glowing pale-white glints inside the mask's dark eye holes. No
visible eyeballs — emotion conveyed through glint shape, angle, size, and
intensity (plus the classic sparkle cross-stars on the bright glints).

Base card (`eyes-neutral.png`) is a literal 2x-upscaled crop of the base head
shot's eye region — mask lines are pixel-identical across all 6 cards. The 5
expressions are edits that change ONLY the glints inside the eye holes.

| Expression | Description | File |
|------------|-------------|------|
| Neutral | Level symmetrical soft glints, calm resting gaze | `eyes/eyes-neutral.png` |
| Blink | Mid-blink: glints compressed to thin faint slits, nearly closed | `eyes/eyes-blink.png` |
| Happy | Warm upturned arcs, brighter golden glow | `eyes/eyes-happy.png` |
| Angry | Sharp blade slivers angled steeply inward-down, harsh glare | `eyes/eyes-angry.png` |
| Sad | Glints drooped downcast, dimmer weary glow | `eyes/eyes-sad.png` |
| Surprised | Large round bright ovals, hot bright core | `eyes/eyes-surprised.png` |

All in `~/workspace/character-rigs/kiko/eyes/`.

---

## 5. HAND POSES

**Finger count:** 5 digits (4 fingers + thumb) — verified by eye on every card
**Skin tone:** #D2A076 (lit, sampled from face; mid #BA8E6D, shadow #896441).
Never lighten past the lit value.

All 10 cards: mature heavyweight wrestler's hands — thick fingers, prominent
knuckles, short nails, weathered tan skin, small healed scars. No text or labels
on any card (the first relaxed base had annotation text and was regenerated
clean).

| Pose | Use for | File |
|------|---------|------|
| Open palm | Gesturing, presenting, stopping | `hands/hand-open-palm.png` |
| Fist | Emphasis, anger, impact stance | `hands/hand-fist.png` |
| Pointing | Directing attention, accusation | `hands/hand-pointing.png` |
| Gripping | Holding staff, handles, ledges | `hands/hand-gripping.png` |
| Thumbs up | Approval | `hands/hand-thumbs-up.png` |
| Relaxed | Idle, hanging at side | `hands/hand-relaxed.png` |
| Counting | Three fingers up — numbers, listing | `hands/hand-counting.png` |
| Beckoning | "Come here" — hooked index | `hands/hand-beckoning.png` |
| Holding | Thumb+index empty pinch (composite prop in post) | `hands/hand-holding.png` |
| Shaka | Hang-loose, casual greeting | `hands/hand-shaka.png` |

All in `~/workspace/character-rigs/kiko/hands/`. Mirror horizontally for the
left hand. Worker-verified: 5 fingers on every card, no extra/missing digits.

---

## 6. COLOR MODEL

Sampled numerically from `kiko-head-base.png` (percentile sampling, not eyeball).

| Area | Hex | Notes |
|------|-----|-------|
| Skin (lit) | #D2A076 | Weathered warm tan. NEVER lighten past this |
| Skin (mid) | #BA8E6D | |
| Skin (shadow) | #896441 | |
| Teeth | #EDE6D6 | Natural, no grill. He never has gold teeth — do NOT add |
| Mouth interior | #2A1A12 | Dark |
| Lips | #534236 | Natural dark, no gloss |
| Stubble | Dark gray-black texture | Heavy, NOT a flat color — preserve the texture |
| Hair (temples) | #3A3A3A | Short, dark with gray |
| Robe | #F0F0F0 | White |
| Fur trim | #F0F0F0 | White, thick |
| Mask silver | #C6C6C6 | Segmented panels |
| Mask silver shadow | #363536 | |
| Mask black | #09090B | Segments + flame patterns |
| Eye holes | #070707 | Near-black void |
| Eye glints | Pale white-yellow | Glow effect with sparkle stars |
| Pendant | #000000 | Small black pendant on cord |
| Background (cards) | #363636 | Neutral dark gray |

---

## 7. SCALE REFERENCE

| Compared to | Relative height | Notes |
|-------------|----------------|-------|
| Static | Taller / heavier | Kiko is one of the largest gang members |
| Ashes | Comparable | Both are the heavyweight presences |
| Door frame | Fills | Broad shoulders, upright squared stance |
| Average member | Taller | Mature heavyweight — he looms |

---

## 8. CHARACTER NOTES

- **OLDER Mutoh only.** The younger Muta look is BANNED — reject any generation
  that drifts young, smooth-skinned, or lean. He is a mature heavyweight with a
  lined, weathered face and heavy stubble.
- **Masked is the primary look** for EP02 generation: silver/black segmented
  mask, vertical ridge segments, flame patterns. The mask NEVER changes design
  between shots — drift hazard.
- **The mouth area is below the mask.** The mask ends above the upper lip; the
  animated mouth region is the visible lower face. Do not draw the mask over
  the mouth.
- **Unmasked reference exists** (older Mutoh, short dark hair, mature lined
  face) but **NEVER give him face paint when unmasked** — that is a banned
  drift. Painted Muta is a different era; Kiko in this show is the older,
  unpainted man OR the masked wrestler.
- **Stubble is texture, not noise.** Do not smooth it, blur it, or "clean" it —
  AI will try to make the skin smooth; that erases his age and is a likeness
  defect.
- **KIKO pendant** — small black pendant on a black cord. Present in the base
  head shot; keep it in future generations where visible.
- **White robe with fur trim** is the Wizard Gang outfit; white pants with black
  trim + black boots is the ring gear (per the cards). Both are white-dominant —
  keep fur trim on the robe look.

---

## 9. LIKENESS CHECKLIST

Before any asset enters the pipeline:

- [ ] Older Muta/Mutoh look — reject any young, smooth, or lean drift
- [ ] Mask design matches (silver/black segmented, ridge segments, flame patterns)
- [ ] Skin tone = #D2A076 (numeric check), never lightened
- [ ] Heavy stubble texture preserved — never smoothed
- [ ] Unmasked faces have NO face paint
- [ ] Teeth natural (#EDE6D6) — no gold teeth, no grill
- [ ] Style: thick black outlines, flat cel shading, no photorealism, no Disney 3D
- [ ] M/B/P viseme shows firm pressed closure
- [ ] Visually verified by human eyes, not just filename

---

*Companion: `KIKO-ANIMATION-GUIDE.md`. Template:
`~/workspace/animation-techniques/templates/character-model-sheet-template.md`.
Pattern source: `~/workspace/ashes-mouth-pack/`.*
