# PROGRAM: opensource-hardening（内部・非公開）

> **種別**: L2 プログラム計画（内部開発資料。`internal/` 配下＝非公開）。
> **作成**: 2026-10-28。ユーザー依頼（5 項目）の分解・優先度・依存・未決。**事業判断（スコープ/納期）は人が決める。**

## 1. 対象（ユーザー依頼の 5 項目）

| # | 依頼 | ワークストリーム |
|---|---|---|
| 1 | PI-DURABLE-ABSORPTION の優先度 A→H→B/C→F/G と §5 能力向上を**実装**し**テスト通過** | WS1 |
| 2 | 公開は**英語主・日本語従**。コード注釈/文字列は英語。説明ドキュメントは英日の 2 種 | WS2 |
| 3 | 一部の skill/agent/workflow を日本語→英語 | WS3 |
| 4 | `opencode.log` の用途・必要性・改名可否 | WS4（調査済） |
| 5 | ソースとテストコードを分離し、**テストは公開しない** | WS5 |

## 2. 実測（現状）

- **テストの所在**（現状ソースと同居）: `mcp/test_server.py`・`mcp/test_memory_ops.py`・`mcp/test_intent.py`・`mcp/test_intent_session.py`・`mcp/conftest.py`・`scripts/e2e_flows.py`・`scripts/cli_adapters_mock.py`。
- **CI**（`.github/workflows/validate.yml`）は `validate_assets.py`・`mcp/test_server.py`・`mcp/test_memory_ops.py`・`e2e_flows.py`・`cli_adapters_mock.py` を実行 → **テストを非公開にすると公開 CI が実行不能**。
- **`opencode.log`**: キット内に生成元なし（ランタイム＝Kilo/OpenCode 側）。
- **日本語で書かれた資産**（本文に日本語を含む行数）:
  - skills: `memory`(28)・`plan-md`(25)・`compliance-legal`(23)・`ask-matt`(20)・`slides`(19)・`imagegen-frontend-mobile`(17)・`screenshots-marketing`(16)・`privacy-review`(16)・`deployment`(16)・`changelog`(14)・`wayfinder`(10)・`design-brief`(9)・`writing-for-agents`(8)・`reference-design-contract`(4)・他。
  - commands: ほぼ全件（`delivery-lite`・`content-delivery-lite`・`market-plan` 等）。
  - agents: 6 件が日本語節「## 実行効率（トークン衛生）」を含む（`product-owner`・`security-reviewer` 等）。
- **公開ドキュメント**（英日 2 種が必要な候補）: `README.md`・`AGENTS.md`・`docs/{USAGE,INTENT-ROUTING,METHODOLOGY,PROCESS-PHILOSOPHY,VERSIONING,PUBLICATION,README}.md`・`docs/design/INTENT-RECEIVER.md`・`mcp/README.md`・`SECURITY.md`・`NOTICE` 等。
- **第三者ライセンス**: skills の一部は MIT / Apache-2.0（`.kilo/skills/ATTRIBUTION.md`）。**翻訳は派生著作物** → 帰属・NOTICE の維持が必要。

## 3. チケット（tracer-bullet）

| id | ws | title | blocked by | 見積（推測） |
|---|---|---|---|---|
| OS-4 | WS4 | `opencode.log` の発生源確認と命名方針 | — | S（調査済・方針のみ） |
| OS-5 | WS5 | ソース/テスト分離＋テスト非公開化＋CI 再設計 | — | M |
| OS-2a | WS2 | 公開コード（`mcp/`・`scripts/`）のコメント/文字列を英語化 | OS-5 | M |
| OS-3b | WS3 | 日本語の skills/agents/commands を英語化（**第三者 skill は原文へ差し替え／自作物のみ英訳**）（旧 OS-3a） | OS-2b（用語統一） | L |
| OS-2b | WS2 | 公開ドキュメントの英日 2 種化（英主・日従） | — | L |
| OS-1a | WS1 | A: `intent_session` 永続化＋再起動 resume（+テスト） | OS-5 | M |
| OS-1b | WS1 | H: コンテキスト予算の可測化（size 指標＋検証） | OS-5 | M |
| OS-1c | WS1 | B: rerun 安全性分類＋副作用の冪等キー | OS-1a | M |
| OS-1d | WS1 | C: 委譲の所有権/abort 契約を明文化 | — | S |
| OS-1e | WS1 | F/G: 先回り圧縮＋ボードの current-view/差分（文書） | — | S |

**依存の要約**: `OS-5`（テスト/CI 再設計）が `OS-1*`・`OS-2a` の前提。`OS-2`↔`OS-3` は用語設計を共有（`OS-2b` を先に）。

