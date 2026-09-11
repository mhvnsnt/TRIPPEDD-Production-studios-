# God Molecule — MARS Oral Repair Execution Prompt

You are operating in TRIPPEDD Production Studios.

Do NOT build another dashboard and do NOT make another generic human head.

The current MARS_CANONICAL scan is the identity source of truth, but it is a closed-mouth surface. A jaw bone alone cannot reveal teeth, tongue or oral cavity.

## Objective

Produce a real talking MARS shot in which:
- the actual MARS likeness remains visible and unchanged outside the repaired oral region;
- the mouth visibly opens;
- upper and lower teeth exist as real geometry;
- a real tongue exists and moves within bounds;
- AA/OH visibly open;
- MM visibly closes;
- EE spreads;
- FF produces the correct lip/teeth relationship;
- both eyes can blink independently;
- Rhubarb timing comes from the real audio track.

## Required OSS

1. Google GNM Head v3 — https://github.com/google/GNM — Apache-2.0.
2. GNM-Studio — https://github.com/Saganaki22/GNM-Studio — use its constrained GNM identity-fit/runtime approach and preserve its third-party notices.
3. MediaPipe — tracking/landmarks.
4. Existing Rhubarb lane — phoneme timing.
5. Existing Blender/Cycles render path.

## Critical identity rule

MARS_CANONICAL is immutable.

Do NOT replace MARS with the GNM head.

Use GNM as:
- oral anatomy donor,
- mouth/lip deformation donor,
- jaw-open deformation source,
- teeth/tongue source,
- expression-space source.

## Execute

1. Locate the exact MARS_CANONICAL file and record its SHA-256.
2. Render neutral front and three-quarter reference images from the actual MARS mesh.
3. Use the GNM-Studio custom-head fitting path to obtain a Mars-specific GNM identity fit from those references. Record fitting residuals. If residuals are UNKNOWN, stop at UNKNOWN.
4. Build the oral donor from Google GNM v3 using its anatomical groups:
   - upper_teeth_and_gums
   - lower_teeth_and_gums
   - tongue
   - upper_lip_region
   - lower_lip_region
   - mouth_sock
5. Align the donor to measured Mars mouth landmarks, not bounding-box guesses.
6. Create the minimum mouth patch/cavity required to reveal the donor anatomy while preserving the surrounding Mars surface.
7. Transfer only the mouth-region deformation from the fitted GNM expression space onto the Mars mouth/lip shell.
8. Drive the donor and Mars mouth shell from one shared jaw/viseme signal. Do not animate the teeth independently of the jaw.
9. Drive blinks separately from mouth animation.
10. Feed the actual recorded dialogue to Rhubarb and use its real phoneme timing.
11. Render a short validation sequence.

## Hard QC

Measure and report:
- neutral mouth gap
- maximum jaw-open gap
- lower-to-upper tooth travel
- tongue travel
- lip corner travel
- MM closure error
- AA/OH opening error
- EE spread
- FF lip/teeth contact
- left blink closure
- right blink closure
- MARS source hash before/after

No screenshot-only PASS.
No telemetry PASS.
No written-cadence PASS for lip-sync.
UNKNOWN is never PASS.

If the first approach fails, keep the real failure evidence and try the next bounded OSS implementation. Do not replace the MARS identity.

## Important

The user already has real MARS renders. We are fixing the anatomical limitation of the closed scan, not redesigning the character.

The immediate deliverable is a real frame/video where the mouth is visibly open with real teeth/tongue while the character still reads as the same MARS.
