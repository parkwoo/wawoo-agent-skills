---
tags: audit
---

# audit

決定・制約・落とし穴の詳細。`memory` スキルと `docs/memory/TEMPLATE.md` に従う。

### MEM-20261028-053

- **日付**: 2026-10-28
- **種別**: 制約・落とし穴
- **内容**: 公開ドキュメント監査の落とし穴: `ls .kilo/skills | wc -l` は 65 を返すが、これは非ディレクトリの `.kilo/skills/README.md`・`ATTRIBUTION.md` を数えるため。実体は **63 skill ディレクトリ**（`python3 scripts/validate_assets.py` → `OK: skills=63 agents=22 commands=16` が正本）。公開文書の件数表記（README/AGENTS/USAGE の 63/22/16）は**正確**。commands も `*.md` は 17 だが実コマンドは 16（README.md を除く）。件数は生成カタログに集約するのが望ましい（重複＝将来ドリフト余地）。
- **出典**: internal/docs/audit/PUBLIC-DOCS-AUTHOR-AUDIT.md

