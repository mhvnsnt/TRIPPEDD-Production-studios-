# SOMBRA NEGRA ANIMATION GUIDE — Full Character Rig

**Character:** Sombra Negra (Wizard Gang)
**Date:** 2026-10-10
**Rule:** Do NOT redesign him. Capture him exactly as shown.
**Voice:** Speaks as Damian Priest — deep, commanding. Voice drives the acting.

This is the complete animation rig for Sombra Negra: 10 mouth visemes, 6 eye expressions, 10 hand poses, following the Ashes rig pattern.

---

## PART A — MOVEMENT: IMPOSING, DELIBERATE

Sombra Negra is the gang's looming threat. Every move reads as slow, heavy, and intentional.

- **Walks:** slow, wide, heel-first. Weight sinks into each step — no bouncing, no bounce-step, no bounce.
- **Turns:** whole-body turns, head last. Head turns get a blink to hide the transition.
- **Gestures:** big and slow — open-palm presents, finger-point accusations, fist slams for emphasis. Small quick gestures are wrong for him.
- **Idle:** nearly still. Breath cycle only — chest rise, tassel sway. Stillness IS his energy.
- **Presence rule:** when he enters, the frame gives him room. He does not share screen space like a side character.
- **Timing:** holds are long. Let reactions land. He never fidgets.

### Tassel Secondary Motion (LOOSE TASSELS — intentional, never removed)

- The thigh tassels have their OWN motion layer. They lag 4–6 frames behind the body.
- On a turn: tassels whip then settle over ~10 frames.
- On a step: tassels swing forward then back, pendulum.
- Idle: slow sway on the breath cycle.
- **Never:** rigid tassels, tassels glued to the legs, or tassels deleted as "artifacts." They are individual rigged parts (per EP02_LIKENESS_BIBLE §8).

---

## PART B — MOUTH / VOICE BEHAVIOR

### The Design
- White face-paint mask, painted-white lips (no pink/red lips). White natural teeth — NOT gold (that's Ashes).
- Mouth sits centered in the mask below the red eyes. Viseme cards are pixel-aligned from one base head.

### Viseme Set (10 — Preston Blair, single base image)

| Viseme | File | Behavior |
|--------|------|----------|
| Rest | viseme-rest.png | Default hold. Lips shut, calm thin line. |
| Ah | viseme-ah.png | Tall oval. Jaw drops — jaw drops FURTHER for him than for most characters (his delivery is big). |
| Ee | viseme-ee.png | Wide, teeth together. |
| Oh | viseme-oh.png | Round O. |
| Oo | viseme-oo.png | Small pursed circle. |
| M/B/P | viseme-mbp.png | Pressed shut, flat line. NON-NEGOTIABLE on m/b/p. |
| F/V | viseme-fv.png | Upper teeth on lower lip. |
| L | viseme-l.png | Tongue up behind upper teeth. |
| Hiss | viseme-hiss.png | Teeth nearly closed. |
| Th | viseme-th.png | Tongue tip out between teeth. |

### Voice-Driven Acting (Damian Priest — deep, commanding)
- He speaks SLOW. Fewer viseme swaps per second than fast talkers. Let the shapes HOLD — 3–4 frames each at minimum.
- Jaw opens wide on emphasized words ("ah" shapes get extra height).
- Pause = closed rest shape. He punctuates sentences with full lip closure, not mouth hang.
- **Never animate through rest** — hold rest on silences, cut to the next shape on attack.
- His menace lives in the STILL mouth between words. Don't keep the mouth moving on pauses.

---

## PART C — EYES: RED EYES SELL THE ACTING

Red eyes are his instrument. The mask hides the brows — the eyes do the work.

| Expression | File | Use |
|------------|------|-----|
| Neutral | eyes-neutral.png | Default. Level red eyes, calm glow. |
| Blink | eyes-blink.png | Every 3–5 seconds during dialogue. ALWAYS blink on head turns. 2–3 frames at 30fps. Blink on stressed words for punch. |
| Happy | eyes-happy.png | Rare. Upturned warm red arcs. Use sparingly — his "happy" still reads menacing. |
| Angry | eyes-angry.png | Sharp inward-down red blades. The threat default when he leans in. |
| Sad | eyes-sad.png | Drooped, dimmed. Rare — use for weary beats only. |
| Surprised | eyes-surprised.png | Large round red ovals. Maximum openness — used at real shocks only. |

- **Eye glow intensity:** brightness scales with emotion. Angry = harsh hot glare. Surprised = hot core. Sad = dim.
- **Never:** eyes turning brown or normal, pupils appearing, white sclera showing.
- Composite eye cards over the red-eye region of the mask. Position is consistent across all 6 cards.

---

## PART D — HANDS

- **Skin tone:** #8E6650, warm medium brown. Never lighten. Black-and-white patterned wristbands on every card.
- **5 digits** on every card, verified.
- Mirror horizontally for the left hand — do not generate separate left-hand cards.
- **hand-holding.png** and **hand-gripping.png** are EMPTY (no prop) — composite the prop into the grip in post.
- Robe sleeves cover the wrists in most shots — only swap hand cards in when the hand is actually visible.
- If the hand isn't doing something, hide it (in sleeves, behind back). Sombra does not fidget.

---

## PART E — WHAT NOT TO DO

1. **Never normalize the red eyes.** Brown/normal eyes = failed asset.
2. **Never delete or "fix" the tassels.** They are rigged loose parts of the outfit.
3. **Never whitewash.** Skin #8E6650 on hands/arms. If a generation lightens it, reject.
4. **Never put pink/red lips on him.** Lips are painted white like the mask.
5. **Never gold-teeth him.** White natural teeth. Gold is Ashes.
6. **Never "SWMG" text.** Pendant is a SKULL.
7. **Never fast-talk his delivery.** Slow, commanding, holds between words.
8. **Never mix the void-face robe variant and the mask head in one scene** without flagging it — the bible documents both.
9. **Never add baked-in text, labels, banners, or captions to cards.** Clean art only (see 2026-10-10 Theory worker incident).
10. **No photorealism, no Disney 3D, no AI slop.** Thick black outlines, flat cel shading, cartoony — per the locked art style.

---

*Companion: `SOMBRA-NEGRA-MODEL-SHEET.md`. Pattern: `~/workspace/ashes-mouth-pack/ASHES-ANIMATION-GUIDE.md`.*
