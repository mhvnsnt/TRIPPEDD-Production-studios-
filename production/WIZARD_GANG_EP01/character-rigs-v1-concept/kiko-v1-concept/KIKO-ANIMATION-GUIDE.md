# KIKO TANAKA ANIMATION GUIDE — Full Character Rig

**Character:** Kiko Tanaka (Wizard Gang) — based on older Keiji Mutoh / The Great Muta
**Date:** 2026-10-10
**Rule:** OLDER Muta only. Never the young version, never face paint on the unmasked man.

This is the complete animation rig for Kiko: 10 mouth visemes (all from ONE
pixel-aligned base head shot), 6 eye expressions (mask glint style), 10 hand
poses (mature heavyweight wrestler hands). It follows the Ashes rig pattern.

---

## PART A — MOUTH

### 1. The Actual Design

**Kiko's mouth is the visible lower face below the mask.** The silver/black
segmented mask covers his forehead, eyes, and cheeks — it ends above the upper
lip. What you animate is a mature man's jaw, full lips, and chin: lined,
weathered skin, heavy gray-black stubble, strong square chin.

- **Mouth shape:** Full, mature lips. Not thin, not pouty — a heavyweight's mouth.
- **Teeth:** Natural off-white (#EDE6D6). He has NO grill, NO gold teeth — do
  not add them. Teeth show in Ah, Ee, Oh, F/V, L, Hiss.
- **Interior:** Dark (#2A1A12) — near-black, flat, no detail needed.
- **Stubble rule:** The heavy stubble texture around the mouth is identity, not
  noise. Every viseme preserves it. If a generation smooths the skin, reject it.
- **Size:** The animated mouth region is compact relative to the head — the mask
  owns the top two-thirds. Mouth sits in the lower third, roughly centered.

### 2. The Single-Base Method

All 10 visemes are edits of ONE base head shot (`kiko-head-base.png`):
- Base: front-facing, masked, neutral closed mouth, white fur-trim robe collar.
- Each viseme edited ONLY the mouth region; mask, eyes, stubble, fur trim, and
  background are pixel-identical across the set.
- This guarantees the mouth swaps in animation never jitter the rest of the face.

### 3. Viseme Set (10 — Full Preston Blair)

| Viseme | File | Preston Blair | Description |
|--------|------|---------------|-------------|
| Rest | viseme-rest.png | Rest / X | Relaxed closed mouth, calm neutral line |
| Ah | viseme-ah.png | A / I | Jaw dropped, open oval, teeth + dark interior |
| Oh | viseme-oh.png | O | Rounded small oval ring, lips slightly pursed |
| Ee | viseme-ee.png | E | Wide toothy grin, lips pulled tight |
| Oo | viseme-oo.png | U | Tight pucker pushed forward, tiny dark gap |
| M/B/P | viseme-mbp.png | M, B, P | Lips pressed firmly in a flat line — NO teeth, NO gap |
| F/V | viseme-fv.png | F, V | Upper front teeth resting on lower lip |
| L | viseme-l.png | L, T, D, N, Th | Slightly open, tongue tip up behind upper teeth |
| Hiss | viseme-hiss.png | S, K, G, Z | Teeth pressed nearly together, tense hiss gap |
| TH | viseme-th.png | (TH) | Tongue tip protruding between the teeth |

**M/B/P is non-negotiable.** Every b, p, m sound in dialogue MUST use the closed
shape. The audience catches a missed lip-closure instantly.

### The Core Principle (Owner's Law)

> "You're supposed to be making the mouths in the different expressions and the
> animations based off of what's there in the scene. Not adding something over
> the scene that's not there."

**Translation:** Animate the mouth that's already in the frame. Don't paste a
foreign mouth onto the scene. The visemes build talking animation FROM his
actual lower face.

---

## PART B — EYES

### Style Decision: MASKED GLINTS

Kiko's eyes are glowing pale-white glints inside the mask's dark eye holes —
there are no visible eyeballs to animate. Emotion is carried through glint
**shape, angle, size, and intensity** (plus the classic sparkle cross-stars).

| Expression | File | Glint description |
|------------|------|-------------------|
| Neutral | eyes-neutral.png | Level symmetrical soft glints, calm resting gaze |
| Blink | eyes-blink.png | Mid-blink: glints compressed to thin faint slits |
| Happy | eyes-happy.png | Warm upturned arcs, brighter golden glow |
| Angry | eyes-angry.png | Sharp blade slivers angled steeply inward-down, harsh glare |
| Sad | eyes-sad.png | Glints drooped downcast, dimmer weary glow |
| Surprised | eyes-surprised.png | Large round bright ovals, hot bright core |

All 6 cards share pixel-identical mask linework: the neutral card is a literal
2x-upscaled crop of the base head shot's eye region, and the 5 expressions are
glint-only edits of it.

### Blink Rules (from the Animation Playbook)
- Blink every 3–5 seconds during dialogue
- **Always blink on head turns** — hides the transition
- Blink on stressed/emphasized words for punch
- Full blink = 2–3 frames at 30fps
- For glints: blink = shrink/fade for 2 frames, then return

### Acting Notes — The Dramatic Performer
Kiko is the theatrical one. His glints do the acting because the mask never
moves:
- **Angry glints + rest mouth** = simmering threat. Hold it — he doesn't yell first.
- **Surprised glints + oh viseme** = his signature emotional beat.
- **Sad glints, dimmed** = the misty-dock-scene register. Dim the glow; don't
  change the shape much.
- Happy is rare and reads huge — upturned golden arcs are a reward beat, use
  sparingly.

---

## PART C — HANDS

### Finger Count: 5 digits (4 fingers + thumb)
Verified by eye on every card. No extra or missing digits anywhere.

### Skin Tone: weathered tan, numerically verified
Lit skin **#D2A076** (mid #BA8E6D, shadow #896441). All cards match the face
tone — never lightened. Small healed scars and prominent knuckles are character
detail; keep them.

### The 10 Poses

| Pose | File | Use for |
|------|------|---------|
| Open palm | hand-open-palm.png | Gesturing, presenting, stopping |
| Fist | hand-fist.png | Emphasis, anger, impact stance |
| Pointing | hand-pointing.png | Directing attention, accusation |
| Gripping | hand-gripping.png | Holding staff, handles, ledges |
| Thumbs up | hand-thumbs-up.png | Approval |
| Relaxed | hand-relaxed.png | Idle, hanging at side |
| Counting | hand-counting.png | Three fingers — numbers, listing |
| Beckoning | hand-beckoning.png | "Come here" — hooked index |
| Holding | hand-holding.png | Thumb+index empty pinch — composite prop in post |
| Shaka | hand-shaka.png | Hang-loose, casual greeting |

### How to Use
- Mirror horizontally for the left hand — do not generate separate left-hand cards
- Robed scenes: hands are often covered by sleeves — only use when visible
- If the hand isn't doing something, hide it (behind back, in robe)
- **hand-holding.png** is an empty pinch — composite the prop into the pinch in post

---

## PART D — ANIMATION NOTES: THE DRAMATIC THEATRICAL PERFORMER

Kiko moves like the legend he's based on — slow, deliberate, theatrical.
Nothing he does is casual.

### Movement Language
- **Slow reveals.** He turns to camera slowly; the mask does the work. Let the
  glints shift expression on the turn (blink on the turn to hide the swap).
- **Held poses.** He holds a gesture 4–8 frames longer than the other members.
  The fist, the pointing finger, the open palm presented outward — these are
  tableau beats, not quick motions.
- **The mist.** In atmospheric scenes (dock, fog, night), animate him emerging
  — slow push-in, glints brightening through the dark before the mask reads.
- **Emotional register.** He's the emotional performer of the gang: sad-dimmed
  glints, surprised-oh, the rare happy arcs. Let him feel things on screen —
  the others play it cool; Kiko plays it big.
- **Weight.** He's the heavyweight. His steps land. His gestures have mass.
  Never animate him quick, twitchy, or light.

### Voice Sync
- Mouth visemes are small relative to the head — the lower face does the
  talking, but the EYES sell the line. Match glint expression to the dialogue
  emotion first, mouth shape second.
- His delivery is slow and measured: hold Ah and Oh shapes a beat longer than
  the audio technically needs. It reads as gravitas, not lag.

---

## WHAT NOT TO DO

- **NEVER the young Muta.** Any generation that drifts young, smooth-skinned, or
  lean is rejected — no exceptions, ever.
- **NO face paint on the unmasked man.** The older Mutoh is unpainted. Paint is
  a banned drift.
- **Do NOT smooth the stubble.** AI will try to clean up the weathered skin —
  that erases his age and breaks likeness. Stubble texture is sacred.
- **Do NOT change the mask design.** Silver/black segmented, ridge segments,
  flame patterns — identical in every shot. Mask drift is a defect.
- **Do NOT draw the mask over the mouth.** The mask ends above the upper lip;
  the animated region is the lower face.
- **Do NOT give him gold teeth or a grill.** His teeth are natural.
- **Do NOT animate him like a young athlete.** No quick twitchy motion, no
  light-footed bounce. He is a slow, heavy, dramatic presence.
- **No photorealism, no Disney 3D.** Thick black outlines, flat cel shading —
  the show's 2D look, always.
- **No labels or text on animation cards.** (The first relaxed-hand base had
  annotation text and was regenerated clean — keep them clean.)

---

*Companion: `KIKO-MODEL-SHEET.md` (likeness law, color model, proportions).
Pattern source: `~/workspace/ashes-mouth-pack/`. Playbook:
`~/workspace/animation-techniques/ANIMATION-PLAYBOOK.md`.*
