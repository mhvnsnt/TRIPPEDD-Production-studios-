# FLA PUPPETS + RIGS + SCENE FILES PROGRAM — log (2026-10-30)

Owner directive (verbatim): "We need to make fla puppets and rigs and scene files for all our shows"
Build order: (1) Wizard Gang [THIS LANE], (2) Cape Jones, (3) Mochiichao show. Wizard Gang first: Ashes proof.
Standard to copy: Gumball production .fla system (71 puppets + scene files, cn-gigaleak-gumball) + TRIPPEDD docs/wizard-gang/ (WG-RIG-TEMPLATE, RIG-DISSECTION, FIRST-SHOT-SPEC, REAL-ANIMATION-V2-STACK).
CHECK-FIRST: nijilive Ashes test scene is in production in the main chat — NOT duplicated here. This lane's scene = the FLA-format twin to the same FIRST-SHOT-SPEC ("The wizards have arrived", Ashes, 72f @24fps).

## Lanes running (spawned 2026-10-30)
- Gumball puppet+scene dissection -> agent-ops/fla-puppets-program-2026-10-30/gumball-dissection.md
- XFL renderer contract + minimal skeleton -> .../renderer-contract.md, .../xfl-skeleton/
- Ashes parts inventory -> .../ashes-inventory.md

## Build steps
1. [ ] FLA-PRODUCTION-STANDARD.md (TRIPPEDD PR, branch->merge per repo rules)
2. [ ] Ashes FLA puppet (.xfl + .fla) from real library parts; XFLParse validation; 3 poses rendered
3. [ ] Ashes FLA scene file (FIRST-SHOT-SPEC twin); rendered clip; frame-change verified
4. [ ] Proof package: structure side-by-side sheet + pose stills + clip

## Owner correction logged 2026-10-30 (Cape Jones phase — LATER, do not act now)
Owner verbatim: "We don't need to cut apart space ghost, cause we already have art and stuff if cape jones".
=> Cape Jones puppet will be built from HIS OWN drawn 2D art in the cape-jones repo
   (characters/design-sheet.png + sheets 04/07/08). The T-pose turnaround sheet
   (characters/sheets/01-tpose-turnaround.jpg, the 3D rig sheet) is BANNED as an
   animation/likeness source per standing law. Do NOT cut apart Space Ghost pieces
   for Cape Jones. Wizard Gang / Ashes scope of this lane is UNCHANGED.

## Owner re-center logged 2026-10-30
Owner verbatim: "But this is about doing it for wizard gang tho" — scope confirmed:
this program's point is WIZARD GANG, Ashes proof first. Cape Jones phase parked
behind the Wizard Gang proof.
COORDINATION: the cut-apart lane was re-aimed to produce a clean cut-apart +
pivot-marked Ashes part set (from the library, incl. cutting apart his full-frame
art) at ~/workspace/your_files/wizard-gang-part-libraries/_cut-apart/ashes/ for
this puppet build to consume. Check for it as it lands; if the build gets there
first from the rig-proof parts, record which part set was used here.

## Owner correction 2026-10-30 — T-POSE RULE (corrected version, supersedes the over-strict ban for rig-building purposes)
Owner verbatim: "if u animate him out of t pose it's fine".
CORRECTED RULE for the FLA standard + all puppet builds:
- T-pose art IS a legitimate rig base — every puppet starts from a T-pose.
- The acceptance bar is on the OUTPUT: finished animation must pose the
  character OUT of the T-pose with real movement. Stiff T-pose-locked output FAILS.
- The source sheet itself does NOT fail for being a T-pose.
- Cape seam/hole defects remain failures regardless.
=> FLA-PRODUCTION-STANDARD.md must carry THIS version of the rule.
(Note: this clarifies the Cape Jones art-source guidance logged earlier — the
CJ phase still builds from his drawn art per his words; the correction here is
that T-pose-derived RIG BASES are not banned, output stiffness is the failure.)

## HARD ACCEPTANCE GATE (owner verbatim, 2026-10-30)
"don't leave him in t pose and call it an animation. Make a damn fla puppet rig
and give him real motion"
GATE (his words, not paraphrase):
1. Real working FLA rig: parts on pivots that actually BEND at neck, shoulders,
   elbows, hips, knees.
2. Proof clip must show REAL MOTION across distinct poses (rig pose -> gesture
   -> point -> settle) with joint bends + weight shift visible BETWEEN frames.
   Idle sway / blink / flat head-slide / whole-character slide = FAIL (pattern
   already rejected twice: GMSS turn-and-nod proof, 2D dance v1).
3. Before reporting: extract frames, verify own-eyes that consecutive poses
   genuinely differ AT THE JOINTS; include a 6-8 frame strip sheet in the proof
   package. If the rig can't bend somewhere, SAY SO in this log — never fake
   it with a slide.

