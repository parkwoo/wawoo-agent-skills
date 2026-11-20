# FAQ

### Is wawoo-skills free?

Yes. MIT license. You provide the AI client and API credentials.

### How is this different from adding skills to the repo?

Skills nobody opens do not help. This kit defines **how they are invoked**: intent → workflow → phased `skill_get`.

### Which clients are supported?

**Cursor**, **Kilo**, **OpenCode** (including Paseo). See [Install](../install/cursor.md).

### Do I need pip for MCP?

No. The bundled server uses **Python 3 stdlib only**.

### Why does Cursor not run `/delivery-lite`?

Cursor does not execute Kilo slash commands. Use MCP `workflow_get` or `@.kilo/commands/delivery-lite.md`.

### Where is progress tracked?

In the kit repo: `docs/plans/ACTIVE.md` (agents update status there — not in chat only).

### Official website?

**https://skills.wawoo.jp** (when deployed). Repo: [github.com/parkwoo/wawoo-agent-skills](https://github.com/parkwoo/wawoo-agent-skills).

More: [README](https://github.com/parkwoo/wawoo-agent-skills/blob/master/README.md) · [USAGE](../USAGE.md)