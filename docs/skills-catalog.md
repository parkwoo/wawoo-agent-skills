---
title: wawoo-skills 技能与工作流目录（98 Skills / 12 Workflows）— AI 编程工程实践库
description: 开源 Agent Skills 与 MCP 工作流索引：Cursor、Claude Code 等客户端可用的工程交付、审查、安全与 UI 能力。
hide:
  - title
  - navigation
---

<div class="kit-catalog-root" markdown="1">

<div class="kit-catalog-hero" markdown="0">

<p class="kit-catalog-title">技能与工作流目录</p>
<p class="kit-catalog-lead">开源 AI 编程工作流引擎：把零散 Prompt 收成可验收的步骤，而不是一屏说明书。</p>
<p class="kit-catalog-usage">在已连接 MCP 的客户端里，用自然语言触发 <code>workflow_get</code> 选工作流，正文点到哪个再 <code>skill_get</code>。</p>
<p class="kit-catalog-example">例：小改动说「走 /delivery-lite」；完整功能说「走 /feature-delivery」。配置见 <a href="/docs/usage/">使用说明</a> · <a href="/download/">免费下载</a>。</p>
<p class="kit-catalog-hero-counts">与 <a href="https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md" target="_blank" rel="noopener noreferrer">GitHub CAPABILITIES</a> 同步 · 98 个 Skill · 21 个 Agent · 12 条 Workflow</p>
<div class="kit-catalog-hero-meta">
<div class="kit-doc-langs">
<a href="/en/docs/skills-catalog/">English</a>
  <span aria-hidden="true">·</span>
  <a href="/ja/docs/skills-catalog/">日本語</a>
  <span aria-hidden="true">·</span>
  <a href="/ko/docs/skills-catalog/">한국어</a>
  <span aria-hidden="true">·</span>
  <strong>简体中文</strong>
</div>
</div>
</div>

<h2 class="kit-catalog-tier" id="cat-workflows">工作流（12）</h2>

<p class="kit-catalog-tier-lead">以 <code>/</code> 开头的入口命令；在客户端用自然语言触发 <code>workflow_get</code>。</p>

<div class="kit-catalog-table" markdown="1">


| 名称 | 说明（简体中文） |
| --- | --- |
| [`/compliance-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/compliance-review.md) | 法务/隐私/安全门禁工作流（compliance-legal → privacy-review → security-review → release-readiness）。 |
| [`/delivery-lite`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/delivery-lite.md) | 轻量交付工作流：SSOT 计划文件状态机、最小仪式（L0–L1），单功能默认入口。 |
| [`/design-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/design-review.md) | 会写代码的设计师：先做视觉审计，再以原子提交配合前后截图修复已上线 UI。 |
| [`/feature-delivery`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/feature-delivery.md) | 经发现、设计、实现、测试、评审与审批门禁交付完整功能。 |
| [`/incident-response`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/incident-response.md) | 以证据调查并安全处置事故或紧急回归，并安排后续跟进。 |
| [`/release-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/release-review.md) | 准备发布评审包：法务/合规、隐私、版本、安全、测试、产物、远程与回滚证据。 |
| [`/research`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/research.md) | 对照高可信一手资料调查问题，并将结论写入仓库内 Markdown 文件。 |
| [`/self-improve`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/self-improve.md) | 自我改进工作流（retro → pdca-cycle → self-review → plan-md）。 |
| [`/self-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/self-review.md) | 自我纠错工作流（code-review → code-skeptic → diagnosing-bugs/tdd → 修复 → 验证）。 |
| [`/sprint-plan`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/sprint-plan.md) | L2 冲刺规划（wayfinder → to-tickets → 优先级/估算/容量 → plan-md）。 |
| [`/status-report`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/status-report.md) | 进度/状态报告（ACTIVE 或 triage/to-tickets → 进度/风险 → plan-md）。 |
| [`/ui-delivery`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/commands/ui-delivery.md) | 设计、实现并审计 Web UI 变更，覆盖响应式与可访问性状态。 |