## 4. 未決（人が決める）

| id | 未決 | 選択肢 |
|---|---|---|
| D1 | WS2 の「説明ドキュメント」範囲 | (a) 公開 docs 全件を英日 2 種 / (b) 主要のみ（README・USAGE・INTENT-ROUTING） |
| D2 | WS3 の対象 | (a) 日本語を含む全資産 / (b) 一部のみ（対象一覧を提示して選択） |
| D3 | 非公開テストの CI | (a) 公開 CI は `validate_assets` のみ・テストは非公開 CI / (b) テストは `internal/`・公開 CI を縮小 / (c) 公開は e2e のみ残す |
| D4 | 英日 2 種の正本 | (a) 英語正本＋日本語翻訳 / (b) 日本語正本＋英語翻訳（現状寄り） |
| D5 | 第三者 skill 翻訳の帰属 | 翻訳版にも元ライセンス/ATTRIBUTION を維持（必須） |

## 5. リスク

- **CI 破壊**（D3）: テストを非公開にすると公開 CI が成立しない。方針確定が前提。
- **翻訳の帰属**（D5）: MIT/Apache-2.0 の skill 翻訳は派生 → `ATTRIBUTION.md`/`NOTICE` を維持。
- **大規模 i18n**（WS2/WS3）: `validate_assets.py` の `name=dir`・参照整合を壊さない。段階分割（1 セッション 1 成果物）。
- **WS1 は挙動変更**: `scripts/e2e_flows.py`＋`mcp/test_*.py` を先に整える（OS-5）。

## 6. 実行順（**正本は `BACKLOG.md`**）

> **順序の二重管理をやめた**（旧版はここに別の並びを書き、`BACKLOG`／チャットと食い違っていた＝不具合）。
> **順序の唯一の正本は `internal/docs/plans/BACKLOG.md`（行の順序＝優先度）**。下表はその要約で、変更時は `BACKLOG.md` を更新する。

**確定順（2026-10-28 統合）**:

```
1  OS-8  言語ポリシー3層（上位方針。先に決める）
2  OS-5  ソース/テスト分離＋テスト非公開＋CI 再設計（OS-1*/OS-2a/OS-9 の前提）
3  OS-9  静的 trigger 撤去 → 学習 DB seed＋upstream（i18n を安全化）
4  OS-3b 第三者 skill を原文へ差し替え／自作物を英訳（要 D2/D5）
5  OS-6  公開/非公開ドキュメント → 実行可能資産化（PUBLICATION→skill）
6  OS-2b 公開ドキュメント英日2種（要 D1/D4）
7  OS-2a 公開コードのコメント/文字列を英語化（OS-5・OS-8 後）
8  OS-1a session 永続化＋再起動 resume（機能実装の起点）
9  OS-1d 委譲の所有権/abort 契約（独立・小）
10 OS-1e 先回り圧縮＋ボード current-view/差分（独立・小）
11 OS-1b コンテキスト予算の可測化（OS-5 後）
12 OS-1c rerun 安全性＋冪等キー（OS-1a 依存）
13 OS-7 ステアリング（追加＋並べ替え＝replan／OS-1a・D6 依存）
14 OS-4  done（証拠あり）
```

**旧 `OS-3a` は `OS-3b` に置換**（§8.3）。**全 15 件・欠落なし**（OS-10 追加）。

**順序はプログラムで検証**する（人の記憶に頼らない）:
`python3 scripts/plan_l2_backlog.py internal/docs/plans/BACKLOG.md`（`depends` 列から未知依存・循環・**行順違反**を検知）。
`--apply` で**依存順に自動整列**。`OS-10` がこの仕組み自体。

## 7. 検証（共通ゲート）

- `python3 scripts/validate_assets.py` / `python3 scripts/plan_active.py docs/plans/ACTIVE.md` / `python3 scripts/e2e_flows.py`（未収束 FAILED = 0）
- CI 相当: `mcp/test_server.py`・`mcp/test_memory_ops.py`・`cli_adapters_mock.py`
- i18n 後も `name=dir`・参照・JSON 整合を維持

---

## 8. 追加意見（2 巡目・2026-10-28）

### 8.1 意見1: 公開/非公開ドキュメント → skill/agent/工作流 化

公開・非公開の**ドキュメントを実行可能資産に変換できるか**を棚卸しする。特に「規約＝書きっぱなし」を**強制**に変える。

