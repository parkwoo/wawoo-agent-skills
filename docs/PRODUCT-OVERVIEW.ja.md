# wawoo-skills：AI コーディングエージェント向けオープンソースキット
<!-- SEO: AI コーディングエージェント (Cursor, Kilo, OpenCode) 向け MCP キット。skill 97・agent 21・workflow 12。同じ依頼を同じ手順で、検証可能な証拠を伴う。製品固有の skill は含みません。 -->

[English](PRODUCT-OVERVIEW.md) · [简体中文](PRODUCT-OVERVIEW.zh-CN.md) · [日本語](PRODUCT-OVERVIEW.ja.md) · [한국어](PRODUCT-OVERVIEW.ko.md)

## このキットとは

**AI コーディングエージェントは skill を持っているのに、使わないことが多い** — そのギャップを埋める **製品非依存**のオープンソースキットです。**skill**・**agent 役割**・**workflow**・**MCP**（Model Context Protocol）サーバを束ね、「最初に何を読むか」「どの workflow に乗るか」を設計します。実装の中身はエージェントが書き、**手順の再現性**だけをレールで支えます。これにより、検証可能な証拠を伴う**再現性のある成果**を保証します。

**件数の定義場所：** `python3 scripts/gen_capabilities.py` のあと `.kilo/CAPABILITIES.md`（手編集しない）。

| 種類 | 件数 | 定義場所 |
|------|------|----------|
| Skill | **97** | `.kilo/CAPABILITIES.md` |
| Agent | **21** | `.kilo/CAPABILITIES.md` |
| Workflow | **12** | `.kilo/commands/<name>.md ファイル群` |

## 60 秒で

**ルーティングなし：**「このバグ直して」→ 即興・レビュー飛ばし → 明日また別ルート。

**wawoo-skills あり：** `interpret_intent` が `/self-review` を選択 → `diagnosing-bugs`・`test-engineering` を順に開く → 「完了」前に再現やログ。

## 向いている人

- **Cursor / Kilo / OpenCode** で skill を置いたが**開かれない**チーム
- レビュー・テスト・コンプライアンスを**形だけにしたくない**人
- **同じタスク → 同じ workflow → 同じ証拠**が欲しいが、実装の創造性は残したい人

## こんな困りごと向け

| # | 困りごと | キットの答え |
|---|----------|--------------|
| 1 | skill があるのに**散文だけ**で進む | `/delivery-lite` 等 + MCP `workflow_get` で入口を固定 |
| 2 | 同じ依頼で毎回ルートが違う | `interpret_intent` が **12** workflow のどれかへ |
| 3 | レビュー・法務・テストが形だけ | 監査系 workflow (例: `/compliance-review`) は読み取り専用・**証拠を求めるゲート** |
| 4 | skill を一度に全部渡して誰も開かない | カタログ → **`skill_get` で 1 個ずつ** |
| 5 | 決定が次セッションに残らない | `memory_recall` / `memory_save`（`docs/USAGE.ja.md` §5.1） |
| 6 | Cursor で slash workflow が動かない | MCP + `@.kilo/commands/` |
| 7 | 証拠なしの「完了」 | `change-readiness`・`docs/plans/` の証拠パターン |
| 8 | 監査中にデプロイ等が走る | workflow ごとの **MCP 許可リスト** |
| 9 | PII・秘密の外部送信 | `content-guardrail`・`data-egress-guard`・`mask_pii` |
| 10 | UI 変更に a11y 証拠がない | `/ui-delivery`・`docs/SKILL-UPLIFT-PILOT.ja.md` |

## 用語を人語に

| 用語 | 意味 |
|------|------|
| 呼び出しを設計する | `interpret_intent` / `workflow_get` から始める |
| 段階的開示 | **SKILL を 1 つずつ**開く |
| フェーズと終了条件 | 各段階の「完了」の定義 |
| MCP | **Model Context Protocol**（Python 標準ライブラリのみ） |
| ゲート | **承認・証拠・観測失敗** — 推測ではなく、検証可能な完了を保証する |

## Skill の地図（用途別）

**97** skill のざっくり分類。名前の全件は `.kilo/CAPABILITIES.md` のみ。

| 分野 | 内容 | 例 |
|------|------|-----|
| 実装・デバッグ | 仕様・実装・バグ | `to-spec`・`implement`・`diagnosing-bugs` |
| 品質・設計 | レビュー・判断 | `code-review`・`change-readiness` |
| UI・Web | 画面・a11y | `frontend-design`・`accessibility-audit` |
| 調査・プロダクト | 発見・計画 | `research`・`product-discovery` |
| 安全・コンプライアンス | リリース前 | `security-review`・`privacy-review` |
| 運用 | デプロイ・障害 | `deployment`・`incident-debugging` |
| 記憶・文脈 | 長いセッション | `memory`・`context-compression` |
| 原則系 | 原則・ガイドライン (例: エンジニアリング上の判断、必要に応じて) | `principle-*` |
| キット自身 | skill の書き方等 | `writing-for-agents`・`publication-boundary` |

## Workflow 一覧（12）

| よくある依頼 | Workflow |
|--------------|----------|
| 小さく直す・1 機能 | `/delivery-lite` |
| 機能のライフサイクル全体 | `/feature-delivery` |
| UI を作る・直す | `/ui-delivery` |
| UI のレビューだけ | `/design-review` |
| 調査して決める | `/research` |
| 自分で品質見直し | `/self-review` |
| プロセス改善 | `/self-improve` |
| スプリント計画 | `/sprint-plan` |
| 進捗報告 | `/status-report` |
| 障害対応 | `/incident-response` |
| リリース前パッケージ | `/release-review` |
| 法務・プライバシー・セキュリティ（読み取り） | `/compliance-review` |

迷ったら **`wawoo-auto`** または **`interpret_intent`**。

## Agent（21）

レビューア・実装者・PO などの**視点**です。一覧は `.kilo/CAPABILITIES.md` の **Agents** 節。

## よくある質問

### 特定製品専用ですか？
**いいえ。** どのリポジトリでも使える汎用キットです（社内専用 skill は**この公開リポジトリには含めません**）。

### MCP に pip は要りますか？
**不要**（Python 3 標準ライブラリのみ）。

### 対応クライアントは？
**Kilo・Cursor・OpenCode**（MCP 設定済み）。手順は `docs/USAGE.ja.md`。

### 件数はどう確認しますか？
`python3 scripts/gen_capabilities.py` → `.kilo/CAPABILITIES.md` ヘッダ（現状 **97 / 21 / 12**）。

## 連携（Paseo・Google・pstack）

- [INTEGRATIONS.ja.md](INTEGRATIONS.ja.md) — Paseo / MWG / pstack

## 次に読む

1. [`docs/INTEGRATIONS.ja.md`](INTEGRATIONS.ja.md)  
2. [`docs/USAGE.ja.md`](USAGE.ja.md)  
3. [`docs/INTENT-ROUTING.ja.md`](INTENT-ROUTING.ja.md)  
4. [`.kilo/CAPABILITIES.md`](../.kilo/CAPABILITIES.md)