</div>


<h2 class="kit-catalog-tier" id="cat-agents">Agent 角色（21）</h2>

<p class="kit-catalog-tier-lead">工作流或 MCP 指定的执行视角；通常不必逐个打开。</p>

<div class="kit-catalog-table" markdown="1">


| 名称 | 说明（简体中文） |
| --- | --- |
| [`accessibility-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/accessibility-reviewer.md) | 对用户流程、语义结构、键盘操作与响应式 UI 做只读可访问性评审。 |
| [`architect`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/architect.md) | 评估架构备选方案、接口、依赖、迁移风险并维护决策记录。 |
| [`Code Reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/code-reviewer.md) | 资深软件工程师角色，进行透彻的代码评审。 |
| [`Code Simplifier`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/code-simplifier.md) | 专注简化/重构代码库中的功能实现。 |
| [`Code Skeptic`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/code-skeptic.md) | 以极度挑剔视角批评你的代码与假设。 |
| [`compliance-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/compliance-reviewer.md) | 变更或发布的法务/合规/隐私评审门禁；收集证据与清单，最终法务判断需人工。 |
| [`Data`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/data.md) | 以 notebook 为先：按请求追加并执行单元格完成数据分析。 |
| [`delivery-lead`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/delivery-lead.md) | 从范围到评审协调基于证据的交付，不绕过审批门禁。 |
| [`docs-localization-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/docs-localization-reviewer.md) | 维护事实准确的技术文档及等价的本地化内容。 |
| [`Documentation Specialist`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/docs-specialist.md) | 专注撰写文档、Markdown 及其他文本类交付物。 |
| [`Frontend Specialist`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/frontend-specialist.md) | React、TypeScript 与现代 CSS 方向的前端专家 agent。 |
| [`implementer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/implementer.md) | 按项目约定实现有边界的软件变更，附聚焦测试与证据化报告。 |
| [`performance-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/performance-reviewer.md) | 评审性能瓶颈、测量设计、预算与回归防护策略。 |
| [`product-owner`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/product-owner.md) | 澄清用户结果、优先级、范围与验收标准，不擅自做业务决策。 |
| [`project-manager`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/project-manager.md) | 敏捷项目管理：冲刺规划、状态报告、风险跟踪与交付协调。 |
| [`qa-engineer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/qa-engineer.md) | 设计测试策略、复现缺陷、评估验证证据并识别覆盖缺口。 |
| [`release-manager`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/release-manager.md) | 准备发布：版本、法务、产物、兼容性、回滚与远程验证检查。 |
| [`security-reviewer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/security-reviewer.md) | 对代码、配置、依赖与交付变更做只读安全评审。 |
| [`sre-operator`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/sre-operator.md) | 以谨慎的先读方式分析日志、监控、事故与云环境运维问题。 |
| [`wawoo-auto`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/wawoo-auto.md) | 默认入口 agent：非平凡请求先经 MCP 路由到 wawoo workflow，再执行该工作流。 |
| [`web-designer`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/agents/web-designer.md) | 设计并实现可访问的响应式 Web 界面，交接前审计实际渲染行为。 |

</div>


<h2 class="kit-catalog-tier" id="cat-skills">Skill 技能（98）</h2>

<p class="kit-catalog-tier-lead">工作流正文点名后再 <code>skill_get</code>；按名称字母序。</p>

<div class="kit-catalog-table" markdown="1">