| 元ドキュメント | 変換先（案） | 種別 |
|---|---|---|
| `docs/PUBLICATION.md` | `publication-boundary` skill ＋ 検証（公開ツリーに内部資料が混入していないか） | skill ＋ check |
| `docs/VERSIONING.md` | `changelog`/`release-readiness`（既存）＋ `validate` 連携 | 既存強化 |
| `docs/METHODOLOGY.md`・`PROCESS-PHILOSOPHY.md` | 既に workflows/agents に反映済（追加の整合確認） | 監査のみ |
| `scripts/readiness.json` | capability の ready 判定（既存 `interpret_intent`） | 既存 |
| 内部 `PROGRAM-*.md`・`BACKLOG.md` | 実行系は skill 化しない（計画は計画のまま） | 除外 |

→ チケット **OS-6**。

### 8.2 意見2: 言語ポリシーの制御（3 層）

| 対象 | 言語 | 制御を置く場所 |
|---|---|---|
| コード・コード注釈・識別子・コミットメッセージ | **英語** | `AGENTS.md` §1 ＋ `language-policy` skill ＋ 各 agent |
| **工程ドキュメント**（plans・ACTIVE・RETRO・evidence・memory 等、コードでない出力） | **日本語** | 同上（workflow の出力規定） |
| **説明ドキュメント**（利用者向け docs/README・USAGE 等） | **英語（主）＋日本語（従）の 2 種** | 同上 |
| エージェントの回答 | **日本語** | `AGENTS.md` §1（既存） |

→ チケット **OS-8**。`AGENTS.md`・`ROUTER`・workflow 出力節・agent 定義に反映。

### 8.3 意見3: 日本語資産の出典と「原文優先」

出典は `zen-router/docs/60-research` に原文あり。**第三者 skill は翻訳せず原文（英語）へ差し替え**、自作物のみ英訳する。

| JA skill | 出典 | 原文の所在 | 方針 |
|---|---|---|---|
| `ask-matt`・`wayfinder`・`writing-for-agents` | Skills For Real Engineers（MIT） | `skills-main/skills-main/skills/…` | **原文へ差し替え** |
| `design-brief`・`reference-design-contract`・`web-design-guidelines`・`imagegen-frontend-mobile`・`screenshots-marketing`・`slides` | OpenDesign（Apache-2.0） | `open-design-main/skills/…` | **原文へ差し替え** |
| `memory`・`plan-md`・`compliance-legal`・`privacy-review`・`deployment`・`changelog`・`change-readiness` | 本リポジトリ（MIT） | なし | **自作を英訳** |

- `AGENTS.md`/`ROUTER` の発火語との整合（日本語 trigger → 英語化）を維持。
- **帰属**（`ATTRIBUTION.md`・`LICENSE.txt`・`NOTICE`）を保持（D5）。
- 帰属の不整合（`slides`＝OpenDesign か自作か等）を**実測で確定**してから差し替え。

→ チケット **OS-3b**（OS-3a を置換・細分化）。

### 8.4 意見4: 実行中の動的タスク変更（ステアリング）

Pi Durable の「実行中に入力してタスクを動的に変更する」機能の実現性。

- **ランタイムの割り込み/キューはホスト（Kilo/Cursor/Agent Manager）の責務**。Agent Manager の `prompt` は実行中セッションに**キュー**され、本会話でも実際に成立している（ユーザーが実行中に意見を追加 → 反映）。
- **本キットで実装できる部分**:
  1. **再ルーティング契約**: 実行中に新指示が来たら `interpret_intent` で再ルートし、**セッションを破棄せず**スコープを更新（ゲートを維持）。`workflow_clear` を強制しない。
  2. **安全な変更**: タスクを冪等・再開可能（**OS-1a**）にし、途中変更で副作用が重複しない。
  3. **計画への反映**: 新指示を `ACTIVE`/`BACKLOG` に**追記**（上書きしない）。
  4. **ステアリング用ツール（任意）**: 例 `steer_task {text}`／`workflow_update {scope}` を MCP に追加し、`mcp_tools_allow` の例外に含める。

→ チケット **OS-7**。実装可否は **OS-1a（永続化/再開）**に依存。

### 8.5 追加チケットと更新後バックログ

`internal/docs/plans/BACKLOG.md` を更新（OS-3b・OS-6・OS-7・OS-8 を追加、OS-3a を OS-3b に置換）。

---

## 9. 質問への回答（3 巡目・2026-10-28）

### 9.1 Q1: 実行中の「動的タスク変更」で**順序**も最適化できるか

**はい（計画レベルで可能）**。追加（append）と並べ替え（reorder）を分離する。

