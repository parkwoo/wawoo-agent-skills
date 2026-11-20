# インストール — OpenCode

公式: [opencode.ai](https://opencode.ai)。**Paseo 内蔵 OpenCode** も同じ設定。

## 一発インストール

```bash
python3 scripts/install_opencode.py
python3 scripts/install_opencode.py --memory-writable
```

`~/.config/opencode/opencode.json` にローカル MCP を書き込む。

スラッシュ workflow は非対応 — **`interpret_intent` → `workflow_get` → `skill_get`**。

環境変数変更後は OpenCode 再起動 / `paseo daemon restart`。

詳細: [USAGE §2.5](../USAGE.ja.md)