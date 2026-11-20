# wawoo-skills: AIコーディングエージェントのための再現可能なワークフロー
<!-- SEO: wawoo-skillsでAIコーディングエージェントを強化。再現可能なワークフローを設計し、一貫した品質を確保し、機能、バグ、コンプライアンスのゲートを強制します。 -->

[English](PRODUCT-OVERVIEW.md) · [日本語](PRODUCT-OVERVIEW.ja.md) · [简体中文](PRODUCT-OVERVIEW.zh-CN.md) · [한국어](PRODUCT-OVERVIEW.ko.md)

## wawoo-skills ができること

AIエージェントは強力なスキルを持っていますが、それらを一貫して効果的に使用することに苦労することがよくあります。wawoo-skillsは、スキル、エージェント、ワークフローといった再利用可能なコンポーネントの構造化されたキットを提供し、AIエージェントをガイドします。これにより、「どの情報を優先するか」と「どの手順に従うか」を設計し、同じ要求に対して常に同じ高品質で再現可能な結果を導き出し、創造性を損なうこともありません。

## こんな困りごとを想定している

| # | 困りごと | キットの答え |
|---|----------|--------------|
| 1 | 手順書・スキルがあるのに、エージェントが**散文だけ**で進む | Workflow（`/delivery-lite` 等）と MCP `workflow_get` で**入口を固定**し、明確な手順を定義します。 |
| 2 | 同じ「バグ直して」でも、毎回違うルート・違う品質 | `interpret_intent` が 20 のワークフローのいずれかにルーティングし、フェーズごとに使用するスキルを指定します。 |
| 3 | レビュー・法務・テストが**形だけ**（ゲート無視） | 監査ワークフローは `implement` を禁止し、**証拠ゲート**で検証可能な成果を要求します。 |
| 4 | スキル 100 個を一度に渡しても、**どれも開かない**＋トークンだけ増える | カタログ駆動型のアプローチで候補を選択し、`skill_get` でスキルを 1 個ずつ開きます（段階的開示）。 |
| 5 | 前回の決定が次のセッションに残らない | `memory_recall` / `memory_save` がクライアントのメモリシステムと統合されます ([MEMORY-CLIENT-GUIDE.ja.md](MEMORY-CLIENT-GUIDE.ja.md))。 |
| 6 | Cursor で `/feature-delivery` が**動かない** | MCP と `@.kilo/commands/` の統合により、コマンド本体が単一の真実の源となります。 |
| 7 | コピー・市場・長文の**どれを使うか分からない** | [COPY-MARKETING-GUIDE.ja.md](COPY-MARKETING-GUIDE.ja.md) のような専用ガイドが明確な方向性を提供します。 |
| 8 | 「完了」と言うだけで、再現手順・ログ・ファイルが無い | `change-readiness` と `docs/evidence/` が具体的な出力とアクティブなコンテンツを保証します。 |
| 9 | 監査中なのにデプロイや memory 書込が走る | ワークフローごとの MCP 許可リストがツールアクセスを制限します（例: `compliance-review` は読み取り専用）。 |
| 10 | Wiki に知見があるのにエージェントが読まない | 作業前 `memory_recall`、workflow 入口で INDEX を読む手順が統合されます。 |
| 11 | 外部 API に PII・秘密がそのまま出る | `guard_content` が `mask_pii` を呼び出し（決定的、LLM非依存）、外部送信前にマスクします。 |
| 12 | UI 変更で a11y・レスポンシブの証拠が残らない | `/ui-delivery` には、アップリフトチェックと証拠収集のステップが含まれています。 |
| 13 | 「とりあえず全部の principle を読め」でコンテキストが死ぬ | 必要な `principle-*` だけフェーズに載せます。 |
| 14 | OpenCode / Paseo / Kilo / Cursor で**設定がバラバラ** | [CLIENT-INTEGRATION-GUIDE.ja.md](CLIENT-INTEGRATION-GUIDE.ja.md) が統一された統合ガイダンスを提供します。 |

## 製品の特徴（機械語を人語に）

| 言い換え前（硬い） | 意味 |
|-------------------|------|
| Invocation by design | **呼び出しを設計する** — 最初のツールは `interpret_intent` / `workflow_get`。 |
| Progressive disclosure | **一度に全部渡さない**。候補だけ見せて、必要な SKILL だけ開くことで、エージェントを圧倒させません。 |
| Phase + exit_criteria | **段階のゴールが書いてある** — 「このステップの完了」を明確にし、エージェントが迷子になるのを減らします。 |
| mcp_tools_allow | **その仕事で使ってよい道具だけ** — 監査中にデプロイしないなど、不適切なアクションを防ぎます。 |
| 承認ゲート / 証拠ゲート / 観測失敗ゲート | **承認・証拠・観測失敗** — 「たぶん直った」だけで閉じません。 |
| Rails not cage | レールは**再現性**のため。実装の中身はエージェントが書くため、創造性を奪いません。 |

