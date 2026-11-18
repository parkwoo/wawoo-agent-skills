# 使い方（Kilo / Cursor / MCP）

## 0. 前提条件

- **Python 3（標準ライブラリのみ）** が必要（MCP サーバ・保守スクリプト）。**追加パッケージ不要**。
- `PATH` に `python3` が通っていること（Windows は `python`）。確認：`python3 --version`。
  - macOS: 無ければ `xcode-select --install`。Linux: `apt install python3` 等。Windows: https://www.python.org/downloads/ で「Add python.exe to PATH」を有効化。
- MCP は `python3` を実行コマンドとして起動（`kilo.json`・`.cursor/mcp.json`）。別名（`python`／`py`）の環境では `command` を実体に合わせる。
- 詳細：README「前提条件（ランタイム）」。

## 1. 収録
- Skills：`.kilo/skills/<name>/SKILL.md`
- Agents：`.kilo/agents/<name>.md`
- Workflows：`.kilo/commands/<name>.md`
- MCP：`mcp/server.py`
- カタログ（自動生成）— **件数はここが正本**：`.kilo/CAPABILITIES.md`

## 2. Kilo CLI / Kilo Code（https://kilo.ai ・ https://kilocode.ai）
1. このディレクトリを開く（`.kilo/` を自動探索、`kilo.json` で MCP 有効）。
2. ワークフロー：`/feature-delivery` など。
3. スキル：モデルが `SKILL.md` を選択、または明示的に参照。

### グローバル配置（全プロジェクトで使う・冪等）
`.kilo/{skills,agents,commands}` を `~/.config/kilo/` へ同期し、MCP と適用範囲メモを冪等登録する（再実行可）。
```bash
python3 scripts/install_global.py --dry-run    # 変更内容の確認
python3 scripts/install_global.py              # 適用（既定ミラー＝余剰を削除）
python3 scripts/install_global.py --no-delete  # 余剰を残す
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py  # 別の配置先
```
- MCP は絶対パス登録（`/usr/bin/python3` ＋ `WAWOO_SKILLS_ROOT`／`WAWOO_MEMORY_READONLY`）。既定は recall-only（`=1`）で、書込を有効化するには `--memory-writable`（`=0`）。詳細は `mcp/README.md`。
- 併せて **`ROUTER.md` を生成**し、`instructions` に **絶対パス**で冪等登録、`default_agent` を `wawoo-auto` に設定する（既定）。
  - Kilo の `instructions` は**絶対パス必須**（相対 `ROUTER.md` は実行時コンテキストに注入されない）。
  - 既定 agent `wawoo-auto` が「最初のツール＝`workflow_get`／`interpret_intent`」を強制し、`code` 既定時のルーティング漏れを防ぐ。
  - 変更は `--default-agent <name>`／`--no-default-agent`／`--force-default-agent` で制御。
- **反映には Kilo の再起動が必要**（agent／command／instruction はサーバ起動時にキャッシュ。VS Code は Reload Window）。
- キットの repo 相対 SSOT を前提とする手順は**キット内でのみ有効**。グローバル `AGENTS.md` にその旨を追記する。
- `validate_assets`：同名 skill／command は **command 側で入口を明文化していれば警告しない**（`design-review`・`research` は対応済み）。未記載の衝突は `WARN` として出る（`scripts/validate_assets.py` の `documents_entry`）。

## 2.5 OpenCode（https://opencode.ai）

