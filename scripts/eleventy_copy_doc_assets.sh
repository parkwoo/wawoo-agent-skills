#!/usr/bin/env bash
# Eleventy 出力に docs の JS/CSS/assets を各 locale 配下へコピー
set -euo pipefail
STAGE="${1:?site root}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WEB="$ROOT/website"
DOCS="$ROOT/docs"

for loc in cn en ja ko; do
  base="$STAGE/$loc/docs"
  [[ -d "$base" ]] || continue
  mkdir -p "$base/javascripts" "$base/stylesheets" "$base/assets"
  cp -f "$DOCS/javascripts/"*.js "$base/javascripts/" 2>/dev/null || true
  cp -f "$DOCS/stylesheets/"*.css "$base/stylesheets/" 2>/dev/null || true
  cp -f "$DOCS/assets/"* "$base/assets/" 2>/dev/null || true
  # kit-doc 用ミニ CSS（Material を使わない）
  {
    echo "/* eleventy kit doc prose */"
    cat "$DOCS/stylesheets/extra.css" 2>/dev/null || true
    cat "$DOCS/stylesheets/material-kit.css" 2>/dev/null || true
  } >"$base/assets/kit-doc.css"
  cp -f "$WEB/kit-header.css" "$base/assets/kit-header.css" 2>/dev/null || true
done
echo "eleventy doc assets → $STAGE/{cn,en,ja,ko}/docs"