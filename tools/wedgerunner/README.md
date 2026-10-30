# WedgeRunner — SPEC H-2 (PDG-style wedge / batch-variation driver)

Original implementation for the TRIPPEDD free-versions build-out
(`docs/BUILD-MAP-FREE-VERSIONS.md`, SPEC H-2). The Houdini TOPs/PDG
lesson: wedge a parameter, run every variant, collect previews, keep
the best. WedgeRunner is that loop for headless Blender.

It **extends the studio's existing headless driver pattern** — the
`blender -b [scene.blend] --python <script> -- <args>` invocation used
by the Cape Jones render-proof lanes (e.g.
`3d-assets/living-room/lighting/render_proof.py`, which sets render
settings inside `bpy` and renders per invocation) — rather than
inventing a new one. What's new is the batch layer around it: a wedge
file, one isolated process per variant, per-variant logs, a contact
sheet, and an honest summary.

## Files

| File | Runs where | Job |
|---|---|---|
| `wedgerunner.py` | system Python 3 (stdlib only; PIL for the PNG sheet if available) | host driver: reads the wedge, spawns one Blender process per variant, collects results, writes summary + contact sheet |
| `blender_driver.py` | inside Blender (`bpy`) | loads one variant, execs the scene script, applies params, renders one still, writes `driver_result.json` |
| `examples/example_scene.py` | inside Blender | example target scene script (cube + light + camera) |
| `examples/example_wedge.json` | — | 3-variant example wedge |
| `examples/test_wedge_with_broken.json` | — | test wedge: 3 good variants + 1 deliberately broken (`__fail__`) |
| `tests/TEST-LOG.md` | — | the real headless test run and its evidence |

## Usage

```bash
python3 wedgerunner.py \
  --wedge examples/example_wedge.json \
  --blender ~/workspace/tools/blender-4.5/blender-4.5.3-linux-x64/blender \
  [--out DIR] [--timeout 600] [--strict]
```

On this VM, run it the way every studio headless Blender job runs —
under Xvfb with `PYTHONPATH` scrubbed (the runner also scrubs
`PYTHONPATH` from each child process itself):

```bash
xvfb-run -a env -u PYTHONPATH python3 wedgerunner.py --wedge ... --blender ...
```

**Engine note (learned in the H-2 test run):** on this VM, Eevee
(`BLENDER_EEVEE_NEXT`) aborts headless — there is no `libEGL.so.1` /
GPU context for it. The studio's proven headless pattern is **Cycles
on CPU** (as in the Cape Jones `render_proof.py` donor), so the
shipped example/test wedges use `CYCLES` with `cycles.device: CPU`
and low samples. Wedge an Eevee batch only on a machine with a
working EGL/GPU stack.

Outputs land in `<out>/` (default: the wedge's `output_dir`, relative
to the wedge file):

```
<out>/
  summary.json          variant -> status / output / sha256 / log / error
  contact_sheet.png     tiled preview of the successful renders (PIL)
  index.html            preview page (thumbnails + params + status)
  <variant>/
    render.png          the variant's render (only when it succeeded)
    blender.log         that variant's full Blender stdout/stderr
    variant.json        the exact variant record the driver received
    result.json         the host-side result record for this variant
    driver_result.json  the in-Blender result record (on success)
```

## Wedge JSON format

```json
{
  "name": "my-batch",
  "blend_file": "scene.blend",        // optional; null = Blender startup scene
  "scene_script": "my_scene.py",      // optional; exec'd inside Blender first
  "output_dir": "out",                // optional default output dir
  "variants": [
    {"name": "unique_name", "params": { "...": "..." }}
  ]
}
```

`blend_file` / `scene_script` are resolved relative to the wedge file.
Variant names must be unique — they become directory names.

## Parameter injection mechanism

Two layers, both documented here and in `blender_driver.py`:

1. **Scene-script params (escape hatch).** The scene script is exec'd
   with globals `bpy`, `VARIANT`, and `PARAMS` (the variant's full
   params dict). Any param the script wants to consume itself — e.g.
   the example's `cube_color` — it simply reads from `PARAMS`.
   A scene script may instead open `blend_file` scenes and just add
   setup; both routes combine freely.

2. **Dotted params (generic driver application).** After the scene
   script runs, the driver applies every dotted key:

   | Key | Applied to |
   |---|---|
   | `render.engine` | `scene.render.engine` (e.g. `BLENDER_EEVEE_NEXT`, `CYCLES`) |
   | `render.samples` | `scene.cycles.samples` **and** `scene.eevee.taa_render_samples` (whichever exist) |
   | `render.resolution` | `[x, y]` → `scene.render.resolution_x/y` |
   | `render.resolution_x` / `render.resolution_y` / `render.film_transparent` / `render.<attr>` | `scene.render.<attr>` |
   | `cycles.<attr>` / `eevee.<attr>` | `scene.cycles.<attr>` / `scene.eevee.<attr>` (sim settings live here, e.g. `cycles.device`, Mantaflow attrs via `scene.…`) |
   | `world.<attr>` | `scene.world.<attr>` |
   | `objects.<Name>.<attr>[.<sub>…]` | `bpy.data.objects[<Name>]`, e.g. `objects.Cube.scale`, `objects.Light.data.energy` |
   | `scene.<path…>` | attribute path under `bpy.context.scene` (covers sim/domain objects reachable from the scene) |
   | `__fail__: true` | raises immediately — the deliberate-failure test hook |

   List values become tuples (Blender vector properties). A param that
   targets a missing object/attribute fails **that variant only**, with
   the reason in its log and `summary.json`.

Parameter sets are arbitrary: sim settings, object properties, and
render samples/resolution/engine are all just params — that is the
whole point of a wedge.

## Resilience contract

- Each variant is a **separate Blender process** with a per-variant
  timeout (`--timeout`, default 600 s).
- Crash, non-zero exit, timeout, missing output, or a bad param →
  that variant is recorded `failed`/`timeout` with its exit code and
  error; the batch continues with the next variant.
- Statuses are never upgraded by hope: `ok` requires exit code 0 **and**
  a non-empty render file on disk (whose SHA-256 is recorded).
- Exit code: `0` = batch completed (read `summary.json` for truth),
  `1` with `--strict` if any variant failed, `2` = wedge/config error
  (nothing ran).

## Test

See `tests/TEST-LOG.md` — a real run of
`examples/test_wedge_with_broken.json` under Blender 4.5.3 headless:
3 variants rendered, the deliberately broken variant recorded as
failed, the variants after it still completed, contact sheet and
summary verified against the files on disk.
