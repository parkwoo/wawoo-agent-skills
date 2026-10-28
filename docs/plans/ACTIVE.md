# ACTIVE — 進行中タスク（SSOT）

> **エージェント**: 作業前に本ファイルを読む。完了時のみ行を更新する。利用者が **git commit を依頼していない**限りコミットしない。

## メタ

| 項目 | 値 |
|------|-----|
| 儀式レベル | L1（例。小改は L0、issue 運用は L2） |
| 入口ワークフロー | `/delivery-lite`（Cursor: `@.kilo/commands/delivery-lite.md`） |
| 最終更新 | 2026-10-28 |

## 状態

`todo` → `doing` → `done`（例外: `blocked`）

- **同時に `doing` は 1 件まで**
- `done` には **証拠**（実行したコマンド、または変更ファイルパス）を 1 行以上
- タスクの完了は **memory に書かない**（memory は決定・制約・落とし穴のみ）

## タスク

| id | status | 内容 | 完了条件 | 証拠 |
|----|--------|------|----------|------|
| rel-0.6.0-T7 | done | e2e `l0_simulated_flow` が実 ACTIVE.md の空を要求する不具合を修正（合成ファイルへ） | `e2e_flows` 全 pass | `scripts/e2e_flows.py` → passed=27 failed=0 |
| rel-0.6.0-F1 | done | バージョン定版: `VERSION`=0.6.0、CHANGELOG `[Unreleased]`→`[0.6.0]` | VERSION と CHANGELOG が一致 | `VERSION`=0.6.0；`CHANGELOG.md` `## [0.6.0] - 2026-10-28` |
| rel-0.6.0-F3 | done | `ATTRIBUTION.md` 更新（agents 22・`wawoo-router` 登記） | 件数が実体と一致 | `.kilo/skills/ATTRIBUTION.md` agents（22）＋`wawoo-router` |
| rel-0.6.0-F4 | done | 顶层 `NOTICE` 追加（Apache-2.0 帰属の集約） | NOTICE 存在・LICENSES と整合 | `NOTICE`（Kilo Marketplace/OpenDesign 帰属 → `LICENSES/`） |
| rel-0.6.0-F5 | done | `SECURITY.md` 追加（脆弱性報告窓口） | SECURITY.md 存在 | `SECURITY.md`（GitHub Security Advisories） |
| rel-0.6.0-F6 | done | `safe_read` のパス判定を `Path.is_relative_to` へ | 境界テスト／既存テスト pass | `mcp/server.py:142`；sibling パス拒否テスト OK／pytest 20 passed |
| rel-0.6.0-F7 | done | `intent_receiver` socket を `chmod 600`・`XDG_RUNTIME_DIR` 優先 | 権限 0o600 を確認 | `mcp/intent_receiver.py`；実測 socket mode 0o600 |
| rel-0.6.0-F2 | doing | 承認後 `git push origin master` ＋ `v0.6.0` tag | 远端・tag を検証 | `origin/master`=`d6d4471`、`refs/tags/v0.6.0` 有り（`v0.1.0` も push 済） |
| rel-0.6.0-F2b | blocked | 歴史 tag `v0.2.0`・`v0.3.0`・`v0.4.0` の push | `workflow` scope 付き認証で push し远端 tag を確認 | push 拒否: `! [remote rejected] … without workflow scope`（tag の履歴に `.github/workflows/validate.yml` を含むため） |

## 詳細計画（任意）

- （`docs/plans/<name>.md` へのリンク。無ければ空）
