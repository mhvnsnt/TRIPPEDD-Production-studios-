# Natron finishing recipes — Pyro Shaping Pack (SPEC H-4)

How each pyro look is finished in Natron after the Cycles render. These are
*recipes* (node chains + knob values) that sit **downstream of the studio's
existing grade canon** — they do not replace it:

- **LOOK 1 Pale Wash** — the cape-jones pale lavender-pink grade.
- **LOOK 2 Deep Saturation** — the cape-jones hot, saturated grade.

Node names are Natron 2.5 built-ins / OpenFX-misc names. The packaged gizmo
versions of LOOK 1 / LOOK 2 themselves are SPEC N-3 (another lane's item);
these recipes assume the plate already passes through that grade node, and
each recipe says where it taps in: **[PRE]** = before the LOOK grade,
**[POST]** = after it.

General rules for all five: work in 32-bit linear, render pyro plates as
multi-layer EXR (`density`/`temperature` rides along in the file), premultiply
only once at the final Merge, and never sharpen a volume — volumes get glow
and grade, never detail enhancement.

---

<a id="jet-flame"></a>
## Jet Flame — pairs with LOOK 2 Deep Saturation

Chain: `Read (pyro EXR)` → `Shuffle (temperature → rgb)` → **[PRE]**
`Grade (gain 1.15 on the temperature pass only)` → `Merge (plus)` over the
beauty → **[POST-LOOK]** `Glow (OpenFX Arena) threshold 0.85, size 6, mix 0.35`.

- The jet is a lance: keep the core near-white. If the core clips before the
  grade, pull the **[PRE]** Grade gain down, never the LOOK's saturation.
- No blur on the density pass — a soft jet reads as a leak, not a thruster.
- Cape Jones hand-cannon shots: duplicate the Glow, set the copy to
  `mix 0.15, size 18` for the room-spill halo.

<a id="campfire"></a>
## Campfire — pairs with LOOK 2 Deep Saturation

Chain: `Read` → **[POST-LOOK]** `Glow threshold 0.7, size 10, mix 0.3` →
`Grade (lift -0.01, gamma 1.03)` → `Merge (over)`.

- Campfire is the warm anchor of a scene: after the glow, warm the *plate
  around it*, not the flame — a `ColorCorrect` on the background plate with
  `master gain (1.04, 1.0, 0.94)` sells the light spill.
- Flicker is already in the sim (noise time animation); do **not** add a
  comp flicker on top or the two fight.
- Wizard Gang hearth plates: this is the default recipe, unchanged.

<a id="explosion-burst"></a>
## Explosion Burst — pairs with LOOK 2 Deep Saturation (LOOK 1 on the flash frame)

Chain: `Read` → `Shuffle (temperature)` → frame-held `WhiteBalance flash`
→ **[POST-LOOK]** `Glow threshold 0.55, size 14, mix 0.5` → `Grade` rolloff.

- **Flash frame only** (the emission peak, usually the first fully-formed
  frame): route that single frame through **LOOK 1 Pale Wash** instead of
  LOOK 2 — the pale flash against the saturated roll is the house burst
  signature. Implement as a `Switch` driven by a one-frame `TimeOffset` hold,
  or simply grade the burst as its own pre-comp and cut the flash frame in.
- Highlight rolloff: final `Grade` with `whitepoint 0.92` so the fireball
  core rolls off instead of clipping to a flat disc.
- Add `Erode` (−1) on the alpha of any holdout matte used against the burst;
  the sim's edge is turbulent and a hard matte edge reads instantly.

<a id="chimney-smoke"></a>
## Chimney Smoke — pairs with LOOK 1 Pale Wash

Chain: `Read` → **[POST-LOOK]** `ColorCorrect (saturation 0.92, gamma 1.05)`
→ `Merge (over)` → optional `Grain` match.

- Pale Wash already desaturates toward lavender; chimney smoke must stay
  *neutral* inside it, so the slight extra desaturation above keeps it from
  picking up a pink cast.
- No glow, no sharpening. If the smoke reads too clean against a live plate,
  match plate grain at the end (`Grain`, size matched to the plate) — smoke
  is the first thing that betrays a comp when its grain differs.
- Keep the smoke's blacks lifted with the plate: never let volume black go
  below the plate's black point.

<a id="fog-bank"></a>
## Fog Bank — pairs with LOOK 1 Pale Wash

Chain: `Read` → `Shuffle (depth/Z)` → **[PRE]** `Grade (gain 0.9)` →
`Merge (over, mix ramped by depth)` → **[POST-LOOK]** `Blur size 2` on the
fog layer only.

- Fog depth-fades the scene behind it: where a Z pass exists, drive the
  Merge `mix` with a `Ramp`/expression on depth so near fog stays thin and
  far fog stacks — one fog plate then serves a whole dolly move.
- A character sitting *inside* the fog (the Pipeline One gag setup): render
  the character with a holdout matte, comp character over fog-back, then
  fog-front (same plate, `mix 0.35`) over the character. Edges stay clean
  because both fog layers are the same sim.
- Pale Wash + fog is deliberately low-contrast; resist adding contrast in
  comp. If the shot needs a focal point, warm one practical light in the
  plate instead.
