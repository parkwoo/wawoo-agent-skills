---
name: modern-web-guidance-bridge
description: On-demand Modern Web Guidance via npx (search/retrieve/legacy-scan). External OSS bridge — do not fork guides into this kit.
license: MIT
---

# Modern Web Guidance bridge

[GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance) を **外部正本**として参照する。262 本の guide を wawoo にコピーしない。

## 前提

- **Node.js + `npx`**（ネットワーク必須）
- 無効化: 環境変数 `WAWOO_MWG_DISABLE=1`
- 実装: `scripts/mwg_bridge.py` · MCP: `mwg_search` / `mwg_retrieve` / `mwg_legacy_scan`

## いつ使う

| 依頼 | 操作 |
|------|------|
| 最新 Web API・Baseline・代替パターン | `search` → 候補 id → `retrieve` |
| リポジトリの legacy パターン洗い出し | `legacy-scan <path>`（P3；詳細は `legacy-web-scan` skill） |
| UI 納品の入口 | 先に **`frontend-guides-hub`**、必要時のみ本 bridge |

## 手順

1. ユーザーのタスクを **1 文の検索クエリ**にする（英語可）。
2. **検索**: `python3 scripts/mwg_bridge.py search "<query>"` または MCP `mwg_search`。
3. 上位 1〜2 件の **id** を選び **取得**: `python3 scripts/mwg_bridge.py retrieve <id>` または MCP `mwg_retrieve`。
4. 取得した guide だけをコンテキストに載せ、実装する。全文を会話に貼り直さない。
5. wawoo の **`web-design-guidelines`** / **`accessibility-audit`** と矛盾する場合は **プロダクト憲章・Vercel guidelines を優先**し、MWG は API 用法の補助とする。

## 禁止

- guide 本文のキット内ミラー・フォーク
- 検索結果を全部 `skill_get` 代替で読む（id 指定の 1 本のみ）