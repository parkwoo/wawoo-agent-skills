# クライアント統合（Kilo · Cursor · OpenCode · Paseo）

[English](CLIENT-INTEGRATION-GUIDE.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## 前提

- **Python 3**（MCP は標準ライブラリのみ）
- 本 repo の**絶対パス**を控える

## 手順の流れ

| # | 内容 |
|---|------|
| 1 | 下記いずれかの install |
| 2 | `memory_save` 要るなら **`--memory-writable`**（[MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md)） |
| 3 | クライアント再起動 / Reload |
| 4 | `python3 scripts/validate_assets.py` |

## Kilo

```bash
python3 scripts/install_global.py --memory-writable
```

## OpenCode / Paseo

```bash
python3 scripts/install_opencode.py --memory-writable
paseo daemon stop && paseo daemon start
```

## Cursor

```bash
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /your/repo --memory-writable
```

既定は **`WAWOO_MEMORY_READONLY=1`**。保存するなら毎回 **`--memory-writable`**。

**次:** [USAGE.ja.md](USAGE.ja.md) · [GUIDES.ja.md](GUIDES.ja.md)