**技術的な外しにくさ:** MCP は **Python 3 標準ライブラリのみ**（追加 pip 不要）。Kilo・Cursor・OpenCode（Paseo 内蔵）で同じキット root を指せる。

## キットの中身（件数）

| 種類 | 件数 | 正本 |
|------|------|------|
| **Skill** | 112 | `.kilo/CAPABILITIES.md`（自動生成・全件表） |
| **Agent** | 23 | `.kilo/CAPABILITIES.md` |
| **Workflow（slash 相当）** | 20 | `.kilo/commands/*.md` |

> **全 skill 名の機械一覧**は `python3 scripts/gen_capabilities.py` のあと `.kilo/CAPABILITIES.md` を見る。本章は**用途別の地図**。

## Skill 地図（カテゴリ）

| カテゴリ | 件数 | 代表 skill | いつ使う | 入口 workflow 例 |
|----------|------|------------|----------|------------------|
| **開発・実装** | 19 | `to-spec`・`tdd`・`implement`・`diagnosing-bugs` | 機能追加・バグ・仕様化 | `/delivery-lite`・`/feature-delivery` |
| **品質・レビュー** | 7 | `engineering-quality`・`test-engineering`・`code-review`・`architecture-decision`・`change-readiness` | マージ前・設計判断 | `/self-review`・`/feature-delivery` |
| **UI・フロント** | 13 | `web-experience-design`・`frontend-design`・`accessibility-audit`・`frontend-guides-hub`・`modern-web-guidance-bridge` | 画面・コンポーネント | `/ui-delivery`・`/design-review` |
| **調査・市場・文案** | 8 | `research`・`product-discovery`・`marketing-psychology`・`viral-hooks`・`writing-*` | 調査・記事・価格の見せ方 | `/research`・`/market-plan`・`/writing` |
| **安全・法務** | 6 | `security-review`・`privacy-review`・`compliance-legal`・`content-guardrail`・`data-egress-guard` | リリース前・外部送信前 | `/compliance-review`・`/release-review` |
| **運用・リリース** | 4+ | `deployment`・`incident-debugging`・`release-readiness`・`dependency-upgrade` | デプロイ・障害 | `/incident-response`・`/release-review` |
| **文書・計画** | 7+ | `plan-md`・`writing-for-agents`・`documentation-localization` | ACTIVE/CONTENT・README | `/content-delivery-lite`・`/status-report` |
| **記憶・コンテキスト** | 4+ | `memory`・`context-compression`・`recall` | 長セッション・決定の保存 | 各 workflow 入口 |
| **エンジニアリング原則** | 24 | `principle-*` | 判断の補助（必要時だけ） | フェーズに 1〜2 個 |
| **キット基盤** | 数個 | `uplift` 系 script・MCP intent・`wawoo-auto` agent | ルーティング・検証 | 常時（MCP） |

**社内専用 skill**（公開 OSS から除外）: `kiun-*`・`paseo-orchestration`・`nextwave-catalog-bridge` 等 — 使う環境だけ `CAPABILITIES` に載る。

## Workflow（入口）早見

| よくある依頼 | まずこれ |
|--------------|----------|
| 小さく直す・1 機能 | `/delivery-lite` |
| 横断機能・設計から | `/feature-delivery` |
| UI を触る | `/ui-delivery` |
| 調べて決める | `/research` |
| 市場・価格の整理 | `/market-plan` |
| 記事・コピー | `/writing` |
| 自分で品質見直し | `/self-review` |
| 障害 | `/incident-response` |
| リリース前 | `/release-review` |

迷ったら agent **`wawoo-auto`** または MCP **`interpret_intent`**。



## よくある質問（FAQ）

### wawoo-skills とは？
AI コーディングエージェント（Cursor・Kilo・OpenCode/Paseo）向けの **skill・agent・workflow・MCP サーバ**のオープンソースキットです。同じ依頼を同じ手順で走らせます。

### スキルを大量に渡すのと何が違う？
**段階的開示**です。カタログ → 候補 → `skill_get` で 1 個ずつ、workflow のフェーズと結びつけます。

### ここでいう MCP は？
**Model Context Protocol**（モデルコンテキストプロトコル）。`interpret_intent`・`workflow_get`・`skill_get`・memory・安全系ツールを IDE から呼べる小さなサーバです。

### pip で追加インストールは必要？
不要です。同梱 MCP サーバは **Python 3 標準ライブラリのみ**で動きます。

## 次に読む

1. [GUIDES.ja.md](GUIDES.ja.md) — 短い手順書の索引  
2. [CLIENT-INTEGRATION-GUIDE.ja.md](CLIENT-INTEGRATION-GUIDE.ja.md) — 導入  
3. [USAGE.ja.md](USAGE.ja.md) — 完全版マニュアル  
4. `.kilo/CAPABILITIES.md` — **全 skill 名リスト**