| 名称 | 说明（简体中文） |
| --- | --- |
| [`accessibility-audit`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/accessibility-audit/SKILL.md) | 审计并改进 Web 可访问性，涵盖语义结构、键盘操作、表单、焦点、对比度、动效与辅助技术兼容性。 |
| [`api-contract-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/api-contract-design/SKILL.md) | 设计或评审 HTTP、RPC、事件及内部 API 契约，明确输入输出、错误、认证与向后兼容。 |
| [`architecture-decision`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/architecture-decision/SKILL.md) | 评估架构选型、依赖、接口、约束与权衡，并产出简洁的架构决策记录（ADR）。 |
| [`ask-matt`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/ask-matt/SKILL.md) | 根据当前情境推荐合适的 skill 或工作流，充当本仓库 skill 的路由器。 |
| [`benchmark-checklist`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/benchmark-checklist/SKILL.md) | 在对外汇报性能数据前，核查基准方法、限流、误差、可重复性与场景相关性。 |
| [`blast-radius`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/blast-radius/SKILL.md) | 在发布前评估变更的潜在爆炸半径，并用可验证证据说明关键安全前提成立。 |
| [`change-readiness`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/change-readiness/SKILL.md) | 在请求人工或外部审计前，对非平凡软件变更做有证据的交接前审查。 |
| [`changelog`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/changelog/SKILL.md) | 从 git 历史（Conventional Commits）生成并维护面向用户的 CHANGELOG/发布说明，并保持版本与 tag 一致。 |
| [`code-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/code-review/SKILL.md) | 自固定基准点审阅 diff，从规范符合度与正确性/风险两条轴线给出可执行反馈。 |
| [`codebase-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/codebase-design/SKILL.md) | 设计深层模块的共享词汇表；用于设计/改进模块接口、寻找可深化抽象的时机。 |
| [`compliance-legal`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/compliance-legal/SKILL.md) | 审查 OSS 许可义务（MIT/Apache-2.0 署名、NOTICE）、SBOM 及产品/服务法务清单（条款、隐私等）。 |
| [`content-guardrail`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/content-guardrail/SKILL.md) | 确定性策略即数据的内容闸门（无模型、无网络），对文本做违禁词、正则与内置密钥检测。 |
| [`context-compression`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/context-compression/SKILL.md) | 用纯 Python 确定性压缩多轮对话上下文（无 LLM、无网络），去陈旧轮次并去重。 |
| [`create-verification-skill`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/create-verification-skill/SKILL.md) | 生成项目本地 verification skill，以用户视角驱动任意语言/框架/平台的应用验证。 |
| [`data-egress-guard`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/data-egress-guard/SKILL.md) | 在文本发往外部 LLM/API 前确定性脱敏 PII 与密钥（无模型、无网络），用占位符替换命中片段。 |
| [`database-change-safety`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/database-change-safety/SKILL.md) | 规划、实施并评审 schema 变更、迁移、回填与清理，兼顾完整性、可用性与可观测性。 |
| [`dependency-upgrade`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/dependency-upgrade/SKILL.md) | 安全评估、应用并验证依赖、运行时、容器镜像或工具链升级，关注兼容性与安全风险。 |
| [`deployment`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/deployment/SKILL.md) | 规划、执行并验证部署/发布（Docker Compose、镜像 tag、环境、迁移、健康检查、回滚）。 |
| [`design-brief`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/design-brief/SKILL.md) | 将 I-Lang 协议格式的结构化设计简报解析为可执行的设计规格，消除模糊需求。 |
| [`design-md`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/design-md/SKILL.md) | 创建并维护 DESIGN.md（Google Stitch 格式的纯文本设计系统文档），供设计与编码 agent 读取。 |
| [`design-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/design-review/SKILL.md) | 会写代码的设计师：先做视觉审计，再以原子提交配合前后截图修复已上线 UI。 |
| [`diagnosing-bugs`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/diagnosing-bugs/SKILL.md) | 针对疑难缺陷与性能回退的诊断闭环；适用于用户说 diagnose/debug 或报告间歇性问题时。 |
| [`documentation-localization`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/documentation-localization/SKILL.md) | 编写、审阅并同步技术文档与本地化内容，确保事实准确、指引可用、链接有效。 |
| [`domain-modeling`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/domain-modeling/SKILL.md) | 构建并打磨项目领域模型；讨论术语、编写 GLOSSARY.md 或记录领域决策时使用。 |
| [`engineering-quality`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/engineering-quality/SKILL.md) | 在明确范围内规划并实现软件变更，强调证据化验证、安全迁移与回滚就绪。 |
| [`fal-gen`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/fal-gen/SKILL.md) | 用 fal.ai 批量生成设计图（头像/插画/背景/纹理）；任务需要生成或占位视觉素材时使用。 |
| [`figure-it-out`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/figure-it-out/SKILL.md) | 当没有更窄流程可用时，设计可审计的大型迁移/多部件变更行动手册。 |
| [`frontend-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/frontend-design/SKILL.md) | 打造有鲜明视觉方向的生产级前端界面，兼顾字体、版式、色彩与微交互细节。 |
| [`frontend-guides-hub`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/frontend-guides-hub/SKILL.md) | Frontend/UI skill 分流入口，为 /ui-delivery 按阶段路由到既有 skill（避免 110 个平铺）。 |
| [`grill-with-docs`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/grill-with-docs/SKILL.md) | 通过高强度问答打磨计划或设计，并同步产出 ADR、术语表等文档沉淀。 |
| [`grilling`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/grilling/SKILL.md) | 对用户计划、决策或想法进行追问式压力测试，检验假设与风险。 |
| [`handoff`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/handoff/SKILL.md) | 将当前会话压缩为交接文档，供其他 agent 无缝续作。 |
| [`how`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/how/SKILL.md) | 回答「X 如何工作」、变更前代码走读，以及模块归属/分层/放置类问题。 |
| [`imagegen-frontend-mobile`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/imagegen-frontend-mobile/SKILL.md) | 为移动应用提供高质量图像概念与提示词，覆盖 iOS/Android 界面与流程的视觉方向。 |
| [`implement`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/implement/SKILL.md) | 依据规格或一组工单实现具体开发任务。 |
| [`implement-spec`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/implement-spec/SKILL.md) | 将 /to-spec 与 /to-tickets 的产出落地为代码实现。 |
| [`in-your-own-words`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/in-your-own-words/SKILL.md) | 用你自己的话复述用户目标与要解决的问题；用于 /in-your-own-words 对齐理解。 |
| [`incident-debugging`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/incident-debugging/SKILL.md) | 通过复现、取证、隔离、缓解与验证，诊断软件事故或高影响缺陷。 |
| [`language-policy`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/language-policy/SKILL.md) | 用三层语言策略（代码英文、工程记录、说明文档双语等）决定并执行书写语言。 |
| [`legacy-web-scan`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/legacy-web-scan/SKILL.md) | Legacy Web 模式扫掠：结合 MWG legacy-scan 与社内规则，将现代化候选项写入 plan-md。 |
| [`maintain-verification-skill`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/maintain-verification-skill/SKILL.md) | 周期性维护项目 verification skill 与特性地图：并行读源码、实机验证，保持映射诚实。 |
| [`memory`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/memory/SKILL.md) | 跨会话持久化并召回项目知识（决策、约束、坑点、常见修复）；开工前先 recall。 |
| [`modern-web-guidance-bridge`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/modern-web-guidance-bridge/SKILL.md) | 通过 npx 按需调用 Modern Web Guidance（search/retrieve/legacy-scan）；外部 OSS 桥，勿 fork 进 kit。 |
| [`openrouter-gen`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/openrouter-gen/SKILL.md) | 经 OpenRouter 图像模型（默认 google/gemini-2.5-flash-image）批量生成设计图素材。 |
| [`pdca-cycle`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/pdca-cycle/SKILL.md) | 对产品、工程、质量或流程改进运行轻量 PDCA（Plan-Do-Check-Act）闭环。 |
| [`performance-audit`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/performance-audit/SKILL.md) | 用代表性负载测量并改进应用/Web 性能，基于瓶颈证据并设置回归防护。 |
| [`plan-md`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/plan-md/SKILL.md) | 将规划交付物（修复方案、实施计划、设计方向、评审回复）固定写入 Markdown 文件。 |
| [`pr`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/pr/SKILL.md) | 撰写 Pull Request 正文时使用。 |
| [`principle-attack-the-premise`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-attack-the-premise/SKILL.md) | 当多个共享同一前提的修复在同一门禁失败时，先写下前提并直接验证再改代码。 |
| [`principle-boundary-discipline`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-boundary-discipline/SKILL.md) | 在接线校验、错误处理或框架适配时，把守卫集中在系统边界（CLI、配置、网络等）。 |
| [`principle-build-the-lever`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-build-the-lever/SKILL.md) | 面对非平凡工作先造杠杆：编辑、迁移、分析、检查都先建工具或证明脚本再做。 |
| [`principle-encode-lessons-in-structure`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-encode-lessons-in-structure/SKILL.md) | 当你第二次写同一条指示或反复纠正时，把规则编码进结构（skill、lint、类型）而非提示词。 |
| [`principle-exhaust-the-design-space`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-exhaust-the-design-space/SKILL.md) | 面对代码库无先例的 UI 或架构决策时，先做 2–3 个竞争原型再收敛选型。 |
| [`principle-experience-first`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-experience-first/SKILL.md) | 在产品、UX 或范围权衡时优先用户体感，而非实现便利；少做妥协版功能。 |
| [`principle-explain-the-number`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-explain-the-number/SKILL.md) | 在测量、汇报或依据数值行动前，说清数字含义、方法与可信边界。 |
| [`principle-fix-root-causes`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-fix-root-causes/SKILL.md) | 调试时把症状追到系统首次出错处并在那里修复；守卫只在无法根除根因时才算修复。 |
| [`principle-foundational-thinking`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-foundational-thinking/SKILL.md) | 写逻辑前先做基础思考：核心类型与数据结构、脚手架 vs 功能顺序、并发假设等。 |
| [`principle-guard-the-context-window`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-guard-the-context-window/SKILL.md) | 上下文将满时：大输出、长文件、重复读取、扇出规划—— bulk 下沉子 agent，主会话留摘要。 |
| [`principle-laziness-protocol`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-laziness-protocol/SKILL.md) | 重构或想加抽象层时偏向删减；评估 diff 规模，避免无必要的信号穿层。 |
| [`principle-make-operations-idempotent`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-make-operations-idempotent/SKILL.md) | 设计会在崩溃/重启/重试间运行的命令或生命周期步骤时，收敛到幂等语义。 |
| [`principle-migrate-callers-then-delete-legacy-apis`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | 引入新内部 API 且旧调用方仍在时，同一波次迁移调用方并删除旧 API。 |
| [`principle-minimize-reader-load`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-minimize-reader-load/SKILL.md) | 审阅难追踪代码时，统计从问题到答案的层级与读者需隐藏的隐式状态。 |
| [`principle-model-the-domain`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-model-the-domain/SKILL.md) | 编写有状态逻辑，或分支繁多、跨文件重复同一形状假设时，先建模领域状态。 |
| [`principle-never-block-on-the-human`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-never-block-on-the-human/SKILL.md) | 对可逆工作别想「我该不该做 X」而阻塞；先做完再汇报。 |
| [`principle-outcome-oriented-execution`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-outcome-oriented-execution/SKILL.md) | 分阶段重写/迁移时以目标架构收敛，不为过渡态长期保留兼容层。 |
| [`principle-prove-it-works`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-prove-it-works/SKILL.md) | 宣称完成前用真实产物验证（跑功能、读实际值、看截图），而非仅看 diff。 |
| [`principle-redesign-from-first-principles`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-redesign-from-first-principles/SKILL.md) | 将新需求融入既有设计时，从第一性原理重审边界而非局部打补丁。 |
| [`principle-separate-before-serializing-shared-state`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-separate-before-serializing-shared-state/SKILL.md) | 并发可能写同一文件/分支/键/状态对象时，先消除共享再谈序列化。 |
| [`principle-sequence-verifiable-units`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-sequence-verifiable-units/SKILL.md) | 多步工作或提交/PR 堆叠时，切成可独立验证的小单元逐步交付。 |
| [`principle-subtract-before-you-add`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-subtract-before-you-add/SKILL.md) | 追加、重构或重写前先删死代码、冗余校验与桩引用，再加新逻辑。 |
| [`principle-test-behavior-not-implementation`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-test-behavior-not-implementation/SKILL.md) | 写/改/保留测试时断言用户可观察行为，使行为变坏时测试必失败。 |
| [`principle-type-system-discipline`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/principle-type-system-discipline/SKILL.md) | 设计类型或静态语言代码时，用类型让非法状态不可表示。 |
| [`privacy-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/privacy-review/SKILL.md) | 审查个人数据（PII）流、最小化、保留、脱敏、日志与跨境处理是否符合隐私要求。 |
| [`product-discovery`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/product-discovery/SKILL.md) | 将模糊的产品/功能请求收敛为问题陈述、用户结果、验收标准、优先级与风险。 |
| [`prototype`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/prototype/SKILL.md) | 搭建可丢弃原型以回答设计问题；用于快速验证状态模型或逻辑是否成立。 |
| [`publication-boundary`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/publication-boundary/SKILL.md) | 防止内部开发物料进入开源仓库公开树；新增文档/脚本或审计公开边界时使用。 |
| [`recall`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/recall/SKILL.md) | 从自身对话历史、现场状态与共享记录（用户报告、既往修复）重建近期工作上下文。 |
| [`reference-design-contract`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/reference-design-contract/SKILL.md) | 将模糊品味、截图、URL 或「做成这种感觉」的参考转为可落地的 DESIGN.md 与实现契约。 |
| [`reflect`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/reflect/SKILL.md) | 并行拉起三个评审子 agent 扫当前 transcript，提炼教训并路由到具体文件修改。 |
| [`release-readiness`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/release-readiness/SKILL.md) | 为软件发布准备并审阅版本、法务文件、CHANGELOG、tag、发布说明与部署检查。 |
| [`research`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/research/SKILL.md) | 对照高可信一手资料调查问题，并将结论写入仓库内 Markdown 文件。 |
| [`retro`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/retro/SKILL.md) | 对一次编码会话进行回顾（retro）。 |
| [`security-review`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/security-review/SKILL.md) | 对应用代码、配置、依赖与交付变更做先读后写的安全评审。 |
| [`setup-matt-pocock-skills`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/setup-matt-pocock-skills/SKILL.md) | 为工程 skill 套件配置仓库：工单系统、分诊标签词汇表与领域文档布局。 |
| [`sharpen`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/sharpen/SKILL.md) | 把任务做得更深而非更大，并重写提示词；用于 /sharpen。 |
| [`show-me-your-work`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/show-me-your-work/SKILL.md) | 为长跑或未值守工作保留可审阅决策轨迹：TSV 日志逐行列出决策、理由与证据。 |
| [`swarm`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/swarm/SKILL.md) | 扇出 N 个并行 worker、汇总 drain，返回一份报告；用于 /swarm 或并行覆盖面任务。 |
| [`tdd`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/tdd/SKILL.md) | 测试驱动开发；用户要测试先行、提 red-green-refactor 或先写失败测试时使用。 |
| [`teach`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/teach/SKILL.md) | 在本工作区内向用户教授新 skill 或概念。 |
| [`test-engineering`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/test-engineering/SKILL.md) | 设计、实现、诊断并评审软件测试，强调有证据的单元/集成/E2E 覆盖。 |
| [`to-spec`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/to-spec/SKILL.md) | 将当前对话合成为规格并发布到项目工单系统，无需访谈式澄清。 ⚠️ |
| [`to-tickets`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/to-tickets/SKILL.md) | 把计划、规格或当前对话拆成 tracer-bullet 工单，声明阻塞边并发布。 ⚠️ |
| [`triage`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/triage/SKILL.md) | 按分诊状态机推进 issue 与外部 PR：分类、核验、必要时 grilling，并写 agent 就绪说明。 ⚠️ |
| [`wayfinder`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/wayfinder/SKILL.md) | 将超出一个 agent 会话体量的大块工作规划为工单上的决策票地图，并编排依赖。 |
| [`web-design-guidelines`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/web-design-guidelines/SKILL.md) | 按 Vercel Web Interface Guidelines 审阅 UI 代码，覆盖版式、字体、色彩、动效等。 |
| [`web-experience-design`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/web-experience-design/SKILL.md) | 设计、实现、审计并交接 Web 界面，附用户任务、视觉层级、响应式与可访问性证据。 |
| [`why`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/why/SKILL.md) | 回答「为何如此设计」、选型理由、回归、复盘或数据阈值背后的 why。 |
| [`writing-for-agents`](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/skills/writing-for-agents/SKILL.md) | 为 agent 编写文档；创建/编辑 skill 或修改 AGENTS.md、CLAUDE.md 时使用。 |