BUILD CONSEQUENCES recorded:
- Puppet symbol design must segment at joints: head on neck pivot; upper_arm and
  forearm+hand as separate symbols per side (elbow pivot); torso pivots at hips
  for weight shift/lean; robe lower section as its own symbol so the "hips/knees"
  read through the robe drape (Ashes is robed — legs are under the robe in all
  library art; if no real leg parts exist, the gap gets LOGGED per gate 3, and
  weight shift is carried by torso lean + robe sway, never by sliding).
- Scene pose plan (72f, FIRST-SHOT-SPEC beats mapped to gate poses):
  rig/entrance pose -> anticipation lean -> ARMS-WIDE gesture on the line's
  stress (shoulder rotation + elbow bends) -> POINT toward camera/council ->
  settle into grin hold with weight shifted. Camera parallax push-in per spec.

## PART SET DECISION (2026-10-30)
The cut-apart lane's set LANDED first and is purpose-built: PRIMARY part set =
~/workspace/your_files/wizard-gang-part-libraries/_cut-apart/ashes/ (parts +
parts.json pivots + swaps/eyes both variants + swaps/mouths Mouth Set One).
Source: GMSS rig-proof 400x864 layers (his own art) — no generator-built packs used.
Inventory deliverable: agent-ops/fla-puppets-program-2026-10-30/ashes-inventory.md (200 PNGs).

## JOINT TRUTH TABLE (measured by cut-apart lane, parts.json — honesty gate)
- waist: REAL bend — torso/robe_skirt share a 30px overlap band of real pixels.
- wrist_R: REAL — hand_R segmented out of arm_R with full outline, lifts clean.
- neck: SMALL tilts only — head/robe meet edge-to-edge (0px overlap), wide turns gap.
- shoulders: MODERATE swings — arms are single drawn pieces IN FRONT of torso
  (z-order reads as overlap); big swings open a wedge at the chest edge.
- ELBOW: NO segment exists in the source art (crossed-arms pose). LOGGED GAP.
- HIPS/KNEES/LEGS: NO leg parts exist in any Ashes art. LOGGED GAP (inventory gap 9).
=> Scene motion is designed ONLY on real pivots: waist lean, shoulder raises,
   wrist lift, head tilt, skirt swing, braid lag, eye/mouth swaps. Point pose =
   arm_R shoulder raise + hand_R wrist lift + head tilt. No slide-faking.

