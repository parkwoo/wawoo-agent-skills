# Install — Kilo

Official: [kilo.ai](https://kilo.ai) · Kilo Code extension.

## Project

Open the kit directory — Kilo auto-discovers `.kilo/` and `kilo.json` (MCP on).

Workflows: `/feature-delivery`, `/delivery-lite`, etc.

## Global (all projects)

```bash
python3 scripts/install_global.py --dry-run
python3 scripts/install_global.py
python3 scripts/install_global.py --no-delete    # keep extra mirrored files
```

Registers MCP with absolute `python3` + `WAWOO_SKILLS_ROOT`. Generates `ROUTER.md`, sets default agent **`wawoo-auto`**.

**Restart Kilo / Reload Window** after install — agents and MCP cache at startup.

Memory writable: `python3 scripts/install_global.py --memory-writable`

Full reference: [USAGE §2](../USAGE.md)