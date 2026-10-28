---
tags: kit, decision
---

# kit

wawoo-skills キット本体に関する決定・制約。

### MEM-20261025-001

- **日付**: 2026-10-25
- **種別**: 決定
- **内容**: 記憶の正本は `docs/memory/`。MCP `memory_save` は INDEX と topic ファイルへ追記する。Kilo ネイティブメモリは補助で、矛盾時はファイルを優先する。
- **出典**: `docs/memory/MEMORY-TOOLS.md`・`.kilo/skills/memory/SKILL.md`

### MEM-20261025-002

- **日付**: 2026-10-25
- **種別**: 決定
- **内容**: L1 の進捗 SSOT は `docs/plans/ACTIVE.md`。`/delivery-lite` が既定入口。タスクの done／証拠は ACTIVE のみ。memory は決定・制約・落とし穴に限定。
- **出典**: `AGENTS.md` §3・`docs/METHODOLOGY.md` §5

### MEM-20261028-001

- **日付**: 2026-10-28
- **種別**: 制約
- **内容**: Kilo の `config.instructions` は**絶対パス必須**（相対 `ROUTER.md` は実行時コンテキストに注入されない）。既定 agent が `code` のままだと MCP ルーティングが漏れるため、`default_agent` を `wawoo-router` に設定する。反映にはエンジン再起動が必要（agent/command/instructions は起動時キャッシュ）。
- **出典**: `scripts/install_global.py`・`AGENTS.md` §4・検証（`kilo run` で最初のツールが `workflow_get`）

### MEM-20261028-002

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 実行衛生・収束ゲート（`AGENTS.md` §4.1）をキット共通規約とする — 1 セッション 1 対象／1 成果物、workflow 切替の明示、失敗の収束（未収束 FAILED = 0）、後始末（残留 0）、記憶 1 件以上、トークン衛生（1 step < 4KB）、ローカル検証。プロジェクト非依存。
- **出典**: `AGENTS.md` §4.1・`.kilo/agents/wawoo-router.md`・`ROUTER.md`・`.kilo/skills/test-engineering/SKILL.md`

### MEM-20261028-003

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 意図ルーティングは「L1 トリガ分類器（`intent_catalog.TRIGGER_KEYWORDS`、ROUTER の発火語と同一正本）+ phases」で決定論的に解決する。監査系 workflow に `implement` phase を持たせないことで、監査→実装の逸脱を構造的に防ぐ（切替宣言を必須化）。
- **出典**: `mcp/intent_catalog.py`・`mcp/intent_interpreter.py`・`docs/INTENT-ROUTING.md` §3.1/§3.2

### MEM-20261028-007

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: キットの MCP サーバ（`mcp/*.py`）と保守スクリプト（`scripts/*.py`）は **CPython 3 標準ライブラリのみ**（追加依存ゼロ・stdio のみ）。前提は「`PATH` に `python3`」。TypeScript 化は「VSCode が動けばどこでも動く」を意味しない: (1) VSCode デスクトップは Electron の Node を `PATH` に公開せず、MCP/スクリプトは外部プロセス起動のため node/python とも `PATH` 必須、(2) VSCode Web（vscode.dev/github.dev）は外部プロセス不可、(3) 学習データは sqlite3（TS では native addon か Node 22+ が必要）。結論（選択肢 A）: Python 継続を明記（`README.md`「前提条件（ランタイム）」・`docs/USAGE.md`「0. 前提条件」）。
- **出典**: `docs/plans/ACTIVE.md` `docs-req-python3`・`kilo.json`・`.cursor/mcp.json`・`mcp/intent_learned_store.py`
- **却下した代替**: 全量 TS 化（JS/TS 開発者以外の易用性は上がらず、依存とビルドを増やす）

### MEM-20261028-008

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 外部ハーネス Pi Durable（https://earendil.com/posts/pi-durable/）の方法論の吸収優先度を **A（`intent_session` 永続化＝実バグ級）→ H（可測性）→ B/C（契約明確化）→ F/G（文書微調整）** とし、**D（名前参照・ホットスワップ）はほぼ parity、E（state↔transcript 原子整合）は原理のみ**とする。分析は `internal/docs/design/PI-DURABLE-ABSORPTION.md`（**内部・非公開**）。
- **出典**: `internal/docs/design/PI-DURABLE-ABSORPTION.md`・`docs/plans/ACTIVE.md` `pi-durable-absorption`
- **却下した代替**: プロセス実行レベルの durability（ホスト＝Kilo/Cursor の責務で MCP が制御不可）・TS 化前提（選択肢 A を維持）

