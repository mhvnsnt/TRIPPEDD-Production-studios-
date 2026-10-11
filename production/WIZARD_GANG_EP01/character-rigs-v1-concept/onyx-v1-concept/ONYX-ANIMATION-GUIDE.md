# ONYX ANIMATION GUIDE — Full Character Rig

**Character:** Onyx (Wizard Gang, green wizard)
**Date:** 2026-10-10
**Rule:** The clown paint is law. Capture it exactly as shown — never redesign it.

This is the complete animation rig for Onyx: 10 mouth visemes, 6 eye expressions, 8 hand poses. It follows the Ashes rig pattern (`~/workspace/ashes-mouth-pack/`).

---

## PART A — MOUTH

### 1. The Actual Design

**Her mouth is a LARGE BLACK PAINTED region — that IS the mouth.**

This is the single most important thing about animating Onyx. She does not have
normal lips that open and close. She has a fixed black painted smile, and speech
reads as openings appearing INSIDE that black region. The paint outline never
moves; only the interior opening changes shape per viseme.

### Key Features
- **Paint:** Full white clown face paint; near-black markings: teardrop/diamond shapes around both eyes, black-painted nose, LARGE black smile region, small black forehead mark. Identical in every card.
- **Mouth behavior:** Openings appear within the black smile region — tall oval (ah), wide grin (ee), round O (oh), tight O (oo), sealed shut (mbp), teeth-on-paint-edge (fv), tongue-up (l), teeth slit (s), tongue-out (th).
- **Teeth:** Natural white. NO grill — never add gold (that's Ashes, not her).
- **Tongue:** Pink, visible only in `l` and `th`.
- **Mouth interior:** Dark/near-black.
- **Card format:** All 10 viseme cards are 737×488 crops of the same mouth box — pixel-aligned. Composite over the mouth region of any front-facing shot.

### What NOT To Do
- Do NOT draw normal lips on her — the mouth lives inside the black paint
- Do NOT stretch, shrink, or move the black smile region between frames
- Do NOT let the teardrops, nose, or forehead mark drift — they are fixed
- Do NOT add a grill or gold teeth
- Do NOT paste a foreign mouth on top of the scene — work from the paint that's there

### 2. Reference
- `reference/onyx-base-face.png` — the single base portrait every card was edited from. Front-facing, neutral, mouth closed. This is the likeness anchor.

### 3. Viseme Set (10 — Full Preston Blair)

| Viseme | File | Preston Blair | Description |
|--------|------|---------------|-------------|
| Rest | viseme-rest.png | (default) | Closed black smile, relaxed, no opening |
| Ah | viseme-ah.png | A / I | Tall open oval, dark interior, white upper teeth at top |
| Ee | viseme-ee.png | E | Wide stretched grin, full white teeth top and bottom |
| Oh | viseme-oh.png | O | Round pursed O opening, small dark oval, no teeth |
| Oo | viseme-oo.png | U | Small tight pursed round opening, smaller than oh |
| M/B/P | viseme-mbp.png | M, B, P | Lips pressed firmly shut — closed black smile, NO opening. Non-negotiable |
| F/V | viseme-fv.png | F, V | White upper teeth on the lower edge of the black paint, narrow dark slit below |
| L | viseme-l.png | L, T, D, N | Small opening, pink tongue tip up behind upper teeth |
| S | viseme-s.png | S, Z | Narrow horizontal slit, teeth nearly touching, thin dark gap |
| Th | viseme-th.png | Th | Slightly open, pink tongue tip between the teeth |

**M/B/P is non-negotiable.** Every b, p, m sound in dialogue MUST use the sealed-shut shape. The audience catches a missed lip-closure instantly.

**Build note:** 9 of 10 visemes are direct edits of the single base portrait (the Ashes-v2 lesson — one base, edit only the mouth, everything stays pixel-aligned). `viseme-s` was drawn procedurally onto the approved mbp card with PIL after the image generator refused the hiss prompt — same paint, same alignment, verified by eye.

### The Core Principle (Owner's Law)

> "You're supposed to be making the mouths in the different expressions and the animations based off of what's there in the scene. Not adding something over the scene that's not there."

**Translation for Onyx:** The black painted smile is already in every shot of her. Animate the opening INSIDE that paint. Never draw a new mouth shape over her face.

---

## PART B — EYES

### Style: PAINTED-FRAME CARTOON EYES

Her eyes are cartoon eyes set inside the white clown face, framed by the locked black teardrop markings. Emotion comes from the eye shapes — the teardrops never change. This is NOT the Ashes glint style; do not reuse his cards.

### The 6 Expressions

| Expression | File | Description |
|------------|------|-------------|
| Neutral | eyes-neutral.png | Default open cartoon eyes, calm |
| Blink | eyes-blink.png | Fully closed, smooth lid curves with lash marks |
| Happy | eyes-happy.png | Upward-curving smiling crescents |
| Angry | eyes-angry.png | Narrowed, angled down toward center, glaring |
| Sad | eyes-sad.png | Drooping lids, downcast, outer corners low |
| Surprised | eyes-surprised.png | Wide open round eyes, raised brows |

All 6 are 898×547 crops of the same eye box — pixel-aligned. Composite over the eye region. The teardrop markings are identical in every card.

### Blink Rules (from the Animation Playbook)
- Blink every 3–5 seconds during dialogue
- **Always blink on head turns** — hides the transition
- Blink on stressed/emphasized words for punch
- Full blink = 2–3 frames at 30fps

---

## PART C — HANDS

### Finger Count: 5 digits (4 fingers + thumb)
Verified by eye on every card.

### Skin Tone: #986646, numerically verified
Sampled averages across all 8 cards: R 139–146, G 93–97, B 62–66 — all within 15 of the #986646 target (152, 102, 70), consistently at-or-darker. Never lightened. If a future card samples lighter than target, reject it.

### The 8 Poses

| Pose | File | Use for |
|------|------|---------|
| Open palm | hand-open-palm.png | Gesturing, presenting, stopping |
| Fist | hand-fist.png | Emphasis, anger |
| Pointing | hand-pointing.png | Directing attention |
| Gripping | hand-gripping.png | Holding handles/staffs (empty — composite prop in post) |
| Thumbs up | hand-thumbs-up.png | Approval, agreement |
| Relaxed | hand-relaxed.png | Idle, hanging at side (back of hand) |
| Counting | hand-counting.png | Holding up 3 fingers — numbers, listing |
| Beckoning | hand-beckoning.png | "Come here" — hooked index finger |

### How to Use
- Mirror horizontally for the left hand — do not generate separate left-hand cards
- Robed characters: most hand shots are covered by sleeves — only use when the hand is visible
- If the hand isn't doing something, hide it (pockets, behind back, in sleeves)

---

## RIG ASSEMBLY NOTES

**File layout** (`~/workspace/character-rigs/onyx/`):
```
visemes/viseme-{rest,ah,ee,oh,oo,mbp,fv,l,s,th}.png   (737×488, pixel-aligned)
eyes/eyes-{neutral,blink,happy,angry,sad,surprised}.png (898×547, pixel-aligned)
hands/hand-{open-palm,fist,pointing,gripping,thumbs-up,relaxed,counting,beckoning}.png
reference/onyx-base-face.png                          (rig source portrait)
ONYX-MODEL-SHEET.md
ONYX-ANIMATION-GUIDE.md  (this file)
```

**Compositing:** The viseme and eye cards are crops from the same base portrait at fixed boxes. To lip-sync a front-facing shot: align the card's paint markings to the shot's paint markings (they match by construction for the base framing), then swap cards per the dialogue cue sheet. For non-front angles, the cards are reference — redraw the opening in the shot's perspective, keeping the paint design locked.

**Likeness checklist (applies to every future Onyx asset):**
- [ ] Paint markings match the base portrait exactly
- [ ] Skin tone = #986646 (numeric check, not eyeball)
- [ ] Teeth natural white — no grill
- [ ] Full-figured build — no slimming
- [ ] Hair black, style consistent
- [ ] Style: thick black outlines, flat cel shading
- [ ] No whitewashing, no color drift
- [ ] Human eyes verified, not just filename

---

*Companion: `ONYX-MODEL-SHEET.md` (the law). Rig pattern: `~/workspace/ashes-mouth-pack/`. Technique layer: `~/workspace/animation-techniques/ANIMATION-PLAYBOOK.md`.*
