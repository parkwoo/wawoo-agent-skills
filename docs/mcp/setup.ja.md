# MCP セットアップ

プロトコル: [modelcontextprotocol.io](https://modelcontextprotocol.io)

## サーバ

```bash
python3 mcp/server.py    # stdio — IDE が起動
```

**Python 3 標準ライブラリのみ**。サーバ用 pip は不要。

## 主なツール

| ツール | 用途 |
|--------|------|
| `interpret_intent` | 曖昧な依頼で workflow を選ぶ |
| `workflow_get` | フェーズ・skill・`exit_criteria`・ツール許可 |
| `skill_get` | `SKILL.md` を 1 件開く |
| `capabilities` / `skill_search` | カタログ |
| `memory_recall` / `memory_save` | `docs/memory/`（`WAWOO_MEMORY_READONLY=1` で save 拒否） |
| `workflow_clear` | セッション終了 |

スモーク:

```bash
python3 scripts/e2e_flows.py
```

## 呼び出し順

1. `interpret_intent` または `workflow_get`  
2. カタログ → フェーズごとに `skill_get`  
3. ゲートを省略しない  
4. 終了時 `workflow_clear`  

memory・環境変数: [USAGE §4–5.1](../USAGE.ja.md)

詳細: リポジトリの `mcp/README.md`