# Episode 01 — SC-01 The Awakening — Shot List

**Canon:** Near-black space, tiny colored stars, cyan rim light. Mars identity locked.  
**Line:** *“Yeah. That happens sometimes.”*  
**Asset:** `MARS_CANONICAL` only. Gaussian off.

---

## SH-001 — White Eye CU

| Field | Spec |
|-------|------|
| **Framing** | Extreme close-up, one or both solid white eyes filling frame |
| **Lens feel** | ~85–100mm equivalent, shallow but not pretty-portrait bokeh — slightly digital |
| **Light** | Cyan rim from camera-left rear; no warm key |
| **Duration** | 2–3 sec |
| **Action** | Micro drift only; eyes do not track like realistic lids unless shape keys exist |
| **Audio** | Soft void bed; optional wet/throat pre-echo from cold open |
| **QC** | Identity recognizable at crop; no generated eye texture swap |

## SH-002 — Pull to Cobalt + Dreads

| Field | Spec |
|-------|------|
| **Framing** | Start tight on mid-face → pull to full floating head + partial dread silhouette |
| **Background** | True black / near-black + sparse multi-hue stars (small, sparkly, not NASA plate) |
| **Light** | Cobalt skin reads saturated; indigo/violet dreads hold detail then fall into black |
| **Duration** | 4–5 sec |
| **Action** | Head float stable; optional slow Y-axis drift ≤5° |
| **Sigil** | Forehead emboss catches cyan once — not a neon sticker |
| **QC** | Neck geometry present (no floating face cut); dread mass matches canonical |

## SH-003 — Deadpan Line

| Field | Spec |
|-------|------|
| **Framing** | Medium close-up, head centered slightly low in frame (void weight above) |
| **Performance** | Mouth: closed → minimal aperture only if oral PASS; prefer subtle jaw if survey green |
| **Dialogue** | *“Yeah. That happens sometimes.”* |
| **Lip-sync** | Real Rhubarb JSON or **deliberate non-sync mute-adjacent** deadpan — never fake cues |
| **Duration** | 3–4 sec + 1 sec hold |
| **Edit** | Hold after line; do not jump-cut away the awkwardness |
| **QC** | If mouth opens: protrusion gate PASS in evidence packet |

---

## Camera / world notes

- World seed not required in pure void plates; if any “room” reflection appears, tag `GM-WORLD-0001` / seed `742918` in manifest.
- Stars are graphic, sparse, multi-colored — bible, not stock milky way.
- Resolution: prefer show delivery target; memory-safe proof may use 640×360 for pipeline only.

## Evidence package for SC-01

- Frames or stills on disk  
- `mars_sha256`  
- Oral survey JSON if SH-003 uses aperture  
- Contact sheet  
- No telemetry-as-final  
