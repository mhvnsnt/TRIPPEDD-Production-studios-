# RIG DISSECTION — how the pro rigs are actually built

**Lane:** WG V2 put-it-to-use, 2026-10-29 · **Owner law applied:** USE-PRO-PRODUCTION-FILES-100%
(build FROM their rigs / backgrounds / movements / sheet packs / camera structure;
excluded: their characters, names, logos, verbatim lines).
**Method:** `.fla` = ZIP of XFL XML → extracted and parsed (Animate writes a non-standard
central directory, so entries were walked by local file header — sizes below are the real
parsed structures, not filenames guessed from a listing). Gumball files are CS3-era binary
`.fla` (OLE2 compound), dissected by UTF-16 string/structure extraction + 7z stream listing.
Dissected files are kept beside this doc in `smiling/` and `gumball/`.

---

## 1. Smiling Friends — Charlie (`SmileFriends.Charlie.fla`, 82,390 B)

Source: `mhvnsnt/cn-gigaleak-cartoon-vault`, release `tv-gigaleak-fla-v1`. Format: Adobe
Animate 22.0 XFL, stage **1920×1080**. The stage itself holds ONE layer named after the
character with ONE instance of the master symbol — the whole character is a single nested
symbol; scenes just drop it in.

### Master symbol `Charlie` — 9 layers (top → bottom as authored)
| Layer | Holds |
|---|---|
| front_arm | Front Arm symbol |
| body_move | Torso Move symbol (a dedicated torso-motion helper) |
| body_mask | mask layer for the body |
| body_thingies | small attachments/details |
| body | Body symbol |
| head | Head symbol |
| body_back | back-of-body drawing (sits behind head, in front of legs) |
| legs | Legs symbol |
| back_arm | Back Arm symbol |

### Head symbol `Charlie Head` — 8 layers, 10 nested symbols
| Layer | Nested symbol | Symbol's own frame count |
|---|---|---|
| rbrow / lbrow | Right Brow / Left Brow | **3 frames each** (3 brow states) |
| lpupil / rpupil | Left Pupil / Right Pupil | 1 drawing each — pupils are SEPARATE symbols so look direction is keyed independently |
| mouth | Mouth | **25 frames** |
| face_scalp | Face Scalp | 1 (the face plate everything sits on) |
| hat | Hat | 1 |
| pubes | Pube 1 / 2 / 3 | 1 each (detail bits as their own symbols) |

### Part-symbol frame counts (the swap libraries)
| Symbol | Frames | Reading |
|---|---|---|
| **Mouth** | **25 keyframes, 1 layer, no labels** | The mouth-switch set: 25 drawings addressed by frame number only |
| Legs | 10 keyframes | gait/pose swap set |
| Back Arm | 3 | arm pose swaps |
| Front Arm | 2 | arm pose swaps |
| Brows L/R | 3 each | expression states |
| Body, Hat, Scalp, Pupils | 1 | static plates |

**Construction rules read off Charlie:** (1) one master symbol per character; (2) head is a
sub-symbol with its own layer stack; (3) every feature that moves on its own (pupils, brows,
mouth) is its own symbol on its own layer; (4) mouths are a frame-addressed drawing library
inside ONE symbol, no fancy naming; (5) masks are real layers in the master (body_mask).

## 2. Smiling Friends — Pim (`SmileFriends.PimRigUpdate.fla`, 296,483 B)

Same release, Animate XFL, stage 1920×1080, stage = one layer / one master instance.
Library is foldered: all parts live under `PimAssets/`.

### Master symbol `Pim` — 5 layers
`head, Larm, body, legs, Rarm` (note: plain side names, no L/R upper/lower split —
arms are single symbols with pose frames).

### Head symbol `Pim Head` — 15 layers (the most detailed head in the set)
| Layer(s) | What it proves |
|---|---|
| LpupilPARENT / RpupilPARENT | pupils sit inside a **PARENT symbol** — a positioning wrapper, so pupil travel is animated on the parent and the pupil drawing itself stays untouched |
| LeyeMASK / ReyeMASK | dedicated **mask layers** clip the pupils to the eye shape |
| pupilL / pupilR | pupil symbols: **3 frames each** |
| eyeL / eyeR | eye white/shape symbols, 1 drawing |
| lidL / lidR | lid symbols: **3 frames each** (open / half / closed blink set) |
| mouth | Mouth symbol (below) |
| scalp | Scalp, 2 frames |
| dingle | the exposed-nerve detail is its own symbol (`Pim Exposed Nerve`) on its own layer |

### Part-symbol frame counts
| Symbol | Frames | Labels |
|---|---|---|
| **Mouth** (layer literally named `mouths`) | **28 keyframes** | 1 label: `bonus` (extra/exceptional shapes parked after the main set) |
| Legs (layer `legs`) | 11 keyframes | **`standing`, `walk start`, `walk end`** — cycle segments are LABELLED inside the symbol |
| Front Arm / Back Hand | 6 each | pose/hand swap sets |
| Lids L/R | 3 each | blink states |
| Pupils L/R | 3 each | |
| Body | 2 layers (`fatbaby`, `shirt`) | body itself split into mass + clothing |

