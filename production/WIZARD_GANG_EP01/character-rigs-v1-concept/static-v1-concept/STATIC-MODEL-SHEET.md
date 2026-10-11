# STATIC — CHARACTER MODEL SHEET

**Show:** Wizard Gang
**Character:** Static
**Date created:** 2026-10-10
**Version:** v1
**Status:** draft (awaiting owner review)

> **Owner's law:** Do NOT redesign him. Capture him exactly as shown.
> His teeth are NORMAL (not sharp like Ashes). His beard stays DARK and FULL — never thin it, never darken his hair.

---

## 1. TURNAROUND

| View | Description | File |
|------|-------------|------|
| Front | Facing camera, arms at sides | `turnaround-front.png` (TODO) |
| 3/4 | Three-quarter turn, facing slightly right | `turnaround-34.png` (TODO) |
| Side | Full profile, facing right | `turnaround-side.png` (TODO) |
| Back | Facing away | `turnaround-back.png` (TODO) |

**Proportions:**
- Height: muscular build, broad chest and shoulders
- Unrobed form: tattooed torso and arms (see GLB / card refs)
- Robed form: deep blue robe with STATIC pendant; base face card shows head/shoulders

**Face anchor:** `static-base-face.png` — the single master likeness. All viseme and eye cards are pixel-edited derivatives of this image (see §8).

---

## 2. EXPRESSION SHEET

Covered by eye-expression cards (visible cartoon eyes). See Section 4.

---

## 3. MOUTH CHART (Preston Blair)

All generated from ONE base image (`static-base-face.png`); only the mouth was changed per card. Fully pixel-aligned.

| Viseme | Sounds | Description for STATIC | File |
|--------|--------|----------------------|------|
| Rest | silence | Relaxed neutral closed mouth, no teeth visible | `visemes/viseme-rest.png` |
| Ah | ah, eye, hat | Jaw dropped wide oval, normal upper + lower teeth visible | `visemes/viseme-ah.png` |
| Ee | egg, eat, tree | Wide grin, upper and lower teeth pressed together, bared | `visemes/viseme-ee.png` |
| Oh | oh, goat, hot | Rounded O opening, normal teeth visible top and bottom | `visemes/viseme-oh.png` |
| Oo | oo, you | Pursed, small round forward lips, teeth hidden | `visemes/viseme-oo.png` |
| M/B/P | m, b, p | Lips pressed firmly shut, flat line — no teeth. Non-negotiable. | `visemes/viseme-mbp.png` |
| F/V | f, v | Upper row of normal teeth resting on lower lip | `visemes/viseme-fv.png` |
| L | l, t, d, n, th | Slightly open, tongue raised up behind upper teeth | `visemes/viseme-l.png` |
| S (hiss) | s, k, g, z | Teeth nearly closed in a tight grin, thin gap | `visemes/viseme-s.png` |
| Th | th | Tongue tip poking between upper and lower teeth | `visemes/viseme-th.png` |

All in `~/workspace/character-rigs/static/visemes/`.

---

## 4. EYE EXPRESSIONS

**Eye style:** Visible cartoon eyes (he has a normal visible face — NOT shrouded). Brown irises, thick black cartoon brows. Emotion is carried by brow angle, lid shape, and eye openness.

| Expression | Description | File |
|------------|-------------|------|
| Neutral | Open brown eyes, relaxed lids, straight neutral gaze | `eyes/eyes-neutral.png` |
| Blink | Mid-blink: closed lids, simple curved lid lines with lash strokes | `eyes/eyes-blink.png` |
| Happy | Joyful upturned arcs, crinkled at outer corners, warm | `eyes/eyes-happy.png` |
| Angry | Thick brows angled steeply inward-down, narrowed intense glare | `eyes/eyes-angry.png` |
| Sad | Brows raised at inner corners and drooping, downcast weary eyes | `eyes/eyes-sad.png` |
| Surprised | Large wide-open round eyes, small pupils, brows raised high | `eyes/eyes-surprised.png` |

All in `~/workspace/character-rigs/static/eyes/`. All are base-face derivatives — identical eye position for compositing.