- **順序＝優先度**で表現し、**再最適化は並べ替え**（内容・証拠は不変）。依存関係のトポロジカル順を満たす範囲で並べ替える。
- **反映タイミング**: 実行中は**ステップ境界**で反映（workflow の phases 順は固定だが、workflow 切替＝再ルートで順序を変えられる）。真の「ステップ途中での割り込み」はホスト＋チェックポイント（**OS-1a**）が前提。
- **実装形**: 新指示で `interpret_intent` 再ルート → 依存を満たす順に**並べ替えた計画**を提示 → `ACTIVE`/`BACKLOG` を並べ替え（上書きしない）。＝**replan アクション**。
- **制約**: `in_progress` は同時 1 件。完了済みは順序変更の対象外。

→ チケット **OS-7**（スコープを「追加のみ」→「追加＋並べ替え＝replan」へ拡張）。

### 9.2 Q2: 動的ルーティング（skill/agent/workflow の自動選択）は i18n 改変の影響を受けるか

**影響は限定的（小）。ただし条件付き。** ルーティングの入力は**中央の 4 つだけ**（実測）:

| 入力 | 所在 | i18n の影響 |
|---|---|---|
| workflow id（＝名前） | `mcp/intent_catalog.py` `WORKFLOWS` | **変更しない**（`validate_assets` が name=dir を強制） |
| workflow `description` | 同 `WORKFLOWS[].description` | 変更すると **upstream スコア（`catalog_for_upstream`）と `ROUTER.md`/`CAPABILITIES.md`** に波及 → **再生成必須** |
| 発火語 `TRIGGER_KEYWORDS`/`WEAK_TRIGGERS` | 同ファイル | **既に 日/中/英 併記**。英語化で壊れにくい。英/日の追加のみ |
| command 名（L0 slash） | `.kilo/commands/<name>.md` | 名前変更は**禁止**（参照破壊） |
| 学習ストア | `data/intent_learned.db` | 入力言語の変化で分布が変わる（自動・再学習可） |

**結論**:
- ルーティングは**ドキュメント本文や skill 本文の翻訳には依存しない**（名前＋説明＋発火語のみ）。よって**コストは低く抑えられる**。
- **高コスト化する条件**（避けるべき）: (a) `id`/`name` を改名する、(b) `description`/`TRIGGER_KEYWORDS` を**片言語だけ**にして再生成しない、(c) `gen_router.py`/`gen_capabilities.py` を回さない。
- **最適解**:
  1. `intent_catalog.py` を**ルーティング唯一の正本**として維持（本文とは分離）。
  2. `description` を**英日併記**（例: `description`(ja) ＋ `description_en`）にし、upstream プロンプトへ両方渡す。
  3. `TRIGGER_KEYWORDS` に英語発火語を追加（既存の日/中は保持＝**双方向**）。
  4. 変更後は `gen_capabilities.py`・`gen_router.py` を実行し、`e2e_flows.py` の `interpret_intent`/`route_task` を再実行。
  5. `validate_assets.py` に「各 workflow が ja/en の description と最低 1 つの en 発火語を持つ」検査を追加。

→ チケット **OS-9**（ルーティング catalog の二言語化・再生成・検証）。決裁 **D7**（`description` の二言語方式）。

### 9.3 補足: `TRIGGER_KEYWORDS` は**静的**（自己学習ではない）

ルーティングには **2 つの L1 機構**があり、混同しやすい。

| 機構 | 実体 | 生成 | 役割 |
|---|---|---|---|
| **L1 trigger** | `mcp/intent_catalog.py` の `TRIGGER_KEYWORDS`（dict リテラル） | **静的・人手（正本）**。`gen_router.py` が `ROUTER.md` の発火語を**ここから生成** | 決定論・無料の分類器（`classify_by_trigger`） |
| **L1 learned** | `data/intent_learned.db`（SQLite）＋`intent_learn_queue.py`（非同期書込） | **動的・自己学習**。高信頼 LLM 判定（upstream, `learn=true`, score≥閾値）だけを蓄積 | 過去入力→workflow の近似（substring/regex, 禁止 regex あり） |

- 解決順: **L0 slash → L1 learned（DB）→ L1 trigger（静的）→ L2 upstream（LLM）**。
- したがって `TRIGGER_KEYWORDS` は**学習で自動生成されない**。`learn` 既定は false（明示時のみ昇格）。
- i18n（**OS-9**）の対象は **静的 `TRIGGER_KEYWORDS`＋`description` の二言語化＋再生成**。**learned DB は入力言語に応じて自動適応**するため改変不要。

---

## 10. 設計検討: 静的 `TRIGGER_KEYWORDS` の廃止/置換（2026-10-28）

### 10.1 現状の位置づけ（実測）

解決順は **L0 slash → L1 learned（DB）→ L1 trigger（静的）→ L2 upstream（LLM）**。
静的 trigger は **learned の後・upstream の前**にある＝**コールドスタート用のブートストラップ**。learned（動的）と upstream（LLM）が既にあるため、多言語の静的語彙表は**維持コストに見合わない**。

