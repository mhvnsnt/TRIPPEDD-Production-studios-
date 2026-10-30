// TRIPPEDD Puppet Control Sheets (SPEC T-1) -- ToonzScript helper.
//
// What this does: exposes a pose's SUBSTITUTION drawings (mouth/eyes/
// hands) at a target frame, using the pose data from the scene's
// poses.json sidecar.
//
// What this deliberately does NOT do: move the controls. ToonzScript's
// Scene API can get/set xsheet cells but cannot read or write pegbar
// keyframes (see docs/TAHOMA2D-SURFACE-NOTES.md), so control poses are
// applied by copy/pasting the keyframes from the scene's pose block,
// per docs/CONTROL-SHEET.md section 2. This script covers the half
// ToonzScript can actually do.
//
// Use: in Tahoma2D, File -> Open Script Console, paste this file's
// contents, edit the CONFIG block (paste the substitution map for the
// pose from poses.json -- this package's generator prints it in the
// scene folder as poses.json), then run.

// ---- CONFIG -------------------------------------------------------------
var TARGET_FRAME = 0;            // 0-based xsheet row to expose at
var HOLD_FRAMES  = 4;            // how long the exposure holds
// part name -> drawing number for the pose (from poses.json / CONTROL-SHEET)
var SUBSTITUTIONS = {
    // "mouth": 1, "eyes": 1, "hand_r": 1
};
// part name -> xsheet column index (column order = part order in the
// character JSON used to generate the scene; column 0 is the first part)
var COLUMNS = {
    // "body": 0, "head": 1, "mouth": 2, "arm_r": 3
};
// -------------------------------------------------------------------------

var scene = new Scene();
for (var part in SUBSTITUTIONS) {
    var col = COLUMNS[part];
    if (col === undefined) { print("no column mapped for " + part); continue; }
    var cell = scene.getCell(TARGET_FRAME, col);
    if (!cell || !cell.level) { print("empty cell for " + part); continue; }
    for (var f = 0; f < HOLD_FRAMES; f++) {
        scene.setCell(TARGET_FRAME + f, col,
                      { level: cell.level, fid: SUBSTITUTIONS[part] });
    }
    print(part + ": exposed drawing " + SUBSTITUTIONS[part] +
          " at frame " + TARGET_FRAME + " (col " + col + ")");
}
