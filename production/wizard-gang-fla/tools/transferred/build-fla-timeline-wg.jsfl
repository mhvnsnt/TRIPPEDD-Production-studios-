// build-fla-timeline-wg.jsfl — Wizard Gang timeline builder
// ADAPTED 2026-11-02 from mhvnsnt/cape-jones cape-jones-rig/build-fla-timeline.jsfl
// under the owner's Cape Jones -> Wizard Gang transfer order (technique transfers;
// Cape Jones symbols/character parts do NOT — symbol set below is the Wizard Gang rig anatomy).
// STATUS: NOT run in Adobe Animate here (no Animate in this VM) — same status as the source.
// The proven build route in this repo is the Python XFL builder (tools/build_puppet.py);
// this JSFL is the in-Animate equivalent for when a scene is finished inside Animate.
//
// WHAT IT DOES:
//  1. Creates Graphic Symbols for the WG FRONT puppet anatomy:
//     HEADCOMP, TORSO, ROBE_SKIRT, ARM_L, ARM_R, CHAIN, EYESCOMP
//     (Ashes adds: BRAID_L, BRAID_R, MOUTHCOMP — his grill is canon, the other 8 are mouthless).
//     WG arms are SINGLE-PIECE in the source art (no upper/lower split exists — logged gap,
//     see docs/wizard-gang/CAPE-JONES-TRANSFER-INVENTORY-2026-11-02.md), so there are no
//     elbow symbols; legs do not exist in the art (robe to the floor), so no leg symbols.
//  2. Makes layers with those names, bottom to top in rig stack order.
//  3. For each keyframe in the clip JSON (paste the clip object below as CLIP),
//     inserts a keyframe at that frame number and sets each part's rotation
//     about its registered pivot (transformation point comes from the symbol).
// ANGLE CONVERSION (from the source file, kept verbatim as method):
//  Clip angles are screen angles: 0 = straight down, positive = toward screen-right,
//  end = joint + length * (sin(angle), cos(angle)).
//  Animate rotation is clockwise in degrees, with 0 = pointing right.
//  rotation = screenAngle - 90.
// Paste a clip object here: {frames:[{f:0, parts:{ARM_R:65, HEAD:5, TORSO:3.5}}, ...]}
var CLIP = {frames: []};
var SYMBOLS = ["ROBE_SKIRT","TORSO","ARM_L","ARM_R","CHAIN","HEADCOMP","EYESCOMP"];
function build() {
  var dom = fl.getDocumentDOM();
  if (!dom) { fl.trace("No document open."); return; }
  var lib = dom.library;
  for (var i = 0; i < SYMBOLS.length; i++) {
    if (!lib.itemExists(SYMBOLS[i])) lib.addNewItem("graphic", SYMBOLS[i]);
  }
  var tl = dom.getTimeline();
  // rename first layer, add the rest (bottom-to-top stack added in reverse)
  tl.layers[0].name = SYMBOLS[0];
  for (var j = SYMBOLS.length - 1; j >= 1; j--) tl.addNewLayer(SYMBOLS[j], "normal", false);
  for (var k = 0; k < CLIP.frames.length; k++) {
    var kf = CLIP.frames[k];
    for (var s = 0; s < SYMBOLS.length; s++) {
      var layer = tl.findLayerIndex(SYMBOLS[s])[0];
      tl.currentLayer = layer;
      tl.insertKeyframe(kf.f);
      if (kf.parts && kf.parts[SYMBOLS[s]] !== undefined) {
        tl.setSelectedFrames(0, kf.f, kf.f);
        var el = tl.layers[layer].frames[kf.f].elements[0];
        if (el) el.rotation = kf.parts[SYMBOLS[s]] - 90;
      }
    }
  }
  fl.trace("WG timeline built: " + CLIP.frames.length + " keyframes.");
}
build();
