# TEST LOG — Pyro Shaping Pack (SPEC H-4)

Date: 2026-10-30. Blender **4.5.3 LTS**
(`~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender`), headless
via `xvfb-run -a env -u PYTHONPATH`, all sim/render work serialized with
`flock /tmp/heavy-test.lock` (box discipline; other lanes were queued on the
same lock). Free RAM before the run: 3,221 MB available. Sims kept tiny:
28-resolution domain, frames 1–20, stills at frame 16, 96×96 px, Cycles
8 samples, no denoising.

## 1. Library build (all 5 looks)

`build_presets.py` applied every preset JSON to a real domain + flow object:

```
LIBRARY LOOK BUILT: campfire        resolution 48  skipped_settings: []
LIBRARY LOOK BUILT: chimney_smoke   resolution 40  skipped_settings: []
LIBRARY LOOK BUILT: explosion_burst resolution 56  skipped_settings: []
LIBRARY LOOK BUILT: fog_bank        resolution 40  skipped_settings: []
LIBRARY LOOK BUILT: jet_flame       resolution 64  skipped_settings: []
SAVED pyro_presets.blend 521179 bytes
```

**Zero skipped settings on all five looks** — every key in every JSON sheet
is a real Blender 4.5.3 Mantaflow property and was applied. (One bug was
found and fixed during the build: flow `smoke_color` is a 3-float RGB
property, not RGBA.)

## 2. Two-look sim + render difference test

`tests/test_pyro.py` applied **explosion_burst** and **fog_bank** to fresh
scenes, stepped each Mantaflow sim live (REPLAY cache) to frame 16, and
rendered one Cycles still per look. Both renders completed
(`TEST RENDER ... skipped_settings: []`, `TEST DONE`).

Measured with `tests/compare_pngs.py` (PIL + numpy) on the reopened PNGs:

| Metric (frame 16) | explosion_burst | fog_bank |
|---|---|---|
| Mean luminance | **0.0608** | **0.0227** |
| Luminance std | 0.1556 | 0.0493 |
| Mean RGB | (0.086, 0.062, 0.034) — warm, red-dominant | (0.022, 0.023, 0.023) — neutral grey |
| Hot pixels (lum > 0.5) | 2.90 % | 0.00 % |
| Lit pixels (lum > 0.05) | 15.0 % | 17.1 % |

- **Mean absolute pixel difference between the two renders: 0.0751**
- **Mean luminance ratio (burst / fog): 2.68×**

Own-eyes check of the reopened PNGs: the burst still shows a rising column
of warm amber fire voxels (blackbody temperature shading working; blockiness
is the deliberate 28-res test grid — production sheets run 56 + noise
upres 3), the fog still shows a soft, flat, ground-hugging grey bank with
no hot pixels. The two looks are measurably and visibly different systems,
not a recolour.

## 3. Artifacts (in this folder)

- `tests/output/render_explosion_burst_f016.png` — 7,660 bytes,
  SHA-256 `e7ef374930369a81439b8c708dddd9413f167b98573245713efb430d4aaf9541`
- `tests/output/render_fog_bank_f016.png` — 6,977 bytes,
  SHA-256 `0a933ae73e32da7d54646f447b210ff6bc85ad6c65da998f0041fbbc9817ab7f`
- `pyro_presets.blend` — 521,179 bytes (generated library, all 5 looks)

Reproduce: `bash tests/run_test.sh`
