<p align="center">
  <img src="assets/wawoo-skills-logo.png" width="128" alt="wawoo-skills ロゴ" />
</p>

<h1 align="center">wawoo-skills 使用ガイド</h1>

<p align="center">
  <strong>導入、設定、活用。</strong>
</p>

<p align="center">
  <a href="USAGE.md">English</a> ·
  <a href="USAGE.ja.md">日本語</a> ·
  <a href="USAGE.zh-CN.md">简体中文</a> ·
  <a href="USAGE.ko.md">한국어</a>
</p>

<p align="center">
  <a href="../README.ja.md">README に戻る</a> ·
  <a href="https://github.com/parkwoo/wawoo-skills">GitHub</a>
</p>

> このドキュメントは**インストール、設定、トラブルシューティング**のみを扱います。「概要と目的」については [`README.ja.md`](../README.ja.md) を参照してください。

**対象**: 初めて導入する開発者。約 10 分で動作するところまで進められます。

**対応**: Kilo、Cursor、OpenCode、Codex、Claude Code、Paseo。本キットは Python 3 標準ライブラリのみで動作します。

## クイックスタート

1. Python 3 を確認 — [§0 前提](#s0)
2. 使用するクライアントに接続 — [§2 クライアント別の接続](#s2)（**Kilo / Cursor が最も簡単**）
3. 検証: `python3 scripts/validate_assets.py` を実行し、`OK` が表示されれば完了です。

それ以外（MCP の引数、メモリ設定、トラブルシューティング）は下の目次から必要なところだけ読んでください。

> **設定を変更したい場合** 作業言語、画像生成のキー、メモリ、ルーティング調整、インストール先は [**§9 設定一覧**](#s9) にまとめてあります。

## 目次

- [0. 前提](#s0)
- [1. 内容](#s1)
  - [1.1 3 種類のアセット: 参照方法](#s1-1) · [1.2 ワークフローの構造](#s1-2) · [1.3 意図ルーティング](#s1-3) · [1.4 アセットを追加する（skill / agent / workflow）](#s1-4)
- [2. クライアント別の接続](#s2)
  - [2.1 Kilo](#s2-1) · [2.2 OpenCode](#s2-2) · [2.3 Cursor](#s2-3) · [2.4 Paseo](#s2-4) · [2.5 Codex](#s2-5) · [2.6 Claude Code](#s2-6)
- [3. MCP サービス](#s3)
- [4. メモリ設定](#s4)
- [5. 呼び出し順](#s5)
  - [5.1 よくある場面: ひとことで、どのワークフロー](#s5-1)
- [6. 保守と検証](#s6)
- [7. 注意事項（依存 / キー / 制限）](#s7)
- [8. トラブルシューティング（FAQ）](#s8)
- [9. 設定一覧（環境変数と設定）](#s9)

<a id="s0"></a>

## 0. 前提: Python 3

- **Python 3（標準ライブラリのみ）**: MCP サービスと保守スクリプトは標準ライブラリだけで動作します。追加パッケージは不要です。
- `PATH` に `python3` が必要（Windows は `python`）。確認: `python3 --version` → `3.x`。
  - macOS: `xcode-select --install`、Linux: `apt install python3` など、Windows: https://www.python.org/downloads/ からインストールし、**"Add python.exe to PATH"** をチェックしてください。
- MCP は `python3` で起動します（`kilo.json`、`.cursor/mcp.json`）。名前が異なる場合（`python` / `py`）は、各設定の `command` を実際のコマンドに変更してください。
- ネットワークも `.env` も不要です（MCP は stdio を使用）。

<a id="s1"></a>

## 1. 内容

要約: **スキルは「何ができるか」、ロールは「誰の視点か」、ワークフローは「どの順で、何をもって完了とするか」です。**

<a id="s1-1"></a>

### 1.1 3 種類のアセット: 参照方法

スキル / ロール / ワークフローの定義は [README の「用語」](../README.ja.md) を参照してください。ここでは**探し方**だけを扱います:

| 種別 | 探し方 |
|---|---|
| スキル skills | `skill_search` / `.kilo/CAPABILITIES.md` |
| ロール agents | `agent_get` |
| ワークフロー workflows | `workflow_get` |
| MCP サービス | `python3 mcp/server.py` |

<a id="s1-2"></a>

### 1.2 ワークフローの構造

**12 のワークフロー一覧は [README「12 のワークフロー」](../README.ja.md) にあります。** ここでは構造だけ説明します — 各ワークフローには:

- **フェーズ（phase）**: 目標 / 担当ロール / 使用するスキル / `exit_criteria`。`workflow_get {name, phase}` で段階ごとに確認できます。
- **ゲート（gate）**: 承認・証拠・失敗の観察。**レビュー系は読み取り専用**（`implement` フェーズがない）。
- **完了条件（exit_criteria）**: 満たさなければ完了とはなりません。

**`implement` フェーズを持たないワークフロー**（`/design-review`、`/compliance-review`、`/release-review`、`/research`、`/status-report` など）は実装フェーズに入りません。コードを変更する場合は `/delivery-lite`、`/feature-delivery`、`/ui-delivery`、`/incident-response`、`/self-improve` のいずれかに切り替えます。

<a id="s1-3"></a>

### 1.3 意図ルーティング

**選び方の順序**（明示 → ローカル語彙 → 学習済み → モデル採点）は [README](../README.ja.md) を参照してください。ここでは、**選択後の管理**について説明します:

- **ツールゲート**: そのワークフローの**許可ツール一覧**（`mcp_tools_allow`）で MCP ツールを制限します。監査系のワークフローでは、読み取りツールのみが許可され、`implement` フェーズは存在しません。
- **セッションゲート**: 呼び出しをまたいで「いまどのワークフローか」を記憶します。`WAWOO_INTENT_RESUME=1` なら再起動後に復元、`WAWOO_INTENT_CLIENT` で複数クライアントの衝突を防ぎます。
- **終了**: `workflow_clear` で現在のセッションゲートを解除します。
- **ルーティングを上書き**: `/name` を直接書くか、`interpret_intent` に `scoring` を渡します。**誤選択 / 見つからない場合**: [§8 トラブルシューティング](#s8) を参照してください（多くの場合、MCP の再起動忘れが原因です）。

<a id="s1-4"></a>

### 1.4 アセットを追加する（skill / agent / workflow）

- **skill**: `.kilo/skills/<name>/SKILL.md` を作成します。`name` はディレクトリ名と一致させ、エントリポイントは 4KB 以下に抑え、詳細は `references/` へ記述してください。
- **agent**: `.kilo/agents/<name>.md` を作成します（`mode: primary|subagent`、権限は必要に応じて）。
- **workflow**: `.kilo/commands/<name>.md` を作成します（frontmatter: `description` / `agent` / `replay`）。
- その後: `python3 scripts/validate_assets.py` を実行し、`python3 scripts/gen_capabilities.py` を実行してください。MCP / Kilo は起動時にコマンドをキャッシュするため、**再起動が必要**です。

<a id="s2"></a>

## 2. クライアント別の接続（Kilo / Cursor / OpenCode / Codex / Paseo）

<a id="s2-1"></a>

### 2.1 Kilo（CLI / Kilo Code）

0. **事前のログイン**: `kilo auth login`（プロバイダーを選んでログイン）。Paseo から Kilo を起動する前にもログインが必要です。
1. このリポジトリを開くだけ（`.kilo/` を自動検出、MCP は `kilo.json` で有効化）。
2. ワークフローは `/feature-delivery` などのスラッシュコマンド。スキルはモデルが選ぶか、明示的に指定します。

**グローバルインストール**（全プロジェクトで使える、再実行可能）:

```bash
python3 scripts/install_global.py --dry-run     # 変更をプレビュー
python3 scripts/install_global.py               # 適用（ミラー: 余分なファイルを削除）
python3 scripts/install_global.py --no-delete   # 余分なファイルを残す
python3 scripts/install_global.py --memory-writable   # memory_save を許可
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py   # 出力先を指定
```

- **以下の 3 つの処理を行います**: ① MCP を書き込む（絶対パスの `python3` + `WAWOO_SKILLS_ROOT` / `WAWOO_MEMORY_READONLY`）。② `ROUTER.md` を生成し、**絶対パス**で `instructions` に登録。③ 既定ロールを `wawoo-auto` に設定（`--default-agent` / `--no-default-agent` で変更）。
- Kilo の `instructions` は**絶対パスでなければなりません**（相対パスは認識されません）。
- **変更後は Kilo の再起動が必要**（agents / commands / instructions は起動時にキャッシュされます。VS Code: Reload Window）。

<a id="s2-2"></a>

### 2.2 OpenCode

`opencode.json` にローカル stdio MCP として追加します:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "wawoo-skills": {
      "type": "local",
      "command": ["python3", "/abs/path/to/wawoo-skills/mcp/server.py"],
      "enabled": true,
      "environment": {
        "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
        "WAWOO_MEMORY_READONLY": "1"
      }
    }
  }
}
```

- 一括設定: `python3 scripts/install_opencode.py`（既定は読み取り専用）。書き込み可にするには `--memory-writable` を指定します。
- OpenCode には**標準のスラッシュコマンド / スキル実行がありません**。MCP 経由で実行する必要があります: `interpret_intent` → `workflow_get` → `skill_get`。

<a id="s2-3"></a>

### 2.3 Cursor

1. ディレクトリを開く（`AGENTS.md` と `.cursor/rules` を読みます）。
2. **Settings → MCP** で `wawoo-skills` を有効化（`.cursor/mcp.json`）。

```bash
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace   # MCP のみ（プロジェクトの mcp.json を上書き）
python3 scripts/install_cursor_global.py                                     # ユーザー階層 ~/.cursor（既存 mcp.json にマージ）
# memory_save を許可:
python3 scripts/install_cursor_global.py --memory-writable
python3 scripts/install_cursor_workspace.py --workspace /path/to/workspace --memory-writable
```

**Cursor の制限:**

- スラッシュコマンド（`/feature-delivery` など）は**動作しません**。
- **エージェント切替なし**（`@.kilo/agents/<role>.md` を参照し、手動でロールを適用してください）。
- **`SKILL.md` の自動検出 / 自動実行なし**。

**MCP がないときの代替**: `@.kilo/CAPABILITIES.md` から候補を選び → `@.kilo/skills/<name>/SKILL.md` を読む → 手順を実行。ワークフローは `@.kilo/commands/<name>.md` を読みます。

<a id="s2-4"></a>

### 2.4 Paseo（OpenCode 内蔵、他とは別物）

Paseo は **マルチエージェント IDE** で、OpenCode を内蔵し、エージェントを独自の **daemon**（バックグラウンドサービス）で動作させます:

- **設定**: **同じ** `~/.config/opencode/opencode.json` を使います（`wawoo-skills` の MCP はここに接続）。インストールは `python3 scripts/install_opencode.py`。
- **事前のログイン**: Paseo が `kilo` / `cursor` を起動する前に、各 CLI でログインしてください（Kilo は `kilo auth login`）。ログインしないと起動しません。
- **再起動のルール**: 環境変数や MCP を変更したら
  ```bash
  paseo daemon stop && paseo daemon start     # 完全に切り替える
  # または: paseo daemon restart              # worker だけ再起動
  ```
  **daemon を再起動すると、それが起動したセッションも一緒に再起動します。**
- **独立プロセス**: VS Code の Kilo 拡張、Cursor デスクトップ、自分のターミナルの opencode/kilo/cursor は **daemon の影響を受けません**。
- **プラグインは別物**: Paseo 自身のプラグインスキル（`npx skills add getpaseo/paseo`）は本キットと無関係です。MCP と daemon を合わせれば併用できます。

<a id="s2-5"></a>

### 2.5 Codex（OpenAI Codex CLI / 拡張）

Codex は `AGENTS.md` を読み、スキルをロードし、MCP に対応します（`~/.codex/config.toml`）。本キットを stdio MCP として追加:

```toml
[mcp_servers.wawoo-skills]
command = "python3"
args = ["/abs/path/to/wawoo-skills/mcp/server.py"]
env = { WAWOO_SKILLS_ROOT = "/abs/path/to/wawoo-skills", WAWOO_MEMORY_READONLY = "1" }
```

- スキルディレクトリは `.agents/skills/` を指します（`.kilo/skills/` の内容を置く場合）。
- Codex は現在**手動設定**が必要で、本リポジトリに一括スクリプトはありません。Codex は `/skills`、`$skill` 呼び出しと MCP（`codex mcp add ...`）に対応します。

<a id="s2-6"></a>

### 2.6 Claude Code（Anthropic CLI）

Claude Code は MCP、`CLAUDE.md`、`.claude/skills/`、`.claude/commands/`（標準のスラッシュコマンド）に対応します。

```bash
claude mcp add wawoo-skills \
  --env WAWOO_SKILLS_ROOT=/abs/path/to/wawoo-skills \
  --env WAWOO_MEMORY_READONLY=1 \
  -- python3 /abs/path/to/wawoo-skills/mcp/server.py
```

- **スキル**: `.kilo/skills` を `.claude/skills` にコピーまたはシンボリックリンクします。
- **ワークフロー**: `.kilo/commands/*.md` を `.claude/commands/` にコピーします（標準のスラッシュコマンド）。
- **契約**: `AGENTS.md` と `CLAUDE.md` は**どちらか一方**を使用してください。両方作成しないでください。
- **サブエージェント**: `Agent`（`subagent_type`）を使用します。`swarm` / `reflect` は並列で動作します。

> **Pi などの他の MCP クライアント**: stdio MCP に対応していれば、同じ `python3 mcp/server.py` で接続できます。スキルディレクトリはクライアントの規則（例: `.pi/skills/`）に従います。サブエージェント拡張があれば `swarm` / `reflect` は並列、なければ順次実行（どちらも対応）。

<a id="s3"></a>

## 3. MCP サービス

本キットの機能は**ローカル MCP サービス**として公開されます（stdio: ローカルプロセス間通信、クライアントが自動起動、ポート不要）。

```bash
python3 mcp/server.py          # 通常はクライアントが起動
python3 scripts/e2e_flows.py   # 契約 / E2E スモーク
```

よく使うツール: `capabilities`、`skill_search`、`skill_get`、`workflow_get`、`agent_get`、`memory_recall`、`memory_save`。意図ルーティング: `interpret_intent` → `workflow_get` → … → `workflow_clear`。サブタスク: `delegate_subtask`。

<a id="s4"></a>

## 4. メモリ設定

### 4.1 ツールの役割

| MCP ツール | 役割 |
|---|---|
| `memory_recall` | `docs/memory/`（INDEX + トピックファイル）から過去の決定を読み込みます。**読み取り専用モードでも使えます。** |
| `memory_save` | 決定を追記します（INDEX + トピックファイル、テンプレート `docs/memory/TEMPLATE.md`）。**`WAWOO_MEMORY_READONLY=1` では拒否されます**。秘密情報は常に拒否されます。 |

メモリの**唯一の信頼できる情報源**は `<kit>/docs/memory/` の Markdown です。クライアント内蔵メモリと衝突する場合は**ファイルを優先**します（`docs/memory/MEMORY-TOOLS.md` 参照）。

### 4.2 `WAWOO_MEMORY_READONLY`（読み取り専用 / 書き込み可）

| 値 | 効果 | いつ使うか |
|---|---|---|
| **`1`**（インストール既定） | **読み取り専用**: `memory_save` はエラー、`memory_recall` は通常どおり | 任意のプロジェクトに MCP を登録する場合、監査 / コンプライアンスのセッション、エージェントにキットへ書かせたくない場合 |
| **`0`** | **読み書き可**: `WAWOO_SKILLS_ROOT/docs/memory/` へ書き込みを許可 | キットのリポジトリ、または同じ `docs/memory/` 構成のワークスペースで日常的に使う場合 |

MCP サービスは**起動時**にクライアント設定の環境変数を読み込みます — **ファイルを変えるだけでは不十分で、クライアントの再起動が必要**です（Kilo Reload、Cursor Reload、OpenCode 再起動、Paseo 内蔵 OpenCode は `paseo daemon restart`）。

### 4.3 クライアント別の設定場所

| クライアント | 設定ファイル | 推奨コマンド（再実行可能） |
|---|---|---|
| Kilo（グローバル） | `~/.config/kilo/kilo.jsonc` → `mcp.wawoo-skills.environment` | `python3 scripts/install_global.py`（既定 `1`）または `--memory-writable`（`0`） |
| OpenCode（ターミナルまたは **Paseo 内蔵**） | `~/.config/opencode/opencode.json` → `mcp.wawoo-skills.environment` | `python3 scripts/install_opencode.py` または `--memory-writable` |
| Cursor（ユーザー） | `~/.cursor/mcp.json` → `mcpServers.wawoo-skills.env` | `python3 scripts/install_cursor_global.py`（他の MCP をマージ）+ `--memory-writable` |
| Cursor（プロジェクト） | `<workspace>/.cursor/mcp.json` | `install_cursor_workspace.py --workspace <root>` + `--memory-writable`（上書き、手動マージが必要） |

**手動設定用のスニペット**（どのクライアントでも、パスだけ変更）:

```json
"environment": {
  "WAWOO_SKILLS_ROOT": "/abs/path/to/wawoo-skills",
  "WAWOO_MEMORY_READONLY": "0"
}
```

任意: `WAWOO_MEMORY_ROOT` でディレクトリを変更（既定 `<kit>/docs/memory`）。

### 4.4 確認方法

```bash
grep -A2 WAWOO_MEMORY_READONLY ~/.config/kilo/kilo.jsonc
grep -A2 WAWOO_MEMORY_READONLY ~/.config/opencode/opencode.json
grep -A2 WAWOO_MEMORY_READONLY ~/.cursor/mcp.json
```

そのあと**クライアントを再起動**し、テストセッションで `memory_save` を一度呼んで確認します。

### 4.5 ワークフロー側の制限

`READONLY=0` でも、一部のワークフローは `memory_save` を**禁止**します（例: `/compliance-review`）。

### 4.6 他のプロジェクトで使う

`docs/memory/INDEX.example.md` を `docs/memory/INDEX.md` にコピーすれば、同じメモリの仕組みを使えます。

<a id="s5"></a>

## 5. 呼び出し順（MCP ツールチェーン）

1. **ワークフロー**を選ぶ（入口）。迷ったら MCP `interpret_intent`。
2. **カタログ / MCP** で候補を選ぶ（全部読まない）。
3. 必要な **skill** だけ開く。
4. ワークフローの**出力形式とゲート**（承認・証拠）に従って実行。
5. 着手前に `memory_recall`、決定したら `memory_save`。

> **基本構造は固定ですが、各手順は状況に応じて調整可能です。** 不要な段階は飛ばし、順序が違えば並べ替え、優先度が変われば調整、方向が違えば範囲変更や中止、互いに独立したサブタスクは同時に進められます。この調整はシステムが証拠に基づいて**自動**で行います。いつでも介入できますが、手作業で組み立てる必要はありません。

<a id="s5-1"></a>

### 5.1 よくある場面: ひとことで、どのワークフロー

| やりたいこと | ひとこと | 動くもの |
|---|---|---|
| バグを直す | 「このバグを直して」 | `/self-review`: まず再現、修正、証拠つきで完了 |
| 小さな機能を足す | 「設定画面を足して」 | `/delivery-lite`: 計画 → 実装 → 検証、`ACTIVE.md` に記録 |
| ブランチをレビュー | 「このブランチをレビューして」 | `/self-review`: 標準と仕様の二軸で並行レビュー |
| リリース準備 | 「リリース準備をして」 | `/release-review`: 法務 / プライバシー / 版 / セキュリティの読み取り専用ゲート |
| 調べてから判断 | 「X を調べて結論を出して」 | `/research`: 調査 → プロダクト発見 → 仕様化 |
| ページを作り直す | 「トップページを作り直して」 | `/ui-delivery`: 設計 → 実装 → アクセシビリティ確認 |
| 障害対応 | 「本番でエラーが出てる」 | `/incident-response`: まず証拠 → 緩和 → 振り返り |

<a id="s6"></a>

## 6. 保守と検証

```bash
python3 scripts/validate_assets.py    # 資産の検証（name=dir、参照、重複、JSON）
python3 scripts/gen_capabilities.py   # 能力一覧を再生成（手動で編集しない）
python3 scripts/e2e_flows.py          # MCP 契約 / E2E スモーク
```

<a id="s7"></a>

## 7. 注意事項（依存 / キー / 制限）

- **issue tracker が必要なスキル**: `to-spec`、`to-tickets`、`triage` は先に設定（GitHub Issues など）し、`setup-matt-pocock-skills` を一度実行してください。
- **画像生成**: `imagegen-frontend-mobile` はプロンプトのみを生成します。実画像は `fal-gen`（`FAL_KEY`）または `openrouter-gen`（`OPENROUTER_API_KEY`）を使用します。
- **Cursor** の制限は §2.3 を参照してください。

> [!WARNING]
> **キーをコミットしない**: API キー / トークン / `.env` をリポジトリにコミットしないでください。`memory_save` は秘密情報を拒否します。

<a id="s8"></a>

## 8. トラブルシューティング（FAQ）

| 症状 | 対応 |
|---|---|
| `memory_save` がエラー（readonly の言及） | `WAWOO_MEMORY_READONLY` を `0` にして**クライアントを再起動**（§4.2） |
| 設定を変えたのに MCP が変わらない | クライアントを再起動してください。Paseo は `paseo daemon stop && paseo daemon start` を実行します。 |
| `python3` が見つからない / 名前が違う | 各設定の `command` を実際のコマンド（`python` / `py`）に |
| Kilo のルーティング説明が効かない | `instructions` は**絶対パス**である必要あり（§2.1） |
| インストール確認 | `python3 scripts/validate_assets.py` で `OK` |

<a id="s9"></a>

## 9. 設定一覧（環境変数と設定）

先に結論: **ほとんどの場合、2 つの設定のみで十分です**すれば十分です — `WAWOO_SKILLS_ROOT`（キットのパス）と `WAWOO_MEMORY_READONLY`（メモリを書き込み可にするか）。

### 9.1 コア（ほぼ必須）

| 変数 | 役割 | 既定 | 設定方法 |
|---|---|---|---|
| `WAWOO_SKILLS_ROOT` | キットのルートの絶対パス | `server.py` の 2 階層上 | クライアント MCP の `environment` / `env`。一括スクリプトが自動で書き込み |
| `WAWOO_MEMORY_READONLY` | `1`=読み取り専用（保存不可）、`0`=書き込み可 | インストールスクリプトは既定 `1` | `install_*.py --memory-writable`、または設定を手動で編集（[§4](#s4)） |
| `WAWOO_MEMORY_ROOT` | メモリのディレクトリ | `<kit>/docs/memory` | 別の場所に置くときに設定 |

### 9.2 作業言語（3 層ポリシー）

既定: **コード = 英語、エンジニアリング記録と応答 = プロジェクトの作業言語（本キット = 日本語）、説明文書 = 英語主体 + 日本語副**。

**変更方法（プロジェクトごとに 1 回）:**

1. `AGENTS.md` §1（マスター定義）を変更;
2. `.kilo/skills/language-policy/SKILL.md` の「(wawoo-skills: Japanese)」2 か所を同期;
3. ルーティング説明を再生成: `python3 scripts/gen_router.py`;
4. この文書の言語説明も合わせる。

> 「文書全体をどの言語にするか」を変える場合は、`README.<lang>.md` / `docs/USAGE.<lang>.md` をその言語で用意します（本キットは `en / ja / zh-CN / ko`）。

### 9.3 画像生成

実際に画像を生成するにはキーを設定します。`imagegen-frontend-mobile` はプロンプトだけを書き、モデルは呼び出しません。

| 機能 | 必要なキー | 置き場所 | 説明 |
|---|---|---|---|
| `fal-gen`（実画像、fal.ai） | `FAL_KEY`（形式 `key_id:secret`） | `.kilo/skills/fal-gen/.env`（`.env.example` をコピー） | **コミット・表示しない**。既定は最安モデル `flux/schnell` |
| `openrouter-gen`（実画像、OpenRouter） | `OPENROUTER_API_KEY`（形式 `sk-or-v1-...`） | `.kilo/skills/openrouter-gen/.env`（`.env.example` をコピー） | 既定 `google/gemini-2.5-flash-image`。`OPENROUTER_IMAGE_MODEL` で変更、より安価な `google/gemini-3.1-flash-lite-image` も可 |
| `imagegen-frontend-mobile` | 不要 | — | **プロンプトのみ**、モデル呼び出しなし |

- 任意: `FAL_BASE_URL` で fal.ai のエンドポイントを指定。
- 2 つの画像スキルは**マニフェスト**で一括生成し、既存ファイルは自動でスキップ（再実行安全）。まず `--dry-run` で確認し、それから生成（画像生成は費用がかかります）。

> [!WARNING]
> **キーをリポジトリに書かない**（`.env` もコミットしない）。キーはローカルの `.env` だけに置き、`.gitignore` で無視されていることを確認してください（本リポジトリは `.env` / `.env.*` を無視し、`.env.example` のみ残します）。

### 9.4 Google Modern Web Guidance

**何か**: Google がまとめた「現代の Web の作り方」オンラインガイド（約 262 本）。

**何を解決するか**: AI の知識は古くなります。Web を作るとき、最新の書き方を必要に応じて取得でき、古くなった書き方も見つけられます。

**使い方**: ひとこと伝えるだけ。エージェントが `modern-web-guidance-bridge` で検索（`mwg_search`）し、取得（`mwg_retrieve`）します。ガイドはリポジトリにコピーしません。

**前提**: Node.js とネットワークが必要。オフラインなら `WAWOO_MWG_DISABLE=1` で無効化。

**既存の基準と衝突するとき**: プロダクト基準 / Vercel を優先。

### 9.5 意図ルーティング（上級、通常は変更不要）

`interpret_intent` が「ワークフローの自動選択」を担います。以下はそのマッチングの細部にだけ影響し、**通常は変更不要**です。

| 変数 | 役割 | 既定 |
|---|---|---|
| `WAWOO_INTENT_LEARN_DB` | 学習済みトリガーの保存先 | `data/intent_learned.db` |
| `WAWOO_INTENT_SESSION` | セッションゲートの状態ファイル | `<root>/data/intent_session.json` |
| `WAWOO_INTENT_RESUME` | `1` で再起動後にゲートを復元 | オフ |
| `WAWOO_INTENT_CLIENT` | クライアント別ファイル、ゲートの衝突を防ぐ | 空 |
| `WAWOO_INTENT_SOCKET` | 常駐 `intent_receiver.py` のソケット | 空 |
| `WAWOO_INTENT_LEXICAL` / `_THRESHOLD` / `_MARGIN` / `_MIN_TOKENS` / `_MAX_ABSTAIN` / `_DEBUG` | 語彙ルーティングのスイッチ・しきい値・デバッグ | `mcp/README.md` 参照 |

### 9.6 インストールと CI

インストールと CI にだけ影響し、日常利用には影響しません。

| 変数 / 引数 | 役割 |
|---|---|
| `KILO_GLOBAL_DIR` | `install_global.py` の出力先（既定 `~/.config/kilo`） |
| `CURSOR_API_KEY` | Cursor CLI の**自動化された CI 環境** 専用（ローカルは通常 `agent login`） |

### 9.7 文書レビュースクリプト（任意）

任意。レビュースクリプト専用で、メインの流れには関与しません。

`scripts/audit_docs_dual.py` / `scripts/openrouter_doc_audit.py` は OpenRouter で文書をレビューします:

- `OPENROUTER_API_KEY`（必須）
- `OPENROUTER_DOC_MODEL`（既定 `google/gemini-2.5-flash`）
- `OPENROUTER_QWEN_MODEL`（既定 `qwen/qwen3-30b-a3b`）

### 9.8 外部の前提

issue tracker が必要な 3 つのスキル: `to-spec`、`to-tickets`、`triage`（`scripts/readiness.json` 参照）。1 回設定: `setup-matt-pocock-skills`。

### 9.9 設定ファイルの対応表

クライアントごとの設定ファイルの場所。**変更後はクライアントを再起動**。

| クライアント / 用途 | ファイル |
|---|---|
| Kilo | `~/.config/kilo/kilo.jsonc`（プロジェクト内 `kilo.json`） |
| Cursor（ユーザー / プロジェクト） | `~/.cursor/mcp.json` / `<workspace>/.cursor/mcp.json` |
| OpenCode / Paseo | `~/.config/opencode/opencode.json` |
| Codex | `~/.codex/config.toml` |
| 画像キー | `.kilo/skills/fal-gen/.env`、`.kilo/skills/openrouter-gen/.env`（**コミット禁止**） |
