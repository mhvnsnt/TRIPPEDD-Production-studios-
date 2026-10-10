# hvl2wav — HivelyTracker AHX/HVL → WAV renderer

Wired 2026-10-07 (Wave 19, Lane C).

## What it is
The offline command-line module renderer from
[pete-gordon/hivelytracker](https://github.com/pete-gordon/hivelytracker)
(BSD-3-Clause). HivelyTracker is the GUI AHX tracker by Xeron/IRIS; `hvl2wav`
is its standalone, GUI-free rendering path: it takes an AHX or HVL chiptune
module and writes a 16-bit WAV — no SDL, no Qt, no GUI needed. This is the
part Wave 18 judged "no CLI"; the `hvl2wav` sub-tool *is* the CLI.

## License
BSD-3-Clause (see upstream LICENSE). Safe to wire.

## Files
- `hvl2wav` — prebuilt Linux x86_64 binary (gcc -O3, 163 KB). Rebuildable any time.
- `src/` — upstream `hvl2wav` directory verbatim
  (`hvl2wav.c`, `replay.c`, `replay.h`, `types.h`, `makefile`, `hvl2wav.1`).
- `demo/illuminated.hvl` — 1.5 KB demo module from the upstream `Songs/` dir.

## Usage
```sh
# rebuild from source (gcc only)
./BUILD.sh
# render a module to WAV (defaults: 44100 Hz stereo)
./hvl2wav -omy-song.wav my-song.hvl
# limit length, change sample rate
./hvl2wav -oout.wav -t1:30 -f48000 my-song.ahx
```

## Why this matters for TRIPPEDD
Chiptune/AHX-style modules are the cheapest way to produce loopable game
music: a full song is ~1–20 KB of data (vs MBs for recorded audio) and
renders deterministically to WAV for the sfx/music lane. Pairs with the
existing `dumb_mod2wav` wiring (tools/wave18_laneC) for MOD/S3M/XM/IT.
