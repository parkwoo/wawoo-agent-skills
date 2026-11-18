# 記憶：想起・保存・クライアント設定

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## このキットの memory とは

チームの**決定・ハマりどころ**を `docs/memory/` の Markdown に残し、作業前に **`memory_recall`**、決定後に **`memory_save`**（書込許可時）で使います。

クライアント内蔵の会話 memory とは別物です。**矛盾時は `docs/memory/` が優先**。[`memory/MEMORY-TOOLS.md`](memory/MEMORY-TOOLS.md)

## MCP ツール

| ツール | 役割 |
|--------|------|
| `memory_recall` | `INDEX.md` と topic を読む。**書込禁止でも可** |
| `memory_save` | [`memory/TEMPLATE.md`](memory/TEMPLATE.md) に従い 1 件追記。`WAWOO_MEMORY_READONLY=1` なら**拒否** |

## `WAWOO_MEMORY_READONLY`（必ず設定）

| 値 | 挙動 | 目安 |
|----|------|------|
| **`1`** | **recall-only**（保存不可） | インストール既定・監査・任意 repo |
| **`0`** | **読み書き可** | `docs/memory/` に決定を残したい日常運用 |

**MCP の `environment`** に書き、変更後は**クライアント再起動**（Kilo/Cursor Reload、OpenCode、Paseo は `paseo daemon restart`）。

## 初回セットアップ（推奨）

1. **wawoo-skills** を cloneし絶対パス（`WAWOO_SKILLS_ROOT`）を控える 
2. いずれかの install に **`--memory-writable`**（[CLIENT-INTEGRATION-GUIDE.ja.md](CLIENT-INTEGRATION-GUIDE.ja.md)） 
3. `grep WAWOO_MEMORY_READONLY` で `0` を確認 
4. 試しに **`memory_save`** — readonly ならエラーに変数名が出る 
5. 自プロジェクトで使うなら [`memory/INDEX.example.md`](memory/INDEX.example.md) を元に `docs/memory/INDEX.md` を用意 

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

## クライアント別

| クライアント | ファイル | コマンド |
|--------------|----------|----------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `install_global.py --memory-writable` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `install_opencode.py --memory-writable` |
| Cursor ユーザー | `~/.cursor/mcp.json` | `install_cursor_global.py --memory-writable` |
| Cursor プロジェクト | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --memory-writable` |

詳細: [USAGE.ja.md §5.1](USAGE.ja.md#51-記憶memory想起保存とクライアント別の設定)

## workflow 制限

`/compliance-review` 等は `READONLY=0` でも **`memory_save` 不可**。[INTENT-ROUTING.ja.md](INTENT-ROUTING.ja.md)

**索引:** [GUIDES.ja.md](GUIDES.ja.md)