OpenCode は `AGENTS.md` を読み、MCP サーバへ **stdio** で接続します。`opencode.json` にローカル MCP として追加します:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "/abs/path/to/wawoo-skills/mcp/server.py"],
      "enabled": true,
      "environment": { "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills" }
    }
  }
}
```
- OpenCode は slash／skill のネイティブ実行を持たない。`AGENTS.md` ＋ MCP（`interpret_intent` → `workflow_get` → `skill_get`）で使う。
- `opencode_stdio_contract` E2E（MCP handshake＋`tools/list`）で検証。

## 3. Cursor（https://cursor.com）
1. このディレクトリを開く（`AGENTS.md` と `.cursor/rules` を読む）。
2. **Settings → MCP** で `wawoo-skills` を有効化（`.cursor/mcp.json`）。
3. ツール `capabilities`／`skill_search`／`skill_get` を利用。

**Cursor の制約**：
- slash command（`/feature-delivery` 等）は**動かない**。
- agent の切替は**無い**（役割は `@.kilo/agents/<role>.md` を読んで適用）。
- `SKILL.md` の**自動発見・自動起動**は**無い**。

**フォールバック（MCP 無し）**：
```
@.kilo/CAPABILITIES.md を見て候補を選び、必要な @.kilo/skills/<name>/SKILL.md を読んで従って。
@.kilo/commands/<name>.md の手順を適用して。
```

## 4. MCP（Model Context Protocol: https://modelcontextprotocol.io）
```bash
python3 mcp/server.py        # stdio（通常はクライアントが起動）
python3 scripts/e2e_flows.py   # 公開スモーク（契約/E2E）
```
**カタログ系**: `capabilities`・`skill_search`・`skill_get`・`workflow_get`・`agent_get`・`memory_recall`・`memory_save`・`evidence_check`。

**意図ルーティング**（任意だが推奨）: `interpret_intent` → `workflow_get` → … → `workflow_clear`。サブタスクは `delegate_subtask`。

- 対外ガイド：**[docs/INTENT-ROUTING.ja.md](INTENT-ROUTING.ja.md)**（L0–L3・スコア JSON・ツールゲート）
- 実装・常駐：`mcp/README.md`

## 5. 呼び出しの順序
1. **Workflow**（入口）を選ぶ。曖昧な依頼は MCP **`interpret_intent`** で 16 workflow から選ぶ（[INTENT-ROUTING.ja.md](INTENT-ROUTING.ja.md)）。明示できるときは **`/delivery-lite`**（`docs/plans/ACTIVE.md` が進捗 SSOT）。セレモニーレベル（L0–L3）は `AGENTS.md` §3（`INTENT-ROUTING.md` の**ルート層** `L0–L3` とは別の軸）。
2. **カタログ／MCP** で候補を選ぶ（全部読まない）。
3. 必要な **Skill** だけ開く。
4. Workflow の**出力スキーマ**と**ゲート**（承認・証拠）に従う。
5. 作業前に `memory` を想起、決定後に保存（MCP `memory_save` は INDEX＋topic ファイル。`docs/memory/TEMPLATE.md`）。

### 記憶（memory）

- 正本: `docs/memory/`（`MEMORY-TOOLS.md` で Kilo／MCP の優先順）
- 納品経路 `/feature-delivery` の入口・出口でも想起／保存
- CI: `validate_assets.py` が memory 内の秘密らしき文字列を検出
- E2E: `python3 scripts/e2e_flows.py`（**L0–L3**・MCP・workflow）。`python3 scripts/cli_adapters_mock.py`（**Kilo/Cursor 入口モック**）
- 検証 CLI: `plan_active` / `plan_l2_backlog` / `plan_l3_record` / `plan_content`

## 6. コンテキスト予算
- 契約 ≤500tok／カタログ ≤1k／Workflow ≤1.5k／**Skill 1 個 ≤2〜4KB**／Memory top-5。
- 段階的開示：全部を一度に渡さない。
- 予算例外：入口 `SKILL.md` のみ先読み。詳細は各 skill の `references/`（例：`imagegen-frontend-mobile`・`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents`）。

### 6.1 Skill 拡充チェックリスト（保守者向け）

skill を増やすときのトークン／コスト対策。ゲートは `AGENTS.ja.md` §8 と `validate_assets.py` と併用する。

| # | やること | 備考 |
|---|----------|------|
| 1 | 入口 `SKILL.md` は手順・ゲートのみ。重い本文は `references/` | 新規自作 skill は **4KB 超えたら references 必須**（`skill_budget_warnings`） |
| 2 | Cursor **ネイティブ skill は curated**（よく使う 15〜30）。残りは **MCP `skill_get` のみ** | `install_cursor_workspace.py` は MCP のみ。全件 symlink は `install_cursor_global.py`（任意）— 一覧例: `scripts/cursor-skills-curated.example.txt` |
| 3 | frontmatter `description` は **1 行・160 文字目安** | `CAPABILITIES.md` は 130 字で切り詰め自動生成。長い description は Cursor `available_skills` を太らせる |
| 4 | 社内専用は `internal/skills` または workspace-only | `publication-boundary` skill。汎用キットに載せすぎない |
| 5 | 長セッションは `compress_context`（MCP）・`/compact`・`memory_save` | 1 セッション = 1 成果物（`AGENTS.ja.md` §4.1） |
| 6 | 監視 | `validate_assets` の 4KB WARN。実運用は **cache_read** と **1 turn の read < 4KB** を先に疑う |

**Workflow と Skill の分担**: 手順の骨格・ゲート・出力形は **Workflow**（`.kilo/commands/`）。Skill はその中の **1 フェーズ手順**（例: `/writing` → `writing-beats` → `writing-shape`。`/research` → `research-decision-room`）。長い synthesis は skill を workflow に置き換えず、`references/` に逃がす。

### 6.2 Uplift pilot（P0–P3）

| 段 | 内容 |
|----|------|
| P0 | **`modern-web-guidance-bridge`** · MCP `mwg_search` / `mwg_retrieve` · `scripts/mwg_bridge.py` |
| P1 | **`web-design-guidelines/expectations.md`** · `scripts/skill_uplift_check.py` |
| P1.1 | **`accessibility-audit` / `deployment`** の expectations · checker · `/ui-delivery` **5b** 証拠パス |
| P1b | **`internal/skill-uplift-ab`** · `scripts/skill_uplift_ab.py`（Playwright A/B） |
| P1.5 | **`frontend-guides-hub`**（UI 線の索引） |
| P2 | uplift/prune 規則 — **`docs/SKILL-UPLIFT-PILOT.ja.md`** |
| P3 | **`legacy-web-scan`** · `scripts/legacy_web_scan.py` + MWG `legacy-scan` |

**Prune ルール（要約）**: 無 skill で ~90% 達成 → 入口を短縮；uplift 低 → **guide/skill を直す**（workflow は維持）；証拠は `docs/evidence/skill-uplift/`。

## 7. 前提が必要なスキル（3）
`to-spec`・`to-tickets`・`triage` は issue tracker が必要。初回に `setup-matt-pocock-skills` を実行。
`scripts/readiness.json` に記載。

## 8. 保守
```bash
python3 scripts/validate_assets.py
python3 scripts/gen_capabilities.py
python3 scripts/e2e_flows.py
```
版管理：`docs/VERSIONING.md`。
