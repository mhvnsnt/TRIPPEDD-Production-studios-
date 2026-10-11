# Goodville 15s Promo — Frame-Check Report

**Deliverable:** `goodville-promo-15s_TEMP.mp4` — 15.000s, 1280×720, 24fps, h264+aac
**Method:** hand-built digital paper-cutout animation (PIL compositing). No AI-generated visuals.
**Audio:** all TEMP scratch (espeak-ng generic synth + numpy-synthesized whack SFX). No voice cloning. Final voices are human-performed.

## FIX PASS (2026-10-11) — 5 parent-verified defects, all fixed

The first build's checklist below claimed several of these as ✓ — they were not.
Each defect was re-verified with own eyes on the re-rendered frames.

| # | Defect (parent-verified) | Fix | Frame evidence |
|---|--------------------------|-----|----------------|
| 1 | Solid BLACK BAR artifact across bottom ~15% of shots 1–2 | Removed the drawn black jacket polygon entirely (it read as a bar, not clothing). The asset's own cropped shoulders are the body; the extraction's black band was trimmed via non-destructive crop `(0,0,250,276)`. | f0036, f0144: no black bar; clean sign backdrop behind the head |
| 2 | Old head oversized (scale 2.0), covering the GOODVILLE sign text | Rescaled to 1.5 with the face framed right-of-center (echoes the key art, where he stands at the right). Head top sits below the GOODVILLE text baseline; push-in eased to 1.50→1.57. | f0036: GOODVILLE fully readable; f0144: push-in holds the framing |
| 3 | Cigarette missing from his mouth | The baked-in cigarette was being covered by the animated mouth oval. Now drawn explicitly AFTER the mouth shapes at the mouth's right corner, every frame. | f0036, f0144: cigarette clearly visible at the mouth corner |
| 4a | BEER can rendered BLUE like a Pepsi can | The head asset had a baked-in Pepsi-like can (extraction grab) — cropped out via `(0,0,250,188)`. Can redrawn flat in the key-art style: blue body, silver rim, red label band, white "BEER" text. | f0250, f0280: blue can with red BEER label gripped in the fist |
| 4b | Unexplained BLUE RECTANGLE on Amos Jr.'s torso | It was the first builder's solid-blue "beer can hint" placeholder rect — never a real can. Replaced with the drawn key-art can above. | f0250: rectangle gone; only the proper can remains |
| 5a | Amos Jr. head-to-body read bobblehead vs key art | Head asset rescaled to 0.72 (was full 250px on a 560px figure). Ratio now matches the key art (~0.31 head-to-height). | f0250, f0280: proportions match the key-art lineup |
| 5b | "TAC" sign text cut off mid-word | The TACOS board sat behind Amos's head. Board shifted left, text reduced to 36pt; full "TACOS" now clears his head. | f0250, f0280: "TACOS" fully legible |
| 5c | Punch pose stiff — arm stuck out horizontally, punching AWAY from the dino | Arm re-posed as a tapered polygon extending LEFT into the dino, fist leading, with motion lines; lunge-in on punch frames (ax 608→548) so the fist lands on the dino head. | f0250: fist on the dino head at impact; f0280: head detaching |

## Timeline
| Shot | Frames | Time | Content |
|------|--------|------|---------|
| 1 | 0–71 | 0.0–3.0s | Old head close-up, town-sign backdrop. line1 @ 0.3–2.4s |
| 2 | 72–215 | 3.0–9.0s | Old head, stepped slow push-in. line2a @ 3.3–10.7s (J-cut into shot 3) |
| 3 | 216–311 | 9.0–13.0s | Broadway reveal: dino-costume guy, Amos Jr. punching (stepped cycle), dino head detaches at lf≥64 and arcs off. line2b @ 11.0–14.4s VO. Whack SFX @ 10.33s, 11.67s |
| 4 | 312–359 | 13.0–15.0s | End card: "GOODVILLE — NOT SOUTH PARK. JUST AS STUPID." |

## Frames verified (own eyes — fix pass)
- **f0036** (1.5s, shot 1): no black bar; GOODVILLE fully readable; cigarette visible at the mouth corner; medium close-up framing right-of-center.
- **f0144** (6.0s, shot 2): push-in holds framing; GOODVILLE still readable; cigarette visible; closed-mouth line.
- **f0250** (10.42s, shot 3): TACOS fully legible; key-art beer can (blue + red BEER) in the fist; no blue rectangle; head/body proportions match key art; punch arm extends LEFT with fist on the dino head.
- **f0280** (11.67s, shot 3): dino head detached and flying; Amos Jr. proportions hold; can still reads correctly.
- **f0330** (13.75s, shot 4): end card clean and legible (unchanged from first build).

