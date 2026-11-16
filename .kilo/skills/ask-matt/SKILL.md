---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---
# Ask Matt (skill router)

Use this to pick a skill/flow inside this repository. Before recommending, **open the target skill's `SKILL.md`** and check it (this summary is orientation only).

## Context budget

- Entry: this `SKILL.md` only (≤4KB guide).
- Detail: read [`references/routing-map.md`](routing-map.md) only when needed.
- Phase boundaries: [`PHASE-BOUNDARIES.md`](../PHASE-BOUNDARIES.md).

## Quick routes (wawoo-skills / Cursor)

| Situation | Entry |
|---|---|
| Ship a feature | `@.kilo/commands/feature-delivery.md` |
| Research → decision | `@.kilo/commands/research.md` |
| Huge and foggy | `wayfinder` → the reference on-ramp |
| No issue tracker configured | `setup-matt-pocock-skills` |

## Automatic route (deterministic · MCP)

To pick a workflow from keywords or an explicit `/workflow`, use MCP **instead of reading this skill** (so the agent can call it reliably).

1. `interpret_intent` (JSON) or `route_task` (human-readable text)
2. If `needs_scoring:true`, **read the full input via `upstream_prompt` and score the workflow fit** (no thinking, one JSON line): `{"workflow":"…","score":0.72,"trigger":"…"}`
3. Pass `scoring` back to the same tool to apply it. **Only when `learn:true`** is a score ≥ 0.85 promoted to the DB asynchronously (learn defaults to off).
4. Use the returned `workflow` with `workflow_get`
5. For ambiguous or composite tasks, use this skill and [`references/routing-map.md`](routing-map.md)

The resident receiver is optional. CLI-only: `scripts/task-router.py` or `scripts/wawoo-route.sh`.

## Selecting the absorbed (pstack) skills

- **Understand intent / runtime**: `why` (rationale, tradeoffs, regression motive), `how` (runtime behavior, ownership/layering before changing).
- **Context & reflection**: `recall` (rebuild working context before starting/resuming), `reflect` (mine learnings into skill edits after).
- **Engineering principles (apply-before)**: `principle-*` (design/debug/verify/context/concurrency/scope). Common:
  - Design: `principle-exhaust-the-design-space`, `principle-redesign-from-first-principles`, `principle-attack-the-premise`
  - Implement: `principle-foundational-thinking`, `principle-model-the-domain`, `principle-subtract-before-you-add`, `principle-type-system-discipline`
  - Debug: `principle-fix-root-causes`, `principle-build-the-lever`
  - Verify: `principle-test-behavior-not-implementation`, `principle-prove-it-works`, `benchmark-checklist`
  - Concurrency/ops: `principle-separate-before-serializing-shared-state`, `principle-make-operations-idempotent`
- **Verification / audit**: `blast-radius` (what else breaks), `create-verification-skill` / `maintain-verification-skill` (project-local verification skill).
- **Orchestration**: `figure-it-out` (auditable playbook for large/ambiguous work), `swarm` (parallel fan-out), `show-me-your-work` (decision log).
- **Prompting**: `sharpen` (deepen the task, then rewrite the prompt), `in-your-own-words` (restate the goal).
