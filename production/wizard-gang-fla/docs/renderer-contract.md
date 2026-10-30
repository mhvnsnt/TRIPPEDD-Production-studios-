# Renderer Contract — what the local XFL renderer can actually draw

**Date / status:** 2026-10-30, test-verified (not just code-read). Every
SUPPORTED / PARTIAL / NO verdict below names its test render or code line.
Test PNGs, logs and the proof MP4 live in `test-renders/` next to this file.
Authoring template: `xfl-skeleton/` in this folder.

**The one-sentence contract:** the renderer draws **one leaf library symbol
at a time** — a single `LIBRARY/<Symbol>.xml` whose *own* timeline contains
`<DOMShape>` vector shapes directly — keyframe by keyframe. It does **not**
assemble puppets: scenes, master symbols, symbol instances, bitmaps, masks,
tweens and matrices are all ignored or crash it. A puppet the parent lane
authors for this renderer must be **flattened**: every part that must appear
in a PNG must exist as `<DOMShape>` edges inside the one symbol file being
rendered, in final position, at the keyframe index being requested.

---

## 0. Environment (exact)

```bash
PY=/home/hatch/workspace/agent-ops/wizard-gang-industry-2026-10-29/venv/bin/python
# Python 3.12.3, shapely 2.2.0, Pillow 13.0.0, numpy 2.5.4 (verified by import)
SRC=/home/hatch/workspace/agent-ops/wizard-gang-industry-2026-10-29/src
```

System `python3` is not the proven interpreter; use the venv above.
Renderer sources (all three are the same core):

| File | Role |
|---|---|
| `src/xfl_render_local.py` | Main CLI. Full render **plus** one PNG per fill colour. Prints `bbox=` per frame to stdout — that printout is the only alignment metadata the pipeline produces (see §5). Identical to the real-hands lane's `xfl_render.py` except it also parses fraction tokens (`a/b`) in `num()`. |
| `src/render_local.py` | Thin wrapper: imports `xfl_render_local`, full renders only, returns count. Guards a missing `<timeline>` by returning `0`. |
| `src/render_all_xfl.py` | Same wrapper, but imports `xfl_render` from the **real-hands** lane (`sys.path` hard-coded to `wizard-gang-real-hands-2026-10-29/src`). Works today (test `p-render-all`), but breaks if that lane's folder moves. Prefer `render_local.py`. |
| `wizard-gang-real-hands-2026-10-29/src/xfl_render_fallback.py` | Alternative rasteriser (edge-chaining instead of shapely polygonize) for pathological self-intersecting shapes. Same input contract: it also collects only `<DOMShape>` per `<DOMFrame>`. Verified working on Charlie Front Arm (test `p-fallback`). Reach for it only when the shapely path fails/OOMs on a shape. |

Namespace the parser requires everywhere:
`xmlns="http://ns.adobe.com/xfl/2008/"` (`xfl_render_local.py:23`).

---

## 1. Renderer entry points (exact commands)

### (a) A whole scene / stage at a given frame — **THERE IS NO SUCH COMMAND**

The scene document (`DOMDocument.xml`) uses `<timelines>` (plural); the
renderer looks for `.//x:timeline/x:DOMTimeline` (singular,
`xfl_render_local.py:223`, `render_local.py:8`). Proven:

```bash
$PY $SRC/xfl_render_local.py <charlie_xfl>/DOMDocument.xml OUT --scale 3
# AttributeError: 'NoneType' object has no attribute 'iter'  (exit 1, no PNG)   [test t4-scene]
$PY $SRC/render_local.py <charlie_xfl>/DOMDocument.xml OUT Scene 3
# prints 0 (exit 0, no PNG)                                                        [test t4b-scene]
```

And it would not help if it ran: the Scene 1 timeline contains only a
`<DOMSymbolInstance libraryItemName="Charlie" …>`, and instances are never
followed (§2). Same result for the skeleton's own `DOMDocument.xml`
(test `s4-skeleton-scene`). **To "render a scene", render each leaf part
symbol separately and composite the PNGs yourself** (offsets in §5).

