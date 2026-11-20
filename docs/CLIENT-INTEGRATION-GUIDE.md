# Client integration (Kilo · Cursor · OpenCode · Paseo)

[English](CLIENT-INTEGRATION-GUIDE.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## Prerequisites

- **Python 3** on `PATH` (stdlib only for MCP).
- Clone or open the **kit root** (`wawoo-skills`).

## 1. Kilo (global)

```bash
cd /path/to/wawoo-skills
python3 scripts/install_global.py --memory-writable   # optional: recall-only if omitted
```

Reload VS Code Kilo. Check: `grep WAWOO_SKILLS_ROOT ~/.config/kilo/kilo.jsonc`

## 2. OpenCode (terminal & Paseo built-in)

```bash
python3 scripts/install_opencode.py --memory-writable
paseo daemon stop && paseo daemon start   # when using Paseo
```

Reads `~/.config/opencode/opencode.json` (commands, agents, MCP, `skills.paths`).

## 3. Cursor

```bash
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /your/workspace --memory-writable
```

**Reload Window** → Settings → MCP → enable `wawoo-skills`.

`install_cursor_workspace.py` **overwrites** project `mcp.json`; use `install_cursor_global.py` to **merge** at user level.

## 4. Memory

Install defaults: `WAWOO_MEMORY_READONLY=1`. For `memory_save`, pass **`--memory-writable`** on every install script above.

Details: [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md) (4 languages).

## 5. Verify

```bash
python3 scripts/validate_assets.py
# MCP smoke is run by install scripts
```

| Check | Command |
|-------|---------|
| Kilo MCP | `grep wawoo-skills ~/.config/kilo/kilo.jsonc` |
| OpenCode | `grep wawoo-skills ~/.config/opencode/opencode.json` |
| Paseo provider | `paseo provider diagnostic opencode` |
| Memory flag | see MEMORY-CLIENT-GUIDE |

## Related

- [GUIDES.md](GUIDES.md) — all short guides
- [USAGE.md](USAGE.md) — full manual
- [COPY-MARKETING-GUIDE.md](COPY-MARKETING-GUIDE.md) — writing workflows