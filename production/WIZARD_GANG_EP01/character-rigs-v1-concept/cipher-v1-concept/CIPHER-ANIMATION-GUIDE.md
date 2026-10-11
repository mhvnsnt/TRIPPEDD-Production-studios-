# CIPHER ANIMATION GUIDE — Full Character Rig

**Character:** Cipher (Wizard Gang — based on Lio Rush 2026 Blackheart persona)
**Date:** 2026-10-10
**Rule:** Do NOT redesign him. Capture him exactly as shown.

This is the complete animation rig for Cipher: 10 mouth visemes, 6 eye expressions, 8 hand poses. It follows the Ashes rig template, built around his defining trait: **the feral manic grin is his default face, not an expression.**

---

## PART A — MOUTH

### 1. The Actual Design

**Cipher's grin is his identity.**

- **Grin:** Wide, corners pulled far back, lips parted. In every reference frame he is grinning — the ref pack (`trippedd-studio/production/WIZARD_GANG_EP01/cipher-refs/`) is 18 stills of manic grin/stare variants. No calm face exists in canon.
- **Mouth interior:** Near-black (#000000), the Blackheart liquid look — glossy ink highlights in the dark. This is INTENTIONAL CHARACTER DESIGN. It is not dirt, not a defect, not something to "clean." The one time a generation lost it (pink interior), it was corrected back.
- **Teeth:** Natural off-white (#F8EACF). Upper row prominently visible in the grin. NOT gold — Cipher has no grill; gold is for his pendant only.
- **Brow:** Heavy, furrowed, black — always. It frames the eyes in every card.
- **Skin:** Dark brown (#7A4839). NEVER lighten.
- **Size:** Mouth is large — the grin dominates the lower face. In close-ups the grin spans roughly 2/3 of face width.

### 2. Build Method (The Single-Base Rule)

Learned from the Ashes v2 failure: **all 10 visemes were derived from ONE base face image** via mouth-only edits — nothing else moved. This keeps every card pixel-aligned. The method:

1. Generate one locked front-facing base face (`viseme-rest.png`, also doubled as `eyes-neutral.png`).
2. For each viseme, edit the base changing ONLY the mouth; every other pixel must survive.
3. Verify each edit with human eyes against the drift list: grin gone? stubble added? interior color changed? skin lightened? If yes — fix or regenerate, never accept.

### 3. Viseme Set (10 — Full Preston Blair)

| Viseme | File | Preston Blair | Description |
|--------|------|---------------|-------------|
| Rest | viseme-rest.png | Rest / X | Wide feral grin at rest, lips parted, black interior, upper teeth visible — manic, never calm |
| Ah | viseme-ah.png | A / I | Jaw dropped in a big oval, upper + lower teeth visible, black interior, corners pulled back |
| Ee | viseme-ee.png | E | Stretched wide grin, teeth nearly clenched, thin black slit between them |
| Oh | viseme-oh.png | O | Rounded puckered opening, teeth peeking top and bottom, deep black interior |
| Oo | viseme-oo.png | U | Small pursed round opening, grin corners pinched tight, small black hole |
| M/B/P | viseme-mbp.png | M, B, P | Lips pressed firmly shut — flat tight dark line, NO teeth — non-negotiable |
| F/V | viseme-fv.png | F, V | Upper teeth resting ON the lower lip, thin dark gap below |
| L | viseme-l.png | L, T, D, N, Th | Slightly open, tongue tip up behind upper teeth, black interior behind |
| S (hiss) | viseme-s.png | S, K, G, Z | Snarling grin, teeth clenched nearly shut, thin horizontal black slit |
| Th | viseme-th.png | Th | Tongue tip poking just past upper teeth, teeth visible, black interior behind |

**M/B/P is non-negotiable.** Every b, p, m sound MUST use the closed shape. Note Cipher's closed shape reads as a tight DARK line — the grin crease lines at the corners keep it feral even when shut. A missed closure on Cipher is doubly visible because his mouth is always so big.

### The Core Principle (Owner's Law, carried over from Ashes)

> "You're supposed to be making the mouths in the different expressions and the animations based off of what's there in the scene. Not adding something over the scene that's not there."

**Translation:** The visemes extend HIS grin into speech shapes. They are not a foreign mouth. When animating dialogue, cut between his actual grin states — don't paste a generic talking mouth over the scene.

### Cipher-Specific Dialogue Energy

He speaks in whisper-to-shriek bursts (Lio Rush 2026 Blackheart). Animation-wise that means:
- Whispers: hold near-mbp/rest shapes, tiny jitter — small fast amplitude on the mouth.
- Shrieks: slam between ah/oh at maximum stretch for 1–2 frames (impact pop), no easing.
- Zoned-out beats: hold viseme-rest with micro eye-drift — he stares THROUGH the scene.

---

## PART B — EYES

### Style Decision: VISIBLE MANIC EYES

Unlike Ashes' shrouded glints, Cipher's eyes are fully visible cartoon eyes — white sclera, dark charcoal pupils — under a heavy furrowed brow. The emotion lives in **pupil size, lid state, and brow angle**, and the brow is as much of the expression as the eyes.

### The 6 Expressions

| Expression | File | Eye/brow description |
|------------|------|---------------------|
| Neutral | eyes-neutral.png | Wide staring manic gaze, heavy furrowed brow, pupils slightly off-center — zoned-out feral (this IS his resting face) |
| Blink | eyes-blink.png | Mid-blink: lids nearly closed into tight lid lines, thin slits — 2–3 frames at 30fps |
| Happy | eyes-happy.png | Wide sparkling eyes, larger pupils with catchlights, brows raised — manic-happy, never cute |
| Angry | eyes-angry.png | Brows slammed down and angled steeply inward, eyes narrowed to sharp slits, small burning pupils |
| Sad | eyes-sad.png | Heavy brows raised inward-up, half-lidded drooped eyes, dark tired bags — sad-feral, never calm-sad |
| Surprised | eyes-surprised.png | Eyes at maximum round size, huge sclera, tiny dot pupils, brows arched high — shocked-feral |

### Cipher Eye Rules
- **He stares.** Hold neutral longer than feels normal — 4–6 seconds before a blink during dialogue, versus the standard 3–5. The stare is the character.
- **Pupils drift.** During zoned-out lines, let the pupils drift off-center for 1–2 seconds before snapping back. That snap is one of his signature beats.
- **Brow leads.** Start an emotional shift with the brow 2 frames before the eyes change — the heavy brow is his telegraph.
- **Never calm eyes.** If a composite ever shows him with soft relaxed eyes, it's wrong — check which card got pulled.

### Correction history (flagged so it never recurs)
- **Sad v1:** generation added facial stubble + reddish mouth interior → corrected: smooth clean-shaven skin, near-black interior, heavier brows.
- **Surprised v1:** generation lost the black interior (pink/red mouth, pink tongue) + thin arched brows → corrected: near-black interior, dark tongue, thick brows.
- **Rule learned:** when generating standalone eye cards, lock "near-black mouth interior, no stubble, heavy brow" in the prompt — these are the three things the generator tries to "fix."

---

## PART C — HANDS

### Finger Count: 5 digits (4 fingers + thumb)
Verified by human eyes on every card. All cards match.

### Skin Tone: #7A4839
Sampled from the face. Every hand card keeps it. Never lightened.

### Wrist Mark: MOTH TATTOO
Every hand card carries a small simple moth tattoo on the back of the wrist — his signature ink (echoes the moth chest tattoo in the likeness bible). If a card lacks it, reject.

### The 8 Poses

| Pose | File | Use for |
|------|------|---------|
| Open palm | hand-open-palm.png | Gesturing, presenting, taunting |
| Fist | hand-fist.png | Emphasis, anger, about-to-pounce |
| Pointing | hand-pointing.png | Directing attention, accusation |
| Gripping | hand-gripping.png | Holding umbrella, staff, handles — composite props into the grip in post |
| Thumbs up | hand-thumbs-up.png | Approval (manic approval — it's never calm) |
| Relaxed | hand-relaxed.png | Idle, hanging at side |
| Counting | hand-counting.png | Holding up 3 fingers — numbers, listing |
| Beckoning | hand-beckoning.png | "Come here" — hooked index, summoning |

### How to Use
- Mirror horizontally for the left hand — do not generate separate left-hand cards
- **hand-gripping.png** holds a plain wooden handle — composite the real prop (umbrella, staff) into the grip in post, or use it as-is for neutral holds
- Robed characters: most hand shots are covered by sleeves — only use when the hand is visible
- If the hand isn't doing something, hide it (pockets, behind back, in sleeves)
- His hands are expressive — he points and beckons a lot (the ring-taunt ref). Favor pointing/beckoning for taunt lines.

### Correction history
- **Fist v1:** generator baked annotation text + borders INTO the artwork ("RIGHT HAND · CLENCHED FIST · REF", skin-tone caption) → regenerated clean with explicit no-text/no-border instructions. Rule learned: always add "NO text, NO labels, NO captions, NO borders, NO frames, NO watermark" to hand prompts.
- **Counting v1:** rendered 2 fingers up instead of 3 → regenerated with explicit "3 fingers UP, 2 digits folded."

---

## TEMPLATE FOR OTHER CHARACTERS

This rig follows the Ashes template. For the remaining characters (Static, Onyx, Theory, Echo, Hollow, Sombra, Kiko):

1. **Collect 10 reference crops** from actual episode frames (mouth/teeth/face)
2. **Document their specific design** — tooth shape, mouth shape, skin tone, variations. Don't assume.
3. **Generate ONE base face, then derive all 10 visemes via mouth-only edits** (the single-base rule — Ashes v2 failure)
4. **Generate 6 eye expressions** in THEIR eye style (visible eyes vs glints vs visor etc.)
5. **Generate hand poses** in THEIR skin tone (verify finger count from frames; add "NO text/labels/borders" to every prompt)
6. **Write a guide like this one** + fill out the model sheet template

**Never reuse Cipher's cards for another character.** Each character gets their own rig.

**The generator's three drift habits (watch for these on every character):**
1. It tries to "calm" the face — neutralize expressions. Lock the signature trait in every prompt.
2. It tries to "clean" unusual mouth colors (dark interiors → pink). Lock the interior explicitly.
3. It tries to "help" by adding annotation text/borders to hand cards. Forbid them explicitly.

**Likeness checklist (applies to every character):**
- [ ] Skin tone matches reference (sampled hex, not eyeballed)
- [ ] Teeth/mouth shape matches reference (not "corrected")
- [ ] No whitewashing, no color drift on lips/skin
- [ ] Style matches show (thick outlines, flat cel shading)
- [ ] All cards visually verified by human eyes before entering the pipeline

---

*Companion: `CIPHER-MODEL-SHEET.md` (design law). Ref pack: `~/workspace/trippedd-studio/production/WIZARD_GANG_EP01/cipher-refs/`. Technique layer: `~/workspace/animation-techniques/ANIMATION-PLAYBOOK.md`.*
