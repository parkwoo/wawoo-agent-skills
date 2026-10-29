# Documentation

> Japanese version: [README.ja.md](README.ja.md)

| Document | Content |
|---|---|
| [USAGE.md](./USAGE.md) | **Main public** — Kilo / Cursor / MCP, call order, context budget |
| [INTENT-ROUTING.md](./INTENT-ROUTING.md) | **Public** — workflow intent routing (L0–L3, `interpret_intent`, tool gate) |
| [METHODOLOGY.md](./METHODOLOGY.md) | Methodology of Skill / Agent / Workflow (why three layers, WARO) |
| [PROCESS-PHILOSOPHY.md](./PROCESS-PHILOSOPHY.md) | Process philosophy (lifecycle D0–D7, gates, traceability) |
| [VERSIONING.md](./VERSIONING.md) | Versioning (SemVer, CHANGELOG, tags) |
| [PUBLICATION.md](./PUBLICATION.md) | Public (git-managed) vs internal asset boundary |
| [memory/TEMPLATE.md](./memory/TEMPLATE.md) · [memory/MEMORY-TOOLS.md](./memory/MEMORY-TOOLS.md) | Memory format and tool priority (the real `INDEX.md`, etc. are created per project; the kit's own is non-public) |

**Design (for deeper reading)**: [design/INTENT-RECEIVER.md](./design/INTENT-RECEIVER.md)

## Whole repository

- `README.md` … overview, contents, quick start
- `AGENTS.md` … agent contract (invocation rules, guardrails)
- `mcp/README.md` … MCP server tools, config, security
- `.kilo/skills/ATTRIBUTION.md` … skill origins and licenses
- `LICENSES/` … full license texts
- `CHANGELOG.md` / `VERSION` … change history, current version

Maintainer-only (not published): `internal/` (tracked in this private repo; details in [PUBLICATION.md](./PUBLICATION.md))
