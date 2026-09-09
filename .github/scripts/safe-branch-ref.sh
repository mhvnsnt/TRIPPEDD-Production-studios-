#!/usr/bin/env bash
set -euo pipefail

# Safe branch-ref helper. Uses GitHub's Git database API through gh instead of
# relying on a higher-level branch wrapper that may race on create/update.
# Usage: safe-branch-ref.sh <source-branch> <target-branch> [force]

SOURCE_BRANCH="${1:?source branch required}"
TARGET_BRANCH="${2:?target branch required}"
FORCE="${3:-false}"
REPO="${GH_REPO:?GH_REPO must be set (owner/name)}"

SOURCE_SHA="$(gh api "repos/${REPO}/git/ref/heads/${SOURCE_BRANCH}" --jq '.object.sha')"

if gh api "repos/${REPO}/git/ref/heads/${TARGET_BRANCH}" >/dev/null 2>&1; then
  gh api --method PATCH "repos/${REPO}/git/refs/heads/${TARGET_BRANCH}" \
    -f "sha=${SOURCE_SHA}" \
    -F "force=${FORCE}" \
    >/dev/null
else
  gh api --method POST "repos/${REPO}/git/refs" \
    -f "ref=refs/heads/${TARGET_BRANCH}" \
    -f "sha=${SOURCE_SHA}" \
    >/dev/null
fi

printf 'Updated refs/heads/%s -> %s\n' "${TARGET_BRANCH}" "${SOURCE_SHA}"
