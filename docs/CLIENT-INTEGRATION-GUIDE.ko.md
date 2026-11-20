# 클라이언트 연동 (Kilo · Cursor · OpenCode · Paseo)

[English](CLIENT-INTEGRATION-GUIDE.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## 전제

- **Python 3** (`PATH`)
- 키트 루트(`wawoo-skills`) 열기

## 1. Kilo

```bash
python3 scripts/install_global.py --memory-writable
```

Kilo **Reload** · `grep WAWOO_SKILLS_ROOT ~/.config/kilo/kilo.jsonc`

## 2. OpenCode / Paseo

```bash
python3 scripts/install_opencode.py --memory-writable
paseo daemon stop && paseo daemon start
```

`~/.config/opencode/opencode.json`

## 3. Cursor

```bash
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /your/workspace --memory-writable
```

**Reload Window** → MCP `wawoo-skills` 활성화

## 4. 메모리

기본 `READONLY=1`. `memory_save` 필요 시 **`--memory-writable`**.

[MEMORY-CLIENT-GUIDE.ko.md](MEMORY-CLIENT-GUIDE.ko.md)

## 5. 검증

`python3 scripts/validate_assets.py` · `paseo provider diagnostic opencode`

## 관련

[GUIDES.ko.md](GUIDES.ko.md) · [USAGE.md](USAGE.md)