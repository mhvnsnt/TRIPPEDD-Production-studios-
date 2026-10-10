# Mocap plan — WIZARD_GANG_SHORT_01

**Law:** real storyboard + REAL MOCAP. Never procedural bone-wiggling, never a "possessed mannequin." Every character motion in SHORT 01 comes from real motion-capture data retargeted onto canon character rigs. Camera moves are camera animation — they are not character animation and must never be presented as such.

## Exact mocap sources

1. **Mixamo (Adobe) — free animation library**
   - License: free for use, including commercial. Royalty-free.
   - Clips for SHORT 01: "Standing Idle", "Standing Idle 2" (subtle weight shift), "Turn Head", "Look Around", "Lean In", "Arm Raise Slow".
   - Use: shots 2–6, 8. Each clip retargeted per character; no clip reused identically across two characters without variation.
2. **CMU Graphics Lab Motion Capture Database**
   - License: free for research/commercial use with attribution.
   - Clips: ambient stand/walk cycles for the rooftop silhouette background figures in shot 1.
   - Use: background only, never hero characters.
3. **Owner-recorded reference (optional, future)**
   - The Narrator's direct-address beat (shot 9) may eventually be driven by owner-captured reference. Not required for SHORT 01. Never synthetic filler.

## Retarget path

- **Primary:** the Forge3D universal retargeter (rig-handoff stage — in progress, owner-architecture-review pending). Character-ready GLBs + retargeted mocap is the 150% Forge3D ladder target.
- **Fallback:** Mixamo auto-rigger on the canon robed GLBs if the Forge3D retargeter is not yet greenlit. The fallback must still be real mocap data on a real rig — procedural animation is not an allowed fallback.
- **Hard requirement:** robed character GLBs must exist before capture. The 8 renders are images, not models. If robed GLBs are not yet generated, SHORT 01's production method goes to the owner as a storyboard-approval question: (a) wait for robed GLBs, or (b) approve a staged-stills pass (camera moves + parallax + composited lighting on approved key art) as the v1 cut. Staged stills are honest cinematography, not fake mocap — the package metadata marks them as such.

## Explicitly forbidden

- Procedural bone animation, noise-driven idle, or any "wiggle" system on hero characters.
- AI video generation of character performance as a substitute for mocap (per the owner's promo-video law — generated material is for concept shots, transitions, or clearly labeled generated content only).
- Reusing another game's character motion data or footage.
