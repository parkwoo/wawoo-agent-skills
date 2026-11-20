# Workflow 早見表

正本: `.kilo/commands/<name>.md`。迷ったら MCP **`interpret_intent`**。

| やりたいこと | 入口 |
|--------------|------|
| 小さな修正・1 機能 | `delivery-lite` |
| ゲート付きの横断機能 | `feature-delivery` |
| UI | `ui-delivery` |
| 調査・決定 | `research` |
| 品質見直し | `self-review` |
| 障害 | `incident-response` |
| リリース前 | `release-review` |
| 法務・監査（読取のみ） | `compliance-review` |
| 記事・文書 | `content-build` / `writing` |
| 進捗報告 | `status-report` |

## 既定ルート

**`wawoo-auto`** と **`interpret_intent`** が **20** workflow のどれかへ。

## Cursor（スラッシュなし）

`@.kilo/commands/delivery-lite.md` を開き手順に従う。フェーズの skill は MCP `skill_get`。

カタログ: `.kilo/CAPABILITIES.md`（自動生成・手編集しない）。

詳細: [INTENT-ROUTING](../INTENT-ROUTING.ja.md) · [GUIDES](../GUIDES.ja.md)