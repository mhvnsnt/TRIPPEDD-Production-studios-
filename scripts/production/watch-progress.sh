#!/usr/bin/env bash
set -euo pipefail

# Run a production command while continuously streaming the same measured
# progress ledger used by the studio UI. This is intentionally telemetry-only:
# percentages and ETAs come from observed completed work, never a timer guess.

if [ "$#" -lt 3 ] || [ "$1" != "--progress-file" ]; then
  echo "usage: $0 --progress-file <path> -- <command> [args...]" >&2
  exit 2
fi
progress_file="$2"
shift 2
[ "${1:-}" = "--" ] || { echo "missing -- separator" >&2; exit 2; }
shift

mkdir -p "$(dirname "$progress_file")"
"$@" &
pid=$!

cleanup() {
  if kill -0 "$pid" 2>/dev/null; then kill "$pid" 2>/dev/null || true; fi
}
trap cleanup INT TERM

last=""
while kill -0 "$pid" 2>/dev/null; do
  if [ -s "$progress_file" ] && command -v jq >/dev/null 2>&1; then
    snapshot=$(jq -r '
      [.stages[] | select(.status == "RUNNING")] as $running |
      ($running[0] // .stages[-1]) as $s |
      if $s == null then
        "PRODUCTION_PROGRESS status=initializing"
      else
        "PRODUCTION_PROGRESS stage=\($s.label) status=\($s.status) percent=\($s.percent)% work=\($s.completed)/\($s.total) elapsed=\((($s.elapsedMs // 0)/1000)|floor)s rate=\(($s.ratePerSecond // 0)|round)/s eta=\($s.etaLabel // "calculating…") message=\($s.message // "")"
      end' "$progress_file" 2>/dev/null || true)
    if [ "$snapshot" != "$last" ]; then
      printf '%s\n' "$snapshot"
      last="$snapshot"
    fi
  else
    echo "PRODUCTION_PROGRESS status=initializing (waiting for measured ledger)"
  fi
  sleep 5
done

wait "$pid"
code=$?
if [ -s "$progress_file" ] && command -v jq >/dev/null 2>&1; then
  jq -r '.stages[] | "PRODUCTION_FINAL stage=\(.label) status=\(.status) percent=\(.percent)% work=\(.completed)/\(.total) elapsed=\((.elapsedMs // 0)/1000|floor)s rate=\((.ratePerSecond // 0)|round)/s eta=\(.etaLabel // "n/a")"' "$progress_file" 2>/dev/null || true
fi
exit "$code"
