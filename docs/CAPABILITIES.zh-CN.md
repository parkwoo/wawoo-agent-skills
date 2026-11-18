# 能力一览（wawoo-skills）

共 **98 个技能、21 个角色、12 条工作流**。本页按**大类 / 小类**列出全部条目；机器可读清单见 `.kilo/CAPABILITIES.md`（自动生成，勿手改）。

返回：[README](../README.zh-CN.md) · [使用说明](USAGE.zh-CN.md)

## 分类与治理（怎么「科学管理」）

**三类东西，三种职责：**

| 类别 | 是什么 | 怎么组织 | 谁负责 |
|---|---|---|---|
| 技能 skills | 可复用的能力单元（`SKILL.md`） | 按「大类 / 小类」分组（见下） | 维护者 |
| 角色 agents | 固定视角（评审者、实现者…） | 按职能分组；不独立成产品 | 维护者 |
| 工作流 workflows | 有阶段与完成条件的流程 | 按场景分组；入口是 `/name` | 交付负责人 |

**质量闸门**（新增或修改时，跑 `python3 scripts/validate_assets.py`）：

- `name` 必须等于目录名；引用（`agent:`、skill 链接）不得断。
- 入口 `SKILL.md` **≤ 2–4KB**（超 4KB 会 WARN，应拆到 `references/`）。
- `description` 一行、**约 160 字符**（过长会被截断）。
- 第三方来源必须登记到 `.kilo/skills/ATTRIBUTION.md` 与 `LICENSES/`；**许可未验证的资产不进公开仓**。
- 外部前提（如 issue tracker）登记到 `scripts/readiness.json`。

**生命周期：**

1. 提案（`plan-md`）→ 2. 起草 `SKILL.md`（一文一职、渐进披露）→ 3. 校验（`validate_assets`）→ 4. 归因登记 → 5. `gen_capabilities.py` 重建目录 → 6. 发版（SemVer：`VERSION` + `CHANGELOG`）。
- 废弃：先迁移调用方，再删除；在 `CHANGELOG` 留记录。

**预算原则**：技能入口要小、细节进 `references/`；运行时是「先给目录、再取一个」，所以分类要**按用途可检索**，而不是按实现细节。

## 技能 skills（98）

