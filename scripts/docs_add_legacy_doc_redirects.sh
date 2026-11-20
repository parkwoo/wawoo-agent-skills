#!/usr/bin/env bash
# 旧 URL・MkDocs 既定パスから正規 URL へ（相对跳转，适配任意 host）
set -euo pipefail
STAGE="${1:?preview-site root}"

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

DOCS="${STAGE}/docs"

# MkDocs 型 /docs/en/USAGE → /en/docs/usage
write_redirect "/en/docs/usage/" "${DOCS}/en/USAGE/index.html"
write_redirect "/en/docs/usage/" "${DOCS}/en/usage/index.html"
write_redirect "/en/docs/changelog/" "${DOCS}/en/changelog/index.html"
write_redirect "/en/docs/" "${DOCS}/en/index.html"
write_redirect "/ja/docs/usage/" "${DOCS}/ja/USAGE/index.html"
write_redirect "/ja/docs/usage/" "${DOCS}/ja/usage/index.html"
write_redirect "/ja/docs/changelog/" "${DOCS}/ja/changelog/index.html"
write_redirect "/ja/docs/" "${DOCS}/ja/index.html"

# 旧无前缀简体 → /cn/docs/
write_redirect "/cn/docs/usage/" "${DOCS}/usage/index.html"
write_redirect "/cn/docs/usage/" "${DOCS}/USAGE/index.html"
write_redirect "/cn/docs/skills-catalog/" "${DOCS}/skills-catalog/index.html"
write_redirect "/cn/docs/changelog/" "${DOCS}/changelog/index.html"
write_redirect "/cn/docs/" "${DOCS}/index.html"

echo "legacy redirects: /docs/* → /cn/docs/*; /docs/{en,ja}/* → /{en,ja}/docs/*"