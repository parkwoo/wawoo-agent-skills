# 客户端集成（Kilo · Cursor · OpenCode · Paseo）

[English](CLIENT-INTEGRATION-GUIDE.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## 前提

- **Python 3** 在 `PATH` 中（MCP 仅用标准库）。
- 打开或克隆 **套件根目录**（`wawoo-skills`）。

## 1. Kilo（全局）

```bash
cd /path/to/wawoo-skills
python3 scripts/install_global.py --memory-writable   # 省略则默认仅回忆
```

重载 VS Code 中的 Kilo。检查：`grep WAWOO_SKILLS_ROOT ~/.config/kilo/kilo.jsonc`

## 2. OpenCode（终端与 Paseo 内置）

```bash
python3 scripts/install_opencode.py --memory-writable
paseo daemon stop && paseo daemon start   # 使用 Paseo 时
```

配置：`~/.config/opencode/opencode.json`（命令、agent、MCP、`skills.paths`）。

## 3. Cursor

```bash
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /your/workspace --memory-writable
```

**Reload Window** → Settings → MCP → 启用 `wawoo-skills`。

项目级 `install_cursor_workspace.py` 会**覆盖** `mcp.json`；用户级 `install_cursor_global.py` 可**合并**其他 MCP。

## 4. 记忆

安装默认 `WAWOO_MEMORY_READONLY=1`。需要 `memory_save` 时，上述命令均加 **`--memory-writable`**。

详见 [MEMORY-CLIENT-GUIDE.zh-CN.md](MEMORY-CLIENT-GUIDE.zh-CN.md)（四语言）。

## 5. 验证

```bash
python3 scripts/validate_assets.py
```

| 检查 | 命令 |
|------|------|
| Kilo MCP | `grep wawoo-skills ~/.config/kilo/kilo.jsonc` |
| OpenCode | `grep wawoo-skills ~/.config/opencode/opencode.json` |
| Paseo | `paseo provider diagnostic opencode` |
| 记忆开关 | 见 MEMORY-CLIENT-GUIDE |

## 相关

- [GUIDES.zh-CN.md](GUIDES.zh-CN.md)
- [USAGE.md](USAGE.md)（英文完整手册）
- [COPY-MARKETING-GUIDE.zh-CN.md](COPY-MARKETING-GUIDE.zh-CN.md)