### MEM-20261028-009

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: `interpret_intent` 後のアクティブ workflow とツールゲートは **in-memory**（`mcp/intent_session.py:16` の `_active`）。**MCP サーバ再起動・クライアント reload で session/選択/ゲートが消える**（再ルーティング漏れ・ゲート逸脱の原因）。学習データは SQLite で永続だが session は非永続。恒久化（A）するまで、この非耐久性を前提に扱う。
- **出典**: `mcp/intent_session.py`・`mcp/intent_learned_store.py`・`internal/docs/design/PI-DURABLE-ABSORPTION.md` §2/A

### MEM-20261028-010

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: 本リポジトリは**オープンソース（公開）**。**内部開発資料**（調査・分析ノート、監査 `*-AUDIT.md`、`RETRO-*`・`self-improve-*`、E2E ログ）は**公開しない** — `internal/`（`.gitignore` 済）配下に置く。公開ツリーには利用者向けキット資産のみを置く。正本は `docs/PUBLICATION.md`。
- **出典**: `docs/PUBLICATION.md`・`.gitignore`（`/internal/`）

### MEM-20261028-011

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: キット本体の **`docs/plans/ACTIVE.md` と `docs/memory/*`（INDEX/kit/general/deployment 等）の実体は公開しない**（`git rm --cached` ＋ `.gitignore`）。公開するのはテンプレートのみ（`docs/plans/ACTIVE.example.md`・`docs/memory/INDEX.example.md`・`TEMPLATE.md`・`MEMORY-TOOLS.md`）。CI（`scripts/e2e_flows.py`）は**実 ACTIVE.md／リポジトリ memory に依存しない**よう自己完結化（example 参照・隔離 memory）。消費側は example からそれぞれ作成する。
- **出典**: `.gitignore`・`docs/PUBLICATION.md`・`scripts/e2e_flows.py`・`docs/plans/ACTIVE.example.md`・`docs/memory/INDEX.example.md`

### MEM-20261028-012

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: バックログ運用は **追記（append-only）**：新指示は行を追加し、既存行は上書きしない（置換は「置換」と明記して残す）。**優先度は行の順序で表し、再最適化は並べ替えで行う**（内容・証拠は不変）。決裁（D）が解けたら依存に合わせて再並べ替え可。`in_progress` は同時 1 件。
- **出典**: `internal/docs/plans/BACKLOG.md`（運用ルール）・`scripts/plan_l2_backlog.py`

### MEM-20261028-013

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: ルーティングの静的 `TRIGGER_KEYWORDS`/`WEAK_TRIGGERS` は**撤去**する（後方互換 flag も置かない）。既存語彙は **学習 DB（`data/intent_learned.db`）へ seed として移行**（`IntentLearnedStore.promote()`、`WEAK_TRIGGERS` は低 confidence）。解決順は **L0 slash → L1 learned（seed 済）→ L2 upstream**。理由: 多言語の人手語彙は保守不能、learned＋upstream で代替可能。トレードオフ: コールドスタートは upstream スコア増（seed＋学習で逓減）。
- **出典**: `internal/docs/plans/PROGRAM-opensource-hardening.md` §10・`mcp/intent_catalog.py`・`mcp/intent_interpreter.py`・`mcp/intent_learned_store.py`

### MEM-20261028-014

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: タスクの**実行順は二重管理しない**。順序の正本は `internal/docs/plans/BACKLOG.md`（行の順序＝優先度）。`PROGRAM` 等の他文書は順序を**要約せず参照**する（旧 `PROGRAM` §6 に別の並びを書き、`BACKLOG`／チャットと食い違う不具合が発生）。`OS-3a` は `OS-3b` に置換。
- **出典**: `internal/docs/plans/BACKLOG.md`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §6

### MEM-20261028-015

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: バックログの**順序・依存はプログラムで管理**する（人の記憶に頼らない）。`scripts/plan_l2_backlog.py` が `depends` 列から未知依存・循環・**行順違反**を検証し、`--apply` で**依存順に自動整列**（内容・証拠は不変）。`in_progress` は同時 1 件、`done` は証拠必須。順序の正本は `BACKLOG.md`（MEM-014）。
- **出典**: `scripts/plan_l2_backlog.py`（`analyze`／`--apply`）・`docs/plans/BACKLOG.example.md`・`internal/docs/plans/BACKLOG.md`

