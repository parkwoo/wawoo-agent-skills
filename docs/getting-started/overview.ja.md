# 概要

wawoo-skills は、AI コーディングエージェント（Cursor・Kilo・OpenCode）向けのオープンソースキットです。**skill**・**agent**・**workflow**・**MCP サーバ**をひとまとめにしています。

## 困りごと

リポジトリに skill があっても、エージェントが**開かず散文で進む** — 同じ依頼でも毎回手順が違う。

## キットの役割

| 部品 | 役割 |
|------|------|
| **Workflow**（`.kilo/commands/`） | 入口 — どの skill をどの順で開くか |
| **MCP**（`mcp/server.py`） | `interpret_intent`・`workflow_get`・`skill_get`・memory・安全系 |
| **カタログ**（`.kilo/CAPABILITIES.md`） | 候補だけ見せる — 全 skill を一度に渡さない |

**Invocation by design** — 手順は workflow が固定し、実装はエージェントが書く。

## 次に読む

- [クイックスタート](quickstart.ja.md) — 約 5 分で MCP を一度通す  
- [インストール](../install/cursor.ja.md) — クライアント別  
- [完全版マニュアル](../USAGE.ja.md) — リファレンス全体  