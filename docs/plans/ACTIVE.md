# ACTIVE — 進行中タスク（SSOT）

> **エージェント**: 作業前に本ファイルを読む。完了時のみ行を更新する。利用者が **git commit を依頼していない**限りコミットしない。

## メタ

| 項目 | 値 |
|------|-----|
| 儀式レベル | L1（例。小改は L0、issue 運用は L2） |
| 入口ワークフロー | `/delivery-lite`（Cursor: `@.kilo/commands/delivery-lite.md`） |
| 最終更新 | 2026-10-29 |

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
| docs-req-python3 | done | ランタイム前提（Python 3・stdlib のみ）を README／USAGE に明記（TS 化の代替＝選択肢 A） | README「前提条件」＋USAGE「0. 前提条件」が存在し Windows 手順を含む | `README.md`「前提条件（ランタイム）」＋`docs/USAGE.md`「0. 前提条件」；`CHANGELOG.md` `[Unreleased]` |
| pi-durable-absorption | done | Pi Durable 方法論の吸収分析を調査ノート化（優先度 A→H→B/C→F/G、D/E は領域外/原理のみ） | 調査ノート存在・事実/推測分離 | `internal/docs/design/PI-DURABLE-ABSORPTION.md`（内部・非公開）；出典 https://earendil.com/posts/pi-durable/ |
| internal-docs-boundary | done | 既存の内部開発資料を公開ツリーから除外（監査/RETRO/self-improve/E2E深さ/出版たたき台→`internal/`）、公開文書の内部参照を中和、`.gitignore`/`PUBLICATION.md` 更新 | `internal/` へ移動済み・公開文書に内部参照なし・`validate`/`e2e` pass | D=`docs/design/INTENT-RECEIVER-AUDIT.md`・`docs/plans/{RETRO,self-improve,E2E-WORKFLOW-COVERAGE}*.md`・`docs/blog/*`；`docs/PUBLICATION.md`・`.gitignore`・`docs/README.md`・`CHANGELOG.md`・`AGENTS.md` |
| internal-ssot-memory | done | `docs/plans/ACTIVE.md` と `docs/memory/*` の実体を非公開化（テンプレ `ACTIVE.example.md`・`INDEX.example.md` を公開）。CI を実ファイル非依存に | 実ファイル非公開・テンプレ公開・私的ファイル非在でも `validate`/`e2e`/`test_server`/`cli_adapters_mock` pass | `git rm --cached`（ACTIVE.md/INDEX/kit/general/deployment）＋`.gitignore`；`docs/plans/ACTIVE.example.md`・`docs/memory/INDEX.example.md`；`scripts/e2e_flows.py`（example 参照＋memory 隔離）；私的ファイル非在で e2e=27/0 |
| docs-author-audit | done | 公開ドキュメント監査（ベストセラー著者視点 F1–F11）の改善を公開文書へ適用（EN 主＋JA 対訳） | README/AGENTS/USAGE/METHODOLOGY/PROCESS-PHILOSOPHY/INTENT-ROUTING/PUBLICATION を更新・`validate_assets` pass | F1/F5/F11 `README.md:1-5`；F4/F6 同（向く人・2 分）；F3 `README.md`/`AGENTS.md:29`/`USAGE.md:15`；F2 5 文書に注記；F7 `docs/PUBLICATION.md:9`；F8 `README.md` Version；EN+JA 同期。監査: `internal/docs/audit/PUBLIC-DOCS-AUTHOR-AUDIT.md`；`python3 scripts/validate_assets.py` → `OK` |
| docs-public-surface | done | 公開面を縮小：設計/工程文書 5 種（EN+JA）を `internal/` へ移動し、公開参照を張り替え | 公開文書に内部参照なし・`validate`/`e2e` pass | M=`docs/METHODOLOGY.md`・`docs/PROCESS-PHILOSOPHY.md`・`docs/PUBLICATION.md`・`docs/README.md`・`docs/design/INTENT-RECEIVER.md`→`internal/docs/`；参照修正=README/AGENTS/USAGE/INTENT-ROUTING/plans README/mcp README/memory SKILL/ask-matt/publication-boundary；`scripts/e2e_flows.py` に `internal_doc()` スキップ；`validate_assets` OK・`e2e_flows` passed=28 failed=0 |

## 詳細計画（任意）

- （`docs/plans/<name>.md` へのリンク。無ければ空）
