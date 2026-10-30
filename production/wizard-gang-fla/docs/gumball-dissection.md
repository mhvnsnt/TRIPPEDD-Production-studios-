# GUMBALL .fla DISSECTION — one master puppet + one episode scene

**Lane:** FLA puppets program, 2026-10-30 · **Purpose:** dissection notes for an FLA production standard.
**Companion to:** `docs/wizard-gang/RIG-DISSECTION.md` §3 (prior lane, CS3-era Gumball puppets 001/Hector,
dissected by OLE2 string extraction). This lane supersedes §3 where the two disagree on format:
the later puppet revision and the scene files are **XFL, fully parsed** (see Method).

**Evidence tags used throughout:**
- **[PARSED]** — read out of the XFL XML DOM (`DOMDocument.xml` / per-symbol `LIBRARY/*.xml`):
  stage size, fps, layer stacks, keyframe indices/durations, frame labels, instance matrices,
  transformation points, loop/firstFrame settings, media items. These are structural facts.
- **[IN-FILE TEXT]** — authored prose inside the files (`DOMStaticText` on NOTES/guide layers),
  extracted from the XML and quoted verbatim (spelling as authored). Also parsed, but it is
  *documentation the crew wrote*, not structure — kept separate for that reason.
- **[DERIVED]** — a standard/rule inferred from the parsed facts, for our own FLA standard.

---

## 0. Method + source inventory (no whole-archive downloads)

Source repo: `mhvnsnt/cn-gigaleak-gumball`, draft release `untagged-1676e192ae8c72e95791`
("Gumball S2 Rigs — gigaleak pull v1"). Two assets on that release:

| Asset | Size | Contents |
|---|---|---|
| `Gumball_S2_Rigs.zip` (asset 641213637) | 685,983,662 B | 132 entries, **62 .fla** |
| `CN-Leaks-001-gumball.zip` (asset 640772406) | 1,709,550,213 B | 876 entries, 71 .fla total |

Range-request tooling (`vzip.py`, central-directory read only) was used for both inventories;
only the two entries dissected below were extracted. Full central directories are kept at
`gumball/s2rigs-central-directory.txt` and `gumball/cnleaks001-central-directory.txt`.

**Inventory findings [PARSED from central directories]:**
- The "S2 Rigs" zip is misnamed by its own contents: of its 62 .fla, **40 are episode scene /
  special-pose files** (`Sc###`, `_REMOTE_`, `_Clean_`, `KeyAnim`, `SC###_FINAL` patterns) and
  only ~15 are `ORIGINAL_PUPPET` files. A scene file therefore exists in this zip — no fallback
  to a second puppet was needed.
- `CN-Leaks-001-gumball.zip` contains a nested `Cartoon Network Leaks/Gumball S2 Rigs/` folder
  holding the **same S2 set** (the two files below appear there with identical uncompressed
  sizes) plus other shows' material. It adds no Gumball scene the S2 zip lacks.
- Scene files present in the S2 zip include (selection): `GB202REMOTE_Sc094_Clean_V023_STN.fla`,
  `GB202REMOTE_Sc103_V0024_cleanup_LW.fla` (34,013,120 B), `GB202REMOTE_Sc108_Clean_V001_STN.fla`,
  `GB202REMOTE_Sc144_KeyAnim_V050_clean_MS.fla`, `GB202REMOTE_Sc160_CLean_V003_jf.fla`,
  `GB211TREASURE_Sc105_V013_clean_GD.fla`, `GB214WORDS_Sc054…Sc099` (9 scenes),
  `GB218Flakers_Sc117_KeyAnim_V007.fla` (51,767,121 B),
  `GB222Bumpkin_Sc090_KeyAnim_V012.fla` (81,421,346 B — largest .fla in the zip).

**Files dissected (kept in `gumball/` beside this doc, with full XFL extractions in
`<name>_xfl/` and machine-readable parses in `*-parsed.json`):**

| # | File | Uncompressed size | SHA-256 | Source entry |
|---|---|---|---|---|
| 1 | `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla` | 1,740,533 B | `fb30f003a3ce91928240a1d7b7ba2dd2023dac710c73527b5d149ab9d3ac6bd4` | `Gumball_S2_Rigs.zip` |
| 2 | `GB202REMOTE_Sc094_Clean_V023_STN.fla` | 22,851,853 B | `15606f522c60946abe61621200150bfccb8871bbf6775471760c7e7724f03786` | `Gumball_S2_Rigs.zip` |

Both are **ZIP-based XFL** (first bytes `PK\x03\x04`), not OLE2. Animate/Flash writes a
non-standard central directory, so extraction walked local file headers (same approach as the
prior lane's Smiling Friends parse). Empty placeholder entries (`.xfl` stubs, 9 B;
`MobileSettings.xml`, 0 B) terminate the walk harmlessly.
Internal stub names are evidence in themselves: the puppet file still contains
`GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_003.xfl` / `…_003a.xfl` stubs next to the `…_008.xfl`
stub (the file was saved-forward from the v003 lineage), and the scene file contains the
crew's template stub `GB2XXNAMEOFTHESHOW_ScXXX_KeyAnim_V000.xfl` — the naming template itself,
shipped inside a production scene.

---

## 1. PUPPET — `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`

### 1.1 Identity / format [PARSED]

