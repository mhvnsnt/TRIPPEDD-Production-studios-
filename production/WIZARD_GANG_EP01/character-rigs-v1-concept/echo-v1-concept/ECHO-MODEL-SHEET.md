# ECHO — CHARACTER MODEL SHEET

**Show:** Wizard Gang
**Character:** Echo
**Date created:** 2026-10-10
**Version:** v1
**Status:** approved

> **Owner's law:** Do NOT redesign her. Capture her exactly as shown.
> **Green hair is law.** Long straight GREEN hair — never black, never brown.
> Normal teeth — NOT sharp (that was Ashes; Echo's teeth are natural).

**Likeness source:** EP02 Likeness Bible §5 (clean Shotzi Blackheart face = canon
variant 2/3; possessed black-mist-mouth variant NOT used here). Real-world basis:
Shotzi Blackheart — feminine, defined features, heavy eye makeup.

---

## 1. TURNAROUND

| View | File | Status |
|------|------|--------|
| Front | `turnaround-front.png` | TODO |
| 3/4 | `turnaround-34.png` | TODO |
| Side | `turnaround-side.png` | TODO |
| Back | `turnaround-back.png` | TODO |

**Proportions:**
- Athletic build (savate fighter)
- Full tattoo sleeves on BOTH arms, chest tattoo, leg tattoo
- Black choker at neck
- Long straight green hair falling past shoulders, framing the face

---

## 2. EXPRESSION SHEET

Covered by eye-expression cards (visible feminine cartoon eyes, heavy winged
eyeliner + long lashes). See Section 4.

---

## 3. MOUTH CHART (Preston Blair)

All cards generated from ONE base image (`viseme-rest.png`) — mouth-only edits,
pixel-aligned across the set. Face = clean Shotzi variant, normal natural white
teeth (NOT sharp, NOT fangs).

| Viseme | Sounds | Description for ECHO | File |
|--------|--------|---------------------|------|
| Rest | silence | Mouth closed, relaxed neutral line, teeth hidden | `visemes/viseme-rest.png` |
| Ee | egg, eat, tree | Lips stretched wide in a grin, upper+lower teeth meeting | `visemes/viseme-ee.png` |
| Oh | oh, goat, hot | Rounded O opening, hint of upper teeth, dark interior | `visemes/viseme-oh.png` |
| Oo | oo, you | Small pursed round lips, no teeth | `visemes/viseme-oo.png` |
| M/B/P | m, b, p | Lips pressed firmly shut, flat line — non-negotiable | `visemes/viseme-mbp.png` |
| F/V | f, v | Upper front teeth resting on lower lip | `visemes/viseme-fv.png` |
| L | l, t, d, n | Mouth slightly open, tongue tip up behind upper teeth | `visemes/viseme-l.png` |
| Hiss | s, z | Teeth nearly together, thin dark gap, lips pulled back | `visemes/viseme-s.png` |
| Ah | ah, eye, hat | Jaw dropped, wide open oval — **MISSING (see note)** | `visemes/viseme-ah.png` |
| Th | th | Tongue tip between teeth — **MISSING (see note)** | `visemes/viseme-th.png` |

**Missing-card note:** `viseme-ah.png` and `viseme-th.png` could not be generated —
the image pipeline refused those two prompts on policy grounds. Do NOT regenerate
them with workarounds; fill them in a later pass. Fallback until then: use
`viseme-oh.png` for AH sounds and `viseme-l.png` for TH sounds (closest jaw/tongue
shape in the set).

**M/B/P is non-negotiable.** Every b, p, m sound MUST use the closed shape.

---

## 4. EYE EXPRESSIONS

**Eye style:** Visible feminine cartoon eyes — brown irises, heavy black winged
eyeliner, long upper lashes, strong dark brows. Emotion conveyed through
lid shape, brow angle, and eye openness.

| Expression | Description | File |
|------------|-------------|------|
| Neutral | Calm resting gaze, level lids, open eyes | `eyes/eyes-neutral.png` |
| Blink | Mid-blink: lids nearly closed, lash line + faint crease | `eyes/eyes-blink.png` |
| Happy | Warm upturned crescent arcs, joyful outer-corner crinkles | `eyes/eyes-happy.png` |
| Angry | Narrowed slits, lids angled steeply down-in, fierce glare | `eyes/eyes-angry.png` |
| Sad | Outer corners drooped, heavy lids, sorrowful brow arch | `eyes/eyes-sad.png` |
| Surprised | Wide round eyes, large pupils, brows raised high | `eyes/eyes-surprised.png` |

All in `~/workspace/character-rigs/echo/eyes/`.

**Known deviation:** `eyes-blink.png` was regenerated as a fresh card (the edit
pass failed on a file race) and the generator added a septum ring + nostril stud
that are NOT in the neutral base. These piercings are NOT canon — ignore them,
or crop to the eye region only.

---

## 5. HAND POSES

**Finger count:** 5 digits (4 fingers + thumb) — verified on every card
**Skin tone:** #FED2AF (light; sampled from cards). Black polish on fingertips.

| Pose | Use for | File |
|------|---------|------|
| Open palm | Gesturing, presenting, the mirror "study" | `hands/hand-open-palm.png` |
| Fist | Emphasis, anger, savate guard | `hands/hand-fist.png` |
| Pointing | Directing attention, accusation | `hands/hand-pointing.png` |
| Gripping | Holding bars, ledges, props | `hands/hand-gripping.png` |
| Thumbs up | Approval | `hands/hand-thumbs-up.png` |
| Relaxed | Idle | `hands/hand-relaxed.png` |
| Counting | Numbers, listing (3 fingers up) | `hands/hand-counting.png` |
| Beckoning | "Come here" — hooked index | `hands/hand-beckoning.png` |

All in `~/workspace/character-rigs/echo/hands/`. Mirror horizontally for the
left hand. Regenerated twice to pass QC: counting (v1 showed 2 fingers, v2 shows
the correct 3) and beckoning (v1 read as an OK-gesture, v2 is a true hook).

---

## 6. COLOR MODEL

Sampled numerically from the generated cards (histogram/mode on 1600px PNGs),
not eyeballed.

| Area | Hex | Notes |
|------|-----|-------|
| Hair | #00FF16 | Vivid green. NEVER black/brown — this is the #1 drift hazard |
| Skin (face) | #FCE2CF | Light natural |
| Skin (hands) | #FED2AF | Light natural |
| Teeth | #FFFFFF | Natural white. NEVER sharp/fangs — that's Ashes, not Echo |
| Robe primary | #C37D99 | Pink |
| Pendant (ECHO) | #FFC75D | Gold, reads "ECHO" |
| Choker | #0A0A0A | Black |
| Nail polish / dark fingers | #1A1A1A | Black |
| Iris | #7A4A24 | Dark brown (visual; heavy black winged liner around) |
| Tattoos | n/a | Full sleeves both arms + chest + leg — MUST be present in full-body shots |

---

## 7. SCALE REFERENCE

| Compared to | Relative height | Notes |
|-------------|----------------|-------|
| Ashes | Shorter | Ashes is one of the larger gang members |
| Group | Fill in from group photo | TODO: measure |

---

## 8. CHARACTER NOTES

- **Green hair is the character.** If a generation returns black/brown hair, reject. Every time. This is the top drift hazard in the bible.
- **Normal teeth.** Do NOT "fix" her teeth into sharp/fang shapes — sharp teeth are ASHES's design, not Echo's.
- **Clean face variant used (canon 2/3).** The possessed black-mist-mouth is canon variant 1 — never mix it into this rig's cards.
- **Tattoos must exist.** Full sleeves both arms, chest tattoo, leg tattoo. These cards are face/hand close-ups so tattoos don't appear here, but any full-body asset without them is wrong.
- **Black choker + pink robe + ECHO pendant** are her identity anchors in robe form.
- **Dark fingers:** black polish on all fingertips, visible in every hand card.
- **Voice:** UNKNOWN — visual-only until owner locks a voice. Do not assign dialogue personality beyond the mirror-fighter concept.
- **Animate what's there:** Don't paste a mouth on top of the scene. Build talking animation FROM her actual mouth.

---

## 9. LIKENESS CHECKLIST

- [ ] Hair is vivid green #00FF16 — numeric check, not eyeball
- [ ] Teeth are normal/natural, not sharp
- [ ] Skin tone matches color model (face #FCE2CF / hands #FED2AF)
- [ ] Clean Shotzi face — none of the possessed-mist variant
- [ ] Choker + pink robe + ECHO pendant present in face cards
- [ ] Tattoos present in any full-body asset
- [ ] Black polish on fingertips in hand cards
- [ ] Style: thick black outlines, flat cel shading
- [ ] Human eyes verified, not just filename

---

*Companion: `ECHO-ANIMATION-GUIDE.md` (full rig documentation). Template: `~/workspace/animation-techniques/templates/character-model-sheet-template.md`. Pattern: `~/workspace/ashes-mouth-pack/`.*
