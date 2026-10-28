# Pi Durable 方法論の吸収分析（research note）

> **種別**: 調査ノート（分析のみ。コード変更なし）。
> **出典**: Pi Durable — https://earendil.com/posts/pi-durable/（記事日付 2026-10-01・**experimental**）
> **調査日**: 2026-10-28。**事実**（一次情報・本リポジトリの実測）と**推測**（本キットへの写像・効果予測）を分離して記す。

---

## 0. 目的

外部ハーネス「Pi Durable」の方法論を一次情報から読み、wawoo-skills が**吸収できるもの**と**領域外**を切り分け、採用優先度を決める。

## 1. 事実 — Pi Durable の主張（記事より）

- **harness = storage ＋ LLM 会話を並列実行する機構**（tools ＋ 実行環境）。**モデル呼び出しから tool 実行まで、すべてが task**で、進む前に checkpoint を保存する。
- **クラッシュ耐性**: 再起動後に同一 storage を開き、未完了 task を最後の checkpoint から継続。中断されたモデル要求は再送し、部分回答は aborted として保持。tool は `replay: "safe"` のときだけ再実行。**送信は `requestId` で exactly-once**。
- **compaction も task**（turn 境界で背景実行）。古いメッセージは**削除せず検索可能**。`reset()` / handoff でも履歴を保持。
- **extension = システムプロンプト section ＋ tools ＋ hooks ＋ tasks**。会話は**コードではなく名前だけ**を保存 → ホットスワップ・更新追従。プロンプトは毎リクエスト再構築。
- **task と会話が一つの ownership tree**。abort は下から上へ伝播。foreground / background を区別。
- **アプリ状態は transcript の隣の typed document**として、**同一 atomic commit** で更新（状態と transcript が食い違わない）。
- **多クライアントが attach**して現況＋差分を受け取り、介入できる。**エージェントが理解できるよう設計**（≈15k 行＝トークン量を明示、storage backend はスキップ可）。
- FAQ: **TypeScript は bootstrap のため**（「Rust 等への移植は容易」）。

## 2. 事実 — wawoo-skills の現状（実測）

| 項目 | 現状 | 根拠 |
|---|---|---|
| 実装 | MCP サーバ＋保守スクリプトは **Python 3 stdlib のみ**（依存ゼロ・stdio） | `mcp/*.py`・`scripts/*.py` |
| ルーティング session | **in-memory**（`_active`）。MCP 再起動で workflow 選択とツールゲートが消える | `mcp/intent_session.py:16` |
| 学習データ | SQLite（永続） | `mcp/intent_learned_store.py`（`sqlite3`） |
| コンテキスト予算 | §5 の**散文**。資産単位のコスト指標は無い | `AGENTS.md` §5・`.kilo/CAPABILITIES.md` |
| 委譲 | `delegate_subtask {background}` はあるが abort/所有権の**契約は未文書** | `mcp/intent_delegation.py`・`mcp/README.md` |
| 協調 | board は `since` cursor で差分読み（＝committed state ＋ delta に近い） | board ツール仕様 |
| handoff | `handoff` skill・`/compact` はあるが「先回り圧縮」「履歴可検索」は未明文化 | `.kilo/skills/handoff/`・`AGENTS.md` §5 |

## 3. 分析 — 吸収候補（推測を含む）

| # | Pi Durable の原則 | 本キットへの写像 | 吸収 |
|---|---|---|---|
| A | storage を開いて未完 task から再開 | `intent_session._active` を `data/` に永続化し再起動後に resume | **する（最優先）** |
| H | agent-legibility を数値で測る | 資産ごとのサイズを `CAPABILITIES.md`/`validate_assets` に表示し予算超過を検出 | **する** |
| B | `requestId` exactly-once／`replay:"safe"` | workflow step の rerun 安全性分類＋副作用操作に冪等 key＋承認 | **する** |
| C | ownership tree と abort 意味論 | 委譲の foreground/background・abort 伝播を契約化（§4.1 と接続） | **する** |
| F | compaction を背景化・履歴保持 | `handoff`/§5 に「先回り圧縮」「履歴は削除せず検索可」を追記 | **する（軽）** |
| G | committed state＋差分配信 | board の「current view 摘要＋差分」を明文化 | **する（軽）** |
| D | コードでなく名前を保存・ホットスワップ | `install_global` ミラー＋同名置換で概ね一致。ただしプロンプトは起動時キャッシュ＝再起動要 | **原則のみ／ほぼ parity** |
| E | app state と transcript の原子整合 | SSOT（`ACTIVE`/`memory`/`plans`）は手動更新で原子的でない | **原理のみ**（fork は不要） |