</div>


<p class="kit-catalog-subhead"><strong>常见任务 → 工作流</strong></p>

<div class="kit-catalog-quickref" markdown="1">

| 场景 | 工作流 | 可复制的一句 |
| --- | --- | --- |
| 日常小需求 / 单功能 | `/delivery-lite` | <code class="kit-catalog-copy" data-kit-copy-cmd="走 /delivery-lite，用 ACTIVE 计划表跟踪，证据过关再收工">走 /delivery-lite，用 ACTIVE 计划表跟踪，证据过关再收工</code> |
| 完整功能 / 多阶段 | `/feature-delivery` | <code class="kit-catalog-copy" data-kit-copy-cmd="走 /feature-delivery，从发现到评审全链路">走 /feature-delivery，从发现到评审全链路</code> |
| 线上故障 / 回归 | `/incident-response` | <code class="kit-catalog-copy" data-kit-copy-cmd="走 /incident-response，先复现和隔离再 permanent fix">走 /incident-response，先复现和隔离再 permanent fix</code> |
| 改 Web UI / 无障碍 | `/ui-delivery` | <code class="kit-catalog-copy" data-kit-copy-cmd="走 /ui-delivery，设计实现和 a11y 证据一起交">走 /ui-delivery，设计实现和 a11y 证据一起交</code> |

