# 文案、广告与长文 — 工作流对照

[English](COPY-MARKETING-GUIDE.md) · [日本語](COPY-MARKETING-GUIDE.ja.md) · [简体中文](COPY-MARKETING-GUIDE.zh-CN.md) · [한국어](COPY-MARKETING-GUIDE.ko.md)

## 一句话

**非代码写作**按目的选 **workflow**；skill 用 `skill_get` **每次只加载一个阶段**，不要通读目录。

## 1. 选哪个入口？

| 目标 | 命令 | 状态正本 | 主要 skill |
|------|------|----------|------------|
| 博客、随笔、专栏、台本 | `/writing` | 可选 `CONTENT.md` | fragments → beats → shape |
| 强标题 / 钩子 | `/writing`（viral） | 同上 | + `viral-hooks` → `marketing-psychology` |
| 科普 / 解说 | `/writing`（science） | 同上 | + `science-writing` |
| 书稿 / 长报告分章 | `/content-delivery-lite` | `CONTENT.md` | `writing-for-agents` 等 |
| 市场 → 价格呈现 | `/market-plan` | `ACTIVE.md` | research 链 → `marketing-psychology` |
| 幻灯片 | `/deck` | `ACTIVE.md` | `slides` |
| 落地页 / 营销截图 | 单 skill | 证据路径 | `screenshots-marketing` 等 |
| 说明文档 | `/delivery-lite` | `ACTIVE.md` | `writing-for-agents` |

**记忆：** 见 [MEMORY-CLIENT-GUIDE.zh-CN.md](MEMORY-CLIENT-GUIDE.zh-CN.md)。

## 2. `/writing` 三阶段

| 阶段 | skill | 做 | 不做 |
|------|-------|-----|------|
| 探索 | `writing-fragments` | 碎片写入一个 md | 提纲、润色 |
| 结构 | `writing-beats` | 排 beat、先落地术语 | 全文初稿 |
| 成稿 | `writing-shape` | 另文件输出终稿 | 改碎片源文件 |

**viral：** 标题/导语 → 再调价格与 CTA **呈现**（不改事实）。

## 3. 分工

- **`viral-hooks`**：标题、开头、结构  
- **`marketing-psychology`**：价格表、CTA（`framing-principles.md`）

## 4. Agent

- `docs-specialist` — 长文  
- `market-researcher` — 市场计划（**定价决策在人**）

## 5. 文档索引

[GUIDES.zh-CN.md](GUIDES.zh-CN.md) · [CLIENT-INTEGRATION-GUIDE.zh-CN.md](CLIENT-INTEGRATION-GUIDE.zh-CN.md)