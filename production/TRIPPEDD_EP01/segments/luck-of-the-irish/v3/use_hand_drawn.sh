#!/bin/bash
# use_hand_drawn.sh — drop a hand-drawn keyframe into the LOTI v3 pipeline.
#
# Usage:
#   ./use_hand_drawn.sh <beat> [--photo [--corners "x1,y1,x2,y2,x3,y3,x4,y4"]] <input>
#
# Beats: s1 s2 s3 s4 s5 freeze
#   s1..s5  -> transformation keyframes (EbSynth-propagated)
#   freeze  -> 100% mascot reveal hero frame (2s hold clip)
#
# What it does:
#   1. Backs up the AI keyframe to hand-drawn/ai-backup/ (never destroyed).
#   2. Processes the input (photo de-skew/crop if --photo; resize to working size).
#   3. Swaps the keyframe (or rebuilds comp/mascot_reveal.mp4 for freeze).
#   4. Re-runs only the affected EbSynth segment(s).
#   5. Re-runs the full assembly (assemble_v3.py — step 9 uses the sequential
#      hits passes; safe end to end).
#
# Then: QC the beat by eye, re-upload, push. PR stays open until graded.
set -e
V3="$(cd "$(dirname "$0")" && pwd)"
KEYS="$V3/keys"
EBS="$V3/ebs"
BACKUP="$V3/hand-drawn/ai-backup"
WRAP="$HOME/workspace/video-fix-tools/ebsynth/run_ebsynth.py"

usage() { echo "usage: $0 <s1|s2|s3|s4|s5|freeze> [--photo [--corners \"x1,y1,x2,y2,x3,y3,x4,y4\"]] <input-png-or-jpg>"; exit 1; }

BEAT="${1:-}"; shift || usage
PHOTO=0; CORNERS=""
while [[ "${1:-}" == --* ]]; do
  case "$1" in
    --photo) PHOTO=1; shift;;
    --corners) CORNERS="$2"; shift 2;;
    *) usage;;
  esac
done
INPUT="${1:-}"; [[ -n "$INPUT" && -f "$INPUT" ]] || usage

case "$BEAT" in
  s1) KEYFILE="s1-eyes.png";      SEGS="segA segB"; WSIZE="640x360";;
  s2) KEYFILE="s2-ears.png";      SEGS="segB segC"; WSIZE="640x360";;
  s3) KEYFILE="s3-grin.png";      SEGS="segC segD"; WSIZE="640x360";;
  s4) KEYFILE="s4-tracksuit.png"; SEGS="segD segE"; WSIZE="640x360";;
  s5) KEYFILE="s5-jump80.png";    SEGS="segE";      WSIZE="640x360";;
  freeze) KEYFILE=""; SEGS=""; WSIZE="1920x1080";;
  *) usage;;
esac

mkdir -p "$BACKUP"

# ---- 1. backup the AI original (first backup wins) ----
if [[ "$BEAT" == "freeze" ]]; then
  [[ -f "$BACKUP/mascot_reveal.mp4" ]] || cp "$V3/comp/mascot_reveal.mp4" "$BACKUP/mascot_reveal.mp4"
  echo "backed up AI mascot_reveal.mp4"
else
  [[ -f "$BACKUP/$KEYFILE" ]] || cp "$KEYS/$KEYFILE" "$BACKUP/$KEYFILE"
  echo "backed up AI $KEYFILE"
fi

# ---- 2. process the input ----
PROCESSED="/tmp/hd-$BEAT.png"
if [[ $PHOTO -eq 1 && -n "$CORNERS" ]]; then
  # true perspective de-skew: corners are TL,TR,BR,BL clockwise from top-left
  IFS=',' read -r x1 y1 x2 y2 x3 y3 x4 y4 <<< "${CORNERS// /}"
  convert "$INPUT" -distort Perspective \
    "$x1,$y1 0,0  $x2,$y2 1920,0  $x3,$y3 1920,1080  $x4,$y4 0,1080" \
    -resize "${WSIZE}!" "$PROCESSED"
  echo "perspective-corrected photo -> $WSIZE"
else
  python3 - "$INPUT" "$PROCESSED" "$WSIZE" "$PHOTO" <<'EOF'
import sys
from PIL import Image
src, dst, wsize, photo = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == '1'
im = Image.open(src).convert('RGB')
w, h = im.size
if min(w, h) < 720:
    sys.exit(f"REFUSED: input {w}x{h} below 1280x720 minimum — too soft for the pipeline")
if max(w, h) < 1920:
    print(f"WARNING: input {w}x{h} below preferred 1920x1080 — proceeding")
if photo:
    # center-crop to 16:9 (shoot flat, drawing fills frame)
    target = 16/9
    if w/h > target: nw, nh = int(h*target), h
    else:            nw, nh = w, int(w/target)
    im = im.crop(((w-nw)//2, (h-nh)//2, (w+nw)//2, (h+nh)//2))
    print("center-cropped photo to 16:9")
tw, th = map(int, wsize.split('x'))
im.resize((tw, th), Image.LANCZOS).save(dst)
print(f"wrote {dst} ({tw}x{th})")
EOF
fi

# ---- 3. swap the keyframe / rebuild the reveal clip ----
if [[ "$BEAT" == "freeze" ]]; then
  ffmpeg -v error -y -loop 1 -framerate 30 -i "$PROCESSED" \
    -t 2.0 -c:v libx264 -pix_fmt yuv420p -crf 18 \
    "$V3/comp/mascot_reveal.mp4"
  echo "rebuilt comp/mascot_reveal.mp4 (2.0s hold of hand-drawn hero)"
else
  cp "$PROCESSED" "$KEYS/$KEYFILE"
  echo "swapped $KEYS/$KEYFILE"
fi

# ---- 4. re-run affected EbSynth segments only ----
run_seg() { # $1=seg $2=k1 $3=i1 $4=k2 $5=i2
  echo "[$(date +%H:%M:%S)] EbSynth $1 (~45s/frame, CPU-bound)"
  ( cd "$EBS" && python3 "$WRAP" --input "$1/input.mp4" \
      --keyframe "$2" --keyframe-index "$3" --keyframes "$4@$5" \
      --output "$1/styled.mp4" --fps 8 --scale 640:360 --keep-frames )
}
for s in $SEGS; do
  case "$s" in
    segA) run_seg segA ../keys/s0-clean.png 0     ../keys/s1-eyes.png 16;;
    segB) run_seg segB ../keys/s1-eyes.png 0     ../keys/s2-ears.png 15;;
    segC) run_seg segC ../keys/s2-ears.png 0     ../keys/s3-grin.png 15;;
    segD) run_seg segD ../keys/s3-grin.png 0     ../keys/s4-tracksuit.png 19;;
    segE) run_seg segE ../keys/s4-tracksuit.png 0 ../keys/s5-jump80.png 15;;
  esac
done

# ---- 5. full assembly (sequential hits passes — no SIGKILL risk) ----
echo "rebuilding final assembly..."
python3 "$V3/assemble_v3.py"

echo
echo "DONE. Next: QC the $BEAT beat by eye, re-upload via remote-storage,"
echo "commit, push. Revert any beat: cp hand-drawn/ai-backup/<file> keys/<file>"