| 大类 | 小类 | 名称 | 说明 |
|---|---|---|---|
| 交付与计划 | 需求 | `product-discovery` | 把模糊需求变成范围、验收标准与优先级 |
| 交付与计划 | 需求 | `in-your-own-words` | 复述你的目标与问题，先对齐再动手 |
| 交付与计划 | 规格 | `to-spec` | 把当前对话整理成规格并发布到 issue tracker |
| 交付与计划 | 规格 | `to-tickets` | 拆成带依赖关系的小票（tracer-bullet） |
| 交付与计划 | 实现 | `implement` | 按规格 / 票据实现 |
| 交付与计划 | 实现 | `implement-spec` | 实现 `to-spec` / `to-tickets` 的结果 |
| 交付与计划 | 计划 | `plan-md` | 任何计划都落成 Markdown 文件 |
| 交付与计划 | 计划 | `wayfinder` | 把超大工作拆成决策票据地图 |
| 交付与计划 | 计划 | `grilling` | 用追问压力测试你的方案 |
| 交付与计划 | 计划 | `grill-with-docs` | 追问的同时产出 ADR / 术语表 |
| 交付与计划 | 计划 | `figure-it-out` | 没有现成流程时，造一份可审计的作战手册 |
| 交付与计划 | 计划 | `sharpen` | 让任务更深而非更大，重写提示 |
| 交付与计划 | 分诊 | `triage` | 把 issue / 外部 PR 推过分诊状态机 |
| 调试与测试 | 调试 | `diagnosing-bugs` | 难缠 bug / 性能回归的诊断循环 |
| 调试与测试 | 测试 | `tdd` | 测试先行（红—绿—重构） |
| 调试与测试 | 测试 | `test-engineering` | 设计 / 实现 / 诊断测试，强调证据覆盖 |
| 调试与测试 | 验证 | `create-verification-skill` | 生成「像用户一样驱动应用」的验证技能 |
| 调试与测试 | 验证 | `maintain-verification-skill` | 定期校准验证技能与功能图 |
| 评审与质量 | 评审 | `code-review` | 从「标准」「规格」两轴评审变更 |
| 评审与质量 | 评审 | `change-readiness` | 交付前的证据化自查 |
| 评审与质量 | 质量 | `engineering-quality` | 明确范围 + 证据验证 + 可回滚 |
| 评审与质量 | 协作 | `pr` | 写 PR 描述 |
| 评审与质量 | 复盘 | `retro` | 对一次编码会话做回顾 |
| 评审与质量 | 风险 | `blast-radius` | 找出改动在别处可能弄坏什么 |
| 架构与代码设计 | 架构 | `architecture-decision` | 评估架构取舍并产出决策记录 |
| 架构与代码设计 | 架构 | `codebase-design` | 设计「深模块」接口的通用词汇 |
| 架构与代码设计 | 接口 | `api-contract-design` | 设计 / 评审 API 契约 |
| 架构与代码设计 | 领域 | `domain-modeling` | 建立并打磨领域模型 / 术语表 |
| 架构与代码设计 | 数据 | `database-change-safety` | 结构变更 / 迁移 / 回填的安全网 |
| 架构与代码设计 | 依赖 | `dependency-upgrade` | 安全地升级依赖 / 运行时 / 工具链 |
| 架构与代码设计 | 原型 | `prototype` | 造丢弃式原型来回答设计问题 |
| 安全与合规 | 安全 | `security-review` | 只读安全评审（代码 / 配置 / 依赖） |
| 安全与合规 | 隐私 | `privacy-review` | 个人数据流 / 最小化 / 留存评审 |
| 安全与合规 | 法务 | `compliance-legal` | OSS 许可义务 / SBOM / 法务清单 |
| 安全与合规 | 发布 | `release-readiness` | 版本 / 许可 / 变更日志 / 回滚检查 |
| 安全与合规 | 外发 | `content-guardrail` | 纯本地：按策略拦截文本 |
| 安全与合规 | 外发 | `data-egress-guard` | 外发前脱敏 PII / 密钥 |
| 安全与合规 | 边界 | `publication-boundary` | 把内部资料挡在公开树之外 |
| 设计与前端 | 可访问性 | `accessibility-audit` | 无障碍审计与改进 |
| 设计与前端 | 界面 | `frontend-design` | 有视觉主张的前端界面 |
| 设计与前端 | 界面 | `web-experience-design` | 设计 → 实现 → 审计 Web 界面 |
| 设计与前端 | 设计 | `design-brief` | 把模糊需求解析成设计规格 |
| 设计与前端 | 设计 | `reference-design-contract` | 把参考图 / URL 变成 DESIGN.md |
| 设计与前端 | 设计 | `design-md` | 维护 DESIGN.md（Google Stitch 格式） |
| 设计与前端 | 评审 | `design-review` | 视觉审计 + 修复（前后对比截图） |
| 设计与前端 | 规范 | `web-design-guidelines` | 按 Vercel Web 界面规范检查 |
| 设计与前端 | 路由 | `frontend-guides-hub` | 把 UI 任务分流到对应技能 |
| 设计与前端 | 现代化 | `legacy-web-scan` | 扫出可现代化改造的遗留 Web 写法 |
| 设计与前端 | 现代化 | `modern-web-guidance-bridge` | 按需调用 Google MWG（不复制 guide） |
| 设计与前端 | 图像 | `imagegen-frontend-mobile` | 移动端界面配图提示词（不出图） |
| 设计与前端 | 图像 | `fal-gen` | 用 fal.ai 批量出图（需 `FAL_KEY`） |
| 设计与前端 | 图像 | `openrouter-gen` | 用 OpenRouter 图片模型批量出图（需 `OPENROUTER_API_KEY`） |
| 调研与写作 | 调研 | `research` | 面向高可信来源调研并落成 Markdown |
| 调研与写作 | 理解 | `why` | 解释「为什么这样设计」（带查证来源） |
| 调研与写作 | 理解 | `how` | 解释「它怎么运作」（代码走查） |
| 调研与写作 | 写作 | `writing-for-agents` | 写给 agent 看的文档 |
| 调研与写作 | 写作 | `language-policy` | 三层语言政策（代码 / 记录 / 文档） |
| 调研与写作 | 本地化 | `documentation-localization` | 多语言文档同步与事实一致 |
| 调研与写作 | 教学 | `teach` | 在本工作区教你一个新概念 |
| 运维与性能 | 运维 | `deployment` | 部署 / 发布（Compose、迁移、健康检查、回滚） |
| 运维与性能 | 性能 | `performance-audit` | 用代表性负载测量并优化性能 |
| 运维与性能 | 性能 | `benchmark-checklist` | 上报性能数据前的体检清单 |
| 运维与性能 | 事故 | `incident-debugging` | 线上事故的取证 / 隔离 / 缓解 / 复盘 |
| 记忆与上下文 | 记忆 | `memory` | 跨会话保存 / 召回决定与坑 |
| 记忆与上下文 | 上下文 | `context-compression` | 纯本地压缩 / 清理长对话 |
| 记忆与上下文 | 上下文 | `recall` | 从历史重建当前工作上下文 |
| 记忆与上下文 | 上下文 | `reflect` | 对会话做复盘并把经验路由回技能 |
| 记忆与上下文 | 交接 | `handoff` | 把会话压成交接文档 |
| 记忆与上下文 | 留痕 | `show-me-your-work` | 长期 / 无人值守工作留决策流水 |
| 工程原则 | 设计 | `principle-foundational-thinking` | 先定核心类型 / 数据结构 |
| 工程原则 | 设计 | `principle-model-the-domain` | 用模型替代成堆分支 |
| 工程原则 | 设计 | `principle-type-system-discipline` | 让非法状态不可表达 |
| 工程原则 | 设计 | `principle-boundary-discipline` | 校验集中在系统边界 |
| 工程原则 | 设计 | `principle-redesign-from-first-principles` | 新需求融入旧设计时重新推导 |
| 工程原则 | 设计 | `principle-exhaust-the-design-space` | 新交互先做 2–3 个原型比较 |
| 工程原则 | 设计 | `principle-laziness-protocol` | 能删就删，最小改动 |
| 工程原则 | 设计 | `principle-subtract-before-you-add` | 先删死代码再加新东西 |
| 工程原则 | 调试 | `principle-fix-root-causes` | 修到「第一次出错」的地方 |
| 工程原则 | 调试 | `principle-attack-the-premise` | 多次失败先质疑共同前提 |
| 工程原则 | 调试 | `principle-explain-the-number` | 报数前先弄清它测的是什么 |
| 工程原则 | 验证 | `principle-prove-it-works` | 用真实产物验证再收工 |
| 工程原则 | 验证 | `principle-test-behavior-not-implementation` | 断言可观察行为，而非实现细节 |
| 工程原则 | 验证 | `principle-sequence-verifiable-units` | 小步可验证地推进 |
| 工程原则 | 验证 | `principle-build-the-lever` | 造工具，而不是手工做 |
| 工程原则 | 上下文 | `principle-guard-the-context-window` | 大输出交给子代理 |
| 工程原则 | 上下文 | `principle-minimize-reader-load` | 减少层数与隐藏状态 |
| 工程原则 | 上下文 | `principle-encode-lessons-in-structure` | 重复纠正就写成规则 / 校验 |
| 工程原则 | 并发与流程 | `principle-separate-before-serializing-shared-state` | 先消除共享，再谈串行 |
| 工程原则 | 并发与流程 | `principle-make-operations-idempotent` | 可重跑并收敛到同一状态 |
| 工程原则 | 并发与流程 | `principle-migrate-callers-then-delete-legacy-apis` | 迁完调用方再删旧 API |
| 工程原则 | 并发与流程 | `principle-outcome-oriented-execution` | 直奔目标架构，不留兼容垃圾 |
| 工程原则 | 产品与取舍 | `principle-experience-first` | 体验优先于实现便利 |
| 工程原则 | 产品与取舍 | `principle-never-block-on-the-human` | 可逆的事别等批准 |
| 流程与编排 | 元 | `ask-matt` | 问「该用哪个技能 / 流程」 |
| 流程与编排 | 编排 | `swarm` | 并行 N 个 worker，汇总成一份报告 |
| 流程与编排 | 版本 | `changelog` | 从 git 历史生成变更日志 |
| 流程与编排 | 初始化 | `setup-matt-pocock-skills` | 一次性配置 issue tracker / 标签 / 文档布局 |
| 流程与编排 | 改进 | `pdca-cycle` | 轻量 PDCA 迭代 |