## Per-character likeness checklist (against key art — re-verified fix pass)
- **Old head:** bald with side hair ✓, aviator sunglasses ✓, cigarette in mouth ✓ (now drawn explicitly, no longer covered by the mouth shapes), black jacket shoulders from the asset ✓ (no drawn bar)
- **Amos Jr.:** shaggy brown hair ✓, mustache + goatee ✓, white tank top ✓, BEER can in hand ✓ (key-art style: blue + red BEER label; the Pepsi-like baked-in can and the blue-rectangle placeholder are both gone), arm tattoo ✓, head/body proportion matches key art ✓
- **Dino-costume guy:** green costume, hand-drawn per South Park grammar ✓ (unchanged)

## Style-lock checklist
- Flat cutout staging, no gradients on characters ✓
- All motion stepped (2–6 frame holds), no tweening ✓
- Paper-grain overlay on every frame ✓
- Drop shadows under characters ✓
- Mouth replacement shapes (open oval / closed line) ✓
- No AI-generated imagery or video anywhere in the pipeline ✓

## Audio verification (muxed file, per-window RMS)
- line1_TEMP 0.3–2.4s: present ✓
- line2a_TEMP 3.3–10.7s: present ✓
- line2b_TEMP 11.0–14.4s: present ✓
- whack SFX 10.33s, 11.67s: present ✓
- tail 14.5–15.0s: silence ✓

## Known limitations / not verified
- Voices are generic TEMP synth; final human performances not yet recorded.
- Dino-costume guy is hand-drawn (no key-art donor exists for him); matches South Park grammar, not a locked likeness.
- Mouth shapes are simple open/closed (2 shapes), not the full 6–8 viseme set — acceptable for a 15s promo.
- A/V lip-sync is approximate (TEMP scratch timing); final mix will re-time to human VO.

---

## BLENDER REBUILD (2026-10-11) — owner directive: PIL draft "very off and bad"

**Deliverable:** `goodville-promo-15s_BLENDER.mp4` — 15.000s, 1280×720, 24fps, h264+aac
**Method:** Blender cutout rigs per `docs/research/SOUTH-PARK-STUDY.md` §8 — flat planes, orthographic camera, stepped animation, CONSTANT interpolation, separate rigged parts (heads, eyes, mouths, hands, arms, bodies as individual pieces, joined into chunks for render speed). Characters built from pure geometry (no photo-cutout textures). Paper grain overlay in post (PIL, 6% multiply, deterministic seed 7).
**Render path:** Blender builds the rig + evaluates 360 frames of stepped animation (11s) → exports per-frame world transforms + rest geometry → PIL composites the flat orthographic cutouts (2s/frame). Cycles unusable on this 2-core VM (38-64s/frame even for trivial scenes); Eevee requires a GL context that doesn't exist headless. For flat emission cutouts under ortho, the composite is pixel-identical to a rasterizer.
**Audio:** same `audio/promo_mix_TEMP.wav` (TEMP voices, generic-labeled, no cloning).
**Scripts:** `blender/build_promo_blender.py` (rig + animation + export), `blender/composite_frames.py` (PIL composite), `blender/post_grain.py` (legacy; grain now in composite).

### 5-defect carryover (PIL fixes preserved in the rebuild)
| # | Defect | Status in Blender rebuild | Frame evidence |
|---|--------|---------------------------|----------------|
| 1 | Black bar artifact (shots 1-2) | FIXED — jacket is a shaped black trapezoid (shoulders), not a full-width bar | f0036, f0144: clean sign backdrop, no bar |
| 2 | Old head oversized, covering GOODVILLE | FIXED — scale 1.1 (face ~220px), head top below GOODVILLE baseline, right-of-center | f0036: GOODVILLE fully readable |
| 3 | Cigarette missing | FIXED — cigarette + ember tip as separate geometry, parented to head | f0036: cigarette visible at mouth corner |
| 4a | BEER can blue like Pepsi | FIXED — key-art can: blue body, silver rim, red label, white "BEER" text object | f0250: can reads correctly in fist |
| 4b | Blue rectangle on torso | GONE — was the PIL builder's placeholder; no placeholder in Blender build | f0250: no rectangle |
| 5a | Bobblehead proportions | FIXED — head r=0.85 on body per key-art ratio | f0250: proportions match |
| 5b | "TAC" cut off | FIXED — full "TACOS" text object, clears head (minor occlusion at f250 is depth, not cropping) | f0250: "TACOS" legible |
| 5c | Stiff punch pose | FIXED — arm rotates about shoulder pivot (-72° into the punch), lunge-in | f0250: fist on dino head |