依存箇所（置換時に触る）:
- `mcp/intent_catalog.py`（`TRIGGER_KEYWORDS`/`WEAK_TRIGGERS`/`classify_by_trigger`）
- `mcp/intent_interpreter.py:264`（L1 段）
- `scripts/gen_router.py`（`ROUTER.md` の発火語列を生成）
- テスト `mcp/test_intent.py`（`test_trigger_classifier_ja/en`・`test_trigger_weak_is_ambiguous`・`test_trigger_learns`）＋ `mcp/conftest.py`（learned 隔離）
- `ROUTER.md` の発火語列

### 10.2 選択肢

| 案 | 内容 | 長所 | 短所 |
|---|---|---|---|
| **A. 全廃** | 静的 trigger を削除。learned ＋ upstream のみ | 保守不要・多言語は LLM 任せ | **コールドスタートで毎回 LLM スコア**（latency/コスト増） |
| **B. 自動生成** | `description`＋名から**ビルド時に多言語 seed を生成**（LLM/規則）。人手メンテなし | 決定論・無料を維持、多言語生成可 | 生成物の品質依存、再生成が必要 |
| **C. セマンティック** | 埋め込みで類似度マッチ（言語非依存） | **言語非依存**・語彙メンテ不要 | 埋め込みモデル/実行系が必要（stdlib 依存ゼロに反する） |
| **D. ハイブリッド（推奨）** | 静的語彙表を**廃止**し、**learned を seed で初期化**（workflow id＋name＋description から自動投入）＋ upstream フォールバック。slash(L0) は維持 | 保守不要・コストは学習で逓減・多言語耐性 | seed 品質の設計が必要 |
| C+ | D ＋ **任意の埋め込み L1**（ホストが埋め込みを渡せる場合のみ） | 品質最大 | 依存（任意・既定 off） |

### 10.3 推奨 → 採用: D（flag なし・学習 DB へ移行）— **D7 決裁済み（2026-10-28）**

1. 静的 `TRIGGER_KEYWORDS`/`WEAK_TRIGGERS` は**残さない（`WAWOO_INTENT_STATIC_TRIGGERS` flag も置かない）**。既存語彙は**学習 DB（`data/intent_learned.db`）へ seed として移行**する（`IntentLearnedStore.promote()` で substring として投入。`WEAK_TRIGGERS` は低 confidence）。
2. 既定の解決順を **L0 slash → L1 learned（seed 済）→ L2 upstream** に変更（**静的段を削除**）。
3. **seed**: 起動時に `data/intent_learned.db` へ workflow の id/name/description から初期エントリを投入（多言語は upstream 採用時に自動追加＝learned が育つ）。
4. `gen_router.py`/`ROUTER.md` の「発火語」列を**「用途/説明」列**へ（言語非依存化）。
5. テストを `test_trigger_*` → `learned-seeded`＋`upstream` 系へ置換。
6. （任意）`WAWOO_INTENT_EMBED_URL` があるときだけ埋め込み L1 を使う拡張点。

**トレードオフ**: コールドスタートでは upstream（ホスト LLM）スコアが増える。→ seed と学習で**逓減**。完全無料・決定論を最優先するなら B（自動生成）を選ぶ。

→ 決裁 **D7**（案 A/B/C/D）。実装はチケット **OS-9**（再定義: 静的 trigger の非推奨化と動的ルーティングへの置換）。

---

## 11. 吸収分析: Genie 4 × Gemini 3.8（世界モデル＋監督＝PM / Delivery Lead・2026-10-28）

### 11.1 出典と確度

- 出典: **ユーザー提供の記事（二次情報）**。「Genie 4」「Gemini 3.8」「Gemini Omni」の**一次発表は未確認** → 主張は**未検証**として扱う。
- 抽出対象は製品仕様ではなく、**「生成モデル＋監督/推論エージェント」の役割分担という設計思想**。

### 11.2 記事の要点（＝記事の主張）

1. **役割分担**: 生成（Genie 4＝世界モデル）と 推論（Gemini 3.8＝司令塔/監督・ガイダンスエージェント）。
2. **監督の仕事**: 目標を**手順に分解**し、生成中の出力を**確認**しながら各段階の成否と次の行動を計画、**一貫性を維持**。
3. **mid-generation の指示解釈**: ユーザーの途中指示（「天気を変えて」「人物を追加」）を**周囲の文脈に沿って解釈**し生成へ反映。
4. **リアルタイム応答**: キャラの会話応答を背後で生成（文脈依存）。
5. 基盤の生成モデルに**推論のオーバーレイ**を重ね、「言葉で変えられ、破綻の少ない」世界を実現。