| Fact | Value |
|---|---|
| Format | XFL 2.1 in ZIP `.fla` |
| Authoring app | Adobe Flash Professional **CS5.5**, Windows, "Saved by Adobe Flash Windows 11.5 build 349" |
| Stage | **2730 × 1625 px**, background `#F6F6F6`, grid 18×18, guides colour `#00FF00` |
| Frame rate | **25 fps** |
| Main timeline | `Scene 1`, **162 frames**, 7 layers (see §1.2) |
| Library | **61 symbols** (`<Include>` count = parsed symbol files = 61), 12 library folders, 1 bitmap |
| Only bitmap | `REF/TEMPLATE/GB_Asset-container_Final` (lossless PNG, source path on a crew desktop: `…/Desktop/PUPPETS/FINAL_PUPPETS_ON_SERVER/GB_Asset-container_Final.png`) |
| Camera | **None.** Zero `camera` elements — CS5.5 predates the Animate camera tool. |
| ActionScript | None found on any main-timeline frame. |

**Format correction to the prior lane:** VERSION_001_CS3 is OLE2 binary; **VERSION_008 is
CS5.5 XFL**. The puppet line crossed formats between revisions — 004/006/008 (and the Darwin
`_CS5` sibling in the same zip) are the XFL generation, 001/Hector are the CS3 generation.
Any tooling built for these puppets must handle both.

### 1.2 The puppet file is an ASSET-CONTAINER stage, not a scene [PARSED]

The 2730×1625 stage exists to lay the whole puppet out on one sheet. Main timeline, 162 frames,
every content layer holding exactly **one keyframe at frame 0 with duration 162**:

| Layer (top→bottom as authored) | Instance placed | Matrix tx, ty | Scale | Loop |
|---|---|---|---|---|
| `GB200_GUMBALL_BACKVIEW_ORIGINAL_PUPPET_v001` | `…BACKVIEW_v001/GB200_GUMBALL_ORIGINAL_PUPPET_BACKVIEW_v001` | 1267.6, 856.45 | 1.0 | loop |
| `GB200_GUMBALL_FLOPPED_ORIGINAL_PUPPET_v001` | `…FLOPPED_v001/GB200_GUMBALL_FLOPPED_ORIGINAL_PUPPET_v001` | 1170.3, 679.75 | 1.0 | loop |
| `GB200_GUMBALL_PUPPET_STD_001` | `…V001/GB200_GUMBALL_PUPPET_001` | 703.6, 971.4 | 0.9987 | play once |
| `GB200_GUMBALL_FRONTVIEW_ORIGINAL_PUPPET_v001` | `…FRONTVIEW_v001/GB200_ORIGINAL_PUPPET_FRONTVIEW_v001` **plus** a second instance: `GB200_GB_MOUTH`, `loop="single frame"`, `firstFrame="112"`, rotated (a=−d≈0.988, b=−0.152, c=+0.152) at 1327.3, 793.6 | 1086.25, 1017.2 | 0.9991 | loop |
| `REF` (folder, locked) → `LINES` (locked) | `REF/TEMPLATE/LINES` | 223.45, 699.5 | 1.0 | loop |
| `REF` (folder, locked) → `FRAME` (locked) | `REF/TEMPLATE/GB200_ASSETT_CONTAINER` | 0.35, 16.65 | 1.0 | loop |

So one .fla ships **four complete view rigs side by side** — standard 3/4 (`STD`), `FRONTVIEW`,
`BACKVIEW`, `FLOPPED` (the mirrored 3/4) — framed by a locked template (`FRAME` = the
asset-container artwork, `LINES` = registration/line overlay). The stray mouth instance pinned
to `firstFrame 112` on the FRONTVIEW layer is a working leftover/specimen, not part of any rig.

### 1.3 View-pack structure [PARSED]

Library folders mirror the views, each versioned `…_v001/`:
`GB200_GB_ORIGINAL_PUPPET_V001/` (STD), `…_FRONTVIEW_v001/`, `…_BACKVIEW_v001/`, `…_FLOPPED_v001/`,
plus `PROPS/`, `REF/`, `REF/TEMPLATE/`, `REF/EXTRAS/TWEEN_FOR_BLINK_and_eating_cycle/`.

Master symbol layer stacks (each master is a **1-frame** graphic symbol; animation lives in
the pose addressing, §1.4):

**STD master `GB200_GUMBALL_PUPPET_001`** — the pose-library master, **95 frames**, 15 layers
(§1.4). Its parts (frame counts = the swap-library sizes):

| Part symbol | Frames | Layers inside | Notes |
|---|---|---|---|
| `GB200_GB_HEADCOMP` | **309** | 13 (see §1.5) | head composition |
| `GB200_GB_BODYCOMP` | 11 | `BODY` (11 kf), `NOTES` (guide, locked) | 11 body shapes |
| `GB200_GB_L_ARM` | 90 | `LABELS` (14 kf), `ARM` (24 kf), `PROPS` (11 kf), `NOTES` | incl. a `PROPS/SANDWICH` instance at f28 |
| `GB200_GB_R_ARM` | 89 | `LABELS_ARMS` (15 kf), `PROPS` (5 kf), `ARM` (26 kf), `NOTES` | |
| `GB200_GB_L_LEG` / `GB200_GB_R_LEG` | 10 / 10 | leg layer (10 kf), `NOTES` | |
| `GB200_GB_TAIL` | 7 | 1 layer, 7 kf | |

