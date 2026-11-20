# 記憶：想起・保存・クライアント設定

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## ツール

| MCP | 用途 |
|-----|------|
| `memory_recall` | `docs/memory/` を読む。書込禁止でも可。 |
| `memory_save` | 1 件追記。`WAWOO_MEMORY_READONLY=1` なら**拒否**。秘密は常に拒否。 |

**正本:** `<kit>/docs/memory/` · `docs/memory/MEMORY-TOOLS.md`

## `WAWOO_MEMORY_READONLY`

| 値 | 挙動 | 目安 |
|----|------|------|
| **`1`**（install 既定） | recall-only | 安全・監査・任意 repo |
| **`0`** | 読み書き可 | 日常開発・三端揃え |

**クライアント MCP の env**。変更後は **再起動**（Kilo/Cursor Reload、OpenCode 再起動、`paseo daemon restart`）。

## 設定場所

| クライアント | ファイル | コマンド |
|--------------|----------|----------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `install_global.py` **`--memory-writable`** |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `install_opencode.py` **`--memory-writable`** |
| Cursor ユーザー | `~/.cursor/mcp.json` | `install_cursor_global.py` **`--memory-writable`** |
| Cursor プロジェクト | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --memory-writable` |

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

## 確認

```bash
grep WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

workflow により `memory_save` 不可の場合あり（`compliance-review` 等）。`docs/INTENT-ROUTING.ja.md`

**索引:** [GUIDES.ja.md](GUIDES.ja.md)