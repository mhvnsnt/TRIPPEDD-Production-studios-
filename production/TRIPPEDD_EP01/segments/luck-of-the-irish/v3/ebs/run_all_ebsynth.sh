#!/bin/bash
# V3 per-part EbSynth propagation. Sequential (CPU-bound); ~45s/frame at 640x360.
V3=~/workspace/trippedd-studio-loti-v2/production/TRIPPEDD_EP01/segments/luck-of-the-irish/v3
WRAP=~/workspace/video-fix-tools/ebsynth/run_ebsynth.py
cd "$V3/ebs" || exit 1
run() {
  local seg="$1" k1="$2" i1="$3" k2="$4" i2="$5"
  echo "[$(date +%H:%M:%S)] START $seg ($k1@$i1 -> $k2@$i2)"
  python3 "$WRAP" --input "$seg/input.mp4" --keyframe "$k1" --keyframe-index "$i1" \
    --keyframes "$k2@$i2" --output "$seg/styled.mp4" --fps 8 --scale 640:360 --keep-frames
  echo "[$(date +%H:%M:%S)] DONE $seg (exit $?)"
}
# segA: t22.9->t25.0, 17f (0..16): clean -> S1 eyes
run segA ../keys/s0-clean.png 0 ../keys/s1-eyes.png 16
# segB: t25.0->t27.0, 16f (0..15): S1 -> S2 ears
run segB ../keys/s1-eyes.png 0 ../keys/s2-ears.png 15
# segC: t27.0->t29.0, 16f (0..15): S2 -> S3 grin
run segC ../keys/s2-ears.png 0 ../keys/s3-grin.png 15
# segD: t29.0->t31.5, 20f (0..19): S3 -> S4 tracksuit
run segD ../keys/s3-grin.png 0 ../keys/s4-tracksuit.png 19
# segE: t31.5->t33.5, 16f (0..15): S4 -> S5 jump 80%
run segE ../keys/s4-tracksuit.png 0 ../keys/s5-jump80.png 15
echo "[$(date +%H:%M:%S)] ALL SEGMENTS DONE"
