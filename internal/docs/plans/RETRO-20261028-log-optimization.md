# L3 振り返り・PDCA — kilo ログ分析に基づく実行効率改善

- **id**: `self-improve-20261028-log-optimization`
- **入口**: `/self-improve`（L3 プロセス改善。SSOT は本ファイル＋`docs/memory/`）
- **詳細計画**: `docs/plans/self-improve-20261028-log-optimization.md`
- **日付**: 2026-10-28

## ベースライン

- 対象: kilo エンジン run `c956c7f2`（2026-10-28 05:21〜）の 5 セッション、283 tool calls、cache_read 約 7.4M。
- 出発点の指標（`kilo.db` の `part.data` と `opencode.log` から実測）:
  - read-only subagent の単発 `read` 最大 **53KB**、子 1 体の cache_read **1.7–2.5M**。
  - 監査 1 チェーンの `skill_get` **16**（うち約 12 は親子で重複）。
  - 権限拒否等の無駄呼び出し **約 8**（`background_process` 拒否 4、不在ファイル read 3、grep 65536B 1）。
  - snapshot の stale `index.lock` による WARN **2**。
  - read-only 時に無効な `memory_save` **1**、当該依頼の `interpret_intent` 往復 **2**。

## 実施（Do）

1. read-only subagent 6 件（security-reviewer / accessibility-reviewer / architect /
   performance-reviewer / product-owner / docs-localization-reviewer）に「実行効率（トークン衛生）」節を追加。
2. `AGENTS.md` §4.1 に「サブエージェント委譲の効率」（skill 重複排除・read 行範囲・`background_process` 回避）を追加。
3. `security-reviewer.md` の `permission.bash` を read-only サブセット許可へ（`*` は deny、`edit` は deny 維持）。
4. `mcp/server.py` の `capabilities` が read-only 時に `memory_save` 無効を明示。
5. `mcp/intent_catalog.py` の `self-improve` トリガ語に log/呼び出し状況の語を追加し、`ROUTER.md` を再生成。
6. `scripts/kilo_snapshot_gc.sh` を追加（dry-run 既定・`--apply` で stale lock 除去＋`git gc --auto`）。
7. （検証で発見）pytest 収集時の学習ストア非隔離を `mcp/conftest.py` の autouse フィクスチャで隔離。

## 証拠（Check）

- `python3 scripts/validate_assets.py` → `OK: skills=55 agents=22 commands=15`（exit 0）
- `python3 -m pytest mcp/ -q` → **20 passed**（修正前: `test_trigger_classifier_ja` が 1 failed）
- `python3 mcp/test_intent.py` → `intent tests: OK`
- `python3 scripts/e2e_flows.py` → `passed=26 failed=1`（`l0_simulated_flow` は ACTIVE.md 追加行が原因 → 行を除去して修正、下記）
- `scripts/kilo_snapshot_gc.sh --apply` → `locks=1 skipped=0 gced=24`、`find … index.lock | wc -l` → **0**
- `gen_capabilities.py` / `gen_router.py` → 再生成 OK（`ROUTER.md` 4093B/67 行）

## 決定（Act）

- **標準化**: 上記の agent 節・AGENTS §4.1・MCP capabilities 告知・snapshot GC をキット標準に採用。
- L3 の SSOT は本 RETRO と `docs/plans/self-improve-20261028-log-optimization.md`。
  ACTIVE（L1）は増やさない（`l0_simulated_flow` は ACTIVE が空であることを要求）。
- ロールバック: agent `permission`／トリガ語は `git` 差分で戻せる。commit は利用者確認後。

## 次ステップ

- 担当: kit メンテナ（delivery-lead / sre-operator）。期限: 2026-11-04。
- 次回レビュー: 同一分析スクリプトで `c956c7f2` 以降を再計測し、
  p95 `read` < 4KB、監査チェーンの `skill_get` ≤ 6、拒否呼び出し 0 を確認する。
