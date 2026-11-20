# クイックスタート

MCP を一度つなげる。追加 pip は不要。

## 1. 前提

```bash
python3 --version   # 3.x（Windows は python --version）
```

キットを clone し、リポジトリルートに `cd`。

## 2. クライアントを選ぶ

| クライアント | ドキュメント |
|-------------|-------------|
| **Cursor**（初回おすすめ） | [Cursor](../install/cursor.ja.md) |
| Kilo | [Kilo](../install/kilo.ja.md) |
| OpenCode / Paseo | [OpenCode](../install/opencode.ja.md) |

**Cursor 最短**

```bash
python3 scripts/install_cursor_workspace.py --workspace /abs/path/to/your/project
```

Cursor をリロード（**Developer: Reload Window**）。設定で MCP **wawoo-skills** を有効化。

`WAWOO_SKILLS_ROOT` は**キットの clone パス**（キット自体を workspace にした場合はインストールスクリプトが設定）。

## 3. 動作確認

エージェントチャットで **`workflow_get`**（`delivery-lite`）を呼ぶか:

```bash
python3 scripts/e2e_flows.py
```

**failed=0** なら OK。

## 4. 最初の workflow

1. `interpret_intent` で一行依頼  
2. 返った workflow を `workflow_get`  
3. フェーズごとに `skill_get` — **一度に 1 skill**

詳細: [Workflow 早見](../workflows/cheat-sheet.ja.md) · [MCP](../mcp/setup.ja.md)