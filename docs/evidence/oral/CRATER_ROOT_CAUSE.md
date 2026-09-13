# THE CRATER IS REAL, AND ITS CAUSE IS THE LOFT FLATTENING HIS OWN LIP LINE

> *"when the mouth is closed the lips should meet. At rest it should be maybe a little
> opening slightly in the middle ... there's too many corner openings at rest."*
> — the owner

## What was banked, and what it got wrong

Banked: *"His scan is perfect. The weld is innocent. The BOOLEAN DIFFERENCE in
`oral_cavity.py` is what removes his corner skin ... narrowing the cutter from 50 mm to
38.9 mm barely helps (8 → 6), so it is not the cutter's WIDTH."*

The conclusion was right. **The control underneath it was vacuous.** It counted cells where
the nearest surface is CAVITY deeper than 15 mm — and an uncarved scan has no cavity, so it
scores 0 of 65 whatever its skin is doing. A control that cannot fail is not a control.

And narrowing with `--slit-x` "barely helped" for a reason nobody had read: **`--slit-x`
scales the contour, and the cavity body behind it is an ELLIPSE of half-width `HW = 36.5 mm`
that `--slit-x` never touches.** The 78% test narrowed the first two rings and left the
flare 69.4 mm wide. It was never a test of width.

## The question asked with one instrument that works on both heads

`tools/character/where_did_his_skin_go.py` fires the same ray at the same (x, z) into the
raw scan and into the shipped head, and prints the depth of the first surface each meets.

**44 of 483 cells across his mouth have no exterior skin on the shipped head**, where the
scan has skin at +5 … +8 mm. In those cells the shipped head's first surface is cavity at
**+31 … +47 mm**. That is the crater, and it is on his **left**: 35 cells left, 9 right —
the same asymmetry as the rest leak (721 rays left, 203 right).

**Reducing a column to its shallowest hit hides this completely.** Column-wise, all 69
columns "agree" to within 0.05 mm, because at z ±4 mm his lip and cheek are intact. The
loss is a band at the seam, z −2 … +2 mm. *A slit cannot be seen by a metric that takes a
minimum across it.*

## The mechanism

His measured inner-lip contour **sweeps 11.5 mm in depth**:

| x mm | −24.7 | −20.6 | −12.2 | −0.7 | +12.0 | +20.9 | +25.3 |
|---|---|---|---|---|---|---|---|
| y mm | **+4.2** | +4.5 | +0.2 | **−7.0** | −2.8 | +2.6 | **+4.2** |

`oral_cavity.py` lofts every ring onto a **constant y** and throws that sweep away. So at
the commissures the front rings sit *in front of his own lip line* and the cutter emerges
through his cheek; at the centre they sit 4–5 mm behind it and nothing breaches.

`tools/character/measure_cutter_breach.py` — ring points outside his head, by generalized
winding number against the raw scan:

| ring | depth | as shipped | carrying the contour's own depth |
|---|---|---|---|
| R1 aperture slit | +1.75 mm | **15 of 56**, worst 2.70 mm | 4 of 56, worst 0.77 mm |
| R2 opening out | +6.50 mm | **4 of 56**, worst 1.07 mm | **0 of 56** |
| R3–R6 cavity body | +17 … +59 mm | 0 | 0 |

Only **3 of 27,150** scan vertices fall inside the cutter — the boolean is not swallowing
his corner vertices, it is shaving the thin shell of FACES the cutter grazes on its way out
through his cheek. That is why six repairs aimed at moving vertices all failed.

## The fix, scored on carved heads before any rebuild

`tools/character/carve_ab.py` carves the same welded scan twice **with Blender's own
DIFFERENCE** — the engine that ships, not a second implementation — and
`predict_carve.py` fires the same rays at both.

```
  welded          23373 verts   46774 faces
  shipped         23830 verts   47688 faces        <- reproduces the shipped head
  contour_depth   23840 verts   47708 faces
  CONTROL  his commissures sit 0.00 mm / 0.00 mm from the welded scan

  shipped          44 of 483 cells   x -31 .. +28 mm   L 35 / R 9
  contour_depth     4 of 483 cells   x -18 .. +17 mm   L  2 / R 2

  PREDICTION: lost cells 44 -> 4   (91% of the crater closed)
```

The 4 that remain are at **x −18 … +17 mm — the centre**, which is exactly where he says
the opening belongs.

## Three controls, because a transform can be wrong and still look plausible

1. **glTF is Y-up, Blender is Z-up.** Every measured number in this repo is in the space
   Blender's importer produced. Querying the raw glTF vertices reported every ring point
   60–130 mm outside his head — the scale of a whole skull — which reads exactly like a
   cutter sticking out of his face and is entirely a transform error. Read off the bounds,
   not assumed: `blender = (x, −z, y)`.
2. **His measured commissures must lie ON the surface**, or the space is wrong. They read
   **0.02 mm / 0.00 mm**. Every tool here refuses above 3–6 mm.
3. **A loft's winding is an accident** of which contour index came first, and it flips the
   sign of every inside/outside answer while the table still looks reasonable. The cavity
   centre must read inside the cutter and a point a metre away must read outside, or the
   tool refuses.