## 角色 agents（21）

角色是**视角**（评审者、实现者、产品负责人……），不是独立产品；可单独用，也可由工作流指定。

| 大类 | 小类 | 名称 | 说明 |
|---|---|---|---|
| 入口 | 路由 | `wawoo-auto` | 默认入口：先把非平凡请求路由到工作流 |
| 交付 | 协调 | `delivery-lead` | 统筹证据化交付，不越过审批 |
| 交付 | 实现 | `implementer` | 按项目约定实现范围明确的改动 |
| 交付 | 测试 | `qa-engineer` | 设计测试策略、复现缺陷、评估验证证据 |
| 交付 | 项目 | `project-manager` | 迭代计划、进度报告、风险跟踪 |
| 交付 | 产品 | `product-owner` | 明确用户结果、优先级、范围与验收标准 |
| 交付 | 发布 | `release-manager` | 版本 / 法务 / 产物 / 回滚 / 远端核对 |
| 评审 | 代码 | `code-reviewer` | 资深工程师视角的细致代码评审 |
| 评审 | 代码 | `code-skeptic` | 不留情面地挑代码毛病 |
| 评审 | 代码 | `code-simplifier` | 简化 / 重构现有代码 |
| 评审 | 安全 | `security-reviewer` | 只读安全评审 |
| 评审 | 合规 | `compliance-reviewer` | 法务 / 合规 / 隐私评审闸门 |
| 评审 | 可访问性 | `accessibility-reviewer` | 只读无障碍评审 |
| 评审 | 性能 | `performance-reviewer` | 性能瓶颈与测量设计评审 |
| 架构 | 架构 | `architect` | 评估架构方案、接口、依赖与迁移风险 |
| 架构 | 数据 | `data` | notebook 优先的数据分析 |
| 设计 | Web | `web-designer` | 设计并实现可访问的响应式界面 |
| 设计 | 前端 | `frontend-specialist` | React / TypeScript / 现代 CSS 专家 |
| 文档 | 文档 | `docs-specialist` | Markdown、README、技能文本 |
| 文档 | 本地化 | `docs-localization-reviewer` | 多语言文档事实一致 |
| 运维 | 运维 | `sre-operator` | 只读优先的日志 / 监控 / 事故分析 |


