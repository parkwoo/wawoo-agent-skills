# Quickstart

Get the MCP server working once. No extra pip packages.

## 1. Prerequisites

```bash
python3 --version   # 3.x required (Windows: python --version)
```

Clone the kit and `cd` into the repo root.

## 2. Pick your client

| Client | Doc |
|--------|-----|
| **Cursor** (recommended for first try) | [Install: Cursor](../install/cursor.md) |
| Kilo | [Install: Kilo](../install/kilo.md) |
| OpenCode / Paseo | [Install: OpenCode](../install/opencode.md) |

**Cursor shortest path**

```bash
python3 scripts/install_cursor_workspace.py --workspace /abs/path/to/your/project
```

Reload Cursor (**Developer: Reload Window**). Enable MCP **wawoo-skills** in Settings.

Set `WAWOO_SKILLS_ROOT` to the **kit repo** path in `.cursor/mcp.json` (install script does this when the workspace is the kit itself).

## 3. Prove it works

In agent chat (MCP enabled), ask the model to call **`workflow_get`** with name `delivery-lite`, or run:

```bash
python3 scripts/e2e_flows.py
```

Expect contract smoke **failed=0**.

## 4. First real workflow

1. `interpret_intent` with a one-line task (e.g. fix a typo in docs).  
2. Open the workflow it suggests via `workflow_get`.  
3. Follow the phase skills with `skill_get` — one skill at a time.

Details: [Workflow cheat sheet](../workflows/cheat-sheet.md) · [MCP setup](../mcp/setup.md)