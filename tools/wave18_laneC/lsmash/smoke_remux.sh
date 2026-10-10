#!/bin/bash
# L-SMASH smoke test: MP4 remux via the ISC-licensed l-smash CLI tools.
# Builds (already built in src/lsmash-src) -> remuxes a captioned MP4 ->
# verifies A/V survival and uses boxdumper to inspect the tx3g caption track.
set -e
LANCEC="$(cd "$(dirname "$0")/.." && pwd)"
LS="$LANCEC/src/lsmash-src"
OUT="$LANCEC/proofs/wave18_lsmash"
mkdir -p "$OUT"
export LD_LIBRARY_PATH="$LS"

# 1. source: 3s testsrc + 440Hz tone + 2 SRT cues muxed as tx3g
ffmpeg -v error -f lavfi -i "testsrc2=duration=3:size=320x240:rate=24" \
  -f lavfi -i "sine=frequency=440:duration=3" \
  -i "$OUT/../fixtures/caption.srt" \
  -c:v libx264 -preset ultrafast -c:a aac -c:s mov_text -shortest \
  -y "$OUT/src_captioned.mp4"

# 2. remux through l-smash
"$LS/cli/remuxer" -i "$OUT/src_captioned.mp4" -o "$OUT/remuxed.mp4" 2>&1 | tail -1

# 3. box structure dumps (packaging visibility)
"$LS/cli/boxdumper" --box "$OUT/src_captioned.mp4" > "$OUT/box_src.txt" 2>&1
"$LS/cli/boxdumper" --box "$OUT/remuxed.mp4" > "$OUT/box_remuxed.txt" 2>&1

# 4. stream inventory before/after
{
  echo "== source =="
  ffprobe -v error -show_entries stream=index,codec_name,codec_type "$OUT/src_captioned.mp4"
  echo "== remuxed =="
  ffprobe -v error -show_entries stream=index,codec_name,codec_type "$OUT/remuxed.mp4"
} > "$OUT/streams.txt" 2>&1

echo "L-SMASH smoke done -> $OUT"
