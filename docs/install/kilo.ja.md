# インストール — Kilo

公式: [kilo.ai](https://kilo.ai) · Kilo Code 拡張。

## プロジェクト

キットディレクトリを開く — `.kilo/` と `kilo.json` を自動検出（MCP オン）。

Workflow: `/feature-delivery`・`/delivery-lite` 等。

## グローバル（全プロジェクト）

```bash
python3 scripts/install_global.py --dry-run
python3 scripts/install_global.py
```

MCP に絶対パスの `python3` と `WAWOO_SKILLS_ROOT` を登録。`ROUTER.md` 生成・既定 agent **`wawoo-auto`**。

**Kilo 再起動 / Reload Window** が必要。

書込み: `python3 scripts/install_global.py --memory-writable`

詳細: [USAGE §2](../USAGE.ja.md)