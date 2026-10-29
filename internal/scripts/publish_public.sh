#!/usr/bin/env bash
# Local publish to the public repo (no GitHub Actions; no private-repo minutes).
#
# Usage (from anywhere):
#   ./internal/scripts/publish_public.sh
#
# Requirements: git-filter-repo installed; push access to the public repo (SSH).
# Override target: PUBLIC_URL=git@github.com:OWNER/REPO.git ./internal/scripts/publish_public.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PUBLIC_URL="${PUBLIC_URL:-git@github.com:parkwoo/wawoo-skills.git}"
ALLOWLIST="$ROOT/.publish-allowlist"

command -v git-filter-repo >/dev/null || { echo "git-filter-repo not installed" >&2; exit 1; }
test -s "$ALLOWLIST" || { echo "missing .publish-allowlist" >&2; exit 1; }
if grep -qE '^(internal/|\.publish-allowlist)' "$ALLOWLIST"; then
  echo "refusing: allowlist contains an internal path" >&2; exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --quiet --no-local "$ROOT" "$TMP/out"
cd "$TMP/out"
git filter-repo --force --paths-from-file "$ALLOWLIST" >/dev/null
git remote remove origin 2>/dev/null || true
git remote add pub "$PUBLIC_URL"
git push --force pub master:master
git push --force pub --tags
echo "published to $PUBLIC_URL ($(git rev-parse --short HEAD))"
