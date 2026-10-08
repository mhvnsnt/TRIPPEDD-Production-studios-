# TRIPPEDD lipsync — Rhubarb Lip Sync pipeline (keyless, local)

Rhubarb Lip Sync 1.14.0 (MIT — per the bundled LICENSE.md; output mouth
cues belong to us outright).
Automatic lip-sync mouth cues from a WAV: outputs mouth shapes over time
for 2D/cartoon puppet rigs (Preston Blair mouth set: A B C D E F G H X).

## Layout

```
tools/lipsync/
  bin/rhubarb            # Linux binary (chmod +x)
  bin/res/               # required acoustic-model data (ships next to binary)
  lipsync_pipeline.sh    # one-command pipeline: WAV -> TSV -> timeline JSON -> verify
  rhubarb_to_timeline.py # TSV -> JSON converter + verifier (coverage/sanity/viseme set)
  BUILD.sh               # build + reproduce the proof end to end
  VISEME_REFERENCE.md    # Preston Blair A-H + X reference + phoneme->viseme guide
  proofs/                # smoke-test mouth-cue outputs
  proofs/lane-b/         # Lane B proof: Static EP02 L1 real timeline + PROOFS_LANE_B.md
  README.md PROOFS.md
```

## Pipeline usage (one command)

```bash
# full pipeline: rhubarb cues + verified timeline JSON
./lipsync_pipeline.sh proofs/lane-b/static_L1_standin_raw.wav proofs/lane-b
# outputs: <name>_cues.tsv, <name>_timeline.json (gapless 0 -> audio duration)
```

The verifier checks: (1) gapless full-duration coverage, (2) sane cue count
vs line length, (3) every viseme in the documented {A..H, X} set — prints
VERIFY: PASS/FAIL and the first 20 rows.

## Raw rhubarb usage

```bash
./bin/rhubarb --version
# TSV mouth cues (default):
./bin/rhubarb -f tsv -o cues.tsv line.wav
# JSON mouth cues:
./bin/rhubarb -f json -o cues.json line.wav
# recognize speech + export both:
./bin/rhubarb --exportFormat tsv,json -o cues line.wav
# extended mouth shapes:
./bin/rhubarb --extendedShapes GHX -f tsv -o cues.tsv line.wav
```

Input WAV requirements: mono or stereo, 16-bit; rhubarb resamples
internally. Best results on clean single-speaker VO.

TSV columns: `start<TAB>end<TAB>mouth-shape`. Map shapes to your
character's mouth sprites in the animation tool.

## Proof

`PROOFS.md` — version output, smoke-test command on a 3s WAV, artifact hashes.
`proofs/lane-b/PROOFS_LANE_B.md` — Lane B real proof: Static's approved EP02 L1
line (espeak-ng stand-in VO — documented) -> Rhubarb -> verified timeline JSON,
SHA-256s, machine-checked coverage/sanity/viseme-set results.
