#!/usr/bin/env bash
set -euo pipefail

# Full-source bootstrap for the TRIPPEDD production runtime.
# This deliberately clones source projects into a cache/workspace rather than
# pretending that a manifest entry is an installed dependency.
# Large model weights belong in model cache / Git LFS / release artifacts.

ROOT="${TRIPPEDD_OSS_ROOT:-third_party/opensource}"
mkdir -p "$ROOT"

clone_or_update() {
  local name="$1" url="$2"
  local dest="$ROOT/$name"
  if [[ -d "$dest/.git" ]]; then
    git -C "$dest" fetch --tags --prune
    git -C "$dest" pull --ff-only || true
  else
    git clone --filter=blob:none "$url" "$dest"
  fi
}

clone_or_update rclone https://github.com/rclone/rclone.git
clone_or_update OpenCue https://github.com/AcademySoftwareFoundation/OpenCue.git
clone_or_update ayon-core https://github.com/ynput/ayon-core.git
clone_or_update pyblish-base https://github.com/pyblish/pyblish-base.git
clone_or_update OpenUSD https://github.com/PixarAnimationStudios/OpenUSD.git
clone_or_update MaterialX https://github.com/AcademySoftwareFoundation/MaterialX.git
clone_or_update gstreamer https://gitlab.freedesktop.org/gstreamer/gstreamer.git
clone_or_update vapoursynth https://github.com/vapoursynth/vapoursynth.git
clone_or_update mlt https://github.com/mltframework/mlt.git
clone_or_update vmaf https://github.com/Netflix/vmaf.git
clone_or_update MediaConch https://github.com/MediaArea/MediaConch.git
clone_or_update qctools https://github.com/bavc/qctools.git
clone_or_update kitsu https://github.com/cgwire/kitsu.git
clone_or_update opentelemetry-collector https://github.com/open-telemetry/opentelemetry-collector.git
clone_or_update prometheus https://github.com/prometheus/prometheus.git
clone_or_update grafana https://github.com/grafana/grafana.git
clone_or_update ardour https://github.com/Ardour/ardour.git
clone_or_update krita https://github.com/KDE/krita.git
clone_or_update OpenFaceFX https://github.com/Emilianavt/OpenFaceFX.git
clone_or_update PantoMatrix https://github.com/PantoMatrix/PantoMatrix.git
clone_or_update BlendCap https://github.com/jasperges/BlendCap.git
clone_or_update moface https://github.com/cgtinker/moface.git
clone_or_update Character-Animation-Pipeline https://github.com/TencentARC/Character-Animation-Pipeline.git
clone_or_update LongVideoSparseAttention https://github.com/svg-project/LongVideoSparseAttention.git

printf '%s\n' "OSS source bootstrap complete: $ROOT"
