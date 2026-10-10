#!/usr/bin/env bash
# Wave 59 Lane C runner — env hygiene for the VAD refinement wire script.
#   * TMPDIR lane-local (the /tmp tmpfs is 512 MB)
#   * strip IPv6 literals (::1, [::1]) from no_proxy/NO_PROXY (httpx crash)
#     — kept for the record; this torch-free script makes no HTTP calls.
#   * VENV_DIR: the lane venv (default: venv/ in the lane dir).
set -euo pipefail
LANE="$(cd "$(dirname "$0")" && pwd)"
export TMPDIR="$LANE/scratch"
mkdir -p "$TMPDIR"
for v in no_proxy NO_PROXY; do
  cur="${!v:-}"
  if [ -n "$cur" ]; then
    cleaned="$(echo "$cur" | tr ',' '\n' | grep -v '::' | tr '\n' ',' | sed 's/,$//')"
    export "$v=$cleaned"
  fi
done
VENV_DIR="${VENV_DIR:-$LANE/venv}"
exec "$VENV_DIR/bin/python" "$LANE/wire_vad_refinement.py" "$@"
