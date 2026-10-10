#!/usr/bin/env bash
set -euo pipefail

# OWNER LAW: GitHub will reject a pushed range containing a >100 MB blob even if
# the current tree no longer references it. This removes oversized historical
# blobs while preserving the current 59 MB MARS_source.glb.
#
# Run from a fresh clone after confirming the working tree is clean:
#   bash tools/git/strip_oversize_history.sh
#   git push --force-with-lease origin main
#
# Requires git-filter-repo (open source):
#   python -m pip install git-filter-repo
#
# This intentionally strips ALL blobs over 100 MiB. The current MARS_source.glb
# is ~59 MB, so it remains. Review `git status` and `git log` before pushing.

LIMIT_MB=100

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "REFUSED: working tree/index is not clean" >&2
  exit 2
fi

if ! command -v git-filter-repo >/dev/null 2>&1; then
  echo "REFUSED: git-filter-repo is not installed" >&2
  echo "Install: python -m pip install git-filter-repo" >&2
  exit 3
fi

before=$(git rev-list --objects --all | git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize)' | awk '$2=="blob" && $3 > 104857600 {n++; mb+=$3/1048576} END {printf "%d oversized blobs, %.1f MiB\n", n+0, mb+0}')
echo "Before: $before"

git filter-repo --force --strip-blobs-bigger-than 100M

git reflog expire --expire=now --all
git gc --prune=now --aggressive

after=$(git rev-list --objects --all | git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize)' | awk '$2=="blob" && $3 > 104857600 {n++; mb+=$3/1048576} END {printf "%d oversized blobs, %.1f MiB\n", n+0, mb+0}')
echo "After:  $after"
if ! git rev-list --objects --all | git cat-file --batch-check='%(objectname) %(objecttype) %(objectsize)' | awk '$2=="blob" && $3 > 104857600 {found=1} END {exit found ? 1 : 0}'; then
  echo "PASS: no >100 MiB blobs remain in reachable history."
else
  echo "FAIL: an oversized reachable blob remains." >&2
  exit 4
fi

echo "Next: inspect the rewritten main, then push with: git push --force-with-lease origin main"
