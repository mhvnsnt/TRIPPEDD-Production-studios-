# Wizard-Rig-Proof Pack Wiring — God-Molecule-Show-Studio `tools/puppet/wizard-rig-proof/`

**Lane:** Phase 3 (i), Wizard Gang wire-up program, 2026-11-13
**Source repo:** `mhvnsnt/God-Molecule-Show-Studio`, path `tools/puppet/wizard-rig-proof/` (main, 685 entries, 257 MB per Oct 29 audit)
**Status:** 18 nijilive `.inp` puppets (9 standard + 9 battle) for all 9 cast members, stored-only, never wired into an episode.
**Companion index:** `WIZARD-RIG-PROOF-PACK-INDEX.json` (same folder, machine-readable per-pack record)
**Ground truth this doc is checked against:** FLA-PRODUCTION-STANDARD.md + WG-RIG-TEMPLATE.md (this repo, `docs/wizard-gang/`) and the Kiko v4/v005 package (PR #308, branch `wg/blairwitch-kiko-proof` — **OPEN, not merged, at time of writing**; cited by branch, not as main).

## 1. What the packs are

Per-character puppet builds from Oct 7 2026 (Waves 4–11, documented in `RIG_PROOF.md` + `RIG_PROOF_WAVE5–WAVE11.md` in the source repo). Each standard folder holds: one `.inp` (nijilive puppet, built with image2live2d), `parts/` (numbered part PNGs + `parts_manifest.json`), `rig_layers/` (finer split incl. closed-eye swaps), `proofs/` (pose renders + `rig_parameters.json`), and the build scripts (`extract_parts.py`, `cut_parts.py`, `build_rig.py`, `render_poses.py`, `validate_inp.py`). Battle folders mirror the structure for a single raised-arm/fist battle pose.

**Sources are group-shot crops, not isolated turnarounds.** Ashes was cut from one 400×864 crop of a group shot; Kiko from `kiko-tanaka-robed.webp` (1060×1945); Hollow standard from a 960×872 half-body bust; Onyx from a 390×960 crop. Neighbour removal was ~40% of the work (Ashes doc). No PSDs were ever produced (pytoshop write proved too low-level; the PNG layers + manifest serve the same purpose for a human rigger).

## 2. Verdicts

Two different bars — do not conflate them:

- **As nijilive puppets: ALL 18 USABLE as-is.** Every `.inp` was structurally validated by this lane in-memory (magic `TRNSRTS\0`, JSON payload parses, every parameter bound, `TEX_SECT` PNG textures decode): 9 standard + 9 battle, params 11–24, 2 physics rigs each, 10–18 animations each. Proof renders exist per pack. They are real, loadable puppets — usable for pose/expression reference, nijilive preview, and timing reference today.
- **As FLA part sources: ALL 18 NEED RE-CUT.** Every pack was cut by the same method — **ROI rectangles × HSV colour segmentation + OpenCV Telea inpainting** (verified in `cut_parts.py` for Kiko, Ashes, Cipher, Static, Onyx, Sombra, Theory, Echo, Hollow, Ashes-battle; the manifests state the method verbatim: "ROI x HSV color segmentation + Telea inpainting"). That is zone/colour partition cutting with straight geometric division (rectangular ROIs) — the exact method the outline-cut standard bans. The v4 Kiko recipe is the compliant method (`production/wizard-gang-fla/kiko-v4/parts.json`: "every part boundary follows a line drawn in the artwork itself… NO zone/region partition, NO square crops, NO invented pixels — joint overlaps are the neighbouring part's own source pixels tucked underneath"). No wizard-rig-proof pack meets it. Re-cut from the same crop sources (or better, isolated turnarounds) following the v4 recipe; the part inventory + param data below is the spec for that re-cut.
- **SUPERSEDED — do not use for FLA: Kiko standard.** Its stored textures contain the source street background plus black rectangular ROI holes (own-eyes + measured: composite is 64% opaque; figure mask leaks 21% into the top background corners; the same street + black rectangles appear in the `.inp` proof renders). Kiko's FLA source is v4/v005 (16 outline-cut parts, PR #308), not this pack.
- **BUST-ONLY — Hollow standard.** Source is a half-body bust; there is no lower body and no arms in frame. Usable as bust/face reference only; a full-body Hollow needs new source art, not a re-cut.

### Per-character verdict table (standard variants)

| Character | .inp (bytes) | Params | Mouth | Eyes | Arms | Textures | Anims | Parts (parts/) | FLA verdict |
|---|---|---|---|---|---|---|---|---|---|
| Ashes | `ashes/Ashes.inp` (1,919,651) | 24 | YES — ParamMouthOpenY/Form, grill | open/smile + closed swaps | 2 single-piece (no elbow) | 15 | 18 | 9: robe, head, braid_L/R, chain, arm_L/R, eyes, grill | NEEDS RE-CUT (richest pack; WG-RIG-TEMPLATE §6 already lists its 9 gaps) |
| Static | `static/Static.inp` (1,486,096) | 16 | none | open/smile + closed | 2 single-piece | 11 | 13 | 7: robe, head, arm_L/R, chain, eye_L/R | NEEDS RE-CUT |
| Cipher | `cipher/Cipher.inp` (1,709,526) | 16 | none | open/smile + closed | 2 single-piece | 11 | 13 | 7: robe, head, arm_L/R, chain, eye_L/R | NEEDS RE-CUT |
| Sombra Negra | `sombra/Sombra.inp` (1,110,313) | 12 | none | open/smile + closed | NONE (no arm parts, no arm params) | 7 | 11 | 5: robe, head, chain, eye_L/R | NEEDS RE-CUT + NEW SOURCE for arms (no arms exist to re-cut) |
| Kiko | `kiko/Kiko.inp` (3,862,859) | 18 | none | NONE — no eye params, no eye parts, no blink proof | 2 single-piece | 9 | 10 | 7: body, head, drape_L/R, chains, arm_L/R | SUPERSEDED by v4/v005 — do not use |
| Theory | `theory/Theory.inp` (1,481,099) | 16 | none | open/smile + closed | 2 single-piece | 11 | 13 | 7: robe, head, arm_L/R, chain, eye_L/R | NEEDS RE-CUT |
| Onyx | `onyx/Onyx.inp` (1,835,870) | 18 | none | open/smile + closed | 2 single-piece | 12 | 13 | 8 in manifest (robe, head, bell_L/R, arm_L/R, eye_L/R) + orphan `03_staff` + duplicate-numbered spares | NEEDS RE-CUT (clean the orphan/duplicate part files first) |
| Echo | `echo/Echo.inp` (1,545,719) | 16 | none | open/smile + closed | 2 single-piece | 11 | 13 | 7: robe, head, chain, arm_L/R, eye_L/R (eyes share index 06) | NEEDS RE-CUT |
| Hollow | `hollow/Hollow.inp` (1,574,288) | 12 | none | open/smile + closed | NONE (no arm parts, no arm params) | 9 | 11 | 5 in manifest (robe, head, eye_L/R) + orphan dupes `04_eye_L`/`05_eye_R`; source is a bust | BUST-ONLY + NEEDS NEW SOURCE for arms/body |

### Battle variants

| Character | .inp (bytes) | Params | Mouth | Eyes | Arms | Anims | Note |
|---|---|---|---|---|---|---|---|
| Ashes-battle | `ashes-battle/AshesBattle.inp` (1,631,048) | 21 | YES (grill) | open/smile + closed | R only (mid-dunk) | 18 | 13 textures; blink no-op found + repaired in Wave 11 |
| Static-battle | `static-battle/StaticBattle.inp` (1,429,150) | 14 | none | open/smile + closed | R only (claw machine) | 13 | 9 textures; no pendant in source, none grafted |
| Cipher-battle | `cipher-battle/CipherBattle.inp` (1,336,988) | 14 | none | open/smile + closed | L only (fist raised) | 13 | 9 parts |
| Sombra-battle | `sombra-battle/SombraBattle.inp` (1,128,244) | 12 | none | open/smile + closed | NONE | 11 | 7 textures; eyes but no arms |
| Kiko-battle | `kiko-battle/KikoBattle.inp` (1,436,407) | 14 | none | YES — eye layers + verified blink (unlike Kiko standard) | L only (fist raised) | 13 | 9 textures; white angular glint shards |
| Theory-battle | `theory-battle/TheoryBattle.inp` (1,318,734) | 14 | none | open/smile + closed | R only (fist raised) | 13 | 9 parts; `.inp` auto-splits the arm into a two-link FK (see §4) |
| Onyx-battle | `onyx-battle/OnyxBattle.inp` (1,225,437) | 14 | none | open/smile + closed | R only | 13 | 9 textures |
| Echo-battle | `echo-battle/EchoBattle.inp` (1,222,755) | 14 | none | open/smile + closed | R only (spray can) | 13 | 10 textures; thin Static-blue strip artifact on left edge (documented preview-renderer UV issue) |
| Hollow-battle | `hollow-battle/HollowBattle.inp` (1,094,846) | 11 | none | open/smile + closed | NONE | 11 | Eyes but no arms; bust-derived |

Battle variants are single-pose packs (one raised arm / prop), not general rigs. They inherit the same banned cut method, so they need re-cut for FLA use too — after the standard rigs, not before.

## 3. Face canon check (measured, not assumed)

- **Ashes keeps his diamond-grill grin in EVERY style: PASS.** Grill present in standard + battle parts, rig layers, and every proof render viewed; mouth params exist ONLY on Ashes (standard + battle). The build script deliberately skips the anime mouth-cavity synthesis so the grill IS the mouth. Eye glints are amber/flame — the FLA standard's flame/amber eye set.
- **The other 8 stay mouthless: PASS.** No mouth layers and no mouth params in any of the other 16 `.inp` files (8 standard + 8 battle). Their expression is carried by eyes/hands/movement, per canon.
- **Mismatch to log (not a canon break, a variant inconsistency): Kiko's eyes differ between variants.** Kiko standard has NO eye parts, NO eye params, NO blink proof — pure void face (2 bright star glints + faint starfield baked into the face plate, seen own-eyes). Kiko battle HAS eye layers and a verified blink. Do not "fix" standard Kiko by inventing eye art; the v4/v005 Kiko (glints baked into the head, no separate eye layers) is the canon reference for Kiko's eyes.
- **Ashes blink is real but tiny.** Pixel-diff of the committed renders: neutral-vs-blink changes 168 px, confined to the eye zone (y 95–138, x 276–535) — a genuine closed-eye swap, but the eye layers are ~100–200 px crumbs, so at full-figure scale the blink is barely visible. (Wave 11 found the same class of defect in Ashes-*battle* — blink was a 79 px no-op — and repaired it; standard Ashes was not repaired the same way.)

## 4. What the packs do NOT have (gaps stay gaps — nothing invented)

Applies to **all 9 standard packs** unless noted:

1. **No legs / hips / knees as separate parts.** Legs exist only as paint inside a fused plate where the source shows them (Kiko standard: full dragon-tights legs inside `01_body`; the rest: robes cover them). No hip/knee/ankle pivots in any wizard-rig-proof pack. (Contrast: Kiko v4 HAS thigh/shin/shoe + hip/knee/ankle pivots — see §6.)
2. **No elbows as drawn splits.** Arms are single-piece `arm_L`/`arm_R`. The `.inp` build auto-splits arms into a two-link FK mesh bend (documented in Wave 10 for Theory-battle) — that is a mesh deform, NOT a drawn elbow split, and does NOT satisfy the FLA joint-segmentation rule. No separate hands anywhere.
3. **No mouth sets.** Ashes has ONE grill drawing + a deform (ParamMouthOpenY/Form) — not a substitution set. The FLA floor is 12 core mouth drawings (Blair A–H, O_ROUND, WIDE, HOLD_POSE…); Ashes needs 14–16 drawn (WG-RIG-TEMPLATE §6). The other 8 need no mouth set by canon — their gap is eye-expression sets instead (only OPEN + SHUT exist; no HALF lids, no SMILE_01/ANGRY_01 expression library, no separate pupils).
4. **No walk/run cycles, no pose libraries.** Proof poses are neutral / head-turn / blink / comparison only. No STAND/GESTURE_WIDE/POINT/WALK library, no TQ/back/flop views (FRONT only).
5. **No PSDs, no nijigenerate GUI open.** The `.inp` files were validated structurally only (`validate_inp.py`); RIG_PROOF.md gap #1: the editor's first-run wizard could not be dismissed headless, so no `.inp` has ever been opened in nijigenerate. A human open of one `.inp` is still owed.
6. **Resolution.** Sources are 390–1060 px wide crops. WG-RIG-TEMPLATE gap 8 stands: soft at 1920×1080; keep characters ≤60% of frame height until parts are redrawn/re-cut at ≥2×.
7. **Known render artifacts (documented in the wave docs, re-confirmed own-eyes this lane):** black rectangular ROI holes + inpaint smears in proof renders (Ashes: black box at left edge, maroon block between robe panels; Kiko: large black rectangles top-left/top-right/between legs); Echo-battle thin Static-blue strip on the left edge (neighbour contamination from the group crop); preview-renderer head-turn breakdown past ~20° (`.inp` keyforms correct per Wave 10).
8. **Orphan/duplicate part files.** Onyx `parts/` holds 16 numbered PNGs for 8 manifest layers (`03_staff`, `04_bell_L`, `05_bell_R`, `06_arm_L`, `07_arm_R`, `08_eye_L`, `08_eye_R` are not in the manifest); Hollow `parts/` holds orphan dupes `04_eye_L`/`05_eye_R`; Kiko-battle `parts/` skips index 05. Clean before any re-cut consumes these folders. Kiko standard's cut inputs (`_clean_bgr.npy`, `_figmask.npy`) are NOT in the repo even though `cut_parts.py` loads them — the re-cut cannot be re-run from the committed tree as-is.
9. **No viseme/lip-sync data.** `assets/lipsync-map.json` in pocket-studio is schema-only (0 clips); nothing in wizard-rig-proof supplies visemes. Rhubarb/OpenFaceFX timing must still be built.

## 5. Proof this lane ran (measured, 2026-11-13)

- **All 9 standard `.inp` parsed in-memory** (raw.githubusercontent, no disk): magic `TRNSRTS\0`, JSON payload parses, params/nodes/animations/physics counted — Ashes 24p/18a/15tex, Cipher 16p/13a/11tex, Echo 16p/13a/11tex, Hollow 12p/11a/9tex, Kiko 18p/10a/9tex, Onyx 18p/13a/12tex, Sombra 12p/11a/7tex, Static 16p/13a/11tex, Theory 16p/13a/11tex; all 9 have 2 physics rigs and 9 nodes. Battle params read from `rig_parameters.json` (table §2); battle `.inp` structural validation rests on Wave 11's own re-validation pass (magic + JSON + bindings + texture decode for all six Wave 7–9 battles) and Wave 10's for the other three.
- **Pixel-diff of committed proof renders (in-memory PIL):** Ashes neutral-vs-blink 168 px changed, eye zone only (real swap, tiny); Ashes neutral-vs-head-turn-mouth-open 70,423 px changed, mean|diff| 26.3 (real pose change); Kiko neutral-vs-head-turn 126,139 px changed, mean|diff| 41.1 (real head/hood shift). None are no-ops.
- **Reassembly check:** Ashes `_composite_check.png` opaque pixels vs `_figmask.npy`: IoU 0.9988 (187,642 vs 187,870 px) — the cut parts reassemble to the cleaned figure essentially exactly. (Composite-vs-raw-crop diff is large by design: the raw crop contains neighbouring characters + background the cut deliberately removed.)
- **Own-eyes (8 images viewed):** Ashes neutral / blink / head-turn-mouth-open, Kiko neutral / head-turn, Ashes composite, Kiko composite, Kiko crop source. Ashes reads correctly (red flame robe, void face, grill, braids, chains, crossed arms, white glove) with the §4.7 artifacts visible. Kiko reads correctly as a figure (white fur hood/coat, void face with star glints, KIKO pendant + skulls/cross/compass, bare chest, dragon tights) but its renders carry the source street background + black rectangles — the reason for the SUPERSEDED verdict.
- **Disk note:** this lane's VM hit the quota wall mid-task (child-process writes >~5 KB failed EPERM with 36 GB df headroom; /tmp tmpfs 74% full). It cleared after a runtime restart; image downloads then succeeded. The PR below was landed via the GitHub git-data API (no clone), the same route Phase 2 used.

## 6. Old Nov 2 gap list vs reality — discrepancy list

The Nov 2 transfer inventory said: "no legs/hips/knees any character, no elbows, Sombra+Hollow no separated arms/hands, Kiko standard eyes = 4 sparkles only". Checked against the REAL v4/v005 data (PR #308 + `kiko-v4/parts.json`) and the wizard-rig-proof packs themselves:

| Old claim | Verdict | Reality |
|---|---|---|
| No legs/hips/knees, any character | **FALSE for Kiko v4; TRUE for wizard-rig-proof as separate parts** | Kiko v4 HAS thigh_L/R, shin_L/R, shoe_L/R with hip/knee/ankle pivots (16 parts, `kiko_v4_mapping.json`, Phase 2 verified). Wizard-rig-proof has NO separate leg parts for any character — but Kiko standard's torso plate DOES contain fully painted legs (dragon tights), and Hollow standard's source is a bust (no legs in frame). The claim conflated the two sources. |
| No elbows | **FALSE for Kiko v4; TRUE for wizard-rig-proof as drawn splits** | Kiko v4 HAS upper_arm/forearm/hand with shoulder/elbow/wrist pivots. Wizard-rig-proof arms are single-piece; the `.inp` auto-split FK bend is a mesh deform, not a drawn elbow. |
| Sombra + Hollow: no separated arms/hands | **TRUE for wizard-rig-proof; UNVERIFIED for the FLA v1s** | Both characters have no arm parts and no arm params in standard AND battle wizard-rig-proof packs. Whether the FLA v1 puppets (`WG104_ORIGINAL_PUPPET_SOMBRA_VERSION_001.fla`, `WG109_ORIGINAL_PUPPET_HOLLOW_VERSION_001.fla`, on main) carry arms was NOT checked in this lane — the 90 MB .fla downloads were blocked by the quota wall. Open check for a follow-up lane. |
| Kiko standard eyes = 4 sparkles only | **WRONG — there are no sparkle eye files at all** | Wizard-rig-proof Kiko standard has ZERO eye parts, ZERO eye params, NO blink proof — pure void face with star glints baked into the face plate (2 bright glints + faint starfield seen own-eyes). Kiko v4 likewise has NO separate eye layers (glints baked into the head; `parts.json` `occluded_gaps`). The "4 sparkles" count matches neither pack. (Kiko *battle* does have separable eye layers + blink — the only Kiko variant that does.) |

## 7. What this fills for EP02 (Phase 1 ground truth)

Phase 1 (`phase1-ep02-state.md`): EP02 v8b (344.81 s) exists as a finished render + complete audio timeline, but has **no rigs/viseme data and no visual source assets** — no script, no shot list, no stills/frames/character art, no full-res master, no WAV stem masters, and the project file's "viseme sheets for all 8 characters in character-rigs/" is false in-repo.

These packs fill:
- **Character visuals for all 9 cast members** — posed stills / reference renders from the `.inp` files (neutral, head-turn, blink, comparison proofs exist per pack). This is the first in-repo visual source material for the EP02 cast as rigged characters.
- **A pose/expression reference system** — head AngleX/Y/Z, body angles, arm raises, breath, eye open/smile params per character (counts in §2). Usable as the timing/posing reference for rebuilding EP02 shots as real animation.
- **Ashes' mouth** — the only mouth in the program (grill deform). EP02's Ashes lines (ritual whisper 75 s, L7 "War fund!" 113 s) are the only dialogue these packs can lip-read at all, and only as a deform, not a viseme set.

These packs do NOT fill:
- **Viseme/lip-sync data for EP02 dialogue.** Static (7 lines), Cipher (4), Onyx (1), Sombra (1), Kiko (1) have no mouth art of any kind in these packs. No Blair A–H, no substitution sets, no Rhubarb output. The mouth sets in WG-RIG-TEMPLATE §4 still need to be drawn.
- **Legs/walk cycles, hands, pose libraries, TQ/back views, scene/BG art, or any EP02 shot/sequence data.** EP02's 20 audio-defined scenes (s10–s29) still have no visual shot list; these packs supply characters, not scenes.
- **The EP02 master or stems.** Unrelated — the packs are a V2 rebuild path for EP02 visuals, not a patch onto the v8b render. EP02 v8b's first 50 s stays locked; any rebuild starts after it.
- **Echo, Theory, Hollow dialogue.** They have packs but zero EP02 lines — the packs don't change that; they only make those characters animatable when lines exist.

## 8. Wire-up order (recommended next steps, not done here)

1. **Kiko:** use v4/v005 (PR #308) — do not touch wizard-rig-proof Kiko standard again except as a negative example.
2. **Ashes first** (FLA program order): re-cut Ashes from the crop source (or a cleaner isolated turnaround when one exists) with outline cuts per the v4 recipe; then draw the §4 mouth set (14–16 grill drawings) — it is the lip-sync system and the blocking gap (WG-RIG-TEMPLATE §6).
3. **Then Static / Cipher / Theory / Onyx / Echo** (have arms + eyes; re-cut + HALF lids + expression library + pupils).
4. **Sombra + Hollow last** — arms don't exist in any source; new arm art must be drawn (owner-approved source or drawn to canon), then re-cut. Hollow also needs a full-body source (current source is a bust).
5. **Battle variants** after the standard rigs — they are pose packs, and their re-cut inherits the standard re-cut.
6. **Human open of one `.inp` in nijigenerate** (RIG_PROOF.md gap #1, still open since Oct 7) to close the editor-load question.
7. **Open check:** dissect `WG104`/`WG109` v1 FLAs for Sombra/Hollow arms (see §6).

## 9. Sources

- `mhvnsnt/God-Molecule-Show-Studio` — `tools/puppet/wizard-rig-proof/` (main): `RIG_PROOF.md`, `RIG_PROOF_WAVE5–WAVE11.md`, `SETUP_WIZARD_WAVE7/9.md`, per-character `parts_manifest.json`, `proofs/rig_parameters.json`, `cut_parts.py`, `build_rig.py`, `validate_inp.py`.
- `mhvnsnt/TRIPPEDD-Production-studios-` — `docs/wizard-gang/FLA-PRODUCTION-STANDARD.md`, `WG-RIG-TEMPLATE.md`; `production/wizard-gang-fla/kiko-v4/parts.json` + `MC105ORIGINAL_PUPPET_KIKO_VERSION_005/kiko_v4_mapping.json` (PR #308, branch `wg/blairwitch-kiko-proof`).
- Oct 29 audit: `~/workspace/agent-ops/wizard-gang-real-anim-repo-audit-2026-10-29.md` (rank 1, 10/10).
- Phase 1 EP02 state: `~/workspace/_wizard-gang-wireup-20261113/phase1-ep02-state.md`.
- Phase 2 checkpoint: `~/workspace/_wizard-gang-wireup-20261113/phase2-blairwitch-kiko/CHECKPOINT.md` (v4 truth: 16 parts, pivots, `occluded_gaps`).
- This lane's checkpoint: `~/workspace/_wizard-gang-wireup-20261113/phase3i-rig-proof/CHECKPOINT.md`.