### MEM-20261028-016

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 監査後の未決を推奨案で採用（ユーザー「顺序执行」指示）: **D1**=公開 docs を主要から順次英日 2 種化／**D3**=pytest 単体を `internal/`・公開 CI は `validate_assets`＋e2e を維持／**D4**=英語正本＋日本語翻訳（英主日従）／**D6**=amend 契約＋専用 MCP ツール（`steer_task`）を実装。**D5**=第三者 skill 翻訳の帰属維持（必須）。**D7**=静的 trigger 撤去＋学習 DB seed。
- **出典**: `internal/docs/plans/PROGRAM-opensource-hardening.md` §12.1・`internal/docs/plans/BACKLOG.md`

### MEM-20261028-017

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: **言語ポリシーは 3 層**（正本 `AGENTS.md` §1・`.kilo/skills/language-policy/SKILL.md`）: (1) コード・注釈・識別子・コミット=**英語**、(2) 工程ドキュメント（`plans`/`ACTIVE`/`RETRO`/`evidence`/`memory`）と応答=**日本語**、(3) 説明ドキュメント（`README`/`docs/USAGE` 等）＝**英語主＋日本語従の 2 種**。`ROUTER.md` にも同ポリシー行を生成。
- **出典**: `AGENTS.md` §1・`.kilo/skills/language-policy/SKILL.md`・`scripts/gen_router.py`

### MEM-20261028-018

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: **pytest 単体テストは非公開**（`internal/tests/`・`.gitignore` 済）。`mcp/` に置かない。公開 CI は `validate_assets.py`＋`e2e_flows.py`＋`cli_adapters_mock.py`（公開）のみ。`install_global.py` のスモークは `internal/tests/` があれば実行・無ければ skip（公開消費側で壊れない）。公開ドキュメントは内部パス（`internal/tests`）を**実行手順として書かない**（注記のみ）。
- **出典**: `.github/workflows/validate.yml`・`scripts/install_global.py`・`internal/tests/`・`docs/USAGE.md`

### MEM-20261028-019

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 意図ルーティングの静的 trigger を**撤去済み**（`TRIGGER_KEYWORDS`/`WEAK_TRIGGERS`/`classify_by_trigger`/`TriggerMatch`）。解決順は **L0 slash → L1 learned → L2 upstream**。`mcp/intent_seed.py` が空 DB を **catalog id で seed**（fresh install ブートストラップ）。旧語彙はローカルの学習 DB へ一括移行（**配布しない**・`.gitignore`）。`ROUTER.md` は「用途/説明」列。多言語は learned＋upstream が担う。
- **出典**: `mcp/intent_catalog.py`・`mcp/intent_interpreter.py`・`mcp/intent_seed.py`・`scripts/gen_router.py`・`docs/INTENT-ROUTING.md`

### MEM-20261028-020

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-3b（日本語資産の英語化）は **4 バッチ**で実施（`PROGRAM` §13）: b1 自作 skill→EN（done）、b2 第三者 skill（原文準拠＋キット追加分のみ英訳・帰属維持）、b3 agents、b4 commands＋`.cursor/rules`。翻訳時も `name=dir`・参照・frontmatter を維持（`validate_assets` が検証）。
- **出典**: `internal/docs/plans/PROGRAM-opensource-hardening.md` §13・`.kilo/skills/`

### MEM-20261028-021

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-3b b2 完了（第三者 skill 9 件を English 化）。第三者 skill の**上流中国語例（`reference-design-contract` の `zh-CN`・triggers）は残置**（原文尊重・帰属）。キット追加の日本語節のみ英訳。`LICENSE.txt`/`NOTICE.txt` 維持。残: b3 agents（日本語節 6 件）・b4 commands＋`.cursor/rules`。
- **出典**: `.kilo/skills/`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §13

### MEM-20261028-022

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: OS-3b 完了。公開資産（自作 skill 7・第三者 skill 9・agents 6・commands 15・`.cursor/rules` 3）を English 化。第三者 skill は**上流中国語例のみ残置**（原文尊重・帰属）。**日本語（Hiragana/Katakana）残 0**。`AGENTS.md`・`docs/*`・`README.md`・コード注釈は OS-2b／OS-2a で別途。
- **出典**: `.kilo/skills/`・`.kilo/agents/`・`.kilo/commands/`・`.cursor/rules/`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §13

