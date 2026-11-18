# 方法论来源与工作流对应（文章素材）

> **内部资料，不公开。** 用于撰写对外技术文章。README 只保留一句概述与（发布后的）文章链接。

这套工具不是凭空造的。它把公开的工程方法论挑出可执行的部分，编排成流程——**不是照搬，而是取用**：

| 来源 | 取用的思想 | 用在哪里 |
|---|---|---|
| Skills For Real Engineers（Matt Pocock，MIT） | 先规格、再拆票、测试先行、分诊、追问式打磨 | `/feature-delivery`、`/research`、`/self-review` 的步骤设计 |
| pstack（Lauren Tan / Poteto，MIT） | 修根因、先减后加、可验证小步、爆炸半径、先量测 | `principle-*` 与各流程的检查点 |
| OpenDesign / Anthropic / Google Labs / Vercel（Apache-2.0） | 设计系统、无障碍、前端规范 | `/ui-delivery`、`/design-review` |
| Corey Haines（marketingskills，MIT） | 营销心理学、钩子与框架 | 营销 / 文案流程 |
| 本仓库（wawoo） | 把以上编排成流程，加上路由、闸门与记忆 | 16 条工作流、MCP 服务 |

> 收口：它不是又一个 prompt 合集，而是**把顶尖工程师的做法固化成可执行的流程**。

## 可写的选题（建议）

- **「技能写了却不用」**：为什么问题不在模型，而在「没人规定它必须用」。
- **从个人方法论到团队流程**：Matt Pocock / pstack 的思想，如何落成 16 条工作流。
- **固定骨架、可变计划**：`steer_task`（追加 / 重排 / 调优先级 / 改范围 / 中止）如何避免「流程把人绑死」。
- **2–4KB 预算**：上下文成本是怎么被钉死的（入口小、细节进 `references/`、`validate_assets` 告警）。
- **证据闸门**：为什么「只凭推断说完成」必须被禁止。

## 发布后

对外文章发布后，在 `README.zh-CN.md` 的「方法论从哪来」补链接（当前为占位）。
