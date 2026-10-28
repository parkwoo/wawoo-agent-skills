---
tags: kit, decision
---

# kit

wawoo-skills キット本体に関する決定・制約。

### MEM-20261025-001

- **日付**: 2026-10-25
- **種別**: 決定
- **内容**: 記憶の正本は `docs/memory/`。MCP `memory_save` は INDEX と topic ファイルへ追記する。Kilo ネイティブメモリは補助で、矛盾時はファイルを優先する。
- **出典**: `docs/memory/MEMORY-TOOLS.md`・`.kilo/skills/memory/SKILL.md`

### MEM-20261025-002

- **日付**: 2026-10-25
- **種別**: 決定
- **内容**: L1 の進捗 SSOT は `docs/plans/ACTIVE.md`。`/delivery-lite` が既定入口。タスクの done／証拠は ACTIVE のみ。memory は決定・制約・落とし穴に限定。
- **出典**: `AGENTS.md` §3・`docs/METHODOLOGY.md` §5

### MEM-20261028-001

- **日付**: 2026-10-28
- **種別**: 制約
- **内容**: Kilo の `config.instructions` は**絶対パス必須**（相対 `ROUTER.md` は実行時コンテキストに注入されない）。既定 agent が `code` のままだと MCP ルーティングが漏れるため、`default_agent` を `wawoo-router` に設定する。反映にはエンジン再起動が必要（agent/command/instructions は起動時キャッシュ）。
- **出典**: `scripts/install_global.py`・`AGENTS.md` §4・検証（`kilo run` で最初のツールが `workflow_get`）

### MEM-20261028-002

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 実行衛生・収束ゲート（`AGENTS.md` §4.1）をキット共通規約とする — 1 セッション 1 対象／1 成果物、workflow 切替の明示、失敗の収束（未収束 FAILED = 0）、後始末（残留 0）、記憶 1 件以上、トークン衛生（1 step < 4KB）、ローカル検証。プロジェクト非依存。
- **出典**: `AGENTS.md` §4.1・`.kilo/agents/wawoo-router.md`・`ROUTER.md`・`.kilo/skills/test-engineering/SKILL.md`

### MEM-20261028-003

- **日付**: 2026-10-28
- **種別**: 決定
- **内容**: 意図ルーティングは「L1 トリガ分類器（`intent_catalog.TRIGGER_KEYWORDS`、ROUTER の発火語と同一正本）+ phases」で決定論的に解決する。監査系 workflow に `implement` phase を持たせないことで、監査→実装の逸脱を構造的に防ぐ（切替宣言を必須化）。
- **出典**: `mcp/intent_catalog.py`・`mcp/intent_interpreter.py`・`docs/INTENT-ROUTING.md` §3.1/§3.2
