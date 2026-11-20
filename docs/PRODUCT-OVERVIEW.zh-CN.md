# wawoo-skills：为 AI 编程智能体提供可复现工作流
<!-- SEO: wawoo-skills 为 Cursor/Kilo/OpenCode 上的 AI 编程智能体提供 112 个 skill、workflow 与 MCP 路由，让同一请求走同一条可验证的路径。 -->

[English](PRODUCT-OVERVIEW.md) · [日本語](PRODUCT-OVERVIEW.ja.md) · [简体中文](PRODUCT-OVERVIEW.zh-CN.md) · [한국어](PRODUCT-OVERVIEW.ko.md)

## wawoo-skills 能做什么

你的 AI 智能体已经有很多 skill，却常常**不用、乱用、每次路线不同**。wawoo-skills 用 **workflow + MCP** 设计「先读什么、走哪几步」，在不过度限制创造力的前提下，让同类请求得到**可复现、可留证**的结果。

## 我们针对的痛点

| # | 痛点 | 套件的回应 |
|---|------|------------|
| 1 | 有技能书却**只靠散文即兴** | Workflow（如 `/delivery-lite`）+ MCP `workflow_get` 固定入口 |
| 2 | 同样「修 bug」每次路线、质量都不同 | `interpret_intent` → **20** 条 workflow 之一；阶段写明开哪些 skill |
| 3 | 评审、法务、测试**流于形式** | 审计类 workflow 禁止 `implement`；**证据门**（要可验证产物） |
| 4 | 一次塞 100+ skill：** token 暴涨、谁也不打开** | 目录 → 候选 → **`skill_get` 逐个打开** |
| 5 | 会话结束决策就丢 | `memory_recall` / `memory_save` + [MEMORY-CLIENT-GUIDE.zh-CN.md](MEMORY-CLIENT-GUIDE.zh-CN.md) |
| 6 | Cursor 里 `/feature-delivery` **不生效** | 需 MCP + `@.kilo/commands/`，命令正文为正本 |
| 7 | 文案、市场、长文**不知用哪个 skill** | [COPY-MARKETING-GUIDE.zh-CN.md](COPY-MARKETING-GUIDE.zh-CN.md) |
| 8 | 口头「完成」、无复现与产物 | `change-readiness`、ACTIVE/CONTENT、`docs/evidence/` |
| 9 | 审计过程中仍部署、写 memory | 每条 workflow 的 **MCP 工具白名单** |
| 10 | Wiki 有知识但 agent 不读 | 开工 `memory_recall`、workflow 入口读 INDEX |
| 11 | PII/密钥直接发到外部 API | `guard_content` → `mask_pii`（确定性脚本） |
| 12 | 改 UI 无 a11y/响应式证据 | `/ui-delivery` 5b + uplift 检查 |
| 13 | 「读完所有 principle」撑爆上下文 | 仅加载当前阶段需要的 `principle-*` |
| 14 | Kilo / Cursor / OpenCode / Paseo **配置不一致** | [CLIENT-INTEGRATION-GUIDE.zh-CN.md](CLIENT-INTEGRATION-GUIDE.zh-CN.md) |

## 产品特点（人话）

| 术语 | 含义 |
|------|------|
| 按设计调用 | **设计调用路径** — 首选 `interpret_intent` / `workflow_get` |
| 渐进披露 | **不一次倒完全库** — 给候选，再开一个 SKILL |
| 阶段 + 退出条件 | **每步完成标准写清楚** |
| mcp_tools_allow | **这份工作允许用的工具** — 审计时不部署 |
| 审批 / 证据 / 观测失败门 | 不能靠猜就说完成；要有批准、复现或实测失败 |
| 轨道不是笼子 | 轨道为**可复现**；实现仍由 agent 写 |

**务实点：** MCP 仅 **Python 3 标准库**；Kilo、Cursor、OpenCode（Paseo）可指向同一 kit root。

## 套件内容（数量）

| 类型 | 数量 | 正本 |
|------|------|------|
| **Skill** | 112 | `.kilo/CAPABILITIES.md`（自动生成全表） |
| **Agent** | 23 | 同上 |
| **Workflow（斜杠命令）** | 20 | `.kilo/commands/*.md` |

> **全部 skill 名称**见 `python3 scripts/gen_capabilities.py` 后的 `.kilo/CAPABILITIES.md`。下文为**按用途的地图**。

## Skill 地图（分类）

| 分类 | 约 | 代表 skill | 场景 | 入口 workflow |
|------|-----|------------|------|----------------|
| **工程实现** | 19 | `to-spec`、`tdd`、`implement`、`diagnosing-bugs` | 功能、缺陷、规格 | `/delivery-lite`、`/feature-delivery` |
| **质量评审** | 7 | `code-review`、`change-readiness` | 合并前、设计决策 | `/self-review` |
| **UI / 前端** | 13 | `web-experience-design`、`accessibility-audit` | 页面、组件 | `/ui-delivery` |
| **调研与文案** | 8 | `research`、`marketing-psychology`、`viral-hooks` | 调研、文章、定价呈现 | `/research`、`/market-plan`、`/writing` |
| **安全法务** | 6 | `security-review`、`privacy-review`、`content-guardrail` | 发布前、外发文本 | `/compliance-review` |
| **运维发布** | 4+ | `deployment`、`incident-debugging` | 部署、故障 | `/incident-response` |
| **文档计划** | 7+ | `plan-md`、`writing-for-agents` | ACTIVE/CONTENT | `/content-delivery-lite` |
| **记忆与上下文** | 4+ | `memory`、`context-compression` | 长会话、保存决策 | 各 workflow 入口 |
| **工程原则** | 24 | `principle-*` | 判断辅助（按需） | 每阶段 1～2 个 |
| **套件基座** | 数个 | uplift、`wawoo-auto` | 路由、校验 | MCP |

**工作区专用 skill**（公开 OSS 不含）：`kiun-*`、`paseo-orchestration`、`nextwave-catalog-bridge` 等。

## Workflow 速查

| 需求 | 先用 |
|------|------|
| 小改 / 单功能 | `/delivery-lite` |
| 跨模块功能 | `/feature-delivery` |
| 做 UI | `/ui-delivery` |
| 调研决策 | `/research` |
| 市场与定价叙事 | `/market-plan` |
| 文章与文案 | `/writing` |
| 自检质量 | `/self-review` |
| 故障 | `/incident-response` |
| 发布前 | `/release-review` |

不确定 → **`wawoo-auto`** 或 **`interpret_intent`**。

## 常见问题（FAQ）

### wawoo-skills 是什么？
面向 **AI 编程智能体**的开源套件：**112 skill、23 agent、20 workflow**，外加 **MCP**（Model Context Protocol）服务器。

### 和「把 skill 全贴进提示词」有何不同？
**渐进披露**：目录 → 候选 → 按阶段 `skill_get` 每次只打开一个 skill。

### MCP 指什么？
**Model Context Protocol**，本仓库内为 **仅用 Python 标准库** 的小型服务，提供 `workflow_get`、`skill_get`、memory 等工具。

### 需要额外 pip 包吗？
不需要。

## 继续阅读

1. [GUIDES.zh-CN.md](GUIDES.zh-CN.md)  
2. [CLIENT-INTEGRATION-GUIDE.zh-CN.md](CLIENT-INTEGRATION-GUIDE.zh-CN.md)  
3. [USAGE.md](USAGE.md)  
4. `.kilo/CAPABILITIES.md` — **完整 skill 名列表**