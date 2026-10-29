---
tags: docs
---

# docs

決定・制約・落とし穴の詳細。`memory` スキルと `docs/memory/TEMPLATE.md` に従う。

### MEM-20261028-054

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 公開ドキュメント監査の後続：指摘対応（F1–F11 の具体改稿）と「有人気な記事」草稿を `internal/docs/blog/`（非公開・gitignore）に保存。ファイル: `public-docs-audit-fixes.zh.md`（4.3K 字）・`wawoo-skills-popular-article.zh.md`（2.4K 字）。ユーザーは中国語で依頼（当リポジトリの既定は日本語）— 今回はユーザー言語に合わせて中国語で執筆した。記事は viral-hooks（Hook→stakes→evidence→steps→objections→payoff→CTA）＋倫理（非誇大、"非ランタイム強制"の限界を明記）。公開は要承認。
- **出典**: internal/docs/blog/


### MEM-20261028-055

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 公開ドキュメント編集の規約（今回適用）: (1) 説明文書は **EN 主（`NAME.md`）＋ JA 対訳（`NAME.ja.md`）を同時更新**する（言語ポリシー AGENTS §1）。(2) **件数は生成カタログ `.kilo/CAPABILITIES.md` を正本**とし、README/AGENTS/USAGE の重複記載は除去。(3) **`L0–L3` は 2 軸**（儀式レベル=METHODOLOGY §5 / ルート層=INTENT-ROUTING §1）— 改名は破壊的なので、各初出に「別の軸」注記を置く方針。(4) 監査記録は非公開 `internal/docs/audit/`、投稿草稿は `internal/docs/blog/`。(5) 文書改善は CHANGELOG `[Unreleased]` に追記（VERSION bump はリリース時）。
- **出典**: docs/plans/ACTIVE.md#docs-author-audit


### MEM-20261028-056

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 公開面の縮小（2026-10-29 適用）: 公開の「読む」文書は **README.md / docs/USAGE.md / docs/INTENT-ROUTING.md** の 3 本のみ。設計・工程文書 **METHODOLOGY / PROCESS-PHILOSOPHY / PUBLICATION / docs/README / design/INTENT-RECEIVER（EN+JA）は `internal/docs(/design)/` へ移動**（非公開）。公開文書の参照は `AGENTS.md` §3（儀式レベル）と `mcp/README.md` に張り替え。`scripts/e2e_flows.py` は `internal_doc()` で **internal/ 不在時にスキップ**（公開クローンで落ちない）。`publication-boundary` skill の Public/Internal リストを更新。必須の公開ファイル（LICENSE/NOTICE/ATTRIBUTION/SECURITY/CHANGELOG/VERSION、AGENTS.md、.kilo/.cursor/mcp/scripts、memory テンプレ）は維持。
- **出典**: docs/plans/ACTIVE.md#docs-public-surface


### MEM-20261029-003

- **日付**: 2026-10-29
- **種別**: 再発しうる修正
- **内容**: 公開文書のコード同期（2026-10-29）。公開リポの文書はソースと完全一致（公開遅延なし）。発見・修正したドリフト: (1) `AGENTS.md`/`.ja` §2 レイアウトが削除済み `docs/design` を記載 → `docs/ … USAGE, INTENT-ROUTING, VERSIONING, plans, memory` に修正、`.cursor/cli.json.example` を追記。(2) EN/JA の**更新履歴の行数ドリフト**: `AGENTS.ja.md` §11 に EN の「3 層言語ポリシー」行が欠落、`docs/INTENT-ROUTING.ja.md` §8 に EN の 2026-10-28 行が欠落 → 追加。(3) 2026-10-29 行（公開面縮小・正本分離）を AGENTS EN/JA に追加。教訓: **EN 主＋JA 従は「見出し構造」だけでなく更新履歴の行パリティも検査する**（`grep -c '^| 2026-'` を EN/JA で比較）。
- **出典**: AGENTS.md