**Construction rules added by Pim:** (6) wrap pupils in parent symbols and clip them with
eye masks instead of redrawing eyes; (7) blinks are a 3-drawing lid set per eye, not a
squash; (8) label cycle segments inside the leg symbol; (9) keep a `bonus` overflow area at
the end of the mouth set for one-off shapes.

## 3. Gumball — master puppets (CS3 binary `.fla`, OLE2)

Source: `mhvnsnt/cn-gigaleak-gumball`, release `untagged-1676e192ae8c72e95791`
(`Gumball_S2_Rigs.zip`, 685,983,662 B, 132 entries, 62 `.fla`). Two puppets were pulled by
ZIP range-request on the central directory (no full download) and dissected:

| File | Size (uncompressed) | What it is |
|---|---|---|
| `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_001_CS3.fla` | 2,736,640 B | the lead character's **original master puppet** |
| `GB200_HECTOR_ORIGINAL_PUPPET_V001_CS3.fla` | 1,512,448 B | a second character's original puppet, same system |

### Naming system (this is the real template value)
`GB<season/ep block>_<CHARCODE>_<VIEW>_<PART>` — e.g. `GB200_GB_FRONTVIEW_HEADCOMP`,
`GB200_HECTOR3.4BACK_FOOT_L`, `GB200_HECTORFRONT_HAND_L`.
- **View packs:** each puppet ships as full **view sets** — `FRONT`, `FRONTVIEW`,
  `3.4BACK` (three-quarter back), `BACK`, `BACKVIEW`, plus pose states (`Flopped_`).
  A character is not one rig; it is one rig PER VIEW, in versioned folders (`…_V001/`).
- **COMP suffix = nested composition:** `HEADCOMP`, `BODYCOMP`, `EYESCOMP` — head/body/eyes
  are comps containing their own sub-parts (`GB200_GB_HEADCOMP/GB200_GB_EAR`,
  `…/GB200_GB_STD_MOUTH`, `GB200_GB_L_ARM`, `GB200_GB_L_LEG`, `GB200_GB_TAIL`…).

### Mouth + eye libraries (documented INSIDE the files)
The puppets carry their own doc strings, verbatim categories:
- "* Mouth shapes for lipsynch." / "* Mouth shapes that can be used for lipsynch and hold poses."
- "* Mouth shapes for head with a big cheek." — mouth sets are **per head-shape variant**
  (`GB200_GB_STD_MOUTH` for the standard head, `Big Cheek head_Mouth Open/Closed`, `_Eating_Mouth_01`, `MOUTH_HOLD_POSE`, `frontview_mouth` per view).
- "* Eyes shapes for standard head." / "* Eyes shapes for Extreme Expressions, for head with a bigger cheek."
- Eye expression library as named symbols: `ANGRY_EYES_01`, `CLOSED_EYES`,
  `CLOSED_EYES_ANGRY_HOLD_01`, `CLOSED_EYES_DESPERATE_03`, `CRYING_EYES_01`, `CUTE_EYES_01`,
  `EYES_CLOSED_SQUASH_01`, `EXT_EYES_HAPPY_01` (EXT = extreme-expression set), and pupils are
  again separate: `CLEAN_PUPILS`.

**Construction rules added by Gumball:** (10) name everything
`SHOW_CHAR_VIEW_PART`, version every puppet folder; (11) build per-view rig packs, not one
universal rig; (12) mouths AND eyes are expression LIBRARIES (named, numbered, with hold
poses), organized per head variant; (13) keep pupils as a standalone clean symbol;
(14) write the usage notes inside the rig file itself.

## 4. Frankie Foster rig — NOT re-downloaded (other lane owns its parse)

Published facts only: puppet rig `.fla`, **18,385,408 B**, draft release `frankie-rig-fla-v1`
in `mhvnsnt/cn-gigaleak-fosters-home` (loose asset, originally `pds3hx.fla`), plus a
90,993,866 B Foster's Flash sources zip (`fosters-flash-v1`) in the same repo. Its full
layer/part parse lands with the FlashXFLParser tool-proof lane; the WG template below does
not depend on it.

## 5. Cross-rig patterns → what WG copies (structure, not art)

1. One master character symbol; the scene holds a single instance of it.
2. Head is a nested sub-rig: face plate, mouth level, pupils (parented + masked),
   eye shapes, lids (3-state), brows/expression layer, headwear/accessory levels.
3. Mouth = ONE symbol/level holding a frame-addressed drawing library:
   **pros use 25 (Charlie) and 28 (Pim) drawings**; core phonemes first, `bonus` tail.
4. Eyes are a library too — expression sets with numbered variants + hold poses;
   pupils always separate.
5. Limbs are pose-swap symbols (2–6 frames), legs carry labelled cycle segments.
6. Characters ship as per-view packs with strict `SHOW_CHAR_VIEW_PART` naming and
   versioned folders.
7. Masks are first-class layers (body mask, eye masks), not afterthoughts.
