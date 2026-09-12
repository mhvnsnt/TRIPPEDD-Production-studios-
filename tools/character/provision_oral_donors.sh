#!/usr/bin/env bash
set -euo pipefail

# Binary donors stay in worker cache, never in git.
ROOT="${TRIPPEDD_DONOR_CACHE:-${HOME}/.cache/trippedd/god-molecule/oral-donors}"
mkdir -p "$ROOT"

FACE_CAP_URL="https://raw.githubusercontent.com/Saganaki22/GNM-Studio/main/public/models/facecap.glb"
FACE_CAP_SHA256="6BFCE6D0FCBB5839F5102B79733007859FEF7C5DF6D9EB49E2264542810B5F64"
FACE_CAP="$ROOT/facecap.glb"
GNM_URL="https://raw.githubusercontent.com/google/GNM/main/gnm/shape/data/versions/v3_0/gnm_head.npz"
GNM="$ROOT/gnm_head.npz"
GNM_EXPR_URL="https://raw.githubusercontent.com/google/GNM/main/gnm/shape/data/semantic_sampler/expression_decoder_model.h5"
GNM_EXPR="$ROOT/expression_decoder_model.h5"

fetch() {
  local url="$1" dst="$2"
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 3 --connect-timeout 20 -o "$dst.tmp" "$url"
  elif command -v wget >/dev/null 2>&1; then
    wget -q --tries=3 -O "$dst.tmp" "$url"
  else
    echo "ORAL_DONOR: FAIL — neither curl nor wget is available" >&2
    exit 2
  fi
  mv "$dst.tmp" "$dst"
}

if [[ ! -s "$FACE_CAP" ]]; then fetch "$FACE_CAP_URL" "$FACE_CAP"; fi
actual="$(sha256sum "$FACE_CAP" | awk '{print toupper($1)}')"
[[ "$actual" == "$FACE_CAP_SHA256" ]] || {
  echo "ORAL_DONOR: FAIL — FaceCap SHA256 mismatch: $actual" >&2
  exit 3
}

if [[ ! -s "$GNM" ]]; then fetch "$GNM_URL" "$GNM"; fi
if [[ ! -s "$GNM_EXPR" ]]; then fetch "$GNM_EXPR_URL" "$GNM_EXPR"; fi
gnm_sha="$(sha256sum "$GNM" | awk '{print toupper($1)}')"
expr_sha="$(sha256sum "$GNM_EXPR" | awk '{print toupper($1)}')"

cat > "$ROOT/manifest.json" <<JSON
{
  "schema": "god-molecule.oral-donor-cache.v2",
  "facecap": {
    "source": "Saganaki22/GNM-Studio",
    "path": "public/models/facecap.glb",
    "sha256": "$actual",
    "license": "MIT",
    "purpose": "oral anatomy / 52-target expression donor; never replaces MARS_CANONICAL"
  },
  "gnm": {
    "source": "google/GNM",
    "path": "gnm/shape/data/versions/v3_0/gnm_head.npz",
    "sha256": "$gnm_sha",
    "license": "Apache-2.0",
    "purpose": "teeth/tongue/mouth-sock anatomy and learned facial expression donor; never replaces MARS_CANONICAL"
  },
  "gnm_expression_decoder": {
    "source": "google/GNM",
    "path": "gnm/shape/data/semantic_sampler/expression_decoder_model.h5",
    "sha256": "$expr_sha",
    "license": "Apache-2.0",
    "purpose": "canonical mouth-open expression basis"
  }
}
JSON

echo "ORAL_DONOR_PROVISION: VERIFIED"
echo "CACHE=$ROOT"
