# ONYX — CHARACTER MODEL SHEET

**Show:** Wizard Gang
**Character:** Onyx (green wizard)
**Date created:** 2026-10-10
**Version:** v1
**Status:** approved

> **The clown face paint is the single source of truth.** White face paint with
> locked black markings — identical in every reference. Never redraw it, never
> "improve" it, never let it drift between cards. Skin is #986646 — never lighten.

---

## 1. TURNAROUND

| View | File | Status |
|------|------|--------|
| Front | `turnaround-front.png` | TODO |
| 3/4 | `turnaround-34.png` | TODO |
| Side | `turnaround-side.png` | TODO |
| Back | `turnaround-back.png` | TODO |

**Proportions:**
- Full-figured build — NEVER slim her down. The generator will try; reject it.
- Head: white clown face paint, long wavy black hair framing the face
- Neck: layered black chokers/necklaces (choker + 3 beaded strands in the base portrait)
- Shoulders: green robe with diamond-shaped black/gold ONYX pendant at the collar

**Base portrait (rig source):** `reference/onyx-base-face.png` — front-facing
head-and-shoulders, neutral expression, mouth closed. ALL viseme and eye cards
were generated as edits of this single image, then cropped to fixed boxes.

---

## 2. EXPRESSION SHEET

Covered by the eye-expression cards (Section 4). The clown paint never changes
with expression — only the eyes and the mouth opening move.

---

## 3. MOUTH CHART (Preston Blair)

**Design rule:** Her mouth is a LARGE BLACK PAINTED region. The visemes read as
mouth movements WITHIN the black paint — the paint markings stay fixed, only
the interior opening changes shape. Never draw normal lips.

| Viseme | Sounds | Description for ONYX | File |
|--------|--------|---------------------|------|
| Rest | silence | Closed black smile, relaxed, no opening | `visemes/viseme-rest.png` |
| Ah | ah, eye, hat | Tall open oval inside the paint, dark interior, white upper teeth at top | `visemes/viseme-ah.png` |
| Ee | egg, eat, tree | Wide stretched grin, full white teeth top and bottom | `visemes/viseme-ee.png` |
| Oh | oh, goat, hot | Round pursed O opening, small dark oval, no teeth | `visemes/viseme-oh.png` |
| Oo | oo, you | Small tight pursed round opening, smaller than oh, no teeth | `visemes/viseme-oo.png` |
| M/B/P | m, b, p | Lips pressed firmly shut — closed black smile, NO opening, NO teeth. Non-negotiable | `visemes/viseme-mbp.png` |
| F/V | f, v | White upper teeth resting on the lower edge of the black paint, narrow dark slit below | `visemes/viseme-fv.png` |
| L | l, t, d, n | Small opening, pink tongue tip up behind the white upper teeth | `visemes/viseme-l.png` |
| S (hiss) | s, z | Narrow horizontal slit, white upper+lower teeth nearly touching, thin dark gap | `visemes/viseme-s.png` |
| Th | th | Slightly open, pink tongue tip poking out between upper and lower teeth | `visemes/viseme-th.png` |

**Build method (the Ashes v2 lesson):** 9 of 10 visemes are direct image-edits of
the ONE base portrait — same pixels everywhere except the mouth interior. All
cards are cropped to the identical mouth box (737×488 at base coords
(430,630)–(1167,1118)), so they are pixel-aligned for lip-sync compositing.
`viseme-s` was drawn procedurally (PIL) onto the mbp card after the image tool
refused the hiss generation — verified by eye, reads cleanly as a cartoon hiss.

**Teeth:** natural white. Onyx has NO grill (unlike Ashes) — never add gold teeth.

---

## 4. EYE EXPRESSIONS

**Eye style:** Cartoon eyes set inside the white clown face, framed by the locked
black teardrop markings. The teardrops NEVER change — only the eye shapes move.

| Expression | Description | File |
|------------|-------------|------|
| Neutral | Default open cartoon eyes, calm | `eyes/eyes-neutral.png` |
| Blink | Eyes fully closed, smooth lid curves with lash marks | `eyes/eyes-blink.png` |
| Happy | Upward-curving smiling crescent eyes | `eyes/eyes-happy.png` |
| Angry | Narrowed eyes angled down toward center, glaring | `eyes/eyes-angry.png` |
| Sad | Drooping lids, downcast, outer corners low | `eyes/eyes-sad.png` |
| Surprised | Wide open round eyes, raised brows | `eyes/eyes-surprised.png` |

