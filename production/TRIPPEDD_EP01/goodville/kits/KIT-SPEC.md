# PRESTON BLAIR KIT SPEC — Goodville Cartoon character kits

**Status:** THE spec for every Goodville character kit. Owner directive 2026-10-11.
**Authority:** `docs/research/SOUTH-PARK-STUDY.md` §§3–4, 8B–8C (character formula,
stepped grammar, geometric kit) + the Character Construction Doctrine in
`production/TRIPPEDD_EP01/reference/goodville/goodville-environment.md`
(South Park grammar + Preston Blair whole-character construction).

A "kit" is a complete set of separate character pieces in flat South Park cutout
style — the way Preston Blair's model sheets break a character into constructible
parts, and the way South Park builds every character from a rigid geometric kit.
Build the kit ONCE per character; every shot, promo, and episode reuses it.

---

## TWO-TIER WORKFLOW (owner's law, 2026-10-11)

- **Tier A — AI-generated promotional art.** Exists (the key art). It's "okay."
  Its job: the **LIKENESS TARGET**. Nothing more.
- **Tier B — hand-built Preston Blair kit characters.** NEVER AI-generated.
  These are the **PRODUCTION ASSETS** — what actually appears on screen.

The job is to drill Tier B until it's as close as possible to the Tier A
likeness. Every kit ships with a **likeness-drill log** (`drill-log.md`):
side-by-side notes vs the promo art, what was iterated, what's still off —
honestly, in the owner's own words where he gives them.

---

## Piece inventory (per character)

Every piece: transparent-background PNG, flat South Park cutout style
(flat fills, minimal/no outlines on bodies per the study), colors
eyedropper-sampled from the key art — never guessed. Naming:
`kits/<character>/<part>_<variant>.png`.

### HEAD
| Piece | Variants | Notes |
|---|---|---|
| `head_base.png` | 1 | Circle head, skin flat. The foundation everything registers to. |
| `hair.png` | 1 (+`_back` if layered) | Hair as a shape arranged BEHIND the head (study §3). Separate piece — it moves independently on head turns. |
| `hat.png` / accessory | 1+ | Hats/accessories are ALWAYS separate — **hat = identity** (study §3). Remove the hat and the character must become unreadable; that's the test. |

### FACE
| Piece | Variants | Notes |
|---|---|---|
| `eyes_open.png` | neutral | Two white ovals side by side (study §3). |
| `eyes_closed.png` | blink | Lids, for the mandatory blink-before-speak. |
| `eyes_angry.png`, `eyes_sad.png`, `eyes_shocked.png`, `eyes_scheming.png` | emotion set | Eyebrows appear only on expression for kids (study §3); adults keep brows. |
| `pupils.png` | neutral + `_left`, `_right`, `_up` | Small black dots, separate so look-direction animates without redrawing eyes. |
| `brows.png` | neutral/angry/sad | Adults: always present. Kids: expression-only. |
| `nose.png` | 1 (adults) | Optional per study §3 — adults get noses, kids usually don't. |
| `facial_hair.png` | 1 | Mustache/goatee/etc. as its own piece where applicable (Amos Jr.). |
| `mouth_closed.png` | line | The small black line. |
| `mouth_open_small.png`, `mouth_open_med.png` | — | Replacement shapes, not phonemes (study §4). |
| `mouth_open_wide.png` | shout | Opens to a cavern (study §3). |
| `mouth_o.png` | O-shape | Surprise / "oh". |
| `mouth_grimace.png` | teeth | Anger / effort. |
| `mouth_smile.png` | — | Where the character smiles. |
| `mouth_canadian_flap.png` | where applicable | South Park Canadian-style split flap mouth (owner-approved for the old head 2026-10-11: "Lahey is Canadian, Trailer Park Boys is Canadian, it's perfect"). Top/bottom flaps that bounce on dialogue. |

Mouth rule: 6–8 replacement shapes per character, swapped stop-motion style
against the voice track (study §8C). Blink-before-speak on every line.

### BODY
| Piece | Variants | Notes |
|---|---|---|
| `torso_base.png` | 1 | Simple-shape body, one flat shirt color (study §8B). |
| `torso_<variant>.png` | as needed | Clothing variants (jacket on/off, etc.). |
| `arm_straight_L/R.png` | rest | At the side. |
| `arm_bent_L/R.png` | — | Elbow bent (holding, gesturing). |
| `arm_punch_L/R.png` | extended | Punch/point poses. Built SP-style when the key art lacks them. |
| `arm_folded.png` | signature poses | E.g. Amos Jr.'s beer-holding fold — the key-art pose, extracted not invented. |
| `hand_mitten_L/R.png` | open | Circles for hands, smaller circles for thumbs (study §3). |
| `hand_fist_L/R.png` | — | Punching / effort. |
| `hand_point_L/R.png` | — | Fingers "appear" only when the scene needs them (study §3). |
| `hand_grip_<prop>_L/R.png` | per prop | Prop-specific grips — e.g. fist gripping the BEER can. The grip and the prop are separate pieces that composite together. |
| `legs_stand.png` | 1 | Rectangle legs (study §8B). |
| `legs_walk_01..06.png` | walk cycle | The stiff side-to-side shuffle, 6 stepped poses, built once and reused (study §8C). |
| `legs_sit.png` | 1 | Seated. |
| `feet_L/R.png` | 1 | Shoes as circles cut in half (study §8B). |

