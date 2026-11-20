# wawoo-skills: Reproducible Workflows for AI Coding Agents
<!-- SEO: Empower your AI coding agent with wawoo-skills. Design reproducible workflows, ensure consistent quality, and enforce gates for features, bugs, and compliance. -->

[English](PRODUCT-OVERVIEW.md) · [日本語](PRODUCT-OVERVIEW.ja.md) · [简体中文](PRODUCT-OVERVIEW.zh-CN.md) · [한국어](PRODUCT-OVERVIEW.ko.md)

## What wawoo-skills does

Your AI agent already possesses powerful skills, but often struggles to use them consistently or effectively. wawoo-skills provides a structured kit of reusable components—skills, agents, and workflows—to guide your AI agent. It designs *what information to prioritize* and *which steps to follow*, ensuring that the same request leads to the same high-quality, reproducible outcome every time, without stifling creativity.

## Common Challenges We Solve

| # | Challenge | How wawoo-skills helps |
|---|-----------|------------------------|
| 1 | Agents improvise in prose despite existing docs and skills | Workflows (e.g., `/delivery-lite`) and MCP `workflow_get` define clear entry points and steps. |
| 2 | Inconsistent quality and paths for identical tasks (e.g., "fix this bug") | `interpret_intent` routes to one of 20 workflows, with phases specifying which skills to use. |
| 3 | Review, legal, and test gates are bypassed or superficial | Audit workflows forbid `implement`; **evidence gates** require verifiable proof. |
| 4 | Dumping 100+ skills overwhelms the agent and wastes tokens | A catalog-driven approach selects candidates, then `skill_get` opens skills one at a time (progressive disclosure). |
| 5 | Decisions and context are lost between sessions | `memory_recall` / `memory_save` integrate with client memory systems ([MEMORY-CLIENT-GUIDE.md](MEMORY-CLIENT-GUIDE.md)). |
| 6 | Slash commands (e.g., `/feature-delivery`) don't work in environments like Cursor without an MCP | MCP integration with `@.kilo/commands/` ensures command bodies are the Single Source of Truth. |
| 7 | Difficulty choosing the right skill for tasks like copy, market research, or long-form writing | Dedicated guides like [COPY-MARKETING-GUIDE.md](COPY-MARKETING-GUIDE.md) provide clear direction. |
| 8 | "Done" without reproduction steps, logs, or artifacts | `change-readiness` and `docs/evidence/` ensure tangible outputs and active content. |
| 9 | Accidental deployments or memory writes during read-only audits | Per-workflow MCP allow lists restrict tool access (e.g., `compliance-review` is read-only). |
| 10 | Wiki knowledge remains unused by the agent | `memory_recall` and INDEX reads are integrated at workflow start. |
| 11 | PII/secrets sent to external APIs | `guard_content` calls `mask_pii` (deterministic, LLM-independent) before egress. |
| 12 | UI work lacks accessibility/responsive evidence | `/ui-delivery` includes steps for uplift checks and evidence collection. |
| 13 | "Read all principles" blows the context window | Only relevant `principle-*` skills are loaded for each phase. |
| 14 | Configuration drift across Kilo, Cursor, OpenCode, Paseo | [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md) provides unified integration guidance. |

## Product Traits (Plain Language)

| Jargon | Meaning |
|--------|---------|
| Invocation by design | **Explicitly design the agent's call path** — starting with `interpret_intent` or `workflow_get`. |
| Progressive disclosure | **Avoid overwhelming the agent** — show skill candidates, then open one SKILL at a time. |
| Phase + exit_criteria | **Clearly define "done for this step"** — reducing agent wandering and improving focus. |
| mcp_tools_allow | **Restrict tools to the job at hand** — preventing actions like deployment during an audit. |
| approval gate / evidence gate / observed-failure gate | **Approval / Evidence / Observed Failure gates** — ensuring tasks are truly complete, not just "probably fixed." |
| Rails, not a cage | Provides **reproducible steps and guardrails**; the agent still handles the creative implementation. |

