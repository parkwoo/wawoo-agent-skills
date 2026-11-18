# wawoo-skills: reproducible workflows for AI coding agents
<!-- SEO: Open-source kit for AI coding agents (Cursor, Kilo, OpenCode) — 97 skills, 21 agents, 12 workflows, Model Context Protocol (MCP) routing. Same request, same steps, with verifiable evidence. -->

[English](PRODUCT-OVERVIEW.md) · [简体中文](PRODUCT-OVERVIEW.zh-CN.md) · [日本語](PRODUCT-OVERVIEW.ja.md) · [한국어](PRODUCT-OVERVIEW.ko.md)

## What this kit is

**Your AI coding agent already has skills — it often does not use them.** wawoo-skills is a **product-neutral**, open-source kit: reusable **skills**, **agent roles**, **workflows**, and an **MCP** (Model Context Protocol) server. It defines what to read first and which workflow to run, so the same kind of request follows the **same steps** without blocking creative implementation. This ensures **reproducible outcomes** with verifiable evidence.

**Inventory (generated; do not hand-edit):** run `python3 scripts/gen_capabilities.py` and read `.kilo/CAPABILITIES.md`.

| Kind | Count | Source |
|------|-------|--------|
| Skills | **97** | `.kilo/CAPABILITIES.md` |
| Agents | **21** | `.kilo/CAPABILITIES.md` |
| Workflows | **12** | `.kilo/commands/<name>.md files` |

## In 60 seconds

**Without routing:** “Fix this bug.” The agent guesses, skips review, and tomorrow’s same request takes a different path.

**With wawoo-skills:** MCP `interpret_intent` picks `/self-review` → phases open `diagnosing-bugs` then `test-engineering` → you get logs or a repro before “done.”

## Who this is for

- Teams on **Cursor / Kilo / OpenCode** who already wrote skills but agents **never open them**
- Maintainers who want **review, test, and compliance** steps that actually run
- Anyone who wants the **same task → same workflow → same evidence**, without banning creative code

## Problems we solve

| # | You see this | Kit response |
|---|--------------|--------------|
| 1 | Skills exist but the agent **only improvises** | Workflows (`/delivery-lite`, …) + MCP `workflow_get` set the entry |
| 2 | Same task, different path every time | `interpret_intent` picks one of **12** workflows; phases name which skills to open |
| 3 | Review / legal / tests are **skipped** | Audit workflows (e.g., `/compliance-review`) are read-only; **evidence-based gates** need artifacts |
| 4 | Pasting the whole skill list wastes context | Catalog → candidates → **`skill_get` one skill at a time** |
| 5 | Team decisions lost next session | `memory_recall` / `memory_save` — see `docs/USAGE.md` §5.1 |
| 6 | Slash workflows need MCP in Cursor | MCP + `@.kilo/commands/`; each command file is the authoritative steps |
| 7 | “Done” with no repro or logs | `change-readiness`, plan/evidence patterns in `docs/plans/` |
| 8 | Dangerous tools during audit | Per-workflow **MCP allow lists** (e.g. `/compliance-review`) |
| 9 | PII or secrets sent outbound | `content-guardrail`, `data-egress-guard`, `mask_pii` |
| 10 | UI changes with no a11y proof | `/ui-delivery` phases + optional uplift checks (`docs/SKILL-UPLIFT-PILOT.md`) |

## How to read the jargon

| Term | Plain meaning |
|------|----------------|
| Invocation by design | **Design the call path** — start with `interpret_intent` or `workflow_get` |
| Progressive disclosure | Open **one SKILL at a time**, not the full catalog |
| Phase + exit_criteria | Each step has a written “done” condition |
| MCP | **Model Context Protocol** — stdlib Python server, no extra pip |
| Gates | **Approval, evidence, and observed failure** — ensuring verifiable completion, not just probable fixes |

## Skill map (by purpose)

Rough grouping of the **97** skills — full names are only in `.kilo/CAPABILITIES.md`.

| Area | About | Examples |
|------|-------|----------|
| Delivery & debugging | Specs, impl, bugs | `to-spec`, `implement`, `diagnosing-bugs`, `tdd` |
| Quality & architecture | Review, readiness | `code-review`, `change-readiness`, `architecture-decision` |
| UI & web | Design, a11y | `frontend-design`, `web-experience-design`, `accessibility-audit` |
| Research & product | Discovery, specs | `research`, `product-discovery`, `plan-md` |
| Safety & compliance | Release gates | `security-review`, `privacy-review`, `compliance-legal` |
| Operations | Ship & incidents | `deployment`, `incident-debugging`, `release-readiness` |
| Memory & context | Long sessions | `memory`, `context-compression` |
| Engineering principles | Principles & Guidelines (e.g., for engineering judgment, use as needed) | `principle-*` |
| Kit meta | Skills for skills | `writing-for-agents`, `publication-boundary`, `wayfinder` |

## Workflows (all 12)

| Your request | Workflow |
|--------------|----------|
| Small change / one feature | `/delivery-lite` |
| Full feature lifecycle | `/feature-delivery` |
| UI build or refresh | `/ui-delivery` |
| UI critique only | `/design-review` |
| Research then decide | `/research` |
| Self quality pass | `/self-review` |
| Process improvement | `/self-improve` |
| Sprint planning | `/sprint-plan` |
| Status / progress | `/status-report` |
| Incident | `/incident-response` |
| Pre-release package | `/release-review` |
| Legal / privacy / security read-only gate | `/compliance-review` |

Not sure where to start? Agent **`wawoo-auto`** or MCP **`interpret_intent`**.

## Agents (21 roles)

Roles are **viewpoints** (reviewer, implementer, PO, …), not separate products. List and descriptions: `.kilo/CAPABILITIES.md` → **Agents**.

## FAQ

### Is this tied to one product or company?
**No.** Skills and workflows are generic; bring your own repo and rules.

### Do I need extra Python packages for MCP?
**No** — the bundled MCP server uses **Python 3 standard library only**.

### Which clients work?
**Kilo**, **Cursor**, and **OpenCode** (with MCP configured). Details: `docs/USAGE.md`.

### How do I verify the inventory?
`python3 scripts/gen_capabilities.py` → read the header in `.kilo/CAPABILITIES.md` (currently **97 / 21 / 12**).

## Integrations (Paseo · Google · pstack)

- **[Paseo](https://github.com/getpaseo/paseo)** — same OpenCode + MCP install as CLI ([INTEGRATIONS.md](INTEGRATIONS.md))
- **Google** — Modern Web Guidance (`mwg_*` MCP) + `design-md` (Stitch); guides stay upstream
- **pstack** — MIT `principle-*` and verification skills ([ATTRIBUTION.md](../.kilo/skills/ATTRIBUTION.md))

## Read next

1. [`docs/INTEGRATIONS.md`](INTEGRATIONS.md) — Paseo, Google MWG, pstack  
2. [`docs/USAGE.md`](USAGE.md) — install, MCP, memory  
3. [`docs/INTENT-ROUTING.md`](INTENT-ROUTING.md) — workflows and tool gates  
4. [`.kilo/CAPABILITIES.md`](../.kilo/CAPABILITIES.md) — full skill and agent tables  