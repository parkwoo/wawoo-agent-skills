#!/usr/bin/env bash
# ローカルプレビュー：build_kit_site.sh → http.server
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT="${PORT:-8765}"
STAGE="${ROOT}/.preview-site"

export WAWOO_SKILLS_GIT_REF="${WAWOO_SKILLS_GIT_REF:-master}"
export KIT_CATALOG_SOURCE="${KIT_CATALOG_SOURCE:-github}"
if [[ -f "$ROOT/scripts/guides_i18n_sync_zh.py" ]] && [[ "${KIT_SKIP_I18N_SYNC:-0}" != "1" ]]; then
  need_i18n="$(python3 -c "
import json
from pathlib import Path
p = Path('$ROOT/website/content/guides.i18n.json')
items = (json.loads(p.read_text()) if p.is_file() else {}).get('items') or {}
print(0 if len(items) >= 90 else 1)
" 2>/dev/null || echo 1)"
  if [[ "$need_i18n" == "1" ]]; then
    echo "Skill 收录说明：CAPABILITIES 仅英文，需写入 guides.i18n.json …"
  fi
fi

bash "$ROOT/scripts/build_kit_site.sh" "$STAGE"

DOC_USAGE="$STAGE/cn/docs/usage/index.html"
if [[ ! -f "$DOC_USAGE" ]]; then
  echo ""
  echo "エラー: ドキュメントがステージにありません（$DOC_USAGE）。"
  echo "  website/ だけを python3 -m http.server で起動すると /docs は必ず 404 です。"
  echo "  必ず本スクリプト ./preview.sh を使ってください。"
  exit 1
fi

grep -qE "kit-doc-layout\.js|kit-doc-body" "$DOC_USAGE" || {
  echo "エラー: cn/docs/usage がドキュメント版式ではありません。"
  exit 1
}

if command -v fuser >/dev/null 2>&1 && fuser "$PORT/tcp" >/dev/null 2>&1; then
  echo ""
  echo "エラー: ポート $PORT は既に使用中です。"
  echo "  別ポート: PORT=8767 ./preview.sh"
  exit 1
fi

WSL_IP=""
if command -v hostname >/dev/null 2>&1; then
  WSL_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi

echo ""
echo "  トップ:     http://127.0.0.1:${PORT}/"
echo "  使用说明:   http://127.0.0.1:${PORT}/cn/docs/usage/"
echo "  English:    http://127.0.0.1:${PORT}/en/docs/usage/"
if [[ -n "$WSL_IP" ]]; then
  echo "  Windows:      http://${WSL_IP}:${PORT}/cn/docs/usage/"
fi
echo ""
echo "  ビルド:     $STAGE/.preview-build.txt"
echo "  終了: Ctrl+C"
echo ""

cd "$STAGE"
exec python3 -m http.server "$PORT" --bind 0.0.0.0