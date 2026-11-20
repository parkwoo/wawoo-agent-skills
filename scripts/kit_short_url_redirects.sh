#!/usr/bin/env bash
# 营销短链 → MkDocs 正文：/{loc}/{page}/ → /{loc}/docs/{page}/
# 与 docs/plans/SITE-MKDOCS-UNIFIED.md §2 一致
set -euo pipefail
STAGE="${1:?preview-site or site root}"

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
    <p><a href="${dest}">继续</a></p>
  </body>
</html>
EOF
}

for loc in cn en ja ko; do
  for page in download guides changelog; do
    mkdir -p "${STAGE}/${loc}/${page}"
    write_redirect "/${loc}/docs/${page}/" "${STAGE}/${loc}/${page}/index.html"
  done
done

# 站点根短链（过渡期）
write_redirect "/cn/docs/usage/" "${STAGE}/download/index.html"
write_redirect "/cn/docs/guides/" "${STAGE}/guides/index.html"
write_redirect "/cn/docs/changelog/" "${STAGE}/changelog/index.html"

mkdir -p "${STAGE}/cn"
write_redirect "/cn/docs/usage/" "${STAGE}/cn/index.html"

echo "kit short URLs: /{cn,en,ja,ko}/{download,guides,changelog}/ → docs"