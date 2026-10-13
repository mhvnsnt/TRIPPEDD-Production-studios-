# WIZARD GANG — Puppet Rig Build Plan
## Gumball-style rigs for the 7 wizards

### The Cast
1. **Ashes** (Bill $aber voice) — leader, sharp teeth, grill varies
2. **Static** (Enzo Amore voice) — loudmouth
3. **Cipher** (Lio Rush feral Blackheart voice) — unhinged
4. **Sombra Negra** (Damian Priest voice) — cool, laid back
5. **Kiko** (3-layer song voice, Muta likeness) — robe guy
6. **Theory** — sighs a lot
7. **Onyx** (soft-spoken canon voice) — quiet threat

### Rig Architecture (from Gumball .fla conventions)

Each wizard gets ONE master puppet file:
```
WG[code]_PUPPET_[CHARACTER]_VERSION_[###].fla
Example: WG100_PUPPET_ASHES_VERSION_001.fla
```

**Layer stack inside each puppet** (top to bottom):
```
WG100_ASHES (root)
├── head
│   ├── hair/hat
│   ├── eyes (L/R separate for blinks)
│   ├── brows
│   ├── nose
│   ├── mouth (viseme pack — see below)
│   └── teeth (Ashes: sharp teeth layer, grill variants as swaps)
├── torso
│   └── robe (main body — wizards are robed, this is the big piece)
├── arm_L
│   ├── upper_arm_L
│   ├── forearm_L
│   └── hand_L
├── arm_R
│   ├── upper_arm_R
│   ├── forearm_R
│   └── hand_R
└── legs (mostly hidden under robes — simple stubs for walk cycles)
```

**Why this works for Wizard Gang:** they're robed characters. The robe IS the torso — one big shape, no complex clothing folds to rig. Arms and head do all the acting. This is simpler than Gumball's rigs.

### Mouth Pack (per character)
Gumball uses symbol-swapped mouth shapes. For Wizard Gang:
- Standard 8-viseme set: AI, E, O, U, M/B/P, F/V, L, rest
- Ashes gets a second set showing sharp teeth
- Cipher gets a feral variant (wider, more teeth)
- Build once per character, swap symbols on the timeline

### The 50-70% Animation Pipeline
1. **Pose keys** — you (or the board artist) pose the puppets at key story beats
2. **Timing chart** — keys placed on the timeline at your dialogue timestamps (we already have these from EP01)
3. **Tween fill** — Animate/After Effects interpolates between poses
4. **AI assist** — AI fills in-betweens INSIDE the posed constraints (not generating whole shots)
5. **12-principles QC** — squash/stretch, anticipation, follow-through checked per shot
6. **Painterly pass** — dramatic beats get the painterly treatment (your locked style)

### File Naming (Gumball convention, adapted)
```
WG[ep]REMOTE_Sc[###]_[Clean|Cleanup]_V[###]_[INITIALS].fla
Example: WG101REMOTE_Sc014_Clean_V003_MUSE.fla
```

### What to Build First
1. Ashes puppet (he has the most lines — EP01 proves it)
2. Ashes mouth pack with teeth variants
3. One test scene: Ashes "the wizards have arrived" (0:01-0:16)
4. If the test works, build the other 6 puppets

### Software
Adobe Animate is what Gumball used (.fla). Free alternative: **OpenToonz** (Studio Ghibli's software, open source) does the same puppet/tween workflow. Blender's Grease Pencil is another free path.
