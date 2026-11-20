#!/usr/bin/env bash
# 多语言 URL 约定: 正本见 docs/plans/SITE-I18N-URL-CONTRACT.md（/cn/docs/usage/）
# /docs/zh/* → 简体正本；旧大写 USAGE → 小写 usage
set -euo pipefail
DOCS_ROOT="${1:?docs root (e.g. site/docs or .preview-site/docs)}"

write_redirect() {
  local dest="$1"
  local file="$2"
  mkdir -p "$(dirname "$file")"
  cat >"$file" <<EOF
<!DOCTYPE html>
<html lang="zh-Hans">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url=${dest}" />
    <link rel="canonical" href="${dest}" />
    <title>跳转</title>
  </head>
  <body>
    <p>页面已移动，<a href="${dest}">点此继续</a>。</p>
  </body>
</html>
EOF
}

# 简体别名 /docs/zh/...
write_redirect "../usage/" "${DOCS_ROOT}/zh/index.html"
write_redirect "../../usage/" "${DOCS_ROOT}/zh/usage/index.html"
write_redirect "../../changelog/" "${DOCS_ROOT}/zh/changelog/index.html"

# 旧路径 /docs/zh/USAGE/（历史）
write_redirect "../../usage/" "${DOCS_ROOT}/zh/USAGE/index.html"

# MkDocs 出力が USAGE のとき小写 usage へ（実体を残す）
if [[ -d "${DOCS_ROOT}/USAGE" && ! -d "${DOCS_ROOT}/usage" ]]; then
  mv "${DOCS_ROOT}/USAGE" "${DOCS_ROOT}/usage"
fi
# 旧大写路径（USAGE が残っている場合のみ跳转页）
if [[ -f "${DOCS_ROOT}/USAGE/index.html" ]]; then
  write_redirect "../usage/" "${DOCS_ROOT}/USAGE/index.html"
fi
write_redirect "../../usage/" "${DOCS_ROOT}/en/USAGE/index.html"
write_redirect "../../usage/" "${DOCS_ROOT}/ja/USAGE/index.html"

echo "docs 别名: ${DOCS_ROOT}/{zh/,USAGE/,en/USAGE/,ja/USAGE/} → usage 小写路径"