### 11.3 本キットへの写像（推測）

| 記事の要素 | 本キットの対応物 | 現状 | 吸収 |
|---|---|---|---|
| PM / Delivery Lead（目標分解・段階監視・一貫性） | `project-manager`／`delivery-lead`＋phases＋`exit_criteria`＋gates(Gₑ) | 部分的 | **OS-11**: 監督ループを明示化（各 step 後に「成功か／次は何か」を確認） |
| 文脈に沿った mid-generation 指示解釈 | `interpret_intent` 再ルート＋ステアリング | 未実装 | **OS-7 拡張**: 解釈は**文脈（計画・会話状態）**を用いる |
| 生成 vs 推論のモデル階層 | 委譲（`delegate_subtask`）・agent の model 指定 | 任意・方針未定義 | **OS-12**: モデル階層/コスト方針（高速＝機械的、推論＝計画/検証） |
| 基盤＋推論オーバーレイ | skills（知識）／workflows・agents（制御）の分離 | 既存 | 原則として維持（混ぜない） |
| 破綻の少ない一貫性 | SSOT（ACTIVE/memory）＋gates＋compaction/handoff | 既存＋OS-1e | 既存を強化 |
| 世界/映像/音声/NPC の**生成** | — | — | **領域外** |

### 11.4 領域外（誇張しない）

- リアルタイムな世界・映像・音声生成、NPC 対話の**実体**。本キットは**ルーティング＋契約＋PM/Delivery Lead 監督**の層であり、生成は行わない。
- したがって吸収できるのは**「PM/Delivery Lead（監督エージェント）」の設計**と**モデル階層の運用**に限られる。

### 11.5 追加チケット

- **OS-11** **PM（`project-manager`）／Delivery Lead（`delivery-lead`）による監督ループ**の明示化（目標分解・段階監視・一貫性）。
  - 記事の「監督/ガイダンスエージェント」＝本キットでは**既存の専門職 `project-manager`（PM）／`delivery-lead`（Delivery Lead）**に読み替える（一般名の“監督”は使わない）。
  - 役割分担: **PM**＝計画・段階監視・整合（L2/L1 の舵取り）、**Delivery Lead**＝納品実行の監督。
- **OS-12** モデル階層・コスト方針（機械的=高速／計画・検証=推論）。
- **OS-7 拡張** 文脈（計画・会話状態）を用いた途中指示の解釈。

### 11.6 ルーティングで「実行中タスクへの途中指示」を解けるか（本題）

**結論: 今のルーティング（1 回きりの分類器）だけでは不可。ただし「amend（差分）意図」を持たせた *監督ループ* に拡張すれば解決できる。**

#### 現状の限界

- `interpret_intent` は**毎回「新規 workflow 選択」**を行う**ステートレスな分類器**。実行中の**計画（ACTIVE/BACKLOG）を文脈にできない**。
- セッションは `intent_session._active`（**in-memory**＝OS-1a 未対応）。`workflow_clear` で捨てる前提で、**継続前提の差分適用が無い**。
- 「新規タスク」と「走行中タスクへの**変更**」を区別する意図種別が無い（どちらも `schedule` に落ちる）。

#### 痛点 → ルーティングで解く（設計）

| 痛点（人が後から思いつく） | 現状 | ルーティングでの解決 |
|---|---|---|
| 実行中の新指示 | 「新規 workflow」と誤判定しがち | 意図種別 **`amend`**（追加/並べ替え/スコープ変更/中断）を導入 |
| 文脈が無視される | 実行計画を参照しない | 解釈時に**実行中の計画＋active workflow を文脈**に渡す（記事の“文脈で指示を解釈”） |
| 計画の変更が手作業 | 人が BACKLOG/ACTIVE を手で直す | ルーティングが**追記＋自動整列**（`plan_l2_backlog --apply`）を起動（OS-10） |
| 完了済みを壊す/上書き | — | **append-only**（内容は不変・順序のみ変更） |
| ツールゲートが壊れる | 再ルートでゲートが変わる | **amend 後もゲートを再計算して維持**（drop しない） |
| 途中変更の副作用重複 | 再実行で二重 | **冪等キー（OS-1c）＋checkpoint（OS-1a）** |
| 継続できない | in-memory で再起動に弱い | **durable session（OS-1a）** |

#### 拡張する契約（`interpret_intent` の出力）

