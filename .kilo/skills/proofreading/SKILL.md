---
name: proofreading
description: Proofread content for typos, punctuation, terminology consistency, numbers/units, cross-references, and tone; verify facts against sources. Use before publishing docs, articles, or reports.
---

# Proofreading（校正）

Fix errors **without changing meaning**. Two passes: **mechanical**, then **consistency & facts**.

## Pass 1 — Mechanical

- 誤字脱字・衍字・重複語。
- 句読点・括弧・全角/半角の統一（中国語：，。；：""、日本語：、。「」）。
- 数字・単位・日付の表記統一（例：`3分` vs `3 分`）。
- リンク切れ、コードブロックの言語タグ。

## Pass 2 — Consistency & facts

- 用語の一貫性（同じものを同じ語で。初出で定義）。
- 時制・人称・トーンの統一。
- 見出しの階層と目次（アンカー）が一致。
- 数字・固有名詞・引用を**出典と照合**（`research`）。推測は「未検証」と明記。
- 表と本文の食い違い（件数・名前）。

## Do not

- 意味を変えない。事実を足さない（足すのは別ステップ）。
- 「校正」で構成を書き換えない（それは `content-audit` の根因修正）。

## Output

- **「原文 → 修正」の対**（理由付き）。
- **未確認事項の一覧**。

## Pairs with

`content-audit`（構成・根因）· `seo-writing`（検索）· `science-writing`（正確さ）
