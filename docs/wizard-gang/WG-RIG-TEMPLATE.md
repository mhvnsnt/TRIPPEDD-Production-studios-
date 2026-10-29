# WG RIG TEMPLATE — the Wizard Gang character-rig standard for Tahoma2D

**Built FROM:** the dissected pro rigs in `RIG-DISSECTION.md` (Smiling Friends Charlie/Pim
Animate structure + Gumball puppet naming/library system), the mystery-coast-ghosted
mouth-switch doctrine (`docs/research/PIPELINE.md`: Tahoma2D cutout, mouth-switch layers,
Rhubarb, 2s/3s), and the animation-techniques-archive character-pipeline (Stage 3 rig spec +
Stage 4 viseme pack). **Stage:** Tahoma2D 1.6.3 (OpenToonz family: parts = levels,
animation = Xsheet columns, drawing substitution = the mouth-switch mechanism).
**One master puppet per wizard** (Pipeline-One/V2 rig plan). Ashes is built first.

---

## 1. Naming (from the Gumball system, WG codes)

```
Character master:  WG_<NAME>                       e.g. WG_ASHES
View pack:         WG_<NAME>_<VIEW>_V<###>         VIEW = FRONT | TQ | BACK   (TQ = three-quarter)
Part level:        WG_<NAME>_<VIEW>_<PART>         e.g. WG_ASHES_FRONT_MOUTH
Mouth drawing:     <VISEME>[_<variant>]            e.g. A, F, X_REST, GRILL_WIDE
Eye drawing:       <STATE>[_<###>]                 e.g. OPEN, HALF, SHUT, ANGRY_01, SMILE_01
```
- Every puppet folder is versioned (`_V001`); never overwrite, version up
  (techniques-archive Stage 6 rule).
- Usage notes live inside the project README, like the Gumball doc strings.

## 2. Column stack (Tahoma2D Xsheet, top of stack = front)

