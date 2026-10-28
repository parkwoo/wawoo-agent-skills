# 計画: kilo ログ分析に基づく実行効率の改善（self-improve）

- **id**: `self-improve-20261028-log-optimization`
- **儀式レベル**: L3（プロセス改善／キット改善）
- **入口**: `/self-improve`（repo: wawoo-skills）
- **作成日**: 2026-10-28
- **証拠（分析元）**: `run=c956c7f2`（kilo エンジン 2026-10-28 05:21〜）の 5 セッション、
  `kilo.db` の `part.data` と `/root/.local/share/kilo/log/opencode.log`（詳細は末尾「証拠」）。
- **関連**: `AGENTS.md` §4.1、`.kilo/agents/security-reviewer.md`、`mcp/server.py`、`mcp/intent_catalog.py`

## 目的

run `c956c7f2` の計測（283 tool calls、cache_read 約 7.4M）で判明した**明確な浪費**を、
キット側（agent 定義・MCP・スクリプト・トリガ）の決定論的な修正で削減する。
「推測で改善したと言わない」ため、各項に**指標**を付す。

## 改善項目（担当・指標・期限）

| # | 改善 | 担当（role/agent） | 指標（Before → Target） | 期限 | 状態 |
|---|------|--------------------|--------------------------|------|------|
| 1 | 読み取り衛生: `grep -n`→`sed -n`/行範囲 read、1 step < 4KB | security-reviewer ほか read-only subagent | 単発 read 出力 53KB → p95 < 4KB、子 1 体の cache_read ≥30% 減 | 2026-11-04 | done |
| 2 | skill 重複排除: 親が要点を渡したら再 `skill_get` しない | workflow（release-review 等）＋全 subagent | 1 監査チェーンの `skill_get` 16 → ≤6 | 2026-11-04 | done |
| 3 | `background_process`/shell: read-only subagent に read-only bash を許可、短命令は 1 回で | security-reviewer ほか read-only subagent | 拒否された tool call 4 → 0 | 2026-10-31 | done |
| 4 | snapshot の stale `index.lock` 清掃＋GC | sre-operator（脚本） | snapshot 書き込み WARN 2 → 0 | 2026-10-31 | done |
| 5 | `memory_save` 可否の自己申告（read-only 検知） | MCP（server.py `capabilities`） | read-only 時の無効 `memory_save` 呼び出し 1 → 0 | 2026-10-31 | done |
| 6 | L1 トリガ語: log/呼び出し状況の語を追加 | MCP（intent_catalog） | 当該依頼の `interpret_intent` 2 往復 → 1 往復 | 2026-10-31 | done |

> **検証結果（2026-10-28）**: `validate_assets` OK／`pytest mcp/` 20 passed／`e2e_flows` 27 passed 0 failed／
> `plan_l3_record` OK／snapshot GC `locks=1 gced=24`→lock 0／MCP live: `capabilities` に read-only 注記、
> `interpret_intent("查看kilo的log…调用状况")` が `self-improve / trigger / L1`（1 往復）に確定。
> 副次修正: pytest 収集時の学習ストア非隔離（`mcp/conftest.py`）。詳細は `RETRO-20261028-log-optimization.md`。

## 実装（Do）

1. **Item 1/2**: read-only subagent（security-reviewer / accessibility-reviewer / architect /
   performance-reviewer / product-owner / docs-localization-reviewer）に「実行効率（トークン衛生）」
   節を追加。`AGENTS.md` §4.1 に read-only subagent の read 規律と skill 重複排除を追記。
2. **Item 3**: `security-reviewer.md` の `permission.bash` を read-only サブセット許可へ変更
   （`git status/log/diff/show/rev-parse/ls-files`・`ls`・`rg`・`grep`・`find` のみ／`*` は deny）。
3. **Item 4**: `scripts/kilo_snapshot_gc.sh` を追加（既定 dry-run、`--apply` で stale lock 除去＋`git gc --auto`）。
4. **Item 5**: `mcp/server.py` の `do_capabilities` が read-only 時に `memory_save` 無効を明示。
5. **Item 6**: `mcp/intent_catalog.py` の `TRIGGER_KEYWORDS["self-improve"]` に
   `日志分析`・`调用状况`・`调用排查`・`运行排查`・`invocation status`・`call status` 等を追加。
   `scripts/gen_router.py` で `ROUTER.md` を再生成（発火語の正本は intent_catalog）。

## 検証（Check）

- `python3 scripts/validate_assets.py`（name=dir・参照・JSON）
- `python3 -m pytest mcp/ -q`（intent/session/memory/server テスト）
- `python3 scripts/e2e_flows.py`（L0–L3 シミュレーション）
- Item 4: `scripts/kilo_snapshot_gc.sh`（dry-run→`--apply`）で stale lock 0 を確認
- Item 5/6: MCP 再起動後に `capabilities`／`interpret_intent` を再実行して挙動確認
- **再チェック**: 同一分析スクリプトで `c956c7f2` 以降の tool/read/cache_read を再計測

## リスク・ロールバック

- agent `permission` 変更はガードレール（read-only 性）に触れる。許可は**非破壊コマンドのみ**で、
  `edit: deny` は維持。問題時は当該 agent の `permission` を元に戻す。
- トリガ語追加は誤ルーティングを招きうるため、既存テスト（`test_trigger_classifier_*`）を必ず通す。
- すべて `git` 差分で戻せる（利用者確認まで commit しない）。

## 証拠（Analysis baseline / 2026-10-28）

| 対象 | tools | read | 最大 read | cache_read | 備考 |
|------|------:|-----:|----------:|-----------:|------|
| `…4RqbWV`（監査 父, wawoo-router） | 13 | 0 | — | 345k | skill_get×4→子で再取得 |
| `…7p6S1T`（security-reviewer） | 83 | 53 | **53KB** | 2.51M | background_process 拒否×1 |
| `…Ce9bW3`（security-reviewer） | 78 | 55 | 25KB | 1.79M | 拒否×2、.git/packed-refs 不在×1 |
| `…cLVMQQ`（security-reviewer） | 85 | 51 | 25KB | 1.75M | 拒否×2 |
| `…QnAEzOY`（本調査） | 24 | 0 | — | 1.00M | 無効 memory_save×1、重複クエリ×1、interpret 2 往復 |
| run 内 WARN | — | — | — | — | snapshot `index.lock` 競合×2 |

- 検出コマンド例: `grep -cE "permission=wawoo-skills_[a-z_]+ " opencode.log`、
  `SELECT json_extract(data,'$.tool') ... FROM part WHERE data LIKE '%"tool":"wawoo-skills_%'`。
