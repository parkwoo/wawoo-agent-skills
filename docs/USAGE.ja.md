# 使い方（Kilo / Cursor / OpenCode / MCP）

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

OpenCode は `AGENTS.md` を読み、`skills.paths` から**ネイティブ skills** を読み込み、MCP サーバへ **stdio** で接続します。キットはリポジトリ直下に `opencode.json` を同梱します:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["AGENTS.md"],
  "skills": { "paths": [".kilo/skills"] },
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "mcp/server.py"],
      "enabled": true
    }
  }
}
```

### グローバル導入（全プロジェクトで使う・冪等）

`.kilo/{agents,commands}` を `~/.config/opencode/{agent,command}` へミラーし、MCP・`instructions`・`skills.paths`・`default_agent` を冪等に登録:
```bash
python3 scripts/install_opencode.py --dry-run    # 差分のプレビュー
python3 scripts/install_opencode.py              # 適用（既定 mirror = 余分を削除）
python3 scripts/install_opencode.py --no-delete  # 余分を保持
python3 scripts/install_opencode.py --memory-writable
OPENCODE_GLOBAL_DIR=/path/to/config python3 scripts/install_opencode.py  # 別ターゲット
```
- agent は `name:`／`id:` を剥がして**キー＝ファイル名**にする（command の `agent:` 参照と一致させる）。
- `mcp.wawoo-skills`（絶対 python＋`WAWOO_SKILLS_ROOT`／`WAWOO_MEMORY_READONLY`）、`instructions`＝`<kit>/AGENTS.md`（**絶対パス**。相対は注入されない）、`skills.paths`＝`<kit>/.kilo/skills`（ネイティブ発見）、`default_agent`＝`wawoo-auto`（`--no-default-agent` で除外）。
- **OpenCode は再起動が必要**（設定は起動時に一度だけ読む）。
- slash のネイティブ実行は無い。workflow は MCP（`interpret_intent` → `workflow_get` → `skill_get`）＋インストール済み subagents/commands で回す。
- `opencode_stdio_contract` E2E（MCP handshake＋`tools/list`）で検証。

## 3. Cursor（https://cursor.com）
1. このディレクトリを開く（`AGENTS.md` と `.cursor/rules` を読む）。
2. **Settings → MCP** で `wawoo-skills` を有効化（`.cursor/mcp.json`）。
3. ツール `capabilities`／`skill_search`／`skill_get`／`agent_get` を利用。

### ネイティブ skills・agents・グローバル rules

Cursor は**ネイティブ skills**（`SKILL.md`）・プロジェクト subagents・ユーザレベル rules を読むため、MCP に加えてネイティブ導入も可能:
```bash
python3 scripts/install_cursor_workspace.py --workspace /abs/path/to/project  # プロジェクト: .cursor/{mcp.json,rules,agents,skills}
python3 scripts/install_cursor_global.py                                      # ユーザ:    ~/.cursor/{rules,agents,skills,mcp.json}
```
- `rules/` は相対 `@.kilo/` をキットの絶対パスへ書き換えてコピー（どのプロジェクトからでも有効）。
- `agents/` は `.kilo/agents` から生成（`name`＋`description`＋本体）。役割の内容は MCP `agent_get` でも取得可。
- `skills/` は `.kilo/skills/<name>` への symlink（キットが単一の出所）。
- **プロジェクト** `.cursor/agents` は app・**CLI・cloud** が読む。**ユーザ** `~/.cursor/agents` は**デスクトップのみ**。CLI/ACP ではプロジェクト導入か MCP `agent_get` を使う。

**Cursor の制約**：
- slash command（`/feature-delivery` 等）は**ネイティブ実行されない** — 手順を適用するか、MCP `workflow_get` で取得。
- agent の自動切替は**無い**。プロジェクト subagent を使うか、`agent_get`／`@.kilo/agents/<role>.md` の役割を適用。

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

**ガードレール / egress**: `mask_pii`（PII/秘密のマスク＋可逆マップ）、`redact_infra`（エラー/ログから内部 IP・ホスト・資格情報を除去）、`guard_content`（policy-as-data の可否ゲート、任意で fail-closed）。

**コンテキスト**: `compress_context` — 会話ターンをオフライン・決定的に圧縮/クリーニング（ヒューリスティック＋曖昧重複排除＋密度予算。LLM・ネットワーク不要）。詳細は `.kilo/skills/context-compression/SKILL.md`。

**意図**: `interpret_intent` は slash → learned → **ローカル語彙（threshold/棄権）** → upstream の順。`python3 mcp/intent_calibrate.py` で閾値を校正。schedule は `complexity` / `model_tier` を返す。

**意図ルーティング**（任意だが推奨）: `interpret_intent` → `workflow_get` → … → `workflow_clear`。サブタスクは `delegate_subtask`。

- 対外ガイド：**[docs/INTENT-ROUTING.ja.md](INTENT-ROUTING.ja.md)**（L0–L3・スコア JSON・ツールゲート）
- 実装・常駐：`mcp/README.md`

## 5. 呼び出しの順序
1. **Workflow**（入口）を選ぶ。曖昧な依頼は MCP **`interpret_intent`** で 12 workflow から選ぶ（[INTENT-ROUTING.ja.md](INTENT-ROUTING.ja.md)）。明示できるときは **`/delivery-lite`**（`docs/plans/ACTIVE.md` が進捗 SSOT）。セレモニーレベル（L0–L3）は `AGENTS.md` §3（`INTENT-ROUTING.md` の**ルート層** `L0–L3` とは別の軸）。
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

## 9. 言語ポリシー（既定と変更方法）

キットは **三層** の言語ポリシーを同梱する — 正本は `AGENTS.md` §1、根拠は `.kilo/skills/language-policy/SKILL.md`:

| 対象 | 既定（`wawoo-skills`） |
|---|---|
| コード（コメント・識別子・文字列・commit・設定キー） | **英語** |
| 工程記録（`plans/`・`ACTIVE.md`・`RETRO-*`・`evidence/`・`memory/`）と**エージェントの応答** | **日本語**（本キットの `project working language`） |
| 説明・対外ドキュメント（`README.md`・`docs/USAGE.md` 等） | **英語（主）＋日本語（副）** の 2 ファイル |

`project working language` は**キットの既定であり固定ではない**。コードは相互運用のため英語のまま、作業言語はプロジェクトの選択。

**作業言語を変える手順**（例：英語や他言語へ）:

1. `AGENTS.md` §1 の「作業言語」行を選択に合わせる。
2. `.kilo/skills/language-policy/SKILL.md` の「(wawoo-skills: Japanese)」と書かれた 2 行を一致させる。
3. 規則を再掲する場合は router を再生成: `python3 scripts/gen_router.py`。
4. 任意：副言語ドキュメント（`*.ja.md`）を外して 1 言語にする。`.publish-allowlist` も更新。
