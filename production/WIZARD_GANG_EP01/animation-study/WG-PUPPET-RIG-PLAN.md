# WIZARD GANG — Puppet Rig Build Plan
## Blender Grease Pencil rigs for the 7 wizards

**Software: Blender Grease Pencil** (owner approved 2026-10-13)
Why: armature-based bone rigging (real deformation, not sliding flat layers),
3D cameras for dramatic angles, lighting + compositing in the same file,
already wired up in this workspace (Blender 4.0.2).

### The Cast
1. **Ashes** (Bill $aber voice) — leader, sharp teeth, grill varies
2. **Static** (Enzo Amore voice) — loudmouth
3. **Cipher** (Lio Rush feral Blackheart voice) — unhinged
4. **Sombra Negra** (Damian Priest voice) — cool, laid back
5. **Kiko** (3-layer song voice, Muta likeness) — robe guy
6. **Theory** — sighs a lot
7. **Onyx** (soft-spoken canon voice) — quiet threat

### Rig Architecture (Gumball conventions, Blender implementation)

Each wizard gets ONE master .blend:
```
WG100_PUPPET_ASHES_V001.blend
```

**Armature** (bones, top to bottom):
```
root
├── head
│   ├── jaw (for mouth open/close + talking)
│   └── eyes.L / eyes.R (separate bones for blinks, look directions)
├── torso (robe — single big bone, minimal deformation)
├── arm_upper.L → arm_fore.L → hand.L
└── arm_upper.R → arm_fore.R → hand.R
```

**Grease Pencil layers** (inside the .blend, bound to bones):
- robe (body — one big shape, weight-painted to torso bone)
- head_base, hair/hat, eyes, brows, nose
- mouth (shape-keyed viseme set — see below)
- teeth (Ashes: separate layer, grill variants as visibility swaps)
- hands (mitten-style, simple — wizards gesture, don't finger-act)

**Why robes are easy:** one big shape, minimal deformation. Arms and head do all the acting. Simpler than Gumball's rigs.

### Mouth Pack (per character, Grease Pencil shape keys)
Standard 8-viseme set: AI, E, O, U, M/B/P, F/V, L, rest.
- Ashes: second set showing sharp teeth
- Cipher: feral variant (wider, more teeth)
- Build once per character, swap on timeline

### The 50-70% Animation Pipeline
1. **Pose keys** — pose the armatures at key story beats
2. **Timing chart** — keys on timeline at dialogue timestamps (EP01's are already mapped)
3. **Blender interpolates** — Graph Editor tweens between poses
4. **AI assist** — AI fills in-betweens INSIDE posed constraints (not whole shots)
5. **12-principles QC** — squash/stretch, anticipation, follow-through per shot
6. **Painterly pass** — dramatic beats get the painterly treatment (locked style)

### File Naming (Gumball convention, adapted)
```
WG[ep]_Sc[###]_[Clean|Cleanup]_V[###].blend
Example: WG101_Sc014_Clean_V003.blend
```

### Build Order
1. Ashes puppet + mouth pack with teeth variants (most lines in EP01)
2. Test scene: "the wizards have arrived" (0:01–0:16)
3. Other 6 puppets once the test works

### Reference Materials
- `fla-rig-conventions.md` — Gumball layer/naming conventions (concepts transfer to Blender)
- `bible-structure-analysis.md` — show bible structure
- CN gigaleak .fla files — study the RIG LOGIC (bone placement, layer separation), rebuild in Blender, don't port files directly