**Practical Note:** The MCP server uses **Python 3 standard library only** (no extra pip packages). The same kit root can be used across Kilo, Cursor, and OpenCode (Paseo).

## What's in the Kit

| Kind | Count | Single Source of Truth (SSOT) |
|------|-------|-------------------------------|
| **Skills** | 112 | `.kilo/CAPABILITIES.md` (auto-generated, full table) |
| **Agents** | 23 | `.kilo/CAPABILITIES.md` |
| **Workflows (slash commands)** | 20 | `.kilo/commands/*.md` |

> For a complete list of all skill **names**, run `python3 scripts/gen_capabilities.py` and refer to `.kilo/CAPABILITIES.md`. Below is a **map by purpose**.

## Skill Map (Categories)

| Category | Count | Examples | When Used | Example Workflow |
|----------|-------|----------|-----------|------------------|
| **Engineering** | 19 | `to-spec`, `tdd`, `implement`, `diagnosing-bugs` | Features, bugs, specs | `/delivery-lite`, `/feature-delivery` |
| **Quality** | 7 | `code-review`, `change-readiness`, `architecture-decision` | Pre-merge, design calls | `/self-review`, `/feature-delivery` |
| **UI / Frontend** | 13 | `web-experience-design`, `accessibility-audit`, `frontend-design` | Screens, components | `/ui-delivery`, `/design-review` |
| **Research & Copy** | 8 | `research`, `marketing-psychology`, `viral-hooks`, `writing-*` | Research, articles, pricing copy | `/research`, `/market-plan`, `/writing` |
| **Safety & Legal** | 6 | `security-review`, `privacy-review`, `content-guardrail` | Pre-release, outbound text | `/compliance-review`, `/release-review` |
| **Ops & Release** | 4+ | `deployment`, `incident-debugging`, `release-readiness` | Deploy, incidents | `/incident-response`, `/release-review` |
| **Docs & Planning** | 7+ | `plan-md`, `writing-for-agents`, `documentation-localization` | ACTIVE/CONTENT, README | `/content-delivery-lite`, `/status-report` |
| **Memory & Context** | 4+ | `memory`, `context-compression`, `recall` | Long sessions, saved decisions | Workflow entry |
| **Principles** | 24 | `principle-*` | Judgment support (only when needed) | 1–2 per phase |
| **Kit Plumbing** | Few | uplift scripts, `wawoo-auto` | Routing, verification | MCP always |

**Workspace-only** skills (omitted from public OSS): `kiun-*`, `paseo-orchestration`, `nextwave-catalog-bridge`, etc.

## Workflow Quick Reference

| Request | Start Here |
|---------|------------|
| Small fix / one feature | `/delivery-lite` |
| Cross-cutting feature | `/feature-delivery` |
| UI work | `/ui-delivery` |
| Decide with research | `/research` |
| Market / pricing narrative | `/market-plan` |
| Article / copy | `/writing` |
| Self quality pass | `/self-review` |
| Incident response | `/incident-response` |
| Pre-release review | `/release-review` |

Unsure? Consult agent **`wawoo-auto`** or MCP **`interpret_intent`**.



## FAQ

### What is wawoo-skills?
An open-source kit of **skills, agents, workflows, and an MCP server** for AI coding agents (Cursor, Kilo, OpenCode/Paseo). It makes the same request follow the same steps.

### How is this different from dumping skills into the agent?
The kit uses **progressive disclosure**: catalog → candidates → `skill_get` one skill at a time, tied to workflow phases—not a 100-skill paste.

### What is MCP in this project?
**Model Context Protocol** — a small Python stdlib server that exposes `interpret_intent`, `workflow_get`, `skill_get`, memory, and safety tools to the IDE.

### Do I need extra Python packages?
No. The bundled MCP server uses **Python 3 standard library only**.

## Read Next

1. [GUIDES.md](GUIDES.md) — Short guide index  
2. [CLIENT-INTEGRATION-GUIDE.md](CLIENT-INTEGRATION-GUIDE.md) — Installation  
3. [USAGE.md](USAGE.md) — Full manual  
4. `.kilo/CAPABILITIES.md` — **Full skill name list**
