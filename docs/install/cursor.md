# Install — Cursor

Official site: [cursor.com](https://cursor.com)

## Steps

1. Open the kit repo or your workspace in Cursor (`AGENTS.md` and `.cursor/rules` apply).
2. Install MCP config:

```bash
# Project only (overwrites workspace .cursor/mcp.json)
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace

# User global (merges into ~/.cursor/mcp.json)
python3 scripts/install_cursor_global.py
```

3. **Settings → MCP** — enable **wawoo-skills**.
4. **Reload Window** after changing JSON.

## Environment

| Variable | Meaning |
|----------|---------|
| `WAWOO_SKILLS_ROOT` | Absolute path to the kit clone |
| `WAWOO_MEMORY_READONLY` | `1` recall-only (default), `0` allow `memory_save` |

Writable memory:

```bash
python3 scripts/install_cursor_global.py --memory-writable
```

## Limitations

- Native **`/feature-delivery`** slash commands do **not** run — use MCP `workflow_get` or `@.kilo/commands/<name>.md`.
- No native agent switching — read `@.kilo/agents/<role>.md` manually.

## Without MCP

```
@.kilo/CAPABILITIES.md → @.kilo/skills/<name>/SKILL.md → @.kilo/commands/<name>.md
```

Full reference: [USAGE §3](../USAGE.md)