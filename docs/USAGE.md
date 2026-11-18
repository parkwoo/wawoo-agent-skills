# Usage (Kilo / Cursor / MCP)

**Overview:** [PRODUCT-OVERVIEW.md](PRODUCT-OVERVIEW.md) · **Guides:** [GUIDES.md](GUIDES.md) (4 languages) · **Memory setup (start here):** [MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md)

> Japanese version: [USAGE.ja.md](https://github.com/parkwoo/wawoo-skills/blob/master/docs/USAGE.ja.md)

## 0. Prerequisites

- **Python 3 (standard library only)** is required (MCP server, maintenance scripts). **No extra packages.**
- `python3` (or `python` on Windows) must be on `PATH`. Check: `python3 --version`.
  - macOS: `xcode-select --install` if missing. Linux: `apt install python3`, etc. Windows: enable "Add python.exe to PATH" at https://www.python.org/downloads/.
- MCP launches with `python3` as the command (`kilo.json`, `.cursor/mcp.json`). If it has another name (`python` / `py`), align `command`.
- Details: README "Prerequisites (runtime)".

## 1. Contents

- Skills: `.kilo/skills/<name>/SKILL.md`
- Agents: `.kilo/agents/<name>.md`
- Workflows: `.kilo/commands/<name>.md`
- MCP: `mcp/server.py`
- Catalog (generated) — **counts live here** (source of truth): `.kilo/CAPABILITIES.md`

## 2. Kilo CLI / Kilo Code (https://kilo.ai · https://kilocode.ai)

1. Open this directory (auto-discovers `.kilo/`; MCP enabled via `kilo.json`).
2. Workflows: `/feature-delivery`, etc.
3. Skills: the model selects a `SKILL.md`, or reference one explicitly.

### Global install (use in all projects, idempotent)

Mirror `.kilo/{skills,agents,commands}` into `~/.config/kilo/` and idempotently register MCP and an applicability note (re-runnable).
```bash
python3 scripts/install_global.py --dry-run    # preview changes
python3 scripts/install_global.py              # apply (default mirror = delete extras)
python3 scripts/install_global.py --no-delete  # keep extras
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py  # alternate target
```
- MCP registers absolute paths (`/usr/bin/python3` + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`). The default is recall-only (`=1`); use `--memory-writable` (`=0`) to enable writes. See `mcp/README.md`.
- It also **generates `ROUTER.md`**, registers it in `instructions` as an **absolute path** idempotently, and sets `default_agent` to `wawoo-auto` (default).
  - Kilo `instructions` **require absolute paths** (a relative `ROUTER.md` is not injected into the runtime context).
  - The default agent `wawoo-auto` enforces "first tool = `workflow_get` / `interpret_intent`", preventing routing gaps when `code` is the default.
  - Control via `--default-agent <name>` / `--no-default-agent` / `--force-default-agent`.
- **Kilo must be restarted to take effect** (agents/commands/instructions are cached at server start; VS Code: Reload Window).
- Steps that assume the kit's repo-relative SSOT are **valid only inside the kit**. Note this in the global `AGENTS.md`.
- `validate_assets`: a skill/command name collision **does not warn if the command documents its entry** (`design-review`, `research` are handled). An undocumented collision is a `WARN` (`documents_entry` in `scripts/validate_assets.py`).

## 2.5 OpenCode (https://opencode.ai)

OpenCode reads `AGENTS.md` and connects MCP servers over stdio. Add the kit as a local MCP server in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "/abs/path/to/wawoo-skills/mcp/server.py"],
      "enabled": true,
      "environment": {
        "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
        "WAWOO_MEMORY_READONLY": "1"
      }
    }
  }
}
```
- OpenCode has no native slash / skill execution; use `AGENTS.md` + MCP (`interpret_intent` → `workflow_get` → `skill_get`).
- **One-shot install**: `python3 scripts/install_opencode.py` (recall-only by default). Use **`--memory-writable`** for `WAWOO_MEMORY_READONLY=0` (§5.1). Paseo's built-in OpenCode uses the same `opencode.json`.
- Verified by the `opencode_stdio_contract` E2E (MCP handshake + `tools/list`).

## 3. Cursor (https://cursor.com)

1. Open this directory (it reads `AGENTS.md` and `.cursor/rules`).
2. Enable `wawoo-skills` in **Settings → MCP** (`.cursor/mcp.json`).
3. Use the tools `capabilities` / `skill_search` / `skill_get`.

**Install (MCP + optional native skill symlinks)**

```bash
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace   # MCP only; overwrites project mcp.json
python3 scripts/install_cursor_global.py                                     # user ~/.cursor; merges wawoo-skills into mcp.json
# Enable memory_save (see §5.1):
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace --memory-writable
```

**Cursor limitations**:
- Slash commands (`/feature-delivery`, etc.) **do not work**.
- There is **no agent switching** (read `@.kilo/agents/<role>.md` and apply the role).
- There is **no auto-discovery / auto-start of `SKILL.md`**.

**Fallback (no MCP)**:
```
Look at @.kilo/CAPABILITIES.md, pick a candidate, read the needed @.kilo/skills/<name>/SKILL.md, and follow it.
Apply the steps in @.kilo/commands/<name>.md.
```

## 4. MCP (Model Context Protocol: https://modelcontextprotocol.io)

```bash
python3 mcp/server.py        # stdio (the client usually launches it)
python3 scripts/e2e_flows.py   # public smoke (contract/E2E)
```
**Catalog tools**: `capabilities`, `skill_search`, `skill_get`, `workflow_get`, `agent_get`, `memory_recall`, `memory_save`, `evidence_check`.

**Intent routing** (optional but recommended): `interpret_intent` → `workflow_get` → … → `workflow_clear`. Subtasks: `delegate_subtask`.

- Public guide: **[docs/INTENT-ROUTING.md](INTENT-ROUTING.md)** (L0–L3, score JSON, tool gate)
- Implementation / resident receiver: `mcp/README.md`

## 5. Call order

1. Choose the **Workflow** (entry). For ambiguous requests, use MCP **`interpret_intent`** to pick from the **12 workflows** ([INTENT-ROUTING.md](INTENT-ROUTING.md); list: [PRODUCT-OVERVIEW.md](PRODUCT-OVERVIEW.md)). When you can be explicit, use **`/delivery-lite`** (`docs/plans/ACTIVE.md` is the progress SSOT). Ceremony levels (L0–L3): see `AGENTS.md` §3 (distinct from the route layers `L0–L3` in `INTENT-ROUTING.md`).
2. Select candidates via the **catalog / MCP** (do not read everything).
3. Open only the **Skills** you need.
4. Follow the workflow's **output schema** and **gates** (approval, evidence).
5. Recall `memory` before work; save decisions after (see **§5.1**).

## 5.1 Memory: recall, save, and how to configure clients

### What the tools do

| MCP tool | Purpose |
|----------|---------|
| `memory_recall` | Read prior decisions from `docs/memory/` (INDEX + topic files). **Works even when writes are disabled.** |
| `memory_save` | Append one decision to INDEX + a topic file (`docs/memory/TEMPLATE.md`). **Rejected** when `WAWOO_MEMORY_READONLY=1`. Secrets are rejected in all cases. |

**SSOT**: Markdown under `<kit>/docs/memory/`. Kilo native memory is auxiliary — on conflict, the files win (`docs/memory/MEMORY-TOOLS.md`).

### `WAWOO_MEMORY_READONLY` (the switch users must set)

| Value | Effect | When to use |
|-------|--------|-------------|
| **`1`** (install **default**) | **Recall-only** — `memory_save` returns an error; agents can still `memory_recall`. | MCP registered from a **random project**; audit / compliance sessions; you do not want the agent writing into the kit tree. |
| **`0`** | **Read + write** — `memory_save` allowed into `WAWOO_SKILLS_ROOT/docs/memory/`. | Daily dev on the kit repo or a workspace that mirrors the same `docs/memory/` layout; Kilo / Cursor / Paseo·OpenCode parity. |

The MCP server reads this from the **client config env** when it starts. Changing the file alone is not enough — **restart the client** (Kilo Reload, Cursor Reload, OpenCode restart, `paseo daemon restart` for built-in OpenCode).

### Where to set it (by client)

| Client | Config file | Recommended command (idempotent) |
|--------|-------------|----------------------------------|
| **Kilo (global)** | `~/.config/kilo/kilo.jsonc` → `mcp.wawoo-skills.environment` | `python3 scripts/install_global.py` (default `1`) or **`--memory-writable`** (`0`) |
| **OpenCode** (terminal or **Paseo built-in**) | `~/.config/opencode/opencode.json` → `mcp.wawoo-skills.environment` | `python3 scripts/install_opencode.py` or **`--memory-writable`** |
| **Cursor (user)** | `~/.cursor/mcp.json` → `mcpServers.wawoo-skills.env` | `python3 scripts/install_cursor_global.py` (**merges** other MCP servers) + **`--memory-writable`** |
| **Cursor (workspace)** | `<workspace>/.cursor/mcp.json` | `python3 scripts/install_cursor_workspace.py --workspace <root>` + **`--memory-writable`** (overwrites `mcp.json` — merge manually if you have other servers) |

**Manual snippet** (any client — adjust path):

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

Optional: `WAWOO_MEMORY_ROOT` overrides the directory (default `<kit>/docs/memory`).

### Verify after changing

```bash
# Kilo
grep -A2 WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
# OpenCode / Paseo
grep -A2 WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
# Cursor
grep -A2 WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

Then restart the client and call `memory_save` once in a test session — or confirm the agent no longer sees “memory_save disabled” in `workflow_get` hints when readonly.

### Workflow limits (independent of this flag)

Some workflows **forbid** `memory_save` via the tool gate even when `READONLY=0` (e.g. `compliance-review`). See `docs/INTENT-ROUTING.md`.

### Related

- Process: `docs/memory/MEMORY-TOOLS.md`, `docs/memory/TEMPLATE.md`, skill `memory`
- `/feature-delivery` entry/exit: recall before, save after
- CI: `validate_assets.py` scans memory for secret-like strings

## 6. Context budget

- Contract ≤500tok / catalog ≤1k / Workflow ≤1.5k / **one skill ≤2–4KB** / memory top-5.
- Progressive disclosure: do not hand everything at once.
- Budget exceptions: read only the entry `SKILL.md`; details live in each skill's `references/` (e.g. `imagegen-frontend-mobile`, `ask-matt`, `wayfinder`, `design-brief`, `writing-for-agents`).

### 6.1 Skill expansion checklist (maintainers)

Token/cost hygiene when adding skills. Pair with `AGENTS.md` §8 and `validate_assets.py`.

| # | Action | Notes |
|---|--------|--------|
| 1 | Entry `SKILL.md` = steps + gates; heavy text in `references/` | New owned skills: **>4KB requires `references/`** (`skill_budget_warnings`) |
| 2 | **Curate** Cursor native skills (15–30 common); rest via **MCP `skill_get`** | `install_cursor_workspace.py` = MCP only. Full symlink = optional `install_cursor_global.py` — see `scripts/cursor-skills-curated.example.txt` |
| 3 | One-line `description`, **~160 chars** | `CAPABILITIES.md` truncates at 130; long descriptions inflate Cursor `available_skills` |
| 4 | Internal-only → `internal/skills` or workspace-only | `publication-boundary` skill |
| 5 | Long sessions: `compress_context`, `/compact`, `memory_save` | One session = one artifact (`AGENTS.md` §4.1) |
| 6 | Watch | `validate_assets` 4KB WARN; in production check **cache_read** and **reads <4KB/turn** first |

**Workflow vs skill**: Workflows (`.kilo/commands/`) own gates and output shape. Skills are **phase procedures** inside them (e.g. `/writing` → `writing-beats` → `writing-shape`; `/research` → `research-decision-room`). Prefer `references/` over turning a long skill into a workflow.

### 6.2 Uplift pilot (P0–P3)

| Phase | Deliverable |
|-------|-------------|
| P0 | `modern-web-guidance-bridge`, MCP `mwg_*`, `scripts/mwg_bridge.py` |
| P1 | `web-design-guidelines/expectations.md`, `scripts/skill_uplift_check.py` |
| P1.1 | `accessibility-audit` / `deployment` expectations, checker, `/ui-delivery` step **5b** |
| P1b | `internal/skill-uplift-ab/`, `scripts/skill_uplift_ab.py` (Playwright A/B) |
| P1.5 | `frontend-guides-hub` |
| P2 | Rules in `docs/SKILL-UPLIFT-PILOT.md` |
| P3 | `legacy-web-scan`, `scripts/legacy_web_scan.py` |

Prune when unguided success ~90%; fix guides on low uplift; evidence under `docs/evidence/skill-uplift/`.

## 7. Skills needing prerequisites (3)

`to-spec`, `to-tickets`, `triage` need an issue tracker. Run `setup-matt-pocock-skills` once.
Listed in `scripts/readiness.json`.

## 8. Maintenance

```bash
python3 scripts/validate_assets.py
python3 scripts/gen_capabilities.py
python3 scripts/e2e_flows.py
```
Versioning: `docs/VERSIONING.md`.