### MEM-20261028-023

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: OS-6 完了。公開境界を**実行可能資産化**：新スキル `.kilo/skills/publication-boundary/SKILL.md`＋`scripts/validate_assets.py` の `public_boundary_violations()`（`git ls-files` で内部パターン混入を検知。working tree で削除済み＝未コミットの除去は除外）。公開 CI（`validate_assets`）で境界違反を落とせる。
- **出典**: `.kilo/skills/publication-boundary/SKILL.md`・`scripts/validate_assets.py`・`docs/PUBLICATION.md`

### MEM-20261028-024

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: OS-2b（公開ドキュメント英日 2 種）の命名は **`NAME.md`＝英語（主）／`NAME.ja.md`＝日本語（従）**、相互リンク。バッチは `PROGRAM` §14（b1 README done、b2 AGENTS、b3 USAGE、b4 INTENT-ROUTING、b5 METHODOLOGY 等、b6 残）。b2 で AGENTS 英訳時は e2e `test_contract_agents_ssot` の日本語アサートを英語へ更新する。
- **出典**: `README.md`・`README.ja.md`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §14

### MEM-20261028-025

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b2 完了（`AGENTS.md` EN＋`AGENTS.ja.md` JA）。**英訳時に e2e の日本語アサートを英語へ更新**する必要がある（例 `test_contract_agents_ssot` は「Tasks and progress source of truth (SSOT)」へ）。同様に b3 以降（USAGE・INTENT-ROUTING）でも e2e／docs の日本語アサートを追随させる。
- **出典**: `AGENTS.md`・`AGENTS.ja.md`・`scripts/e2e_flows.py`

### MEM-20261028-026

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b3 完了（`docs/USAGE.md` EN＋`USAGE.ja.md` JA）。OS-2b は残 b4（INTENT-ROUTING）・b5（METHODOLOGY/PROCESS-PHILOSOPHY/VERSIONING/PUBLICATION/docs/README）・b6（mcp/README・SECURITY・INTENT-RECEIVER・plans/README・memory テンプレ）。件数の陳腐化（55/21）も随時修正（57/22）。
- **出典**: `docs/USAGE.md`・`docs/USAGE.ja.md`

### MEM-20261028-027

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b4 完了（`docs/INTENT-ROUTING.md` EN＋`.ja`）。残 b5（METHODOLOGY/PROCESS-PHILOSOPHY/VERSIONING/PUBLICATION/docs/README）・b6（mcp/README・SECURITY・INTENT-RECEIVER・plans/README・memory テンプレ）。
- **出典**: `docs/INTENT-ROUTING.md`・`docs/INTENT-ROUTING.ja.md`

### MEM-20261028-028

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b5a 完了（`docs/VERSIONING.md`・`PUBLICATION.md`・`README.md` を EN＋`.ja`）。b5 を b5a（done）／b5b（METHODOLOGY・PROCESS-PHILOSOPHY）に分割。残 b5b・b6。
- **出典**: `docs/*.ja.md`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §14

### MEM-20261028-029

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b5b1 完了（`docs/METHODOLOGY.md` EN＋`.ja`）。b5b を b5b1（done）／b5b2（PROCESS-PHILOSOPHY）に分割。残 b5b2・b6。
- **出典**: `docs/METHODOLOGY.md`・`docs/METHODOLOGY.ja.md`

### MEM-20261028-030

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b5b2 完了（`docs/PROCESS-PHILOSOPHY.md` EN＋`.ja`）。**b5（主要 docs）完了**。残 **b6**（`mcp/README.md`・`SECURITY.md`・`docs/design/INTENT-RECEIVER.md`・`docs/plans/README.md`・`docs/memory/{TEMPLATE,MEMORY-TOOLS,INDEX.example}.md`）。
- **出典**: `docs/PROCESS-PHILOSOPHY.md`・`docs/PROCESS-PHILOSOPHY.ja.md`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §14

### MEM-20261028-031

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b6a 完了（`SECURITY.md` EN＋`SECURITY.ja.md`、`docs/plans/README.md` EN＋`.ja`、`docs/memory/{TEMPLATE,MEMORY-TOOLS,INDEX.example}.md` は**機構のため EN のみ**）。b6 を b6a（done）／b6b（`mcp/README.md`・`docs/design/INTENT-RECEIVER.md`）に分割。
- **出典**: `SECURITY.ja.md`・`docs/plans/README.ja.md`・`docs/memory/TEMPLATE.md`