## STEP 1 DONE (2026-10-30, verified on main)
FLA-PRODUCTION-STANDARD.md MERGED to TRIPPEDD main via PR #285 (merge verified:
contents API returns the file at 10,151 B; PR additions 169 / deletions 0).
Carries: GB-derived naming/settings/construction, required symbol sets (mouth
floor 12, eyes BOTH base-white + colourway), pivot rules, scene stack +
parallax, owner T-pose correction + real-motion gate in his words, joint truth
table requirement, build order (WG -> CJ own-art -> Mochiichao).
NOTE: two earlier background-exec handoffs falsely claimed a PR #277 existed;
direct verification showed nothing committed. Flow was redone in foreground
(commit c0b684b -> push -> PR #285 -> merge). CI status checks not readable
via this token (GraphQL scope) — docs-only 0-deletion merge proceeded per
MERGE-IT-YOURSELF law.


## STEPS 2+3 BUILT (2026-10-30 ~16:40-17:30 CDT) — Ashes FLA puppet + scene

BUILDER: ~/workspace/fla-build/build_ashes.py (authors XFL in the real Gumball
dialect — px-float instance matrices, transformationPoint per instance,
single-frame/firstFrame graphic addressing, labelled pose + face libraries).
RENDERER: ~/workspace/fla-build/fla_render.py — PIL compositor that EXECUTES the
authored FLA's own XML (nested symbols, firstFrame semantics, full matrices).
Why not the industry-lane renderer: its contract (renderer-contract.md) proves
it draws single leaf vector symbols only — no bitmaps/nesting. Validation of
the .fla files themselves = unzip round-trip (93/102 entries, testzip clean)
+ FlashXFLParser full parse. Frames shown to the owner are exactly the
transforms the .fla encodes — no separate cheat render.

PUPPET: WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla (6.1 MB)
- XFLParse: 18 library symbols, 36 symbol layers, 253 symbol frames, exit 0.
- Master WG_ASHES_FRONT_PUPPET = 13-frame labelled pose library: NEUTRAL,
  NEUTRAL_BLINK, ANTICIPATION, GESTURE_WIDE, GESTURE_TALK1/2, GESTURE_BLINK,
  POINT, POINT_HOLD, SETTLE, SETTLE_BLINK, REST_X, TRANSITION.
- HEADCOMP = 8 labelled face states (NEUTRAL, BLINK, TALK_1, TALK_2,
  TALK_WIDE, SMILE, LOOK_R, ANGRY). EYESCOMP = 12 frames (frame 0 = baked
  eyes; colourway pair swaps SMILE/LOOK_L/R/UP/DOWN/ANGRY registered at
  scale 1.0 offset (112,78), template-match diff 13.6 + visually verified;
  base-white pairs included as library frames 7-10). MOUTHCOMP = all 14
  Mouth Set One shapes as labelled library frames. BLINK = eye-closed
  lid textures from rig-layers 7/8 (registered full-canvas overlays).
- Mouth in scene = GRILL instance deform (scaleY open / scaleX widen about
  grill pivot (189,170)) — the same method as the original Ashes.inp
  (ParamMouthOpenY/Form). Set-One strip overlays were TESTED and FAILED
  registration (different aspect than the baked grill -> double-draw);
  they ship as library frames only. In-file note carries this.
- Eye base-white overlays FAILED visual verification over the baked
  colourway eyes (fringing/show-through). Library-complete per standard;
  scene uses colourway. V002 fix for both = clean face plate (head without
  baked eyes/grill) — does not exist in library. LOGGED GAP.

JOINT TRUTH — MEASURED FROM THE ART (supersedes optimistic assumptions):
- The source figure is a CROSSED-ARMS illustration. TORSO has NO pixels at
  rows 300-440; robe_full covers nothing above row ~460; the chest zone is
  covered ONLY by the two crossed arm slabs. Any mirrored shoulder spread
  opens a see-through chest seam (tested at +/-42, +/-28, +/-14 — all open).
- Shipped solution set (all real library art, no fabrication):
  (1) GESTURE = crossed-arms unit drop (+6px, x1.04 about shoulder pivots)
      + waist lean-back + head tilt + face change — reads as presenting
      settle, zero seams.
  (2) POINT = arm_R +65deg about shoulder (298,335) + wrist -15deg — the
      slab sweeps up in place, glove raises to head height.
  (3) FIGURE_UNDERLAY: the master's bottom layer is the complete base
      figure (rig-proof 00_base_full_figure.png, the very art the parts
      were cut from) following the torso transform — production safety
      underlay; guarantees no see-through seam can appear in any pose.
      Side effect disclosed: at POINT the underlay's rest glove faintly
      ghosts under the raised arm (reads as robe fold at scene scale).
- Poses verified OWN-EYES from compositor renders: neutral / gesture /
  point / settle all assemble clean, Ashes identity exact (void face,
  amber flame eyes, diamond grill, braids, chain). Pose stills in
  ~/workspace/fla-build/proof/pose_{0,3,7,9}.png.

SCENE: WG101ARRIVAL_Sc001_Clean_V001_ASH.fla (6.1 MB)
- XFLParse: 21 symbols, 39 layers, 256 frames, exit 0. 1920x1080 @24fps,
  72 frames, Gumball scene stack (audio/framecounter/fieldguide/FG plate/
  ASHES/BG mid/BG far/layout), puppet symbols COPIED in (never linked),
  Pipeline One parallax push-in (char scale 0.72->0.81, plates drift
  -10/-26/-70 on 2s). Pose beats per FIRST-SHOT-SPEC: neutral -> blink ->
  anticipation -> gesture+talk (grill deform lip-flap, demonstrative —
  voice is owner-gated, audio layer ships empty) -> point -> transition
  -> settle -> REST_X grin hold.
- BG plates are AUTHORED set dressing painted in-script (night skyline/
  rooftops/FG columns), labelled authored — not character parts, and NOT
  Foster's/Scooby art (their images are name/image-excluded; method only).
- Frames rendered: 53 of 72 (f000-f052) in ~/workspace/fla-build/proof/frames/.

## INCIDENT — SANDBOX EXEC WRITE BLOCK (2026-10-30 ~17:24 CDT, ongoing)
Mid-render, ALL content writes via exec/shell began failing with
PermissionError EPERM (file creation succeeds, content write/flush fails):
python PIL saves, plain open().write() of existing PNG bytes, cp, and
ffmpeg output all fail; dd wrote once early in the window. File-TOOL writes
(muse.write) still work. This is a runtime/sandbox layer block, not a disk
or code problem (disk 79%, files/partitions healthy; writes were fine at
17:21). Frames f053+ and the MP4 encode are BLOCKED on it, not on the
build. Retry plan: re-test exec write periodically; when it lifts, render
frames 53-71 (script ready), ffmpeg CRF17 encode, build frame strip
[0,12,20,32,44,56,66,71] + Gumball-vs-Ashes structure sheet, then report.
NOTHING was deleted or killed; all 53 rendered frames + both .fla + both
XFL trees + builder/renderer sources are intact on disk.
