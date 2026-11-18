# Client integration (Kilo · Cursor · OpenCode · Paseo)

[English](CLIENT-INTEGRATION-GUIDE.md) · [简体中文](CLIENT-INTEGRATION-GUIDE.zh-CN.md) · [日本語](CLIENT-INTEGRATION-GUIDE.ja.md) · [한국어](CLIENT-INTEGRATION-GUIDE.ko.md)

## Prerequisites

- **Python 3** on `PATH` (MCP uses stdlib only).
- Clone this repo — note the **absolute path** to the kit root.

## Quick path

| Step | Action |
|------|--------|
| 1 | Pick client below and run install script |
| 2 | Set **`--memory-writable`** if you need `memory_save` ([MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md)) |
| 3 | Restart client / Reload Window |
| 4 | `python3 scripts/validate_assets.py` |

## Kilo

```bash
cd /path/to/wawoo-skills
python3 scripts/install_global.py --memory-writable
```

Reload Kilo. Check: `grep WAWOO_SKILLS_ROOT ~/.config/kilo/kilo.jsonc`

## OpenCode (and Paseo)

```bash
python3 scripts/install_opencode.py --memory-writable
# Paseo:
paseo daemon stop && paseo daemon start
```

Config: `~/.config/opencode/opencode.json`

## Cursor

```bash
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /your/repo --memory-writable
```

**Reload Window** → enable MCP server `wawoo-skills`.

Project install **overwrites** `.cursor/mcp.json`; user-global install **merges** other servers.

## Memory default

Install scripts default to **`WAWOO_MEMORY_READONLY=1`** (recall-only). Pass **`--memory-writable`** on every install if you want saves.

**Guide:** [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md) (4 languages).

## Verify

```bash
python3 scripts/validate_assets.py
grep wawoo-skills ~/.config/kilo/kilo.jsonc 2>/dev/null || true
```

**Next:** [USAGE.md](USAGE.md) · [GUIDES.md](GUIDES.md)