### MEM-20261028-032

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2b b6b1 完了（`mcp/README.md` EN＋`.ja`）。b6b を b6b1（done）／b6b2（`docs/design/INTENT-RECEIVER.md`）に分割。b6b2 が OS-2b 最後。
- **出典**: `mcp/README.md`・`mcp/README.ja.md`

### MEM-20261028-033

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-2b 完了**。公開ドキュメントを **EN 主（`NAME.md`）＋JA 従（`NAME.ja.md`）** の 2 種に（README・AGENTS・USAGE・INTENT-ROUTING・VERSIONING・PUBLICATION・docs/README・METHODOLOGY・PROCESS-PHILOSOPHY・SECURITY・plans/README・mcp/README・INTENT-RECEIVER）。memory テンプレ（TEMPLATE/MEMORY-TOOLS/INDEX.example）は機構として EN のみ。
- **出典**: 各 `*.md`／`*.ja.md`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §14

### MEM-20261028-034

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2a は 4 バッチ（`PROGRAM` §15）: b1a `mcp/*.py`（catalog 以外）のコメント/docstring/メッセージ→EN（done）、b1b `intent_catalog.py` の description→EN、b2 `scripts/*.py`、b3 shell。**`mcp/memory_ops.py` の日本語セクション名など「JA 工程ドキュメントを生成する定数」は JA 維持**（英語化しない）。英語化した実行時メッセージを参照する内部テストは追随更新（例 `test_intent_session`）。
- **出典**: `mcp/`・`scripts/`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §15

### MEM-20261028-035

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2a b1b 完了（`intent_catalog.py` の description・phase goal/exit_criteria → EN）。**`mcp/` は完了**（残 JP は `memory_ops.py` の JA 工程ドキュメント生成定数のみ＝意図的）。残 b2 `scripts/*.py`・b3 shell。
- **出典**: `mcp/intent_catalog.py`・`internal/tests/test_intent.py`

### MEM-20261028-036

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2a b2a 完了（小スクリプトの docstring/comment/生成文を English、`CAPABILITIES.md` 再生成）。**パーサ用キーワード（`## タスク`・`## バックログ`・`## 目次`・regex の日本語選択肢）と JA テンプレに一致するテスト fixture は維持**（英語化しない）。残 b2b（gen_router/install_global）・b2c（plan_l2_backlog/e2e_flows）・b3 shell。
- **出典**: `scripts/`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §15

### MEM-20261028-037

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: OS-2a b2b 完了（`gen_router.py` の ROUTER 内容を English 化＝生成 `ROUTER.md` も英語。`install_global.py` の docstring/help を English）。残 b2c（`plan_l2_backlog.py`・`e2e_flows.py`）・b3 shell。
- **出典**: `scripts/gen_router.py`・`scripts/install_global.py`

### MEM-20261028-038

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-2a 完了**。公開コード（`mcp/`・`scripts/*.py`・shell）のコメント/docstring/メッセージ/workflow description を English 化。生成 `ROUTER.md` も英語。**意図的に JA を残す**: memory の JA 工程ドキュメント生成定数（`memory_ops` セクション名）、パーサ用キーワード（`## タスク`・`## バックログ`・`## 目次`・regex 日本語選択肢）、JA テンプレに一致する E2E fixture。
- **出典**: `mcp/`・`scripts/`・`internal/docs/plans/PROGRAM-opensource-hardening.md` §15

### MEM-20261028-039

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-1a 完了**。`intent_session` を**永続化**し、MCP 再起動後にアクティブ workflow とツールゲートを**復元（resume）**。保存先は `data/intent_session.json`（`WAWOO_INTENT_SESSION` で上書き・TTL 12h・atomic write・corrupt 時は無視）。`workflow_clear` でファイル削除。e2e は `mcp_call` ごとに session を隔離（ゲート持ち越し防止）。テスト `test_session_persists_across_restart`。
- **出典**: `mcp/intent_session.py`・`internal/tests/test_intent_session.py`・`scripts/e2e_flows.py`・`.gitignore`

