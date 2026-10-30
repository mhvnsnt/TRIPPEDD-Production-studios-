# MouthSwap Bridge — Rhubarb → timed mouth swaps (SPEC T-2)

Rhubarb Lip Sync outputs *when* each mouth shape happens; the shows' mouth
libraries hold the shapes as images. Turning the timings into exposed
mouth drawings used to be hand work on every dialogue scene. This bridge
automates that step — the exact step the owner's scene-by-scene method
waits on (he records a line, then lip sync happens in post).

## What it does

Input: a voice line (any audio ffmpeg reads) **or** an existing Rhubarb
output (`.json` / `.tsv`), plus a folder of mouth images named by Rhubarb
shape code. Output, in the `--out` folder:

| File | What it is |
|---|---|
| `mouthswap_timing.csv` | Timing/exposure sheet, one row per exposure: `frame, frame_end, phoneme, mouth_file, start_s, end_s`. This is the 2D-side sheet: ffmpeg compositing reads it directly, and for Tahoma2D it is the mouth level's cell plan (frame → drawing file). |
| `mouthswap_plan.json` | The same plan in machine form (fps, total frames, resolved mouth image paths, cues). |
| `mouthswap_blender.py` | Self-contained Blender script (plan embedded). Run it in Blender: it sets the scene fps/frame range and builds one image plane per mouth shape in a `MouthSwap` collection, visibility keyed frame-accurately with CONSTANT interpolation — exactly one mouth exposed on every frame. |
| `rhubarb.json` | (audio input only) a copy of the raw Rhubarb output the plan was built from. |

`blender_mouthswap.py` is the template the bridge embeds the plan into;
it can also be run directly against a plan:
`blender -b --python blender_mouthswap.py -- --plan mouthswap_plan.json`

## Usage

```bash
# from a voice recording (bridge converts + runs Rhubarb itself)
python3 mouthswap_bridge.py --audio voice-cipher-c1.mp3 \
    --mouth-dir /path/to/mouths --fps 30 --out ./lipsync_out

# from an existing Rhubarb output
python3 mouthswap_bridge.py --rhubarb cues.json \
    --mouth-dir /path/to/mouths --fps 60 --out ./lipsync_out

# then, in Blender (headless or GUI):
blender -b --python ./lipsync_out/mouthswap_blender.py
```

Options: `--dialog dialog.txt` (spoken text; improves Rhubarb),
`--recognizer phonetic` (faster, rougher), `--duration SECONDS`
(override the length inferred from a TSV input), `--rhubarb-bin PATH`.

## Mouth library naming

A file belongs to shape code `C` when its stem is the code itself
(`A.png`) or starts with the code followed by `_` or `-` (`B_open.png`).
An exact stem match wins over a prefixed one. Codes are the basic Rhubarb
set `A B C D E F G H X` (X = rest/silence). A shape used by the line but
missing from the folder falls back to the X image with a loud warning;
if X itself is missing the bridge stops and says so. Extended Rhubarb
shapes (G/X combinations etc.) are rejected loudly, not silently mapped.

## Frame convention

Frames are 1-based. Frame *f* covers `[(f-1)/fps, f/fps)` and exposes the
shape active at the frame's **start instant**. Cues are gap-filled with X
before framing, so every frame has exactly one shape; a cue shorter than
one frame that contains no frame start is absorbed by its neighbours
(standard exposure practice). CSV times are the frame-quantized times.

## Design notes / donor check

Per the repo's DONOR FIRST law, the existing donor was inspected first:
`~/workspace/tools/lipsync/rhubarb_to_visemes.py` already turns Rhubarb
output into a per-frame EDL — but mapped onto one Preston-Blair-named PNG
kit (`viseme-{stem}.png`) and with no Blender output. SPEC T-2 calls for
code-named mouth sets (the shows' mouth-only PNG libraries) and a keyed
Blender swap, so the bridge is a separate, small tool; it reuses Rhubarb's
documented CLI and output formats only. All code here is original.

Two environment-driven choices worth knowing:

* **Rhubarb's TSV is two-column** (`start, shape`; a shape holds until
  the next row, with a sentinel row at the audio duration). The loader
  handles that format plus three-column `start, end, shape` files.
* The audio path's temp workdir sits **next to `--out`**, not in the
  system temp dir — on the studio VM `/tmp` is a small tmpfs that fills.

## Tests

`tests/` holds the test kit used to verify this tool end to end:

* `make_test_mouths.py` — generates the sample A–H/X library in
  `tests/sample_mouths/` (simple PIL test art).
* `verify_timing.py` — independently re-derives the expected shape for
  every frame from raw Rhubarb JSON and compares the CSV (and optionally
  a Blender dump) frame-for-frame.
* `check_blender.py` — runs inside Blender after the build script and
  dumps the visible shape per frame.

Verified 2026-10-30 on the real sample line
`voice-delivery/voice-cipher-c1.mp3` (6.24 s, 36 Rhubarb cues, shapes
X/C/A/B/F/E): CSV **and** the built Blender rig match Rhubarb
frame-for-frame at **30 fps (188 frames)** and **60 fps (375 frames)**;
the TSV input path produces output identical to the JSON path; the
`--audio` path (bridge runs Rhubarb itself) passes the same check.
Blender 4.5.3 headless build: `MOUTHSWAP_OK planes=6 cues=36`.