## 4. 採用優先度（決定）

```
A（実バグ級: 再起動で session 消失）
  → H（可測性）
    → B/C（契約の明確化）
      → F/G（ドキュメント微調整）
D/E は並行または原理のみ
```

- **A**: 「再起動後に workflow ゲートと選択が消える」は**実際の欠陥**。最優先。
- **H**: 予算を測定可能にし、選択を客観化（“安い候補から”）。
- **B/C**: 再試行安全性・委譲ライフサイクルを契約として固定。
- **F/G**: 既存資産の文言追補。低リスク。
- **D/E**: 領域差・原理差が大きく、実装の費用対効果が低い。

## 5. 期待される能力向上（推測）

| 能力 | Before | After | 由来 |
|---|---|---|---|
| 持久ルーティング | 再起動で session 消失 | 再起動後も resume | A |
| ゲート完整性 | 再起動で門が消え逸脱しうる | 門が復元し強制継続 | A |
| 文脈予算の自動検証 | 散文のみ | 資産コスト可視化・超過検出 | H |
| 再試行安全性 | 概念なし（副作用が重複しうる） | step 分類＋冪等 key | B |
| 委譲ライフサイクル | 契約未文書 | foreground/background・abort 伝播を明文化 | C |
| 長時間セッション持続 | 強制時のみ圧縮 | 先回り圧縮・履歴可検索 | F |
| 後発参加のオンボーディング | cursor 差分読み | current view＋差分モデル | G |

**横断効果**: kit の中核目的（「能力はあるのに呼ばれない」）に対し、**軌道がセッションを越えて持続**するため長会話・再起動時のルーティング漏れが構造的に減る。可測性（H）で予算超過を CI/CLI で検出できる。可搬性は不変（A/H は stdlib の JSONL/SQLite で実現可・**Python 継続**）。

## 6. 領域外（誇張しない）

- **プロセス実行レベルの checkpoint/resume**（モデル/tool 呼び出しの中断再開）は**ホスト（Kilo/Cursor）の責務**。MCP では制御できず、本キットは**変わらない**。
- **多クライアント UI の `watch()` ストリーミング**・**storage backend 差し替え**は成果物（Markdown/MCP）の領域外。
- **runtime としての並列実行**は持たない（wawoo-skills は常にルーティング＋契約層）。

## 7. 検証（採用時）

- A: `mcp/test_server.py`＋`scripts/e2e_flows.py` に「再起動後に gate/session 復元」往復テスト。
- H: `scripts/validate_assets.py` にサイズ指標（超過→非ゼロ or WARN）。
- B/C/F: workflow/skill 契約に明文化し、`scripts/validate_assets.py` で参照整合を検査。
- 既存ゲート維持: 未収束 `FAILED = 0`・`python3 scripts/plan_active.py docs/plans/ACTIVE.md` 通過。

## 8. 未決 / 次アクション

- [ ] A: `intent_session._active` の永続化方式（JSONL か SQLite か）と resume の UX（`workflow_clear` 以外に `workflow_resume` を足すか）。
- [ ] H: サイズ指標の単位（KB / 概算 token）と閾値。
- [ ] B: rerun 安全フラグの付与先（command frontmatter か skill か）。
- [ ] C: abort 契約の記述先（`AGENTS.md` か `mcp/README.md` か）。