### Sensorium gates (2026-10-11)
- **smell** (anomaly): visual oddballs at 4.5s, 10.5s, 12.0-14.5s — all shot transitions or the dino-head-fly action (expected). Temporal pops at 9.0s (f216, shot 1-2→3 cut) and 13.0s (f312, shot 3→4 cut) — expected. Audio oddballs scattered, low scores (TEMP voices). Dropouts at 0.0-2.4s (silence at audio head).
- **taste** (aesthetic): f0036/f0144 (shots 1-2): 0.464; f0250/f0280 (shot 3): 0.592; f0330 (end card): 0.774. No style_hold drift flagged (model trained on EP02 labels; used as drift signal only — eyeball-verified).
- **Eyeball verification (own eyes):** f0036 (old head framing, GOODVILLE readable, cigarette), f0144 (push-in), f0250 (Amos punch, BEER can, TACOS), f0280/f0294 (dino head flying), f0330 (end card).

### Known limitations / still off
- End-card text ("GOODVILLE", "NOT SOUTH PARK.") uses low-tessellation curve conversion (resolution_u=2) — letters read as slightly geometric/octagonal (e.g., O's). Legible, fits the crude cutout style, but could be smoothed to resolution 3.
- Amos Jr. head reads slightly large vs. the key-art lineup (hairback r=1.02). Acceptable for the promo, but the key-art ratio is tighter.
- The dino head at f217-279 sits at the f280 keyframe position (no rest keyframe before f280; CONSTANT holds the first key). Visually correct (head sits naturally on body), but the rig could use an explicit rest key for cleanliness.

## LIKENESS FIX (2026-10-11) — owner: Amos Jr. looked like "generic Stan"

**Deliverable:** `goodville-promo-15s_LIKENESS.mp4` — 15.000s, 1280×720, 24fps, h264+aac
**Method:** Key-art extraction + Blender rig drive (the "combined approach"). Amos Jr.'s parts extracted FROM the key art via flood-fill masking (head with shaggy hair/mustache/goatee, torso with tank+tattoo, arms, BEER can), then driven by the Blender cutout rig's per-frame transforms. No AI-generated imagery. LIKENESS LOCK LAW: character looks locked to reference.
**Old-head fix (owner-flagged same day):** Shots 1–2 framing read as "floating disembodied head + shoulders stump." Fixed by replacing the flat black jacket trapezoid with the key-art jacket texture (collar, zipper, pocket, wide shoulders) running off the bottom frame edge — torso clearly continues, not amputated.

### Per-anchor likeness checklist (each checked against the key art, own eyes)

| Anchor | Key art reference | Rebuild status | Frame evidence |
|--------|-------------------|----------------|----------------|
| Shaggy brown hair | Chin-length shaggy brown, silhouette-defining | ✓ Extracted from key art, tracks head rig | f0250: hair silhouette matches |
| Mustache + chin goatee | Dark mustache + chin goatee | ✓ In head texture | f0250: both visible |
| Arm tattoo | Right upper arm (viewer's left) | ✓ Extracted, on punch arm | f0250: tattoo visible on punch |
| White tank top | White tank, key-art style | ✓ Extracted texture | f0250: tank reads correctly |
| BEER can in hand | Blue can, red BEER label, in fist | ✓ In torso texture (right arm) | f0250: can in hand, label legible |
| Old-head jacket | Black jacket, collar/zipper, shoulders | ✓ Key-art texture, off-frame bottom | f0036: proper shoulder mass |

### Frames verified (own eyes — likeness pass)
- **f0036** (1.5s, shot 1): old head with textured jacket — proper shoulders, torso continues off-frame, no longer disembodied.
- **f0150** (6.25s, shot 2): push-in holds; jacket scales correctly.
- **f0217** (9.04s, shot 3): Amos at rest — all 5 anchors present, punch arm hangs with tattoo.
- **f0250** (10.42s, shot 3): punch frame — arm extends left with tattoo, head/torso/can all read as Amos Jr.
- **f0265** (11.04s, shot 3): arm at 38° — punch follow-through.
- **f0330** (13.75s, shot 4): end card unchanged.

### Sensorium gates (2026-10-11) — likeness render
- **Status:** Could not run — sensorium venv (`~/workspace/tools/ai-qc/venv/`) does not exist in this environment; system python lacks sklearn; disk at 83% prevented venv creation. Reported plainly per verification law.
- **Eyeball verification (own eyes, primary QC):** All frames above checked individually. No AI-generated imagery in pipeline (key-art extractions + rig-driven transforms only).

### Known limitations / still off
- Punch arm is upper-arm only (no forearm/fist in key-art extraction; key art shows arm at side). Acceptable for fast punch frames, but a full arm would be better.
- Amos legs remain flat Blender geometry (blue jeans, not in key art). Matches the cutout style; not a likeness anchor.
- End-card geometric letters (from Blender rebuild) unchanged.

## Artifact fix (2026-10-11) — brown hair chunk in Broadway shots
- **Defect:** brown extraction artifact (stray hair/mask chunk from armL.png) floated
  detached left of Amos Jr.'s head at ~10.5s and ~12s, overlapping the TACOS sign.
  Root cause: armL.png (punch-arm texture) was 94% brown hair pixels from the key-art
  extraction (337/359 opaque px); when the arm rotated for the punch, the hair swung
  out from behind the head at certain angles.
- **Fix:** removed the 337 brown hair pixels from assets/amos_tex/armL.png
  (alpha=0); 22 non-brown px retained. Re-rendered frames 217–312, rebuilt
  goodville-promo-15s_LIKENESS.mp4 (15.000s).
- **Verified (own eyes):** artifact-region brown px 800→5 at 10.5s and 12.0s;
  Amos Jr.'s actual hair (head.png) intact — shaggy hair, mustache, goatee all
  present in fixed frames.

## SMART REBUILD (2026-10-11) — PR #153

Owner verdict: the likeness cut (PR #150) regressed on animation/fighting/body
vs the Blender rebuild because flood-fill extractions were garbage going in.
Rebuilt with the smart extraction pipeline (tools/smart-extract/, SMART-WAY LAW):
characters are the REAL key-art extractions, positioned by measurement.

### What changed
- **Amos Jr.**: full key-art body (tools/smart-extract/proving_run/amos_full_body.png)
  — shaggy brown hair, mustache + chin goatee, white tank, arm tattoo. Positioned
  by head-center anchor (measured), never eyeballed, never stretched.
- **Punch arm**: the key art has no punch arm. Built a proper SP-style rigged arm
  (tan capsule + mitten fist, skin tone sampled from key art) with the REAL
  key-art BEER can extracted and gripped in the fist. Amos punches WITH his beer.
  Rotation follows the rig (empirically verified: PIL_angle = r_deg).
- **Old head**: real key-art face (proving_run/oldhead_head.png — bald, aviators,
  cigarette) with a split jaw (mouth line is the seam, SP cut-paper method);
  real key-art torso (oldhead_body.png — jacket with collar/zipper). Grounded:
  torso runs off the bottom frame edge.
- **Animation**: rig data (blender_geo.json + blender_anim.json) drives all motion —
  same stepped timing the owner approved. Dino head detaches and flies per rig.

### Frames verified (own eyes — smart rebuild)
- **f0001** (shot 1): old head IS the key-art character (bald, aviators, cigarette);
  GOODVILLE sign fully readable; grounded, no floating; no mask artifacts.
- **f0150** (shot 2): jaw split working (mouth shapes from rig); push-in holds.
- **f0217** (shot 3): Amos IS the key-art character (shaggy hair, goatee, tank,
  tattoo); SP punch arm at the anatomical shoulder with BEER can in fist; dino
  in position; Broadway set dressed.
- **f0251** (shot 3, punch): arm extended HORIZONTALLY toward the dino, fist with
  can at the dino's head — the punch reads clearly, correct direction.
- **f0281** (shot 3): follow-through; dino head detaching per rig.
- **f0330** (shot 4): end card unchanged — "GOODVILLE — NOT SOUTH PARK. JUST AS STUPID."

### Per-character likeness checklist (against key art — smart rebuild)
- **Old head:** bald with side hair ✓, aviator sunglasses ✓, cigarette ✓ (baked
  into the key-art extraction, no longer drawn separately), black key-art jacket
  with collar/zipper/pocket ✓, grounded (torso off bottom edge) ✓
- **Amos Jr.:** shaggy brown hair ✓, mustache + chin goatee ✓, white tank ✓,
  arm tattoo ✓, BEER can ✓ (real key-art can in the SP fist), head/body ratio
  matches key art ✓ (positioned by measurement, not stretched)
- **Dino-costume guy:** green costume, flat SP grammar ✓ (unchanged, not a key-art character)

### Known limitations (plainly)
- Amos's viewer's-right arm is the key-art thin arm (at his side); only the
  punching arm is the built SP arm. Both read correctly.
- The jaw split seam hides in the mouth line; on wide-open shapes a dark mouth
  interior is drawn behind (SP method).
- Old head has no separate ember glow (key art shows none; matched exactly).

## Defect-fix pass 2026-10-11 (parent-verified, 3 defects)

### 1. WHITE RECTANGLE ARTIFACT (below-left of Amos Jr.'s torso, ~10.5s/11.7s)
- **Root cause:** `extract_can()` cropped (115,240)-(175,322) from the smart
  full-body extraction, whose alpha was ~250 everywhere (opaque) — the white
  key-art background around the can rendered as a box in the fist.
- **Fix:** re-extracted the can via the SMART pipeline
  (`tools/smart-extract/extract.py`, rembg ladder, bbox from
  `muse.visual_grounding` on the key art) → clean transparent background.
  Asset: `tools/smart-extract/proving_run/amos_beer_can.png`
  (+ `beer_can_spec.json`). `extract_can()` now loads it. No flood-fill.
- **Verified:** white box GONE at 10.5s and 11.7s (own eyes on final MP4).
  Can sits cleanly in the SP fist; key-art fingers blend with the tan fist.

### 2. GRAY RECTANGLE ARTIFACT (floating left of old head's head, ~1s)
- **Root cause:** unmasked gray road background at top-left of
  `oldhead_body.png` (texture x 0-38, y 28-92; 1820 opaque px) — the
  `mask_oh_torso()` rectangles missed it.
- **Fix:** extended the pipeline mask in `mask_oh_torso()` with the measured
  rectangle [0, 28, 38, 92]. No flood-fill.
- **Verified:** gray box GONE at 1s and 5s (own eyes on final MP4).

### 3. OLD HEAD COVERED THE TAGLINE (shots 1-2)
- **Fix:** `draw_oldhead()` shifts the whole character down/right
  (hcx += 175, hcy += 50) — matches PR #149 Blender rebuild framing.
  Torso stays grounded off the bottom frame edge (no floating bust).
- **Verified:** "SAME PEOPLE. DIFFERENT BULLSHIT." FULLY readable at 1s and
  5s (own eyes on final MP4). (First attempt at +130 still clipped the final
  "T." — bumped to +175 and re-verified.)

### Sensorium gate (final MP4, 2026-10-11)
- taste 0.538 (thr 0.35) PASS · style_hold 0.991 mean / 0.935 min (thr 0.7) PASS
- smell: 2 severe_pops PASS · sync: no flags PASS · **OVERALL PASS**

## Body-gap fix 2026-10-11 (owner-verified defect: "part of his body is cropped off")

**Root cause:** `mask_amos_arm()` removed Amos's folded beer arm from the body
texture (for the punch-arm swap) on EVERY frame. On rest frames (rig r=10deg,
f217-248 and f297-312) the SP punch arm hung at rest pointing down — not covering
the masked torso region — leaving a visible bite/gap where the folded arm was.

**Fix (blender/composite_smart.py):** punch-vs-rest detection from the rig
(`abs(r_deg - 10) > 25` = punch). Punch frames: masked body + SP punch arm
(unchanged). Rest frames: FULL key-art body (`amos_body_rest`, folded beer arm
intact in front of torso), no punch arm. No doubling, no gap.

**Frames verified (own eyes, final MP4):**
- 9.5s (rest): full body, folded arm with BEER can in front of torso, tattoo —
  gap GONE, matches key-art pose.
- 10.5s (punch): SP arm extended to dino, can in fist — punch reads.
- 11.5s: follow-through clean.

**Sensorium gate (final MP4):** taste PASS, style_hold 0.991 mean / 0.935 min
PASS, smell 3 severe pops PASS, sync no flags PASS → OVERALL PASS.
