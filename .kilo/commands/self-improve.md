---
description: Self-improvement (retro → pdca-cycle → self-review → plan-md)
agent: project-manager
replay: safe
---

# Self Improve

1. Read `AGENTS.md` and recall `memory` (past decisions, failures, avoidances).
2. **`retro`**: review the **facts** of this iteration (what you did, what happened, the gap vs expectation).
3. **`pdca-cycle`**: decide **improvement actions** via Plan → Do → Check → Act (make them measurable).
4. If needed, **roll out the self-correction steps** (`code-review` → the `.kilo/agents/code-skeptic.md` viewpoint → `tdd`) to pay down technical debt.
5. If needed, reduce complexity using the **`.kilo/agents/code-simplifier.md` viewpoint** (no behavior change; Task delegation allowed).
6. **`plan-md`**: save the improvement plan as Markdown (**owner, deadline, metric**).
7. **`memory`**: save learnings and prevention. Confirm the effect at the next `retro`.

## Gates

- Base improvements on **evidence** (metrics, failure logs). Do not claim "improved" by inference.
- Business decisions, contracts, and legal are made by humans.
- Destructive changes, production, and deletions require approval.

## Privacy / security / context

- Before any external LLM/API call or returning output: `guard_content` (policy gate) → `mask_pii` / `redact_infra` (redact) — see `data-egress-guard`.
- Never echo internal IPs, hosts, URLs, ports, or credentials in errors or logs.
- When context is long or repetitive: `context-compression` (MCP `compress_context`) + `principle-guard-the-context-window`.
- Security/privacy review: `security-review` / `privacy-review` (audit phase).
