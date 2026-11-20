#!/usr/bin/env bash
# website/kit-typography.css を styles.css・material-kit.css 末尾に追記（別 <link> 不要）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TYPO="$ROOT/website/kit-typography.css"
MARKER="/* === kit-typography SSOT（正本: website/kit-typography.css）=== */"

merge_into() {
  local target="$1"
  python3 - "$target" "$TYPO" "$MARKER" <<'PY'
import sys
from pathlib import Path

target, typo, marker = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
text = target.read_text(encoding="utf-8") if target.exists() else ""
if marker in text:
    text = text.split(marker, 1)[0].rstrip() + "\n"
body = typo.read_text(encoding="utf-8").strip()
target.write_text(f"{text.rstrip()}\n\n{marker}\n{body}\n", encoding="utf-8")
PY
}

merge_into "$ROOT/website/styles.css"
merge_into "$ROOT/docs/stylesheets/material-kit.css"
echo "merged kit-typography → styles.css, material-kit.css"