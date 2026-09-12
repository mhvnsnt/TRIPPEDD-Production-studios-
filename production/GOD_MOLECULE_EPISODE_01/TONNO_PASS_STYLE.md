# Episode 01 — SC-02 Tonnō Pass — Style Spec

**Canon intent:** Reality degrades into a cheap old video-game / quantized retro digital dream. Mars realizes the universe is running on bad hardware.

**Name check:** Production references **Tonnō / Eastern Mind (Osamu Sato)**, LSD: Dream Emulator, early-3D banded limited-palette energy — not a licensed asset dump. Homage via constraints, not theft of specific IP art.

---

## What changes (story)

| From (SC-01) | To (SC-02) |
|--------------|------------|
| Near-cinematic void | Quantized, posterized, wrong FPS |
| Continuous light | Palette indexing, banding, dither |
| Stable identity mesh | Same identity, degraded *display* |
| Philosophy tone | Same deadpan, now trapped in UI |

**Hard rule:** Degradation is a **style/compositor lane**. It must not hide missing geometry, failed oral gates, or identity drift.

---

## Technical recipe (production)

### Resolution / time
- Working look: **640×480** or **320×240** nested inside HD timeline (integer scale)  
- Frame feel: **8–12 fps** hold or stepped  
- Optional: 1-frame flash of “load” artifact between SC-01 and SC-02  

### Palette
- Limited ramp derived from **actual Mars reference frames** (cobalt, indigo, cyan, black, 1–2 accent errors)  
- Posterize / index color; allow intentional palette mistakes (one flesh-wrong pixel cluster is funnier than perfect quantize)  

### Surface
- Banding on gradients (skin → void)  
- Slight affine “affine warp” or CRT roll **once**, not constant nausea  
- Optional low-bit texture crawl on dreads only  

### UI / game layer (optional inserts)
- Fake debug string: `ROOM_RECURSE_DEPTH=1`  
- Blocky collision ghost of the recursive room  
- Not readable tutorial text — atmospheric junk  

### Audio
- Bit-crushed bed or 8-bit-adjacent tone under dialogue  
- Dialogue stays intelligible; Mars does not become a chipmunk unless showrunner asks  

---

## Mars identity under Tonnō

| Allowed | Forbidden |
|---------|-----------|
| Same mesh / same likeness, displayed degraded | New generated face “in the style of” |
| White eyes as flat graphic emissive | Realistic iris recovery |
| Sigil as few-pixel emboss | Sigil redesigned |
| Oral aperture if PASS | Mouth sticker / 2D mouth that denies 3D survey |

---

## Pipeline placement

```
SC-01 beauty (or proxy)
    → style node / Comfy or Blender compositor quantize
    → QC: mars_sha256 still matches source asset
    → evidence stills + hash
```

Gaussian splats: **still off** unless a specific recursive-room plate is promoted after first creative-final exists.

---

## Exit into SC-03

Tonnō Pass ends when the “game” reveals a door/room that is **too detailed** for the palette — hard cut or snap back toward seed-world geometry (Room Recurses). Joke: the cheap renderer was a coping mechanism for infinity.
