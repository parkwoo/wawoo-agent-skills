# 架构优势：router + 门禁 + 工作流（代码审计）

> **内部资料，不公开。** 基于对 `mcp/` 的代码审计，记录这套件「为什么强」的真实机制，供技术文章与对外文案取材。所有结论都能在括号里的文件/函数找到依据。

## 一句话

**router 选流程 → 门禁锁工具 → 工作流编排阶段与完成条件。** 三者是一条链，不是三个并列功能。

```
用户一句话
  → interpret_intent（router）
  → activate_schedule（门禁：按流程锁定 mcp_tools_allow）
  → workflow_get {phase}（阶段：goal / agent / skills / exit_criteria）
  → evidence_check（证据：真跑校验）
  → steer_task / delegate_subtask（运行中调计划）
  → workflow_clear（解除门禁）
```

## 1. Router：一句话 → 一条流程

依据：`mcp/intent_interpreter.py`、`mcp/intent_commands.py`、`mcp/intent_lexical.py`、`mcp/intent_upstream.py`

- **优先级**：`L0 显式命令 → L1 本地词法（默认开）→ L1 已学习触发词 → L2 上游评分`。
- **学习阈值**：`_LEARN_MIN_SCORE = 0.85` 只用于「把一次评分提升为已学习触发词」，**不是匹配阈值**；匹配是触发词命中（`find_match`）。
- **来源标记**：`explicit / learned / upstream / local / pending / fallback`，便于排查「为什么选了这条」。
- **路由层**：`route_layer = L0 | L1 | L2`。
- **显式覆盖**：写 `/name` 可直接指定，绕过评分。
- **`needs_scoring`**：候选不明确时返回该标记，让上游模型补一个评分再定。

> 优势点：**默认自动、可解释（source/layer/score）、可覆盖（/name）**。

## 2. 会话门禁：流程决定能用什么工具

依据：`mcp/intent_session.py`、`mcp/server.py`（`activate_schedule` / `do_workflow_clear`）

- 选中流程后**激活会话门禁**，当前会话绑定 `workflow / agent / mcp_tools_allow / command_path`。
- **豁免工具**（门禁期间始终可调）：`interpret_intent`、`route_task`、`workflow_clear`、`delegate_subtask`、`steer_task`、`compress_context`、`mask_pii`、`redact_infra`、`guard_content`。
- **持久化**：`WAWOO_INTENT_RESUME=1` 时，门禁可跨 MCP 重启恢复；只持久化最小字段（**不存原始 prompt**）。
- **TTL**：持久化会话超过 **12 小时**忽略并删除。
- **按客户端隔离**：`WAWOO_INTENT_CLIENT` 生成 `intent_session.<client>.json`，避免多客户端串台。
- `workflow_clear` 结束会话、解除门禁。

> 优势点：**权限不是「叮嘱模型别改」，而是会话级的工具白名单**。

### 门禁范围（重要，写文章时别说过头）

- `check_tool_allowed(name)` 在 MCP 分发处生效（`server.py`），**只拦 MCP 工具**，**不拦宿主（Kilo/Cursor 等）的原生文件编辑与终端**。
- 所以准确表述是「**MCP 工具只读**」，不是「代理完全不能改代码」。宿主侧的读写在门禁之外，靠流程与评审约束。
- `implement_allowed` 目前只写入 schedule（`intent_interpreter.py`），**不直接阻断**宿主编辑；它是「该流程有没有 implement 阶段」的元数据。

### 已知不一致（待决策）

- `self-review.md` 第 6 步要求「Fix → re-verify」，但 `intent_catalog.WORKFLOW_PHASES["self-review"] = ("audit", "verify", "report")` **没有 implement**（`implement_allowed=false`）。
- 由于门禁只管 MCP 工具，这不阻塞宿主编辑，但**语义矛盾**。二选一：给 `self-review` 加 `implement` 阶段，或把命令改成「只审不改，修复切 `/delivery-lite`」。

## 3. 工作流目录：工具档位 + 阶段

依据：`mcp/intent_catalog.py`

### 3.1 工具档位

| 档位 | 含义 | 典型 |
|---|---|---|
| `_MCP_FULL` | 可读可写 | 交付 / 实现类 |
| `_MCP_READ` | 只读 | 发现、理解、设计、计划、审计、调研 |
| `_MCP_AUDIT` | 只读 + `evidence_check` | 发布、报告 |

每个 `WorkflowSpec` 自带 `mcp_tools`；`mcp_tools_allow(id)` 返回该流程允许的工具集。

### 3.2 阶段（`BASE_PHASES`）

每个阶段都有：`id / goal / agent / skills / tools / exit_criteria / parallel_group`。

