# MARS Parallel Face Lanes

The face is developed as isolated, measurable lanes so one deformation cannot be mistaken for another.

| Lane | Authority | Status / next gate |
|---|---|---|
| Eyes / blink | Owner-drawn eyelid linework | **PROTECTED** — do not rebuild unless a measured regression/improvement is proven; require OPEN/HALF/CLOSED/HALF/OPEN proof |
| Nostrils / nose | Owner-drawn yellow nostril rims | **PROTECTED** — preserve the measured new-key result; depth remains UNKNOWN until independently measured; no legacy-key contamination |
| Mouth / oral | Existing oral measurements + linework | **PROTECTED** — preserve current geometry/material authority; only local measured correctives allowed |
| Brows | Owner-drawn red brow lines | **BUILD** — independent brow controls, zero accidental blink coupling |
| Ears | Measured source geometry | **BUILD** — independent L/R controls; helix/antihelix/concha/tragus/antitragus/lobule/rim; six-view proof |
| Hair | Measured source geometry | **BUILD** — root attachment → equilibrium pre-roll → deforming collision → edge contacts → penetration gate → motion proof |
| Face tissue / FACS | Owner linework + measured source surface | **BUILD** — local correctives only; no global remesh |

## Protection law

A lane marked PROTECTED is not fair game for a generic auto-rigger. Its existing evidence is the baseline. Any modification must demonstrate a measured improvement without degrading the baseline visual proof. If the comparison is unavailable, the lane is `UNKNOWN`, not PASS.

## Mesh quality law

The canonical MARS render surface is immutable. If the scan contains visibly oversized triangles, solve that with a **derived** high-density working mesh or local quad-preserving topology operation, never by replacing the source. Quality is evaluated by edge-length distribution, curvature/silhouette, normals, UV preservation, materials and projected detail — not triangle count alone. A derived mesh cannot become canonical merely because it has more polygons.

## Hair law

The previous 36-frame hair test demonstrated a real secondary-motion mechanism but also showed creep and insufficient settling. The completion lane therefore requires at least 120 pre-roll frames, equilibrium evidence, deforming surface collision and edge contacts. A larger motion number is not success if the hair drifts or penetrates the face.

## Depth law

An orthographic owner-drawn plate establishes 2-D observation. It does not establish hidden 3-D depth. When depth is not independently established by committed geometry or measurement evidence, the result is `UNKNOWN`.

## Integration order

1. Protect passing eyes, nostrils and mouth.
2. Measure and rig ears.
3. Build brow and local facial-tissue/FACS controls.
4. Finish hair attachment and dynamics with equilibrium and collision.
5. Build derived fine-topology working geometry only where measurement proves the source needs it.
6. Run full multi-view, multi-state facial and hair proof.
7. Integrate only receipts whose source hashes and visual evidence match the current source.
