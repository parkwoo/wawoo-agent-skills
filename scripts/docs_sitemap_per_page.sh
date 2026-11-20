#!/usr/bin/env bash
# Material の一部スクリプトが現在ページ URL 基準で sitemap.xml を取りに行く。
# 各 index.html があるディレクトリへサイトルート sitemap への相対 symlink を置く。
set -euo pipefail
DOCS_ROOT="${1:?docs root (e.g. site/docs or .preview-site/docs)}"
SITEMAP="${DOCS_ROOT}/sitemap.xml"
if [[ ! -f "$SITEMAP" ]]; then
  echo "skip: no sitemap at ${SITEMAP}"
  exit 0
fi

while IFS= read -r -d '' idx; do
  dir="$(dirname "$idx")"
  if [[ "$dir" == "$DOCS_ROOT" ]]; then
    continue
  fi
  rel="$(realpath --relative-to="$dir" "$SITEMAP")"
  ln -sf "$rel" "${dir}/sitemap.xml"
done < <(find "$DOCS_ROOT" -name index.html -print0)

echo "docs sitemap スタブ: ${DOCS_ROOT} 配下の index ディレクトリ"