### MEM-20261028-040

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-1d 完了**。委譲の**所有権/abort 契約**を明文化: サブタスクは生成した呼び出し／phase が所有。foreground はターンとともに abort、background はターン外へ生存し追跡＋後始末。abort は**下から上へ**伝播。`delegate_subtask` は**指示のみ**を返し実行はホスト（IDE Task）、親は続行前に結果検証。追記先: `mcp/README`・`AGENTS.md §4.1`・`docs/INTENT-ROUTING §7`（各 EN/JA）。
- **出典**: `mcp/README.md`・`AGENTS.md`・`docs/INTENT-ROUTING.md`

### MEM-20261028-041

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-1e 完了**。`AGENTS.md` §5 に**先回り圧縮**（予算前に自然な区切りで compact・要点は handoff/memory・履歴は検索可能なまま）、§4.1 に**ボード＝committed state＋差分**（後発参加者は現況→`since` カーソル、投稿は実質更新のみ）を EN/JA で明文化。
- **出典**: `AGENTS.md`・`AGENTS.ja.md`

### MEM-20261028-042

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-1b 完了**。`CAPABILITIES.md` に **size 列**（entry `SKILL.md` の KB、生成）を追加し見出しを英語化。`validate_assets.py` に `skill_budget_warnings()`＝**4KB 超を WARN**（例外: `imagegen-frontend-mobile`・`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents`）。現状 11 件が 4KB 超（第三者系が中心）→ 可視化のみ、失敗にはしない。
- **出典**: `scripts/gen_capabilities.py`・`scripts/validate_assets.py`・`.kilo/CAPABILITIES.md`

### MEM-20261028-043

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-1c 完了**。全 command に **`replay: safe|unsafe`** を付与（`incident-response`=unsafe、他 14=safe）。`validate_assets.py` が未指定/不正を **FAIL**（`command_replay_issues`）。`delegate_subtask` に **`idempotency_key?`** を追加し payload に反映（`intent_delegation`・`server` schema）。`AGENTS.md` §4.1（EN/JA）に**リプレイ安全規則**を明文化（unsafe は冪等キー、自動再実行は safe のみ）。
- **出典**: `.kilo/commands/*.md`・`scripts/validate_assets.py`・`mcp/intent_delegation.py`・`mcp/server.py`

### MEM-20261028-044

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-7 完了**。MCP に **`steer_task`** を追加（`mcp/intent_steer.py`）。実行中計画（`docs/plans/BACKLOG.md`/`ACTIVE.md`）を文脈に `amend` を返す。`op`（add/reorder/reprioritize/scope_change/abort）指定時は適用指示、未指定時は **`needs_classification`** を返しホスト LLM が分類→再呼び出し。**MCP は計画ファイルを書かない**（ホストがステップ境界で適用）。ゲート中も呼べる（`_GATE_EXEMPT` に追加）。
- **出典**: `mcp/intent_steer.py`・`mcp/server.py`・`mcp/intent_session.py`・`docs/INTENT-ROUTING.md`

### MEM-20261028-045

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-11 完了**。`project-manager`・`delivery-lead` に **Supervision loop** を明示化（Goal→Success（証拠）→Next→Consistency→Amend via `steer_task`）。**PM＝計画/backlog/順序**、**Delivery Lead＝実行監督**。承認ゲートで停止。
- **出典**: `.kilo/agents/project-manager.md`・`.kilo/agents/delivery-lead.md`

### MEM-20261028-046

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-12 完了**。`delegate_subtask` に **`model_tier?`（`fast`/`reasoning`）** を追加（payload に反映）。方針: 機械的ステップ=高速/安価、計画・検証=推論。`AGENTS §4.1`（EN/JA）・`mcp/README`（EN/JA）に記載。
- **出典**: `mcp/intent_delegation.py`・`mcp/server.py`・`AGENTS.md`

### MEM-20261028-047

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **OS-13 完了**。evidence ログ命名を `e2e-run-` → **`wawoo-e2e-<UTC>.log`** に統一。`CHANGELOG.md` 冒頭に「日本語のプロジェクト記録・版の正本は `VERSION`」を明記。
- **出典**: `internal/scripts/e2e/e2e_with_evidence.sh`・`CHANGELOG.md`