```
interpret_intent(text, session?) → 次のいずれか
  schedule   : 新規タスク（現行どおり）
  amend      : 走行中計画への差分 {op: add|reorder|reprioritize|scope_change|abort, targets}
  clarify    : 曖昧 → 確認（needs_scoring と同系）
```
- `amend` は**実行計画を文脈**に解釈し、BACKLOG/ACTIVE を**追記**→`--apply` で整列→**ゲート再計算**。適用は**ステップ境界**（OS-11 PM/Delivery Lead 監督 + OS-1a checkpoint）。

#### 依存（この解決が立つ順）

`OS-1a（durable/checkpoint）` → `OS-9（動的ルーティング）` → `OS-7（amend/steering）` → `OS-11（PM/Delivery Lead 監督ループ）`。`OS-1c`（冪等）は途中変更の安全に必要。

→ **OS-7 のスコープを「amend 意図種別＋実行計画を文脈にした解釈」まで拡張**（下記 BACKLOG に反映）。

---

## 12. 監査（self-review）指摘と反映（2026-10-28）

監査レポート（読み取り専用）の指摘に対する**反映**。

| 指摘 | 重要度 | 反映 |
|---|---|---|
| C1 `install_global.py:223` が `mcp/test_server.py` を実行 → OS-5 でテスト移設すると壊れる | High | **OS-5 のスコープに内包**（`install_global` のテスト非依存化） |
| C2 `e2e_with_evidence.sh`・`internal.example/.../smoke.sh` が移設テストを参照 | Med | **OS-5 のスコープに内包** |
| C3 `.cursor/rules`・`internal.example` が i18n 対象に未明記 | Med | **OS-2b／OS-3b の対象に追加** |
| C4 `CHANGELOG`/`VERSION`・`wawoo-*.log`・`internal.example` 整合が未チケット | Low | **OS-13 を追加**（`internal.example` の整合は OS-5 に一本化＝重複回避） |
| 依存: OS-5（D3）がクリティカルパス | High | D3 を最優先の決裁に位置付け（下記） |
| 矛盾: テスト非公開 vs 公開 CI | High | **D3 で解消**（推奨: pytest 単体を `internal/`・公開 CI は `validate_assets`＋e2e 維持） |
| 矛盾: 言語境界（工程=JA／説明=EN+JA）未定義 | Med | **D1/D4 で確定**（推奨: 説明=英主日従、工程=日） |
| 矛盾: 静的 trigger 撤去後の fresh install | Med | **OS-9 の受入に明記**（description 由来 seed） |
| リスク: 第三者 skill 翻訳の帰属 | High | **D5**（`ATTRIBUTION`/`LICENSE`/`NOTICE` 維持） |
| リスク: i18n 工数 | High | 段階分割（OS-2b→OS-2a→OS-3b）で吸収 |

### 12.1 決裁ステータス（D1–D7）

| id | 内容 | 状態 |
|---|---|---|
| D1 | 「説明ドキュメント」の範囲 | **採用（2026-10-28・「顺序执行」指示）**: 公開 docs を主要から順次英日 2 種化 |
| D2 | 英語化する資産の範囲 | **確定**（§8.3 の表＝第三者 9・自作 7） |
| D3 | テスト非公開後の公開 CI | **採用（同）**: pytest 単体→`internal/`、公開 CI は `validate_assets` ＋ e2e 契約検証を維持 |
| D4 | 英日 2 種の正本 | **採用（同）**: 英語正本＋日本語翻訳（英主日従） |
| D5 | 第三者 skill 翻訳の帰属 | **確定（必須）**: 元ライセンス維持 |
| D6 | ステアリングの方式 | **採用（同）**: amend 契約＋専用 MCP ツール（`steer_task` 等）は実装する |
| D7 | 静的 trigger の扱い | **決裁済**: 撤去＋学習 DB へ seed（flag なし） |

### 13.1 OS-3b 下位バッチ（2026-10-28）

| バッチ | 対象 | 状態 |
|---|---|---|
| b1 | 自作 skill（`memory`・`plan-md`・`compliance-legal`・`privacy-review`・`deployment`・`changelog`・`change-readiness`）→ English | **done**（JP 0・gates green） |
| b2 | 第三者 skill（`ask-matt`・`wayfinder`・`writing-for-agents`・`design-brief`・`reference-design-contract`・`web-design-guidelines`・`imagegen-frontend-mobile`・`screenshots-marketing`・`slides`）→ 原文準拠＋日本語追加分を English（帰属維持） | **done**（上流 zh 例のみ残置） |
| b3 | agents（日本語節を持つ 6 件）→ English | **done** |
| b4 | commands / workflows（15 件）→ English、`.cursor/rules` も対象 | **done** |