### PROPS
| Piece | Notes |
|---|---|
| `prop_<name>.png` | Signature props, separate pieces: Amos Jr.'s BEER can, red cap guy's bottle, glasses guy's bong, etc. Props are identity anchors — extract from key art, never redraw from memory. |

### Kit completeness checklist
A kit is DONE when it holds: head base, hair, hat/accessory separate,
eye set (open/closed + 4 emotions), pupils (4 directions), brows, nose (adults),
facial hair (where applicable), full 6–8 mouth set (+ Canadian flap where
applicable), torso + clothing variants, 4 arm poses per side, 4 hand types per
side (+ prop grips), legs (stand/walk 6/sit), feet, all signature props,
`manifest.json`, and `drill-log.md`.

---

## manifest.json format

```json
{
  "character": "amos-jr",
  "source": "assets/references/ep01/source/Goodville - Not South Park.png",
  "tier": "B",
  "identity_checklist": ["shaggy brown hair", "mustache + chin goatee",
    "white tank top", "arm tattoo", "BEER can"],
  "parts": [
    {"file": "head_base.png", "method": "extracted|hand-built|donor",
     "anchor": {"x": 0, "y": 0, "w": 0, "h": 0},
     "notes": "key-art bbox this piece was taken/measured from"}
  ]
}
```

- `method`: **extracted** (smart-extract from key art), **hand-built**
  (drawn in SP style, colors sampled), **donor** (copied from a verified part).
- `anchor`: the key-art bbox measurement the piece registers to.
- `identity_checklist`: the anchors that make this character THIS character —
  every one must read on the relevant pieces, checked by eye.

## drill-log.md format

```markdown
# Likeness drill log — <character>
## vs Tier A promo art
- <what matches>
- <what's off, honestly>
## Iterations
- <date>: <what changed and why>
## Still off
- <open items>
```

## Build discipline (non-negotiable)

1. **Extract with tools/smart-extract/** (sense → trace → cut → verify loop).
   NEVER flood-fill. NEVER eyeball a crop.
2. **Hand-build what's missing** in flat SP cutout style; colors sampled from
   the key art, never guessed.
3. **Read every PNG with your own eyes.** Automated checks catch specks;
   eyes catch likeness.
4. **No invented design.** Visual design only — the key art is the model sheet.
   (Amos Sr. has no visual reference: his kit waits for the owner's eye.
   Don't guess the face.)
5. **Position from measurement.** Part placement derives from key-art
   anchors in the manifest, never eyeballed.
6. **BODY INTEGRITY.** Every character's body must be WHOLE in every frame.
   Check for missing chunks and background showing through where body should
   be — not just added artifacts. Zoom crops of the torso region on every
   character, every beat, before anything ships. (Owner 2026-10-11: a
   rectangular chunk of Amos's torso shipped missing because checks looked
   for junk, not holes.)
7. **No rectangular/square limbs.** All arms/legs taper with rounded ends —
   SP cutout grammar. A uniform bar with 90° corners is never a limb.
   (Owner 2026-10-11: "big square cropped out of Amos Jr.")
8. **NO SQUARE CUTS ON PIECES (owner 2026-10-11).** Every kit piece edge that
   joins another piece is shaped to fit its neighbor — curved, rounded, never
   a straight cut. If a piece was cropped with a straight edge (polygon mask,
   rectangular crop), reshape the edge into a smooth contour before it ships.
   Applies to every character, every piece, no exceptions.

## Mirror-reconstruction (standing technique, owner 2026-10-11)

When one side of a body part is intact and the other is damaged/missing,
**mirror the good half across the centerline** — don't hand-guess the missing
half. (Owner's fix for Amos's half-torso: mirror the intact right half to
rebuild the full Preston Blair torso, reconnect the waistband with no gap.)

**SYMMETRY GATE (owner refinement 2026-10-11) — mirror ONLY when the part is
actually symmetric:**
1. **CHECK symmetry first.** Compare the halves: pose, clothing folds, facial
   features, accessories. Torso and legs are usually safe; most of South Park's
   stuff is pretty symmetrical — which makes most of it easy to build on and
   repair and add to.
2. **Mirror only if symmetric.** Hands/arms in different poses, asymmetric
   eyes, asymmetric clothing details (a tattoo on one side, a pocket, a fold
   pattern that doesn't repeat) → do NOT mirror; hand-build instead.
3. **Verify the seam is invisible.** After mirroring, read the result with your
   own eyes: the centerline seam must disappear. If it doesn't, the part
   wasn't symmetric enough — hand-build it.

Head stays original unless the face is verified symmetric (hair is usually
asymmetric). Remove mirrored limbs that would double with rigged parts (tight
mask, not a big polygon).

**Manifest fields for every mirrored piece** (in addition to the standard fields):
```json
{"file": "torso_mirrored_punch.png", "method": "mirrored",
 "mirrored_from": "right half (intact)",
 "symmetry_verified": true,
 "symmetry_notes": "plain white tank, no asymmetric details on source half"}
```
- `symmetry_verified: false` → the piece was NOT mirrored; see notes for the
  hand-built alternative.
