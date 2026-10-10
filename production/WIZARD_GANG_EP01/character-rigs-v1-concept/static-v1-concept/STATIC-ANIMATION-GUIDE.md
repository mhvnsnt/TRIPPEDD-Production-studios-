# STATIC ANIMATION GUIDE — Full Character Rig

**Character:** Static (Wizard Gang)
**Date:** 2026-10-10
**Rule:** Do NOT redesign him. Capture him exactly as shown.

This is the complete animation rig for Static: 10 mouth visemes, 6 eye expressions, 8 hand poses. It follows the Ashes rig template and the single-base pipeline law (all mouth/eye cards are edits of ONE base face).

---

## PART A — MOUTH

### 1. The Actual Design

**Static's teeth are NORMAL — that is his character, not a placeholder.**

Unlike Ashes (sharp teeth), Static has a regular bearded-man's mouth: plain white blocky teeth, natural lips, full dark beard framing the mouth. Do not give him sharp teeth, a grill, or fangs.

### Key Features
- **Tooth shape:** Normal, slightly blocky cartoon teeth. Upper and lower rows.
- **Mouth shape:** Sits in a small gap between mustache and beard. Compact — mouth cards are tight crops of this region.
- **Color:** Teeth natural white; lips natural skin-tone shaded; beard #000000 frames everything.
- **Skin:** Light (#FFCEA8, sampled). NEVER darken, NEVER lighten.
- **Hair:** Bleached blond (#FFF987) — visible at frame edges in all cards. NEVER darken.
- **Beard:** Dark and full (#000000) — never thinned, never faded. If a card's beard thins, reject the card.

### What NOT To Do
- Do NOT give him sharp/fang teeth (that's Ashes)
- Do NOT give him a gold grill (that's Ashes)
- Do NOT thin the beard to show more mouth — the compact bearded mouth IS the design
- Do NOT darken his hair
- Do NOT animate a mouth that wasn't there — work from the cards

### 2. Viseme Set (10 — Full Preston Blair)

All cards are edits of `static-base-face.png` — mouth only. Pixel-aligned by construction.

| Viseme | File | Preston Blair | Description |
|--------|------|---------------|-------------|
| Rest | viseme-rest.png | Rest / X | Relaxed neutral closed mouth, no teeth |
| Ah | viseme-ah.png | A / I | Jaw dropped wide oval, upper + lower teeth visible |
| Oh | viseme-oh.png | O | Rounded O opening, teeth visible top and bottom |
| Ee | viseme-ee.png | E | Wide grin, upper + lower teeth pressed together, bared |
| Oo | viseme-oo.png | U | Pursed forward, small round opening, teeth hidden |
| M/B/P | viseme-mbp.png | M, B, P | Lips pressed firmly shut, flat line — no teeth |
| F/V | viseme-fv.png | F, V | Upper teeth resting on lower lip |
| L | viseme-l.png | L, T, D, N, Th | Slightly open, tongue raised behind upper teeth |
| S (hiss) | viseme-s.png | S, Z | Teeth nearly closed in tight grin, thin gap |
| Th | viseme-th.png | Th | Tongue tip between upper and lower teeth |

**M/B/P is non-negotiable.** Every b, p, m sound in dialogue MUST use the closed shape. The audience catches a missed lip-closure instantly.

### The Core Principle (Owner's Law)

> "You're supposed to be making the mouths in the different expressions and the animations based off of what's there in the scene. Not adding something over the scene that's not there."

**Translation:** Animate the mouth that's already in the frame. The visemes exist for building talking animation FROM his actual mouth, not for overlaying a foreign mouth.

### Static-Specific Lip-Sync Notes
- His acting is LOUD and fast (Enzo Amore energy). Dialogue pacing runs hot — favor punchy 2-frame mouth swaps over long holds.
- **Ee is his signature sound.** His hype lines land on wide grins — lean on viseme-ee for emphasis beats.
- The beard keeps mouths small on screen: in wide shots, mouth motion reads through jaw/head bob more than lip detail. In close-ups, the viseme cards carry it.
- Always composite over the base face — the cards share its exact geometry.

---

## PART B — EYES

### Style Decision: VISIBLE CARTOON EYES

Static has a normal visible face — brown irises, white sclera, thick black cartoon brows. He is NOT shrouded (no void face, no glints — that's Ashes' look). Emotion is carried by brow angle, lid shape, and openness. All 6 cards are base-face edits; eye position is identical across cards for compositing.

### The 6 Expressions

| Expression | File | Eye description |
|------------|------|-----------------|
| Neutral | eyes-neutral.png | Open brown eyes, relaxed lids, straight gaze — default acting state |
| Blink | eyes-blink.png | Mid-blink: closed lids, curved lid lines with lash strokes |
| Happy | eyes-happy.png | Joyful upturned arcs, crinkled outer corners — his hype face |
| Angry | eyes-angry.png | Brows angled steeply inward-down, narrowed intense glare |
| Sad | eyes-sad.png | Brows raised inner/drooping, downcast weary eyes |
| Surprised | eyes-surprised.png | Large wide-open round eyes, small pupils, brows high |

### Blink Rules (from the Animation Playbook)
- Blink every 3–5 seconds during dialogue
- **Always blink on head turns** — hides the transition
- Blink on stressed/emphasized words for punch
- Full blink = 2–3 frames at 30fps

### Static-Specific Acting Notes
- **Default to happy/neutral.** He is the loud hype man of the gang — resting grumpy is off-character. Angry is for genuine conflict beats only.
- Surprised pairs with oo/ah mouths for his classic "WAIT WHAT" double-take.
- Happy eyes + ee mouth = his victory face. Use it.

---

## PART C — HANDS

### Finger Count: 5 digits (4 fingers + thumb)
All cards verified clean: correct anatomy, no extras, no merged digits.

### Skin Tone: light, numerically verified
Sampled from base face: **#FFCEA8**. All cards match. Never darken, never lighten.

### The 8 Poses

| Pose | File | Use for |
|------|------|---------|
| Open palm | hand-open-palm.png | Gesturing, presenting, stopping — his "listen to me" hand |
| Fist | hand-fist.png | Emphasis, anger, hype mic-drop moments |
| Pointing | hand-pointing.png | Directing attention, accusation, calling people out |
| Gripping | hand-gripping.png | Holding staff, mic, handles |
| Thumbs up | hand-thumbs-up.png | Approval, agreement |
| Relaxed | hand-relaxed.png | Idle, hanging at side |
| Counting | hand-counting.png | Holding up 3 fingers — numbers, listing |
| Beckoning | hand-beckoning.png | "Come here" — hooked index |

### How to Use
- Mirror horizontally for the left hand — do not generate separate left-hand cards
- Cards are CLEAN assets: hand only, white background, NO baked-in text or borders (the first pass had label headers baked in and was regenerated)
- Static talks with his hands. Pointing + beckoning + open-palm are his gestural vocabulary — pair them with ee/ah mouths on punchlines
- If the hand isn't doing something, hide it (robe sleeves, behind back)
- White background keys out cleanly for compositing

---

## RIG ASSEMBLY NOTES

1. **Base face is the anchor:** `static-base-face.png` — every viseme and eye card is an edit of this exact image. Composite cards over it at 100% scale, same position: they are pixel-aligned.
2. **Generation rule for new cards:** If a new expression is ever needed, generate it as an EDIT of `static-base-face.png` with only the target feature changed — never a fresh generation. (The Ashes v2 failure.)
3. **Hand compositing:** hands are standalone assets on white; key out the white, scale to scene, mirror for left.
4. **Voice/emotion mapping:** Static's dialogue runs loud and fast. Scene-specific BGM per the owner's 2026-10-10 audio direction applies at final mix; dialogue is placed first, music mixed around it.

## LIKENESS CHECKLIST (all cards — verified this build)

- [x] Skin tone = #FFCEA8 (numeric)
- [x] Hair bleached blond #FFF987, messy medium — never darkened (all 16 face cards)
- [x] Beard dark #000000 and full — never thinned (all 16 face cards)
- [x] Teeth normal, not sharp, no grill (all 10 visemes)
- [x] Robe deep blue #111B5A, pendant reads STATIC (base face)
- [x] Style: thick black outlines, flat cel shading
- [x] All 24 cards visually verified by human eyes, not just filename

---

*Companion: `STATIC-MODEL-SHEET.md` (model sheet). Template lineage: `~/workspace/ashes-mouth-pack/ASHES-ANIMATION-GUIDE.md`. Technique layer: `~/workspace/animation-techniques/ANIMATION-PLAYBOOK.md`.*
