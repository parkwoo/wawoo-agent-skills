#!/usr/bin/env bash
# UI mock のみ（MkDocs なし）— 五ページを配信。必ず HTTP で開く（file:// 不可）。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${PORT:-8765}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "エラー: python3 がありません。"
  exit 1
fi

if command -v fuser >/dev/null 2>&1 && fuser "${PORT}/tcp" >/dev/null 2>&1; then
  echo ""
  echo "警告: ポート ${PORT} は既に使用中です。"
  echo "  別ターミナルで古い http.server を止める: fuser -k ${PORT}/tcp"
  echo "  または: PORT=8766 ./preview-ui.sh"
  echo ""
  exit 1
fi

WSL_IP=""
if command -v hostname >/dev/null 2>&1; then
  WSL_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi

echo ""
echo "  配信目录: ${ROOT}"
echo "  ────────────────────────────────────────"
echo "  WSL / Linux 浏览器:"
echo "    http://127.0.0.1:${PORT}/"
echo "    http://127.0.0.1:${PORT}/docs/"
echo "    http://127.0.0.1:${PORT}/guides/"
echo "    http://127.0.0.1:${PORT}/changelog/"
echo "    http://127.0.0.1:${PORT}/download/"
if [[ -n "$WSL_IP" ]]; then
  echo "  Windows 浏览器（localhost 不通时）:"
  echo "    http://${WSL_IP}:${PORT}/"
fi
echo "  ────────────────────────────────────────"
echo "  注意:"
echo "  · 本ターミナルを閉じるとサーバーが止まります（Ctrl+C で終了）"
echo "  · HTML をダブルクリック（file://）しない — CSS が読めず真っ白になります"
echo "  · Windows からは PowerShell で .\\preview-ui.ps1 も可"
echo "  · /docs/usage/ は MkDocs 未統合のため 404 — ドキュメントは ./preview.sh を使う"
echo ""

cd "$ROOT"
exec python3 -m http.server "$PORT" --bind 0.0.0.0