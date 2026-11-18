<p align="center">
  <img src="assets/wawoo-skills-logo.png" width="128" alt="wawoo-skills logo" />
</p>

<h1 align="center">wawoo-skills Usage</h1>

<p align="center">
  <strong>A guide to installation, configuration, and usage.</strong>
</p>

<p align="center">
  <a href="USAGE.md">English</a> ·
  <a href="USAGE.ja.md">日本語</a> ·
  <a href="USAGE.zh-CN.md">简体中文</a> ·
  <a href="USAGE.ko.md">한국어</a>
</p>

<p align="center">
  <a href="../README.md">Back to README</a> ·
  <a href="https://github.com/parkwoo/wawoo-skills">GitHub</a>
</p>

> This document covers **installation, configuration, and troubleshooting** only. For "what it is and why," see [`README.md`](../README.md).

**Who it's for**: Developers setting up the kit for the first time. Expect about 10 minutes to a working setup.

**Supports**: Kilo, Cursor, OpenCode, Codex, Claude Code, Paseo (Python 3 standard library only).

## Fastest path (read this first)

1. Confirm Python 3 — [§0 Prerequisites](#s0)
2. Connect your client — [§2 Per-client setup](#s2) (**Kilo / Cursor are easiest**)
3. Verify — `python3 scripts/validate_assets.py` prints `OK`

Everything else (MCP parameters, memory settings, troubleshooting) is in the table of contents below.

> **Need to change a setting?** Working language, image-generation keys, memory, routing tuning, install target — all in [**§9 Settings**](#s9).

## Contents

- [0. Prerequisites](#s0)
- [1. What gets installed](#s1)
  - [1.1 How to look things up](#s1-1) · [1.2 Workflow structure](#s1-2) · [1.3 Managing the router](#s1-3) · [1.4 Add your own](#s1-4)
- [2. Per-client setup](#s2)
  - [2.1 Kilo](#s2-1) · [2.2 OpenCode](#s2-2) · [2.3 Cursor](#s2-3) · [2.4 Paseo](#s2-4) · [2.5 Codex](#s2-5) · [2.6 Claude Code](#s2-6)
- [3. MCP service](#s3)
- [4. Memory settings](#s4)
- [5. Call order](#s5)
  - [5.1 Common scenarios](#s5-1)
- [6. Maintenance and verification](#s6)
- [7. Cautions](#s7)
- [8. Troubleshooting](#s8)
- [9. Settings reference](#s9)

<a id="s0"></a>

## 0. Prerequisites: Python 3

- **Python 3 (standard library only)**: The MCP service and maintenance scripts use only the standard library. No extra packages are required.
- `python3` must be on `PATH` (Windows: `python`). Check: `python3 --version` → `3.x`.
  - macOS: `xcode-select --install`; Linux: `apt install python3`, etc.; Windows: install from https://www.python.org/downloads/ and select the **"Add python.exe to PATH"** option.
- MCP runs as `python3` (`kilo.json`, `.cursor/mcp.json`). If yours is named differently (`python` / `py`), change `command` in each config.
- No network and no `.env` needed (MCP uses stdio).

<a id="s1"></a>

## 1. What gets installed

One line: **a skill is "what it can do," an agent role is "whose viewpoint," and a workflow is "in what order, and what counts as done."**

<a id="s1-1"></a>

### 1.1 The three asset types: how to look them up

For definitions of skills / agents / workflows, see the [README glossary](../README.md). This section only covers **how to look things up**:

| Type | How to look up |
|---|---|
| Skills | `skill_search` / `.kilo/CAPABILITIES.md` |
| Agents | `agent_get` |
| Workflows | `workflow_get` |
| MCP service | `python3 mcp/server.py` |

<a id="s1-2"></a>

### 1.2 What a workflow looks like

**The list of 12 workflows is in the [README "12 workflows"](../README.md).** This section covers their structure — every workflow has:

- **Phases**: goal / owning agent / skills / `exit_criteria`; inspect one phase with `workflow_get {name, phase}`.
- **Gates**: approval, evidence, observed failure; **audit-type workflows are read-only** (no implement phase).
- **Exit criteria**: If these criteria are not met, the workflow is not considered complete.

**Workflows without an `implement` phase** (e.g., `/design-review`, `/compliance-review`, `/release-review`, `/research`, `/status-report`) never enter implementation. To change code, switch to `/delivery-lite`, `/feature-delivery`, `/ui-delivery`, `/incident-response`, or `/self-improve`.

<a id="s1-3"></a>

### 1.3 Intent routing (router)

**The selection order** (explicit → local lexical → learned → model score) is in the [README](../README.md). This section covers **how it's managed after selection**:

- **Tool gate**: Limits MCP tools to the workflow's **allow-list** (`mcp_tools_allow`) — audit workflows get read tools only, with no implement phase.
- **Session gate**: Remembers "which workflow we're in" across calls; `WAWOO_INTENT_RESUME=1` restores it after a restart, and `WAWOO_INTENT_CLIENT` keeps clients from clobbering each other.
- **Finish**: `workflow_clear` releases the current session gate.
- **Override routing**: Write `/name` directly, or pass `scoring` to `interpret_intent`. **Wrong pick or not found**: See [§8 Troubleshooting](#s8) (usually a missing MCP restart).

<a id="s1-4"></a>

### 1.4 Add your own (skill / agent / workflow)

- **skill**: Create `.kilo/skills/<name>/SKILL.md`; `name` must equal the directory name, the entry file stays ≤4KB, details go in `references/`.
- **agent**: Create `.kilo/agents/<name>.md` (`mode: primary|subagent`, permissions as needed).
- **workflow**: Create `.kilo/commands/<name>.md` (frontmatter: `description` / `agent` / `replay`).
- Then: `python3 scripts/validate_assets.py` → `python3 scripts/gen_capabilities.py` → **restart MCP / Kilo** (commands are cached at startup).

<a id="s2"></a>

## 2. Per-client setup (Kilo / Cursor / OpenCode / Codex / Paseo)

<a id="s2-1"></a>

### 2.1 Kilo (CLI / Kilo Code)

0. **Sign in first**: `kilo auth login` (pick a provider and sign in). Paseo also needs you signed in before it can launch Kilo.
1. Open this repository (`.kilo/` is auto-discovered; MCP is enabled by `kilo.json`).
2. Use slash commands like `/feature-delivery`; skills are chosen by the model or referenced explicitly.

**Global install** (available in every project; safe to re-run):

```bash
python3 scripts/install_global.py --dry-run     # preview changes
python3 scripts/install_global.py               # apply (mirror: delete extras)
python3 scripts/install_global.py --no-delete   # keep extra files
python3 scripts/install_global.py --memory-writable   # allow memory_save
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py   # custom target
```

- **This script performs three actions**: ① writes the MCP entry (absolute `python3` + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`); ② generates `ROUTER.md` and registers it as **absolute** `instructions`; ③ sets the default agent to `wawoo-auto` (`--default-agent` / `--no-default-agent` to change).
- Kilo's `instructions` **must be absolute paths** (relative paths are not injected).
- **Restart Kilo after changes** (agents / commands / instructions are cached at startup; VS Code: Reload Window).

<a id="s2-2"></a>

### 2.2 OpenCode

Add the kit as a local stdio MCP in `opencode.json`:

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

- One-shot setup: `python3 scripts/install_opencode.py` (read-only by default); add `--memory-writable` for writes.
- OpenCode has **no native slash commands / skill execution**; always go through MCP: `interpret_intent` → `workflow_get` → `skill_get`.

<a id="s2-3"></a>

### 2.3 Cursor

1. Open the directory (it reads `AGENTS.md` and `.cursor/rules`).
2. Enable `wawoo-skills` in **Settings → MCP** (`.cursor/mcp.json`).

```bash
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace   # MCP only (overwrites project mcp.json)
python3 scripts/install_cursor_global.py                                     # user-level ~/.cursor (merged)
# allow memory_save:
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace --memory-writable
```

**Cursor's limitations:**

- Slash commands (`/feature-delivery`, etc.) **do not run**;
- **No agent switching** (read `@.kilo/agents/<role>.md` and adopt the role yourself);
- **No automatic discovery / execution of `SKILL.md`**.

**Fallback without MCP**: Pick from `@.kilo/CAPABILITIES.md` → read `@.kilo/skills/<name>/SKILL.md` → follow the steps; workflows are defined in `@.kilo/commands/<name>.md`.

<a id="s2-4"></a>

### 2.4 Paseo (built-in OpenCode; different from the rest)

Paseo is a **multi-agent IDE** that ships OpenCode and runs agents inside its own **daemon** (a background service):

- **Config**: Uses the **same** `~/.config/opencode/opencode.json` (the `wawoo-skills` MCP connects there); install with `python3 scripts/install_opencode.py`.
- **Sign in first**: Before Paseo launches `kilo` / `cursor`, sign in to that CLI (Kilo: `kilo auth login`), or it won't start.
- **Restart rules**: After changing env vars or MCP,
  ```bash
  paseo daemon stop && paseo daemon start     # full switch
  # or: paseo daemon restart                  # worker only
  ```
  **Restarting the daemon also restarts the sessions it started.**
- **Separate processes**: The VS Code Kilo extension, Cursor desktop, and opencode/kilo/cursor in your own terminal are **not affected** by the daemon.
- **Plugins are separate**: Paseo's own plugin skills (`npx skills add getpaseo/paseo`) are unrelated to this kit; once MCP and the daemon are set up, they coexist.

<a id="s2-5"></a>

### 2.5 Codex (OpenAI Codex CLI / extension)

Codex reads `AGENTS.md`, loads skills, and supports MCP (`~/.codex/config.toml`). Add the kit as a stdio MCP:

```toml
[mcp_servers.wawoo-skills]
command = "python3"
args = ["/abs/path/to/wawoo-skills/mcp/server.py"]
env = { WAWOO_SKILLS_ROOT = "/abs/path/to/wawoo-skills", WAWOO_MEMORY_READONLY = "1" }
```

- Point the skills directory at `.agents/skills/` (if you copy `.kilo/skills/` there).
- Codex currently needs **manual configuration**; this repository does not include an automated installation script. Codex supports `/skills`, `$skill`, and MCP (`codex mcp add ...`).

<a id="s2-6"></a>

### 2.6 Claude Code (Anthropic CLI)

Claude Code supports MCP, `CLAUDE.md`, `.claude/skills/`, and `.claude/commands/` (native slash commands).

```bash
claude mcp add wawoo-skills \
  --env WAWOO_SKILLS_ROOT=/abs/path/to/wawoo-skills \
  --env WAWOO_MEMORY_READONLY=1 \
  -- python3 /abs/path/to/wawoo-skills/mcp/server.py
```

- **Skills**: Copy or symlink `.kilo/skills` to `.claude/skills`.
- **Workflows**: Copy `.kilo/commands/*.md` to `.claude/commands/` (native slash commands).
- **Contract**: Use `AGENTS.md` **or** `CLAUDE.md` — not both.
- **Subagents**: Use `Agent` (`subagent_type`); `swarm` / `reflect` can run in parallel.

> **Other MCP clients (e.g., Pi)**: If they support stdio MCP, connect with the same `python3 mcp/server.py`; skills live per the client's convention (e.g., `.pi/skills/`). With a subagent extension, `swarm` / `reflect` run in parallel; without one, they run sequentially (both are supported).

<a id="s3"></a>

## 3. MCP service

The kit's capabilities are exposed through a **local MCP service** (stdio: local process communication; the client starts it; no ports).

```bash
python3 mcp/server.py          # usually started by the client
python3 scripts/e2e_flows.py   # contract / E2E smoke
```

Common tools: `capabilities`, `skill_search`, `skill_get`, `workflow_get`, `agent_get`, `memory_recall`, `memory_save`; intent routing: `interpret_intent` → `workflow_get` → … → `workflow_clear`; subtasks: `delegate_subtask`.

<a id="s4"></a>

## 4. Memory settings

### 4.1 What the tools do

| MCP tool | Purpose |
|---|---|
| `memory_recall` | Reads past decisions from `docs/memory/` (INDEX + topic files). **Works in read-only mode.** |
| `memory_save` | Appends a decision (INDEX + topic file, template `docs/memory/TEMPLATE.md`). **Rejected when `WAWOO_MEMORY_READONLY=1`**; secrets are always rejected. |

The **single source of truth** for memory is the Markdown under `<kit>/docs/memory/`; if it conflicts with a client's built-in memory, **the content of these files takes precedence** (see `docs/memory/MEMORY-TOOLS.md`).

### 4.2 `WAWOO_MEMORY_READONLY` (read-only / writable)

| Value | Effect | When to use |
|---|---|---|
| **`1`** (install default) | **Read-only**: `memory_save` errors, `memory_recall` works | MCP registered in any project; audit/compliance sessions; you don't want the agent writing into the kit |
| **`0`** | **Readable and writable**: Writes to `WAWOO_SKILLS_ROOT/docs/memory/` | Daily work in the kit repo or a workspace with the same `docs/memory/` layout |

The MCP service reads this from the client's env **at startup** — **after editing the configuration, you must restart the client for the changes to take effect** (Kilo Reload, Cursor Reload, OpenCode restart, Paseo's built-in OpenCode via `paseo daemon restart`).

### 4.3 Where to set it per client

| Client | Config file | Recommended command (re-runnable) |
|---|---|---|
| Kilo (global) | `~/.config/kilo/kilo.jsonc` → `mcp.wawoo-skills.environment` | `python3 scripts/install_global.py` (default `1`) or `--memory-writable` (`0`) |
| OpenCode (terminal or **Paseo built-in**) | `~/.config/opencode/opencode.json` → `mcp.wawoo-skills.environment` | `python3 scripts/install_opencode.py` or `--memory-writable` |
| Cursor (user) | `~/.cursor/mcp.json` → `mcpServers.wawoo-skills.env` | `python3 scripts/install_cursor_global.py` (merges other MCPs) + `--memory-writable` |
| Cursor (project) | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root>` + `--memory-writable` (overwrites; merge manually) |

**Manual snippet** (any client; change the path):

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

Optional: `WAWOO_MEMORY_ROOT` overrides the directory (default `<kit>/docs/memory`).

### 4.4 How to verify

```bash
grep -A2 WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep -A2 WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep -A2 WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

Then **restart the client** and call `memory_save` once in a test session.

### 4.5 Workflows restrict it too

Even with `READONLY=0`, some workflows **forbid** `memory_save` (e.g., `/compliance-review`).

### 4.6 Reuse in other projects

Copy `docs/memory/INDEX.example.md` to `docs/memory/INDEX.md` to use the same memory mechanism.

<a id="s5"></a>

## 5. Call order (MCP tool chain)

1. Pick a **workflow** (the entry point); if unsure, use MCP `interpret_intent`.
2. Use the **catalog / MCP** to pick candidates (don't read everything).
3. Open only the **skill** you need.
4. Follow the workflow's **output shape and gates** (approval, evidence).
5. `memory_recall` before you start; `memory_save` when you decide.

> **While the overall workflow structure is fixed, the individual steps are flexible.** Skip an unnecessary step, reorder, change priorities, change scope or stop, and run independent subtasks in parallel. The system makes these adjustments **automatically** from evidence; you can step in at any time, but manual planning is not required.

<a id="s5-1"></a>

### 5.1 Common scenarios: one sentence → which workflow

| What you want | What you say | What runs |
|---|---|---|
| Fix a bug | "Fix this bug" | `/self-review`: reproduce first, then fix, with evidence |
| Add a small feature | "Add a settings page" | `/delivery-lite`: plan → implement → verify, logged to `ACTIVE.md` |
| Review a branch | "Review this branch" | `/self-review`: standards + spec axes in parallel |
| Prepare a release | "Prepare a release" | `/release-review`: legal / privacy / version / security read-only gates |
| Research before deciding | "Research X, then decide" | `/research`: research → product discovery → spec |
| Redo a page | "Redo the home page" | `/ui-delivery`: design → implement → accessibility check |
| Handle an incident | "Production is erroring" | `/incident-response`: evidence → mitigate → review |

<a id="s6"></a>

## 6. Maintenance and verification

```bash
python3 scripts/validate_assets.py    # asset checks (name=dir, refs, duplicates, JSON)
python3 scripts/gen_capabilities.py   # regenerate the catalog (don't hand-edit)
python3 scripts/e2e_flows.py          # MCP contract / E2E smoke
```

<a id="s7"></a>

## 7. Cautions (dependencies / keys / limits)

- **Skills that need an issue tracker**: `to-spec`, `to-tickets`, `triage` need configuration first (e.g., GitHub Issues), then run `setup-matt-pocock-skills`.
- **Image generation**: `imagegen-frontend-mobile` only writes prompts; for real images use `fal-gen` (`FAL_KEY`) or `openrouter-gen` (`OPENROUTER_API_KEY`).
- **Cursor** limitations: see §2.3.

> [!WARNING]
> **Never commit keys**: Do not commit API keys / tokens / `.env`; `memory_save` rejects secrets.

<a id="s8"></a>

## 8. Troubleshooting (FAQ)

| Symptom | Fix |
|---|---|
| `memory_save` errors (mentions readonly) | Set `WAWOO_MEMORY_READONLY=0` and **restart the client** (§4.2) |
| Changed config but MCP is unchanged | Restart the client; Paseo: `paseo daemon stop && paseo daemon start` |
| `python3` not found / different name | Change `command` in each config to the real one (`python` / `py`) |
| Kilo routing notes not applying | `instructions` must be **absolute paths** (§2.1) |
| Confirm the install | `python3 scripts/validate_assets.py` prints `OK` |

<a id="s9"></a>

## 9. Settings reference (env vars and config)

Key variables: **most people only set two** — `WAWOO_SKILLS_ROOT` (kit path) and `WAWOO_MEMORY_READONLY` (whether memory is writable).

### 9.1 Core (almost always set)

| Variable | Purpose | Default | How to set |
|---|---|---|---|
| `WAWOO_SKILLS_ROOT` | Absolute path to the kit root | Two levels above `server.py` | Client MCP `environment` / `env`; one-shot scripts write it |
| `WAWOO_MEMORY_READONLY` | `1` = read-only (can't save), `0` = writable | Install scripts default to `1` | `install_*.py --memory-writable`, or edit the config ([§4](#s4)) |
| `WAWOO_MEMORY_ROOT` | Memory directory | `<kit>/docs/memory` | Set it to put memory elsewhere |

### 9.2 Working language (three-tier policy)

Default: **code = English; engineering records and replies = the project working language (this kit = Japanese); explanatory docs = English primary + Japanese secondary**.

**To change (once per project):**

1. Edit `AGENTS.md` §1 (the authoritative contract);
2. Sync the two `(wawoo-skills: Japanese)` occurrences in `.kilo/skills/language-policy/SKILL.md`;
3. Regenerate routing notes: `python3 scripts/gen_router.py`;
4. Match this document's language notes.

> To change which language a whole document uses, produce `README.<lang>.md` / `docs/USAGE.<lang>.md` (this kit ships `en / ja / zh-CN / ko`).

### 9.3 Image generation

Set a key to actually generate images; `imagegen-frontend-mobile` only writes prompts and never calls a model.

| Capability | Key needed | Where | Notes |
|---|---|---|---|
| `fal-gen` (real images, fal.ai) | `FAL_KEY` (format `key_id:secret`) | `.kilo/skills/fal-gen/.env` (copy `.env.example`) | **Never commit or echo**; default cheapest model `flux/schnell` |
| `openrouter-gen` (real images, OpenRouter) | `OPENROUTER_API_KEY` (format `sk-or-v1-...`) | `.kilo/skills/openrouter-gen/.env` (copy `.env.example`) | Default `google/gemini-2.5-flash-image`; change with `OPENROUTER_IMAGE_MODEL`; cheaper: `google/gemini-3.1-flash-lite-image` |
| `imagegen-frontend-mobile` | None | — | **Prompts only**, no model call |

- Optional: `FAL_BASE_URL` sets the fal.ai endpoint.
- Both image skills generate in batches from a **manifest** and skip existing files (safe to re-run): run `--dry-run` first, confirm, then generate (images cost money).

> [!WARNING]
> **Never write keys into the repo** (don't commit `.env` either). Keep keys in a local `.env`, and confirm it's ignored by `.gitignore` (this repo ignores `.env` / `.env.*`, keeping only `.env.example`).

### 9.4 Google Modern Web Guidance

**What it is**: An online guide set from Google on "how to build modern web" (about 262 entries).

**What it solves**: An AI model's training data can become outdated. When building web UI, fetch the latest approach on demand — and it can also find old patterns worth retiring.

**How to use**: Describe your requirements in a prompt; the agent uses `modern-web-guidance-bridge` to search (`mwg_search`) and retrieve (`mwg_retrieve`). The guides are not copied into the repo.

**Prerequisite**: Node.js and network; offline, set `WAWOO_MWG_DISABLE=1` to turn it off.

**When it conflicts with existing standards**: Product standards / Vercel win.

### 9.5 Intent routing (advanced; usually unchanged)

`interpret_intent` handles "auto-pick the workflow"; the settings below only affect its matching details and **usually don't need changing**.

| Variable | Purpose | Default |
|---|---|---|
| `WAWOO_INTENT_LEARN_DB` | Learned-trigger store | `data/intent_learned.db` |
| `WAWOO_INTENT_SESSION` | Session-gate state file | `<root>/data/intent_session.json` |
| `WAWOO_INTENT_RESUME` | `1` restores the gate after a restart | off |
| `WAWOO_INTENT_CLIENT` | Per-client file, avoids gate collisions | empty |
| `WAWOO_INTENT_SOCKET` | Socket for the resident `intent_receiver.py` | empty |
| `WAWOO_INTENT_LEXICAL` / `_THRESHOLD` / `_MARGIN` / `_MIN_TOKENS` / `_MAX_ABSTAIN` / `_DEBUG` | Lexical routing switch, thresholds, debug | see `mcp/README.md` |

### 9.6 Install and CI

Affects installation and CI only, not daily use.

| Variable / flag | Purpose |
|---|---|
| `KILO_GLOBAL_DIR` | Target directory for `install_global.py` (default `~/.config/kilo`) |
| `CURSOR_API_KEY` | Cursor CLI **unattended CI** only (locally, use `agent login`) |

### 9.7 Doc-review scripts (optional)

Optional; used only by the review scripts, not part of the main flow.

`scripts/audit_docs_dual.py` / `scripts/openrouter_doc_audit.py` review docs via OpenRouter:

- `OPENROUTER_API_KEY` (required)
- `OPENROUTER_DOC_MODEL` (default `google/gemini-2.5-flash`)
- `OPENROUTER_QWEN_MODEL` (default `qwen/qwen3-30b-a3b`)

### 9.8 External prerequisites

Three skills need an issue tracker: `to-spec`, `to-tickets`, `triage` (see `scripts/readiness.json`). Configure once: `setup-matt-pocock-skills`.

### 9.9 Config file map

Where each client's config lives; **restart the client after changes**.

| Client / purpose | File |
|---|---|
| Kilo | `~/.config/kilo/kilo.jsonc` (project `kilo.json`) |
| Cursor (user / project) | `~/.cursor/mcp.json` / `<workspace>/.cursor/mcp.json` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` |
| Codex | `~/.codex/config.toml` |
| Image keys | `.kilo/skills/fal-gen/.env`, `.kilo/skills/openrouter-gen/.env` (**do not commit**) |
