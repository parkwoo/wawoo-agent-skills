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

## pstack 吸收后的选择指引（新增）

- **理解需求/意图**：`why`（为何这样做/设计取舍/回归动机）、`how`（如何运行/改动前走查/归属分层）。
- **上下文与反思**：`recall`（开工/续接前重建上下文）、`reflect`（会话后提炼并落到 skill 编辑）。
- **工程原则（apply-before）**：`principle-*`（设计/调试/验证/上下文/并发/范围）。常用：
  - 设计：`principle-exhaust-the-design-space`、`principle-redesign-from-first-principles`、`principle-attack-the-premise`
  - 实现：`principle-foundational-thinking`、`principle-model-the-domain`、`principle-subtract-before-you-add`、`principle-type-system-discipline`
  - 调试：`principle-fix-root-causes`、`principle-build-the-lever`
  - 验证：`principle-test-behavior-not-implementation`、`principle-prove-it-works`、`benchmark-checklist`
  - 并发/运维：`principle-separate-before-serializing-shared-state`、`principle-make-operations-idempotent`
- **验证/审计**：`blast-radius`（改动会破坏什么）、`create-verification-skill` / `maintain-verification-skill`（项目级验证 skill）。
- **编排**：`figure-it-out`（大型/模糊工作的可审计 playbook）、`swarm`（并行 fan-out）、`show-me-your-work`（决策日志）。
- **提示**：`sharpen`（把任务做深再重写 prompt）、`in-your-own-words`（复述目标）。
