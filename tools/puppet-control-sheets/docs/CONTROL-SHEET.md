# Puppet Control Sheet Convention v1 — Tahoma2D

SPEC T-1. The studio standard every 2D puppet in Tahoma2D ships with, so
any animator can open any character — Wizard Gang, 2D Cape Jones, or a
future show — and find the same controls in the same places. This is the
Tahoma2D-native answer to Toon Boom Harmony's Master Controllers: where
Harmony gives the rigger a widget API, Tahoma2D gives us **pegbars** —
named transform nodes in the Stage Schematic with keyframable channels.
The convention standardizes those pegbars, and the generator
(`puppet_control_sheets/generate_puppet_scene.py`) builds them into the
scene file. See `TAHOMA2D-SURFACE-NOTES.md` for why this lands as
scene-file generation rather than in-app widgets.

## 1. The control hierarchy (identical for every character)

```
Table
└── CTRL_ROOT            whole puppet: placement in the shot
    └── CTRL_BODY        torso group: lean, bounce, squash anchor
        ├── CTRL_HEAD    head group: tilt, turn, nod
        │   ├── Col<mouth>   → mouth level (substitution drawings)
        │   └── Col<eyes>    → eyes level (substitution drawings)
        ├── CTRL_ARM_R   right arm group: swing, raise
        │   └── Col<hand_r>  → hand level (substitution drawings)
        ├── CTRL_ARM_L   left arm group
        │   └── Col<hand_l>
        └── Col<body>    → body level
```

Rules:

1. **Controls are pegbars named `CTRL_<PART>`**, uppercase, one per part
   group. Animators keyframe *controls*, never part columns directly.
   Implementation note (learned from Tahoma's loader, see
   TAHOMA2D-SURFACE-NOTES.md): a .tnz stage-object **id** can only be
   `Table`, `Camera<N>`, `Peg<N>` or `Col<N>` — any other id string
   parses to None and the peg is silently dropped. So the wiring uses
   Tahoma ids (`Peg1` is always CTRL_ROOT, `Peg2..N` the part controls
   in hierarchy order, allocated by the generator and recorded in
   `poses.json` under `control_pegs`), and the `CTRL_*` identity lives
   in the pegbar's **name**, which is what the Stage Schematic shows.
   The convention an animator sees is unchanged: find `CTRL_HEAD`,
   keyframe it.
2. **Every part is a raster level on its own xsheet column.** The
   column's own pegbar (`Col<N>`, auto-named by Tahoma2D) is parented
   **under the part's control peg** — that parenting is the wiring: key
   the control and the part (plus everything parented below it) moves.
3. **Parenting follows the body**: head rides body, hands ride arms,
   mouth/eyes ride head. A control's children are listed in the
   character JSON's `parent_control` field; the generator enforces the
   chain `CTRL_* → … → CTRL_ROOT → Table`.
4. **Control channels** are the pegbar channels Tahoma2D exposes:
   `x`, `y` (stage units; 1.0 ≈ 100 px at template camera), `angle`
   (degrees, the workhorse for head tilt / arm swing), `sx`, `sy`
   (scale), `sc` (overall scale). Every control carries all of them with
   identity defaults, so the Function Editor shows the same curves for
   every puppet.
5. **Part rest offsets live on the control peg's default `x`/`y`**
   (from the character JSON `offset`, in px ÷ 100), not baked into the
   drawing, so zeroing a control's keyframes returns the puppet to its
   model-sheet rest pose.

## 2. Pose library — named poses as control keyframes

A pose is a named set of control transforms. Storage, two copies that
must agree:

- **In the scene**: after the shot frames, a **pose block** holds each
  pose keyframed on its controls for `pose_hold_frames` frames
  (default 4). Pose order and names come from the character JSON.
  Every generated puppet starts with the studio starter set:
  `neutral`, `wave`, `point`, `lean_left`, `lean_right` (a show template
  may trim it, never rename it).
- **`poses.json` sidecar** next to the scene: pose name → block frame →
  exact channel values. This is the machine-readable copy the
  ToonzScript helper and future tooling read.

**Exposure workflow for the animator** (the "named pose-library exposure
workflow" from the spec):

1. Scrub to the pose's block frame in the pose block; the puppet shows
   the pose, controls already keyed.
2. In the Function Editor / Stage Schematic, copy the control keyframes
   at that frame.
3. Paste them at the shot frame where the pose is wanted. Interpolate
   in/out by adding the neighbouring pose the same way — poses are
   keyframe sets, so pose-to-pose animation is copy/paste, not re-posing.
4. Substitution parts (mouth, eyes, hands) are exposed per pose by the
   generator in the pose block (their cells cycle drawings there), and
   in the shot the animator sets the part column's cell to the drawing
   the pose calls for — the drawing *number* is the pose contract
   (see §3).

## 3. Drawing substitutions

Parts declared with `"drawings": N` in the character JSON are
substitution levels: one level, N numbered drawings
(`<part>.0001.png` … `<part>.000N.png`), swapped by changing the cell's
frame id on the exposure sheet — Tahoma2D's native drawing-substitution
mechanism, same role as Harmony's drawing library.

Standard substitution sets:

| part  | drawings | meaning (by number)                                   |
|-------|----------|-------------------------------------------------------|
| mouth | 9        | the show's standard mouth set (T-2 MouthSwap feeds it) |
| eyes  | 3        | 1 open, 2 blink/half, 3 closed                        |
| hands | 4        | 1 flat, 2 point, 3 fist, 4 open/grab                  |

Drawing 1 is always the neutral/rest drawing and is what the shot
frames expose by default.

## 4. Per-show puppet templates

`templates/` holds one JSON per show — `wizard-gang.json`,
`cape-jones-2d.json`. A template is the control layout above with the
show's standard part list, canvas sizes, camera (1920×1080 @ 24 fps)
and starter poses. The layout is *identical* across shows; only the
part list, palette and canvases differ. To ship a new character:

1. Copy the show template, rename `parts_template` → `parts`, set
   `"character"`, and fill in each part's real canvas/color (or replace
   the generated placeholder drawings with the character's real levels
   afterwards — same filenames).
2. Run the generator → `<character>.tnz` + `poses.json` + drawings.
3. Run the validator; then the tcomposer smoke render (README §Test).

## 5. What this convention deliberately is not

- Not an in-app widget panel. Tahoma2D 1.6.3 has no API for one
  (see TAHOMA2D-SURFACE-NOTES.md). If a future Tahoma2D exposes peg/
  keyframe scripting, the `poses.json` contract is the migration path:
  a widget would read the same file and set the same keyframes.
- Not a deformer rig. Bone/Plastic work (gap G-T3 in the build map) is
  per-character and sits *below* the part level; controls still group
  and drive the parts exactly as above.
