# Skill Uplift Pilot（MWG 思想の軽量版）

## 0. 一文

**guidance が agent 出力を本当に改善するか**を、expectations + 静的チェック +（任意で）guided/unguided メモで追い、**uplift 低・無 skill でも通る項目は prune** する。

## ロードマップ（実装済み）

| 段 | 内容 | 成果物 |
|----|------|--------|
| P0 | MWG bridge | `modern-web-guidance-bridge` · `scripts/mwg_bridge.py` · MCP `mwg_*` |
| P1 | Expectations 试点 | `web-design-guidelines/expectations.md` · `scripts/skill_uplift_check.py` |
| P1.1 | a11y + deploy 试点 | `accessibility-audit` / `deployment` の `expectations.md` · checker 拡張 · `ui-delivery` 5b 証拠パス |
| P1b | Playwright A/B | `internal/skill-uplift-ab/` · `scripts/skill_uplift_ab.py` |
| P1.5 | Frontend hub | `frontend-guides-hub` skill |
| P2 | Uplift/prune 規則 | 本書 + `USAGE.ja.md` §6.2 |
| P3 | Legacy scan | `legacy-web-scan` · `scripts/legacy_web_scan.py` + MWG `legacy-scan` |

## §6.2 Uplift / Prune ルール

1. **無 skill でも ~90% 達成** → 入口 `SKILL.md` を短くするか `references/` へ降格。カタログ description も短縮。
2. **uplift 低**（guided でも静的チェック改善が小さい）→ **guide を直す**。workflow は変えない（フェーズ境界を壊さない）。
3. **uplift 高** → expectations にチェックを追加し、`skill_uplift_check.py` にルールを足す。
4. 証拠は `docs/evidence/skill-uplift/<skill>-<YYYYMMDD>.json` に保存（git 追跡可・秘密なし）。

## P1 / P1.1 実行例

```bash
TS=$(date -u +%Y%m%dT%H%M%SZ)
python3 scripts/skill_uplift_check.py web-design-guidelines --path /path/to/ui-root \
  > docs/evidence/skill-uplift/web-design-guidelines-${TS}.json
python3 scripts/skill_uplift_check.py accessibility-audit --path /path/to/ui-root \
  > docs/evidence/skill-uplift/accessibility-audit-${TS}.json
python3 scripts/skill_uplift_check.py deployment --path /path/to/compose-dir \
  > docs/evidence/skill-uplift/deployment-${TS}.json
```

**P1.1 静的ルール（要約）**

| skill | ルール id（抜粋） |
|-------|-------------------|
| `accessibility-audit` | `a11y-html-lang` · `a11y-page-h1` · `a11y-input-label` · `a11y-button-type` · `a11y-skip-link` |
| `deployment` | `deploy-no-latest-tag` · `deploy-plain-secret-env` · `deploy-missing-healthcheck` |

配線: `.kilo/commands/ui-delivery.md` **5b** · `.kilo/agents/web-designer.md`「Skill ルーティング」3 行。

## Playwright A/B（自動・較正用）

```bash
cd internal/skill-uplift-ab && npm install && npx playwright install chromium
cd ../..  # skills root
python3 scripts/skill_uplift_ab.py --out docs/evidence/skill-uplift/ab-accessible-dialog.json
```

- シナリオ `accessible-dialog`：`fixtures/unguided`（低 pass）vs `fixtures/guided`（高 pass）
- 出力: `unguided` / `guided` の **pass_rate** と **uplift**（guided − unguided）
- 手動 agent 評価: 同一 `task.md` で 2 回実装し、将来 `--unguided` / `--guided` に成果物 dir を渡す（現行は bundled fixtures のみ）

詳細: `internal/skill-uplift-ab/README.ja.md`

静的チェックとの併用: finding_count 差分は引き続き手動メモ可。

## ルール SSOT

- 対象 skill 集合: `scripts/uplift_pilot.py` → `UPLIFT_PILOT_SKILLS`
- 有効な静的ルール id: `ACTIVE_STATIC_RULES`（`expectations.md` の `[rule-id]` と一致）

## MCP（P0）

| ツール | 用途 |
|--------|------|
| `mwg_search` | `query` → JSON 候補 |
| `mwg_retrieve` | `id` → guide 本文 |
| `mwg_legacy_scan` | `path` → MWG legacy レポート |

無効: `WAWOO_MWG_DISABLE=1`

## 関連

- `docs/USAGE.ja.md` §6.1（拡充チェックリスト）
- [Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance-src)