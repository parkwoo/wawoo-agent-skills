# ドキュメント・README・製品文案（公開キット）

[English](COPY-WRITING-GUIDE.md) · [简体中文](COPY-WRITING-GUIDE.zh-CN.md) · [日本語](COPY-WRITING-GUIDE.ja.md) · [한국어](COPY-WRITING-GUIDE.ko.md)

## 一言

公開 repo は**エンジニアリング向け文案**中心です。広告用 `/writing`・`viral-hooks` 等は**このツリーに含みません**。

## 何があるか

| 目的 | 入口 | skill | agent |
|------|------|-------|-------|
| README・AGENTS・skill | `/delivery-lite` | `writing-for-agents` | `docs-specialist` |
| 多言語 doc | 同上 | `documentation-localization`・`language-policy` | `docs-localization-reviewer` |
| PR 本文 | 同上 | `pr` | `docs-specialist` |
| 計画・進捗 | `/status-report` 等 | `plan-md` | `project-manager` |
| 調査→仕様 | `/research` | `research` → `product-discovery` | `product-owner` |

## README を直す手順

1. `/delivery-lite` または `interpret_intent` 
2. `memory_recall`（[MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md)） 
3. **`writing-for-agents` だけ**開く 
4. [GUIDES.ja.md](GUIDES.ja.md) へリンク 
5. 必要なら `memory_save`（`READONLY=0`）

## `writing-for-agents` の要点

1 文書 1 役割・秘密を例に出さない・詳細は `references/`

**索引:** [GUIDES.ja.md](GUIDES.ja.md)