方針: 第三者は **upstream（`zen-router/docs/60-research`）の英語原文に寄せ**、キット追加の日本語節のみ英訳。`LICENSE.txt`/`NOTICE.txt`/`ATTRIBUTION` を維持。

### 14.1 OS-2b 下位バッチ（英日 2 種・`NAME.md`(EN) ＋ `NAME.ja.md`(JA)）

| バッチ | 対象 | 状態 |
|---|---|---|
| b1 | `README.md`(EN)＋`README.ja.md`(JA)（件数 57/22、版 0.6.0 を修正） | **done** |
| b2 | `AGENTS.md`＋`AGENTS.ja.md`（e2e `test_contract_agents_ssot` の日本語アサートを英語へ更新） | **done** |
| b3 | `docs/USAGE.md`＋`.ja` | **done** |
| b4 | `docs/INTENT-ROUTING.md`＋`.ja` | **done** |
| b5a | `docs/{VERSIONING,PUBLICATION,README}.md`＋`.ja` | **done** |
| b5b1 | `docs/METHODOLOGY.md`＋`.ja` | **done** |
| b5b2 | `docs/PROCESS-PHILOSOPHY.md`＋`.ja` | **done** |
| b6a | `SECURITY.md`(EN+`.ja`)・`docs/plans/README.md`(EN+`.ja`)・`docs/memory/{TEMPLATE,MEMORY-TOOLS,INDEX.example}.md`(EN のみ・機構) | **done** |
| b6b1 | `mcp/README.md`＋`.ja` | **done** |
| b6b2 | `docs/design/INTENT-RECEIVER.md`＋`.ja` | **done** |

方針: 英語を `NAME.md`（主）、日本語を `NAME.ja.md`（従）。相互リンクを張る。ゲート（validate/e2e）を維持。

### 15.1 OS-2a 下位バッチ（公開コード英文化）

| バッチ | 対象 | 状態 |
|---|---|---|
| b1a | `mcp/*.py`（`intent_catalog.py` を除く）のコメント・docstring・メッセージ | **done**（残 JP は `memory_ops.py` の**JA 工程ドキュメント生成定数**のみ＝意図的保持） |
| b1b | `mcp/intent_catalog.py` の workflow `description`・phase goal/exit_criteria（→ English）＋テスト追随 | **done** |
| b2a | 小スクリプト（`validate_assets`・`gen_capabilities`・`plan_active`・`plan_content`・`plan_l3_record`・`task-router`・`cli_adapters_mock`） | **done**（パーサ用キーワードは維持） |
| b2b | `gen_router.py`（ROUTER 内容→EN）・`install_global.py` | **done** |
| b2c | `plan_l2_backlog.py`・`e2e_flows.py`（コメント/docstring。JA fixture は維持） | **done** |
| b3 | shell（`*.sh`・`*.zsh`）のコメント | open |

方針: コード・コメント・識別子・**実行時メッセージ**は English。**JA 工程ドキュメントを生成する定数**（memory のセクション名等）は維持。

---

## 16. 創作系 skill の比較・選定（2026-10-28）

| 候補 | 出典 / ライセンス | 判定 | 理由 |
|---|---|---|---|
| `writing-fragments`/`writing-beats`/`writing-shape` | SFE / **MIT** | **採用** | explore→構成→執筆の中核。汎用。 |
| `teach` | SFE / **MIT** | **採用**（例外予算） | 概念を教える設計（科普の教育モード）。参照 FORMAT 同梱。 |
| `marketing-psychology` | OpenDesign / **Apache-2.0** | **再利用** | hook/framing（人气）の心理面。既存。 |
| `article-magazine`・`blog-post` | OpenDesign / **Apache-2.0** | **任意** | HTML 版面。文章そのものではない。 |
| `science-writer`（nobodyonlyc/skills） | **LICENSE ファイル無し**（frontmatter のみ MIT 主張）・自動生成の巨大リポジトリ | **不採用** | ライセンス実物を確認できない（D5）。供給網リスク。 |
| `scientific-writing`（K-Dense, MIT） | MIT | **不採用** | 学術論文向けで科普と目的が異なる（重複・過剰）。 |
| `writing-in-the-sciences`（jingkarqi, MIT 表記） | MIT（索引情報） | **不採用** | `science-writing`（自作物）と重複。 |
| `content-writer`（claude-office, MIT） | MIT | **不採用** | `writing-*` と重複。 |
| `content-research-writer`（Kilo Marketplace） | **NOASSERTION** | **不採用** | ライセンス不明。 |

**採用して残したもの**: `writing-*`（MIT）、`teach`（MIT）、**オリジナル** `science-writing`（科普）・`viral-hooks`（人气）、既存 `marketing-psychology`（Apache）。**skills 63**。
