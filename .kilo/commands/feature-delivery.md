---
description: Deliver a feature through discovery, design, implementation, testing, review, and approval gates.
agent: delivery-lead
replay: safe
---

# Feature Delivery

For an ordinary L1 request, consider `/delivery-lite` and `docs/plans/ACTIVE.md` first. Use this workflow when gates, discovery, and UI/security boundaries are heavy.

0. **Understand first**: `recall` + `why`/`how`; restate the goal and smallest change.
1. Read project instructions and inspect repository status; preserve unrelated changes.
2. **Memory (entry)**: `memory_recall` or read `docs/memory/INDEX.md` for prior decisions, constraints, and gotchas (`memory` skill).
2b. **Context hygiene**: if the conversation or context is long or repetitive, clean it first — MCP `compress_context` or the `context-compression` skill (deterministic, offline).
3. Use `product-discovery` to establish user outcome, acceptance criteria, scope, and open decisions.
4. Use `architecture-decision` when interfaces, data, dependencies, or significant tradeoffs change.
5. Delegate implementation and apply `engineering-quality`.
6. Use `test-engineering`; add `web-experience-design` and `accessibility-audit` for UI work, and `security-review` for sensitive boundaries.
7. Run `change-readiness` and report requested outcome, implementation, evidence, unverified items, risks, rollback, and approval required.
8. **Memory (exit)**: persist new decisions, constraints, or gotchas via `memory_save` or `docs/memory/` append (PROCESS P4 / D7).
9. Do not publish, deploy, push, tag, or perform external mutations unless explicitly approved.

## Apply-before skills

discover: `in-your-own-words`, `principle-attack-the-premise`; design: `principle-exhaust-the-design-space`; implement: `how` + `principle-*`; verify: `principle-prove-it-works`, `create-verification-skill`.

## Privacy / security / context

- Before any external LLM/API call or returning output: `guard_content` (policy gate) → `mask_pii` / `redact_infra` (redact) — see `data-egress-guard`.
- Never echo internal IPs, hosts, URLs, ports, or credentials in errors or logs.
- When context is long or repetitive: `context-compression` (MCP `compress_context`) + `principle-guard-the-context-window`.
- Security/privacy review: `security-review` / `privacy-review` (audit phase).