| 阶段 | 默认 agent | 工具档 | 完成条件（示例） |
|---|---|---|---|
| discover | product-owner | READ | 结果与验收标准已写明 |
| understand | architect | READ | 目标复述 / 意图证据 / 运行模型 |
| design | architect | READ | 决策、备选与被否原因 |
| plan | project-manager | READ | 计划已落盘且有 id |
| implement | implementer | FULL | 范围明确 / 有测试 / 无密钥 |
| verify | qa-engineer | FULL | 0 未收敛 FAILED / 0 残留容器 / 有命令记录 |
| audit | security-reviewer | READ | 发现 + 证据（含严重度） |
| research | product-owner | READ | 事实与推断分开记录 |
| release | release-manager | AUDIT | 版本 / 标签 / 回滚 / 未验证项 |
| report | delivery-lead | AUDIT | 证据、未验证、风险、下一步 |

- **按流程组装**（`WORKFLOW_PHASES`）：如 `feature-delivery = understand→discover→design→implement→verify→report`；`design-review = audit→report`。
- **按流程覆写**（`PHASE_OVERRIDES`，**追加式**）：如 `ui-delivery.implement` 换成 `web-designer` 并追加 `web-experience-design`；`compliance-review.audit` 追加法务/隐私技能。
- **是否可改代码**：`implement_allowed(id)` = 该流程是否含 `implement` 阶段。**没有 implement 的流程，想改代码必须显式切换流程**。

> 优势点：**同一套 10 个阶段复用出 12 条流程**；「审查类只读」由结构保证，不靠自觉。

## 4. 执行期：阶段、委派、证据

依据：`mcp/server.py`

- `workflow_get {name, phase}`：返回某阶段的 `goal / agent / skills / mcp_tools_allow / exit_criteria`。
- `delegate_subtask {phase}`：把子任务按阶段包装，自动带上该阶段的 `exit_criteria`；支持 `model_tier`、`idempotency_key`。
- `evidence_check`：**真的执行** `scripts/validate_assets.py`，不是让模型自评。
- `skill_get` / `capabilities` / `skill_search`：渐进披露，按需取一个技能。

> 优势点：**「完成」有可执行的判定，不靠语言承诺**。

## 5. 运行中改计划（steering）

依据：`mcp/server.py do_steer_task`、`mcp/intent_steer.py`

- 支持操作：`add / reorder / reprioritize / scope_change / abort`。
- 解释成结构化 op，作用在**当前活跃流程**上；不需要重开流程。
- 与 `delegate_subtask` 配合：互不依赖的部分拆并行，带阶段 `exit_criteria` 回收。

> 优势点：**骨架固定、计划可调**——不会因为流程而死板。

## 6. 配套能力（同样有代码支撑）

- **渐进披露**：`capabilities → skill_search → skill_get`（`server.py`）。
- **上下文压缩**：`compress_context`（skill `context-compression`，纯本地）。
- **记忆**：`memory_recall` / `memory_save`（`mcp/memory_ops.py`；`WAWOO_MEMORY_READONLY` 控制写）。
- **外发护栏**：`guard_content` / `mask_pii` / `redact_infra`（确定性，无模型）。
- **预算**：`validate_assets.py` 对 `SKILL.md` 有 4KB 预算告警。

## 7. 为什么这是优势（对外可以这样讲）

| 常见做法 | 这套件 |
|---|---|
| 把技能列表一股脑塞给模型 | router 选流程，再按流程取技能 |
| 「请只读，不要改代码」 | 会话门禁 + 只读工具档，写工具根本不可用 |
| 「记得写测试/留证据」 | 阶段 `exit_criteria` + `evidence_check` 实跑 |
| 计划定死后无法调整 | `steer_task` 运行中改计划 |
| 审稿/评审靠模型自评 | 阶段化 + 证据；审查类无 implement |

## 8. 可写的文章选题

1. **「一个 router 管住整个流程」**：从 4 级选择到会话门禁。
2. **「只读不是叮嘱，是没给你写工具」**：工具白名单与审查类设计。
3. **「10 个阶段复用出 12 条流程」**：阶段目录 + 覆写。
4. **「完成要有证据」**：exit_criteria + evidence_check。
5. **「计划可以变」**：steer_task / delegate_subtask。

## 9. 代码索引

| 关注点 | 文件 |
|---|---|
| 路由选择 | `mcp/intent_interpreter.py` · `intent_commands.py` · `intent_lexical.py` · `intent_upstream.py` |
| 会话门禁 | `mcp/intent_session.py` |
| 流程/阶段/工具档 | `mcp/intent_catalog.py` |
| MCP 工具 | `mcp/server.py` |
| 改计划 / 委派 | `mcp/intent_steer.py` · `mcp/intent_delegation.py` |
| 记忆 | `mcp/memory_ops.py` |
| 目录生成 | `scripts/gen_capabilities.py` |