## 工作流 workflows（12）

| 大类 | 小类 | 名称 | 说明 |
|---|---|---|---|
| 交付 | 小改动 | `/delivery-lite` | 轻量交付：SSOT 计划文件状态机（默认入口） |
| 交付 | 完整功能 | `/feature-delivery` | 发现 → 设计 → 实现 → 测试 → 评审 → 批准 |
| 设计 | UI | `/ui-delivery` | 设计 → 实现 → 审计 Web UI |
| 设计 | 评审 | `/design-review` | 只读 UI 设计评审 |
| 评审 | 自查 | `/self-review` | 自纠错：评审 → 调试 / TDD → 修复 → 验证 |
| 评审 | 合规 | `/compliance-review` | 法务 / 隐私 / 安全只读闸门 |
| 评审 | 发布 | `/release-review` | 发布审查包（含回滚证据） |
| 调研 | 决策 | `/research` | 调研 → 决策（→ 规格 / 票据） |
| 计划 | 迭代 | `/sprint-plan` | 迭代计划（L2） |
| 计划 | 报告 | `/status-report` | 进度 / 状态报告 |
| 运维 | 事故 | `/incident-response` | 取证 → 缓解 → 跟进 |
| 流程 | 改进 | `/self-improve` | 复盘 → PDCA → 自查 → 计划 |
