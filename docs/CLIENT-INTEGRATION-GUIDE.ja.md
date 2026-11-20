# クライアント統合（Kilo · Cursor · OpenCode · Paseo）

[English](CLIENT-INTEGRATION-GUIDE.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## 前提

- **Python 3** が `PATH` にあること（MCP は標準ライブラリのみ）。
- キット root（`wawoo-skills`）を開く。

## 1. Kilo（グローバル）

```bash
cd /path/to/wawoo-skills
python3 scripts/install_global.py --memory-writable
```

Kilo / VS Code を **Reload**。確認: `grep WAWOO_SKILLS_ROOT ~/.config/kilo/kilo.jsonc`

## 2. OpenCode（ターミナル・Paseo 内蔵）

```bash
python3 scripts/install_opencode.py --memory-writable
paseo daemon stop && paseo daemon start
```

`~/.config/opencode/opencode.json` が正本。

## 3. Cursor

```bash
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /your/workspace --memory-writable
```

**Reload Window** → MCP で `wawoo-skills` 有効。

ワークスペース用 install は `mcp.json` を**上書き**。他 MCP がある場合は global の**マージ**を使う。

## 4. 記憶

既定は recall-only（`READONLY=1`）。三端で `memory_save` するなら各 install に **`--memory-writable`**。

[MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md)（4 言語）

## 5. 検証

```bash
python3 scripts/validate_assets.py
paseo provider diagnostic opencode
```

## 関連

- [GUIDES.ja.md](GUIDES.ja.md)
- [USAGE.ja.md](USAGE.ja.md)
- 社内詳細: `workspace/docs/RUNBOOK-SKILLS-INTEGRATION.md`