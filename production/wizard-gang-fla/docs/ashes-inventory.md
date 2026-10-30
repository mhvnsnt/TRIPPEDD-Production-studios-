# ASHES — Full Part Inventory, Mapped to Puppet Symbol Slots

**Date:** 2026-10-30 · **Scope:** Ashes ONLY (`ashes/` + `ashes-battle/`). No other character's folder was inventoried.
**Library root:** `~/workspace/your_files/wizard-gang-part-libraries/`
**Method:** every PNG measured with PIL (dimensions, mode, alpha extrema, % fully-transparent / % fully-opaque). Ambiguous files were opened and viewed (marked 👁 below). Sources read first: top-level `INDEX.md`, `ashes/INDEX.md`, `ashes-battle/INDEX.md`, both `rig-proof/parts_manifest.json`.
**Totals:** `ashes/` = **136 PNGs**, `ashes-battle/` = **64 PNGs** (200 total, incl. contact/verify sheets), plus 2 `.inp` puppet files and 2 manifests.

## How to read the alpha classes

| Class | Meaning |
|---|---|
| **CUTOUT** | RGBA, real transparent background; canvas ≈ part bbox + margin. Puppet-ready as-is. |
| **FULL-CANVAS TEXTURE** | RGBA on the full source frame (400×864 std / 780×885 battle). Alpha isolates ONLY the part, in its assembled position — this is the GMSS `.inp` texture format. The RGB under the transparent area is the *full illustration* (per top INDEX method note), so a viewer that ignores alpha shows the whole character; an alpha-correct compositor shows only the part. Puppet-usable, but NOT a tight cutout — crop to the alpha-bbox given in Appendix C. |
| **FULL-FRAME (no alpha)** | RGB, 100% opaque. The part is shown *in situ* with the character/scene behind it. Reference only — not a puppet part without a new extraction. |
| **SHEET** | Contact/verify/proof sheet, RGB. Not a part. |

**Colourway note (correction to the INDEX wording):** `ashes/INDEX.md` calls the shipped eye colourway "red/black graphic." Viewed 👁, the standard eyes are actually **amber/orange almond eyes with a white flame-shaped core**; the battle eyes are **flat yellow slits**. The base-white sets exist as documented (white RGB, luminance folded into alpha — they render near-invisible on a white background, which is expected).

---

## 1. SLOT MAP — best source per puppet symbol slot (WG-RIG-TEMPLATE)

Paths are relative to the library root. "Best" = tightest real cutout of Ashes' own art first; pack art and full-frame references are demoted and labelled.