### (b) A single library symbol (all its keyframes)

```bash
# CLI — full + per-fill PNGs, bbox printed per frame:
$PY $SRC/xfl_render_local.py "LIBRARY/Charlie Front Arm.xml" OUTDIR [--scale 3]
#   -> OUTDIR/frame00_full.png, frame01_full.png,
#      OUTDIR/frame00_fill_FC683F.png, frame00_fill_FCFF75.png, ...
#   stdout: frame 0: faces=2 fills=['#FC683F', '#FCFF75'] bbox=(0.0, 0.0, 221.0, 343.0)   [test t1]

# Wrapper — full renders only, custom prefix, prints the count rendered:
$PY $SRC/render_local.py "LIBRARY/Charlie Back Arm.xml" OUTDIR CHARLIE_BACK_ARM 3
#   -> OUTDIR/CHARLIE_BACK_ARM_F0.png, _F1.png, _F2.png ; prints 3              [test t5]
```

Defaults: `--scale 3` in both wrappers / CLI arg; the library function's own
default is 4. Scale is a plain pixel multiplier (output = shape-units ×
scale); despite the module docstring's "supersampled" wording, `render()`
performs **no final downsample** (its resize line is an identity), so edges
are PIL-aliased at the chosen scale — pick the final scale you actually want.

### (c) A symbol at a specific swap-frame (mouth/eye substitution sets)

A substitution set is **one symbol with one keyframe per variant** — e.g.
`Charlie Mouth.xml` has 25 keyframes (0–24), `Pim Mouth.xml` 28, brow/pupil
symbols 3 each. Select the variant by keyframe index:

```bash
$PY $SRC/xfl_render_local.py "LIBRARY/Charlie Mouth.xml" OUTDIR --frames 0,11 --scale 3
#   -> frame00_full.png, frame11_full.png                                       [test t2]
```

Proven distinct: rendering all 25 Charlie Mouth keyframes gave 23 distinct
full-render hashes (2 duplicate pairs — identical drawings authored twice),
and frames 0 vs 11 differ in size and pixels (1689×1026 vs 1687×1024)
[test `t2b-mouth-all`]. The wrappers (`render_local.py` /
`render_all_xfl.py`) have **no** frame selector — they render every keyframe;
use the CLI for a single swap-frame.
Note what this is *not*: the Animate mechanism — a parent instance with
`firstFrame="1" loop="single frame"` (how `Charlie Head.xml` actually pins
the brow/mouth variants) — does nothing here, because instances don't render
at all (§4).

---

## 2. Support matrix

