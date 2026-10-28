# L2 バックログ（内部・非公開）

**SSOT**: issue tracker 未設定のためローカル代替。`docs/plans/BACKLOG.example.md` 形式。
計画詳細: `internal/docs/plans/PROGRAM-opensource-hardening.md`

## 運用ルール

- **追記（append-only）**: 新指示は行を**追加**する。既存行の内容は上書きしない。置換は「置換」と明記して残す（例: OS-3a → OS-3b）。
- **優先度＝行の順序**。**順序は依存（`depends` 列）から自動検証**される。人の記憶に頼らない。
- **並べ替えは `--apply` で自動**: `python3 scripts/plan_l2_backlog.py internal/docs/plans/BACKLOG.md --apply`（内容・証拠は不変）。
- `status`: `open` → `in_progress`（同時 1 件）→ `done`（証拠必須）／`blocked`。
- **決定（D1–D7）は `depends` に書かない**（issue id のみ）。決裁は title/evidence に記す。

## バックログ

| issue | status | title | evidence | depends |
|-------|--------|-------|----------|---------|
| OS-8 | done | 言語ポリシー 3 層（コード=EN／工程ドキュメント=JA／説明=EN+JA）を AGENTS/skill/workflow に追加（agent は契約 `AGENTS.md §1`＋`ROUTER.md` 経由で適用） | `AGENTS.md` §1（3 層表）；`.kilo/skills/language-policy/SKILL.md`；`scripts/gen_router.py`（ROUTER に言語ポリシー行）；counts 56；`validate_assets` OK／`e2e` 27/0 | — |
| OS-5 | done | ソース/テスト分離＋テスト非公開化＋CI 再設計＋追随更新 | D3 採用。`mcp/test_{server,memory_ops,intent,intent_session}.py`＋`conftest.py` → `internal/tests/`（`parents[2]` 修正・`test_memory_ops` に sys.path 追加）。CI=`validate_assets`＋e2e＋cli_adapters_mock。`install_global` のスモークを内部テスト任意化。`e2e_with_evidence.sh`→`internal/scripts/e2e/`。公開 docs は公開コマンドへ置換。検証: `pytest internal/tests`→20 passed／公開 CI 相当 green | — |
| OS-9 | done | 静的 trigger 撤去→learned seed＋upstream の動的ルーティング | D7 採用。`TRIGGER_KEYWORDS`/`WEAK_TRIGGERS`/`classify_by_trigger`/`TriggerMatch` を撤去（flag なし）。解決順=`slash→learned→upstream`。`mcp/intent_seed.py` が空 DB を catalog id で seed。旧語彙 150 件を**ローカル学習 DB へ移行（非配布）**。`gen_router.py` を「用途/説明」列へ。テスト書換。検証: `pytest internal/tests`→20 passed／`validate_assets` OK／`e2e` 27/0 | OS-5 |
| OS-3b | done | 日本語資産の英語化（自作 skill 7・第三者 skill 9・agents 6・commands 15＋`.cursor/rules` 3 → English） | JP(Hiragana/Katakana)残 0（上流 zh のみ）・`validate_assets` OK／`e2e` 27/0／`plan_l2_backlog` OK・`PROGRAM` §13 | — |
| OS-6 | done | 公開/非公開ドキュメントを実行可能資産化（特に PUBLICATION→skill/check） | `.kilo/skills/publication-boundary/SKILL.md`（新規）＋`scripts/validate_assets.py` `public_boundary_violations()`（公開ツリーへの内部混入を検知）。検証: `validate_assets` OK（violations=[]）／`e2e` 27/0／skills 57 | OS-8 |
| OS-2b | done | 公開ドキュメントの英日 2 種化（英主・日従、`NAME.md`+`NAME.ja.md`、`PROGRAM` §14 b1–b6b2） | README/AGENTS/USAGE/INTENT-ROUTING/VERSIONING/PUBLICATION/docs README/METHODOLOGY/PROCESS-PHILOSOPHY/SECURITY/plans README/mcp README/INTENT-RECEIVER を EN+JA。memory テンプレは機構で EN のみ。`validate` OK／`e2e` 27/0 | — |
| OS-2a | done | 公開コード（`mcp/`・`scripts/`・shell）のコメント/文字列を英語化（`PROGRAM` §15） | `mcp/` 全体・`scripts/*.py`・shell → English（残 JP は memory の JA 生成定数・パーサ用キーワード・JA fixture のみ＝意図的）。`pytest internal/tests` 20 passed／`validate` OK／`e2e` 27/0 | OS-5 |
| OS-1a | done | A: `intent_session` 永続化＋再起動 resume（+テスト） | `mcp/intent_session.py` に JSON 永続化（`data/intent_session.json`・`WAWOO_INTENT_SESSION` で上書き・TTL 12h・atomic write・corrupt 時は無視）。`activate/clear` で保存・削除、`_load` で resume。テスト `test_session_persists_across_restart`。e2e は呼び出し毎に session 隔離。`pytest internal/tests` 21 passed／`validate` OK／`e2e` 27/0 | OS-5 |
| OS-1d | done | C: 委譲の所有権/abort 契約を明文化 | `mcp/README.md`/`.ja`（所有権・abort 伝播・実行・後始末）、`AGENTS.md`/`.ja` §4.1、`docs/INTENT-ROUTING.md`/`.ja` §7 に追記。`validate` OK／`e2e` 27/0 | — |
| OS-1e | done | F/G: 先回り圧縮＋ボード current-view/差分（文書） | `AGENTS.md`/`.ja` §5（先回り圧縮・履歴は検索可能なまま）・§4.1（ボード＝committed state＋差分・後発参加者は since カーソル）。`validate` OK／`e2e` 27/0 | — |
| OS-1b | done | H: コンテキスト予算の可測化（size 指標＋検証） | `gen_capabilities.py` に **size 列**（entry `SKILL.md` の KB）を追加し `CAPABILITIES.md` を英語見出しで再生成。`validate_assets.py` に `skill_budget_warnings()`（4KB 超過を WARN・例外 `imagegen-frontend-mobile`/`ask-matt`/`wayfinder`/`design-brief`/`writing-for-agents`）。検出 11 件。`validate` OK／`e2e` 27/0／`pytest` 21 passed | OS-5 |
| OS-1c | done | B: rerun 安全性分類＋副作用の冪等キー | 全 command に `replay: safe|unsafe`（`incident-response`=unsafe）を追加、`validate_assets` が未指定/不正を FAIL。`delegate_subtask` に `idempotency_key?`（`intent_delegation`/`server`/schema）を追加し payload へ反映。`AGENTS §4.1`（EN/JA）にリプレイ安全規則を明文化。テスト追加。`pytest` 21 passed／`validate` OK／`e2e` 27/0 | OS-1a |
| OS-7 | done | ルーティングに amend 意図種別と実行計画を文脈にした解釈（ステアリング/replan） | `mcp/intent_steer.py`（`build_steer_payload`・plan context）＋ MCP `steer_task`（`op` 無しは `needs_classification`、計画ファイルは書かない）。ゲート中も許可（`_GATE_EXEMPT`）。`AGENTS`/`INTENT-ROUTING`/`mcp/README`（EN/JA）に amend 契約。テスト `test_steer_payload`。`pytest` 22 passed／`validate` OK／`e2e` 27/0 | OS-1a, OS-9 |
| OS-11 | done | PM/Delivery Lead による監督ループの明示化（目標分解・段階監視・一貫性） | `project-manager.md`・`delivery-lead.md` に **Supervision loop**（Goal/Success/Next/Consistency/Amend）を追加。PM=計画・順序、Delivery Lead=実行監督。`validate` OK／`e2e` 27/0 | — |
| OS-12 | done | モデル階層・コスト方針（機械的=高速／計画・検証=推論）を委譲・ルーティングに導入 | `delegate_subtask` に `model_tier?`（`fast`/`reasoning`、`intent_delegation`/`server` schema・payload 反映）。`AGENTS §4.1`（EN/JA）に方針、`mcp/README`（EN/JA）に引数。テスト追加。`pytest` 22 passed／`validate` OK／`e2e` 27/0 | — |
| OS-13 | done | 低優先の追補: `CHANGELOG`/`VERSION` の言語・版、`wawoo-*.log` 命名規約 | evidence ログ prefix を `e2e-run-`→`wawoo-e2e-` に統一（`internal/scripts/e2e/e2e_with_evidence.sh`・内部手順）。`CHANGELOG.md` 冒頭に言語（日本語のプロジェクト記録）と `VERSION` 正本を明記。`validate` OK／`e2e` 27/0 | — |
| OS-10 | done | バックログの依存解決・順序検証・自動整列をスクリプト化（順序の二重管理を排除） | `scripts/plan_l2_backlog.py`（`validate_order`／`--apply`）；`python3 scripts/plan_l2_backlog.py internal/docs/plans/BACKLOG.md` → OK | — |
| OS-4 | done | `opencode.log` の用途調査（キット内に生成元なし＝ランタイム/OpenCode 側と判明） | `grep -rni opencode .kilo mcp scripts`（生成元 0 件） | — |

検証・整列: `python3 scripts/plan_l2_backlog.py internal/docs/plans/BACKLOG.md [--apply]`
