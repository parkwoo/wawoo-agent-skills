# インストール — Cursor

公式: [cursor.com](https://cursor.com)

## 手順

1. キットまたはワークスペースを Cursor で開く（`AGENTS.md`・`.cursor/rules`）。
2. MCP 設定:

```bash
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace
python3 scripts/install_cursor_global.py   # ユーザー全体（merge）
```

3. **Settings → MCP** で **wawoo-skills** を有効化。
4. JSON 変更後は **Reload Window**。

## 環境変数

| 変数 | 意味 |
|------|------|
| `WAWOO_SKILLS_ROOT` | キット clone の絶対パス |
| `WAWOO_MEMORY_READONLY` | `1` 参照のみ（既定）· `0` で `memory_save` 可 |

書込みを許可:

```bash
python3 scripts/install_cursor_global.py --memory-writable
```

## 制限

- ネイティブ **`/feature-delivery`** 等は**動かない** — MCP の `workflow_get` または `@.kilo/commands/<name>.md`。
- エージェント切替は非対応 — `@.kilo/agents/<role>.md` を手で参照。

## MCP なし

```
@.kilo/CAPABILITIES.md → @.kilo/skills/<name>/SKILL.md → @.kilo/commands/<name>.md
```

詳細: [USAGE §3](../USAGE.ja.md)