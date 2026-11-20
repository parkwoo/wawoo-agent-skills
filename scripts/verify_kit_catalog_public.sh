#!/usr/bin/env bash
# 公開 kit 収録ページに workspace 専用条目や古い件数が混ざっていないか検証する。
set -euo pipefail

ROOT="${1:-}"
if [[ -z "$ROOT" || ! -d "$ROOT" ]]; then
  echo "用法: $0 <.preview-site または site ルート>"
  exit 2
fi

# gen_site_capabilities_json.py の _FORBIDDEN_PUBLIC_NAMES と同期
FORBIDDEN_RE='kiun-report-corpus|paseo-orchestration|nextwave-catalog-bridge|wawoo-tools-stg-dagu-test|git-identity|kiun-corpus-auditor|kiun-corpus-wave'

shopt -s nullglob
html_files=(
  "$ROOT/cn/docs/skills-catalog/index.html"
  "$ROOT"/en/docs/skills-catalog/index.html
  "$ROOT"/ja/docs/skills-catalog/index.html
  "$ROOT"/ko/docs/skills-catalog/index.html
)

missing=0
for f in "${html_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "警告: 収録 HTML がありません: $f"
    missing=1
    continue
  fi
  if grep -Eiq "$FORBIDDEN_RE" "$f"; then
    echo "エラー: 内部専用条目が HTML に残っています: $f"
    grep -Ei "$FORBIDDEN_RE" "$f" | head -5
    exit 1
  fi
  if grep -Eq '114[[:space:]]+Skills|114[[:space:]]+skills|共 114 Skills' "$f"; then
    echo "エラー: 古い件数（114）が HTML に残っています: $f"
    exit 1
  fi
  if ! grep -Eq '\b98\b' "$f"; then
    echo "エラー: 期待する件数 98 が HTML に見つかりません: $f"
    exit 1
  fi
done

json="$ROOT/content/capabilities.catalog.json"
if [[ -f "$json" ]] && grep -Eiq "$FORBIDDEN_RE" "$json"; then
  echo "エラー: capabilities.catalog.json に内部専用 skill 名があります: $json"
  exit 1
fi

if [[ "$missing" -eq 1 ]]; then
  echo "エラー: 収録ページのビルドが不完全です。./website/preview.sh を再実行してください。"
  exit 1
fi

echo "verify_kit_catalog_public: OK ($ROOT)"