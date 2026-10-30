# Wizard Gang — FLA Puppets + Rigs + Scene Files: Ashes Proof V001

First proof of the FLA puppets program (owner directive 2026-10-30: "We need to
make fla puppets and rigs and scene files for all our shows"). Standard:
`docs/wizard-gang/FLA-PRODUCTION-STANDARD.md` (on main, PR #285), distilled
from the owner's Gumball production files.

## Contents
- `WG101_ORIGINAL_PUPPET_ASHES_VERSION_001.fla` — Ashes puppet (modern .fla =
  zipped XFL; unzip to get the editable XFL tree: DOMDocument.xml + LIBRARY/).
  13-frame labelled pose library, HEADCOMP with 8 face states, EYESCOMP
  (colourway swaps + base-white set), MOUTHCOMP (14 Mouth Set One shapes),
  parts on real pivots from the library cut-apart set.
- `WG101ARRIVAL_Sc001_Clean_V001_ASH.fla` — scene to FIRST-SHOT-SPEC
  ("The wizards have arrived"): 1920x1080 @24fps, 72 frames, Gumball scene
  stack, puppet copied into scene library, Pipeline One parallax push-in.
- `tools/` — `build_ashes.py` (XFL authoring), `fla_render.py` (compositor
  that executes the .fla XML — the local leaf renderer cannot draw
  bitmap/nested files, see `docs/renderer-contract.md`), `finish_proof.py`
  (renders remaining frames, encodes MP4, builds proof sheets).
- `proof/` — pose stills (neutral / gesture / point / settle) rendered from
  the puppet .fla, and scene frames f000-f052 rendered from the scene .fla.
- `docs/` — Ashes part inventory (200 PNGs measured), Gumball puppet+scene
  dissection, XFL renderer contract. `PROGRAM-LOG.md` — full lane log.

## Validation (verified, not claimed)
- Both .fla: unzip round-trip clean; FlashXFLParser full parse, exit 0 —
  puppet 18 symbols / 36 layers / 253 frames; scene 21 symbols / 39 layers /
  256 frames.
- All character art is real library art (cut-apart set from GMSS rig-proof
  layers). Nothing redrawn or generated. BG plates in the scene are authored
  set dressing, labelled as such in the log.

## Known limits (logged honestly, see PROGRAM-LOG.md joint truth table)
- Source figure is a crossed-arms illustration: no elbow segment, no legs/
  hips/knees, and no chest drawn under the crossed arms. Gesture/point poses
  are designed on the real pivots only; a disclosed figure underlay (the
  complete base figure the parts were cut from) backstops seams.
- Mouth Set One strips and base-white eye overlays failed registration over
  the baked face — they ship as library swap frames; scene mouth is the
  grill deform (original Ashes.inp method). V002 needs a clean face plate.

## WIP at push time (owner pause order 2026-10-30)
Scene frames f053-f071, the MP4 encode, the frame-strip sheet and the
structure comparison sheet were mid-render when a sandbox write failure
blocked local file writes (see PROGRAM-LOG.md incident note). Run
`python3 tools/finish_proof.py` (paths inside are absolute to the build
workspace) to complete the proof package; it is idempotent and self-probes
for the write block.
