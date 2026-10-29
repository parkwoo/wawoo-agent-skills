---
tags: release
---

# release

決定・制約・落とし穴の詳細。`memory` スキルと `docs/memory/TEMPLATE.md` に従う。

### MEM-20261028-057

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 公開/非公開の分離を **2 リポジトリ + publish** に移行（2026-10-29）。(1) 正本は **parkwoo/wawoo-skills-internal（非公開）**：キット＋`internal/` を全部追跡（`/internal/` 等の gitignore を解除）。(2) 公開は **parkwoo/wawoo-skills（PUBLIC）**：`.github/workflows/publish-public.yml`（タグ時のみ）が `.publish-allowlist` で `git filter-repo` → SSH deploy key（secret `PUBLIC_DEPLOY_KEY`）で push。(3) `scripts/validate_assets.py` の境界検査は「git ls-files に internal」から「**allowlist に internal を入れない**」へ変更（source は internal を追跡するため）。(4) ローカルの `origin` は push URL を `DISABLED_DO_NOT_PUSH` に設定し誤 push を防止。(5) 落とし穴: 現 PAT は `workflow` スコープ無し → `.github/workflows/*` を含む push は拒否される。**SSH なら可**（今回 SSH で回避）。
- **出典**: internal/docs/PUBLICATION.md


### MEM-20261029-001

- **日付**: 2026-10-29
- **種別**: 決定
- **内容**: 旧足場を撤去（2026-10-29）: `internal.example/` と `scripts/bootstrap-internal.sh` を削除。`internal/` に無かった 5 ファイル（`docs/audit/AGENT-ACTIVE-E2E.md`・`scripts/e2e/{active_apply_dryrun.py,agent-active-live.sh,fixtures/*}`）は `internal/` へ退避してから削除。内部ツールは `internal/` 直下に集約（bootstrap 手順は廃止）。`scripts/e2e_flows.py` の `agent_active_sandbox_dry` テストは `internal/scripts/e2e/agent-active-live.sh` を参照し、無ければスキップに変更。deploy key ローテーションは「新規追加→secret 更新→検証→旧削除」の順（`gh repo deploy-key add/delete` + `gh secret set PUBLIC_DEPLOY_KEY`）。
- **出典**: scripts/e2e_flows.py