| Slot | Best source (own-art cutout) | Dims / class | Alternates / notes |
|---|---|---|---|
| **robe_body** | `ashes/rig-proof/parts/01_robe.png` (texture) | 400×864 FULL-CANVAS TEXTURE, alpha-bbox (15,270)–(330,864) | The ONLY extracted own-art robe. 👁 Robe + crossed lower sleeves with gold flame motifs; head area is an inpainted black void; background ghosting lives in the transparent RGB. No tight-cropped extracted robe exists in `ashes/robe/` — that folder is pack art only. |
| **robe_front** | `ashes/robe/WG_ASHES_FRONT_ROBE_FRONT.png` ⚠ PACK | 660×920 CUTOUT | Parametric pack robe (red, V-collar, sash, flame-point hem), sleeveless — sleeves are separate pack files. No extracted front/back split exists; the extracted robe (above) is a single front-facing layer. |
| **robe_back** | `ashes/robe/WG_ASHES_FRONT_ROBE_BACK.png` ⚠ PACK ONLY | 660×920 CUTOUT | **No extracted robe back anywhere** — see GAPS. |
| **head / face plate** | `ashes/head-hood/WG_ASHES_FRONT_HEAD_HOOD_UP.png` | 294×269 CUTOUT | 👁 Combined unit: red flame hood + black void face + eyes + grill + braid tops + chain top + robe shoulders. It serves as head AND face plate because the source stores them as one. `FACE_PLATE.png` is **not on disk** in standard (INDEX logs it as a byte-duplicate, SKIP). No face-only (hoodless) plate exists — see GAPS. |
| **hood** | (same file as head, above) | 294×269 CUTOUT | No hood-only separation exists anywhere; hood is fused with face/braids in every source. Battle: `ashes-battle/head-hood/WG_ASHES_FRONT_HEAD_HOOD_UP.png`, 179×182 CUTOUT 👁 (dunk-pose head, braids flying horizontal, yellow slit eyes + yellow grill, `$` chain; minor night-sky remnants at corners). |
| **hood_down** | — NONE — | — | **GAP** (see §3). |
| **braid_L** | `ashes/hair-accessories/WG_ASHES_FRONT_BRAID_L.png` | 109×246 CUTOUT | 👁 Gold braid; the file's RGB frame also contains robe/face surround (alpha isolates the braid). Texture form: `ashes/rig-proof/parts/03_braid_L.png` (alpha-bbox (85,170)–(178,400)). Battle: 78×227 CUTOUT. |
| **braid_R** | `ashes/hair-accessories/WG_ASHES_FRONT_BRAID_R.png` | 94×243 CUTOUT | Texture form: `rig-proof/parts/04_braid_R.png` (bbox (222,170)–(300,397)). Battle: 77×224 CUTOUT. |
| **chain / accessory** | `ashes/hair-accessories/WG_ASHES_FRONT_CHAIN.png` | 100×136 CUTOUT | 👁 Gold chain + pendant letters, hanging between the braids (braid edges visible in RGB; alpha isolates chain). Texture form: `rig-proof/parts/05_chain.png` (bbox (158,225)–(242,345)). Battle: 88×130 CUTOUT. That is the only accessory class for Ashes — no other accessory part exists. |
| **arm_L** | `ashes/arms/WG_ASHES_FRONT_ARM_L_REST.png` | 209×181 CUTOUT | 👁 Crossed-arms pose segment: red sleeve mass with braid + chain-letter fragments overlapping — it is a slice of the crossed-arms illustration, NOT a free-hanging arm. Only pose that exists (REST/crossed). Battle: **no arm_L at all** — GAP. |
| **arm_R** | `ashes/arms/WG_ASHES_FRONT_ARM_R_REST.png` | 139×181 CUTOUT | Crossed-arms segment, includes the white hand area. Battle: `ashes-battle/arms/WG_ASHES_FRONT_ARM_R_REST.png`, 151×353 CUTOUT 👁 — despite the "REST" name this is the **raised overhead dunk arm** (red sleeve + white glove hand + basketball at top; night scene in RGB surround). Filename lies about the pose. |
| **hand sets — real extracted** | `ashes/hands/WG_ASHES_FRONT_HAND_R_REST_ON_ARM.png` | 79×61 CUTOUT | 👁 White glove hand resting on the red sleeve — the **only** extracted own-art hand, **only R, only REST**. Battle twin: 69×69. **No extracted hand_L, no other extracted pose** — GAP for a real pose library. |
| **hand sets — pack gloves** ⚠ | `ashes/hands-gloves/WG_ASHES_FRONT_GLOVE_<POSE>_<L\|R>.png` ×20 | 306–426 px wide CUTOUTs | 10 poses × L/R: REST, OPEN, WAVE, FIST, POINT 👁 (clean white glove, cuff line), GRAB, THUMBS_UP, PEACE, FINGER_GUN, PINCH. PIL-parametric pack art (owner verdict 2026-10-29: homemade look, acceptable only if nothing better exists). Shared real-drawn candidate sets (Gumball/Nicole/Pim/Charlie) live in `_candidates/` per the top INDEX — outside the Ashes folders, not inventoried here. |
| **hand sets — approved pack** | `ashes/ashes-approved-pack/hands/*.png` ×10 | 1600×1600 (pointing 1920×1280), FULL-FRAME, no alpha | 👁 Real drawn **brown skin** hands (pointing viewed: hand fills frame on flat white). Poses: beckoning, counting, fist, gripping, holding, open-palm, pointing, relaxed, shaka, thumbs-up. Different design language from the void-face puppet (skin, not glove) and no alpha — reference / re-extraction source only. |
| **eye_L / eye_R — colourway** | `ashes/eyes/WG_ASHES_FRONT_EYE_L_OPEN.png` / `…_R_OPEN.png` | 62×60 / 64×59 CUTOUT | 👁 Amber almond + white flame core — filenames verified TRUE (they really are eyes). ⚠ The L_OPEN single carries a small red hood-with-flame fragment in its top-left corner in RGB; the PAIR files are the cleaner stock. |
| **eye lids — half** | `…_EYE_L_HALF.png` / `…_EYE_R_HALF.png` | 62×60 / 64×59 CUTOUT | Edited half-lid squash of OPEN (per INDEX), not a separate extraction. Battle twins: 42×27 / 34×25. |
| **eye lids — shut** | `…_EYE_L_SHUT.png` / `…_EYE_R_SHUT.png` | 68×34 each CUTOUT | 👁 L_SHUT is a single orange curved lid line — minimal but real, extracted from the closed-eye layers. Battle twins: 39×21 / 33×20. |
| **pupils (separate)** | `…_PUPIL_L.png` / `…_PUPIL_R.png` | 24×19 each CUTOUT | 👁 Edited bright-core crop of OPEN (orange surround + white flame core) — a "pupil" only in the loose sense; Ashes' eye has no anatomical pupil. Battle twins: 33×18 / 26×16. |
| **eye pairs + expressions** | `…_EYE_PAIR_OPEN.png` + LOOK_L / LOOK_R / LOOK_UP / LOOK_DOWN / SMILE / ANGRY | 152×76 (ANGRY 151×76) CUTOUT | 👁 PAIR_OPEN verified: both amber eyes at native spacing. LOOK_* are pupil-shift edits; SMILE = crescent mask edit; ANGRY = shear edit. Battle pairs: same 7 states at 76×27 (yellow slits). |
| **eyes — base-white variant** | `ashes/eyes/base-white/` — all 15 files, same names | same dims as colourway, CUTOUT | Complete mirror set: L/R × (OPEN/HALF/SHUT), PUPIL L/R, all 7 pairs. Battle base-white: complete 15 in `ashes-battle/eyes/base-white/`. |
| **eyes — approved pack** | `ashes/ashes-approved-pack/eyes/*.png` ×6 | 1600×1600 FULL-FRAME, no alpha | 👁 Full-face close-ups in a DIFFERENT design (red hood with gold Celtic-knot trim, glowing white/crescent eyes, **no grill visible**): neutral (white slits), happy (gold crescents), angry, blink, sad, surprised. Expression reference only; not swappable onto the standard puppet. |
| **mouth / grill swap set** | `ashes/mouths/set-one/` — **Mouth Set One, 14 shapes** (full list §2) | CUTOUT (two construction families, see §2) | 👁 Verified real gold grill mouths (X_REST, WIDE, B viewed). Plus rig-proof in-situ grill: `parts/09_grill.png` texture (bbox (115,155)–(264,185)) and `rig-layers/9_mouth_cavity.png` 👁 (small oval open-mouth cavity — white/brown/tan — that sits BEHIND a grill; not a grill itself). Approved visemes ×10 are FULL-FRAME and a different (human, bearded) design 👁 — not usable on the void-face puppet. |
| **legs / feet** | — no own-art part — | — | **GAP.** Standard design is robe-covered to the floor. Battle figure *shows* black pants + sneakers, but only inside the assembled figure — never separated. Only foot stock: ⚠ pack shoes `ashes/feet/WG_ASHES_FRONT_SHOE_L/R/PAIR.png` (300×190 / 624×190 CUTOUT 👁 generic dark-red cartoon shoes, side view). |
| **robe sleeves (pack)** ⚠ | `ashes/robe/WG_ASHES_FRONT_SLEEVE_L.png` / `…_R.png` | 366×566 CUTOUT | Pack arm solution: sleeve + glove = complete arm. No extracted standalone sleeve exists (extracted arms are crossed-pose segments). |
| **energy-ball / battle prop** | `ashes-battle/rig-proof/parts/07_ball.png` | 780×885 FULL-CANVAS TEXTURE, alpha-bbox (423,36)–(532,153) | **CORRECTION:** 👁 this is a **basketball** (orange, black seams) — Ashes' battle variant is a mid-dunk basketball pose. There is **no energy-ball part for Ashes**; the green energy orb in the battle source scene belongs to the neighbouring character at the frame's left edge. No tight cutout of the ball exists — texture only. |

