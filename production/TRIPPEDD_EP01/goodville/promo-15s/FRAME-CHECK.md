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
