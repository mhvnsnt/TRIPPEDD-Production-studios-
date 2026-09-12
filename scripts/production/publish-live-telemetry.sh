#!/usr/bin/env bash
set -euo pipefail

# Durable live telemetry channel for production runs.
# GitHub Actions log blobs are not a reliable live API: they may be unavailable
# while a job is running. This publisher mirrors measured progress to a stable
# GitHub Issue comment and can additionally emit metrics to OSS observability
# backends when configured.

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <progress-file>" >&2
  exit 2
fi

progress_file="$1"
repo="${GITHUB_REPOSITORY:-}"
issue_number="${TRIPPEDD_TELEMETRY_ISSUE_NUMBER:-16}"
token="${GITHUB_TOKEN:-}"
marker='<!-- trippedd-live-telemetry -->'
interval="${TRIPPEDD_TELEMETRY_PUBLISH_INTERVAL_SECONDS:-5}"
parent_pid="${TRIPPEDD_TELEMETRY_PARENT_PID:-}"

# If a parent PID is supplied, remain alive for the entire production command.
# This fixes the previous one-shot publisher, which could publish one snapshot
# and then leave the remainder of the build invisible.
while true; do
  if [ -n "$parent_pid" ] && ! kill -0 "$parent_pid" 2>/dev/null; then
    break
  fi

  if [ ! -s "$progress_file" ] || ! command -v jq >/dev/null 2>&1; then
    sleep "$interval"
    continue
  fi

  snapshot=$(jq -c . "$progress_file" 2>/dev/null || true)
  if [ -z "$snapshot" ]; then
    sleep "$interval"
    continue
  fi

  markdown=$(jq -r --arg marker "$marker" '
    def bar($p):
      (($p // 0) | floor) as $n |
      ((($n / 5) | floor)) as $filled |
      (20 - $filled) as $empty |
      ("█" * $filled) + ("░" * $empty);
    ($marker + "\n" +
    "# TRIPPEDD Live Production Telemetry\n\n" +
    "**Run:** `" + ((.runId // "unknown")|tostring) + "`  \\n" +
    "**Overall:** " + ((.overallPercent // "UNKNOWN")|tostring) + "% " + bar(.overallPercent) + "\n\n" +
    "| Stage | Status | Progress | Work | Elapsed | Rate | ETA | Current operation | Heartbeat |\n" +
    "|---|---|---:|---:|---:|---:|---:|---|---|\n" +
    ([.stages[]? |
      "| " + (.label|tostring) + " | " + (.status|tostring) + " | " + ((.percent // "UNKNOWN")|tostring) + "% | " + ((.completed // "UNKNOWN")|tostring) + "/" + ((.total // "UNKNOWN")|tostring) + " | " + ((.elapsedMs // 0)/1000|floor|tostring) + "s | " + ((.ratePerSecond // "UNKNOWN")|tostring) + "/s | " + ((.etaLabel // "UNKNOWN")|tostring) + " | " + ((.message // "")|gsub("\\|";"/")) + " | " + ((.heartbeatAt // "UNKNOWN")|tostring) + " |"
    ] | join("\n")) + "\n\n<details><summary>Machine-readable snapshot</summary>\n\n```json\n" + ($snapshot) + "\n```\n</details>"
    )' --arg snapshot "$snapshot" "$progress_file" 2>/dev/null || true)

  # GitHub Issue is the durable, immediately retrievable fallback channel.
  if [ -n "$repo" ] && [ -n "$token" ] && command -v curl >/dev/null 2>&1; then
    api="https://api.github.com/repos/${repo}/issues/${issue_number}/comments"
    headers=(-H "Authorization: Bearer ${token}" -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' -H 'Content-Type: application/json')
    comments=$(curl -fsS "${headers[@]}" "$api?per_page=100" 2>/dev/null || true)
    comment_id=$(printf '%s' "$comments" | jq -r --arg marker "$marker" '.[] | select(.body | contains($marker)) | .id' | head -n1)
    payload=$(jq -n --arg body "$markdown" '{body:$body}')
    if [ -n "$comment_id" ]; then
      curl -fsS -X PATCH "${headers[@]}" "https://api.github.com/repos/${repo}/issues/comments/${comment_id}" -d "$payload" >/dev/null 2>&1 || true
    else
      curl -fsS -X POST "${headers[@]}" "$api" -d "$payload" >/dev/null 2>&1 || true
    fi
  fi

  # Optional Prometheus Pushgateway sink. Prometheus documents Pushgateway as
  # appropriate for short-lived/batch jobs; this is opt-in and never replaces
  # the canonical production ledger.
  if [ -n "${TRIPPEDD_PUSHGATEWAY_URL:-}" ] && command -v curl >/dev/null 2>&1; then
    run_id=$(jq -r '.runId // "unknown"' "$progress_file")
    overall=$(jq -r '.overallPercent // 0' "$progress_file")
    printf 'trippedd_production_overall_percent %s\n' "$overall" | \
      curl --fail --silent --show-error --data-binary @- "${TRIPPEDD_PUSHGATEWAY_URL%/}/metrics/job/trippedd_ep01/run/${run_id}" >/dev/null 2>&1 || true
  fi

  sleep "$interval"
done
