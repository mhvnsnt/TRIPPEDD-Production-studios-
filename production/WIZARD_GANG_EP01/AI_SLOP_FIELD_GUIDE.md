# AI SLOP FIELD GUIDE — Wizard Gang Production QC

**Version:** 1.0 — 2026-10-10
**Purpose:** Detect, fix, and prevent common AI video generation defects in Wizard Gang episodes.
**Companion doc:** `EP02_AI_SLOP_AUDIT.md` (shot-specific findings for EP02 — this guide is the general playbook).

**Locked art styles (owner-approved, no exceptions):**
- 🎨 **Cartoony base** — Shadow Wizard Money Gang 2D cartoon. Flat cel-shaded colors, bold black outlines.
- 🖌️ **Painterly** — Only at intended dramatic beats.
- 🚫 **Never:** 3D rendering, photorealistic, CGI, cinematic realism.

---

## TABLE OF CONTENTS

1. [Defect 1: Synchronized Motion](#1-synchronized-motion) *(deep dive)*
2. [Defect 2: 3D/Realistic Drift](#2-3drealistic-drift)
3. [Defect 3: Background Morphing](#3-background-morphing)
4. [Defect 4: Face/Body/Hand Instability](#4-facebodyhand-instability)
5. [Defect 5: Identity Drift](#5-identity-drift)
6. [Defect 6: Prop Instability](#6-prop-instability)
7. [Defect 7: Lighting/Texture Popping](#7-lightingtexture-popping)
8. [Programmatic Detection Toolkit](#programmatic-detection-toolkit)
9. [Per-Shot QC Checklist Template](#per-shot-qc-checklist-template)
10. [Prompt Templates (Defect-Proof)](#prompt-templates-defect-proof)
11. [Regeneration Decision Tree](#regeneration-decision-tree)

---

## 1. SYNCHRONIZED MOTION

**What it is:** Multiple characters moving identically or at the same time in an unnatural way. All 9 wizards swaying in the same direction at the same moment. Everyone turning their heads simultaneously. A crowd that moves like a single organism instead of individual people.

**Why it looks wrong:** Real humans never move in perfect sync unless deliberately choreographed (military drill, dance routine). In a natural scene, each person has their own timing: one shifts weight, another scratches their nose 2 seconds later, a third is completely still. When AI syncs everyone, it triggers an uncanny "puppet" feeling.

### Why AI models do this (technical causes)

1. **Shared temporal attention.** Video diffusion models use temporal attention layers that process motion across frames. When multiple similar-looking subjects (e.g., 9 robed figures) occupy the frame, the temporal attention doesn't cleanly separate "character A's motion" from "character B's motion." Motion information bleeds across subjects through shared attention weights, causing them to inherit the same movement pattern.

2. **Cross-attention identity bleed.** When subjects share similar scale, lighting, and appearance (hooded figures in similar robes), the model's cross-attention layers confuse which motion tokens belong to which character. Research on dual-character generation confirms this: "latent cross-attention layers easily confuse identity tokens" when subjects look similar.

3. **Training data bias.** Video models are trained heavily on dance videos, music videos, sports footage, and crowd scenes — all contexts where synchronized motion is common. The model's prior leans toward syncing group movement because that's statistically dominant in training data.

4. **Single motion latent.** Many architectures encode "the motion of this clip" as a relatively low-dimensional signal. With limited capacity to represent 9 independent motion tracks, the model collapses them into one dominant pattern.

5. **Prompt under-specification.** If the prompt says "the wizards sit around the table talking" without specifying individual actions, the model fills the gap with the simplest solution: everyone does the same thing.

### How to spot it (manual)

- **The freeze test:** Pause at 3-4 random timestamps. Are multiple characters in the same pose? Same arm angle? Same head tilt? Real groups don't mirror each other.
- **The onset test:** Watch for movement starts. Do 3+ characters begin moving on the exact same frame? Natural movement has staggered onsets (100-500ms apart minimum).
- **The idle test:** In a "standing around" scene, is anyone actually idle? If all 9 are swaying/bobbing continuously with the same rhythm, that's sync slop.
- **The blink test:** Do multiple characters blink on the same frame? This is a dead giveaway — real blinks are never synchronized.
- **Speed check:** Play at 0.25x. Synchronized motion becomes obvious in slow motion — you'll see the lockstep.

### How to detect it (programmatic)

**Method A: Pose correlation analysis (MediaPipe)**
```python
# Extract pose landmarks for each person per frame using MediaPipe Pose
# For each pair of people, compute cross-correlation of a key joint's
# vertical position over time (e.g., nose y-coordinate for head bob)
# FLAG: if correlation > 0.85 for 3+ pairs, motion is suspiciously synced

import mediapipe as mp
import numpy as np
from scipy.signal import correlate

# Pseudocode:
# poses[person_id][frame] = np.array of landmark positions
# for each pair (a, b):
#     signal_a = poses[a][:, NOSE_Y]  # head bob over time
#     signal_b = poses[b][:, NOSE_Y]
#     corr = np.corrcoef(signal_a, signal_b)[0,1]
#     if corr > 0.85:
#         print(f"SYNC WARNING: persons {a} and {b}, correlation={corr:.2f}")
```

**Method B: Optical flow synchrony**
```python
# Divide frame into N regions (one per character via bounding boxes)
# Compute mean optical flow vector per region per frame
# FLAG: if 3+ regions have flow vectors pointing the same direction
#        with similar magnitude for 10+ consecutive frames
import cv2
# flow = cv2.calcOpticalFlowFarneback(prev, next, ...)
# Per-region mean flow -> compare directions via cosine similarity
```

**Method C: Motion onset detection**
```python
# For each tracked person, detect frames where movement starts
# (frame-to-frame joint displacement exceeds threshold)
# FLAG: if 3+ people have onsets within 2 frames of each other,
#        more than twice in a 5-second clip
```

**Recommended stack:** MediaPipe Pose (33 landmarks, multi-person) + numpy/scipy for correlation. All free, all CPU-runnable.

### How to fix it (post-generation)

1. **Stagger in edit:** If the motion is synced but otherwise good, split characters into layers (rotoscope/mask), then offset each layer's timing by 3-8 frames in the NLE. This breaks the lockstep.
2. **Freeze some characters:** Mask 2-3 background characters and hold them on a single clean frame (with subtle scale breathing added). Not everyone needs to move.
3. **Replace worst offenders:** If 2 characters are egregiously synced, regenerate just those as isolated elements and composite back.

### How to prevent it (prompting)

**The golden rule: describe each character's action individually, with different timing.**

```
BAD:  "Nine wizards sit around a table talking and gesturing"

GOOD: "Nine wizards around a table. Wizard in red leans forward gesturing
       with right hand. Wizard in blue sits back, arms crossed, still.
       Wizard in green turns head left after a pause. Wizard in yellow
       taps fingers on table intermittently. Others mostly still with
       subtle individual idle shifts at different times. No synchronized
       movement. Each character moves on their own timing."
```

**Key prompt phrases:**
- `"each character moves independently on their own timing"`
- `"no synchronized movement, no lockstep motion"`
- `"natural staggered idle: some still, some shifting at different moments"`
- `"asymmetric natural group behavior, NOT choreographed"`
- Describe 3-4 specific individual actions, then `"remaining characters mostly still"`

**Structural prevention:**
- **Limit simultaneous subjects.** The #1 structural fix per multiple sources: fewer people in frame = fewer sync artifacts. "Videos look much more stable when the action is separated in time or space."
- **Sequential framing.** Pan from person to person instead of showing all 9 at once. Only the foreground subject needs detailed motion.
- **Depth staging.** Put 2-3 characters in sharp foreground focus, rest soft/out of focus in background. The model handles 2-3 independent motions far better than 9.

---

## 2. 3D/REALISTIC DRIFT

**What it is:** A shot that starts (or should be) 2D cartoon gradually or suddenly rendering as 3D CGI or photorealistic. Skin gets subsurface scattering, muscles get volumetric shading, fabric gets realistic weave, lighting goes cinematic.

**EP02 examples:** Shot 12-3 (~100s, war fund): Cipher's skin developed 3D subsurface scattering. Shot 20-1 (~190s, bridge): photorealistic muscle shading. The pattern: **unmasked faces trigger the drift.** Hooded/robed characters held 2D; every bare face drifted realistic.

**Why it happens:**
- The model's training data is dominated by photorealistic/3D content. "High quality" in the model's latent space = photorealistic.
- Words like "detailed," "cinematic," "high quality," "real character motion" push toward realism.
- Human faces are the strongest photorealism trigger — the model has vastly more photorealistic face data than 2D cartoon face data.
- Image-to-video: if the input still has any shading gradient (not pure flat color), the model "upgrades" it to 3D.

**How to spot it:**
- **Skin test:** Is skin flat color or does it have gradient shading, pores, subsurface glow? Flat = 2D. Gradient/pores = drift.
- **Outline test:** Are outlines bold, consistent black lines? Or do they disappear into soft shading? Disappearing outlines = 3D drift.
- **Muscle test:** Are muscles defined by simple shapes or by realistic anatomical shading? Anatomy = drift.
- **Lighting test:** Is lighting flat/stylized or does it have realistic falloff, rim light, ambient occlusion? Cinematic lighting on a cartoon = drift.

**How to fix it:**
1. **Regenerate with hard style lock** (see prompt templates below). This is the primary fix.
2. **2D filter pass:** Cartoonization (white-box cartoon GAN, AnimeGAN) can pull mild drift back. Won't fix full photorealism.
3. **EbSynth keyframe:** Paint one frame in proper 2D style, propagate. Good for mild-to-moderate drift.

**How to prevent it:**
- Never use "realistic," "detailed," "cinematic," "high quality" without "2D cartoon" qualifier.
- Always include explicit negatives: `"NOT 3D, NOT photorealistic, NOT CGI, NOT cinematic rendering, NOT subsurface scattering"`
- Anchor with style reference: use the same approved 2D still as image input for every generation.
- The "decide the style once" rule: don't redescribe style fresh each time. Use one locked style block, copy-paste verbatim.

---

## 3. BACKGROUND MORPHING

**What it is:** Background elements shift, warp, breathe, or rearrange independently of any camera movement. Walls bend. Posters change. Windows move. The background feels "alive" in a way that breaks immersion.

**Why it happens:**
- The model doesn't have a persistent 3D understanding of the scene. Each frame's background is re-inferred, causing drift.
- Without a vanishing point or spatial anchor, the model can't keep geometry stable.
- Camera movement prompts ("slow pan") without spatial references cause the model to invent new background rather than reveal existing background.

**How to spot it:**
- **Edge lock test:** Pick a background vertical edge (door frame, building corner). Scrub through the clip. Does it stay in the same screen position (static camera) or move smoothly (panning camera)? If it wobbles, bends, or jumps — morphing.
- **Detail test:** Look at background text, posters, signs. Does the text change between frames? Do details appear/disappear?
- **The still comparison:** Compare frame 1 and last frame backgrounds side by side. Same camera position? They should match (minus animated elements like flames).

**How to fix it:**
1. **Lock the background:** Extract a clean background plate from the best frame. Composite characters (rotoscoped) over the locked plate.
2. **Stabilize in post:** If morphing is subtle, use planar tracking to pin background elements.
3. **Regenerate with locked camera:** `"static camera, locked-off shot, background completely still"`

**How to prevent it:**
- `"locked camera, static background, no background movement"`
- Add spatial anchors: `"one-point perspective, fixed vanishing point"`
- For image-to-video: the input still IS the background — instruct `"preserve background exactly as in input image, only animate characters"`

---

## 4. FACE/BODY/HAND INSTABILITY

**What it is:** Features morph between frames. Fingers merge into blobs. Teeth count changes. Eyes warp. Limbs briefly deform.

**Why it happens:**
- Hands: the model doesn't understand hand anatomy as 3D structure — it pattern-matches 2D hand appearances. During motion, the pattern breaks.
- Faces: identity isn't locked across frames; each frame re-infers facial features.
- Small/fast-moving parts exceed the model's temporal resolution.

**How to spot it:**
- **Hand count:** Pause during any hand action. Count fingers. 6+ = fail. Merged blob = fail.
- **Teeth check:** During dialogue, does tooth count/shape stay consistent?
- **Slow-mo scrub:** At 0.25x, watch faces during head turns. Warping/morphing becomes obvious.
- **Contact points:** Where hands touch objects — this is where the model fails most. Check every hand-object interaction.

**How to fix it:**
1. **Cut around it:** If a hand morphs for 5 frames, cut those frames or cover with a reaction shot.
2. **Freeze + replace:** Hold on a clean frame during the bad section.
3. **Regenerate the specific action** with explicit hand description: `"right hand grips dice with thumb and two fingers clearly separated"`

**How to prevent it:**
- Name every contact point: `"hand grips table edge, fingers individually visible"`
- Avoid complex hand actions in group shots. Save detailed hand work for close-ups with fewer subjects.
- `"anatomically correct hands, five distinct fingers"` in every prompt with visible hands.

---

## 5. IDENTITY DRIFT

**What it is:** A character's face, outfit, or proportions change between shots or within a shot. Static's beard gets thicker. Cipher's mask shape shifts. Robe colors change.

**Why it happens:**
- Each generation is independent — nothing carries identity forward unless explicitly anchored.
- Similar characters (9 robed figures) cause cross-attention confusion — features bleed between characters.

**How to spot it:**
- **Side-by-side:** Screenshot the same character from 3 different shots. Compare face shape, outfit details, colors, proportions.
- **The lineup test:** In group shots, can you identify each character by their established visual markers? If two "different" characters look interchangeable, identity has drifted.

**How to fix it:**
- Character reference sheets. Every generation uses the same approved still as image input.
- The LIKENESS_BIBLE.md is the authority — check every character against it.

**How to prevent it:**
- Image-to-video (not text-to-video) for every shot. The input still IS the identity anchor.
- Never redescribe a character in text alone. Always pair with reference image.
- `"maintain exact character design from input image, no reinterpretation"`

---

## 6. PROP INSTABILITY

**What it is:** Objects appear, disappear, change shape, or teleport. The war fund hat changes size. Dice become cards. A burger becomes a hot dog.

**How to spot it:**
- **Prop inventory:** List every prop in frame 1. Check each is present and consistent in the last frame.
- **Shape check:** Does the war fund hat maintain its shape? Does the dice stay dice?

**How to fix/prevent:**
- Name and describe each prop in the prompt: `"a brown fedora hat (the war fund) sits center table, unchanged throughout"`
- `"props remain consistent, no objects appear or disappear"`
- Fewer props = fewer failures. Only include story-critical props.

---

## 7. LIGHTING/TEXTURE POPPING

**What it is:** Sudden shifts in lighting direction, intensity, or surface detail within a single shot. Skin goes from flat to pore-detailed mid-shot. Shadows flip direction.

**EP02 example:** Shot 20-1 bridge scene had moonlight from two different angles. Skin texture popped from flat 2D to detailed pores within single clips.

**Why it happens:**
- The model re-infers lighting per frame without a persistent light source model.
- "Cinematic lighting" prompts cause the model to add dramatic light that shifts as the "camera" (imaginary) moves.

**How to spot it:**
- **Shadow direction:** Draw a mental line from shadow to object. Does the light source stay consistent?
- **Texture scrub:** Watch skin/fabric at 0.5x. Does detail level suddenly change? That's popping.
- **Flicker test:** Step through frame by frame. Any frame that's noticeably brighter/darker than neighbors = pop.

**How to fix:**
- Color grade to even out pops (limited effectiveness).
- Regenerate with locked lighting: `"single consistent light source from upper left, no lighting changes"`

**How to prevent it:**
- Always specify light source: `"warm candlelight from table center, consistent throughout"`
- Avoid "dramatic lighting," "cinematic lighting" — these invite popping.
- `"flat cartoon lighting, no realistic light falloff"`

---

## PROGRAMMATIC DETECTION TOOLKIT

**Stack (all free, CPU-runnable):**
- `opencv-python` — optical flow, frame differencing, edge detection
- `mediapipe` — multi-person pose tracking (33 landmarks)
- `numpy` / `scipy` — correlation analysis, signal processing
- `Pillow` — frame extraction, comparison

**Planned scripts** (to be built in `~/workspace/video-fix-tools/qc/`):

| Script | Detects | Method |
|--------|---------|--------|
| `sync_detect.py` | Synchronized motion | MediaPipe pose → cross-correlation of joint trajectories |
| `style_drift.py` | 3D/realistic drift | Edge density + gradient analysis (flat 2D = fewer gradients) |
| `bg_stability.py` | Background morphing | Feature matching (ORB) between first/last frame backgrounds |
| `hand_check.py` | Hand anatomy | MediaPipe Hands → finger count per frame |
| `identity_check.py` | Identity drift | Face embedding distance across shots (FaceNet/ArcFace) |
| `flicker_detect.py` | Lighting/texture pop | Frame-to-frame luminance variance spikes |

**Manual review is still primary.** Automated tools flag candidates; human eyes confirm.

---

## PER-SHOT QC CHECKLIST TEMPLATE

Copy this for each shot. PASS requires all checks green.

```
SHOT: ___  TIME: ___-___  CLIP FILE: ___

STYLE
[ ] 2D cartoon base held throughout (no 3D/realistic drift)
[ ] Outlines bold and consistent (no disappearing edges)
[ ] Skin is flat color (no pores, no subsurface scattering)
[ ] Lighting is flat/stylized (no cinematic falloff)
[ ] If painterly beat: intentional, matches approved dramatic moments

MOTION
[ ] No synchronized group movement (stagger test passed)
[ ] Each character has individual timing
[ ] No lockstep head turns, blinks, or sways
[ ] Idle characters are actually idle (not all bobbing)

FACES & HANDS
[ ] Finger count correct in all visible hands (5 max)
[ ] No finger merging/blobbing during motion
[ ] Teeth consistent during dialogue
[ ] Eyes stable (no warping during head turns)
[ ] Hand-object contact points clean

IDENTITY
[ ] Each character matches LIKENESS_BIBLE.md
[ ] Outfit colors/designs match approved stills
[ ] No feature bleed between similar characters

BACKGROUND & PROPS
[ ] Background stable (no morphing/warping)
[ ] Background text/signs legible and consistent
[ ] All props present and shape-consistent
[ ] Lighting direction consistent throughout

VERDICT: [ ] PASS  [ ] FAIL → Remedy: ___
QC BY: ___  DATE: ___
```

---

## PROMPT TEMPLATES (DEFECT-PROOF)

### Universal Style Lock Block
Append verbatim to every generation prompt:
```
STYLE: 2D cartoon animation, flat cel-shaded colors, bold black outlines,
Shadow Wizard Money Gang aesthetic. NOT 3D, NOT photorealistic, NOT CGI,
NOT cinematic rendering, NOT subsurface scattering, NOT realistic skin
texture. Maintain exact character designs from input image.
```

### Group Scene (Anti-Sync)
```
[STYLE LOCK BLOCK]
[Number] characters [location]. [Character 1]: [specific individual action].
[Character 2]: [different specific action, different timing].
[Character 3]: [still or subtle idle]. Remaining characters mostly still
with natural staggered micro-movements at different times.
Each character moves independently on their own timing.
No synchronized movement, no lockstep motion, no choreographed group action.
Asymmetric natural group behavior.
```

### Close-Up / Dialogue (Anti-Drift)
```
[STYLE LOCK BLOCK]
Close-up of [character] [action]. Anatomically correct hands with five
distinct fingers clearly separated. Face maintains exact design from
input image — no morphing, no feature changes. Single consistent light
source from [direction]. Static camera, locked-off. Background completely
still, preserve exactly as in input image.
```

### Action Shot (Anti-Morph)
```
[STYLE LOCK BLOCK]
[Character] performing [specific action with clear start/end poses].
Motion is [speed]: smooth and readable, not frantic. Hands: [describe
exact hand positions and contact points]. One dominant camera movement:
[static / slow push-in / pan left]. No conflicting camera instructions.
```

### Negative Prompt Bank (copy-paste)
```
3D render, photorealistic, CGI, cinematic, subsurface scattering,
realistic skin, pore detail, volumetric lighting, ray tracing,
octane render, unreal engine, plastic skin, wax figure,
synchronized movement, lockstep, choreographed, mirrored poses,
morphing, warping, extra fingers, fused hands, disappearing objects,
changing faces, inconsistent lighting, flickering
```

---

## REGENERATION DECISION TREE

```
Defect found in QC
    │
    ├─ Is it in 1-2 frames? → CUT those frames or cover with reaction shot
    │
    ├─ Is motion good but style drifted? → EbSynth keyframe OR 2D filter pass
    │
    ├─ Is motion synced but style OK? → Stagger in edit (offset layers 3-8 frames)
    │
    ├─ Is it a single character issue? → Regenerate as isolated element, composite
    │
    ├─ Is the whole shot bad? → Full regenerate with defect-proof prompt
    │       │
    │       └─ Regeneration still drifts? → Try 2 more times max
    │               │
    │               └─ Still bad after 3? → Manual repair (rotoscope/paint)
    │                       or CUT the shot
    │
    └─ Can't fix and can't cut? → Document as known issue, ship it
```

**The 3-attempt rule:** If regeneration doesn't fix it in 3 tries with adjusted prompts, stop generating and switch to manual repair or editorial solutions. Endless regeneration is not a strategy.

---

## SOURCES & FURTHER READING

- Higgsfield: "AI Video Prompt Mistakes" — https://higgsfield.ai/blog/ai-video-prompt-mistakes
- Higgsfield: "Keep Characters Consistent" — https://higgsfield.ai/blog/keep-characters-consistent-ai-animated-series
- TalkMarkets: "Practical Framework for Reviewing AI Video Transformations" — https://talkmarkets.com/article/a-practical-framework-for-reviewing-ai-video-transformations-346132
- Dev.to: "Symmetrical Choreography in Latent Video" (dual-character sync causes) — https://dev.to/theomarsh/symmetrical-choreography-in-latent-video-engineering-the-dual-character-apt-music-video-pipeline-27ad
- Dev.to: "Seedance Prompt Failures" (camera-verb collision, jitter causes) — https://dev.to/hamimelon2026_40bd96eff01/seedance-prompt-failures-whats-actually-causing-the-jitter-deformation-and-wrong-references-46mp
- Medium: "Why AI Videos Feel Fake" (character anchors, environment consistency) — https://medium.com/budgetpixel-ai/why-ai-videos-feel-fake-and-how-consistency-fixes-everything-7c9dc9aa5720
- PCWorld: "Why Your AI Videos Look Distorted" (multi-subject limits, sequential framing) — https://www.pcworld.com/article/3057497/why-your-ai-videos-look-distorted-and-5-fixes-that-actually-work.html
- MITO: "Keep AI Video Characters Consistent" (negative constraints technique) — https://mito.ai/blog/how-to-keep-ai-video-characters-consistent/
- ScienMag survey: "AI Video Generation Gets Human" (temporal consistency gaps) — https://scienmag.com/ai-video-generation-gets-human-a-new-survey-maps-the-fields-biggest-hurdles/

---

*End of Field Guide v1.0. Update this doc every time a new defect is found or a new fix is proven.*
