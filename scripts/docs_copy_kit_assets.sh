#!/usr/bin/env bash
# MkDocs 出力に kit 顶栏／氛围 JS を同梱（/kit-header.css だけだと docs 単体で 404 になる）
set -euo pipefail
DOCS_ROOT="${1:?e.g. site/docs}"
WEB="${2:-$(cd "$(dirname "$0")/../website" && pwd)}"

mkdir -p "${DOCS_ROOT}/assets"
cp -f "${WEB}/kit-header.css" "${DOCS_ROOT}/assets/kit-header.css"
cp -f "${WEB}/kit-typography.css" "${DOCS_ROOT}/assets/kit-typography.css"
cp -f "${WEB}/kit-ambience.js" "${DOCS_ROOT}/assets/kit-ambience.js"