## 2. Mouth Set One — every shape (`ashes/mouths/set-one/`)

All 14 verified CUTOUT (RGBA). Two construction families:
**Family T (teeth grin, semi-transparent gold, ~15–18% fully opaque + ~30% partial alpha):** A, B, BARE_TEETH, C, F, G, HOLD_POSE, SMUG, WIDE, X_REST.
**Family C (black mouth-cavity disc with gold teeth at the rim, 76% opaque, ~315 px wide):** D, E, H, O_ROUND. 👁 D and E viewed: black oval cavity, gold teeth top/bottom — these read as open-mouth shapes, not plain grins.

| File | Dims | Shows |
|---|---|---|
| WG_ASHES_MOUTH_A.png | 329×35 | 👁 Thin closed gold-teeth strip |
| WG_ASHES_MOUTH_B.png | 329×97 | 👁 Gold grill grin, two rows |
| WG_ASHES_MOUTH_BARE_TEETH.png | 336×136 | Bared gold grill grin |
| WG_ASHES_MOUTH_C.png | 376×115 | Gold grill grin (widest of the strip family except WIDE) |
| WG_ASHES_MOUTH_D.png | 315×292 | 👁 Family C cavity disc, tall |
| WG_ASHES_MOUTH_E.png | 315×204 | 👁 Family C cavity disc |
| WG_ASHES_MOUTH_F.png | 168×129 | Small gold grill shape (smallest file in the set) |
| WG_ASHES_MOUTH_G.png | 336×100 | Gold grill grin |
| WG_ASHES_MOUTH_H.png | 315×224 | Family C cavity disc |
| WG_ASHES_MOUTH_HOLD_POSE.png | 336×146 | Gold grill hold grin |
| WG_ASHES_MOUTH_O_ROUND.png | 315×244 | Family C cavity disc (round-O) |
| WG_ASHES_MOUTH_SMUG.png | 352×136 | Smug gold grill grin |
| WG_ASHES_MOUTH_WIDE.png | 436×144 | 👁 Widest gold grill grin in the set |
| WG_ASHES_MOUTH_X_REST.png | 336×136 | 👁 Rest gold grill grin (the default — Ashes' grin stays on 100% of the time per owner canon) |

**Approved-pack visemes (FULL-FRAME, no alpha, different human design 👁):** viseme-ah 1760×1440 (open mouth, gold fang grill, bearded face close-up), viseme-ee 1760×1440, viseme-closed 1600×1600, viseme-oo 1600×1600, viseme-fv / -l / -mbp / -oh / -rest / -snarl 1728×1408 each.

## 3. GAPS — slots with NO usable real part (logged, no substitutes proposed)

1. **hood_down** — no hood-down head exists in any Ashes source. Total gap (standard + battle).
2. **Face plate separate from hood** — standard ships only the fused HEAD_HOOD_UP (FACE_PLATE logged as duplicate, not on disk). No hoodless void-face plate, no hood-only shell. Battle ships both filenames (179×182 each, hashes differ) but both are the same fused head unit — still no separation.
3. **robe_back (extracted)** — no back view of the robe (or of ANY part: no TQ/BACK view exists for Ashes at all). Only the parametric pack ROBE_BACK fills the slot.
4. **Tight extracted robe_body** — the extracted robe exists ONLY as a full-canvas `.inp` texture (`01_robe.png`, with inpainted head void and crossed sleeves baked in). No tight-cropped, sleeve-free extracted robe cutout.
5. **arm_L — battle variant** — battle source has one arm only (the raised dunk arm). No battle arm_L.
6. **Arm pose swaps** — only ONE arm pose exists per side: crossed/REST (standard) and raised-dunk (battle R). No arms-wide, no pointing, no lowered free arm as extracted parts. (Pack sleeves are the only alternate arm covering.)
7. **hand_L — extracted own-art** — none. The only extracted hand is R/REST (79×61). Every other real-pose hand stock is either pack gloves (parametric) or the approved pack's full-frame brown-skin hands (no alpha, different design).
8. **Extracted hand pose library beyond REST** — zero additional extracted poses (POINT/FIST/etc. exist only as pack gloves or full-frame approved frames).
9. **Legs** — no leg part of any kind, either variant. (Battle shows pants+sneakers only inside the assembled figure.)
10. **Feet — own-art** — no extracted shoe/foot. Battle's sneakers were never separated. Only generic pack shoes exist.
11. **Ball as a tight cutout** — the basketball exists only as a full-canvas texture layer (`07_ball.png`); no cropped ball PNG. (And no energy-ball part exists at all — see slot map correction.)
12. **Eyebrows** — none, by design (void face; expression is carried by eyes/hands/movement per owner canon). Logged for completeness.
13. **Resolution** — standard-variant own-art tops out at the 400×864 source frame (eyes 62 px, grill ~150 px wide). No hi-res version of any extracted standard part exists. Battle eyes are smaller still (pair 76×27).
14. **Assembled arms-wide pose** — no full-body reference in that pose exists (see §4).

## 4. Assembled full-body pose references

| File | Dims / class | Pose |
|---|---|---|
| `ashes/rig-proof/parts/00_base_full_figure.png` | 400×864 FULL-CANVAS TEXTURE (figure alpha-isolated; RGB shows the alley scene) | **Neutral, arms crossed** — the canonical standard reference |
| `ashes/rig-proof/proofs/ashes_pose_neutral.png` | 864×864 CUTOUT (transparent bg) 👁 | Neutral, arms crossed, assembled puppet |
| `ashes/rig-proof/proofs/ashes_pose_blink.png` | 864×864 CUTOUT | Same pose, blink state |
| `ashes/rig-proof/proofs/ashes_pose_head-turn_mouth-open.png` | 864×864 CUTOUT | Same pose, head-turn + mouth-open state |
| `ashes/rig-proof/proofs/ashes_pose_comparison.png` | 2592×864 SHEET (RGB) 👁 | Triptych of the three states above |
| `ashes/rig-proof/root/ashes_crop_source.png` | 400×864 FULL-FRAME (RGB) | The original source illustration (crossed arms, alley background) |
| `ashes-battle/rig-proof/proofs/ashes_battle_pose_neutral.png` | 864×864 CUTOUT 👁 | **Mid-dunk, arm raised holding basketball** — the only raised-arm assembled reference; some fence-pixel remnants at the legs |
| `ashes-battle/rig-proof/proofs/ashes_battle_pose_blink.png` / `…_blink_opacity.png` | 864×864 CUTOUT ×2 | Dunk pose, blink variants (hashes differ; near-identical) |
| `ashes-battle/rig-proof/proofs/ashes_battle_pose_head-turn_mouth-open.png` | 864×864 CUTOUT | Dunk pose, head-turn state |
| `ashes-battle/rig-proof/proofs/ashes_battle_pose_comparison.png` | 1200×840, RGBA ~98% opaque | Battle state comparison sheet |
| `ashes-battle/rig-proof/parts/00_base_full_figure.png` | 780×885 FULL-CANVAS TEXTURE 👁 | Source group scene: Ashes mid-dunk at right; other characters + court in RGB — crop to alpha before any use |
| `ashes-battle/rig-proof/root/ashes_battle_crop_source.png` | 780×885 FULL-FRAME (RGB) | Original battle source scene |

**No arms-wide assembled figure and no pointing assembled figure exist** in either variant. The pointing references that exist are part-level only: pack `GLOVE_POINT_L/R` and the approved full-frame `hand-pointing.png`.

## 5. rig-proof/ — the primary puppet-building stock (exact texture list)

### Standard — `ashes/rig-proof/` (puppet file: `Ashes.inp`, 1,919,651 B, nijilive/Inochi2D data)
Source frame 400×864 (`ashes_crop_source.png`). Stack bottom→top per manifest: robe, head, braid_L, braid_R, chain, arm_L, arm_R, eyes, grill. Method: HSV segmentation + Telea inpainting.

`parts/` — all 400×864 FULL-CANVAS TEXTUREs:
| File | Alpha-bbox (the actual part) | Part pixels (manifest) |
|---|---|---|
| 00_base_full_figure.png | (6,17)–(332,864) | full figure |
| 01_robe.png | (15,270)–(330,864) | 94,036 |
| 02_head.png | (50,17)–(328,270) | 45,678 |
| 03_braid_L.png | (85,170)–(178,400) | 5,317 |
| 04_braid_R.png | (222,170)–(300,397) | 2,467 |
| 05_chain.png | (158,225)–(242,345) | 4,062 |
| 06_arm_L.png | (15,295)–(208,460) | 28,387 |
| 07_arm_R.png | (208,295)–(332,460) | 18,206 |
| 08_eyes.png | (115,95)–(270,142) | 1,332 |
| 09_grill.png | (115,155)–(264,185) | 1,854 |
| _composite_check.png | (15,17)–(332,864) | recomposited stack check (not a part) |

`rig-layers/` — all 400×864 FULL-CANVAS TEXTUREs, near-total transparency except the part:
07_eye_l.png (bbox (128,95)–(174,139)) · 08_eye_r.png ((200,95)–(248,138)) · 7_eye_closed_l.png ((125,114)–(177,132)) · 8_eye_closed_r.png ((198,114)–(250,132)) · 9_mouth_cavity.png 👁 ((129,149)–(250,232), oval cavity behind the grill).

`proofs/`: the 4 assembled renders + comparison in §4, plus 2 editor screenshots (1280×800 RGB, not parts): `nijigenerate_editor_gui-blocked.png`, `nijigenerate_editor_gui-fixed.png`.

### Battle — `ashes-battle/rig-proof/` (puppet file: `AshesBattle.inp`, 1,631,048 B)
Source frame 780×885, mid-dunk pose, one arm only (manifest's own note). Stack: robe, head, braid_L, braid_R, chain, arm, **ball**, eyes, grill.

`parts/` — all 780×885 FULL-CANVAS TEXTUREs:
00_base_full_figure.png ((413,35)–(780,801)) · 01_robe.png ((413,42)–(780,801), 88,783 px) · 02_head.png ((585,152)–(748,318), 22,193 px) · 03_braid_L.png ((588,224)–(650,435), 3,034 px) · 04_braid_R.png ((700,224)–(761,435), 2,232 px) · 05_chain.png ((642,268)–(714,382), 1,328 px) · 06_arm.png ((453,95)–(588,432), 17,805 px — the single raised arm) · **07_ball.png ((423,36)–(532,153), 8,687 px — basketball)** · 08_eyes.png ((640,196)–(698,207), 289 px) · 09_grill.png ((652,222)–(698,264), 804 px) · _composite_check.png.

`rig-layers/` — all 780×885: 01_face_base.png ((585,152)–(748,318) — same bbox as 02_head) · 07_eye_l.png · 08_eye_r.png · 7_eye_closed_l.png · 8_eye_closed_r.png. (No mouth-cavity layer in battle.)

**What battle adds over standard:** the basketball prop layer, a raised-arm pose, a dunk-pose head with horizontal braids, yellow-slit eyes + yellow grill colourway, visible pants/sneakers in the assembled figure, and a second complete eye set (colourway + base-white) at much smaller size. It does NOT add: arm_L, mouths, gloves/robe/feet packs (shared from standard per its INDEX), or any energy effect.

## 6. ashes-approved-pack/ — exact contents (26 PNGs, ALL full-frame, NO alpha)

| Subfolder | Files | Dims | What they actually show |
|---|---|---|---|
| eyes/ (6) | eyes-neutral, eyes-happy, eyes-angry, eyes-blink, eyes-sad, eyes-surprised | 1600×1600 RGB | 👁👁 Close-up void face in the Celtic-trim hood design; only the eye expression changes; no grill in frame. NOT eye cutouts. |
| mouths/ (10) | viseme-ah, -closed, -ee, -fv, -l, -mbp, -oh, -oo, -rest, -snarl | 1600×1600 / 1728×1408 / 1760×1440 RGB | 👁 Extreme close-ups of a HUMAN bearded mouth with gold fang grill (viseme-ah viewed). A different Ashes design from the void-face puppet. |
| hands/ (10) | hand-beckoning, -counting, -fist, -gripping, -holding, -open-palm, -pointing, -relaxed, -shaka, -thumbs-up | 1600×1600 RGB (pointing 1920×1280) | 👁 Brown skin hand filling the frame on flat white (pointing viewed). Real drawn hands, but skin — not the puppet's white glove — and no alpha. |

Verdict: the approved pack is an expression/pose **reference** set in two alternate designs. Nothing in it can be dropped into the puppet as a symbol without a new extraction, and its faces do not match the standard puppet's design.

## Appendix A — exhaustive per-file record, `ashes/` (136 PNGs)

Class key: CUTOUT / FULL-CANVAS TEXTURE (FCT) / FULL-FRAME (FF) / SHEET. Alpha % = fully-transparent / fully-opaque pixel share (PIL).

### arms/ (3)
| File | Dims | Alpha | Class | Actually shows |
|---|---|---|---|---|
| WG_ASHES_FRONT_ARM_L_REST.png | 209×181 | 28/72 | CUTOUT | Crossed-arm sleeve segment + braid/chain fragments |
| WG_ASHES_FRONT_ARM_R_REST.png | 139×181 | 38/62 | CUTOUT | Crossed-arm sleeve segment incl. hand area |
| _CONTACT_SHEET.png | 480×226 | none (RGB) | SHEET | Arms contact sheet |

### ashes-approved-pack/ (26) — ALL FULL-FRAME, RGB, no alpha
eyes/ (1600×1600 each): eyes-angry, eyes-blink, eyes-happy 👁, eyes-neutral 👁, eyes-sad, eyes-surprised — full-face close-ups, Celtic-trim hood design.
hands/ (1600×1600 each except pointing 1920×1280): hand-beckoning, hand-counting, hand-fist, hand-gripping, hand-holding, hand-open-palm, hand-pointing 👁, hand-relaxed, hand-shaka, hand-thumbs-up — brown skin hands on flat white.
mouths/: viseme-ah 👁 1760×1440, viseme-ee 1760×1440, viseme-closed 1600×1600, viseme-oo 1600×1600, viseme-fv 1728×1408, viseme-l 1728×1408, viseme-mbp 1728×1408, viseme-oh 1728×1408, viseme-rest 1728×1408, viseme-snarl 1728×1408 — human bearded mouth close-ups with gold fang grill.

### eyes/ colourway (15) + sheets (2)
| File | Dims | Alpha % | Class | Shows |
|---|---|---|---|---|
| WG_ASHES_FRONT_EYE_L_OPEN.png | 62×60 | 60/40 | CUTOUT | 👁 Amber almond eye, white flame core; small hood-flame fragment in RGB corner |
| WG_ASHES_FRONT_EYE_R_OPEN.png | 64×59 | 64/36 | CUTOUT | Amber almond eye |
| WG_ASHES_FRONT_EYE_L_HALF.png | 62×60 | 70/13 (+17 partial) | CUTOUT | Half-lid edit of L_OPEN |
| WG_ASHES_FRONT_EYE_R_HALF.png | 64×59 | 73/12 (+15 partial) | CUTOUT | Half-lid edit of R_OPEN |
| WG_ASHES_FRONT_EYE_L_SHUT.png | 68×34 | 76/24 | CUTOUT | 👁 Orange lid line only |
| WG_ASHES_FRONT_EYE_R_SHUT.png | 68×34 | 76/24 | CUTOUT | Orange lid line only |
| WG_ASHES_FRONT_PUPIL_L.png | 24×19 | 78/22 | CUTOUT | 👁 Bright-core crop (orange + white flame) |
| WG_ASHES_FRONT_PUPIL_R.png | 24×19 | 78/22 | CUTOUT | Bright-core crop |
| WG_ASHES_FRONT_EYE_PAIR_OPEN.png | 152×76 | 76/24 | CUTOUT | 👁 Both eyes, native spacing |
| WG_ASHES_FRONT_EYE_PAIR_LOOK_L/R/UP/DOWN.png | 152×76 ×4 | ~77/23 | CUTOUT | Pair, pupil-shift edits |
| WG_ASHES_FRONT_EYE_PAIR_SMILE.png | 152×76 | 87/13 | CUTOUT | Pair, crescent-mask edit |
| WG_ASHES_FRONT_EYE_PAIR_ANGRY.png | 151×76 | 73/21 | CUTOUT | Pair, shear edit |
| _CONTACT_SHEET.png | 960×904 | none | SHEET | Eyes contact sheet |
| _VERIFY_base-white.png | 1096×646 | none | SHEET | Colourway-vs-white verification sheet |

### eyes/base-white/ (15)
Same 15 filenames and dims as the colourway set; RGBA with white RGB, opaque share 0% (all luminance in partial alpha) — true base-white variants, CUTOUT class.

### feet/ (4)
WG_ASHES_FRONT_SHOE_L.png 300×190 CUTOUT (49/45) · WG_ASHES_FRONT_SHOE_R.png 300×190 CUTOUT · WG_ASHES_FRONT_SHOE_PAIR.png 624×190 CUTOUT 👁 (generic dark-red side-view cartoon shoes, pack) · _CONTACT_SHEET.png 900×220 SHEET.

### hair-accessories/ (4)
WG_ASHES_FRONT_BRAID_L.png 109×246 CUTOUT (74/26) 👁 gold braid · WG_ASHES_FRONT_BRAID_R.png 94×243 CUTOUT (77/23) · WG_ASHES_FRONT_CHAIN.png 100×136 CUTOUT (64/36) 👁 gold chain + pendant · _CONTACT_SHEET.png 720×226 SHEET.
Note: INDEX-listed duplicates HAIR_SIDE_A/B and ACCESSORY are NOT on disk (logged SKIP in the source INDEX) — the folder holds only the 3 unique parts.

### hands/ (2)
WG_ASHES_FRONT_HAND_R_REST_ON_ARM.png 79×61 CUTOUT (74/26) 👁 white glove hand on red sleeve — the sole extracted hand · _CONTACT_SHEET.png 240×226 SHEET.

### hands-gloves/ (21) — all CUTOUT, parametric pack
REST_L/R 426×498 · OPEN_L/R 413×498 · WAVE_L/R 413×513 · FIST_L/R 325×441 · POINT_L/R 323×498 👁(R) · GRAB_L/R 352×440 · THUMBS_UP_L/R 306×498 · PEACE_L/R 323×498 · FINGER_GUN_L/R 337×441 · PINCH_L/R 343×498 · _CONTACT_SHEET.png 1050×920 SHEET.

### head-hood/ (2)
WG_ASHES_FRONT_HEAD_HOOD_UP.png 294×269 CUTOUT (39/61) 👁 fused hood+face+eyes+grill+braid-tops+shoulders · _CONTACT_SHEET.png 240×226 SHEET. (No FACE_PLATE file on disk — see GAPS #2.)

### mouths/set-one/ (14)
Full table in §2. All CUTOUT.

### rig-proof/ (23)
parts/ (11): 00_base_full_figure, 01_robe 👁, 02_head, 03_braid_L, 04_braid_R, 05_chain, 06_arm_L, 07_arm_R, 08_eyes 👁(=full RGB under alpha; alpha isolates eyes only), 09_grill (same note), _composite_check — all 400×864 FCT; bboxes in §5.
rig-layers/ (5): 07_eye_l, 08_eye_r, 7_eye_closed_l, 8_eye_closed_r (all 400×864 FCT, ≥99.9% transparent outside the eye) + 9_mouth_cavity 400×864 FCT 👁.
proofs/ (6): ashes_pose_neutral 864×864 CUTOUT 👁 · ashes_pose_blink 864×864 CUTOUT · ashes_pose_head-turn_mouth-open 864×864 CUTOUT · ashes_pose_comparison 2592×864 SHEET 👁 · nijigenerate_editor_gui-blocked 1280×800 FF · nijigenerate_editor_gui-fixed 1280×800 FF.
root/ (1): ashes_crop_source.png 400×864 FF (original illustration).

### robe/ (5) — all pack
WG_ASHES_FRONT_ROBE_FRONT.png 660×920 CUTOUT 👁 · WG_ASHES_FRONT_ROBE_BACK.png 660×920 CUTOUT · WG_ASHES_FRONT_SLEEVE_L.png 366×566 CUTOUT · WG_ASHES_FRONT_SLEEVE_R.png 366×566 CUTOUT · _CONTACT_SHEET.png 600×900 SHEET.

## Appendix B — exhaustive per-file record, `ashes-battle/` (64 PNGs)

### arms/ (2)
WG_ASHES_FRONT_ARM_R_REST.png 151×353 CUTOUT (58/42) 👁 raised dunk arm + glove hand (name says REST; pose is overhead) · _CONTACT_SHEET.png 240×226 SHEET. **No arm_L file.**

### eyes/ colourway (15) + base-white/ (15) + sheet (1)
Singles: EYE_L_OPEN 42×27 · EYE_R_OPEN 34×25 · EYE_L_HALF 42×27 · EYE_R_HALF 34×25 · EYE_L_SHUT 39×21 · EYE_R_SHUT 33×20 · PUPIL_L 33×18 · PUPIL_R 26×16 — all CUTOUT, yellow-slit colourway.
Pairs (76×27; ANGRY 74×27): PAIR_OPEN 👁 (two yellow slits — verified true), PAIR_LOOK_L/R/UP/DOWN, PAIR_SMILE, PAIR_ANGRY — all CUTOUT.
base-white/: same 15 names/dims, CUTOUT. _CONTACT_SHEET.png 960×904 SHEET.

### hair-accessories/ (4)
BRAID_L 78×227 CUTOUT · BRAID_R 77×224 CUTOUT · CHAIN 88×130 CUTOUT · _CONTACT_SHEET.png 720×226 SHEET.

### hands/ (2)
WG_ASHES_FRONT_HAND_R_REST_ON_ARM.png 69×69 CUTOUT (79/21) — glove pixels segmented from the raised arm · _CONTACT_SHEET.png 240×226 SHEET.

### head-hood/ (3)
WG_ASHES_FRONT_HEAD_HOOD_UP.png 179×182 CUTOUT 👁 · WG_ASHES_FRONT_FACE_PLATE.png 179×182 CUTOUT (different hash, same fused-head content class — not a hoodless face) · _CONTACT_SHEET.png 480×226 SHEET.

### rig-proof/ (22)
parts/ (11): all 780×885 FCT — 00_base_full_figure 👁, 01_robe, 02_head, 03_braid_L, 04_braid_R, 05_chain, 06_arm, 07_ball (basketball), 08_eyes, 09_grill, _composite_check. Bboxes/pixel counts in §5.
rig-layers/ (5): all 780×885 FCT — 01_face_base, 07_eye_l, 08_eye_r, 7_eye_closed_l, 8_eye_closed_r.
proofs/ (5): ashes_battle_pose_neutral 864×864 CUTOUT 👁 · ashes_battle_pose_blink 864×864 CUTOUT · ashes_battle_pose_blink_opacity 864×864 CUTOUT · ashes_battle_pose_head-turn_mouth-open 864×864 CUTOUT · ashes_battle_pose_comparison 1200×840 (~98% opaque).
root/ (1): ashes_battle_crop_source.png 780×885 FF.

## Appendix C — verification notes & filename lies found

1. **"Energy ball" does not exist.** Battle `07_ball.png` is a basketball 👁. The green energy orb in the battle scene belongs to a different character at the frame edge.
2. **`ARM_R_REST` (battle) is not a rest pose** — it is the raised dunk arm 👁.
3. **Approved-pack "eyes" are not eyes and "mouths" are not the puppet's mouth** — they are full-frame close-ups in two alternate designs (Celtic-trim void face; human bearded face) 👁. All 26 files RGB, zero alpha — the top INDEX's "FULL-FRAME, not cutouts" flag is confirmed per-file by PIL.
4. **Eye colourway naming** — INDEX says "red/black graphic"; the actual standard eyes are amber/orange with white flame cores 👁, battle eyes are yellow slits 👁.
5. **HEAD_HOOD_UP is a fused unit** (hood+face+eyes+grill+braid tops+shoulders) 👁 in both variants; there is no separable hood or face plate.
6. **Extracted arms are crossed-pose segments**, not articulated arm symbols 👁; ARM_L_REST's alpha includes braid/chain overlap.
7. **Mouth Set One splits into two families** (teeth-strip grins vs black cavity discs D/E/H/O_ROUND) 👁 — a puppet build must treat the cavity-disc shapes as open-mouth states, not grins.
8. **Rig-proof textures store full-illustration RGB under alpha** — any tool that flattens RGB will appear to show "full-frame character" files; alpha-aware tools show the isolated part. PIL alpha stats in this inventory are the ground truth.
9. Contact/verify sheets (11 total across both folders) are RGB with no alpha and are not parts; they are excluded from every slot assignment above.
