# EffectorKit (SPEC C-1)

A MoGraph-style effector layer on Blender **Geometry Nodes**: a named,
ordered stack of effectors that transform cloned instances, each shaped
by a spatial falloff. Built for the bump/title cards, logo stings, and
object-crowd gags that sit between scenes in Cape Jones and Wizard Gang
episodes — the shots that used to be a fresh Geometry Nodes build every
time.

**Clean-room note.** The *behavior* (Cloner + stackable effectors +
fields/falloffs, as documented in public MoGraph documentation) was
studied from public docs only. Everything here is an original
construction from Blender's own Geometry Nodes primitives — no
third-party code, assets, or presets. Donor check first (repo law): the
repo had no existing Geometry Nodes asset library or node-group code to
reuse (checked `tools/` — absent — and code search for
`GeometryNodeTree`/`node_groups` on 2026-10-30), so this is an original
build, not a hand-rolled replacement of a donor.

## The fixed effector order

Effectors always apply in this order (stacking order *is* the
animation — reorder and the result changes):

```
EK_ClonerGrid -> EK_Plain -> EK_Random -> EK_Step -> EK_Shader
              -> EK_Sound -> EK_Delay -> out
```

`EK_EffectorStack` is a single group that wires exactly this chain and
re-exposes every effector input, prefixed (`Plain: Offset`,
`Step: Offset Per Step`, …), so the whole stack is driven from one
modifier panel. The add-on composes the same order from the individual
groups, skipping disabled effectors.

## Files

| File | What it is |
|---|---|
| `effectorkit_gn.py` | The construction library: builds every node group + the wav-spectrum bake. Single source of truth. |
| `build_effectorkit_library.py` | Generates `effectorkit_library.blend` (all groups marked as assets) + a demo shelf scene inside it. |
| `effectorkit_library.blend` | Generated artifact (small; regenerate any time with the build script). |
| `addon/effectorkit/__init__.py` | Sidebar panel add-on: pick prototype object/collection, toggle effectors, Apply; plus spectrum bake operator. |
| `demo_effectorkit.py` | Builds a 16×4 demo grid through Plain+Random+Step+Sound+Delay, saves `.blend`, renders a still. |
| `test_effectorkit.py` | Headless proof tests asserting on evaluated instance transforms. |
| `test_log.txt` | Captured output of the proof run on Blender 4.5.3. |

## Install / use

1. Regenerate (or use the shipped) library:
   `blender -b --factory-startup --python build_effectorkit_library.py`
2. Either append the `EK_*` groups from `effectorkit_library.blend`
   into your scene (they are asset-marked, so the file also works as an
   Asset Library), **or** install the add-on: zip the
   `addon/effectorkit/` folder, install via Preferences → Add-ons, open
   the **EffectorKit** sidebar tab, pick a prototype, Apply.
3. Tune parameters on the host's Geometry Nodes modifier.

## Falloff (shared by every effector)

Every effector group starts with the same falloff sockets. The falloff
produces a per-instance weight `W` in 0..1; the true influence is
`Strength × W`.

| Input | Meaning |
|---|---|
| `Falloff Mode` | 0 = None (W = 1 everywhere), 1 = Sphere, 2 = Box, 3 = Noise |
| `Falloff Use Object Center` | 1 = take the centre from `Falloff Center Object`'s location, 0 = use `Falloff Center` |
| `Falloff Center Object` | Optional object whose location is the falloff centre |
| `Falloff Center` | Centre position (when not using an object) |
| `Falloff Radius` | Sphere radius / box half-extent at which weight reaches 0 |
| `Falloff Softness` | 0 = tight core, 1 = broad shoulder (shapes the smoothstep weight curve's exponent) |
| `Falloff Noise Scale` | Spatial scale of the noise field (Noise mode) |
| `Falloff Noise Strength` | How far noise can pull the weight down (Noise mode) |

Sphere/Box share one weight curve: `smoothstep(1 − d/Radius)` raised to
`mix(3.0, 0.35, Softness)`. Box distance is Chebyshev (max axis), so the
falloff region is a rounded cube. Noise mode ignores Radius: weight =
`1 − NoiseStrength × (1 − noise(Position × NoiseScale))`.

## The effectors

All rotation inputs are **degrees** at the interface (converted to
radians inside). `Strength` is the last socket of every group unless
noted.

### EK_ClonerGrid — the Cloner
`Instance Object`, `Count X`, `Count Y`, `Spacing`. Grid of instances
centred on the origin (Size = (Count−1) × Spacing). For collections of
prototypes, use the add-on's Collection mode (it builds the same grid
with a Collection Info source and per-instance cycling).

