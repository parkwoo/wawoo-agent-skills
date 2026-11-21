#!/usr/bin/env bash
# Eleventy + 収録生成 + website マージ（preview.sh / docs.yml 共用）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="${1:?output directory e.g. $ROOT/site}"

export WAWOO_SKILLS_GIT_REF="${WAWOO_SKILLS_GIT_REF:-master}"
export KIT_CATALOG_SOURCE="${KIT_CATALOG_SOURCE:-github}"
export KIT_BUCKETS_LENIENT="${KIT_BUCKETS_LENIENT:-1}"

if [[ -f "$ROOT/scripts/gen_catalog_skill_buckets.py" ]]; then
  python3 "$ROOT/scripts/gen_catalog_skill_buckets.py" || {
    [[ "$KIT_BUCKETS_LENIENT" == "1" ]] || exit 1
    echo "注意: catalog-skill-buckets 未生成（続行）" >&2
  }
fi
if [[ -f "$ROOT/scripts/gen_site_capabilities_json.py" ]] && [[ "${KIT_SKIP_SITE_GEN:-0}" != "1" ]]; then
  if ! python3 "$ROOT/scripts/gen_site_capabilities_json.py"; then
    if [[ "${KIT_GEN_LENIENT:-1}" == "1" ]]; then
      echo "WARN: 収録再生成をスキップ（既存 docs/skills-catalog*.md を使用）" >&2
    else
      exit 1
    fi
  fi
fi
if [[ -f "$ROOT/scripts/install_kit_chrome.py" ]]; then
  python3 "$ROOT/scripts/install_kit_chrome.py"
fi

rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -a "$ROOT/website/." "$STAGE/"

python3 "$ROOT/scripts/eleventy_stage_content.py"

if [[ ! -f "$ROOT/node_modules/@11ty/eleventy/package.json" ]]; then
  command -v npm >/dev/null || { echo "ERROR: npm 必須（Eleventy）" >&2; exit 1; }
  (cd "$ROOT" && npm ci --no-audit --no-fund)
fi

(cd "$ROOT" && npx --yes eleventy --config=.eleventy.cjs --quiet --output="$STAGE")

bash "$ROOT/scripts/eleventy_copy_doc_assets.sh" "$STAGE"
bash "$ROOT/scripts/docs_add_legacy_doc_redirects.sh" "$STAGE"
bash "$ROOT/scripts/kit_short_url_redirects.sh" "$STAGE"
for loc in cn en ja ko; do
  bash "$ROOT/scripts/docs_sitemap_per_page.sh" "$STAGE/${loc}/docs" 2>/dev/null || true
done

BUILD_ID="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "kit-eleventy-build=${BUILD_ID}" >"$STAGE/.preview-build.txt"

if [[ ! -f "$STAGE/cn/docs/usage/index.html" ]]; then
  echo "ERROR: cn/docs/usage/index.html がありません" >&2
  exit 1
fi

if [[ "${KIT_SKIP_CATALOG_VERIFY:-0}" != "1" ]] && [[ -x "$ROOT/scripts/verify_kit_catalog_public.sh" ]]; then
  bash "$ROOT/scripts/verify_kit_catalog_public.sh" "$STAGE"
fi

echo "Eleventy 出力: $STAGE（build=${BUILD_ID}）"