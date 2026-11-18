# 客户端集成（Kilo · Cursor · OpenCode · Paseo）

[English](CLIENT-INTEGRATION-GUIDE.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## 前提

- **Python 3**（MCP 仅用标准库）
- 克隆本仓库并记下**绝对路径**

## 步骤

1. 运行下面对应安装脚本  
2. 需要 `memory_save` 时加 **`--memory-writable`**（[MEMORY-CLIENT-GUIDE.zh-CN.md](MEMORY-CLIENT-GUIDE.zh-CN.md)）  
3. 重启客户端 / Reload Window  
4. `python3 scripts/validate_assets.py`

## Kilo

`python3 scripts/install_global.py --memory-writable`

## OpenCode / Paseo

`python3 scripts/install_opencode.py --memory-writable` · Paseo：`paseo daemon restart`

## Cursor

`install_cursor_global.py` / `install_cursor_workspace.py`，均加 **`--memory-writable`**

默认 **`WAWOO_MEMORY_READONLY=1`**（只回忆）。要写入须每次加 **`--memory-writable`**。

**索引：** [GUIDES.zh-CN.md](GUIDES.zh-CN.md)