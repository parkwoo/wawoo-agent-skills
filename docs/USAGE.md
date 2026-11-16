# Usage (Kilo / Cursor / OpenCode / MCP)

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

OpenCode reads `AGENTS.md`, loads **native skills** from `skills.paths`, and connects MCP servers over stdio. The kit ships `opencode.json` at the repo root:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md"],
  "skills": { "paths": [".kilo/skills"] },
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "mcp/server.py"],
      "enabled": true
    }
  }
}
```

### Global install (use in all projects, idempotent)

Mirror `.kilo/{agents,commands}` into `~/.config/opencode/{agent,command}` and idempotently register MCP, `instructions`, `skills.paths`, and `default_agent`:
```bash
python3 scripts/install_opencode.py --dry-run    # preview changes
python3 scripts/install_opencode.py              # apply (default mirror = delete extras)
python3 scripts/install_opencode.py --no-delete  # keep extras
python3 scripts/install_opencode.py --memory-writable
OPENCODE_GLOBAL_DIR=/path/to/config python3 scripts/install_opencode.py  # alternate target
```
- Agents are mirrored with `name:` / `id:` stripped so the **agent key equals the file name** (what command `agent:` references; OpenCode otherwise keys an agent by `name:`).
- Registers `mcp.wawoo-skills` (absolute python + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`), `instructions` = `<kit>/AGENTS.md` (**absolute** — relative paths are not injected), `skills.paths` = `<kit>/.kilo/skills` (native discovery), and `default_agent` = `wawoo-auto` (`--no-default-agent` to skip).
- **OpenCode must be restarted** (config is loaded once at startup).
- No native slash execution: workflows run through MCP (`interpret_intent` → `workflow_get` → `skill_get`) plus the installed native subagents/commands.
- Verified by the `opencode_stdio_contract` E2E (MCP handshake + `tools/list`).

## 3. Cursor (https://cursor.com)

1. Open this directory (it reads `AGENTS.md` and `.cursor/rules`).
2. Enable `wawoo-skills` in **Settings → MCP** (`.cursor/mcp.json`).
3. Use the tools `capabilities` / `skill_search` / `skill_get` / `agent_get`.

### Native skills, agents, and global rules

Cursor reads native skills (`SKILL.md`), project subagents, and user-level rules, so the kit can be installed natively in addition to MCP:
```bash
python3 scripts/install_cursor_workspace.py --workspace /abs/path/to/project  # project: .cursor/{mcp.json,rules,agents,skills}
python3 scripts/install_cursor_global.py                                      # user:    ~/.cursor/{rules,agents,skills,mcp.json}
```
- `rules/` are copied with relative `@.kilo/` references rewritten to the kit's absolute path (valid from any project).
- `agents/` are generated from `.kilo/agents` (`name` + `description` + role body); obtain a role's content directly with MCP `agent_get`.
- `skills/` are symlinks to `.kilo/skills/<name>` (the kit stays the single source).
- **Project-level** `.cursor/agents` is read by the app, **CLI, and cloud agents**; **user-level** `~/.cursor/agents` is read by the **desktop app only**. For Cursor CLI / ACP, use the project install or MCP `agent_get`.

**Cursor limitations**:
- Slash commands (`/feature-delivery`, etc.) **do not run natively** — apply their steps, or fetch them via MCP `workflow_get`.
- There is **no automatic agent switching**; use a project subagent or apply the role from `agent_get` / `@.kilo/agents/<role>.md`.

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

**Guardrails / egress**: `mask_pii` (PII/secret masking + reversible mapping), `redact_infra` (strip private IPs/hosts/credentials from errors/logs), `guard_content` (policy-as-data allow/block gate, optional fail-closed).

**Context**: `compress_context` — deterministic, offline cleaning/compression of conversation turns (heuristic filters + fuzzy dedup + density budget; no LLM, no network). See `.kilo/skills/context-compression/SKILL.md`.

**Intent**: `interpret_intent` resolves slash → **local lexical (threshold/abstain)** → learned → upstream; calibrate with `python3 mcp/intent_calibrate.py`; schedules carry `complexity` / `model_tier`.

**Intent routing** (optional but recommended): `interpret_intent` → `workflow_get` → … → `workflow_clear`. Subtasks: `delegate_subtask`.

- Public guide: **[docs/INTENT-ROUTING.md](INTENT-ROUTING.md)** (L0–L3, score JSON, tool gate)
- Implementation / resident receiver: `mcp/README.md`

## 5. Call order

1. Choose the **Workflow** (entry). For ambiguous requests, use MCP **`interpret_intent`** to pick from the 12 workflows ([INTENT-ROUTING.md](INTENT-ROUTING.md)). When you can be explicit, use **`/delivery-lite`** (`docs/plans/ACTIVE.md` is the progress SSOT). Ceremony levels (L0–L3): see `AGENTS.md` §3 (distinct from the route layers `L0–L3` in `INTENT-ROUTING.md`).
2. Select candidates via the **catalog / MCP** (do not read everything).
3. Open only the **Skills** you need.
4. Follow the workflow's **output schema** and **gates** (approval, evidence).
5. Recall `memory` before work; save decisions after (`memory_save` writes INDEX + a topic file; `docs/memory/TEMPLATE.md`).

### Memory

- SSOT: `docs/memory/` (priority order for Kilo / MCP in `MEMORY-TOOLS.md`)
- Recall/save also at the entry and exit of `/feature-delivery`
- CI: `validate_assets.py` detects secret-like strings in memory
- E2E: `python3 scripts/e2e_flows.py` (**L0–L3**, MCP, workflow). `python3 scripts/cli_adapters_mock.py` (**Kilo/Cursor entry mock**)
- Validation CLIs: `plan_active` / `plan_l2_backlog` / `plan_l3_record` / `plan_content`

## 6. Context budget

- Contract ≤500tok / catalog ≤1k / Workflow ≤1.5k / **one skill ≤2–4KB** / memory top-5.
- Progressive disclosure: do not hand everything at once.
- Budget exceptions: read only the entry `SKILL.md`; details live in each skill's `references/` (e.g. `imagegen-frontend-mobile`, `ask-matt`, `wayfinder`, `design-brief`, `writing-for-agents`).

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

## 9. Language policy (default and how to change)

The kit ships a **three-tier** language policy — authoritative contract in `AGENTS.md` §1, rationale in `.kilo/skills/language-policy/SKILL.md`:

| Target | Default (`wawoo-skills`) |
|---|---|
| Code: comments, identifiers, strings, commit messages, config keys | **English** |
| Engineering records (`plans/`, `ACTIVE.md`, `RETRO-*`, `evidence/`, `memory/`) **and agent responses** | **Japanese** — the kit's `project working language` |
| Explanatory / user-facing docs (`README.md`, `docs/USAGE.md`, ...) | **English (primary) + Japanese (secondary)** — two files |

The `project working language` is a **kit default, not a hard rule**. Code stays English for tooling interop; the working language is your project's choice.

**To change the working language** (e.g. to English or another language):

1. Edit `AGENTS.md` §1 so the "working language" row states your choice.
2. Update `.kilo/skills/language-policy/SKILL.md` — the two rows that read "(wawoo-skills: Japanese)" must match.
3. Regenerate the router if it restates the rule: `python3 scripts/gen_router.py` (Kilo global `ROUTER.md`).
4. Optionally drop the secondary-language docs (`*.ja.md`) and ship one language; update `.publish-allowlist` accordingly.
