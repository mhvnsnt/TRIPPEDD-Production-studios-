#!/usr/bin/env bash
set -euo pipefail

# Run a production command while continuously streaming the measured production
# ledger. Percentages and ETAs come from observed work; this wrapper never
# invents progress. A missing/stale heartbeat is treated as UNKNOWN/STALLED,
# not healthy RUNNING, and terminates the child so bounded recovery can act.

if [ "$#" -lt 3 ] || [ "$1" != "--progress-file" ]; then
  echo "usage: $0 --progress-file <path> -- <command> [args...]" >&2
  exit 2
fi
progress_file="$2"
shift 2
[ "${1:-}" = "--" ] || { echo "missing -- separator" >&2; exit 2; }
shift

stall_seconds="${TRIPPEDD_PROGRESS_STALL_SECONDS:-180}"
mkdir -p "$(dirname "$progress_file")"
"$@" &
pid=$!

cleanup() {
  if kill -0 "$pid" 2>/dev/null; then kill "$pid" 2>/dev/null || true; fi
}
trap cleanup INT TERM

last=""
stalled=0
while kill -0 "$pid" 2>/dev/null; do
  if [ -s "$progress_file" ] && command -v jq >/dev/null 2>&1; then
    now=$(date +%s)
    snapshot=$(jq -r '
      [.stages[] | select(.status == "RUNNING")] as $running |
      ($running[0] // .stages[-1]) as $s |
      if $s == null then
        "PRODUCTION_PROGRESS status=UNKNOWN reason=no-stage-telemetry"
      else
        "PRODUCTION_PROGRESS stage=\($s.label) status=\($s.status) percent=\($s.percent)% work=\($s.completed)/\($s.total) elapsed=\((($s.elapsedMs // 0)/1000)|floor)s rate=\(($s.ratePerSecond // 0)|round)/s eta=\($s.etaLabel // "calculating…") heartbeat=\($s.heartbeatAt // "unknown") message=\($s.message // "")"
      end' "$progress_file" 2>/dev/null || true)

    heartbeat=$(jq -r '[.stages[] | select(.status == "RUNNING") | .heartbeatAt // empty] | .[0] // empty' "$progress_file" 2>/dev/null || true)
    heartbeat_age=""
    if [ -n "$heartbeat" ]; then
      heartbeat_epoch=$(date -d "$heartbeat" +%s 2>/dev/null || true)
      if [ -n "$heartbeat_epoch" ]; then heartbeat_age=$((now-heartbeat_epoch)); fi
    fi

    if [ -n "$heartbeat_age" ] && [ "$heartbeat_age" -ge "$stall_seconds" ]; then
      echo "PRODUCTION_STALLED stage-heartbeat-age=${heartbeat_age}s threshold=${stall_seconds}s; terminating child for bounded recovery" >&2
      stalled=1
      kill "$pid" 2>/dev/null || true
      break
    fi

    if [ "$snapshot" != "$last" ]; then
      printf '%s\n' "$snapshot"
      last="$snapshot"
    fi
  else
    echo "PRODUCTION_PROGRESS status=UNKNOWN reason=waiting-for-measured-ledger"
  fi
  sleep 5
done

if [ "$stalled" -eq 1 ]; then
  wait "$pid" 2>/dev/null || true
  echo "PRODUCTION_FINAL status=FAILED reason=telemetry-stalled"
  exit 75
fi

wait "$pid"
code=$?
if [ -s "$progress_file" ] && command -v jq >/dev/null 2>&1; then
  jq -r '.stages[] | "PRODUCTION_FINAL stage=\(.label) status=\(.status) percent=\(.percent)% work=\(.completed)/\(.total) elapsed=\((.elapsedMs // 0)/1000|floor)s rate=\((.ratePerSecond // 0)|round)/s eta=\(.etaLabel // "n/a")"' "$progress_file" 2>/dev/null || true
fi
exit "$code"
