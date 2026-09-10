#!/usr/bin/env bash
set -euo pipefail

# Production law: a process is not considered actively running unless its
# measured progress ledger is observable and heartbeating. Percentages, rates
# and ETAs are derived from observed work; missing telemetry is UNKNOWN, not
# healthy RUNNING. This prevents silent multi-hour black boxes.

if [ "$#" -lt 3 ] || [ "$1" != "--progress-file" ]; then
  echo "usage: $0 --progress-file <path> -- <command> [args...]" >&2
  exit 2
fi
progress_file="$2"
shift 2
[ "${1:-}" = "--" ] || { echo "missing -- separator" >&2; exit 2; }
shift

stall_seconds="${TRIPPEDD_PROGRESS_STALL_SECONDS:-180}"
telemetry_grace_seconds="${TRIPPEDD_PROGRESS_TELEMETRY_GRACE_SECONDS:-60}"
mkdir -p "$(dirname "$progress_file")"
"$@" &
pid=$!
started_at=$(date +%s)

cleanup() {
  if kill -0 "$pid" 2>/dev/null; then kill "$pid" 2>/dev/null || true; fi
}
trap cleanup INT TERM

last=""
stalled=0
while kill -0 "$pid" 2>/dev/null; do
  now=$(date +%s)
  telemetry_age=$((now-started_at))
  if [ ! -s "$progress_file" ] || ! command -v jq >/dev/null 2>&1; then
    echo "PRODUCTION_PROGRESS status=UNKNOWN reason=waiting-for-measured-ledger elapsed=${telemetry_age}s grace=${telemetry_grace_seconds}s"
    if [ "$telemetry_age" -ge "$telemetry_grace_seconds" ]; then
      echo "PRODUCTION_STALLED reason=no-observable-production-telemetry age=${telemetry_age}s threshold=${telemetry_grace_seconds}s" >&2
      stalled=1
      kill "$pid" 2>/dev/null || true
      break
    fi
    sleep 5
    continue
  fi

  snapshot=$(jq -r '
    [.stages[] | select(.status == "RUNNING")] as $running |
    ($running[0] // .stages[-1]) as $s |
    if $s == null then
      "PRODUCTION_PROGRESS status=UNKNOWN reason=no-stage-telemetry"
    else
      "PRODUCTION_PROGRESS stage=\($s.label) status=\($s.status) stage_percent=\($s.percent)% overall_percent=\(.overallPercent // "UNKNOWN")% work=\($s.completed)/\($s.total) overall_work=\(.overallCompleted // "UNKNOWN")/\(.overallTotal // "UNKNOWN") elapsed=\((($s.elapsedMs // 0)/1000)|floor)s rate=\(($s.ratePerSecond // 0)|round)/s eta=\($s.etaLabel // "UNKNOWN") heartbeat=\($s.heartbeatAt // "unknown") message=\($s.message // "")"
    end' "$progress_file" 2>/dev/null || true)

  heartbeat=$(jq -r '[.stages[] | select(.status == "RUNNING") | .heartbeatAt // empty] | .[0] // empty' "$progress_file" 2>/dev/null || true)
  heartbeat_age=""
  if [ -n "$heartbeat" ]; then
    heartbeat_epoch=$(date -d "$heartbeat" +%s 2>/dev/null || true)
    if [ -n "$heartbeat_epoch" ]; then heartbeat_age=$((now-heartbeat_epoch)); fi
  fi

  if [ -z "$heartbeat_age" ] || [ "$heartbeat_age" -ge "$stall_seconds" ]; then
    echo "PRODUCTION_STALLED reason=no-fresh-heartbeat age=${heartbeat_age:-UNKNOWN}s threshold=${stall_seconds}s" >&2
    stalled=1
    kill "$pid" 2>/dev/null || true
    break
  fi

  if [ "$snapshot" != "$last" ]; then
    printf '%s\n' "$snapshot"
    if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
      printf '### TRIPPEDD live production telemetry\n\n`%s`\n\n' "$snapshot" > "$GITHUB_STEP_SUMMARY"
    fi
    last="$snapshot"
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
  jq -r '"PRODUCTION_FINAL overall_percent=\(.overallPercent // "UNKNOWN")% overall_work=\(.overallCompleted // "UNKNOWN")/\(.overallTotal // "UNKNOWN")" , (.stages[] | "PRODUCTION_FINAL stage=\(.label) status=\(.status) percent=\(.percent)% work=\(.completed)/\(.total) elapsed=\((.elapsedMs // 0)/1000|floor)s rate=\((.ratePerSecond // 0)|round)/s eta=\(.etaLabel // "UNKNOWN")")' "$progress_file" 2>/dev/null || true
fi
exit "$code"
