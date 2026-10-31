# Tahoma2D 1.6.3 surface investigation — what T-1 could honestly build on

Investigated at build time (2026-10-30) against the wired Tahoma2D
1.6.3 on this machine (`~/workspace/tools/tahoma2d/`) and the official
Tahoma2D/OpenToonz documentation. Verdict first:

> **There is no master-controller / custom-widget API in Tahoma2D.**
> The honest landing form for SPEC T-1 is Python-driven **scene-file
> generation** — exactly the fallback the spec's scope note predicted.
> The generator in this package is the deliverable, not a stopgap.

## What the surface actually offers

1. **ToonzScript** (in-app scripting; Tahoma2D docs, "ToonzScript"
   page). ECMAScript/QtScript, run via File → Run Script or the Script
   Console; scripts live in `tahomastuff/library/script/`. Its Scene
   API can: load/save a scene, get/set xsheet **cells**, insert
   columns, list levels, and render frames/scenes (Rasterizer /
   Renderer objects). It **cannot** create or edit pegbars, set
   keyframes, build Stage Schematic hierarchy, or register custom
   on-canvas widgets/sliders. So ToonzScript can *use* a rig (swap
   exposures, render) but cannot *build* one. This package ships one
   ToonzScript helper (`toonzscript/apply_pose_exposure.js`) that does
   the part ToonzScript is genuinely good at: exposing a pose's
   substitution drawings at a chosen frame from `poses.json` data
   pasted in by the animator.
2. **The `.tnz` scene file** — a text, XML-like format (not guaranteed
   well-formed XML: real Tahoma/OpenToonz scenes fail strict XML
   parsing, so tooling must scan tolerantly; Tahoma's own loader is the
   authority). Structure verified against real sample scenes
   (opentoonz_sample `cleanup.tnz` / `dwanko_run.tnz`): `<levelSet>`
   (levels with `$scenefolder`-relative paths), `<xsheet><columns>`
   (level columns with exposure cells + column FX), `<pegbars>` —
   named transform nodes with `<parent>` hierarchy and keyframable
   channels (`x`, `y`, `z`, `rot` [rotation], `sx`, `sy`, `sc`, `shx`, `shy`; keyframes as
   `<L>frame value</L>` with `<prev>` on later keys), and `<fxnodes>`.
   A column's pegbar (`Col<N>`) parented under another pegbar is how
   Tahoma itself expresses "this part rides that control" — the exact
   mechanism the T-1 convention standardizes.
3. **Headless CLI tools** in the install (`usr/bin/`): `tcomposer`
   (renders a `.tnz` to image sequences; `-frame`, `-range`, `-o`,
   `-TAHOMA2DROOT` qualifiers — verified working under `xvfb-run` on
   this box) and `tconverter` (image/level conversion). `tcomposer` is
   the validation authority for generated scenes: if it loads and
   renders the scene, Tahoma2D accepts the rig.
4. **Loader facts established the hard way during this build**
   (all verified against the Tahoma2D source + live runs):
   - On Linux the system paths come from
     `~/.config/Tahoma2D/SystemVar.ini`, key `TAHOMA2DROOT` -> the
     tahomastuff folder. It did not exist on this box, so the GUI
     stopped at an "Undefined or empty" dialog and tcomposer spun.
     Creating it (one line under `[General]`) fixed env init for both.
   - `tcomposer` must be given the scene as an **absolute path**: its
     project search walks up from the scene's parent folder, and a
     bare relative filename loops forever (parent of "" is "").
   - Stage-object ids: only `None`/`Table`/`Camera<N>`/`Peg<N>`/
     `Col<N>` (or a bare integer) parse; anything else becomes NoneId
     and the peg + its parenting are silently dropped
     (`toStageObjectId()` in tstageobject.cpp). Display names live in
     the pegbar's `<name>` child.
   - The rotation channel serializes as `<rot>`, not `<angle>`
     (TStageObject::loadData throws on `<angle>`); a level column
     likewise rejects a `<name>` child (TXshLevelColumn). Both errors
     were hit and fixed during the test loop in test-output/.
4. **Native rigging features** the convention builds on (present in
   1.6.3, per Tahoma2D docs): Stage Schematic peg hierarchy, Skeleton
   Tool, Plastic Tool, indexed palettes, drawing levels/substitutions
   on the exposure sheet. Master Controllers are a Harmony feature;
   no equivalent exists here — gap G-T1 in the build map is real.

## What was built on it

- A documented pegbar control convention (CONTROL-SHEET.md).
- A stdlib-only Python generator that emits a complete puppet scene
  (controls + hierarchy + part levels + pose-block keyframes +
  substitution exposures) from a character JSON, plus a `poses.json`
  sidecar.
- Per-show templates (Wizard Gang, 2D Cape Jones) sharing one layout.
- A tolerant structural validator, and tcomposer render evidence
  (test-output/).

## Addendum (2026-10-30, runtime fix lane) — the relative-path hang, reproduced and fixed

The proof-verification lane saw tcomposer hang twice (900 s timeouts)
on this kit's scene, stalling right after `Loading testpuppet`, while
the generator and validator passed. Root cause, reproduced live: the
invocation used a **relative scene path**. tcomposer's project search
walks up from the scene's parent folder and loops forever on a
relative path (the §2.4 note above); the log tail — plugin load
finished, `Loading testpuppet`, then nothing — is the signature.
With an absolute path the same scene renders in ~1–5 s.

Runtime state confirmed/fixed on the VM:

- `~/.config/Tahoma2D/SystemVar.ini` (`TAHOMA2DROOT` -> the
  tahomastuff folder) is present and correct; it is the file whose
  absence hung env init during the build (§2.4).
- The `varName:... TAHOMA2DROOT not set...` startup lines print in
  **successful** runs too — benign expander noise, not the failure.
- The box's tcomposer wrapper (`~/workspace/tools/tahoma2d/
  run-tcomposer.sh`) now rewrites any `.tnz` argument to an absolute
  path and exports `TAHOMA2DROOT`, so relative-path callers are safe
  through the wrapper. Full runtime notes:
  `~/workspace/tools/tahoma2d/WIRING.md`.
- Re-verified end to end after the fix: generator -> validator
  (RESULT: PASS, 0 FAIL) -> tcomposer frame 28 in 0.39 s; output
  md5 `10aad171...`, bit-identical to the wave frame recorded in
  test-output/VALIDATION-LOG.md. FUSE is not implicated (native
  extracted tree, unlike the OpenToonz flatpak).
