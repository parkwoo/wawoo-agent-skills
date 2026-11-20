# Memory: recall, save, client setup

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

## Tools

| MCP tool | Purpose |
|----------|---------|
| `memory_recall` | Read `docs/memory/` (INDEX + topics). Works when writes are disabled. |
| `memory_save` | Append one entry. **Blocked** when `WAWOO_MEMORY_READONLY=1`. Secrets always rejected. |

**SSOT:** `<kit>/docs/memory/`. See `docs/memory/MEMORY-TOOLS.md`.

## `WAWOO_MEMORY_READONLY`

| Value | Effect | Typical use |
|-------|--------|-------------|
| **`1`** (install default) | Recall-only — no `memory_save` | Random repos, audits, safety |
| **`0`** | Read + write | Daily kit work; match Kilo / Cursor / OpenCode |

Set in the **client MCP env**. **Restart** the client after changes (Kilo Reload, Cursor Reload, OpenCode restart, `paseo daemon restart`).

## Where to set

| Client | File | Command |
|--------|------|---------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `python3 scripts/install_global.py` or **`--memory-writable`** |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `python3 scripts/install_opencode.py` **`--memory-writable`** |
| Cursor (user) | `~/.cursor/mcp.json` | `python3 scripts/install_cursor_global.py` **`--memory-writable`** |
| Cursor (project) | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root> --memory-writable` |

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

## Verify

```bash
grep WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

Some workflows block `memory_save` anyway (e.g. `compliance-review`). See `docs/INTENT-ROUTING.md`.

**Index:** [GUIDES.md](GUIDES.md)