One character = one Tahoma2D scene block of levels, in this order (mirrors Charlie's
9-layer master, with Pim's head internals):

| # | Level (part) | Content / substitution set |
|---|---|---|
| 1 | `<NAME>_FRONTARM` (screen-front arm) | pose-swap level: 4–6 arm+hand drawings |
| 2 | `<NAME>_ACCESSORY_FX` | chains/props that sit in front (Ashes: chain front swing) |
| 3 | `<NAME>_ROBE_FRONT` / `TORSO_FRONT` | robe front panel / torso front |
| 4 | `<NAME>_HEAD` (sub-scene, §3) | the whole head rig |
| 5 | `<NAME>_ROBE_BODY` / `BODY` | main body mass (breathing = moving hold on this level) |
| 6 | `<NAME>_ROBE_BACK` / `BODY_BACK` | back panel so head/arms layer correctly in turns |
| 7 | `<NAME>_LEGS` | labelled segments: `standing` / `walk_start` / `walk_end` (Pim system) |
| 8 | `<NAME>_BACKARM` | pose-swap level: 3–6 drawings |
| 9 | `<NAME>_SHADOW` | contact shadow plate |

Head turns are done the Pipeline-One way: the head sub-rig carries FRONT and TQ face
plates as substitutions; full TQ/BACK view packs are separate versions of the whole
stack (Gumball rule), built when a scene actually needs them.

## 3. Head sub-rig (from Charlie's 8 layers + Pim's 15)

| Order | Level | Standard |
|---|---|---|
| 1 | `BROW_L` / `BROW_R` (or expression brow plate) | **3 states each** (neutral / raised / lowered) — Charlie system. Void-face characters (Ashes) replace brows with the eye-expression set, §4 |
| 2 | `PUPIL_L_PARENT` → `PUPIL_L` | pupil drawing inside a **parent level** (Pim system): travel keyed on the parent, drawing untouched |
| 3 | `PUPIL_R_PARENT` → `PUPIL_R` | same |
| 4 | `EYE_L` / `EYE_R` | eye shape; pupils clipped to it with a Tahoma2D **mask column** (Pim's LeyeMASK/ReyeMASK) |
| 5 | `LID_L` / `LID_R` | **3 drawings each: OPEN / HALF / SHUT** — blinks are lid swaps, never a squash |
| 6 | `MOUTH` | §4 — the mouth-switch level |
| 7 | `FACE` | face/scalp plate everything mounts on |
| 8 | `HEADWEAR` | hat/hood plate; hood characters ALSO carry `HOOD_DOWN` substitution |
| 9 | `HAIR_FX` | braids/locks as separate levels (keyed sway; nijilive physics does NOT transfer — hand-key or Plastic-mesh) |
| 10 | `ACCESSORY` | chains, grill shine, earrings — own level each |

## 4. Mouth-switch standard (the heart of it)

- ONE `MOUTH` level per head view. Drawings are addressed by cell substitution —
  this is the mystery-coast mouth-switch system, and it is exactly Charlie's
  25-frame / Pim's 28-frame single-symbol library translated to Tahoma2D.
- **Feed:** Rhubarb (bundled in Tahoma2D 1.5+; also local 1.14.0 +
  `~/workspace/tools/lipsync/rhubarb_to_visemes.py`) outputs OpenToonz/Moho `.dat`
  with Preston Blair mouth names → drops straight into Tahoma2D timing.
- **Core set (drawn in the character's own style — techniques-archive Stage 4 law:
  position from the chart, style from the character):**

| # | Drawing | Rhubarb/Blair code | Notes |
|---|---|---|---|
| 1 | X_REST | X | closed/neutral — for Ashes this IS the grill grin (canon signature) |
| 2–9 | A B C D E F G H | A–H | the 8 Blair phoneme shapes |
| 10 | O_ROUND | (W/Q) | round/purse |
| 11 | WIDE | — | shout/laugh hold |
| 12 | HOLD_POSE | — | a held mid-shape for HB-style holds (Gumball `MOUTH_HOLD_POSE`) |
| 13+ | char-specific | — | per character, see Ashes below |
| tail | BONUS_## | — | one-off shapes, parked after the set (Pim's `bonus` rule) |

- Working size: **13 core + character set; pros run 25–28 total.** Do not ship a rig
  with fewer than the 12 core drawings.
- Eyes standard (Gumball library rule): `OPEN, HALF, SHUT` per eye via lids, plus an
  expression drawing set `SMILE_01, ANGRY_01, DESPERATE_01…` numbered variants with
  hold poses (`CLOSED_EYES_ANGRY_HOLD_01` pattern).

## 5. Animation conventions baked into the template

- Animate on **2s and 3s** (8–12 unique poses/sec) per mystery-coast/HB doctrine;
  holds are the style — selective smoothing only where the timing chart marks it.
- Walk/run cycles are authored ONCE as template scenes and reused (stock library:
  walk, run, idle, talk poses, reaction).
- Every level named; no "Layer 1" survives QC (Stage 6 checklist).

---

## 6. Applied: ASHES — existing parts mapped, gaps listed

Existing stock (God-Molecule-Show-Studio `tools/puppet/wizard-rig-proof/ashes/`):
a validated nijilive `.inp` (15 parts, 24 params, 2 physics rigs, 18 animations) cut from
one 400×864 group-shot crop; `parts/` 9 layers; `rig_layers/` finer 13-file split;
pose proofs (neutral / head-turn mouth-open / blink).

| Template slot | Existing Ashes part | Verdict |
|---|---|---|
| ROBE_BODY | `parts/01_robe` (+ `rig_layers/00_torso`) | HAVE — one merged robe+torso plate |
| HEAD / FACE | `parts/02_head` (= `rig_layers/01_face_base`) | HAVE — face void plate |
| HAIR_FX | `parts/03_braid_L`, `04_braid_R` (= `rig_layers/02/03_hair_side`) | HAVE — 2 braid levels (nijilive splits hair into 5 sway params; Tahoma2D keys them by hand) |
| ACCESSORY (chain) | `parts/05_chain` (= `rig_layers/04_accessory`) | HAVE |
| FRONTARM / BACKARM | `parts/06_arm_L`, `07_arm_R` (= `rig_layers/05_arm_l`, `06_arm_r`) | HAVE as single drawings only — see gap 4 |
| EYE_L / EYE_R | `rig_layers/07_eye_l`, `08_eye_r` (parts/ has them merged as `08_eyes`) | HAVE (split exists in rig_layers) |
| LID (shut only) | `rig_layers/7_eye_closed_l`, `8_eye_closed_r` | PARTIAL — closed state only |
| MOUTH | `parts/09_grill` (= `rig_layers/09_mouth` + `9_mouth_cavity`) | PARTIAL — ONE grill drawing + cavity; the .inp animates it by deform (ParamMouthOpenY / ParamMouthForm), which is NOT a substitution set |

### What Ashes is missing to be rig-complete (build list, in order)
1. **The mouth set (blocking gap).** Draw the §4 set in Ashes' style, grill-first:
   `X_REST` = the signature diamond-grill grin (canon: the grin stays in every style),
   Blair A–H adapted so the grill reads in the open shapes, `O_ROUND`, `WIDE`
   (grill stretched — the .inp proof pose already shows this deformation reads),
   `HOLD_POSE`, plus Ashes-specifics: `GRILL_BARE_TEETH` (unrobed/serious),
   `GRIN_SMUG`. Target 14–16 drawings. No other gap matters until this exists —
   it is the lip-sync system.
2. **Pupils + eye internals.** No separate pupil levels and no eye masks exist
   (eyes are flat plates). Build `PUPIL_L/R` + parent levels + mask columns per §3
   so look-direction can be keyed (Pim system).
3. **Lid middle state + eye expression set.** Only open + shut exist. Add `HALF`
   per eye, and the void-face expression library that replaces brows:
   `SMILE_01` (the .inp has ParamEyeSmile as a deform — needs a drawn state),
   `ANGRY_01`, `SHUT_HOLD` (Gumball hold-pose pattern).
4. **Arm/hand pose libraries.** Arms are 1 drawing each; pros carry 2–6 pose swaps.
   Draw per the playbook's "Ashes' 10-Pose Library" (§5 of ANIMATION-PLAYBOOK):
   point, raised-decree, down-rest, hold-prop, etc., split arm/hand if a pose needs it.
5. **Legs + feet.** None exist — the robe covers them in the only source crop.
   Needed for walk cycles and any unrobed shot: `LEGS` level with labelled
   `standing / walk_start / walk_end` segments + feet.
6. **Robe split + hood states.** Split `01_robe` into `ROBE_FRONT` / `ROBE_BODY` /
   `ROBE_BACK` so turns layer like Charlie's body/body_back. Add `HOOD_DOWN`
   substitution for the head plate — robed/unrobed is a WG identity rule
   (unrobed must hold face/body/skin/eyes/design), so both states must be swaps
   in the same rig, not separate characters. (The one hood-off identity-swap gag
   in EP01/02 is a gag, not a rig state.)
7. **TQ view pack.** Ashes exists FRONT-only (+ a separate front battle crop).
   First TQ need triggers `WG_ASHES_TQ_V001` per §1. Not blocking for the
   first proof shot (spec'd front + camera move).
8. **Resolution.** Source art is a 400×864 crop — soft at 1920×1080 stage size.
   Redraw/re-cut parts at ≥2× screen size when the mouth set is drawn (same pass,
   same style); until then the proof shot keeps Ashes at ≤60% of frame height.
9. **Battle variant parity.** `ashes-battle/` mirrors the same 9-part structure
   (with `07_ball` energy-ball part) — it inherits gaps 1–6 wholesale; fix the
   standard rig first, then port the sets.
