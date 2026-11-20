# よくある質問

### 無料か？

はい。MIT。AI クライアントと API キーは各自。

### リポジトリに skill を置くのと何が違う？

開かれない skill は意味がない。**呼び出し**を設計する: intent → workflow → `skill_get`。

### 対応クライアントは？

**Cursor**・**Kilo**・**OpenCode**（Paseo 含む）。[インストール](../install/cursor.ja.md)

### MCP に pip は必要？

不要。**Python 3 標準ライブラリのみ**。

### Cursor で `/delivery-lite` が動かない

Kilo のスラッシュは非対応。MCP `workflow_get` または `@.kilo/commands/delivery-lite.md`。

### 進捗はどこに書く？

キット内 `docs/plans/ACTIVE.md`（チャットだけで完結しない）。

### 公式サイトは？

**https://skills.wawoo.jp**（デプロイ後）。リポジトリ: [github.com/parkwoo/wawoo-agent-skills](https://github.com/parkwoo/wawoo-agent-skills)。

他: [README.ja](https://github.com/parkwoo/wawoo-agent-skills/blob/master/README.ja.md) · [USAGE](../USAGE.ja.md)