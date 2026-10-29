---
tags: licensing
---

# licensing

決定・制約・落とし穴の詳細。`memory` スキルと `docs/memory/TEMPLATE.md` に従う。

### MEM-20261029-011

- **日付**: 2026-10-29
- **種別**: 決定
- **内容**: 公開範囲とライセンス帰属（2026-10-29）: (1) **`ja-proofread`（日本語中の中国語チェック）は非公開化** — 普遍性が無いため `.kilo/skills/ja-proofread` → `internal/skills/ja-proofread` へ移動。公開 `validate_assets.py` から中国語検査（`japanese_consistency_warnings`）を削除。(2) **`fal-gen` を公開キットに同梱**（開発で使用）— `.kilo/skills/fal-gen/` に `SKILL.md`（英訳）・`fal_gen.py`（CJK 0 に英訳）・`templates/manifest.example.json`・`.env.example`・`.gitignore`。**`.env` はコピーしない**（root `.gitignore` で `.env` 無視）。README の画像生成 Caution を「fal-gen 同梱（FAL_KEY 要）」に更新。(3) **帰属を wawoo.jp に統一** — `LICENSE`・`NOTICE` の `Copyright (c) 2026 wawoo` → **`wawoo.jp`**、ATTRIBUTION の自作分にも明記。自作資産は LICENSE(MIT)+NOTICE+ATTRIBUTION で保護（各 SKILL.md の frontmatter には license 欄を持たせない運用）。skills=64。公開反映 `e55720f`。
- **出典**: .kilo/skills/ATTRIBUTION.md