### MEM-20261028-048

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: コード監査指摘への対応。 (1) session 永続化は**最小フィールドのみ**（`workflow`/`agent`/`mcp_tools_allow`/`command_path`/`delegation_hint`/`intent_id`）で**本文 `prompt`/`clean_text` を保存しない**。(2) resume は **`WAWOO_INTENT_RESUME`（既定 off）** で明示化（無断 resume・複数クライアント混線の回避）。 (3) `validate_assets` の memory 境界 regex を厳密化（`TEMPLATEX.md` を検出、`*.ja.md` は許可）。 (4) `replay` 検査は `agent:` を持つ workflow のみ。 (5) 予算 WARN を 1 行に集約。 (6) 永続化/読込失敗を stderr に記録。
- **出典**: `mcp/intent_session.py`・`scripts/validate_assets.py`・`docs/INTENT-ROUTING.md`・`mcp/README.md`

### MEM-20261028-049

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: (1) 既定 agent を **`wawoo-router` → `wawoo-auto`** に改名（`kilo.json` default_agent・`install_global.py` 既定・`CAPABILITIES`/`ATTRIBUTION`/`USAGE`/`AGENTS`）。※グローバル配置は `install_global.py` 再実行で反映（要承認）。(2) session 永続: resume は**既定 off**（`WAWOO_INTENT_RESUME=1` で有効・無効時は書込なし）、`WAWOO_INTENT_CLIENT` で**クライアント別ファイル**。TTL/多重クライアント/resume-off テスト追加。(3) Cursor ルール最新化（`wawoo-auto`・MCP ツール・replay）。(4) **OpenCode 対応**: `docs/USAGE` EN/JA に `opencode.json` MCP 設定例＋E2E `opencode_stdio_contract`（stdio handshake＋tools/list）。
- **出典**: `kilo.json`・`scripts/install_global.py`・`mcp/intent_session.py`・`docs/USAGE.md`・`scripts/e2e_flows.py`

### MEM-20261028-050

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: (1) **OpenCode 実接続を検証**：`opencode` 1.18.34 が `/root/.opencode/bin/opencode` に導入済み。プロジェクト `opencode.json` の `mcp` に kit を local 登録 → `opencode mcp list` で **`wawoo-skills ✓ connected`**。`.cursor` 相当のフォルダは **MCP＋AGENTS.md 運用では不要**（ネイティブ agent/command を使う場合のみ `.opencode/` 任意）。(2) **創作系アセット調査**：MIT（skills-main）の `writing-fragments`/`writing-beats`/`writing-shape`（探索→ビート→記事化）、Apache-2.0（OpenDesign）の `article-magazine`/`blog-post`（HTML レイアウト）。`content-research-writer` は **NOASSERTION＝不採用**。**小説・脚本・脱口秀の専用 skill はローカルに友好ライセンスで無し**。
- **出典**: `opencode mcp list`（実測）・`/home/git/zen-router/docs/60-research/{skills-main,open-design-main}`

### MEM-20261028-051

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: **`/writing` workflow と MIT の筆記 skill を吸収**。`writing-fragments`（explore）→`writing-beats`（構成）→`writing-shape`（執筆）を `.kilo/skills/` に追加（SFE/MIT・帰属維持）。`.kilo/commands/writing.md`（agent=docs-specialist・replay=safe）を新設し、`intent_catalog` の `WORKFLOWS`/`WORKFLOW_PHASES`/`PHASE_OVERRIDES` に `writing` を登録。`/content-delivery-lite` に並行利用の注記。**skills 60・workflows 16**、`ATTRIBUTION`（SFE 24）・各 docs/Cursor 更新。
- **出典**: `.kilo/skills/writing-*`・`.kilo/commands/writing.md`・`mcp/intent_catalog.py`・`.kilo/skills/ATTRIBUTION.md`

### MEM-20261028-052

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 創作系を**比較・選定**して吸収。**採用**: `writing-fragments/beats/shape`（SFE/MIT）、`teach`（SFE/MIT・予算例外）、オリジナル `science-writing`（科普）・`viral-hooks`（人气）、既存 `marketing-psychology`（Apache）。**不採用**: `science-writer`（nobodyonlyc＝LICENSE 実物無し・自動生成巨大 repo）、`scientific-writing`（K-Dense＝学術向けで過剰）、`writing-in-the-sciences`/`content-writer`（重複）、`content-research-writer`（NOASSERTION）。**skills 63**。`/writing` に **general/science/viral モード**。
- **出典**: `internal/docs/plans/PROGRAM-opensource-hardening.md` §16・`.kilo/skills/{teach,science-writing,viral-hooks}`・`docs/USAGE`