**FRONTVIEW master `GB200_ORIGINAL_PUPPET_FRONTVIEW_v001`** — 1 frame, 10 layers:
`HIDE_NECK`, `GB_frontview_Head_comp`, `GB_L_ARM_FRONT`, `GB_R_ARM_FRONT`, `GB_Frontview_body`,
`GB_Frontview_L_ARM`, `GB_frontview_R_arm`, `GB_frontview_R_Leg`, `GB_frontview_L_leg`,
`GB_frontview_Tail`. Front-view arms are split into a behind-body arm symbol **and** a separate
`*_ARMFRONT` symbol per side (L/R_ARMFRONT) — the front sliver of the arm is its own part so the
body can sit between the two. Its HEADCOMP has 4 layers: `GB_Frontview_Eyes`, `GB_Frontview_mouth`,
`GB_Frontview_Head`, `GB_Frontview_ears` — and its mouth/eyes are **single drawings** (1 kf each):
the front view ships without the STD view's expression libraries.

**BACKVIEW master** — 1 frame, 8 layers: `HIDE_NECK`, `GB_backview_headcomp`, `GB_backview_r_arm`,
`GB_Backview_tail`, `GB_backview_body`, `GB_backview_R_Leg`, `GB_backview_L_leg`,
`GB_backview_l_arm`. Its HEADCOMP is 4 shape layers (`Front_Ear`, `Whiskers`, `Gb_backview_head`,
`Back_Ear`) — no mouth, no eyes, as expected for a back view.

**FLOPPED master** — 1 frame, 9 layers, mirroring STD's stack incl. its own HEAD_COMP
(`GB_Flopped_Mouth`, `GB_Flopped_Eyes`, `GB_Floped_head` [sic], ears) — a separately drawn
mirrored rig, **not** a −1 scale instance of the STD rig.

Recurring device in every master: a **`HIDE_NECK` layer** — a neck-occluder shape layer whose
whole job is hiding the neck joint under the head.

### 1.4 How a pose is addressed: labelled pose library + `single frame`/`firstFrame` [PARSED]

The STD master is not animated by tweens. It is a **95-frame pose library**: a locked-style
label track `POSES_LABELS` names each pose block, and every part layer holds graphic instances
of the part symbols with `loop="single frame"` and a `firstFrame` pointing into that part's
own swap library. 154 instances total in the master
(HEADCOMP ×22 [19 single-frame + 3 play-once], L_LEG ×29, R_ARM ×29, L_ARM ×27, BODYCOMP ×16,
R_LEG ×16, TAIL ×15).

Pose label map (`POSES_LABELS`, frame index → label):

| @ | Label | @ | Label |
|---|---|---|---|
| 0 | `GB002_STD_STAND_UP` [sic — 002] | 56 | `GB200_EXT_HAPPY` |
| 29 | `GB200_STD_SOFA_SITING_001` | 62 | `GB200_EXT_ANGRY` |
| 38 | `GB200_STD_CHAIR_SITTING_001` | 77 | `GB200_EXT_SUPER_CUTE` |
| 44 | `GB200_STD_SOFA_SITTING_002` | 80 | `GB200__SQUASH` |
| 47 | `GB200_STD_SAD_001` | 83 | `GB200_RUN` |
| 53 | `GB200_STD_BEND_LEGS_001` | 89 | `GB200_WALK` |
| | | 92 | `GB200_SCARED_POSE_V001` |

Registration/pivot evidence (frame-0 pose, `transformationPoint` = the instance pivot):
HEADCOMP instance at tx −271.35, ty −247.15 with transformationPoint **(127.7, 224.45)**;
BODYCOMP tx −162.2, ty −55.6, tp (37.5, 125.15); L_ARM_FRONT tx −103.55, ty −37.4, tp (13, 8.25);
R_ARM tp (9.5, 0.55); L_LEG tp (10.55, 3.35); R_LEG tp (25.5, 4.25); TAIL tp (−15.3, −16.1).
Pivots sit at the **joint** (shoulder/hip/neck), in each part symbol's local coordinates —
the same transformationPoint repeats across every keyframe of that part's layer, so the joint
never drifts between poses.

Arm swap libraries are labelled the same way (`GB200_GB_L_ARM` `LABELS` track, frames 25–34 and
54–55: `STD_HAND_EXPLAINING`, `STD_SHRUG_SHOULDER`, `POINTING_FINGER`, `EATING_ARM`,
`ARMS_ON_TABLE`, `EXT_FORCING_EXPLAINING_HANDS`, `SHOUTING_ARM`, `HAND_ON_TABLE_CHEEK`,
`POINTING_HAND_V002`, `SCARED_HAND`, `FIST_CLOSED_EXTREME_POSE`, `HAPPY_FIST`).

### 1.5 HEADCOMP — the head is a 309-frame expression machine [PARSED]

`GB200_GB_HEADCOMP`: **309 frames**, 13 layers:

| Layer | Type/visibility | Content |
|---|---|---|
| `LABELS_HEAD` | locked | head-state labels (below) |
| `NOTES_FOR_SOI_GUMBALL_PEOPLE` | **guide** | crew notes layer ("SOI" = School of Image / the outsourcing studio) |
| `GB200_GB_STD_MOUTH` | normal | 26 instances of `GB200_GB_MOUTH`, all `loop="single frame"`, addressed by `firstFrame` (e.g. f0 of headcomp → mouth frame 0 held 26 f; then firstFrame 17, 18…) at tx ≈ (91.5, 131.25), tp (40.2, 9) |
| `EYES_COMP_SEPARATED` | **folder, visible=false** | parked separated eye layers (next 5 rows) |
| `EYEBROWNS` [sic] | guide, hidden, child of folder | 54 kf |
| `CLEAN_EYES_LINES` | guide, hidden, child | 48 kf |
| `WHITE_MASK_01` | guide, hidden, child | 48 kf |
| `CLEAN_PUPILS` | guide, hidden, child | 50 kf |
| `WHITE_MASK_02` | guide, hidden, child | 48 kf |
| `GB200_GB_STD_EYESCOMP` | normal | 19 instances of `GB200_GB_EYESCOMP_SYMBOL` — **the eyes as actually used: one comp instance** |
| `GB200_GB_STD_HEAD` | normal | 20 instances of `GB200_GB_HEAD` (head-shape library) |
| `GB200_GB_STD_EAR2` / `GB200_GB_STD_EAR1` | normal | 19 / 18 instances of the two ear symbols |

