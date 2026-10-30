# FLA PRODUCTION STANDARD — Wizard Gang puppets, rigs, and scene files

**Owner directive (2026-10-30):** *"We need to make fla puppets and rigs and scene
files for all our shows"* — and for Wizard Gang first: *"But this is about doing
it for wizard gang tho."*

**Derived from:** a full XML dissection of two real Gumball production files the
owner holds (`GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`, 1,740,533 B, and
episode scene `GB202REMOTE_Sc094_Clean_V023_STN.fla`, 22,851,853 B — both CS5.5
XFL, from `mhvnsnt/cn-gigaleak-gumball`, release `gumball-s2-rigs-v1`). Full
dissection with parsed frame/label maps:
`agent-ops/fla-puppets-program-2026-10-30/gumball-dissection.md`.
**Companion docs:** `WG-RIG-TEMPLATE.md` (part/level standard), `RIG-DISSECTION.md`
(Smiling Friends + Gumball naming), `FIRST-SHOT-SPEC.md` (first proof shot).

A modern `.fla` is a ZIP of XFL XML (`DOMDocument.xml` + `LIBRARY/*.xml` +
media). We author XFL directly, zip to `.fla`, validate by round-trip parse
(FlashXFLParser), and render poses with the local XFL renderer. Structure is
copied from the Gumball system; every drawing is our own characters' real art
from the part library — never redrawn substitutes (PACKS-ARE-PULLED law).

---

## 1. File naming (adapted from the GB codes)

```
Puppet file:  WG<block>_ORIGINAL_PUPPET_<CHAR>_VERSION_<NNN>.fla
              e.g. WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla
Scene file:   WG<block><EPSLUG>_Sc<NNN>_<Stage>_V<NNN>_<INITIALS>.fla
              e.g. WG101ARRIVAL_Sc001_Clean_V001_ASH.fla
              Stage = KeyAnim | Clean | FINAL
Symbol:       WG_<CHARCODE>_<VIEW>_<PART>      e.g. WG_ASHES_FRONT_HEADCOMP
              Compositions suffix COMP: HEADCOMP, BODYCOMP, EYESCOMP, MOUTHCOMP
View:         FRONT | TQ (three-quarter) | BACK | FLOP (drawn, not mirrored)
Library folder: <PUPPET>_V<NNN>/ per view; scene folders:
              Scene attributes/{BACKGROUNDS, CHARACTERS, FX, PROPS, VIDEO AND SOUNDS}
              + Field&Framecounter/
```

- Every puppet is versioned; never overwrite a shipped version, version up.
- One character = **one rig per view**. A flopped view is its own drawn rig
  inside a puppet (inside a *scene*, an instance may be flopped by matrix for
  an exit — Gumball scene rule).

## 2. Document settings

| | Puppet file | Scene file |
|---|---|---|
| Stage | Asset-container sheet (all view rigs side by side under a locked REF template) — **never animate on the puppet stage** | **1920×1080** |
| Frame rate | 24 fps | **24 fps**, animate on 2s (Gumball originals ran 25 fps; WG house rate is 24 per FIRST-SHOT-SPEC) |
| Camera | none (guide/field layers only) | camera move is keyframed plate/instanced-symbol transforms (Pipeline One parallax, §6) |

## 3. Puppet construction

1. **Master symbol per view.** The stage/scene holds ONE instance of the
   master; everything lives inside it. Master layer order is part-named,
   top→bottom (front-to-back): front arm → accessory → robe/torso front →
   head comp → body → robe back → legs → back arm → shadow. Front/back splits
   where the body must pass between (`ARM_FRONT` vs `ARM_BEHIND`), plus a
   `HIDE_NECK` occluder layer where the head meets the body.
2. **Head is a nested comp** (`HEADCOMP`): face plate, mouth comp, pupils,
   eye shapes, lids, expression/brow layer, headwear, hair/FX — each feature
   that moves on its own is its own symbol on its own layer (Charlie/Pim rule).
3. **Posing = labelled pose library + `single frame` addressing.** The master
   symbol's timeline is a pose library (labels: STAND, GESTURE_WIDE, POINT,
   WALK, RUN…); scenes place graphic instances with `loop="single frame"` +
   `firstFrame` = the pose's frame. Label tracks are separate locked layers —
   never address drawings by bare frame number alone.
4. **Pivots:** every part instance carries a `transformationPoint` at the
   anatomical joint (neck, shoulder, elbow, wrist, waist/hip, knee), and the
   point is **identical across all keyframes** of that part's layer. A part
   that rotates around its corner is below standard.
5. **Joint segmentation:** upper arm and forearm+hand are separate symbols
   (elbow pivot between them) *when the source art carries them*. Where the
   source art fuses a joint (see §7, joint truth table), the rig ships with
   the pivots that exist and the gap is written into the file's notes —
   never simulated with a whole-part slide.
6. **Documentation lives in the file:** locked `NOTES` guide layers in the
   master and per part symbol (what the set is, how to address it, known
   gaps), exactly as the Gumball puppets carry theirs. A puppet without
   in-file notes is below standard.
7. Reference/template material is quarantined in `REF/` folders and guide
   layers — present for the crew, excluded from export.

