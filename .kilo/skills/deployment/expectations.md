# deployment — expectations（uplift pilot）

Docker Compose / compose YAML の静的チェック。シークレットのコミット可否は別ゲート（本 checker は平文っぽい env の検出のみ）。

## Compose

- `[deploy-no-latest-tag]` `image:` に `:latest` を使わない（イミュータブルタグ推奨）
- `[deploy-plain-secret-env]` 環境変数値に `password`/`secret`/`api_key` らしき平文（`.env` 参照 `$$` / `${}` は除外）
- `[deploy-missing-healthcheck]` `ports` を公開するサービスに `healthcheck` ブロックが無い

## 対象ファイル

`docker-compose.yml`・`compose.yml` 等（`.yml`/`.yaml`）。`Dockerfile` 単体は P1.2 候補。

## 検証

```bash
python3 scripts/skill_uplift_check.py deployment --path <repo-or-compose-dir>
```