# 클라이언트 연동 (Kilo · Cursor · OpenCode · Paseo)

[English](CLIENT-INTEGRATION-GUIDE.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## 전제

- **Python 3** (MCP stdlib)
- 키트 root **절대 경로**

## 순서

1. 아래 install 스크립트  
2. `memory_save` 필요 시 **`--memory-writable`** ([MEMORY-CLIENT-GUIDE.ko.md](MEMORY-CLIENT-GUIDE.ko.md))  
3. 클라이언트 재시작  
4. `validate_assets.py`

## 명령

- Kilo: `install_global.py --memory-writable`
- OpenCode/Paseo: `install_opencode.py --memory-writable`
- Cursor: `install_cursor_global.py` / `install_cursor_workspace.py`

기본 **`WAWOO_MEMORY_READONLY=1`**.

**목차:** [GUIDES.ko.md](GUIDES.ko.md)