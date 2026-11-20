---
description: Creative/article writing (explore → beats → shape), optionally with magazine/blog layout; runs parallel to content-delivery-lite.
agent: docs-specialist
replay: safe
---

# Writing（記事・コラム・台本の下書き）

**目標**: 素材を失わず **探索 → 構成 → 清書** の三段で仕上げる。全体の地図は `docs/COPY-MARKETING-GUIDE.ja.md`。

> 入口: `/writing` · 手順の正本: 本 command · 三 skill は MIT（`ATTRIBUTION.md`）

## いつ使うか

- ブログ、エッセイ、コラム、ニュースレター、小説下書き、トーク台本
- **章単位・長期の知識成果物**は併用 `/content-delivery-lite`（`CONTENT.md` が進捗の正本）

## モード（上乗せ skill）

| mode | 追加 skill | 用途 |
|------|------------|------|
| **general**（既定） | なし | 上記三段のみ |
| **science** | `science-writing` | 一般向け解説・エビデンス分離 |
| **viral** | `viral-hooks` → `marketing-psychology` | タイトル・フック・価格/CTA の見せ方（**事実は変えない**） |

## 手順

1. （任意）長編なら `CONTENT.md` に行を足す（`/content-delivery-lite`）
2. **探索** — `writing-fragments`: 断片だけを 1 つの md に追記（構成はまだ）
3. **構成** — `writing-beats`: 用語を先に地面に置き、ビート列を確定
4. **清書** — `writing-shape`: 断片ファイルは編集せず、完成稿を別出力
5. （任意）HTML 誌面: OpenDesign `article-magazine` / `blog-post`（無ければ Markdown のみ）
6. **検証** — 事実は `research`、トーン・ Web は `web-design-guidelines`。未検証は明示
7. `docs/` に保存し、証拠（パス・字数・レビュー日）を残す

## ゲート

- **公開・外部送信は承認後**
- 事実と推測を分離。出典・引用を捏造しない
- 第三者 skill の帰属（MIT）を保持

## 関連

- `docs/COPY-MARKETING-GUIDE.ja.md` · `/content-delivery-lite` · `writing-for-agents`（skill 文書用）