Two facts matter here. (1) The separated eye construction (brows / eye lines / **two white
mask layers** / pupils as independent layers) exists in the file but is **parked as hidden
guide layers inside a hidden folder** — guide layers don't export, so the shipped head uses
the pre-composed `EYESCOMP_SYMBOL` instance instead. The masks are real: pupils are clipped
by white eye-shape masks, exactly the Pim pattern from the prior dissection.
(2) `GB200_GB_HEAD` itself is a **5-frame head-shape library**, labelled
`STANDARD_HEAD` / `BIG_CHEEK_HEAD` / `BIG_CHEEK_HEAD_02` / `SQUASH_HEAD` / `Eating_head_01`
(layers `LABEL_01`, `WHISKERS` — whiskers are redrawn per head shape — `HEAD_LINE`).

Head-state labels (`LABELS_HEAD`): `STD_HEAD` @0, then a demo reel of assembled expressions:
`EXAMPLE_EXP_SAD_001` @86, `EXTREME_ANGRY_001` @87, `EXTREME_ANGRY_LIPSYNCH_002` @88,
`EXAMPLE_EXP_EXTREME_HAPPY` @90, `SQUASH_HEAD` @91, `GB200_EATING_HEAD_V001` @92,
`GB200_CUTE_HEAD_V001` @93, `GB200_SCARED_FACE_V001` @94, `EXTREME_ANGRY_002` @95,
`FORCE_SMILE_01/02` @96/97, `HEAD_STD_EYES_BIG_CHEEK` @105, `HEAD_BIG_CHEEK` @150,
`GB200_EATING_CYCLE_WIP` @175. Frames 0–85 are the standard head's working range; 86+ is a
catalogue of pre-assembled example expressions a layout artist can copy.

### 1.6 MOUTH library — `GB200_GB_MOUTH`, 280 frames [PARSED]

Layers: `LABEL_01` (category track, 12 kf), `LABEL_02` (phoneme track, **124 kf**),
`GB200_OL_CHEEK` (33 kf — cheek outline), `GB200_MUZZEL` [sic] (149 kf), `GB200_MOUTH` (124 kf),
`Layer 3` (2 kf). The mouth drawing and its muzzle/cheek linework are **separate layers keyed
in parallel**, so the muzzle can be swapped independently of the mouth interior.

Category map (`LABEL_01` frame ranges):

| Range | Category |
|---|---|
| 0–16 | `HAPPY_LIPSYNCH` |
| 17–36 | `SAD_LIPSYNCH` |
| 37–78 | `MOUTH_HOLD_POSE` |
| 79–104 | `STD_EXTRA_MOUTH_FOR_LIPSYNCH` |
| 105–123 | `STD_LIPSYNCH_BIG_MOUTH_HAPPY` |
| 124–149 | `STD_LIPSYNCH_BIG_MOUTH_SAD` (label repeated @141) |
| 150–166 | `BIG_CHEEK_LIPSYNCH_HAPPY` |
| 167–229 | `BIG_CHEEK_LIPSYNCH_SAD_ANGRY` |
| 230–279 | `CHEWING_CYCLE_(to use with eating head shape)` |

Phoneme map (`LABEL_02`, happy set; the sad set repeats the same sequence at 17–33, and both
repeat again inside the big-mouth ranges at 105+ and the big-cheek ranges at 150+):
`HAPPY_REST` 0, `HAPPY_B` 1, `HAPPY_ P,M` 2, `HAPPY_N,S` 3, `F` 4, `O_01` 5, `O_02` 6, `O_03` 7,
`O,U,W` 8, `HAPPY_L_01` 9, `HAPPY_L_02` 10, `HAPPY_A_01` 11, `HAPPY_A_02` 12, `HAPPY_A_03` 13,
`HAPPY_A_05` 14 [no A_04 label — numbering as authored], `HAPPY_A,I` 15, `HAPPY_CH,S` 16.
Hold poses @37–53 include `TEETH_SMILE_01`, `OPEN_SMILE_02`, `TEETH_SAD_01/02`, `OPEN_SAD_01`,
extreme-angry/happy poses, `eating_mouth_01`, cute/scared/whistling specials, `EXT_TEETH_SMILE_003/004`.
**Counting method:** the swap set is not "280 mouths" — it is ~124 keyframed mouth drawings
(124 kf on the `GB200_MOUTH` layer) organised into labelled emotional/phonetic blocks across a
280-frame timeline, with muzzle (149 kf) and cheek (33 kf) variants keyed alongside.

### 1.7 EYES library — `GB200_GB_EYESCOMP` + `GB200_GB_EYESCOMP_SYMBOL`, 445 frames [PARSED]

Two near-twin symbols ship: `GB200_GB_EYESCOMP` (3 layers: `LABEL_01`, `LABEL_02`,
`WHITE_MASK_02` — the drawings sit directly on these tracks) and
`GB200_GB_EYESCOMP_SYMBOL` (7 layers: the same two label tracks + `EYEBROWNS` 61 kf,
`CLEAN_EYES_LINES` 55 kf, `WHITE_MASK_01` 54 kf, `CLEAN_PUPILS` 56 kf, `WHITE_MASK_02` 54 kf —
the fully separated build HEADCOMP actually instances). Both are **445 frames**.

