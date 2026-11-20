# 文案・広告・長文 — 読み方とワークフロー早見

[English](COPY-MARKETING-GUIDE.md) · [日本語](COPY-MARKETING-GUIDE.ja.md) · [简体中文](COPY-MARKETING-GUIDE.zh-CN.md) · [한국어](COPY-MARKETING-GUIDE.ko.md)

## 0. 一文

**コード以外の「書く仕事」**は目的別に workflow を選び、skill は **1 フェーズずつ** `skill_get` する。いきなりカタログ全読みしない。

## 1. どの入口を使うか

| やりたいこと | 入口（command） | 状態の正本 | 主な skill 列 |
|--------------|-----------------|------------|----------------|
| ブログ・エッセイ・コラム・台本の下書き | `/writing` | 任意で `CONTENT.md` | `writing-fragments` → `writing-beats` → `writing-shape` |
| 人気記事・強いタイトル・フック | `/writing`（mode: viral） | 同上 | ＋ `viral-hooks` → `marketing-psychology` |
| 図解・科普・一般向け解説 | `/writing`（mode: science） | 同上 | ＋ `science-writing` |
| 書籍・長報告・章単位の進捗管理 | `/content-delivery-lite` | `docs/plans/CONTENT.md` | `writing-for-agents`・`documentation-localization` |
| 市場調査 → 事業・価格の打ち手 | `/market-plan` | `ACTIVE.md` + `plan-md` | `research` → `research-decision-room` → `product-discovery` → `marketing-psychology` |
| 提案スライド | `/deck` | `ACTIVE.md` | `slides` ＋ 上記 research 系 |
| LP・マーケ画像 | スキル単体 | 証拠パス | `screenshots-marketing`・`fal-gen`（任意） |
| **説明・手順書・README** | `/delivery-lite` または docs 直編 | `ACTIVE.md` | `writing-for-agents`・`language-policy` |

**記憶**: 作業前に `memory_recall`、方針が決まったら `memory_save`（設定: [MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md)）。

## 2. `/writing` の三段（日本語で何をするか）

| 段 | skill | やること | やらないこと |
|----|--------|----------|----------------|
| **探索** | `writing-fragments` | 会話から「断片」だけを 1 つの md に貯める | 目次・構成・清書 |
| **構成** | `writing-beats` | 読者が理解できる順に「ビート」を並べ、用語を先に地面に置く | 一気に全文ドラフト |
| **清書** | `writing-shape` | 断片ファイルは触らず、別出力で段落ごとに完成稿 | 構造の再設計 |

**viral モード追加**: `viral-hooks` でタイトル・導入（約束・証拠・オープンループ）→ `marketing-psychology` で価格・CTA・比較の**見せ方**だけ整える（事実は変えない）。

## 3. `marketing-psychology` と `viral-hooks` の役割分担

| | `viral-hooks` | `marketing-psychology` |
|--|----------------|-------------------------|
| 対象 | タイトル・冒頭・記事の型 | 価格・プラン比較・CTA・ベネフィットの順序 |
| 出力 | 見出し案 3 本＋導入 1 本 | フレーミング前後（before/after 短文） |
| 禁止 | 釣りタイトル・架空の数字 | 虚偽の希少性・誇大な保証 |

手順の正本: `marketing-psychology` の `references/framing-principles.md`（原則一覧）。

## 4. 担当 agent

| agent | いつ載せるか |
|-------|----------------|
| **docs-specialist** | `/writing`・`/content-delivery-lite`（長文・ドキュメント） |
| **market-researcher** | `/market-plan`・`/research`（調査と計画。**価格・契約の決定は人**） |

MCP: 非自明な依頼は `interpret_intent` → `workflow_get` → 上表の command に合わせる。

## 5. 説明系ドキュメントの地図（漏れやすい所）

| 主题 | 正本 | 以前の穴 |
|------|------|----------|
| Kilo/Cursor/OpenCode 導入 | `docs/USAGE.ja.md` | 分散していた → §2〜§3・§5.1 に集約 |
| 記憶の on/off | [MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md)（4 言語） | `READONLY` の意味が表に無かった |
| 三端インストール | [CLIENT-INTEGRATION-GUIDE.ja.md](CLIENT-INTEGRATION-GUIDE.ja.md)（4 言語） | OpenCode・memory 抜け |
| ガイド一覧 | [GUIDES.ja.md](GUIDES.ja.md) | Paseo 形式の言語切替 |
| Uplift / UI 証拠 | `docs/SKILL-UPLIFT-PILOT.ja.md`・`/ui-delivery` 5b | OSS EN 版は P1.1 追跡中 |
| 文案・市場 | **本書** | workflow と skill の対応が無かった |
| 記憶の優先順 | `docs/memory/MEMORY-TOOLS.md` | → §5.1 へリンク済み |
| 意図ルーティング | `docs/INTENT-ROUTING.ja.md` | `memory_save` ゲートは workflow 別 |

## 6. 品質ゲート（文案共通）

1. **事実と推測を分ける**（`/research` と同じ）。
2. **タイトルと本文の約束を一致**させる。
3. **外部送信・公開は承認後**（`guard_content` → `mask_pii`）。
4. 数値・ testimonial は**出典または未検証ラベル**。

## 7. 最短 example

```text
「技術ブログを1本」
→ workflow: /writing
→ fragments ファイルを決める → writing-fragments
→ beats 確定 → writing-beats
→ 清書 md → writing-shape
→ viral なら viral-hooks でタイトル3案
```

```text
「競合と価格の見せ方を整理」
→ /market-plan
→ research で根拠 → research-decision-room
→ marketing-psychology で価格表の before/after のみ
```