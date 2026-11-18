# Memory: recall, save, and client setup

[English](MEMORY-CLIENT-GUIDE.md) · [日本語](MEMORY-CLIENT-GUIDE.ja.md) · [简体中文](MEMORY-CLIENT-GUIDE.zh-CN.md) · [한국어](MEMORY-CLIENT-GUIDE.ko.md)

<!-- SEO: wawoo-skills memory_recall memory_save WAWOO_MEMORY_READONLY Cursor Kilo OpenCode MCP setup -->

## What memory does here

The kit stores **team decisions and gotchas** as Markdown under `docs/memory/`. Agents load them with **`memory_recall`** before work and append with **`memory_save`** after decisions (when writes are allowed).

**Not the same as** the client’s built-in chat memory: in this kit, **`docs/memory/` files win** on conflict. See [`memory/MEMORY-TOOLS.md`](memory/MEMORY-TOOLS.md).

## MCP tools

| Tool | What it does |
|------|----------------|
| `memory_recall` | Read `INDEX.md` + topic files. **Works even when saves are disabled.** |
| `memory_save` | Append one entry from [`memory/TEMPLATE.md`](memory/TEMPLATE.md). **Blocked** when `WAWOO_MEMORY_READONLY=1`. Secrets always rejected. |

## `WAWOO_MEMORY_READONLY` (you must set this)

| Value | Behavior | When to use |
|-------|----------|-------------|
| **`1`** | **Recall-only** — no `memory_save` | Default install; audits; MCP on random repos |
| **`0`** | **Read + write** | You want the kit to remember decisions in `docs/memory/` |

Set it in the **MCP `environment`** block, then **restart** the client (Kilo / Cursor Reload Window, OpenCode restart, Paseo: `paseo daemon restart`).

## First-time setup (recommended)

1. Clone **wawoo-skills** and note the absolute path (`WAWOO_SKILLS_ROOT`).
2. Run **one** install script with **`--memory-writable`** (see [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md)).
3. Confirm env:

```bash
grep WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc 2>/dev/null
grep WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json 2>/dev/null
grep WAWOO_MEMORY_READONLY ~/.cursor/mcp.json 2>/dev/null
```

4. In a test chat, call **`memory_save`** once. If readonly, the error names `WAWOO_MEMORY_READONLY`.
5. Copy [`memory/INDEX.example.md`](memory/INDEX.example.md) → `docs/memory/INDEX.md` in **your project** if you use memory outside the kit repo.

Example JSON:

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

Optional: `WAWOO_MEMORY_ROOT` overrides the directory (default `<kit>/docs/memory`).

## Per client

| Client | Config file | Install |
|--------|-------------|---------|
| Kilo | `~/.config/kilo/kilo.jsonc` | `python3 scripts/install_global.py --memory-writable` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` | `python3 scripts/install_opencode.py --memory-writable` |
| Cursor (user) | `~/.cursor/mcp.json` | `python3 scripts/install_cursor_global.py --memory-writable` |
| Cursor (project) | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root> --memory-writable` |

Longer install steps: [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md). Full manual: [USAGE.md §5.1](USAGE.md#51-memory-recall-save-and-how-to-configure-clients).

## Workflow limits

Some workflows **forbid** `memory_save` even when `READONLY=0` (e.g. `/compliance-review`). See [INTENT-ROUTING.md](INTENT-ROUTING.md).

**Term:** **MCP allow list** = each workflow only permits certain tools (no deploy during audit).

**See also:** [GUIDES.md](GUIDES.md)

**Index:** [GUIDES.md](GUIDES.md)