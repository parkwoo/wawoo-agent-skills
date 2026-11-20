# Overview

wawoo-skills is an open-source kit: **skills**, **agents**, **workflows**, and an **MCP server** for AI coding agents (Cursor, Kilo, OpenCode).

## The problem

Agents often **ignore** skill files in the repo — same task, different improvisation every time.

## What this kit does

| Piece | Role |
|-------|------|
| **Workflows** (`.kilo/commands/`) | Named entry points — which skills to open, in order |
| **MCP** (`mcp/server.py`) | `interpret_intent`, `workflow_get`, `skill_get`, memory, safety tools |
| **Catalog** (`.kilo/CAPABILITIES.md`) | Pick candidates — never paste every skill at once |

**Invocation by design** — workflows set the steps; the agent still writes the code.

## Next

- [Quickstart](quickstart.md) — first successful MCP call in about 5 minutes  
- [Install](../install/cursor.md) — client-specific setup  
- [Full manual](../USAGE.md) — complete reference  