Category map (`LABEL_01`): `STD_EYES` @0, `CLOSED_EYES` @9, `STD_SPECIAL_EXPRESSIONS` @26,
`EXT_SPECIAL_EXPRESSION` @86, `BIG_CHEEK_STD_EYES_001` @105, then (SYMBOL version)
`BIG_CHEEK_EXT_EYES` @150, `SPECIAL_POSE_EATING_CYCLE` @175 (plain EYESCOMP: whistling @125,
eating @160), and three **animated blink examples** at the end:
`STD_HEAD_ANIMATED_BLINK_EXAMPLE_001` @230, `…BIG_CHEEK…_002` @265,
`EXT_HEAD_ANIMATED_BLINK_SUPRISED/SCARED` @290 (to 444).
Named drawings (`LABEL_02`, selection): `STANDARD_EYES_01…04` @0–3, closed set @9–14
(`eyes_Closed_HAPPY_01`, `Eyes_CLOSED_02`, `CLOSED_EYES_DESPERATE_03` [SYMBOL build: absent],
`CLOSED_EYES_ANGRY_HOLD_01`, `EYES_CLOSED_SQUASH_01`, `EYES_CLOSED_SERIOUS_06`),
`BLINK_01` @16, `BLINK_02` @20, expressions @26–34 (`STD_SNEEKY_EYES_01/02`, `STD_SCARED_EYES_01`,
`CRYING_EYES_01`, `ANGRY_EYES_01`, `CUTE_EYES_01`, `SNEEKY_EYES_03`, `'blase'`, `Sneeky_04`),
extreme/big-cheek set @87–96 (`EXT_EYES_ANGRY_01`, `EXT_EYES_HAPPY_01`,
`CLOSED_EYES_FOR_EATING_HEAD`, `GB200_CUTE_zEYES_BIG_CHEEK_HEAD_V001` [sic],
`GB200_SCARED_EYES_BIG_CHEEK_V001`, `BIG_CHEEK_ANGRY_EYES_V002`, `EXT_BEAN_SHAPE_EYES`).
Pupils are their own layer/symbol (`CLEAN_PUPILS`) — never drawn into the eye whites.

### 1.8 The puppet's own instructions [IN-FILE TEXT]

On locked guide `NOTES` layers in BODYCOMP / L_ARM / R_ARM / L_LEG / R_LEG (Arial-Black 24,
dark red `#6D0101`), verbatim (body version):

> "Notes : Those shapes are not animated or inbetweens. They show how Gumball's body works.
> Gb's body needs to be redrawn according to the storyboard. You can reuse those shapes if it
> matches the storyboard or use them as references."

HEAD (per head shape): Standard Head — "Used most of the time." Big Cheek —
"The Big cheek head is used for extreme expressions. It is just a graphic solution. If the
character is really angry or super happy and the mouth doesn't fit into the standard head
then don't hesitate to draw a bigger cheek." Big-cheek closed-mouth variant — when the mouth
is closed "it is nicer to have his whiskers bigger. The head is less 'empty'."
Eating head — "Gumball's head can change of shape when his mouth is full of food or he is
hurt (to be updated)."
EAR1: "Ear Up, looks better when Gumball is happy …" / "Ear down looks better when Gumball
is sad, down… It is as well a graphic solution when Gumball has his arms above his head in
extreme posings."
EYESCOMP NB (repeated as a text block across the library): "* Eyes shapes for standard head."
/ "* Eyes shapes for Extreme Expressions, for head with a bigger cheek." /
"Those eyes are approved examples for the start of the production. There will be new posing
and shapes in futur storyboards. This puppet should be updated in layout, approved by Ben
and Mic, then sent to the an animators (maybe every month) to avoid them to redraw
everything and save time."
MOUTH NB: "* Mouth shapes for lipsynch." / "* Mouth shapes that can be used for lipsynch and
hold poses." / "* Mouth shapes for head with a big cheek." / same update note, plus:
"The lipsynch will also need to be updated according to the storyboard. Gumball can speak
with and extreme mouth or when he eats. Just use the standard lipsynch as a reference."

**This is the single most important correction this dissection makes to the prior lane's
reading:** the part libraries are **approved reference/pose banks, not a promise that the
show is assembled from them untouched**. The crew's own notes instruct the animator to
*redraw the body/arms/legs per storyboard*, reusing shapes only when they match. Sections
2.4–2.5 show a production scene doing exactly that.

Also in the puppet library: `PROPS/SANDWICH` (3 frames, 2 layers — a held prop with its own
mini-library) and `REF/EXTRAS/TWEEN_FOR_BLINK_and_eating_cycle/Tween 1…8` (1-frame tween
specimens referenced by the blink-example sections of EYESCOMP_SYMBOL).

---

## 2. SCENE — `GB202REMOTE_Sc094_Clean_V023_STN.fla` (GB202 "The Remote", Scene 094)

### 2.1 Identity / format [PARSED]