All in `~/workspace/character-rigs/onyx/eyes/`. All are edits of the single base
portrait, cropped to the identical eye box (898×547 at base coords
(350,300)–(1248,847)) — pixel-aligned.

---

## 5. HAND POSES

**Finger count:** 5 digits (4 fingers + thumb) — verified on every card by eye
**Skin tone:** #986646 — numerically verified on all 8 cards (sampled averages
139–146 / 93–97 / 62–66 — all within 15 of target, consistently at-or-darker.
Never lightened.)

| Pose | Use for | File |
|------|---------|------|
| Open palm | Gesturing, presenting | `hands/hand-open-palm.png` |
| Fist | Emphasis, anger | `hands/hand-fist.png` |
| Pointing | Directing attention | `hands/hand-pointing.png` |
| Gripping | Holding handles, staffs (empty — composite prop in post) | `hands/hand-gripping.png` |
| Thumbs up | Approval | `hands/hand-thumbs-up.png` |
| Relaxed | Idle, hanging at side (back of hand) | `hands/hand-relaxed.png` |
| Counting | Holding up 3 fingers — numbers, listing | `hands/hand-counting.png` |
| Beckoning | "Come here" — hooked index finger | `hands/hand-beckoning.png` |

All in `~/workspace/character-rigs/onyx/hands/`. Flat 2D cartoon, thick black
outlines, cel shading, white background, wrist cut clean. Mirror horizontally
for the left hand — do not generate separate left-hand cards.

---

## 6. COLOR MODEL

| Area | Hex | Notes |
|------|-----|-------|
| Skin | #986646 | Medium brown. NEVER lighten. Numerically verified on all hand cards. |
| Clown face paint | #FFFFFF | Full-face white paint — this is PAINT, not skin |
| Paint markings | #0A0A0A | Near-black: eye teardrops, nose, smile region, forehead mark |
| Teeth | #F2F2F2 | Natural white. NO grill — never add gold |
| Tongue | pink | Visible only in l/th visemes |
| Mouth interior | dark | Near-black opening inside the paint |
| Hair | #1A1A1A | Near-black, long and wavy |
| Chokers/necklaces | #0A0A0A | Black — layered choker + beaded strands |
| Robe primary | green | Wizard robe |
| ONYX pendant | black/gold diamond | At the robe collar |

---

## 7. SCALE REFERENCE

| Compared to | Relative height | Notes |
|-------------|----------------|-------|
| Ashes | Shorter | Onyx is mid-size; Ashes is one of the larger members |
| Group | Fill in from group photo | TODO: measure |

---

## 8. CHARACTER NOTES

- **The paint is the character.** White clown face + black teardrops + black nose + large black smile + forehead mark. If any marking shifts, moves, or disappears between cards, the card is wrong.
- **The smile region is FIXED.** Visemes change only the interior opening. The black painted smile outline never stretches, shrinks, or moves.
- **No grill.** Her teeth are natural white. The gold-teeth rule is Ashes-only.
- **Full-figured, always.** Reject any generation that slims her.
- **Hair stays black.** No color swapping.
- **Skin #986646 on every visible skin pixel** — hands, neck, arms. The face is paint; everything else is #986646. Check numerically, not by eye.
- **mbp note:** the mbp card carries a subtle seam line through the black paint from the generator — it reads as the pressed-lip seal line and is acceptable. Do not "clean" it into a different mouth shape.
- **viseme-s note:** drawn procedurally (PIL) after the image tool refused the hiss prompt. It is a rig asset built from the approved mbp card, not a new face — same paint, same alignment.

---

## 9. LIKENESS CHECKLIST

Before any asset enters the pipeline:

- [ ] Paint markings match the base portrait exactly (teardrops, nose, smile, forehead mark)
- [ ] Skin tone = #986646 (numeric check on hands/arms/neck)
- [ ] Teeth are natural white — no grill, no gold
- [ ] Build is full-figured — no slimming
- [ ] Hair is black
- [ ] Style: thick black outlines, flat cel shading, Shadow Wizard Money Gang base
- [ ] No whitewashing, no color drift
- [ ] Visually verified by human eyes, not just filename

---

*Companion: `ONYX-ANIMATION-GUIDE.md` (full rig documentation). Template: `~/workspace/animation-techniques/templates/character-model-sheet-template.md`. Rig pattern: `~/workspace/ashes-mouth-pack/`.*
