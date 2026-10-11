# ECHO ANIMATION GUIDE — Full Character Rig

**Character:** Echo (Wizard Gang)
**Date:** 2026-10-10
**Rule:** Do NOT redesign her. Capture her exactly as shown.

This is the complete animation rig for Echo: 8 mouth visemes, 6 eye expressions, 8 hand poses. It follows the Ashes rig template (`~/workspace/ashes-mouth-pack/`).

---

## PART A — MOUTH

### 1. The Actual Design (Bible-Locked)

**Echo's teeth are NORMAL — that's her character, not a defect.**

The SHARP-teeth look belongs to Ashes. Echo has natural, white, human teeth in a feminine mouth. Do not "fix" her into fangs — and do not soften Ashes into her.

**Face variant in use:** clean Shotzi Blackheart face (canon variant 2/3). The possessed black-mist-mouth is canon variant 1 — a different rig's problem, never mixed in here.

### Key Features
- **Tooth shape:** Natural, even, white. Upper teeth visible in smiles and open vowels.
- **Mouth shape:** Feminine, full lips, defined cupid's bow. Neutral rest = relaxed straight line.
- **Skin:** Light (#FCE2CF sampled). NEVER darken or lighten.
- **Hair frame:** Long straight vivid-green hair (#00FF16) frames both sides of the face in every card. If a card loses the green, the card is wrong.
- **Choker + robe:** Black choker and pink robe collar with gold ECHO pendant anchor the face cards.
- **Single-base rule:** ALL visemes were generated as mouth-only edits of ONE base image (`viseme-rest.png`). Everything outside the mouth is pixel-identical across the set — no re-alignment needed when cutting between cards.

### What NOT To Do
- Do NOT make the teeth sharp/pointed (that's Ashes, not Echo)
- Do NOT turn the green hair black or brown (the #1 drift hazard)
- Do NOT swap in the possessed-mist mouth variant
- Do NOT animate a mouth that wasn't there — work from what's in the frame
- Do NOT whitewash or recolor her skin tone. Ever.

### 2. Viseme Set (8 — Preston Blair; 2 pending)

| Viseme | File | Preston Blair | Description |
|--------|------|---------------|-------------|
| Rest | viseme-rest.png | Rest / X | Mouth closed, relaxed neutral line, teeth hidden |
| Ee | viseme-ee.png | E | Lips stretched wide in a grin, teeth meeting edge-to-edge |
| Oh | viseme-oh.png | O | Rounded O opening, hint of upper teeth |
| Oo | viseme-oo.png | U | Small pursed round lips, no teeth |
| M/B/P | viseme-mbp.png | M, B, P | Lips pressed firmly shut, flat line — no teeth |
| F/V | viseme-fv.png | F, V | Upper front teeth resting on lower lip |
| L | viseme-l.png | L, T, D, N | Slightly open, tongue tip up behind upper teeth |
| Hiss | viseme-s.png | S, Z | Teeth nearly together, thin dark gap, lips pulled back |

**Missing (policy-blocked, do not retry with workarounds):**
- `viseme-ah.png` (AH: jaw dropped wide) → fallback: `viseme-oh.png`
- `viseme-th.png` (TH: tongue tip between teeth) → fallback: `viseme-l.png`

**M/B/P is non-negotiable.** Every b, p, m sound in dialogue MUST use the closed shape. The audience catches a missed lip-closure instantly.

### The Core Principle (Owner's Law)

> "You're supposed to be making the mouths in the different expressions and the animations based off of what's there in the scene. Not adding something over the scene that's not there."

**Translation:** Animate the mouth that is already hers. Don't paste a foreign mouth onto her face. The visemes are for building talking animation FROM her actual mouth design.

---

## PART B — EYES

### Style Decision: VISIBLE FEMININE CARTOON EYES

Unlike Ashes' shrouded glints, Echo's eyes are fully visible: brown irises, heavy black winged eyeliner, long upper lashes, strong dark brows. Her expressions read through **lid shape, brow angle, and openness** — classic 2D cartoon acting.

(Eye cards are framed as forehead-to-nose crops of the same character design as the mouth cards: green hair framing, same brows, same liner style.)

### The 6 Expressions

| Expression | File | Description |
|------------|------|-------------|
| Neutral | eyes-neutral.png | Calm resting gaze, level lids, open eyes |
| Blink | eyes-blink.png | Mid-blink: lids nearly closed, lash line + faint crease above |
| Happy | eyes-happy.png | Warm upturned crescent arcs, crinkle notches at outer corners |
| Angry | eyes-angry.png | Narrowed slits angled steeply down-in, fierce glare |
| Sad | eyes-sad.png | Outer corners drooped low, heavy lids, sorrowful brow arch |
| Surprised | eyes-surprised.png | Wide round eyes, large pupils, brows raised high |

**Blink card caveat:** `eyes-blink.png` carries non-canon nose piercings (septum ring + nostril stud) added by the generator on a fresh-card regeneration — the edit-based attempt failed on a file race. The piercings are NOT her design. Crop to the eye region or ignore them; never treat them as canon.

### Blink Rules (from the Animation Playbook)
- Blink every 3–5 seconds during dialogue
- **Always blink on head turns** — hides the transition
- Blink on stressed/emphasized words for punch
- Full blink = 2–3 frames at 30fps
- Echo's heavy lashes make the blink read clearly even at 2 frames

### Usage
Match the expression to the dialogue emotion — her eyes sell the acting, especially the mirror-fighter "study" beat: neutral, locked-on gaze while she memorizes an opponent's style.

---

## PART C — HANDS

### Finger Count: 5 digits (4 fingers + thumb)
Verified on every card. All cards match.

### Skin Tone: light, numerically sampled
Face #FCE2CF · hands #FED2AF. All cards cluster consistently — never recolored.

### Signature Detail: BLACK POLISH
Every fingertip carries black nail polish (dark fingers per the bible). Present in all 8 cards. If a hand card loses the black polish, reject it.

### The 8 Poses

| Pose | File | Use for |
|------|------|---------|
| Open palm | hand-open-palm.png | Gesturing, presenting, the mirror "study" hand |
| Fist | hand-fist.png | Emphasis, anger, savate guard |
| Pointing | hand-pointing.png | Directing attention, accusation |
| Gripping | hand-gripping.png | Holding bars, ledges, handles |
| Thumbs up | hand-thumbs-up.png | Approval, agreement |
| Relaxed | hand-relaxed.png | Idle, hanging at side |
| Counting | hand-counting.png | Holding up 3 fingers — numbers, listing |
| Beckoning | hand-beckoning.png | "Come here" — hooked index finger |

### How to Use
- Mirror horizontally for the left hand — do not generate separate left-hand cards
- Robed characters: most hand shots are covered by sleeves — only use when the hand is visible
- If the hand isn't doing something, hide it (pockets, behind back, in sleeves)
- Her savate base means hands stay in guard or gesture — she copies with her whole body, so hands often mirror the opponent's

### QC Notes (what got fixed)
- **Counting** v1 showed 2 fingers (peace sign) — regenerated; v2 shows the correct 3.
- **Beckoning** v1 read as an OK-gesture — regenerated; v2 is a true hooked-index "come here."

---

## TEMPLATE NOTES FOR OTHER CHARACTERS

This rig follows the Ashes template. The single-base-image method worked: generate ONE neutral face, then mouth-only edits for every viseme. It held pixel alignment across all 8 cards with zero re-alignment work.

**Watch for:**
1. **Policy blocks on mouth-interior prompts** — `ah` and `th` were both refused. Phrase future attempts without interior/tongue detail, or plan fallbacks up front.
2. **Fresh generations drift** — the blink card regenerated from scratch picked up nose piercings. Prefer edit-chaining from the base over fresh generations.
3. **Hand pose misreads** — counting and beckoning both needed a second pass. Verify finger COUNT (not just finger presence) and the dominant gesture read before accepting.

**Likeness checklist (applies to every character):**
- [ ] Skin tone matches reference (sampled hex, not eyeballed)
- [ ] Teeth/mouth shape matches reference (not "corrected")
- [ ] No whitewashing, no color drift on lips/skin/hair
- [ ] Style matches show (thick outlines, flat cel shading)
- [ ] All cards visually verified before entering the pipeline

---

*Companion: `ECHO-MODEL-SHEET.md` (color model + likeness law). Template: `~/workspace/animation-techniques/templates/character-model-sheet-template.md`. Pattern: `~/workspace/ashes-mouth-pack/ASHES-ANIMATION-GUIDE.md`.*