| Fact | Value |
|---|---|
| Format | XFL 2.1 in ZIP `.fla` |
| Authoring app | Adobe Flash Professional **CS5.5**, Windows, build **325** (puppet file: build 349) |
| Stage | **1920 × 1080 px** (broadcast stage — unlike the puppet's asset-container stage) |
| Frame rate | **25 fps** (confirms the owner's screenshot note for this exact file) |
| Main timeline | `Scene 1`, **56 frames = 2.24 s** at 25 fps, 9 layers (1 folder + 8) |
| Library | 49 `<Include>`s / 50 parsed symbol files, 10 folders, 5 media items |
| Naming decode | `GB202` = episode (S2 ep. "The Remote"), `REMOTE` = episode slug, `Sc094` = scene 94, `Clean` = cleanup stage, `V023` = version, `STN` = animator/studio initials |

Media items [PARSED] — every external is a **library item with its production path recorded**:

| Item | Type | Source path as authored |
|---|---|---|
| `Scene atributes/BACKGROUNDS/GB202REMOTE_SC094_LO_BG.JPEG` | bitmap, 2,473,410 B, isJPEG | `../../../05_LAYOUT/02_APPROVED/Sc094/GB202REMOTE_SC094_LO_BG.JPEG` |
| `Scene atributes/PROPS/GB202Remote_Props_TVRemoteSet_final.jpg` | bitmap, 1,034,947 B | `ASSETS/PROPS/SEASON 2/GB202_TheRemote/GB202Remote_Props_TVRemoteSet_final.jpg` |
| `Scene atributes/VIDEO AND SOUNDS/GB202_REMOTE_ANIM_094.wav` | sound, 215,918 B | `../../../04_ANIMATIC/SHOT BREAKDOWNS/MONO WAVS/GB202_REMOTE_ANIM_094.wav` |
| `Scene atributes/VIDEO AND SOUNDS/GB202REMOTE_SC094_LO_QT.flv` | video | `../../../05_LAYOUT/02_APPROVED/Sc094/GB202REMOTE_SC094_LO_QT.flv` |
| `GB23_SC_092.wav` | sound (orphan — from another scene, not placed on the timeline) | `//turner.com/dfslon/London/OSDGumball/Team/Season 2/…` (studio server path) |

(The library folder is literally named `Scene atributes` [sic] in the file.)

### 2.2 Main timeline — layer stack [PARSED]

All 8 content layers sit inside one locked folder (`Folder 1`, parentLayerIndex 0).
**Every layer except the one being animated is `locked="true"`** in this clean file.

| Layer | Type | Locked | Content over 56 frames |
|---|---|---|---|
| `audio` | normal | ✔ | 1 keyframe, f0, dur 56: `soundName="…/GB202_REMOTE_ANIM_094.wav"`, `soundSync="stream"`, flat SoundEnvelope (32768/32768). The animatic audio is stream-synced to the scene, not attached as an event sound. |
| `framecounter` | normal | ✔ | 1 instance of `Field&Framecounter/framecounter1000`, scale 1.6839, tx 2026.85, ty 198.2 (burn-in counter parked at the stage's top-right edge area; counter symbol is built to 1999 frames from three digit sub-counters of 10/100/999 frames) |
| `fieldguide` | **guide** | ✔ | 1 instance of `Field&Framecounter/Fieldguide_001` (3 shape layers — field/frame lines), tx 959, ty 1178.3 |
| `Mom Angry run Cycle` | normal | — (current/selected) | 20 keyframes; symbol content on f6–16 and f49–55 only (see §2.3) |
| `mom` | normal | ✔ | 3 keyframes; symbol content on f17–48 only (see §2.3) |
| `CAR` | normal | ✔ | **One `DOMShape`** at f0, dur 56 — a single drawn shape held for the whole scene (no symbol, no bitmap) |
| `background` | normal | ✔ | 1 instance of symbol `bg`, scale 0.848, tx 948.25, ty 188.05 |
| `layout mov` | **guide**, `visible="false"` | ✔ | 1 `DOMVideoInstance` of the layout QuickTime (`…_LO_QT.flv`), `frameRight=38400` twips = 1920 px, `frameBottom=21600` = 1080 px, at tx 0.2, ty 0.1 — the approved layout movie, full-frame, as a hidden guide under the animation |

**Camera/background structure:** there is **no camera object** (0 camera elements, CS5.5).
Camera/layout intent is carried by (a) the hidden full-frame layout video on a guide layer,
(b) the field guide, and (c) the background bitmap's own placement: `bg` is a 1-frame symbol
holding a single bitmap instance of the approved layout background JPEG
(`GB202REMOTE_SC094_LO_BG.JPEG`), scaled 0.848 on stage. Any camera move would have to be
executed by moving these layers — in this 56-frame scene, background, CAR shape and guides
are all static for the full duration; only the character layers change.

### 2.3 How the puppet is instanced — two rigs, alternating, never both [PARSED]

The character in Sc094 is **Nicole ("Mom") — Gumball does not appear in this scene.**
She is present in two completely different rig forms, and the two main-timeline character
layers are **exact complements**:

| Frames | `Mom Angry run Cycle` layer | `mom` layer |
|---|---|---|
| 0–5 | blank keyframe (dur 6) | blank (dur 17) |
| 6–16 | **11 single-frame steps** of `Mom angry run rough` | blank |
| 17–48 | blank (dur 32) | **1 instance** of the Mom pose-library puppet |
| 49–55 | **7 single-frame steps** of `Mom angry run rough`, **flipped** | blank (dur 7) |

**Form A — pose-library puppet (f17–48).** One graphic instance:
`GB200_NICOLE_ORIGINAL_PUPPET_V001/GB200_MOM_ORIGINAL_PUPPET_V001`,
`loop="loop"`, `firstFrame="17"`, scale **0.5303**, tx 1334.75, ty 173.35,
transformationPoint (186.55, 318.75). That symbol is a **159-frame pose library** — the same
architecture as the Gumball STD master (label track `POSES_LABELS`: `GB200_STD_STAND_UP` @0,
`GB200_STD_SITING_001` @62, `GB200_STD_EATING_001` @69, `GB200_STD_SAD_001` @77,
`GB200_STD_BEND_LEGS_001` @89, `GB200_EXT_ANGRY` @99, `GB200_EXT_HAPPY` @112, `GB200__SQUASH`
@119, `GB200_RUN` @128, `GB200_WALK` @140; 14 layers; 88 child instances addressed by
`single frame`/`firstFrame` into Mom's own part libraries — HEADCOMP 114 f, MOUTH 154 f,
EYECOMP 60 f, HEAD 5 f, BODYCOMP 11 f, arms 11–12 f, legs 10 f, tail 6 f, ears 4 f).
The scene does **not** link the external puppet file: the puppet is **copied into the scene's
library** (all symbols are local; no `sourceFlaName` linkage on any symbol in either file).
A second, foldered copy (`Scene atributes/CHARACTERS/GB200_NICOLE_ORIGINAL_PUPPET_V001/…`,
a different 60-frame build with its own `REMOTE` prop layers and 20-layer stack) also sits in
the library but is **referenced by no timeline** in the file — a parked working copy.
The used copy is additionally referenced inside `Mom angry run rough` on its `New model`
reference layer (8 placements, `single frame`, firstFrame 18).

**Form B — scene-built run rig (f6–16, f49–55).** `Mom angry run rough` is a **96-frame,
23-layer** symbol built for this scene, mixing finished and rough work in one timeline:
clean part layers (`L arm`, `Head`, `Body`, `Skirt`, `Tail`, `R arm`, `L leg`, `R leg`, `Ear`)
sit beside their own rough counterparts (`rough`, `Rough`, `rough l arm`, `rough body`,
`rough head`, `rough ears`, `rough skirt`, `rough tail`, `rough legs`, `rough r arm`),
plus two `REMOTE` prop layers (60 instances of the TV-remote prop symbol,
`GB202Remote_Props_TVRemoteSet_final.swf`, 27 frames), a `New model` layer (the pose-puppet
placements above), an `old cycle` layer, and 83 instances of the foldered Mom HEADCOMP.
On the main timeline the animator **steps it by hand**: each keyframe is a separate graphic
instance with `loop="play once"` and `firstFrame` set equal to the scene frame index
(f6→firstFrame 6, f7→7, … f16→16; f49→49 … f55→55), repositioned every frame —
entrance run: scale 0.7181, tx **2208 → 1454** (entering from off-stage right, moving left),
ty ≈ −14…3.5; exit run: scale **−0.7181** (negative `a` = flopped), tx **1542 → 2109**
(moving right, back off-stage), ty ≈ 741–759. No motion tweens anywhere on the layer
(`tweenType` absent on every keyframe) — the run's travel is keyframed instance-by-instance,
and the flop is done with the instance matrix, not a flipped rig.

**Scene-specific 3/4 rig built alongside:** the library also holds a purpose-built
three-quarter run/head rig that the run symbol draws on — `MOM_34_HEADCOMP` (**110 frames**,
18 layers incl. two `MASK` layers, separate `MOM_34_PUPIL_L/R` (4 f), `MOM_34_WHITE_L/R`
(43 f each, label track: `blink` @1, `ovs` @6, `closed` @10, `misc` @19), whiskers, ears,
and an embedded `audio` layer), `MOM_3-4_MOUTHCOMP` (**109 frames**; its label track is a
*different, lowercase* phoneme convention — `happy rest`, `mm/bb`, `bb/pp`, `ee`, `a`, `a/ah`,
`ah`, `uh/oh`, `oh`, `u`, `vv/ff`, `ll`, `nn/dd/zz`, `sss`, `rest`, then a sad set — 34 labels),
`mom run 001MOM_34_COMP` (59 f, 10 layers), `mom run_2` / `mom run_2 copy` (16 f gait pieces),
`mom run_3`. In other words: **when the stock puppet didn't cover the shot, the scene crew
built a new view-specific rig inside the scene file**, reusing the master's head/mouth/eye
*system* (labels, masks, separate pupils) but not its symbols.

### 2.4 What the scene proves about the pipeline [PARSED + IN-FILE TEXT]

1. Scenes are **self-contained**: puppet, props, background, layout video, animatic WAV and
   frame counter are all copied into the scene .fla. Nothing is externally linked.
2. The stock puppet covers **held/posed acting** (Form A, one instanced pose-library symbol);
   **locomotion and scene-specific action are redrawn/built per scene** (Form B + the MOM_34
   rig) — exactly what the puppet's own NOTES layers instruct (§1.8).
3. Cleanup state is visible in the file mechanics: `_Clean_` in the name, every non-active
   layer locked, rough and clean layers coexisting inside the run symbol (roughs not deleted),
   and a leftover orphan sound from scene 092 still sitting in the library.
4. Dialogue/animatic sync is a **stream sound on its own locked layer** spanning the scene.

---

## 3. FLA PRODUCTION STANDARD — rules derived from both files [DERIVED]

**File & naming**
1. Puppet file: `GB<block>_ORIGINAL_PUPPET_<CHAR>_VERSION_<NNN>`; scene file:
   `GB<ep><SLUG>_Sc<NNN>_<Stage>_V<NNN>_<INITIALS>` (template stub shipped in-file:
   `GB2XXNAMEOFTHESHOW_ScXXX_KeyAnim_V000`). Stage words seen: `Clean`, `KeyAnim`, `FINAL`.
2. Symbol naming: `GB<block>_<CHARCODE>_<VIEW>_<PART>`, comps suffixed `COMP`
   (`HEADCOMP`, `BODYCOMP`, `EYESCOMP`/`EYECOMP`, `MOUTHCOMP`); library folders =
   `<PUPPET>_v001/` per view; scene library folders = `Scene atributes/{BACKGROUNDS,
   CHARACTERS, FX, PROPS, VIDEO AND SOUNDS}` + `Field&Framecounter/`.

**Document settings**
3. Broadcast scenes: **1920×1080 @ 25 fps**. Puppet files: an asset-container stage
   (2730×1625 here) laying all view rigs out side-by-side under a locked template frame —
   never animate on the puppet file's stage.

**Puppet construction**
4. One character = **one rig per view** (STD 3/4, FRONTVIEW, BACKVIEW, FLOPPED drawn
   separately — flopping is a rig, not a scale trick, inside puppets; note the scene-level
   exception in §2.3 where an *instance* is flopped for an exit run).
5. Master symbol layer order is part-named, with front/back splits where the body must pass
   between (`L_ARM_FRONT` vs `L_ARM_BEHIND`), and a `HIDE_NECK` occluder layer in every master.
6. Posing = **labelled pose library + graphic instances with `loop="single frame"` +
   `firstFrame`** into each part's swap library. Label tracks are separate locked layers
   (`POSES_LABELS`, `LABELS_HEAD`, `LABEL_01`/`LABEL_02`) — never name drawings only by frame #.
7. Part swap-library sizes from this puppet (Gumball STD): mouth ~124 keyframed drawings on a
   280 f labelled timeline; eyes 445 f; headcomp 309 f; head shapes 5; body 11; arms ~24–26 kf
   (89–90 f timelines); legs 10; tail 7. Front/back views may ship **reduced** libraries
   (single-drawing mouth/eyes in FRONTVIEW here) — the STD 3/4 view carries the full set.
8. Mouth system: two label tracks (category + phoneme), emotional sets repeat the same phoneme
   sequence (REST, B, P/M, N/S, F, O×3, O/U/W, L×2, A×3–5, A/I, CH/S, TH), hold poses and
   extreme/special poses parked after the lipsynch sets, chewing cycle last; mouth, muzzle and
   cheek on **separate parallel layers**.
9. Eye system: expression library (standard / closed / blink / special / extreme / big-cheek
   categories), pupils always a separate symbol/layer (`CLEAN_PUPILS`), eye whites as masks
   (`WHITE_MASK_01/02`), brows separate (`EYEBROWNS`); animated blink *examples* stored at the
   end of the library timeline. Head shapes are a labelled library (standard / big-cheek ×2 /
   squash / eating) with whiskers redrawn per shape.
10. Pivots: instance `transformationPoint` at the anatomical joint, identical across all
    keyframes of that part's layer.
11. **Documentation lives in the file**: locked guide `NOTES` layers per part symbol
    (Arial-Black 24, #6D0101), label tracks, and NB update notes ("approved examples… this
    puppet should be updated in layout… maybe every month"). A puppet without in-file notes
    is below standard.
12. Reference/template material is quarantined: `REF/` folders, guide layers, hidden folders
    (`EYES_COMP_SEPARATED`) — present for the crew, excluded from export.

**Scene construction**
13. Scene stage stack, top→bottom: `audio` (stream WAV) → `framecounter` → `fieldguide`
    (guide) → character layers → `CAR`/foreground shapes → `background` → `layout mov`
    (guide, hidden, full-frame layout video). Everything inside one folder; **lock every
    layer you are not animating**.
14. Puppets are **copied into the scene library**, never linked; scene-specific views/cycles
    are built as new local symbols following the same label/mask/pupil system.
15. Graphic-symbol frame-stepping (`play once` + `firstFrame` = scene frame) is the accepted
    way to run a cycle across a scene; travel is keyframed per frame, no motion tweens on
    the character layers in this file.
16. Background = approved layout artwork as a bitmap inside a 1-frame `bg` symbol; props are
    bitmap-sourced symbols instanced on their own layers inside character comps
    (`REMOTE` layers; the prop carries its own 27-frame library).

**Honesty notes / limits of this dissection**
- All counts above are keyframe counts parsed from the XML (`DOMFrame` index/duration sums);
  "frames" for a symbol = max over its layers of summed durations. Two label-track layers in
  `GB200_GB_MOUTH` disagree slightly (LABEL_01 sums to 118 in the Mom copy — Gumball's sums
  to its full 280); where a layer's frames didn't cover the symbol length, the symbol total
  is the max layer length, as tabled.
- No rendering was performed; shape-level drawing content (beyond layer/element census —
  e.g. the scene's single `CAR` shape) was not visually verified.
- The prior lane's CS3 findings (doc strings, naming) are consistent with this parse; the
  one correction is format: **VERSION_008 and the scene files are CS5.5 XFL, not OLE2.**

**Files kept for reuse** (`~/workspace/agent-ops/fla-puppets-program-2026-10-30/gumball/`):
both `.fla` files, both full `_xfl/` extractions (all `DOMDocument.xml` + `LIBRARY/*.xml`),
`puppet008-parsed.json` / `scene094-parsed.json` machine-readable parses,
`puppet008-infile-texts.txt` / `scene094-infile-texts.txt` extracted in-file prose, and
both archives' central-directory inventories.
