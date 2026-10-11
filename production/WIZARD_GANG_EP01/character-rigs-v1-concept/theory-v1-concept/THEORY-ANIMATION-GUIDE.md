# THEORY — ANIMATION GUIDE

**Show:** Wizard Gang · **Character:** Theory / "The Algorithm" · **Date:** 2026-10-10 · **Version:** v1

Companion to `THEORY-MODEL-SHEET.md`. How she moves, how she speaks, and what to never do.

---

## 1. WHO SHE IS (MOVEMENT IDENTITY)

Theory is the intellectual of the gang — a notebook writer. Her body language is **precise, economical, and thoughtful.** She never flails, never lunges, never thrashes. Every gesture looks considered, like she's mid-thought even when still.

- **Resting state:** upright posture, shoulders relaxed but squared, hands often clasped or one hand holding the other's wrist. Chin slightly raised — observant, not arrogant.
- **Energy level:** low baseline, high intentionality. When she moves, it means something.
- **Rhythm:** deliberate beats. She pauses between gestures. The pause IS the gesture — let her hold a beat before she points or turns a page.

## 2. HOW SHE MOVES

### Head and face
- **Unrobed:** small, controlled head tilts (a few degrees, not cartoon swings). Eyebrows do the emotional lifting — a slight raise reads as surprise, a slow lower as skepticism. Her mouth moves cleanly to the viseme chart; no jaw exaggeration, no rubbery mouth.
- **Robed:** no head needed for emotion — the glints do it all. Glint changes should read instantly: narrow to sharp for anger, droop for sad, widen for surprise. A glint "narrow" (2–3 frames) can precede a knowing line. Glint drift across shots is a defect — same shape, same position, same robe.

### Writing gestures (her signature)
- Writing is held mid-frame when she does it: pen pinch grip (`hand-holding.png`), wrist resting, small precise strokes. She writes *while* listening — the pen keeps moving under dialogue.
- Page-turn: two fingers (`hand-gripping.png` to open-palm flip). Never a fast cartoon page-slap — it's a slow, deliberate turn, like she doesn't want to lose the thought.
- Notebook-tap: index finger (`hand-pointing.png`) taps the page twice for emphasis on a line of dialogue. TWO taps, not one, not three.

### Gesturing
- Open-palm presentations are her default explanation move — palm up, fingers together, elbow relaxed.
- Pointing is rare and deliberate: one slow index extension, held. She points AT the thing that matters, not around the room.
- Counting on fingers for lists ("first, second") — use `hand-counting.png` variants.
- Her fist almost never closes. If she fists, something is wrong — play it as the beat's climax.

## 3. LIP SYNC RULES

- Use the 10 Preston Blair cards from `visemes/` — they are pixel-aligned from a single base.
- **M/B/P is non-negotiable:** lips fully pressed, no teeth, no gap. A leaking MBP ruins sync more than any other viseme.
- Hold each viseme 2–3 frames minimum; Theory's delivery is measured, not rapid-fire.
- No mouth on the robed void form — EVER. If a robed shot needs dialogue, the voice carries it (glints can pulse subtly). Never paste a mouth into the void.

## 4. EYE / GLINT ACTING

| Emotion | Glint shape | Intensity |
|---------|------------|-----------|
| Thinking | Narrow, steady slits | Normal |
| Knowing / "I figured it out" | One glint sharpens slightly before the other | +10% |
| Anger | Blades angled inward-down | Hot glare |
| Sad | Outer corners drooped | Dim |
| Amused (her version of happy) | Soft upturned arcs — reserved, not bubbly | Warm |
| Surprise | Large round ovals | Hot core |

Theory doesn't do big cartoon takes. Her surprise is a glint widen, not a scream.

## 5. HAND ACTING NOTES

- 5 digits always (4 fingers + thumb) — verified on every card.
- Mirror horizontally for the left hand; do NOT redraw.
- Pen grip is pinch: thumb + index, three fingers curled — `hand-holding.png`.
- When she holds the notebook, the hand cards composite onto the prop in post — never bake a prop into the card.

## 6. WHAT NOT TO DO (DEFECTS, NOT VARIATIONS)

1. **NO Disney/Pixar 3D face.** She is flat 2D cel, thick black outlines. Any render with gradient-shaded cheeks, subsurface skin, or 3D depth is a defect — reject it.
2. **NO ear shrinkage.** The cat ears are LARGE and upright. Ears that shrink, flatten, or vanish between shots are the #1 drift hazard — check every frame.
3. **NO sunglasses on attire 1/3.** The rejected sunglasses v1 is dead. Sunglasses appearing = regenerate.
4. **NO generic face drift.** She has a specific face: soft features, full lips, septum ring. If she stops looking like the viseme base between attires, the card is wrong.
5. **NO whitewashing.** Skin #AE5B2A, locked. Any generation that lightens her gets rejected and redone.
6. **NO mouth on the void.** Robed form = black void + glints. No lips, no teeth, no eyebrows, no nose in the void.
7. **NO frenetic motion.** She is not Cipher. No flailing, no speed-lines-on-idle, no bounce. If her walk cycle has more bounce than a brisk stroll, it's wrong.
8. **NO pink/metallic lips.** Lips are natural warm brown. Pink lipstick reads as a different person.
9. **NO locs changing.** Medium length, dark, beaded. Not longer, not shorter, not another color, not straightened.
10. **NO hand drift.** 5 digits, delicate and precise. Six fingers, meaty hands, or claws = regenerate.

## 7. SCENE NOTES

- Notebook is her anchor prop. When she's on screen in a quiet scene, the notebook should be present or implied (in hand, on lap, under arm).
- Robed scenes: she leads from stillness. The other gang members emote around her; she is the calm center.
- Intellectual beats pair with narrow glints and slow hand gestures — never fast cuts during her lines.

---

*Rig cards: `visemes/` (10), `eyes/` (6), `hands/` (10). All human-eye QC'd 2026-10-10. Model sheet: `THEORY-MODEL-SHEET.md`.*
