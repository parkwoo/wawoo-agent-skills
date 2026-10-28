---
tags: deployment
---

# deployment

決定・制約・落とし穴の詳細。`memory` スキルと `docs/memory/TEMPLATE.md` に従う。

### MEM-20261028-006

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 本デプロイ（/root/.config/kilo）の MCP wawoo-skills は memory_save を有効化（WAWOO_MEMORY_READONLY=0）。キット側は install_global.py --memory-writable で切替可能。既定は recall-only。
- **出典**: kilo.jsonc + scripts/install_global.py

