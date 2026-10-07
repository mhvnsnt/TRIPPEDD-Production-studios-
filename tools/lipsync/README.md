# TRIPPEDD lipsync — Rhubarb Lip Sync (binary, keyless, local)

Rhubarb Lip Sync 1.14.0 (MIT — per the bundled LICENSE.md; output mouth
cues belong to us outright).
Automatic lip-sync mouth cues from a WAV: outputs mouth shapes over time
for 2D/cartoon puppet rigs (Preston Blair mouth set: A B C D E F G H X).

## Layout

```
tools/lipsync/
  bin/rhubarb            # Linux binary (chmod +x)
  bin/res/               # required acoustic-model data (ships next to binary)
  proofs/                # smoke-test mouth-cue outputs
  README.md PROOFS.md
```

## Usage

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
