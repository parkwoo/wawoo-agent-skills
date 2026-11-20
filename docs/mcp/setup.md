# MCP setup

Protocol overview: [modelcontextprotocol.io](https://modelcontextprotocol.io)

## Server

```bash
python3 mcp/server.py    # stdio — the IDE launches this
```

**Python 3 stdlib only.** No pip install for the server itself.

## Core tools

| Tool | Purpose |
|------|---------|
| `interpret_intent` | Pick a workflow for an ambiguous request |
| `workflow_get` | Phases, skills, `exit_criteria`, tool allow list |
| `skill_get` | Open one `SKILL.md` |
| `capabilities` / `skill_search` | Catalog without loading every skill |
| `memory_recall` / `memory_save` | `docs/memory/` (save blocked when `WAWOO_MEMORY_READONLY=1`) |
| `workflow_clear` | End session |

Smoke test:

```bash
python3 scripts/e2e_flows.py
```

## Call order

1. `interpret_intent` or explicit `workflow_get`  
2. Catalog / `skill_search` → `skill_get` per phase  
3. Gates — do not skip evidence or approval steps  
4. `workflow_clear` when done  

Memory and client env tables: [USAGE §4–5.1](../USAGE.md)

Deep dive: `mcp/README.md` in the repo.