| Feature | Verdict | Evidence |
|---|---|---|
| Vector shapes: `<Edge edges="…">` with `!` move, `\|` line, `[` quadratic, `]` cubic segments | **SUPPORTED** | `parse_edges`/`sample` (`xfl_render_local.py:51,77`); coordinates are **twips, ÷20** (`num()` calls in `parse_edges`). Real Charlie/Pim leaf symbols render correctly (tests t1, t5, p-render-all, p-fallback). |
| Solid colour fills (`<FillStyle><SolidColor color="#RRGGBB"/>`) | **SUPPORTED** | `shape_data` (`:90`). No `color` attr → black `#000000` (real Charlie Pupil symbols rely on this). |
| Solid strokes (`<SolidStroke weight="…">` + SolidColor) | **SUPPORTED** | `shape_data` (`:90`); stroke width = `weight × scale` px, min 1. Colour-less stroke fill → black. |
| Per-fill separation PNGs | **SUPPORTED** (CLI only) | `frameNN_fill_<HEX>.png` per fill colour present — this is how individual drawn parts (e.g. the yellow hand inside the arm symbol) were lifted in the original lanes. |
| Multiple layers in one symbol | **PARTIAL — flattened** | All layers' shapes for a given frame index are merged into one image (`tl.iter(DOMFrame)` + `findall('.//x:elements/x:DOMShape')`, `:226–228`). Layer order, `locked`, `layerType`, visibility are **never read** (no such string exists in the code — grep-verified). Locked layers render exactly like unlocked ones (Charlie master test, below). |
| Multiple `<DOMShape>`s in one frame | **PARTIAL — index-collision hazard** | Shapes are merged, but the fill/stroke tables are merged **by index** (`fills_all.update(fills)`, `:241`). Proven: two rects, both `FillStyle index="1"`, red then blue → **both rendered blue, red vanished**, stdout reported only `['#0000FF']` [test `p-collide`]. Author with indices unique across *all* shapes in the frame, or one shape per frame. |
| Nested symbols / `<DOMSymbolInstance>` | **NO** | Instances are never collected — only `DOMShape` is searched for (`:228`). Master symbol `Charlie.xml` (9 layers, 7 part instances + 2 direct shapes) rendered **only its 2 direct shapes**: an orange blob + black squiggles — *not Charlie* [test t3, image inspected]. Skeleton `PosedParent.xml` (instance only) → no PNG, exit 0 [test s3]. |
| Symbol instance matrices (`<Matrix a b c d tx ty/>`) | **NO** | Never parsed anywhere. See §4 for both instance-level and shape-level proof. |
| Bitmap fills / bitmap instances (`DOMBitmapInstance`, `DOMBitmapItem`, `media/`, `LIBRARY/*.png`, `bin/*.dat`) | **NO** | No bitmap code path exists. Smiling Friends Charlie/Pim contain zero bitmaps (pure vector). The Darwin XFL's one bitmap (`REF/TEMPLATE/GB_Asset-container_Final`, `DOMBitmapItem` + `bin/M 1 1323686635.dat`) is the real-world shape of the manifest — and its symbol `GB200_ASSETT_CONTAINER.xml` contains only a `DOMBitmapInstance`. Skeleton `BitmapPic.xml` built exactly that way → no PNG, exit 0 from both entry points [tests s2/s2b]. The renderer never opens `DOMDocument.xml`'s `<media>`, the `href` PNG, or any `bin/*.dat`. |
| Gradient fills (`LinearGradient` / `RadialGradient`) | **NO** | `shape_data` looks up `SolidColor` only; a gradient fill yields colour `None`. Proven: gradient rect → face detected, `fills=[]`, image = black stroke outline on transparency, interior empty [test `p-gradient`]. (Darwin XFL contains 37 gradient references — all would lose their fill.) |
| Fill/stroke alpha (`alpha="0.5"`) | **NO — silently opaque** | `alpha` attribute never read; proven: `alpha="0.5"` red rect rendered `(255,0,0,255)` [test `p-alpha`]. Output alpha is only ever 255 (fill/stroke) or 0 (background/holes). |
| Masks (`layerType="mask"` + `parentLayerIndex`) | **NO — mask renders as ordinary art** | In test t3, `Charlie.xml`'s `body_mask` layer shape **is** the orange blob in the output (filled `#FC683F`, fully visible), and the masked `body_thingies` strokes render unclipped on top. No clipping is applied anywhere. |
| Layers: guide/hidden/folder semantics | **NO** | Same code path as masks: layer attributes are never inspected; everything with a `DOMShape` draws. |
| Frame scripts, frame labels, `<scripts>` | **NO** | The strings `label`/`script` do not occur in any renderer file (grep-verified). Only `DOMFrame/@index` is read. (Real files do carry scripts — e.g. 12 `Script` hits across the Charlie library — all inert here.) |
| Motion/classic tweens, `duration`, non-keyframe frames | **NO** | Only `<DOMFrame>` elements present in the XML are rendered, keyed by their `index`. There is no interpolation code and `duration` is never read. A 10-frame hold authored as one keyframe renders **one** PNG. Sparse keyframe indices stay sparse (Darwin `GB200_DRW_EYECOMP.xml` keyframes jump 4→9→…→276 — you'd get PNGs at exactly those indices, nothing between). |
| `<Edge cubics="…">` attribute | **NO (ignored, harmless)** | Only the `edges` attribute is parsed; `cubics`-only `<Edge>` elements (Animate writes them alongside, e.g. throughout `Charlie Mouth.xml`) contribute empty segment lists. Don't author geometry *only* in `cubics`. |
| Text (`<DOMText>`) | **NO** | Never collected. Darwin XFL carries 1,935 `DOMText` occurrences — all invisible to this renderer. |
| Stage size / background colour / scene framing | **NO** | Canvas is per-frame tight bbox of the shapes + 6 shape-units padding on every side (`render()`, `:174`). `DOMDocument` `width`/`height`/`backgroundColor` are never read. Background is transparent. |
| Whole `.fla` file as input | **NO** | The renderer takes an **extracted symbol XML file**, not a `.fla`/zip. Extract first (an XFL `.fla` is a zip: `DOMDocument.xml` + `LIBRARY/*.xml`), or use an already-extracted XFL folder such as `wizard-gang-v2-put-to-use-2026-10-29/smiling/charlie_xfl/`. For structure inventory of a `.fla`, use FlashXFLParser (§6). |

---

## 3. Minimal KNOWN-GOOD XFL skeleton (authoring template)

**Location:** [`xfl-skeleton/`](sandbox://workspace/agent-ops/fla-puppets-program-2026-10-30/xfl-skeleton/)
— full annotated inventory in its `README.md`. Contents:

```
xfl-skeleton/
  Skeleton.xfl            # marker file, content "PROXY-CS5" (as in Charlie.xfl; renderer ignores it)
  DOMDocument.xml         # <media> DOMBitmapItem + <symbols> Includes + Scene 1 (structure only; does NOT render)
  LIBRARY/
    TwoFrame.xml          # THE renderable unit: 1 graphic symbol, 2 keyframes, DOMShape-only
    BitmapPic.xml         # negative fixture: DOMBitmapInstance only -> renders nothing
    PosedParent.xml       # negative fixture: rotated DOMSymbolInstance only -> renders nothing
  media/dot.png           # 40x40 PNG named by DOMBitmapItem href="media/dot.png"
  bin/M 1 1234567890.dat  # bitmapDataHRef cache copy (PNG bytes), mirroring the Darwin layout
```

Verified run (test `s1-skeleton-twoframe`):

```bash
$PY $SRC/xfl_render_local.py xfl-skeleton/LIBRARY/TwoFrame.xml OUT --scale 3
# frame 0: faces=1 fills=['#FF0000'] bbox=(0.0, 0.0, 100.0, 50.0)
# frame 1: faces=2 fills=['#0000FF', '#00FF00'] bbox=(0.0, 0.0, 100.0, 50.0)
```

Frame 1 image inspected: blue left half, green right half, black stroke —
exactly as authored.

### The exact XML the renderer expects (from `TwoFrame.xml`)

Root — a **symbol file**, not the document:

```xml
<DOMSymbolItem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xmlns="http://ns.adobe.com/xfl/2008/"
               name="TwoFrame" itemID="00000000-00000101"
               symbolType="graphic" lastModified="1731804399">
  <timeline>
    <DOMTimeline name="TwoFrame" layerDepthEnabled="true">
      <layers>
        <DOMLayer name="Layer_1" color="#00FFFF" current="true" isSelected="true">
          <frames>
            <DOMFrame index="0" keyMode="9728">
              <elements>
                <DOMShape>
                  <fills>
                    <FillStyle index="1"><SolidColor color="#FF0000"/></FillStyle>
                  </fills>
                  <strokes>
                    <StrokeStyle index="1"><SolidStroke weight="2"><fill><SolidColor/></fill></SolidStroke></StrokeStyle>
                  </strokes>
                  <edges>
                    <Edge fillStyle1="1" strokeStyle="1"
                          edges="!0 0|2000 0!2000 0|2000 1000!2000 1000|0 1000!0 1000|0 0"/>
                  </edges>
                </DOMShape>
              </elements>
            </DOMFrame>
            <!-- index="1" keyframe: same structure, blue+green fills (indices 1 and 2) -->
          </frames>
        </DOMLayer>
      </layers>
    </DOMTimeline>
  </timeline>
</DOMSymbolItem>
```

Non-negotiable details, each proven:

1. **First `<timeline>/<DOMTimeline>` in the file is the one used**
   (`root.find(...)` in both entry points). One symbol per file.
2. **Twips**: all edge coordinates ÷ 20 → `2000` = 100 px. Decimal and
   `#hex` fixed-point tokens are accepted (that's how real files encode
   fractions/negatives); plain integers always work.
3. **Winding + fill side**: the rectangle above traverses clockwise in
   screen coords (y-down) and fills via `fillStyle1`. The identical
   rectangle with `fillStyle0="1"` rendered **0 faces** (stroke only)
   [probe in `/tmp` during authoring; re-provable in one run]. Rule:
   clockwise loop → `fillStyle1`; counter-clockwise → `fillStyle0`.
   When in doubt, copy the skeleton's pattern verbatim.
4. **Style indices are per-frame-global** (§2 collision): within one
   rendered frame, never reuse a `FillStyle`/`StrokeStyle` index with a
   different colour across shapes. One `<DOMShape>` per frame (the
   skeleton's pattern, and how the real Charlie/Pim leaf symbols are
   overwhelmingly authored) sidesteps this entirely.
5. `DOMDocument.xml` manifest entries (`<media><DOMBitmapItem … href=
   "media/dot.png" bitmapDataHRef="M 1 1234567890.dat" frameRight="800"
   frameBottom="800"/>`, `<symbols><Include href="TwoFrame.xml" …/>`) are
   included in the skeleton so the folder is a complete, honest XFL that
   Animate/FlashXFLParser can read — but **no renderer reads them**. Don't
   expect a bitmap listed there to appear in any PNG.

---

## 4. How poses are posed — **they aren't (in XFL)**

The Animate posing mechanism is the instance matrix:

```xml
<DOMSymbolInstance libraryItemName="Charlie Front Arm" symbolType="graphic" loop="single frame">
  <matrix><Matrix tx="355.65" ty="136.1"/></matrix>
  <transformationPoint><Point x="110.5" y="-39.55"/></transformationPoint>
</DOMSymbolInstance>
```

(real example, `Charlie.xml` — the master symbol is *nothing but* such
instances: scale `a="0.800064086914062" d="0.800064086914062" tx="638.45"
ty="112.9"` at scene level, per-part `tx/ty` inside `Charlie`.)

Renderer verdict, both levels proven:

- **Instance level: NO.** Skeleton `PosedParent.xml` — a `TwoFrame` instance
  with 90° rotation `a="0" b="1" c="-1" d="0" tx="100" ty="50"` and
  `firstFrame="1"` — produced **no PNG at all** from either entry point
  (exit 0) [tests s3/s3b]. The instance, its matrix, its `firstFrame` and
  its `transformationPoint` are all unread.
- **Shape level: NO.** A `<DOMShape>` given its own
  `<matrix><Matrix tx="500" ty="500"/></matrix>` rendered byte-identically
  to the untransformed shape — same bbox `(0.0, 0.0, 100.0, 50.0)`, same
  pixel counts [test `p-shapematrix`]. (Real production shapes don't carry
  shape-level matrices — 0 occurrences across the Charlie/Pim/Darwin
  libraries — but even if you write one, it's ignored.)

**So the only way to pose for this renderer is to bake the transform into
the geometry**: apply rotation/scale/translation to the edge coordinates
(twips) of the leaf symbol's `<DOMShape>`s before writing the XML, i.e.
author one flattened leaf symbol per pose. Compositing parts at different
offsets is done *after* rendering, in image space, using the bbox offsets
in §5 — not in XFL.

---

## 5. Video path — batch PNG sequence → ffmpeg: **YES, with a re-canvas step**

One CLI run already batch-renders **every keyframe** of a symbol (or the
`--frames` subset). But the raw sequence is **not** ffmpeg-ready: the canvas
is each frame's own tight bbox, so sizes jump frame to frame. Proven with
Charlie Front Arm @ scale 3: frame 0 = 699×1065, frame 1 = 988×1298
[test t1]; Charlie Back Arm: 663×1293 / 1418×895 / 1294×1437 [test t5].

Origin-correct fix (uses the renderer's own stdout bboxes — image pixel =
`(coord − bbox_min + 6) × scale`): paste each frame at
`((minxᵢ − global_minx) × scale, (minyᵢ − global_miny) × scale)` on a canvas
sized from the global bbox. A tested helper doing exactly this ships next
to this contract: **`recanvas.py`**. End-to-end proof [tests `v1-*`]:

```bash
# 1. batch-render, capturing the bbox log
$PY $SRC/xfl_render_local.py "LIBRARY/Charlie Front Arm.xml" raw/ --scale 3 > raw.log 2>&1
#    raw.log: frame 0: ... bbox=(0.0, 0.0, 221.0, 343.0)
#             frame 1: ... bbox=(78.8, -49.2, 396.2, 371.6)

# 2. re-canvas to one fixed size, origin-aligned
$PY recanvas.py raw/ raw.log seq/
#    frame 0: scale=3 offset=(0,148) -> (1224, 1298)
#    frame 1: scale=3 offset=(236,0) -> (1224, 1298)   # one distinct size

# 3. encode (pad filter guards odd dimensions for yuv420p)
ffmpeg -y -framerate 12 -i seq/frame%04d.png \
       -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" -c:v libx264 -pix_fmt yuv420p out.mp4
#    ffprobe proof: 1224x1298, r_frame_rate=12/1, nb_frames=2  [test-renders/v1-frontarm-12fps.mp4]
```

Caveats that are part of the contract:

- The sequence contains **keyframes only**. Holds/tweens are not expanded —
  duplicate or hold frames in the encoder input yourself if a keyframe must
  stay on screen longer (e.g. `ffmpeg -framerate` won't invent them).
- Sparse keyframe indices (Darwin-style 0,1,2,3,9,10,…) come out named by
  index (`frame09_full.png`), with gaps; `recanvas.py` preserves index
  numbering as `frame0009.png`, so plan the ffmpeg pattern accordingly.
- Multi-part video = render each part symbol separately, re-canvas each
  part's sequence against **one shared global bbox** if parts must stay in
  registration, then composite per frame (PIL `alpha_composite` / ffmpeg
  `overlay`). There is no XFL-level assembly step.

---

## 6. FlashXFLParser harness — verified (structure inventory only)

Prebuilt binary present (no rebuild needed):
`~/workspace/tools/FlashXFLParser/harness/bin-out/XFLParse.dll`,
.NET SDK 8.0.427 at `~/workspace/tools/dotnet/sdk/dotnet`.
(If it ever goes missing: `bash harness/build.sh` in that folder.)

```bash
~/workspace/tools/dotnet/sdk/dotnet ~/workspace/tools/FlashXFLParser/harness/bin-out/XFLParse.dll <file.fla>
```

- `SmileFriends.Charlie.fla` (82,390 B) → **exit 0**: scene 1920×1080,
  **18 library symbols, 33 layers, 73 frames**; master `Charlie` = 9 layers
  referencing the part symbols. This is the reliable way to *inventory* a
  puppet's hierarchy before flattening it for the renderer.
- `SmileFriends.PimRigUpdate.fla` (296,483 B) → **exit 0**: scene + master
  `Pim` (5 layers → Pim Head / Front Arm / Body / Legs / Back Hand) parsed,
  **but its TOTALS under-count**: it reported "1 library symbols" although
  the extracted `DOMDocument.xml` lists 17 `<Include>`s (subfolder
  `PimAssets/…` symbols weren't counted) [log: `test-renders/xflparse-pim.log`].
  Trust the extracted XML for Pim-style subfolder libraries.
- `tools/flash-work/frankie/pds3hx.fla` → **exit 2**, explicit
  `LEGACY-BINARY-FLA: … pre-CS5 OLE/MFC-serialization format, not an XFL
  zip` [log: `test-renders/xflparse-frankie.log`]. Legacy `.fla`s are out
  of scope for both the parser and the renderer.
- XFLParse is **inventory only**: it reports symbols/layers/frames/refs.
  It renders nothing, and its fps field prints blank for these files.

---

## 7. Authoring checklist for the parent lane

To author a puppet **this renderer can actually draw**:

1. One folder per XFL (copy `xfl-skeleton/`), one file per part under
   `LIBRARY/`, each a `DOMSymbolItem` with a single `<timeline>`.
2. Every part = `<DOMShape>` geometry only: `SolidColor` fills,
   `SolidStroke` strokes, geometry in the `edges` attribute
   (`!`/`|`/`[`/`]`), coordinates in twips.
3. One `<DOMShape>` per frame, or frame-wide-unique style indices.
4. Clockwise loops → `fillStyle1` (copy the skeleton rectangle pattern).
5. Substitution sets (mouths, eyes, brows, hands): one symbol, one
   keyframe per variant, contiguous indices starting at 0; select with
   `--frames N`.
6. Poses: bake each pose into its own flattened leaf symbol (transform the
   twip coordinates). Do **not** author `DOMSymbolInstance` hierarchies,
   matrices, masks, bitmaps, gradients, text or tweens expecting them to
   survive — they will silently vanish or, for masks, draw as solid art.
7. Assembly & motion happen downstream of the renderer: per-part PNG
   sequences → `recanvas.py` → PIL/ffmpeg compositing at the bbox offsets.

## Test evidence index (`test-renders/`)

| Test | Proves |
|---|---|
| `t1-charlie-front-arm/`, `t5-render-local/`, `p-render-all/`, `p-fallback/` | Leaf symbols render via all three entry points + fallback; per-frame canvas sizes differ |
| `t2-charlie-mouth/`, `t2b-mouth-all/` | `--frames` swap-frame selection; 25 mouth keyframes → 23 distinct drawings |
| `t3-charlie-master/` | Master symbol renders only its 2 direct shapes; mask layer draws as solid art; instances ignored |
| `t4-scene/`, `t4b-scene/`, `s4-skeleton-scene/` | Scene/`DOMDocument.xml`: CLI crashes, wrapper returns 0 |
| `s1-skeleton-twoframe/` | Skeleton graphic symbol renders exactly as authored (frame 1 image inspected) |
| `s2-skeleton-bitmap/`, `s3-posed-parent/` (+ `s2b`/`s3b`) | Bitmap-instance and posed-instance symbols render nothing |
| `p-gradient/`, `p-alpha/`, `p-shapematrix/`, `p-collide/` (+ `probes.log`) | Gradient = no fill; alpha ignored; shape matrix ignored; fill-index collision recolours |
| `v1-frontarm-raw/`, `v1-frontarm.log`, `v1-frontarm-seq/`, `v1-frontarm-12fps.mp4` | Full video path: batch render → re-canvas → ffprobe-verified MP4 |
| `xflparse-pim.log`, `xflparse-frankie.log` | XFLParse: modern Pim parses (totals under-count subfolder symbols); legacy Frankie rejected, exit 2 |
| `skeleton-tests.log` | Console log of the skeleton test runs |
