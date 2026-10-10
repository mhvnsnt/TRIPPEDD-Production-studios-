# Episode 01 — SC-03 The Room Recurses

**Canon:** The room contains a room; scale error is the joke and the cosmology.  
**Seed:** parent `742918` (`GM-WORLD-0001`); optional child seed recorded with parent id.  
**Exit from:** Tonnō Pass (cheap renderer cracks; too much infinity for the palette).

---

## Premise

Mars is not *visiting* a room in his mind. The room is a **scale of his substrate**. When the camera pushes through a door, window, molar, or UI panel, it enters another interior that should not fit.

Additive gag (optional): zoning stickers, “Kevin District” graffiti, a streetlight the size of a tooth — only if oral/world plates support it.

---

## Shots

### SH-010 — Palette Break

| Field | Spec |
|-------|------|
| **Action** | Tonnō limited palette **fails upward** — one surface gains continuous shading the game UI cannot afford |
| **Duration** | 1–2 sec |
| **Audio** | Bit-crush drops out mid-tone |
| **QC** | Still same Mars hash if he is in frame |

### SH-011 — Threshold

| Field | Spec |
|-------|------|
| **Framing** | Door / arch / mouth-aperture / CRT frame as portal (pick one per cut; mouth only if oral PASS) |
| **Push** | Camera crosses threshold; parallax on procedural low-poly from seed |
| **World** | `GM-WORLD-0001` memory-safe geometry or higher instance count if farm allows |
| **Duration** | 3–5 sec |
| **Manifest** | `world_seed: 742918`, `scene_id: GM-WORLD-0001` |

### SH-012 — Scale Error Reveal

| Field | Spec |
|-------|------|
| **Image** | Architectural space where one object is molar-scale wrong (streetlight, chair, sun) |
| **Mars** | Optional: tiny in frame or reflected; never a second generated face |
| **Line (optional)** | *“This used to be a thought.”* / *“We’re over occupancy.”* |
| **Duration** | 4–6 sec |
| **Gaussian** | Still **off** for first proof; splat detail only after creative-final plate exists |

### SH-013 — Recurse Beat

| Field | Spec |
|-------|------|
| **Action** | Visible smaller doorway inside the room, same proportion language |
| **Hold** | Let the audience see the pattern without explanation |
| **Duration** | 2–3 sec |
| **Rule** | Do not VO-explain the infinite regress |

---

## Environment production

```
seed 742918
  → procedural / low-poly layout (build_memory_safe_scene or worldgen export)
  → OpenUSD World/Procedural layer (environments/GM-WORLD-0001/GM-WORLD-0001.usda)
  → optional SplatEnv later (ParticleField3DGaussianSplat)
  → composite with Mars ref
```

**Memory-safe defaults:** 640×360, ≤96 instances, Gaussian disabled, 8-frame proof before hero lengths.

---

## QC

- [ ] Seed + scene id in manifest  
- [ ] Mars sha256 if character in frame  
- [ ] No telemetry creative_final  
- [ ] Mouth portal path ⇒ oral protrusion PASS  
- [ ] Tonnō exit was style, not a failed SC-01 render  
