#!/usr/bin/env bash
set -euo pipefail

# Durable live telemetry channel for production runs.
# GitHub Actions log blobs are not a reliable live API: they may be unavailable
# while a job is running. This publisher mirrors measured progress to a stable
# GitHub Issue comment, which is retrievable through the Issues API while the
# workflow is still running.

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <progress-file>" >&2
  exit 2
fi

progress_file="$1"
repo="${GITHUB_REPOSITORY:-}"
issue_number="${TRIPPEDD_TELEMETRY_ISSUE_NUMBER:-16}"
token="${GITHUB_TOKEN:-}"
marker='<!-- trippedd-live-telemetry -->'

[ -n "$repo" ] || exit 0
[ -n "$token" ] || exit 0
[ -s "$progress_file" ] || exit 0
command -v curl >/dev/null 2>&1 || exit 0
command -v jq >/dev/null 2>&1 || exit 0

api="https://api.github.com/repos/${repo}/issues/${issue_number}/comments"

snapshot=$(jq -c . "$progress_file" 2>/dev/null || true)
[ -n "$snapshot" ] || exit 0

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

[ -n "$markdown" ] || exit 0

headers=(-H "Authorization: Bearer ${token}" -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' -H 'Content-Type: application/json')

comments=$(curl -fsS "${headers[@]}" "$api?per_page=100" 2>/dev/null || true)
comment_id=$(printf '%s' "$comments" | jq -r --arg marker "$marker" '.[] | select(.body | contains($marker)) | .id' | head -n1)
payload=$(jq -n --arg body "$markdown" '{body:$body}')

if [ -n "$comment_id" ]; then
  curl -fsS -X PATCH "${headers[@]}" "https://api.github.com/repos/${repo}/issues/comments/${comment_id}" -d "$payload" >/dev/null 2>&1 || true
else
  curl -fsS -X POST "${headers[@]}" "$api" -d "$payload" >/dev/null 2>&1 || true
fi
