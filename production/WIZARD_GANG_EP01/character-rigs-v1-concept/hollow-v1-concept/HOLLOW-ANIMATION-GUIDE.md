# HOLLOW ANIMATION GUIDE — Silent-Character Rig

**Character:** Hollow (Wizard Gang)
**Date:** 2026-10-10
**Rule:** FULLY MASKED — the face is NEVER visible. The mask pattern NEVER changes.

This is the complete animation rig for Hollow: 10 mask-mouth visemes, 6 eye-glint
expressions, 10 hand poses. Built for a character who is **mostly SILENT** —
he acts through body language and eyes, not dialogue.

---

## PART A — MOUTH (the mask's shark-tooth jaw)

### 1. The Actual Design

Hollow's "mouth" is the **jagged white shark-tooth design on his black lucha mask**
(#FEFEFE teeth on #0A0A0A mask). It is NOT a human mouth — it is mask artwork that
moves like a jaw. The zigzag tooth pattern is his identity: sharp points, never
rounded, never smoothed, never replaced with lips and teeth.

All 10 viseme cards were generated from ONE base image, so they are pixel-aligned.
The tooth pattern stretches, splits, and puckers across visemes but never changes
its jagged identity.

### 2. Viseme Set (10 — Full Preston Blair, adapted for the mask)

| Viseme | File | Shape |
|--------|------|-------|
| Rest | viseme-rest.png | Closed zigzag grin line — the default mask face |
| Ah | viseme-ah.png | Wide dark oval, jagged teeth top + bottom |
| Ee | viseme-ee.png | Teeth bared grimace, stretched zigzag, thin slit |
| Oh | viseme-oh.png | Rounded oval, teeth around top + bottom edges |
| Oo | viseme-oo.png | Small puckered ring-of-teeth opening |
| M/B/P | viseme-mbp.png | Fully shut flat seam — NON-NEGOTIABLE |
| F/V | viseme-fv.png | Upper teeth over lower mask lip — bite/grit |
| L | viseme-l.png | Slightly open, tongue tip behind upper teeth |
| Hiss | viseme-hiss.png | Narrow slit between tooth rows |
| Th | viseme-th.png | Tongue poking between the teeth |

**M/B/P is non-negotiable.** When he finally gets a voice, every b, p, m sound
uses the fully-shut seam. The mask mouth closes exactly like a real mouth would.

### 3. What NOT To Do

- Do NOT put a human mouth on the mask — no lips, no gums, no realistic teeth
- Do NOT smooth or round the shark teeth ("fixing" them is a defect)
- Do NOT change the zigzag pattern between visemes — compare against viseme-rest.png
- Do NOT let the tongue color drift — tongue is #F77988, only in L / TH

---

## PART B — EYES (acting through the glints)

### The Silent Actor's Instrument

Hollow has no voice and no visible face. His **eyes are his dialogue**. The ice-blue
glints (#AEE7FB) inside the blue-trimmed eye holes carry every emotion the way a
talking character's voice would. When in doubt, push the eyes harder — the audience
reads him through them.

### The 6 Expressions

| Expression | File | Glint description |
|------------|------|-------------------|
| Neutral | eyes-neutral.png | Level symmetrical soft glints — his resting recruiting gaze |
| Blink | eyes-blink.png | Compressed to thin faint lines — use every 3–5s, always on head turns |
| Happy | eyes-happy.png | Upturned crescent arcs, brighter — rare, use sparingly |
| Angry | eyes-angry.png | Sharp inward-down blades, hot white core — intimidation beat |
| Sad | eyes-sad.png | Drooped outer corners, dimmer — the quiet beat |
| Surprised | eyes-surprised.png | Large round ovals, hot core — maximum openness |

### Acting Rules for a Silent Character

1. **Blink is his punctuation.** Without dialogue, blinks mark the ends of his
   "sentences" — the beat after a gesture lands, before he turns away.
2. **Hold the stare.** His recruiting-pitch energy is a long, unbroken neutral
   gaze. Do NOT cut away or blink-flutter during the pitch — the stillness IS the menace.
3. **Angry glints + slow head tilt = his entire threat vocabulary.** He doesn't
   shout. The blades come out and the head tilts 5 degrees. That's the scene.
4. **Never warm the glints.** #AEE7FB ice-blue always. Warm yellow glints belong
   to Ashes — cross-contamination breaks both characters.
5. **Surprised is his loudest emotion.** Use it once per episode maximum.
   A silent character who is never surprised is unreadable; one who is often
   surprised is a cartoon.

---

## PART C — HANDS (the second voice)

### Why Hands Matter More for Him

With no dialogue and no face, Hollow's hands do the talking most characters do
with their mouths. The recruiting pitch is choreographed like a speech:

| Beat | Hand | Notes |
|------|------|-------|
| The invitation | hand-beckoning.png | Hooked index — his signature move. Hold it. |
| The promise | hand-open-palm.png | Open, presenting — "look what we offer" |
| The proof | hand-counting.png | Three fingers — listing the terms |
| The seal | hand-fist.png | Clench on the final beat |
| The casual | hand-shaka.png | Only with people he's already won over |

### Technical Notes

- **Finger count:** 5 digits (4 fingers + thumb) — verified on every card
- **Skin tone:** #B17447 — PROVISIONAL, sampled from the cards; confirm against
  episode frames when Hollow appears in 2D
- **Mirror horizontally for the left hand** — do not generate separate left cards
- **hand-holding.png** is an empty pinch — composite props (pendant, coin, flyer) in post
- Robed scenes: hands emerge from the orange sleeves — keep the wrist crop clean

---

## PART D — THE RECRUITING PITCH (his scene grammar)

Hollow is "always mid-recruiting-pitch" (likeness bible). His scenes follow a rhythm:

1. **Enter still.** Neutral glints, relaxed hands, mask forward. Let the mask do the work.
2. **The beckon.** One hooked finger. Eyes stay neutral — the contrast is the hook.
3. **The terms.** Counting hand, slow deliberate finger raises. Blink between each term.
4. **The close.** Open palm extended toward the recruit. Long hold. No blink.
5. **The turn.** Angry blades for one beat if refused — then walk away, glints back
   to neutral before he exits frame. Never let the audience see him break.

**Timing:** He moves SLOWER than the talking characters. A silent character who
moves fast looks panicked. Half-speed gestures, full-speed eye changes.

---

## PART E — WHAT NOT TO DO (hard rules)

1. **NEVER unmask him.** No "dramatic reveal," no mask slipping, no battle damage
   exposing skin. The mask is the character. An unmasked Hollow is not Hollow.
2. **NEVER show a face under the mask.** Not in shadow, not in silhouette, not in
   "what's under there" teases. Black void inside the eye holes, always.
3. **NEVER change the mask pattern.** The zigzag teeth, blue trim, tassels,
   dreadlock strands, ear protrusions — all fixed. New shot, same mask. Compare
   every new render against `visemes/viseme-rest.png`.
4. **NEVER let the hair strands vanish.** If a render drops the dreadlocks, it is
   a failed render, not a style choice.
5. **NEVER give him a voice without owner approval.** He is silent until the owner
   finds the voice. The visemes exist for THAT day — not as an excuse to make him talk now.
6. **NEVER warm his glints.** Ice-blue #AEE7FB. Warm = Ashes. Different character.
7. **NEVER rush him.** Slow gestures, held stares. Speed is the enemy of menace.
8. **NEVER bake text into cards.** All rig cards are clean art only — no labels,
   banners, or captions (swept 2026-10-10).

---

## TEMPLATE NOTE

This rig follows the Ashes pattern (`~/workspace/ashes-mouth-pack/`):
one aligned base for all visemes, eye cards in the character's eye style
(glints through mask holes), 10 hand poses in the character's skin tone,
every card verified by human eyes before entering the pipeline.

*Companion: `HOLLOW-MODEL-SHEET.md` (color model + likeness checklist). Likeness source: `EP02_LIKENESS_BIBLE.md` §7.*
