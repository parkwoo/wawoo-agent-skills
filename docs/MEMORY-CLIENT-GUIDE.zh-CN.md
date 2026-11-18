# 记忆：回忆、保存与客户端配置

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## 本套件里的 memory 是什么

把**团队决定与踩坑**写成 `docs/memory/` 下的 Markdown。开工前用 **`memory_recall`**，作决定后用 **`memory_save`**（允许写入时）。

与客户端自带对话记忆**不是一回事**；冲突时以 **`docs/memory/` 文件为准**。见 [`memory/MEMORY-TOOLS.md`](memory/MEMORY-TOOLS.md)。

## MCP 工具

| 工具 | 作用 |
|------|------|
| `memory_recall` | 读 `INDEX.md` 与主题文件。**只读模式仍可用。** |
| `memory_save` | 按 [`memory/TEMPLATE.md`](memory/TEMPLATE.md) 追加一条。`WAWOO_MEMORY_READONLY=1` 时**拒绝**。 |

## `WAWOO_MEMORY_READONLY`（必配）

| 值 | 效果 | 场景 |
|----|------|------|
| **`1`** | **仅回忆**，不能 `memory_save` | 安装默认、审计、任意仓库挂 MCP |
| **`0`** | **可读可写** | 要在 `docs/memory/` 里积累决策 |

写在**客户端 MCP 的 environment**，改后**重启客户端**（Kilo/Cursor 重载窗口、OpenCode 重启、Paseo：`paseo daemon restart`）。

## 首次配置（推荐）

1. 克隆 **wawoo-skills**，记下绝对路径  
2. 任一安装脚本加 **`--memory-writable`**（[CLIENT-INTEGRATION-GUIDE.zh-CN.md](CLIENT-INTEGRATION-GUIDE.zh-CN.md)）  
3. `grep WAWOO_MEMORY_READONLY` 确认为 `0`  
4. 试一次 **`memory_save`**  
5. 在业务仓库用时，参考 [`memory/INDEX.example.md`](memory/INDEX.example.md) 建 `docs/memory/INDEX.md`  

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

## 各客户端

| 客户端 | 配置文件 | 命令 |
|--------|----------|------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `install_global.py --memory-writable` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `install_opencode.py --memory-writable` |
| Cursor 用户 | `~/.cursor/mcp.json` | `install_cursor_global.py --memory-writable` |
| Cursor 项目 | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --memory-writable` |

完整说明：[USAGE.md §5.1](USAGE.md#51-memory-recall-save-and-how-to-configure-clients)

**索引：** [GUIDES.zh-CN.md](GUIDES.zh-CN.md)