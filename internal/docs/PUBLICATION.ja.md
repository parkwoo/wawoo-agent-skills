# 公開範囲（外部）と内部資産

## 外部（git 管理・クローンに含まれる）

利用者向けのキット本体:

- `README.md`、`AGENTS.md`、`docs/USAGE.md`、`docs/INTENT-ROUTING.md`、`docs/VERSIONING.md`、`SECURITY.md`、`CHANGELOG.md`（**日本語のプロジェクト記録**）、`VERSION`、`docs/memory/TEMPLATE.md`・`MEMORY-TOOLS.md`・`INDEX.example.md`、`docs/plans/README.md`・`*.example.md` — 説明文書には `*.ja.md` の対訳も含む
- `.kilo/`（skills / agents / commands）、`.cursor/rules`、`mcp/`
- `scripts/validate_assets.py`、`scripts/gen_capabilities.py`
- `.github/workflows/`（資産・MCP スモーク）
- `LICENSE`、`LICENSES/`、`.kilo/skills/ATTRIBUTION.md`

## 内部（git 管理外）

メンテナ・監査・実測用。**公開 clone には含まれない**。

| 配置（ローカル） | 内容 |
|---|---|
| `internal/docs/MAINTAINER.md` | メンテナ手順 |
| `internal/docs/audit/` | 監査記録・E2E 手順 |
| `internal/docs/design/` | **調査・分析ノート**（例: 外部ツール比較・吸収分析、`*-AUDIT.md`） |
| `internal/docs/plans/` | **開発過程資料**（`RETRO-*`・`self-improve-*`・E2E 深さ対応表） |
| `internal/docs/blog/` | **出版・連載たたき台**（Qiita/Kindle 目次案） |
| `docs/plans/ACTIVE.md`（ローカルのみ） | **キット自身の進捗 SSOT**（公開テンプレは `docs/plans/ACTIVE.example.md`） |
| `docs/memory/*.md`（ローカルのみ） | **キット自身の記憶**（公開テンプレは `TEMPLATE.md`・`MEMORY-TOOLS.md`・`INDEX.example.md`） |
| `internal/scripts/e2e/` | スモーク・CLI 実測スクリプト |
| `internal/docker/e2e/` | Docker 実測 |
| `internal/scripts/audit_*.py` | 監査生成 |

### 内部開発資料（公開しない）

次は**メンテナの開発過程資料**であり、公開 clone に含めない（`internal/` 配下に置く）。

- 調査・分析ノート（外部ツールの比較・吸収分析など）
- 監査記録（`*-AUDIT.md` 等）
- 振り返り・自己改善（`RETRO-*.md`・`self-improve-*.md`）
- E2E 実行ログ（`docs/plans/evidence/`・gitignore 済）と E2E 深さ対応表
- 出版・連載たたき台（`docs/blog/` 相当）

> **移行済み（2026-10-28）**: 以下を `internal/` へ移動し、公開ツリーから除去した（履歴には残る点に注意）。
> - `docs/design/INTENT-RECEIVER-AUDIT.md` → `internal/docs/design/`
> - `docs/plans/RETRO-20261028-log-optimization.md`・`self-improve-20261028-log-optimization.md`・`E2E-WORKFLOW-COVERAGE.md` → `internal/docs/plans/`
> - `docs/blog/*` → `internal/docs/blog/`
>
> **公開を維持する判断（要再検討可）: 撤回（2026-10-28）**。`docs/plans/ACTIVE.md`（キット自身の進捗）と `docs/memory/` の**実体は公開しない**。公開クローンには各テンプレート（`ACTIVE.example.md`・`INDEX.example.md`・`TEMPLATE.md`・`MEMORY-TOOLS.md`）のみを置き、実体は各プロジェクトで作成する。CI（`scripts/e2e_flows.py`）は実ファイルに依存しない（テンプレート／隔離 memory を使用）。
>
> **移行済み（2026-10-29）**: 公開の読書面を `README.md`・`docs/USAGE.md`・`docs/INTENT-ROUTING.md` に絞るため、設計・工程文書を公開ツリーから `internal/` へ移動（EN+JA）。移動対象: `docs/METHODOLOGY.md`・`docs/PROCESS-PHILOSOPHY.md`・`docs/PUBLICATION.md`・`docs/README.md`・`docs/design/INTENT-RECEIVER.md` → `internal/docs/design/`・`internal/docs/`。公開文書の参照は `AGENTS.md` §3／`mcp/README.md` に張り替え、`scripts/e2e_flows.py` は `internal/` 不在時に METHODOLOGY 検査をスキップする。

> **正本の分離（2026-10-29）**: **本リポジトリ（`wawoo-skills-internal`・非公開）が正本**で、キット**と** `internal/` の両方を追跡する。**公開**キットは `parkwoo/wawoo-skills` で、`.github/workflows/publish-public.yml`（タグ時のみ）が `.publish-allowlist` に従って**生成**する。公開は SSH deploy key（secret `PUBLIC_DEPLOY_KEY`）で行う。公開リポは重い CI（無料）、本リポは publish のみ（タグ時・最小分数）。ローカル保護: 本クローンの `origin` の push URL は無効化（`DISABLED_DO_NOT_PUSH`）し、内部物が公開リポへ push されないようにする。

内部ツールは `internal/` 直下に置く（本非公開リポジトリで追跡。テンプレ／bootstrap 手順は無し）。

```bash
./internal/scripts/e2e/smoke.sh
```

## 秘密

`.env` は従来どおり gitignore（`.env.example` はキー名の例のみ）。

## 記憶（`docs/memory/`）

| 利用形態 | 推奨 |
|----------|------|
| **キット本体**（wawoo-skills） | 実体（`INDEX.md`・`kit.md`・`general.md`・`deployment.md` 等）は **非公開**（`.gitignore`）。公開するのは `TEMPLATE.md`・`MEMORY-TOOLS.md`・`INDEX.example.md` のみ |
| **消費側プロジェクト**（キットをコピーして別製品を開発） | `INDEX.md` を `INDEX.example.md` から作成し、チーム共有する決定は **コミット**。個人メモのみなら `docs/memory/local/` を `.gitignore` に追加（`local/` は任意・未同梱） |
| **秘密** | memory に書かない（`validate_assets.py` がパターン検査） |

ツールの優先順: `docs/memory/MEMORY-TOOLS.md`。
