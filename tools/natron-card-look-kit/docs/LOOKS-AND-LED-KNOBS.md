# LOOK + LED gizmo pack — knobs and sources (SPEC N-3)

Every value below comes from the cape-jones pipeline. Nothing here is a
new look. Canon stack order: **lights → render look → finish grade.**

## The two looks (canon)

Source: `mhvnsnt/cape-jones` `docs/lighting/RENDER-LOOKS.md` +
`production/pipeline/render_looks.py` (PR #264, merged 2026-10-29).

| | LOOK 1 — PALE WASH | LOOK 2 — DEEP SATURATION |
|---|---|---|
| Feel | flat, pale, washed-out; everyday rooms, daylight, talking scenes | rich, punchy; walls deep, blacks blacker; night + LED + moody scenes |
| Canon definition | Blender view transform **AgX** (built-in OCIO) | **ACES 1.0 - SDR Video** via the ACES cg-config OCIO (`cg-config-v2.1.0_aces-v1.3_ocio-v2.1.ocio`) |
| Default? | **Yes — a scene with no named look is LOOK 1** | picked per scene |
| Proof (canon) | Scene 1 frame 40: pale lavender-pink | same frame: deep magenta, hot coral chair, properly black cape |

### Exact route (linear plates)

If the plate arriving in Natron is a scene-linear EXR, the look is a
colour-management step, not a grade: set the project/view to the same
transform as canon (Blender AgX config for LOOK 1; the cape-jones ACES
cg-config for LOOK 2, view `ACES 1.0 - SDR Video`). Natron is
OCIO-managed (it ships `blender` and `nuke-default` OCIO configs under
`Resources/OpenColorIO-Configs/`; point the project at the cape-jones
ACES config file for LOOK 2 exactness).

### Gizmo route (display-referred plates — the normal comp case)

The gizmos translate the looks for plates that are already
display-referred (PNG/MP4 plates, 2D animation, Pipeline One cards),
using the cape-jones finish-grade family (`grades.py`) as the bridge:

| Gizmo | Chain | Baked values (source) |
|---|---|---|
| `CJLook1PaleWash` | Saturation → Grade | saturation **0.82**, gamma lift **1.12** — the pale/desaturated end of the grade family (cf. `outside-storm` sat 0.85; AgX's own desaturating shoulder) |
| `CJLook2DeepSaturation` | Saturation → Grade | saturation **1.45**, contrast **1.10**, blackPoint **−0.02** — `cj-day` sat 1.35 / contrast 1.08, `cj-royal` sat 1.45 / contrast 1.10, `outside-acid` sat 2.0 is the ceiling the family never exceeds for a base look |

**Knobs:**

- LOOK 1: `Saturation Scale` (×0.82; 1.0 = canon), `Lift (Gamma)`.
- LOOK 2: `Saturation Scale` (×1.45), `Contrast` (canon 1.10),
  `Black Lift` (canon −0.02; negative deepens, never crush — the cape
  #000000 is deepened, not crushed, per `grades.py` header).

## LED gizmos

Sources: static LED grades in `grades.py`; glow in `comp_glow.py`;
animated hue-cycling versions stay in `led_controller.py` (ffmpeg,
time expressions) — the Natron groups are the static comp form;
animate `Tint`/`Glow Strength` for movement.

Translation: an ffmpeg `colorchannelmixer` matrix's **diagonal**
(rr/gg/bb) is a per-channel gain = a Natron **Multiply** tint; `eq
saturation/contrast` map 1:1 to Saturation + Grade gamma. Off-diagonal
mixer terms are small (≤0.25) cross-talk; they are listed here for the
record and are the first thing to add if a plate match ever fails.

| Gizmo | grades.py key | Matrix (mixer) | eq | comp_glow.py glow |
|---|---|---|---|---|
| `CJLedDeepPurpleGlow` | `led-deep-purple` | rr=1.0 rb=0.25 / gg=0.80 gb=0.15 / br=0.20 bg=0.05 bb=1.30 → tint (1.0, 0.80, 1.30) | sat 1.40, contrast 1.10, bright −0.01 | `neon-sign` glow 0.6, light-wrap 0.3 |
| `CJLedPartyGlow` | `led-party` | rr=1.15 rb=0.10 / gg=1.05 gb=0.10 / br=0.10 bg=0.05 bb=1.15 → tint (1.15, 1.05, 1.15) | sat 1.80, contrast 1.12, bright +0.02 | `energy-blast` glow 1.0, light-wrap 0.7 |

Other static LED grades in `grades.py` (`led-chill-blue`,
`led-sunset`, `led-ghost-teal`, `led-ember`) follow the same
translation — copy a gizmo, change TINT/SATURATION/CONTRAST at the top
of the file (they are named constants), rename the plugin ID/label.

**Knobs (both LED gizmos):** `Intensity (Mix)` (Grade mix; 1.0 =
canon), `Saturation Scale` (×baked), `Glow Strength` (Merge mix of the
screen-blended blur; canon per table, 0 = grade only), `Glow Size`
(blur size; comp_glow.py scales sigma 8 + 20×glow, default 16 ≈ the
neon-sign range).

**Palette law carried over from `grades.py`:** signature grades
protect the white suit (#FFFFFF stays blown out, never tinted); LED
grades intentionally tint the whole frame — that is what LED strips do
to a real room. The LED gizmos are LED-only for that reason; do not
use them as general grades.
