#!/usr/bin/env bash
# MkDocs i18n 构建后レイアウト:
#   zh（default）→ /cn/docs/...
#   en/ja/ko      → /{locale}/docs/...
# 共有 assets  → /docs/assets/ 等
set -euo pipefail
STAGE="${1:?preview-site root (e.g. .preview-site)}"
DOCS="${STAGE}/docs"

for loc in en ja ko; do
  if [[ -d "${DOCS}/${loc}" ]]; then
    mkdir -p "${STAGE}/${loc}"
    rm -rf "${STAGE}/${loc}/docs"
    mv "${DOCS}/${loc}" "${STAGE}/${loc}/docs"
  fi
done

# 简体 → /cn/docs/（zh ビルド成果は DOCS 直下）
mkdir -p "${STAGE}/cn/docs"
for name in skills-catalog changelog; do
  if [[ -d "${DOCS}/${name}" ]]; then
    mv "${DOCS}/${name}" "${STAGE}/cn/docs/"
  fi
done
if [[ -d "${DOCS}/usage" ]]; then
  mv "${DOCS}/usage" "${STAGE}/cn/docs/"
fi
for f in index.html 404.html; do
  if [[ -f "${DOCS}/${f}" ]]; then
    mv "${DOCS}/${f}" "${STAGE}/cn/docs/"
  fi
done
if [[ -f "${DOCS}/sitemap.xml" ]]; then
  cp -a "${DOCS}/sitemap.xml" "${STAGE}/cn/docs/sitemap.xml"
fi

fix_html_tree() {
  local tree="$1"
  [[ -d "$tree" ]] || return 0
  find "$tree" -type f -name '*.html' -print0 | while IFS= read -r -d '' f; do
    sed -i \
      -e 's|href="\.\./\.\./assets/|href="/docs/assets/|g' \
      -e 's|src="\.\./\.\./assets/|src="/docs/assets/|g' \
      -e 's|href="\.\./\.\./stylesheets/|href="/docs/stylesheets/|g' \
      -e 's|href="\.\./\.\./javascripts/|href="/docs/javascripts/|g' \
      -e 's|src="\.\./\.\./javascripts/|src="/docs/javascripts/|g' \
      -e 's|href="\.\./\.\./search/|href="/docs/search/|g' \
      -e 's|url:"\.\./\.\./search/|url:"/docs/search/|g' \
      -e 's|href="/docs/en/|href="/en/docs/|g' \
      -e 's|href="/docs/ja/|href="/ja/docs/|g' \
      -e 's|href="/docs/ko/|href="/ko/docs/|g' \
      -e 's|href="../../en/|href="/en/docs/|g' \
      -e 's|href="../../ja/|href="/ja/docs/|g' \
      -e 's|href="../../ko/|href="/ko/docs/|g' \
      -e 's|href="../../usage/|href="/cn/docs/usage/|g' \
      -e 's|href="../../skills-catalog/|href="/cn/docs/skills-catalog/|g' \
      -e 's|href="../../changelog/|href="/cn/docs/changelog/|g' \
      -e 's|href="/docs/usage/|href="/cn/docs/usage/|g' \
      -e 's|href="/docs/skills-catalog/|href="/cn/docs/skills-catalog/|g' \
      -e 's|href="/docs/changelog/|href="/cn/docs/changelog/|g' \
      -e 's|href="/docs/zh/|href="/cn/docs/|g' \
      -e 's|/USAGE/|/usage/|g' \
      "$f"
  done
}

fix_html_tree "${STAGE}/en/docs"
fix_html_tree "${STAGE}/ja/docs"
fix_html_tree "${STAGE}/ko/docs"
fix_html_tree "${STAGE}/cn/docs"
fix_html_tree "${DOCS}"

echo "docs relayout: zh→/cn/docs/, en|ja|ko→/{loc}/docs/, assets→/docs/*"