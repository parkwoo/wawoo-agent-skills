# 记忆：回忆、保存与客户端配置

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## 工具

| MCP 工具 | 作用 |
|----------|------|
| `memory_recall` | 读取 `docs/memory/`（索引 + 主题文件）。只读模式下仍可用。 |
| `memory_save` | 追加一条记录。`WAWOO_MEMORY_READONLY=1` 时**拒绝**。含秘密的内容始终拒绝。 |

**正本：** 套件目录下 `docs/memory/`。详见 `docs/memory/MEMORY-TOOLS.md`。

## `WAWOO_MEMORY_READONLY`

| 值 | 效果 | 适用场景 |
|----|------|----------|
| **`1`**（安装默认） | 仅回忆，不能 `memory_save` | 任意仓库挂 MCP、审计、偏安全 |
| **`0`** | 可读可写 | 日常在套件仓库工作；与 Kilo / Cursor / OpenCode 一致 |

写在 **客户端 MCP 的 environment** 里。改完后必须 **重启客户端**（Kilo 重载窗口、Cursor 重载、OpenCode 重启、Paseo 则 `paseo daemon restart`）。

## 配置位置

| 客户端 | 文件 | 命令 |
|--------|------|------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `python3 scripts/install_global.py` 或加 **`--memory-writable`** |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `python3 scripts/install_opencode.py` **`--memory-writable`** |
| Cursor（用户） | `~/.cursor/mcp.json` | `python3 scripts/install_cursor_global.py` **`--memory-writable`** |
| Cursor（项目） | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root> --memory-writable` |

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

## 验证

```bash
grep WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

部分 workflow 仍会禁止 `memory_save`（如 `compliance-review`）。见 `docs/INTENT-ROUTING.md`。

**索引：** [GUIDES.zh-CN.md](GUIDES.zh-CN.md)