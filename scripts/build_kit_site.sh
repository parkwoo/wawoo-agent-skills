#!/usr/bin/env bash
# MkDocs + 収録生成 + locale 再配置 + website マージの正本（preview.sh / docs.yml 共用）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="${1:?output directory e.g. $ROOT/site}"

export WAWOO_SKILLS_GIT_REF="${WAWOO_SKILLS_GIT_REF:-master}"
export KIT_CATALOG_SOURCE="${KIT_CATALOG_SOURCE:-github}"

if [[ -f "$ROOT/scripts/gen_catalog_skill_buckets.py" ]]; then
  python3 "$ROOT/scripts/gen_catalog_skill_buckets.py"
fi
if [[ -f "$ROOT/scripts/gen_site_capabilities_json.py" ]]; then
  python3 "$ROOT/scripts/gen_site_capabilities_json.py"
fi
if [[ -f "$ROOT/scripts/install_kit_chrome.py" ]]; then
  python3 "$ROOT/scripts/install_kit_chrome.py"
fi

rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -a "$ROOT/website/." "$STAGE/"

MKDOCS="python3 -m mkdocs"
if [[ -x "$ROOT/.venv-docs/bin/mkdocs" ]]; then
  MKDOCS="$ROOT/.venv-docs/bin/mkdocs"
elif ! python3 -c "import mkdocs" 2>/dev/null; then
  MKDOCS=""
fi

if [[ -n "$MKDOCS" ]]; then
  bash "$ROOT/scripts/merge_kit_typography.sh"
  (cd "$ROOT" && $MKDOCS build -q)
  bash "$ROOT/scripts/docs_copy_kit_assets.sh" "$ROOT/site/docs"
  if [[ -d "$ROOT/site/docs" ]]; then
    rm -rf "$STAGE/docs"
    cp -a "$ROOT/site/docs" "$STAGE/docs"
    bash "$ROOT/scripts/docs_add_zh_aliases.sh" "$STAGE/docs"
    bash "$ROOT/scripts/docs_relayout_locale_paths.sh" "$STAGE"
    bash "$ROOT/scripts/docs_add_legacy_doc_redirects.sh" "$STAGE"
    bash "$ROOT/scripts/kit_short_url_redirects.sh" "$STAGE"
    bash "$ROOT/scripts/docs_sitemap_per_page.sh" "$STAGE/docs"
    for loc in cn en ja ko; do
      bash "$ROOT/scripts/docs_sitemap_per_page.sh" "$STAGE/${loc}/docs" 2>/dev/null || true
    done
    BUILD_ID="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    echo "kit-docs-build=${BUILD_ID}" >"$STAGE/.preview-build.txt"
    if [[ "${KIT_SKIP_CATALOG_VERIFY:-0}" != "1" ]] && [[ -x "$ROOT/scripts/verify_kit_catalog_public.sh" ]]; then
      bash "$ROOT/scripts/verify_kit_catalog_public.sh" "$STAGE"
    fi
  fi
else
  echo "注意: MkDocs 未インストール — ランディングのみステージします。" >&2
fi