---

## 5. HAND POSES

**Finger count:** 5 digits (4 fingers + thumb)
**Skin tone:** #FFCEA8 (sampled from base face, numeric — not eyeballed)
**Card format:** Clean — no baked-in text/labels/borders. Hand only on white.

| Pose | Use for | File |
|------|---------|------|
| Open palm | Gesturing, presenting, stopping | `hands/hand-open-palm.png` |
| Fist | Emphasis, anger, Enzo-style mic-drop moments | `hands/hand-fist.png` |
| Pointing | Directing attention, accusation | `hands/hand-pointing.png` |
| Gripping | Holding staff, mic, handles | `hands/hand-gripping.png` |
| Thumbs up | Approval, agreement | `hands/hand-thumbs-up.png` |
| Relaxed | Idle, hanging at side | `hands/hand-relaxed.png` |
| Counting | Numbers, listing (3 fingers up) | `hands/hand-counting.png` |
| Beckoning | "Come here" — hooked index | `hands/hand-beckoning.png` |

All in `~/workspace/character-rigs/static/hands/`. Mirror horizontally for left hand.

---

## 6. COLOR MODEL

| Area | Hex | Notes |
|------|-----|-------|
| Skin | #FFCEA8 | Light. Sampled numerically from `static-base-face.png`. Never darken or lighten. |
| Hair | #FFF987 | BLEACHED-BLOND. Never darken. Messy medium-length. |
| Beard | #000000 | Dark, FULL. Never thin, never fade. |
| Teeth | #FFFFFF-ish (natural) | NORMAL teeth — not sharp, no grill. |
| Tongue | standard cartoon pink | |
| Lips | natural skin-tone shaded | No lipstick, no metallic |
| Robe primary | #111B5A | DEEP BLUE |
| Pendant | gold (#D4AF37) | Reads "STATIC" (canon-locked text) |
| Eyes (iris) | brown | White sclera |

---

## 7. SCALE REFERENCE

| Compared to | Relative height | Notes |
|-------------|----------------|-------|
| Ashes | Shorter | Ashes is one of the larger gang members |
| Group | Fill in from group photo | TODO: measure |

---

## 8. CHARACTER NOTES

- **Single-base pipeline (the Ashes v2 lesson):** ALL 10 visemes and all 6 eye cards were generated as image edits of ONE base face (`static-base-face.png`) with only the target feature changed. This guarantees pixel alignment across the whole rig. Never regenerate individual cards from scratch.
- **Normal teeth are the design.** Static does NOT have sharp teeth — that's Ashes. Do not "fix" him with a grill or fangs.
- **Beard rule:** DARK and FULL in every card. Drift hazards: beard thinning/disappearing, hair darkening. Any card with a thinned beard is rejected.
- **Hand card rule (the labels incident):** First-pass hand cards shipped with baked-in text headers/footers ("ANIMATION RIG REFERENCE CARD" etc.) and were regenerated CLEAN. Rig cards must be asset-only: hand, white background, no text.
- **Pendant:** reads "STATIC" — never "SWMG" as text on screen (canon).
- **Personality/acting:** loud, energetic, Enzo Amore energy. Big gestures, big grins, mic-hand energy. The happy/ee viseme and pointing/beckoning hands are his workhorses.

---

## 9. LIKENESS CHECKLIST

Before any asset enters the pipeline:

- [ ] Skin tone = #FFCEA8 (numeric check)
- [ ] Hair is bleached blond (#FFF987), messy, medium length — never darkened
- [ ] Beard is dark and full (#000000), never thinned
- [ ] Teeth are normal, not sharp, no grill
- [ ] Robe is deep blue (#111B5A), pendant reads STATIC
- [ ] Style: thick black outlines, flat cel shading (SWWMG base)
- [ ] Visually verified by human eyes, not just filename — all 24 cards checked this build

---

*Companion: `STATIC-ANIMATION-GUIDE.md` (full rig documentation). Template: `~/workspace/animation-techniques/templates/character-model-sheet-template.md`.*
