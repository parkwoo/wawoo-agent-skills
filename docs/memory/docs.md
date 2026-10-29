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


### MEM-20261029-004

- **日付**: 2026-10-29
- **種別**: 再発しうる修正
- **内容**: 公開文書の改善（2026-10-29）: (1) **日本語文書の内部リンクを JA 版へ**修正（`README.ja.md`・`docs/USAGE.ja.md`・`docs/INTENT-ROUTING.ja.md` が EN `*.md` を指していた → `*.ja.md`。トップの「English version」リンクのみ EN のまま）。(2) **Oct-28 の新機能を追記**: README(EN/JA) に「Capabilities／主な機能」節（意図ルーティング=学習＋上流、フェーズとゲート、動的ステア、委譲＋**モデル階層 fast|reasoning**、Gₐ/Gₑ/Gₒ、段階的開示、記憶）。`model_tier` は実装済みだが未記載だったので INTENT-ROUTING §3.2 P3 に追記。検証: validate OK / e2e 28/0。公開反映 `17475c1`。
- **出典**: README.ja.md


### MEM-20261029-005

- **日付**: 2026-10-29
- **種別**: 決定
- **内容**: 公開文書の強化（2026-10-29）: (1) **OpenCode 対応**を追加 — `opencode.json`（`mcp.wawoo-skills` type=local, command=[python3,mcp/server.py]）、README(EN/JA)「対応環境／対応ツール」と `AGENTS(.ja) §6` に追記、allowlist に `opencode.json`。(2) **MkDocs Material** でドキュメントサイト：`mkdocs.yml`（`docs_dir: docs`, theme material, `exclude_docs: memory/ plans/`, nav=EN/日本語 両方）＋`requirements-docs.txt`（mkdocs-material のみ）＋`.github/workflows/docs.yml`（build→`actions/deploy-pages`）。**GitHub Pages 有効化**（`gh api -X POST repos/.../pages -f build_type=workflow`）→ https://parkwoo.github.io/wawoo-skills/ （EN+JA 200）。落とし穴: **`docs_dir` は config の子でなければならない**（リポジトリ直下 `docs_dir: .` は不可）。また **mkdocs-static-i18n の suffix 構造は GitHub 流の `NAME.ja.md` 内部リンクと衝突**する（`suffix` オプション無しで locale から `NAME.<locale>.md` を期待。EN ページ→`.ja.md` リンクが「not found」警告）→ i18n プラグインは使わず、**EN/日本語 を別 nav セクションとして掲載**して全リンクを解決させた。CI は公開リポ（無料）。
- **出典**: mkdocs.yml


### MEM-20261029-006

- **日付**: 2026-10-29
- **種別**: 再発しうる修正
- **内容**: ライセンスと日本語校正（2026-10-29）: (1) **`fal-gen` は自作 skill（MIT）**であり「ライセンス不明」ではなかった → `README(.ja)` と `.kilo/skills/ATTRIBUTION.md` の除外理由を訂正（除外は第三者ではなく外部依存 fal.ai のため、同梱せずグローバル運用）。Marketplace business 3 件のみが第三者 NOASSERTION。(2) **日本語校正 skill `ja-proofread` を新規追加**（簡体字中国語のみの文字を検出→日本語へ、記号・MT くせ・用語統一、Gₑ で grep 0 件を確認）。`scripts/validate_assets.py` に **WARN 検査**（`*.ja.md` と `.kilo/skills/**` の簡体字中国語のみ文字）を追加（`ja-proofread` 自身は除外）。(3) 実際の中国語混入を修正: `reference-design-contract/SKILL.md`（zh_name/triggers/example_prompt_i18n の zh-CN→ja）と `web-design-guidelines/SKILL.md`（trigger「设计审查」→「デザインレビュー」）。skills=64。
- **出典**: .kilo/skills/ATTRIBUTION.md


### MEM-20261029-007

- **日付**: 2026-10-29
- **種別**: 決定
- **内容**: 日本語文書の英語混在とサイト言語切替（2026-10-29）: (1) **`ja-proofread` を拡張** — 簡体字中国語のみ文字に加え「日本語の文中の英単語（skill→スキル等）」と置換表・MT くせ・記号・用語統一を追加。(2) **JA 文書の英語混在を一括軽減**（README/AGENTS/USAGE/INTENT-ROUTING/index .ja.md）。落とし穴: 単純一括置換は **`AGENTS.md`→エージェント.md・`Skills For Real Engineers`→スキル For…** のように識別子/固有名詞を壊す。対策＝**大小文字を区別（小文字のみ）＋前後が `[A-Za-z0-9_\-/.\`]` を除外**し、バッククォート内は置換しない。適用後「日本語↔カタカナ語」間の半角スペースを除去。(3) **MkDocs に `mkdocs-static-i18n`（suffix）を導入**し言語切替＋言語別 nav に（EN=/、JA=/ja/、hreflang）。トレードオフ: i18n と GitHub 流の `NAME.ja.md` リンクは両立しない（`.ja.md` は i18n ビルドで「not found」）ため、`validation.links.not_found=ignore` で警告のみ抑制（リンクは GitHub 優先で維持）。Zensical 移行警告は `NO_MKDOCS_2_WARNING=1` で抑制可。公開反映 `ba86790`。
- **出典**: mkdocs.yml

