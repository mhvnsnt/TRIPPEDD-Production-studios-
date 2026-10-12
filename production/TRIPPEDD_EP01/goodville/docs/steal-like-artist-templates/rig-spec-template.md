# CHARACTER RIG SPEC TEMPLATE
## Adobe Animate Puppet Rig — Based on professional conventions
## See `study-notes/fla-rig-conventions.md` for the full breakdown

**Show:** [Show name + code, e.g., WG = Wizard Gang]
**Character:** [Character name]
**Episode/Production code:** [e.g., 201]
**Version:** [001, 002... — increment on every save, never overwrite]
**Artist:** [Your initials]
**Date:** [YYYY-MM-DD]
**Status:** [rough / clean / cleanup / final]
**File name:** `[CODE][epcode]_ORIGINAL_PUPPET_[CHARACTER]_VERSION_[###].fla`

> Example: `WG201_ORIGINAL_PUPPET_ASHES_VERSION_001.fla`

---

## 1. TIMELINE SETUP

| Setting | Value |
|---------|-------|
| Frame rate | 25 FPS (broadcast) / 24 (film) / 30 (web) — pick one per project |
| Stage size | [e.g., 1920×1080] |
| Safe areas | [ ] 14:9 safe guide placed |
| | [ ] 6:9 safe guide placed |

---

## 2. LAYER HIERARCHY

*Every body part on its own named layer. No "Layer 1". Character's left/right (not viewer's).*

```
[CODE]_[CHARACTER]  (top-level layer)
├── head
│   ├── skull_base
│   ├── eyes (→ nested symbol: eye expressions)
│   ├── pupils
│   ├── brows
│   ├── nose
│   ├── mouth (→ nested symbol: viseme frames)
│   ├── ears_L
│   ├── ears_R
│   └── [character-specific: horns, hat, etc.]
├── neck
├── torso
│   ├── chest
│   └── belly
├── arm_L_upper
├── arm_L_lower
├── hand_L (→ nested symbol: hand poses)
├── arm_R_upper
├── arm_R_lower
├── hand_R (→ nested symbol: hand poses)
├── leg_L_upper
├── leg_L_lower
├── foot_L
├── leg_R_upper
├── leg_R_lower
├── foot_R
└── [character-specific: tail, wings, accessories]
```

*Delete rows that don't apply. Add character-specific parts.*

---

## 3. NESTED SYMBOLS

### Mouth Symbol
- **Type:** Graphic Symbol (NOT MovieClip — must sync to main timeline)
- **Frames:** One per viseme + character-specific shapes
- **Playback:** Single frame (stepped via timeline)

| Frame | Viseme | Label |
|-------|--------|-------|
| 1 | Closed / Rest | `rest` |
| 2 | Ah | `ah` |
| 3 | Ee | `ee` |
| 4 | Oh | `oh` |
| 5 | Oo | `oo` |
| 6 | M/B/P | `mbp` |
| 7 | F/V | `fv` |
| 8 | L | `l` |
| 9 | Hiss (S/K/G/Z) | `hiss` |
| 10 | W | `w` |
| 11+ | [Character-specific] | |

### Hand Symbols (L and R)
- **Type:** Graphic Symbol
- **Frames:** One per pose

| Frame | Pose | Label |
|-------|------|-------|
| 1 | Relaxed / Neutral | `neutral` |
| 2 | Open palm | `open` |
| 3 | Fist | `fist` |
| 4 | Pointing | `point` |
| 5 | Gripping | `grip` |
| 6+ | [Character-specific] | |

### Eye Symbol
- **Type:** Graphic Symbol
- **Frames:** Neutral, blink, happy, angry, sad, surprised + character-specific

---

## 4. REGISTRATION POINTS

| Symbol | Registration | Notes |
|--------|-------------|-------|
| Head | Center of neck joint | Rotates naturally on neck |
| Upper arm | Shoulder joint | |
| Lower arm | Elbow joint | |
| Hand | Wrist joint | |
| Upper leg | Hip joint | |
| Lower leg | Knee joint | |
| Foot | Ankle joint | |

*Set registration points BEFORE animating. Wrong pivots = broken puppet.*

---

## 5. VERSION LOG

| Version | Date | Artist | Changes |
|---------|------|--------|---------|
| 001 | | | Initial rig |
| | | | |

---

## 6. QC CHECKLIST (before marking "final")

- [ ] Every layer has a descriptive name (no "Layer 1")
- [ ] Mouth symbol syncs correctly (test with a dialogue line)
- [ ] Hand poses all present and labeled
- [ ] Registration points set on all rotating joints
- [ ] Rig matches the character model sheet (proportions, colors)
- [ ] Tested with a walk cycle (no broken joints)
- [ ] Tested with a dialogue test (mouth shapes readable)
- [ ] File named per convention with version number
- [ ] Previous version preserved (not overwritten)

---

*Template version: 2026-10-12*
*Based on observed professional Animate puppet conventions.*
*Build YOUR characters with this structure.*
