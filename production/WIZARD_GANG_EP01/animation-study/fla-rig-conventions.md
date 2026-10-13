# Adobe Animate Puppet Rig — Production Conventions
## Observed from CN Gigaleak (Gumball production files)

> These are FACTS about file naming and organization observed in production.
> No copyrighted content reproduced. Use these conventions for YOUR rigs.

---

## 1. FILE NAMING CONVENTION

### Master Puppet Files
```
GB[production-code]_[DESCRIPTION]_VERSION_[###].fla
```
**Example:** `GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla`

| Part | Meaning |
|------|---------|
| `GB` | Show code (Gumball) — use your show's code |
| `200` | Production/episode code |
| `ORIGINAL_PUPPET_GUMBALL` | Description in CAPS_WITH_UNDERSCORES |
| `VERSION_008` | Version number, zero-padded to 3 digits |

**Rule:** NEVER overwrite a version. Save as new version number. Old versions are history.

### Scene/Shot Files
```
GB[code]REMOTE_Sc[###]_[Clean|Cleanup]_V[###]_[INITIALS].fla
```
**Examples:**
- `GB202REMOTE_Sc094_Clean_V023_STN.fla`
- `GB202REMOTE_Sc103_V0024_cleanup_LW.fla`

| Part | Meaning |
|------|---------|
| `REMOTE` | Produced remotely (outsourced or off-site) |
| `Sc094` | Scene 94 |
| `Clean` / `cleanup` | Pipeline stage |
| `V023` / `V0024` | Version (note: inconsistent padding — pick one and stick to it) |
| `STN` / `LW` | Artist initials (who did this version) |

### Pipeline Stages (in order)
1. *(no tag)* — rough / layout
2. `REMOTE` — sent out for production
3. `Clean` — cleaned-up animation
4. `cleanup` — final cleanup pass

**Lesson:** The filename IS the production tracker. Anyone can read a filename
and know: what show, what scene, what stage, what version, who touched it last.

---

## 2. TIMELINE SETUP

| Setting | Value | Notes |
|---------|-------|-------|
| Frame rate | 25.00 FPS | PAL broadcast standard |
| Safe areas | "14:9 safe" and "6:9 safe" | Broadcast safe-area guides on every file |

**Apply to your work:** Set 25 FPS for broadcast, add safe-area guides.
(Or 24 FPS for film / 30 FPS for web — but PICK ONE per project.)

---

## 3. LAYER NAMING CONVENTION

### Top-Level Layer
```
GB[code]_[CHARACTERNAME]
```
**Example:** `GB200_GUMBALL`

### Sub-Layers
Descriptive names for each body part / component, nested under the character layer.

**Puppeting principle** (confirmed by Foster's Home production interviews):
> Individual parts of the character's body are on separate layers,
> contained inside the symbol of the character. Parts are moved via
> tweening or step-by-step animation.

**Standard sub-layer structure for a character puppet:**
```
GB200_GUMBALL
├── head
│   ├── eyes
│   ├── pupils
│   ├── brows
│   ├── nose
│   ├── mouth (→ mouth chart symbol with viseme frames)
│   └── ears
├── torso
├── arm_L_upper
├── arm_L_lower
├── hand_L (→ hand pose symbol)
├── arm_R_upper
├── arm_R_lower
├── hand_R (→ hand pose symbol)
├── leg_L_upper
├── leg_L_lower
├── foot_L
├── leg_R_upper
├── leg_R_lower
├── foot_R
└── tail / accessory (character-specific)
```

**Rules:**
- Left/Right designated as `_L` / `_R` (character's left/right, not viewer's)
- Mouth is a nested SYMBOL containing viseme frames (not separate layers)
- Hands are nested SYMBOLS containing pose frames
- Every layer name is descriptive — no "Layer 1", "Layer 2"

---

## 4. SYMBOL NESTING STRATEGY

```
Character (MovieClip Symbol)
└── Body Parts (Layers)
    └── Mouth (Graphic Symbol → frames = visemes)
    └── Hands (Graphic Symbol → frames = poses)
    └── Eyes (Graphic Symbol → frames = expressions)
```

**Why Graphic Symbols (not MovieClips) for mouths/hands/eyes:**
- Graphic symbols sync to the main timeline (frame-accurate lip sync)
- MovieClips run on independent timelines (harder to sync)
- Graphic symbol frames can be stepped through with "single frame" playback

---

## 5. ADOPT THIS FOR YOUR RIGS

**Naming template for YOUR shows:**
```
[SHOWCODE][epcode]_[DESCRIPTION]_VERSION_[###].fla
```

**Examples for Wizard Gang:**
- `WG201_ORIGINAL_PUPPET_ASHES_VERSION_001.fla`
- `WG201_ORIGINAL_PUPPET_STATIC_VERSION_001.fla`

**Examples for Goodville:**
- `GV101_ORIGINAL_PUPPET_DICKIE_VERSION_001.fla`

**Checklist for every new puppet:**
- [ ] 25 FPS timeline (or your project's standard)
- [ ] Safe-area guides on stage
- [ ] Top layer named `[CODE]_[CHARACTER]`
- [ ] Every body part on its own named sub-layer
- [ ] Mouth as nested graphic symbol with viseme frames
- [ ] Hands as nested graphic symbol with pose frames
- [ ] No "Layer 1" — every layer has a real name
- [ ] Version number in filename, incremented on every save
- [ ] Artist initials on scene files

---

*Documented from observed production files, 2026-10-12*
*For study purposes — apply the conventions, not the characters.*