## 4. Required symbol sets per character

Every character puppet ships these sets before it is called a rig. Sizes are
floors, from the pro files (Gumball STD view: mouth ~124 drawings, eyes 445 f
of expressions, arms ~24–26 keyframes) and the WG template.

| Set | Contents | Floor |
|---|---|---|
| Body parts | robe/torso front+body+back (or torso set), head comp, arm_front, arm_behind (upper + forearm/hand split where art allows), legs w/ labelled cycle segments (standing / walk_start / walk_end), shadow plate | all slots present or gap-logged |
| **Mouth set** | ONE `MOUTHCOMP` symbol, frame-addressed library: `X_REST` (closed/neutral), Blair A–H, `O_ROUND`, `WIDE`, `HOLD_POSE`, character-specific shapes, `BONUS_##` tail. Label tracks: category + phoneme. | 12 core drawings (pros run 25–28) |
| **Eye set** | `EYESCOMP`: per-eye OPEN / HALF / SHUT (lids are swaps, never a squash), pupils as a separate clean symbol, expression library with numbered variants + hold poses (`SMILE_01`, `ANGRY_01`, `CLOSED_EYES_ANGRY_HOLD_01` pattern). **Two colourway variants ship in the same puppet**: the base-white set AND the character's colourway set, as separately labelled swap ranges. | both variants, all states |
| Hand set | per-side hand drawings for the poses the arms ship (rest, point, open, grip, character poses), addressed like the arm libraries | matched to arm set |
| Pose library | labelled master poses: STAND/NEUTRAL, GESTURE_WIDE, POINT, plus the cycles the show reuses (walk, run, idle talk) | 3 poses minimum for a proof puppet |

**Ashes exception (canon):** Ashes is the only Wizard Gang cast member with a
mouth — his diamond-grill set IS his mouth set, and the grin (`X_REST`) is on
his face 100% of the time. The other eight are void-faced: their mouth parts
are rare-expression parts only, expression carried by eyes/hands/movement.
Ashes' colourway is the flame/amber eye set; his base-white set ships too.

## 5. The T-pose rule (owner's corrected version, 2026-10-30)

Owner, verbatim: *"if u animate him out of t pose it's fine."*

- T-pose art **is** a legitimate rig base — every puppet starts from one.
- The acceptance bar is on the **output**: finished animation must pose the
  character OUT of the T-pose with real movement. Stiff T-pose-locked output
  fails; the source sheet does not.
- Seam/hole defects at joins (the cape-hole family) fail regardless of source.

## 6. Scene file structure

Scene layer stack, top→bottom, everything inside one folder; **lock every
layer you are not animating** (Gumball scene rule):

```
audio            (stream-synced WAV: animatic/dialogue)
framecounter
fieldguide       (guide layer: safe areas, field notes)
<character layers>   one per character, master-symbol instances
props / FG shapes    (props are bitmap-sourced symbols with their own libraries)
background       (BG plates as symbols; parallax = far/mid/near plates on
                  separate layers, slid at different rates — Pipeline One)
layout mov       (guide, hidden: layout/animatic video or plates)
```

- Puppets are **copied into the scene library**, never externally linked.
  Scene-specific views or cycles are built as new local symbols following
  this same standard.
- Cycles run across a scene by graphic-symbol frame-stepping
  (`play once` + `firstFrame` = scene frame); character travel is keyframed —
  no whole-character slide as a substitute for joint motion.
- Background = approved layout art as bitmap(s) inside 1-frame `bg` symbols,
  one per depth plate for parallax shots.

## 7. Acceptance gates (owner's words, 2026-10-30)

Owner, verbatim: *"don't leave him in t pose and call it an animation. Make a
damn fla puppet rig and give him real motion."*

1. **The rig must bend** — parts on pivots that move at neck, shoulders,
   elbows, hips, knees, as the art allows. Every puppet ships a **joint
   truth table** in its in-file notes + build log: which joints bend, which
   are fused in the source art, which parts don't exist. A joint that can't
   bend is *said*, never faked with a slide.
2. **The proof clip must show real motion** across distinct poses (rig pose →
   gesture → point → settle) with joint bends and weight shift visible
   between frames. Idle sway, blink-only, flat head-slide, or whole-character
   slide = FAIL (this pattern has been rejected twice; do not ship a third).
3. **Own-eyes frame verification before reporting:** extract frames, confirm
   consecutive poses genuinely differ at the joints, and include a 6–8 frame
   strip sheet in the proof package so the motion reads in one image.
4. Parts come only from the character's real library art. A missing part is
   a logged gap, never an invented drawing.
5. Per-character isolation: one character's build touches nothing of the
   other eight.

## 8. Build order (program)

1. **Wizard Gang** — Ashes proof puppet + proof scene (FIRST-SHOT-SPEC twin),
   then the other eight cast puppets to this standard.
2. **Cape Jones** — from *his own* drawn 2D art in the cape-jones repo
   (owner, 2026-10-30: "We don't need to cut apart space ghost, cause we
   already have art and stuff if cape jones"). Parked until the WG proof lands.
3. **The Mochiichao show** — same standard, its own art. Parked likewise.