</div>

<details class="kit-catalog-tier-details">
<summary>三类能力怎么区分（展开对照表）</summary>

<div class="kit-catalog-tier-guide" markdown="1">

| 类型 | 是什么 | 何时用 |
| --- | --- | --- |
| **Workflow** | 固定步骤的流程入口（<code>/delivery-lite</code> 等） | 先对齐「我在做哪类事」 |
| **Agent** | 角色视角（审代码、做 UI…） | 一般由工作流或 MCP 指定 |
| **Skill** | 单份 SKILL.md 操作说明 | 正文点名后再 <code>skill_get</code> |

</div>

</details>

<p class="kit-catalog-subhead"><strong>精选亮点</strong></p>

<div class="kit-catalog-highlights" markdown="1">

<article class="kit-catalog-highlight"><strong>工作流状态机</strong><p>用 <code>/delivery-lite</code>、<code>/feature-delivery</code> 等固定流程串联 skill，完成标准由工具校验，不是靠模型自评。</p></article>

<article class="kit-catalog-highlight"><strong>context-compression</strong><p>纯 Python、无 LLM 的上下文压缩，长会话前先瘦身，省 Token。</p></article>

<article class="kit-catalog-highlight"><strong>data-egress-guard</strong><p>外发 API 前确定性脱敏 PII/密钥，守门类 skill，不依赖模型自觉。</p></article>

<article class="kit-catalog-highlight"><strong>code-review + self-review</strong><p>合入前双轴评审 + 挑刺视角，证据导向，适合严肃改码场景。</p></article>

</div>

<p class="kit-catalog-footer">
生成于 2026-11-20T14:08:23Z · [CAPABILITIES 正本](https://github.com/parkwoo/wawoo-agent-skills/blob/master/.kilo/CAPABILITIES.md)
 [使用说明](usage.md) · [免费下载](/download/) · [更新日志](/changelog/) · [GitHub](https://github.com/parkwoo/wawoo-agent-skills)
</p>

</div>
