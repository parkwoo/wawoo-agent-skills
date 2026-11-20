#!/usr/bin/env bash
# リリース直前の機械チェック（README 版表示・資産検証・公開境界）。
# 使い方:
#   ./scripts/release_preflight.sh              # VERSION 反映 + 検証
#   ./scripts/release_preflight.sh v0.8.0     # 上記 + タグと VERSION の一致
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 scripts/sync_readme_version.py
python3 scripts/validate_assets.py
python3 scripts/check_public_boundary.py

if [[ $# -ge 1 ]]; then
  tag="${1#v}"
  ver="$(tr -d '[:space:]' < VERSION)"
  if [[ "$tag" != "$ver" ]]; then
    echo "release_preflight: tag $1 does not match VERSION ($ver)" >&2
    exit 1
  fi
  echo "OK: tag $1 matches VERSION"
fi

if ! git diff --quiet -- README.md README.ja.md README.ko.md README.zh-CN.md 2>/dev/null; then
  echo "NOTE: sync_readme_version updated README*.md — commit before tagging." >&2
  exit 1
fi

echo "release_preflight: OK ($(cat VERSION))"