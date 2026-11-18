---
name: legacy-web-scan
description: Legacy Web パターン掃引 — MWG legacy-scan と社内ルールで modernization 候補を plan-md へ。
license: MIT
---

# Legacy Web scan

## 手順

1. 対象パスを決める（例: `nextwave-bz` テーマ、`wawoo-tools` フロント）。
2. **MWG**: `python3 scripts/mwg_bridge.py legacy-scan <path>` または MCP `mwg_legacy_scan`（要 npx）。
3. **社内ルール**: `python3 scripts/legacy_web_scan.py <path>` — jQuery/Bootstrap3 等の軽量 grep。
4. 結果を **`plan-md`** にまとめ、優先度と **modern-web-guidance-bridge** で拾う guide id をリンク。
5. 破壊的削除・本番反映は **承認ゲート**。

## 参照

- `scripts/legacy_web_scan.py`
- `modern-web-guidance-bridge` skill