### EK_Plain — constant offset
`Offset` (vector), `Rotation (deg)`, `Scale`. Each is multiplied by
Strength × W and applied (translate in world space, then rotate, then
scale). Scale blends from 1 (`mix(1, Scale, Strength×W)`), so W = 0
leaves instances untouched.

### EK_Random — seeded per-instance randomness
`Seed`, `Position Amount`, `Rotation Amount (deg)`, `Scale Amount`.
Two random streams (seed and seed+1000) keep position and rotation
decorrelated. Offsets are uniform in ±Amount; scale is
`1 ± Scale Amount` per axis. Same seed ⇒ same result, deterministically
(verified in tests).

### EK_Step — sequential ramp across clones
`Offset Per Step`, `Rotation Per Step (deg)`, `Scale Per Step`.
Everything is multiplied by the instance **Index**, so clone *i* gets
*i* steps: offset `i × Offset Per Step`, rotation likewise, scale
`1 + i × Scale Per Step`. This is the rising-stairs / fan-out workhorse.

### EK_Shader — image-driven
`Image`, `Mapping Scale`, `Mapping Offset`, `Offset Amount`,
`Scale Amount`. Each instance samples the image at
`Position × Mapping Scale + Mapping Offset` (so a grid maps across the
image by world position), converts to luminance, and applies
`offset = luminance × Strength × W × Offset Amount`,
`scale = 1 + luminance × Strength × W × Scale Amount`.
No image ⇒ luminance 0 ⇒ no effect.

### EK_Sound — audio spectrum
`Bands Curve`, `Cycle Length`, `Offset Amount`, `Scale Amount`.
Bake a spectrum first (add-on button, or
`effectorkit_gn.bake_spectrum_curve(wav, bands)`): the bake analyses a
.wav with a Goertzel filter bank (log-spaced bands, 40 Hz → Nyquist)
and writes a curve object whose control-point **Y** values are the
normalized band levels (point X = band position). In the group,
instance *i* reads band `i mod Cycle Length` (control points sampled
directly by index — not arc-length, so band *i* is exactly point *i*):
`offset = level × Strength × W × Offset Amount`,
`scale = 1 + level × Strength × W × Scale Amount`.
Set `Cycle Length` to the bake's band count so a row of clones becomes
a spectrum bar chart.

### EK_Delay — temporal smoothing (simulation zone)
`Factor`, `Start Frame`. The group's output positions chase their
input (target) positions: `P ← mix(P_prev, P_target, Factor × Strength
× W)` per frame, stored in a simulation zone (per-instance attribute
`ek_smooth` on the INSTANCE domain). On frames ≤ `Start Frame` the
factor snaps to 1 so the state initializes exactly on target. Lower
Factor = lazier, springier follow. Because it is a simulation, play /
 step the timeline from `Start Frame` — scrubbing backwards shows the
cached state, like any Blender sim.

## Proof

`test_effectorkit.py` (Blender 4.5.3, headless) asserts on evaluated
instance transforms from the depsgraph — not on "it rendered":
Plain's exact offset, sphere falloff weights (centre weight 0.409 =
the exact value of the documented curve at that distance), Random's
boundedness + determinism, Step's exact `i × 0.25` ramp, Shader's
white/black image split, Sound's per-instance Z matching the baked
spectrum values, Delay's geometric chase (0 → 0.4 → 0.72 → →2.0 at
Factor 0.2), the full stack, and a rendered still. See `test_log.txt`.
